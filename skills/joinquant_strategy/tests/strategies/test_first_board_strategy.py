import pytest
from unittest.mock import Mock, MagicMock, patch
from datetime import datetime
import pandas as pd
from types import SimpleNamespace
import sys


class TestFirstBoardStrategy:
    @pytest.fixture(autouse=True)
    def setup_mocks(self, mock_jqdata):
        self.jqdata = mock_jqdata
        self.g = SimpleNamespace()
        self.g.trade_count = 0
        self.g.win_count = 0
        self.g.pnl_list = []
        self.g.target = []
        
        self.jqdata.g = self.g
        sys.modules['jqdata'] = self.jqdata
        
        patcher = patch.dict(sys.modules, {'jqdata': self.jqdata})
        patcher.start()
        self.addCleanup(patcher.stop)
        
        import first_board_strategy as module
        self.module = module

    def addCleanup(self, cleanup):
        cleanup()

    def test_initialize_sets_options(self):
        context = SimpleNamespace()
        
        self.module.initialize(context)
        
        self.jqdata.set_option.assert_any_call("use_real_price", True)
        self.jqdata.set_option.assert_any_call("avoid_future_data", True)
        self.jqdata.log.set_level.assert_called_once_with("system", "error")
        assert self.jqdata.run_daily.call_count == 3

    def test_initialize_sets_global_variables(self):
        context = SimpleNamespace()
        
        self.module.initialize(context)
        
        assert self.g.trade_count == 0
        assert self.g.win_count == 0
        assert self.g.pnl_list == []

    def test_select_stocks_identifies_limit_up(self):
        context = SimpleNamespace()
        context.previous_date = datetime(2024, 1, 15)
        
        mock_securities = pd.DataFrame({
            'display_name': ['平安银行', '万科A', '浦发银行']
        }, index=['000001.XSHE', '000002.XSHE', '600000.XSHG'])
        self.jqdata.get_all_securities.return_value = mock_securities
        
        df = pd.DataFrame({
            'code': ['000001.XSHE', '000002.XSHE'],
            'close': [10.0, 20.0],
            'high_limit': [10.0, 20.0]
        })
        self.jqdata.get_price.return_value = df
        
        self.module.select_stocks(context)
        
        assert self.g.target == ['000001.XSHE', '000002.XSHE']

    def test_select_stocks_filters_excluded_stocks(self):
        context = SimpleNamespace()
        context.previous_date = datetime(2024, 1, 15)
        
        mock_securities = pd.DataFrame({
            'display_name': ['Stock1', 'Stock2', 'Stock3', 'Stock4', 'Stock5']
        }, index=['000001.XSHE', '688001.XSHG', '300001.XSHE', '400001.XSHE', '800001.XSHG'])
        self.jqdata.get_all_securities.return_value = mock_securities
        
        df = pd.DataFrame({
            'code': ['000001.XSHE'],
            'close': [10.0],
            'high_limit': [10.0]
        })
        self.jqdata.get_price.return_value = df
        
        self.module.select_stocks(context)
        
        assert '688001.XSHG' not in self.g.target
        assert '300001.XSHE' not in self.g.target
        assert '400001.XSHE' not in self.g.target
        assert '800001.XSHG' not in self.g.target

    def test_select_stocks_handles_no_limit_up(self):
        context = SimpleNamespace()
        context.previous_date = datetime(2024, 1, 15)
        
        mock_securities = pd.DataFrame({
            'display_name': ['平安银行']
        }, index=['000001.XSHE'])
        self.jqdata.get_all_securities.return_value = mock_securities
        
        df = pd.DataFrame({
            'code': ['000001.XSHE'],
            'close': [9.0],
            'high_limit': [10.0]
        })
        self.jqdata.get_price.return_value = df
        
        self.module.select_stocks(context)
        
        assert self.g.target == []

    def test_select_stocks_handles_empty_data(self):
        context = SimpleNamespace()
        context.previous_date = datetime(2024, 1, 15)
        
        mock_securities = pd.DataFrame({
            'display_name': ['平安银行']
        }, index=['000001.XSHE'])
        self.jqdata.get_all_securities.return_value = mock_securities
        
        df = pd.DataFrame({'code': [], 'close': [], 'high_limit': []})
        self.jqdata.get_price.return_value = df
        
        self.module.select_stocks(context)
        
        assert self.g.target == []

    def test_buy_stocks_no_target(self):
        context = SimpleNamespace()
        context.portfolio = SimpleNamespace()
        context.portfolio.available_cash = 100000
        
        self.g.target = []
        
        self.module.buy_stocks(context)
        
        self.jqdata.get_current_data.assert_not_called()

    def test_buy_stocks_filters_paused_stocks(self):
        context = SimpleNamespace()
        context.portfolio = SimpleNamespace()
        context.portfolio.available_cash = 100000
        
        self.g.target = ['000001.XSHE']
        
        stock_data = SimpleNamespace()
        stock_data.paused = True
        stock_data.pre_close = 10.0
        stock_data.day_open = 10.0
        stock_data.high_limit = 11.0
        
        self.jqdata.get_current_data.return_value = {'000001.XSHE': stock_data}
        
        self.module.buy_stocks(context)
        
        self.jqdata.order.assert_not_called()

    def test_buy_stocks_filters_open_pct_range(self):
        context = SimpleNamespace()
        context.portfolio = SimpleNamespace()
        context.portfolio.available_cash = 100000
        
        self.g.target = ['000001.XSHE']
        
        stock_data = SimpleNamespace()
        stock_data.paused = False
        stock_data.pre_close = 10.0
        stock_data.day_open = 10.5
        stock_data.high_limit = 11.0
        stock_data.last_price = 10.5
        
        self.jqdata.get_current_data.return_value = {'000001.XSHE': stock_data}
        
        self.module.buy_stocks(context)
        
        self.jqdata.order.assert_not_called()

    def test_buy_stocks_in_range_minus_1_5(self):
        context = SimpleNamespace()
        context.portfolio = SimpleNamespace()
        context.portfolio.available_cash = 100000
        
        self.g.target = ['000001.XSHE']
        
        stock_data = SimpleNamespace()
        stock_data.paused = False
        stock_data.pre_close = 10.0
        stock_data.day_open = 9.9
        stock_data.high_limit = 11.0
        stock_data.last_price = 9.9
        
        self.jqdata.get_current_data.return_value = {'000001.XSHE': stock_data}
        
        self.module.buy_stocks(context)
        
        assert self.g.trade_count > 0

    def test_buy_stocks_in_range_plus_1_5(self):
        context = SimpleNamespace()
        context.portfolio = SimpleNamespace()
        context.portfolio.available_cash = 100000
        
        self.g.target = ['000001.XSHE']
        
        stock_data = SimpleNamespace()
        stock_data.paused = False
        stock_data.pre_close = 10.0
        stock_data.day_open = 10.1
        stock_data.high_limit = 11.0
        stock_data.last_price = 10.1
        
        self.jqdata.get_current_data.return_value = {'000001.XSHE': stock_data}
        
        self.module.buy_stocks(context)
        
        assert self.g.trade_count > 0

    def test_buy_stocks_out_of_range_high(self):
        context = SimpleNamespace()
        context.portfolio = SimpleNamespace()
        context.portfolio.available_cash = 100000
        
        self.g.target = ['000001.XSHE']
        
        stock_data = SimpleNamespace()
        stock_data.paused = False
        stock_data.pre_close = 10.0
        stock_data.day_open = 10.2
        stock_data.high_limit = 11.0
        stock_data.last_price = 10.5
        
        self.jqdata.get_current_data.return_value = {'000001.XSHE': stock_data}
        
        self.module.buy_stocks(context)
        
        self.jqdata.order.assert_not_called()

    def test_buy_stocks_out_of_range_low(self):
        context = SimpleNamespace()
        context.portfolio = SimpleNamespace()
        context.portfolio.available_cash = 100000
        
        self.g.target = ['000001.XSHE']
        
        stock_data = SimpleNamespace()
        stock_data.paused = False
        stock_data.pre_close = 10.0
        stock_data.day_open = 9.8
        stock_data.high_limit = 11.0
        stock_data.last_price = 10.0
        
        self.jqdata.get_current_data.return_value = {'000001.XSHE': stock_data}
        
        self.module.buy_stocks(context)
        
        self.jqdata.order.assert_not_called()

    def test_buy_stocks_missing_in_current_data(self):
        context = SimpleNamespace()
        context.portfolio = SimpleNamespace()
        context.portfolio.available_cash = 100000
        
        self.g.target = ['000001.XSHE']
        
        self.jqdata.get_current_data.return_value = {}
        
        self.module.buy_stocks(context)
        
        self.jqdata.order.assert_not_called()

    def test_buy_stocks_calculates_shares_correctly(self):
        context = SimpleNamespace()
        context.portfolio = SimpleNamespace()
        context.portfolio.available_cash = 100000
        
        self.g.target = ['000001.XSHE']
        
        stock_data = SimpleNamespace()
        stock_data.paused = False
        stock_data.pre_close = 10.0
        stock_data.day_open = 10.0
        stock_data.high_limit = 11.0
        stock_data.last_price = 10.0
        
        self.jqdata.get_current_data.return_value = {'000001.XSHE': stock_data}
        
        self.module.buy_stocks(context)
        
        assert self.g.trade_count > 0

    def test_buy_stocks_limits_to_3_stocks(self):
        context = SimpleNamespace()
        context.portfolio = SimpleNamespace()
        context.portfolio.available_cash = 300000
        
        self.g.target = ['000001.XSHE', '000002.XSHE', '000003.XSHE', '000004.XSHE']
        
        current_data = {}
        for s in self.g.target:
            stock_data = SimpleNamespace()
            stock_data.paused = False
            stock_data.pre_close = 10.0
            stock_data.day_open = 10.0
            stock_data.high_limit = 11.0
            stock_data.last_price = 10.0
            current_data[s] = stock_data
        
        self.jqdata.get_current_data.return_value = current_data
        
        self.module.buy_stocks(context)
        
        assert self.jqdata.order.call_count <= 3

    def test_sell_stocks_with_positions(self):
        context = SimpleNamespace()
        context.portfolio = SimpleNamespace()
        pos = SimpleNamespace()
        pos.closeable_amount = 100
        pos.avg_cost = 10.0
        context.portfolio.positions = {'000001.XSHE': pos}
        
        stock_data = SimpleNamespace()
        stock_data.last_price = 11.0
        self.jqdata.get_current_data.return_value = {'000001.XSHE': stock_data}
        
        self.module.sell_stocks(context)
        
        self.jqdata.order_target.assert_called_once_with('000001.XSHE', 0)
        assert len(self.g.pnl_list) == 1
        assert self.g.win_count == 1

    def test_sell_stocks_with_loss(self):
        context = SimpleNamespace()
        context.portfolio = SimpleNamespace()
        pos = SimpleNamespace()
        pos.closeable_amount = 100
        pos.avg_cost = 11.0
        context.portfolio.positions = {'000001.XSHE': pos}
        
        stock_data = SimpleNamespace()
        stock_data.last_price = 10.0
        self.jqdata.get_current_data.return_value = {'000001.XSHE': stock_data}
        
        self.module.sell_stocks(context)
        
        assert len(self.g.pnl_list) == 1
        assert self.g.win_count == 0

    def test_sell_stocks_no_closeable_amount(self):
        context = SimpleNamespace()
        context.portfolio = SimpleNamespace()
        pos = SimpleNamespace()
        pos.closeable_amount = 0
        pos.avg_cost = 10.0
        context.portfolio.positions = {'000001.XSHE': pos}
        
        self.module.sell_stocks(context)
        
        self.jqdata.order_target.assert_not_called()

    def test_sell_stocks_multiple_positions(self):
        context = SimpleNamespace()
        context.portfolio = SimpleNamespace()
        
        pos1 = SimpleNamespace()
        pos1.closeable_amount = 100
        pos1.avg_cost = 10.0
        
        pos2 = SimpleNamespace()
        pos2.closeable_amount = 100
        pos2.avg_cost = 20.0
        
        context.portfolio.positions = {'000001.XSHE': pos1, '000002.XSHE': pos2}
        
        stock_data1 = SimpleNamespace()
        stock_data1.last_price = 11.0
        
        stock_data2 = SimpleNamespace()
        stock_data2.last_price = 21.0
        
        self.jqdata.get_current_data.return_value = {
            '000001.XSHE': stock_data1,
            '000002.XSHE': stock_data2
        }
        
        self.module.sell_stocks(context)
        
        assert self.jqdata.order_target.call_count == 2
        assert len(self.g.pnl_list) == 2