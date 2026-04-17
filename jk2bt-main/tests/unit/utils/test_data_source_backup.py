"""
test_data_source_backup.py
数据源备份模块测试
"""

import pytest
import pandas as pd
from unittest.mock import patch, MagicMock
from jk2bt.data.sources.data_source_backup import (
    set_tushare_token,
    _get_tushare_token,
    DEFAULT_STOCK_DAILY_SOURCES,
    DEFAULT_ETF_DAILY_SOURCES,
    DEFAULT_INDEX_SOURCES,
    DEFAULT_MINUTE_SOURCES,
    _normalize_stock_daily,
    _normalize_sina_daily,
    _normalize_tushare_daily,
    _normalize_baostock_daily,
    _normalize_etf_daily,
    _normalize_minute_data,
    _normalize_futures_daily,
    _normalize_option_daily,
    get_stock_daily_with_fallback,
)


class TestTushareToken:
    """测试 Tushare Token 设置"""

    def test_set_and_get_token(self):
        """测试设置和获取 Token"""
        set_tushare_token("test_token_123")
        assert _get_tushare_token() == "test_token_123"

    def test_token_persistence(self):
        """测试 Token 持久化"""
        set_tushare_token("my_token")
        assert _get_tushare_token() == "my_token"


class TestDefaultSources:
    """测试默认数据源配置"""

    def test_stock_daily_sources(self):
        """测试股票日线默认源"""
        assert "sina" in DEFAULT_STOCK_DAILY_SOURCES
        assert "east_money" in DEFAULT_STOCK_DAILY_SOURCES
        assert "tushare" in DEFAULT_STOCK_DAILY_SOURCES
        assert "baostock" in DEFAULT_STOCK_DAILY_SOURCES

    def test_etf_daily_sources(self):
        """测试 ETF 日线默认源"""
        assert "sina" in DEFAULT_ETF_DAILY_SOURCES
        assert "east_money" in DEFAULT_ETF_DAILY_SOURCES

    def test_index_sources(self):
        """测试指数默认源"""
        assert "sina" in DEFAULT_INDEX_SOURCES
        assert "csindex" in DEFAULT_INDEX_SOURCES

    def test_minute_sources(self):
        """测试分钟数据默认源"""
        assert DEFAULT_MINUTE_SOURCES == ["east_money"]


class TestNormalizeStockDaily:
    """测试股票日线数据标准化"""

    def test_chinese_columns(self):
        """测试中文列名"""
        df = pd.DataFrame(
            {
                "日期": ["2023-01-01", "2023-01-02"],
                "开盘": [100.0, 101.0],
                "最高": [105.0, 106.0],
                "最低": [99.0, 100.0],
                "收盘": [103.0, 104.0],
                "成交量": [1000, 1100],
                "成交额": [103000, 114000],
            }
        )
        result = _normalize_stock_daily(df)
        assert "datetime" in result.columns
        assert "open" in result.columns

    def test_english_columns(self):
        """测试英文列名"""
        df = pd.DataFrame(
            {
                "date": ["2023-01-01", "2023-01-02"],
                "open": [100.0, 101.0],
                "high": [105.0, 106.0],
                "low": [99.0, 100.0],
                "close": [103.0, 104.0],
                "volume": [1000, 1100],
                "amount": [103000, 114000],
            }
        )
        result = _normalize_stock_daily(df)
        assert "datetime" in result.columns
        assert "open" in result.columns

    def test_empty_dataframe(self):
        """测试空 DataFrame"""
        result = _normalize_stock_daily(pd.DataFrame())
        assert result.empty

    def test_none_dataframe(self):
        """测试 None 输入"""
        result = _normalize_stock_daily(None)
        assert result.empty


class TestNormalizeSinaDaily:
    """测试新浪日线数据标准化"""

    def test_basic_normalization(self):
        """测试基本标准化"""
        df = pd.DataFrame(
            {
                "date": ["2023-01-01", "2023-01-02"],
                "open": [100.0, 101.0],
                "high": [105.0, 106.0],
                "low": [99.0, 100.0],
                "close": [103.0, 104.0],
                "volume": [1000, 1100],
                "amount": [103000, 114000],
            }
        )
        result = _normalize_sina_daily(df)
        assert "datetime" in result.columns
        assert result["datetime"].dtype == "datetime64[ns]"

    def test_empty_returns_empty(self):
        """测试空数据返回空 DataFrame"""
        result = _normalize_sina_daily(pd.DataFrame())
        assert result.empty


class TestNormalizeTushareDaily:
    """测试 Tushare 日线数据标准化"""

    def test_trade_date_column(self):
        """测试 trade_date 列处理"""
        df = pd.DataFrame(
            {
                "trade_date": ["20230101", "20230102"],
                "open": [100.0, 101.0],
                "high": [105.0, 106.0],
                "low": [99.0, 100.0],
                "close": [103.0, 104.0],
                "vol": [1000, 1100],
                "amount": [103000, 114000],
            }
        )
        result = _normalize_tushare_daily(df)
        assert "datetime" in result.columns


class TestNormalizeBaostockDaily:
    """测试 Baostock 日线数据标准化"""

    def test_numeric_conversion(self):
        """测试数值类型转换"""
        df = pd.DataFrame(
            {
                "date": ["2023-01-01", "2023-01-02"],
                "open": ["100.0", "101.0"],
                "high": ["105.0", "106.0"],
                "low": ["99.0", "100.0"],
                "close": ["103.0", "104.0"],
                "volume": ["1000", "1100"],
                "amount": ["103000", "114000"],
            }
        )
        result = _normalize_baostock_daily(df)
        assert pd.api.types.is_numeric_dtype(result["open"])


class TestNormalizeEtfDaily:
    """测试 ETF 日线数据标准化"""

    def test_etf_uses_stock_normalizer(self):
        """测试 ETF 使用股票标准化器"""
        df = pd.DataFrame(
            {
                "日期": ["2023-01-01"],
                "开盘": [100.0],
                "最高": [105.0],
                "最低": [99.0],
                "收盘": [103.0],
                "成交量": [1000],
            }
        )
        result = _normalize_etf_daily(df)
        assert "datetime" in result.columns


class TestNormalizeMinuteData:
    """测试分钟数据标准化"""

    def test_chinese_columns(self):
        """测试中文列名"""
        df = pd.DataFrame(
            {
                "时间": ["2023-01-01 09:30", "2023-01-01 09:31"],
                "开盘": [100.0, 101.0],
                "最高": [105.0, 106.0],
                "最低": [99.0, 100.0],
                "收盘": [103.0, 104.0],
                "成交量": [1000, 1100],
                "成交额": [103000, 114000],
            }
        )
        result = _normalize_minute_data(df)
        assert "datetime" in result.columns
        assert "money" in result.columns


class TestNormalizeFuturesDaily:
    """测试期货日线数据标准化"""

    def test_date_column(self):
        """测试日期列处理"""
        df = pd.DataFrame(
            {
                "date": ["2023-01-01", "2023-01-02"],
                "open": [100.0, 101.0],
                "high": [105.0, 106.0],
                "low": [99.0, 100.0],
                "close": [103.0, 104.0],
                "volume": [1000, 1100],
            }
        )
        result = _normalize_futures_daily(df)
        assert "datetime" in result.columns

    def test_chinese_date_column(self):
        """测试中文日期列"""
        df = pd.DataFrame(
            {
                "日期": ["2023-01-01", "2023-01-02"],
                "开盘": [100.0, 101.0],
                "收盘": [103.0, 104.0],
            }
        )
        result = _normalize_futures_daily(df)
        assert "datetime" in result.columns


class TestNormalizeOptionDaily:
    """测试期权日线数据标准化"""

    def test_option_uses_futures_normalizer(self):
        """测试期权使用期货标准化器"""
        df = pd.DataFrame(
            {
                "date": ["2023-01-01"],
                "open": [100.0],
                "close": [103.0],
            }
        )
        result = _normalize_option_daily(df)
        assert "datetime" in result.columns


class TestGetStockDailyWithFallback:
    """测试带备用源的数据获取"""

    @patch("jk2bt.utils.data_source_backup.fetch_stock_daily_sina")
    @patch("jk2bt.utils.data_source_backup.fetch_stock_daily_eastmoney")
    def test_sina_success(self, mock_eastmoney, mock_sina):
        """测试新浪成功时返回"""
        mock_sina.return_value = pd.DataFrame({"date": ["2023-01-01"], "close": [100]})
        mock_eastmoney.return_value = pd.DataFrame()

        result = get_stock_daily_with_fallback(
            symbol="sh600519",
            start="2023-01-01",
            end="2023-01-10",
        )

        assert len(result) == 1
        mock_sina.assert_called_once()
        mock_eastmoney.assert_not_called()

    @patch("jk2bt.utils.data_source_backup.fetch_stock_daily_sina")
    @patch("jk2bt.utils.data_source_backup.fetch_stock_daily_eastmoney")
    def test_sina_fails_eastmoney_success(self, mock_eastmoney, mock_sina):
        """测试新浪失败后东方财富成功"""
        mock_sina.return_value = pd.DataFrame()
        mock_eastmoney.return_value = pd.DataFrame(
            {"date": ["2023-01-01"], "close": [100]}
        )

        result = get_stock_daily_with_fallback(
            symbol="sh600519",
            start="2023-01-01",
            end="2023-01-10",
        )

        assert len(result) == 1
        mock_sina.assert_called_once()
        mock_eastmoney.assert_called_once()

    @patch("jk2bt.utils.data_source_backup.fetch_stock_daily_sina")
    def test_all_fail_returns_empty(self, mock_sina):
        """测试所有数据源失败返回空"""
        mock_sina.return_value = pd.DataFrame()

        result = get_stock_daily_with_fallback(
            symbol="sh600519",
            start="2023-01-01",
            end="2023-01-10",
            sources=["sina"],
        )

        assert result.empty

    @patch("jk2bt.utils.data_source_backup.fetch_stock_daily_sina")
    def test_custom_sources(self, mock_sina):
        """测试自定义数据源列表"""
        mock_sina.return_value = pd.DataFrame({"date": ["2023-01-01"], "close": [100]})

        result = get_stock_daily_with_fallback(
            symbol="sh600519",
            start="2023-01-01",
            end="2023-01-10",
            sources=["sina"],
        )

        mock_sina.assert_called_once()

    def test_fallback_to_cache(self):
        """测试回退到缓存"""
        mock_cache = MagicMock(
            return_value=pd.DataFrame({"date": ["2023-01-01"], "close": [100]})
        )

        with patch(
            "jk2bt.utils.data_source_backup.fetch_stock_daily_sina",
            return_value=pd.DataFrame(),
        ):
            result = get_stock_daily_with_fallback(
                symbol="sh600519",
                start="2023-01-01",
                end="2023-01-10",
                fallback_to_cache=True,
                cache_getter=mock_cache,
            )

        mock_cache.assert_called_once()
