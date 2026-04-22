"""
Tests for risk_control_baseline_rq.py
Risk control baseline version (A group)
"""
import sys
import builtins
from pathlib import Path
import pytest
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from unittest.mock import MagicMock, patch, Mock

sys.path.insert(0, str(Path(__file__).parent.parent))


class MockBar:
    def __init__(self, close=10.0, open_price=9.5, is_trading=True, limit_up=11.0, last=10.0):
        self.close = close
        self.open = open_price
        self.is_trading = is_trading
        self.limit_up = limit_up
        self.last = last


class MockPosition:
    def __init__(self, quantity=100):
        self.quantity = quantity


class MockPortfolio:
    def __init__(self):
        self.positions = {}


class MockContext:
    def __init__(self):
        self.now = datetime(2024, 7, 1, 14, 50)
        self.portfolio = MockPortfolio()
        self.month_count = 0
        self.last_month = None
        self.trades_count = 0


class MockInstrument:
    def __init__(self, order_book_id):
        self.order_book_id = order_book_id


@pytest.fixture
def rq_globals():
    mocks = {
        'order_target_percent': Mock(),
        'all_instruments': Mock(return_value=[]),
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
        import risk_control_baseline_rq
        importlib.reload(risk_control_baseline_rq)
        context = MockContext()
        risk_control_baseline_rq.init(context)
        assert context.month_count == 0
        assert context.last_month is None
        assert context.trades_count == 0


class TestHandleBar:
    def test_handle_bar_first_call_rebalance(self, rq_globals):
        import importlib
        import risk_control_baseline_rq
        importlib.reload(risk_control_baseline_rq)
        context = MockContext()
        risk_control_baseline_rq.init(context)
        context.now = datetime(2024, 7, 1, 10, 0)
        with patch.object(risk_control_baseline_rq, 'rebalance') as mock_rebalance:
            risk_control_baseline_rq.handle_bar(context, {})
            mock_rebalance.assert_called_once()
            assert context.month_count == 1

    def test_handle_bar_same_month_no_rebalance(self, rq_globals):
        import importlib
        import risk_control_baseline_rq
        importlib.reload(risk_control_baseline_rq)
        context = MockContext()
        risk_control_baseline_rq.init(context)
        context.month_count = 1
        context.last_month = 7
        context.now = datetime(2024, 7, 15, 10, 0)
        with patch.object(risk_control_baseline_rq, 'rebalance') as mock_rebalance:
            risk_control_baseline_rq.handle_bar(context, {})
            mock_rebalance.assert_not_called()

    def test_handle_bar_new_month_rebalance(self, rq_globals):
        import importlib
        import risk_control_baseline_rq
        importlib.reload(risk_control_baseline_rq)
        context = MockContext()
        risk_control_baseline_rq.init(context)
        context.month_count = 1
        context.last_month = 7
        context.now = datetime(2024, 8, 1, 10, 0)
        with patch.object(risk_control_baseline_rq, 'rebalance') as mock_rebalance:
            risk_control_baseline_rq.handle_bar(context, {})
            mock_rebalance.assert_called_once()
            assert context.last_month == 8

    def test_handle_bar_late_day_near_limit_up_no_clear(self, rq_globals):
        import importlib
        import risk_control_baseline_rq
        importlib.reload(risk_control_baseline_rq)
        context = MockContext()
        risk_control_baseline_rq.init(context)
        context.month_count = 1
        context.last_month = 7
        context.now = datetime(2024, 7, 15, 14, 50)
        context.portfolio.positions = {'000001.XSHE': MockPosition(quantity=100)}
        bar_dict = {'000001.XSHE': MockBar(last=10.995, limit_up=11.0)}
        risk_control_baseline_rq.handle_bar(context, bar_dict)
        clear_calls = [c for c in rq_globals['order_target_percent'].call_args_list if c[0][1] == 0]
        assert len(clear_calls) == 0

    def test_handle_bar_before_late_day_no_clear(self, rq_globals):
        import importlib
        import risk_control_baseline_rq
        importlib.reload(risk_control_baseline_rq)
        context = MockContext()
        risk_control_baseline_rq.init(context)
        context.month_count = 1
        context.last_month = 7
        context.now = datetime(2024, 7, 15, 14, 30)
        context.portfolio.positions = {'000001.XSHE': MockPosition(quantity=100)}
        bar_dict = {'000001.XSHE': MockBar(last=10.0, limit_up=11.0)}
        risk_control_baseline_rq.handle_bar(context, bar_dict)
        clear_calls = [c for c in rq_globals['order_target_percent'].call_args_list if c[0][1] == 0]
        assert len(clear_calls) == 0


class TestRebalance:
    def test_rebalance_no_limit_up_stocks(self, rq_globals):
        rq_globals['all_instruments'].return_value = [MockInstrument('000001.XSHE')]
        rq_globals['history_bars'].return_value = None
        import importlib
        import risk_control_baseline_rq
        importlib.reload(risk_control_baseline_rq)
        context = MockContext()
        context.month_count = 0
        risk_control_baseline_rq.rebalance(context, {})
        rq_globals['order_target_percent'].assert_not_called()

    def test_rebalance_volume_filter(self, rq_globals):
        rq_globals['all_instruments'].return_value = [MockInstrument('000001.XSHE')]
        def mock_history_bars(stock, count, freq, fields, date=None):
            if 'limit_up' in str(fields) and 'volume' in str(fields):
                return np.array([(11.0, 11.0, 500000)], dtype=[('close', 'f8'), ('limit_up', 'f8'), ('volume', 'f8')])
            return None
        rq_globals['history_bars'].side_effect = mock_history_bars
        import importlib
        import risk_control_baseline_rq
        importlib.reload(risk_control_baseline_rq)
        context = MockContext()
        context.month_count = 0
        risk_control_baseline_rq.rebalance(context, {})
        buy_calls = [c for c in rq_globals['order_target_percent'].call_args_list if c[0][1] > 0]
        assert len(buy_calls) == 0

    def test_rebalance_limit_up_threshold(self, rq_globals):
        rq_globals['all_instruments'].return_value = [MockInstrument('000001.XSHE')]
        def mock_history_bars(stock, count, freq, fields, date=None):
            if 'limit_up' in str(fields) and 'volume' in str(fields):
                return np.array([(10.89, 11.0, 2000000)], dtype=[('close', 'f8'), ('limit_up', 'f8'), ('volume', 'f8')])
            return None
        rq_globals['history_bars'].side_effect = mock_history_bars
        import importlib
        import risk_control_baseline_rq
        importlib.reload(risk_control_baseline_rq)
        context = MockContext()
        context.month_count = 0
        risk_control_baseline_rq.rebalance(context, {})
        buy_calls = [c for c in rq_globals['order_target_percent'].call_args_list if c[0][1] > 0]
        assert len(buy_calls) == 0

    def test_rebalance_with_limit_up_stocks(self, rq_globals):
        rq_globals['all_instruments'].return_value = [MockInstrument('000001.XSHE')]
        def mock_history_bars(stock, count, freq, fields, date=None):
            if 'limit_up' in str(fields) and 'volume' in str(fields):
                return np.array([(11.0, 11.0, 2000000)], dtype=[('close', 'f8'), ('limit_up', 'f8'), ('volume', 'f8')])
            return np.array([(11.0, 12.1)], dtype=[('open', 'f8'), ('limit_up', 'f8')])
        rq_globals['history_bars'].side_effect = mock_history_bars
        import importlib
        import risk_control_baseline_rq
        importlib.reload(risk_control_baseline_rq)
        context = MockContext()
        context.month_count = 0
        risk_control_baseline_rq.rebalance(context, {})
        assert rq_globals['history_bars'].call_count > 0

    def test_rebalance_limits_to_3_stocks(self, rq_globals):
        rq_globals['all_instruments'].return_value = [MockInstrument(f'00000{i}.XSHE') for i in range(1, 6)]
        def mock_history_bars(stock, count, freq, fields, date=None):
            if 'limit_up' in str(fields) and 'volume' in str(fields):
                return np.array([(11.0, 11.0, 2000000)], dtype=[('close', 'f8'), ('limit_up', 'f8'), ('volume', 'f8')])
            return np.array([(10.5, 12.1)], dtype=[('open', 'f8'), ('limit_up', 'f8')])
        rq_globals['history_bars'].side_effect = mock_history_bars
        import importlib
        import risk_control_baseline_rq
        importlib.reload(risk_control_baseline_rq)
        context = MockContext()
        context.month_count = 0
        risk_control_baseline_rq.rebalance(context, {})
        buy_calls = [c for c in rq_globals['order_target_percent'].call_args_list if c[0][1] > 0]
        assert len(buy_calls) <= 3

    def test_rebalance_exception_handled(self, rq_globals):
        rq_globals['all_instruments'].return_value = [MockInstrument('000001.XSHE')]
        rq_globals['history_bars'].side_effect = Exception("API Error")
        import importlib
        import risk_control_baseline_rq
        importlib.reload(risk_control_baseline_rq)
        context = MockContext()
        context.month_count = 0
        risk_control_baseline_rq.rebalance(context, {})
        rq_globals['order_target_percent'].assert_not_called()

    def test_rebalance_limit_up_zero(self, rq_globals):
        rq_globals['all_instruments'].return_value = [MockInstrument('000001.XSHE')]
        def mock_history_bars(stock, count, freq, fields, date=None):
            return np.array([(10.0, 0, 2000000)], dtype=[('close', 'f8'), ('limit_up', 'f8'), ('volume', 'f8')])
        rq_globals['history_bars'].side_effect = mock_history_bars
        import importlib
        import risk_control_baseline_rq
        importlib.reload(risk_control_baseline_rq)
        context = MockContext()
        context.month_count = 0
        risk_control_baseline_rq.rebalance(context, {})
        buy_calls = [c for c in rq_globals['order_target_percent'].call_args_list if c[0][1] > 0]
        assert len(buy_calls) == 0


class TestEdgeCases:
    def test_handle_bar_time_boundary_14_49(self, rq_globals):
        import importlib
        import risk_control_baseline_rq
        importlib.reload(risk_control_baseline_rq)
        context = MockContext()
        risk_control_baseline_rq.init(context)
        context.month_count = 1
        context.last_month = 7
        context.now = datetime(2024, 7, 15, 14, 49)
        context.portfolio.positions = {'000001.XSHE': MockPosition(quantity=100)}
        bar_dict = {'000001.XSHE': MockBar(last=10.0, limit_up=11.0)}
        risk_control_baseline_rq.handle_bar(context, bar_dict)
        clear_calls = [c for c in rq_globals['order_target_percent'].call_args_list if c[0][1] == 0]
        assert len(clear_calls) == 0

    def test_rebalance_stocks_limited_to_200(self, rq_globals):
        rq_globals['all_instruments'].return_value = [MockInstrument(f'00000{i:03d}.XSHE') for i in range(300)]
        rq_globals['history_bars'].return_value = None
        import importlib
        import risk_control_baseline_rq
        importlib.reload(risk_control_baseline_rq)
        context = MockContext()
        context.month_count = 0
        risk_control_baseline_rq.rebalance(context, {})
        limit_up_calls = [c for c in rq_globals['history_bars'].call_args_list if 'limit_up' in str(c)]
        assert len(limit_up_calls) <= 200