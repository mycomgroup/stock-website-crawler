"""
test_mock.py
测试 Mock 数据源
"""

import pytest
import pandas as pd
from datetime import datetime, date
from unittest.mock import patch

from jk2bt.data.sources.mock import MockDataSource, create_mock_with_sample_data
from jk2bt.data.sources.error_codes import DataSourceError


class TestMockDataSource:
    """测试 MockDataSource 类"""

    @pytest.fixture
    def mock_source(self):
        return MockDataSource(seed=42, generate_random=True)

    @pytest.fixture
    def preset_source(self):
        return create_mock_with_sample_data()

    def test_creation(self):
        """测试创建 Mock 数据源"""
        source = MockDataSource()
        assert source.name == "mock"
        assert source.source_type == "mock"
        assert source._seed == 42
        assert source._generate_random is True

    def test_default_index_stocks(self, mock_source):
        """测试默认指数成分股"""
        stocks = mock_source.get_index_stocks("000300.XSHG")
        assert len(stocks) > 0
        assert "600519.XSHG" in stocks

    def test_default_trading_days(self, mock_source):
        """测试默认交易日"""
        days = mock_source.get_trading_days()
        assert len(days) > 0
        assert "2020-01-02" in days

    def test_get_daily_data_generates_random(self, mock_source):
        """测试生成随机日线数据"""
        df = mock_source.get_daily_data("600000", "2020-01-01", "2020-01-10")
        assert isinstance(df, pd.DataFrame)
        assert len(df) > 0
        assert "open" in df.columns
        assert "close" in df.columns
        assert "volume" in df.columns

    def test_get_daily_data_with_preset(self, preset_source):
        """测试预设数据"""
        df = preset_source.get_daily_data("sh600000", "2020-01-01", "2020-01-10")
        assert isinstance(df, pd.DataFrame)
        assert len(df) == 5
        assert df["close"].iloc[0] == 10.2

    def test_set_mock_data(self, mock_source):
        """测试设置 Mock 数据"""
        preset_df = pd.DataFrame(
            {
                "datetime": [datetime(2020, 1, 1)],
                "open": [100.0],
                "high": [105.0],
                "low": [95.0],
                "close": [102.0],
                "volume": [1000000],
            }
        )
        mock_source.set_mock_data("daily", "test600000", preset_df)

        df = mock_source.get_daily_data("test600000", "2020-01-01", "2020-01-02")
        assert len(df) == 1
        assert df["close"].iloc[0] == 102.0

    def test_error_mode_network_error(self, mock_source):
        """测试网络错误模式"""
        mock_source.set_error_mode("network_error")
        with pytest.raises(DataSourceError) as exc_info:
            mock_source.get_daily_data("600000", "2020-01-01", "2020-01-10")
        assert "模拟网络错误" in str(exc_info.value)

    def test_error_mode_data_error(self, mock_source):
        """测试数据错误模式"""
        mock_source.set_error_mode("data_error")
        with pytest.raises(DataSourceError) as exc_info:
            mock_source.get_daily_data("600000", "2020-01-01", "2020-01-10")
        assert "模拟数据错误" in str(exc_info.value)

    def test_error_mode_timeout(self, mock_source):
        """测试超时错误模式"""
        mock_source.set_error_mode("timeout")
        with pytest.raises(DataSourceError) as exc_info:
            mock_source.get_daily_data("600000", "2020-01-01", "2020-01-10")
        assert "模拟超时" in str(exc_info.value)

    def test_clear_error_mode(self, mock_source):
        """测试清除错误模式"""
        mock_source.set_error_mode("network_error")
        mock_source.clear_error_mode()
        df = mock_source.get_daily_data("600000", "2020-01-01", "2020-01-10")
        assert len(df) > 0

    def test_get_index_stocks(self, mock_source):
        """测试获取指数成分股"""
        stocks = mock_source.get_index_stocks("000300")
        assert isinstance(stocks, list)
        assert len(stocks) >= 10

    def test_get_index_components(self, mock_source):
        """测试获取指数成分股详情"""
        df = mock_source.get_index_components("000300", include_weights=True)
        assert isinstance(df, pd.DataFrame)
        assert "code" in df.columns
        assert "weight" in df.columns

    def test_get_trading_days_filtered(self, mock_source):
        """测试过滤后的交易日"""
        days = mock_source.get_trading_days(start_date="2020-01-10")
        assert all(d >= "2020-01-10" for d in days)

    def test_get_securities_list_stock(self, mock_source):
        """测试获取股票列表"""
        df = mock_source.get_securities_list(security_type="stock")
        assert isinstance(df, pd.DataFrame)
        assert "code" in df.columns

    def test_get_securities_list_etf(self, mock_source):
        """测试获取 ETF 列表"""
        df = mock_source.get_securities_list(security_type="etf")
        assert isinstance(df, pd.DataFrame)
        assert len(df) > 0

    def test_get_security_info(self, mock_source):
        """测试获取证券信息"""
        info = mock_source.get_security_info("600519")
        assert isinstance(info, dict)
        assert info["code"] == "600519"
        assert "display_name" in info

    def test_get_minute_data(self, mock_source):
        """测试获取分钟数据"""
        df = mock_source.get_minute_data("600000", freq="1min", start_date="2020-01-01")
        assert isinstance(df, pd.DataFrame)
        assert len(df) == 240

    def test_get_money_flow(self, mock_source):
        """测试获取资金流向"""
        df = mock_source.get_money_flow(
            "600519", start_date="2020-01-01", end_date="2020-01-10"
        )
        assert isinstance(df, pd.DataFrame)
        assert "main_net" in df.columns

    def test_get_north_money_flow(self, mock_source):
        """测试获取北向资金"""
        df = mock_source.get_north_money_flow()
        assert isinstance(df, pd.DataFrame)
        assert "north_net" in df.columns

    def test_get_industry_stocks(self, mock_source):
        """测试获取行业成分股"""
        stocks = mock_source.get_industry_stocks("801010")
        assert isinstance(stocks, list)
        assert len(stocks) >= 2

    def test_get_industry_mapping(self, mock_source):
        """测试获取股票所属行业"""
        industry = mock_source.get_industry_mapping("600519")
        assert industry == "801010"

    def test_get_finance_indicator(self, mock_source):
        """测试获取财务指标"""
        df = mock_source.get_finance_indicator("600519")
        assert isinstance(df, pd.DataFrame)
        assert "roe" in df.columns

    def test_health_check(self, mock_source):
        """测试健康检查"""
        result = mock_source.health_check()
        assert result["status"] == "ok"
        assert result["latency_ms"] == 0

    def test_get_source_info(self, mock_source):
        """测试获取数据源信息"""
        info = mock_source.get_source_info()
        assert info["name"] == "mock"
        assert info["type"] == "mock"
        assert "error_mode" in info
        assert "seed" in info


class TestCreateMockWithSampleData:
    """测试预设 Mock 数据工厂函数"""

    def test_returns_mock_data_source(self):
        """验证返回 MockDataSource 实例"""
        mock = create_mock_with_sample_data()
        assert isinstance(mock, MockDataSource)

    def test_has_preset_daily_data(self):
        """验证有预设日线数据"""
        mock = create_mock_with_sample_data()
        df = mock.get_daily_data("sh600000", "2020-01-01", "2020-01-10")
        assert len(df) == 5

    def test_has_preset_index_stocks(self):
        """验证有预设指数成分股"""
        mock = create_mock_with_sample_data()
        stocks = mock.get_index_stocks("000300.XSHG")
        assert len(stocks) > 0


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
