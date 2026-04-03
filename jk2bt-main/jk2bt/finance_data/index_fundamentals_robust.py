"""
index_fundamentals_robust.py

指数与基本面接口稳健性增强模块。

提供 RobustResult 封装类和稳健版 API：
- get_index_weights_robust
- get_index_stocks_robust
- get_fundamentals_robust
- get_history_fundamentals_robust

核心改进：
1. 不轻易返回 None/空结果
2. 空结果带原因说明
3. 支持多种指数代码格式
4. 统一的 query/entity/security 参数处理
"""

import warnings
import pandas as pd
from datetime import datetime
import os
import re
import logging

logger = logging.getLogger(__name__)


SUPPORTED_INDEXES = {
    "000300": "沪深300",
    "000016": "上证50",
    "000905": "中证500",
    "000852": "中证1000",
    "000903": "中证100",
    "000922": "中证红利",
    "000925": "基本面50",
    "000001": "上证指数",
    "399001": "深证成指",
    "399006": "创业板指",
    "000985": "中证全指",
    "399317": "国证A指",
    "000993": "全指信息",
    "000991": "全指医药",
    "399971": "中证传媒",
    "000992": "全指金融",
    "399932": "中证主要消费",
    "399393": "国证地产",
    "000959": "军工指数",
}

INDEX_CODE_ALIAS_MAP = {
    "sh000300": "000300",
    "sz399001": "399001",
    "sz399006": "399006",
    "000300.xshg": "000300",
    "399001.xshe": "399001",
    "399006.xshe": "399006",
    "hs300": "000300",
    "沪深300": "000300",
    "sz50": "000016",
    "上证50": "000016",
    "zz500": "000905",
    "中证500": "000905",
    "zz1000": "000852",
    "中证1000": "000852",
    "cyb": "399006",
    "创业板": "399006",
    "上证指数": "000001",
    "深证成指": "399001",
}


class RobustResult:
    """
    稳健结果封装类，用于统一处理API返回结果。

    属性:
        success: bool - 是否成功获取数据
        data: Any - 返回的数据（DataFrame/list等）
        reason: str - 失败原因或成功说明
        source: str - 数据来源（'cache'/'network'/'fallback'）

    用法:
        result = get_index_stocks_robust('000300.XSHG')
        if result.success:
            stocks = result.data
        else:
            log.warn(f"获取失败: {result.reason}")
    """

    def __init__(self, success=True, data=None, reason="", source="network"):
        self.success = success
        self.data = data if data is not None else pd.DataFrame()
        self.reason = reason
        self.source = source

    def __bool__(self):
        return self.success

    def __repr__(self):
        status = "SUCCESS" if self.success else "FAILED"
        return f"<RobustResult[{status}] source={self.source} reason='{self.reason}' data_type={type(self.data).__name__}>"

    def is_empty(self):
        if isinstance(self.data, pd.DataFrame):
            return self.data.empty
        elif isinstance(self.data, (list, tuple)):
            return len(self.data) == 0
        return self.data is None


def format_index_code(index_code):
    """格式化指数代码为6位数字，支持多种格式别名"""
    code = str(index_code).lower().strip()
    if code in INDEX_CODE_ALIAS_MAP:
        code = INDEX_CODE_ALIAS_MAP[code]
    code = code.replace(".xshg", "").replace(".xshe", "")
    code = code.replace("sh", "").replace("sz", "")
    code = code.zfill(6)
    if code.startswith("399") and len(code) == 6:
        return code
    return code


def get_supported_indexes():
    """获取支持的指数列表"""
    return dict(SUPPORTED_INDEXES)


def normalize_security_param(security, entity=None):
    """
    标准化 security/entity 参数。

    参数:
        security: 股票代码
        entity: security 的别名（聚宽风格）

    返回:
        list: 标准化后的股票代码列表
    """
    if entity is not None:
        security = entity

    if security is None:
        return []

    if isinstance(security, str):
        return [security]

    return list(security)


def normalize_fields_param(fields):
    """
    标准化 fields 参数。

    参数:
        fields: 字段列表，可以是字符串列表或字段代理对象列表

    返回:
        list: 标准化后的字段名列表
    """
    if fields is None:
        return []

    if isinstance(fields, str):
        return [fields]

    if hasattr(fields, "__iter__"):
        field_names = []
        for f in fields:
            if hasattr(f, "_field"):
                table = getattr(f, "_table", "")
                if table:
                    field_names.append(f"{table}.{f._field}")
                else:
                    field_names.append(f._field)
            elif isinstance(f, str):
                field_names.append(f)
        return field_names

    return []


_FUNDAMENTALS_SCHEMA = {
    "valuation": [
        "code",
        "pe_ratio",
        "pb_ratio",
        "ps_ratio",
        "market_cap",
        "circulating_market_cap",
        "dividend_ratio",
    ],
    "income": ["code", "statDate", "营业收入", "营业成本", "净利润", "营业利润"],
    "balance": [
        "code",
        "statDate",
        "资产总计",
        "负债合计",
        "所有者权益合计",
        "应收账款",
        "应付账款",
    ],
    "cash_flow": ["code", "statDate", "货币资金", "净利润", "投资收益", "营业利润"],
}

_HISTORY_FUNDAMENTALS_SCHEMA = ["code", "statDate"]


def get_schema_columns(table_name):
    """获取表的默认 schema 列"""
    return _FUNDAMENTALS_SCHEMA.get(table_name, ["code"])


def create_empty_result(schema_cols, reason="", success=False, source="fallback"):
    """创建带 schema 的空结果"""
    empty_df = pd.DataFrame(columns=schema_cols)
    return RobustResult(success=success, data=empty_df, reason=reason, source=source)


def wrap_fundamentals_result(df, table_name, symbols, robust=False, errors=None):
    """
    封装基本面查询结果。

    参数:
        df: 查询结果 DataFrame
        table_name: 表名
        symbols: 股票代码列表
        robust: 是否返回 RobustResult
        errors: 错误列表

    返回:
        DataFrame 或 RobustResult
    """
    schema_cols = get_schema_columns(table_name) if table_name else ["code"]

    if df is None or (isinstance(df, pd.DataFrame) and df.empty):
        reason = f"查询返回空数据 (表: {table_name}, 股票数: {len(symbols) if symbols else 0})"
        if errors:
            reason += f", 错误: {errors[:3]}"
        empty_df = pd.DataFrame(columns=schema_cols)
        if robust:
            return RobustResult(
                success=False, data=empty_df, reason=reason, source="network"
            )
        return empty_df

    for col in schema_cols:
        if col not in df.columns:
            df[col] = None

    reason = f"成功获取 {len(df)} 条记录 (表: {table_name})"
    if errors:
        reason += f", 部分: {len(errors)} 个错误"

    if robust:
        return RobustResult(success=True, data=df, reason=reason, source="network")
    return df


def check_index_supported(index_code):
    """
    检查指数代码是否支持。

    返回:
        tuple: (is_supported: bool, normalized_code: str, message: str)
    """
    normalized = format_index_code(index_code)

    if normalized in SUPPORTED_INDEXES:
        return (
            True,
            normalized,
            f"指数 '{index_code}' -> '{normalized}' ({SUPPORTED_INDEXES[normalized]})",
        )

    return (
        False,
        normalized,
        f"指数代码 '{index_code}' 不在支持列表中 (标准化为 '{normalized}'). 支持的指数: {list(SUPPORTED_INDEXES.keys())[:10]}...",
    )
