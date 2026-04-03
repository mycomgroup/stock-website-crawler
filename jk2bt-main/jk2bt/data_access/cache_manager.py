"""
src/data_access/cache_manager.py
数据访问层缓存管理器 - 整合 db/unified_cache.py。

提供统一的缓存管理接口，支持:
- 内存缓存 (快速访问)
- DuckDB 缓存 (持久化)
- 可配置的缓存策略 (TTL, 策略)
"""

import logging
import threading
import time
from typing import Optional, Dict, Any
from datetime import datetime, timedelta
import pandas as pd

logger = logging.getLogger(__name__)

# 尝试导入现有的统一缓存模块
_UNIFIED_CACHE_AVAILABLE = False
try:
    from jk2bt.db.unified_cache import (
        UnifiedCacheManager,
        CachePolicy,
        TableSchema,
        get_unified_cache,
    )
    _UNIFIED_CACHE_AVAILABLE = True
except ImportError:
    logger.warning("unified_cache 模块不可用，将使用简化缓存")


class SimpleMemoryCache:
    """简化版内存缓存 (当 unified_cache 不可用时使用)"""

    def __init__(self, max_items: int = 1000, default_ttl_hours: int = 24):
        self._cache: Dict[str, pd.DataFrame] = {}
        self._timestamps: Dict[str, float] = {}
        self._metadata: Dict[str, Dict[str, Any]] = {}
        self._lock = threading.Lock()
        self._max_items = max_items
        self._default_ttl_hours = default_ttl_hours

    def _make_key(self, domain: str, table: str, **conditions) -> str:
        """生成缓存 key"""
        parts = [domain, table]
        for k, v in sorted(conditions.items()):
            if v is not None:
                parts.append(f"{k}={v}")
        return ":".join(parts)

    def get(self, domain: str, table: str, **conditions) -> Optional[pd.DataFrame]:
        """获取缓存"""
        key = self._make_key(domain, table, **conditions)
        with self._lock:
            if key in self._cache:
                # 检查 TTL
                timestamp = self._timestamps.get(key, 0)
                age_hours = (time.time() - timestamp) / 3600
                if age_hours < self._default_ttl_hours:
                    return self._cache[key].copy()
                else:
                    # 缓存过期，删除
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
        """设置缓存"""
        key = self._make_key(domain, table, **conditions)
        with self._lock:
            # 检查容量，淘汰最旧
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
        """失效缓存"""
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
        """清空缓存"""
        with self._lock:
            self._cache.clear()
            self._timestamps.clear()
            self._metadata.clear()

    def stats(self) -> Dict:
        """缓存统计"""
        with self._lock:
            return {
                "total_items": len(self._cache),
                "max_items": self._max_items,
                "domains": list(set(k.split(":")[0] for k in self._cache.keys())),
            }


class DataAccessCacheManager:
    """
    数据访问层缓存管理器。

    整合现有的 unified_cache.py，提供统一接口。

    使用方式:
        cache = get_cache()
        df = cache.get('market', 'stock_daily', symbol='sh600000')
        cache.set('market', 'stock_daily', df, symbol='sh600000')
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
        """初始化缓存管理器"""
        if _UNIFIED_CACHE_AVAILABLE:
            self._backend = get_unified_cache()
            self._backend_type = "unified"
            logger.info("使用 UnifiedCacheManager 作为缓存后端")
        else:
            self._backend = SimpleMemoryCache()
            self._backend_type = "simple"
            logger.info("使用 SimpleMemoryCache 作为缓存后端")

        # 缓存策略配置
        self._domain_policies: Dict[str, int] = {
            "meta": 168,      # 元数据缓存 7 天
            "market": 24,     # 行情数据缓存 1 天
            "finance": 72,    # 财务数据缓存 3 天
            "index": 168,     # 指数成分股缓存 7 天
            "industry": 168,  # 行业数据缓存 7 天
            "default": 24,    # 默认缓存 1 天
        }

    @classmethod
    def get_instance(cls) -> "DataAccessCacheManager":
        """获取单例实例"""
        return cls()

    @classmethod
    def reset_instance(cls):
        """重置单例 (用于测试)"""
        with cls._lock:
            cls._instance = None

    def get_ttl(self, domain: str) -> int:
        """获取域的缓存 TTL"""
        return self._domain_policies.get(domain, self._domain_policies["default"])

    def set_ttl(self, domain: str, ttl_hours: int):
        """设置域的缓存 TTL"""
        self._domain_policies[domain] = ttl_hours

    def get(
        self,
        domain: str,
        table: str,
        use_cache: bool = True,
        **conditions,
    ) -> Optional[pd.DataFrame]:
        """
        获取缓存数据。

        Args:
            domain: 业务域 (如 'market', 'meta', 'finance')
            table: 表名 (如 'stock_daily', 'trade_days')
            use_cache: 是否使用缓存
            **conditions: 查询条件

        Returns:
            DataFrame 或 None (缓存不存在或过期)
        """
        if not use_cache:
            return None

        if self._backend_type == "unified":
            try:
                return self._backend.get(domain, table, use_cache=True, **conditions)
            except Exception as e:
                logger.warning(f"缓存获取失败: {e}")
                return None
        else:
            return self._backend.get(domain, table, **conditions)

    def set(
        self,
        domain: str,
        table: str,
        df: pd.DataFrame,
        metadata: Dict = None,
        **conditions,
    ):
        """
        设置缓存数据。

        Args:
            domain: 业务域
            table: 表名
            df: 数据 DataFrame
            metadata: 元数据 (可选)
            **conditions: 条件标识
        """
        if df is None or df.empty:
            return

        if self._backend_type == "unified":
            try:
                # unified_cache 使用 set 方法写入数据库并更新内存缓存
                self._backend.set(domain, table, df, **conditions)
            except Exception as e:
                logger.warning(f"缓存写入失败: {e}")
        else:
            self._backend.set(domain, table, df, metadata, **conditions)

    def invalidate(self, domain: str = None, table: str = None, **conditions):
        """失效缓存"""
        if self._backend_type == "unified":
            self._backend.invalidate(domain, table, **conditions)
        else:
            self._backend.invalidate(domain, table, **conditions)

    def clear(self):
        """清空所有缓存"""
        if self._backend_type == "unified":
            self._backend.clear_cache()
        else:
            self._backend.clear()

    def stats(self) -> Dict:
        """缓存统计信息"""
        if self._backend_type == "unified":
            stats = self._backend.stats()
            stats["backend_type"] = "unified"
            return stats
        else:
            return {
                "backend_type": "simple",
                **self._backend.stats(),
                "domain_policies": self._domain_policies,
            }

    def has_data(self, domain: str, table: str, **conditions) -> bool:
        """检查是否有缓存数据"""
        if self._backend_type == "unified":
            return self._backend.has_data(domain, table, **conditions)
        else:
            cached = self.get(domain, table, **conditions)
            return cached is not None and not cached.empty

    def register_domain(self, domain: str, db_path: str = None, schemas: list = None):
        """注册新的缓存域"""
        if self._backend_type == "unified" and db_path:
            try:
                self._backend.register_db(domain, db_path, schemas)
                logger.info(f"注册缓存域: {domain} -> {db_path}")
            except Exception as e:
                logger.warning(f"注册缓存域失败: {e}")


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