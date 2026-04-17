"""
test_cache_status.py
测试缓存状态模块
"""

import pytest
from unittest.mock import patch, MagicMock


class TestCacheManager:
    """测试 CacheManager 类"""

    @pytest.fixture
    def mock_parquet_adapter(self):
        """创建 mock ParquetAdapter"""
        with patch("jk2bt.data.storage.cache_status.ParquetAdapter") as mock:
            instance = MagicMock()
            mock.return_value = instance
            yield instance

    def test_import(self):
        """测试导入"""
        from jk2bt.data.storage.cache_status import CacheManager

        assert CacheManager is not None

    def test_get_cache_manager_function(self):
        """测试 get_cache_manager 函数"""
        from jk2bt.data.storage.cache_status import get_cache_manager

        assert callable(get_cache_manager)

    def test_check_cache_status_function(self):
        """测试 check_cache_status 函数"""
        from jk2bt.data.storage.cache_status import check_cache_status

        assert callable(check_cache_status)


class TestCacheManagerMethods:
    """测试 CacheManager 方法"""

    def test_get_date_range_method(self):
        """测试 _get_date_range 方法存在"""
        from jk2bt.data.storage.cache_status import CacheManager

        assert hasattr(CacheManager, "_get_date_range")

    def test_check_stock_daily_cache_method(self):
        """测试 check_stock_daily_cache 方法存在"""
        from jk2bt.data.storage.cache_status import CacheManager

        assert hasattr(CacheManager, "check_stock_daily_cache")

    def test_check_etf_daily_cache_method(self):
        """测试 check_etf_daily_cache 方法存在"""
        from jk2bt.data.storage.cache_status import CacheManager

        assert hasattr(CacheManager, "check_etf_daily_cache")

    def test_check_index_daily_cache_method(self):
        """测试 check_index_daily_cache 方法存在"""
        from jk2bt.data.storage.cache_status import CacheManager

        assert hasattr(CacheManager, "check_index_daily_cache")

    def test_get_cache_summary_method(self):
        """测试 get_cache_summary 方法存在"""
        from jk2bt.data.storage.cache_status import CacheManager

        assert hasattr(CacheManager, "get_cache_summary")

    def test_check_meta_cache_method(self):
        """测试 check_meta_cache 方法存在"""
        from jk2bt.data.storage.cache_status import CacheManager

        assert hasattr(CacheManager, "check_meta_cache")

    def test_validate_cache_for_offline_method(self):
        """测试 validate_cache_for_offline 方法存在"""
        from jk2bt.data.storage.cache_status import CacheManager

        assert hasattr(CacheManager, "validate_cache_for_offline")


class TestCacheStatusResultStructure:
    """测试缓存状态结果结构"""

    def test_stock_daily_result_structure(self):
        """测试股票日线缓存结果结构"""
        from jk2bt.data.storage.cache_status import CacheManager
        import pandas as pd

        mock_db = MagicMock()
        mock_db.count_records.return_value = 0
        mock_db.query.return_value = pd.DataFrame()

        with patch.object(CacheManager, "__init__", lambda x, y=None: None):
            manager = CacheManager()
            manager.db = mock_db
            manager.db_path = None

            result = manager.check_stock_daily_cache(
                "600519", "2020-01-01", "2020-12-31"
            )

            assert "has_data" in result
            assert "is_complete" in result
            assert "min_date" in result
            assert "max_date" in result
            assert "count" in result

    def test_etf_daily_result_structure(self):
        """测试 ETF 日线缓存结果结构"""
        from jk2bt.data.storage.cache_status import CacheManager
        import pandas as pd

        mock_db = MagicMock()
        mock_db.count_records.return_value = 0
        mock_db.query.return_value = pd.DataFrame()

        with patch.object(CacheManager, "__init__", lambda x, y=None: None):
            manager = CacheManager()
            manager.db = mock_db
            manager.db_path = None

            result = manager.check_etf_daily_cache("510300", "2020-01-01", "2020-12-31")

            assert "has_data" in result
            assert "is_complete" in result

    def test_index_daily_result_structure(self):
        """测试指数日线缓存结果结构"""
        from jk2bt.data.storage.cache_status import CacheManager
        import pandas as pd

        mock_db = MagicMock()
        mock_db.count_records.return_value = 0
        mock_db.query.return_value = pd.DataFrame()

        with patch.object(CacheManager, "__init__", lambda x, y=None: None):
            manager = CacheManager()
            manager.db = mock_db
            manager.db_path = None

            result = manager.check_index_daily_cache(
                "000300", "2020-01-01", "2020-12-31"
            )

            assert "has_data" in result
            assert "is_complete" in result


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
