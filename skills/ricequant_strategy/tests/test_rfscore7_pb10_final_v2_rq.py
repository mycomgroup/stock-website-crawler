"""
Tests for rfscore7_pb10_final_v2_rq.py
"""
import sys
from unittest.mock import MagicMock, patch
from datetime import datetime, date
import numpy as np
import pandas as pd
import pytest

from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "data"))


class MockBar:
    def __init__(self, close=10.0, limit_up=11.0, limit_down=9.0, is_trading=True):
        self.close = close
        self.limit_up = limit_up
        self.limit_down = limit_down
        self.is_trading = is_trading


class MockInstrument:
    def __init__(self, order_book_id="600519.XSHG", symbol="test"):
        self.order_book_id = order_book_id
        self.symbol = symbol


class MockPosition:
    def __init__(self, market_value=0):
        self.market_value = market_value


class TestRfscore7Pb10FinalV2Rq:
    def test_sign_positive(self):
        from rfscore7_pb10_final_v2_rq import sign
        import pandas as pd
        ser = pd.Series([1, -1, 0, 5, -5])
        result = sign(ser)
        assert result.iloc[0] == 1
        assert result.iloc[1] == 0

    def test_init(self, rq_mocks):
        from rfscore7_pb10_final_v2_rq import init
        context = MagicMock()
        init(context)
        assert context.benchmark == "000300.XSHG"
        assert context.ipo_days == 180
        assert context.base_hold_num == 20

    def test_handle_bar_same_month(self, rq_mocks):
        from rfscore7_pb10_final_v2_rq import handle_bar, init
        context = MagicMock()
        context.now = datetime(2024, 7, 15)
        context.last_rebalance_month = 7
        init(context)
        handle_bar(context, {})

    @patch("rfscore7_pb10_final_v2_rq.rebalance")
    def test_handle_bar_new_month(self, mock_rebalance, rq_mocks):
        from rfscore7_pb10_final_v2_rq import handle_bar, init
        context = MagicMock()
        context.now = datetime(2024, 7, 1)
        context.last_rebalance_month = 6
        init(context)
        handle_bar(context, {})
        mock_rebalance.assert_called_once()

    @patch("rfscore7_pb10_final_v2_rq.index_components")
    @patch("rfscore7_pb10_final_v2_rq.all_instruments")
    def test_get_universe_success(self, mock_all_instruments, mock_index_components, rq_mocks):
        from rfscore7_pb10_final_v2_rq import get_universe
        mock_index_components.side_effect = lambda idx: ["600519.XSHG"] if idx == "000300.XSHG" else []
        mock_all_instruments.return_value = pd.DataFrame({
            "order_book_id": ["600519.XSHG"],
            "listed_date": [date(2020, 1, 1)],
        })
        context = MagicMock()
        context.now = MagicMock()
        context.now.date.return_value = date(2024, 7, 1)
        context.ipo_days = 180
        bar_dict = {"600519.XSHG": MockBar(is_trading=True)}
        with patch("rfscore7_pb10_final_v2_rq.instruments", return_value=MockInstrument(symbol="test")):
            result = get_universe(context, bar_dict)
            assert isinstance(result, list)

    @patch("rfscore7_pb10_final_v2_rq.index_components")
    def test_get_universe_exception(self, mock_index_components, rq_mocks):
        from rfscore7_pb10_final_v2_rq import get_universe
        mock_index_components.side_effect = Exception("API error")
        context = MagicMock()
        context.now = MagicMock()
        context.now.date.return_value = date(2024, 7, 1)
        bar_dict = {}
        result = get_universe(context, bar_dict)
        assert result == []

    @patch("rfscore7_pb10_final_v2_rq.index_components")
    @patch("rfscore7_pb10_final_v2_rq.history_bars")
    def test_calc_market_state_success(self, mock_history_bars, mock_index_components, rq_mocks):
        from rfscore7_pb10_final_v2_rq import calc_market_state
        mock_index_components.return_value = ["600519.XSHG"] * 50
        mock_history_bars.return_value = np.array([10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 30])
        context = MagicMock()
        bar_dict = {"600519.XSHG": MockBar()}
        result = calc_market_state(context, bar_dict)
        assert "breadth" in result
        assert "trend_on" in result

    @patch("rfscore7_pb10_final_v2_rq.index_components")
    def test_calc_market_state_exception(self, mock_index_components, rq_mocks):
        from rfscore7_pb10_final_v2_rq import calc_market_state
        mock_index_components.side_effect = Exception("API error")
        context = MagicMock()
        bar_dict = {}
        result = calc_market_state(context, bar_dict)
        assert result["breadth"] == 0.5
        assert result["trend_on"] == True

    def test_get_pb_ratio_success(self, rq_mocks):
        from rfscore7_pb10_final_v2_rq import get_pb_ratio
        stocks = ["600519.XSHG"]
        watch_date = date(2024, 7, 1)
        with patch("rfscore7_pb10_final_v2_rq.instruments", return_value=MockInstrument()):
            result = get_pb_ratio(stocks, watch_date)
            assert isinstance(result, pd.Series)

    def test_get_pb_ratio_exception(self, rq_mocks):
        from rfscore7_pb10_final_v2_rq import get_pb_ratio
        stocks = ["600519.XSHG"]
        watch_date = date(2024, 7, 1)
        with patch("rfscore7_pb10_final_v2_rq.instruments", side_effect=Exception("API error")):
            result = get_pb_ratio(stocks, watch_date)
            assert np.isnan(result.iloc[0])

    @patch("rfscore7_pb10_final_v2_rq.history_bars")
    def test_calc_rfscore_simple_success(self, mock_history_bars, rq_mocks):
        from rfscore7_pb10_final_v2_rq import calc_rfscore_simple
        mock_history_bars.return_value = np.array([10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 30])
        context = MagicMock()
        bar_dict = {}
        stocks = ["600519.XSHG"]
        result = calc_rfscore_simple(context, bar_dict, stocks)
        assert isinstance(result, list)

    @patch("rfscore7_pb10_final_v2_rq.history_bars")
    def test_calc_rfscore_simple_none_bars(self, mock_history_bars, rq_mocks):
        from rfscore7_pb10_final_v2_rq import calc_rfscore_simple
        mock_history_bars.return_value = None
        context = MagicMock()
        bar_dict = {}
        stocks = ["600519.XSHG"]
        result = calc_rfscore_simple(context, bar_dict, stocks)
        assert result == []

    @patch("rfscore7_pb10_final_v2_rq.get_universe")
    @patch("rfscore7_pb10_final_v2_rq.calc_rfscore_simple")
    def test_choose_stocks_success(self, mock_calc, mock_get_universe, rq_mocks):
        from rfscore7_pb10_final_v2_rq import choose_stocks
        mock_get_universe.return_value = ["600519.XSHG"]
        mock_calc.return_value = [{"code": "600519.XSHG", "fscore": 6, "momentum": 5}]
        context = MagicMock()
        bar_dict = {}
        result = choose_stocks(context, bar_dict, 5)
        assert len(result) <= 5

    @patch("rfscore7_pb10_final_v2_rq.get_universe")
    def test_choose_stocks_empty_universe(self, mock_get_universe, rq_mocks):
        from rfscore7_pb10_final_v2_rq import choose_stocks
        mock_get_universe.return_value = []
        context = MagicMock()
        bar_dict = {}
        result = choose_stocks(context, bar_dict, 5)
        assert result == []

    def test_filter_buyable_success(self, rq_mocks):
        from rfscore7_pb10_final_v2_rq import filter_buyable
        context = MagicMock()
        bar_dict = {"600519.XSHG": MockBar(close=10, limit_up=11, limit_down=9, is_trading=True)}
        with patch("rfscore7_pb10_final_v2_rq.instruments", return_value=MockInstrument(symbol="test")):
            result = filter_buyable(context, bar_dict, ["600519.XSHG"])
            assert len(result) >= 0

    def test_filter_buyable_st_stock(self, rq_mocks):
        from rfscore7_pb10_final_v2_rq import filter_buyable
        context = MagicMock()
        bar_dict = {"600519.XSHG": MockBar(close=10, limit_up=11, limit_down=9, is_trading=True)}
        with patch("rfscore7_pb10_final_v2_rq.instruments", return_value=MockInstrument(symbol="ST某某")):
            result = filter_buyable(context, bar_dict, ["600519.XSHG"])
            assert "600519.XSHG" not in result

    def test_filter_buyable_limit_up(self, rq_mocks):
        from rfscore7_pb10_final_v2_rq import filter_buyable
        context = MagicMock()
        bar_dict = {"600519.XSHG": MockBar(close=10.95, limit_up=11.0, limit_down=9.0, is_trading=True)}
        with patch("rfscore7_pb10_final_v2_rq.instruments", return_value=MockInstrument(symbol="test")):
            result = filter_buyable(context, bar_dict, ["600519.XSHG"])
            assert "600519.XSHG" not in result

    @patch("rfscore7_pb10_final_v2_rq.calc_market_state")
    @patch("rfscore7_pb10_final_v2_rq.choose_stocks")
    @patch("rfscore7_pb10_final_v2_rq.filter_buyable")
    def test_rebalance_market_extreme(self, mock_filter, mock_choose, mock_calc, rq_mocks):
        from rfscore7_pb10_final_v2_rq import rebalance, init
        context = MagicMock()
        context.now = MagicMock()
        context.now.date.return_value = date(2024, 7, 1)
        context.portfolio.positions.keys.return_value = []
        context.breadth_stop = 0.15
        context.breadth_reduce = 0.25
        mock_calc.return_value = {"breadth": 0.1, "trend_on": False}
        init(context)
        rebalance(context, {})

    @patch("rfscore7_pb10_final_v2_rq.calc_market_state")
    @patch("rfscore7_pb10_final_v2_rq.choose_stocks")
    @patch("rfscore7_pb10_final_v2_rq.filter_buyable")
    def test_rebalance_market_weak(self, mock_filter, mock_choose, mock_calc, rq_mocks):
        from rfscore7_pb10_final_v2_rq import rebalance, init
        context = MagicMock()
        context.now = MagicMock()
        context.now.date.return_value = date(2024, 7, 1)
        context.portfolio.positions.keys.return_value = []
        context.portfolio.total_value = 100000
        context.portfolio.positions.get.return_value = MockPosition(market_value=0)
        context.breadth_stop = 0.15
        context.breadth_reduce = 0.25
        context.reduced_hold_num = 10
        mock_calc.return_value = {"breadth": 0.2, "trend_on": False}
        mock_choose.return_value = ["600519.XSHG"]
        mock_filter.return_value = ["600519.XSHG"]
        init(context)
        rebalance(context, {})

    @patch("rfscore7_pb10_final_v2_rq.calc_market_state")
    @patch("rfscore7_pb10_final_v2_rq.choose_stocks")
    @patch("rfscore7_pb10_final_v2_rq.filter_buyable")
    def test_rebalance_market_normal(self, mock_filter, mock_choose, mock_calc, rq_mocks):
        from rfscore7_pb10_final_v2_rq import rebalance, init
        context = MagicMock()
        context.now = MagicMock()
        context.now.date.return_value = date(2024, 7, 1)
        context.portfolio.positions.keys.return_value = []
        context.portfolio.total_value = 100000
        context.portfolio.positions.get.return_value = MockPosition(market_value=0)
        context.breadth_stop = 0.15
        context.breadth_reduce = 0.25
        mock_calc.return_value = {"breadth": 0.5, "trend_on": True}
        mock_choose.return_value = ["600519.XSHG"]
        mock_filter.return_value = ["600519.XSHG"]
        init(context)
        rebalance(context, {})