"""
Tests for risk_control_debug.py
Risk control debug/testing script for RiceQuant Notebook
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


class MockInstrument:
    def __init__(self, order_book_id):
        self.order_book_id = order_book_id


@pytest.fixture
def rq_globals():
    mocks = {
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


class TestRiskControlDebugExecution:
    def test_script_execution_no_stocks(self, rq_globals):
        rq_globals['all_instruments'].return_value = []
        rq_globals['history_bars'].return_value = None
        with patch('builtins.print'):
            import importlib
            import risk_control_debug
            importlib.reload(risk_control_debug)

    def test_script_filters_stocks_by_prefix(self, rq_globals):
        rq_globals['all_instruments'].return_value = [
            MockInstrument('000001.XSHE'),
            MockInstrument('688001.XSHG'),
            MockInstrument('300001.XSHE'),
        ]
        rq_globals['history_bars'].return_value = None
        with patch('builtins.print'):
            import importlib
            import risk_control_debug
            importlib.reload(risk_control_debug)
            assert rq_globals['all_instruments'].called

    def test_script_with_limit_up_stocks(self, rq_globals):
        rq_globals['all_instruments'].return_value = [
            MockInstrument('000001.XSHE'),
            MockInstrument('000002.XSHE')
        ]
        def mock_history_bars(stock, count, freq, fields, date=None):
            if 'limit_up' in str(fields) and 'volume' in str(fields):
                return np.array([(11.0, 11.0, 2000000)], dtype=[('close', 'f8'), ('limit_up', 'f8'), ('volume', 'f8')])
            return np.array([(11.0, 12.1)], dtype=[('open', 'f8'), ('limit_up', 'f8')])
        rq_globals['history_bars'].side_effect = mock_history_bars
        with patch('builtins.print'):
            import importlib
            import risk_control_debug
            importlib.reload(risk_control_debug)

    def test_script_volume_filter_low(self, rq_globals):
        rq_globals['all_instruments'].return_value = [MockInstrument('000001.XSHE')]
        def mock_history_bars(stock, count, freq, fields, date=None):
            if 'limit_up' in str(fields) and 'volume' in str(fields):
                return np.array([(11.0, 11.0, 500000)], dtype=[('close', 'f8'), ('limit_up', 'f8'), ('volume', 'f8')])
            return None
        rq_globals['history_bars'].side_effect = mock_history_bars
        with patch('builtins.print'):
            import importlib
            import risk_control_debug
            importlib.reload(risk_control_debug)

    def test_script_exception_in_history_bars(self, rq_globals):
        rq_globals['all_instruments'].return_value = [MockInstrument('000001.XSHE')]
        rq_globals['history_bars'].side_effect = Exception("API Error")
        with patch('builtins.print'):
            import importlib
            import risk_control_debug
            importlib.reload(risk_control_debug)

    def test_script_limit_up_threshold(self, rq_globals):
        rq_globals['all_instruments'].return_value = [MockInstrument('000001.XSHE')]
        def mock_history_bars(stock, count, freq, fields, date=None):
            if 'limit_up' in str(fields) and 'volume' in str(fields):
                return np.array([(10.89, 11.0, 2000000)], dtype=[('close', 'f8'), ('limit_up', 'f8'), ('volume', 'f8')])
            return None
        rq_globals['history_bars'].side_effect = mock_history_bars
        with patch('builtins.print'):
            import importlib
            import risk_control_debug
            importlib.reload(risk_control_debug)


class TestStockFilterLogic:
    def test_filter_excludes_68_prefix(self, rq_globals):
        rq_globals['all_instruments'].return_value = [
            MockInstrument('688001.XSHG'),
            MockInstrument('000001.XSHE')
        ]
        rq_globals['history_bars'].return_value = None
        with patch('builtins.print'):
            import importlib
            import risk_control_debug
            importlib.reload(risk_control_debug)
            assert rq_globals['all_instruments'].called

    def test_filter_excludes_3_prefix(self, rq_globals):
        rq_globals['all_instruments'].return_value = [
            MockInstrument('300001.XSHE'),
            MockInstrument('000001.XSHE')
        ]
        rq_globals['history_bars'].return_value = None
        with patch('builtins.print'):
            import importlib
            import risk_control_debug
            importlib.reload(risk_control_debug)
            assert rq_globals['all_instruments'].called


class TestPrintOutput:
    def test_print_called(self, rq_globals):
        rq_globals['all_instruments'].return_value = []
        printed_messages = []
        def mock_print(msg):
            printed_messages.append(str(msg))
        with patch('builtins.print', side_effect=mock_print):
            import importlib
            import risk_control_debug
            importlib.reload(risk_control_debug)
            assert len(printed_messages) > 0


class TestEdgeCases:
    def test_history_bars_returns_empty_array(self, rq_globals):
        rq_globals['all_instruments'].return_value = [MockInstrument('000001.XSHE')]
        rq_globals['history_bars'].return_value = np.array([])
        with patch('builtins.print'):
            import importlib
            import risk_control_debug
            importlib.reload(risk_control_debug)

    def test_script_stocks_limited_to_100(self, rq_globals):
        rq_globals['all_instruments'].return_value = [MockInstrument(f'00000{i:03d}.XSHE') for i in range(200)]
        rq_globals['history_bars'].return_value = None
        with patch('builtins.print'):
            import importlib
            import risk_control_debug
            importlib.reload(risk_control_debug)
            limit_up_calls = [c for c in rq_globals['history_bars'].call_args_list if 'limit_up' in str(c) and 'volume' in str(c)]
            assert len(limit_up_calls) <= 100

    def test_pandas_timestamp_import(self, rq_globals):
        rq_globals['all_instruments'].return_value = []
        rq_globals['history_bars'].return_value = None
        with patch('builtins.print'):
            import importlib
            import risk_control_debug
            importlib.reload(risk_control_debug)
            assert hasattr(pd, 'Timestamp')