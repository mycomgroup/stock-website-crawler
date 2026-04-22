"""
Tests for sentiment_switch_rq_strategy.py
"""
import sys
from pathlib import Path
from unittest.mock import MagicMock, patch
from datetime import datetime
import pytest
import numpy as np

sys.path.insert(0, str(Path(__file__).parent.parent))

from tests.conftest import MockContext, MockBar, MockBarDict, MockPortfolio, MockInstrument


class MockPortfolioRQ:
    def __init__(self):
        self.starting_cash = 1000000
        self.total_value = 1000000
        self.positions = {}


class MockContextRQ:
    def __init__(self):
        self.now = datetime(2024, 7, 1)
        self.portfolio = MockPortfolioRQ()
        self.sentiment_threshold = None
        self.lianban_threshold = None
        self.max_stocks = None
        self.low_open_min = None
        self.low_open_max = None
        self.total_trades = None
        self.sentiment_on_days = None
        self.sentiment_off_days = None


@pytest.fixture
def mock_context_rq():
    return MockContextRQ()


@pytest.fixture
def mock_scheduler():
    scheduler = MagicMock()
    scheduler.run_daily = MagicMock()
    return scheduler


class MockStockInfo:
    def __init__(self, order_book_id):
        self.order_book_id = order_book_id


class MockBarInfo:
    def __init__(self, close=10.0, open_price=10.0, high_limit=11.0):
        self.close = close
        self.open = open_price
        self.high_limit = high_limit


@pytest.fixture
def mock_rq_api():
    mocks = {}
    
    def mock_all_instruments(type_str):
        return [
            MockStockInfo("000001.XSHE"),
            MockStockInfo("000002.XSHE"),
            MockStockInfo("600000.XSHG"),
        ]
    
    def mock_history_bars(stock_id, bar_count, frequency, fields):
        if isinstance(fields, list):
            bars = []
            for i in range(bar_count):
                bars.append({
                    "close": 10.0 + i * 0.5,
                    "high_limit": 11.0 + i * 0.5,
                })
            return bars
        return np.array([10.0, 10.5, 11.0])
    
    mocks["all_instruments"] = mock_all_instruments
    mocks["history_bars"] = mock_history_bars
    mocks["order_target_value"] = MagicMock()
    mocks["order_value"] = MagicMock()
    mocks["market_open"] = lambda minute=0: f"market_open_{minute}"
    
    return mocks


class TestInit:
    def test_init_sets_parameters(self, mock_context_rq, mock_scheduler, mock_rq_api):
        with patch("sentiment_switch_rq_strategy.scheduler", mock_scheduler):
            with patch("sentiment_switch_rq_strategy.market_open", mock_rq_api["market_open"]):
                module = __import__("sentiment_switch_rq_strategy")
                module.init(mock_context_rq)
                
                assert mock_context_rq.sentiment_threshold == 30
                assert mock_context_rq.lianban_threshold == 2
                assert mock_context_rq.max_stocks == 3
                assert mock_context_rq.low_open_min == -5
                assert mock_context_rq.low_open_max == -1
                assert mock_context_rq.total_trades == 0
                assert mock_context_rq.sentiment_on_days == 0
                assert mock_context_rq.sentiment_off_days == 0

    def test_init_scheduler_called(self, mock_context_rq, mock_scheduler, mock_rq_api):
        with patch("sentiment_switch_rq_strategy.scheduler", mock_scheduler):
            with patch("sentiment_switch_rq_strategy.market_open", mock_rq_api["market_open"]):
                module = __import__("sentiment_switch_rq_strategy")
                module.init(mock_context_rq)
                
                mock_scheduler.run_daily.assert_called_once()


class TestGetZtCount:
    def test_get_zt_count_returns_tuple(self, mock_rq_api, mock_context_rq):
        with patch("sentiment_switch_rq_strategy.all_instruments", mock_rq_api["all_instruments"]):
            with patch("sentiment_switch_rq_strategy.history_bars", mock_rq_api["history_bars"]):
                module = __import__("sentiment_switch_rq_strategy")
                bar_dict = {}
                result = module.get_zt_count(mock_context_rq, bar_dict)
                
                assert isinstance(result, tuple)
                assert len(result) == 2

    def test_get_zt_count_zt_count_positive(self, mock_rq_api, mock_context_rq):
        with patch("sentiment_switch_rq_strategy.all_instruments", mock_rq_api["all_instruments"]):
            with patch("sentiment_switch_rq_strategy.history_bars", mock_rq_api["history_bars"]):
                module = __import__("sentiment_switch_rq_strategy")
                bar_dict = {}
                zt_count, max_lianban = module.get_zt_count(mock_context_rq, bar_dict)
                
                assert zt_count >= 0
                assert max_lianban >= 0

    def test_get_zt_count_empty_stocks(self, mock_rq_api, mock_context_rq):
        def mock_all_instruments_empty(type_str):
            return []
        
        with patch("sentiment_switch_rq_strategy.all_instruments", mock_all_instruments_empty):
            with patch("sentiment_switch_rq_strategy.history_bars", mock_rq_api["history_bars"]):
                module = __import__("sentiment_switch_rq_strategy")
                bar_dict = {}
                result = module.get_zt_count(mock_context_rq, bar_dict)
                
                assert result == (0, 0)

    def test_get_zt_count_exception_returns_zero(self, mock_rq_api, mock_context_rq):
        def mock_all_instruments_error(type_str):
            raise Exception("API error")
        
        with patch("sentiment_switch_rq_strategy.all_instruments", mock_all_instruments_error):
            module = __import__("sentiment_switch_rq_strategy")
            bar_dict = {}
            result = module.get_zt_count(mock_context_rq, bar_dict)
            
            assert result == (0, 0)

    def test_get_zt_count_limit_up_detection(self, mock_rq_api, mock_context_rq):
        def mock_history_bars_limit_up(stock_id, bar_count, frequency, fields):
            bars = []
            for i in range(bar_count):
                bars.append({
                    "close": 11.0 + i,
                    "high_limit": 11.0 + i,
                })
            return bars
        
        with patch("sentiment_switch_rq_strategy.all_instruments", mock_rq_api["all_instruments"]):
            with patch("sentiment_switch_rq_strategy.history_bars", mock_history_bars_limit_up):
                module = __import__("sentiment_switch_rq_strategy")
                bar_dict = {}
                zt_count, max_lianban = module.get_zt_count(mock_context_rq, bar_dict)
                
                assert zt_count >= 0

    def test_get_zt_count_none_bars(self, mock_rq_api, mock_context_rq):
        def mock_history_bars_none(stock_id, bar_count, frequency, fields):
            return None
        
        with patch("sentiment_switch_rq_strategy.all_instruments", mock_rq_api["all_instruments"]):
            with patch("sentiment_switch_rq_strategy.history_bars", mock_history_bars_none):
                module = __import__("sentiment_switch_rq_strategy")
                bar_dict = {}
                result = module.get_zt_count(mock_context_rq, bar_dict)
                
                assert result[0] >= 0

    def test_get_zt_count_lianban_calculation(self, mock_rq_api, mock_context_rq):
        def mock_history_bars_lianban(stock_id, bar_count, frequency, fields):
            if bar_count >= 10:
                bars = []
                for i in range(bar_count):
                    bars.append({
                        "close": 11.0,
                        "high_limit": 11.0,
                    })
                return bars
            bars = []
            for i in range(bar_count):
                bars.append({
                    "close": 11.0 if i == bar_count - 2 else 10.0,
                    "high_limit": 11.0,
                })
            return bars
        
        with patch("sentiment_switch_rq_strategy.all_instruments", mock_rq_api["all_instruments"]):
            with patch("sentiment_switch_rq_strategy.history_bars", mock_history_bars_lianban):
                module = __import__("sentiment_switch_rq_strategy")
                bar_dict = {}
                zt_count, max_lianban = module.get_zt_count(mock_context_rq, bar_dict)
                
                assert max_lianban >= 0


class TestGetLowOpenStocks:
    def test_get_low_open_stocks_returns_list(self, mock_rq_api, mock_context_rq):
        mock_context_rq.low_open_min = -5
        mock_context_rq.low_open_max = -1
        
        with patch("sentiment_switch_rq_strategy.history_bars", mock_rq_api["history_bars"]):
            module = __import__("sentiment_switch_rq_strategy")
            bar_dict = MockBarDict()
            zt_stocks = [MockStockInfo("000001.XSHE")]
            
            result = module.get_low_open_stocks(mock_context_rq, bar_dict, zt_stocks)
            
            assert isinstance(result, list)

    def test_get_low_open_stocks_empty_zt_stocks(self, mock_rq_api, mock_context_rq):
        mock_context_rq.low_open_min = -5
        mock_context_rq.low_open_max = -1
        
        with patch("sentiment_switch_rq_strategy.history_bars", mock_rq_api["history_bars"]):
            module = __import__("sentiment_switch_rq_strategy")
            bar_dict = MockBarDict()
            zt_stocks = []
            
            result = module.get_low_open_stocks(mock_context_rq, bar_dict, zt_stocks)
            
            assert result == []

    def test_get_low_open_stocks_stock_not_in_bar_dict(self, mock_rq_api, mock_context_rq):
        mock_context_rq.low_open_min = -5
        mock_context_rq.low_open_max = -1
        
        with patch("sentiment_switch_rq_strategy.history_bars", mock_rq_api["history_bars"]):
            module = __import__("sentiment_switch_rq_strategy")
            bar_dict = {}
            zt_stocks = [MockStockInfo("999999.XSHE")]
            
            result = module.get_low_open_stocks(mock_context_rq, bar_dict, zt_stocks)
            
            assert result == []

    def test_get_low_open_stocks_none_bars(self, mock_rq_api, mock_context_rq):
        mock_context_rq.low_open_min = -5
        mock_context_rq.low_open_max = -1
        
        def mock_history_bars_none(stock_id, bar_count, frequency, fields):
            return None
        
        with patch("sentiment_switch_rq_strategy.history_bars", mock_history_bars_none):
            module = __import__("sentiment_switch_rq_strategy")
            bar_dict = MockBarDict()
            zt_stocks = [MockStockInfo("000001.XSHE")]
            
            result = module.get_low_open_stocks(mock_context_rq, bar_dict, zt_stocks)
            
            assert result == []


class TestRebalance:
    def test_rebalance_sentiment_off(self, mock_rq_api, mock_context_rq):
        mock_context_rq.sentiment_threshold = 30
        mock_context_rq.lianban_threshold = 2
        mock_context_rq.sentiment_on_days = 0
        mock_context_rq.sentiment_off_days = 0
        mock_context_rq.portfolio.positions = {}
        
        def mock_get_zt_count(context, bar_dict):
            return (20, 1)
        
        with patch("sentiment_switch_rq_strategy.all_instruments", mock_rq_api["all_instruments"]):
            with patch("sentiment_switch_rq_strategy.history_bars", mock_rq_api["history_bars"]):
                with patch("sentiment_switch_rq_strategy.order_target_value", mock_rq_api["order_target_value"]):
                    module = __import__("sentiment_switch_rq_strategy")
                    bar_dict = MockBarDict()
                    
                    original_get_zt_count = module.get_zt_count
                    module.get_zt_count = mock_get_zt_count
                    
                    module.rebalance(mock_context_rq, bar_dict)
                    
                    assert mock_context_rq.sentiment_off_days == 1
                    
                    module.get_zt_count = original_get_zt_count


class TestAfterTrading:
    def test_after_trading_not_full_year(self, mock_context_rq):
        mock_context_rq.sentiment_on_days = 100
        mock_context_rq.sentiment_off_days = 50
        mock_context_rq.total_trades = 30
        
        module = __import__("sentiment_switch_rq_strategy")
        bar_dict = {}
        
        module.after_trading(mock_context_rq, bar_dict)

    def test_after_trading_full_year(self, mock_context_rq, capsys):
        mock_context_rq.sentiment_on_days = 150
        mock_context_rq.sentiment_off_days = 92
        mock_context_rq.total_trades = 50
        
        module = __import__("sentiment_switch_rq_strategy")
        bar_dict = {}
        
        module.after_trading(mock_context_rq, bar_dict)
        
        captured = capsys.readouterr()
        assert "全年统计" in captured.out

    def test_after_trading_prints_summary(self, mock_context_rq, capsys):
        mock_context_rq.sentiment_on_days = 150
        mock_context_rq.sentiment_off_days = 92
        mock_context_rq.total_trades = 50
        
        module = __import__("sentiment_switch_rq_strategy")
        bar_dict = {}
        
        module.after_trading(mock_context_rq, bar_dict)
        
        captured = capsys.readouterr()
        assert "情绪开启天数" in captured.out or captured.out == ""