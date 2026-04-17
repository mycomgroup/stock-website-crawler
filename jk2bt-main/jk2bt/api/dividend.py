"""
jk2bt/api/dividend.py
Dividend Information API Module

JQData compatible interface for dividend and bonus data.
Data sources: AkShare

Main functions:
- get_dividend_info: Get dividend and bonus information
- get_dividend_history: Get historical dividend records
- get_stock_bonus: Get stock bonus information
- get_adjust_factor: Get adjustment factor
- get_rights_issue: Get rights issue information
- calculate_ex_rights_price: Calculate ex-rights price
"""

import pandas as pd
from typing import Optional, List, Dict, Union

from jk2bt.data.finance.dividend import (
    get_dividend_info as _get_dividend_info,
    get_dividend_history as _get_dividend_history,
    get_stock_bonus as _get_stock_bonus,
    get_adjust_factor as _get_adjust_factor,
    get_rights_issue as _get_rights_issue,
    calculate_ex_rights_price as _calculate_ex_rights_price,
    get_next_dividend as _get_next_dividend,
    query_dividend as _query_dividend,
)


def get_dividend_info(
    security: str,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    force_update: bool = False,
    use_duckdb: bool = True,
) -> pd.DataFrame:
    """
    Get dividend and bonus information.

    JQData compatible interface

    Parameters
    ----
    security : str
        Security code, supports formats:
        - '000001.XSHE' (JQData format)
        - '600519.XSHG' (JQData format)
        - 'sh600519' (akshare format)
        - '600519' (pure code)
    start_date : str, optional
        Start date (ex-dividend date)
    end_date : str, optional
        End date
    force_update : bool, optional
        Force update from network
    use_duckdb : bool, optional
        Use DuckDB cache (default True)

    Returns
    ----
    pd.DataFrame
        Dividend information with fields:
        - code: Security code (JQData format)
        - board_plan_pub_date: Board plan announcement date
        - bonus_ratio_rmb: Cash dividend per share (CNY)
        - transfer_ratio: Transfer ratio
        - bonus_share_ratio: Bonus share ratio
        - ex_dividend_date: Ex-dividend date
        - record_date: Record date
        - pay_date: Payment date
        - report_date: Report date
        - adjust_factor: Adjustment factor
        - dividend_type: Dividend type
        - company_name: Company name

    Examples
    ----
    >>> df = get_dividend_info('600519.XSHG')
    >>> df = get_dividend_info('600519.XSHG', start_date='2023-01-01', end_date='2024-01-01')
    """
    result = _get_dividend_info(
        security,
        start_date=start_date,
        end_date=end_date,
        force_update=force_update,
        use_duckdb=use_duckdb,
    )
    if result is None or result.empty:
        return pd.DataFrame(
            columns=[
                "code",
                "board_plan_pub_date",
                "bonus_ratio_rmb",
                "transfer_ratio",
                "bonus_share_ratio",
                "ex_dividend_date",
                "record_date",
                "pay_date",
                "report_date",
                "adjust_factor",
                "dividend_type",
                "company_name",
            ]
        )
    return result


def get_dividend_history(
    security: str,
    years: int = 5,
    force_update: bool = False,
) -> pd.DataFrame:
    """
    Get historical dividend records.

    JQData compatible interface

    Parameters
    ----
    security : str
        Security code
    years : int, optional
        Number of years to query (default 5)
    force_update : bool, optional
        Force update from network

    Returns
    ----
    pd.DataFrame
        Historical dividend statistics with fields:
        - code: Security code (JQData format)
        - year: Year
        - dividend_count: Number of dividends
        - total_dividend: Total dividend per share
        - avg_dividend: Average dividend per share
        - max_dividend: Maximum dividend per share
        - min_dividend: Minimum dividend per share

    Examples
    ----
    >>> df = get_dividend_history('600519.XSHG', years=5)
    """
    result = _get_dividend_history(security, years=years, force_update=force_update)
    if result is None or result.empty:
        return pd.DataFrame(
            columns=[
                "code",
                "year",
                "dividend_count",
                "total_dividend",
                "avg_dividend",
                "max_dividend",
                "min_dividend",
            ]
        )
    return result


def get_stock_bonus(
    security: str,
    force_update: bool = False,
) -> pd.DataFrame:
    """
    Get stock bonus (bonus shares) information.

    JQData compatible interface

    Parameters
    ----
    security : str
        Security code
    force_update : bool, optional
        Force update from network

    Returns
    ----
    pd.DataFrame
        Stock bonus information with fields:
        - code: Security code
        - bonus_share_ratio: Bonus share ratio
        - transfer_ratio: Transfer ratio
        - ex_dividend_date: Ex-dividend date
        - report_date: Report date

    Examples
    ----
    >>> df = get_stock_bonus('600519.XSHG')
    """
    result = _get_stock_bonus(security, force_update=force_update)
    if result is None or result.empty:
        return pd.DataFrame(
            columns=[
                "code",
                "bonus_share_ratio",
                "transfer_ratio",
                "ex_dividend_date",
                "report_date",
            ]
        )
    return result


def get_adjust_factor(
    symbol: str,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    force_update: bool = False,
    use_duckdb: bool = True,
) -> pd.DataFrame:
    """
    Get adjustment factor.

    JQData compatible interface

    Parameters
    ----
    symbol : str
        Security code
    start_date : str, optional
        Start date
    end_date : str, optional
        End date
    force_update : bool, optional
        Force update from network
    use_duckdb : bool, optional
        Use DuckDB cache (default True)

    Returns
    ----
    pd.DataFrame
        Adjustment factor data with fields:
        - code: Security code
        - ex_dividend_date: Ex-dividend date
        - adjust_factor: Adjustment factor
        - bonus_ratio_rmb: Cash dividend per share (CNY)
        - bonus_share_ratio: Bonus share ratio
        - transfer_ratio: Transfer ratio

    Examples
    ----
    >>> df = get_adjust_factor('600519.XSHG')
    """
    result = _get_adjust_factor(
        symbol,
        start_date=start_date,
        end_date=end_date,
        force_update=force_update,
        use_duckdb=use_duckdb,
    )
    if result is None or result.empty:
        return pd.DataFrame(
            columns=[
                "code",
                "ex_dividend_date",
                "adjust_factor",
                "bonus_ratio_rmb",
                "bonus_share_ratio",
                "transfer_ratio",
            ]
        )
    return result


def get_rights_issue(
    symbol: str,
    force_update: bool = False,
    use_duckdb: bool = True,
) -> pd.DataFrame:
    """
    Get rights issue information.

    JQData compatible interface

    Parameters
    ----
    symbol : str
        Security code
    force_update : bool, optional
        Force update from network
    use_duckdb : bool, optional
        Use DuckDB cache (default True)

    Returns
    ----
    pd.DataFrame
        Rights issue information with fields:
        - code: Security code
        - ex_dividend_date: Ex-dividend date
        - bonus_ratio_rmb: Cash dividend per share (CNY)
        - bonus_share_ratio: Bonus share ratio
        - transfer_ratio: Transfer ratio
        - record_date: Record date
        - rights_issue_ratio: Rights issue ratio (not supported yet)

    Examples
    ----
    >>> df = get_rights_issue('600519.XSHG')
    """
    result = _get_rights_issue(symbol, force_update=force_update, use_duckdb=use_duckdb)
    if result is None or result.empty:
        return pd.DataFrame(
            columns=[
                "code",
                "ex_dividend_date",
                "bonus_ratio_rmb",
                "bonus_share_ratio",
                "transfer_ratio",
                "record_date",
                "rights_issue_ratio",
            ]
        )
    return result


def calculate_ex_rights_price(
    price: float,
    dividend_info: Union[Dict, pd.DataFrame, pd.Series],
) -> float:
    """
    Calculate ex-rights price.

    JQData compatible interface

    Parameters
    ----
    price : float
        Original price (closing price)
    dividend_info : dict, DataFrame, or Series
        Dividend information

    Returns
    ----
    float
        Ex-rights price

    Formula
    ----
    Ex-rights price = (Original price - Cash dividend per share) / (1 + Bonus share ratio + Transfer ratio)

    Examples
    ----
    >>> df = get_dividend_info('600519.XSHG')
    >>> ex_price = calculate_ex_rights_price(1800.0, df.iloc[0])
    """
    return _calculate_ex_rights_price(price, dividend_info)


__all__ = [
    "get_dividend_info",
    "get_dividend_history",
    "get_stock_bonus",
    "get_adjust_factor",
    "get_rights_issue",
    "calculate_ex_rights_price",
]
