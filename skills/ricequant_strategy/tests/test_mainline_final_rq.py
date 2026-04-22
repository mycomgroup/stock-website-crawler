"""
Tests for mainline_final_rq.py
"""
import sys
from unittest.mock import MagicMock, patch, call
from datetime import datetime, date
import numpy as np
import pytest

from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "data"))


class TestMainlineFinalRq:
    def test_init(self, rq_mocks):
        from mainline_final_rq import init
        context = MagicMock()
        context.now = datetime(2024, 7, 1)
        init(context)
        assert context.hold_num == 10
        assert context.last_rebalance_month == -1

    def test_handle_bar_same_month(self, rq_mocks):
        from mainline_final_rq import handle_bar, init
        context = MagicMock()
        context.now = datetime(2024, 7, 15)
        context.last_rebalance_month = 7
        context.portfolio.positions.keys.return_value = []
        init(context)
        handle_bar(context, {})
        context.portfolio.positions.keys.assert_not_called()

    @patch("mainline_final_rq.get_universe")
    @patch("mainline_final_rq.choose_stocks")
    def test_handle_bar_new_month(self, mock_choose_stocks, mock_get_universe, rq_mocks):
        from mainline_final_rq import handle_bar, init
        context = MagicMock()
        context.now = datetime(2024, 7, 1)
        context.last_rebalance_month = 6
        context.portfolio.positions.keys.return_value = ["600519.XSHG"]
        context.portfolio.total_value = 1000000
        mock_get_universe.return_value = ["000001.XSHE", "000002.XSHE"]
        mock_choose_stocks.return_value = ["000001.XSHE"]
        init(context)
        handle_bar(context, {})
        assert context.last_rebalance_month == 7

    @patch("mainline_final_rq.get_universe")
    def test_handle_bar_empty_universe(self, mock_get_universe, rq_mocks):
        from mainline_final_rq import handle_bar, init
        context = MagicMock()
        context.now = datetime(2024, 7, 1)
        context.last_rebalance_month = 6
        mock_get_universe.return_value = []
        init(context)
        handle_bar(context, {})
        assert context.last_rebalance_month == 7

    @patch("mainline_final_rq.index_components")
    def test_get_universe_success(self, mock_index_components, rq_mocks):
        from mainline_final_rq import get_universe
        mock_index_components.side_effect = lambda idx: ["600519.XSHG", "000001.XSHE"] if idx == "000300.XSHG" else ["000002.XSHE", "688001.XSHG"]
        context = MagicMock()
        result = get_universe(context)
        assert "600519.XSHG" in result
        assert "688001.XSHG" not in result

    @patch("mainline_final_rq.index_components")
    def test_get_universe_exception(self, mock_index_components, rq_mocks):
        from mainline_final_rq import get_universe
        mock_index_components.side_effect = Exception("API error")
        context = MagicMock()
        result = get_universe(context)
        assert result == []

    @patch("mainline_final_rq.history_bars")
    def test_choose_stocks_success(self, mock_history_bars, rq_mocks):
        from mainline_final_rq import choose_stocks
        mock_history_bars.return_value = np.array([10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 30])
        context = MagicMock()
        stocks = ["600519.XSHG", "000001.XSHE"]
        result = choose_stocks(context, stocks, 5)
        assert len(result) <= 5

    @patch("mainline_final_rq.history_bars")
    def test_choose_stocks_none_bars(self, mock_history_bars, rq_mocks):
        from mainline_final_rq import choose_stocks
        mock_history_bars.return_value = None
        context = MagicMock()
        stocks = ["600519.XSHG"]
        result = choose_stocks(context, stocks, 5)
        assert result == []

    @patch("mainline_final_rq.history_bars")
    def test_choose_stocks_short_bars(self, mock_history_bars, rq_mocks):
        from mainline_final_rq import choose_stocks
        mock_history_bars.return_value = np.array([10, 11, 12])
        context = MagicMock()
        stocks = ["600519.XSHG"]
        result = choose_stocks(context, stocks, 5)
        assert result == []

    @patch("mainline_final_rq.history_bars")
    def test_choose_stocks_exception(self, mock_history_bars, rq_mocks):
        from mainline_final_rq import choose_stocks
        mock_history_bars.side_effect = Exception("API error")
        context = MagicMock()
        stocks = ["600519.XSHG"]
        result = choose_stocks(context, stocks, 5)
        assert result == []

    @patch("mainline_final_rq.history_bars")
    def test_choose_stocks_momentum_negative(self, mock_history_bars, rq_mocks):
        from mainline_final_rq import choose_stocks
        mock_history_bars.return_value = np.array([30, 29, 28, 27, 26, 25, 24, 23, 22, 21, 20, 19, 18, 17, 16, 15, 14, 13, 12, 10])
        context = MagicMock()
        stocks = ["600519.XSHG"]
        result = choose_stocks(context, stocks, 5)
        assert "600519.XSHG" not in result

    @patch("mainline_final_rq.history_bars")
    def test_choose_stocks_below_ma20(self, mock_history_bars, rq_mocks):
        from mainline_final_rq import choose_stocks
        mock_history_bars.return_value = np.array([10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 8])
        context = MagicMock()
        stocks = ["600519.XSHG"]
        result = choose_stocks(context, stocks, 5)
        assert "600519.XSHG" not in result

    @patch("mainline_final_rq.history_bars")
    def test_choose_stocks_multiple_stocks(self, mock_history_bars, rq_mocks):
        from mainline_final_rq import choose_stocks
        call_count = [0]
        def side_effect(*args, **kwargs):
            call_count[0] += 1
            base = 10 + call_count[0]
            return np.array([base] * 19 + [base * 1.2])
        mock_history_bars.side_effect = side_effect
        context = MagicMock()
        stocks = ["600519.XSHG", "000001.XSHE", "000002.XSHE"]
        result = choose_stocks(context, stocks, 2)
        assert len(result) <= 2

    @patch("mainline_final_rq.history_bars")
    def test_choose_stocks_limit_stocks(self, mock_history_bars, rq_mocks):
        from mainline_final_rq import choose_stocks
        mock_history_bars.return_value = np.array([10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 30])
        context = MagicMock()
        stocks = ["600519.XSHG"] * 150
        result = choose_stocks(context, stocks, 10)
        assert len(result) <= 10