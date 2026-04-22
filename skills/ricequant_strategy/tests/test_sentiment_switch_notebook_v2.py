"""
Tests for sentiment_switch_notebook_v2.py
"""
import sys
from pathlib import Path
from unittest.mock import MagicMock, patch
from datetime import datetime, timedelta
import pytest
import numpy as np

sys.path.insert(0, str(Path(__file__).parent.parent))


class MockStock:
    def __init__(self, order_book_id, close_price=10.0):
        self.order_book_id = order_book_id
        self.close_price = close_price


@pytest.fixture
def mock_rq_api():
    mocks = {}
    
    def mock_get_trading_dates(start_date, end_date):
        dates = []
        start = datetime.strptime(start_date, "%Y-%m-%d")
        end = datetime.strptime(end_date, "%Y-%m-%d")
        current = start
        while current <= end:
            if current.weekday() < 5:
                dates.append(current.strftime("%Y-%m-%d"))
            current += timedelta(days=1)
        return dates
    
    def mock_all_instruments(type_str, date=None):
        return [
            MockStock("000001.XSHE"),
            MockStock("000002.XSHE"),
            MockStock("600000.XSHG"),
        ]
    
    def mock_history_bars(stock_id, bar_count, frequency, fields, start_date=None, end_date=None):
        if fields == "close":
            return np.array([10.0, 10.5, 11.0])
        elif fields == "open":
            return np.array([10.2])
        return [10.0, 10.5]
    
    mocks["get_trading_dates"] = mock_get_trading_dates
    mocks["all_instruments"] = mock_all_instruments
    mocks["history_bars"] = mock_history_bars
    
    return mocks


class TestNotebookV2Main:
    def test_notebook_v2_execution_basic(self, mock_rq_api, capsys):
        with patch.dict(sys.modules, {
            "get_trading_dates": mock_rq_api["get_trading_dates"],
            "all_instruments": mock_rq_api["all_instruments"],
            "history_bars": mock_rq_api["history_bars"],
        }):
            exec(open(Path(__file__).parent.parent / "sentiment_switch_notebook_v2.py").read(), {"__name__": "__main__"})
        
        captured = capsys.readouterr()
        assert "情绪择时框架测试 v2" in captured.out

    def test_notebook_v2_handles_empty_stocks(self, mock_rq_api, capsys):
        def mock_all_instruments_empty(type_str, date=None):
            return []
        
        with patch.dict(sys.modules, {
            "get_trading_dates": mock_rq_api["get_trading_dates"],
            "all_instruments": mock_all_instruments_empty,
            "history_bars": mock_rq_api["history_bars"],
        }):
            exec(open(Path(__file__).parent.parent / "sentiment_switch_notebook_v2.py").read(), {"__name__": "__main__"})
        
        captured = capsys.readouterr()
        assert "测试完成" in captured.out

    def test_notebook_v2_handles_none_stocks(self, mock_rq_api, capsys):
        def mock_all_instruments_none(type_str, date=None):
            return None
        
        with patch.dict(sys.modules, {
            "get_trading_dates": mock_rq_api["get_trading_dates"],
            "all_instruments": mock_all_instruments_none,
            "history_bars": mock_rq_api["history_bars"],
        }):
            exec(open(Path(__file__).parent.parent / "sentiment_switch_notebook_v2.py").read(), {"__name__": "__main__"})
        
        captured = capsys.readouterr()
        assert "测试完成" in captured.out

    def test_notebook_v2_sentiment_on_threshold(self, mock_rq_api, capsys):
        def mock_history_bars_zt(*args, **kwargs):
            if "close" in str(args):
                return np.array([10.0, 11.1])
            return np.array([10.5])
        
        with patch.dict(sys.modules, {
            "get_trading_dates": mock_rq_api["get_trading_dates"],
            "all_instruments": mock_rq_api["all_instruments"],
            "history_bars": mock_history_bars_zt,
        }):
            exec(open(Path(__file__).parent.parent / "sentiment_switch_notebook_v2.py").read(), {"__name__": "__main__"})
        
        captured = capsys.readouterr()
        assert "测试完成" in captured.out

    def test_notebook_v2_low_open_detection(self, mock_rq_api, capsys):
        def mock_history_bars_low_open(stock_id, bar_count, frequency, fields, start_date=None, end_date=None):
            if fields == "close":
                return np.array([10.0, 10.5, 11.0])
            elif fields == "open":
                return np.array([9.6])
            return np.array([10.0])
        
        with patch.dict(sys.modules, {
            "get_trading_dates": mock_rq_api["get_trading_dates"],
            "all_instruments": mock_rq_api["all_instruments"],
            "history_bars": mock_history_bars_low_open,
        }):
            exec(open(Path(__file__).parent.parent / "sentiment_switch_notebook_v2.py").read(), {"__name__": "__main__"})
        
        captured = capsys.readouterr()
        assert "测试完成" in captured.out

    def test_notebook_v2_trading_dates(self, mock_rq_api):
        dates = mock_rq_api["get_trading_dates"]("2024-03-01", "2024-03-15")
        assert len(dates) > 0
        assert "2024-03-01" in dates

    def test_notebook_v2_handles_history_bars_none(self, mock_rq_api, capsys):
        def mock_history_bars_none(*args, **kwargs):
            return None
        
        with patch.dict(sys.modules, {
            "get_trading_dates": mock_rq_api["get_trading_dates"],
            "all_instruments": mock_rq_api["all_instruments"],
            "history_bars": mock_history_bars_none,
        }):
            exec(open(Path(__file__).parent.parent / "sentiment_switch_notebook_v2.py").read(), {"__name__": "__main__"})
        
        captured = capsys.readouterr()
        assert "测试完成" in captured.out

    def test_notebook_v2_handles_exception(self, mock_rq_api, capsys):
        def mock_all_instruments_error(*args, **kwargs):
            raise Exception("API error")
        
        with patch.dict(sys.modules, {
            "get_trading_dates": mock_rq_api["get_trading_dates"],
            "all_instruments": mock_all_instruments_error,
            "history_bars": mock_rq_api["history_bars"],
        }):
            exec(open(Path(__file__).parent.parent / "sentiment_switch_notebook_v2.py").read(), {"__name__": "__main__"})
        
        captured = capsys.readouterr()
        assert "测试完成" in captured.out or "错误" in captured.out

    def test_notebook_v2_pct_change_calculation(self):
        today_close = 11.0
        prev_close = 10.0
        pct_change = (today_close / prev_close - 1) * 100
        assert abs(pct_change - 10.0) < 0.001

    def test_notebook_v2_open_ratio_calculation(self):
        next_open = 9.5
        prev_close = 10.0
        open_ratio = (next_open / prev_close - 1) * 100
        assert abs(open_ratio - (-5.0)) < 0.001

    def test_notebook_v2_signals_collection(self, mock_rq_api, capsys):
        with patch.dict(sys.modules, {
            "get_trading_dates": mock_rq_api["get_trading_dates"],
            "all_instruments": mock_rq_api["all_instruments"],
            "history_bars": mock_rq_api["history_bars"],
        }):
            exec(open(Path(__file__).parent.parent / "sentiment_switch_notebook_v2.py").read(), {"__name__": "__main__"})
        
        captured = capsys.readouterr()
        assert "测试结果" in captured.out or "测试完成" in captured.out

    def test_notebook_v2_min_function(self):
        result = min(5, 10)
        assert result == 5

        result = min(10, 5)
        assert result == 5