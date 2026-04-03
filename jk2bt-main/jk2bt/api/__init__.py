"""
src/api/__init__.py
API 层公共接口 —— 按功能分组导出所有公开符号

分组：
  1. 行情数据       来自 market.py
  2. 订单与组合     来自 order.py
  3. 过滤工具       来自 filter.py
  4. 财务数据       来自 finance.py
  5. 统计与因子     来自 stats.py + factor.py
  6. 日期工具       来自 date.py
  7. 技术指标       来自 indicators.py
  8. 榜单数据       来自 billboard.py
  9. 缓存与性能     来自 cache.py

向后兼容说明：
  - will_sell_on_limit_up、will_buy_on_limit_down、get_position_ratio
    从 order.py 导出，保持向后兼容
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
    get_ticks_enhanced,
    get_open_price,
    get_close_price,
    get_high_limit,
    get_low_limit,
)

# --- 订单与组合 ---
from jk2bt.api.order import (
    order_shares,
    order_target_percent,
    LimitOrderStyle,
    MarketOrderStyle,
    rebalance_portfolio,
    get_portfolio_weights,
    calculate_position_value,
)

from jk2bt.api.order import (
    will_sell_on_limit_up,
    will_buy_on_limit_down,
    get_position_ratio,
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


__all__ = [
    # 行情数据
    "get_price",
    "get_price_jq",
    "history",
    "attribute_history",
    "get_bars",
    "get_bars_jq",
    "get_market",
    "get_detailed_quote",
    "get_ticks_enhanced",
    "get_open_price",
    "get_close_price",
    "get_high_limit",
    "get_low_limit",
    # 订单与组合
    "order_shares",
    "order_target_percent",
    "LimitOrderStyle",
    "MarketOrderStyle",
    "rebalance_portfolio",
    "get_portfolio_weights",
    "calculate_position_value",
    "will_sell_on_limit_up",
    "will_buy_on_limit_down",
    "get_position_ratio",
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
]
