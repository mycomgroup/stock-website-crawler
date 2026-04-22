"""
Tests for simple_etf_rq.py
"""
import sys
from unittest.mock import MagicMock, patch
from datetime import datetime
import pytest

from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "data"))


class MockBar:
    def __init__(self, close=10.0):
        self.close = close


class TestSimpleEtfRq:
    def test_init(self, rq_mocks):
        from simple_etf_rq import init
        context = MagicMock()
        init(context)
        assert context.last_month == -1
        assert context.stock == "510300.XSHG"

    def test_rebalance_same_month(self, rq_mocks):
        from simple_etf_rq import rebalance, init
        context = MagicMock()
        context.now = datetime(2024, 7, 15)
        context.last_month = 7
        init(context)
        rebalance(context, {})

    def test_rebalance_stock_not_in_bar(self, rq_mocks):
        from simple_etf_rq import rebalance, init
        context = MagicMock()
        context.now = datetime(2024, 7, 1)
        context.last_month = 6
        context.stock = "510300.XSHG"
        init(context)
        rebalance(context, {})
        assert context.last_month == 7

    def test_rebalance_invalid_price(self, rq_mocks):
        from simple_etf_rq import rebalance, init
        context = MagicMock()
        context.now = datetime(2024, 7, 1)
        context.last_month = 6
        context.stock = "510300.XSHG"
        init(context)
        bar_dict = {"510300.XSHG": MockBar(close=0)}
        rebalance(context, bar_dict)
        assert context.last_month == 7

    def test_rebalance_success(self, rq_mocks):
        from simple_etf_rq import rebalance, init
        context = MagicMock()
        context.now = datetime(2024, 7, 1)
        context.last_month = 6
        context.stock = "510300.XSHG"
        init(context)
        bar_dict = {"510300.XSHG": MockBar(close=4.5)}
        rebalance(context, bar_dict)
        assert context.last_month == 7