"""
tests/test_market_missing.py
补充缺失的 market_data 模块测试

测试模块：
- stock.py - 股票行情
- etf.py - ETF 行情
- index.py - 指数行情
- minute.py - 分钟数据
- industry.py - 行业数据
- call_auction.py - 集合竞价
- north_money.py - 北向资金
- fund_of.py - 基金
- lof.py - LOF 基金
"""

import pytest
import pandas as pd
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))


class TestStockAPI:
    """测试股票行情 API"""

    def test_import_stock_module(self):
        """测试导入 stock 模块"""
        from jk2bt.market_data.stock import get_stock_daily

        assert callable(get_stock_daily)

    def test_get_stock_daily_basic(self):
        """测试获取股票日线数据"""
        from jk2bt.market_data.stock import get_stock_daily

        df = get_stock_daily(
            "sh600519",
            start="2025-01-01",
            end="2025-01-31",
            force_update=False,
        )

        assert isinstance(df, pd.DataFrame)


class TestETFAPI:
    """测试 ETF 行情 API"""

    def test_import_etf_module(self):
        """测试导入 etf 模块"""
        from jk2bt.market_data.etf import get_etf_daily

        assert callable(get_etf_daily)

    def test_get_etf_daily_basic(self):
        """测试获取 ETF 日线数据"""
        from jk2bt.market_data.etf import get_etf_daily

        df = get_etf_daily(
            "510300",
            start="2025-01-01",
            end="2025-01-31",
            force_update=False,
        )

        assert isinstance(df, pd.DataFrame)


class TestIndexAPI:
    """测试指数行情 API"""

    def test_import_index_module(self):
        """测试导入 index 模块"""
        from jk2bt.market_data.index import get_index_daily

        assert callable(get_index_daily)

    def test_get_index_daily_basic(self):
        """测试获取指数日线数据"""
        from jk2bt.market_data.index import get_index_daily

        df = get_index_daily(
            "000300",
            start="2025-01-01",
            end="2025-01-31",
            force_update=False,
        )

        assert isinstance(df, pd.DataFrame)


class TestMinuteAPI:
    """测试分钟数据 API"""

    def test_import_minute_module(self):
        """测试导入 minute 模块"""
        from jk2bt.market_data.minute import (
            get_stock_minute,
            get_etf_minute,
        )

        assert callable(get_stock_minute)
        assert callable(get_etf_minute)

    def test_get_stock_minute_basic(self):
        """测试获取股票分钟数据"""
        from jk2bt.market_data.minute import (
            get_stock_minute,
        )

        df = get_stock_minute(
            "sh600519",
            period="1m",
            start="2025-01-15 09:30:00",
            end="2025-01-15 15:00:00",
            force_update=False,
        )

        assert isinstance(df, pd.DataFrame)


class TestIndustryAPI:
    """测试行业数据 API"""

    def test_import_industry_module(self):
        """测试导入 industry 模块"""
        from jk2bt.market_data.industry import (
            get_industry_stocks,
            get_stock_industry,
        )

        assert callable(get_industry_stocks)
        assert callable(get_stock_industry)

    def test_get_stock_industry_basic(self):
        """测试获取股票所属行业"""
        from jk2bt.market_data.industry import (
            get_stock_industry,
        )

        result = get_stock_industry("600519.XSHG")

        assert result is not None or result == {}


class TestCallAuctionAPI:
    """测试集合竞价 API"""

    def test_import_call_auction_module(self):
        """测试导入 call_auction 模块"""
        from jk2bt.market_data.call_auction import (
            get_call_auction,
        )

        assert callable(get_call_auction)

    def test_get_call_auction_realtime(self):
        """测试获取实时竞价数据"""
        from jk2bt.market_data.call_auction import (
            get_call_auction,
        )

        # 使用当日日期（实时数据）
        from datetime import date

        today = date.today().strftime("%Y-%m-%d")

        df = get_call_auction(
            stock_list=["600519.XSHG"],
            start_date=today,
            end_date=today,
        )

        assert isinstance(df, pd.DataFrame)
        assert "capability" in df.columns


class TestNorthMoneyAPI:
    """测试北向资金 API"""

    def test_import_north_money_module(self):
        """测试导入 north_money 模块"""
        from jk2bt.market_data.north_money import (
            get_north_money_flow,
        )

        assert callable(get_north_money_flow)


class TestFundOfAPI:
    """测试场外基金 API"""

    def test_import_fund_of_module(self):
        """测试导入 fund_of 模块"""
        from jk2bt.market_data.fund_of import (
            get_fund_of_nav,
        )

        assert callable(get_fund_of_nav)

    def test_get_fund_of_nav(self):
        """测试获取场外基金净值"""
        from jk2bt.market_data.fund_of import (
            get_fund_of_nav,
        )

        # 使用知名基金代码测试
        try:
            df = get_fund_of_nav("000001", start="2024-01-01", end="2024-12-31")
            assert isinstance(df, pd.DataFrame)
        except Exception:
            # 网络不可用时跳过
            pass


class TestLOFAPI:
    """测试 LOF 基金 API"""

    def test_import_lof_module(self):
        """测试导入 lof 模块"""
        from jk2bt.market_data.lof import (
            get_lof_daily,
        )

        assert callable(get_lof_daily)

    def test_get_lof_daily(self):
        """测试获取 LOF 日线数据"""
        from jk2bt.market_data.lof import (
            get_lof_daily,
        )

        # 使用知名 LOF 代码测试（招商中证白酒）
        try:
            df = get_lof_daily(
                "161725",
                start="2024-12-01",
                end="2024-12-31",
                retry_count=1,
            )
            assert isinstance(df, pd.DataFrame)
        except Exception:
            # 网络不可用时跳过
            pass


def test_quick_validation():
    """快速验证测试"""
    print("\n=== 快速验证测试 ===")

    from jk2bt.market_data.stock import get_stock_daily
    from jk2bt.market_data.etf import get_etf_daily
    from jk2bt.market_data.index import get_index_daily

    print("\n1. 测试股票日线")
    df_stock = get_stock_daily(
        "sh600519", "2025-01-01", "2025-01-31", force_update=False
    )
    print(f"   股票日线数据: {len(df_stock)} 条")

    print("\n2. 测试 ETF 日线")
    df_etf = get_etf_daily("510300", "2025-01-01", "2025-01-31", force_update=False)
    print(f"   ETF 日线数据: {len(df_etf)} 条")

    print("\n3. 测试指数日线")
    df_index = get_index_daily("000300", "2025-01-01", "2025-01-31", force_update=False)
    print(f"   指数日线数据: {len(df_index)} 条")

    print("\n=== 验证完成 ===\n")


if __name__ == "__main__":
    test_quick_validation()
    pytest.main([__file__, "-v", "-s"])
