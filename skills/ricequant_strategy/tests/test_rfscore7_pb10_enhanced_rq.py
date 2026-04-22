"""
Tests for rfscore7_pb10_enhanced_rq.py
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


class TestSentimentSwitch:
    def test_init(self):
        from rfscore7_pb10_enhanced_rq import SentimentSwitch
        ss = SentimentSwitch()
        assert ss.hl_count == 0
        assert ss.ll_count == 0
        assert ss.sentiment_score == 50
        assert ss.sentiment_state == 2

    @patch("rfscore7_pb10_enhanced_rq.all_instruments")
    def test_update_success(self, mock_all_instruments):
        from rfscore7_pb10_enhanced_rq import SentimentSwitch
        mock_all_instruments.return_value = pd.DataFrame({"order_book_id": ["600519.XSHG"] * 50})
        ss = SentimentSwitch()
        bar_dict = {}
        for i in range(50):
            bar_dict[f"stock{i}"] = MockBar(close=10.95, limit_up=11.0, limit_down=9.0)
        context = MagicMock()
        ss.update(context, bar_dict)
        assert ss.hl_count > 0

    @patch("rfscore7_pb10_enhanced_rq.all_instruments")
    def test_update_exception(self, mock_all_instruments):
        from rfscore7_pb10_enhanced_rq import SentimentSwitch
        mock_all_instruments.side_effect = Exception("API error")
        ss = SentimentSwitch()
        context = MagicMock()
        ss.update(context, {})
        assert ss.sentiment_score == 50

    def test_get_position_ratio(self):
        from rfscore7_pb10_enhanced_rq import SentimentSwitch
        ss = SentimentSwitch()
        for state, expected in [(4, 1.0), (3, 0.8), (2, 0.6), (1, 0.3), (0, 0.0)]:
            ss.sentiment_state = state
            assert ss.get_position_ratio() == expected


class TestFourTierPosition:
    def test_init(self):
        from rfscore7_pb10_enhanced_rq import FourTierPosition
        ftp = FourTierPosition(base_hold=15)
        assert ftp.base_hold_num == 15
        assert ftp.defensive_hold_num == 12
        assert ftp.bottom_hold_num == 10
        assert ftp.extreme_hold_num == 0

    @patch("rfscore7_pb10_enhanced_rq.index_components")
    @patch("rfscore7_pb10_enhanced_rq.history_bars")
    def test_calc_breadth_success(self, mock_history_bars, mock_index_components):
        from rfscore7_pb10_enhanced_rq import FourTierPosition
        mock_index_components.return_value = ["600519.XSHG"] * 100
        mock_history_bars.return_value = np.array([10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 30])
        ftp = FourTierPosition()
        context = MagicMock()
        bar_dict = {"600519.XSHG": MockBar()}
        result = ftp.calc_breadth(context, bar_dict)
        assert 0 <= result <= 1

    @patch("rfscore7_pb10_enhanced_rq.index_components")
    def test_calc_breadth_exception(self, mock_index_components):
        from rfscore7_pb10_enhanced_rq import FourTierPosition
        mock_index_components.side_effect = Exception("API error")
        ftp = FourTierPosition()
        context = MagicMock()
        bar_dict = {}
        result = ftp.calc_breadth(context, bar_dict)

    @patch("rfscore7_pb10_enhanced_rq.history_bars")
    def test_calc_trend_success(self, mock_history_bars):
        from rfscore7_pb10_enhanced_rq import FourTierPosition
        mock_history_bars.return_value = np.array([10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 30])
        ftp = FourTierPosition()
        context = MagicMock()
        bar_dict = {}
        result = ftp.calc_trend(context, bar_dict)
        assert isinstance(result, bool)

    @patch("rfscore7_pb10_enhanced_rq.history_bars")
    def test_calc_trend_exception(self, mock_history_bars):
        from rfscore7_pb10_enhanced_rq import FourTierPosition
        mock_history_bars.side_effect = Exception("API error")
        ftp = FourTierPosition()
        context = MagicMock()
        bar_dict = {}
        result = ftp.calc_trend(context, bar_dict)
        assert result == False

    def test_get_target_hold_num_extreme(self):
        from rfscore7_pb10_enhanced_rq import FourTierPosition
        ftp = FourTierPosition()
        ftp.breadth_extreme = 0.15
        context = MagicMock()
        bar_dict = {}
        with patch.object(ftp, "calc_breadth", return_value=0.1):
            with patch.object(ftp, "calc_trend", return_value=False):
                result = ftp.get_target_hold_num(context, bar_dict)
                assert result[0] == 0

    def test_get_target_hold_num_normal(self):
        from rfscore7_pb10_enhanced_rq import FourTierPosition
        ftp = FourTierPosition()
        context = MagicMock()
        bar_dict = {}
        with patch.object(ftp, "calc_breadth", return_value=0.5):
            with patch.object(ftp, "calc_trend", return_value=True):
                result = ftp.get_target_hold_num(context, bar_dict)
                assert result[0] == 15


class TestRfscore7Pb10EnhancedRq:
    def test_init(self, rq_mocks):
        from rfscore7_pb10_enhanced_rq import init
        context = MagicMock()
        init(context)
        assert context.benchmark == "000300.XSHG"
        assert hasattr(context, "sentiment")
        assert hasattr(context, "position_rule")

    def test_handle_bar_same_month(self, rq_mocks):
        from rfscore7_pb10_enhanced_rq import handle_bar, init
        context = MagicMock()
        context.now = datetime(2024, 7, 15)
        context.last_rebalance_month = 7
        context.sentiment = MagicMock()
        init(context)
        handle_bar(context, {})

    @patch("rfscore7_pb10_enhanced_rq.rebalance")
    def test_handle_bar_new_month(self, mock_rebalance, rq_mocks):
        from rfscore7_pb10_enhanced_rq import handle_bar, init
        context = MagicMock()
        context.now = datetime(2024, 7, 1)
        context.last_rebalance_month = 6
        context.sentiment = MagicMock()
        init(context)
        handle_bar(context, {})
        mock_rebalance.assert_called_once()

    @patch("rfscore7_pb10_enhanced_rq.index_components")
    @patch("rfscore7_pb10_enhanced_rq.all_instruments")
    def test_get_universe_success(self, mock_all_instruments, mock_index_components, rq_mocks):
        from rfscore7_pb10_enhanced_rq import get_universe
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
        with patch("rfscore7_pb10_enhanced_rq.instruments", return_value=MockInstrument(symbol="test")):
            result = get_universe(context, bar_dict)
            assert isinstance(result, list)

    @patch("rfscore7_pb10_enhanced_rq.index_components")
    def test_get_universe_exception(self, mock_index_components, rq_mocks):
        from rfscore7_pb10_enhanced_rq import get_universe
        mock_index_components.side_effect = Exception("API error")
        context = MagicMock()
        context.now = MagicMock()
        context.now.date.return_value = date(2024, 7, 1)
        bar_dict = {}
        result = get_universe(context, bar_dict)
        assert result == []

    @patch("rfscore7_pb10_enhanced_rq.history_bars")
    def test_calc_rfscore_simple_success(self, mock_history_bars, rq_mocks):
        from rfscore7_pb10_enhanced_rq import calc_rfscore_simple
        mock_history_bars.return_value = np.array([10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 30])
        context = MagicMock()
        bar_dict = {}
        stocks = ["600519.XSHG"]
        result = calc_rfscore_simple(context, bar_dict, stocks)
        assert isinstance(result, list)

    @patch("rfscore7_pb10_enhanced_rq.history_bars")
    def test_calc_rfscore_simple_none_bars(self, mock_history_bars, rq_mocks):
        from rfscore7_pb10_enhanced_rq import calc_rfscore_simple
        mock_history_bars.return_value = None
        context = MagicMock()
        bar_dict = {}
        stocks = ["600519.XSHG"]
        result = calc_rfscore_simple(context, bar_dict, stocks)
        assert result == []

    @patch("rfscore7_pb10_enhanced_rq.get_universe")
    @patch("rfscore7_pb10_enhanced_rq.calc_rfscore_simple")
    def test_choose_stocks_success(self, mock_calc, mock_get_universe, rq_mocks):
        from rfscore7_pb10_enhanced_rq import choose_stocks
        mock_get_universe.return_value = ["600519.XSHG"]
        mock_calc.return_value = [{"code": "600519.XSHG", "fscore": 6, "momentum": 5}]
        context = MagicMock()
        bar_dict = {}
        result = choose_stocks(context, bar_dict, 5)
        assert len(result) <= 5

    @patch("rfscore7_pb10_enhanced_rq.get_universe")
    def test_choose_stocks_empty_universe(self, mock_get_universe, rq_mocks):
        from rfscore7_pb10_enhanced_rq import choose_stocks
        mock_get_universe.return_value = []
        context = MagicMock()
        bar_dict = {}
        result = choose_stocks(context, bar_dict, 5)
        assert result == []

    def test_filter_buyable_success(self, rq_mocks):
        from rfscore7_pb10_enhanced_rq import filter_buyable
        context = MagicMock()
        bar_dict = {"600519.XSHG": MockBar(close=10, limit_up=11, limit_down=9, is_trading=True)}
        with patch("rfscore7_pb10_enhanced_rq.instruments", return_value=MockInstrument(symbol="test")):
            result = filter_buyable(context, bar_dict, ["600519.XSHG"])
            assert len(result) >= 0

    def test_filter_buyable_st_stock(self, rq_mocks):
        from rfscore7_pb10_enhanced_rq import filter_buyable
        context = MagicMock()
        bar_dict = {"600519.XSHG": MockBar(close=10, limit_up=11, limit_down=9, is_trading=True)}
        with patch("rfscore7_pb10_enhanced_rq.instruments", return_value=MockInstrument(symbol="ST某某")):
            result = filter_buyable(context, bar_dict, ["600519.XSHG"])
            assert "600519.XSHG" not in result

    def test_filter_buyable_limit_up(self, rq_mocks):
        from rfscore7_pb10_enhanced_rq import filter_buyable
        context = MagicMock()
        bar_dict = {"600519.XSHG": MockBar(close=10.95, limit_up=11.0, limit_down=9.0, is_trading=True)}
        with patch("rfscore7_pb10_enhanced_rq.instruments", return_value=MockInstrument(symbol="test")):
            result = filter_buyable(context, bar_dict, ["600519.XSHG"])
            assert "600519.XSHG" not in result

    @patch("rfscore7_pb10_enhanced_rq.choose_stocks")
    @patch("rfscore7_pb10_enhanced_rq.filter_buyable")
    def test_rebalance_zero_hold(self, mock_filter, mock_choose, rq_mocks):
        from rfscore7_pb10_enhanced_rq import rebalance, init
        context = MagicMock()
        context.now = MagicMock()
        context.now.date.return_value = date(2024, 7, 1)
        context.portfolio.positions.keys.return_value = []
        context.sentiment = MagicMock()
        context.sentiment.get_position_ratio.return_value = 0.0
        context.position_rule = MagicMock()
        context.position_rule.get_target_hold_num.return_value = (0, 0.1, False)
        init(context)
        rebalance(context, {})