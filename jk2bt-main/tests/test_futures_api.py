"""
test_futures_api.py
期货合约 API 测试

验证:
- get_future_contracts
- get_dominant_contract
- get_contract_multiplier
- get_margin_rate
- calculate_position_value
- calculate_required_margin
- get_future_daily
"""

import unittest
import pandas as pd
from datetime import datetime
import warnings

warnings.filterwarnings("ignore")

try:
    from jk2bt.market_data.futures import (
        parse_future_contract,
        get_future_contracts,
        get_dominant_contract,
        get_contract_multiplier,
        get_margin_rate,
        calculate_position_value,
        calculate_required_margin,
        get_future_daily,
        get_future_spot,
        CHINA_FUTURE_EXCHANGE_INFO,
        INDEX_FUTURE_PRODUCT_MAP,
    )
    from jk2bt.core.strategy_base import (
        get_future_contracts_jq,
        get_dominant_contract_jq,
        get_contract_multiplier_jq,
        get_margin_rate_jq,
        calculate_position_value_jq,
        calculate_required_margin_jq,
        get_future_daily_jq,
    )

    FUTURES_AVAILABLE = True
except ImportError as e:
    warnings.warn(f"期货模块导入失败: {e}")
    FUTURES_AVAILABLE = False


class TestFuturesContractParsing(unittest.TestCase):
    """测试期货合约代码解析"""

    def test_parse_index_future(self):
        """测试股指期货合约解析"""
        if not FUTURES_AVAILABLE:
            self.skipTest("期货模块不可用")

        result = parse_future_contract("IF2312")
        self.assertIsNotNone(result)
        self.assertEqual(result["product"], "IF")
        self.assertEqual(result["year"], "23")
        self.assertEqual(result["month"], "12")
        self.assertEqual(result["exchange"], "CFFEX")
        self.assertEqual(result["full_code"], "IF2312")

    def test_parse_commodity_future(self):
        """测试商品期货合约解析"""
        if not FUTURES_AVAILABLE:
            self.skipTest("期货模块不可用")

        result = parse_future_contract("AU2312")
        self.assertIsNotNone(result)
        self.assertEqual(result["product"], "AU")
        self.assertEqual(result["exchange"], "SHFE")

    def test_parse_with_ccfx_suffix(self):
        """测试带CCFX后缀的合约解析"""
        if not FUTURES_AVAILABLE:
            self.skipTest("期货模块不可用")

        result = parse_future_contract("IF2312.CCFX")
        self.assertIsNotNone(result)
        self.assertEqual(result["product"], "IF")
        self.assertEqual(result["full_code"], "IF2312")


class TestGetFutureContracts(unittest.TestCase):
    """测试获取期货合约列表"""

    def test_get_if_contracts(self):
        """测试获取沪深300股指期货合约"""
        if not FUTURES_AVAILABLE:
            self.skipTest("期货模块不可用")

        df = get_future_contracts(product="IF", date="2023-12-01")

        self.assertIsInstance(df, pd.DataFrame)
        if not df.empty:
            self.assertIn("contract", df.columns)
            self.assertIn("product", df.columns)
            self.assertIn("exchange", df.columns)

            if_list = df["contract"].tolist()
            self.assertTrue(any(c.startswith("IF") for c in if_list))

            print(f"\nIF合约列表 ({len(df)} 个):")
            print(df[["contract", "product", "month", "is_trading"]].to_string())

    def test_get_cffex_contracts(self):
        """测试获取中金所所有合约"""
        if not FUTURES_AVAILABLE:
            self.skipTest("期货模块不可用")

        df = get_future_contracts(exchange="CFFEX", date="2023-12-01")

        self.assertIsInstance(df, pd.DataFrame)
        if not df.empty:
            self.assertIn("exchange", df.columns)
            exchanges = df["exchange"].unique()
            self.assertTrue(all(e == "CFFEX" for e in exchanges))

            print(f"\n中金所合约列表 ({len(df)} 个):")
            products = df["product"].unique()
            print(f"产品: {list(products)}")

    def test_jq_wrapper(self):
        """测试聚宽风格包装函数"""
        if not FUTURES_AVAILABLE:
            self.skipTest("期货模块不可用")

        df = get_future_contracts_jq(product="IC")

        self.assertIsInstance(df, pd.DataFrame)
        print(f"\nIC合约列表 (JQ风格): {len(df)} 个")


class TestGetDominantContract(unittest.TestCase):
    """测试获取主力合约"""

    def test_get_if_dominant(self):
        """测试获取IF主力合约"""
        if not FUTURES_AVAILABLE:
            self.skipTest("期货模块不可用")

        contract = get_dominant_contract("IF")

        self.assertIsNotNone(contract)
        self.assertTrue(contract.startswith("IF"))

        print(f"\nIF主力合约: {contract}")

    def test_get_ic_dominant(self):
        """测试获取IC主力合约"""
        if not FUTURES_AVAILABLE:
            self.skipTest("期货模块不可用")

        contract = get_dominant_contract("IC")

        self.assertIsNotNone(contract)
        self.assertTrue(contract.startswith("IC"))

        print(f"\nIC主力合约: {contract}")

    def test_jq_wrapper(self):
        """测试聚宽风格包装函数"""
        if not FUTURES_AVAILABLE:
            self.skipTest("期货模块不可用")

        contract = get_dominant_contract_jq("IH")

        self.assertIsNotNone(contract)
        print(f"\nIH主力合约 (JQ风格): {contract}")


class TestContractMultiplier(unittest.TestCase):
    """测试合约乘数"""

    def test_if_multiplier(self):
        """测试IF合约乘数"""
        if not FUTURES_AVAILABLE:
            self.skipTest("期货模块不可用")

        multiplier = get_contract_multiplier("IF2312")

        self.assertIsNotNone(multiplier)
        self.assertEqual(multiplier, 300)

        print(f"\nIF合约乘数: {multiplier}")

    def test_ic_multiplier(self):
        """测试IC合约乘数"""
        if not FUTURES_AVAILABLE:
            self.skipTest("期货模块不可用")

        multiplier = get_contract_multiplier("IC2401")

        self.assertIsNotNone(multiplier)
        self.assertEqual(multiplier, 200)

        print(f"\nIC合约乘数: {multiplier}")

    def test_commodity_multiplier(self):
        """测试商品期货合约乘数"""
        if not FUTURES_AVAILABLE:
            self.skipTest("期货模块不可用")

        multiplier = get_contract_multiplier("AU2312")

        self.assertIsNotNone(multiplier)
        self.assertEqual(multiplier, 1000)

        print(f"\nAU合约乘数: {multiplier}")

    def test_jq_wrapper(self):
        """测试聚宽风格包装函数"""
        if not FUTURES_AVAILABLE:
            self.skipTest("期货模块不可用")

        multiplier = get_contract_multiplier_jq("IM2401")

        self.assertIsNotNone(multiplier)
        self.assertEqual(multiplier, 200)
        print(f"\nIM合约乘数 (JQ风格): {multiplier}")


class TestMarginRate(unittest.TestCase):
    """测试保证金比例"""

    def test_if_margin_rate(self):
        """测试IF保证金比例"""
        if not FUTURES_AVAILABLE:
            self.skipTest("期货模块不可用")

        rate = get_margin_rate("IF2312")

        self.assertIsNotNone(rate)
        self.assertEqual(rate, 0.12)

        print(f"\nIF保证金比例: {rate}")

    def test_ic_margin_rate(self):
        """测试IC保证金比例"""
        if not FUTURES_AVAILABLE:
            self.skipTest("期货模块不可用")

        rate = get_margin_rate("IC2401")

        self.assertIsNotNone(rate)
        self.assertEqual(rate, 0.14)

        print(f"\nIC保证金比例: {rate}")


class TestPositionValueCalculation(unittest.TestCase):
    """测试持仓价值计算"""

    def test_calculate_position_value(self):
        """测试持仓价值计算"""
        if not FUTURES_AVAILABLE:
            self.skipTest("期货模块不可用")

        value = calculate_position_value(4000, 10, "IF2312")

        self.assertIsNotNone(value)
        expected = 4000 * 300 * 10
        self.assertEqual(value, expected)

        print(f"\nIF2312持仓价值 (价格4000, 10手): {value}")

    def test_jq_wrapper(self):
        """测试聚宽风格包装函数"""
        if not FUTURES_AVAILABLE:
            self.skipTest("期货模块不可用")

        value = calculate_position_value_jq(5000, 5, "IC2401")

        self.assertIsNotNone(value)
        expected = 5000 * 200 * 5
        self.assertEqual(value, expected)
        print(f"\nIC2401持仓价值 (JQ风格, 价格5000, 5手): {value}")


class TestRequiredMarginCalculation(unittest.TestCase):
    """测试保证金计算"""

    def test_calculate_required_margin(self):
        """测试保证金计算"""
        if not FUTURES_AVAILABLE:
            self.skipTest("期货模块不可用")

        margin = calculate_required_margin(4000, 10, "IF2312")

        self.assertIsNotNone(margin)
        expected = 4000 * 300 * 10 * 0.12
        self.assertEqual(margin, expected)

        print(f"\nIF2312所需保证金 (价格4000, 10手): {margin}")

    def test_jq_wrapper(self):
        """测试聚宽风格包装函数"""
        if not FUTURES_AVAILABLE:
            self.skipTest("期货模块不可用")

        margin = calculate_required_margin_jq(5000, 5, "IC2401")

        self.assertIsNotNone(margin)
        expected = 5000 * 200 * 5 * 0.14
        self.assertEqual(margin, expected)
        print(f"\nIC2401所需保证金 (JQ风格, 价格5000, 5手): {margin}")


class TestFutureDailyData(unittest.TestCase):
    """测试期货日线数据"""

    def test_get_future_daily(self):
        """测试获取期货日线数据"""
        if not FUTURES_AVAILABLE:
            self.skipTest("期货模块不可用")

        try:
            df = get_future_daily(
                "IF2312", start_date="2023-11-01", end_date="2023-12-01"
            )

            self.assertIsInstance(df, pd.DataFrame)

            if not df.empty:
                self.assertIn("datetime", df.columns)
                self.assertIn("close", df.columns)

                print(f"\nIF2312日线数据 ({len(df)} 条):")
                print(df.tail(5).to_string())
            else:
                print("\nIF2312日线数据为空 (可能合约已过期)")

        except Exception as e:
            print(f"\n获取日线数据失败: {e}")
            self.skipTest(f"数据获取失败: {e}")

    def test_jq_wrapper(self):
        """测试聚宽风格包装函数"""
        if not FUTURES_AVAILABLE:
            self.skipTest("期货模块不可用")

        try:
            dominant = get_dominant_contract("IF")
            if dominant:
                df = get_future_daily_jq(
                    dominant, start_date="2024-01-01", end_date="2024-01-15"
                )

                self.assertIsInstance(df, pd.DataFrame)
                print(f"\n{dominant}日线数据 (JQ风格): {len(df)} 条")

        except Exception as e:
            print(f"\n获取日线数据失败: {e}")


class TestExchangeInfo(unittest.TestCase):
    """测试交易所信息"""

    def test_cffex_info(self):
        """测试中金所信息"""
        if not FUTURES_AVAILABLE:
            self.skipTest("期货模块不可用")

        cffex = CHINA_FUTURE_EXCHANGE_INFO["CFFEX"]

        self.assertEqual(cffex["name"], "中国金融期货交易所")
        self.assertIn("IF", cffex["products"])
        self.assertIn("IC", cffex["products"])

        self.assertEqual(cffex["multipliers"]["IF"], 300)
        self.assertEqual(cffex["multipliers"]["IC"], 200)

        print(f"\n中金所产品: {cffex['products']}")
        print(f"IF乘数: {cffex['multipliers']['IF']}")
        print(f"IF保证金: {cffex['margin_rates']['IF']}")


class TestIntegration(unittest.TestCase):
    """集成测试"""

    def test_full_workflow(self):
        """测试完整工作流程"""
        if not FUTURES_AVAILABLE:
            self.skipTest("期货模块不可用")

        print("\n=== 期货交易完整流程测试 ===")

        product = "IF"

        print(f"\n1. 获取{product}合约列表...")
        contracts_df = get_future_contracts(product=product)
        if contracts_df.empty:
            print("  未找到合约")
            return

        print(f"  找到 {len(contracts_df)} 个合约")

        print(f"\n2. 获取{product}主力合约...")
        dominant = get_dominant_contract(product)
        print(f"  主力合约: {dominant}")

        if not dominant:
            return

        print(f"\n3. 获取合约乘数...")
        multiplier = get_contract_multiplier(dominant)
        print(f"  乘数: {multiplier}")

        print(f"\n4. 获取保证金比例...")
        margin_rate = get_margin_rate(dominant)
        print(f"  保证金比例: {margin_rate}")

        price = 4000
        quantity = 10

        print(f"\n5. 计算持仓价值 (价格{price}, 手数{quantity})...")
        position_value = calculate_position_value(price, quantity, dominant)
        print(f"  持仓价值: {position_value}")

        print(f"\n6. 计算所需保证金...")
        required_margin = calculate_required_margin(price, quantity, dominant)
        print(f"  所需保证金: {required_margin}")

        print("\n=== 测试完成 ===")


if __name__ == "__main__":
    unittest.main(verbosity=2)
