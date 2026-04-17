"""
jk2bt/api/unlock.py
Restricted share release (unlock) data API module.

Provides JQData compatible interfaces for restricted share unlock data.
Data sources: AkShare

Main functions:
- get_unlock_info: Get restricted share unlock information
- get_unlock_calendar: Get market-wide unlock calendar
- get_unlock_schedule: Get unlock schedule
- get_unlock_pressure: Calculate unlock pressure
- get_unlock_history: Get historical unlock records
- get_upcoming_unlocks: Get upcoming unlocks
- analyze_unlock_impact: Analyze unlock impact on stock price
"""

import pandas as pd
from typing import Optional


def get_unlock_info(
    symbol: str,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    force_update: bool = False,
):
    """
    Get restricted share unlock information (robust version).

    JQData compatible interface

    Parameters
    ----------
    symbol : str
        Stock code in any format (e.g. '000001.XSHE', 'sh600519', '600519')
    start_date : str, optional
        Start date, format 'YYYY-MM-DD'
    end_date : str, optional
        End date, format 'YYYY-MM-DD'
    force_update : bool, optional
        Force update from network, default False

    Returns
    -------
    RobustResult
        Result object with:
        - success: Whether the query succeeded
        - data: DataFrame with unlock data
        - reason: Result description
        - source: Data source (cache/network/error)

    Examples
    --------
    >>> result = get_unlock_info('600519.XSHG')
    >>> if result.success:
    >>>     df = result.data
    >>>     print(f"Got {len(df)} unlock records")
    """
    from jk2bt.data.finance.unlock import get_unlock_info as _get_unlock_info

    return _get_unlock_info(
        symbol,
        start_date=start_date,
        end_date=end_date,
        force_update=force_update,
    )


def get_unlock_calendar(
    date: Optional[str] = None,
    force_update: bool = False,
) -> pd.DataFrame:
    """
    Get market-wide unlock calendar for a specific date.

    JQData compatible interface

    Parameters
    ----------
    date : str, optional
        Query date, format 'YYYY-MM-DD', default today
    force_update : bool, optional
        Force update from network, default False

    Returns
    -------
    pd.DataFrame
        Unlock calendar data:
        - code: Stock code (JQData format)
        - unlock_date: Unlock date
        - unlock_amount: Unlock amount
        - unlock_ratio: Unlock ratio
        - unlock_type: Unlock type
        - holder_type: Holder type

    Examples
    --------
    >>> df = get_unlock_calendar('2024-01-15')
    >>> print(df.head())
    """
    from jk2bt.data.finance.unlock import get_unlock_calendar as _get_unlock_calendar

    result = _get_unlock_calendar(date=date, force_update=force_update)
    if result is None or result.empty:
        return pd.DataFrame(
            columns=[
                "code",
                "unlock_date",
                "unlock_amount",
                "unlock_ratio",
                "unlock_type",
                "holder_type",
            ]
        )
    return result


def get_unlock_schedule(
    symbol: str,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    force_update: bool = False,
) -> pd.DataFrame:
    """
    Get unlock schedule (alias interface).

    JQData compatible interface

    Parameters
    ----------
    symbol : str
        Stock code in any format
    start_date : str, optional
        Start date, format 'YYYY-MM-DD'
    end_date : str, optional
        End date, format 'YYYY-MM-DD'
    force_update : bool, optional
        Force update from network, default False

    Returns
    -------
    pd.DataFrame
        Unlock schedule data

    Examples
    --------
    >>> df = get_unlock_schedule('600519.XSHG')
    >>> print(df.head())
    """
    from jk2bt.data.finance.unlock import get_unlock_schedule as _get_unlock_schedule

    result = _get_unlock_schedule(
        symbol,
        start_date=start_date,
        end_date=end_date,
        force_update=force_update,
    )
    if result is None or result.empty:
        return pd.DataFrame(
            columns=[
                "code",
                "unlock_date",
                "unlock_amount",
                "unlock_ratio",
                "unlock_type",
                "holder_type",
            ]
        )
    return result


def get_unlock_pressure(
    symbol: str,
    days_ahead: int = 30,
    force_update: bool = False,
) -> dict:
    """
    Calculate unlock pressure indicator.

    JQData compatible interface

    Parameters
    ----------
    symbol : str
        Stock code in any format
    days_ahead : int, optional
        Number of days ahead to check, default 30
    force_update : bool, optional
        Force update from network, default False

    Returns
    -------
    dict
        Unlock pressure data:
        - code: Stock code
        - total_unlock_amount: Total unlock amount
        - total_unlock_value: Total unlock market value
        - pressure_level: Pressure level (high/medium/low/none)

    Examples
    --------
    >>> result = get_unlock_pressure('600519.XSHG', days_ahead=30)
    >>> print(result)
    """
    from jk2bt.data.finance.unlock import get_unlock_pressure as _get_unlock_pressure

    return _get_unlock_pressure(
        symbol,
        days_ahead=days_ahead,
        force_update=force_update,
    )


def get_unlock_history(
    security: str,
    years: int = 3,
    force_update: bool = False,
) -> pd.DataFrame:
    """
    Get historical unlock records.

    JQData compatible interface

    Parameters
    ----------
    security : str
        Stock code in any format
    years : int, optional
        Number of years to query, default 3
    force_update : bool, optional
        Force update from network, default False

    Returns
    -------
    pd.DataFrame
        Historical unlock data:
        - code: Stock code (JQData format)
        - unlock_date: Unlock date
        - unlock_amount: Unlock amount
        - unlock_ratio: Unlock ratio
        - unlock_type: Unlock type
        - holder_type: Holder type

    Examples
    --------
    >>> df = get_unlock_history('600519.XSHG', years=3)
    >>> print(df.head())
    """
    from jk2bt.data.finance.unlock import get_unlock_history as _get_unlock_history

    result = _get_unlock_history(
        security,
        years=years,
        force_update=force_update,
    )
    if result is None or result.empty:
        return pd.DataFrame(
            columns=[
                "code",
                "unlock_date",
                "unlock_amount",
                "unlock_ratio",
                "unlock_type",
                "holder_type",
            ]
        )
    return result


def get_upcoming_unlocks(
    days: int = 30,
    force_update: bool = False,
) -> pd.DataFrame:
    """
    Get list of stocks with upcoming unlocks.

    JQData compatible interface

    Parameters
    ----------
    days : int, optional
        Number of days ahead, default 30
    force_update : bool, optional
        Force update from network, default False

    Returns
    -------
    pd.DataFrame
        Upcoming unlocks data:
        - code: Stock code (JQData format)
        - unlock_date: Unlock date
        - unlock_amount: Unlock amount
        - unlock_ratio: Unlock ratio
        - unlock_type: Unlock type
        - unlock_market_value: Unlock market value (if available)

    Examples
    --------
    >>> df = get_upcoming_unlocks(days=30)
    >>> print(df.head())
    """
    from jk2bt.data.finance.unlock import get_upcoming_unlocks as _get_upcoming_unlocks

    result = _get_upcoming_unlocks(days=days, force_update=force_update)
    if result is None or result.empty:
        return pd.DataFrame(
            columns=[
                "code",
                "unlock_date",
                "unlock_amount",
                "unlock_ratio",
                "unlock_type",
                "unlock_market_value",
            ]
        )
    return result


def analyze_unlock_impact(
    security: str,
    force_update: bool = False,
) -> dict:
    """
    Analyze unlock impact on stock price.

    JQData compatible interface

    Parameters
    ----------
    security : str
        Stock code in any format
    force_update : bool, optional
        Force update from network, default False

    Returns
    -------
    dict
        Impact analysis:
        - code: Stock code
        - upcoming_unlocks: Number of upcoming unlocks (next 30 days)
        - total_unlock_amount: Total unlock amount
        - avg_unlock_ratio: Average unlock ratio
        - impact_level: Impact level (high/medium/low/none)
        - risk_factors: List of risk factors
        - historical_impact: Historical unlock impact analysis

    Examples
    --------
    >>> result = analyze_unlock_impact('600519.XSHG')
    >>> print(result)
    """
    from jk2bt.data.finance.unlock import (
        analyze_unlock_impact as _analyze_unlock_impact,
    )

    return _analyze_unlock_impact(
        security,
        force_update=force_update,
    )


__all__ = [
    "get_unlock_info",
    "get_unlock_calendar",
    "get_unlock_schedule",
    "get_unlock_pressure",
    "get_unlock_history",
    "get_upcoming_unlocks",
    "analyze_unlock_impact",
]
