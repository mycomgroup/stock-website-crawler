"""
Tests for mainline_strategy_rq.py
"""
import sys
from unittest.mock import MagicMock, patch
from datetime import datetime, date
import pandas as pd
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


class MockInstrument:
    def __init__(self, order_book_id="600519.XSHG"):
        self.order_book_id = order_book_id


class TestMainlineStrategyRq:
    def test_init(self, rq_mocks):
        from mainline_strategy_rq import init
        context = MagicMock()
        init(context)
        assert context.position_stock is None
        assert context.entry_price == 0
        assert context.hold_days == 0
        assert context.max_hold_days == 2
        assert context.stop_loss_pct == -0.04

    @patch("mainline_strategy_rq.all_instruments")
    @patch("mainline_strategy_rq.history_bars")
    @patch("mainline_strategy_rq.get_previous_trading_date")
    def test_get_limit_up_stocks_empty(self, mock_prev_date, mock_history_bars, mock_all_instruments, rq_mocks):
        from mainline_strategy_rq import get_limit_up_stocks
        mock_prev_date.return_value = date(2024, 6, 28)
        mock_all_instruments.return_value = pd.DataFrame({"order_book_id": []})
        context = MagicMock()
        context.now = MagicMock()
        context.now.date.return_value = date(2024, 7, 1)
        result = get_limit_up_stocks(context, {})
        assert result == []

    @patch("mainline_strategy_rq.all_instruments")
    @patch("mainline_strategy_rq.history_bars")
    @patch("mainline_strategy_rq.get_previous_trading_date")
    def test_get_limit_up_stocks_success(self, mock_prev_date, mock_history_bars, mock_all_instruments, rq_mocks):
        from mainline_strategy_rq import get_limit_up_stocks
        mock_prev_date.return_value = date(2024, 6, 28)
        mock_all_instruments.return_value = pd.DataFrame({
            "order_book_id": ["600519.XSHG", "000001.XSHE", "688001.XSHG", "430001.XSHE"]
        })
        mock_history_bars.return_value = [
            {"close": 10, "high": 10, "limit_up": 11},
            {"close": 10.5, "high": 10.5, "limit_up": 11},
        ]
        context = MagicMock()
        context.now = MagicMock()
        context.now.date.return_value = date(2024, 7, 1)
        result = get_limit_up_stocks(context, {})
        assert "688001.XSHG" not in result

    @patch("mainline_strategy_rq.all_instruments")
    @patch("mainline_strategy_rq.history_bars")
    @patch("mainline_strategy_rq.get_previous_trading_date")
    def test_get_limit_up_stocks_bars_none(self, mock_prev_date, mock_history_bars, mock_all_instruments, rq_mocks):
        from mainline_strategy_rq import get_limit_up_stocks
        mock_prev_date.return_value = date(2024, 6, 28)
        mock_all_instruments.return_value = pd.DataFrame({"order_book_id": ["600519.XSHG"]})
        mock_history_bars.return_value = None
        context = MagicMock()
        context.now = MagicMock()
        context.now.date.return_value = date(2024, 7, 1)
        result = get_limit_up_stocks(context, {})
        assert result == []

    def test_select_and_trade_already_position(self, rq_mocks):
        from mainline_strategy_rq import select_and_trade, init
        context = MagicMock()
        context.position_stock = "600519.XSHG"
        init(context)
        select_and_trade(context, {})
        assert context.position_stock == "600519.XSHG"

    @patch("mainline_strategy_rq.get_limit_up_stocks")
    def test_select_and_trade_no_zt_stocks(self, mock_get_limit_up, rq_mocks):
        from mainline_strategy_rq import select_and_trade, init
        mock_get_limit_up.return_value = []
        context = MagicMock()
        context.position_stock = None
        init(context)
        select_and_trade(context, {})
        assert context.position_stock is None

    @patch("mainline_strategy_rq.get_limit_up_stocks")
    @patch("mainline_strategy_rq.history_bars")
    def test_select_and_trade_success(self, mock_history_bars, mock_get_limit_up, rq_mocks):
        from mainline_strategy_rq import select_and_trade, init
        mock_get_limit_up.return_value = ["600519.XSHG"]
        mock_history_bars.return_value = [
            {"close": 10, "open": 10.1, "limit_up": 11},
            {"close": 10, "open": 10.1, "limit_up": 11},
        ]
        context = MagicMock()
        context.position_stock = None
        context.now = MagicMock()
        context.now.date.return_value = date(2024, 7, 1)
        context.portfolio.total_value = 100000
        init(context)
        bar_dict = {"600519.XSHG": MockBar(close=10.5, open_price=10.1, limit_up=11)}
        select_and_trade(context, bar_dict)
        assert context.position_stock == "600519.XSHG"

    def test_check_exit_none_position(self, rq_mocks):
        from mainline_strategy_rq import check_exit, init
        context = MagicMock()
        context.position_stock = None
        init(context)
        check_exit(context, {})
        assert context.position_stock is None

    def test_check_exit_stock_not_in_bar(self, rq_mocks):
        from mainline_strategy_rq import check_exit, init
        context = MagicMock()
        context.position_stock = "600519.XSHG"
        init(context)
        check_exit(context, {})
        assert context.position_stock == "600519.XSHG"

    def test_check_exit_stop_loss(self, rq_mocks):
        from mainline_strategy_rq import check_exit, init
        context = MagicMock()
        context.position_stock = "600519.XSHG"
        context.entry_price = 100
        context.hold_days = 1
        context.stop_loss_pct = -0.04
        context.now = MagicMock()
        context.now.date.return_value = date(2024, 7, 2)
        init(context)
        bar_dict = {"600519.XSHG": MockBar(close=95, high=96, limit_up=110)}
        check_exit(context, bar_dict)
        assert context.position_stock is None

    def test_check_exit_hold_limit_up(self, rq_mocks):
        from mainline_strategy_rq import check_exit, init
        context = MagicMock()
        context.position_stock = "600519.XSHG"
        context.entry_price = 100
        context.hold_days = 1
        context.stop_loss_pct = -0.04
        init(context)
        bar_dict = {"600519.XSHG": MockBar(close=109, high=109.5, limit_up=110)}
        check_exit(context, bar_dict)
        assert context.position_stock == "600519.XSHG"

    def test_check_exit_max_hold_days(self, rq_mocks):
        from mainline_strategy_rq import check_exit, init
        context = MagicMock()
        context.position_stock = "600519.XSHG"
        context.entry_price = 100
        context.hold_days = 2
        context.max_hold_days = 2
        context.stop_loss_pct = -0.04
        context.now = MagicMock()
        context.now.date.return_value = date(2024, 7, 2)
        init(context)
        bar_dict = {"600519.XSHG": MockBar(close=102, high=103, limit_up=110)}
        check_exit(context, bar_dict)
        assert context.position_stock is None

    def test_check_exit_no_signal(self, rq_mocks):
        from mainline_strategy_rq import check_exit, init
        context = MagicMock()
        context.position_stock = "600519.XSHG"
        context.entry_price = 100
        context.hold_days = 0
        context.max_hold_days = 2
        context.stop_loss_pct = -0.04
        init(context)
        bar_dict = {"600519.XSHG": MockBar(close=102, high=103, limit_up=110)}
        check_exit(context, bar_dict)
        assert context.position_stock == "600519.XSHG"

    def test_after_trading_end_no_position(self, rq_mocks):
        from mainline_strategy_rq import after_trading_end, init
        context = MagicMock()
        context.position_stock = None
        init(context)
        after_trading_end(context, {})
        assert context.hold_days == 0

    def test_after_trading_end_with_position(self, rq_mocks):
        from mainline_strategy_rq import after_trading_end, init
        context = MagicMock()
        context.position_stock = "600519.XSHG"
        context.hold_days = 0
        init(context)
        after_trading_end(context, {})
        assert context.hold_days == 1