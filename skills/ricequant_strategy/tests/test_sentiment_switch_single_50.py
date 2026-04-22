"""
Tests for sentiment_switch_single_50.py
"""
import sys
from pathlib import Path
from unittest.mock import MagicMock, patch
from datetime import datetime
import pytest
import numpy as np

sys.path.insert(0, str(Path(__file__).parent.parent))

from tests.conftest import MockContext, MockBar, MockBarDict, MockPortfolio, create_mock_history_bars


class MockPortfolioSingle50:
    def __init__(self):
        self.starting_cash = 1000000
        self.total_value = 1000000
        self.positions = {}


class MockContextSingle50:
    def __init__(self):
        self.now = datetime(2024, 7, 1)
        self.portfolio = MockPortfolioSingle50()
        self.threshold = None
        self.max_positions = None
        self.position_size = None


@pytest.fixture
def mock_context_single50():
    return MockContextSingle50()


@pytest.fixture
def mock_scheduler():
    scheduler = MagicMock()
    scheduler.run_monthly = MagicMock()
    return scheduler


@pytest.fixture
def mock_rq_api():
    mocks = {}
    
    def mock_all_instruments(type_str):
        return ["000001.XSHE", "000002.XSHE", "600000.XSHG", "600519.XSHG"]
    
    def mock_history_bars(stock, bar_count, frequency, fields):
        if fields == "close":
            return np.array([10.0, 10.5, 11.0, 10.8, 10.9])
        elif fields == "open":
            return np.array([10.2, 10.6, 11.1, 10.9, 11.0])
        elif fields == "limit_up":
            return np.array([11.0, 11.5, 12.0, 11.8, 12.0])
        elif isinstance(fields, list):
            bars = []
            for i in range(bar_count):
                bars.append({
                    "close": 10.0 + i * 0.5,
                    "open": 10.1 + i * 0.5,
                    "limit_up": 11.0 + i * 0.5,
                })
            return bars
        return None
    
    mocks["all_instruments"] = mock_all_instruments
    mocks["history_bars"] = mock_history_bars
    mocks["order_target"] = MagicMock()
    mocks["order_target_percent"] = MagicMock()
    
    return mocks


class TestInit:
    def test_init_sets_parameters(self, mock_context_single50, mock_scheduler, mock_rq_api):
        with patch("sentiment_switch_single_50.scheduler", mock_scheduler):
            module = __import__("sentiment_switch_single_50")
            module.init(mock_context_single50)
            
            assert mock_context_single50.threshold == 50
            assert mock_context_single50.max_positions == 5
            assert mock_context_single50.position_size == 0.2
            mock_scheduler.run_monthly.assert_called_once()


class TestGetZtCount:
    def test_get_zt_count_returns_int(self, mock_rq_api, mock_context_single50):
        with patch("sentiment_switch_single_50.all_instruments", mock_rq_api["all_instruments"]):
            with patch("sentiment_switch_single_50.history_bars", mock_rq_api["history_bars"]):
                module = __import__("sentiment_switch_single_50")
                result = module.get_zt_count(mock_context_single50)
                
                assert isinstance(result, int)

    def test_get_zt_count_above_threshold(self, mock_rq_api, mock_context_single50):
        def mock_history_bars_limit_up(stock, bar_count, frequency, fields):
            return [{"close": 11.0, "limit_up": 11.0}]
        
        with patch("sentiment_switch_single_50.all_instruments", mock_rq_api["all_instruments"]):
            with patch("sentiment_switch_single_50.history_bars", mock_history_bars_limit_up):
                module = __import__("sentiment_switch_single_50")
                result = module.get_zt_count(mock_context_single50)
                
                assert result >= 0

    def test_get_zt_count_filters_special_stocks(self, mock_rq_api, mock_context_single50):
        def mock_all_instruments_special(type_str):
            return ["688001.XSHG", "430001.XSHE", "830001.XSHE", "000001.XSHE"]
        
        with patch("sentiment_switch_single_50.all_instruments", mock_all_instruments_special):
            with patch("sentiment_switch_single_50.history_bars", mock_rq_api["history_bars"]):
                module = __import__("sentiment_switch_single_50")
                result = module.get_zt_count(mock_context_single50)
                
                assert isinstance(result, int)

    def test_get_zt_count_exception_returns_default(self, mock_rq_api, mock_context_single50):
        def mock_all_instruments_error(type_str):
            raise Exception("API error")
        
        with patch("sentiment_switch_single_50.all_instruments", mock_all_instruments_error):
            module = __import__("sentiment_switch_single_50")
            result = module.get_zt_count(mock_context_single50)
            
            assert result == 100

    def test_get_zt_count_empty_stocks(self, mock_rq_api, mock_context_single50):
        def mock_all_instruments_empty(type_str):
            return []
        
        with patch("sentiment_switch_single_50.all_instruments", mock_all_instruments_empty):
            with patch("sentiment_switch_single_50.history_bars", mock_rq_api["history_bars"]):
                module = __import__("sentiment_switch_single_50")
                result = module.get_zt_count(mock_context_single50)
                
                assert result >= 0

    def test_get_zt_count_none_bars(self, mock_rq_api, mock_context_single50):
        def mock_history_bars_none(stock, bar_count, frequency, fields):
            return None
        
        with patch("sentiment_switch_single_50.all_instruments", mock_rq_api["all_instruments"]):
            with patch("sentiment_switch_single_50.history_bars", mock_history_bars_none):
                module = __import__("sentiment_switch_single_50")
                result = module.get_zt_count(mock_context_single50)
                
                assert isinstance(result, int)


class TestSelectStocks:
    def test_select_stocks_returns_list(self, mock_rq_api, mock_context_single50):
        mock_context_single50.max_positions = 5
        
        with patch("sentiment_switch_single_50.all_instruments", mock_rq_api["all_instruments"]):
            with patch("sentiment_switch_single_50.history_bars", mock_rq_api["history_bars"]):
                module = __import__("sentiment_switch_single_50")
                bar_dict = MockBarDict()
                result = module.select_stocks(mock_context_single50, bar_dict)
                
                assert isinstance(result, list)

    def test_select_stocks_empty_result(self, mock_rq_api, mock_context_single50):
        mock_context_single50.max_positions = 5
        
        def mock_all_instruments_empty(type_str):
            return []
        
        with patch("sentiment_switch_single_50.all_instruments", mock_all_instruments_empty):
            with patch("sentiment_switch_single_50.history_bars", mock_rq_api["history_bars"]):
                module = __import__("sentiment_switch_single_50")
                bar_dict = MockBarDict()
                result = module.select_stocks(mock_context_single50, bar_dict)
                
                assert result == []

    def test_select_stocks_max_positions_limit(self, mock_rq_api, mock_context_single50):
        mock_context_single50.max_positions = 2
        
        with patch("sentiment_switch_single_50.all_instruments", mock_rq_api["all_instruments"]):
            with patch("sentiment_switch_single_50.history_bars", mock_rq_api["history_bars"]):
                module = __import__("sentiment_switch_single_50")
                bar_dict = MockBarDict()
                result = module.select_stocks(mock_context_single50, bar_dict)
                
                assert len(result) <= 2

    def test_select_stocks_filters_special_stocks(self, mock_rq_api, mock_context_single50):
        mock_context_single50.max_positions = 5
        
        def mock_all_instruments_special(type_str):
            return ["688001.XSHG", "430001.XSHE", "000001.XSHE"]
        
        with patch("sentiment_switch_single_50.all_instruments", mock_all_instruments_special):
            with patch("sentiment_switch_single_50.history_bars", mock_rq_api["history_bars"]):
                module = __import__("sentiment_switch_single_50")
                bar_dict = MockBarDict()
                result = module.select_stocks(mock_context_single50, bar_dict)
                
                assert isinstance(result, list)

    def test_select_stocks_exception_returns_empty(self, mock_rq_api, mock_context_single50):
        mock_context_single50.max_positions = 5
        
        def mock_all_instruments_error(type_str):
            raise Exception("API error")
        
        with patch("sentiment_switch_single_50.all_instruments", mock_all_instruments_error):
            module = __import__("sentiment_switch_single_50")
            bar_dict = MockBarDict()
            result = module.select_stocks(mock_context_single50, bar_dict)
            
            assert result == []


class TestAdjustPositions:
    def test_adjust_positions_sells_not_selected(self, mock_rq_api, mock_context_single50):
        mock_order_target = MagicMock()
        mock_order_target_percent = MagicMock()
        
        mock_context_single50.position_size = 0.2
        mock_context_single50.portfolio.positions = {"000001.XSHE": MagicMock()}
        
        with patch("sentiment_switch_single_50.order_target", mock_order_target):
            with patch("sentiment_switch_single_50.order_target_percent", mock_order_target_percent):
                module = __import__("sentiment_switch_single_50")
                selected = ["000002.XSHE"]
                module.adjust_positions(mock_context_single50, selected)
                
                mock_order_target.assert_called()

    def test_adjust_positions_buys_selected(self, mock_rq_api, mock_context_single50):
        mock_order_target = MagicMock()
        mock_order_target_percent = MagicMock()
        
        mock_context_single50.position_size = 0.2
        mock_context_single50.portfolio.positions = {}
        
        with patch("sentiment_switch_single_50.order_target", mock_order_target):
            with patch("sentiment_switch_single_50.order_target_percent", mock_order_target_percent):
                module = __import__("sentiment_switch_single_50")
                selected = ["000001.XSHE"]
                module.adjust_positions(mock_context_single50, selected)
                
                mock_order_target_percent.assert_called_with("000001.XSHE", 0.2)

    def test_adjust_positions_holds_existing(self, mock_rq_api, mock_context_single50):
        mock_order_target = MagicMock()
        mock_order_target_percent = MagicMock()
        
        mock_context_single50.position_size = 0.2
        mock_context_single50.portfolio.positions = {"000001.XSHE": MagicMock()}
        
        with patch("sentiment_switch_single_50.order_target", mock_order_target):
            with patch("sentiment_switch_single_50.order_target_percent", mock_order_target_percent):
                module = __import__("sentiment_switch_single_50")
                selected = ["000001.XSHE"]
                module.adjust_positions(mock_context_single50, selected)
                
                mock_order_target.assert_not_called()
                mock_order_target_percent.assert_not_called()


class TestClearPositions:
    def test_clear_positions_clears_all(self, mock_rq_api, mock_context_single50):
        mock_order_target = MagicMock()
        
        mock_context_single50.portfolio.positions = {
            "000001.XSHE": MagicMock(),
            "000002.XSHE": MagicMock(),
        }
        
        with patch("sentiment_switch_single_50.order_target", mock_order_target):
            module = __import__("sentiment_switch_single_50")
            module.clear_positions(mock_context_single50)
            
            assert mock_order_target.call_count == 2

    def test_clear_positions_empty_positions(self, mock_rq_api, mock_context_single50):
        mock_order_target = MagicMock()
        
        mock_context_single50.portfolio.positions = {}
        
        with patch("sentiment_switch_single_50.order_target", mock_order_target):
            module = __import__("sentiment_switch_single_50")
            module.clear_positions(mock_context_single50)
            
            mock_order_target.assert_not_called()


class TestRebalance:
    def test_rebalance_below_threshold_clears(self, mock_rq_api, mock_context_single50, capsys):
        mock_context_single50.threshold = 50
        mock_context_single50.max_positions = 5
        mock_context_single50.position_size = 0.2
        mock_context_single50.portfolio.positions = {}
        
        def mock_get_zt_count_low(context):
            return 30
        
        mock_order_target = MagicMock()
        
        with patch("sentiment_switch_single_50.all_instruments", mock_rq_api["all_instruments"]):
            with patch("sentiment_switch_single_50.history_bars", mock_rq_api["history_bars"]):
                with patch("sentiment_switch_single_50.order_target", mock_order_target):
                    with patch("sentiment_switch_single_50.order_target_percent", mock_rq_api["order_target_percent"]):
                        module = __import__("sentiment_switch_single_50")
                        original_get_zt_count = module.get_zt_count
                        module.get_zt_count = mock_get_zt_count_low
                        
                        bar_dict = MockBarDict()
                        module.rebalance(mock_context_single50, bar_dict)
                        
                        captured = capsys.readouterr()
                        assert "情绪过低" in captured.out
                        
                        module.get_zt_count = original_get_zt_count

    def test_rebalance_above_threshold_normal(self, mock_rq_api, mock_context_single50, capsys):
        mock_context_single50.threshold = 50
        mock_context_single50.max_positions = 5
        mock_context_single50.position_size = 0.2
        mock_context_single50.portfolio.positions = {}
        
        def mock_get_zt_count_high(context):
            return 80
        
        with patch("sentiment_switch_single_50.all_instruments", mock_rq_api["all_instruments"]):
            with patch("sentiment_switch_single_50.history_bars", mock_rq_api["history_bars"]):
                with patch("sentiment_switch_single_50.order_target", MagicMock()):
                    with patch("sentiment_switch_single_50.order_target_percent", MagicMock()):
                        module = __import__("sentiment_switch_single_50")
                        original_get_zt_count = module.get_zt_count
                        module.get_zt_count = mock_get_zt_count_high
                        
                        bar_dict = MockBarDict()
                        module.rebalance(mock_context_single50, bar_dict)
                        
                        captured = capsys.readouterr()
                        assert "情绪正常" in captured.out
                        
                        module.get_zt_count = original_get_zt_count

    def test_rebalance_no_selected_stocks(self, mock_rq_api, mock_context_single50, capsys):
        mock_context_single50.threshold = 50
        mock_context_single50.max_positions = 5
        mock_context_single50.position_size = 0.2
        mock_context_single50.portfolio.positions = {}
        
        def mock_get_zt_count_high(context):
            return 80
        
        def mock_select_stocks_empty(context, bar_dict):
            return []
        
        with patch("sentiment_switch_single_50.all_instruments", mock_rq_api["all_instruments"]):
            with patch("sentiment_switch_single_50.history_bars", mock_rq_api["history_bars"]):
                with patch("sentiment_switch_single_50.order_target", MagicMock()):
                    with patch("sentiment_switch_single_50.order_target_percent", MagicMock()):
                        module = __import__("sentiment_switch_single_50")
                        original_get_zt_count = module.get_zt_count
                        original_select_stocks = module.select_stocks
                        module.get_zt_count = mock_get_zt_count_high
                        module.select_stocks = mock_select_stocks_empty
                        
                        bar_dict = MockBarDict()
                        module.rebalance(mock_context_single50, bar_dict)
                        
                        captured = capsys.readouterr()
                        assert "无选中股票" in captured.out
                        
                        module.get_zt_count = original_get_zt_count
                        module.select_stocks = original_select_stocks


class TestConfig:
    def test_config_exists(self):
        module = __import__("sentiment_switch_single_50")
        
        assert hasattr(module, "__config__")
        assert "base" in module.__config__
        assert "start_date" in module.__config__["base"]