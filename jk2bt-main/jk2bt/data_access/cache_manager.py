"""
src/data_access/cache_manager.py
[DEPRECATED] 数据访问层缓存管理器 - 已废弃，请使用 parquet_cache 模块。

此类仅为向后兼容保留，内部转发到 parquet_cache.CacheManager。
新代码应直接使用：from parquet_cache import get_cache_manager
"""

import logging
import threading
import time
from typing import Optional, Dict, Any
from datetime import datetime, timedelta
import pandas as pd

logger = logging.getLogger(__name__)

# parquet_cache 表名映射
DOMAIN_TABLE_MAP = {
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
    """将 domain/table 映射到 parquet_cache 表名"""
    return DOMAIN_TABLE_MAP.get((domain, table), table)


class DataAccessCacheManager:
    """
    [DEPRECATED] 数据访问层缓存管理器。

    此类已废弃，仅为向后兼容保留。内部转发到 parquet_cache.CacheManager。
    新代码应直接使用：from parquet_cache import get_cache_manager
    """

    _instance = None
    _lock = threading.Lock()

    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
                    cls._instance._init()
        return cls._instance

    def _init(self):
        self._parquet_cache = None
        self._fallback = SimpleMemoryCache()

        try:
            from parquet_cache import get_cache_manager

            self._parquet_cache = get_cache_manager()
            logger.info("DataAccessCacheManager: 使用 parquet_cache 作为后端")
        except Exception as e:
            logger.warning(
                f"DataAccessCacheManager: parquet_cache 不可用，使用 fallback: {e}"
            )

        # 缓存策略配置（保留以兼容旧代码）
        self._domain_policies: Dict[str, int] = {
            "meta": 168,  # 元数据缓存 7 天
            "market": 24,  # 行情数据缓存 1 天
            "finance": 72,  # 财务数据缓存 3 天
            "index": 168,  # 指数成分股缓存 7 天
            "industry": 168,  # 行业数据缓存 7 天
            "default": 24,  # 默认缓存 1 天
        }

    def get(
        self, domain: str, table: str, use_cache: bool = True, **conditions
    ) -> Optional[pd.DataFrame]:
        if not use_cache:
            return None

        if self._parquet_cache is not None:
            try:
                table_name = _resolve_table_name(domain, table)
                where = conditions if conditions else None
                return self._parquet_cache.get(table_name, where=where)
            except Exception as e:
                logger.warning(f"parquet_cache get 失败，使用 fallback: {e}")

        return self._fallback.get(domain, table, **conditions)

    def set(
        self,
        domain: str,
        table: str,
        df: pd.DataFrame,
        metadata: Dict = None,
        **conditions,
    ):
        if df is None or df.empty:
            return

        if self._parquet_cache is not None:
            try:
                table_name = _resolve_table_name(domain, table)
                self._parquet_cache.put(table_name, df)
                return
            except Exception as e:
                logger.warning(f"parquet_cache put 失败，使用 fallback: {e}")

        self._fallback.set(domain, table, df, metadata, **conditions)

    def invalidate(self, domain: str = None, table: str = None, **conditions):
        if self._parquet_cache is not None:
            try:
                if domain and table:
                    table_name = _resolve_table_name(domain, table)
                    self._parquet_cache.invalidate(
                        table_name, where=conditions if conditions else None
                    )
                else:
                    self._parquet_cache.invalidate(table or domain)
                return
            except Exception as e:
                logger.warning(f"parquet_cache invalidate 失败: {e}")

        self._fallback.invalidate(domain, table, **conditions)

    def clear(self):
        if self._parquet_cache is not None:
            try:
                for table_name in self._parquet_cache.list_tables():
                    self._parquet_cache.invalidate(table_name)
                return
            except Exception as e:
                logger.warning(f"parquet_cache clear 失败: {e}")

        self._fallback.clear()

    def stats(self) -> Dict:
        result = {"backend_type": "parquet_cache" if self._parquet_cache else "simple"}

        if self._parquet_cache is not None:
            try:
                result["parquet_stats"] = self._parquet_cache.get_stats()
            except Exception:
                pass

        result["fallback_stats"] = self._fallback.stats()
        return result

    def has_data(self, domain: str, table: str, **conditions) -> bool:
        if self._parquet_cache is not None:
            try:
                table_name = _resolve_table_name(domain, table)
                where = conditions if conditions else None
                return self._parquet_cache.exists(table_name, where=where)
            except Exception:
                pass

        cached = self._fallback.get(domain, table, **conditions)
        return cached is not None and not cached.empty

    def get_ttl(self, domain: str) -> int:
        return self._domain_policies.get(domain, self._domain_policies["default"])

    def set_ttl(self, domain: str, ttl_hours: int):
        self._domain_policies[domain] = ttl_hours

    def register_domain(self, domain: str, db_path: str = None, schemas: list = None):
        logger.info(f"register_domain 已废弃（parquet_cache 使用 table_registry 管理）")

    @classmethod
    def get_instance(cls) -> "DataAccessCacheManager":
        return cls()

    @classmethod
    def reset_instance(cls):
        with cls._lock:
            cls._instance = None


# SimpleMemoryCache 保留不变（作为 fallback）
class SimpleMemoryCache:
    """简化版内存缓存 (当 parquet_cache 不可用时使用)"""

    def __init__(self, max_items: int = 1000, default_ttl_hours: int = 24):
        self._cache: Dict[str, pd.DataFrame] = {}
        self._timestamps: Dict[str, float] = {}
        self._metadata: Dict[str, Dict[str, Any]] = {}
        self._lock = threading.Lock()
        self._max_items = max_items
        self._default_ttl_hours = default_ttl_hours

    def _make_key(self, domain: str, table: str, **conditions) -> str:
        parts = [domain, table]
        for k, v in sorted(conditions.items()):
            if v is not None:
                parts.append(f"{k}={v}")
        return ":".join(parts)

    def get(self, domain: str, table: str, **conditions) -> Optional[pd.DataFrame]:
        key = self._make_key(domain, table, **conditions)
        with self._lock:
            if key in self._cache:
                timestamp = self._timestamps.get(key, 0)
                age_hours = (time.time() - timestamp) / 3600
                if age_hours < self._default_ttl_hours:
                    return self._cache[key].copy()
                else:
                    self._cache.pop(key, None)
                    self._timestamps.pop(key, None)
                    self._metadata.pop(key, None)
        return None

    def set(
        self,
        domain: str,
        table: str,
        df: pd.DataFrame,
        metadata: Dict = None,
        **conditions,
    ):
        key = self._make_key(domain, table, **conditions)
        with self._lock:
            if len(self._cache) >= self._max_items:
                oldest_key = min(self._timestamps, key=self._timestamps.get)
                self._cache.pop(oldest_key, None)
                self._timestamps.pop(oldest_key, None)
                self._metadata.pop(oldest_key, None)

            self._cache[key] = df.copy()
            self._timestamps[key] = time.time()
            if metadata:
                self._metadata[key] = metadata

    def invalidate(self, domain: str = None, table: str = None, **conditions):
        with self._lock:
            keys_to_remove = []
            key_prefix = self._make_key(domain or "", table or "", **conditions)

            for key in self._cache:
                if key_prefix and not key.startswith(key_prefix):
                    continue
                if domain and not key.startswith(domain + ":"):
                    continue
                keys_to_remove.append(key)

            for key in keys_to_remove:
                self._cache.pop(key, None)
                self._timestamps.pop(key, None)
                self._metadata.pop(key, None)

    def clear(self):
        with self._lock:
            self._cache.clear()
            self._timestamps.clear()
            self._metadata.clear()

    def stats(self) -> Dict:
        with self._lock:
            return {
                "total_items": len(self._cache),
                "max_items": self._max_items,
                "domains": list(set(k.split(":")[0] for k in self._cache.keys())),
            }


def get_cache() -> DataAccessCacheManager:
    """获取缓存管理器单例"""
    return DataAccessCacheManager.get_instance()


def clear_cache():
    """清空缓存"""
    get_cache().clear()


def reset_cache():
    """重置缓存管理器 (用于测试)"""
    DataAccessCacheManager.reset_instance()


__all__ = [
    "DataAccessCacheManager",
    "SimpleMemoryCache",
    "get_cache",
    "clear_cache",
    "reset_cache",
]
