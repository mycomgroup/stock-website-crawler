"""
Tests for strategy_enhanced_rq.py
"""
import sys
from unittest.mock import MagicMock, patch
from datetime import datetime
import numpy as np
import pytest

from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "data"))


class TestStrategyEnhancedRq:
    def test_init(self, rq_mocks):
        from strategy_enhanced_rq import init
        context = MagicMock()
        init(context)
        assert context.benchmark == "000300.XSHG"
        assert context.base_hold_num == 15
        assert context.defensive_hold_num == 12
        assert context.bottom_hold_num == 10
        assert context.extreme_hold_num == 0

    def test_handle_bar_same_month(self, rq_mocks):
        from strategy_enhanced_rq import handle_bar, init
        context = MagicMock()
        context.now = datetime(2024, 7, 15)
        context.last_rebalance_month = 7
        init(context)
        handle_bar(context, {})

    @patch("strategy_enhanced_rq.get_universe")
    @patch("strategy_enhanced_rq.calc_market_state")
    @patch("strategy_enhanced_rq.get_hold_num")
    @patch("strategy_enhanced_rq.choose_stocks")
    def test_handle_bar_new_month(self, mock_choose, mock_get_hold, mock_calc, mock_get_universe, rq_mocks):
        from strategy_enhanced_rq import handle_bar, init
        context = MagicMock()
        context.now = datetime(2024, 7, 1)
        context.last_rebalance_month = 6
        context.portfolio.positions.keys.return_value = []
        context.portfolio.total_value = 100000
        mock_get_universe.return_value = ["600519.XSHG"]
        mock_calc.return_value = {"breadth": 0.5, "trend_on": True}
        mock_get_hold.return_value = 15
        mock_choose.return_value = ["600519.XSHG"]
        init(context)
        handle_bar(context, {})
        assert context.last_rebalance_month == 7

    @patch("strategy_enhanced_rq.get_universe")
    def test_handle_bar_empty_universe(self, mock_get_universe, rq_mocks):
        from strategy_enhanced_rq import handle_bar, init
        context = MagicMock()
        context.now = datetime(2024, 7, 1)
        context.last_rebalance_month = 6
        mock_get_universe.return_value = []
        init(context)
        handle_bar(context, {})

    @patch("strategy_enhanced_rq.get_hold_num")
    @patch("strategy_enhanced_rq.get_universe")
    def test_handle_bar_zero_hold(self, mock_get_universe, mock_get_hold, rq_mocks):
        from strategy_enhanced_rq import handle_bar, init
        context = MagicMock()
        context.now = datetime(2024, 7, 1)
        context.last_rebalance_month = 6
        context.portfolio.positions.keys.return_value = ["600519.XSHG"]
        mock_get_universe.return_value = ["600519.XSHG"]
        mock_get_hold.return_value = 0
        init(context)
        handle_bar(context, {})

    @patch("strategy_enhanced_rq.index_components")
    def test_get_universe_success(self, mock_index_components, rq_mocks):
        from strategy_enhanced_rq import get_universe
        mock_index_components.side_effect = lambda idx: ["600519.XSHG", "688001.XSHG"] if idx == "000300.XSHG" else ["000001.XSHE"]
        context = MagicMock()
        result = get_universe(context)
        assert "688001.XSHG" not in result

    @patch("strategy_enhanced_rq.index_components")
    def test_get_universe_exception(self, mock_index_components, rq_mocks):
        from strategy_enhanced_rq import get_universe
        mock_index_components.side_effect = Exception("API error")
        context = MagicMock()
        result = get_universe(context)
        assert result == []

    @patch("strategy_enhanced_rq.history_bars")
    @patch("strategy_enhanced_rq.index_components")
    def test_calc_market_state_success(self, mock_index_components, mock_history_bars, rq_mocks):
        from strategy_enhanced_rq import calc_market_state
        mock_index_components.return_value = ["600519.XSHG"] * 30
        mock_history_bars.return_value = np.array([10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 30])
        context = MagicMock()
        result = calc_market_state(context)
        assert "breadth" in result
        assert "trend_on" in result

    @patch("strategy_enhanced_rq.history_bars")
    def test_calc_market_state_none_bars(self, mock_history_bars, rq_mocks):
        from strategy_enhanced_rq import calc_market_state
        mock_history_bars.return_value = None
        context = MagicMock()
        result = calc_market_state(context)
        assert result["breadth"] == 0.5
        assert result["trend_on"] == True

    @patch("strategy_enhanced_rq.history_bars")
    def test_calc_market_state_short_bars(self, mock_history_bars, rq_mocks):
        from strategy_enhanced_rq import calc_market_state
        mock_history_bars.return_value = np.array([10, 11, 12])
        context = MagicMock()
        result = calc_market_state(context)
        assert result["breadth"] == 0.5
        assert result["trend_on"] == True

    def test_calc_market_state_exception(self, rq_mocks):
        from strategy_enhanced_rq import calc_market_state
        with patch("strategy_enhanced_rq.history_bars", side_effect=Exception("API error")):
            context = MagicMock()
            result = calc_market_state(context)
            assert result["breadth"] == 0.5
            assert result["trend_on"] == True

    def test_get_hold_num_extreme(self, rq_mocks):
        from strategy_enhanced_rq import get_hold_num, init
        context = MagicMock()
        context.extreme_hold_num = 0
        init(context)
        market_state = {"breadth": 0.1, "trend_on": False}
        result = get_hold_num(context, market_state)
        assert result == 0

    def test_get_hold_num_bottom(self, rq_mocks):
        from strategy_enhanced_rq import get_hold_num, init
        context = MagicMock()
        context.bottom_hold_num = 10
        init(context)
        market_state = {"breadth": 0.2, "trend_on": False}
        result = get_hold_num(context, market_state)
        assert result == 10

    def test_get_hold_num_defensive(self, rq_mocks):
        from strategy_enhanced_rq import get_hold_num, init
        context = MagicMock()
        context.defensive_hold_num = 12
        init(context)
        market_state = {"breadth": 0.3, "trend_on": False}
        result = get_hold_num(context, market_state)
        assert result == 12

    def test_get_hold_num_normal(self, rq_mocks):
        from strategy_enhanced_rq import get_hold_num, init
        context = MagicMock()
        context.base_hold_num = 15
        init(context)
        market_state = {"breadth": 0.5, "trend_on": True}
        result = get_hold_num(context, market_state)
        assert result == 15

    def test_get_hold_num_bottom_with_trend(self, rq_mocks):
        from strategy_enhanced_rq import get_hold_num, init
        context = MagicMock()
        context.base_hold_num = 15
        init(context)
        market_state = {"breadth": 0.2, "trend_on": True}
        result = get_hold_num(context, market_state)
        assert result == 15

    @patch("strategy_enhanced_rq.history_bars")
    def test_choose_stocks_success(self, mock_history_bars, rq_mocks):
        from strategy_enhanced_rq import choose_stocks
        mock_history_bars.return_value = np.array([10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 30])
        context = MagicMock()
        stocks = ["600519.XSHG", "000001.XSHE"]
        result = choose_stocks(context, stocks, 5)
        assert len(result) <= 5

    @patch("strategy_enhanced_rq.history_bars")
    def test_choose_stocks_none_bars(self, mock_history_bars, rq_mocks):
        from strategy_enhanced_rq import choose_stocks
        mock_history_bars.return_value = None
        context = MagicMock()
        stocks = ["600519.XSHG"]
        result = choose_stocks(context, stocks, 5)
        assert result == []

    @patch("strategy_enhanced_rq.history_bars")
    def test_choose_stocks_short_bars(self, mock_history_bars, rq_mocks):
        from strategy_enhanced_rq import choose_stocks
        mock_history_bars.return_value = np.array([10, 11, 12])
        context = MagicMock()
        stocks = ["600519.XSHG"]
        result = choose_stocks(context, stocks, 5)
        assert result == []

    @patch("strategy_enhanced_rq.history_bars")
    def test_choose_stocks_exception(self, mock_history_bars, rq_mocks):
        from strategy_enhanced_rq import choose_stocks
        mock_history_bars.side_effect = Exception("API error")
        context = MagicMock()
        stocks = ["600519.XSHG"]
        result = choose_stocks(context, stocks, 5)
        assert result == []