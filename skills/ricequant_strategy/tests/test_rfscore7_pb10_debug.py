"""
Tests for rfscore7_pb10_debug.py
"""
import sys
from pathlib import Path
from unittest.mock import MagicMock, patch
from datetime import datetime
import numpy as np
import pandas as pd
import pytest

sys.path.insert(0, str(Path(__file__).parent.parent))


class MockPortfolioDebug:
    def __init__(self):
        self.starting_cash = 1000000
        self.total_value = 1000000
        self.positions = {}


class MockContextDebug:
    def __init__(self):
        self.now = datetime(2024, 7, 1)
        self.portfolio = MockPortfolioDebug()
        self.benchmark = "000300.XSHG"
        self.use_real_price = True
        self.hold_num = 20
        self.pb_pct = 0.10
        self.breadth_reduce = 0.25
        self.breadth_stop = 0.15
        self.reduced_hold_num = 10
        self.last_rebalance_month = -1
        self.run_count = 0
        self.error_count = 0
        self.trade_count = 0


class MockPositionDebug:
    def __init__(self, market_value=50000):
        self.market_value = market_value
        self.quantity = 1000


@pytest.fixture(scope="module")
def mock_rq_globals():
    mock_logger = MagicMock()
    mock_scheduler = MagicMock()
    
    def mock_index_components(index_name):
        if index_name == "000300.XSHG":
            return ["600000.XSHG", "600519.XSHG", "000001.XSHE", "688001.XSHG"]
        elif index_name == "000905.XSHG":
            return ["000002.XSHE", "600036.XSHG", "000651.XSHE", "688002.XSHG"]
        return []
    
    def mock_history_bars(stock, bar_count, frequency, fields, include_now=False):
        if stock == "000300.XSHG":
            return np.array([3800, 3810, 3820, 3830, 3840, 3850, 3860, 3870, 3880, 3890,
                             3900, 3910, 3920, 3930, 3940, 3950, 3960, 3970, 3980, 4000])
        return np.array([10.0, 10.5, 11.0, 11.5, 12.0, 12.5, 13.0, 13.5, 14.0, 14.5,
                        15.0, 15.5, 16.0, 16.5, 17.0, 17.5, 18.0, 18.5, 19.0, 20.0])
    
    def mock_get_factor(stocks, factors, start_date=None, end_date=None):
        n = min(len(stocks), 4)
        data = {
            "order_book_id": stocks[:n],
            "roa": [5.0, 3.0, -1.0, 8.0][:n],
            "roe": [10.0, 5.0, -2.0, 15.0][:n],
            "gross_profit_margin": [30.0, 25.0, 20.0, 40.0][:n],
            "net_profit_margin": [8.0, 5.0, -1.0, 12.0][:n],
            "net_profit_yoy": [15.0, -5.0, 20.0, 10.0][:n],
            "or_yoy": [10.0, 5.0, -10.0, 8.0][:n],
            "pe_ratio": [15.0, -5.0, 20.0, 30.0][:n],
            "pb_ratio": [1.5, 2.0, 0.8, 3.0][:n],
        }
        return pd.DataFrame(data)
    
    def mock_order_target_value(stock, value):
        return None
    
    yield {
        "logger": mock_logger,
        "scheduler": mock_scheduler,
        "index_components": mock_index_components,
        "history_bars": mock_history_bars,
        "get_factor": mock_get_factor,
        "order_target_value": mock_order_target_value,
    }


@pytest.fixture
def patch_rq_globals(mock_rq_globals):
    import importlib
    if "rfscore7_pb10_debug" in sys.modules:
        del sys.modules["rfscore7_pb10_debug"]
    
    import rfscore7_pb10_debug as module
    
    for name, value in mock_rq_globals.items():
        setattr(module, name, value)
    
    yield module


class TestRfscore7Pb10Debug:
    def test_init(self, patch_rq_globals, mock_rq_globals):
        module = patch_rq_globals
        context = MockContextDebug()
        module.init(context)
        assert context.benchmark == "000300.XSHG"
        assert context.use_real_price == True
        assert context.hold_num == 20
        assert context.pb_pct == 0.10
        assert context.breadth_reduce == 0.25
        assert context.breadth_stop == 0.15
        assert context.reduced_hold_num == 10
        assert context.last_rebalance_month == -1
        assert context.run_count == 0
        assert context.error_count == 0
        assert context.trade_count == 0
        mock_rq_globals["logger"].info.assert_called()

    def test_handle_bar_first_month(self, patch_rq_globals):
        module = patch_rq_globals
        context = MockContextDebug()
        module.init(context)
        context.last_rebalance_month = 6
        
        with patch.object(module, "rebalance"):
            module.handle_bar(context, {})
            assert context.last_rebalance_month == 7
            assert context.run_count == 1

    def test_handle_bar_same_month(self, patch_rq_globals):
        module = patch_rq_globals
        context = MockContextDebug()
        module.init(context)
        context.last_rebalance_month = 7
        
        with patch.object(module, "rebalance"):
            module.handle_bar(context, {})
            assert context.last_rebalance_month == 7
            assert context.run_count == 0

    def test_handle_bar_with_exception(self, patch_rq_globals, mock_rq_globals):
        module = patch_rq_globals
        context = MockContextDebug()
        module.init(context)
        context.last_rebalance_month = 6
        
        with patch.object(module, "rebalance", side_effect=Exception("Test error")):
            module.handle_bar(context, {})
            assert context.error_count == 1
            mock_rq_globals["logger"].error.assert_called()

    def test_get_universe_success(self, patch_rq_globals):
        module = patch_rq_globals
        context = MockContextDebug()
        result = module.get_universe(context)
        assert len(result) > 0
        assert "688001.XSHG" not in result
        assert "688002.XSHG" not in result

    def test_get_universe_exception(self, patch_rq_globals):
        module = patch_rq_globals
        context = MockContextDebug()
        
        with patch.object(module, "index_components", side_effect=Exception("API error")):
            result = module.get_universe(context)
            assert result == []

    def test_calc_rfscore7_success(self, patch_rq_globals):
        module = patch_rq_globals
        context = MockContextDebug()
        stocks = ["000001.XSHE", "000002.XSHE", "600000.XSHG", "600519.XSHG"]
        result = module.calc_rfscore7(context, stocks)
        assert isinstance(result, pd.DataFrame)
        assert "rfscore7" in result.columns

    def test_calc_rfscore7_with_date_column(self, patch_rq_globals):
        module = patch_rq_globals
        context = MockContextDebug()
        stocks = ["000001.XSHE", "000002.XSHE"]
        
        def mock_get_factor_with_date(stocks, factors, start_date=None, end_date=None):
            data = {
                "order_book_id": stocks,
                "date": ["2024-07-01"] * len(stocks),
                "roa": [5.0, 3.0],
                "roe": [10.0, 5.0],
                "gross_profit_margin": [30.0, 25.0],
                "net_profit_margin": [8.0, 5.0],
                "net_profit_yoy": [15.0, -5.0],
                "or_yoy": [10.0, 5.0],
                "pe_ratio": [15.0, -5.0],
                "pb_ratio": [1.5, 2.0],
            }
            return pd.DataFrame(data)
        
        with patch.object(module, "get_factor", mock_get_factor_with_date):
            result = module.calc_rfscore7(context, stocks)
            assert isinstance(result, pd.DataFrame)

    def test_calc_rfscore7_returns_none(self, patch_rq_globals):
        module = patch_rq_globals
        context = MockContextDebug()
        stocks = ["000001.XSHE"]
        
        with patch.object(module, "get_factor", return_value=None):
            result = module.calc_rfscore7(context, stocks)
            assert result.empty

    def test_calc_rfscore7_returns_empty(self, patch_rq_globals):
        module = patch_rq_globals
        context = MockContextDebug()
        stocks = ["000001.XSHE"]
        
        with patch.object(module, "get_factor", return_value=pd.DataFrame()):
            result = module.calc_rfscore7(context, stocks)
            assert result.empty

    def test_calc_rfscore7_exception(self, patch_rq_globals):
        module = patch_rq_globals
        context = MockContextDebug()
        stocks = ["000001.XSHE"]
        
        with patch.object(module, "get_factor", side_effect=Exception("API error")):
            result = module.calc_rfscore7(context, stocks)
            assert result.empty

    def test_calc_market_state_success(self, patch_rq_globals):
        module = patch_rq_globals
        context = MockContextDebug()
        result = module.calc_market_state(context)
        assert "breadth" in result
        assert "trend_on" in result
        assert 0 <= result["breadth"] <= 1

    def test_calc_market_state_none_bars(self, patch_rq_globals):
        module = patch_rq_globals
        context = MockContextDebug()
        
        with patch.object(module, "history_bars", return_value=None):
            result = module.calc_market_state(context)
            assert result["breadth"] == 0.5
            assert result["trend_on"] == True

    def test_calc_market_state_short_bars(self, patch_rq_globals):
        module = patch_rq_globals
        context = MockContextDebug()
        
        with patch.object(module, "history_bars", return_value=np.array([10, 11, 12])):
            result = module.calc_market_state(context)
            assert result["breadth"] == 0.5
            assert result["trend_on"] == True

    def test_calc_market_state_exception(self, patch_rq_globals):
        module = patch_rq_globals
        context = MockContextDebug()
        
        with patch.object(module, "history_bars", side_effect=Exception("API error")):
            result = module.calc_market_state(context)
            assert result["breadth"] == 0.5
            assert result["trend_on"] == True

    def test_calc_market_state_trend_on(self, patch_rq_globals):
        module = patch_rq_globals
        context = MockContextDebug()
        
        def mock_history_bars_trend_on(stock, bar_count, frequency, fields, include_now=False):
            if stock == "000300.XSHG":
                return np.array([3800] * 19 + [4000])
            return np.array([10] * 19 + [12])
        
        with patch.object(module, "history_bars", mock_history_bars_trend_on):
            result = module.calc_market_state(context)
            assert result["trend_on"] == True

    def test_calc_market_state_trend_off(self, patch_rq_globals):
        module = patch_rq_globals
        context = MockContextDebug()
        
        def mock_history_bars_trend_off(stock, bar_count, frequency, fields, include_now=False):
            if stock == "000300.XSHG":
                return np.array([4000] * 19 + [3800])
            return np.array([12] * 19 + [10])
        
        with patch.object(module, "history_bars", mock_history_bars_trend_off):
            result = module.calc_market_state(context)
            assert result["trend_on"] == False

    def test_choose_stocks_success(self, patch_rq_globals):
        module = patch_rq_globals
        context = MockContextDebug()
        result = module.choose_stocks(context, 5)
        assert isinstance(result, list)

    def test_choose_stocks_empty_universe(self, patch_rq_globals):
        module = patch_rq_globals
        context = MockContextDebug()
        
        with patch.object(module, "get_universe", return_value=[]):
            result = module.choose_stocks(context, 5)
            assert result == []

    def test_choose_stocks_empty_factor(self, patch_rq_globals):
        module = patch_rq_globals
        context = MockContextDebug()
        
        with patch.object(module, "calc_rfscore7", return_value=pd.DataFrame()):
            result = module.choose_stocks(context, 5)
            assert result == []

    def test_choose_stocks_with_pb_filter(self, patch_rq_globals):
        module = patch_rq_globals
        context = MockContextDebug()
        context.pb_pct = 0.50
        
        def mock_calc_rfscore7(context, stocks):
            data = {
                "order_book_id": ["000001.XSHE", "000002.XSHE", "600000.XSHG"],
                "rfscore7": [5, 4, 3],
                "pb_ratio": [1.0, 2.0, 3.0],
            }
            return pd.DataFrame(data)
        
        with patch.object(module, "calc_rfscore7", mock_calc_rfscore7):
            with patch.object(module, "get_universe", return_value=["000001.XSHE", "000002.XSHE", "600000.XSHG"]):
                result = module.choose_stocks(context, 2)
                assert len(result) <= 2

    def test_choose_stocks_no_pb_column(self, patch_rq_globals):
        module = patch_rq_globals
        context = MockContextDebug()
        
        def mock_calc_rfscore7(context, stocks):
            data = {
                "order_book_id": ["000001.XSHE", "000002.XSHE"],
                "rfscore7": [5, 4],
            }
            return pd.DataFrame(data)
        
        with patch.object(module, "calc_rfscore7", mock_calc_rfscore7):
            with patch.object(module, "get_universe", return_value=["000001.XSHE", "000002.XSHE"]):
                result = module.choose_stocks(context, 2)
                assert len(result) <= 2

    def test_choose_stocks_with_order_book_id(self, patch_rq_globals):
        module = patch_rq_globals
        context = MockContextDebug()
        
        def mock_calc_rfscore7(context, stocks):
            data = {
                "order_book_id": ["000001.XSHE", "000002.XSHE", "600000.XSHG"],
                "rfscore7": [7, 6, 5],
                "pb_ratio": [0.5, 0.8, 1.0],
            }
            return pd.DataFrame(data)
        
        with patch.object(module, "calc_rfscore7", mock_calc_rfscore7):
            with patch.object(module, "get_universe", return_value=["000001.XSHE", "000002.XSHE", "600000.XSHG"]):
                result = module.choose_stocks(context, 2)
                assert len(result) <= 2

    def test_choose_stocks_without_order_book_id(self, patch_rq_globals):
        module = patch_rq_globals
        context = MockContextDebug()
        
        def mock_calc_rfscore7(context, stocks):
            data = {
                "rfscore7": [7, 6, 5],
                "pb_ratio": [0.5, 0.8, 1.0],
            }
            df = pd.DataFrame(data, index=["000001.XSHE", "000002.XSHE", "600000.XSHG"])
            return df
        
        with patch.object(module, "calc_rfscore7", mock_calc_rfscore7):
            with patch.object(module, "get_universe", return_value=["000001.XSHE", "000002.XSHE", "600000.XSHG"]):
                result = module.choose_stocks(context, 2)
                assert len(result) <= 2

    def test_rebalance_normal_position(self, patch_rq_globals, mock_rq_globals):
        module = patch_rq_globals
        context = MockContextDebug()
        module.init(context)
        
        def mock_calc_market_state(context):
            return {"breadth": 0.5, "trend_on": True}
        
        with patch.object(module, "calc_market_state", mock_calc_market_state):
            with patch.object(module, "choose_stocks", return_value=["000001.XSHE"]):
                module.rebalance(context, {})
                mock_rq_globals["logger"].info.assert_called()

    def test_rebalance_reduce_position(self, patch_rq_globals):
        module = patch_rq_globals
        context = MockContextDebug()
        module.init(context)
        
        def mock_calc_market_state(context):
            return {"breadth": 0.20, "trend_on": False}
        
        with patch.object(module, "calc_market_state", mock_calc_market_state):
            with patch.object(module, "choose_stocks", return_value=["000001.XSHE"]):
                module.rebalance(context, {})

    def test_rebalance_empty_position(self, patch_rq_globals):
        module = patch_rq_globals
        context = MockContextDebug()
        module.init(context)
        
        def mock_calc_market_state(context):
            return {"breadth": 0.10, "trend_on": False}
        
        with patch.object(module, "calc_market_state", mock_calc_market_state):
            module.rebalance(context, {})

    def test_rebalance_sell_existing_positions(self, patch_rq_globals):
        module = patch_rq_globals
        context = MockContextDebug()
        module.init(context)
        context.portfolio.positions = {"600000.XSHG": MockPositionDebug()}
        
        def mock_calc_market_state(context):
            return {"breadth": 0.5, "trend_on": True}
        
        with patch.object(module, "calc_market_state", mock_calc_market_state):
            with patch.object(module, "choose_stocks", return_value=["000001.XSHE"]):
                module.rebalance(context, {})

    def test_rebalance_buy_new_positions(self, patch_rq_globals):
        module = patch_rq_globals
        context = MockContextDebug()
        module.init(context)
        context.portfolio.total_value = 1000000
        
        def mock_calc_market_state(context):
            return {"breadth": 0.5, "trend_on": True}
        
        with patch.object(module, "calc_market_state", mock_calc_market_state):
            with patch.object(module, "choose_stocks", return_value=["000001.XSHE", "000002.XSHE"]):
                module.rebalance(context, {})

    def test_rebalance_zero_total_value(self, patch_rq_globals):
        module = patch_rq_globals
        context = MockContextDebug()
        module.init(context)
        context.portfolio.total_value = 0
        
        def mock_calc_market_state(context):
            return {"breadth": 0.5, "trend_on": True}
        
        with patch.object(module, "calc_market_state", mock_calc_market_state):
            with patch.object(module, "choose_stocks", return_value=["000001.XSHE"]):
                module.rebalance(context, {})

    def test_after_trading(self, patch_rq_globals, mock_rq_globals):
        module = patch_rq_globals
        context = MockContextDebug()
        context.run_count = 5
        context.error_count = 1
        context.trade_count = 10
        context.portfolio.positions = {"000001.XSHE": MockPositionDebug()}
        context.portfolio.total_value = 1000000
        module.after_trading(context)
        mock_rq_globals["logger"].info.assert_called()

    def test_rfscore7_calculation_all_positive(self, patch_rq_globals):
        module = patch_rq_globals
        context = MockContextDebug()
        stocks = ["000001.XSHE"]
        
        def mock_get_factor_all_positive(stocks, factors, start_date=None, end_date=None):
            data = {
                "order_book_id": stocks,
                "roa": [5.0],
                "roe": [10.0],
                "gross_profit_margin": [50.0],
                "net_profit_margin": [8.0],
                "net_profit_yoy": [15.0],
                "or_yoy": [10.0],
                "pe_ratio": [15.0],
                "pb_ratio": [1.5],
            }
            return pd.DataFrame(data)
        
        with patch.object(module, "get_factor", mock_get_factor_all_positive):
            result = module.calc_rfscore7(context, stocks)
            assert result["rfscore7"].iloc[0] >= 0

    def test_rfscore7_calculation_all_negative(self, patch_rq_globals):
        module = patch_rq_globals
        context = MockContextDebug()
        stocks = ["000001.XSHE"]
        
        def mock_get_factor_all_negative(stocks, factors, start_date=None, end_date=None):
            data = {
                "order_book_id": stocks,
                "roa": [-5.0],
                "roe": [-10.0],
                "gross_profit_margin": [5.0],
                "net_profit_margin": [-8.0],
                "net_profit_yoy": [-15.0],
                "or_yoy": [-10.0],
                "pe_ratio": [-15.0],
                "pb_ratio": [1.5],
            }
            return pd.DataFrame(data)
        
        with patch.object(module, "get_factor", mock_get_factor_all_negative):
            result = module.calc_rfscore7(context, stocks)
            assert result["rfscore7"].iloc[0] >= 0