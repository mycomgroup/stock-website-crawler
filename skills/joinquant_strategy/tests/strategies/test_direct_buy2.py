import pytest
from unittest.mock import Mock, MagicMock, patch
from datetime import datetime
import pandas as pd
from types import SimpleNamespace
import sys


class TestDirectBuy2:
    @pytest.fixture(autouse=True)
    def setup_mocks(self, mock_jqdata):
        self.jqdata = mock_jqdata
        self.g = SimpleNamespace()
        self.g.bought = False
        
        self.jqdata.g = self.g
        sys.modules['jqdata'] = self.jqdata
        
        patcher = patch.dict(sys.modules, {'jqdata': self.jqdata})
        patcher.start()
        self.addCleanup(patcher.stop)
        
        import direct_buy2 as module
        self.module = module

    def addCleanup(self, cleanup):
        cleanup()

    def test_initialize_sets_options(self):
        context = SimpleNamespace()
        
        self.module.initialize(context)
        
        self.jqdata.set_option.assert_any_call("use_real_price", True)
        self.jqdata.set_benchmark.assert_called_once_with("000300.XSHG")
        self.jqdata.log.set_level.assert_called_once_with("system", "error")
        assert self.g.bought == False

    def test_initialize_sets_run_daily(self):
        context = SimpleNamespace()
        
        self.module.initialize(context)
        
        assert self.jqdata.run_daily.call_count == 2

    def test_trade_buys_when_not_bought(self):
        context = SimpleNamespace()
        self.g.bought = False
        
        self.module.trade(context)
        
        self.jqdata.order_value.assert_any_call("000001.XSHE", 500000)
        self.jqdata.order_value.assert_any_call("600000.XSHG", 500000)
        assert self.g.bought == True

    def test_trade_does_not_buy_when_already_bought(self):
        context = SimpleNamespace()
        self.g.bought = True
        
        self.module.trade(context)
        
        self.jqdata.order_value.assert_not_called()

    def test_sell_clears_bought_flag(self):
        context = SimpleNamespace()
        context.portfolio = SimpleNamespace()
        context.portfolio.positions = {'000001.XSHE': SimpleNamespace()}
        self.g.bought = True
        
        self.module.sell(context)
        
        assert self.g.bought == False

    def test_sell_orders_target_zero(self):
        context = SimpleNamespace()
        context.portfolio = SimpleNamespace()
        context.portfolio.positions = {'000001.XSHE': SimpleNamespace()}
        
        self.module.sell(context)
        
        self.jqdata.order_target.assert_called_with('000001.XSHE', 0)

    def test_sell_handles_multiple_positions(self):
        context = SimpleNamespace()
        context.portfolio = SimpleNamespace()
        pos1 = SimpleNamespace()
        pos2 = SimpleNamespace()
        context.portfolio.positions = {'000001.XSHE': pos1, '600000.XSHG': pos2}
        
        self.module.sell(context)
        
        assert self.jqdata.order_target.call_count == 2

    def test_sell_handles_empty_positions(self):
        context = SimpleNamespace()
        context.portfolio = SimpleNamespace()
        context.portfolio.positions = {}
        
        self.module.sell(context)
        
        self.jqdata.order_target.assert_not_called()