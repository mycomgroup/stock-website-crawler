"""
Tests for attribution_a_ultra_simple.py
Ultra simplified small cap market value factor strategy
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
        self.rebalance_day = 1


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
        import attribution_a_ultra_simple
        importlib.reload(attribution_a_ultra_simple)
        context = MockContext()
        attribution_a_ultra_simple.init(context)
        assert context.stock_list == []
        assert context.rebalance_day == 1


class TestBeforeTrading:
    def test_before_trading_on_rebalance_day(self, rq_globals):
        import importlib
        import attribution_a_ultra_simple
        importlib.reload(attribution_a_ultra_simple)
        context = MockContext()
        context.now = datetime(2024, 7, 1, 9, 30)
        with patch.object(attribution_a_ultra_simple, 'do_rebalance') as mock_rebalance:
            attribution_a_ultra_simple.before_trading(context)
            mock_rebalance.assert_called_once_with(context)

    def test_before_trading_not_on_rebalance_day(self, rq_globals):
        import importlib
        import attribution_a_ultra_simple
        importlib.reload(attribution_a_ultra_simple)
        context = MockContext()
        context.now = datetime(2024, 7, 15, 9, 30)
        with patch.object(attribution_a_ultra_simple, 'do_rebalance') as mock_rebalance:
            attribution_a_ultra_simple.before_trading(context)
            mock_rebalance.assert_not_called()

    def test_before_trading_custom_rebalance_day(self, rq_globals):
        import importlib
        import attribution_a_ultra_simple
        importlib.reload(attribution_a_ultra_simple)
        context = MockContext()
        context.rebalance_day = 15
        context.now = datetime(2024, 7, 15, 9, 30)
        with patch.object(attribution_a_ultra_simple, 'do_rebalance') as mock_rebalance:
            attribution_a_ultra_simple.before_trading(context)
            mock_rebalance.assert_called_once_with(context)


class TestDoRebalance:
    def test_do_rebalance_empty_stock_list(self, rq_globals):
        rq_globals['all_instruments'].return_value = pd.DataFrame({'order_book_id': []})
        rq_globals['history_bars'].return_value = None
        import importlib
        import attribution_a_ultra_simple
        importlib.reload(attribution_a_ultra_simple)
        context = MockContext()
        attribution_a_ultra_simple.do_rebalance(context)
        rq_globals['order_target_percent'].assert_not_called()

    def test_do_rebalance_with_valid_stocks(self, rq_globals):
        rq_globals['all_instruments'].return_value = pd.DataFrame({
            'order_book_id': ['000001.XSHE', '000002.XSHE']
        })
        def mock_history_bars(code, count, freq, fields):
            return np.array([(10.0,)], dtype=[('close', 'f8')])
        rq_globals['history_bars'].side_effect = mock_history_bars
        import importlib
        import attribution_a_ultra_simple
        importlib.reload(attribution_a_ultra_simple)
        context = MockContext()
        attribution_a_ultra_simple.do_rebalance(context)
        assert rq_globals['order_target_percent'].call_count > 0

    def test_do_rebalance_clears_old_positions(self, rq_globals):
        rq_globals['all_instruments'].return_value = pd.DataFrame({'order_book_id': ['000001.XSHE']})
        def mock_history_bars(code, count, freq, fields):
            return np.array([(10.0,)], dtype=[('close', 'f8')])
        rq_globals['history_bars'].side_effect = mock_history_bars
        import importlib
        import attribution_a_ultra_simple
        importlib.reload(attribution_a_ultra_simple)
        context = MockContext()
        context.portfolio.positions = {'999999.XSHG': Mock()}
        attribution_a_ultra_simple.do_rebalance(context)
        rq_globals['order_target_percent'].assert_any_call('999999.XSHG', 0)

    def test_do_rebalance_history_bars_none(self, rq_globals):
        rq_globals['all_instruments'].return_value = pd.DataFrame({'order_book_id': ['000001.XSHE']})
        rq_globals['history_bars'].return_value = None
        import importlib
        import attribution_a_ultra_simple
        importlib.reload(attribution_a_ultra_simple)
        context = MockContext()
        attribution_a_ultra_simple.do_rebalance(context)
        rq_globals['order_target_percent'].assert_not_called()

    def test_do_rebalance_history_bars_empty(self, rq_globals):
        rq_globals['all_instruments'].return_value = pd.DataFrame({'order_book_id': ['000001.XSHE']})
        rq_globals['history_bars'].return_value = np.array([])
        import importlib
        import attribution_a_ultra_simple
        importlib.reload(attribution_a_ultra_simple)
        context = MockContext()
        attribution_a_ultra_simple.do_rebalance(context)
        rq_globals['order_target_percent'].assert_not_called()

    def test_do_rebalance_zero_price_ignored(self, rq_globals):
        rq_globals['all_instruments'].return_value = pd.DataFrame({'order_book_id': ['000001.XSHE', '000002.XSHE']})
        def mock_history_bars(code, count, freq, fields):
            if code == '000001.XSHE':
                return np.array([(0.0,)], dtype=[('close', 'f8')])
            return np.array([(10.0,)], dtype=[('close', 'f8')])
        rq_globals['history_bars'].side_effect = mock_history_bars
        import importlib
        import attribution_a_ultra_simple
        importlib.reload(attribution_a_ultra_simple)
        context = MockContext()
        attribution_a_ultra_simple.do_rebalance(context)
        assert '000001.XSHE' not in context.stock_list

    def test_do_rebalance_negative_price_ignored(self, rq_globals):
        rq_globals['all_instruments'].return_value = pd.DataFrame({'order_book_id': ['000001.XSHE', '000002.XSHE']})
        def mock_history_bars(code, count, freq, fields):
            if code == '000001.XSHE':
                return np.array([(-5.0,)], dtype=[('close', 'f8')])
            return np.array([(10.0,)], dtype=[('close', 'f8')])
        rq_globals['history_bars'].side_effect = mock_history_bars
        import importlib
        import attribution_a_ultra_simple
        importlib.reload(attribution_a_ultra_simple)
        context = MockContext()
        attribution_a_ultra_simple.do_rebalance(context)
        assert '000001.XSHE' not in context.stock_list

    def test_do_rebalance_exception_in_history_bars_handled(self, rq_globals):
        rq_globals['all_instruments'].return_value = pd.DataFrame({'order_book_id': ['000001.XSHE', '000002.XSHE']})
        def mock_history_bars(code, count, freq, fields):
            if code == '000001.XSHE':
                raise Exception("API Error")
            return np.array([(10.0,)], dtype=[('close', 'f8')])
        rq_globals['history_bars'].side_effect = mock_history_bars
        import importlib
        import attribution_a_ultra_simple
        importlib.reload(attribution_a_ultra_simple)
        context = MockContext()
        attribution_a_ultra_simple.do_rebalance(context)
        assert len(context.stock_list) == 1

    def test_do_rebalance_selects_lowest_price(self, rq_globals):
        rq_globals['all_instruments'].return_value = pd.DataFrame({
            'order_book_id': ['000001.XSHE', '000002.XSHE', '000003.XSHE']
        })
        def mock_history_bars(code, count, freq, fields):
            prices = {'000001.XSHE': 30.0, '000002.XSHE': 10.0, '000003.XSHE': 5.0}
            return np.array([(prices[code],)], dtype=[('close', 'f8')])
        rq_globals['history_bars'].side_effect = mock_history_bars
        import importlib
        import attribution_a_ultra_simple
        importlib.reload(attribution_a_ultra_simple)
        context = MockContext()
        attribution_a_ultra_simple.do_rebalance(context)
        assert context.stock_list[0] == '000003.XSHE'

    def test_do_rebalance_limits_to_20_stocks(self, rq_globals):
        rq_globals['all_instruments'].return_value = pd.DataFrame({
            'order_book_id': [f"00000{i:03d}.XSHE" for i in range(150)]
        })
        def mock_history_bars(code, count, freq, fields):
            return np.array([(10.0,)], dtype=[('close', 'f8')])
        rq_globals['history_bars'].side_effect = mock_history_bars
        import importlib
        import attribution_a_ultra_simple
        importlib.reload(attribution_a_ultra_simple)
        context = MockContext()
        attribution_a_ultra_simple.do_rebalance(context)
        assert len(context.stock_list) == 20

    def test_do_rebalance_stops_at_100_stocks(self, rq_globals):
        rq_globals['all_instruments'].return_value = pd.DataFrame({
            'order_book_id': [f"00000{i:03d}.XSHE" for i in range(200)]
        })
        def mock_history_bars(code, count, freq, fields):
            return np.array([(10.0,)], dtype=[('close', 'f8')])
        rq_globals['history_bars'].side_effect = mock_history_bars
        import importlib
        import attribution_a_ultra_simple
        importlib.reload(attribution_a_ultra_simple)
        context = MockContext()
        attribution_a_ultra_simple.do_rebalance(context)
        assert rq_globals['history_bars'].call_count == 100

    def test_do_rebalance_single_stock_selection(self, rq_globals):
        rq_globals['all_instruments'].return_value = pd.DataFrame({'order_book_id': ['000001.XSHE']})
        def mock_history_bars(code, count, freq, fields):
            return np.array([(10.0,)], dtype=[('close', 'f8')])
        rq_globals['history_bars'].side_effect = mock_history_bars
        import importlib
        import attribution_a_ultra_simple
        importlib.reload(attribution_a_ultra_simple)
        context = MockContext()
        attribution_a_ultra_simple.do_rebalance(context)
        rq_globals['order_target_percent'].assert_called_with('000001.XSHE', 1.0)


class TestHandleBar:
    def test_handle_bar_pass(self, rq_globals):
        import importlib
        import attribution_a_ultra_simple
        importlib.reload(attribution_a_ultra_simple)
        context = MockContext()
        bar_dict = {}
        result = attribution_a_ultra_simple.handle_bar(context, bar_dict)
        assert result is None


class TestEdgeCases:
    def test_do_rebalance_sorted_by_price(self, rq_globals):
        rq_globals['all_instruments'].return_value = pd.DataFrame({
            'order_book_id': ['000003.XSHE', '000001.XSHE', '000002.XSHE']
        })
        def mock_history_bars(code, count, freq, fields):
            prices = {'000001.XSHE': 30.0, '000002.XSHE': 10.0, '000003.XSHE': 5.0}
            return np.array([(prices[code],)], dtype=[('close', 'f8')])
        rq_globals['history_bars'].side_effect = mock_history_bars
        import importlib
        import attribution_a_ultra_simple
        importlib.reload(attribution_a_ultra_simple)
        context = MockContext()
        attribution_a_ultra_simple.do_rebalance(context)
        assert context.stock_list[0] == '000003.XSHE'