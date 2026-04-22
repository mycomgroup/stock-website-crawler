import pytest
from unittest.mock import Mock, MagicMock, patch
from datetime import datetime
import pandas as pd
from types import SimpleNamespace
import sys


class TestDirectBuy:
    @pytest.fixture(autouse=True)
    def setup_mocks(self, mock_jqdata):
        self.jqdata = mock_jqdata
        self.g = SimpleNamespace()
        self.g.day = 0
        
        self.jqdata.g = self.g
        sys.modules['jqdata'] = self.jqdata
        
        patcher = patch.dict(sys.modules, {'jqdata': self.jqdata})
        patcher.start()
        self.addCleanup(patcher.stop)
        
        import direct_buy as module
        self.module = module

    def addCleanup(self, cleanup):
        cleanup()

    def test_initialize_sets_options(self):
        context = SimpleNamespace()
        
        self.module.initialize(context)
        
        self.jqdata.set_option.assert_any_call("use_real_price", True)
        self.jqdata.set_benchmark.assert_called_once_with("000300.XSHG")
        self.jqdata.log.set_level.assert_called_once_with("system", "error")
        assert self.g.day == 0

    def test_handle_data_increments_day(self):
        context = SimpleNamespace()
        context.portfolio = SimpleNamespace()
        context.portfolio.positions = {}
        
        data = SimpleNamespace()
        
        self.module.handle_data(context, data)
        
        assert self.g.day == 1

    def test_handle_data_buys_on_first_day(self):
        context = SimpleNamespace()
        context.portfolio = SimpleNamespace()
        context.portfolio.positions = {}
        
        data = SimpleNamespace()
        self.g.day = 0
        
        self.module.handle_data(context, data)
        
        self.jqdata.order_value.assert_any_call("000001.XSHE", 500000)
        self.jqdata.order_value.assert_any_call("600000.XSHG", 500000)

    def test_handle_data_sells_on_day_10(self):
        context = SimpleNamespace()
        context.portfolio = SimpleNamespace()
        context.portfolio.positions = {'000001.XSHE': SimpleNamespace(closeable_amount=100)}
        
        data = SimpleNamespace()
        self.g.day = 9
        
        self.module.handle_data(context, data)
        
        self.jqdata.order_target.assert_called()

    def test_handle_data_does_not_buy_after_first_day(self):
        context = SimpleNamespace()
        context.portfolio = SimpleNamespace()
        context.portfolio.positions = {}
        
        data = SimpleNamespace()
        self.g.day = 2
        
        self.module.handle_data(context, data)
        
        self.jqdata.order_value.assert_not_called()

    def test_handle_data_does_not_sell_before_day_10(self):
        context = SimpleNamespace()
        context.portfolio = SimpleNamespace()
        context.portfolio.positions = {'000001.XSHE': SimpleNamespace()}
        
        data = SimpleNamespace()
        self.g.day = 5
        
        self.module.handle_data(context, data)
        
        self.jqdata.order_target.assert_not_called()

    def test_handle_data_day_sequence(self):
        context = SimpleNamespace()
        context.portfolio = SimpleNamespace()
        context.portfolio.positions = {}
        
        data = SimpleNamespace()
        
        for _ in range(3):
            self.module.handle_data(context, data)
        
        assert self.g.day == 3