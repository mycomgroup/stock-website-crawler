"""
tests/test_market_data_stock.py
单元测试 for jk2bt/data/market/stock.py

覆盖场景:
- get_stock_daily: 缓存命中、缓存未命中、离线模式、数据源失败回退、写入成功/失败
- get_stock_daily_fast: 缓存命中、从数据源获取、写入失败
- get_stock_daily_legacy: 缓存命中、离线模式、重试成功、重试失败回退缓存、重试失败无缓存
- 日期过滤逻辑
- 空数据/异常数据处理
"""

import pytest
import pandas as pd
from unittest.mock import patch, MagicMock, PropertyMock
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))


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
            "日期": dates,
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
    """每个测试前重置 DuckDB 单例缓存，避免状态泄漏"""
    from jk2bt.data.storage import parquet_adapter

    parquet_adapter._PROCESS_SINGLETONS.clear()
    yield
    parquet_adapter._PROCESS_SINGLETONS.clear()


# ============================================================================
# get_stock_daily 测试
# ============================================================================


class TestGetStockDaily:
    """测试 get_stock_daily 函数"""

    @patch("jk2bt.data.market.stock.get_writer_manager")
    @patch("jk2bt.data.market.stock.get_stock_daily_with_fallback")
    @patch("jk2bt.data.market.stock.get_shared_read_only_manager")
    def test_cache_hit_returns_cached_data(
        self, mock_get_read, mock_fallback, mock_get_write
    ):
        """缓存命中：直接返回缓存数据，不调用数据源"""
        sample_df = _make_sample_df()

        db_mock = MagicMock()
        db_mock.has_data.return_value = True
        db_mock.get_stock_daily.return_value = sample_df
        mock_get_read.return_value = db_mock

        from jk2bt.data.market.stock import get_stock_daily

        result = get_stock_daily("sh600000", "2024-01-01", "2024-01-31")

        db_mock.has_data.assert_called_once()
        db_mock.get_stock_daily.assert_called_once_with(
            "sh600000", "2024-01-01", "2024-01-31", "qfq"
        )
        mock_fallback.assert_not_called()
        mock_get_write.assert_not_called()
        assert isinstance(result, pd.DataFrame)
        assert not result.empty
        assert "openinterest" in result.columns

    @patch("jk2bt.data.market.stock.get_writer_manager")
    @patch("jk2bt.data.market.stock.get_stock_daily_with_fallback")
    @patch("jk2bt.data.market.stock.get_shared_read_only_manager")
    def test_cache_hit_force_update_bypasses_cache(
        self, mock_get_read, mock_fallback, mock_get_write
    ):
        """force_update=True 时跳过缓存检查"""
        sample_df = _make_sample_df()
        raw_df = _make_raw_df_chinese()

        db_mock = MagicMock()
        db_mock.has_data.return_value = True  # 即使有缓存也应该被忽略
        mock_get_read.return_value = db_mock

        mock_fallback.return_value = raw_df

        write_mock = MagicMock()
        mock_get_write.return_value = write_mock

        from jk2bt.data.market.stock import get_stock_daily

        result = get_stock_daily(
            "sh600000", "2024-01-01", "2024-01-31", force_update=True
        )

        # force_update=True 时 has_data 不应被调用
        db_mock.has_data.assert_not_called()
        mock_fallback.assert_called_once()
        assert isinstance(result, pd.DataFrame)

    @patch("jk2bt.data.market.stock.get_writer_manager")
    @patch("jk2bt.data.market.stock.get_stock_daily_with_fallback")
    @patch("jk2bt.data.market.stock.get_shared_read_only_manager")
    def test_cache_miss_fetches_from_source(
        self, mock_get_read, mock_fallback, mock_get_write
    ):
        """缓存未命中：从数据源获取并写入数据库"""
        sample_df = _make_sample_df()
        raw_df = _make_raw_df_chinese()

        db_mock = MagicMock()
        db_mock.has_data.return_value = False
        db_mock.get_stock_daily.return_value = pd.DataFrame()
        mock_get_read.return_value = db_mock

        mock_fallback.return_value = raw_df

        write_mock = MagicMock()
        mock_get_write.return_value = write_mock

        from jk2bt.data.market.stock import get_stock_daily

        result = get_stock_daily("sh600000", "2024-01-01", "2024-01-31")

        mock_fallback.assert_called_once()
        write_mock.insert_stock_daily.assert_called_once()
        assert isinstance(result, pd.DataFrame)
        assert not result.empty

    @patch("jk2bt.data.market.stock.get_writer_manager")
    @patch("jk2bt.data.market.stock.get_stock_daily_with_fallback")
    @patch("jk2bt.data.market.stock.get_shared_read_only_manager")
    def test_offline_mode_with_cache(
        self, mock_get_read, mock_fallback, mock_get_write
    ):
        """离线模式：有缓存时返回缓存数据"""
        sample_df = _make_sample_df()

        db_mock = MagicMock()
        db_mock.has_data.return_value = False
        db_mock.get_stock_daily.return_value = sample_df
        mock_get_read.return_value = db_mock

        from jk2bt.data.market.stock import get_stock_daily

        result = get_stock_daily(
            "sh600000", "2024-01-01", "2024-01-31", offline_mode=True
        )

        mock_fallback.assert_not_called()
        assert isinstance(result, pd.DataFrame)
        assert not result.empty

    @patch("jk2bt.data.market.stock.get_stock_daily_with_fallback")
    @patch("jk2bt.data.market.stock.get_shared_read_only_manager")
    def test_offline_mode_no_cache_raises(self, mock_get_read, mock_fallback):
        """离线模式：无缓存时抛出 ValueError"""
        db_mock = MagicMock()
        db_mock.has_data.return_value = False
        db_mock.get_stock_daily.return_value = pd.DataFrame()
        mock_get_read.return_value = db_mock

        from jk2bt.data.market.stock import get_stock_daily

        with pytest.raises(ValueError, match="离线模式下无缓存数据"):
            get_stock_daily("sh600000", "2024-01-01", "2024-01-31", offline_mode=True)

    @patch("jk2bt.data.market.stock.get_writer_manager")
    @patch("jk2bt.data.market.stock.get_stock_daily_with_fallback")
    @patch("jk2bt.data.market.stock.get_shared_read_only_manager")
    def test_all_sources_fail_fallback_to_cache(
        self, mock_get_read, mock_fallback, mock_get_write
    ):
        """所有数据源失败后回退到本地缓存"""
        sample_df = _make_sample_df()

        db_mock = MagicMock()
        db_mock.has_data.return_value = False
        db_mock.get_stock_daily.return_value = sample_df
        mock_get_read.return_value = db_mock

        mock_fallback.return_value = pd.DataFrame()  # 数据源返回空

        from jk2bt.data.market.stock import get_stock_daily

        result = get_stock_daily("sh600000", "2024-01-01", "2024-01-31")

        mock_fallback.assert_called_once()
        assert isinstance(result, pd.DataFrame)
        assert not result.empty

    @patch("jk2bt.data.market.stock.get_writer_manager")
    @patch("jk2bt.data.market.stock.get_stock_daily_with_fallback")
    @patch("jk2bt.data.market.stock.get_shared_read_only_manager")
    def test_all_sources_fail_no_cache_raises(
        self, mock_get_read, mock_fallback, mock_get_write
    ):
        """所有数据源失败且无缓存时抛出 ValueError"""
        db_mock = MagicMock()
        db_mock.has_data.return_value = False
        db_mock.get_stock_daily.return_value = pd.DataFrame()
        mock_get_read.return_value = db_mock

        mock_fallback.return_value = None  # 数据源返回 None

        from jk2bt.data.market.stock import get_stock_daily

        with pytest.raises(ValueError, match="所有数据源获取失败"):
            get_stock_daily("sh600000", "2024-01-01", "2024-01-31")

    @patch("jk2bt.data.market.stock.get_writer_manager")
    @patch("jk2bt.data.market.stock.get_stock_daily_with_fallback")
    @patch("jk2bt.data.market.stock.get_shared_read_only_manager")
    def test_write_failure_does_not_affect_result(
        self, mock_get_read, mock_fallback, mock_get_write
    ):
        """写入数据库失败不应影响返回结果"""
        raw_df = _make_raw_df_chinese()

        db_mock = MagicMock()
        db_mock.has_data.return_value = False
        mock_get_read.return_value = db_mock

        mock_fallback.return_value = raw_df

        write_mock = MagicMock()
        write_mock.insert_stock_daily.side_effect = Exception("写入失败")
        mock_get_write.return_value = write_mock

        from jk2bt.data.market.stock import get_stock_daily

        result = get_stock_daily("sh600000", "2024-01-01", "2024-01-31")

        write_mock.insert_stock_daily.assert_called_once()
        assert isinstance(result, pd.DataFrame)
        assert not result.empty

    @patch("jk2bt.data.market.stock.get_writer_manager")
    @patch("jk2bt.data.market.stock.get_stock_daily_with_fallback")
    @patch("jk2bt.data.market.stock.get_shared_read_only_manager")
    def test_date_filtering(self, mock_get_read, mock_fallback, mock_get_write):
        """返回数据应过滤到请求的日期范围"""
        # 数据源返回更宽范围的数据（使用英文列名，因为 fallback 返回的数据已经标准化）
        dates = pd.date_range("2023-12-25", periods=15, freq="B")
        raw_df = pd.DataFrame(
            {
                "datetime": dates,
                "open": [10.0 + i for i in range(15)],
                "high": [11.0 + i for i in range(15)],
                "low": [9.0 + i for i in range(15)],
                "close": [10.5 + i for i in range(15)],
                "volume": [1000 + i * 100 for i in range(15)],
                "amount": [10000.0 + i * 1000 for i in range(15)],
            }
        )

        db_mock = MagicMock()
        db_mock.has_data.return_value = False
        mock_get_read.return_value = db_mock

        mock_fallback.return_value = raw_df

        write_mock = MagicMock()
        mock_get_write.return_value = write_mock

        from jk2bt.data.market.stock import get_stock_daily

        result = get_stock_daily("sh600000", "2024-01-01", "2024-01-10")

        assert isinstance(result, pd.DataFrame)
        # 验证日期过滤
        assert result["datetime"].min() >= pd.to_datetime("2024-01-01")
        assert result["datetime"].max() <= pd.to_datetime("2024-01-10")

    @patch("jk2bt.data.market.stock.get_writer_manager")
    @patch("jk2bt.data.market.stock.get_stock_daily_with_fallback")
    @patch("jk2bt.data.market.stock.get_shared_read_only_manager")
    def test_custom_data_sources(self, mock_get_read, mock_fallback, mock_get_write):
        """自定义数据源列表应传递给 fallback 函数"""
        raw_df = _make_raw_df_chinese()

        db_mock = MagicMock()
        db_mock.has_data.return_value = False
        mock_get_read.return_value = db_mock

        mock_fallback.return_value = raw_df
        write_mock = MagicMock()
        mock_get_write.return_value = write_mock

        from jk2bt.data.market.stock import get_stock_daily

        custom_sources = ["east_money", "tushare"]
        get_stock_daily(
            "sh600000",
            "2024-01-01",
            "2024-01-31",
            data_sources=custom_sources,
        )

        call_kwargs = mock_fallback.call_args
        assert call_kwargs.kwargs["sources"] == custom_sources

    @patch("jk2bt.data.market.stock.get_writer_manager")
    @patch("jk2bt.data.market.stock.get_stock_daily_with_fallback")
    @patch("jk2bt.data.market.stock.get_shared_read_only_manager")
    def test_cache_getter_handles_exception(
        self, mock_get_read, mock_fallback, mock_get_write
    ):
        """cache_getter 内部异常应被捕获并返回空 DataFrame"""
        raw_df = _make_raw_df_chinese()

        db_mock = MagicMock()
        db_mock.has_data.return_value = False
        # 让 get_stock_daily 在 fallback 内部调用时抛异常
        db_mock.get_stock_daily.side_effect = Exception("DB error")
        mock_get_read.return_value = db_mock

        mock_fallback.return_value = raw_df
        write_mock = MagicMock()
        mock_get_write.return_value = write_mock

        from jk2bt.data.market.stock import get_stock_daily

        result = get_stock_daily("sh600000", "2024-01-01", "2024-01-31")

        assert isinstance(result, pd.DataFrame)
        assert not result.empty


# ============================================================================
# get_stock_daily_fast 测试
# ============================================================================


class TestGetStockDailyFast:
    """测试 get_stock_daily_fast 函数"""

    @patch("jk2bt.data.market.stock.get_writer_manager")
    @patch("jk2bt.data.market.stock.fetch_stock_daily_eastmoney")
    @patch("jk2bt.data.market.stock.get_shared_read_only_manager")
    def test_cache_hit(self, mock_get_read, mock_fetch, mock_get_write):
        """缓存命中：直接返回缓存"""
        sample_df = _make_sample_df()

        db_mock = MagicMock()
        db_mock.has_data.return_value = True
        db_mock.get_stock_daily.return_value = sample_df
        mock_get_read.return_value = db_mock

        from jk2bt.data.market.stock import get_stock_daily_fast

        result = get_stock_daily_fast("sh600000", "2024-01-01", "2024-01-31")

        db_mock.has_data.assert_called_once()
        mock_fetch.assert_not_called()
        mock_get_write.assert_not_called()
        assert isinstance(result, pd.DataFrame)
        assert not result.empty

    @patch("jk2bt.data.market.stock.get_writer_manager")
    @patch("jk2bt.data.market.stock.fetch_stock_daily_eastmoney")
    @patch("jk2bt.data.market.stock.get_shared_read_only_manager")
    def test_cache_miss_fetches_eastmoney(
        self, mock_get_read, mock_fetch, mock_get_write
    ):
        """缓存未命中：从东方财富获取"""
        raw_df = _make_raw_df_chinese()

        db_mock = MagicMock()
        db_mock.has_data.return_value = False
        mock_get_read.return_value = db_mock

        mock_fetch.return_value = raw_df

        write_mock = MagicMock()
        mock_get_write.return_value = write_mock

        from jk2bt.data.market.stock import get_stock_daily_fast

        result = get_stock_daily_fast("sh600000", "2024-01-01", "2024-01-31")

        mock_fetch.assert_called_once_with(
            "sh600000", "2024-01-01", "2024-01-31", "qfq"
        )
        write_mock.insert_stock_daily.assert_called_once()
        assert isinstance(result, pd.DataFrame)
        assert not result.empty

    @patch("jk2bt.data.market.stock.get_writer_manager")
    @patch("jk2bt.data.market.stock.fetch_stock_daily_eastmoney")
    @patch("jk2bt.data.market.stock.get_shared_read_only_manager")
    def test_fetch_failure_raises(self, mock_get_read, mock_fetch, mock_get_write):
        """获取失败时抛出 ValueError"""
        db_mock = MagicMock()
        db_mock.has_data.return_value = False
        mock_get_read.return_value = db_mock

        mock_fetch.return_value = pd.DataFrame()

        from jk2bt.data.market.stock import get_stock_daily_fast

        with pytest.raises(ValueError, match="快速获取失败"):
            get_stock_daily_fast("sh600000", "2024-01-01", "2024-01-31")

    @patch("jk2bt.data.market.stock.get_writer_manager")
    @patch("jk2bt.data.market.stock.fetch_stock_daily_eastmoney")
    @patch("jk2bt.data.market.stock.get_shared_read_only_manager")
    def test_write_failure_silent(self, mock_get_read, mock_fetch, mock_get_write):
        """写入失败应静默处理"""
        raw_df = _make_raw_df_chinese()

        db_mock = MagicMock()
        db_mock.has_data.return_value = False
        mock_get_read.return_value = db_mock

        mock_fetch.return_value = raw_df

        write_mock = MagicMock()
        write_mock.insert_stock_daily.side_effect = Exception("write error")
        mock_get_write.return_value = write_mock

        from jk2bt.data.market.stock import get_stock_daily_fast

        result = get_stock_daily_fast("sh600000", "2024-01-01", "2024-01-31")

        assert isinstance(result, pd.DataFrame)
        assert not result.empty


# ============================================================================
# get_stock_daily_legacy 测试
# ============================================================================


class TestGetStockDailyLegacy:
    """测试 get_stock_daily_legacy 函数"""

    @patch("jk2bt.data.market.stock.get_writer_manager")
    @patch("jk2bt.data.sources.get_adapter")
    @patch("jk2bt.data.market.stock.get_shared_read_only_manager")
    def test_cache_hit(self, mock_get_read, mock_get_adapter, mock_get_write):
        """缓存命中：直接返回缓存数据"""
        sample_df = _make_sample_df()

        db_mock = MagicMock()
        db_mock.has_data.return_value = True
        db_mock.get_stock_daily.return_value = sample_df
        mock_get_read.return_value = db_mock

        from jk2bt.data.market.stock import get_stock_daily_legacy

        result = get_stock_daily_legacy("sh600000", "2024-01-01", "2024-01-31")

        db_mock.has_data.assert_called_once()
        mock_get_write.assert_not_called()
        assert isinstance(result, pd.DataFrame)
        assert not result.empty

    @patch("jk2bt.data.market.stock.get_writer_manager")
    @patch("jk2bt.data.sources.get_adapter")
    @patch("jk2bt.data.market.stock.get_shared_read_only_manager")
    def test_offline_mode_with_cache(
        self, mock_get_read, mock_get_adapter, mock_get_write
    ):
        """离线模式有缓存：返回缓存"""
        sample_df = _make_sample_df()

        db_mock = MagicMock()
        db_mock.has_data.return_value = False
        db_mock.get_stock_daily.return_value = sample_df
        mock_get_read.return_value = db_mock

        from jk2bt.data.market.stock import get_stock_daily_legacy

        result = get_stock_daily_legacy(
            "sh600000", "2024-01-01", "2024-01-31", offline_mode=True
        )

        assert isinstance(result, pd.DataFrame)

    @patch("jk2bt.data.market.stock.get_writer_manager")
    @patch("jk2bt.data.sources.get_adapter")
    @patch("jk2bt.data.market.stock.get_shared_read_only_manager")
    def test_offline_mode_no_cache_raises(
        self, mock_get_read, mock_get_adapter, mock_get_write
    ):
        """离线模式无缓存：抛出 ValueError"""
        db_mock = MagicMock()
        db_mock.has_data.return_value = False
        db_mock.get_stock_daily.return_value = pd.DataFrame()
        mock_get_read.return_value = db_mock

        from jk2bt.data.market.stock import get_stock_daily_legacy

        with pytest.raises(ValueError, match="离线模式下无缓存数据"):
            get_stock_daily_legacy(
                "sh600000", "2024-01-01", "2024-01-31", offline_mode=True
            )

    @patch("jk2bt.data.market.stock.get_writer_manager")
    @patch("jk2bt.data.sources.get_adapter")
    @patch("jk2bt.data.market.stock.get_shared_read_only_manager")
    def test_first_attempt_success(
        self, mock_get_read, mock_get_adapter, mock_get_write
    ):
        """第一次尝试就成功获取数据"""
        raw_df = _make_raw_df_chinese()

        db_mock = MagicMock()
        db_mock.has_data.return_value = False
        mock_get_read.return_value = db_mock

        adapter_mock = MagicMock()
        adapter_mock.get_stock_hist.return_value = raw_df
        mock_get_adapter.return_value = adapter_mock

        write_mock = MagicMock()
        mock_get_write.return_value = write_mock

        from jk2bt.data.market.stock import get_stock_daily_legacy

        result = get_stock_daily_legacy(
            "sh600000", "2024-01-01", "2024-01-31", max_retries=3, retry_delay=0
        )

        adapter_mock.get_stock_hist.assert_called_once()
        write_mock.insert_stock_daily.assert_called_once()
        assert isinstance(result, pd.DataFrame)
        assert not result.empty

    @patch("jk2bt.data.market.stock.get_writer_manager")
    @patch("jk2bt.data.sources.get_adapter")
    @patch("jk2bt.data.market.stock.get_shared_read_only_manager")
    def test_retry_success_on_second_attempt(
        self, mock_get_read, mock_get_adapter, mock_get_write
    ):
        """第二次重试成功"""
        raw_df = _make_raw_df_chinese()

        db_mock = MagicMock()
        db_mock.has_data.return_value = False
        mock_get_read.return_value = db_mock

        adapter_mock = MagicMock()
        # 第一次失败，第二次成功
        adapter_mock.get_stock_hist.side_effect = [
            pd.DataFrame(),  # 第一次返回空
            raw_df,  # 第二次返回数据
        ]
        mock_get_adapter.return_value = adapter_mock

        write_mock = MagicMock()
        mock_get_write.return_value = write_mock

        from jk2bt.data.market.stock import get_stock_daily_legacy

        result = get_stock_daily_legacy(
            "sh600000", "2024-01-01", "2024-01-31", max_retries=3, retry_delay=0
        )

        assert adapter_mock.get_stock_hist.call_count == 2
        assert isinstance(result, pd.DataFrame)

    @patch("jk2bt.data.sources.get_adapter")
    @patch("jk2bt.data.market.stock.get_shared_read_only_manager")
    def test_all_retries_fail_with_cache_fallback(
        self, mock_get_read, mock_get_adapter
    ):
        """所有重试失败，但有缓存可回退"""
        sample_df = _make_sample_df()

        db_mock = MagicMock()
        db_mock.has_data.return_value = False
        # 重试期间和最终回退都返回缓存
        db_mock.get_stock_daily.return_value = sample_df
        mock_get_read.return_value = db_mock

        adapter_mock = MagicMock()
        adapter_mock.get_stock_hist.side_effect = Exception("network error")
        mock_get_adapter.return_value = adapter_mock

        from jk2bt.data.market.stock import get_stock_daily_legacy

        # max_retries=2: 第一次失败后检查缓存发现有数据，直接返回（不会重试第二次）
        result = get_stock_daily_legacy(
            "sh600000", "2024-01-01", "2024-01-31", max_retries=2, retry_delay=0
        )

        # 第一次失败后回退到缓存，只调用了一次
        assert adapter_mock.get_stock_hist.call_count == 1
        assert isinstance(result, pd.DataFrame)
        assert not result.empty

    @patch("jk2bt.data.sources.get_adapter")
    @patch("jk2bt.data.market.stock.get_shared_read_only_manager")
    def test_all_retries_fail_no_cache_raises(self, mock_get_read, mock_get_adapter):
        """所有重试失败且无缓存：抛出 ValueError"""
        db_mock = MagicMock()
        db_mock.has_data.return_value = False
        db_mock.get_stock_daily.return_value = pd.DataFrame()
        mock_get_read.return_value = db_mock

        adapter_mock = MagicMock()
        adapter_mock.get_stock_hist.side_effect = Exception("network error")
        mock_get_adapter.return_value = adapter_mock

        from jk2bt.data.market.stock import get_stock_daily_legacy

        with pytest.raises(ValueError, match="数据获取失败"):
            get_stock_daily_legacy(
                "sh600000", "2024-01-01", "2024-01-31", max_retries=2, retry_delay=0
            )

    @patch("jk2bt.data.market.stock.get_writer_manager")
    @patch("jk2bt.data.sources.get_adapter")
    @patch("jk2bt.data.market.stock.get_shared_read_only_manager")
    def test_date_filtering_legacy(
        self, mock_get_read, mock_get_adapter, mock_get_write
    ):
        """legacy 函数也应正确过滤日期"""
        # legacy 函数内部做了列名映射，所以用中文列名
        dates = pd.date_range("2023-12-25", periods=15, freq="B")
        raw_df = pd.DataFrame(
            {
                "日期": dates,
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
        mock_get_read.return_value = db_mock

        adapter_mock = MagicMock()
        adapter_mock.get_stock_hist.return_value = raw_df
        mock_get_adapter.return_value = adapter_mock

        write_mock = MagicMock()
        mock_get_write.return_value = write_mock

        from jk2bt.data.market.stock import get_stock_daily_legacy

        result = get_stock_daily_legacy(
            "sh600000", "2024-01-01", "2024-01-10", max_retries=1, retry_delay=0
        )

        assert result["datetime"].min() >= pd.to_datetime("2024-01-01")
        assert result["datetime"].max() <= pd.to_datetime("2024-01-10")

    @patch("jk2bt.data.market.stock.get_writer_manager")
    @patch("jk2bt.data.sources.get_adapter")
    @patch("jk2bt.data.market.stock.get_shared_read_only_manager")
    def test_retry_with_cache_fallback_during_retry(
        self, mock_get_read, mock_get_adapter, mock_get_write
    ):
        """重试期间检查缓存，有缓存则提前返回"""
        sample_df = _make_sample_df()

        db_mock = MagicMock()
        db_mock.has_data.return_value = False
        # 重试期间返回缓存数据
        db_mock.get_stock_daily.return_value = sample_df
        mock_get_read.return_value = db_mock

        adapter_mock = MagicMock()
        adapter_mock.get_stock_hist.side_effect = Exception("network error")
        mock_get_adapter.return_value = adapter_mock

        from jk2bt.data.market.stock import get_stock_daily_legacy

        result = get_stock_daily_legacy(
            "sh600000", "2024-01-01", "2024-01-31", max_retries=3, retry_delay=0
        )

        # 第一次失败后，重试时检查缓存并返回
        assert isinstance(result, pd.DataFrame)
        assert not result.empty

    @patch("jk2bt.data.market.stock.get_writer_manager")
    @patch("jk2bt.data.sources.get_adapter")
    @patch("jk2bt.data.market.stock.get_shared_read_only_manager")
    def test_empty_raw_data_raises(
        self, mock_get_read, mock_get_adapter, mock_get_write
    ):
        """adapter 返回 None 时应抛出 ValueError"""
        db_mock = MagicMock()
        db_mock.has_data.return_value = False
        mock_get_read.return_value = db_mock

        adapter_mock = MagicMock()
        adapter_mock.get_stock_hist.return_value = None
        mock_get_adapter.return_value = adapter_mock

        from jk2bt.data.market.stock import get_stock_daily_legacy

        with pytest.raises(ValueError, match="akshare 返回空数据"):
            get_stock_daily_legacy(
                "sh600000", "2024-01-01", "2024-01-31", max_retries=1, retry_delay=0
            )


# ============================================================================
# 边界情况测试
# ============================================================================


class TestEdgeCases:
    """边界情况和异常数据处理"""

    @patch("jk2bt.data.market.stock.get_writer_manager")
    @patch("jk2bt.data.market.stock.get_adapter")
    @patch("jk2bt.data.market.stock.get_shared_read_only_manager")
    def test_empty_dataframe_from_cache_hit(
        self, mock_get_read, mock_get_adapter, mock_get_write
    ):
        """缓存命中但返回空 DataFrame 时应继续获取数据"""
        db_mock = MagicMock()
        db_mock.has_data.return_value = True
        db_mock.get_stock_daily.return_value = pd.DataFrame()  # 空数据
        mock_get_read.return_value = db_mock

        raw_df = _make_raw_df_chinese()
        adapter_mock = MagicMock()
        adapter_mock.get_daily_data.return_value = raw_df
        mock_get_adapter.return_value = adapter_mock

        write_mock = MagicMock()
        mock_get_write.return_value = write_mock

        from jk2bt.data.market.stock import get_stock_daily

        result = get_stock_daily("sh600000", "2024-01-01", "2024-01-31")

        assert isinstance(result, pd.DataFrame)
        assert not result.empty

    @patch("jk2bt.data.market.stock.get_writer_manager")
    @patch("jk2bt.data.market.stock.get_adapter")
    @patch("jk2bt.data.market.stock.get_shared_read_only_manager")
    def test_none_from_fallback_with_empty_cache(
        self, mock_get_read, mock_get_adapter, mock_get_write
    ):
        """adapter 返回 None 且缓存为空时抛出 ValueError"""
        db_mock = MagicMock()
        db_mock.has_data.return_value = False
        db_mock.get_stock_daily.return_value = pd.DataFrame()
        mock_get_read.return_value = db_mock

        adapter_mock = MagicMock()
        adapter_mock.get_daily_data.return_value = None
        mock_get_adapter.return_value = adapter_mock

        from jk2bt.data.market.stock import get_stock_daily

        with pytest.raises(ValueError):
            get_stock_daily("sh600000", "2024-01-01", "2024-01-31")

    @patch("jk2bt.data.market.stock.get_writer_manager")
    @patch("jk2bt.data.market.stock.get_adapter")
    @patch("jk2bt.data.market.stock.get_shared_read_only_manager")
    def test_fast_none_from_fetch(
        self, mock_get_read, mock_get_adapter, mock_get_write
    ):
        """fast 函数 adapter 返回 None 时应抛出"""
        db_mock = MagicMock()
        db_mock.has_data.return_value = False
        mock_get_read.return_value = db_mock

        adapter_mock = MagicMock()
        adapter_mock.get_daily_data.return_value = None
        mock_get_adapter.return_value = adapter_mock

        from jk2bt.data.market.stock import get_stock_daily_fast

        with pytest.raises(ValueError, match="所有数据源获取失败"):
            get_stock_daily_fast("sh600000", "2024-01-01", "2024-01-31")

    @patch("jk2bt.data.market.stock.get_writer_manager")
    @patch("jk2bt.data.market.stock.get_adapter")
    @patch("jk2bt.data.market.stock.get_shared_read_only_manager")
    def test_output_has_openinterest_column(
        self, mock_get_read, mock_get_adapter, mock_get_write
    ):
        """输出应包含 openinterest 列（standardize_ohlcv 添加）"""
        raw_df = _make_raw_df_chinese()

        db_mock = MagicMock()
        db_mock.has_data.return_value = False
        mock_get_read.return_value = db_mock

        adapter_mock = MagicMock()
        adapter_mock.get_daily_data.return_value = raw_df
        mock_get_adapter.return_value = adapter_mock

        write_mock = MagicMock()
        mock_get_write.return_value = write_mock

        from jk2bt.data.market.stock import get_stock_daily

        result = get_stock_daily("sh600000", "2024-01-01", "2024-01-31")

        assert "openinterest" in result.columns
        assert (result["openinterest"] == 0.0).all()

    @patch("jk2bt.data.market.stock.get_writer_manager")
    @patch("jk2bt.data.market.stock.get_adapter")
    @patch("jk2bt.data.market.stock.get_shared_read_only_manager")
    def test_output_columns_standardized(
        self, mock_get_read, mock_get_adapter, mock_get_write
    ):
        """输出列应标准化"""
        raw_df = _make_raw_df_chinese()

        db_mock = MagicMock()
        db_mock.has_data.return_value = False
        mock_get_read.return_value = db_mock

        adapter_mock = MagicMock()
        adapter_mock.get_daily_data.return_value = raw_df
        mock_get_adapter.return_value = adapter_mock

        write_mock = MagicMock()
        mock_get_write.return_value = write_mock

        from jk2bt.data.market.stock import get_stock_daily

        result = get_stock_daily("sh600000", "2024-01-01", "2024-01-31")

        expected_cols = [
            "datetime",
            "open",
            "high",
            "low",
            "close",
            "volume",
            "amount",
            "openinterest",
        ]
        for col in expected_cols:
            assert col in result.columns
