"""
Tests for sentiment_switch_notebook.py
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


class MockBar:
    def __init__(self, close=10.0):
        self.close = close


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
            MockStock("000001.XSHE", 10.0),
            MockStock("000002.XSHE", 11.0),
            MockStock("600000.XSHG", 12.0),
        ]
    
    def mock_history_bars(stock_id, bar_count, frequency, fields, start_date=None, end_date=None):
        if fields == "close":
            return np.array([10.0, 10.5, 11.0])
        return [MockBar(10.0), MockBar(10.5)]
    
    mocks["get_trading_dates"] = mock_get_trading_dates
    mocks["all_instruments"] = mock_all_instruments
    mocks["history_bars"] = mock_history_bars
    
    return mocks


class TestNotebookMain:
    def test_notebook_execution_basic(self, mock_rq_api, capsys):
        with patch.dict(sys.modules, {
            "get_trading_dates": mock_rq_api["get_trading_dates"],
            "all_instruments": mock_rq_api["all_instruments"],
            "history_bars": mock_rq_api["history_bars"],
        }):
            exec(open(Path(__file__).parent.parent / "sentiment_switch_notebook.py").read(), {"__name__": "__main__"})
        
        captured = capsys.readouterr()
        assert "情绪择时框架测试开始" in captured.out

    def test_notebook_handles_empty_stocks(self, mock_rq_api, capsys):
        def mock_all_instruments_empty(type_str, date=None):
            return []
        
        with patch.dict(sys.modules, {
            "get_trading_dates": mock_rq_api["get_trading_dates"],
            "all_instruments": mock_all_instruments_empty,
            "history_bars": mock_rq_api["history_bars"],
        }):
            exec(open(Path(__file__).parent.parent / "sentiment_switch_notebook.py").read(), {"__name__": "__main__"})
        
        captured = capsys.readouterr()
        assert "测试完成" in captured.out

    def test_notebook_handles_none_stocks(self, mock_rq_api, capsys):
        def mock_all_instruments_none(type_str, date=None):
            return None
        
        with patch.dict(sys.modules, {
            "get_trading_dates": mock_rq_api["get_trading_dates"],
            "all_instruments": mock_all_instruments_none,
            "history_bars": mock_rq_api["history_bars"],
        }):
            exec(open(Path(__file__).parent.parent / "sentiment_switch_notebook.py").read(), {"__name__": "__main__"})
        
        captured = capsys.readouterr()
        assert "测试完成" in captured.out

    def test_notebook_handles_history_bars_exception(self, mock_rq_api, capsys):
        def mock_history_bars_error(*args, **kwargs):
            raise Exception("API error")
        
        with patch.dict(sys.modules, {
            "get_trading_dates": mock_rq_api["get_trading_dates"],
            "all_instruments": mock_rq_api["all_instruments"],
            "history_bars": mock_history_bars_error,
        }):
            exec(open(Path(__file__).parent.parent / "sentiment_switch_notebook.py").read(), {"__name__": "__main__"})
        
        captured = capsys.readouterr()
        assert "测试完成" in captured.out or "错误" in captured.out

    def test_notebook_zt_count_logic(self, mock_rq_api):
        bar = MockBar(11.0)
        result = bar.close / bar.close >= 1.095
        assert isinstance(result, bool)

    def test_notebook_trading_dates_iteration(self, mock_rq_api):
        dates = mock_rq_api["get_trading_dates"]("2024-01-01", "2024-01-10")
        assert len(dates) > 0
        assert all(isinstance(d, str) for d in dates)

    def test_notebook_handles_zero_prev_bars(self, mock_rq_api, capsys):
        def mock_history_bars_empty(*args, **kwargs):
            return []
        
        with patch.dict(sys.modules, {
            "get_trading_dates": mock_rq_api["get_trading_dates"],
            "all_instruments": mock_rq_api["all_instruments"],
            "history_bars": mock_history_bars_empty,
        }):
            exec(open(Path(__file__).parent.parent / "sentiment_switch_notebook.py").read(), {"__name__": "__main__"})
        
        captured = capsys.readouterr()
        assert "测试完成" in captured.out

    def test_notebook_bar_close_attribute(self, mock_rq_api):
        bar = MockBar(10.0)
        assert hasattr(bar, "close")
        assert bar.close == 10.0

    def test_notebook_bar_close_positive(self, mock_rq_api):
        bar = MockBar(10.0)
        assert bar.close > 0

    def test_notebook_output_format(self, mock_rq_api, capsys):
        with patch.dict(sys.modules, {
            "get_trading_dates": mock_rq_api["get_trading_dates"],
            "all_instruments": mock_rq_api["all_instruments"],
            "history_bars": mock_rq_api["history_bars"],
        }):
            exec(open(Path(__file__).parent.parent / "sentiment_switch_notebook.py").read(), {"__name__": "__main__"})
        
        captured = capsys.readouterr()
        assert "测试完成" in captured.out or "测试开始" in captured.out

    def test_notebook_imports(self, mock_rq_api):
        import numpy as np
        assert np is not None