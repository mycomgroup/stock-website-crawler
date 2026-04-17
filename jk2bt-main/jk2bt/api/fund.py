"""
jk2bt/api/fund.py
Fund data API module

Provides JQData compatible interfaces for fund data.
Data sources: AkShare (eastmoney)

Functions:
- get_etf_daily: ETF daily行情
- get_fund_nav / get_fund_of_nav: 场外基金净值
- get_fund_of_info: 基金基本信息
- get_fund_of_daily_list: 基金日列表
- get_lof_daily: LOF日行情
- get_lof_spot: LOF实时行情
- get_lof_nav: LOF净值
"""

import pandas as pd
from typing import Optional, List

from jk2bt.data.market.etf import get_etf_daily as _get_etf_daily
from jk2bt.data.market.fund_of import get_fund_of_nav as _get_fund_of_nav
from jk2bt.data.market.fund_of import get_fund_of_info as _get_fund_of_info
from jk2bt.data.market.fund_of import get_fund_of_daily_list as _get_fund_of_daily_list
from jk2bt.data.market.lof import get_lof_daily as _get_lof_daily
from jk2bt.data.market.lof import get_lof_spot as _get_lof_spot
from jk2bt.data.market.lof import get_lof_nav as _get_lof_nav


def get_etf_daily(
    symbol: str,
    start: str,
    end: str,
    force_update: bool = False,
    data_sources: Optional[List[str]] = None,
) -> pd.DataFrame:
    """
    Get ETF daily OHLCV data.

    JQData compatible interface

    Parameters
    ----
    symbol : str
        ETF code, e.g. '510300' (without exchange prefix)
    start : str
        Start date 'YYYY-MM-DD'
    end : str
        End date 'YYYY-MM-DD'
    force_update : bool
        Force refresh from data source
    data_sources : list, optional
        Data source priority list, default ["east_money", "tushare"]

    Returns
    ----
    pd.DataFrame
        Standardized OHLCV data with columns:
        datetime, open, high, low, close, volume, amount
    """
    if not symbol or not start or not end:
        return pd.DataFrame()

    try:
        return _get_etf_daily(
            symbol=symbol,
            start=start,
            end=end,
            force_update=force_update,
            data_sources=data_sources,
        )
    except Exception:
        return pd.DataFrame()


def get_fund_nav(
    symbol: str,
    start: Optional[str] = None,
    end: Optional[str] = None,
    force_update: bool = False,
) -> pd.DataFrame:
    """
    Get off-exchange fund NAV (Net Asset Value) history.

    JQData compatible interface

    Parameters
    ----
    symbol : str
        Fund code, e.g. '000001' (Huaxia Growth Mixed)
    start : str, optional
        Start date 'YYYY-MM-DD'
    end : str, optional
        End date 'YYYY-MM-DD'
    force_update : bool
        Force refresh

    Returns
    ----
    pd.DataFrame
        NAV data with columns:
        datetime, unit_nav, acc_nav, daily_growth_rate, purchase_status, redeem_status
    """
    if not symbol:
        return pd.DataFrame()

    try:
        return _get_fund_of_nav(
            symbol=symbol,
            start=start,
            end=end,
            force_update=force_update,
        )
    except Exception:
        return pd.DataFrame()


get_fund_of_nav = get_fund_nav


def get_fund_of_info(symbol: str) -> dict:
    """
    Get off-exchange fund basic information.

    JQData compatible interface

    Parameters
    ----
    symbol : str
        Fund code

    Returns
    ----
    dict
        Fund basic info: name, type, manager, etc.
    """
    if not symbol:
        return {}

    try:
        return _get_fund_of_info(symbol=symbol)
    except Exception:
        return {}


def get_fund_of_daily_list() -> pd.DataFrame:
    """
    Get all off-exchange funds daily NAV list.

    JQData compatible interface

    Returns
    ----
    pd.DataFrame
        Daily NAV data for all off-exchange funds
    """
    try:
        return _get_fund_of_daily_list()
    except Exception:
        return pd.DataFrame()


def get_lof_daily(
    symbol: str,
    start: str,
    end: str,
    period: str = "daily",
    adjust: str = "",
    force_update: bool = False,
    retry_count: int = 3,
) -> pd.DataFrame:
    """
    Get LOF daily OHLCV data.

    JQData compatible interface

    Parameters
    ----
    symbol : str
        LOF code, e.g. '161725' (China Securities Liquidity LOF)
    start : str
        Start date 'YYYY-MM-DD'
    end : str
        End date 'YYYY-MM-DD'
    period : str
        Period: daily/weekly/monthly
    adjust : str
        Adjustment type: qfq/hfq/'' (empty for no adjustment)
    force_update : bool
        Force refresh from akshare
    retry_count : int
        Number of retries for network requests

    Returns
    ----
    pd.DataFrame
        Standardized OHLCV data with columns:
        datetime, open, high, low, close, volume, amount
    """
    if not symbol or not start or not end:
        return pd.DataFrame()

    try:
        return _get_lof_daily(
            symbol=symbol,
            start=start,
            end=end,
            period=period,
            adjust=adjust,
            force_update=force_update,
            retry_count=retry_count,
        )
    except Exception:
        return pd.DataFrame()


def get_lof_spot() -> pd.DataFrame:
    """
    Get all LOF real-time quote list.

    JQData compatible interface

    Returns
    ----
    pd.DataFrame
        LOF real-time data with columns: code, name, latest_price, change_pct, etc.
    """
    try:
        return _get_lof_spot()
    except Exception:
        return pd.DataFrame()


def get_lof_nav(
    symbol: str,
    start: Optional[str] = None,
    end: Optional[str] = None,
) -> pd.DataFrame:
    """
    Get LOF off-exchange NAV data (stable interface).

    JQData compatible interface

    Parameters
    ----
    symbol : str
        LOF code, e.g. '161725'
    start : str, optional
        Start date 'YYYY-MM-DD'
    end : str, optional
        End date 'YYYY-MM-DD'

    Returns
    ----
    pd.DataFrame
        NAV data with columns:
        datetime, unit_nav, acc_nav, daily_growth_rate, purchase_status, redeem_status
    """
    if not symbol:
        return pd.DataFrame()

    try:
        return _get_lof_nav(symbol=symbol, start=start, end=end)
    except Exception:
        return pd.DataFrame()


__all__ = [
    "get_etf_daily",
    "get_fund_nav",
    "get_fund_of_nav",
    "get_fund_of_info",
    "get_fund_of_daily_list",
    "get_lof_daily",
    "get_lof_spot",
    "get_lof_nav",
]
