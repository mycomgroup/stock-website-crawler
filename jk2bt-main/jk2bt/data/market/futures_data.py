"""
futures_data.py - Shim layer re-exporting from futures.py

This module exists for backward compatibility.
Functions that api/futures.py needs are imported from futures.py.
"""

from jk2bt.data.market.futures import (
    FUTURE_UNDERLYING_MAP,
    get_futures_info,
    get_dominant_contract,
    _infer_dominant_contract,
    _get_exchange_by_underlying,
    _get_multiplier,
    _get_order_contracts,
    # These have different signatures in futures.py, keep local versions below
)

# Import list-based versions - these have the signatures api/futures.py expects
# They shadow the above re-exports (which we don't use anyway)
from jk2bt.data.market.futures import (
    get_future_contracts_list as _get_future_contracts_list,
    get_futures_daily_list as _get_futures_daily_list,
)

# Keep local implementations to maintain backward compatibility
# These are imported by api/futures.py with specific signatures
import warnings
from typing import Optional, List
import pandas as pd
from datetime import datetime

from jk2bt.data.sources import get_adapter


def get_future_contracts(
    underlying_symbol: str,
    date: Optional[str] = None,
    exchange: Optional[str] = None,
) -> List[str]:
    """
    获取期货合约列表。

    参数
    ----
    underlying_symbol : str
        期货品种代码
    date : str, optional
        查询日期，格式 'YYYY-MM-DD'
    exchange : str, optional
        交易所代码

    返回
    ----
    List[str]
        合约代码列表
    """
    return _get_future_contracts_list(underlying_symbol, exchange)


def get_futures_daily(
    contract_code: str,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
) -> pd.DataFrame:
    """
    获取期货日线行情。

    参数
    ----
    contract_code : str
        合约代码
    start_date : str, optional
        开始日期
    end_date : str, optional
        结束日期

    返回
    ----
    pd.DataFrame
        日线行情数据
    """
    return _get_futures_daily_list(contract_code, start_date, end_date)


__all__ = [
    "get_dominant_contract",
    "get_futures_info",
    "get_future_contracts",
    "get_futures_daily",
    "FUTURE_UNDERLYING_MAP",
    "_get_exchange_by_underlying",
    "_get_multiplier",
    "_infer_dominant_contract",
    "_get_order_contracts",
]
