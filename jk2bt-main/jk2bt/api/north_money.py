"""
jk2bt/api/north_money.py
North money (北向资金) API module

Provides JQData compatible interfaces for northbound money flow data.
Data sources: AkShare (eastmoney HSGT)

Functions:
- get_north_money_flow: North money net flow
- get_north_money_daily: North money daily data
- get_north_money_holdings: North money holdings statistics
- get_north_money_stock_flow: Individual stock north money flow
- get_north_money_stock_detail: Individual stock north money detail
- compute_north_money_signal: North money timing signal
- get_north_top_active_stocks: Top 10 active stocks by turnover
- get_north_quota_info: Quota and trading info
- get_north_exchange_rate: Exchange rate for northbound trading
- get_north_calendar: Trading calendar
"""

import pandas as pd
from typing import Optional, Dict

from jk2bt.data.market.north_money import get_north_money_flow as _get_north_money_flow
from jk2bt.data.market.north_money import (
    get_north_money_daily as _get_north_money_daily,
)
from jk2bt.data.market.north_money import (
    get_north_money_holdings as _get_north_money_holdings,
)
from jk2bt.data.market.north_money import (
    get_north_money_stock_flow as _get_north_money_stock_flow,
)
from jk2bt.data.market.north_money import (
    get_north_money_stock_detail as _get_north_money_stock_detail,
)
from jk2bt.data.market.north_money import (
    compute_north_money_signal as _compute_north_money_signal,
)
from jk2bt.data.market.north_money import (
    get_north_top_active_stocks as _get_north_top_active_stocks,
)
from jk2bt.data.market.north_money import (
    get_north_quota_info as _get_north_quota_info,
)
from jk2bt.data.market.north_money import (
    get_north_exchange_rate as _get_north_exchange_rate,
)
from jk2bt.data.market.north_money import (
    get_north_calendar as _get_north_calendar,
)


def get_north_money_flow(
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
) -> pd.DataFrame:
    """
    Get north money net flow data (daily).

    JQData compatible interface

    Parameters
    ----
    start_date : str, optional
        Start date 'YYYY-MM-DD'
    end_date : str, optional
        End date 'YYYY-MM-DD'

    Returns
    ----
    pd.DataFrame
        North money net flow data with columns:
        date, net_inflow, inflow, outflow
    """
    try:
        return _get_north_money_flow(start_date=start_date, end_date=end_date)
    except Exception:
        return pd.DataFrame()


def get_north_money_daily(
    date: Optional[str] = None,
) -> Dict[str, float]:
    """
    Get north money data for a specific date.

    JQData compatible interface

    Parameters
    ----
    date : str, optional
        Query date, default is most recent trading day

    Returns
    ----
    Dict[str, float]
        {'net_inflow': net inflow amount, 'inflow': inflow, 'outflow': outflow}
    """
    try:
        return _get_north_money_daily(date=date)
    except Exception:
        return {"net_inflow": 0.0, "inflow": 0.0, "outflow": 0.0}


def get_north_money_holdings(
    date: Optional[str] = None,
    top_n: int = 50,
) -> pd.DataFrame:
    """
    Get north money holdings statistics.

    JQData compatible interface

    Parameters
    ----
    date : str, optional
        Query date
    top_n : int
        Return top N stocks by holdings value

    Returns
    ----
    pd.DataFrame
        North money holdings data with columns:
        code, name, holdings, holding_value, holding_pct, holding_value_pct,
        holdings_change, holding_value_change
    """
    try:
        return _get_north_money_holdings(date=date, top_n=top_n)
    except Exception:
        return pd.DataFrame()


def get_north_money_stock_flow(
    symbol: str,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
) -> pd.DataFrame:
    """
    Get north money flow data for a specific stock.

    JQData compatible interface

    Parameters
    ----
    symbol : str
        Stock code
    start_date : str, optional
        Start date
    end_date : str, optional
        End date

    Returns
    ----
    pd.DataFrame
        Stock north money flow data with columns:
        date, net_inflow, inflow, outflow
    """
    if not symbol:
        return pd.DataFrame()

    try:
        return _get_north_money_stock_flow(
            symbol=symbol,
            start_date=start_date,
            end_date=end_date,
        )
    except Exception:
        return pd.DataFrame()


def get_north_money_stock_detail(
    symbol: str,
    date: Optional[str] = None,
) -> Dict[str, any]:
    """
    Get north money detail for a specific stock on a specific date.

    JQData compatible interface

    Parameters
    ----
    symbol : str
        Stock code
    date : str, optional
        Query date

    Returns
    ----
    Dict[str, any]
        {'net_inflow': net inflow, 'holdings': holdings, 'holding_change': holdings change,
         'link_id': 'sh' or 'sz', 'link_name': '沪股通' or '深股通'}
    """
    if not symbol:
        code = symbol or ""
        link_id = "sh" if code.startswith("6") else "sz"
        link_name = "沪股通" if link_id == "sh" else "深股通"
        return {
            "net_inflow": 0.0,
            "holdings": 0.0,
            "holding_change": 0.0,
            "link_id": link_id,
            "link_name": link_name,
        }

    try:
        return _get_north_money_stock_detail(symbol=symbol, date=date)
    except Exception:
        code = (
            symbol.replace("sh", "")
            .replace("sz", "")
            .replace(".XSHG", "")
            .replace(".XSHE", "")
            .zfill(6)
        )
        link_id = "sh" if code.startswith("6") else "sz"
        link_name = "沪股通" if link_id == "sh" else "深股通"
        return {
            "net_inflow": 0.0,
            "holdings": 0.0,
            "holding_change": 0.0,
            "link_id": link_id,
            "link_name": link_name,
        }


def compute_north_money_signal(
    window: int = 20,
    threshold: float = 30.0,
    date: Optional[str] = None,
) -> Dict[str, any]:
    """
    Compute north money timing signal.

    JQData compatible interface

    Parameters
    ----
    window : int
        Window period for moving average
    threshold : float
        Signal threshold (100 million yuan)
    date : str, optional
        Calculation end date

    Returns
    ----
    Dict[str, any]
        {
            'signal': 1 (inflow signal), -1 (outflow signal), 0 (neutral),
            'net_inflow': today's net inflow,
            'avg_inflow': N-day average net inflow,
            'description': signal description
        }
    """
    try:
        return _compute_north_money_signal(
            window=window,
            threshold=threshold,
            date=date,
        )
    except Exception:
        return {
            "signal": 0,
            "net_inflow": 0.0,
            "avg_inflow": 0.0,
            "description": "Data unavailable",
        }


def get_north_top_active_stocks(
    date: Optional[str] = None,
    link_id: Optional[str] = None,
) -> pd.DataFrame:
    """
    Get top 10 most active stocks by northbound turnover.

    JQData compatible interface

    Parameters
    ----
    date : str, optional
        Query date, default is most recent trading day
    link_id : str, optional
        'sh' for 沪股通, 'sz' for 深股通, None for both

    Returns
    ----
    pd.DataFrame
        Top active stocks with columns:
        code, name, close, change_pct, turnover, north_net_inflow,
        north_holdings, north_holdings_pct, link_id, link_name
    """
    try:
        return _get_north_top_active_stocks(date=date, link_id=link_id)
    except Exception:
        return pd.DataFrame()


def get_north_quota_info(
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
) -> pd.DataFrame:
    """
    Get northbound quota and trading information.

    JQData compatible interface

    Parameters
    ----
    start_date : str, optional
        Start date 'YYYY-MM-DD'
    end_date : str, optional
        End date 'YYYY-MM-DD'

    Returns
    ----
    pd.DataFrame
        Quota info with columns:
        date, link_id, link_name, daily_quota, used_quota, balance, net_inflow
    """
    try:
        return _get_north_quota_info(start_date=start_date, end_date=end_date)
    except Exception:
        return pd.DataFrame()


def get_north_exchange_rate(
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
) -> pd.DataFrame:
    """
    Get northbound trading exchange rate (HKD/CNY).

    JQData compatible interface

    Parameters
    ----
    start_date : str, optional
        Start date 'YYYY-MM-DD'
    end_date : str, optional
        End date 'YYYY-MM-DD'

    Returns
    ----
    pd.DataFrame
        Exchange rate data with columns:
        date, link_id, exchange_rate, currency
    """
    try:
        return _get_north_exchange_rate(start_date=start_date, end_date=end_date)
    except Exception:
        return pd.DataFrame()


def get_north_calendar(
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
) -> pd.DataFrame:
    """
    Get northbound trading calendar.

    JQData compatible interface

    Parameters
    ----
    start_date : str, optional
        Start date 'YYYY-MM-DD'
    end_date : str, optional
        End date 'YYYY-MM-DD'

    Returns
    ----
    pd.DataFrame
        Trading calendar with columns:
        date, is_trading, link_id, holiday
    """
    try:
        return _get_north_calendar(start_date=start_date, end_date=end_date)
    except Exception:
        return pd.DataFrame()


__all__ = [
    "get_north_money_flow",
    "get_north_money_daily",
    "get_north_money_holdings",
    "get_north_money_stock_flow",
    "get_north_money_stock_detail",
    "compute_north_money_signal",
    "get_north_top_active_stocks",
    "get_north_quota_info",
    "get_north_exchange_rate",
    "get_north_calendar",
]
