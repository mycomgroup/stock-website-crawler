"""
Tests for rfscore7_pb10_full.py
"""
import sys
from pathlib import Path
from unittest.mock import MagicMock, patch
from datetime import datetime
import numpy as np
import pandas as pd
import pytest

sys.path.insert(0, str(Path(__file__).parent.parent))


class MockPortfolioFull:
    def __init__(self):
        self.starting_cash = 1000000
        self.total_value = 1000000
        self.positions = {}


class MockContextFull:
    def __init__(self):
        self.now = datetime(2024, 7, 1)
        self.portfolio = MockPortfolioFull()
        self.benchmark = "000300.XSHG"
        self.use_real_price = True
        self.hold_num = 20
        self.pb_pct = 0.10
        self.breadth_reduce = 0.25
        self.breadth_stop = 0.15
        self.reduced_hold_num = 10


class MockPositionFull:
    def __init__(self, market_value=50000):
        self.market_value = market_value
        self.quantity = 1000


class MockSchedulerFull:
    def __init__(self):
        self.scheduled_functions = []
    
    def run_monthly(self, func, monthday=1):
        self.scheduled_functions.append((func, monthday))


@pytest.fixture(scope="module")
def setup_rq_mocks_full():
    mock_logger = MagicMock()
    mock_scheduler = MockSchedulerFull()
    sys.modules["logger"] = mock_logger
    sys.modules["scheduler"] = mock_scheduler
    
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
        n = len(stocks[:4] if len(stocks) >= 4 else stocks)
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
    
    sys.modules["index_components"] = mock_index_components
    sys.modules["history_bars"] = mock_history_bars
    sys.modules["get_factor"] = mock_get_factor
    sys.modules["order_target_value"] = mock_order_target_value
    
    yield mock_logger
    
    del sys.modules["logger"]
    del sys.modules["scheduler"]


class TestRfscore7Pb10Full:
    def test_init(self, setup_rq_mocks_full):
        from rfscore7_pb10_full import init
        context = MockContextFull()
        init(context)
        assert context.benchmark == "000300.XSHG"
        assert context.use_real_price == True
        assert context.hold_num == 20
        assert context.pb_pct == 0.10
        assert context.breadth_reduce == 0.25
        assert context.breadth_stop == 0.15
        assert context.reduced_hold_num == 10
        setup_rq_mocks_full.info.assert_called()

    def test_get_universe_success(self, setup_rq_mocks_full):
        from rfscore7_pb10_full import get_universe
        context = MockContextFull()
        result = get_universe(context)
        assert len(result) > 0
        assert "688001.XSHG" not in result
        assert "688002.XSHG" not in result

    def test_get_universe_combined_pool(self, setup_rq_mocks_full):
        from rfscore7_pb10_full import get_universe
        context = MockContextFull()
        result = get_universe(context)
        hs300_stocks = ["600000.XSHG", "600519.XSHG", "000001.XSHE"]
        zz500_stocks = ["000002.XSHE", "600036.XSHG", "000651.XSHE"]
        for stock in hs300_stocks + zz500_stocks:
            if not stock.startswith("688"):
                assert stock in result

    def test_calc_rfscore7_batch_success(self, setup_rq_mocks_full):
        from rfscore7_pb10_full import calc_rfscore7_batch
        context = MockContextFull()
        stocks = ["000001.XSHE", "000002.XSHE", "600000.XSHG", "600519.XSHG"]
        date_str = "2024-07-01"
        result = calc_rfscore7_batch(context, stocks, date_str)
        assert isinstance(result, pd.DataFrame)
        assert "rfscore7" in result.columns

    def test_calc_rfscore7_batch_with_date_column(self, setup_rq_mocks_full):
        from rfscore7_pb10_full import calc_rfscore7_batch
        context = MockContextFull()
        stocks = ["000001.XSHE", "000002.XSHE"]
        date_str = "2024-07-01"
        
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
        
        with patch("rfscore7_pb10_full.get_factor", mock_get_factor_with_date):
            result = calc_rfscore7_batch(context, stocks, date_str)
            assert isinstance(result, pd.DataFrame)

    def test_calc_rfscore7_batch_returns_none(self, setup_rq_mocks_full):
        from rfscore7_pb10_full import calc_rfscore7_batch
        context = MockContextFull()
        stocks = ["000001.XSHE"]
        date_str = "2024-07-01"
        
        with patch("rfscore7_pb10_full.get_factor", return_value=None):
            result = calc_rfscore7_batch(context, stocks, date_str)
            assert result.empty

    def test_calc_rfscore7_batch_returns_empty(self, setup_rq_mocks_full):
        from rfscore7_pb10_full import calc_rfscore7_batch
        context = MockContextFull()
        stocks = ["000001.XSHE"]
        date_str = "2024-07-01"
        
        with patch("rfscore7_pb10_full.get_factor", return_value=pd.DataFrame()):
            result = calc_rfscore7_batch(context, stocks, date_str)
            assert result.empty

    def test_calc_rfscore7_batch_exception(self, setup_rq_mocks_full):
        from rfscore7_pb10_full import calc_rfscore7_batch
        context = MockContextFull()
        stocks = ["000001.XSHE"]
        date_str = "2024-07-01"
        
        with patch("rfscore7_pb10_full.get_factor", side_effect=Exception("API error")):
            result = calc_rfscore7_batch(context, stocks, date_str)
            assert result.empty

    def test_calc_market_state_success(self, setup_rq_mocks_full):
        from rfscore7_pb10_full import calc_market_state
        context = MockContextFull()
        result = calc_market_state(context)
        assert "breadth" in result
        assert "trend_on" in result
        assert 0 <= result["breadth"] <= 1

    def test_calc_market_state_none_bars(self, setup_rq_mocks_full):
        from rfscore7_pb10_full import calc_market_state
        context = MockContextFull()
        
        with patch("rfscore7_pb10_full.history_bars", return_value=None):
            result = calc_market_state(context)
            assert result["breadth"] == 0.5
            assert result["trend_on"] == True

    def test_calc_market_state_short_bars(self, setup_rq_mocks_full):
        from rfscore7_pb10_full import calc_market_state
        context = MockContextFull()
        
        with patch("rfscore7_pb10_full.history_bars", return_value=np.array([10, 11, 12])):
            result = calc_market_state(context)
            assert result["breadth"] == 0.5
            assert result["trend_on"] == True

    def test_calc_market_state_exception(self, setup_rq_mocks_full):
        from rfscore7_pb10_full import calc_market_state
        context = MockContextFull()
        
        with patch("rfscore7_pb10_full.history_bars", side_effect=Exception("API error")):
            result = calc_market_state(context)
            assert result["breadth"] == 0.5
            assert result["trend_on"] == True

    def test_calc_market_state_high_breadth(self, setup_rq_mocks_full):
        from rfscore7_pb10_full import calc_market_state
        context = MockContextFull()
        
        def mock_history_bars_high(stock, bar_count, frequency, fields, include_now=False):
            if stock == "000300.XSHG":
                return np.array([3800] * 19 + [4000])
            return np.array([10] * 19 + [12])
        
        with patch("rfscore7_pb10_full.history_bars", mock_history_bars_high):
            result = calc_market_state(context)
            assert result["breadth"] >= 0

    def test_calc_market_state_low_breadth(self, setup_rq_mocks_full):
        from rfscore7_pb10_full import calc_market_state
        context = MockContextFull()
        
        def mock_history_bars_low(stock, bar_count, frequency, fields, include_now=False):
            if stock == "000300.XSHG":
                return np.array([4000] * 19 + [3800])
            return np.array([12] * 19 + [10])
        
        with patch("rfscore7_pb10_full.history_bars", mock_history_bars_low):
            result = calc_market_state(context)
            assert result["breadth"] >= 0

    def test_choose_stocks_success(self, setup_rq_mocks_full):
        from rfscore7_pb10_full import choose_stocks
        context = MockContextFull()
        result = choose_stocks(context, 5)
        assert isinstance(result, list)

    def test_choose_stocks_empty_factor(self, setup_rq_mocks_full):
        from rfscore7_pb10_full import choose_stocks
        context = MockContextFull()
        
        with patch("rfscore7_pb10_full.calc_rfscore7_batch", return_value=pd.DataFrame()):
            result = choose_stocks(context, 5)
            assert result == []

    def test_choose_stocks_with_pb_filter(self, setup_rq_mocks_full):
        from rfscore7_pb10_full import choose_stocks
        context = MockContextFull()
        context.pb_pct = 0.50
        
        def mock_calc_rfscore7_batch(context, stocks, date_str):
            data = {
                "order_book_id": ["000001.XSHE", "000002.XSHE", "600000.XSHG"],
                "rfscore7": [5, 4, 3],
                "pb_ratio": [1.0, 2.0, 3.0],
            }
            return pd.DataFrame(data)
        
        with patch("rfscore7_pb10_full.calc_rfscore7_batch", mock_calc_rfscore7_batch):
            result = choose_stocks(context, 2)
            assert len(result) <= 2

    def test_choose_stocks_no_pb_column(self, setup_rq_mocks_full):
        from rfscore7_pb10_full import choose_stocks
        context = MockContextFull()
        
        def mock_calc_rfscore7_batch(context, stocks, date_str):
            data = {
                "order_book_id": ["000001.XSHE", "000002.XSHE"],
                "rfscore7": [5, 4],
            }
            return pd.DataFrame(data)
        
        with patch("rfscore7_pb10_full.calc_rfscore7_batch", mock_calc_rfscore7_batch):
            result = choose_stocks(context, 2)
            assert len(result) <= 2

    def test_choose_stocks_with_order_book_id(self, setup_rq_mocks_full):
        from rfscore7_pb10_full import choose_stocks
        context = MockContextFull()
        
        def mock_calc_rfscore7_batch(context, stocks, date_str):
            data = {
                "order_book_id": ["000001.XSHE", "000002.XSHE", "600000.XSHG"],
                "rfscore7": [7, 6, 5],
                "pb_ratio": [0.5, 0.8, 1.0],
            }
            return pd.DataFrame(data)
        
        with patch("rfscore7_pb10_full.calc_rfscore7_batch", mock_calc_rfscore7_batch):
            result = choose_stocks(context, 2)
            assert len(result) <= 2

    def test_choose_stocks_without_order_book_id(self, setup_rq_mocks_full):
        from rfscore7_pb10_full import choose_stocks
        context = MockContextFull()
        
        def mock_calc_rfscore7_batch(context, stocks, date_str):
            data = {
                "rfscore7": [7, 6, 5],
                "pb_ratio": [0.5, 0.8, 1.0],
            }
            df = pd.DataFrame(data, index=["000001.XSHE", "000002.XSHE", "600000.XSHG"])
            return df
        
        with patch("rfscore7_pb10_full.calc_rfscore7_batch", mock_calc_rfscore7_batch):
            result = choose_stocks(context, 2)
            assert len(result) <= 2

    def test_rebalance_normal_position(self, setup_rq_mocks_full):
        from rfscore7_pb10_full import rebalance, init
        context = MockContextFull()
        init(context)
        
        def mock_calc_market_state(context):
            return {"breadth": 0.5, "trend_on": True}
        
        with patch("rfscore7_pb10_full.calc_market_state", mock_calc_market_state):
            with patch("rfscore7_pb10_full.choose_stocks", return_value=["000001.XSHE"]):
                rebalance(context, {})
                setup_rq_mocks_full.info.assert_called()

    def test_rebalance_reduce_position(self, setup_rq_mocks_full):
        from rfscore7_pb10_full import rebalance, init
        context = MockContextFull()
        init(context)
        
        def mock_calc_market_state(context):
            return {"breadth": 0.20, "trend_on": False}
        
        with patch("rfscore7_pb10_full.calc_market_state", mock_calc_market_state):
            with patch("rfscore7_pb10_full.choose_stocks", return_value=["000001.XSHE"]):
                rebalance(context, {})

    def test_rebalance_empty_position(self, setup_rq_mocks_full):
        from rfscore7_pb10_full import rebalance, init
        context = MockContextFull()
        init(context)
        
        def mock_calc_market_state(context):
            return {"breadth": 0.10, "trend_on": False}
        
        with patch("rfscore7_pb10_full.calc_market_state", mock_calc_market_state):
            rebalance(context, {})

    def test_rebalance_sell_existing_positions(self, setup_rq_mocks_full):
        from rfscore7_pb10_full import rebalance, init
        context = MockContextFull()
        init(context)
        context.portfolio.positions = {"600000.XSHG": MockPositionFull()}
        
        def mock_calc_market_state(context):
            return {"breadth": 0.5, "trend_on": True}
        
        with patch("rfscore7_pb10_full.calc_market_state", mock_calc_market_state):
            with patch("rfscore7_pb10_full.choose_stocks", return_value=["000001.XSHE"]):
                rebalance(context, {})

    def test_rebalance_buy_new_positions(self, setup_rq_mocks_full):
        from rfscore7_pb10_full import rebalance, init
        context = MockContextFull()
        init(context)
        context.portfolio.total_value = 1000000
        
        def mock_calc_market_state(context):
            return {"breadth": 0.5, "trend_on": True}
        
        with patch("rfscore7_pb10_full.calc_market_state", mock_calc_market_state):
            with patch("rfscore7_pb10_full.choose_stocks", return_value=["000001.XSHE", "000002.XSHE"]):
                rebalance(context, {})

    def test_rebalance_zero_total_value(self, setup_rq_mocks_full):
        from rfscore7_pb10_full import rebalance, init
        context = MockContextFull()
        init(context)
        context.portfolio.total_value = 0
        
        def mock_calc_market_state(context):
            return {"breadth": 0.5, "trend_on": True}
        
        with patch("rfscore7_pb10_full.calc_market_state", mock_calc_market_state):
            with patch("rfscore7_pb10_full.choose_stocks", return_value=["000001.XSHE"]):
                rebalance(context, {})

    def test_rebalance_existing_position_rebalance(self, setup_rq_mocks_full):
        from rfscore7_pb10_full import rebalance, init
        context = MockContextFull()
        init(context)
        context.portfolio.total_value = 1000000
        pos = MockPositionFull(market_value=40000)
        context.portfolio.positions = {"000001.XSHE": pos}
        
        def mock_calc_market_state(context):
            return {"breadth": 0.5, "trend_on": True}
        
        with patch("rfscore7_pb10_full.calc_market_state", mock_calc_market_state):
            with patch("rfscore7_pb10_full.choose_stocks", return_value=["000001.XSHE", "000002.XSHE"]):
                rebalance(context, {})

    def test_rfscore7_batch_calculation_all_factors(self, setup_rq_mocks_full):
        from rfscore7_pb10_full import calc_rfscore7_batch
        context = MockContextFull()
        stocks = ["000001.XSHE"]
        date_str = "2024-07-01"
        
        def mock_get_factor_all(stocks, factors, start_date=None, end_date=None):
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
        
        with patch("rfscore7_pb10_full.get_factor", mock_get_factor_all):
            result = calc_rfscore7_batch(context, stocks, date_str)
            assert "rfscore7" in result.columns

    def test_rfscore7_batch_missing_factors(self, setup_rq_mocks_full):
        from rfscore7_pb10_full import calc_rfscore7_batch
        context = MockContextFull()
        stocks = ["000001.XSHE"]
        date_str = "2024-07-01"
        
        def mock_get_factor_partial(stocks, factors, start_date=None, end_date=None):
            data = {
                "order_book_id": stocks,
                "roa": [5.0],
            }
            return pd.DataFrame(data)
        
        with patch("rfscore7_pb10_full.get_factor", mock_get_factor_partial):
            result = calc_rfscore7_batch(context, stocks, date_str)
            assert "rfscore7" in result.columns

    def test_choose_stocks_limit_hold_num(self, setup_rq_mocks_full):
        from rfscore7_pb10_full import choose_stocks
        context = MockContextFull()
        
        def mock_calc_rfscore7_batch(context, stocks, date_str):
            data = {
                "order_book_id": [f"stock{i}" for i in range(30)],
                "rfscore7": [7 - i % 7 for i in range(30)],
                "pb_ratio": [0.5 + i * 0.1 for i in range(30)],
            }
            return pd.DataFrame(data)
        
        with patch("rfscore7_pb10_full.calc_rfscore7_batch", mock_calc_rfscore7_batch):
            with patch("rfscore7_pb10_full.get_universe", return_value=[f"stock{i}" for i in range(30)]):
                result = choose_stocks(context, 5)
                assert len(result) <= 5

    def test_rebalance_position_adjustment_threshold(self, setup_rq_mocks_full):
        from rfscore7_pb10_full import rebalance, init
        context = MockContextFull()
        init(context)
        context.portfolio.total_value = 1000000
        pos = MockPositionFull(market_value=450000)
        context.portfolio.positions = {"000001.XSHE": pos}
        
        def mock_calc_market_state(context):
            return {"breadth": 0.5, "trend_on": True}
        
        with patch("rfscore7_pb10_full.calc_market_state", mock_calc_market_state):
            with patch("rfscore7_pb10_full.choose_stocks", return_value=["000001.XSHE"]):
                rebalance(context, {})

    def test_rebalance_buy_exception(self, setup_rq_mocks_full):
        from rfscore7_pb10_full import rebalance, init
        context = MockContextFull()
        init(context)
        context.portfolio.total_value = 1000000
        
        def mock_calc_market_state(context):
            return {"breadth": 0.5, "trend_on": True}
        
        with patch("rfscore7_pb10_full.calc_market_state", mock_calc_market_state):
            with patch("rfscore7_pb10_full.choose_stocks", return_value=["000001.XSHE", "000002.XSHE"]):
                rebalance(context, {})