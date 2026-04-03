"""
tests/integration/test_duckdb.py
DuckDB 集成测试（迁移自 tests/test_duckdb_integration.py）

这些测试需要真实数据库和数据，标记为 integration。
"""

import pytest

pytestmark = pytest.mark.integration


class TestDuckDBConnection:
    """DuckDB 连接与数据统计测试"""

    def test_duckdb_manager_importable(self):
        """DuckDBManager 可导入"""
        try:
            from jk2bt.db import DuckDBManager
            assert DuckDBManager is not None
        except ImportError:
            pytest.skip("src.db.DuckDBManager 不可用")

    def test_duckdb_connection(self):
        """DuckDB 连接正常"""
        try:
            from jk2bt.db import DuckDBManager
        except ImportError:
            pytest.skip("src.db.DuckDBManager 不可用")

        db = DuckDBManager()
        stock_count = db.count_records("stock_daily")
        etf_count = db.count_records("etf_daily")
        index_count = db.count_records("index_daily")

        assert isinstance(stock_count, int)
        assert isinstance(etf_count, int)
        assert isinstance(index_count, int)

    def test_duckdb_get_symbols(self):
        """DuckDB 获取代码列表"""
        try:
            from jk2bt.db import DuckDBManager
        except ImportError:
            pytest.skip("src.db.DuckDBManager 不可用")

        db = DuckDBManager()
        stock_symbols = db.get_symbols("stock_daily")
        assert isinstance(stock_symbols, list)


class TestMarketDataModules:
    """market_data 模块数据加载测试"""

    def test_get_stock_daily_importable(self):
        """get_stock_daily 可导入"""
        try:
            from jk2bt.market_data import get_stock_daily
            assert callable(get_stock_daily)
        except ImportError:
            pytest.skip("src.market_data.get_stock_daily 不可用")

    def test_get_etf_daily_importable(self):
        """get_etf_daily 可导入"""
        try:
            from jk2bt.market_data import get_etf_daily
            assert callable(get_etf_daily)
        except ImportError:
            pytest.skip("src.market_data.get_etf_daily 不可用")

    def test_get_index_daily_importable(self):
        """get_index_daily 可导入"""
        try:
            from jk2bt.market_data import get_index_daily
            assert callable(get_index_daily)
        except ImportError:
            pytest.skip("src.market_data.get_index_daily 不可用")

    def test_stock_daily_returns_dataframe(self):
        """get_stock_daily 返回 DataFrame"""
        try:
            from jk2bt.market_data import get_stock_daily
        except ImportError:
            pytest.skip("src.market_data.get_stock_daily 不可用")

        import pandas as pd
        result = get_stock_daily("sh600000", "2023-01-01", "2023-12-31")
        assert isinstance(result, pd.DataFrame)

    def test_etf_daily_returns_dataframe(self):
        """get_etf_daily 返回 DataFrame"""
        try:
            from jk2bt.market_data import get_etf_daily
        except ImportError:
            pytest.skip("src.market_data.get_etf_daily 不可用")

        import pandas as pd
        result = get_etf_daily("510300", "2023-01-01", "2023-12-31")
        assert isinstance(result, pd.DataFrame)


class TestGetPriceIntegration:
    """get_price 集成测试"""

    def test_get_price_importable(self):
        """get_price 可从 src 导入"""
        try:
            from jk2bt import get_price
            assert callable(get_price)
        except ImportError:
            pytest.skip("src.get_price 不可用")

    def test_get_price_multiple_symbols(self):
        """get_price 多标的返回 dict"""
        try:
            from jk2bt import get_price
        except ImportError:
            pytest.skip("src.get_price 不可用")

        result = get_price(["sh600000", "sz000001"], "2023-01-01", "2023-12-31")
        assert isinstance(result, dict)
        assert len(result) > 0


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
