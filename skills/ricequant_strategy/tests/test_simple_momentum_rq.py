"""
Tests for simple_momentum_rq.py
"""
import sys
from unittest.mock import MagicMock, patch
from datetime import date
import pytest

from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "data"))


class MockBar:
    def __init__(self, close=10.0, limit_up=11.0, limit_down=9.0):
        self.close = close
        self.limit_up = limit_up
        self.limit_down = limit_down


class TestSimpleMomentumRq:
    def test_init(self, rq_mocks):
        from simple_momentum_rq import init
        context = MagicMock()
        init(context)
        assert context.position_stock is None
        assert context.entry_price == 0
        assert context.hold_days == 0

    def test_trade_already_position_profit(self, rq_mocks):
        from simple_momentum_rq import trade, init
        context = MagicMock()
        context.position_stock = "600519.XSHG"
        context.entry_price = 100
        context.hold_days = 0
        init(context)
        bar_dict = {"600519.XSHG": MockBar(close=104)}
        trade(context, bar_dict)
        assert context.position_stock is None

    def test_trade_already_position_loss(self, rq_mocks):
        from simple_momentum_rq import trade, init
        context = MagicMock()
        context.position_stock = "600519.XSHG"
        context.entry_price = 100
        context.hold_days = 0
        init(context)
        bar_dict = {"600519.XSHG": MockBar(close=96)}
        trade(context, bar_dict)
        assert context.position_stock is None

    def test_trade_already_position_max_hold(self, rq_mocks):
        from simple_momentum_rq import trade, init
        context = MagicMock()
        context.position_stock = "600519.XSHG"
        context.entry_price = 100
        context.hold_days = 3
        init(context)
        bar_dict = {"600519.XSHG": MockBar(close=102)}
        trade(context, bar_dict)
        assert context.position_stock is None

    def test_trade_already_position_no_sell(self, rq_mocks):
        from simple_momentum_rq import trade, init
        context = MagicMock()
        context.position_stock = "600519.XSHG"
        context.entry_price = 100
        context.hold_days = 0
        init(context)
        bar_dict = {"600519.XSHG": MockBar(close=102)}
        trade(context, bar_dict)
        assert context.position_stock == "600519.XSHG"
        assert context.hold_days == 1

    def test_trade_already_position_not_in_bar(self, rq_mocks):
        from simple_momentum_rq import trade, init
        context = MagicMock()
        context.position_stock = "600519.XSHG"
        context.entry_price = 100
        context.hold_days = 0
        init(context)
        trade(context, {})
        assert context.hold_days == 1

    @patch("simple_momentum_rq.history_bars")
    def test_trade_no_position_drop_below_threshold(self, mock_history_bars, rq_mocks):
        from simple_momentum_rq import trade, init
        mock_history_bars.return_value = [100, 95]
        context = MagicMock()
        context.position_stock = None
        context.now = MagicMock()
        context.now.date.return_value = date(2024, 7, 1)
        init(context)
        bar_dict = {"600519.XSHG": MockBar(close=95, limit_up=110, limit_down=90)}
        trade(context, bar_dict)
        assert context.position_stock == "600519.XSHG"

    @patch("simple_momentum_rq.history_bars")
    def test_trade_no_position_above_threshold(self, mock_history_bars, rq_mocks):
        from simple_momentum_rq import trade, init
        mock_history_bars.return_value = [100, 102]
        context = MagicMock()
        context.position_stock = None
        context.now = MagicMock()
        context.now.date.return_value = date(2024, 7, 1)
        init(context)
        bar_dict = {"600519.XSHG": MockBar(close=102, limit_up=110, limit_down=90)}
        trade(context, bar_dict)
        assert context.position_stock is None

    @patch("simple_momentum_rq.history_bars")
    def test_trade_no_position_limit_up(self, mock_history_bars, rq_mocks):
        from simple_momentum_rq import trade, init
        mock_history_bars.return_value = [100, 95]
        context = MagicMock()
        context.position_stock = None
        context.now = MagicMock()
        context.now.date.return_value = date(2024, 7, 1)
        init(context)
        bar_dict = {"600519.XSHG": MockBar(close=109, limit_up=110, limit_down=90)}
        trade(context, bar_dict)
        assert context.position_stock is None

    @patch("simple_momentum_rq.history_bars")
    def test_trade_no_position_invalid_price(self, mock_history_bars, rq_mocks):
        from simple_momentum_rq import trade, init
        mock_history_bars.return_value = [100, 95]
        context = MagicMock()
        context.position_stock = None
        init(context)
        bar_dict = {"600519.XSHG": MockBar(close=0, limit_up=110, limit_down=90)}
        trade(context, bar_dict)
        assert context.position_stock is None

    @patch("simple_momentum_rq.history_bars")
    def test_trade_no_position_none_bars(self, mock_history_bars, rq_mocks):
        from simple_momentum_rq import trade, init
        mock_history_bars.return_value = None
        context = MagicMock()
        context.position_stock = None
        init(context)
        bar_dict = {"600519.XSHG": MockBar(close=95)}
        trade(context, bar_dict)
        assert context.position_stock is None

    @patch("simple_momentum_rq.history_bars")
    def test_trade_no_position_short_bars(self, mock_history_bars, rq_mocks):
        from simple_momentum_rq import trade, init
        mock_history_bars.return_value = [95]
        context = MagicMock()
        context.position_stock = None
        init(context)
        bar_dict = {"600519.XSHG": MockBar(close=95)}
        trade(context, bar_dict)
        assert context.position_stock is None

    def test_trade_no_position_not_in_bar(self, rq_mocks):
        from simple_momentum_rq import trade, init
        context = MagicMock()
        context.position_stock = None
        context.now = MagicMock()
        context.now.date.return_value = date(2024, 7, 1)
        init(context)
        trade(context, {})
        assert context.position_stock is None

    @patch("simple_momentum_rq.history_bars")
    def test_trade_no_position_exception(self, mock_history_bars, rq_mocks):
        from simple_momentum_rq import trade, init
        mock_history_bars.side_effect = Exception("API error")
        context = MagicMock()
        context.position_stock = None
        init(context)
        bar_dict = {"600519.XSHG": MockBar(close=95)}
        trade(context, bar_dict)
        assert context.position_stock is None

    def test_after_trading_end(self, rq_mocks):
        from simple_momentum_rq import after_trading_end
        context = MagicMock()
        after_trading_end(context, {})