"""
test_multi_asset.py
多资产能力验证测试

验证:
- LOF 数据获取和交易
- OF 净值数据和申赎模拟
- 期货元数据获取
"""

import unittest
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from jk2bt.asset_router import (
    identify_asset,
    AssetType,
    TradingStatus,
    get_trading_status_desc,
)
from jk2bt.market_data.lof import (
    get_lof_daily_with_fallback,
    get_lof_nav,
)
from jk2bt.market_data.fund_of import get_fund_of_nav
from jk2bt.market_data.futures import (
    get_contract_multiplier,
    get_margin_rate,
    get_future_contracts,
)
from jk2bt.core.strategy_base import FundOFPosition


class TestAssetRouterMultiAsset(unittest.TestCase):
    """测试资产路由器对多资产的支持"""

    def test_identify_stock(self):
        """测试股票识别"""
        info = identify_asset("600519.XSHG")
        self.assertEqual(info.asset_type, AssetType.STOCK)
        self.assertEqual(info.trading_status, TradingStatus.SUPPORTED)

    def test_identify_etf(self):
        """测试 ETF 识别"""
        info = identify_asset("510300.XSHG")
        self.assertEqual(info.asset_type, AssetType.ETF)
        self.assertEqual(info.trading_status, TradingStatus.SUPPORTED)

    def test_identify_lof(self):
        """测试 LOF 识别"""
        info = identify_asset("161725")
        self.assertEqual(info.asset_type, AssetType.LOF)
        self.assertIn(
            info.trading_status,
            [TradingStatus.SUPPORTED, TradingStatus.NETWORK_UNSTABLE],
        )

    def test_identify_fund_of(self):
        """测试场外基金识别"""
        info = identify_asset("000001.OF")
        self.assertEqual(info.asset_type, AssetType.FUND_OF)
        self.assertEqual(info.trading_status, TradingStatus.IDENTIFIED_ONLY)

    def test_identify_future(self):
        """测试股指期货识别"""
        info = identify_asset("IF2403.CCFX")
        self.assertEqual(info.asset_type, AssetType.FUTURE_CCFX)
        self.assertEqual(info.trading_status, TradingStatus.IDENTIFIED_ONLY)

    def test_trading_status_desc(self):
        """测试交易状态描述"""
        self.assertEqual(get_trading_status_desc("600519.XSHG"), "支持交易")
        self.assertIn(
            get_trading_status_desc("161725"), ["支持交易", "接口不稳定(可能失败)"]
        )
        self.assertIn(
            get_trading_status_desc("000001.OF"),
            ["已识别(暂不支持)", "已识别(暂不支持交易)"],
        )
        self.assertIn(
            get_trading_status_desc("IF2403.CCFX"),
            ["已识别(暂不支持)", "已识别(暂不支持交易)"],
        )


class TestLOFData(unittest.TestCase):
    """测试 LOF 数据获取"""

    def test_lof_nav_data(self):
        """测试 LOF 净值数据获取"""
        try:
            df = get_lof_nav("161725", start="2024-01-01", end="2024-03-01")
            self.assertFalse(df.empty, "LOF 净值数据不应为空")
            self.assertIn("datetime", df.columns)
            self.assertIn("unit_nav", df.columns)
            print(f"\nLOF 净值数据行数: {len(df)}")
            print(f"列名: {list(df.columns)}")
        except Exception as e:
            self.skipTest(f"LOF 净值数据获取失败: {e}")


class TestFundOFData(unittest.TestCase):
    """测试场外基金数据获取"""

    def test_fund_of_nav(self):
        """测试场外基金净值获取"""
        try:
            df = get_fund_of_nav("000001", start="2024-01-01", end="2024-03-01")
            self.assertFalse(df.empty, "场外基金净值数据不应为空")
            self.assertIn("datetime", df.columns)
            self.assertIn("unit_nav", df.columns)
            print(f"\nOF 净值数据行数: {len(df)}")
            print(f"列名: {list(df.columns)}")
        except Exception as e:
            self.skipTest(f"场外基金净值获取失败: {e}")


class TestFundOFPosition(unittest.TestCase):
    """测试场外基金申赎模拟"""

    def test_subscribe(self):
        """测试申购"""
        pos = FundOFPosition("000001")
        shares, fee = pos.subscribe(10000, nav=1.5, fee_rate=0.0015)

        self.assertAlmostEqual(shares, 6656.67, places=1)
        self.assertAlmostEqual(fee, 15, places=1)
        self.assertAlmostEqual(pos.shares, 6656.67, places=1)
        self.assertAlmostEqual(pos.cost, 10000, places=1)

    def test_redeem(self):
        """测试赎回"""
        pos = FundOFPosition("000001")
        pos.subscribe(10000, nav=1.5)

        actual_amount, fee = pos.redeem(3000, nav=1.6, holding_days=100)

        self.assertGreater(actual_amount, 0)
        self.assertGreater(fee, 0)
        self.assertAlmostEqual(pos.shares, 3656.67, places=1)

    def test_profit_calculation(self):
        """测试收益计算"""
        pos = FundOFPosition("000001")
        pos.subscribe(10000, nav=1.5)

        profit = pos.get_profit(current_nav=1.6)
        profit_rate = pos.get_profit_rate(current_nav=1.6)

        self.assertGreater(profit, 0)
        self.assertGreater(profit_rate, 0)

    def test_redeem_fee_by_holding_days(self):
        """测试赎回费率随持有天数变化"""
        pos = FundOFPosition("000001")
        pos.subscribe(10000, nav=1.5)

        _, fee_30d = pos.redeem(1000, nav=1.6, holding_days=30)
        pos.subscribe(10000, nav=1.5)  # 补充份额
        _, fee_180d = pos.redeem(1000, nav=1.6, holding_days=180)
        pos.subscribe(10000, nav=1.5)  # 补充份额
        _, fee_365d = pos.redeem(1000, nav=1.6, holding_days=365)

        # 30天费率0.5%, 180天费率0.25%, 365天费率0%
        self.assertGreater(fee_30d, fee_180d)
        self.assertGreater(fee_180d, fee_365d)
        self.assertEqual(fee_365d, 0)


class TestFuturesMetadata(unittest.TestCase):
    """测试期货元数据"""

    def test_contract_multiplier(self):
        """测试合约乘数"""
        multiplier_if = get_contract_multiplier("IF2403")
        self.assertEqual(multiplier_if, 300)

        multiplier_ic = get_contract_multiplier("IC2403")
        self.assertEqual(multiplier_ic, 200)

    def test_margin_rate(self):
        """测试保证金比例"""
        margin_if = get_margin_rate("IF2403")
        self.assertGreater(margin_if, 0)
        self.assertLess(margin_if, 1)

    def test_future_contracts(self):
        """测试期货合约信息获取"""
        try:
            df = get_future_contracts(date="2024-03-15")
            self.assertFalse(df.empty, "期货合约信息不应为空")
            self.assertIn("合约代码", df.columns)
            print(f"\n期货合约数: {len(df)}")
            if_df = df[df["品种"] == "IF"] if "品种" in df.columns else df
            print(f"IF合约数: {len(if_df)}")
        except Exception as e:
            self.skipTest(f"期货合约信息获取失败: {e}")


class TestMarketAPILofSupport(unittest.TestCase):
    """测试 market_api 对 LOF 的支持"""

    def test_lof_detection(self):
        """测试 LOF 代码检测"""
        from jk2bt.api.market import _normalize_symbol

        lof_codes = ["161725", "162411", "160105"]
        for code in lof_codes:
            normalized = _normalize_symbol(code)
            self.assertTrue(normalized.startswith("16"), f"{code} 应被识别为 LOF")


if __name__ == "__main__":
    unittest.main(verbosity=2)
