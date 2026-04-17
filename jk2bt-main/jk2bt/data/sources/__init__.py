"""
src/data_access/__init__.py
统一数据访问层 - 提供单一入口管理所有数据获取。

架构:
    DataSource (抽象基类)
        ├── AkShareAdapter (AkShare 实现)
        ├── MockDataSource (测试 Mock)
        └── [未来可扩展] 其他数据源

    DataRegistry (数据源注册中心)
        └── 管理默认数据源，支持动态切换

    CacheManager (统一缓存)
        └── 整合 db/unified_cache.py

使用方式:
    # 获取默认数据源
    from jk2bt.data.sources import get_data_source

    source = get_data_source()
    df = source.get_daily_data('sh600000', '2020-01-01', '2020-12-31')

    # 注册自定义数据源
    from jk2bt.data.sources import DataRegistry
    DataRegistry.register(my_custom_source)

    # 使用 Mock 数据源测试
    from jk2bt.data.sources import MockDataSource
    DataRegistry.register(MockDataSource())

向后兼容:
    现有代码可以直接使用原有 market_data 模块，
    内部逐步迁移到统一数据访问层。
"""

from .base import DataSource, DataSourceError
from .akshare import AkShareAdapter
from .mock import MockDataSource, create_mock_with_sample_data
from .registry import (
    DataRegistry,
    set_data_source,
    reset_data_source,
    get_source_health,
)
from jk2bt.cache import get_cache_manager, CacheManager, reset_cache_manager
from .router import (
    MultiSourceRouter,
    EmptyDataPolicy,
    ExecutionResult,
    create_simple_router,
)

# ── 向后兼容: 旧 cache_manager API 包装器 ─────────────────────────

_DOMAIN_TABLE_MAP = {
    ("market", "stock_daily"): "stock_daily",
    ("market", "etf_daily"): "etf_daily",
    ("market", "index_daily"): "index_daily",
    ("meta", "trade_days"): "trade_calendar",
    ("meta", "index_components"): "index_components",
    ("meta", "securities"): "securities",
    ("finance", "finance_indicator"): "finance_indicator",
    ("market", "money_flow"): "money_flow",
    ("market", "north_flow"): "north_flow",
    ("index", "index_components"): "index_components",
    ("industry", "industry_components"): "industry_components",
}


def _resolve_table_name(domain: str, table: str) -> str:
    return _DOMAIN_TABLE_MAP.get((domain, table), table)


class _LegacyCacheAdapter:
    """Compatibility wrapper: old DataAccessCacheManager API → new CacheManager."""

    def get(self, domain: str, table: str, use_cache: bool = True, **conditions):
        if not use_cache:
            return None
        cm = get_cache_manager()
        table_name = _resolve_table_name(domain, table)
        where = conditions if conditions else None
        return cm.get(table_name, where=where)

    def set(self, domain: str, table: str, df, metadata=None, **conditions):
        if df is None or (hasattr(df, "empty") and df.empty):
            return
        cm = get_cache_manager()
        table_name = _resolve_table_name(domain, table)
        cm.put(table_name, df)

    def invalidate(self, domain=None, table=None, **conditions):
        cm = get_cache_manager()
        if domain and table:
            table_name = _resolve_table_name(domain, table)
            cm.invalidate(table_name)
        else:
            cm.invalidate(table or domain)

    def clear(self):
        cm = get_cache_manager()
        for t in cm.list_tables():
            cm.invalidate(t)

    def stats(self):
        return {"backend_type": "parquet_cache"}

    def has_data(self, domain: str, table: str, **conditions) -> bool:
        cm = get_cache_manager()
        table_name = _resolve_table_name(domain, table)
        where = conditions if conditions else None
        return cm.exists(table_name, where=where)


_dataAccessCacheManager_instance = None


def get_cache() -> _LegacyCacheAdapter:
    """Compatibility: returns adapter wrapping jk2bt.cache.CacheManager."""
    global _dataAccessCacheManager_instance
    if _dataAccessCacheManager_instance is None:
        _dataAccessCacheManager_instance = _LegacyCacheAdapter()
    return _dataAccessCacheManager_instance


def clear_cache():
    """Compatibility: clear all cache tables."""
    get_cache().clear()


def reset_cache():
    """Compatibility: reset cache manager singleton."""
    global _dataAccessCacheManager_instance
    reset_cache_manager()
    _dataAccessCacheManager_instance = None


DataAccessCacheManager = _LegacyCacheAdapter
from .error_codes import (
    ErrorCode,
    DataAccessException,
    DataSourceError as DataSourceErrorCode,
    SourceUnavailableError,
    NoDataError,
    TimeoutError,
    RateLimitError,
)
from .akshare_compat import AkShareCompatAdapter, get_compat_adapter, FUNCTION_ALIASES

# ── 全局单例工厂 ──────────────────────────────────────────────────

_default_adapter = None


def get_adapter() -> AkShareAdapter:
    """获取全局默认 AkShareAdapter 单例"""
    global _default_adapter
    if _default_adapter is None:
        _default_adapter = AkShareAdapter()
    return _default_adapter


def set_adapter(adapter) -> None:
    """替换全局适配器（用于测试注入）"""
    global _default_adapter
    _default_adapter = adapter


def get_data_source():
    """Alias for get_adapter() — consolidated to single access pattern."""
    return get_adapter()


# Patch DataRegistry.get_source to use the same singleton
_original_dr_get_source = DataRegistry.get_source


@classmethod
def _dr_get_source_patched(cls):
    return get_adapter()


DataRegistry.get_source = _dr_get_source_patched


__all__ = [
    # 抽象基类
    "DataSource",
    "DataSourceError",
    # 数据源实现
    "AkShareAdapter",
    "MockDataSource",
    "create_mock_with_sample_data",
    # 注册中心
    "DataRegistry",
    "get_data_source",
    "set_data_source",
    "reset_data_source",
    "get_source_health",
    # 缓存管理
    "DataAccessCacheManager",
    "get_cache",
    "clear_cache",
    "reset_cache",
    "get_cache_manager",
    "CacheManager",
    # 多源路由
    "MultiSourceRouter",
    "EmptyDataPolicy",
    "ExecutionResult",
    "create_simple_router",
    # 错误码
    "ErrorCode",
    "DataAccessException",
    "SourceUnavailableError",
    "NoDataError",
    "TimeoutError",
    "RateLimitError",
    # AkShare 版本适配
    "AkShareCompatAdapter",
    "get_compat_adapter",
    "FUNCTION_ALIASES",
    # 单例工厂
    "get_adapter",
    "set_adapter",
]
