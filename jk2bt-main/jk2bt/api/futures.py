"""
jk2bt/api/futures.py
期货数据 API 模块

提供 JQData 兼容的期货数据查询接口。
数据源: AkShare

主要功能:
- get_dominant_future: 获取主力合约代码
- get_futures_info: 获取期货合约信息
- get_future_contracts: 获取期货合约列表
- get_order_future_bar: 获取连续合约bar行情
"""

import pandas as pd
from typing import Optional, List, Literal
import warnings
import re


FUTURE_EXCHANGE_MAP = {
    "IF": "CCFX",
    "IC": "CCFX",
    "IH": "CCFX",
    "IM": "CCFX",
    "T": "CCFX",
    "TF": "CCFX",
    "TS": "CCFX",
    "TL": "CCFX",
    "AU": "XSGE",
    "AG": "XSGE",
    "CU": "XSGE",
    "AL": "XSGE",
    "ZN": "XSGE",
    "PB": "XSGE",
    "NI": "XSGE",
    "SN": "XSGE",
    "RB": "XSGE",
    "HC": "XSGE",
    "SS": "XSGE",
    "I": "XDCE",
    "J": "XDCE",
    "JM": "XDCE",
    "ZC": "XDCE",
    "A": "XDCE",
    "B": "XDCE",
    "M": "XDCE",
    "Y": "XDCE",
    "P": "XDCE",
    "C": "XDCE",
    "CS": "XDCE",
    "JD": "XDCE",
    "L": "XDCE",
    "V": "XDCE",
    "PP": "XDCE",
    "EG": "XDCE",
    "MA": "XDCE",
    "TA": "XZCE",
    "OI": "XZCE",
    "RM": "XZCE",
    "SR": "XZCE",
    "CF": "XZCE",
    "SC": "XINE",
    "NR": "XINE",
}


def _is_index_code(symbol: str) -> bool:
    """判断是否为品种指数代码（如 AG8888.XSGE）"""
    if not symbol:
        return False
    match = re.match(r"^([A-Z]+)8888\.([A-Z]+)$", symbol.upper())
    if match:
        product = match.group(1)
        return product in FUTURE_EXCHANGE_MAP
    return False


def _get_product_from_index(symbol: str) -> Optional[str]:
    """从品种指数代码提取品种代码"""
    match = re.match(r"^([A-Z]+)8888\.([A-Z]+)$", symbol.upper())
    if match:
        return match.group(1)
    return None


def get_dominant_future(
    underlying_symbol: str,
    date: Optional[str] = None,
) -> str:
    """
    获取主力合约代码。

    聚宽兼容接口

    参数
    ----
    underlying_symbol : str
        标的合约代码，如 'IF', 'IC', 'IH', 'AU', 'CU' 等
        也支持品种指数格式如 'AG8888.XSGE'（返回 AG8888.CCFX）
    date : str, optional
        查询日期，格式 'YYYY-MM-DD'

    返回
    ----
    str
        主力合约代码，如 'IF2401'
        如果传入品种指数格式如 'AG8888.XSGE'，返回 'AG8888.CCFX'

    示例
    ----
    >>> contract = get_dominant_future('IF')
    >>> print(contract)
    'IF2401'
    >>> contract = get_dominant_future('AG8888.XSGE')
    >>> print(contract)
    'AG8888.CCFX'
    """
    if _is_index_code(underlying_symbol):
        product = _get_product_from_index(underlying_symbol)
        if product:
            exchange = FUTURE_EXCHANGE_MAP.get(product, "CCFX")
            return f"{product}8888.{exchange}"
        return ""

    from jk2bt.market_data.futures_data import get_dominant_contract

    result = get_dominant_contract(underlying_symbol, date)
    return result or ""


def get_futures_info(
    contract_code: Optional[str] = None,
    exchange: Optional[str] = None,
    fields: Optional[List[str]] = None,
) -> pd.DataFrame:
    """
    获取期货合约信息。

    聚宽兼容接口

    参数
    ----
    contract_code : str, optional
        合约代码，如 'IF2401'，None 表示获取所有合约
    exchange : str, optional
        交易所代码:
        - 'CFFEX': 中金所
        - 'SHFE': 上期所
        - 'DCE': 大商所
        - 'CZCE': 郑商所
    fields : list of str, optional
        返回字段列表

    返回
    ----
    pd.DataFrame
        合约信息:
        - code: 合约代码
        - name: 合约名称
        - exchange: 交易所
        - multiplier: 合约乘数
        - min_change: 最小变动价位

    示例
    ----
    >>> df = get_futures_info('IF')
    >>> print(df.head())
    """
    from jk2bt.market_data.futures_data import get_futures_info as _get_futures_info

    result = _get_futures_info(contract_code, exchange)

    if fields and not result.empty:
        available_fields = [f for f in fields if f in result.columns]
        if available_fields:
            result = result[available_fields]

    return result


def get_future_contracts(
    underlying_symbol: str,
    exchange: Optional[str] = None,
) -> List[str]:
    """
    获取期货合约列表。

    聚宽兼容接口

    参数
    ----
    underlying_symbol : str
        标的合约代码，如 'IF', 'IC', 'AU' 等
    exchange : str, optional
        交易所代码

    返回
    ----
    List[str]
        合约代码列表

    示例
    ----
    >>> contracts = get_future_contracts('IF')
    >>> print(contracts)
    ['IF2401', 'IF2402', 'IF2403', ...]
    """
    from jk2bt.market_data.futures_data import (
        get_future_contracts as _get_future_contracts,
    )

    return _get_future_contracts(underlying_symbol, exchange)


def get_dominant_contracts(
    underlying_symbols: List[str],
    date: Optional[str] = None,
) -> pd.DataFrame:
    """
    批量获取主力合约。

    参数
    ----
    underlying_symbols : List[str]
        标的合约代码列表
    date : str, optional
        查询日期

    返回
    ----
    pd.DataFrame
        主力合约信息
    """
    from jk2bt.market_data.futures_data import (
        get_dominant_contract,
        FUTURE_UNDERLYING_MAP,
        _get_exchange_by_underlying,
        _get_multiplier,
    )

    results = []
    for underlying in underlying_symbols:
        contract = get_dominant_contract(underlying, date)
        if contract:
            results.append(
                {
                    "underlying": underlying,
                    "contract": contract,
                    "name": FUTURE_UNDERLYING_MAP.get(underlying, ""),
                    "exchange": _get_exchange_by_underlying(underlying),
                    "multiplier": _get_multiplier(underlying),
                }
            )

    return pd.DataFrame(results)


def get_settlement_price(
    contract_code: str,
    date: Optional[str] = None,
) -> float:
    """
    获取期货结算价。

    参数
    ----
    contract_code : str
        合约代码
    date : str, optional
        查询日期

    返回
    ----
    float
        结算价
    """
    from jk2bt.market_data.futures_data import get_futures_daily

    df = get_futures_daily(contract_code, start_date=date, end_date=date)

    if not df.empty:
        return float(df["close"].iloc[0])

    return 0.0


def get_order_future_bar(
    product: str,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    bar_count: Optional[int] = None,
    fields: Optional[List[str]] = None,
    include_now: bool = True,
) -> pd.DataFrame:
    """
    获取当月/次月/当季/隔季等合约拼接而成的bar行情。

    聚宽兼容接口

    参数
    ----
    product : str
        期货品种代码，如 'IF', 'IC', 'AU', 'AG' 等
    start_date : str, optional
        起始日期，格式 'YYYY-MM-DD'
    end_date : str, optional
        结束日期，格式 'YYYY-MM-DD'
    bar_count : int, optional
        获取bar数量（从 end_date 往前计算）
    fields : list of str, optional
        返回字段列表
    include_now : bool
        是否包含当前交易日

    返回
    ----
    pd.DataFrame
        连续合约bar行情:
        - datetime: 日期时间
        - open: 开盘价
        - high: 最高价
        - low: 最低价
        - close: 收盘价
        - volume: 成交量

    示例
    ----
    >>> df = get_order_future_bar('AG', start_date='2023-01-01', end_date='2023-12-31')
    >>> df = get_order_future_bar('IF', bar_count=100)
    """
    from jk2bt.market_data.futures_data import (
        get_futures_daily,
        _get_order_contracts,
    )
    from datetime import datetime, timedelta

    product = product.upper()

    if bar_count and bar_count > 0 and end_date:
        end_dt = pd.to_datetime(end_date)
        all_dates = pd.date_range(end=end_dt, periods=bar_count, freq="B")
        start_date = all_dates[0].strftime("%Y-%m-%d")
    elif not start_date:
        start_date = "2020-01-01"
    if not end_date:
        end_date = datetime.now().strftime("%Y-%m-%d")

    try:
        order_contracts = _get_order_contracts(product)
        if not order_contracts:
            warnings.warn(f"无法获取 {product} 的顺序合约列表")
            return pd.DataFrame()

        all_bars = []
        for contract in order_contracts:
            df = get_futures_daily(contract, start_date=start_date, end_date=end_date)
            if df is not None and not df.empty:
                if "datetime" in df.columns:
                    df["datetime"] = pd.to_datetime(df["datetime"])
                elif "date" in df.columns:
                    df["datetime"] = pd.to_datetime(df["date"])
                df = (
                    df.rename(columns={"date": "datetime"})
                    if "date" in df.columns
                    else df
                )
                df["contract"] = contract
                all_bars.append(df)

        if not all_bars:
            return pd.DataFrame()

        combined = pd.concat(all_bars, ignore_index=True)
        combined = combined.sort_values("datetime").drop_duplicates(
            subset=["datetime"], keep="last"
        )
        combined = combined.reset_index(drop=True)

        if fields:
            available = [f for f in fields if f in combined.columns]
            if "datetime" not in available and "datetime" in combined.columns:
                available = ["datetime"] + available
            combined = combined[available]

        return combined

    except Exception as e:
        warnings.warn(f"获取连续合约bar行情失败 {product}: {e}")
        return pd.DataFrame()


def get_future_index_bar(
    product: str,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    bar_count: Optional[int] = None,
    fields: Optional[List[str]] = None,
) -> pd.DataFrame:
    """
    获取期货品种指数bar行情。

    参数
    ----
    product : str
        期货品种代码，如 'AG', 'AU', 'CU' 等
    start_date : str, optional
        起始日期
    end_date : str, optional
        结束日期
    bar_count : int, optional
        获取bar数量
    fields : list of str, optional
        返回字段列表

    返回
    ----
    pd.DataFrame
        品种指数bar行情

    示例
    ----
    >>> df = get_future_index_bar('AG', start_date='2023-01-01', end_date='2023-12-31')
    """
    warnings.warn(
        "get_future_index_bar 需要专业数据源（如聚宽JQData），akshare暂无品种指数接口"
    )
    return pd.DataFrame()


# 聚宽风格别名
get_dominant_future_jq = get_dominant_future
get_futures_info_jq = get_futures_info
get_future_contracts_jq = get_future_contracts


__all__ = [
    "get_dominant_future",
    "get_futures_info",
    "get_future_contracts",
    "get_dominant_contracts",
    "get_settlement_price",
    "get_order_future_bar",
    "get_future_index_bar",
    "get_dominant_future_jq",
    "get_futures_info_jq",
    "get_future_contracts_jq",
]
