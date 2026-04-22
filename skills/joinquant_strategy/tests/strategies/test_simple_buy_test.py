import pytest
from unittest.mock import Mock, MagicMock, patch
from datetime import datetime
import pandas as pd
from types import SimpleNamespace
import sys


class TestSimpleBuyTest:
    @pytest.fixture(autouse=True)
    def setup_mocks(self, mock_jqdata):
        self.jqdata = mock_jqdata
        self.g = SimpleNamespace()
        self.g.count = 0
        
        self.jqdata.g = self.g
        sys.modules['jqdata'] = self.jqdata
        
        patcher = patch.dict(sys.modules, {'jqdata': self.jqdata})
        patcher.start()
        self.addCleanup(patcher.stop)
        
        import simple_buy_test as module
        self.module = module

    def addCleanup(self, cleanup):
        cleanup()

    def test_initialize_sets_options(self):
        context = SimpleNamespace()
        
        self.module.initialize(context)
        
        self.jqdata.set_option.assert_called_once_with("use_real_price", True)
        self.jqdata.log.set_level.assert_called_once_with("system", "error")
        assert self.g.count == 0

    def test_handle_data_first_count(self):
        context = SimpleNamespace()
        context.current_dt = datetime(2024, 1, 15)
        context.portfolio = SimpleNamespace()
        context.portfolio.positions = {}
        
        data = SimpleNamespace()
        
        self.g.count = 0
        
        self.module.handle_data(context, data)
        
        assert self.g.count == 1
        self.jqdata.log.info.assert_called()
        self.jqdata.order_value.assert_any_call("000001.XSHE", 50000)
        self.jqdata.order_value.assert_any_call("600000.XSHG", 50000)

    def test_handle_data_second_count(self):
        context = SimpleNamespace()
        context.current_dt = datetime(2024, 1, 15)
        context.portfolio = SimpleNamespace()
        context.portfolio.positions = {}
        
        data = SimpleNamespace()
        
        self.g.count = 1
        
        self.module.handle_data(context, data)
        
        assert self.g.count == 2

    def test_handle_data_third_count_sells(self):
        context = SimpleNamespace()
        context.current_dt = datetime(2024, 1, 15)
        
        pos = SimpleNamespace()
        context.portfolio = SimpleNamespace()
        context.portfolio.positions = {'000001.XSHE': pos, '600000.XSHG': pos}
        
        data = SimpleNamespace()
        
        self.g.count = 2
        
        self.module.handle_data(context, data)
        
        assert self.g.count == 3
        self.jqdata.order_target.assert_called()

    def test_handle_data_exceeds_three(self):
        context = SimpleNamespace()
        context.current_dt = datetime(2024, 1, 15)
        context.portfolio = SimpleNamespace()
        context.portfolio.positions = {}
        
        data = SimpleNamespace()
        
        self.g.count = 3
        
        self.module.handle_data(context, data)
        
        assert self.g.count == 4
        self.jqdata.order_value.assert_not_called()
        self.jqdata.order_target.assert_not_called()

    def test_handle_data_logs_start_message(self):
        context = SimpleNamespace()
        context.current_dt = datetime(2024, 1, 15)
        context.portfolio = SimpleNamespace()
        context.portfolio.positions = {}
        
        data = SimpleNamespace()
        
        self.g.count = 0
        
        self.module.handle_data(context, data)
        
        call_args = self.jqdata.log.info.call_args_list
        assert any("策略启动" in str(call) for call in call_args)

    def test_handle_data_logs_buy_message(self):
        context = SimpleNamespace()
        context.current_dt = datetime(2024, 1, 15)
        context.portfolio = SimpleNamespace()
        context.portfolio.positions = {}
        
        data = SimpleNamespace()
        
        self.g.count = 0
        
        self.module.handle_data(context, data)
        
        call_args = self.jqdata.log.info.call_args_list
        assert any("买入" in str(call) for call in call_args)

    def test_handle_data_third_count_logs_sell_message(self):
        context = SimpleNamespace()
        context.current_dt = datetime(2024, 1, 15)
        
        pos = SimpleNamespace()
        context.portfolio = SimpleNamespace()
        context.portfolio.positions = {'000001.XSHE': pos}
        
        data = SimpleNamespace()
        
        self.g.count = 2
        
        self.module.handle_data(context, data)
        
        call_args = self.jqdata.log.info.call_args_list
        assert any("卖出" in str(call) for call in call_args)

    def test_handle_data_buys_correct_stocks(self):
        context = SimpleNamespace()
        context.current_dt = datetime(2024, 1, 15)
        context.portfolio = SimpleNamespace()
        context.portfolio.positions = {}
        
        data = SimpleNamespace()
        
        self.g.count = 0
        
        self.module.handle_data(context, data)
        
        calls = [call[0][0] for call in self.jqdata.order_value.call_args_list]
        assert "000001.XSHE" in calls
        assert "600000.XSHG" in calls

    def test_handle_data_buy_value_is_50000(self):
        context = SimpleNamespace()
        context.current_dt = datetime(2024, 1, 15)
        context.portfolio = SimpleNamespace()
        context.portfolio.positions = {}
        
        data = SimpleNamespace()
        
        self.g.count = 0
        
        self.module.handle_data(context, data)
        
        calls = self.jqdata.order_value.call_args_list
        for call in calls:
            assert call[0][1] == 50000

    def test_handle_data_sells_all_positions(self):
        context = SimpleNamespace()
        context.current_dt = datetime(2024, 1, 15)
        
        pos1 = SimpleNamespace()
        pos2 = SimpleNamespace()
        context.portfolio = SimpleNamespace()
        context.portfolio.positions = {'000001.XSHE': pos1, '600000.XSHG': pos2}
        
        data = SimpleNamespace()
        
        self.g.count = 2
        
        self.module.handle_data(context, data)
        
        calls = [call[0][0] for call in self.jqdata.order_target.call_args_list]
        assert "000001.XSHE" in calls
        assert "600000.XSHG" in calls

    def test_handle_data_order_target_value_is_zero(self):
        context = SimpleNamespace()
        context.current_dt = datetime(2024, 1, 15)
        
        pos = SimpleNamespace()
        context.portfolio = SimpleNamespace()
        context.portfolio.positions = {'000001.XSHE': pos}
        
        data = SimpleNamespace()
        
        self.g.count = 2
        
        self.module.handle_data(context, data)
        
        calls = self.jqdata.order_target.call_args_list
        for call in calls:
            assert call[0][1] == 0

    def test_handle_data_no_positions_to_sell(self):
        context = SimpleNamespace()
        context.current_dt = datetime(2024, 1, 15)
        context.portfolio = SimpleNamespace()
        context.portfolio.positions = {}
        
        data = SimpleNamespace()
        
        self.g.count = 2
        
        self.module.handle_data(context, data)
        
        self.jqdata.order_target.assert_not_called()