"""
test_unified_cache.py
测试统一缓存模块
"""

import pytest
from unittest.mock import patch, MagicMock
import pandas as pd


class TestCachePolicy:
    """测试 CachePolicy 数据类"""

    def test_import(self):
        """测试导入"""
        from jk2bt.data.storage.unified_cache import CachePolicy

        assert CachePolicy is not None

    def test_creation(self):
        """测试创建"""
        from jk2bt.data.storage.unified_cache import CachePolicy

        policy = CachePolicy(domain="test", ttl_hours=24)
        assert policy.domain == "test"
        assert policy.ttl_hours == 24

    def test_is_valid_with_ttl(self):
        """测试 TTL 有效性"""
        from jk2bt.data.storage.unified_cache import CachePolicy
        import time

        policy = CachePolicy(domain="test", ttl_hours=1)
        timestamp = time.time() - 1800
        assert policy.is_valid(timestamp) is True

    def test_is_valid_expired(self):
        """测试过期"""
        from jk2bt.data.storage.unified_cache import CachePolicy
        import time

        policy = CachePolicy(domain="test", ttl_hours=1)
        timestamp = time.time() - 7200
        assert policy.is_valid(timestamp) is False

    def test_is_valid_no_ttl(self):
        """测试无 TTL 永远有效"""
        from jk2bt.data.storage.unified_cache import CachePolicy
        import time

        policy = CachePolicy(domain="test", ttl_hours=0)
        timestamp = time.time() - 100000
        assert policy.is_valid(timestamp) is True


class TestTableSchema:
    """测试 TableSchema 数据类"""

    def test_import(self):
        """测试导入"""
        from jk2bt.data.storage.unified_cache import TableSchema

        assert TableSchema is not None

    def test_creation(self):
        """测试创建"""
        from jk2bt.data.storage.unified_cache import TableSchema

        schema = TableSchema(
            name="test",
            columns=[("col1", "VARCHAR"), ("col2", "INTEGER")],
            primary_key=["col1"],
        )
        assert schema.name == "test"
        assert len(schema.columns) == 2

    def test_create_sql(self):
        """测试生成 SQL"""
        from jk2bt.data.storage.unified_cache import TableSchema

        schema = TableSchema(
            name="test",
            columns=[("col1", "VARCHAR"), ("col2", "INTEGER")],
            primary_key=["col1"],
        )
        sql = schema.create_sql()
        assert "CREATE TABLE IF NOT EXISTS test" in sql
        assert "col1" in sql
        assert "col2" in sql

    def test_index_sqls(self):
        """测试生成索引 SQL"""
        from jk2bt.data.storage.unified_cache import TableSchema

        schema = TableSchema(
            name="test",
            columns=[("col1", "VARCHAR"), ("col2", "INTEGER")],
            primary_key=["col1"],
            indexes=["col2"],
        )
        sqls = schema.index_sqls()
        assert len(sqls) == 1
        assert "CREATE INDEX" in sqls[0]


class TestSharedMemoryCache:
    """测试共享内存缓存"""

    def test_import(self):
        """测试导入"""
        from jk2bt.data.storage.unified_cache import SharedMemoryCache

        assert SharedMemoryCache is not None

    @patch("jk2bt.data.storage.unified_cache.get_config")
    def test_creation(self, mock_config):
        """测试创建"""
        mock_config.return_value.cache.max_memory_items = 1000
        cache = SharedMemoryCache()
        assert cache._max_items == 1000

    def test_make_key(self):
        """测试生成缓存键"""
        with patch("jk2bt.data.storage.unified_cache.get_config") as mock_config:
            mock_config.return_value.cache.max_memory_items = 1000
            from jk2bt.data.storage.unified_cache import SharedMemoryCache

            cache = SharedMemoryCache()
            key = cache._make_key("domain", "table", symbol="600519")
            assert "domain" in key
            assert "table" in key
            assert "600519" in key

    def test_get_set(self):
        """测试获取和设置"""
        with patch("jk2bt.data.storage.unified_cache.get_config") as mock_config:
            mock_config.return_value.cache.max_memory_items = 1000
            from jk2bt.data.storage.unified_cache import SharedMemoryCache

            cache = SharedMemoryCache()
            df = pd.DataFrame({"a": [1, 2, 3]})
            cache.set("domain", "table", df, symbol="600519")
            result = cache.get("domain", "table", symbol="600519")
            assert result is not None
            assert len(result) == 3

    def test_get_miss(self):
        """测试缓存未命中"""
        with patch("jk2bt.data.storage.unified_cache.get_config") as mock_config:
            mock_config.return_value.cache.max_memory_items = 1000
            from jk2bt.data.storage.unified_cache import SharedMemoryCache

            cache = SharedMemoryCache()
            result = cache.get("nonexistent", "table")
            assert result is None

    def test_invalidate(self):
        """测试失效"""
        with patch("jk2bt.data.storage.unified_cache.get_config") as mock_config:
            mock_config.return_value.cache.max_memory_items = 1000
            from jk2bt.data.storage.unified_cache import SharedMemoryCache

            cache = SharedMemoryCache()
            df = pd.DataFrame({"a": [1]})
            cache.set("domain", "table1", df)
            cache.set("domain", "table2", df)
            cache.invalidate(table="table1")
            assert cache.get("domain", "table1") is None
            assert cache.get("domain", "table2") is not None

    def test_clear(self):
        """测试清空"""
        with patch("jk2bt.data.storage.unified_cache.get_config") as mock_config:
            mock_config.return_value.cache.max_memory_items = 1000
            from jk2bt.data.storage.unified_cache import SharedMemoryCache

            cache = SharedMemoryCache()
            df = pd.DataFrame({"a": [1]})
            cache.set("d1", "t1", df)
            cache.set("d2", "t2", df)
            cache.clear()
            assert len(cache._cache) == 0

    def test_stats(self):
        """测试统计"""
        with patch("jk2bt.data.storage.unified_cache.get_config") as mock_config:
            mock_config.return_value.cache.max_memory_items = 1000
            from jk2bt.data.storage.unified_cache import SharedMemoryCache

            cache = SharedMemoryCache()
            df = pd.DataFrame({"a": [1]})
            cache.set("domain1", "table1", df)
            stats = cache.stats()
            assert "total_items" in stats
            assert "max_items" in stats
            assert "domains" in stats


class TestUnifiedCacheManager:
    """测试统一缓存管理器"""

    @patch("jk2bt.data.storage.unified_cache.get_config")
    def test_singleton_pattern(self, mock_config):
        """测试单例模式"""
        mock_config.return_value.cache.max_memory_items = 1000
        mock_config.return_value.cache.ttl_hours = 24
        from jk2bt.data.storage.unified_cache import UnifiedCacheManager

        UnifiedCacheManager.reset_instance()
        manager1 = UnifiedCacheManager.get_instance()
        manager2 = UnifiedCacheManager.get_instance()
        assert manager1 is manager2

    @patch("jk2bt.data.storage.unified_cache.get_config")
    def test_register_db(self, mock_config):
        """测试注册数据库"""
        mock_config.return_value.cache.max_memory_items = 1000
        mock_config.return_value.cache.ttl_hours = 24
        from jk2bt.data.storage.unified_cache import UnifiedCacheManager

        UnifiedCacheManager.reset_instance()
        manager = UnifiedCacheManager.get_instance()
        manager.register_db("test_domain", "/tmp/test.db", [], False)
        assert "test_domain" in manager._db_adapters

    @patch("jk2bt.data.storage.unified_cache.get_config")
    def test_register_policy(self, mock_config):
        """测试注册策略"""
        mock_config.return_value.cache.max_memory_items = 1000
        mock_config.return_value.cache.ttl_hours = 24
        from jk2bt.data.storage.unified_cache import UnifiedCacheManager, CachePolicy

        UnifiedCacheManager.reset_instance()
        manager = UnifiedCacheManager.get_instance()
        policy = CachePolicy(domain="test", ttl_hours=12)
        manager.register_policy(policy)
        assert manager.get_policy("test").ttl_hours == 12

    @patch("jk2bt.data.storage.unified_cache.get_config")
    def test_reset_instance(self, mock_config):
        """测试重置单例"""
        mock_config.return_value.cache.max_memory_items = 1000
        mock_config.return_value.cache.ttl_hours = 24
        from jk2bt.data.storage.unified_cache import UnifiedCacheManager

        UnifiedCacheManager.reset_instance()
        manager1 = UnifiedCacheManager.get_instance()
        UnifiedCacheManager.reset_instance()
        manager2 = UnifiedCacheManager.get_instance()
        assert manager1 is not manager2


class TestConvenienceFunctions:
    """测试便捷函数"""

    def test_get_unified_cache_exists(self):
        """测试 get_unified_cache 函数存在"""
        from jk2bt.data.storage.unified_cache import get_unified_cache

        assert callable(get_unified_cache)

    def test_clear_unified_cache_exists(self):
        """测试 clear_unified_cache 函数存在"""
        from jk2bt.data.storage.unified_cache import clear_unified_cache

        assert callable(clear_unified_cache)

    def test_reset_unified_cache_exists(self):
        """测试 reset_unified_cache 函数存在"""
        from jk2bt.data.storage.unified_cache import reset_unified_cache

        assert callable(reset_unified_cache)


class TestDuckDBAdapter:
    """测试 DuckDB 适配器"""

    @patch("jk2bt.data.storage.unified_cache.duckdb")
    def test_import(self, mock_duckdb):
        """测试导入"""
        from jk2bt.data.storage.unified_cache import DuckDBAdapter

        assert DuckDBAdapter is not None

    @patch("jk2bt.data.storage.unified_cache.duckdb")
    def test_creation(self, mock_duckdb):
        """测试创建"""
        from jk2bt.data.storage.unified_cache import DuckDBAdapter

        adapter = DuckDBAdapter("/tmp/test.db", read_only=True)
        assert adapter.db_path == "/tmp/test.db"
        assert adapter.read_only is True


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
