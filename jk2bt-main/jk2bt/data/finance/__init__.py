"""
finance_data/__init__.py
公开导出财务子模块的核心函数。
"""

from .company_info import (
    get_company_info,
    get_security_status,
    query_company_basic_info,
    query_status_change,
    run_query_simple as run_query_simple_company,
    get_listing_info,
    get_company_info_robust,
    query_company_info_robust,
    get_security_status_robust,
    get_company_info_list,
    get_industry_info,
    prewarm_company_info_cache,
    get_management_info,
    get_employee_info,
    get_name_history,
)
from .shareholder import (
    get_top_shareholders,
    get_top_float_shareholders,
    get_shareholder_structure,
    get_shareholder_concentration,
    prewarm_shareholder_cache,
    get_shareholders,
    get_top10_shareholders,
    get_top10_float_shareholders,
    get_shareholder_count,
    query_shareholder_top10,
    query_shareholder_float_top10,
    query_shareholder_num,
    run_query_simple as run_query_simple_shareholder,
)
from .dividend import (
    get_dividend_info,
    get_dividend_history,
    calculate_ex_rights_price,
    get_stock_bonus,
    get_adjust_factor,
    get_dividend_by_date,
    query_dividend,
    run_query_simple as run_query_simple_dividend,
    get_dividend,
    get_rights_issue,
    get_next_dividend,
    query_dividend_right,
    calculate_adjust_price,
    FinanceQuery,
    finance,
    _DIVIDEND_SCHEMA,
    _RIGHTS_ISSUE_SCHEMA,
    _NEXT_DIVIDEND_SCHEMA,
    _ADJUST_FACTOR_SCHEMA,
)
from .income import (
    get_income,
)
from .cashflow import (
    get_cashflow,
)
from .margin import (
    get_margin_data,
    get_margin_history,
)
from .forecast import (
    get_forecast_data,
)
from .share_change import (
    get_share_change,
    query_share_change,
    run_query_simple as run_query_simple_share_change,
    get_pledge_info,
    get_major_holder_trade,
    get_insider_trading,
    get_major_shareholder_change,
    analyze_share_change_trend,
    get_freeze_info,
    get_capital_change,
    get_topholder_change,
    query_pledge_data,
    query_freeze_data,
    query_capital_change,
)
from .unlock import (
    get_unlock,
    query_unlock,
    get_unlock_calendar,
    get_unlock_schedule,
    get_unlock_pressure,
    run_query_simple as run_query_simple_unlock,
    get_unlock_info,
    get_upcoming_unlocks,
    get_unlock_history,
    analyze_unlock_impact,
    get_unlock_info_batch,
    query_lock_share,
)
from .macro import (
    get_macro_china_gdp,
    get_macro_china_cpi,
    get_macro_china_ppi,
    get_macro_china_pmi,
    get_macro_china_interest_rate,
    get_macro_china_exchange_rate,
    query_macro_data,
    get_macro_cpi,
    get_macro_ppi,
    get_macro_gdp,
    get_macro_m2,
    get_macro_interest_rate,
    query_macro,
    get_macro_indicator_robust,
    get_macro_data,
    get_macro_series,
    get_macro_indicators,
    get_gdp_data,
    get_cpi_data,
    get_pmi_data,
    get_interest_rate,
    get_macro_indicator,
    run_query_simple as run_query_simple_macro,
    run_offset_query,
)
from .tables import (
    STK_BALANCE_SHEET_SCHEMA,
    STK_INCOME_STATEMENT_SCHEMA,
    STK_CASHFLOW_STATEMENT_SCHEMA,
    FUND_NET_VALUE_SCHEMA,
    FUND_PORTFOLIO_SCHEMA,
    get_balance_sheet,
    get_income_statement,
    get_cashflow_statement,
    get_fund_net_value,
    get_fund_portfolio,
    FinanceTables,
    finance_tables,
)

__all__ = [
    "get_company_info",
    "get_security_status",
    "query_company_basic_info",
    "query_status_change",
    "run_query_simple_company",
    "get_listing_info",
    "get_company_info_robust",
    "query_company_info_robust",
    "get_security_status_robust",
    "get_company_info_list",
    "get_industry_info",
    "prewarm_company_info_cache",
    "get_management_info",
    "get_employee_info",
    "get_name_history",
    "get_top_shareholders",
    "get_top_float_shareholders",
    "get_shareholder_structure",
    "get_shareholder_concentration",
    "prewarm_shareholder_cache",
    "get_shareholders",
    "get_top10_shareholders",
    "get_top10_float_shareholders",
    "get_shareholder_count",
    "query_shareholder_top10",
    "query_shareholder_float_top10",
    "query_shareholder_num",
    "run_query_simple_shareholder",
    "get_dividend_info",
    "get_dividend_history",
    "calculate_ex_rights_price",
    "get_stock_bonus",
    "get_adjust_factor",
    "get_dividend_by_date",
    "query_dividend",
    "run_query_simple_dividend",
    "get_dividend",
    "get_rights_issue",
    "get_next_dividend",
    "query_dividend_right",
    "calculate_adjust_price",
    "FinanceQuery",
    "finance",
    "_DIVIDEND_SCHEMA",
    "_RIGHTS_ISSUE_SCHEMA",
    "_NEXT_DIVIDEND_SCHEMA",
    "_ADJUST_FACTOR_SCHEMA",
    "get_income",
    "get_cashflow",
    "get_margin_data",
    "get_margin_history",
    "get_forecast_data",
    "get_share_change",
    "query_share_change",
    "run_query_simple_share_change",
    "get_pledge_info",
    "get_major_holder_trade",
    "get_shareholder_changes",
    "get_insider_trading",
    "get_major_shareholder_change",
    "analyze_share_change_trend",
    "get_freeze_info",
    "get_capital_change",
    "get_topholder_change",
    "query_pledge_data",
    "query_freeze_data",
    "query_capital_change",
    "get_unlock",
    "query_unlock",
    "get_unlock_calendar",
    "get_unlock_schedule",
    "get_unlock_pressure",
    "run_query_simple_unlock",
    "get_unlock_info",
    "get_upcoming_unlocks",
    "get_unlock_history",
    "analyze_unlock_impact",
    "get_unlock_info_batch",
    "query_lock_share",
    "get_macro_china_gdp",
    "get_macro_china_cpi",
    "get_macro_china_ppi",
    "get_macro_china_pmi",
    "get_macro_china_interest_rate",
    "get_macro_china_exchange_rate",
    "query_macro_data",
    "get_macro_cpi",
    "get_macro_ppi",
    "get_macro_gdp",
    "get_macro_m2",
    "get_macro_interest_rate",
    "query_macro",
    "get_macro_indicator_robust",
    "get_macro_data",
    "get_macro_series",
    "get_macro_indicators",
    "get_gdp_data",
    "get_cpi_data",
    "get_pmi_data",
    "get_interest_rate",
    "get_macro_indicator",
    "run_query_simple_macro",
    "run_offset_query",
    # Finance Tables
    "STK_BALANCE_SHEET_SCHEMA",
    "STK_INCOME_STATEMENT_SCHEMA",
    "STK_CASHFLOW_STATEMENT_SCHEMA",
    "FUND_NET_VALUE_SCHEMA",
    "FUND_PORTFOLIO_SCHEMA",
    "get_balance_sheet",
    "get_income_statement",
    "get_cashflow_statement",
    "get_fund_net_value",
    "get_fund_portfolio",
    "FinanceTables",
    "finance_tables",
    "get_financial_data",
]


def get_financial_data(
    securities,
    start_date=None,
    end_date=None,
    fields=None,
    count=None,
    report_type="all",
):
    """
    获取财务数据统一接口（兼容聚宽风格）。

    Parameters
    ----------
    securities : str or list
        股票代码或代码列表
    start_date : str, optional
        起始日期 'YYYY-MM-DD'
    end_date : str, optional
        结束日期 'YYYY-MM-DD'
    fields : list, optional
        字段列表，如 ['code', 'pub_date', 'stat_date', 'roe', 'roa', 'eps']
    count : int, optional
        数据条数
    report_type : str, default 'all'
        报表类型：'income'(利润表), 'balance'(资产负债表), 'cashflow'(现金流量表),
        'indicator'(财务指标), 'all'

    Returns
    -------
    pd.DataFrame
        财务数据 DataFrame
    """
    from jk2bt.data.sources import get_adapter

    if isinstance(securities, str):
        securities = [securities]

    all_results = []

    for symbol in securities:
        code = symbol.replace(".XSHG", "").replace(".XSHE", "").zfill(6)

        if report_type == "income":
            try:
                df = get_income(code, start_date=start_date, end_date=end_date)
                if not df.empty:
                    df["code"] = code
                    all_results.append(df)
            except Exception:
                pass

        elif report_type == "balance":
            try:
                df = get_balance_sheet(code, start_date=start_date, end_date=end_date)
                if not df.empty:
                    df["code"] = code
                    all_results.append(df)
            except Exception:
                pass

        elif report_type == "cashflow":
            try:
                df = get_cashflow(code, start_date=start_date, end_date=end_date)
                if not df.empty:
                    df["code"] = code
                    all_results.append(df)
            except Exception:
                pass

        elif report_type == "indicator":
            try:
                df = get_forecast_data(code)
                if df is not None and not df.empty:
                    df["code"] = code
                    if start_date:
                        df = df[df["pub_date"] >= start_date]
                    if end_date:
                        df = df[df["pub_date"] <= end_date]
                    all_results.append(df)
            except Exception:
                pass

        else:
            try:
                income_df = get_income(code, start_date=start_date, end_date=end_date)
                if income_df is not None and not income_df.empty:
                    income_df["code"] = code
                    all_results.append(income_df)
            except Exception:
                pass

            try:
                balance_df = get_balance_sheet(
                    code, start_date=start_date, end_date=end_date
                )
                if balance_df is not None and not balance_df.empty:
                    balance_df["code"] = code
                    all_results.append(balance_df)
            except Exception:
                pass

            try:
                cashflow_df = get_cashflow(
                    code, start_date=start_date, end_date=end_date
                )
                if cashflow_df is not None and not cashflow_df.empty:
                    cashflow_df["code"] = code
                    all_results.append(cashflow_df)
            except Exception:
                pass

    if not all_results:
        return pd.DataFrame()

    combined = pd.concat(all_results, ignore_index=True)

    if fields:
        available_fields = [f for f in fields if f in combined.columns]
        combined = combined[available_fields]

    if count:
        combined = combined.tail(count)

    return combined
