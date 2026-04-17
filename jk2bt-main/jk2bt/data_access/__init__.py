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
    from jk2bt.data_access import get_data_source

    source = get_data_source()
    df = source.get_daily_data('sh600000', '2020-01-01', '2020-12-31')

    # 注册自定义数据源
    from jk2bt.data_access import DataRegistry
    DataRegistry.register(my_custom_source)

    # 使用 Mock 数据源测试
    from jk2bt.data_access import MockDataSource
    DataRegistry.register(MockDataSource())

向后兼容:
    现有代码可以直接使用原有 market_data 模块，
    内部逐步迁移到统一数据访问层。
"""

from .data_source import DataSource, DataSourceError
from .akshare_adapter import AkShareAdapter
from .mock_data_source import MockDataSource, create_mock_with_sample_data
from .data_registry import (
    DataRegistry,
    set_data_source,
    reset_data_source,
    get_source_health,
)
from .cache_manager import DataAccessCacheManager, get_cache, clear_cache, reset_cache
from parquet_cache import get_cache_manager, CacheManager as ParquetCacheManager
from .source_router import (
    MultiSourceRouter,
    EmptyDataPolicy,
    ExecutionResult,
    create_simple_router,
)
from .error_codes import (
    ErrorCode,
    DataAccessException,
    DataSourceError as DataAccessExceptionCode,
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
    "ParquetCacheManager",
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
