"""
jk2bt/api/shareholder.py
Shareholder Information API Module

JQData compatible interface for shareholder data.
Data sources: AkShare

Main functions:
- get_top10_shareholders: Get top 10 shareholders
- get_top10_float_shareholders: Get top 10 float shareholders
- get_shareholder_count: Get shareholder count time series
- get_shareholder_structure: Get shareholder structure by type
"""

import pandas as pd
from typing import Optional, List, Dict

from jk2bt.data.finance.shareholder import (
    get_top10_shareholders as _get_top10_shareholders,
    get_top10_float_shareholders as _get_top10_float_shareholders,
    get_shareholder_count as _get_shareholder_count,
    get_shareholder_structure as _get_shareholder_structure,
    get_shareholders as _get_shareholders,
    get_top_shareholders as _get_top_shareholders_old,
    get_top_float_shareholders as _get_top_float_shareholders_old,
)


def get_top10_shareholders(
    symbol: str,
    date: Optional[str] = None,
    force_update: bool = False,
) -> pd.DataFrame:
    """
    Get top 10 shareholders snapshot.

    JQData compatible interface

    Parameters
    ----
    symbol : str
        Security code, supports formats:
        - '000001.XSHE' (JQData format)
        - '600519.XSHG' (JQData format)
        - 'sh600519' (akshare format)
        - '600519' (pure code)
    date : str, optional
        Query date
    force_update : bool, optional
        Force update from network

    Returns
    ----
    pd.DataFrame
        Top 10 shareholders data with fields:
        - code: Security code (JQData format)
        - shareholder_name: Shareholder name
        - shareholder_type: Shareholder type
        - hold_amount: Holding amount
        - hold_ratio: Holding ratio
        - change_type: Change type
        - report_date: Report date
        - ann_date: Announcement date
        - rank: Rank

    Examples
    ----
    >>> df = get_top10_shareholders('600519.XSHG')
    >>> df = get_top10_shareholders('600519.XSHG', date='2024-03-31')
    """
    result = _get_top10_shareholders(symbol, date=date, force_update=force_update)
    if result is None or result.empty:
        return pd.DataFrame(
            columns=[
                "code",
                "report_date",
                "ann_date",
                "shareholder_name",
                "shareholder_code",
                "shareholder_type",
                "hold_amount",
                "hold_ratio",
                "change_type",
                "change_amount",
                "rank",
            ]
        )
    return result


def get_top10_float_shareholders(
    symbol: str,
    date: Optional[str] = None,
    force_update: bool = False,
) -> pd.DataFrame:
    """
    Get top 10 float shareholders snapshot.

    JQData compatible interface

    Parameters
    ----
    symbol : str
        Security code
    date : str, optional
        Query date
    force_update : bool, optional
        Force update from network

    Returns
    ----
    pd.DataFrame
        Top 10 float shareholders data with fields:
        - code: Security code (JQData format)
        - shareholder_name: Shareholder name
        - shareholder_type: Shareholder type
        - hold_amount: Holding amount
        - hold_ratio: Holding ratio
        - change_type: Change type
        - report_date: Report date
        - ann_date: Announcement date
        - rank: Rank

    Examples
    ----
    >>> df = get_top10_float_shareholders('600519.XSHG')
    """
    result = _get_top10_float_shareholders(symbol, date=date, force_update=force_update)
    if result is None or result.empty:
        return pd.DataFrame(
            columns=[
                "code",
                "report_date",
                "ann_date",
                "shareholder_name",
                "shareholder_code",
                "shareholder_type",
                "hold_amount",
                "hold_ratio",
                "change_type",
                "change_amount",
                "rank",
            ]
        )
    return result


def get_shareholder_count(
    symbol: str,
    force_update: bool = False,
) -> pd.DataFrame:
    """
    Get shareholder count time series.

    JQData compatible interface

    Parameters
    ----
    symbol : str
        Security code
    force_update : bool, optional
        Force update from network

    Returns
    ----
    pd.DataFrame
        Shareholder count data with fields:
        - code: Security code (JQData format)
        - report_date: Report date
        - ann_date: Announcement date
        - holder_num: Holder count
        - holder_num_change: Holder count change
        - holder_num_change_ratio: Holder count change ratio

    Examples
    ----
    >>> df = get_shareholder_count('600519.XSHG')
    """
    result = _get_shareholder_count(symbol, force_update=force_update)
    if result is None or result.empty:
        return pd.DataFrame(
            columns=[
                "code",
                "report_date",
                "ann_date",
                "holder_num",
                "holder_num_change",
                "holder_num_change_ratio",
            ]
        )
    return result


def get_shareholder_structure(
    security: str,
    force_update: bool = False,
    use_duckdb: bool = True,
) -> pd.DataFrame:
    """
    Get shareholder structure (statistics by shareholder type).

    JQData compatible interface

    Parameters
    ----
    security : str
        Security code
    force_update : bool, optional
        Force update from network
    use_duckdb : bool, optional
        Use DuckDB cache (default True)

    Returns
    ----
    pd.DataFrame
        Shareholder structure data with fields:
        - code: Security code
        - shareholder_type: Shareholder type (state-owned, institutional, individual, etc.)
        - hold_ratio: Holding ratio
        - report_date: Report date

    Examples
    ----
    >>> df = get_shareholder_structure('600519.XSHG')
    """
    result = _get_shareholder_structure(
        security, force_update=force_update, use_duckdb=use_duckdb
    )
    if result is None or result.empty:
        return pd.DataFrame(
            columns=["code", "shareholder_type", "hold_ratio", "report_date"]
        )
    return result


__all__ = [
    "get_top10_shareholders",
    "get_top10_float_shareholders",
    "get_shareholder_count",
    "get_shareholder_structure",
]
