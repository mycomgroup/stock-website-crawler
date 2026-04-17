"""
jk2bt/api/share_change.py
Share change data API module.

Provides JQData compatible interfaces for shareholder change data.
Data sources: AkShare

Main functions:
- get_pledge_info: Get share pledge information
- get_freeze_info: Get share freeze information
- get_capital_change: Get capital change information
- get_major_holder_trade: Get major holder trading information
- get_shareholder_changes: Get shareholder change data
- get_insider_trading: Get insider trading information
- get_major_shareholder_change: Get major shareholder change
"""

import pandas as pd
from typing import Optional


def get_pledge_info(
    symbol: str,
    force_update: bool = False,
) -> pd.DataFrame:
    """
    Get share pledge information.

    JQData compatible interface

    Parameters
    ----------
    symbol : str
        Stock code in any format (e.g. '000001.XSHE', 'sh600519', '600519')
    force_update : bool, optional
        Force update from network, default False

    Returns
    -------
    pd.DataFrame
        Share pledge data:
        - code: Stock code (JQData format)
        - pledge_date: Pledge date
        - pledgor: Pledgor name
        - pledgee: Pledgee name
        - pledge_amount: Pledge amount
        - pledge_ratio: Pledge ratio

    Examples
    --------
    >>> df = get_pledge_info('600519.XSHG')
    >>> print(df.head())
    """
    from jk2bt.data.finance.share_change import get_pledge_info as _get_pledge_info

    result = _get_pledge_info(symbol, force_update=force_update)
    if result is None or result.empty:
        return pd.DataFrame(
            columns=[
                "code",
                "pledge_date",
                "pledgor",
                "pledgee",
                "pledge_amount",
                "pledge_ratio",
            ]
        )
    return result


def get_freeze_info(
    symbol: str,
    force_update: bool = False,
) -> pd.DataFrame:
    """
    Get share freeze information.

    JQData compatible interface

    Parameters
    ----------
    symbol : str
        Stock code in any format
    force_update : bool, optional
        Force update from network, default False

    Returns
    -------
    pd.DataFrame
        Share freeze data:
        - code: Stock code (JQData format)
        - shareholder_name: Shareholder name
        - freeze_amount: Frozen shares
        - freeze_ratio: Freeze ratio
        - freeze_date: Freeze date
        - freeze_reason: Freeze reason
        - freeze_type: Freeze type
        - unfreeze_date: Unfreeze date

    Examples
    --------
    >>> df = get_freeze_info('000001.XSHE')
    >>> print(df.head())
    """
    from jk2bt.data.finance.share_change import get_freeze_info as _get_freeze_info

    result = _get_freeze_info(symbol, force_update=force_update)
    if result is None or result.empty:
        return pd.DataFrame(
            columns=[
                "code",
                "shareholder_name",
                "freeze_amount",
                "freeze_ratio",
                "freeze_date",
                "freeze_reason",
                "freeze_type",
                "unfreeze_date",
            ]
        )
    return result


def get_capital_change(
    symbol: str,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    force_update: bool = False,
    use_duckdb: bool = True,
) -> pd.DataFrame:
    """
    Get capital change information.

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
    use_duckdb : bool, optional
        Use DuckDB cache, default True

    Returns
    -------
    pd.DataFrame
        Capital change data:
        - code: Stock code (JQData format)
        - change_type: Change type
        - change_amount: Change amount
        - change_date: Change date
        - change_reason: Change reason
        - total_capital_before: Total capital before change
        - total_capital_after: Total capital after change
        - circulating_capital_before: Circulating capital before
        - circulating_capital_after: Circulating capital after

    Examples
    --------
    >>> df = get_capital_change('600519.XSHG', start_date='2023-01-01')
    >>> print(df.head())
    """
    from jk2bt.data.finance.share_change import (
        get_capital_change as _get_capital_change,
    )

    result = _get_capital_change(
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
                "change_type",
                "change_amount",
                "change_date",
                "change_reason",
                "total_capital_before",
                "total_capital_after",
                "circulating_capital_before",
                "circulating_capital_after",
            ]
        )
    return result


def get_major_holder_trade(
    symbol: str,
    force_update: bool = False,
) -> pd.DataFrame:
    """
    Get major holder trading information.

    JQData compatible interface

    Parameters
    ----------
    symbol : str
        Stock code in any format
    force_update : bool, optional
        Force update from network, default False

    Returns
    -------
    pd.DataFrame
        Major holder trade data:
        - code: Stock code (JQData format)
        - holder_name: Holder name
        - trade_date: Trade date
        - trade_type: Trade type (buy/sell)
        - trade_amount: Trade amount

    Examples
    --------
    >>> df = get_major_holder_trade('600519.XSHG')
    >>> print(df.head())
    """
    from jk2bt.data.finance.share_change import (
        get_major_holder_trade as _get_major_holder_trade,
    )

    result = _get_major_holder_trade(symbol, force_update=force_update)
    if result is None or result.empty:
        return pd.DataFrame(
            columns=["code", "holder_name", "trade_date", "trade_type", "trade_amount"]
        )
    return result


def get_shareholder_changes(
    code: str,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    force_update: bool = False,
    use_duckdb: bool = True,
):
    """
    Get shareholder change data (robust version).

    JQData compatible interface

    Parameters
    ----------
    code : str
        Stock code in any format
    start_date : str, optional
        Start date, format 'YYYY-MM-DD'
    end_date : str, optional
        End date, format 'YYYY-MM-DD'
    force_update : bool, optional
        Force update from network, default False
    use_duckdb : bool, optional
        Use DuckDB cache, default True

    Returns
    -------
    RobustResult
        Result object with:
        - success: Whether the query succeeded
        - data: DataFrame with shareholder change data
        - reason: Result description
        - source: Data source (cache/network/fallback)

    Examples
    --------
    >>> result = get_shareholder_changes('600519.XSHG', start_date='2023-01-01')
    >>> if result.success:
    >>>     df = result.data
    >>>     print(f"Got {len(df)} records")
    """
    from jk2bt.data.finance.share_change import (
        get_shareholder_changes as _get_shareholder_changes,
    )

    return _get_shareholder_changes(
        code,
        start_date=start_date,
        end_date=end_date,
        force_update=force_update,
        use_duckdb=use_duckdb,
    )


def get_insider_trading(
    security: str,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    force_update: bool = False,
) -> pd.DataFrame:
    """
    Get insider trading information.

    JQData compatible interface

    Parameters
    ----------
    security : str
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
        Insider trading data:
        - code: Stock code (JQData format)
        - insider_name: Insider name
        - position: Position/title
        - change_date: Change date
        - change_type: Change type (buy/sell)
        - change_amount: Change amount
        - change_ratio: Change ratio
        - hold_amount_after: Holding amount after change

    Examples
    --------
    >>> df = get_insider_trading('600519.XSHG', start_date='2023-01-01')
    >>> print(df.head())
    """
    from jk2bt.data.finance.share_change import (
        get_insider_trading as _get_insider_trading,
    )

    result = _get_insider_trading(
        security,
        start_date=start_date,
        end_date=end_date,
        force_update=force_update,
    )
    if result is None or result.empty:
        return pd.DataFrame(
            columns=[
                "code",
                "insider_name",
                "position",
                "change_date",
                "change_type",
                "change_amount",
                "change_ratio",
                "hold_amount_after",
            ]
        )
    return result


def get_major_shareholder_change(
    security: str,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    force_update: bool = False,
    use_duckdb: bool = True,
) -> pd.DataFrame:
    """
    Get major shareholder change information.

    JQData compatible interface

    Parameters
    ----------
    security : str
        Stock code in any format
    start_date : str, optional
        Start date, format 'YYYY-MM-DD'
    end_date : str, optional
        End date, format 'YYYY-MM-DD'
    force_update : bool, optional
        Force update from network, default False
    use_duckdb : bool, optional
        Use DuckDB cache, default True

    Returns
    -------
    pd.DataFrame
        Major shareholder change data

    Examples
    --------
    >>> df = get_major_shareholder_change('600519.XSHG')
    >>> print(df.head())
    """
    from jk2bt.data.finance.share_change import (
        get_major_shareholder_change as _get_major_shareholder_change,
    )

    result = _get_major_shareholder_change(
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
                "shareholder_name",
                "change_date",
                "change_type",
                "change_amount",
                "change_ratio",
                "hold_amount_after",
                "hold_ratio_after",
            ]
        )
    return result


__all__ = [
    "get_pledge_info",
    "get_freeze_info",
    "get_capital_change",
    "get_major_holder_trade",
    "get_shareholder_changes",
    "get_insider_trading",
    "get_major_shareholder_change",
]
