"""
Tests for rfscore7_enhanced_rq.py
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


class TestSentimentSwitch:
    def test_init(self):
        from rfscore7_enhanced_rq import SentimentSwitch
        ss = SentimentSwitch()
        assert ss.sentiment_score == 50
        assert ss.sentiment_state == 2

    @patch("rfscore7_enhanced_rq.all_instruments")
    def test_update_high_limit_up_count(self, mock_all_instruments):
        from rfscore7_enhanced_rq import SentimentSwitch
        mock_all_instruments.return_value = pd.DataFrame({"order_book_id": ["600519.XSHG"] * 50})
        ss = SentimentSwitch()
        bar_dict = {}
        for i in range(50):
            bar_dict[f"stock{i}"] = MockBar(close=10.95, limit_up=11.0, limit_down=9.0)
        ss.update(bar_dict)
        assert ss.sentiment_score >= 50

    @patch("rfscore7_enhanced_rq.all_instruments")
    def test_update_low_limit_up_count(self, mock_all_instruments):
        from rfscore7_enhanced_rq import SentimentSwitch
        mock_all_instruments.return_value = pd.DataFrame({"order_book_id": ["600519.XSHG"] * 50})
        ss = SentimentSwitch()
        bar_dict = {}
        for i in range(50):
            bar_dict[f"stock{i}"] = MockBar(close=9.05, limit_up=11.0, limit_down=9.0)
        ss.update(bar_dict)
        assert ss.sentiment_score < 50

    @patch("rfscore7_enhanced_rq.all_instruments")
    def test_update_exception(self, mock_all_instruments):
        from rfscore7_enhanced_rq import SentimentSwitch
        mock_all_instruments.side_effect = Exception("API error")
        ss = SentimentSwitch()
        ss.update({})
        assert ss.sentiment_score == 50

    def test_get_position_ratio_state_4(self):
        from rfscore7_enhanced_rq import SentimentSwitch
        ss = SentimentSwitch()
        ss.sentiment_state = 4
        assert ss.get_position_ratio() == 1.0

    def test_get_position_ratio_state_3(self):
        from rfscore7_enhanced_rq import SentimentSwitch
        ss = SentimentSwitch()
        ss.sentiment_state = 3
        assert ss.get_position_ratio() == 0.8

    def test_get_position_ratio_state_2(self):
        from rfscore7_enhanced_rq import SentimentSwitch
        ss = SentimentSwitch()
        ss.sentiment_state = 2
        assert ss.get_position_ratio() == 0.6

    def test_get_position_ratio_state_1(self):
        from rfscore7_enhanced_rq import SentimentSwitch
        ss = SentimentSwitch()
        ss.sentiment_state = 1
        assert ss.get_position_ratio() == 0.3

    def test_get_position_ratio_state_0(self):
        from rfscore7_enhanced_rq import SentimentSwitch
        ss = SentimentSwitch()
        ss.sentiment_state = 0
        assert ss.get_position_ratio() == 0.0

    def test_get_position_ratio_unknown_state(self):
        from rfscore7_enhanced_rq import SentimentSwitch
        ss = SentimentSwitch()
        ss.sentiment_state = 99
        assert ss.get_position_ratio() == 0.6


class TestRfscore7EnhancedRq:
    def test_init(self, rq_mocks):
        from rfscore7_enhanced_rq import init
        context = MagicMock()
        init(context)
        assert context.benchmark == "000300.XSHG"
        assert context.base_hold_num == 15
        assert context.defensive_hold_num == 12

    def test_handle_bar_same_month(self, rq_mocks):
        from rfscore7_enhanced_rq import handle_bar, init
        context = MagicMock()
        context.now = datetime(2024, 7, 15)
        context.last_rebalance_month = 7
        context.sentiment = MagicMock()
        context.sentiment.update = MagicMock()
        init(context)
        handle_bar(context, {})
        context.sentiment.update.assert_called_once()

    @patch("rfscore7_enhanced_rq.get_universe")
    @patch("rfscore7_enhanced_rq.calc_market_state")
    @patch("rfscore7_enhanced_rq.choose_stocks")
    def test_handle_bar_new_month(self, mock_choose, mock_calc, mock_get_universe, rq_mocks):
        from rfscore7_enhanced_rq import handle_bar, init
        context = MagicMock()
        context.now = datetime(2024, 7, 1)
        context.last_rebalance_month = 6
        context.portfolio.positions.keys.return_value = []
        context.portfolio.total_value = 100000
        context.sentiment = MagicMock()
        context.sentiment.get_position_ratio.return_value = 0.6
        context.sentiment.sentiment_state = 2
        mock_get_universe.return_value = ["600519.XSHG"]
        mock_calc.return_value = {"breadth": 0.5, "trend_on": True}
        mock_choose.return_value = ["600519.XSHG"]
        init(context)
        handle_bar(context, {})
        assert context.last_rebalance_month == 7

    @patch("rfscore7_enhanced_rq.get_universe")
    def test_handle_bar_empty_universe(self, mock_get_universe, rq_mocks):
        from rfscore7_enhanced_rq import handle_bar, init
        context = MagicMock()
        context.now = datetime(2024, 7, 1)
        context.last_rebalance_month = 6
        context.sentiment = MagicMock()
        context.sentiment.update = MagicMock()
        mock_get_universe.return_value = []
        init(context)
        handle_bar(context, {})

    @patch("rfscore7_enhanced_rq.index_components")
    def test_get_universe_success(self, mock_index_components, rq_mocks):
        from rfscore7_enhanced_rq import get_universe
        mock_index_components.side_effect = lambda idx: ["600519.XSHG", "688001.XSHG"] if idx == "000300.XSHG" else ["000001.XSHE"]
        context = MagicMock()
        bar_dict = {}
        result = get_universe(context, bar_dict)
        assert "688001.XSHG" not in result

    @patch("rfscore7_enhanced_rq.index_components")
    def test_get_universe_exception(self, mock_index_components, rq_mocks):
        from rfscore7_enhanced_rq import get_universe
        mock_index_components.side_effect = Exception("API error")
        context = MagicMock()
        bar_dict = {}
        result = get_universe(context, bar_dict)
        assert result == []

    @patch("rfscore7_enhanced_rq.index_components")
    @patch("rfscore7_enhanced_rq.history_bars")
    def test_calc_market_state_success(self, mock_history_bars, mock_index_components, rq_mocks):
        from rfscore7_enhanced_rq import calc_market_state
        mock_index_components.return_value = ["600519.XSHG"] * 50
        mock_history_bars.return_value = np.array([10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 30])
        context = MagicMock()
        bar_dict = {}
        result = calc_market_state(context, bar_dict)
        assert "breadth" in result
        assert "trend_on" in result

    @patch("rfscore7_enhanced_rq.index_components")
    def test_calc_market_state_exception(self, mock_index_components, rq_mocks):
        from rfscore7_enhanced_rq import calc_market_state
        mock_index_components.side_effect = Exception("API error")
        context = MagicMock()
        bar_dict = {}
        result = calc_market_state(context, bar_dict)
        assert result["breadth"] == 0.5
        assert result["trend_on"] == True

    @patch("rfscore7_enhanced_rq.history_bars")
    def test_choose_stocks_success(self, mock_history_bars, rq_mocks):
        from rfscore7_enhanced_rq import choose_stocks
        mock_history_bars.return_value = np.array([10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 30])
        context = MagicMock()
        bar_dict = {}
        stocks = ["600519.XSHG", "000001.XSHE"]
        result = choose_stocks(context, bar_dict, stocks, 5)
        assert len(result) <= 5

    @patch("rfscore7_enhanced_rq.history_bars")
    def test_choose_stocks_none_bars(self, mock_history_bars, rq_mocks):
        from rfscore7_enhanced_rq import choose_stocks
        mock_history_bars.return_value = None
        context = MagicMock()
        bar_dict = {}
        stocks = ["600519.XSHG"]
        result = choose_stocks(context, bar_dict, stocks, 5)
        assert result == []

    @patch("rfscore7_enhanced_rq.history_bars")
    def test_choose_stocks_short_bars(self, mock_history_bars, rq_mocks):
        from rfscore7_enhanced_rq import choose_stocks
        mock_history_bars.return_value = np.array([10, 11, 12])
        context = MagicMock()
        bar_dict = {}
        stocks = ["600519.XSHG"]
        result = choose_stocks(context, bar_dict, stocks, 5)
        assert result == []

    def test_handle_bar_zero_hold_num(self, rq_mocks):
        from rfscore7_enhanced_rq import handle_bar, init
        context = MagicMock()
        context.now = datetime(2024, 7, 1)
        context.last_rebalance_month = 6
        context.portfolio.positions.keys.return_value = ["600519.XSHG"]
        context.sentiment = MagicMock()
        context.sentiment.update = MagicMock()
        context.sentiment.get_position_ratio.return_value = 0.0
        context.sentiment.sentiment_state = 0
        context.extreme_hold_num = 0
        context.breadth_extreme = 0.15
        init(context)
        with patch("rfscore7_enhanced_rq.get_universe", return_value=["600519.XSHG"]):
            with patch("rfscore7_enhanced_rq.calc_market_state", return_value={"breadth": 0.1, "trend_on": False}):
                with patch("rfscore7_enhanced_rq.choose_stocks", return_value=[]):
                    handle_bar(context, {})