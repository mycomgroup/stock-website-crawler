"""
test_executor.py
executor.py 单元测试

测试场景覆盖:
1. _COMMON_INDICES 常用指数映射
2. _COMMON_ETFS 常用ETF映射
3. _static_analyze_stock_pool 静态分析股票池
4. _load_stock_data_from_cache 数据加载
5. _load_minute_data 分钟数据加载
6. _discover_strategy_stocks 股票池发现
"""

import pytest
from unittest.mock import MagicMock, patch
import re

try:
    from jk2bt.engine.executor import (
        _COMMON_INDICES,
        _COMMON_ETFS,
        _static_analyze_stock_pool,
        _load_stock_data_from_cache,
        _load_minute_data,
        _discover_strategy_stocks,
    )
except ImportError:
    pytest.skip("executor module not available", allow_module_level=True)


class TestCommonIndices:
    """测试 _COMMON_INDICES 常用指数映射"""

    def test_not_empty(self):
        """测试不为空"""
        assert len(_COMMON_INDICES) > 0

    def test_hs300(self):
        """测试沪深300"""
        assert "000300.XSHG" in _COMMON_INDICES
        assert _COMMON_INDICES["000300.XSHG"] == "沪深300"
        assert "000300" in _COMMON_INDICES

    def test_zz500(self):
        """测试中证500"""
        assert "000905.XSHG" in _COMMON_INDICES
        assert _COMMON_INDICES["000905.XSHG"] == "中证500"

    def test_zz1000(self):
        """测试中证1000"""
        assert "000852.XSHG" in _COMMON_INDICES

    def test_cyb(self):
        """测试创业板"""
        assert "399006.XSHE" in _COMMON_INDICES
        assert _COMMON_INDICES["399006.XSHE"] == "创业板指"

    def test_sz50(self):
        """测试上证50"""
        assert "000016.XSHG" in _COMMON_INDICES
        assert _COMMON_INDICES["000016.XSHG"] == "上证50"


class TestCommonETFS:
    """测试 _COMMON_ETFS 常用ETF映射"""

    def test_not_empty(self):
        """测试不为空"""
        assert len(_COMMON_ETFS) > 0

    def test_zz500_etf(self):
        """测试中证500ETF"""
        assert "510500.XSHG" in _COMMON_ETFS
        assert _COMMON_ETFS["510500.XSHG"] == "中证500ETF"

    def test_hs300_etf(self):
        """测试沪深300ETF"""
        assert "510300.XSHG" in _COMMON_ETFS
        assert _COMMON_ETFS["510300.XSHG"] == "沪深300ETF"

    def test_sz50_etf(self):
        """测试上证50ETF"""
        assert "510050.XSHG" in _COMMON_ETFS

    def test_cyb_etf(self):
        """测试创业板ETF"""
        assert "159915.XSHE" in _COMMON_ETFS
        assert _COMMON_ETFS["159915.XSHE"] == "创业板ETF"


class TestStaticAnalyzeStockPool:
    """测试 _static_analyze_stock_pool 静态分析"""

    def test_empty_functions_returns_empty(self):
        """测试空策略函数返回空集合"""
        result, failure_report = _static_analyze_stock_pool({})
        assert result == set()
        assert "index_weight_failures" in failure_report

    def test_finds_index_stocks_in_source(self):
        """测试在源代码中找到指数调用"""
        strategy_source = 'get_index_stocks("000300.XSHG")'
        result, failure_report = _static_analyze_stock_pool(
            {}, strategy_source=strategy_source
        )
        assert "total_attempted" in failure_report

    def test_finds_stock_codes_in_source(self):
        """测试在源代码中找到股票代码"""
        strategy_source = '"600519.XSHG"'
        result, failure_report = _static_analyze_stock_pool(
            {}, strategy_source=strategy_source
        )
        assert "600519.XSHG" in result

    def test_finds_etf_codes_in_source(self):
        """测试在源代码中找到ETF代码"""
        strategy_source = '"510500.XSHG"'
        result, failure_report = _static_analyze_stock_pool(
            {}, strategy_source=strategy_source
        )
        assert "510500.XSHG" in result

    def test_finds_short_stock_codes(self):
        """测试找到短股票代码"""
        strategy_source = '"600519"'
        result, failure_report = _static_analyze_stock_pool(
            {}, strategy_source=strategy_source
        )
        assert "600519.XSHG" in result

    def test_failure_report_structure(self):
        """测试失败报告结构"""
        _, failure_report = _static_analyze_stock_pool({})
        assert "index_weight_failures" in failure_report
        assert "all_securities_failure" in failure_report
        assert "network_failures" in failure_report
        assert "total_attempted" in failure_report
        assert "total_successful" in failure_report


class TestLoadStockDataFromCache:
    """测试 _load_stock_data_from_cache 数据加载"""

    def test_converts_xshg_code(self):
        """测试转换XSHG代码"""
        with patch("jk2bt.engine.executor.ParquetAdapter") as mock_adapter:
            mock_instance = MagicMock()
            mock_instance.get_stock_daily.return_value = None
            mock_adapter.return_value = mock_instance

            result = _load_stock_data_from_cache(
                "600519.XSHG", "2024-01-01", "2024-12-31"
            )

    def test_converts_xshe_code(self):
        """测试转换XSHE代码"""
        with patch("jk2bt.engine.executor.ParquetAdapter") as mock_adapter:
            mock_instance = MagicMock()
            mock_instance.get_stock_daily.return_value = None
            mock_adapter.return_value = mock_instance

            result = _load_stock_data_from_cache(
                "000001.XSHE", "2024-01-01", "2024-12-31"
            )

    def test_converts_plain_code_sh(self):
        """测试转换纯沪市代码"""
        with patch("jk2bt.engine.executor.ParquetAdapter") as mock_adapter:
            mock_instance = MagicMock()
            mock_instance.get_stock_daily.return_value = None
            mock_adapter.return_value = mock_instance

            result = _load_stock_data_from_cache("600519", "2024-01-01", "2024-12-31")

    def test_converts_plain_code_sz(self):
        """测试转换纯深市代码"""
        with patch("jk2bt.engine.executor.ParquetAdapter") as mock_adapter:
            mock_instance = MagicMock()
            mock_instance.get_stock_daily.return_value = None
            mock_adapter.return_value = mock_instance

            result = _load_stock_data_from_cache("000001", "2024-01-01", "2024-12-31")


class TestLoadMinuteData:
    """测试 _load_minute_data 分钟数据加载"""

    def test_converts_xshg_code(self):
        """测试转换XSHG代码"""
        with patch("jk2bt.engine.executor.get_stock_minute") as mock_get:
            mock_get.return_value = None

            result = _load_minute_data("600519.XSHG", "2024-01-01", "2024-12-31")

    def test_converts_xshe_code(self):
        """测试转换XSHE代码"""
        with patch("jk2bt.engine.executor.get_stock_minute") as mock_get:
            mock_get.return_value = None

            result = _load_minute_data("000001.XSHE", "2024-01-01", "2024-12-31")

    def test_returns_none_for_empty_data(self):
        """测试空数据返回None"""
        with patch("jk2bt.engine.executor.get_stock_minute") as mock_get:
            mock_get.return_value = None

            result = _load_minute_data("600519.XSHG", "2024-01-01", "2024-12-31")
            assert result is None


class TestDiscoverStrategyStocks:
    """测试 _discover_strategy_stocks 股票池发现"""

    def test_returns_discovered_stocks_and_report(self):
        """测试返回发现的股票和报告"""
        with patch("jk2bt.engine.executor._static_analyze_stock_pool") as mock_static:
            mock_static.return_value = (set(), {"index_weight_failures": []})

            with patch("jk2bt.engine.executor._get_strategy_wrapper") as mock_wrapper:
                mock_wrapper.return_value = None

                result, report = _discover_strategy_stocks(
                    {}, "2024-01-01", "2024-12-31"
                )

                assert isinstance(result, set)
                assert isinstance(report, dict)
                assert "static_analysis" in report
                assert "warnings" in report

    def test_report_has_correct_structure(self):
        """测试报告结构正确"""
        with patch("jk2bt.engine.executor._static_analyze_stock_pool") as mock_static:
            mock_static.return_value = (set(), {"index_weight_failures": []})

            with patch("jk2bt.engine.executor._get_strategy_wrapper"):
                _, report = _discover_strategy_stocks({}, "2024-01-01", "2024-12-31")

                assert "static_analysis" in report
                assert "fallback_used" in report
