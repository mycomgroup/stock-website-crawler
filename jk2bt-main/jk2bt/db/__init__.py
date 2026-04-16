"""
db/__init__.py
Parquet 数据库管理模块 - 统一缓存架构。
"""

from .parquet_adapter import ParquetAdapter
from .cache_status import CacheManager, get_cache_manager, check_cache_status
from .migrate import (
    auto_migrate,
    migrate_stock_pickles,
    migrate_etf_pickles,
    migrate_index_pickles,
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
from .meta_cache_api import (
    get_trade_days_from_cache,
    get_securities_from_cache,
    get_security_info_from_cache,
    prewarm_meta_cache,
    check_meta_cache_status,
)

try:
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

    _UNIFIED_CACHE_AVAILABLE = True
except ImportError:
    _UNIFIED_CACHE_AVAILABLE = False

try:
    from .migrate_pickle import (
        migrate_all_pickle,
        migrate_meta_cache,
        migrate_index_cache,
        verify_migration,
    )

    _MIGRATE_PICKLE_AVAILABLE = True
except ImportError:
    _MIGRATE_PICKLE_AVAILABLE = False

__all__ = [
    "ParquetAdapter",
    "CacheManager",
    "get_cache_manager",
    "check_cache_status",
    "auto_migrate",
    "migrate_stock_pickles",
    "migrate_etf_pickles",
    "migrate_index_pickles",
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
    "get_trade_days_from_cache",
    "get_securities_from_cache",
    "get_security_info_from_cache",
    "prewarm_meta_cache",
    "check_meta_cache_status",
]
