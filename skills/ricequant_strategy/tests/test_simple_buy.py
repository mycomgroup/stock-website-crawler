"""
Tests for simple_buy.py
"""
import sys
from pathlib import Path
from unittest.mock import MagicMock, patch
from datetime import datetime
import pytest

sys.path.insert(0, str(Path(__file__).parent.parent))


class MockPortfolioSimple:
    def __init__(self):
        self.starting_cash = 1000000
        self.total_value = 1000000
        self.positions = {}


class MockContextSimple:
    def __init__(self):
        self.now = datetime(2024, 7, 1)
        self.portfolio = MockPortfolioSimple()
        self.bought = False


@pytest.fixture(scope="module")
def setup_rq_mocks_simple():
    def mock_index_components(index_name):
        if index_name == "000300.XSHG":
            return ["600000.XSHG", "600519.XSHG", "000001.XSHE"]
        return []
    
    def mock_order_target_percent(stock, percent):
        return None
    
    sys.modules["index_components"] = mock_index_components
    sys.modules["order_target_percent"] = mock_order_target_percent
    
    yield
    
    del sys.modules["index_components"]
    del sys.modules["order_target_percent"]


class TestSimpleBuy:
    def test_init(self, setup_rq_mocks_simple):
        from simple_buy import init
        context = MockContextSimple()
        init(context)
        assert context.bought == False

    def test_handle_bar_buy_once(self, setup_rq_mocks_simple, capsys):
        from simple_buy import handle_bar, init
        context = MockContextSimple()
        init(context)
        bar_dict = {}
        handle_bar(context, bar_dict)
        assert context.bought == True

    def test_handle_bar_skip_after_bought(self, setup_rq_mocks_simple, capsys):
        from simple_buy import handle_bar, init
        context = MockContextSimple()
        init(context)
        context.bought = True
        bar_dict = {}
        handle_bar(context, bar_dict)
        assert context.bought == True

    def test_handle_bar_empty_components(self, setup_rq_mocks_simple, capsys):
        from simple_buy import handle_bar, init
        context = MockContextSimple()
        init(context)
        
        with patch("simple_buy.index_components", return_value=[]):
            bar_dict = {}
            handle_bar(context, bar_dict)
            assert context.bought == False

    def test_handle_bar_none_components(self, setup_rq_mocks_simple, capsys):
        from simple_buy import handle_bar, init
        context = MockContextSimple()
        init(context)
        
        with patch("simple_buy.index_components", return_value=None):
            bar_dict = {}
            handle_bar(context, bar_dict)
            assert context.bought == False

    def test_handle_bar_exception(self, setup_rq_mocks_simple, capsys):
        from simple_buy import handle_bar, init
        context = MockContextSimple()
        init(context)
        
        with patch("simple_buy.index_components", side_effect=Exception("API error")):
            bar_dict = {}
            handle_bar(context, bar_dict)
            assert context.bought == False

    def test_handle_bar_buy_first_stock(self, setup_rq_mocks_simple, capsys):
        from simple_buy import handle_bar, init
        context = MockContextSimple()
        init(context)
        
        stocks = ["000001.XSHE", "000002.XSHE", "600000.XSHG"]
        with patch("simple_buy.index_components", return_value=stocks):
            bar_dict = {}
            handle_bar(context, bar_dict)
            assert context.bought == True

    def test_handle_bar_multiple_calls(self, setup_rq_mocks_simple, capsys):
        from simple_buy import handle_bar, init
        context = MockContextSimple()
        init(context)
        bar_dict = {}
        
        handle_bar(context, bar_dict)
        assert context.bought == True
        
        handle_bar(context, bar_dict)
        assert context.bought == True

    def test_order_target_percent_called(self, setup_rq_mocks_simple):
        from simple_buy import handle_bar, init
        context = MockContextSimple()
        init(context)
        
        mock_order = MagicMock()
        with patch("simple_buy.index_components", return_value=["000001.XSHE"]):
            with patch("simple_buy.order_target_percent", mock_order):
                bar_dict = {}
                handle_bar(context, bar_dict)
                mock_order.assert_called_once_with("000001.XSHE", 0.95)

    def test_order_target_percent_not_called_after_bought(self, setup_rq_mocks_simple):
        from simple_buy import handle_bar, init
        context = MockContextSimple()
        init(context)
        context.bought = True
        
        mock_order = MagicMock()
        with patch("simple_buy.index_components", return_value=["000001.XSHE"]):
            with patch("simple_buy.order_target_percent", mock_order):
                bar_dict = {}
                handle_bar(context, bar_dict)
                mock_order.assert_not_called()