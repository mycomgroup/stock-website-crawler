"""
jk2bt/api/macro.py
Macro economic data API module

Provides JQData compatible interfaces for macro economic data.
Data sources: AkShare

Functions:
- get_macro_gdp: GDP data
- get_macro_cpi: CPI inflation data
- get_macro_ppi: PPI data
- get_macro_pmi: PMI data
- get_macro_m2: M2 money supply
- get_macro_interest_rate: Interest rate data
- get_macro_exchange_rate: Exchange rate data
- get_macro_data: General macro data query
"""

import pandas as pd
from typing import Optional

from jk2bt.data.finance.macro import get_macro_gdp as _get_macro_gdp
from jk2bt.data.finance.macro import get_macro_cpi as _get_macro_cpi
from jk2bt.data.finance.macro import get_macro_ppi as _get_macro_ppi
from jk2bt.data.finance.macro import get_macro_china_pmi as _get_macro_china_pmi
from jk2bt.data.finance.macro import get_macro_m2 as _get_macro_m2
from jk2bt.data.finance.macro import get_macro_interest_rate as _get_macro_interest_rate
from jk2bt.data.finance.macro import (
    get_macro_china_exchange_rate as _get_macro_china_exchange_rate,
)
from jk2bt.data.finance.macro import get_macro_data as _get_macro_data


_ETF_SCHEMA = ["indicator", "date", "value", "unit", "YoY", "MoM"]


def get_macro_gdp(
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    force_update: bool = False,
) -> pd.DataFrame:
    """
    Get China GDP data.

    JQData compatible interface

    Parameters
    ----
    start_date : str, optional
        Start date
    end_date : str, optional
        End date
    force_update : bool
        Force refresh

    Returns
    ----
    pd.DataFrame
        GDP data with columns: indicator, date, value, unit, YoY, MoM
    """
    try:
        df = _get_macro_gdp(force_update=force_update)
        if df.empty:
            return pd.DataFrame(columns=_ETF_SCHEMA)
        if start_date:
            df = df[df["date"] >= pd.to_datetime(start_date)]
        if end_date:
            df = df[df["date"] <= pd.to_datetime(end_date)]
        return df
    except Exception:
        return pd.DataFrame(columns=_ETF_SCHEMA)


def get_macro_cpi(
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    force_update: bool = False,
) -> pd.DataFrame:
    """
    Get China CPI data.

    JQData compatible interface

    Parameters
    ----
    start_date : str, optional
        Start date
    end_date : str, optional
        End date
    force_update : bool
        Force refresh

    Returns
    ----
    pd.DataFrame
        CPI data with columns: indicator, date, value, unit, YoY, MoM
    """
    try:
        df = _get_macro_cpi(force_update=force_update)
        if df.empty:
            return pd.DataFrame(columns=_ETF_SCHEMA)
        if start_date:
            df = df[df["date"] >= pd.to_datetime(start_date)]
        if end_date:
            df = df[df["date"] <= pd.to_datetime(end_date)]
        return df
    except Exception:
        return pd.DataFrame(columns=_ETF_SCHEMA)


def get_macro_ppi(
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    force_update: bool = False,
) -> pd.DataFrame:
    """
    Get China PPI data.

    JQData compatible interface

    Parameters
    ----
    start_date : str, optional
        Start date
    end_date : str, optional
        End date
    force_update : bool
        Force refresh

    Returns
    ----
    pd.DataFrame
        PPI data with columns: indicator, date, value, unit, YoY, MoM
    """
    try:
        df = _get_macro_ppi(force_update=force_update)
        if df.empty:
            return pd.DataFrame(columns=_ETF_SCHEMA)
        if start_date:
            df = df[df["date"] >= pd.to_datetime(start_date)]
        if end_date:
            df = df[df["date"] <= pd.to_datetime(end_date)]
        return df
    except Exception:
        return pd.DataFrame(columns=_ETF_SCHEMA)


def get_macro_pmi(
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    force_update: bool = False,
) -> pd.DataFrame:
    """
    Get China PMI data.

    JQData compatible interface

    Parameters
    ----
    start_date : str, optional
        Start date
    end_date : str, optional
        End date
    force_update : bool
        Force refresh

    Returns
    ----
    pd.DataFrame
        PMI data with columns: indicator, date, value, unit, YoY, MoM
    """
    try:
        df = _get_macro_china_pmi(
            start_date=start_date,
            end_date=end_date,
            force_update=force_update,
        )
        if df.empty:
            return pd.DataFrame(columns=_ETF_SCHEMA)
        return df
    except Exception:
        return pd.DataFrame(columns=_ETF_SCHEMA)


def get_macro_m2(
    force_update: bool = False,
) -> pd.DataFrame:
    """
    Get China M2 money supply data.

    JQData compatible interface

    Parameters
    ----
    force_update : bool
        Force refresh

    Returns
    ----
    pd.DataFrame
        M2 data with columns: indicator, date, value, unit, YoY, MoM
    """
    try:
        df = _get_macro_m2(force_update=force_update)
        if df.empty:
            return pd.DataFrame(columns=_ETF_SCHEMA)
        return df
    except Exception:
        return pd.DataFrame(columns=_ETF_SCHEMA)


def get_macro_interest_rate(
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    force_update: bool = False,
) -> pd.DataFrame:
    """
    Get China interest rate data (PBOC benchmark rate).

    JQData compatible interface

    Parameters
    ----
    start_date : str, optional
        Start date
    end_date : str, optional
        End date
    force_update : bool
        Force refresh

    Returns
    ----
    pd.DataFrame
        Interest rate data with columns: indicator, date, value, unit, YoY, MoM
    """
    try:
        df = _get_macro_interest_rate(force_update=force_update)
        if df.empty:
            return pd.DataFrame(columns=_ETF_SCHEMA)
        if start_date:
            df = df[df["date"] >= pd.to_datetime(start_date)]
        if end_date:
            df = df[df["date"] <= pd.to_datetime(end_date)]
        return df
    except Exception:
        return pd.DataFrame(columns=_ETF_SCHEMA)


def get_macro_exchange_rate(
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    force_update: bool = False,
) -> pd.DataFrame:
    """
    Get China exchange rate data (RMB exchange rate).

    JQData compatible interface

    Parameters
    ----
    start_date : str, optional
        Start date
    end_date : str, optional
        End date
    force_update : bool
        Force refresh

    Returns
    ----
    pd.DataFrame
        Exchange rate data with columns: indicator, date, value, unit, YoY, MoM
    """
    try:
        df = _get_macro_china_exchange_rate(
            start_date=start_date,
            end_date=end_date,
            force_update=force_update,
        )
        if df.empty:
            return pd.DataFrame(columns=_ETF_SCHEMA)
        return df
    except Exception:
        return pd.DataFrame(columns=_ETF_SCHEMA)


def get_macro_data(
    indicator_type: str,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    force_update: bool = False,
) -> pd.DataFrame:
    """
    Get macro economic indicator data (unified interface).

    JQData compatible interface

    Parameters
    ----
    indicator_type : str
        Indicator type, supports: cpi, ppi, gdp, m2, interest_rate
    start_date : str, optional
        Start date
    end_date : str, optional
        End date
    force_update : bool
        Force refresh

    Returns
    ----
    pd.DataFrame
        Macro data with columns: indicator, date, value, unit, YoY, MoM
    """
    try:
        df = _get_macro_data(
            indicator_type=indicator_type,
            start_date=start_date,
            end_date=end_date,
            force_update=force_update,
        )
        if df.empty:
            return pd.DataFrame(columns=_ETF_SCHEMA)
        return df
    except Exception:
        return pd.DataFrame(columns=_ETF_SCHEMA)


__all__ = [
    "get_macro_gdp",
    "get_macro_cpi",
    "get_macro_ppi",
    "get_macro_pmi",
    "get_macro_m2",
    "get_macro_interest_rate",
    "get_macro_exchange_rate",
    "get_macro_data",
]
