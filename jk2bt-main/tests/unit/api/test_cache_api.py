"""
tests/unit/api/test_cache_api.py
缓存 API 单元测试

测试覆盖:
1. CurrentDataCache - 当前数据缓存器
2. get_current_data_cached - 带缓存的当前数据获取
3. get_current_data_batch - 批量获取当前数据
4. BatchDataLoader - 批量数据加载器
5. DataPreloader - 数据预加载器
6. 缓存函数
"""

import pytest
import pandas as pd
import numpy as np
from unittest.mock import patch, MagicMock
import threading
import time


class TestCurrentDataCache:
    """测试 CurrentDataCache 类"""

    def test_singleton(self):
        from jk2bt.api.cache import CurrentDataCache

        cache1 = CurrentDataCache()
        cache2 = CurrentDataCache()

        assert cache1 is cache2

    def test_get_without_cache(self):
        from jk2bt.api.cache import CurrentDataCache

        cache = CurrentDataCache()
        cache._cache.clear()
        cache._timestamps.clear()

        with patch("jk2bt.api.cache.get_current_data") as mock_get_cd:
            mock_entry = MagicMock()
            mock_entry.last_price = 100.0
            mock_get_cd.return_value = {"600519.XSHG": mock_entry}

            result = cache.get("600519.XSHG")

            assert result is not None

    def test_invalidate_all(self):
        from jk2bt.api.cache import CurrentDataCache

        cache = CurrentDataCache()
        cache._cache["test"] = "value"
        cache._timestamps["test"] = datetime.now()

        cache.invalidate()

        assert len(cache._cache) == 0
        assert len(cache._timestamps) == 0

    def test_invalidate_single(self):
        from jk2bt.api.cache import CurrentDataCache
        from datetime import datetime

        cache = CurrentDataCache()
        cache._cache["test1"] = "value1"
        cache._cache["test2"] = "value2"
        cache._timestamps["test1"] = datetime.now()
        cache._timestamps["test2"] = datetime.now()

        cache.invalidate("test1")

        assert "test1" not in cache._cache
        assert "test2" in cache._cache

    def test_set_ttl(self):
        from jk2bt.api.cache import CurrentDataCache

        cache = CurrentDataCache()
        cache.set_ttl(120)

        assert cache._ttl_seconds == 120


class TestGetCurrentDataCached:
    """测试带缓存的当前数据获取"""

    @patch("jk2bt.api.cache.CurrentDataCache")
    def test_get_current_data_cached(self, mock_cache_class):
        mock_cache = MagicMock()
        mock_entry = MagicMock()
        mock_entry.last_price = 100.0
        mock_cache.get.return_value = mock_entry
        mock_cache_class.return_value = mock_cache

        from jk2bt.api.cache import get_current_data_cached

        result = get_current_data_cached("600519.XSHG")

        mock_cache.get.assert_called_once()


class TestGetCurrentDataBatch:
    """测试批量获取当前数据"""

    @patch("jk2bt.api.cache.CurrentDataCache")
    def test_get_current_data_batch_with_cache(self, mock_cache_class):
        mock_cache = MagicMock()
        mock_entry = MagicMock()
        mock_entry.last_price = 100.0
        mock_cache.get.return_value = mock_entry
        mock_cache_class.return_value = mock_cache

        from jk2bt.api.cache import get_current_data_batch

        codes = ["600519.XSHG", "000001.XSHE"]
        result = get_current_data_batch(codes, use_cache=True)

        assert len(result) == 2

    @patch("jk2bt.api.cache.get_current_data")
    def test_get_current_data_batch_without_cache(self, mock_get_cd):
        mock_entry = MagicMock()
        mock_entry.last_price = 100.0
        mock_get_cd.return_value = {
            "600519.XSHG": mock_entry,
            "000001.XSHE": mock_entry,
        }

        from jk2bt.api.cache import get_current_data_batch

        codes = ["600519.XSHG", "000001.XSHE"]
        result = get_current_data_batch(codes, use_cache=False)

        assert len(result) == 2


class TestBatchDataLoader:
    """测试批量数据加载器"""

    @patch("jk2bt.api.cache.get_price")
    def test_load_stocks(self, mock_get_price):
        mock_get_price.return_value = pd.DataFrame(
            {
                "datetime": pd.date_range("2024-01-01", periods=5),
                "open": [100, 101, 102, 103, 104],
                "high": [105, 106, 107, 108, 109],
                "low": [95, 96, 97, 98, 99],
                "close": [100, 101, 102, 103, 104],
                "volume": [1000, 1100, 1200, 1300, 1400],
            }
        )

        from jk2bt.api.cache import BatchDataLoader

        loader = BatchDataLoader()
        result = loader.load_stocks(["600519.XSHG"], "2024-01-01", "2024-01-05")

        assert "600519.XSHG" in result

    @patch("jk2bt.api.cache.get_index_stocks")
    @patch("jk2bt.api.cache.BatchDataLoader.load_stocks")
    def test_preload_index_stocks(self, mock_load, mock_get_index):
        mock_get_index.return_value = ["600519.XSHG", "000001.XSHE"]

        from jk2bt.api.cache import BatchDataLoader

        loader = BatchDataLoader()
        loader.preload_index_stocks("000300.XSHG", "2024-01-01", "2024-01-05")

        mock_load.assert_called_once()


class TestDataPreloader:
    """测试数据预加载器"""

    def test_init(self):
        from jk2bt.api.cache import DataPreloader

        preloader = DataPreloader()

        assert preloader._loaded_data == {}

    @patch("jk2bt.api.cache.BatchDataLoader")
    def test_preload_market_data(self, mock_loader_class):
        mock_loader = MagicMock()
        mock_loader.load_stocks.return_value = {"600519.XSHG": pd.DataFrame()}
        mock_loader_class.return_value = mock_loader

        from jk2bt.api.cache import DataPreloader

        preloader = DataPreloader()
        preloader.preload_market_data(["600519.XSHG"], "2024-01-01", "2024-01-05")

        assert "market" in preloader._loaded_data

    def test_get_loaded_data(self):
        from jk2bt.api.cache import DataPreloader

        preloader = DataPreloader()
        preloader._loaded_data["test"] = {"key": "value"}

        result = preloader.get_loaded_data("test")

        assert result == {"key": "value"}

    def test_get_loaded_data_not_found(self):
        from jk2bt.api.cache import DataPreloader

        preloader = DataPreloader()

        result = preloader.get_loaded_data("nonexistent")

        assert result is None

    def test_clear(self):
        from jk2bt.api.cache import DataPreloader

        preloader = DataPreloader()
        preloader._loaded_data = {"test": "value"}

        preloader.clear()

        assert len(preloader._loaded_data) == 0


class TestOptimizeDataFrameMemory:
    """测试 DataFrame 内存优化"""

    def test_optimize_dataframe_memory(self):
        from jk2bt.api.cache import optimize_dataframe_memory

        df = pd.DataFrame(
            {
                "string_col": ["a", "b", "c", "d"] * 10,
                "float_col": np.random.randn(40),
                "int_col": np.random.randint(0, 100, 40),
            }
        )

        result = optimize_dataframe_memory(df)

        assert result is not None


class TestBatchGetFundamentals:
    """测试批量获取财务数据"""

    @patch("jk2bt.api.cache.get_fundamentals")
    def test_batch_get_fundamentals(self, mock_get_fund):
        mock_get_fund.return_value = pd.DataFrame({"code": ["600519.XSHG"], "pe": [30]})

        from jk2bt.api.cache import batch_get_fundamentals

        class MockQuery:
            _symbols = ["600519.XSHG"]

        result = batch_get_fundamentals(MockQuery(), ["600519.XSHG"])

        assert isinstance(result, pd.DataFrame)


class TestWarmUpCache:
    """测试缓存预热"""

    @patch("jk2bt.api.cache.cached_get_security_info")
    @patch("jk2bt.api.cache.CurrentDataCache")
    def test_warm_up_cache(self, mock_cache_class, mock_security_info):
        mock_cache = MagicMock()
        mock_cache_class.return_value = mock_cache

        from jk2bt.api.cache import warm_up_cache

        warm_up_cache(["600519.XSHG"])

        mock_cache.get.assert_called()


class TestMemoryUsage:
    """测试内存使用获取"""

    @patch("psutil.Process")
    def test_get_memory_usage(self, mock_process_class):
        mock_process = MagicMock()
        mock_process.memory_info.return_value.rss = 1024 * 1024 * 100
        mock_process.memory_info.return_value.vms = 1024 * 1024 * 200
        mock_process.memory_percent.return_value = 5.0
        mock_process_class.return_value = mock_process

        from jk2bt.api.cache import get_memory_usage

        result = get_memory_usage()

        assert "rss" in result
        assert "vms" in result
        assert "percent" in result


class TestCleanupMemory:
    """测试内存清理"""

    @patch("gc.collect")
    @patch("jk2bt.api.cache.cached_get_index_stocks")
    @patch("jk2bt.api.cache.cached_get_security_info")
    @patch("jk2bt.api.cache.CurrentDataCache")
    def test_cleanup_memory(self, mock_cache_class, mock_sec, mock_idx, mock_gc):
        from jk2bt.api.cache import cleanup_memory

        cleanup_memory()

        mock_cache_class.return_value.invalidate.assert_called()


class TestCacheModuleExports:
    """测试模块导出"""

    def test_all_exports_exist(self):
        from jk2bt.api.cache import __all__

        expected = [
            "CurrentDataCache",
            "get_current_data_cached",
            "get_current_data_batch",
            "cached_get_security_info",
            "cached_get_index_stocks",
            "BatchDataLoader",
            "DataPreloader",
            "preload_data_for_strategy",
            "batch_get_fundamentals",
            "warm_up_cache",
            "get_memory_usage",
            "cleanup_memory",
            "optimize_dataframe_memory",
        ]

        for name in expected:
            assert name in __all__, f"{name} not in __all__"
