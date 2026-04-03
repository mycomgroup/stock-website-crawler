"""
财务类 API 模块（权威文件）

从 missing_apis.py 迁移的财务相关函数：
- get_locked_shares: 获取限售股解禁数据
- get_fund_info: 获取基金信息
- get_fundamentals_continuously: 连续获取基本面数据

数据源说明:
- 限售股解禁、基金信息为特殊数据，使用 akshare 作为数据源
- 采用延迟导入，避免顶层依赖耦合
"""

import pandas as pd
import warnings
from typing import Optional, List, Union, Dict
from datetime import datetime


def _get_akshare():
    """延迟导入 akshare，避免顶层依赖耦合"""
    try:
        import akshare as ak
        return ak
    except ImportError:
        warnings.warn("AkShare 未安装，部分财务 API 将不可用")
        return None


def get_locked_shares(
    stock_list: Optional[Union[str, List[str]]] = None,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    forward_count: int = 90,
) -> pd.DataFrame:
    """
    获取限售股解禁信息

    聚宽兼容接口

    参数:
        stock_list: 股票代码或股票列表，None 表示获取全部
        start_date: 开始日期，格式 'YYYY-MM-DD'
        end_date: 结束日期
        forward_count: 向前查找天数

    返回:
        DataFrame，包含解禁信息:
        - code: 股票代码
        - unlock_date: 解禁日期
        - unlock_shares: 解禁股数
        - unlock_ratio: 解禁比例
        - unlock_value: 解禁市值
    """
    ak = _get_akshare()
    if ak is None:
        return pd.DataFrame(
            columns=["code", "unlock_date", "unlock_shares", "unlock_ratio", "unlock_value"]
        )

    if isinstance(stock_list, str):
        securities = [stock_list]
    elif stock_list is None:
        securities = None
    else:
        securities = stock_list

    try:
        df = ak.stock_restricted_release_summary_em()

        if df is None or df.empty:
            return pd.DataFrame(
                columns=["code", "unlock_date", "unlock_shares", "unlock_ratio", "unlock_value"]
            )

        column_mapping = {
            "股票代码": "code",
            "解禁日期": "unlock_date",
            "解禁股数": "unlock_shares",
            "解禁市值": "unlock_value",
            "占流通股比例": "unlock_ratio",
        }
        df = df.rename(columns=column_mapping)

        if "code" in df.columns:
            df["code"] = df["code"].apply(lambda x: str(x).zfill(6))
            df["code"] = df["code"].apply(
                lambda x: f"{x}.XSHG" if x.startswith("6") else f"{x}.XSHE"
            )

        if "unlock_date" in df.columns:
            df["unlock_date"] = pd.to_datetime(df["unlock_date"], errors="coerce")
            if start_date:
                df = df[df["unlock_date"] >= pd.to_datetime(start_date)]
            if end_date:
                df = df[df["unlock_date"] <= pd.to_datetime(end_date)]

        if securities and "code" in df.columns:
            df = df[df["code"].isin(securities)]

        return df.reset_index(drop=True)

    except Exception as e:
        warnings.warn(f"获取限售股解禁数据失败: {e}")
        return pd.DataFrame(
            columns=["code", "unlock_date", "unlock_shares", "unlock_ratio", "unlock_value"]
        )


def get_fund_info(
    fund_code: str,
    fields: Optional[List[str]] = None,
) -> Dict:
    """
    获取基金基本信息

    聚宽兼容接口

    参数:
        fund_code: 基金代码
        fields: 需要获取的字段列表

    返回:
        Dict，包含基金信息
    """
    ak = _get_akshare()
    if ak is None:
        return {}

    try:
        df = ak.fund_name_em()

        if df is None or df.empty:
            return {}

        fund_row = df[df["基金代码"] == fund_code.zfill(6)]

        if fund_row.empty:
            return {}

        row = fund_row.iloc[0]

        result = {
            "fund_code": fund_code,
            "fund_name": row.get("基金简称", ""),
            "fund_type": row.get("基金类型", ""),
            "inception_date": row.get("成立日期", ""),
        }

        if fields:
            result = {k: v for k, v in result.items() if k in fields}

        return result

    except Exception as e:
        warnings.warn(f"获取基金信息失败 {fund_code}: {e}")
        return {}


def get_fundamentals_continuously(
    query_obj,
    start_date: str,
    end_date: Optional[str] = None,
    frequency: int = 1,
    count: Optional[int] = None,
    fields: Optional[List[str]] = None,
) -> pd.DataFrame:
    """
    连续获取财务数据

    聚宽兼容接口 - 获取时间序列的财务数据

    参数:
        query_obj: 查询对象
        start_date: 开始日期
        end_date: 结束日期
        frequency: 查询频率（天）
        count: 获取次数
        fields: 字段列表

    返回:
        DataFrame，包含时间序列财务数据
    """
    from jk2bt.finance_data import get_balance_sheet, get_income_statement

    table_name = None
    code = None

    if hasattr(query_obj, "__class__"):
        table_name = query_obj.__class__.__name__

    if hasattr(query_obj, "left"):
        if hasattr(query_obj.left, "__class__"):
            table_name = query_obj.left.__class__.__name__
        if hasattr(query_obj, "right"):
            code = str(query_obj.right)

    if end_date:
        dates = pd.date_range(start=start_date, end=end_date, freq=f"{frequency}D")
    elif count:
        dates = pd.date_range(start=start_date, periods=count, freq=f"{frequency}D")
    else:
        dates = pd.date_range(start=start_date, end=datetime.now(), freq=f"{frequency}D")

    results = []

    for date in dates:
        date_str = date.strftime("%Y-%m-%d")

        try:
            if table_name in ("indicator", "STK_INCOME_STATEMENT"):
                if code:
                    df = get_income_statement(code, end_date=date_str)
                    if not df.empty:
                        df["date"] = date_str
                        results.append(df)
            elif table_name == "STK_BALANCE_SHEET":
                if code:
                    df = get_balance_sheet(code, end_date=date_str)
                    if not df.empty:
                        df["date"] = date_str
                        results.append(df)
        except Exception:
            pass

    if not results:
        return pd.DataFrame()

    return pd.concat(results, ignore_index=True)


__all__ = [
    "get_locked_shares",
    "get_fund_info",
    "get_fundamentals_continuously",
]
