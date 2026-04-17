"""
test_duckdb_manager.py
测试 DuckDB 管理器
"""

import pytest
import pandas as pd
from unittest.mock import patch, MagicMock


class TestLocalCache:
    """测试 LocalCache 本地缓存类"""

    def test_import(self):
        """测试导入"""
        from jk2bt.data.storage.duckdb_manager import LocalCache

        assert LocalCache is not None

    def test_creation(self):
        """测试创建"""
        from jk2bt.data.storage.duckdb_manager import LocalCache

        cache = LocalCache(max_size=100)
        assert cache._max_size == 100

    def test_make_key(self):
        """测试缓存键生成"""
        from jk2bt.data.storage.duckdb_manager import LocalCache

        cache = LocalCache()
        key = cache._make_key("stock_daily", "600519", "2020-01-01", "2020-12-31")
        assert "stock_daily" in key
        assert "600519" in key

    def test_get_set(self):
        """测试获取和设置"""
        from jk2bt.data.storage.duckdb_manager import LocalCache

        cache = LocalCache()
        df = pd.DataFrame({"a": [1, 2, 3]})
        cache.set("table", "symbol", "start", "end", df)
        result = cache.get("table", "symbol", "start", "end")
        assert result is not None
        assert len(result) == 3

    def test_get_miss(self):
        """测试缓存未命中"""
        from jk2bt.data.storage.duckdb_manager import LocalCache

        cache = LocalCache()
        result = cache.get("nonexistent", "key", "start", "end")
        assert result is None

    def test_invalidate(self):
        """测试失效"""
        from jk2bt.data.storage.duckdb_manager import LocalCache

        cache = LocalCache()
        df = pd.DataFrame({"a": [1]})
        cache.set("table", "symbol", "start", "end", df)
        cache.invalidate(table="table")
        result = cache.get("table", "symbol", "start", "end")
        assert result is None

    def test_clear(self):
        """测试清空"""
        from jk2bt.data.storage.duckdb_manager import LocalCache

        cache = LocalCache()
        df = pd.DataFrame({"a": [1]})
        cache.set("t1", "s1", "start", "end", df)
        cache.set("t2", "s2", "start", "end", df)
        cache.clear()
        assert len(cache._cache) == 0


class TestDuckDBManagerCreation:
    """测试 DuckDBManager 创建"""

    @patch("jk2bt.data.storage.duckdb_manager.duckdb")
    def test_creation(self, mock_duckdb):
        """测试创建实例"""
        from jk2bt.data.storage.duckdb_manager import DuckDBManager

        manager = DuckDBManager(db_path=":memory:", read_only=True)
        assert manager.db_path == ":memory:"
        assert manager.read_only is True

    @patch("jk2bt.data.storage.duckdb_manager.duckdb")
    def test_default_values(self, mock_duckdb):
        """测试默认值"""
        from jk2bt.data.storage.duckdb_manager import DuckDBManager

        manager = DuckDBManager()
        assert manager.use_cache is True


class TestDuckDBManagerConstants:
    """测试 DuckDBManager 常量"""

    def test_write_retry_count(self):
        """测试写入重试次数"""
        from jk2bt.data.storage.duckdb_manager import DuckDBManager

        assert hasattr(DuckDBManager, "_WRITE_RETRY_COUNT")
        assert DuckDBManager._WRITE_RETRY_COUNT > 0

    def test_silent_retry_flag(self):
        """测试静默重试标志"""
        from jk2bt.data.storage.duckdb_manager import DuckDBManager

        assert hasattr(DuckDBManager, "_SILENT_RETRY")
        assert isinstance(DuckDBManager._SILENT_RETRY, bool)


class TestGlobalCache:
    """测试全局缓存"""

    def test_global_cache_exists(self):
        """测试全局缓存存在"""
        from jk2bt.data.storage.duckdb_manager import _global_cache

        assert _global_cache is not None

    def test_clear_global_cache(self):
        """测试清除全局缓存"""
        from jk2bt.data.storage.duckdb_manager import clear_global_cache, _global_cache

        clear_global_cache()
        assert len(_global_cache._cache) == 0


class TestFactoryFunctions:
    """测试工厂函数"""

    @patch("jk2bt.data.storage.duckdb_manager.duckdb")
    def test_get_shared_read_only_manager(self, mock_duckdb):
        """测试获取只读管理器"""
        from jk2bt.data.storage.duckdb_manager import get_shared_read_only_manager

        manager = get_shared_read_only_manager(db_path=":memory:")
        assert manager.read_only is True

    @patch("jk2bt.data.storage.duckdb_manager.duckdb")
    def test_get_writer_manager(self, mock_duckdb):
        """测试获取写入管理器"""
        from jk2bt.data.storage.duckdb_manager import get_writer_manager

        manager = get_writer_manager(db_path=":memory:")
        assert manager.read_only is False

    @patch("jk2bt.data.storage.duckdb_manager.duckdb")
    def test_get_manager_read_only(self, mock_duckdb):
        """测试 get_manager 只读模式"""
        from jk2bt.data.storage.duckdb_manager import get_manager

        manager = get_manager(db_path=":memory:", read_only=True)
        assert manager.read_only is True

    @patch("jk2bt.data.storage.duckdb_manager.duckdb")
    def test_get_manager_write(self, mock_duckdb):
        """测试 get_manager 写入模式"""
        from jk2bt.data.storage.duckdb_manager import get_manager

        manager = get_manager(db_path=":memory:", read_only=False)
        assert manager.read_only is False


class TestDuckDBManagerMethods:
    """测试 DuckDBManager 方法"""

    @patch("jk2bt.data.storage.duckdb_manager.duckdb")
    def test_has_insert_methods(self, mock_duckdb):
        """测试插入方法存在"""
        from jk2bt.data.storage.duckdb_manager import DuckDBManager

        assert hasattr(DuckDBManager, "insert_stock_daily")
        assert hasattr(DuckDBManager, "insert_etf_daily")
        assert hasattr(DuckDBManager, "insert_index_daily")

    @patch("jk2bt.data.storage.duckdb_manager.duckdb")
    def test_has_get_methods(self, mock_duckdb):
        """测试获取方法存在"""
        from jk2bt.data.storage.duckdb_manager import DuckDBManager

        assert hasattr(DuckDBManager, "get_stock_daily")
        assert hasattr(DuckDBManager, "get_etf_daily")
        assert hasattr(DuckDBManager, "get_index_daily")

    @patch("jk2bt.data.storage.duckdb_manager.duckdb")
    def test_has_has_data(self, mock_duckdb):
        """测试 has_data 方法存在"""
        from jk2bt.data.storage.duckdb_manager import DuckDBManager

        assert hasattr(DuckDBManager, "has_data")

    @patch("jk2bt.data.storage.duckdb_manager.duckdb")
    def test_has_count_records(self, mock_duckdb):
        """测试 count_records 方法存在"""
        from jk2bt.data.storage.duckdb_manager import DuckDBManager

        assert hasattr(DuckDBManager, "count_records")

    @patch("jk2bt.data.storage.duckdb_manager.duckdb")
    def test_has_get_symbols(self, mock_duckdb):
        """测试 get_symbols 方法存在"""
        from jk2bt.data.storage.duckdb_manager import DuckDBManager

        assert hasattr(DuckDBManager, "get_symbols")


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
