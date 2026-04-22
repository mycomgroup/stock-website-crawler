"""
Tests for minimal_buy_rq.py
"""
import sys
from unittest.mock import MagicMock, patch
from datetime import datetime
import pytest

from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "data"))


class MockBar:
    def __init__(self, close=10.0, is_trading=True):
        self.close = close
        self.is_trading = is_trading


class MockPosition:
    def __init__(self, quantity=0):
        self.quantity = quantity


class TestMinimalBuyRq:
    def test_init(self, rq_mocks):
        from minimal_buy_rq import init
        context = MagicMock()
        init(context)
        assert context.benchmark == "000300.XSHG"
        assert context.test_stock == "600519.XSHG"

    def test_handle_bar_stock_not_in_bar_dict(self, rq_mocks):
        from minimal_buy_rq import handle_bar, init
        context = MagicMock()
        context.test_stock = "600519.XSHG"
        init(context)
        handle_bar(context, {})

    def test_handle_bar_stock_in_bar_dict(self, rq_mocks):
        from minimal_buy_rq import handle_bar, init
        context = MagicMock()
        context.test_stock = "600519.XSHG"
        context.portfolio.positions = {"600519.XSHG": MockPosition(quantity=0)}
        context.portfolio.total_value = 100000
        init(context)
        bar_dict = {"600519.XSHG": MockBar(close=1800, is_trading=True)}
        handle_bar(context, bar_dict)

    def test_handle_bar_already_has_position(self, rq_mocks):
        from minimal_buy_rq import handle_bar, init
        context = MagicMock()
        context.test_stock = "600519.XSHG"
        context.portfolio.positions = {"600519.XSHG": MockPosition(quantity=100)}
        init(context)
        bar_dict = {"600519.XSHG": MockBar(close=1800, is_trading=True)}
        handle_bar(context, bar_dict)

    def test_handle_bar_not_trading(self, rq_mocks):
        from minimal_buy_rq import handle_bar, init
        context = MagicMock()
        context.test_stock = "600519.XSHG"
        context.portfolio.positions = {"600519.XSHG": MockPosition(quantity=0)}
        init(context)
        bar_dict = {"600519.XSHG": MockBar(close=1800, is_trading=False)}
        handle_bar(context, bar_dict)