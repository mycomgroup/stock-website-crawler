"""
test_subportfolios.py
测试资产路由和子账户模型
"""

import unittest
import backtrader as bt
import pandas as pd
from datetime import datetime

from jk2bt.core.strategy_base import JQ2BTBaseStrategy
from jk2bt.asset_router import (
    AssetType,
    AssetCategory,
    TradingStatus,
    AssetRouter,
    identify_asset,
    is_etf,
    is_stock,
    is_fund_of,
    is_future,
    is_index,
)
from jk2bt.strategy.subportfolios import (
    SubportfolioType,
    SubportfolioConfig,
    SubportfolioProxy,
    SubportfolioManager,
)


class TestAssetRouter(unittest.TestCase):
    def test_identify_stock_sh(self):
        info = identify_asset("600519.XSHG")
        self.assertEqual(info.asset_type, AssetType.STOCK)
        self.assertEqual(info.category, AssetCategory.EQUITY)
        self.assertTrue(info.is_supported())

    def test_identify_stock_sz(self):
        info = identify_asset("000001.XSHE")
        self.assertEqual(info.asset_type, AssetType.STOCK)
        self.assertEqual(info.category, AssetCategory.EQUITY)
        self.assertTrue(info.is_supported())

    def test_identify_etf_51(self):
        info = identify_asset("510300.XSHG")
        self.assertEqual(info.asset_type, AssetType.ETF)
        self.assertEqual(info.category, AssetCategory.FUND)
        self.assertTrue(info.is_supported())

    def test_identify_etf_15(self):
        info = identify_asset("159915.XSHE")
        self.assertIn(info.asset_type, [AssetType.ETF, AssetType.LOF])
        self.assertEqual(info.category, AssetCategory.FUND)
        self.assertTrue(info.is_supported())

    def test_identify_fund_of(self):
        info = identify_asset("000001.OF")
        self.assertEqual(info.asset_type, AssetType.FUND_OF)
        self.assertEqual(info.category, AssetCategory.FUND)
        self.assertTrue(info.is_identified_only())
        self.assertFalse(info.is_supported())

    def test_identify_future_ccfx(self):
        info = identify_asset("IF2312.CCFX")
        self.assertEqual(info.asset_type, AssetType.FUTURE_CCFX)
        self.assertEqual(info.category, AssetCategory.FUTURE)
        self.assertTrue(info.is_identified_only())
        self.assertFalse(info.is_supported())

    def test_identify_index(self):
        info = identify_asset("000300.XSHG")
        self.assertEqual(info.asset_type, AssetType.INDEX)
        self.assertEqual(info.category, AssetCategory.INDEX)
        self.assertTrue(info.is_identified_only())

    def test_identify_stock_with_prefix(self):
        info = identify_asset("sh600519")
        self.assertEqual(info.asset_type, AssetType.STOCK)
        self.assertEqual(info.exchange, "XSHG")

    def test_identify_stock_pure_code(self):
        info = identify_asset("600519")
        self.assertEqual(info.asset_type, AssetType.STOCK)
        self.assertEqual(info.normalized_code, "600519")

    def test_helper_functions(self):
        self.assertTrue(is_stock("600519.XSHG"))
        self.assertTrue(is_etf("510300.XSHG"))
        self.assertTrue(is_fund_of("000001.OF"))
        self.assertTrue(is_future("IF2312.CCFX"))
        self.assertTrue(is_index("000300.XSHG"))

    def test_group_by_type(self):
        router = AssetRouter()
        codes = ["600519.XSHG", "510300.XSHG", "000001.OF", "IF2312.CCFX"]
        groups = router.group_by_type(codes)
        self.assertEqual(len(groups.get(AssetType.STOCK, [])), 1)
        self.assertEqual(len(groups.get(AssetType.ETF, [])), 1)
        self.assertEqual(len(groups.get(AssetType.FUND_OF, [])), 1)
        self.assertEqual(len(groups.get(AssetType.FUTURE_CCFX, [])), 1)

    def test_identify_lof_16(self):
        info = identify_asset("160105.XSHE")
        self.assertEqual(info.asset_type, AssetType.LOF)
        self.assertEqual(info.category, AssetCategory.FUND)
        self.assertEqual(info.trading_status, TradingStatus.NETWORK_UNSTABLE)

    def test_identify_multiple_future_codes(self):
        codes = ["IF2312.CCFX", "IC2312.CCFX", "IH2312.CCFX", "IM2312.CCFX"]
        for code in codes:
            info = identify_asset(code)
            self.assertEqual(info.asset_type, AssetType.FUTURE_CCFX)
            self.assertEqual(info.exchange, "CCFX")

    def test_identify_etf_52(self):
        info = identify_asset("520030.XSHG")
        self.assertEqual(info.asset_type, AssetType.ETF)

    def test_identify_etf_50(self):
        info = identify_asset("501050.XSHG")
        self.assertEqual(info.asset_type, AssetType.ETF)

    def test_identify_unknown_code(self):
        info = identify_asset("XYZ123")
        self.assertEqual(info.asset_type, AssetType.UNKNOWN)
        self.assertEqual(info.category, AssetCategory.UNKNOWN)

    def test_identify_stock_3_prefix(self):
        info = identify_asset("300001.XSHE")
        self.assertEqual(info.asset_type, AssetType.STOCK)
        self.assertEqual(info.exchange, "XSHE")

    def test_identify_index_399(self):
        info = identify_asset("399006.XSHE")
        self.assertEqual(info.asset_type, AssetType.INDEX)
        self.assertEqual(info.exchange, "XSHE")

    def test_normalize_code_padding(self):
        info = identify_asset("519")
        self.assertEqual(info.normalized_code, "000519")

    def test_is_tradable(self):
        router = AssetRouter()
        self.assertTrue(router.is_tradable("600519.XSHG"))
        self.assertTrue(router.is_tradable("510300.XSHG"))
        self.assertFalse(router.is_tradable("000001.OF"))
        self.assertFalse(router.is_tradable("IF2312.CCFX"))

    def test_get_supported_assets(self):
        router = AssetRouter()
        codes = [
            "600519.XSHG",
            "510300.XSHG",
            "000001.OF",
            "IF2312.CCFX",
            "300001.XSHE",
        ]
        supported = router.get_supported_assets(codes)
        self.assertIn("600519.XSHG", supported)
        self.assertIn("510300.XSHG", supported)
        self.assertIn("300001.XSHE", supported)
        self.assertNotIn("000001.OF", supported)
        self.assertNotIn("IF2312.CCFX", supported)

    def test_cache_behavior(self):
        router = AssetRouter()
        info1 = router.identify("600519.XSHG")
        info2 = router.identify("600519.XSHG")
        self.assertIs(info1, info2)
        router.clear_cache()
        info3 = router.identify("600519.XSHG")
        self.assertIsNot(info1, info3)

    def test_add_custom_rule(self):
        router = AssetRouter()
        router.add_custom_rule("CUSTOM.*", AssetType.STOCK)
        self.assertEqual(len(router._custom_rules), 1)

    def test_metadata_set_get(self):
        info = identify_asset("600519.XSHG")
        info.set_metadata("test_key", "test_value")
        self.assertEqual(info.get_metadata("test_key"), "test_value")
        self.assertIsNone(info.get_metadata("nonexistent"))
        self.assertEqual(info.get_metadata("nonexistent", "default"), "default")

    def test_repr_string(self):
        info = identify_asset("600519.XSHG")
        repr_str = repr(info)
        self.assertIn("600519.XSHG", repr_str)
        self.assertIn("stock", repr_str)
        self.assertIn("supported", repr_str)

    def test_get_trading_status_desc(self):
        from jk2bt.asset_router import (
            get_trading_status_desc,
        )

        self.assertEqual(get_trading_status_desc("600519.XSHG"), "支持交易")
        self.assertEqual(get_trading_status_desc("000001.OF"), "已识别(暂不支持)")
        self.assertEqual(get_trading_status_desc("IF2312.CCFX"), "已识别(暂不支持)")

    def test_is_data_readable(self):
        from jk2bt.asset_router import is_data_readable

        self.assertTrue(is_data_readable("600519.XSHG"))
        self.assertTrue(is_data_readable("510300.XSHG"))
        self.assertTrue(is_data_readable("160105.XSHE"))
        self.assertFalse(is_data_readable("000001.OF"))
        self.assertFalse(is_data_readable("IF2312.CCFX"))

    def test_exchange_detection_no_suffix(self):
        info_sh = identify_asset("600519")
        self.assertEqual(info_sh.exchange, "XSHG")
        info_sz = identify_asset("000001")
        self.assertEqual(info_sz.exchange, "XSHE")

    def test_index_code_variants(self):
        index_codes = ["000016.XSHG", "000905.XSHG", "000852.XSHG", "000903.XSHG"]
        for code in index_codes:
            info = identify_asset(code)
            self.assertEqual(info.asset_type, AssetType.INDEX)


class TestSubportfolioCashAccount(unittest.TestCase):
    def test_initial_cash(self):
        from subportfolios import SubportfolioCashAccount

        account = SubportfolioCashAccount(10000.0, 0)
        self.assertEqual(account.cash, 10000.0)
        self.assertEqual(account.initial_cash, 10000.0)
        self.assertEqual(account.available_cash, 10000.0)

    def test_deposit(self):
        from subportfolios import SubportfolioCashAccount

        account = SubportfolioCashAccount(10000.0, 0)
        result = account.deposit(5000.0)
        self.assertTrue(result)
        self.assertEqual(account.cash, 15000.0)

    def test_deposit_negative_fail(self):
        from subportfolios import SubportfolioCashAccount

        account = SubportfolioCashAccount(10000.0, 0)
        result = account.deposit(-1000.0)
        self.assertFalse(result)
        self.assertEqual(account.cash, 10000.0)

    def test_deposit_zero(self):
        from subportfolios import SubportfolioCashAccount

        account = SubportfolioCashAccount(10000.0, 0)
        result = account.deposit(0.0)
        self.assertTrue(result)
        self.assertEqual(account.cash, 10000.0)

    def test_withdraw_success(self):
        from subportfolios import SubportfolioCashAccount

        account = SubportfolioCashAccount(10000.0, 0)
        result = account.withdraw(3000.0)
        self.assertTrue(result)
        self.assertEqual(account.cash, 7000.0)

    def test_withdraw_fail_negative(self):
        from subportfolios import SubportfolioCashAccount

        account = SubportfolioCashAccount(10000.0, 0)
        result = account.withdraw(-1000.0)
        self.assertFalse(result)
        self.assertEqual(account.cash, 10000.0)

    def test_withdraw_fail_insufficient(self):
        from subportfolios import SubportfolioCashAccount

        account = SubportfolioCashAccount(10000.0, 0)
        result = account.withdraw(15000.0)
        self.assertFalse(result)
        self.assertEqual(account.cash, 10000.0)

    def test_withdraw_allow_negative(self):
        from subportfolios import SubportfolioCashAccount

        account = SubportfolioCashAccount(10000.0, 0, allow_negative=True)
        result = account.withdraw(15000.0)
        self.assertTrue(result)
        self.assertEqual(account.cash, -5000.0)

    def test_transactions_log(self):
        from subportfolios import SubportfolioCashAccount

        account = SubportfolioCashAccount(10000.0, 0)
        account.deposit(5000.0, "test deposit")
        account.withdraw(3000.0, "test withdraw")
        transactions = account.get_transactions()
        self.assertEqual(len(transactions), 2)
        self.assertEqual(transactions[0]["type"], "deposit")
        self.assertEqual(transactions[1]["type"], "withdraw")

    def test_transactions_with_reason(self):
        from subportfolios import SubportfolioCashAccount

        account = SubportfolioCashAccount(10000.0, 0)
        account.deposit(5000.0, "initial allocation")
        account.withdraw(3000.0, "buy stock")
        transactions = account.get_transactions()
        self.assertEqual(transactions[0]["reason"], "initial allocation")
        self.assertEqual(transactions[1]["reason"], "buy stock")

    def test_multiple_transactions(self):
        from subportfolios import SubportfolioCashAccount

        account = SubportfolioCashAccount(10000.0, 0)
        for i in range(5):
            account.deposit(1000.0)
            account.withdraw(500.0)
        transactions = account.get_transactions()
        self.assertEqual(len(transactions), 10)
        expected_cash = 10000.0 + 5 * 1000.0 - 5 * 500.0
        self.assertEqual(account.cash, expected_cash)

    def test_reset_to_initial(self):
        from subportfolios import SubportfolioCashAccount

        account = SubportfolioCashAccount(10000.0, 0)
        account.deposit(5000.0)
        account.withdraw(3000.0)
        account.reset()
        self.assertEqual(account.cash, 10000.0)
        self.assertEqual(len(account.get_transactions()), 0)

    def test_reset_to_new_value(self):
        from subportfolios import SubportfolioCashAccount

        account = SubportfolioCashAccount(10000.0, 0)
        account.deposit(5000.0)
        account.reset(20000.0)
        self.assertEqual(account.cash, 20000.0)
        self.assertEqual(account.initial_cash, 10000.0)
        self.assertEqual(len(account.get_transactions()), 0)

    def test_transaction_balance_recorded(self):
        from subportfolios import SubportfolioCashAccount

        account = SubportfolioCashAccount(10000.0, 0)
        account.deposit(5000.0)
        transactions = account.get_transactions()
        self.assertEqual(transactions[0]["balance_after"], 15000.0)


class TestSubportfolioProxy(unittest.TestCase):
    def test_basic_properties(self):
        config = SubportfolioConfig(
            name="test_sp",
            type=SubportfolioType.STOCK,
            initial_cash=50000.0,
        )
        sp = SubportfolioProxy(config, 0)
        self.assertEqual(sp.name, "test_sp")
        self.assertEqual(sp.cash, 50000.0)
        self.assertEqual(sp.total_value, 50000.0)
        self.assertEqual(sp.id, 0)
        self.assertEqual(sp.type, SubportfolioType.STOCK)

    def test_add_position(self):
        config = SubportfolioConfig(
            name="test_sp",
            type=SubportfolioType.STOCK,
            initial_cash=100000.0,
        )
        sp = SubportfolioProxy(config, 0)
        sp.add_position("600519.XSHG", 100, 100.0)
        self.assertEqual(len(sp.positions), 1)
        self.assertEqual(sp.positions_value, 10000.0)
        self.assertEqual(sp.total_value, 110000.0)

    def test_add_position_accumulate(self):
        config = SubportfolioConfig(
            name="test_sp",
            type=SubportfolioType.STOCK,
            initial_cash=100000.0,
        )
        sp = SubportfolioProxy(config, 0)
        sp.add_position("600519.XSHG", 100, 100.0)
        sp.add_position("600519.XSHG", 50, 120.0)
        pos = sp.positions.get("600519.XSHG")
        self.assertEqual(pos.size, 150)
        avg_price = (100 * 100 + 50 * 120) / 150
        self.assertAlmostEqual(pos.price, avg_price, places=2)

    def test_deposit_withdraw(self):
        config = SubportfolioConfig(
            name="test_sp",
            type=SubportfolioType.STOCK,
            initial_cash=50000.0,
        )
        sp = SubportfolioProxy(config, 0)
        sp.deposit_cash(10000.0)
        self.assertEqual(sp.cash, 60000.0)
        sp.withdraw_cash(5000.0)
        self.assertEqual(sp.cash, 55000.0)

    def test_update_position_price(self):
        config = SubportfolioConfig(
            name="test_sp",
            type=SubportfolioType.STOCK,
            initial_cash=100000.0,
        )
        sp = SubportfolioProxy(config, 0)
        sp.add_position("600519.XSHG", 100, 100.0)
        sp.update_position_price("600519.XSHG", 120.0)
        pos = sp.positions.get("600519.XSHG")
        self.assertEqual(pos.price, 120.0)
        self.assertEqual(pos.value, 12000.0)
        self.assertEqual(sp.positions_value, 12000.0)

    def test_remove_position(self):
        config = SubportfolioConfig(
            name="test_sp",
            type=SubportfolioType.STOCK,
            initial_cash=100000.0,
        )
        sp = SubportfolioProxy(config, 0)
        sp.add_position("600519.XSHG", 100, 100.0)
        sp.add_position("000001.XSHE", 200, 50.0)
        sp.remove_position("600519.XSHG")
        self.assertEqual(len(sp.positions), 1)
        self.assertNotIn("600519.XSHG", sp.positions)
        self.assertEqual(sp.positions_value, 10000.0)

    def test_add_position_reduce_to_zero(self):
        config = SubportfolioConfig(
            name="test_sp",
            type=SubportfolioType.STOCK,
            initial_cash=100000.0,
        )
        sp = SubportfolioProxy(config, 0)
        sp.add_position("600519.XSHG", 100, 100.0)
        sp.add_position("600519.XSHG", -100, 120.0)
        self.assertEqual(len(sp.positions), 0)
        self.assertEqual(sp.positions_value, 0)

    def test_returns_positive(self):
        config = SubportfolioConfig(
            name="test_sp",
            type=SubportfolioType.STOCK,
            initial_cash=100000.0,
        )
        sp = SubportfolioProxy(config, 0)
        sp.add_position("600519.XSHG", 100, 100.0)
        sp.update_position_price("600519.XSHG", 120.0)
        expected_returns = (100000.0 + 12000.0) / 100000.0 - 1
        self.assertAlmostEqual(sp.returns, expected_returns, places=4)

    def test_returns_zero_initial_cash(self):
        config = SubportfolioConfig(
            name="test_sp",
            type=SubportfolioType.STOCK,
            initial_cash=0.0,
        )
        sp = SubportfolioProxy(config, 0)
        sp.deposit_cash(10000.0)
        self.assertEqual(sp.returns, 0.0)

    def test_multiple_positions(self):
        config = SubportfolioConfig(
            name="test_sp",
            type=SubportfolioType.STOCK,
            initial_cash=100000.0,
        )
        sp = SubportfolioProxy(config, 0)
        sp.add_position("600519.XSHG", 100, 100.0)
        sp.add_position("000001.XSHE", 200, 50.0)
        sp.add_position("300001.XSHE", 50, 200.0)
        self.assertEqual(len(sp.positions), 3)
        self.assertEqual(sp.positions_value, 10000.0 + 10000.0 + 10000.0)

    def test_can_trade_default(self):
        config = SubportfolioConfig(
            name="test_sp",
            type=SubportfolioType.STOCK,
            initial_cash=100000.0,
        )
        sp = SubportfolioProxy(config, 0)
        self.assertTrue(sp.can_trade("600519.XSHG"))
        self.assertTrue(sp.can_trade("000001.XSHE"))

    def test_can_trade_with_filter(self):
        def stock_filter(code):
            return code.startswith("6")

        config = SubportfolioConfig(
            name="test_sp",
            type=SubportfolioType.STOCK,
            initial_cash=100000.0,
            asset_filter=stock_filter,
        )
        sp = SubportfolioProxy(config, 0)
        self.assertTrue(sp.can_trade("600519.XSHG"))
        self.assertFalse(sp.can_trade("000001.XSHE"))

    def test_reset_cash(self):
        config = SubportfolioConfig(
            name="test_sp",
            type=SubportfolioType.STOCK,
            initial_cash=100000.0,
        )
        sp = SubportfolioProxy(config, 0)
        sp.add_position("600519.XSHG", 100, 100.0)
        sp.deposit_cash(5000.0)
        sp.reset_cash(50000.0)
        self.assertEqual(sp.cash, 50000.0)
        self.assertEqual(len(sp.positions), 0)

    def test_available_cash(self):
        config = SubportfolioConfig(
            name="test_sp",
            type=SubportfolioType.STOCK,
            initial_cash=100000.0,
        )
        sp = SubportfolioProxy(config, 0)
        self.assertEqual(sp.available_cash, 100000.0)
        sp.withdraw_cash(30000.0)
        self.assertEqual(sp.available_cash, 70000.0)

    def test_repr_string(self):
        config = SubportfolioConfig(
            name="test_sp",
            type=SubportfolioType.STOCK,
            initial_cash=100000.0,
        )
        sp = SubportfolioProxy(config, 0)
        repr_str = repr(sp)
        self.assertIn("test_sp", repr_str)
        self.assertIn("id=0", repr_str)

    def test_transactions_from_proxy(self):
        config = SubportfolioConfig(
            name="test_sp",
            type=SubportfolioType.STOCK,
            initial_cash=100000.0,
        )
        sp = SubportfolioProxy(config, 0)
        sp.deposit_cash(10000.0, "test")
        sp.withdraw_cash(5000.0, "trade")
        transactions = sp.get_transactions()
        self.assertEqual(len(transactions), 2)


class TestSubportfolioManager(unittest.TestCase):
    def test_set_subportfolios(self):
        manager = SubportfolioManager()
        manager.initialize(100000.0)
        configs = [
            SubportfolioConfig(
                name="股票账户", type=SubportfolioType.STOCK, initial_cash=30000.0
            ),
            SubportfolioConfig(
                name="ETF账户", type=SubportfolioType.ETF, initial_cash=20000.0
            ),
        ]
        sp_list = manager.set_subportfolios(configs)
        self.assertEqual(len(sp_list), 2)
        self.assertEqual(sp_list[0].name, "股票账户")
        self.assertEqual(sp_list[1].name, "ETF账户")

    def test_get_subportfolio(self):
        manager = SubportfolioManager()
        manager.initialize(100000.0)
        configs = [
            SubportfolioConfig(
                name="sp1", type=SubportfolioType.STOCK, initial_cash=30000.0
            ),
        ]
        manager.set_subportfolios(configs)
        sp = manager.get_subportfolio(0)
        self.assertIsNotNone(sp)
        self.assertEqual(sp.name, "sp1")
        self.assertIsNone(manager.get_subportfolio(10))

    def test_transfer_cash(self):
        manager = SubportfolioManager()
        manager.initialize(100000.0)
        configs = [
            SubportfolioConfig(
                name="sp1", type=SubportfolioType.STOCK, initial_cash=50000.0
            ),
            SubportfolioConfig(
                name="sp2", type=SubportfolioType.ETF, initial_cash=30000.0
            ),
        ]
        manager.set_subportfolios(configs)
        result = manager.transfer_cash(0, 1, 10000.0)
        self.assertTrue(result)
        self.assertEqual(manager.subportfolios[0].cash, 40000.0)
        self.assertEqual(manager.subportfolios[1].cash, 40000.0)

    def test_transfer_cash_fail_insufficient(self):
        manager = SubportfolioManager()
        manager.initialize(100000.0)
        configs = [
            SubportfolioConfig(
                name="sp1", type=SubportfolioType.STOCK, initial_cash=5000.0
            ),
            SubportfolioConfig(
                name="sp2", type=SubportfolioType.ETF, initial_cash=30000.0
            ),
        ]
        manager.set_subportfolios(configs)
        result = manager.transfer_cash(0, 1, 10000.0)
        self.assertFalse(result)
        self.assertEqual(manager.subportfolios[0].cash, 5000.0)
        self.assertEqual(manager.subportfolios[1].cash, 30000.0)

    def test_transfer_from_main(self):
        manager = SubportfolioManager()
        manager.initialize(100000.0)
        configs = [
            SubportfolioConfig(
                name="sp1", type=SubportfolioType.STOCK, initial_cash=0.0
            ),
        ]
        manager.set_subportfolios(configs)
        result = manager.transfer_from_main(0, 20000.0)
        self.assertTrue(result)
        self.assertEqual(manager.main_cash, 80000.0)
        self.assertEqual(manager.subportfolios[0].cash, 20000.0)

    def test_get_summary(self):
        manager = SubportfolioManager()
        manager.initialize(100000.0)
        configs = [
            SubportfolioConfig(
                name="sp1", type=SubportfolioType.STOCK, initial_cash=30000.0
            ),
        ]
        manager.set_subportfolios(configs)
        summary = manager.get_summary()
        self.assertEqual(summary["main_cash"], 100000.0)
        self.assertEqual(len(summary["subportfolios"]), 1)
        self.assertEqual(summary["subportfolios"][0]["cash"], 30000.0)

    def test_add_subportfolio(self):
        manager = SubportfolioManager()
        manager.initialize(100000.0)
        configs = [
            SubportfolioConfig(
                name="sp1", type=SubportfolioType.STOCK, initial_cash=30000.0
            ),
        ]
        manager.set_subportfolios(configs)
        new_config = SubportfolioConfig(
            name="sp2", type=SubportfolioType.ETF, initial_cash=20000.0
        )
        new_sp = manager.add_subportfolio(new_config)
        self.assertEqual(len(manager.subportfolios), 2)
        self.assertEqual(new_sp.name, "sp2")
        self.assertEqual(new_sp.id, 1)

    def test_get_subportfolio_by_name(self):
        manager = SubportfolioManager()
        manager.initialize(100000.0)
        configs = [
            SubportfolioConfig(
                name="股票账户", type=SubportfolioType.STOCK, initial_cash=30000.0
            ),
            SubportfolioConfig(
                name="ETF账户", type=SubportfolioType.ETF, initial_cash=20000.0
            ),
        ]
        manager.set_subportfolios(configs)
        sp = manager.get_subportfolio_by_name("股票账户")
        self.assertIsNotNone(sp)
        self.assertEqual(sp.name, "股票账户")
        self.assertIsNone(manager.get_subportfolio_by_name("不存在"))

    def test_transfer_to_main(self):
        manager = SubportfolioManager()
        manager.initialize(100000.0)
        configs = [
            SubportfolioConfig(
                name="sp1", type=SubportfolioType.STOCK, initial_cash=50000.0
            ),
        ]
        manager.set_subportfolios(configs)
        result = manager.transfer_to_main(0, 10000.0)
        self.assertTrue(result)
        self.assertEqual(manager.main_cash, 110000.0)
        self.assertEqual(manager.subportfolios[0].cash, 40000.0)

    def test_transfer_to_main_insufficient(self):
        manager = SubportfolioManager()
        manager.initialize(100000.0)
        configs = [
            SubportfolioConfig(
                name="sp1", type=SubportfolioType.STOCK, initial_cash=5000.0
            ),
        ]
        manager.set_subportfolios(configs)
        result = manager.transfer_to_main(0, 10000.0)
        self.assertFalse(result)
        self.assertEqual(manager.main_cash, 100000.0)
        self.assertEqual(manager.subportfolios[0].cash, 5000.0)

    def test_transfer_cash_zero_amount(self):
        manager = SubportfolioManager()
        manager.initialize(100000.0)
        configs = [
            SubportfolioConfig(
                name="sp1", type=SubportfolioType.STOCK, initial_cash=50000.0
            ),
            SubportfolioConfig(
                name="sp2", type=SubportfolioType.ETF, initial_cash=30000.0
            ),
        ]
        manager.set_subportfolios(configs)
        result = manager.transfer_cash(0, 1, 0.0)
        self.assertFalse(result)

    def test_transfer_cash_negative_amount(self):
        manager = SubportfolioManager()
        manager.initialize(100000.0)
        configs = [
            SubportfolioConfig(
                name="sp1", type=SubportfolioType.STOCK, initial_cash=50000.0
            ),
            SubportfolioConfig(
                name="sp2", type=SubportfolioType.ETF, initial_cash=30000.0
            ),
        ]
        manager.set_subportfolios(configs)
        result = manager.transfer_cash(0, 1, -1000.0)
        self.assertFalse(result)

    def test_transfer_cash_invalid_indices(self):
        manager = SubportfolioManager()
        manager.initialize(100000.0)
        configs = [
            SubportfolioConfig(
                name="sp1", type=SubportfolioType.STOCK, initial_cash=50000.0
            ),
        ]
        manager.set_subportfolios(configs)
        result = manager.transfer_cash(0, 10, 1000.0)
        self.assertFalse(result)
        result = manager.transfer_cash(10, 0, 1000.0)
        self.assertFalse(result)

    def test_total_cash(self):
        manager = SubportfolioManager()
        manager.initialize(100000.0)
        configs = [
            SubportfolioConfig(
                name="sp1", type=SubportfolioType.STOCK, initial_cash=50000.0
            ),
            SubportfolioConfig(
                name="sp2", type=SubportfolioType.ETF, initial_cash=30000.0
            ),
        ]
        manager.set_subportfolios(configs)
        self.assertEqual(manager.total_cash, 100000.0 + 50000.0 + 30000.0)

    def test_get_total_value(self):
        manager = SubportfolioManager()
        manager.initialize(100000.0)
        configs = [
            SubportfolioConfig(
                name="sp1", type=SubportfolioType.STOCK, initial_cash=50000.0
            ),
        ]
        manager.set_subportfolios(configs)
        manager.subportfolios[0].add_position("600519.XSHG", 100, 100.0)
        total = manager.get_total_value()
        self.assertEqual(total, 100000.0 + 50000.0 + 10000.0)

    def test_reset_all(self):
        manager = SubportfolioManager()
        manager.initialize(100000.0)
        configs = [
            SubportfolioConfig(
                name="sp1", type=SubportfolioType.STOCK, initial_cash=50000.0
            ),
        ]
        manager.set_subportfolios(configs)
        manager.transfer_from_main(0, 10000.0)
        manager.subportfolios[0].add_position("600519.XSHG", 100, 100.0)
        manager.reset_all()
        self.assertEqual(manager.main_cash, 100000.0)
        self.assertEqual(manager.subportfolios[0].cash, 50000.0)
        self.assertEqual(len(manager.subportfolios[0].positions), 0)

    def test_getitem_access(self):
        manager = SubportfolioManager()
        manager.initialize(100000.0)
        configs = [
            SubportfolioConfig(
                name="sp1", type=SubportfolioType.STOCK, initial_cash=30000.0
            ),
            SubportfolioConfig(
                name="sp2", type=SubportfolioType.ETF, initial_cash=20000.0
            ),
        ]
        manager.set_subportfolios(configs)
        sp0 = manager[0]
        sp1 = manager[1]
        self.assertEqual(sp0.name, "sp1")
        self.assertEqual(sp1.name, "sp2")

    def test_len_method(self):
        manager = SubportfolioManager()
        manager.initialize(100000.0)
        self.assertEqual(len(manager), 0)
        configs = [
            SubportfolioConfig(
                name="sp1", type=SubportfolioType.STOCK, initial_cash=30000.0
            ),
        ]
        manager.set_subportfolios(configs)
        self.assertEqual(len(manager), 1)

    def test_repr_string(self):
        manager = SubportfolioManager()
        manager.initialize(100000.0)
        repr_str = repr(manager)
        self.assertIn("count=0", repr_str)
        self.assertIn("main_cash=100000", repr_str)

    def test_initialize_twice(self):
        manager = SubportfolioManager()
        manager.initialize(100000.0)
        manager.initialize(200000.0)
        self.assertEqual(manager.main_cash, 100000.0)

    def test_main_cash_before_initialize(self):
        manager = SubportfolioManager()
        self.assertEqual(manager.main_cash, 0.0)

    def test_transfer_from_main_before_initialize(self):
        manager = SubportfolioManager()
        result = manager.transfer_from_main(0, 1000.0)
        self.assertFalse(result)

    def test_summary_returns_field(self):
        manager = SubportfolioManager()
        manager.initialize(100000.0)
        configs = [
            SubportfolioConfig(
                name="sp1", type=SubportfolioType.STOCK, initial_cash=100000.0
            ),
        ]
        manager.set_subportfolios(configs)
        manager.subportfolios[0].add_position("600519.XSHG", 100, 100.0)
        manager.subportfolios[0].update_position_price("600519.XSHG", 110.0)
        summary = manager.get_summary()
        self.assertIn("returns", summary["subportfolios"][0])
        expected_returns = (100000.0 + 11000.0) / 100000.0 - 1
        self.assertAlmostEqual(
            summary["subportfolios"][0]["returns"], expected_returns, places=4
        )


class TestContextProxySubportfolios(unittest.TestCase):
    def test_context_subportfolios_default(self):
        cerebro = bt.Cerebro()
        cerebro.broker.setcash(100000.0)

        df = pd.DataFrame(
            {
                "open": [10.0] * 5,
                "high": [10.5] * 5,
                "low": [9.5] * 5,
                "close": [10.0] * 5,
                "volume": [1000] * 5,
                "openinterest": [0] * 5,
            },
            index=pd.date_range("2023-01-01", periods=5),
        )
        data = bt.feeds.PandasData(dataname=df, name="test_stock")
        cerebro.adddata(data)

        class TestStrategy(JQ2BTBaseStrategy):
            def __init__(self):
                super().__init__()
                self.test_results = {}

            def next(self):
                super().next()
                self.test_results["subportfolios_count"] = len(
                    self.context.subportfolios
                )

        cerebro.addstrategy(TestStrategy)
        results = cerebro.run()
        strategy = results[0]
        self.assertEqual(strategy.test_results["subportfolios_count"], 1)

    def test_context_set_subportfolios(self):
        cerebro = bt.Cerebro()
        cerebro.broker.setcash(100000.0)

        df = pd.DataFrame(
            {
                "open": [10.0] * 5,
                "high": [10.5] * 5,
                "low": [9.5] * 5,
                "close": [10.0] * 5,
                "volume": [1000] * 5,
                "openinterest": [0] * 5,
            },
            index=pd.date_range("2023-01-01", periods=5),
        )
        data = bt.feeds.PandasData(dataname=df, name="test_stock")
        cerebro.adddata(data)

        class TestStrategy(JQ2BTBaseStrategy):
            def initialize(self):
                configs = [
                    {"name": "股票账户", "type": "stock", "initial_cash": 40000.0},
                    {"name": "ETF账户", "type": "etf", "initial_cash": 30000.0},
                ]
                self.context.set_subportfolios(configs)

            def __init__(self):
                super().__init__()
                self.test_results = {}

            def next(self):
                super().next()
                if len(self) == 2:
                    self.test_results["sp_count"] = len(self.context.subportfolios)
                    self.test_results["sp0_cash"] = self.context.subportfolios[0].cash
                    self.test_results["sp1_cash"] = self.context.subportfolios[1].cash

        cerebro.addstrategy(TestStrategy)
        results = cerebro.run()
        strategy = results[0]
        self.assertEqual(strategy.test_results["sp_count"], 2)
        self.assertEqual(strategy.test_results["sp0_cash"], 40000.0)
        self.assertEqual(strategy.test_results["sp1_cash"], 30000.0)

    def test_context_transfer_cash(self):
        cerebro = bt.Cerebro()
        cerebro.broker.setcash(100000.0)

        df = pd.DataFrame(
            {
                "open": [10.0] * 5,
                "high": [10.5] * 5,
                "low": [9.5] * 5,
                "close": [10.0] * 5,
                "volume": [1000] * 5,
                "openinterest": [0] * 5,
            },
            index=pd.date_range("2023-01-01", periods=5),
        )
        data = bt.feeds.PandasData(dataname=df, name="test_stock")
        cerebro.adddata(data)

        class TestStrategy(JQ2BTBaseStrategy):
            def initialize(self):
                configs = [
                    {"name": "sp0", "type": "stock", "initial_cash": 50000.0},
                    {"name": "sp1", "type": "etf", "initial_cash": 30000.0},
                ]
                self.context.set_subportfolios(configs)

            def __init__(self):
                super().__init__()
                self.test_results = {}

            def next(self):
                super().next()
                if len(self) == 2:
                    result = self.context.transfer_cash(0, 1, 10000.0)
                    self.test_results["transfer_result"] = result
                    self.test_results["sp0_after"] = self.context.subportfolios[0].cash
                    self.test_results["sp1_after"] = self.context.subportfolios[1].cash

        cerebro.addstrategy(TestStrategy)
        results = cerebro.run()
        strategy = results[0]
        self.assertTrue(strategy.test_results["transfer_result"])
        self.assertEqual(strategy.test_results["sp0_after"], 40000.0)
        self.assertEqual(strategy.test_results["sp1_after"], 40000.0)

    def test_context_cash_view_distinct(self):
        cerebro = bt.Cerebro()
        cerebro.broker.setcash(100000.0)

        df = pd.DataFrame(
            {
                "open": [10.0] * 5,
                "high": [10.5] * 5,
                "low": [9.5] * 5,
                "close": [10.0] * 5,
                "volume": [1000] * 5,
                "openinterest": [0] * 5,
            },
            index=pd.date_range("2023-01-01", periods=5),
        )
        data = bt.feeds.PandasData(dataname=df, name="test_stock")
        cerebro.adddata(data)

        class TestStrategy(JQ2BTBaseStrategy):
            def initialize(self):
                configs = [
                    {"name": "sp0", "type": "stock", "initial_cash": 40000.0},
                    {"name": "sp1", "type": "etf", "initial_cash": 30000.0},
                ]
                self.context.set_subportfolios(configs)

            def __init__(self):
                super().__init__()
                self.test_results = {}

            def next(self):
                super().next()
                if len(self) == 2:
                    self.test_results["sp0_cash_is_independent"] = (
                        self.context.subportfolios[0].cash == 40000.0
                    )
                    self.test_results["sp1_cash_is_independent"] = (
                        self.context.subportfolios[1].cash == 30000.0
                    )
                    self.test_results["main_cash_different"] = (
                        self.context.portfolio.cash
                        != self.context.subportfolios[0].cash
                    )

        cerebro.addstrategy(TestStrategy)
        results = cerebro.run()
        strategy = results[0]
        self.assertTrue(strategy.test_results["sp0_cash_is_independent"])
        self.assertTrue(strategy.test_results["sp1_cash_is_independent"])
        self.assertTrue(strategy.test_results["main_cash_different"])

    def test_context_get_subportfolio_by_name(self):
        cerebro = bt.Cerebro()
        cerebro.broker.setcash(100000.0)

        df = pd.DataFrame(
            {
                "open": [10.0] * 5,
                "high": [10.5] * 5,
                "low": [9.5] * 5,
                "close": [10.0] * 5,
                "volume": [1000] * 5,
                "openinterest": [0] * 5,
            },
            index=pd.date_range("2023-01-01", periods=5),
        )
        data = bt.feeds.PandasData(dataname=df, name="test_stock")
        cerebro.adddata(data)

        class TestStrategy(JQ2BTBaseStrategy):
            def initialize(self):
                configs = [
                    {"name": "股票账户", "type": "stock", "initial_cash": 40000.0},
                    {"name": "ETF账户", "type": "etf", "initial_cash": 30000.0},
                ]
                self.context.set_subportfolios(configs)

            def __init__(self):
                super().__init__()
                self.test_results = {}

            def next(self):
                super().next()
                if len(self) == 2:
                    sp = self.context.get_subportfolio_by_name("股票账户")
                    self.test_results["found_sp"] = sp is not None
                    self.test_results["sp_name"] = sp.name if sp else None
                    not_found = self.context.get_subportfolio_by_name("不存在")
                    self.test_results["not_found"] = not_found is None

        cerebro.addstrategy(TestStrategy)
        results = cerebro.run()
        strategy = results[0]
        self.assertTrue(strategy.test_results["found_sp"])
        self.assertEqual(strategy.test_results["sp_name"], "股票账户")
        self.assertTrue(strategy.test_results["not_found"])

    def test_context_transfer_to_main(self):
        cerebro = bt.Cerebro()
        cerebro.broker.setcash(100000.0)

        df = pd.DataFrame(
            {
                "open": [10.0] * 5,
                "high": [10.5] * 5,
                "low": [9.5] * 5,
                "close": [10.0] * 5,
                "volume": [1000] * 5,
                "openinterest": [0] * 5,
            },
            index=pd.date_range("2023-01-01", periods=5),
        )
        data = bt.feeds.PandasData(dataname=df, name="test_stock")
        cerebro.adddata(data)

        class TestStrategy(JQ2BTBaseStrategy):
            def initialize(self):
                configs = [
                    {"name": "sp0", "type": "stock", "initial_cash": 50000.0},
                ]
                self.context.set_subportfolios(configs)

            def __init__(self):
                super().__init__()
                self.test_results = {}

            def next(self):
                super().next()
                if len(self) == 2:
                    result = self.context.transfer_to_main(0, 10000.0)
                    self.test_results["transfer_result"] = result
                    self.test_results["sp0_after"] = self.context.subportfolios[0].cash

        cerebro.addstrategy(TestStrategy)
        results = cerebro.run()
        strategy = results[0]
        self.assertTrue(strategy.test_results["transfer_result"])
        self.assertEqual(strategy.test_results["sp0_after"], 40000.0)

    def test_context_summary(self):
        cerebro = bt.Cerebro()
        cerebro.broker.setcash(100000.0)

        df = pd.DataFrame(
            {
                "open": [10.0] * 5,
                "high": [10.5] * 5,
                "low": [9.5] * 5,
                "close": [10.0] * 5,
                "volume": [1000] * 5,
                "openinterest": [0] * 5,
            },
            index=pd.date_range("2023-01-01", periods=5),
        )
        data = bt.feeds.PandasData(dataname=df, name="test_stock")
        cerebro.adddata(data)

        class TestStrategy(JQ2BTBaseStrategy):
            def initialize(self):
                configs = [
                    {"name": "sp0", "type": "stock", "initial_cash": 40000.0},
                    {"name": "sp1", "type": "etf", "initial_cash": 30000.0},
                ]
                self.context.set_subportfolios(configs)

            def __init__(self):
                super().__init__()
                self.test_results = {}

            def next(self):
                super().next()
                if len(self) == 2:
                    summary = self.context.get_subportfolio_summary()
                    self.test_results["main_cash"] = summary["main_cash"]
                    self.test_results["sp_count"] = len(summary["subportfolios"])
                    self.test_results["total_value"] = summary["total_value"]

        cerebro.addstrategy(TestStrategy)
        results = cerebro.run()
        strategy = results[0]
        self.assertEqual(strategy.test_results["main_cash"], 100000.0)
        self.assertEqual(strategy.test_results["sp_count"], 2)
        self.assertEqual(strategy.test_results["total_value"], 170000.0)

    def test_context_add_subportfolio(self):
        cerebro = bt.Cerebro()
        cerebro.broker.setcash(100000.0)

        df = pd.DataFrame(
            {
                "open": [10.0] * 5,
                "high": [10.5] * 5,
                "low": [9.5] * 5,
                "close": [10.0] * 5,
                "volume": [1000] * 5,
                "openinterest": [0] * 5,
            },
            index=pd.date_range("2023-01-01", periods=5),
        )
        data = bt.feeds.PandasData(dataname=df, name="test_stock")
        cerebro.adddata(data)

        class TestStrategy(JQ2BTBaseStrategy):
            def initialize(self):
                configs = [
                    {"name": "sp0", "type": "stock", "initial_cash": 40000.0},
                ]
                self.context.set_subportfolios(configs)
                new_config = {"name": "sp1", "type": "etf", "initial_cash": 20000.0}
                self.context.add_subportfolio(new_config)

            def __init__(self):
                super().__init__()
                self.test_results = {}

            def next(self):
                super().next()
                if len(self) == 2:
                    self.test_results["sp_count"] = len(self.context.subportfolios)
                    self.test_results["sp1_name"] = self.context.subportfolios[1].name

        cerebro.addstrategy(TestStrategy)
        results = cerebro.run()
        strategy = results[0]
        self.assertEqual(strategy.test_results["sp_count"], 2)
        self.assertEqual(strategy.test_results["sp1_name"], "sp1")


if __name__ == "__main__":
    unittest.main()
