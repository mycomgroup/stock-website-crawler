"""
jk2bt - 聚宽策略本地运行框架

模块结构：
- core:      策略基类、运行器
- factors:   因子模块（连续值，选股打分用）
- signals:   信号模块（离散事件，择时用）
- risk:      风控模块（风险度量，仓位控制用）
- indicators: 指标计算层
- finance_data: 财务数据
- market_data: 市场数据
"""

# 版本信息
__version__ = "1.0.0"
__author__ = "jk2bt"

# =============================================================================
# 日志系统初始化
# =============================================================================
import os
from jk2bt.utils.logging_config import setup_logging

# 通过环境变量控制日志级别，默认INFO
setup_logging(level=os.environ.get("JK2BT_LOG_LEVEL", "INFO"))

# =============================================================================
# Core - 策略运行器
# =============================================================================
from jk2bt.core.runner import (
    run_jq_strategy,
    load_jq_strategy,
    JQStrategyWrapper,
    LimitOrderStyle,
    MarketOrderStyle,
)

# =============================================================================
# Core - 策略基类
# =============================================================================
from jk2bt.core.strategy_base import (
    JQ2BTBaseStrategy as StrategyBase,
    GlobalState,
    ContextProxy,
    JQLogAdapter,
    TimerManager,
    get_price,
    get_price_unified,
    get_price_jq,
    get_fundamentals,
    get_fundamentals_jq,
    get_current_data,
    get_current_tick,
    history,
    attribute_history,
    get_index_weights,
    get_index_stocks,
    get_all_securities_jq,
    get_security_info_jq,
    get_factor_values_jq,
    get_all_trade_days,
    get_extras,
    get_bars,
    get_billboard_list,
    query,
    valuation,
    income,
    balance,
    cash_flow,
    indicator,
    finance,
    format_stock_symbol_for_akshare,
    jq_code_to_ak,
    ak_code_to_jq,
    get_akshare_stock_data,
    get_akshare_etf_data,
    get_history_fundamentals_jq,
)

# 以下函数在 runner.py 中定义
from jk2bt.core.runner import get_trade_days, get_call_auction, get_ticks, get_valuation

# =============================================================================
# Core - 运行时IO
# =============================================================================
from jk2bt.core.io import (
    record,
    send_message,
    read_file,
    write_file,
    get_record_data,
    get_messages,
    clear_runtime_data,
    set_runtime_dir,
)

# =============================================================================
# Core - 资产路由
# =============================================================================
from jk2bt.core.asset_router import (
    AssetType,
    AssetCategory,
    TradingStatus,
    AssetInfo,
    AssetRouter,
    get_asset_router,
    identify_asset,
    is_etf,
    is_stock,
    is_fund_of,
    is_future,
    is_index,
    get_trading_status_desc,
)

# =============================================================================
# API - 交易API
# =============================================================================
from jk2bt.api import (
    order_shares,
    order_target_percent,
    filter_st,
    filter_paused,
    filter_limit_up,
    filter_limit_down,
    filter_new_stocks,
    get_high_limit,
    get_low_limit,
    get_price as get_price_api,
    history as history_api,
    attribute_history as attribute_history_api,
    get_bars,
    get_price_jq,
    get_bars_jq,
    CurrentDataCache,
    get_current_data_cached,
    get_current_data_batch,
    BatchDataLoader,
    preload_data_for_strategy,
    DataPreloader,
    warm_up_cache,
    cleanup_memory,
    get_memory_usage,
)

# =============================================================================
# API - 增强功能
# =============================================================================
from jk2bt.api.enhancements import (
    calculate_position_value,
    get_position_ratio,
    rebalance_portfolio,
    get_portfolio_weights,
)

# =============================================================================
# Strategy - 辅助函数
# =============================================================================
from jk2bt.strategy.helpers import (
    calculate_ma,
    calculate_ema,
    calculate_std,
    calculate_boll,
    calculate_rsi,
    calculate_macd,
    calculate_kdj,
    calculate_atr,
    calculate_sharpe,
    calculate_max_drawdown as calculate_max_drawdown_helper,
    calculate_annualized_return,
    calculate_volatility as calculate_volatility_helper,
    rebalance_equally,
    get_top_holdings,
)

# =============================================================================
# Strategy - 子账户
# =============================================================================
from jk2bt.strategy.subportfolios import (
    SubportfolioType,
    SubportfolioConfig,
    SubportfolioPosition,
    SubportfolioCashAccount,
    SubportfolioProxy,
    SubportfolioManager,
    set_subportfolios,
    transfer_cash,
    get_subportfolio_summary,
)

# =============================================================================
# Signals - 信号模块（包含择时信号和指标数据）
# =============================================================================
from jk2bt.signals import (
    # RSRS择时信号
    compute_rsrs,
    compute_rsrs_signal,
    get_rsrs_for_index,
    get_current_rsrs_signal,
    # 市场情绪信号
    compute_crowding_ratio,
    compute_gisi,
    compute_fed_model,
    compute_graham_index,
    # 指标数据
    get_indicator_data,
    get_indicator_batch,
    get_indicator_ranking,
    filter_by_indicator,
)

# =============================================================================
# Factors - 因子模块
# =============================================================================
from jk2bt.factors import get_factor_values_jq, finance

# =============================================================================
# Risk - 风控模块
# =============================================================================
from jk2bt.risk import (
    compute_volatility,
    compute_volatility_adjusted_position,
    compute_atr_based_stop_loss,
    compute_max_drawdown,
    check_drawdown_alert,
    kelly_criterion,
    risk_parity_position,
)

__all__ = [
    # Version
    "__version__",
    "__author__",
    # Core - Runner
    "run_jq_strategy",
    "load_jq_strategy",
    "JQStrategyWrapper",
    # Core - Strategy Base
    "StrategyBase",
    "JQ2BTBaseStrategy",
    "GlobalState",
    "ContextProxy",
    "JQLogAdapter",
    "TimerManager",
    # Core - Data API
    "get_price",
    "get_price_unified",
    "get_price_jq",
    "get_fundamentals",
    "get_fundamentals_jq",
    "get_current_data",
    "get_current_tick",
    "history",
    "attribute_history",
    "get_index_weights",
    "get_index_stocks",
    "get_all_securities_jq",
    "get_security_info_jq",
    "get_factor_values_jq",
    "get_all_trade_days",
    "get_trade_days",
    "get_extras",
    "get_bars",
    "get_billboard_list",
    "get_call_auction",
    "get_ticks",
    "get_valuation",
    "get_history_fundamentals_jq",
    # Core - Finance Tables
    "query",
    "valuation",
    "income",
    "balance",
    "cash_flow",
    "indicator",
    "finance",
    # Core - Symbol Conversion
    "format_stock_symbol_for_akshare",
    "jq_code_to_ak",
    "ak_code_to_jq",
    "get_akshare_stock_data",
    "get_akshare_etf_data",
    # Core - Runtime IO
    "record",
    "send_message",
    "read_file",
    "write_file",
    "get_record_data",
    "get_messages",
    "clear_runtime_data",
    "set_runtime_dir",
    # Core - Asset Router
    "AssetType",
    "AssetCategory",
    "TradingStatus",
    "AssetInfo",
    "AssetRouter",
    "get_asset_router",
    "identify_asset",
    "is_etf",
    "is_stock",
    "is_fund_of",
    "is_future",
    "is_index",
    "get_trading_status_desc",
    # API - Trading
    "order_shares",
    "order_target_percent",
    "filter_st",
    "filter_paused",
    "filter_limit_up",
    "filter_limit_down",
    "filter_new_stocks",
    "get_high_limit",
    "get_low_limit",
    "get_bars",
    "get_price_jq",
    "get_bars_jq",
    # API - Optimization
    "CurrentDataCache",
    "get_current_data_cached",
    "get_current_data_batch",
    "BatchDataLoader",
    "preload_data_for_strategy",
    "DataPreloader",
    "warm_up_cache",
    "cleanup_memory",
    "get_memory_usage",
    # API - Position
    "calculate_position_value",
    "get_position_ratio",
    "rebalance_portfolio",
    "get_portfolio_weights",
    # Strategy - Helpers
    "calculate_ma",
    "calculate_ema",
    "calculate_std",
    "calculate_boll",
    "calculate_rsi",
    "calculate_macd",
    "calculate_kdj",
    "calculate_atr",
    "calculate_sharpe",
    "calculate_max_drawdown",
    "calculate_annualized_return",
    "calculate_volatility",
    "rebalance_equally",
    "get_top_holdings",
    # Strategy - Subportfolio
    "SubportfolioType",
    "SubportfolioConfig",
    "SubportfolioPosition",
    "SubportfolioCashAccount",
    "SubportfolioProxy",
    "SubportfolioManager",
    "set_subportfolios",
    "transfer_cash",
    "get_subportfolio_summary",
    # Order Styles
    "LimitOrderStyle",
    "MarketOrderStyle",
    # Indicators
    "get_indicator_data",
    "get_indicator_batch",
    "get_indicator_ranking",
    "filter_by_indicator",
    # Factors
    "get_factor_values_jq",
    # Signals
    "compute_rsrs",
    "compute_rsrs_signal",
    "get_rsrs_for_index",
    "get_current_rsrs_signal",
    "compute_crowding_ratio",
    "compute_gisi",
    "compute_fed_model",
    "compute_graham_index",
    # Risk
    "compute_volatility",
    "compute_volatility_adjusted_position",
    "compute_atr_based_stop_loss",
    "compute_max_drawdown",
    "check_drawdown_alert",
    "kelly_criterion",
    "risk_parity_position",
]

# Alias for backwards compatibility
JQ2BTBaseStrategy = StrategyBase

# Alias: __all__ uses calculate_max_drawdown, but imported as calculate_max_drawdown_helper
calculate_max_drawdown = calculate_max_drawdown_helper
calculate_volatility = calculate_volatility_helper
