"""
engine - 回测引擎

包含策略运行器、策略基类、执行器、全局状态
"""

# Runner
from jk2bt.engine.runner import (
    run_jq_strategy,
    load_jq_strategy,
)

# Strategy Base
from jk2bt.engine.strategy_base import (
    JQ2BTBaseStrategy,
    GlobalState,
    ContextProxy,
    JQLogAdapter,
    TimerManager,
)

# Wrapper
from jk2bt.engine.strategy_wrapper import (
    JQStrategyWrapper,
)

# Asset Router
from jk2bt.engine.asset_router import (
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
)

# Securities Utils
from jk2bt.engine.securities_utils import (
    format_stock_symbol_for_akshare,
    jq_code_to_ak,
    ak_code_to_jq,
)

# Constants
from jk2bt.engine.constants import (
    SECURITY_INDEXES,
    INDEX_FALLBACK_MAP,
)

# Exceptions
from jk2bt.engine.exceptions import (
    JK2BTError,
    DataSourceError,
    NetworkError,
    CacheError,
    ValidationError,
    StrategyError,
)

__all__ = [
    # Runner
    "run_jq_strategy",
    "load_jq_strategy",
    # Strategy Base
    "JQ2BTBaseStrategy",
    "GlobalState",
    "ContextProxy",
    "JQLogAdapter",
    "TimerManager",
    # Wrapper
    "JQStrategyWrapper",
    # Asset Router
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
    # Securities Utils
    "format_stock_symbol_for_akshare",
    "jq_code_to_ak",
    "ak_code_to_jq",
    # Exceptions
    "JK2BTError",
    "DataSourceError",
    "NetworkError",
    "CacheError",
    "ValidationError",
    "StrategyError",
]
