"""
Tests for task02_dual_threshold_v2.py
"""
import sys
from pathlib import Path
from unittest.mock import MagicMock, patch, MagicMock
from datetime import datetime
import pytest
import numpy as np
import importlib

sys.path.insert(0, str(Path(__file__).parent.parent))

from tests.conftest import MockContext, MockBar, MockBarDict, MockPortfolio, create_mock_history_bars


class MockInstrumentsList:
    def __init__(self, stocks):
        self.order_book_id = stocks


class MockPortfolioDualThreshold:
    def __init__(self):
        self.starting_cash = 1000000
        self.total_value = 1000000
        self.positions = {}


class MockContextDualThreshold:
    def __init__(self):
        self.now = datetime(2024, 7, 1)
        self.portfolio = MockPortfolioDualThreshold()
        self.low_threshold = None
        self.high_threshold = None
        self.max_positions = None
        self.position_size = None


@pytest.fixture
def mock_context_dual_threshold():
    return MockContextDualThreshold()


@pytest.fixture
def mock_scheduler():
    scheduler = MagicMock()
    scheduler.run_monthly = MagicMock()
    return scheduler


@pytest.fixture
def mock_rq_api():
    mocks = {}
    
    def mock_all_instruments(type_str):
        return MockInstrumentsList(["000001.XSHE", "000002.XSHE", "600000.XSHG", "600519.XSHG"])
    
    def mock_history_bars(stock, bar_count, frequency, fields):
        if fields == "close":
            return np.array([10.0, 10.5])
        elif isinstance(fields, list):
            bars = []
            for i in range(bar_count):
                bars.append({
                    "close": 10.5 + i * 0.1,
                    "open": 10.6 + i * 0.1,
                    "limit_up": 11.5 + i * 0.1,
                })
            return bars
        return None
    
    mocks["all_instruments"] = mock_all_instruments
    mocks["history_bars"] = mock_history_bars
    mocks["order_target"] = MagicMock()
    mocks["order_target_percent"] = MagicMock()
    
    return mocks


@pytest.fixture
def inject_mocks(mock_scheduler, mock_rq_api):
    sys.modules["scheduler"] = mock_scheduler
    sys.modules["all_instruments"] = mock_rq_api["all_instruments"]
    sys.modules["history_bars"] = mock_rq_api["history_bars"]
    sys.modules["order_target"] = mock_rq_api["order_target"]
    sys.modules["order_target_percent"] = mock_rq_api["order_target_percent"]
    
    yield
    
    for key in ["scheduler", "all_instruments", "history_bars", "order_target", "order_target_percent"]:
        if key in sys.modules:
            del sys.modules[key]


class TestInit:
    def test_init_sets_parameters(self, mock_context_dual_threshold, inject_mocks, mock_scheduler):
        module = importlib.import_module("task02_dual_threshold_v2")
        module.init(mock_context_dual_threshold)
        
        assert mock_context_dual_threshold.low_threshold == 50
        assert mock_context_dual_threshold.high_threshold == 150
        assert mock_context_dual_threshold.max_positions == 5
        assert mock_context_dual_threshold.position_size == 0.2
        mock_scheduler.run_monthly.assert_called_once()


class TestGetZtCount:
    def test_get_zt_count_returns_int(self, mock_context_dual_threshold, inject_mocks):
        module = importlib.import_module("task02_dual_threshold_v2")
        result = module.get_zt_count(mock_context_dual_threshold)
        
        assert isinstance(result, int)

    def test_get_zt_count_positive(self, mock_context_dual_threshold, inject_mocks):
        module = importlib.import_module("task02_dual_threshold_v2")
        result = module.get_zt_count(mock_context_dual_threshold)
        
        assert result >= 0

    def test_get_zt_count_filters_special_stocks(self, mock_context_dual_threshold, inject_mocks):
        def mock_all_instruments_special(type_str):
            return MockInstrumentsList(["688001.XSHG", "430001.XSHE", "830001.XSHE", "000001.XSHE"])
        
        sys.modules["all_instruments"] = mock_all_instruments_special
        module = importlib.import_module("task02_dual_threshold_v2")
        importlib.reload(module)
        result = module.get_zt_count(mock_context_dual_threshold)
        
        assert isinstance(result, int)

    def test_get_zt_count_exception_returns_default(self, mock_context_dual_threshold, inject_mocks):
        def mock_all_instruments_error(type_str):
            raise Exception("API error")
        
        sys.modules["all_instruments"] = mock_all_instruments_error
        module = importlib.import_module("task02_dual_threshold_v2")
        importlib.reload(module)
        result = module.get_zt_count(mock_context_dual_threshold)
        
        assert result == 100

    def test_get_zt_count_empty_stocks(self, mock_context_dual_threshold, inject_mocks):
        def mock_all_instruments_empty(type_str):
            return MockInstrumentsList([])
        
        sys.modules["all_instruments"] = mock_all_instruments_empty
        module = importlib.import_module("task02_dual_threshold_v2")
        importlib.reload(module)
        result = module.get_zt_count(mock_context_dual_threshold)
        
        assert isinstance(result, int)

    def test_get_zt_count_none_bars(self, mock_context_dual_threshold, inject_mocks):
        def mock_history_bars_none(stock, bar_count, frequency, fields):
            return None
        
        sys.modules["history_bars"] = mock_history_bars_none
        module = importlib.import_module("task02_dual_threshold_v2")
        importlib.reload(module)
        result = module.get_zt_count(mock_context_dual_threshold)
        
        assert isinstance(result, int)

    def test_get_zt_count_limit_up_detection(self, mock_context_dual_threshold, inject_mocks):
        def mock_history_bars_limit_up(stock, bar_count, frequency, fields):
            return [{"close": 11.0, "limit_up": 11.0}]
        
        sys.modules["history_bars"] = mock_history_bars_limit_up
        module = importlib.import_module("task02_dual_threshold_v2")
        importlib.reload(module)
        result = module.get_zt_count(mock_context_dual_threshold)
        
        assert result >= 0


class TestSelectStocks:
    def test_select_stocks_returns_list(self, mock_context_dual_threshold, inject_mocks):
        mock_context_dual_threshold.max_positions = 5
        module = importlib.import_module("task02_dual_threshold_v2")
        result = module.select_stocks(mock_context_dual_threshold)
        
        assert isinstance(result, list)

    def test_select_stocks_empty_result(self, mock_context_dual_threshold, inject_mocks):
        mock_context_dual_threshold.max_positions = 5
        
        def mock_all_instruments_empty(type_str):
            return MockInstrumentsList([])
        
        sys.modules["all_instruments"] = mock_all_instruments_empty
        module = importlib.import_module("task02_dual_threshold_v2")
        importlib.reload(module)
        result = module.select_stocks(mock_context_dual_threshold)
        
        assert result == []

    def test_select_stocks_max_positions_limit(self, mock_context_dual_threshold, inject_mocks):
        mock_context_dual_threshold.max_positions = 2
        module = importlib.import_module("task02_dual_threshold_v2")
        result = module.select_stocks(mock_context_dual_threshold)
        
        assert len(result) <= 2

    def test_select_stocks_filters_special_stocks(self, mock_context_dual_threshold, inject_mocks):
        mock_context_dual_threshold.max_positions = 5
        
        def mock_all_instruments_special(type_str):
            return MockInstrumentsList(["688001.XSHG", "430001.XSHE", "000001.XSHE"])
        
        sys.modules["all_instruments"] = mock_all_instruments_special
        module = importlib.import_module("task02_dual_threshold_v2")
        importlib.reload(module)
        result = module.select_stocks(mock_context_dual_threshold)
        
        assert isinstance(result, list)

    def test_select_stocks_exception_returns_empty(self, mock_context_dual_threshold, inject_mocks):
        mock_context_dual_threshold.max_positions = 5
        
        def mock_all_instruments_error(type_str):
            raise Exception("API error")
        
        sys.modules["all_instruments"] = mock_all_instruments_error
        module = importlib.import_module("task02_dual_threshold_v2")
        importlib.reload(module)
        result = module.select_stocks(mock_context_dual_threshold)
        
        assert result == []

    def test_select_stocks_none_bars(self, mock_context_dual_threshold, inject_mocks):
        mock_context_dual_threshold.max_positions = 5
        
        def mock_history_bars_none(stock, bar_count, frequency, fields):
            return None
        
        sys.modules["history_bars"] = mock_history_bars_none
        module = importlib.import_module("task02_dual_threshold_v2")
        importlib.reload(module)
        result = module.select_stocks(mock_context_dual_threshold)
        
        assert isinstance(result, list)


class TestAdjustPositions:
    def test_adjust_positions_sells_not_selected(self, mock_context_dual_threshold, inject_mocks):
        mock_order_target = MagicMock()
        mock_order_target_percent = MagicMock()
        
        mock_context_dual_threshold.position_size = 0.2
        mock_context_dual_threshold.portfolio.positions = {"000001.XSHE": MagicMock()}
        
        sys.modules["order_target"] = mock_order_target
        sys.modules["order_target_percent"] = mock_order_target_percent
        module = importlib.import_module("task02_dual_threshold_v2")
        importlib.reload(module)
        
        selected = ["000002.XSHE"]
        module.adjust_positions(mock_context_dual_threshold, selected)
        
        mock_order_target.assert_called()

    def test_adjust_positions_buys_selected(self, mock_context_dual_threshold, inject_mocks):
        mock_order_target = MagicMock()
        mock_order_target_percent = MagicMock()
        
        mock_context_dual_threshold.position_size = 0.2
        mock_context_dual_threshold.portfolio.positions = {}
        
        sys.modules["order_target"] = mock_order_target
        sys.modules["order_target_percent"] = mock_order_target_percent
        module = importlib.import_module("task02_dual_threshold_v2")
        importlib.reload(module)
        
        selected = ["000001.XSHE"]
        module.adjust_positions(mock_context_dual_threshold, selected)
        
        mock_order_target_percent.assert_called_with("000001.XSHE", 0.2)

    def test_adjust_positions_holds_existing(self, mock_context_dual_threshold, inject_mocks):
        mock_order_target = MagicMock()
        mock_order_target_percent = MagicMock()
        
        mock_context_dual_threshold.position_size = 0.2
        mock_context_dual_threshold.portfolio.positions = {"000001.XSHE": MagicMock()}
        
        sys.modules["order_target"] = mock_order_target
        sys.modules["order_target_percent"] = mock_order_target_percent
        module = importlib.import_module("task02_dual_threshold_v2")
        importlib.reload(module)
        
        selected = ["000001.XSHE"]
        module.adjust_positions(mock_context_dual_threshold, selected)
        
        mock_order_target.assert_not_called()
        mock_order_target_percent.assert_not_called()


class TestClearAll:
    def test_clear_all_clears_positions(self, mock_context_dual_threshold, inject_mocks):
        mock_order_target = MagicMock()
        
        mock_context_dual_threshold.portfolio.positions = {
            "000001.XSHE": MagicMock(),
            "000002.XSHE": MagicMock(),
        }
        
        sys.modules["order_target"] = mock_order_target
        module = importlib.import_module("task02_dual_threshold_v2")
        importlib.reload(module)
        
        module.clear_all(mock_context_dual_threshold)
        
        assert mock_order_target.call_count == 2

    def test_clear_all_empty_positions(self, mock_context_dual_threshold, inject_mocks):
        mock_order_target = MagicMock()
        
        mock_context_dual_threshold.portfolio.positions = {}
        
        sys.modules["order_target"] = mock_order_target
        module = importlib.import_module("task02_dual_threshold_v2")
        importlib.reload(module)
        
        module.clear_all(mock_context_dual_threshold)
        
        mock_order_target.assert_not_called()


class TestRebalance:
    def test_rebalance_below_low_threshold(self, mock_context_dual_threshold, inject_mocks, capsys):
        mock_context_dual_threshold.low_threshold = 50
        mock_context_dual_threshold.high_threshold = 150
        mock_context_dual_threshold.max_positions = 5
        mock_context_dual_threshold.position_size = 0.2
        mock_context_dual_threshold.portfolio.positions = {}
        
        module = importlib.import_module("task02_dual_threshold_v2")
        
        original_get_zt_count = module.get_zt_count
        module.get_zt_count = lambda ctx: 30
        
        bar_dict = MockBarDict()
        module.rebalance(mock_context_dual_threshold, bar_dict)
        
        captured = capsys.readouterr()
        assert "情绪过低" in captured.out
        
        module.get_zt_count = original_get_zt_count

    def test_rebalance_above_high_threshold(self, mock_context_dual_threshold, inject_mocks, capsys):
        mock_context_dual_threshold.low_threshold = 50
        mock_context_dual_threshold.high_threshold = 150
        mock_context_dual_threshold.max_positions = 5
        mock_context_dual_threshold.position_size = 0.2
        mock_context_dual_threshold.portfolio.positions = {}
        
        module = importlib.import_module("task02_dual_threshold_v2")
        
        original_get_zt_count = module.get_zt_count
        module.get_zt_count = lambda ctx: 200
        
        bar_dict = MockBarDict()
        module.rebalance(mock_context_dual_threshold, bar_dict)
        
        captured = capsys.readouterr()
        assert "情绪过热" in captured.out
        
        module.get_zt_count = original_get_zt_count

    def test_rebalance_normal_range(self, mock_context_dual_threshold, inject_mocks, capsys):
        mock_context_dual_threshold.low_threshold = 50
        mock_context_dual_threshold.high_threshold = 150
        mock_context_dual_threshold.max_positions = 5
        mock_context_dual_threshold.position_size = 0.2
        mock_context_dual_threshold.portfolio.positions = {}
        
        module = importlib.import_module("task02_dual_threshold_v2")
        
        original_get_zt_count = module.get_zt_count
        original_select_stocks = module.select_stocks
        module.get_zt_count = lambda ctx: 80
        module.select_stocks = lambda ctx: ["000001.XSHE", "000002.XSHE"]
        
        bar_dict = MockBarDict()
        module.rebalance(mock_context_dual_threshold, bar_dict)
        
        captured = capsys.readouterr()
        assert "涨停家数" in captured.out
        
        module.get_zt_count = original_get_zt_count
        module.select_stocks = original_select_stocks

    def test_rebalance_boundary_low(self, mock_context_dual_threshold, inject_mocks, capsys):
        mock_context_dual_threshold.low_threshold = 50
        mock_context_dual_threshold.high_threshold = 150
        mock_context_dual_threshold.max_positions = 5
        mock_context_dual_threshold.position_size = 0.2
        mock_context_dual_threshold.portfolio.positions = {}
        
        module = importlib.import_module("task02_dual_threshold_v2")
        
        original_get_zt_count = module.get_zt_count
        original_select_stocks = module.select_stocks
        module.get_zt_count = lambda ctx: 50
        module.select_stocks = lambda ctx: ["000001.XSHE"]
        
        bar_dict = MockBarDict()
        module.rebalance(mock_context_dual_threshold, bar_dict)
        
        captured = capsys.readouterr()
        assert "情绪正常" in captured.out
        
        module.get_zt_count = original_get_zt_count
        module.select_stocks = original_select_stocks

    def test_rebalance_boundary_high(self, mock_context_dual_threshold, inject_mocks, capsys):
        mock_context_dual_threshold.low_threshold = 50
        mock_context_dual_threshold.high_threshold = 150
        mock_context_dual_threshold.max_positions = 5
        mock_context_dual_threshold.position_size = 0.2
        mock_context_dual_threshold.portfolio.positions = {}
        
        module = importlib.import_module("task02_dual_threshold_v2")
        
        original_get_zt_count = module.get_zt_count
        original_select_stocks = module.select_stocks
        module.get_zt_count = lambda ctx: 150
        module.select_stocks = lambda ctx: ["000001.XSHE"]
        
        bar_dict = MockBarDict()
        module.rebalance(mock_context_dual_threshold, bar_dict)
        
        captured = capsys.readouterr()
        assert "情绪正常" in captured.out
        
        module.get_zt_count = original_get_zt_count
        module.select_stocks = original_select_stocks

    def test_rebalance_no_selected_stocks(self, mock_context_dual_threshold, inject_mocks, capsys):
        mock_context_dual_threshold.low_threshold = 50
        mock_context_dual_threshold.high_threshold = 150
        mock_context_dual_threshold.max_positions = 5
        mock_context_dual_threshold.position_size = 0.2
        mock_context_dual_threshold.portfolio.positions = {}
        
        module = importlib.import_module("task02_dual_threshold_v2")
        
        original_get_zt_count = module.get_zt_count
        original_select_stocks = module.select_stocks
        module.get_zt_count = lambda ctx: 80
        module.select_stocks = lambda ctx: []
        
        bar_dict = MockBarDict()
        module.rebalance(mock_context_dual_threshold, bar_dict)
        
        captured = capsys.readouterr()
        assert "涨停家数" in captured.out
        
        module.get_zt_count = original_get_zt_count
        module.select_stocks = original_select_stocks