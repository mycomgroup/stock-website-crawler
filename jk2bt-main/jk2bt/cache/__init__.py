"""
Parquet Cache - 多进程并发安全的 Parquet 缓存系统

Usage:
    from jk2bt.cache import CacheManager

    cache = CacheManager(base_dir=resolve_cache_path("data_cache/cache"))

    # 写入
    cache.put("stock_daily", df, partition_value="2024-04-01")

    # 读取
    df = cache.get("stock_daily", where={"symbol": "600519", "date": ("2024-04-01", "2024-04-30")})

    # 聚合
    from jk2bt.cache import run_aggregation
    run_aggregation(resolve_cache_path("data_cache/cache"))
"""

__version__ = "0.1.0"

from .config import CacheConfig, TableConfig, DEFAULT_CONFIG
from .registry import (
    CacheTable,
    TableInfo,
    TableRegistry,
    DEFAULT_REGISTRY,
    # 所有预定义的表
    STOCK_DAILY,
    ETF_DAILY,
    INDEX_DAILY,
    FUTURES_DAILY,
    CONVERSION_BOND_DAILY,
    INDEX_COMPONENTS,
    INDEX_WEIGHTS,
    FINANCE_INDICATOR,
    MONEY_FLOW,
    NORTH_FLOW,
    INDUSTRY_COMPONENTS,
    HOLDER,
    DIVIDEND,
    VALUATION,
    UNLOCK,
    SPOT_SNAPSHOT,
    SECTOR_FLOW_SNAPSHOT,
    HSGT_HOLD_SNAPSHOT,
    STOCK_MINUTE,
    ETF_MINUTE,
    SECURITIES,
    TRADE_CALENDAR,
    INDUSTRY_LIST,
    CONCEPT_LIST,
    COMPANY_INFO,
    FACTOR_CACHE,
)
from .manager import (
    CacheManager,
    get_cache_manager,
    reset_cache_manager,
)
from .aggregator import Aggregator, run_aggregation
from .memory import MemoryCache
from .query import QueryEngine
from .writer import AtomicWriter
from .partition import PartitionManager
from .validator import (
    SchemaValidator,
    SchemaValidationError,
    infer_schema,
    normalize_date_columns,
    deduplicate_by_key,
)

__all__ = [
    "__version__",
    "CacheConfig",
    "TableConfig",
    "DEFAULT_CONFIG",
    "CacheTable",
    "TableInfo",
    "TableRegistry",
    "DEFAULT_REGISTRY",
    "STOCK_DAILY",
    "ETF_DAILY",
    "INDEX_DAILY",
    "FUTURES_DAILY",
    "CONVERSION_BOND_DAILY",
    "INDEX_COMPONENTS",
    "FINANCE_INDICATOR",
    "MONEY_FLOW",
    "NORTH_FLOW",
    "INDUSTRY_COMPONENTS",
    "HOLDER",
    "DIVIDEND",
    "VALUATION",
    "UNLOCK",
    "SPOT_SNAPSHOT",
    "SECTOR_FLOW_SNAPSHOT",
    "HSGT_HOLD_SNAPSHOT",
    "STOCK_MINUTE",
    "ETF_MINUTE",
    "SECURITIES",
    "TRADE_CALENDAR",
    "INDUSTRY_LIST",
    "CONCEPT_LIST",
    "COMPANY_INFO",
    "FACTOR_CACHE",
    "CacheManager",
    "get_cache_manager",
    "reset_cache_manager",
    "Aggregator",
    "run_aggregation",
    "MemoryCache",
    "QueryEngine",
    "AtomicWriter",
    "PartitionManager",
    "SchemaValidator",
    "SchemaValidationError",
    "infer_schema",
    "normalize_date_columns",
    "deduplicate_by_key",
]
