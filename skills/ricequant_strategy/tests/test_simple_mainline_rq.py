"""
Tests for simple_mainline_rq.py
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


class TestSimpleMainlineRq:
    def test_init(self, rq_mocks):
        from simple_mainline_rq import init
        context = MagicMock()
        init(context)
        assert context.stocks == ["000001.XSHE", "600000.XSHG", "000002.XSHE"]
        assert context.bought == False

    def test_rebalance_already_bought(self, rq_mocks):
        from simple_mainline_rq import rebalance, init
        context = MagicMock()
        context.bought = True
        init(context)
        rebalance(context, {})

    @patch("simple_mainline_rq.history_bars")
    def test_rebalance_none_bars(self, mock_history_bars, rq_mocks):
        from simple_mainline_rq import rebalance, init
        mock_history_bars.return_value = None
        context = MagicMock()
        context.bought = False
        context.stocks = ["000001.XSHE"]
        init(context)
        rebalance(context, {})
        assert context.bought == False

    @patch("simple_mainline_rq.history_bars")
    def test_rebalance_short_bars(self, mock_history_bars, rq_mocks):
        from simple_mainline_rq import rebalance, init
        mock_history_bars.return_value = [10, 11, 12]
        context = MagicMock()
        context.bought = False
        context.stocks = ["000001.XSHE"]
        init(context)
        rebalance(context, {})
        assert context.bought == False

    @patch("simple_mainline_rq.history_bars")
    def test_rebalance_below_ma5(self, mock_history_bars, rq_mocks):
        from simple_mainline_rq import rebalance, init
        mock_history_bars.return_value = [10, 10, 10, 10, 10]
        context = MagicMock()
        context.bought = False
        context.stocks = ["000001.XSHE"]
        init(context)
        rebalance(context, {})
        assert context.bought == False

    @patch("simple_mainline_rq.history_bars")
    def test_rebalance_above_ma5(self, mock_history_bars, rq_mocks):
        from simple_mainline_rq import rebalance, init
        mock_history_bars.return_value = [10, 10, 10, 10, 11]
        context = MagicMock()
        context.bought = False
        context.stocks = ["000001.XSHE"]
        init(context)
        rebalance(context, {})
        assert context.bought == True

    @patch("simple_mainline_rq.history_bars")
    def test_rebalance_exception(self, mock_history_bars, rq_mocks):
        from simple_mainline_rq import rebalance, init
        mock_history_bars.side_effect = Exception("API error")
        context = MagicMock()
        context.bought = False
        context.stocks = ["000001.XSHE"]
        init(context)
        rebalance(context, {})
        assert context.bought == False

    def test_after_trading_end(self, rq_mocks):
        from simple_mainline_rq import after_trading_end
        context = MagicMock()
        after_trading_end(context, {})