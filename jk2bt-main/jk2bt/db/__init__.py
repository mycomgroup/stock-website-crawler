"""
db/__init__.py
DuckDB 数据库管理模块 - 统一缓存架构。
"""

from .duckdb_manager import DuckDBManager
from .cache_status import CacheManager, get_cache_manager, check_cache_status
from .migrate import (
    auto_migrate,
    migrate_stock_pickles,
    migrate_etf_pickles,
    migrate_index_pickles,
)
from .unified_cache import (
    UnifiedCacheManager,
    CachePolicy,
    TableSchema,
    DuckDBAdapter,
    SharedMemoryCache,
    get_unified_cache,
    clear_unified_cache,
    reset_unified_cache,
)
from .cache_config import (
    META_SCHEMAS,
    MARKET_SCHEMAS,
    OPTION_SCHEMAS,
    CONVERSION_BOND_SCHEMAS,
    MACRO_SCHEMAS,
    SHARE_CHANGE_SCHEMAS,
    UNLOCK_SCHEMAS,
    INDEX_COMPONENTS_SCHEMAS,
    DEFAULT_POLICIES,
    DOMAIN_DB_MAPPING,
    init_default_cache,
)
from .migrate_pickle import (
    migrate_all_pickle,
    migrate_meta_cache,
    migrate_index_cache,
    verify_migration,
)
from .meta_cache_api import (
    get_trade_days_from_cache,
    get_securities_from_cache,
    get_security_info_from_cache,
    prewarm_meta_cache,
    check_meta_cache_status,
)

__all__ = [
    "DuckDBManager",
    "CacheManager",
    "get_cache_manager",
    "check_cache_status",
    "auto_migrate",
    "migrate_stock_pickles",
    "migrate_etf_pickles",
    "migrate_index_pickles",
    "UnifiedCacheManager",
    "CachePolicy",
    "TableSchema",
    "DuckDBAdapter",
    "SharedMemoryCache",
    "get_unified_cache",
    "clear_unified_cache",
    "reset_unified_cache",
    "META_SCHEMAS",
    "MARKET_SCHEMAS",
    "OPTION_SCHEMAS",
    "CONVERSION_BOND_SCHEMAS",
    "MACRO_SCHEMAS",
    "SHARE_CHANGE_SCHEMAS",
    "UNLOCK_SCHEMAS",
    "INDEX_COMPONENTS_SCHEMAS",
    "DEFAULT_POLICIES",
    "DOMAIN_DB_MAPPING",
    "init_default_cache",
    "migrate_all_pickle",
    "migrate_meta_cache",
    "migrate_index_cache",
    "verify_migration",
    "get_trade_days_from_cache",
    "get_securities_from_cache",
    "get_security_info_from_cache",
    "prewarm_meta_cache",
    "check_meta_cache_status",
]
