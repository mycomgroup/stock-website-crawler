"""
jk2bt/api/company_info.py
Company Information API Module

JQData compatible interface for company basic information.
Data sources: AkShare

Main functions:
- get_company_info: Get company basic information
- get_security_status: Get securities trading status
- get_listing_info: Get listing information
- get_company_info_list: Batch get company information
"""

import pandas as pd
from typing import Optional, List, Dict, Union

from jk2bt.data.finance.company_info import (
    get_company_info as _get_company_info,
    get_security_status as _get_security_status,
    get_listing_info as _get_listing_info,
    get_company_info_list as _get_company_info_list,
    get_industry_info as _get_industry_info,
    get_management_info as _get_management_info,
    get_employee_info as _get_employee_info,
    get_name_history as _get_name_history,
)


def get_company_info(
    symbol: Union[str, List[str]],
    force_update: bool = False,
    use_duckdb: bool = True,
) -> pd.DataFrame:
    """
    Get company basic information.

    JQData compatible interface

    Parameters
    ----
    symbol : str or list of str
        Security code, supports multiple formats:
        - '000001.XSHE' (JQData format)
        - '600519.XSHG' (JQData format)
        - 'sh600519' (akshare format)
        - '600519' (pure code)
    force_update : bool, optional
        Force update from network
    use_duckdb : bool, optional
        Use DuckDB cache (default True)

    Returns
    ----
    pd.DataFrame
        Company information with fields:
        - code: Security code (JQData format)
        - company_name: Company name
        - establish_date: Establishment date
        - list_date: Listing date
        - main_business: Main business
        - industry: Industry
        - registered_address: Registered address
        - company_status: Company status

    Examples
    ----
    >>> df = get_company_info('600519.XSHG')
    >>> df = get_company_info(['600519.XSHG', '000001.XSHE'])
    """
    result = _get_company_info(symbol, force_update=force_update, use_duckdb=use_duckdb)
    if result is None or result.empty:
        return pd.DataFrame(
            columns=[
                "code",
                "company_name",
                "establish_date",
                "list_date",
                "main_business",
                "industry",
                "registered_address",
                "company_status",
                "status_change_date",
                "change_type",
            ]
        )
    return result


def get_security_status(
    symbol: str,
    date: Optional[str] = None,
    force_update: bool = False,
    use_duckdb: bool = True,
) -> pd.DataFrame:
    """
    Get securities trading status (suspension, resumption, delisting, etc.).

    JQData compatible interface

    Parameters
    ----
    symbol : str
        Security code
    date : str, optional
        Query date in 'YYYY-MM-DD' or 'YYYYMMDD' format, default recent trading day
    force_update : bool, optional
        Force update from network
    use_duckdb : bool, optional
        Use DuckDB cache (default True)

    Returns
    ----
    pd.DataFrame
        Status information with fields:
        - code: Security code (JQData format)
        - status_date: Status date
        - status_type: Status type (normal, suspended, resumed, delisted, etc.)
        - reason: Reason for status change

    Examples
    ----
    >>> df = get_security_status('600519.XSHG', date='2024-01-01')
    """
    result = _get_security_status(
        symbol, date=date, force_update=force_update, use_duckdb=use_duckdb
    )
    if result is None or result.empty:
        return pd.DataFrame(columns=["code", "status_date", "status_type", "reason"])
    return result


def get_listing_info(
    symbol: Optional[str] = None,
    symbols: Optional[List[str]] = None,
    force_update: bool = False,
) -> pd.DataFrame:
    """
    Get stock listing information (STK_LIST).

    JQData compatible interface

    Parameters
    ----
    symbol : str, optional
        Single security code
    symbols : list of str, optional
        Multiple security codes
    force_update : bool, optional
        Force update from network

    Returns
    ----
    pd.DataFrame
        Listing information with fields:
        - code: Security code (JQData format)
        - name: Security name
        - start_date: Listing date
        - state_id: Status code (301001=normal, 301002=suspended, 301003=delisted)
        - state: Status description

    Examples
    ----
    >>> df = get_listing_info('600519.XSHG')
    >>> df = get_listing_info(symbols=['600519.XSHG', '000001.XSHE'])
    """
    result = _get_listing_info(
        symbol=symbol, symbols=symbols, force_update=force_update
    )
    if result is None or result.empty:
        return pd.DataFrame(columns=["code", "name", "start_date", "state_id", "state"])
    return result


def get_company_info_list(
    securities: List[str],
    force_update: bool = False,
    use_duckdb: bool = True,
) -> Dict[str, pd.DataFrame]:
    """
    Batch get company information, return dict format.

    JQData compatible interface

    Parameters
    ----
    securities : list of str
        Security code list, e.g. ['600000.XSHG', '000001.XSHE']
    force_update : bool, optional
        Force update from network
    use_duckdb : bool, optional
        Use DuckDB cache (default True)

    Returns
    ----
    dict{security: DataFrame}
        Each security corresponds to a DataFrame

    Examples
    ----
    >>> result = get_company_info_list(['600519.XSHG', '000001.XSHE'])
    >>> df_600519 = result['600519.XSHG']
    """
    if securities is None or len(securities) == 0:
        return {}

    result_dict = _get_company_info_list(
        securities, force_update=force_update, use_duckdb=use_duckdb
    )

    for key in result_dict:
        if result_dict[key] is None or result_dict[key].empty:
            result_dict[key] = pd.DataFrame(
                columns=[
                    "code",
                    "company_name",
                    "establish_date",
                    "list_date",
                    "main_business",
                    "industry",
                    "registered_address",
                    "company_status",
                    "status_change_date",
                    "change_type",
                ]
            )

    return result_dict


def get_industry_info(
    security: str,
    force_update: bool = False,
) -> pd.DataFrame:
    """
    Get industry information.

    JQData compatible interface

    Parameters
    ----
    security : str
        Security code, e.g. '600000.XSHG'
    force_update : bool, optional
        Force update

    Returns
    ----
    pd.DataFrame
        Industry information with fields:
        - code: Security code (JQData format)
        - industry_code: Industry code
        - industry_name: Industry name
        - industry_level: Industry level

    Examples
    ----
    >>> df = get_industry_info('600519.XSHG')
    >>> print(df['industry_name'])
    """
    result = _get_industry_info(security, force_update=force_update)
    if result is None or result.empty:
        return pd.DataFrame(
            columns=["code", "industry_code", "industry_name", "industry_level"]
        )
    return result


def get_management_info(
    symbol: str,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    force_update: bool = False,
    use_duckdb: bool = True,
) -> pd.DataFrame:
    """
    Get company management personnel information.

    JQData compatible interface

    Parameters
    ----
    symbol : str
        Security code, e.g. '600519.XSHG'
    start_date : str, optional
        Start date in 'YYYY-MM-DD' format
    end_date : str, optional
        End date in 'YYYY-MM-DD' format
    force_update : bool, optional
        Force update from network
    use_duckdb : bool, optional
        Use DuckDB cache (default True)

    Returns
    ----
    pd.DataFrame
        Management information with fields:
        - code: Security code (JQData format)
        - name: Executive name
        - position: Position/title
        - gender: Gender
        - education: Education level
        - start_date: Start date of tenure
        - end_date: End date of tenure
        - shares_held: Number of shares held
        - compensation: Annual compensation

    Examples
    ----
    >>> df = get_management_info('600519.XSHG')
    >>> df = get_management_info('000001.XSHE', start_date='2020-01-01')
    """
    result = _get_management_info(
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
                "name",
                "position",
                "gender",
                "education",
                "start_date",
                "end_date",
                "shares_held",
                "compensation",
            ]
        )
    return result


def get_employee_info(
    symbol: str,
    year: Optional[int] = None,
    force_update: bool = False,
    use_duckdb: bool = True,
) -> pd.DataFrame:
    """
    Get company employee information.

    JQData compatible interface

    Parameters
    ----
    symbol : str
        Security code, e.g. '600519.XSHG'
    year : int, optional
        Report year, e.g. 2023
    force_update : bool, optional
        Force update from network
    use_duckdb : bool, optional
        Use DuckDB cache (default True)

    Returns
    ----
    pd.DataFrame
        Employee information with fields:
        - code: Security code (JQData format)
        - report_date: Report date
        - employee_count: Total employee count
        - professional_count: Professional staff count
        - production_count: Production staff count
        - sales_count: Sales staff count
        - finance_count: Finance staff count
        - admin_count: Administrative staff count
        - education_bachelor: Bachelor degree count
        - education_master: Master degree count
        - education_phd: PhD degree count

    Examples
    ----
    >>> df = get_employee_info('600519.XSHG')
    >>> df = get_employee_info('000001.XSHE', year=2023)
    """
    result = _get_employee_info(
        symbol,
        year=year,
        force_update=force_update,
        use_duckdb=use_duckdb,
    )
    if result is None or result.empty:
        return pd.DataFrame(
            columns=[
                "code",
                "report_date",
                "employee_count",
                "professional_count",
                "production_count",
                "sales_count",
                "finance_count",
                "admin_count",
                "education_bachelor",
                "education_master",
                "education_phd",
            ]
        )
    return result


def get_name_history(
    symbol: str,
    force_update: bool = False,
    use_duckdb: bool = True,
) -> pd.DataFrame:
    """
    Get company name change history.

    JQData compatible interface

    Parameters
    ----
    symbol : str
        Security code, e.g. '600519.XSHG'
    force_update : bool, optional
        Force update from network
    use_duckdb : bool, optional
        Use DuckDB cache (default True)

    Returns
    ----
    pd.DataFrame
        Name history with fields:
        - code: Security code (JQData format)
        - name: Historical name
        - start_date: Start date of name usage
        - end_date: End date of name usage
        - change_reason: Reason for name change

    Examples
    ----
    >>> df = get_name_history('600519.XSHG')
    """
    result = _get_name_history(
        symbol,
        force_update=force_update,
        use_duckdb=use_duckdb,
    )
    if result is None or result.empty:
        return pd.DataFrame(
            columns=["code", "name", "start_date", "end_date", "change_reason"]
        )
    return result


__all__ = [
    "get_company_info",
    "get_security_status",
    "get_listing_info",
    "get_company_info_list",
    "get_industry_info",
    "get_management_info",
    "get_employee_info",
    "get_name_history",
]
