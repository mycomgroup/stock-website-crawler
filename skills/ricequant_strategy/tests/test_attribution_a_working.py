"""
Tests for attribution_a_working.py
Fixed version of small cap market value factor strategy
"""
import sys
from pathlib import Path
import builtins
from pathlib import Path
import pytest
import pandas as pd
import numpy as np
from datetime import datetime
from unittest.mock import MagicMock, patch, Mock

sys.path.insert(0, str(Path(__file__).parent.parent))


class MockBar:
    def __init__(self, close=10.0, open_price=10.0, is_trading=True, limit_up=11.0):
        self.close = close
        self.open = open_price
        self.is_trading = is_trading
        self.limit_up = limit_up


class MockPortfolio:
    def __init__(self):
        self.positions = {}


class MockContext:
    def __init__(self):
        self.now = datetime(2024, 7, 1, 10, 0)
        self.portfolio = MockPortfolio()
        self.stock_list = []
        self.month = 0
        self.has_rebalanced = False


class MockInstrument:
    def __init__(self, order_book_id):
        self.order_book_id = order_book_id


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
        import attribution_a_working
        importlib.reload(attribution_a_working)
        context = MockContext()
        attribution_a_working.init(context)
        assert context.stock_list == []
        assert context.month == 0
        assert context.has_rebalanced == False


class TestHandleBar:
    def test_handle_bar_new_month_rebalance(self, rq_globals):
        import importlib
        import attribution_a_working
        importlib.reload(attribution_a_working)
        context = MockContext()
        attribution_a_working.init(context)
        context.now = datetime(2024, 7, 1, 10, 0)
        with patch.object(attribution_a_working, 'do_rebalance') as mock_rebalance:
            attribution_a_working.handle_bar(context, {})
            mock_rebalance.assert_called_once()
            assert context.has_rebalanced == True

    def test_handle_bar_same_month_no_rebalance(self, rq_globals):
        import importlib
        import attribution_a_working
        importlib.reload(attribution_a_working)
        context = MockContext()
        attribution_a_working.init(context)
        context.month = 7
        context.has_rebalanced = True
        context.now = datetime(2024, 7, 15, 10, 0)
        with patch.object(attribution_a_working, 'do_rebalance') as mock_rebalance:
            attribution_a_working.handle_bar(context, {})
            mock_rebalance.assert_not_called()

    def test_handle_bar_rebalance_after_reset(self, rq_globals):
        import importlib
        import attribution_a_working
        importlib.reload(attribution_a_working)
        context = MockContext()
        attribution_a_working.init(context)
        context.month = 7
        context.has_rebalanced = True
        context.now = datetime(2024, 8, 2, 10, 0)
        with patch.object(attribution_a_working, 'do_rebalance') as mock_rebalance:
            attribution_a_working.handle_bar(context, {})
            assert context.month == 8
            assert context.has_rebalanced == True
            mock_rebalance.assert_called_once()

    def test_handle_bar_rebalance_day_boundary_day_5(self, rq_globals):
        import importlib
        import attribution_a_working
        importlib.reload(attribution_a_working)
        context = MockContext()
        attribution_a_working.init(context)
        context.now = datetime(2024, 7, 5, 10, 0)
        with patch.object(attribution_a_working, 'do_rebalance') as mock_rebalance:
            attribution_a_working.handle_bar(context, {})
            mock_rebalance.assert_called_once()

    def test_handle_bar_no_rebalance_after_day_5(self, rq_globals):
        import importlib
        import attribution_a_working
        importlib.reload(attribution_a_working)
        context = MockContext()
        attribution_a_working.init(context)
        context.month = 7
        context.has_rebalanced = False
        context.now = datetime(2024, 7, 6, 10, 0)
        with patch.object(attribution_a_working, 'do_rebalance') as mock_rebalance:
            attribution_a_working.handle_bar(context, {})
            mock_rebalance.assert_not_called()


class TestDoRebalance:
    def test_do_rebalance_empty_stock_list(self, rq_globals):
        rq_globals['all_instruments'].return_value = pd.DataFrame({'order_book_id': []})
        rq_globals['history_bars'].return_value = None
        import importlib
        import attribution_a_working
        importlib.reload(attribution_a_working)
        context = MockContext()
        attribution_a_working.do_rebalance(context, {})
        rq_globals['order_target_percent'].assert_not_called()

    def test_do_rebalance_with_valid_stocks(self, rq_globals):
        rq_globals['all_instruments'].return_value = pd.DataFrame({'order_book_id': ['000001.XSHE', '000002.XSHE']})
        def mock_history_bars(code, count, freq, fields):
            return np.array([(10.0,)], dtype=[('close', 'f8')])
        rq_globals['history_bars'].side_effect = mock_history_bars
        import importlib
        import attribution_a_working
        importlib.reload(attribution_a_working)
        context = MockContext()
        bar_dict = {'000001.XSHE': MockBar(), '000002.XSHE': MockBar()}
        attribution_a_working.do_rebalance(context, bar_dict)
        assert rq_globals['order_target_percent'].call_count > 0

    def test_do_rebalance_clears_old_positions(self, rq_globals):
        rq_globals['all_instruments'].return_value = pd.DataFrame({'order_book_id': ['000001.XSHE']})
        def mock_history_bars(code, count, freq, fields):
            return np.array([(10.0,)], dtype=[('close', 'f8')])
        rq_globals['history_bars'].side_effect = mock_history_bars
        import importlib
        import attribution_a_working
        importlib.reload(attribution_a_working)
        context = MockContext()
        context.portfolio.positions = {'999999.XSHG': Mock()}
        bar_dict = {'000001.XSHE': MockBar()}
        attribution_a_working.do_rebalance(context, bar_dict)
        rq_globals['order_target_percent'].assert_any_call('999999.XSHG', 0)

    def test_do_rebalance_history_bars_none(self, rq_globals):
        rq_globals['all_instruments'].return_value = pd.DataFrame({'order_book_id': ['000001.XSHE']})
        rq_globals['history_bars'].return_value = None
        import importlib
        import attribution_a_working
        importlib.reload(attribution_a_working)
        context = MockContext()
        attribution_a_working.do_rebalance(context, {})
        rq_globals['order_target_percent'].assert_not_called()

    def test_do_rebalance_zero_price_ignored(self, rq_globals):
        rq_globals['all_instruments'].return_value = pd.DataFrame({'order_book_id': ['000001.XSHE', '000002.XSHE']})
        def mock_history_bars(code, count, freq, fields):
            if code == '000001.XSHE':
                return np.array([(0.0,)], dtype=[('close', 'f8')])
            return np.array([(10.0,)], dtype=[('close', 'f8')])
        rq_globals['history_bars'].side_effect = mock_history_bars
        import importlib
        import attribution_a_working
        importlib.reload(attribution_a_working)
        context = MockContext()
        bar_dict = {'000002.XSHE': MockBar()}
        attribution_a_working.do_rebalance(context, bar_dict)
        assert '000001.XSHE' not in context.stock_list

    def test_do_rebalance_only_buys_stocks_in_bar_dict(self, rq_globals):
        rq_globals['all_instruments'].return_value = pd.DataFrame({'order_book_id': ['000001.XSHE', '000002.XSHE']})
        def mock_history_bars(code, count, freq, fields):
            return np.array([(10.0,)], dtype=[('close', 'f8')])
        rq_globals['history_bars'].side_effect = mock_history_bars
        import importlib
        import attribution_a_working
        importlib.reload(attribution_a_working)
        context = MockContext()
        bar_dict = {'000001.XSHE': MockBar()}
        attribution_a_working.do_rebalance(context, bar_dict)
        buy_calls = [c for c in rq_globals['order_target_percent'].call_args_list if c[0][1] > 0]
        assert len(buy_calls) == 1

    def test_do_rebalance_selects_lowest_price(self, rq_globals):
        rq_globals['all_instruments'].return_value = pd.DataFrame({
            'order_book_id': ['000001.XSHE', '000002.XSHE', '000003.XSHE']
        })
        def mock_history_bars(code, count, freq, fields):
            prices = {'000001.XSHE': 30.0, '000002.XSHE': 10.0, '000003.XSHE': 5.0}
            return np.array([(prices[code],)], dtype=[('close', 'f8')])
        rq_globals['history_bars'].side_effect = mock_history_bars
        import importlib
        import attribution_a_working
        importlib.reload(attribution_a_working)
        context = MockContext()
        bar_dict = {'000001.XSHE': MockBar(), '000002.XSHE': MockBar(), '000003.XSHE': MockBar()}
        attribution_a_working.do_rebalance(context, bar_dict)
        assert context.stock_list[0] == '000003.XSHE'

    def test_do_rebalance_limits_to_20_stocks(self, rq_globals):
        rq_globals['all_instruments'].return_value = pd.DataFrame({
            'order_book_id': [f"00000{i:03d}.XSHE" for i in range(150)]
        })
        def mock_history_bars(code, count, freq, fields):
            return np.array([(10.0,)], dtype=[('close', 'f8')])
        rq_globals['history_bars'].side_effect = mock_history_bars
        import importlib
        import attribution_a_working
        importlib.reload(attribution_a_working)
        context = MockContext()
        bar_dict = {f"00000{i:03d}.XSHE": MockBar() for i in range(150)}
        attribution_a_working.do_rebalance(context, bar_dict)
        assert len(context.stock_list) == 20

    def test_do_rebalance_stops_at_100_stocks(self, rq_globals):
        rq_globals['all_instruments'].return_value = pd.DataFrame({
            'order_book_id': [f"00000{i:03d}.XSHE" for i in range(200)]
        })
        def mock_history_bars(code, count, freq, fields):
            return np.array([(10.0,)], dtype=[('close', 'f8')])
        rq_globals['history_bars'].side_effect = mock_history_bars
        import importlib
        import attribution_a_working
        importlib.reload(attribution_a_working)
        context = MockContext()
        attribution_a_working.do_rebalance(context, {})
        assert rq_globals['history_bars'].call_count == 100


class TestEdgeCases:
    def test_do_rebalance_single_stock_selection(self, rq_globals):
        rq_globals['all_instruments'].return_value = pd.DataFrame({'order_book_id': ['000001.XSHE']})
        def mock_history_bars(code, count, freq, fields):
            return np.array([(10.0,)], dtype=[('close', 'f8')])
        rq_globals['history_bars'].side_effect = mock_history_bars
        import importlib
        import attribution_a_working
        importlib.reload(attribution_a_working)
        context = MockContext()
        bar_dict = {'000001.XSHE': MockBar()}
        attribution_a_working.do_rebalance(context, bar_dict)
        rq_globals['order_target_percent'].assert_called_with('000001.XSHE', 1.0)

    def test_handle_bar_month_transition_reset_flag(self, rq_globals):
        import importlib
        import attribution_a_working
        importlib.reload(attribution_a_working)
        context = MockContext()
        attribution_a_working.init(context)
        context.month = 7
        context.has_rebalanced = True
        context.now = datetime(2024, 8, 1, 10, 0)
        attribution_a_working.handle_bar(context, {})
        assert context.month == 8
        assert context.has_rebalanced == True