"""
market_data/money_flow.py
个股资金流数据模块，使用 AkShare 获取个股资金流向数据。

功能:
- 个股资金流（日度）
- 支持股票列表批量查询
- 支持日期区间和 count 参数
"""

import warnings
from typing import Optional, List, Union
import pandas as pd
from datetime import datetime, timedelta

try:
    import akshare as ak

    AKSHARE_AVAILABLE = True
except ImportError:
    AKSHARE_AVAILABLE = False
    warnings.warn("akshare未安装，资金流数据将不可用")


COLUMN_MAP = {
    "日期": "date",
    "收盘价": "close",
    "涨跌幅": "change_pct",
    "主力净流入-净额": "net_amount_main",
    "主力净流入-净占比": "net_pct_main",
    "超大单净流入-净额": "net_amount_xl",
    "超大单净流入-净占比": "net_pct_xl",
    "大单净流入-净额": "net_amount_l",
    "大单净流入-净占比": "net_pct_l",
    "中单净流入-净额": "net_amount_m",
    "中单净流入-净占比": "net_pct_m",
    "小单净流入-净额": "net_amount_s",
    "小单净流入-净占比": "net_pct_s",
}

ALL_FIELDS = list(COLUMN_MAP.values())

DEFAULT_SCHEMA = ["sec_code", "date", "close", "change_pct"] + [
    "net_amount_main",
    "net_pct_main",
    "net_amount_xl",
    "net_pct_xl",
    "net_amount_l",
    "net_pct_l",
    "net_amount_m",
    "net_pct_m",
    "net_amount_s",
    "net_pct_s",
]


def _get_empty_dataframe(fields: Optional[List[str]] = None) -> pd.DataFrame:
    """
    返回带稳定列名的空 DataFrame。

    参数
    ----
    fields : list, optional
        需要的字段列表，默认返回全部字段

    返回
    ----
    pd.DataFrame
        带 schema 的空 DataFrame
    """
    if fields is None:
        columns = DEFAULT_SCHEMA
    else:
        columns = [f for f in DEFAULT_SCHEMA if f in fields]
        if "sec_code" not in columns:
            columns = ["sec_code"] + columns
        if "date" not in columns and len(columns) > 0:
            columns = ["date"] + columns

    return pd.DataFrame(columns=columns)


def _normalize_symbol(symbol: str) -> tuple:
    """
    标准化股票代码，返回 (code, market) 元组。

    参数
    ----
    symbol : str
        股票代码，支持多种格式：'sh600000', '600000.XSHG', '600000'

    返回
    ----
    tuple : (code, market)
        code: 6位股票代码
        market: 'sh' 或 'sz' 或 'bj'
    """
    symbol = str(symbol).strip()

    if ".XSHG" in symbol:
        code = symbol.replace(".XSHG", "").replace("sh", "")
        market = "sh"
    elif ".XSHE" in symbol:
        code = symbol.replace(".XSHE", "").replace("sz", "")
        market = "sz"
    elif symbol.startswith("sh"):
        code = symbol[2:]
        market = "sh"
    elif symbol.startswith("sz"):
        code = symbol[2:]
        market = "sz"
    elif symbol.startswith("bj"):
        code = symbol[2:]
        market = "bj"
    else:
        code = symbol
        if code.startswith("6"):
            market = "sh"
        elif code.startswith(("0", "3")):
            market = "sz"
        elif code.startswith(("4", "8")):
            market = "bj"
        else:
            market = "sh"

    return code.zfill(6), market


def _get_single_stock_flow(
    symbol: str,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    count: Optional[int] = None,
    fields: Optional[List[str]] = None,
) -> pd.DataFrame:
    """
    获取单只股票的资金流数据。

    参数
    ----
    symbol : str
        股票代码
    start_date : str, optional
        开始日期 'YYYY-MM-DD'
    end_date : str, optional
        结束日期 'YYYY-MM-DD'
    count : int, optional
        返回最近N天的数据
    fields : list, optional
        需要返回的字段

    返回
    ----
    pd.DataFrame
        资金流数据，失败时返回带 schema 的空表
    """
    code, market = _normalize_symbol(symbol)
    sec_code = f"{market}{code}"

    if not AKSHARE_AVAILABLE:
        return _get_empty_dataframe(fields)

    try:
        df = ak.stock_individual_fund_flow(stock=code, market=market)

        if df is None or df.empty:
            return _get_empty_dataframe(fields)

        df = df.rename(columns=COLUMN_MAP)

        if "date" in df.columns:
            df["date"] = pd.to_datetime(df["date"])

        df["sec_code"] = sec_code

        if start_date:
            df = df[df["date"] >= pd.to_datetime(start_date)]
        if end_date:
            df = df[df["date"] <= pd.to_datetime(end_date)]

        if count and len(df) > count:
            df = df.head(count)

        df = df.sort_values("date", ascending=False).reset_index(drop=True)

        return df

    except Exception as e:
        warnings.warn(f"获取 {symbol} 资金流失败: {e}")
        return _get_empty_dataframe(fields)


def get_money_flow(
    security_list: Optional[Union[str, List[str]]] = None,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    fields: Optional[Union[str, List[str]]] = None,
    count: Optional[int] = None,
    **kwargs,
) -> pd.DataFrame:
    """
    获取个股资金流数据。

    参数
    ----
    security_list : str or list of str, optional
        股票代码或股票列表，如 'sh600000' 或 ['sh600000', 'sz000001']
        支持多种格式：'sh600000', '600000.XSHG', '600000'
    start_date : str, optional
        开始日期 'YYYY-MM-DD'（与 count 二选一）
    end_date : str, optional
        结束日期 'YYYY-MM-DD'
    fields : str or list of str, optional
        需要返回的字段，如 ['sec_code', 'date', 'change_pct', 'net_pct_main']
        可用字段: sec_code, date, close, change_pct,
                 net_amount_main, net_pct_main,
                 net_amount_xl, net_pct_xl,
                 net_amount_l, net_pct_l,
                 net_amount_m, net_pct_m,
                 net_amount_s, net_pct_s
    count : int, optional
        返回最近N天的数据（与 start_date 二选一）

    返回
    ----
    pd.DataFrame
        资金流数据，包含指定字段。
        无数据或离线时返回带稳定列名的空表。

    示例
    ----
    >>> # 获取单只股票最近1天数据
    >>> df = get_money_flow('sh600000', count=1, fields=['sec_code', 'change_pct'])

    >>> # 获取多只股票指定日期数据
    >>> df = get_money_flow(['sh600000', 'sz000001'], end_date='2024-01-15',
    >>>                     fields=['sec_code', 'net_pct_main'], count=1)

    >>> # 获取股票列表按日期区间
    >>> df = get_money_flow(stock_list, start_date='2024-01-01', end_date='2024-01-31')
    """
    if isinstance(fields, str):
        select_fields = (
            ["sec_code", "date", fields]
            if fields not in ["sec_code", "date"]
            else [fields]
        )
    elif fields is None:
        select_fields = ["sec_code", "date"] + [
            f for f in ALL_FIELDS if f not in ["sec_code", "date"]
        ]
    else:
        select_fields = list(fields)
        if "sec_code" not in select_fields:
            select_fields = ["sec_code"] + select_fields

    if security_list is None:
        return _get_empty_dataframe(select_fields)

    if isinstance(security_list, str):
        symbols = [security_list]
    else:
        symbols = list(security_list)

    results = []

    for symbol in symbols:
        df = _get_single_stock_flow(
            symbol=symbol,
            start_date=start_date,
            end_date=end_date,
            count=count,
            fields=select_fields,
        )

        if not df.empty:
            available_fields = [f for f in select_fields if f in df.columns]
            if available_fields:
                results.append(df[available_fields])

    if not results:
        return _get_empty_dataframe(select_fields)

    final_df = pd.concat(results, ignore_index=True)

    return final_df


__all__ = ["get_money_flow"]
