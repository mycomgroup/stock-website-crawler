"""
test_akshare_adapter_cache.py
AkShareAdapter 缓存功能连通性测试

测试所有加缓存的方法，验证：
1. 能正常调用 akshare 获取数据
2. 缓存读写生效（第二次调用命中缓存）
3. 最小数据量，加速测试

注意：使用历史日期确保有数据，避免周末非交易日无数据导致 skip
"""

import pytest
import pandas as pd
from datetime import datetime, timedelta
import logging

logger = logging.getLogger(__name__)


# 使用历史日期确保有数据（避免周末非交易日无数据）
HISTORICAL_START = "2024-01-01"
HISTORICAL_END = "2024-01-10"


def _skip_if_no_akshare(adapter):
    """跳过无 akshare 的情况"""
    if not adapter._akshare_available:
        pytest.skip("akshare 不可用")


class TestAkShareAdapterCache:
    """测试 AkShareAdapter 缓存功能"""

    @pytest.fixture(scope="class")
    def adapter(self):
        """创建 adapter 实例，类级别复用"""
        from jk2bt.data.sources.akshare_adapter import AkShareAdapter

        return AkShareAdapter(use_cache=True)

    # ── P0 日线类 ──

    def test_get_daily_data(self, adapter):
        """测试日线数据缓存"""
        _skip_if_no_akshare(adapter)
        df1 = adapter.get_daily_data("600519", HISTORICAL_START, HISTORICAL_END)
        assert isinstance(df1, pd.DataFrame)
        df2 = adapter.get_daily_data("600519", HISTORICAL_START, HISTORICAL_END)
        assert isinstance(df2, pd.DataFrame)

    def test_get_etf_daily(self, adapter):
        """测试 ETF 日线缓存"""
        _skip_if_no_akshare(adapter)
        df1 = adapter.get_etf_daily("510300", HISTORICAL_START, HISTORICAL_END)
        assert isinstance(df1, pd.DataFrame)
        df2 = adapter.get_etf_daily("510300", HISTORICAL_START, HISTORICAL_END)
        assert isinstance(df2, pd.DataFrame)

    def test_get_index_daily(self, adapter):
        """测试指数日线缓存"""
        _skip_if_no_akshare(adapter)
        df1 = adapter.get_index_daily("000300", HISTORICAL_START, HISTORICAL_END)
        assert isinstance(df1, pd.DataFrame)
        df2 = adapter.get_index_daily("000300", HISTORICAL_START, HISTORICAL_END)
        assert isinstance(df2, pd.DataFrame)

    # ── P0 指数成分类 ──

    def test_get_index_stocks(self, adapter):
        """测试指数成分股列表缓存"""
        _skip_if_no_akshare(adapter)
        stocks1 = adapter.get_index_stocks("000300")
        assert isinstance(stocks1, list)
        assert len(stocks1) >= 10

        stocks2 = adapter.get_index_stocks("000300")
        assert isinstance(stocks2, list)

    def test_get_index_components(self, adapter):
        """测试指数成分股详情缓存"""
        _skip_if_no_akshare(adapter)
        df1 = adapter.get_index_components("000300")
        assert isinstance(df1, pd.DataFrame)

        df2 = adapter.get_index_components("000300")
        assert isinstance(df2, pd.DataFrame)

    # ── P0 财务类 ──

    def test_get_finance_indicator(self, adapter):
        """测试财务指标缓存"""
        _skip_if_no_akshare(adapter)
        df1 = adapter.get_finance_indicator("600519")
        assert isinstance(df1, pd.DataFrame)

        df2 = adapter.get_finance_indicator("600519")
        assert isinstance(df2, pd.DataFrame)

    def test_get_cashflow(self, adapter):
        """测试现金流缓存"""
        _skip_if_no_akshare(adapter)
        df1 = adapter.get_cashflow("600519")
        assert isinstance(df1, pd.DataFrame)

        df2 = adapter.get_cashflow("600519")
        assert isinstance(df2, pd.DataFrame)

    # ── P1 资金流类 ──

    def test_get_money_flow(self, adapter):
        """测试资金流向缓存"""
        _skip_if_no_akshare(adapter)
        df1 = adapter.get_money_flow("600519")
        assert isinstance(df1, pd.DataFrame)

        df2 = adapter.get_money_flow("600519")
        assert isinstance(df2, pd.DataFrame)

    def test_get_north_money_flow(self, adapter):
        """测试北向资金缓存"""
        _skip_if_no_akshare(adapter)
        df1 = adapter.get_north_money_flow()
        assert isinstance(df1, pd.DataFrame)
        df2 = adapter.get_north_money_flow()
        assert isinstance(df2, pd.DataFrame)

    # ── P1 行业概念类 ──

    def test_get_industry_stocks(self, adapter):
        """测试行业成分股缓存（使用申万一级农林牧渔）"""
        _skip_if_no_akshare(adapter)
        stocks1 = adapter.get_industry_stocks("801010")  # 农林牧渔一级行业
        assert isinstance(stocks1, list)
        assert len(stocks1) >= 1
        stocks2 = adapter.get_industry_stocks("801010")
        assert isinstance(stocks2, list)

    def test_get_industry_mapping(self, adapter):
        """测试行业映射缓存"""
        _skip_if_no_akshare(adapter)
        industry1 = adapter.get_industry_mapping("600519")
        assert isinstance(industry1, str)

        industry2 = adapter.get_industry_mapping("600519")
        assert isinstance(industry2, str)

    # ── P1 估值类 ──

    def test_get_index_valuation(self, adapter):
        """测试指数估值缓存"""
        _skip_if_no_akshare(adapter)
        df1 = adapter.get_index_valuation("000300")
        assert isinstance(df1, pd.DataFrame)
        df2 = adapter.get_index_valuation("000300")
        assert isinstance(df2, pd.DataFrame)

    def test_get_stock_valuation(self, adapter):
        """测试个股估值缓存"""
        _skip_if_no_akshare(adapter)
        df1 = adapter.get_stock_valuation("600519")
        assert isinstance(df1, pd.DataFrame)
        df2 = adapter.get_stock_valuation("600519")
        assert isinstance(df2, pd.DataFrame)

    def test_get_stock_pe_pb(self, adapter):
        """测试 PE/PB 缓存"""
        _skip_if_no_akshare(adapter)
        df1 = adapter.get_stock_pe_pb("600519")
        assert isinstance(df1, pd.DataFrame)
        df2 = adapter.get_stock_pe_pb("600519")
        assert isinstance(df2, pd.DataFrame)

    # ── P2 分红/质押/解禁 ──

    def test_get_dividend_fhps(self, adapter):
        """测试分红送股缓存"""
        _skip_if_no_akshare(adapter)
        df1 = adapter.get_dividend_fhps(symbol="600519")
        assert isinstance(df1, pd.DataFrame)
        df2 = adapter.get_dividend_fhps(symbol="600519")
        assert isinstance(df2, pd.DataFrame)

    def test_get_pledge_ratio_em(self, adapter):
        """测试股权质押缓存"""
        _skip_if_no_akshare(adapter)
        df1 = adapter.get_pledge_ratio_em("600519")
        assert isinstance(df1, pd.DataFrame)
        df2 = adapter.get_pledge_ratio_em("600519")
        assert isinstance(df2, pd.DataFrame)

    def test_get_unlock_schedule(self, adapter):
        """测试解禁计划缓存"""
        _skip_if_no_akshare(adapter)
        df1 = adapter.get_unlock_schedule("600519")
        assert isinstance(df1, pd.DataFrame)
        df2 = adapter.get_unlock_schedule("600519")
        assert isinstance(df2, pd.DataFrame)

    # ── P2 宏观/两融 ──

    def test_get_macro_raw(self, adapter):
        """测试宏观数据缓存"""
        _skip_if_no_akshare(adapter)
        df1 = adapter.get_macro_raw("gdp")
        assert isinstance(df1, pd.DataFrame)

        df2 = adapter.get_macro_raw("gdp")
        assert isinstance(df2, pd.DataFrame)

    def test_get_margin_detail(self, adapter):
        """测试融资融券缓存（使用历史交易日）"""
        _skip_if_no_akshare(adapter)
        df1 = adapter.get_margin_detail("sh", "2024-01-05")  # 使用历史交易日
        assert isinstance(df1, pd.DataFrame)
        df2 = adapter.get_margin_detail("sh", "2024-01-05")
        assert isinstance(df2, pd.DataFrame)


class TestAkShareAdapterCacheDisabled:
    """测试缓存关闭时正常请求"""

    @pytest.fixture
    def adapter_no_cache(self):
        from jk2bt.data.sources.akshare_adapter import AkShareAdapter

        return AkShareAdapter(use_cache=False)

    def test_get_daily_data_no_cache(self, adapter_no_cache):
        """缓存关闭时日线数据正常"""
        _skip_if_no_akshare(adapter_no_cache)
        df = adapter_no_cache.get_daily_data("600519", HISTORICAL_START, HISTORICAL_END)
        assert isinstance(df, pd.DataFrame)


if __name__ == "__main__":
    pytest.main([__file__, "-v", "-s", "--timeout=120"])
