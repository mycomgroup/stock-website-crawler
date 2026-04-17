"""
test_base.py
测试 DataSource 抽象基类
"""

import pytest
from abc import ABC
from datetime import datetime, date
from typing import List, Dict, Any

from jk2bt.data.sources.base import DataSource
from jk2bt.data.sources.error_codes import DataSourceError


class ConcreteDataSource(DataSource):
    """DataSource 的具体实现，用于测试"""

    name = "test"
    source_type = "test"

    def get_daily_data(
        self,
        symbol: str,
        start_date,
        end_date,
        adjust: str = "qfq",
        **kwargs,
    ):
        import pandas as pd

        return pd.DataFrame(
            {
                "datetime": [datetime(2020, 1, 1)],
                "open": [10.0],
                "high": [10.5],
                "low": [9.5],
                "close": [10.2],
                "volume": [1000000],
            }
        )

    def get_index_stocks(self, index_code: str, **kwargs) -> List[str]:
        return ["600519.XSHG", "600036.XSHG"]

    def get_index_components(
        self,
        index_code: str,
        include_weights: bool = True,
        **kwargs,
    ):
        import pandas as pd

        return pd.DataFrame(
            {
                "index_code": ["000300.XSHG"],
                "code": ["600519.XSHG"],
                "stock_name": ["测试股票"],
                "weight": [10.0],
            }
        )

    def get_trading_days(
        self,
        start_date=None,
        end_date=None,
        **kwargs,
    ) -> List[str]:
        return ["2020-01-02", "2020-01-03"]

    def get_securities_list(
        self,
        security_type: str = "stock",
        date=None,
        **kwargs,
    ):
        import pandas as pd

        return pd.DataFrame(
            {
                "code": ["600519.XSHG"],
                "display_name": ["贵州茅台"],
                "type": ["stock"],
            }
        )

    def get_security_info(self, symbol: str, **kwargs) -> Dict[str, Any]:
        return {
            "code": symbol,
            "display_name": "测试股票",
            "type": "stock",
        }

    def get_minute_data(
        self,
        symbol: str,
        freq: str = "1min",
        start_date=None,
        end_date=None,
        **kwargs,
    ):
        import pandas as pd

        return pd.DataFrame(
            {
                "datetime": [datetime(2020, 1, 1, 9, 30)],
                "open": [10.0],
                "high": [10.1],
                "low": [9.9],
                "close": [10.05],
                "volume": [10000],
            }
        )

    def get_money_flow(
        self,
        symbol: str,
        start_date=None,
        end_date=None,
        **kwargs,
    ):
        import pandas as pd

        return pd.DataFrame(
            {
                "date": ["2020-01-02"],
                "main_buy": [1000000],
                "main_sell": [800000],
                "main_net": [200000],
            }
        )

    def get_north_money_flow(
        self,
        start_date=None,
        end_date=None,
        **kwargs,
    ):
        import pandas as pd

        return pd.DataFrame(
            {
                "date": ["2020-01-02"],
                "north_buy": [50000000],
                "north_sell": [45000000],
                "north_net": [5000000],
            }
        )

    def get_industry_stocks(
        self,
        industry_code: str,
        level: int = 1,
        **kwargs,
    ) -> List[str]:
        return ["600519.XSHG", "000858.XSHE"]

    def get_industry_mapping(
        self,
        symbol: str,
        level: int = 1,
        **kwargs,
    ) -> str:
        return "801010"

    def get_finance_indicator(
        self,
        symbol: str,
        fields=None,
        start_date=None,
        end_date=None,
        **kwargs,
    ):
        import pandas as pd

        return pd.DataFrame(
            {
                "date": ["2020-03-31"],
                "roe": [0.15],
            }
        )

    def get_call_auction(
        self,
        symbol: str,
        date=None,
        **kwargs,
    ):
        import pandas as pd

        return pd.DataFrame(
            {
                "time": ["09:15:00"],
                "price": [10.0],
                "volume": [1000],
            }
        )


class TestDataSourceBase:
    """测试 DataSource 基类"""

    @pytest.fixture
    def source(self):
        return ConcreteDataSource()

    def test_is_abc(self, source):
        """验证 DataSource 是抽象基类"""
        assert issubclass(DataSource, ABC)
        assert isinstance(source, DataSource)

    def test_name_and_type(self, source):
        """测试数据源名称和类型"""
        assert source.name == "test"
        assert source.source_type == "test"

    def test_get_daily_data(self, source):
        """测试获取日线数据"""
        df = source.get_daily_data("600519", "2020-01-01", "2020-12-31")
        assert len(df) == 1
        assert "open" in df.columns
        assert "high" in df.columns
        assert "close" in df.columns

    def test_get_index_stocks(self, source):
        """测试获取指数成分股"""
        stocks = source.get_index_stocks("000300")
        assert len(stocks) == 2
        assert "600519.XSHG" in stocks

    def test_get_trading_days(self, source):
        """测试获取交易日"""
        days = source.get_trading_days()
        assert len(days) == 2
        assert "2020-01-02" in days

    def test_get_securities_list(self, source):
        """测试获取证券列表"""
        df = source.get_securities_list()
        assert len(df) == 1
        assert "code" in df.columns

    def test_get_security_info(self, source):
        """测试获取证券信息"""
        info = source.get_security_info("600519")
        assert info["code"] == "600519"
        assert "display_name" in info

    def test_get_money_flow(self, source):
        """测试获取资金流向"""
        df = source.get_money_flow("600519")
        assert len(df) == 1
        assert "main_net" in df.columns

    def test_get_north_money_flow(self, source):
        """测试获取北向资金"""
        df = source.get_north_money_flow()
        assert len(df) == 1
        assert "north_net" in df.columns

    def test_get_industry_stocks(self, source):
        """测试获取行业成分股"""
        stocks = source.get_industry_stocks("801010")
        assert len(stocks) == 2

    def test_get_industry_mapping(self, source):
        """测试获取股票所属行业"""
        industry = source.get_industry_mapping("600519")
        assert industry == "801010"

    def test_get_finance_indicator(self, source):
        """测试获取财务指标"""
        df = source.get_finance_indicator("600519")
        assert len(df) == 1
        assert "roe" in df.columns

    def test_health_check(self, source):
        """测试健康检查"""
        result = source.health_check()
        assert result["status"] == "ok"
        assert "message" in result
        assert "latency_ms" in result

    def test_get_source_info(self, source):
        """测试获取数据源信息"""
        info = source.get_source_info()
        assert info["name"] == "test"
        assert info["type"] == "test"

    def test_get_etf_daily_default(self, source):
        """测试默认 ETF 日线获取"""
        df = source.get_etf_daily("510300", "2020-01-01", "2020-12-31")
        assert len(df) == 1

    def test_get_index_daily_default(self, source):
        """测试默认指数日线获取"""
        df = source.get_index_daily("000300", "2020-01-01", "2020-12-31")
        assert len(df) == 1

    def test_not_implemented_methods(self, source):
        """测试未实现方法抛出 NotImplementedError"""
        with pytest.raises(NotImplementedError):
            source.get_st_stocks()

        with pytest.raises(NotImplementedError):
            source.get_suspended_stocks()

        with pytest.raises(NotImplementedError):
            source.get_index_valuation("000300")

        with pytest.raises(NotImplementedError):
            source.get_stock_pe_pb("600519")


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
