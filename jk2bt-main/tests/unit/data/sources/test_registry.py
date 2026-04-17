"""
test_registry.py
测试数据源注册中心
"""

import pytest
from unittest.mock import patch, MagicMock

from jk2bt.data.sources.registry import (
    DataRegistry,
    get_data_source,
    set_data_source,
    reset_data_source,
)
from jk2bt.data.sources.base import DataSource
from jk2bt.data.sources.mock import MockDataSource


class DummyDataSource(DataSource):
    """用于测试的虚拟数据源"""

    name = "dummy"
    source_type = "dummy"

    def get_daily_data(self, symbol, start_date, end_date, adjust="qfq", **kwargs):
        import pandas as pd

        return pd.DataFrame()

    def get_index_stocks(self, index_code, **kwargs):
        return []

    def get_index_components(self, index_code, include_weights=True, **kwargs):
        import pandas as pd

        return pd.DataFrame()

    def get_trading_days(self, start_date=None, end_date=None, **kwargs):
        return []

    def get_securities_list(self, security_type="stock", date=None, **kwargs):
        import pandas as pd

        return pd.DataFrame()

    def get_security_info(self, symbol, **kwargs):
        return {}

    def get_minute_data(
        self, symbol, freq="1min", start_date=None, end_date=None, **kwargs
    ):
        import pandas as pd

        return pd.DataFrame()

    def get_money_flow(self, symbol, start_date=None, end_date=None, **kwargs):
        import pandas as pd

        return pd.DataFrame()

    def get_north_money_flow(self, start_date=None, end_date=None, **kwargs):
        import pandas as pd

        return pd.DataFrame()

    def get_industry_stocks(self, industry_code, level=1, **kwargs):
        return []

    def get_industry_mapping(self, symbol, level=1, **kwargs):
        return ""

    def get_finance_indicator(
        self, symbol, fields=None, start_date=None, end_date=None, **kwargs
    ):
        import pandas as pd

        return pd.DataFrame()

    def get_call_auction(self, symbol, date=None, **kwargs):
        import pandas as pd

        return pd.DataFrame()


class TestDataRegistry:
    """测试 DataRegistry 类"""

    @pytest.fixture(autouse=True)
    def reset_registry(self):
        """每个测试后重置注册表"""
        DataRegistry.reset()
        yield
        DataRegistry.reset()

    def test_singleton_pattern(self):
        """测试单例模式"""
        registry1 = DataRegistry()
        registry2 = DataRegistry()
        assert registry1 is registry2

    def test_register_and_get_source(self):
        """测试注册和获取数据源"""
        mock_source = MockDataSource()
        DataRegistry.register(mock_source)

        source = DataRegistry.get_source()
        assert source is mock_source
        assert source.name == "mock"

    def test_register_validates_type(self):
        """测试注册时类型验证"""
        with pytest.raises(ValueError):
            DataRegistry.register("not a datasource")

    def test_register_class(self):
        """测试注册数据源类"""
        DataRegistry.register_class(MockDataSource)
        source = DataRegistry.get_source()
        assert isinstance(source, MockDataSource)

    def test_reset(self):
        """测试重置功能"""
        mock_source = MockDataSource()
        DataRegistry.register(mock_source)
        assert DataRegistry.get_source() is mock_source

        DataRegistry.reset()
        assert not DataRegistry.is_initialized()

    def test_get_source_info(self):
        """测试获取数据源信息"""
        mock_source = MockDataSource()
        DataRegistry.register(mock_source)

        info = DataRegistry.get_source_info()
        assert info["status"] == "initialized"
        assert info["name"] == "mock"

    def test_get_source_info_not_initialized(self):
        """测试未初始化时的信息"""
        info = DataRegistry.get_source_info()
        assert info["status"] == "not_initialized"
        assert info["name"] is None

    def test_health_check(self):
        """测试健康检查"""
        mock_source = MockDataSource()
        DataRegistry.register(mock_source)

        result = DataRegistry.health_check()
        assert result["status"] == "ok"

    def test_is_initialized(self):
        """测试初始化状态检查"""
        assert not DataRegistry.is_initialized()
        DataRegistry.register(MockDataSource())
        assert DataRegistry.is_initialized()

    def test_get_source_name(self):
        """测试获取数据源名称"""
        assert DataRegistry.get_source_name() == "not_initialized"
        DataRegistry.register(MockDataSource())
        assert DataRegistry.get_source_name() == "mock"


class TestConvenienceFunctions:
    """测试便捷函数"""

    @pytest.fixture(autouse=True)
    def reset_registry(self):
        DataRegistry.reset()
        yield
        DataRegistry.reset()

    def test_get_data_source(self):
        """测试 get_data_source 函数"""
        DataRegistry.register(MockDataSource())
        source = get_data_source()
        assert isinstance(source, DataSource)

    def test_set_data_source(self):
        """测试 set_data_source 函数"""
        mock_source = MockDataSource()
        set_data_source(mock_source)
        assert DataRegistry.get_source() is mock_source

    def test_reset_data_source(self):
        """测试 reset_data_source 函数"""
        DataRegistry.register(MockDataSource())
        reset_data_source()
        assert not DataRegistry.is_initialized()


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
