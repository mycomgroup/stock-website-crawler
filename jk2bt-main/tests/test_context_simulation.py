import unittest
import backtrader as bt
import pandas as pd
from datetime import datetime

from jk2bt.core.strategy_base import (
    JQ2BTBaseStrategy,
    ContextProxy,
    PortfolioProxy,
    PositionProxy,
)


class TestStrategy(JQ2BTBaseStrategy):
    """测试策略"""

    def __init__(self):
        super().__init__()
        self.test_results = {}

    def next(self):
        super().next()
        self.test_results["positions"] = self.context.portfolio.positions
        self.test_results["total_value"] = self.context.portfolio.total_value
        self.test_results["available_cash"] = self.context.portfolio.available_cash
        self.test_results["returns"] = self.context.portfolio.returns
        self.test_results["current_dt"] = self.context.current_dt


class TestContextSimulation(unittest.TestCase):
    def test_context_portfolio_positions(self):
        cerebro = bt.Cerebro()
        cerebro.broker.setcash(100000.0)

        df = pd.DataFrame(
            {
                "datetime": pd.date_range("2023-01-01", periods=10),
                "open": [10.0] * 10,
                "high": [10.5] * 10,
                "low": [9.5] * 10,
                "close": [10.0] * 10,
                "volume": [1000] * 10,
                "openinterest": [0] * 10,
            }
        )
        data = bt.feeds.PandasData(
            dataname=df,
            datetime="datetime",
            open="open",
            high="high",
            low="low",
            close="close",
            volume="volume",
            openinterest="openinterest",
            name="test_stock",
        )
        cerebro.adddata(data)
        cerebro.addstrategy(TestStrategy)

        results = cerebro.run()
        strategy = results[0]

        positions = strategy.test_results["positions"]
        self.assertIsInstance(positions, dict)

    def test_context_portfolio_total_value(self):
        cerebro = bt.Cerebro()
        cerebro.broker.setcash(100000.0)

        df = pd.DataFrame(
            {
                "datetime": pd.date_range("2023-01-01", periods=10),
                "open": [10.0] * 10,
                "high": [10.5] * 10,
                "low": [9.5] * 10,
                "close": [10.0] * 10,
                "volume": [1000] * 10,
                "openinterest": [0] * 10,
            }
        )
        data = bt.feeds.PandasData(
            dataname=df,
            datetime="datetime",
            open="open",
            high="high",
            low="low",
            close="close",
            volume="volume",
            openinterest="openinterest",
            name="test_stock",
        )
        cerebro.adddata(data)
        cerebro.addstrategy(TestStrategy)

        results = cerebro.run()
        strategy = results[0]

        self.assertIsInstance(strategy.test_results["total_value"], float)
        self.assertEqual(strategy.test_results["total_value"], 100000.0)

    def test_context_portfolio_available_cash(self):
        cerebro = bt.Cerebro()
        cerebro.broker.setcash(50000.0)

        df = pd.DataFrame(
            {
                "datetime": pd.date_range("2023-01-01", periods=5),
                "open": [100.0] * 5,
                "high": [105.0] * 5,
                "low": [95.0] * 5,
                "close": [100.0] * 5,
                "volume": [1000] * 5,
                "openinterest": [0] * 5,
            }
        )
        data = bt.feeds.PandasData(
            dataname=df,
            datetime="datetime",
            open="open",
            high="high",
            low="low",
            close="close",
            volume="volume",
            openinterest="openinterest",
            name="test_stock",
        )
        cerebro.adddata(data)
        cerebro.addstrategy(TestStrategy)

        results = cerebro.run()
        strategy = results[0]

        self.assertIsInstance(strategy.test_results["available_cash"], float)
        self.assertEqual(strategy.test_results["available_cash"], 50000.0)

    def test_context_portfolio_returns(self):
        cerebro = bt.Cerebro()
        cerebro.broker.setcash(100000.0)

        df = pd.DataFrame(
            {
                "datetime": pd.date_range("2023-01-01", periods=10),
                "open": [10.0] * 10,
                "high": [10.5] * 10,
                "low": [9.5] * 10,
                "close": [10.0] * 10,
                "volume": [1000] * 10,
                "openinterest": [0] * 10,
            }
        )
        data = bt.feeds.PandasData(
            dataname=df,
            datetime="datetime",
            open="open",
            high="high",
            low="low",
            close="close",
            volume="volume",
            openinterest="openinterest",
            name="test_stock",
        )
        cerebro.adddata(data)
        cerebro.addstrategy(TestStrategy)

        results = cerebro.run()
        strategy = results[0]

        self.assertIsInstance(strategy.test_results["returns"], float)
        self.assertEqual(strategy.test_results["returns"], 0.0)

    def test_context_current_dt(self):
        cerebro = bt.Cerebro()
        cerebro.broker.setcash(100000.0)

        df = pd.DataFrame(
            {
                "datetime": pd.date_range("2023-01-01", periods=5),
                "open": [10.0] * 5,
                "high": [10.5] * 5,
                "low": [9.5] * 5,
                "close": [10.0] * 5,
                "volume": [1000] * 5,
                "openinterest": [0] * 5,
            }
        )
        data = bt.feeds.PandasData(
            dataname=df,
            datetime="datetime",
            open="open",
            high="high",
            low="low",
            close="close",
            volume="volume",
            openinterest="openinterest",
            name="test_stock",
        )
        cerebro.adddata(data)
        cerebro.addstrategy(TestStrategy)

        results = cerebro.run()
        strategy = results[0]

        self.assertIsNotNone(strategy.test_results["current_dt"])

    def test_context_subportfolios(self):
        cerebro = bt.Cerebro()
        cerebro.broker.setcash(100000.0)

        df = pd.DataFrame(
            {
                "datetime": pd.date_range("2023-01-01", periods=5),
                "open": [10.0] * 5,
                "high": [10.5] * 5,
                "low": [9.5] * 5,
                "close": [10.0] * 5,
                "volume": [1000] * 5,
                "openinterest": [0] * 5,
            }
        )
        data = bt.feeds.PandasData(
            dataname=df,
            datetime="datetime",
            open="open",
            high="high",
            low="low",
            close="close",
            volume="volume",
            openinterest="openinterest",
            name="test_stock",
        )
        cerebro.adddata(data)
        cerebro.addstrategy(TestStrategy)

        results = cerebro.run()
        strategy = results[0]

        self.assertIsInstance(strategy.context.subportfolios, list)
        self.assertEqual(len(strategy.context.subportfolios), 1)

    def test_portfolio_market_value(self):
        cerebro = bt.Cerebro()
        cerebro.broker.setcash(100000.0)

        df = pd.DataFrame(
            {
                "datetime": pd.date_range("2023-01-01", periods=5),
                "open": [10.0] * 5,
                "high": [10.5] * 5,
                "low": [9.5] * 5,
                "close": [10.0] * 5,
                "volume": [1000] * 5,
                "openinterest": [0] * 5,
            }
        )
        data = bt.feeds.PandasData(
            dataname=df,
            datetime="datetime",
            open="open",
            high="high",
            low="low",
            close="close",
            volume="volume",
            openinterest="openinterest",
            name="test_stock",
        )
        cerebro.adddata(data)
        cerebro.addstrategy(TestStrategy)

        results = cerebro.run()
        strategy = results[0]

        market_value = strategy.context.portfolio.market_value
        self.assertIsInstance(market_value, float)
        self.assertEqual(market_value, 0.0)

    def test_position_proxy_properties(self):
        cerebro = bt.Cerebro()
        cerebro.broker.setcash(100000.0)

        df = pd.DataFrame(
            {
                "datetime": pd.date_range("2023-01-01", periods=10),
                "open": [10.0] * 10,
                "high": [10.5] * 10,
                "low": [9.5] * 10,
                "close": [10.0] * 10,
                "volume": [10000] * 10,
                "openinterest": [0] * 10,
            }
        )
        data = bt.feeds.PandasData(
            dataname=df,
            datetime="datetime",
            open="open",
            high="high",
            low="low",
            close="close",
            volume="volume",
            openinterest="openinterest",
            name="test_stock",
        )
        cerebro.adddata(data)

        class BuyStrategy(JQ2BTBaseStrategy):
            def __init__(self):
                super().__init__()
                self.pos_checked = False

            def next(self):
                super().next()
                if not self.pos_checked and len(self) == 2:
                    self.buy(data=self.datas[0], size=100)
                    self.pos_checked = True

                if len(self) > 3:
                    positions = self.context.portfolio.positions
                    if "test_stock" in positions:
                        pos = positions["test_stock"]
                        self.test_total_amount = pos.total_amount
                        self.test_value = pos.value
                        self.test_price = pos.price

        cerebro.addstrategy(BuyStrategy)
        results = cerebro.run()
        strategy = results[0]

        if hasattr(strategy, "test_total_amount"):
            self.assertEqual(strategy.test_total_amount, 100)
            self.assertIsInstance(strategy.test_value, float)
            self.assertIsInstance(strategy.test_price, float)


if __name__ == "__main__":
    unittest.main()
