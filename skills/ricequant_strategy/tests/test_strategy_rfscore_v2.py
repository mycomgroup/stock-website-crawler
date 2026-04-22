"""
Tests for strategy_rfscore_v2.py
"""
import sys
from pathlib import Path
from unittest.mock import MagicMock, patch
from datetime import datetime
import numpy as np
import pandas as pd
import pytest

sys.path.insert(0, str(Path(__file__).parent.parent))


class MockPortfolioV2:
    def __init__(self):
        self.starting_cash = 1000000
        self.total_value = 1000000
        self.positions = {}


class MockContextV2:
    def __init__(self):
        self.now = datetime(2024, 7, 1)
        self.portfolio = MockPortfolioV2()
        self.benchmark = "000300.XSHG"
        self.use_real_price = True
        self.ipo_days = 180
        self.base_hold_num = 20
        self.reduced_hold_num = 10
        self.breadth_reduce = 0.25
        self.breadth_stop = 0.15
        self.primary_pb_group = 1
        self.reduced_pb_group = 2


class MockPositionV2:
    def __init__(self, market_value=50000, quantity=1000):
        self.market_value = market_value
        self.quantity = quantity


class MockSchedulerV2:
    def __init__(self):
        self.scheduled_functions = []
    
    def run_monthly(self, func, monthday=1):
        self.scheduled_functions.append((func, monthday))


@pytest.fixture(scope="module")
def setup_rq_mocks_v2():
    mock_logger = MagicMock()
    mock_scheduler = MockSchedulerV2()
    sys.modules["logger"] = mock_logger
    sys.modules["scheduler"] = mock_scheduler
    
    def mock_index_components(index_name):
        if index_name == "000300.XSHG":
            return ["600000.XSHG", "600519.XSHG", "000001.XSHE", "688001.XSHG"][:100]
        elif index_name == "000905.XSHG":
            return ["000002.XSHE", "600036.XSHG", "000651.XSHE", "688002.XSHG"][:100]
        return []
    
    def mock_history_bars(stock, bar_count, frequency, fields, include_now=False):
        if isinstance(fields, list):
            bars = {
                "close": np.array([10.0, 10.5, 11.0, 11.5, 12.0, 12.5, 13.0, 13.5, 14.0, 14.5,
                                  15.0, 15.5, 16.0, 16.5, 17.0, 17.5, 18.0, 18.5, 19.0, 20.0]),
                "volume": np.array([1000, 1100, 1200, 1300, 1400, 1500, 1600, 1700, 1800, 1900,
                                   2000, 2100, 2200, 2300, 2400, 2500, 2600, 2700, 2800, 3000]),
            }
            return bars
        if stock == "000300.XSHG":
            return np.array([3800, 3810, 3820, 3830, 3840, 3850, 3860, 3870, 3880, 3890,
                             3900, 3910, 3920, 3930, 3940, 3950, 3960, 3970, 3980, 4000])
        return np.array([10.0, 10.5, 11.0, 11.5, 12.0, 12.5, 13.0, 13.5, 14.0, 14.5,
                        15.0, 15.5, 16.0, 16.5, 17.0, 17.5, 18.0, 18.5, 19.0, 20.0])
    
    def mock_current_snapshot(stock):
        return MagicMock(last_price=20.0)
    
    def mock_order_target_value(stock, value):
        return None
    
    sys.modules["index_components"] = mock_index_components
    sys.modules["history_bars"] = mock_history_bars
    sys.modules["current_snapshot"] = mock_current_snapshot
    sys.modules["order_target_value"] = mock_order_target_value
    
    yield mock_logger
    
    del sys.modules["logger"]
    del sys.modules["scheduler"]


class TestStrategyRfscoreV2:
    def test_init(self, setup_rq_mocks_v2):
        from strategy_rfscore_v2 import init
        context = MockContextV2()
        init(context)
        assert context.benchmark == "000300.XSHG"
        assert context.use_real_price == True
        assert context.ipo_days == 180
        assert context.base_hold_num == 20
        assert context.reduced_hold_num == 10
        assert context.breadth_reduce == 0.25
        assert context.breadth_stop == 0.15
        assert context.primary_pb_group == 1
        assert context.reduced_pb_group == 2
        setup_rq_mocks_v2.info.assert_called()

    def test_get_universe_success(self, setup_rq_mocks_v2):
        from strategy_rfscore_v2 import get_universe
        context = MockContextV2()
        result = get_universe(context)
        assert len(result) <= 100
        assert "688001.XSHG" not in result

    def test_get_universe_logs_info(self, setup_rq_mocks_v2):
        from strategy_rfscore_v2 import get_universe
        context = MockContextV2()
        result = get_universe(context)
        setup_rq_mocks_v2.info.assert_called()

    def test_calc_rfscore_simple_success(self, setup_rq_mocks_v2):
        from strategy_rfscore_v2 import calc_rfscore_simple
        context = MockContextV2()
        result = calc_rfscore_simple(context, "000001.XSHE")
        assert result is not None
        assert 1 <= result <= 7

    def test_calc_rfscore_simple_none_bars(self, setup_rq_mocks_v2):
        from strategy_rfscore_v2 import calc_rfscore_simple
        context = MockContextV2()
        
        with patch("strategy_rfscore_v2.history_bars", return_value=None):
            result = calc_rfscore_simple(context, "000001.XSHE")
            assert result is None

    def test_calc_rfscore_simple_short_bars(self, setup_rq_mocks_v2):
        from strategy_rfscore_v2 import calc_rfscore_simple
        context = MockContextV2()
        
        with patch("strategy_rfscore_v2.history_bars", return_value=np.array([10, 11, 12])):
            result = calc_rfscore_simple(context, "000001.XSHE")
            assert result is None

    def test_calc_rfscore_simple_exception(self, setup_rq_mocks_v2):
        from strategy_rfscore_v2 import calc_rfscore_simple
        context = MockContextV2()
        
        with patch("strategy_rfscore_v2.history_bars", side_effect=Exception("API error")):
            result = calc_rfscore_simple(context, "000001.XSHE")
            assert result is None

    def test_calc_rfscore_simple_positive_momentum(self, setup_rq_mocks_v2):
        from strategy_rfscore_v2 import calc_rfscore_simple
        context = MockContextV2()
        
        def mock_bars_rising(stock, bar_count, frequency, fields, include_now=False):
            return {
                "close": np.array([10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 30]),
                "volume": np.array([100] * 20),
            }
        
        with patch("strategy_rfscore_v2.history_bars", mock_bars_rising):
            result = calc_rfscore_simple(context, "000001.XSHE")
            assert result >= 3

    def test_calc_rfscore_simple_negative_momentum(self, setup_rq_mocks_v2):
        from strategy_rfscore_v2 import calc_rfscore_simple
        context = MockContextV2()
        
        def mock_bars_falling(stock, bar_count, frequency, fields, include_now=False):
            return {
                "close": np.array([30, 29, 28, 27, 26, 25, 24, 23, 22, 21, 20, 19, 18, 17, 16, 15, 14, 13, 12, 10]),
                "volume": np.array([100] * 20),
            }
        
        with patch("strategy_rfscore_v2.history_bars", mock_bars_falling):
            result = calc_rfscore_simple(context, "000001.XSHE")
            assert result >= 1

    def test_calc_rfscore_simple_high_vol_ratio(self, setup_rq_mocks_v2):
        from strategy_rfscore_v2 import calc_rfscore_simple
        context = MockContextV2()
        
        def mock_bars_high_vol(stock, bar_count, frequency, fields, include_now=False):
            return {
                "close": np.array([10] * 20),
                "volume": np.array([100] * 15 + [200] * 5),
            }
        
        with patch("strategy_rfscore_v2.history_bars", mock_bars_high_vol):
            result = calc_rfscore_simple(context, "000001.XSHE")
            assert result is not None

    def test_calc_rfscore_simple_low_vol_ratio(self, setup_rq_mocks_v2):
        from strategy_rfscore_v2 import calc_rfscore_simple
        context = MockContextV2()
        
        def mock_bars_low_vol(stock, bar_count, frequency, fields, include_now=False):
            return {
                "close": np.array([10] * 20),
                "volume": np.array([200] * 15 + [100] * 5),
            }
        
        with patch("strategy_rfscore_v2.history_bars", mock_bars_low_vol):
            result = calc_rfscore_simple(context, "000001.XSHE")
            assert result is not None

    def test_calc_rfscore_simple_price_position_high(self, setup_rq_mocks_v2):
        from strategy_rfscore_v2 import calc_rfscore_simple
        context = MockContextV2()
        
        def mock_bars_high_pos(stock, bar_count, frequency, fields, include_now=False):
            return {
                "close": np.array([10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29]),
                "volume": np.array([100] * 20),
            }
        
        with patch("strategy_rfscore_v2.history_bars", mock_bars_high_pos):
            result = calc_rfscore_simple(context, "000001.XSHE")
            assert result >= 3

    def test_calc_rfscore_simple_price_position_low(self, setup_rq_mocks_v2):
        from strategy_rfscore_v2 import calc_rfscore_simple
        context = MockContextV2()
        
        def mock_bars_low_pos(stock, bar_count, frequency, fields, include_now=False):
            return {
                "close": np.array([29, 28, 27, 26, 25, 24, 23, 22, 21, 20, 19, 18, 17, 16, 15, 14, 13, 12, 11, 10]),
                "volume": np.array([100] * 20),
            }
        
        with patch("strategy_rfscore_v2.history_bars", mock_bars_low_pos):
            result = calc_rfscore_simple(context, "000001.XSHE")
            assert result >= 1

    def test_calc_rfscore_simple_zero_vol(self, setup_rq_mocks_v2):
        from strategy_rfscore_v2 import calc_rfscore_simple
        context = MockContextV2()
        
        def mock_bars_zero_vol(stock, bar_count, frequency, fields, include_now=False):
            return {
                "close": np.array([10] * 20),
                "volume": np.array([0] * 20),
            }
        
        with patch("strategy_rfscore_v2.history_bars", mock_bars_zero_vol):
            result = calc_rfscore_simple(context, "000001.XSHE")
            assert result is not None

    def test_calc_rfscore_simple_flat_price(self, setup_rq_mocks_v2):
        from strategy_rfscore_v2 import calc_rfscore_simple
        context = MockContextV2()
        
        def mock_bars_flat(stock, bar_count, frequency, fields, include_now=False):
            return {
                "close": np.array([10.0] * 20),
                "volume": np.array([100] * 20),
            }
        
        with patch("strategy_rfscore_v2.history_bars", mock_bars_flat):
            result = calc_rfscore_simple(context, "000001.XSHE")
            assert result is not None

    def test_get_stock_metrics_success(self, setup_rq_mocks_v2):
        from strategy_rfscore_v2 import get_stock_metrics
        context = MockContextV2()
        stocks = ["000001.XSHE", "000002.XSHE", "600000.XSHG"]
        result = get_stock_metrics(context, stocks)
        assert isinstance(result, list)

    def test_get_stock_metrics_empty_stocks(self, setup_rq_mocks_v2):
        from strategy_rfscore_v2 import get_stock_metrics
        context = MockContextV2()
        result = get_stock_metrics(context, [])
        assert result == []

    def test_get_stock_metrics_none_bars(self, setup_rq_mocks_v2):
        from strategy_rfscore_v2 import get_stock_metrics
        context = MockContextV2()
        
        with patch("strategy_rfscore_v2.history_bars", return_value=None):
            result = get_stock_metrics(context, ["000001.XSHE"])
            assert result == []

    def test_get_stock_metrics_exception_handling(self, setup_rq_mocks_v2):
        from strategy_rfscore_v2 import get_stock_metrics
        context = MockContextV2()
        
        def mock_bars_exception(stock, bar_count, frequency, fields, include_now=False):
            raise Exception("API error")
        
        with patch("strategy_rfscore_v2.history_bars", mock_bars_exception):
            result = get_stock_metrics(context, ["000001.XSHE"])
            assert isinstance(result, list)

    def test_get_stock_metrics_with_snapshot(self, setup_rq_mocks_v2):
        from strategy_rfscore_v2 import get_stock_metrics
        context = MockContextV2()
        stocks = ["000001.XSHE"]
        result = get_stock_metrics(context, stocks)
        assert isinstance(result, list)

    def test_calc_market_state_success(self, setup_rq_mocks_v2):
        from strategy_rfscore_v2 import calc_market_state
        context = MockContextV2()
        result = calc_market_state(context)
        assert "breadth" in result
        assert "trend_on" in result

    def test_calc_market_state_none_bars(self, setup_rq_mocks_v2):
        from strategy_rfscore_v2 import calc_market_state
        context = MockContextV2()
        
        with patch("strategy_rfscore_v2.history_bars", return_value=None):
            result = calc_market_state(context)
            assert result["breadth"] == 0.5
            assert result["trend_on"] == True

    def test_calc_market_state_short_bars(self, setup_rq_mocks_v2):
        from strategy_rfscore_v2 import calc_market_state
        context = MockContextV2()
        
        with patch("strategy_rfscore_v2.history_bars", return_value=np.array([10, 11, 12])):
            result = calc_market_state(context)
            assert result["breadth"] == 0.5
            assert result["trend_on"] == True

    def test_calc_market_state_trend_on(self, setup_rq_mocks_v2):
        from strategy_rfscore_v2 import calc_market_state
        context = MockContextV2()
        
        def mock_bars_trend_on(stock, bar_count, frequency, fields, include_now=False):
            if stock == "000300.XSHG":
                return np.array([3800] * 19 + [4000])
            return np.array([10] * 19 + [12])
        
        with patch("strategy_rfscore_v2.history_bars", mock_bars_trend_on):
            result = calc_market_state(context)
            assert result["trend_on"] == True

    def test_calc_market_state_trend_off(self, setup_rq_mocks_v2):
        from strategy_rfscore_v2 import calc_market_state
        context = MockContextV2()
        
        def mock_bars_trend_off(stock, bar_count, frequency, fields, include_now=False):
            if stock == "000300.XSHG":
                return np.array([4000] * 19 + [3800])
            return np.array([12] * 19 + [10])
        
        with patch("strategy_rfscore_v2.history_bars", mock_bars_trend_off):
            result = calc_market_state(context)
            assert result["trend_on"] == False

    def test_choose_stocks_success(self, setup_rq_mocks_v2):
        from strategy_rfscore_v2 import choose_stocks
        context = MockContextV2()
        result = choose_stocks(context, 5)
        assert isinstance(result, list)

    def test_choose_stocks_empty_metrics(self, setup_rq_mocks_v2):
        from strategy_rfscore_v2 import choose_stocks
        context = MockContextV2()
        
        with patch("strategy_rfscore_v2.get_stock_metrics", return_value=[]):
            result = choose_stocks(context, 5)
            assert result == []

    def test_choose_stocks_low_fscore(self, setup_rq_mocks_v2):
        from strategy_rfscore_v2 import choose_stocks
        context = MockContextV2()
        
        mock_metrics = [
            {"code": "000001.XSHE", "fscore": 3, "momentum": 5},
            {"code": "000002.XSHE", "fscore": 4, "momentum": 3},
        ]
        
        with patch("strategy_rfscore_v2.get_stock_metrics", return_value=mock_metrics):
            result = choose_stocks(context, 5)
            assert result == []

    def test_choose_stocks_high_fscore(self, setup_rq_mocks_v2):
        from strategy_rfscore_v2 import choose_stocks
        context = MockContextV2()
        
        mock_metrics = [
            {"code": "000001.XSHE", "fscore": 7, "momentum": 10},
            {"code": "000002.XSHE", "fscore": 6, "momentum": 5},
            {"code": "600000.XSHG", "fscore": 6, "momentum": 8},
        ]
        
        with patch("strategy_rfscore_v2.get_stock_metrics", return_value=mock_metrics):
            result = choose_stocks(context, 2)
            assert len(result) <= 2

    def test_choose_stocks_fscore_sorting(self, setup_rq_mocks_v2):
        from strategy_rfscore_v2 import choose_stocks
        context = MockContextV2()
        
        mock_metrics = [
            {"code": "000001.XSHE", "fscore": 6, "momentum": 1},
            {"code": "000002.XSHE", "fscore": 7, "momentum": 0},
        ]
        
        with patch("strategy_rfscore_v2.get_stock_metrics", return_value=mock_metrics):
            result = choose_stocks(context, 2)
            assert "000002.XSHE" in result

    def test_rebalance_normal_position(self, setup_rq_mocks_v2):
        from strategy_rfscore_v2 import rebalance, init
        context = MockContextV2()
        init(context)
        
        def mock_calc_market_state(context):
            return {"breadth": 0.5, "trend_on": True}
        
        with patch("strategy_rfscore_v2.calc_market_state", mock_calc_market_state):
            with patch("strategy_rfscore_v2.choose_stocks", return_value=["000001.XSHE"]):
                rebalance(context, {})
                setup_rq_mocks_v2.info.assert_called()

    def test_rebalance_reduce_position(self, setup_rq_mocks_v2):
        from strategy_rfscore_v2 import rebalance, init
        context = MockContextV2()
        init(context)
        
        def mock_calc_market_state(context):
            return {"breadth": 0.20, "trend_on": False}
        
        with patch("strategy_rfscore_v2.calc_market_state", mock_calc_market_state):
            with patch("strategy_rfscore_v2.choose_stocks", return_value=["000001.XSHE"]):
                rebalance(context, {})

    def test_rebalance_empty_position(self, setup_rq_mocks_v2):
        from strategy_rfscore_v2 import rebalance, init
        context = MockContextV2()
        init(context)
        
        def mock_calc_market_state(context):
            return {"breadth": 0.10, "trend_on": False}
        
        with patch("strategy_rfscore_v2.calc_market_state", mock_calc_market_state):
            rebalance(context, {})

    def test_rebalance_sell_existing_positions(self, setup_rq_mocks_v2):
        from strategy_rfscore_v2 import rebalance, init
        context = MockContextV2()
        init(context)
        context.portfolio.positions = {"600000.XSHG": MockPositionV2()}
        
        def mock_calc_market_state(context):
            return {"breadth": 0.5, "trend_on": True}
        
        with patch("strategy_rfscore_v2.calc_market_state", mock_calc_market_state):
            with patch("strategy_rfscore_v2.choose_stocks", return_value=["000001.XSHE"]):
                rebalance(context, {})

    def test_rebalance_buy_new_positions(self, setup_rq_mocks_v2):
        from strategy_rfscore_v2 import rebalance, init
        context = MockContextV2()
        init(context)
        context.portfolio.total_value = 1000000
        
        def mock_calc_market_state(context):
            return {"breadth": 0.5, "trend_on": True}
        
        with patch("strategy_rfscore_v2.calc_market_state", mock_calc_market_state):
            with patch("strategy_rfscore_v2.choose_stocks", return_value=["000001.XSHE", "000002.XSHE"]):
                rebalance(context, {})

    def test_rebalance_zero_total_value(self, setup_rq_mocks_v2):
        from strategy_rfscore_v2 import rebalance, init
        context = MockContextV2()
        init(context)
        context.portfolio.total_value = 0
        
        def mock_calc_market_state(context):
            return {"breadth": 0.5, "trend_on": True}
        
        with patch("strategy_rfscore_v2.calc_market_state", mock_calc_market_state):
            with patch("strategy_rfscore_v2.choose_stocks", return_value=["000001.XSHE"]):
                rebalance(context, {})

    def test_rebalance_existing_position_adjustment(self, setup_rq_mocks_v2):
        from strategy_rfscore_v2 import rebalance, init
        context = MockContextV2()
        init(context)
        context.portfolio.total_value = 1000000
        pos = MockPositionV2(market_value=450000, quantity=1000)
        context.portfolio.positions = {"000001.XSHE": pos}
        
        def mock_calc_market_state(context):
            return {"breadth": 0.5, "trend_on": True}
        
        with patch("strategy_rfscore_v2.calc_market_state", mock_calc_market_state):
            with patch("strategy_rfscore_v2.choose_stocks", return_value=["000001.XSHE"]):
                rebalance(context, {})

    def test_rebalance_position_threshold(self, setup_rq_mocks_v2):
        from strategy_rfscore_v2 import rebalance, init
        context = MockContextV2()
        init(context)
        context.portfolio.total_value = 1000000
        pos = MockPositionV2(market_value=500000, quantity=1000)
        context.portfolio.positions = {"000001.XSHE": pos}
        
        def mock_calc_market_state(context):
            return {"breadth": 0.5, "trend_on": True}
        
        with patch("strategy_rfscore_v2.calc_market_state", mock_calc_market_state):
            with patch("strategy_rfscore_v2.choose_stocks", return_value=["000001.XSHE"]):
                rebalance(context, {})

    def test_rebalance_position_below_threshold(self, setup_rq_mocks_v2):
        from strategy_rfscore_v2 import rebalance, init
        context = MockContextV2()
        init(context)
        context.portfolio.total_value = 1000000
        pos = MockPositionV2(market_value=950000, quantity=1000)
        context.portfolio.positions = {"000001.XSHE": pos}
        
        def mock_calc_market_state(context):
            return {"breadth": 0.5, "trend_on": True}
        
        with patch("strategy_rfscore_v2.calc_market_state", mock_calc_market_state):
            with patch("strategy_rfscore_v2.choose_stocks", return_value=["000001.XSHE"]):
                rebalance(context, {})

    def test_get_stock_metrics_limit_50(self, setup_rq_mocks_v2):
        from strategy_rfscore_v2 import get_stock_metrics
        context = MockContextV2()
        stocks = [f"stock{i}" for i in range(100)]
        result = get_stock_metrics(context, stocks)
        assert isinstance(result, list)