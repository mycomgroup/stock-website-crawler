"""
tests/unit/data/market/test_etf.py
单元测试 for jk2bt/data/market/etf.py

覆盖场景:
- get_etf_daily: 缓存命中、缓存未命中、数据源失败回退缓存、写入失败
- 日期过滤逻辑
- 空数据处理
"""

import pytest
import pandas as pd
from unittest.mock import patch, MagicMock
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))


def _make_sample_df(start="2024-01-02", end="2024-01-10", rows=5):
    """生成标准化 OHLCV 测试数据"""
    dates = pd.date_range(start, periods=rows, freq="B")
    return pd.DataFrame(
        {
            "datetime": dates,
            "open": [10.0 + i for i in range(rows)],
            "high": [11.0 + i for i in range(rows)],
            "low": [9.0 + i for i in range(rows)],
            "close": [10.5 + i for i in range(rows)],
            "volume": [1000 + i * 100 for i in range(rows)],
            "amount": [10000.0 + i * 1000 for i in range(rows)],
        }
    )


def _make_raw_df_chinese(start="2024-01-02", rows=5):
    """生成中文列名的原始数据（akshare 格式）"""
    dates = pd.date_range(start, periods=rows, freq="B")
    return pd.DataFrame(
        {
            "datetime": dates,
            "开盘": [10.0 + i for i in range(rows)],
            "最高": [11.0 + i for i in range(rows)],
            "最低": [9.0 + i for i in range(rows)],
            "收盘": [10.5 + i for i in range(rows)],
            "成交量": [1000 + i * 100 for i in range(rows)],
            "成交额": [10000.0 + i * 1000 for i in range(rows)],
        }
    )


@pytest.fixture(autouse=True)
def reset_singletons():
    """每个测试前重置 DuckDB 单例缓存"""
    try:
        from jk2bt.data.storage import parquet_adapter

        parquet_adapter._PROCESS_SINGLETONS.clear()
    except ImportError:
        pass
    yield


class TestGetEtfDaily:
    """测试 get_etf_daily 函数"""

    @patch("jk2bt.data.market.etf.ParquetAdapter")
    @patch("jk2bt.data.market.etf.get_adapter")
    def test_cache_hit_returns_cached_data(self, mock_get_adapter, mock_parquet):
        """缓存命中：直接返回缓存数据"""
        sample_df = _make_sample_df()

        db_mock = MagicMock()
        db_mock.has_data.return_value = True
        db_mock.get_etf_daily.return_value = sample_df
        mock_parquet.return_value = db_mock

        from jk2bt.data.market.etf import get_etf_daily

        result = get_etf_daily("510300", "2024-01-01", "2024-01-31")

        db_mock.has_data.assert_called_once()
        mock_get_adapter.assert_not_called()
        assert isinstance(result, pd.DataFrame)
        assert not result.empty

    @patch("jk2bt.data.market.etf.ParquetAdapter")
    @patch("jk2bt.data.market.etf.get_adapter")
    def test_cache_miss_fetches_from_source(self, mock_get_adapter, mock_parquet):
        """缓存未命中：从数据源获取"""
        sample_df = _make_sample_df()

        db_mock = MagicMock()
        db_mock.has_data.return_value = False
        db_mock.get_etf_daily.return_value = pd.DataFrame()
        mock_parquet.return_value = db_mock

        adapter_mock = MagicMock()
        adapter_mock.get_etf_daily.return_value = _make_raw_df_chinese()
        mock_get_adapter.return_value = adapter_mock

        write_mock = MagicMock()
        db_mock.insert_etf_daily = write_mock.insert_etf_daily

        from jk2bt.data.market.etf import get_etf_daily

        result = get_etf_daily("510300", "2024-01-01", "2024-01-31")

        adapter_mock.get_etf_daily.assert_called_once()
        assert isinstance(result, pd.DataFrame)
        assert not result.empty

    @patch("jk2bt.data.market.etf.ParquetAdapter")
    @patch("jk2bt.data.market.etf.get_adapter")
    def test_force_update_bypasses_cache(self, mock_get_adapter, mock_parquet):
        """force_update=True 时跳过缓存检查"""
        db_mock = MagicMock()
        db_mock.has_data.return_value = True
        mock_parquet.return_value = db_mock

        adapter_mock = MagicMock()
        adapter_mock.get_etf_daily.return_value = _make_raw_df_chinese()
        mock_get_adapter.return_value = adapter_mock

        from jk2bt.data.market.etf import get_etf_daily

        result = get_etf_daily("510300", "2024-01-01", "2024-01-31", force_update=True)

        db_mock.has_data.assert_not_called()
        adapter_mock.get_etf_daily.assert_called_once()
        assert isinstance(result, pd.DataFrame)

    @patch("jk2bt.data.market.etf.ParquetAdapter")
    @patch("jk2bt.data.market.etf.get_adapter")
    def test_all_sources_fail_with_cache_fallback(self, mock_get_adapter, mock_parquet):
        """所有数据源失败后回退到本地缓存"""
        sample_df = _make_sample_df()

        db_mock = MagicMock()
        db_mock.has_data.return_value = False
        db_mock.get_etf_daily.side_effect = [pd.DataFrame(), sample_df]
        mock_parquet.return_value = db_mock

        adapter_mock = MagicMock()
        adapter_mock.get_etf_daily.return_value = pd.DataFrame()
        mock_get_adapter.return_value = adapter_mock

        from jk2bt.data.market.etf import get_etf_daily

        result = get_etf_daily("510300", "2024-01-01", "2024-01-31")

        assert isinstance(result, pd.DataFrame)
        assert not result.empty

    @patch("jk2bt.data.market.etf.ParquetAdapter")
    @patch("jk2bt.data.market.etf.get_adapter")
    def test_all_sources_fail_no_cache_raises(self, mock_get_adapter, mock_parquet):
        """所有数据源失败且无缓存时抛出 ValueError"""
        db_mock = MagicMock()
        db_mock.has_data.return_value = False
        db_mock.get_etf_daily.return_value = pd.DataFrame()
        mock_parquet.return_value = db_mock

        adapter_mock = MagicMock()
        adapter_mock.get_etf_daily.return_value = pd.DataFrame()
        mock_get_adapter.return_value = adapter_mock

        from jk2bt.data.market.etf import get_etf_daily

        with pytest.raises(ValueError, match="所有数据源获取失败"):
            get_etf_daily("510300", "2024-01-01", "2024-01-31")

    @patch("jk2bt.data.market.etf.ParquetAdapter")
    @patch("jk2bt.data.market.etf.get_adapter")
    def test_write_failure_does_not_affect_result(self, mock_get_adapter, mock_parquet):
        """写入数据库失败不应影响返回结果"""
        db_mock = MagicMock()
        db_mock.has_data.return_value = False
        db_mock.get_etf_daily.return_value = pd.DataFrame()
        db_mock.insert_etf_daily.side_effect = Exception("写入失败")
        mock_parquet.return_value = db_mock

        adapter_mock = MagicMock()
        adapter_mock.get_etf_daily.return_value = _make_raw_df_chinese()
        mock_get_adapter.return_value = adapter_mock

        from jk2bt.data.market.etf import get_etf_daily

        result = get_etf_daily("510300", "2024-01-01", "2024-01-31")

        assert isinstance(result, pd.DataFrame)
        assert not result.empty

    @patch("jk2bt.data.market.etf.ParquetAdapter")
    @patch("jk2bt.data.market.etf.get_adapter")
    def test_date_filtering(self, mock_get_adapter, mock_parquet):
        """返回数据应过滤到请求的日期范围"""
        dates = pd.date_range("2023-12-25", periods=15, freq="B")
        raw_df = pd.DataFrame(
            {
                "datetime": dates,
                "开盘": [10.0 + i for i in range(15)],
                "最高": [11.0 + i for i in range(15)],
                "最低": [9.0 + i for i in range(15)],
                "收盘": [10.5 + i for i in range(15)],
                "成交量": [1000 + i * 100 for i in range(15)],
                "成交额": [10000.0 + i * 1000 for i in range(15)],
            }
        )

        db_mock = MagicMock()
        db_mock.has_data.return_value = False
        db_mock.get_etf_daily.return_value = pd.DataFrame()
        mock_parquet.return_value = db_mock

        adapter_mock = MagicMock()
        adapter_mock.get_etf_daily.return_value = raw_df
        mock_get_adapter.return_value = adapter_mock

        from jk2bt.data.market.etf import get_etf_daily

        result = get_etf_daily("510300", "2024-01-01", "2024-01-10")

        assert isinstance(result, pd.DataFrame)
        assert result["datetime"].min() >= pd.to_datetime("2024-01-01")
        assert result["datetime"].max() <= pd.to_datetime("2024-01-10")

    @patch("jk2bt.data.market.etf.ParquetAdapter")
    @patch("jk2bt.data.market.etf.get_adapter")
    def test_empty_dataframe_from_source(self, mock_get_adapter, mock_parquet):
        """数据源返回空数据时应回退到缓存"""
        sample_df = _make_sample_df()

        db_mock = MagicMock()
        db_mock.has_data.return_value = False
        db_mock.get_etf_daily.side_effect = [pd.DataFrame(), sample_df]
        mock_parquet.return_value = db_mock

        adapter_mock = MagicMock()
        adapter_mock.get_etf_daily.return_value = pd.DataFrame()
        mock_get_adapter.return_value = adapter_mock

        from jk2bt.data.market.etf import get_etf_daily

        result = get_etf_daily("510300", "2024-01-01", "2024-01-31")

        assert isinstance(result, pd.DataFrame)

    @patch("jk2bt.data.market.etf.ParquetAdapter")
    @patch("jk2bt.data.market.etf.get_adapter")
    def test_output_columns_standardized(self, mock_get_adapter, mock_parquet):
        """输出列应标准化"""
        db_mock = MagicMock()
        db_mock.has_data.return_value = False
        db_mock.get_etf_daily.return_value = pd.DataFrame()
        mock_parquet.return_value = db_mock

        adapter_mock = MagicMock()
        adapter_mock.get_etf_daily.return_value = _make_raw_df_chinese()
        mock_get_adapter.return_value = adapter_mock

        from jk2bt.data.market.etf import get_etf_daily

        result = get_etf_daily("510300", "2024-01-01", "2024-01-31")

        expected_cols = ["datetime", "open", "high", "low", "close", "volume"]
        for col in expected_cols:
            assert col in result.columns
