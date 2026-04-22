import pytest
from unittest.mock import Mock, MagicMock, patch
from datetime import datetime
import pandas as pd
from types import SimpleNamespace
import sys


class TestFixBuy:
    @pytest.fixture(autouse=True)
    def setup_mocks(self, mock_jqdata):
        self.jqdata = mock_jqdata
        self.g = SimpleNamespace()
        
        self.jqdata.g = self.g
        sys.modules['jqdata'] = self.jqdata
        
        patcher = patch.dict(sys.modules, {'jqdata': self.jqdata})
        patcher.start()
        self.addCleanup(patcher.stop)
        
        import fix_buy as module
        self.module = module

    def addCleanup(self, cleanup):
        cleanup()

    def test_initialize_sets_options(self):
        context = SimpleNamespace()
        
        self.module.initialize(context)
        
        self.jqdata.set_option.assert_called_once_with("use_real_price", True)
        self.jqdata.log.set_level.assert_called_once_with("system", "error")
        self.jqdata.set_benchmark.assert_called_once_with("000300.XSHG")
        assert self.jqdata.run_daily.call_count == 2

    def test_buy_with_no_positions(self):
        context = SimpleNamespace()
        context.portfolio = SimpleNamespace()
        context.portfolio.positions = {}
        context.portfolio.available_cash = 100000
        
        self.module.buy(context)
        
        self.jqdata.order_value.assert_any_call("000001.XSHE", 40000)
        self.jqdata.order_value.assert_any_call("600000.XSHG", 40000)

    def test_buy_with_existing_positions(self):
        context = SimpleNamespace()
        context.portfolio = SimpleNamespace()
        pos = SimpleNamespace()
        pos.closeable_amount = 100
        context.portfolio.positions = {'000001.XSHE': pos}
        context.portfolio.available_cash = 50000
        
        self.module.buy(context)
        
        self.jqdata.order_value.assert_not_called()

    def test_buy_calculates_40_percent_allocation(self):
        context = SimpleNamespace()
        context.portfolio = SimpleNamespace()
        context.portfolio.positions = {}
        context.portfolio.available_cash = 100000
        
        self.module.buy(context)
        
        calls = self.jqdata.order_value.call_args_list
        for call in calls:
            assert call[0][1] == 40000

    def test_buy_logs_info(self):
        context = SimpleNamespace()
        context.portfolio = SimpleNamespace()
        context.portfolio.positions = {}
        context.portfolio.available_cash = 100000
        
        self.module.buy(context)
        
        self.jqdata.log.info.assert_called()

    def test_sell_with_positions(self):
        context = SimpleNamespace()
        context.portfolio = SimpleNamespace()
        pos = SimpleNamespace()
        pos.closeable_amount = 100
        context.portfolio.positions = {'000001.XSHE': pos}
        
        self.module.sell(context)
        
        self.jqdata.order_target.assert_called_once_with('000001.XSHE', 0)

    def test_sell_without_closeable_amount(self):
        context = SimpleNamespace()
        context.portfolio = SimpleNamespace()
        pos = SimpleNamespace()
        pos.closeable_amount = 0
        context.portfolio.positions = {'000001.XSHE': pos}
        
        self.module.sell(context)
        
        self.jqdata.order_target.assert_not_called()

    def test_sell_no_positions(self):
        context = SimpleNamespace()
        context.portfolio = SimpleNamespace()
        context.portfolio.positions = {}
        
        self.module.sell(context)
        
        self.jqdata.order_target.assert_not_called()

    def test_sell_multiple_positions(self):
        context = SimpleNamespace()
        context.portfolio = SimpleNamespace()
        
        pos1 = SimpleNamespace()
        pos1.closeable_amount = 100
        
        pos2 = SimpleNamespace()
        pos2.closeable_amount = 100
        
        context.portfolio.positions = {'000001.XSHE': pos1, '600000.XSHG': pos2}
        
        self.module.sell(context)
        
        assert self.jqdata.order_target.call_count == 2

    def test_sell_logs_info(self):
        context = SimpleNamespace()
        context.portfolio = SimpleNamespace()
        pos = SimpleNamespace()
        pos.closeable_amount = 100
        context.portfolio.positions = {'000001.XSHE': pos}
        
        self.module.sell(context)
        
        self.jqdata.log.info.assert_called()

    def test_buy_zero_cash(self):
        context = SimpleNamespace()
        context.portfolio = SimpleNamespace()
        context.portfolio.positions = {}
        context.portfolio.available_cash = 0
        
        self.module.buy(context)
        
        self.jqdata.order_value.assert_any_call("000001.XSHE", 0)
        self.jqdata.order_value.assert_any_call("600000.XSHG", 0)

    def test_sell_empty_positions_dict(self):
        context = SimpleNamespace()
        context.portfolio = SimpleNamespace()
        context.portfolio.positions = {}
        
        self.module.sell(context)
        
        self.jqdata.order_target.assert_not_called()