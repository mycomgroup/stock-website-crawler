"""
Tests for attribution_c_event_rq.py
Pure event (first board low open) strategy
"""
import sys
from pathlib import Path
import builtins
from pathlib import Path
import pytest
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from unittest.mock import MagicMock, patch, Mock

sys.path.insert(0, str(Path(__file__).parent.parent))


class MockBar:
    def __init__(self, close=10.0, open_price=9.5, is_trading=True, limit_up=11.0):
        self.close = close
        self.open = open_price
        self.is_trading = is_trading
        self.limit_up = limit_up


class MockPosition:
    def __init__(self, quantity=100):
        self.quantity = quantity


class MockPortfolio:
    def __init__(self):
        self.positions = {}


class MockContext:
    def __init__(self):
        self.now = datetime(2024, 7, 2, 9, 30)
        self.portfolio = MockPortfolio()
        self.target_stock = None
        self.buy_price = 0
        self.hold_days = 0


@pytest.fixture
def rq_globals():
    mocks = {
        'logger': Mock(),
        'order_target_percent': Mock(),
        'all_instruments': Mock(return_value=pd.DataFrame({'order_book_id': []})),
        'history_bars': Mock(return_value=None),
    }
    original = {}
    for name, mock in mocks.items():
        if hasattr(builtins, name):
            original[name] = getattr(builtins, name)
        setattr(builtins, name, mock)
    yield mocks
    for name in mocks:
        if name in original:
            setattr(builtins, name, original[name])
        else:
            delattr(builtins, name)


class TestInit:
    def test_init_sets_default_values(self, rq_globals):
        import importlib
        import attribution_c_event_rq
        importlib.reload(attribution_c_event_rq)
        context = MockContext()
        attribution_c_event_rq.init(context)
        assert context.target_stock is None
        assert context.buy_price == 0
        assert context.hold_days == 0


class TestHandleBar:
    def test_handle_bar_no_position_finds_buy(self, rq_globals):
        import importlib
        import attribution_c_event_rq
        importlib.reload(attribution_c_event_rq)
        context = MockContext()
        attribution_c_event_rq.init(context)
        with patch.object(attribution_c_event_rq, 'find_and_buy') as mock_find:
            attribution_c_event_rq.handle_bar(context, {})
            mock_find.assert_called_once()

    def test_handle_bar_with_position_hold_days_zero(self, rq_globals):
        import importlib
        import attribution_c_event_rq
        importlib.reload(attribution_c_event_rq)
        context = MockContext()
        attribution_c_event_rq.init(context)
        context.target_stock = '000001.XSHE'
        context.portfolio.positions = {'000001.XSHE': MockPosition()}
        context.hold_days = 0
        attribution_c_event_rq.handle_bar(context, {})
        rq_globals['order_target_percent'].assert_called_with('000001.XSHE', 0)
        assert context.hold_days == 0
        assert context.target_stock is None

    def test_handle_bar_sell_after_one_day(self, rq_globals):
        import importlib
        import attribution_c_event_rq
        importlib.reload(attribution_c_event_rq)
        context = MockContext()
        attribution_c_event_rq.init(context)
        context.target_stock = '000001.XSHE'
        context.portfolio.positions = {'000001.XSHE': MockPosition()}
        context.hold_days = 1
        attribution_c_event_rq.handle_bar(context, {})
        rq_globals['order_target_percent'].assert_called_with('000001.XSHE', 0)
        assert context.target_stock is None
        assert context.hold_days == 0


class TestFindAndBuy:
    def test_find_and_buy_no_stocks(self, rq_globals):
        rq_globals['all_instruments'].return_value = pd.DataFrame({'order_book_id': []})
        import importlib
        import attribution_c_event_rq
        importlib.reload(attribution_c_event_rq)
        context = MockContext()
        attribution_c_event_rq.find_and_buy(context, {})
        rq_globals['order_target_percent'].assert_not_called()

    def test_find_and_buy_stock_not_in_bar_dict(self, rq_globals):
        rq_globals['all_instruments'].return_value = pd.DataFrame({'order_book_id': ['000001.XSHE']})
        def mock_history_bars(code, count, freq, fields, date=None):
            if 'limit_up' in str(fields):
                return np.array([(10.0, 10.0)], dtype=[('close', 'f8'), ('limit_up', 'f8')])
            return np.array([(10.0,)], dtype=[('close', 'f8')])
        rq_globals['history_bars'].side_effect = mock_history_bars
        import importlib
        import attribution_c_event_rq
        importlib.reload(attribution_c_event_rq)
        context = MockContext()
        attribution_c_event_rq.find_and_buy(context, {})
        rq_globals['order_target_percent'].assert_not_called()

    def test_find_and_buy_stock_not_trading(self, rq_globals):
        rq_globals['all_instruments'].return_value = pd.DataFrame({'order_book_id': ['000001.XSHE']})
        def mock_history_bars(code, count, freq, fields, date=None):
            if 'limit_up' in str(fields):
                return np.array([(10.0, 10.0)], dtype=[('close', 'f8'), ('limit_up', 'f8')])
            return np.array([(10.0,)], dtype=[('close', 'f8')])
        rq_globals['history_bars'].side_effect = mock_history_bars
        import importlib
        import attribution_c_event_rq
        importlib.reload(attribution_c_event_rq)
        context = MockContext()
        bar_dict = {'000001.XSHE': MockBar(is_trading=False)}
        attribution_c_event_rq.find_and_buy(context, bar_dict)
        rq_globals['order_target_percent'].assert_not_called()

    def test_find_and_buy_open_out_of_range(self, rq_globals):
        rq_globals['all_instruments'].return_value = pd.DataFrame({'order_book_id': ['000001.XSHE']})
        def mock_history_bars(code, count, freq, fields, date=None):
            if 'limit_up' in str(fields):
                return np.array([(10.0, 10.0)], dtype=[('close', 'f8'), ('limit_up', 'f8')])
            return np.array([(10.0,)], dtype=[('close', 'f8')])
        rq_globals['history_bars'].side_effect = mock_history_bars
        import importlib
        import attribution_c_event_rq
        importlib.reload(attribution_c_event_rq)
        context = MockContext()
        bar_dict = {'000001.XSHE': MockBar(open_price=10.5)}
        attribution_c_event_rq.find_and_buy(context, bar_dict)
        rq_globals['order_target_percent'].assert_not_called()

    def test_find_and_buy_successful_buy(self, rq_globals):
        rq_globals['all_instruments'].return_value = pd.DataFrame({'order_book_id': ['000001.XSHE']})
        def mock_history_bars(code, count, freq, fields, date=None):
            if 'limit_up' in str(fields):
                return np.array([(10.0, 10.0)], dtype=[('close', 'f8'), ('limit_up', 'f8')])
            return np.array([(10.0,)], dtype=[('close', 'f8')])
        rq_globals['history_bars'].side_effect = mock_history_bars
        import importlib
        import attribution_c_event_rq
        importlib.reload(attribution_c_event_rq)
        context = MockContext()
        bar_dict = {'000001.XSHE': MockBar(open_price=10.1, close=10.2)}
        attribution_c_event_rq.find_and_buy(context, bar_dict)
        rq_globals['order_target_percent'].assert_called_with('000001.XSHE', 1.0)
        assert context.target_stock == '000001.XSHE'

    def test_find_and_buy_not_limit_up(self, rq_globals):
        rq_globals['all_instruments'].return_value = pd.DataFrame({'order_book_id': ['000001.XSHE']})
        def mock_history_bars(code, count, freq, fields, date=None):
            if 'limit_up' in str(fields):
                return np.array([(10.0, 11.0)], dtype=[('close', 'f8'), ('limit_up', 'f8')])
            return np.array([(10.0,)], dtype=[('close', 'f8')])
        rq_globals['history_bars'].side_effect = mock_history_bars
        import importlib
        import attribution_c_event_rq
        importlib.reload(attribution_c_event_rq)
        context = MockContext()
        bar_dict = {'000001.XSHE': MockBar(open_price=10.1, close=10.2)}
        attribution_c_event_rq.find_and_buy(context, bar_dict)
        rq_globals['order_target_percent'].assert_not_called()


class TestEdgeCases:
    def test_find_and_buy_limit_up_detection(self, rq_globals):
        rq_globals['all_instruments'].return_value = pd.DataFrame({'order_book_id': ['000001.XSHE']})
        def mock_history_bars(code, count, freq, fields, date=None):
            if 'limit_up' in str(fields):
                return np.array([(11.0, 11.01)], dtype=[('close', 'f8'), ('limit_up', 'f8')])
            return np.array([(11.0,)], dtype=[('close', 'f8')])
        rq_globals['history_bars'].side_effect = mock_history_bars
        import importlib
        import attribution_c_event_rq
        importlib.reload(attribution_c_event_rq)
        context = MockContext()
        bar_dict = {'000001.XSHE': MockBar(open_price=11.1, close=11.2)}
        attribution_c_event_rq.find_and_buy(context, bar_dict)
        assert context.target_stock == '000001.XSHE'

    def test_find_and_buy_prev_bars_none(self, rq_globals):
        rq_globals['all_instruments'].return_value = pd.DataFrame({'order_book_id': ['000001.XSHE']})
        def mock_history_bars(code, count, freq, fields, date=None):
            if 'limit_up' in str(fields):
                return np.array([(10.0, 10.0)], dtype=[('close', 'f8'), ('limit_up', 'f8')])
            return None
        rq_globals['history_bars'].side_effect = mock_history_bars
        import importlib
        import attribution_c_event_rq
        importlib.reload(attribution_c_event_rq)
        context = MockContext()
        bar_dict = {'000001.XSHE': MockBar(open_price=10.1, close=10.2)}
        attribution_c_event_rq.find_and_buy(context, bar_dict)
        rq_globals['order_target_percent'].assert_not_called()

    def test_find_and_buy_only_first_qualified(self, rq_globals):
        rq_globals['all_instruments'].return_value = pd.DataFrame({'order_book_id': ['000001.XSHE', '000002.XSHE']})
        def mock_history_bars(code, count, freq, fields, date=None):
            if 'limit_up' in str(fields):
                return np.array([(10.0, 10.0)], dtype=[('close', 'f8'), ('limit_up', 'f8')])
            return np.array([(10.0,)], dtype=[('close', 'f8')])
        rq_globals['history_bars'].side_effect = mock_history_bars
        import importlib
        import attribution_c_event_rq
        importlib.reload(attribution_c_event_rq)
        context = MockContext()
        bar_dict = {'000001.XSHE': MockBar(open_price=10.1, close=10.2), '000002.XSHE': MockBar(open_price=10.1, close=10.2)}
        attribution_c_event_rq.find_and_buy(context, bar_dict)
        rq_globals['order_target_percent'].assert_called_once()

    def test_find_and_buy_prev_bars_empty(self, rq_globals):
        rq_globals['all_instruments'].return_value = pd.DataFrame({'order_book_id': ['000001.XSHE']})
        def mock_history_bars(code, count, freq, fields, date=None):
            if 'limit_up' in str(fields):
                return np.array([(10.0, 10.0)], dtype=[('close', 'f8'), ('limit_up', 'f8')])
            return np.array([], dtype=[('close', 'f8')])
        rq_globals['history_bars'].side_effect = mock_history_bars
        import importlib
        import attribution_c_event_rq
        importlib.reload(attribution_c_event_rq)
        context = MockContext()
        bar_dict = {'000001.XSHE': MockBar(open_price=10.1, close=10.2)}
        attribution_c_event_rq.find_and_buy(context, bar_dict)
        rq_globals['order_target_percent'].assert_not_called()