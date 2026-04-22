"""
Tests for simple_buy_hold.py
"""
import sys
from unittest.mock import MagicMock, patch
from datetime import datetime
import pytest

from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "data"))


class MockBar:
    def __init__(self, close=10.0):
        self.close = close


class TestSimpleBuyHold:
    def test_init(self, rq_mocks):
        from simple_buy_hold import init
        context = MagicMock()
        init(context)
        assert context.stock == "000001.XSHE"
        assert context.bought == False

    def test_trade_already_bought(self, rq_mocks):
        from simple_buy_hold import trade, init
        context = MagicMock()
        context.bought = True
        init(context)
        trade(context, {})

    @patch("simple_buy_hold.history_bars")
    def test_trade_none_bars(self, mock_history_bars, rq_mocks):
        from simple_buy_hold import trade, init
        mock_history_bars.return_value = None
        context = MagicMock()
        context.bought = False
        context.stock = "000001.XSHE"
        init(context)
        trade(context, {})
        assert context.bought == False

    @patch("simple_buy_hold.history_bars")
    def test_trade_short_bars(self, mock_history_bars, rq_mocks):
        from simple_buy_hold import trade, init
        mock_history_bars.return_value = [10, 11, 12]
        context = MagicMock()
        context.bought = False
        context.stock = "000001.XSHE"
        init(context)
        trade(context, {})
        assert context.bought == False

    @patch("simple_buy_hold.history_bars")
    def test_trade_stock_not_in_bar(self, mock_history_bars, rq_mocks):
        from simple_buy_hold import trade, init
        mock_history_bars.return_value = [10, 11, 12, 13, 14]
        context = MagicMock()
        context.bought = False
        context.stock = "000001.XSHE"
        init(context)
        trade(context, {})
        assert context.bought == False

    @patch("simple_buy_hold.history_bars")
    def test_trade_invalid_price(self, mock_history_bars, rq_mocks):
        from simple_buy_hold import trade, init
        mock_history_bars.return_value = [10, 11, 12, 13, 14]
        context = MagicMock()
        context.bought = False
        context.stock = "000001.XSHE"
        init(context)
        bar_dict = {"000001.XSHE": MockBar(close=0)}
        trade(context, bar_dict)
        assert context.bought == False

    @patch("simple_buy_hold.history_bars")
    def test_trade_success(self, mock_history_bars, rq_mocks):
        from simple_buy_hold import trade, init
        mock_history_bars.return_value = [10, 11, 12, 13, 14]
        context = MagicMock()
        context.bought = False
        context.stock = "000001.XSHE"
        context.portfolio.total_value = 100000
        init(context)
        bar_dict = {"000001.XSHE": MockBar(close=12)}
        trade(context, bar_dict)
        assert context.bought == True

    def test_after_trading_end(self, rq_mocks):
        from simple_buy_hold import after_trading_end
        context = MagicMock()
        after_trading_end(context, {})

    @patch("simple_buy_hold.history_bars")
    def test_trade_exception(self, mock_history_bars, rq_mocks):
        from simple_buy_hold import trade, init
        mock_history_bars.side_effect = Exception("API error")
        context = MagicMock()
        context.bought = False
        context.stock = "000001.XSHE"
        init(context)
        trade(context, {})
        assert context.bought == False