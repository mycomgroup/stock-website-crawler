"""
Tests for attribution_a_simple_rq.py
Pure small cap market value factor strategy - simplified version
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


class MockScheduler:
    def __init__(self):
        self.scheduled_functions = []
    
    def run_monthly(self, func, day):
        self.scheduled_functions.append((func, day))


class MockContext:
    def __init__(self):
        self.now = datetime(2024, 7, 1, 10, 0)
        self.portfolio = MockPortfolio()
        self.stocks = []


class MockInstrument:
    def __init__(self, order_book_id):
        self.order_book_id = order_book_id


@pytest.fixture
def rq_globals():
    mocks = {
        'logger': Mock(),
        'scheduler': MockScheduler(),
        'order_target_percent': Mock(),
        'all_instruments': Mock(return_value=pd.DataFrame({'order_book_id': []})),
        'get_factor': Mock(return_value=None),
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
        import attribution_a_simple_rq
        importlib.reload(attribution_a_simple_rq)
        context = MockContext()
        attribution_a_simple_rq.init(context)
        assert context.stocks == []
        assert len(builtins.scheduler.scheduled_functions) == 1


class TestHandleBar:
    def test_handle_bar_pass(self, rq_globals):
        import importlib
        import attribution_a_simple_rq
        importlib.reload(attribution_a_simple_rq)
        context = MockContext()
        bar_dict = {}
        result = attribution_a_simple_rq.handle_bar(context, bar_dict)
        assert result is None


class TestRebalance:
    def test_rebalance_empty_stock_list(self, rq_globals):
        rq_globals['all_instruments'].return_value = pd.DataFrame({'order_book_id': []})
        rq_globals['get_factor'].return_value = None
        import importlib
        import attribution_a_simple_rq
        importlib.reload(attribution_a_simple_rq)
        context = MockContext()
        attribution_a_simple_rq.rebalance(context, {})
        rq_globals['order_target_percent'].assert_not_called()

    def test_rebalance_with_valid_stocks(self, rq_globals):
        rq_globals['all_instruments'].return_value = pd.DataFrame({
            'order_book_id': ['000001.XSHE', '000002.XSHE']
        })
        def mock_get_factor(stock, factor):
            caps = {'000001.XSHE': 100000000, '000002.XSHE': 50000000}
            return pd.DataFrame({'market_cap': [caps.get(stock, 100000)]})
        rq_globals['get_factor'].side_effect = mock_get_factor
        import importlib
        import attribution_a_simple_rq
        importlib.reload(attribution_a_simple_rq)
        context = MockContext()
        attribution_a_simple_rq.rebalance(context, {})
        assert rq_globals['order_target_percent'].call_count > 0

    def test_rebalance_factor_data_none(self, rq_globals):
        rq_globals['all_instruments'].return_value = pd.DataFrame({'order_book_id': ['000001.XSHE']})
        rq_globals['get_factor'].return_value = None
        import importlib
        import attribution_a_simple_rq
        importlib.reload(attribution_a_simple_rq)
        context = MockContext()
        attribution_a_simple_rq.rebalance(context, {})
        rq_globals['order_target_percent'].assert_not_called()

    def test_rebalance_factor_data_empty(self, rq_globals):
        rq_globals['all_instruments'].return_value = pd.DataFrame({'order_book_id': ['000001.XSHE']})
        rq_globals['get_factor'].return_value = pd.DataFrame()
        import importlib
        import attribution_a_simple_rq
        importlib.reload(attribution_a_simple_rq)
        context = MockContext()
        attribution_a_simple_rq.rebalance(context, {})
        rq_globals['order_target_percent'].assert_not_called()

    def test_rebalance_negative_market_cap_ignored(self, rq_globals):
        rq_globals['all_instruments'].return_value = pd.DataFrame({'order_book_id': ['000001.XSHE', '000002.XSHE']})
        def mock_get_factor(stock, factor):
            caps = {'000001.XSHE': -100000, '000002.XSHE': 50000000}
            return pd.DataFrame({'market_cap': [caps.get(stock, 100000)]})
        rq_globals['get_factor'].side_effect = mock_get_factor
        import importlib
        import attribution_a_simple_rq
        importlib.reload(attribution_a_simple_rq)
        context = MockContext()
        attribution_a_simple_rq.rebalance(context, {})
        rq_globals['order_target_percent'].assert_called_with('000002.XSHE', 1.0)

    def test_rebalance_zero_market_cap_ignored(self, rq_globals):
        rq_globals['all_instruments'].return_value = pd.DataFrame({'order_book_id': ['000001.XSHE', '000002.XSHE']})
        def mock_get_factor(stock, factor):
            caps = {'000001.XSHE': 0, '000002.XSHE': 50000000}
            return pd.DataFrame({'market_cap': [caps.get(stock, 100000)]})
        rq_globals['get_factor'].side_effect = mock_get_factor
        import importlib
        import attribution_a_simple_rq
        importlib.reload(attribution_a_simple_rq)
        context = MockContext()
        attribution_a_simple_rq.rebalance(context, {})
        rq_globals['order_target_percent'].assert_called_with('000002.XSHE', 1.0)

    def test_rebalance_clears_old_positions(self, rq_globals):
        rq_globals['all_instruments'].return_value = pd.DataFrame({'order_book_id': ['000001.XSHE']})
        rq_globals['get_factor'].return_value = pd.DataFrame({'market_cap': [100000000]})
        import importlib
        import attribution_a_simple_rq
        importlib.reload(attribution_a_simple_rq)
        context = MockContext()
        context.portfolio.positions = {'999999.XSHG': Mock()}
        attribution_a_simple_rq.rebalance(context, {})
        rq_globals['order_target_percent'].assert_any_call('999999.XSHG', 0)

    def test_rebalance_selects_smallest_cap(self, rq_globals):
        rq_globals['all_instruments'].return_value = pd.DataFrame({
            'order_book_id': ['000001.XSHE', '000002.XSHE', '600000.XSHG']
        })
        caps = {'000001.XSHE': 100000000, '000002.XSHE': 50000000, '600000.XSHG': 200000000}
        def mock_get_factor(stock, factor):
            return pd.DataFrame({'market_cap': [caps.get(stock, 100000)]})
        rq_globals['get_factor'].side_effect = mock_get_factor
        import importlib
        import attribution_a_simple_rq
        importlib.reload(attribution_a_simple_rq)
        context = MockContext()
        attribution_a_simple_rq.rebalance(context, {})
        assert context.stocks[:2] == ['000002.XSHE', '000001.XSHE']

    def test_rebalance_limits_to_20_stocks(self, rq_globals):
        rq_globals['all_instruments'].return_value = pd.DataFrame({
            'order_book_id': [f"00000{i:03d}.XSHE" for i in range(250)]
        })
        rq_globals['get_factor'].return_value = pd.DataFrame({'market_cap': [10000000]})
        import importlib
        import attribution_a_simple_rq
        importlib.reload(attribution_a_simple_rq)
        context = MockContext()
        attribution_a_simple_rq.rebalance(context, {})
        buy_calls = [c for c in rq_globals['order_target_percent'].call_args_list if c[0][1] > 0]
        assert len(buy_calls) == 20

    def test_rebalance_exception_in_get_factor_handled(self, rq_globals):
        rq_globals['all_instruments'].return_value = pd.DataFrame({'order_book_id': ['000001.XSHE', '000002.XSHE']})
        def mock_get_factor(stock, factor):
            if stock == '000001.XSHE':
                raise Exception("API Error")
            return pd.DataFrame({'market_cap': [50000000]})
        rq_globals['get_factor'].side_effect = mock_get_factor
        import importlib
        import attribution_a_simple_rq
        importlib.reload(attribution_a_simple_rq)
        context = MockContext()
        attribution_a_simple_rq.rebalance(context, {})
        rq_globals['order_target_percent'].assert_called_with('000002.XSHE', 1.0)


class TestEdgeCases:
    def test_rebalance_single_stock_selection(self, rq_globals):
        rq_globals['all_instruments'].return_value = pd.DataFrame({'order_book_id': ['000001.XSHE']})
        rq_globals['get_factor'].return_value = pd.DataFrame({'market_cap': [100000000]})
        import importlib
        import attribution_a_simple_rq
        importlib.reload(attribution_a_simple_rq)
        context = MockContext()
        attribution_a_simple_rq.rebalance(context, {})
        rq_globals['order_target_percent'].assert_called_with('000001.XSHE', 1.0)

    def test_rebalance_stocks_limited_to_500(self, rq_globals):
        rq_globals['all_instruments'].return_value = pd.DataFrame({
            'order_book_id': [f"00000{i:03d}.XSHE" for i in range(1000)]
        })
        rq_globals['get_factor'].return_value = pd.DataFrame({'market_cap': [10000000]})
        import importlib
        import attribution_a_simple_rq
        importlib.reload(attribution_a_simple_rq)
        context = MockContext()
        attribution_a_simple_rq.rebalance(context, {})
        assert rq_globals['get_factor'].call_count <= 500