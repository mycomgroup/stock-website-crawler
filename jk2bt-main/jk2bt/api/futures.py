"""
jk2bt/api/futures.py
期货数据 API 模块

提供 JQData 兼容的期货数据查询接口。
数据源: AkShare

主要功能:
- get_dominant_future: 获取主力合约代码
- get_futures_info: 获取期货合约信息
- get_future_contracts: 获取期货合约列表
"""

import pandas as pd
from typing import Optional, List
import warnings


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
    date : str, optional
        查询日期，格式 'YYYY-MM-DD'

    返回
    ----
    str
        主力合约代码，如 'IF2401'

    示例
    ----
    >>> contract = get_dominant_future('IF')
    >>> print(contract)
    'IF2401'
    """
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
    from jk2bt.market_data.futures_data import get_future_contracts as _get_future_contracts

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
            results.append({
                "underlying": underlying,
                "contract": contract,
                "name": FUTURE_UNDERLYING_MAP.get(underlying, ""),
                "exchange": _get_exchange_by_underlying(underlying),
                "multiplier": _get_multiplier(underlying),
            })

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
    "get_dominant_future_jq",
    "get_futures_info_jq",
    "get_future_contracts_jq",
]