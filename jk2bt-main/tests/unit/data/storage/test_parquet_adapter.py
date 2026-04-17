"""
test_parquet_adapter.py
测试 Parquet 适配器
"""

import pytest
import pandas as pd
from unittest.mock import patch, MagicMock


class TestParquetAdapter:
    """测试 ParquetAdapter 类"""

    @pytest.fixture
    def mock_cache_manager(self):
        """创建 mock CacheManager"""
        mock = MagicMock()
        mock.get.return_value = pd.DataFrame()
        mock.put.return_value = None
        mock.query_engine.count.return_value = 0
        return mock

    def test_import(self):
        """测试导入"""
        from jk2bt.data.storage.parquet_adapter import ParquetAdapter

        assert ParquetAdapter is not None

    @patch("jk2bt.data.storage.parquet_adapter.get_cache_manager")
    def test_creation(self, mock_get_cache, mock_cache_manager):
        """测试创建实例"""
        mock_get_cache.return_value = mock_cache_manager
        from jk2bt.data.storage.parquet_adapter import ParquetAdapter

        adapter = ParquetAdapter()
        assert adapter is not None

    def test_table_map(self):
        """测试表映射"""
        from jk2bt.data.storage.parquet_adapter import _TABLE_MAP

        assert "stock_daily" in _TABLE_MAP
        assert "etf_daily" in _TABLE_MAP
        assert "index_daily" in _TABLE_MAP


class TestParquetAdapterMethods:
    """测试 ParquetAdapter 方法"""

    @patch("jk2bt.data.storage.parquet_adapter.get_cache_manager")
    def test_insert_methods_exist(self, mock_get_cache, mock_cache_manager):
        """测试插入方法存在"""
        mock_get_cache.return_value = mock_cache_manager
        from jk2bt.data.storage.parquet_adapter import ParquetAdapter

        adapter = ParquetAdapter()
        assert hasattr(adapter, "insert_stock_daily")
        assert hasattr(adapter, "insert_etf_daily")
        assert hasattr(adapter, "insert_index_daily")

    @patch("jk2bt.data.storage.parquet_adapter.get_cache_manager")
    def test_get_methods_exist(self, mock_get_cache, mock_cache_manager):
        """测试获取方法存在"""
        mock_get_cache.return_value = mock_cache_manager
        from jk2bt.data.storage.parquet_adapter import ParquetAdapter

        adapter = ParquetAdapter()
        assert hasattr(adapter, "get_stock_daily")
        assert hasattr(adapter, "get_etf_daily")
        assert hasattr(adapter, "get_index_daily")

    @patch("jk2bt.data.storage.parquet_adapter.get_cache_manager")
    def test_has_data_exists(self, mock_get_cache, mock_cache_manager):
        """测试 has_data 方法存在"""
        mock_get_cache.return_value = mock_cache_manager
        from jk2bt.data.storage.parquet_adapter import ParquetAdapter

        adapter = ParquetAdapter()
        assert hasattr(adapter, "has_data")

    @patch("jk2bt.data.storage.parquet_adapter.get_cache_manager")
    def test_count_records_exists(self, mock_get_cache, mock_cache_manager):
        """测试 count_records 方法存在"""
        mock_get_cache.return_value = mock_cache_manager
        from jk2bt.data.storage.parquet_adapter import ParquetAdapter

        adapter = ParquetAdapter()
        assert hasattr(adapter, "count_records")

    @patch("jk2bt.data.storage.parquet_adapter.get_cache_manager")
    def test_get_symbols_exists(self, mock_get_cache, mock_cache_manager):
        """测试 get_symbols 方法存在"""
        mock_get_cache.return_value = mock_cache_manager
        from jk2bt.data.storage.parquet_adapter import ParquetAdapter

        adapter = ParquetAdapter()
        assert hasattr(adapter, "get_symbols")

    @patch("jk2bt.data.storage.parquet_adapter.get_cache_manager")
    def test_clear_cache_exists(self, mock_get_cache, mock_cache_manager):
        """测试 clear_cache 方法存在"""
        mock_get_cache.return_value = mock_cache_manager
        from jk2bt.data.storage.parquet_adapter import ParquetAdapter

        adapter = ParquetAdapter()
        assert hasattr(adapter, "clear_cache")


class TestParquetAdapterInternalMethods:
    """测试 ParquetAdapter 内部方法"""

    @patch("jk2bt.data.storage.parquet_adapter.get_cache_manager")
    def test_to_jq_exists(self, mock_get_cache, mock_cache_manager):
        """测试 _to_jq 方法存在"""
        mock_get_cache.return_value = mock_cache_manager
        from jk2bt.data.storage.parquet_adapter import ParquetAdapter

        adapter = ParquetAdapter()
        assert hasattr(adapter, "_to_jq")

    @patch("jk2bt.data.storage.parquet_adapter.get_cache_manager")
    def test_rename_to_date_exists(self, mock_get_cache, mock_cache_manager):
        """测试 _rename_to_date 方法存在"""
        mock_get_cache.return_value = mock_cache_manager
        from jk2bt.data.storage.parquet_adapter import ParquetAdapter

        adapter = ParquetAdapter()
        assert hasattr(adapter, "_rename_to_date")

    @patch("jk2bt.data.storage.parquet_adapter.get_cache_manager")
    def test_rename_to_datetime_exists(self, mock_get_cache, mock_cache_manager):
        """测试 _rename_to_datetime 方法存在"""
        mock_get_cache.return_value = mock_cache_manager
        from jk2bt.data.storage.parquet_adapter import ParquetAdapter

        adapter = ParquetAdapter()
        assert hasattr(adapter, "_rename_to_datetime")

    @patch("jk2bt.data.storage.parquet_adapter.get_cache_manager")
    def test_ensure_amount_exists(self, mock_get_cache, mock_cache_manager):
        """测试 _ensure_amount 方法存在"""
        mock_get_cache.return_value = mock_cache_manager
        from jk2bt.data.storage.parquet_adapter import ParquetAdapter

        adapter = ParquetAdapter()
        assert hasattr(adapter, "_ensure_amount")


class TestFactoryFunctions:
    """测试工厂函数"""

    @patch("jk2bt.data.storage.parquet_adapter.get_cache_manager")
    def test_get_shared_read_only_manager(self, mock_get_cache, mock_cache_manager):
        """测试获取只读管理器"""
        mock_get_cache.return_value = mock_cache_manager
        from jk2bt.data.storage.parquet_adapter import get_shared_read_only_manager

        manager = get_shared_read_only_manager()
        assert manager.read_only is True

    @patch("jk2bt.data.storage.parquet_adapter.get_cache_manager")
    def test_get_writer_manager(self, mock_get_cache, mock_cache_manager):
        """测试获取写入管理器"""
        mock_get_cache.return_value = mock_cache_manager
        from jk2bt.data.storage.parquet_adapter import get_writer_manager

        manager = get_writer_manager()
        assert manager.read_only is False

    @patch("jk2bt.data.storage.parquet_adapter.get_cache_manager")
    def test_get_manager_read_only(self, mock_get_cache, mock_cache_manager):
        """测试 get_manager 只读模式"""
        mock_get_cache.return_value = mock_cache_manager
        from jk2bt.data.storage.parquet_adapter import get_manager

        manager = get_manager(read_only=True)
        assert manager.read_only is True


class TestLocalCacheStub:
    """测试 LocalCache 存根类"""

    def test_local_cache_stub_exists(self):
        """测试 LocalCache 存根存在"""
        from jk2bt.data.storage.parquet_adapter import LocalCache

        assert LocalCache is not None

    def test_local_cache_stub_methods(self):
        """测试 LocalCache 存根方法"""
        from jk2bt.data.storage.parquet_adapter import LocalCache

        cache = LocalCache()
        assert hasattr(cache, "get")
        assert hasattr(cache, "set")
        assert hasattr(cache, "invalidate")
        assert hasattr(cache, "clear")


class TestClearGlobalCache:
    """测试清除全局缓存"""

    def test_clear_global_cache_exists(self):
        """测试 clear_global_cache 函数存在"""
        from jk2bt.data.storage.parquet_adapter import clear_global_cache

        assert callable(clear_global_cache)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
