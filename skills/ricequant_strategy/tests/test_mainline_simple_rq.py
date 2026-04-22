"""
Tests for mainline_simple_rq.py
"""
import sys
from unittest.mock import MagicMock, patch
from datetime import datetime, date
import pytest

from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "data"))


class MockBar:
    def __init__(self, close=10.0, open_price=10.0, high=10.5, limit_up=11.0, is_trading=True):
        self.close = close
        self.open = open_price
        self.high = high
        self.limit_up = limit_up
        self.is_trading = is_trading


class TestMainlineSimpleRq:
    def test_init(self, rq_mocks):
        from mainline_simple_rq import init
        context = MagicMock()
        init(context)
        assert context.position_stock is None
        assert context.entry_price == 0

    def test_select_stock_already_position(self, rq_mocks):
        from mainline_simple_rq import select_stock
        context = MagicMock()
        context.position_stock = "600519.XSHG"
        context.entry_price = 100
        select_stock(context, {})
        assert context.position_stock == "600519.XSHG"

    @patch("mainline_simple_rq.index_components")
    @patch("mainline_simple_rq.history_bars")
    def test_select_stock_no_candidates(self, mock_history_bars, mock_index_components, rq_mocks):
        from mainline_simple_rq import select_stock, init
        mock_index_components.return_value = ["600519.XSHG"]
        mock_history_bars.return_value = [
            {"close": 10, "open": 11, "high": 12, "limit_up": 13},
            {"close": 10, "open": 11, "high": 12, "limit_up": 13},
        ]
        context = MagicMock()
        context.position_stock = None
        context.now = MagicMock()
        context.now.date.return_value = date(2024, 7, 1)
        context.portfolio.total_value = 100000
        init(context)
        bar_dict = {"600519.XSHG": MockBar(close=11, open_price=10.5, limit_up=13)}
        select_stock(context, bar_dict)
        assert context.position_stock is None

    @patch("mainline_simple_rq.index_components")
    @patch("mainline_simple_rq.history_bars")
    def test_select_stock_with_candidates(self, mock_history_bars, mock_index_components, rq_mocks):
        from mainline_simple_rq import select_stock, init
        mock_index_components.return_value = ["600519.XSHG"]
        mock_history_bars.return_value = [
            {"close": 10, "open": 9.8, "high": 12, "limit_up": 11},
            {"close": 10, "open": 9.8, "high": 12, "limit_up": 11},
        ]
        context = MagicMock()
        context.position_stock = None
        context.now = MagicMock()
        context.now.date.return_value = date(2024, 7, 1)
        context.portfolio.total_value = 100000
        init(context)
        bar_dict = {"600519.XSHG": MockBar(close=10, open_price=9.7, high=10.5, limit_up=11)}
        select_stock(context, bar_dict)
        assert context.position_stock == "600519.XSHG"

    @patch("mainline_simple_rq.index_components")
    def test_select_stock_empty_pool(self, mock_index_components, rq_mocks):
        from mainline_simple_rq import select_stock, init
        mock_index_components.return_value = []
        context = MagicMock()
        context.position_stock = None
        context.now = MagicMock()
        context.now.date.return_value = date(2024, 7, 1)
        init(context)
        select_stock(context, {})
        assert context.position_stock is None

    def test_check_sell_none_position(self, rq_mocks):
        from mainline_simple_rq import check_sell
        context = MagicMock()
        context.position_stock = None
        check_sell(context, {})
        assert context.position_stock is None

    def test_check_sell_stock_not_in_bar(self, rq_mocks):
        from mainline_simple_rq import check_sell
        context = MagicMock()
        context.position_stock = "600519.XSHG"
        context.entry_price = 100
        check_sell(context, {})
        assert context.position_stock == "600519.XSHG"

    def test_check_sell_profit_above_threshold(self, rq_mocks):
        from mainline_simple_rq import check_sell, init
        context = MagicMock()
        context.position_stock = "600519.XSHG"
        context.entry_price = 100
        context.now = MagicMock()
        context.now.date.return_value = date(2024, 7, 2)
        init(context)
        bar_dict = {"600519.XSHG": MockBar(close=106, high=108)}
        check_sell(context, bar_dict)
        assert context.position_stock is None
        assert context.entry_price == 0

    def test_check_sell_loss_below_threshold(self, rq_mocks):
        from mainline_simple_rq import check_sell, init
        context = MagicMock()
        context.position_stock = "600519.XSHG"
        context.entry_price = 100
        context.now = MagicMock()
        context.now.date.return_value = date(2024, 7, 2)
        init(context)
        bar_dict = {"600519.XSHG": MockBar(close=95, high=96)}
        check_sell(context, bar_dict)
        assert context.position_stock is None

    def test_check_sell_no_signal(self, rq_mocks):
        from mainline_simple_rq import check_sell, init
        context = MagicMock()
        context.position_stock = "600519.XSHG"
        context.entry_price = 100
        context.now = MagicMock()
        context.now.date.return_value = date(2024, 7, 2)
        init(context)
        bar_dict = {"600519.XSHG": MockBar(close=102, high=103)}
        check_sell(context, bar_dict)
        assert context.position_stock == "600519.XSHG"

    def test_after_trading_end(self, rq_mocks):
        from mainline_simple_rq import after_trading_end
        context = MagicMock()
        after_trading_end(context, {})

    @patch("mainline_simple_rq.history_bars")
    def test_select_stock_bars_none(self, mock_history_bars, rq_mocks):
        from mainline_simple_rq import select_stock, init
        mock_history_bars.return_value = None
        context = MagicMock()
        context.position_stock = None
        context.now = MagicMock()
        context.now.date.return_value = date(2024, 7, 1)
        init(context)
        with patch("mainline_simple_rq.index_components", return_value=["600519.XSHG"]):
            select_stock(context, {})
        assert context.position_stock is None

    @patch("mainline_simple_rq.history_bars")
    def test_select_stock_bars_short(self, mock_history_bars, rq_mocks):
        from mainline_simple_rq import select_stock, init
        mock_history_bars.return_value = [{"close": 10}]
        context = MagicMock()
        context.position_stock = None
        context.now = MagicMock()
        context.now.date.return_value = date(2024, 7, 1)
        init(context)
        with patch("mainline_simple_rq.index_components", return_value=["600519.XSHG"]):
            select_stock(context, {})
        assert context.position_stock is None