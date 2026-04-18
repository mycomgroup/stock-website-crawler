"""
src/api/__init__.py
API 层公共接口 —— 按功能分组导出所有公开符号

分组：
  1. 行情数据       来自 market.py
  2. 过滤工具       来自 filter.py
  3. 财务数据       来自 finance.py
  4. 统计与因子     来自 stats.py + factor.py
  5. 日期工具       来自 date.py
  6. 技术指标       来自 indicators.py
  7. 榜单数据       来自 billboard.py
  8. 缓存与性能     来自 cache.py

注意：订单相关函数（order_shares, order_target_percent 等）已移到 engine 层。
      请使用 from jk2bt.engine import order_shares 或 from jk2bt import order_shares。

向后兼容说明：
  - APIUsageInfo、analyze_api_gaps 仍从 gap_analyzer.py 导入，保持向后兼容
  - APIGapAnalyzer 不再导出（开发工具，不属于运行时 API）
  - _internal 下的符号不在 __all__ 中
"""

# --- 行情数据 ---
from jk2bt.api.market import (
    get_price,
    get_price_jq,
    history,
    attribute_history,
    get_bars,
    get_bars_jq,
    get_market,
    get_detailed_quote,
    get_open_price,
    get_close_price,
    get_high_limit,
    get_low_limit,
)

# --- 证券元数据 ---
from jk2bt.api.securities import (
    get_all_securities,
    get_security_info,
    get_all_securities_jq,
    get_security_info_jq,
    normalize_code,
)

# --- 因子看板 ---
from jk2bt.api.factor_kanban import (
    get_all_factors,
    get_factor_kanban_values,
    get_factor_stats,
    get_factor_style_returns,
    get_factor_specific_returns,
    get_factor_cov,
)

# --- 过滤工具 ---
from jk2bt.api.filter import (
    get_dividend_ratio_filter_list,
    get_margine_stocks,
    filter_new_stock,
    filter_st_stock,
    filter_paused_stock,
    apply_common_filters,
    filter_st,
    filter_paused,
    filter_limit_up,
    filter_limit_down,
    filter_new_stocks,
)

# --- 财务数据 ---
from jk2bt.api.finance import (
    get_locked_shares,
    get_fund_info,
    get_fundamentals_continuously,
)

# --- 统计与因子 ---
from jk2bt.api.stats import (
    get_ols,
    get_zscore,
    get_rank,
    get_factor_filter_list,
    get_num,
    get_beta,
)

from jk2bt.api.factor import (
    get_north_factor,
    get_comb_factor,
    get_factor_momentum,
)

# --- 日期工具 ---
from jk2bt.api.date import (
    get_shifted_date,
    get_previous_trade_date,
    get_next_trade_date,
    transform_date,
    is_trade_date,
    get_trade_dates_between,
    count_trade_dates_between,
    clear_trade_days_cache,
)

# --- 技术指标 ---
from jk2bt.api.indicators import (
    MA,
    EMA,
    MACD,
    KDJ,
    RSI,
    BOLL,
    ATR,
)

# --- 榜单数据 ---
from jk2bt.api.billboard import (
    get_billboard_list,
    get_institutional_holdings,
    get_billboard_hot_stocks,
    get_broker_statistics,
)

# --- 缓存与性能 ---
from jk2bt.api.cache import (
    CurrentDataCache,
    get_current_data_cached,
    get_current_data_batch,
    cached_get_security_info,
    cached_get_index_stocks,
    BatchDataLoader,
    DataPreloader,
    preload_data_for_strategy,
    batch_get_fundamentals,
    warm_up_cache,
    get_memory_usage,
    cleanup_memory,
    optimize_dataframe_memory,
)

# --- 向后兼容：gap_analyzer 公开符号（APIGapAnalyzer 除外） ---
from jk2bt.api.gap_analyzer import (
    APIUsageInfo,
    analyze_api_gaps,
)

# --- 因子分析 ---
from jk2bt.api.factor_analysis import (
    FactorAnalyzer,
    analyze_factor,
    AttributionAnalysis,
)

# --- 概念板块 ---
from jk2bt.api.concept import (
    get_concepts,
    get_concept_stocks,
    get_concept,
    get_all_concepts,
    get_concepts_jq,
    get_concept_stocks_jq,
    get_concept_jq,
    get_industry,
    get_stock_industry,
)

# --- 融资融券 ---
from jk2bt.api.margin import (
    get_mtss,
    get_margincash_stocks,
    get_marginsec_stocks,
    get_mtss_jq,
)

# --- 期货数据 ---
from jk2bt.api.futures import (
    get_dominant_future,
    get_futures_info,
    get_future_contracts,
    get_dominant_contracts,
    get_settlement_price,
    get_order_future_bar,
    get_future_index_bar,
    get_dominant_future_jq,
    get_futures_info_jq,
    get_future_contracts_jq,
)

# --- 估值数据 ---
from jk2bt.api.valuation import (
    get_index_valuation,
    get_valuation,
    get_index_valuation_jq,
)

# --- 金融行业指标 ---
from jk2bt.api.financial_indicator import (
    bank_indicator,
    security_indicator,
    insurance_indicator,
    bank_indicator_jq,
    security_indicator_jq,
    insurance_indicator_jq,
)

# --- 公司信息 ---
from jk2bt.api.company_info import (
    get_company_info,
    get_security_status,
    get_listing_info,
    get_company_info_list,
    get_industry_info,
)

# --- 股东数据 ---
from jk2bt.api.shareholder import (
    get_top10_shareholders,
    get_top10_float_shareholders,
    get_shareholder_count,
    get_shareholder_structure,
)

# --- 分红送股 ---
from jk2bt.api.dividend import (
    get_dividend_info,
    get_dividend_history,
    get_stock_bonus,
    get_adjust_factor,
    get_rights_issue,
    calculate_ex_rights_price,
)

# --- 股东变动数据 ---
from jk2bt.api.share_change import (
    get_pledge_info,
    get_freeze_info,
    get_capital_change,
    get_major_holder_trade,
    get_shareholder_changes,
    get_insider_trading,
    get_major_shareholder_change,
)

# --- 限售解禁数据 ---
from jk2bt.api.unlock import (
    get_unlock_info,
    get_unlock_calendar,
    get_unlock_schedule,
    get_unlock_pressure,
    get_unlock_history,
    get_upcoming_unlocks,
    analyze_unlock_impact,
)

# --- 基金数据 ---
from jk2bt.api.fund import (
    get_etf_daily,
    get_fund_nav,
    get_fund_of_nav,
    get_fund_of_info,
    get_fund_of_daily_list,
    get_lof_daily,
    get_lof_spot,
    get_lof_nav,
)

# --- 宏观数据 ---
from jk2bt.api.macro import (
    get_macro_gdp,
    get_macro_cpi,
    get_macro_ppi,
    get_macro_pmi,
    get_macro_m2,
    get_macro_interest_rate,
    get_macro_exchange_rate,
    get_macro_data,
)

# --- 北向资金 ---
from jk2bt.api.north_money import (
    get_north_money_flow,
    get_north_money_daily,
    get_north_money_holdings,
    get_north_money_stock_flow,
    get_north_money_stock_detail,
    compute_north_money_signal,
)

# --- 可转债数据 ---
from jk2bt.api.bond import (
    get_conversion_bond_list,
    get_conversion_bond_price,
    get_conversion_bond_info,
    get_conversion_bond_detail,
    get_conversion_bond_quote,
    get_conversion_info,
    calculate_conversion_value,
    calculate_premium_rate,
    get_conversion_bond_history,
    get_conversion_price,
    calculate_conversion_premium,
    get_conversion_bond_daily,
    get_conversion_value,
)

# --- 期权数据 ---
from jk2bt.api.option import (
    get_option_list,
    get_option_price,
    get_option_daily,
    get_option_greeks,
    get_option_info,
    get_option_chain,
    get_option,
    calculate_option_implied_vol,
    get_option_quote,
    query_option,
    get_option_ticks,
    get_option_preopen,
    get_option_adjustment,
    get_option_exercise_info,
    get_option_trade_rank,
    get_commodity_option_ticks,
)

# --- 市场数据扩展 ---
from jk2bt.api.market import (
    get_call_auction,
    get_preopen_infos,
)

# --- 资金流向 ---
from jk2bt.api.money_flow_api import (
    get_money_flow,
    get_money_flow_pro,
)

# --- JQ兼容扩展 ---
from jk2bt.api.jq_compat import (
    get_extras,
)

# --- 基金数据扩展 ---
from jk2bt.api.fund import (
    get_fund_margin_list,
    get_fund_short_sell_list,
    get_etf_tracking_index,
)


__all__ = [
    # 证券元数据
    "get_all_securities",
    "get_security_info",
    "get_all_securities_jq",
    "get_security_info_jq",
    "normalize_code",
    # 因子看板
    "get_all_factors",
    "get_factor_kanban_values",
    "get_factor_stats",
    "get_factor_style_returns",
    "get_factor_specific_returns",
    "get_factor_cov",
    # 行情数据
    "get_price",
    "get_price_jq",
    "history",
    "attribute_history",
    "get_bars",
    "get_bars_jq",
    "get_market",
    "get_detailed_quote",
    "get_open_price",
    "get_close_price",
    "get_high_limit",
    "get_low_limit",
    # 过滤工具
    "get_dividend_ratio_filter_list",
    "get_margine_stocks",
    "filter_new_stock",
    "filter_st_stock",
    "filter_paused_stock",
    "apply_common_filters",
    "filter_st",
    "filter_paused",
    "filter_limit_up",
    "filter_limit_down",
    "filter_new_stocks",
    # 财务数据
    "get_locked_shares",
    "get_fund_info",
    "get_fundamentals_continuously",
    # 统计与因子
    "get_ols",
    "get_zscore",
    "get_rank",
    "get_factor_filter_list",
    "get_num",
    "get_beta",
    "get_north_factor",
    "get_comb_factor",
    "get_factor_momentum",
    # 日期工具
    "get_shifted_date",
    "get_previous_trade_date",
    "get_next_trade_date",
    "transform_date",
    "is_trade_date",
    "get_trade_dates_between",
    "count_trade_dates_between",
    "clear_trade_days_cache",
    # 技术指标
    "MA",
    "EMA",
    "MACD",
    "KDJ",
    "RSI",
    "BOLL",
    "ATR",
    # 榜单数据
    "get_billboard_list",
    "get_institutional_holdings",
    "get_billboard_hot_stocks",
    "get_broker_statistics",
    # 缓存与性能
    "CurrentDataCache",
    "get_current_data_cached",
    "get_current_data_batch",
    "cached_get_security_info",
    "cached_get_index_stocks",
    "BatchDataLoader",
    "DataPreloader",
    "preload_data_for_strategy",
    "batch_get_fundamentals",
    "warm_up_cache",
    "get_memory_usage",
    "cleanup_memory",
    "optimize_dataframe_memory",
    # 向后兼容：gap_analyzer 公开符号（不含 APIGapAnalyzer）
    "APIUsageInfo",
    "analyze_api_gaps",
    # 因子分析
    "FactorAnalyzer",
    "analyze_factor",
    "AttributionAnalysis",
    # 概念板块
    "get_concepts",
    "get_concept_stocks",
    "get_concept",
    "get_all_concepts",
    "get_concepts_jq",
    "get_concept_stocks_jq",
    "get_concept_jq",
    "get_industry",
    "get_stock_industry",
    # 融资融券
    "get_mtss",
    "get_margincash_stocks",
    "get_marginsec_stocks",
    "get_mtss_jq",
    # 期货数据
    "get_dominant_future",
    "get_futures_info",
    "get_future_contracts",
    "get_dominant_contracts",
    "get_settlement_price",
    "get_order_future_bar",
    "get_future_index_bar",
    "get_dominant_future_jq",
    "get_futures_info_jq",
    "get_future_contracts_jq",
    # 估值数据
    "get_index_valuation",
    "get_valuation",
    "get_index_valuation_jq",
    # 金融行业指标
    "bank_indicator",
    "security_indicator",
    "insurance_indicator",
    "bank_indicator_jq",
    "security_indicator_jq",
    "insurance_indicator_jq",
    # 股东变动数据
    "get_pledge_info",
    "get_freeze_info",
    "get_capital_change",
    "get_major_holder_trade",
    "get_shareholder_changes",
    "get_insider_trading",
    "get_major_shareholder_change",
    # 限售解禁数据
    "get_unlock_info",
    "get_unlock_calendar",
    "get_unlock_schedule",
    "get_unlock_pressure",
    "get_unlock_history",
    "get_upcoming_unlocks",
    "analyze_unlock_impact",
    # 公司信息
    "get_company_info",
    "get_security_status",
    "get_listing_info",
    "get_company_info_list",
    "get_industry_info",
    # 股东数据
    "get_top10_shareholders",
    "get_top10_float_shareholders",
    "get_shareholder_count",
    "get_shareholder_structure",
    # 分红送股
    "get_dividend_info",
    "get_dividend_history",
    "get_stock_bonus",
    "get_adjust_factor",
    "get_rights_issue",
    "calculate_ex_rights_price",
    # 基金数据
    "get_etf_daily",
    "get_fund_nav",
    "get_fund_of_nav",
    "get_fund_of_info",
    "get_fund_of_daily_list",
    "get_lof_daily",
    "get_lof_spot",
    "get_lof_nav",
    # 宏观数据
    "get_macro_gdp",
    "get_macro_cpi",
    "get_macro_ppi",
    "get_macro_pmi",
    "get_macro_m2",
    "get_macro_interest_rate",
    "get_macro_exchange_rate",
    "get_macro_data",
    # 北向资金
    "get_north_money_flow",
    "get_north_money_daily",
    "get_north_money_holdings",
    "get_north_money_stock_flow",
    "get_north_money_stock_detail",
    "compute_north_money_signal",
    # 可转债数据
    "get_conversion_bond_list",
    "get_conversion_bond_price",
    "get_conversion_bond_info",
    "get_conversion_bond_detail",
    "get_conversion_bond_quote",
    "get_conversion_info",
    "calculate_conversion_value",
    "calculate_premium_rate",
    "get_conversion_bond_history",
    "get_conversion_price",
    "calculate_conversion_premium",
    "get_conversion_bond_daily",
    "get_conversion_value",
    # 期权数据
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
    # 市场数据扩展
    "get_call_auction",
    "get_preopen_infos",
    # 资金流向
    "get_money_flow",
    "get_money_flow_pro",
    # JQ兼容扩展
    "get_extras",
    # 基金数据扩展
    "get_fund_margin_list",
    "get_fund_short_sell_list",
    "get_etf_tracking_index",
]
