"""
Tests for rfscore7_original_rq.py
"""
import sys
from unittest.mock import MagicMock, patch
from datetime import datetime
import numpy as np
import pytest

from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "data"))


class TestRfscore7OriginalRq:
    def test_init(self, rq_mocks):
        from rfscore7_original_rq import init
        context = MagicMock()
        init(context)
        assert context.benchmark == "000300.XSHG"
        assert context.ipo_days == 180
        assert context.base_hold_num == 20
        assert context.reduced_hold_num == 10

    def test_handle_bar_same_month(self, rq_mocks):
        from rfscore7_original_rq import handle_bar, init
        context = MagicMock()
        context.now = datetime(2024, 7, 15)
        context.last_rebalance_month = 7
        init(context)
        handle_bar(context, {})

    @patch("rfscore7_original_rq.get_universe")
    @patch("rfscore7_original_rq.calc_market_state")
    @patch("rfscore7_original_rq.choose_stocks")
    def test_handle_bar_market_extreme(self, mock_choose, mock_calc, mock_get_universe, rq_mocks):
        from rfscore7_original_rq import handle_bar, init
        context = MagicMock()
        context.now = datetime(2024, 7, 1)
        context.last_rebalance_month = 6
        context.portfolio.positions.keys.return_value = []
        context.breadth_stop = 0.15
        context.breadth_reduce = 0.25
        mock_get_universe.return_value = ["600519.XSHG"]
        mock_calc.return_value = {"breadth": 0.1, "trend_on": False}
        init(context)
        handle_bar(context, {})
        assert context.last_rebalance_month == 7

    @patch("rfscore7_original_rq.get_universe")
    @patch("rfscore7_original_rq.calc_market_state")
    @patch("rfscore7_original_rq.choose_stocks")
    def test_handle_bar_market_weak(self, mock_choose, mock_calc, mock_get_universe, rq_mocks):
        from rfscore7_original_rq import handle_bar, init
        context = MagicMock()
        context.now = datetime(2024, 7, 1)
        context.last_rebalance_month = 6
        context.portfolio.positions.keys.return_value = []
        context.portfolio.total_value = 100000
        context.breadth_stop = 0.15
        context.breadth_reduce = 0.25
        context.reduced_hold_num = 10
        mock_get_universe.return_value = ["600519.XSHG"]
        mock_calc.return_value = {"breadth": 0.2, "trend_on": False}
        mock_choose.return_value = ["600519.XSHG"]
        init(context)
        handle_bar(context, {})

    @patch("rfscore7_original_rq.get_universe")
    @patch("rfscore7_original_rq.calc_market_state")
    @patch("rfscore7_original_rq.choose_stocks")
    def test_handle_bar_market_normal(self, mock_choose, mock_calc, mock_get_universe, rq_mocks):
        from rfscore7_original_rq import handle_bar, init
        context = MagicMock()
        context.now = datetime(2024, 7, 1)
        context.last_rebalance_month = 6
        context.portfolio.positions.keys.return_value = []
        context.portfolio.total_value = 100000
        context.breadth_stop = 0.15
        context.breadth_reduce = 0.25
        mock_get_universe.return_value = ["600519.XSHG"]
        mock_calc.return_value = {"breadth": 0.5, "trend_on": True}
        mock_choose.return_value = ["600519.XSHG"]
        init(context)
        handle_bar(context, {})

    @patch("rfscore7_original_rq.get_universe")
    def test_handle_bar_empty_universe(self, mock_get_universe, rq_mocks):
        from rfscore7_original_rq import handle_bar, init
        context = MagicMock()
        context.now = datetime(2024, 7, 1)
        context.last_rebalance_month = 6
        mock_get_universe.return_value = []
        init(context)
        handle_bar(context, {})

    @patch("rfscore7_original_rq.index_components")
    def test_get_universe_success(self, mock_index_components, rq_mocks):
        from rfscore7_original_rq import get_universe
        mock_index_components.side_effect = lambda idx: ["600519.XSHG", "688001.XSHG"] if idx == "000300.XSHG" else ["000001.XSHE"]
        context = MagicMock()
        bar_dict = {}
        result = get_universe(context, bar_dict)
        assert "688001.XSHG" not in result

    @patch("rfscore7_original_rq.index_components")
    def test_get_universe_exception(self, mock_index_components, rq_mocks):
        from rfscore7_original_rq import get_universe
        mock_index_components.side_effect = Exception("API error")
        context = MagicMock()
        bar_dict = {}
        result = get_universe(context, bar_dict)
        assert result == []

    @patch("rfscore7_original_rq.index_components")
    @patch("rfscore7_original_rq.history_bars")
    def test_calc_market_state_success(self, mock_history_bars, mock_index_components, rq_mocks):
        from rfscore7_original_rq import calc_market_state
        mock_index_components.return_value = ["600519.XSHG"] * 50
        mock_history_bars.return_value = np.array([10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 30])
        context = MagicMock()
        bar_dict = {}
        result = calc_market_state(context, bar_dict)
        assert "breadth" in result
        assert "trend_on" in result

    @patch("rfscore7_original_rq.index_components")
    def test_calc_market_state_exception(self, mock_index_components, rq_mocks):
        from rfscore7_original_rq import calc_market_state
        mock_index_components.side_effect = Exception("API error")
        context = MagicMock()
        bar_dict = {}
        result = calc_market_state(context, bar_dict)
        assert result["breadth"] == 0.5
        assert result["trend_on"] == True

    @patch("rfscore7_original_rq.history_bars")
    def test_choose_stocks_success(self, mock_history_bars, rq_mocks):
        from rfscore7_original_rq import choose_stocks
        mock_history_bars.return_value = np.array([10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 30])
        context = MagicMock()
        bar_dict = {}
        stocks = ["600519.XSHG", "000001.XSHE"]
        result = choose_stocks(context, bar_dict, stocks, 5)
        assert len(result) <= 5

    @patch("rfscore7_original_rq.history_bars")
    def test_choose_stocks_none_bars(self, mock_history_bars, rq_mocks):
        from rfscore7_original_rq import choose_stocks
        mock_history_bars.return_value = None
        context = MagicMock()
        bar_dict = {}
        stocks = ["600519.XSHG"]
        result = choose_stocks(context, bar_dict, stocks, 5)
        assert result == []

    @patch("rfscore7_original_rq.history_bars")
    def test_choose_stocks_short_bars(self, mock_history_bars, rq_mocks):
        from rfscore7_original_rq import choose_stocks
        mock_history_bars.return_value = np.array([10, 11, 12])
        context = MagicMock()
        bar_dict = {}
        stocks = ["600519.XSHG"]
        result = choose_stocks(context, bar_dict, stocks, 5)
        assert result == []

    @patch("rfscore7_original_rq.history_bars")
    def test_choose_stocks_exception(self, mock_history_bars, rq_mocks):
        from rfscore7_original_rq import choose_stocks
        mock_history_bars.side_effect = Exception("API error")
        context = MagicMock()
        bar_dict = {}
        stocks = ["600519.XSHG"]
        result = choose_stocks(context, bar_dict, stocks, 5)
        assert result == []