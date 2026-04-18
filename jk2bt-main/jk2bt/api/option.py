"""
jk2bt/api/option.py
Options API module - JQData compatible interface.

Provides JoinQuant compatible options data query interfaces.
Data source: AkShare + local data layer

Main functions:
- get_option_list: Get options contract list
- get_option_price: Get options quote/price
- get_option_daily: Get options daily bar data
- get_option_greeks: Get Greeks risk indicators
- get_option_info: Get options contract info
- get_option_chain: Get options chain
- get_option: Get single option data
- calculate_option_implied_vol: Calculate implied volatility
- get_option_quote: Get options quote
- query_option: Batch query options
- get_option_ticks: Get options tick data
- get_option_preopen: Get options preopen static data
"""

import pandas as pd
from typing import List, Optional

from jk2bt.data.market.option import (
    get_option_list as _get_option_list,
    get_option_price as _get_option_price,
    get_option_daily as _get_option_daily,
    get_option_greeks as _get_option_greeks,
    get_option_info as _get_option_info,
    get_option_chain as _get_option_chain,
    get_option as _get_option,
    calculate_option_implied_vol as _calculate_option_implied_vol,
    query_option as _query_option,
    get_option_ticks as _get_option_ticks,
    get_option_preopen as _get_option_preopen,
    _OPTION_SCHEMA,
    _OPTION_BASIC_SCHEMA,
    _OPTION_DAILY_SCHEMA,
    _GREEKS_SCHEMA,
    _OPTION_TICK_SCHEMA,
    _OPT_DAILY_PREOPEN_SCHEMA,
)


def get_option_list(
    underlying: str = "sse",
    force_update: bool = False,
    use_duckdb: bool = True,
    use_cache: bool = True,
) -> pd.DataFrame:
    """
    Get options contract list.

    JQData compatible interface

    Parameters
    ----
    underlying : str
        Underlying type: 'sse' (SSE ETF options), 'szse' (SZSE ETF options),
        'cffex' (CFFEX index options), 'all'
    force_update : bool
        Force update from network
    use_duckdb : bool
        Use DuckDB cache
    use_cache : bool
        Use cache

    Returns
    ----
    pd.DataFrame
        Options contract list with columns:
        - option_code: Option code
        - option_name: Option name
        - underlying_code: Underlying code
        - underlying: Underlying code (alias)
        - underlying_name: Underlying name
        - strike: Strike price
        - expiry_date: Expiry date
        - option_type: Option type (Call/Put)
        - contract_unit: Contract unit
        - exercise_type: Exercise type
        - listing_date: Listing date
        - close: Close price
        - volume: Volume
        - date: Date

    Examples
    ----
    >>> df = get_option_list('sse')
    >>> df = get_option_list('all')
    """
    result = _get_option_list(
        underlying=underlying,
        force_update=force_update,
        use_duckdb=use_duckdb,
        use_cache=use_cache,
    )
    if result.success and result.data is not None:
        return result.data
    return pd.DataFrame(columns=_OPTION_SCHEMA)


def get_option_price(
    option_code: str,
    force_update: bool = False,
    use_cache: bool = True,
) -> pd.DataFrame:
    """
    Get options real-time quote.

    JQData compatible interface

    Parameters
    ----
    option_code : str
        Option code
    force_update : bool
        Force update from network
    use_cache : bool
        Use cache

    Returns
    ----
    pd.DataFrame
        Options quote data with columns:
        - option_code: Option code
        - option_name: Option name
        - trade_code: Trade code
        - underlying: Underlying code
        - option_type: Option type
        - strike: Strike price
        - contract_unit: Contract unit
        - expiry_date: Expiry date
        - date: Date

    Examples
    ----
    >>> df = get_option_price('10004012')
    """
    result = _get_option_price(
        option_code=option_code,
        force_update=force_update,
        use_cache=use_cache,
    )
    if result.success and result.data is not None:
        return result.data
    return pd.DataFrame(columns=_OPTION_SCHEMA)


def get_option_daily(
    option_code: str,
    start_date: str = None,
    end_date: str = None,
    force_update: bool = False,
    use_cache: bool = True,
) -> pd.DataFrame:
    """
    Get options daily bar data.

    JQData compatible interface

    Parameters
    ----
    option_code : str
        Option code
    start_date : str, optional
        Start date, format 'YYYY-MM-DD'
    end_date : str, optional
        End date, format 'YYYY-MM-DD'
    force_update : bool
        Force update from network
    use_cache : bool
        Use cache

    Returns
    ----
    pd.DataFrame
        Daily bar data with columns:
        - option_code: Option code
        - date: Date
        - open: Open price
        - high: High price
        - low: Low price
        - close: Close price
        - volume: Volume

    Examples
    ----
    >>> df = get_option_daily('10004012', start_date='2024-01-01', end_date='2024-12-31')
    """
    result = _get_option_daily(
        option_code=option_code,
        start_date=start_date,
        end_date=end_date,
        force_update=force_update,
        use_cache=use_cache,
    )
    if result.success and result.data is not None:
        return result.data
    return pd.DataFrame(columns=_OPTION_DAILY_SCHEMA)


def get_option_greeks(
    option_code: str,
    force_update: bool = False,
    use_cache: bool = True,
) -> pd.DataFrame:
    """
    Get options Greeks risk indicators.

    JQData compatible interface

    Parameters
    ----
    option_code : str
        Option code
    force_update : bool
        Force update from network
    use_cache : bool
        Use cache

    Returns
    ----
    pd.DataFrame
        Greeks data with columns:
        - option_code: Option code
        - option_name: Option name
        - delta: Delta
        - gamma: Gamma
        - theta: Theta
        - vega: Vega
        - implied_vol: Implied volatility
        - strike: Strike price
        - last_price: Last price
        - theoretical_value: Theoretical value
        - date: Date

    Examples
    ----
    >>> df = get_option_greeks('10004012')
    """
    result = _get_option_greeks(
        option_code=option_code,
        force_update=force_update,
        use_cache=use_cache,
    )
    if result.success and result.data is not None:
        return result.data
    return pd.DataFrame(columns=_GREEKS_SCHEMA)


def get_option_info(
    option_code: str,
    force_update: bool = False,
    use_cache: bool = True,
) -> pd.DataFrame:
    """
    Get options contract details.

    JQData compatible interface

    Parameters
    ----
    option_code : str
        Option code
    force_update : bool
        Force update from network
    use_cache : bool
        Use cache

    Returns
    ----
    pd.DataFrame
        Contract details with columns:
        - option_code: Option code
        - option_name: Option name
        - underlying: Underlying code
        - strike: Strike price
        - expiry_date: Expiry date
        - option_type: Option type
        - trade_code: Trade code
        - contract_unit: Contract unit
        - date: Date

    Examples
    ----
    >>> df = get_option_info('10004012')
    """
    result = _get_option_info(
        option_code=option_code,
        force_update=force_update,
        use_cache=use_cache,
    )
    if result.success and result.data is not None:
        return result.data
    return pd.DataFrame(columns=_OPTION_BASIC_SCHEMA)


def get_option_chain(
    underlying: str,
    expiry_date: str = None,
    force_update: bool = False,
) -> pd.DataFrame:
    """
    Get options chain data.

    JQData compatible interface

    Parameters
    ----
    underlying : str
        Underlying code (e.g. '510050', '159915')
    expiry_date : str, optional
        Expiry date filter
    force_update : bool
        Force update from network

    Returns
    ----
    pd.DataFrame
        Options chain data

    Examples
    ----
    >>> df = get_option_chain('510050')
    >>> df = get_option_chain('510050', expiry_date='2024-03-27')
    """
    result = _get_option_chain(
        underlying=underlying,
        expiry_date=expiry_date,
        force_update=force_update,
    )
    if result.success and result.data is not None:
        return result.data
    return pd.DataFrame(columns=_OPTION_SCHEMA)


def get_option(
    option_code: str,
    force_update: bool = False,
    use_duckdb: bool = True,
) -> pd.DataFrame:
    """
    Get single option data (legacy interface compatible).

    JQData compatible interface

    Parameters
    ----
    option_code : str
        Option code
    force_update : bool
        Force update from network
    use_duckdb : bool
        Use DuckDB cache

    Returns
    ----
    pd.DataFrame
        Single option data

    Examples
    ----
    >>> df = get_option('10004012')
    """
    df = _get_option(
        option_code=option_code,
        force_update=force_update,
        use_duckdb=use_duckdb,
    )
    if df is not None and not df.empty:
        return df
    return pd.DataFrame(columns=_OPTION_SCHEMA)


def calculate_option_implied_vol(
    option_code: str,
    price: float,
    underlying_price: float = None,
    risk_free_rate: float = 0.03,
    force_update: bool = False,
) -> dict:
    """
    Calculate options implied volatility using Black-Scholes model.

    JQData compatible interface

    Parameters
    ----
    option_code : str
        Option code
    price : float
        Current option price
    underlying_price : float, optional
        Underlying asset price (auto-fetch if not provided)
    risk_free_rate : float
        Risk-free interest rate (default 3%)
    force_update : bool
        Force update from network

    Returns
    ----
    dict
        Result containing:
        - success: bool
        - option_code: str
        - price: float
        - strike: float
        - underlying_price: float
        - time_to_expiry: float
        - implied_vol: float
        - risk_free_rate: float
        - delta, gamma, theta, vega: float (optional)
        - reason: str (if failed)

    Examples
    ----
    >>> result = calculate_option_implied_vol('10004012', 0.5, underlying_price=3.0)
    >>> print(result['implied_vol'])
    """
    return _calculate_option_implied_vol(
        option_code=option_code,
        price=price,
        underlying_price=underlying_price,
        risk_free_rate=risk_free_rate,
        force_update=force_update,
    )


def get_option_quote(
    option_code: str,
    force_update: bool = False,
) -> pd.DataFrame:
    """
    Get options quote data (legacy interface compatible).

    JQData compatible interface

    Parameters
    ----
    option_code : str
        Option code
    force_update : bool
        Force update from network

    Returns
    ----
    pd.DataFrame
        Options quote data

    Examples
    ----
    >>> df = get_option_quote('10004012')
    """
    return get_option(option_code, force_update=force_update)


def query_option(
    option_codes: List[str],
    force_update: bool = False,
    use_duckdb: bool = True,
) -> pd.DataFrame:
    """
    Batch query options (finance.STK_OPTION_DAILY compatible).

    JQData compatible interface

    Parameters
    ----
    option_codes : list of str
        List of option codes
    force_update : bool
        Force update from network
    use_duckdb : bool
        Use DuckDB cache

    Returns
    ----
    pd.DataFrame
        Batch query results

    Examples
    ----
    >>> df = query_option(['10004012', '10004013'])
    """
    df = _query_option(
        option_codes=option_codes,
        force_update=force_update,
        use_duckdb=use_duckdb,
    )
    if df is not None and not df.empty:
        return df
    return pd.DataFrame(columns=_OPTION_SCHEMA)


def get_option_ticks(
    option_code: str,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    exchange: Optional[str] = None,
) -> pd.DataFrame:
    """
    Get option tick data.

    JQData compatible interface

    Parameters
    ----
    option_code : str
        Option code
    start_date : str, optional
        Start date, format 'YYYY-MM-DD'
    end_date : str, optional
        End date, format 'YYYY-MM-DD'
    exchange : str, optional
        Exchange: 'sse' (SSE ETF options), 'szse' (SZSE ETF options),
        'czce' (CZCE commodity options), 'shfe' (SHFE), 'dce' (DCE),
        'cffex' (CFFEX index options)

    Returns
    ----
    pd.DataFrame
        Tick data with columns:
        - datetime: Timestamp
        - option_code: Option code
        - price: Last price
        - volume: Volume
        - bid_price1~5: Bid prices
        - ask_price1~5: Ask prices
        - bid_volume1~5: Bid volumes
        - ask_volume1~5: Ask volumes

    Examples
    ----
    >>> df = get_option_ticks('10004012')
    >>> df = get_option_ticks('510050C2403M02800', exchange='sse')
    """
    result = _get_option_ticks(
        option_code=option_code,
        start_date=start_date,
        end_date=end_date,
        exchange=exchange,
    )
    if result.success and result.data is not None:
        return result.data
    return pd.DataFrame(columns=_OPTION_TICK_SCHEMA)


def get_option_preopen(
    date: Optional[str] = None,
    exchange: Optional[str] = None,
) -> pd.DataFrame:
    """
    Get option daily preopen static data.

    JQData compatible interface

    Parameters
    ----
    date : str, optional
        Date, format 'YYYY-MM-DD', default today
    exchange : str, optional
        Exchange: 'sse', 'szse', 'cffex', 'all'

    Returns
    ----
    pd.DataFrame
        Preopen data with columns:
        - date: Date
        - option_code: Option code
        - option_name: Option name
        - underlying_code: Underlying code
        - pre_settle: Previous settlement price
        - pre_close: Previous close price
        - pre_position: Previous open interest
        - limit_up: Limit up price
        - limit_down: Limit down price

    Examples
    ----
    >>> df = get_option_preopen()
    >>> df = get_option_preopen(date='2024-03-01', exchange='sse')
    """
    result = _get_option_preopen(
        date=date,
        exchange=exchange,
    )
    if result.success and result.data is not None:
        return result.data
    preopen_schema = [
        "date",
        "option_code",
        "option_name",
        "underlying_code",
        "pre_settle",
        "pre_close",
        "pre_position",
        "limit_up",
        "limit_down",
    ]
    return pd.DataFrame(columns=preopen_schema)


def get_option_adjustment(option_code: str) -> pd.DataFrame:
    """
    获取期权合约调整记录。

    NotImplementedError: 期权调整记录需要专业数据源。
    """
    raise NotImplementedError(
        "opt.OPT_ADJUSTMENT 需要专业数据源（如聚宽JQData）。"
        "请替换为其他数据源（如Tushare/Wind/交易所API）。"
    )


def get_option_exercise_info(option_code: str) -> pd.DataFrame:
    """
    获取期权行权交收信息。

    NotImplementedError: 期权行权交收信息需要专业数据源。
    """
    raise NotImplementedError(
        "opt.OPT_EXERCISE_INFO 需要专业数据源（如聚宽JQData）。请替换为其他数据源。"
    )


def get_option_trade_rank(exchange: str, date: str) -> pd.DataFrame:
    """
    获取期权交易和持仓排名统计。

    NotImplementedError: 期权交易排名需要专业数据源。
    """
    raise NotImplementedError(
        "opt.OPT_TRADE_RANK_STK 需要专业数据源（如聚宽JQData）。请替换为其他数据源。"
    )


def get_commodity_option_ticks(option_code: str, date: str) -> pd.DataFrame:
    """
    获取商品期权Tick数据。

    NotImplementedError: 商品期权Tick数据需要专业数据源。
    """
    raise NotImplementedError(
        "商品期权Tick数据需要专业数据源（如聚宽JQData）。"
        "当前akshare仅提供金融期权Tick。请替换为其他数据源。"
    )


class OPT_RISK_INDICATOR:
    """期权风险指标表"""

    date = None
    option_code = None
    delta = None
    gamma = None
    theta = None
    vega = None
    rho = None
    implied_vol = None
    time_value = None
    intrinsic_value = None


__all__ = [
    "get_option_list",
    "get_option_price",
    "get_option_daily",
    "get_option_greeks",
    "get_option_info",
    "get_option_chain",
    "get_option",
    "calculate_option_implied_vol",
    "get_option_quote",
    "query_option",
    "get_option_ticks",
    "get_option_preopen",
    "get_option_adjustment",
    "get_option_exercise_info",
    "get_option_trade_rank",
    "get_commodity_option_ticks",
    "OPT_RISK_INDICATOR",
]
