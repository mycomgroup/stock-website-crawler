import unittest
import backtrader as bt
import pandas as pd
from datetime import datetime

from jk2bt.core.strategy_base import (
    JQ2BTBaseStrategy,
    jq_code_to_ak,
    set_current_strategy,
)


def create_mock_data(name, price=100.0, dates=None):
    if dates is None:
        dates = pd.date_range("2024-01-01", periods=10)
    df = pd.DataFrame(
        {
            "datetime": dates,
            "open": [price] * len(dates),
            "high": [price * 1.02] * len(dates),
            "low": [price * 0.98] * len(dates),
            "close": [price] * len(dates),
            "volume": [10000] * len(dates),
            "openinterest": [0] * len(dates),
        }
    )
    data = bt.feeds.PandasData(dataname=df.set_index("datetime"), name=name)
    return data


class TestGetDataByName(unittest.TestCase):
    def test_jq_format(self):
        self.assertEqual(jq_code_to_ak("600519.XSHG"), "sh600519")
        self.assertEqual(jq_code_to_ak("000001.XSHE"), "sz000001")

    def test_ak_format(self):
        self.assertEqual(jq_code_to_ak("sh600519"), "sh600519")
        self.assertEqual(jq_code_to_ak("sz000001"), "sz000001")

    def test_pure_code(self):
        self.assertEqual(jq_code_to_ak("600519"), "sh600519")
        self.assertEqual(jq_code_to_ak("000001"), "sz000001")


class TestStrategyOrderBuy(JQ2BTBaseStrategy):
    def initialize(self):
        self.orders = []
        self.run_daily(self._test_buy, time_str="after_close")

    def _test_buy(self, context):
        if len(self.orders) == 0:
            data = self.datas[0]
            data_name = data._name

            self.orders.append(self.order_target(data_name, 100))
            self.orders.append(self.order_value(data_name, 10000))
            self.orders.append(self.order_target_value(data_name, 5000))
            self.orders.append(self.order_target_percent(data, 0.1))
            self.orders.append(self.order(data_name, 50))
            self.orders.append(self._get_data_by_name(data_name))


class TestStrategyOrderSell(JQ2BTBaseStrategy):
    def initialize(self):
        self.orders = []
        self.run_daily(self._test_sell, time_str="after_close")

    def _test_sell(self, context):
        if len(self.orders) == 0:
            data = self.datas[0]
            data_name = data._name

            self.orders.append(self.order(data_name, -50))


class TestStrategyInvalid(JQ2BTBaseStrategy):
    def initialize(self):
        self.orders = []
        self.run_daily(self._test_invalid, time_str="after_close")

    def _test_invalid(self, context):
        if len(self.orders) == 0:
            self.orders.append(self.order_target("999999.XSHG", 100))
            self.orders.append(self.order("999999.XSHG", 100))
            self.orders.append(self.order_target_percent(self.datas[0], 1.5))
            self.orders.append(self.order_target_percent(self.datas[0], -0.1))
            self.orders.append(self.order_value("999999.XSHG", 10000))
            self.orders.append(self._get_data_by_name("999999.XSHG"))


class TestOrderFunctionsIntegrated(unittest.TestCase):
    def test_order_buy_functions(self):
        cerebro = bt.Cerebro()
        cerebro.broker.setcash(1000000)
        cerebro.adddata(create_mock_data("sh600519", price=100.0))
        cerebro.addstrategy(TestStrategyOrderBuy, printlog=False)
        results = cerebro.run()
        strat = results[0]

        for i in range(5):
            self.assertIsNotNone(strat.orders[i], f"order function {i} returned None")
        self.assertIsNotNone(strat.orders[5], "_get_data_by_name returned None")

    def test_order_sell_functions(self):
        cerebro = bt.Cerebro()
        cerebro.broker.setcash(1000000)
        cerebro.adddata(create_mock_data("sh600519", price=100.0))
        cerebro.addstrategy(TestStrategyOrderSell, printlog=False)
        results = cerebro.run()
        strat = results[0]

        self.assertIsNotNone(strat.orders[0], "order sell returned None")

    def test_order_invalid_functions(self):
        cerebro = bt.Cerebro()
        cerebro.broker.setcash(1000000)
        cerebro.adddata(create_mock_data("sh600519", price=100.0))
        cerebro.addstrategy(TestStrategyInvalid, printlog=False)
        results = cerebro.run()
        strat = results[0]

        self.assertIsNone(
            strat.orders[0], "order_target with invalid code should return None"
        )
        self.assertIsNone(strat.orders[1], "order with invalid code should return None")
        self.assertIsNone(
            strat.orders[2],
            "order_target_percent with invalid ratio should return None",
        )
        self.assertIsNone(
            strat.orders[3],
            "order_target_percent with negative ratio should return None",
        )
        self.assertIsNone(
            strat.orders[4], "order_value with invalid code should return None"
        )
        self.assertIsNone(
            strat.orders[5], "_get_data_by_name with invalid code should return None"
        )


class TestGlobalOrderFunctions(unittest.TestCase):
    def test_global_order_target_without_strategy(self):
        from jk2bt.core.strategy_base import order_target

        result = order_target("sh600519", 100)
        self.assertIsNone(result)

    def test_global_order_value_without_strategy(self):
        from jk2bt.core.strategy_base import order_value

        result = order_value("sh600519", 10000)
        self.assertIsNone(result)

    def test_global_order_without_strategy(self):
        from jk2bt.core.strategy_base import order

        result = order("sh600519", 100)
        self.assertIsNone(result)


class TestOrderValueCalculation(unittest.TestCase):
    def test_order_value_calculation(self):
        cerebro = bt.Cerebro()
        cerebro.broker.setcash(1000000)

        class CalcStrategy(JQ2BTBaseStrategy):
            def initialize(self):
                self.buy_size = None
                self.run_daily(self._calc, time_str="after_close")

            def _calc(self, context):
                if self.buy_size is None:
                    price = self.datas[0].close[0]
                    self.buy_size = int(10000 / price)

        cerebro.adddata(create_mock_data("600519", price=100.0))
        cerebro.addstrategy(CalcStrategy, printlog=False)
        results = cerebro.run()
        strat = results[0]
        self.assertEqual(strat.buy_size, 100)


class TestGetDataByFormat(unittest.TestCase):
    def test_get_data_jq_format(self):
        cerebro = bt.Cerebro()
        cerebro.broker.setcash(1000000)

        class FindStrategy(JQ2BTBaseStrategy):
            def initialize(self):
                self.found = None
                self.run_daily(self._find, time_str="after_close")

            def _find(self, context):
                if self.found is None:
                    self.found = self._get_data_by_name("600519.XSHG")

        cerebro.adddata(create_mock_data("sh600519", price=100.0))
        cerebro.addstrategy(FindStrategy, printlog=False)
        results = cerebro.run()
        strat = results[0]
        self.assertIsNotNone(strat.found)

    def test_get_data_pure_code(self):
        cerebro = bt.Cerebro()
        cerebro.broker.setcash(1000000)

        class FindStrategy(JQ2BTBaseStrategy):
            def initialize(self):
                self.found = None
                self.run_daily(self._find, time_str="after_close")

            def _find(self, context):
                if self.found is None:
                    self.found = self._get_data_by_name("600519")

        cerebro.adddata(create_mock_data("sh600519", price=100.0))
        cerebro.addstrategy(FindStrategy, printlog=False)
        results = cerebro.run()
        strat = results[0]
        self.assertIsNotNone(strat.found)


if __name__ == "__main__":
    unittest.main(verbosity=2)
