"""
securities_utils.py
证券代码工具函数、指数常量定义、格式化函数。

提供聚宽风格的证券代码转换和验证功能。
"""

import os
import re
import warnings
import pandas as pd
from datetime import datetime

# 项目根目录和缓存目录
_PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
_CACHE_BASE_DIR = os.path.join(_PROJECT_ROOT, "cache")

# 日期列候选名称
_DATE_COLUMN_CANDIDATES = {
    "market": ["日期", "date", "trade_date", "trading_date"],
    "financial": [
        "报告期",
        "报告日期",
        "报告日",
        "报表日期",
        "STATEMENT_DATE",
        "date",
        "report_date",
    ],
}


def _find_date_column(df: pd.DataFrame, category: str = "market") -> str:
    """动态检测 DataFrame 中的日期列名。

    Parameters
    ----------
    df : pd.DataFrame
    category : str, 'market' 或 'financial'

    Returns
    -------
    str : 日期列名，若找不到则返回 None
    """
    candidates = _DATE_COLUMN_CANDIDATES.get(
        category, _DATE_COLUMN_CANDIDATES["market"]
    )
    for col in candidates:
        if col in df.columns:
            return col
    return None


def _resolve_cache_dir(cache_dir: str) -> str:
    """解析缓存目录路径，支持相对路径和绝对路径"""
    if os.path.isabs(cache_dir):
        return cache_dir
    return os.path.join(_CACHE_BASE_DIR, cache_dir)


# =====================================================================
# 股票代码工具函数
# =====================================================================


def format_stock_symbol_for_akshare(symbol):
    """
    将各种格式的股票代码统一转为 6 位纯数字字符串，供 AkShare 使用。
    支持: sh600000 / sz000001 / 600000.XSHG / 000001.XSHE / 600000 / 000001
    """
    if symbol.startswith("sh") or symbol.startswith("sz"):
        symbol = symbol[2:]
    if symbol.endswith(".XSHG") or symbol.endswith(".XSHE"):
        symbol = symbol[:6]
    return symbol.zfill(6)


def jq_code_to_ak(code):
    """
    聚宽代码格式 → 带前缀的本地格式。
    600519.XSHG → sh600519
    000001.XSHE → sz000001
    sh600519    → sh600519（不变）
    """
    if code.endswith(".XSHG"):
        return "sh" + code[:6]
    elif code.endswith(".XSHE"):
        return "sz" + code[:6]
    elif code.startswith("sh") or code.startswith("sz"):
        return code
    else:
        # 纯 6 位数字，按首位判断
        c = code.zfill(6)
        if c.startswith("6"):
            return "sh" + c
        else:
            return "sz" + c


def ak_code_to_jq(code):
    """
    带前缀本地格式 → 聚宽格式。
    sh600519 → 600519.XSHG
    sz000001 → 000001.XSHE
    """
    if code.startswith("sh"):
        return code[2:] + ".XSHG"
    elif code.startswith("sz"):
        return code[2:] + ".XSHE"
    return code


def _stock_code_to_jq(code):
    """将股票代码转换为聚宽格式"""
    code = str(code).strip()
    if code.startswith("6"):
        return code + ".XSHG"
    else:
        return code + ".XSHE"


# =====================================================================
# 指数相关常量
# =====================================================================


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
    "399101": "深证100",
    "399303": "国证2000",
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

# 需要使用 ak.index_stock_cons 而非 ak.index_stock_cons_weight_csindex 的指数
CONS_ONLY_INDICES = {"399101", "399303", "399006", "399001"}

# 指数替代映射 - 当某个指数数据不可用时，使用替代指数
INDEX_FALLBACK_MAP = {
    "399101": "000903",  # 深证100 -> 中证100 (相似的大盘风格)
    "399303": "000852",  # 国证2000 -> 中证1000 (相似的小盘风格)
    "399006": "399006",  # 创业板指 (通常可用)
    "399001": "399001",  # 深证成指 (通常可用)
}

# 指数说明 - 用于日志和用户提示
INDEX_DESCRIPTION = {
    "399101": "深证100 - 深圳市场规模大、流动性好的100只股票，可替代为沪深300或中证100",
    "399303": "国证2000 - A股小市值公司，可替代为中证1000",
    "399006": "创业板指 - 创业板最具代表性的100只股票",
    "399001": "深证成指 - 深圳市场核心指数",
}

# 指数代码别名映射
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
    "000300.xshe": "000300",
    "000016.xshe": "000016",
    "000905.xshe": "000905",
    "000852.xshe": "000852",
    "000903.xshe": "000903",
    "000922.xshe": "000922",
    "399005.xshe": "399005",
    "399102.xshe": "399102",
    "399107.xshe": "399107",
    "399311.xshe": "399311",
    "399303.xshe": "399303",
    "399101.xshe": "399101",
    "sz100": "399101",
    "深证100": "399101",
    "gj2000": "399303",
    "国证2000": "399303",
    "zz100": "000903",
    "中证100": "000903",
    "zzhl": "000922",
    "中证红利": "000922",
    "cyb100": "399006",
    "创业板指": "399006",
    "gza": "399317",
    "国证a指": "399317",
    "zqxx": "000993",
    "全指信息": "000993",
    "zqyy": "000991",
    "全指医药": "000991",
    "zqjr": "000992",
    "全指金融": "000992",
    "zgcm": "399971",
    "中证传媒": "399971",
    "zgxf": "399932",
    "中证消费": "399932",
    "gzdc": "399393",
    "国证地产": "399393",
    "jgzs": "000959",
    "军工指数": "000959",
}


def _format_index_code(index_code):
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


def _normalize_index_weights(df):
    """标准化指数权重DataFrame"""
    result = pd.DataFrame()

    col_mapping = {
        "成分券代码": ["成分券代码", "证券代码", "股票代码", "code"],
        "权重": ["权重", "weight", "W", "w"],
        "证券名称": ["证券名称", "股票名称", "name", "display_name"],
        "行业代码": ["行业代码", "industry_code", "CITICS行业代码"],
    }

    for target_col, source_cols in col_mapping.items():
        for src_col in source_cols:
            if src_col in df.columns:
                result[target_col] = df[src_col]
                break

    if "成分券代码" in result.columns:
        result["code"] = result["成分券代码"].apply(lambda x: _stock_code_to_jq(x))
        result = result.set_index("code")

    if "权重" in result.columns:
        result["weight"] = result["权重"].astype(float)
    elif "W" in result.columns:
        result["weight"] = result["W"].astype(float)

    return result


# =====================================================================
# RobustResult - 稳健结果封装类
# =====================================================================


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