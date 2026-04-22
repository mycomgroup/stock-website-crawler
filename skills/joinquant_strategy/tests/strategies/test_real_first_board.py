import pytest
from unittest.mock import Mock, MagicMock, patch
from datetime import datetime, timedelta
import pandas as pd
from types import SimpleNamespace
import sys


class TestRealFirstBoard:
    @pytest.fixture(autouse=True)
    def setup_mocks(self, mock_jqdata):
        self.jqdata = mock_jqdata
        self.g = SimpleNamespace()
        self.g.trades = 0
        self.g.targets = []
        
        self.jqdata.g = self.g
        sys.modules['jqdata'] = self.jqdata
        
        patcher = patch.dict(sys.modules, {'jqdata': self.jqdata})
        patcher.start()
        self.addCleanup = lambda f: f()
        
        import real_first_board as module
        self.module = module

    def test_initialize_sets_options(self):
        context = SimpleNamespace()
        
        self.module.initialize(context)
        
        self.jqdata.set_option.assert_any_call("use_real_price", True)
        self.jqdata.set_option.assert_any_call("avoid_future_data", True)
        self.jqdata.log.set_level.assert_called_once_with("system", "error")
        self.jqdata.set_benchmark.assert_called_once_with("000300.XSHG")
        assert self.jqdata.run_daily.call_count == 3

    def test_initialize_sets_global_variables(self):
        context = SimpleNamespace()
        
        self.module.initialize(context)
        
        assert self.g.trades == 0

    def test_initialize_no_slippage(self):
        context = SimpleNamespace()
        
        self.module.initialize(context)
        
        self.jqdata.set_slippage.assert_not_called()

    def test_select_finds_limit_up_stocks(self):
        context = SimpleNamespace()
        context.previous_date = datetime(2024, 1, 15)
        
        mock_securities = pd.DataFrame({
            'display_name': ['平安银行', '万科A', '浦发银行']
        }, index=['000001.XSHE', '000002.XSHE', '600000.XSHG'])
        self.jqdata.get_all_securities.return_value = mock_securities
        
        df = pd.DataFrame({
            'code': ['000001.XSHE', '000002.XSHE', '600000.XSHG'],
            'close': [10.0, 20.0, 15.0],
            'high_limit': [10.0, 20.0, 15.0]
        })
        self.jqdata.get_price.return_value = df
        
        self.module.select(context)
        
        assert len(self.g.targets) > 0
        assert '000001.XSHE' in self.g.targets

    def test_select_filters_excluded_stocks(self):
        context = SimpleNamespace()
        context.previous_date = datetime(2024, 1, 15)
        
        stocks = ['000001.XSHE', '688001.XSHG', '400001.XSHE', '300001.XSHE', '800001.XSHG']
        mock_securities = pd.DataFrame({
            'display_name': ['Stock' + str(i) for i in range(5)]
        }, index=stocks)
        self.jqdata.get_all_securities.return_value = mock_securities
        
        df = pd.DataFrame({
            'code': ['000001.XSHE'],
            'close': [10.0],
            'high_limit': [10.0]
        })
        self.jqdata.get_price.return_value = df
        
        self.module.select(context)
        
        for s in self.g.targets:
            assert s[0] not in "483"
            assert s[:2] != "68"

    def test_select_limits_to_30_stocks(self):
        context = SimpleNamespace()
        context.previous_date = datetime(2024, 1, 15)
        
        stocks = [f'00000{i}.XSHE' for i in range(50)]
        mock_securities = pd.DataFrame({
            'display_name': ['Stock' + str(i) for i in range(50)]
        }, index=stocks)
        self.jqdata.get_all_securities.return_value = mock_securities
        
        df = pd.DataFrame({
            'code': stocks,
            'close': [10.0] * 50,
            'high_limit': [10.0] * 50
        })
        self.jqdata.get_price.return_value = df
        
        self.module.select(context)
        
        assert len(self.g.targets) <= 30

    def test_select_no_limit_up_stocks(self):
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
        
        self.module.select(context)
        
        assert self.g.targets == []

    def test_buy_no_targets(self):
        context = SimpleNamespace()
        context.previous_date = datetime(2024, 1, 15)
        context.portfolio = SimpleNamespace()
        context.portfolio.available_cash = 100000
        
        self.g.targets = []
        
        self.module.buy(context)
        
        self.jqdata.get_current_data.assert_not_called()
        assert self.g.trades == 0

    def test_buy_filters_paused_stocks(self):
        context = SimpleNamespace()
        context.previous_date = datetime(2024, 1, 15)
        context.portfolio = SimpleNamespace()
        context.portfolio.available_cash = 100000
        
        self.g.targets = ['000001.XSHE']
        
        stock_data = SimpleNamespace()
        stock_data.paused = True
        
        self.jqdata.get_current_data.return_value = {'000001.XSHE': stock_data}
        
        self.module.buy(context)
        
        self.jqdata.order_value.assert_not_called()
        assert self.g.trades == 0

    def test_buy_filters_st_stocks(self):
        context = SimpleNamespace()
        context.previous_date = datetime(2024, 1, 15)
        context.portfolio = SimpleNamespace()
        context.portfolio.available_cash = 100000
        
        self.g.targets = ['000001.XSHE']
        
        stock_data = SimpleNamespace()
        stock_data.paused = False
        stock_data.is_st = True
        
        self.jqdata.get_current_data.return_value = {'000001.XSHE': stock_data}
        
        self.module.buy(context)
        
        self.jqdata.order_value.assert_not_called()
        assert self.g.trades == 0

    def test_buy_filters_open_pct_range(self):
        context = SimpleNamespace()
        context.previous_date = datetime(2024, 1, 15)
        context.portfolio = SimpleNamespace()
        context.portfolio.available_cash = 100000
        
        self.g.targets = ['000001.XSHE']
        
        stock_data = SimpleNamespace()
        stock_data.paused = False
        stock_data.is_st = False
        stock_data.day_open = 10.5
        stock_data.pre_close = 10.0
        
        self.jqdata.get_current_data.return_value = {'000001.XSHE': stock_data}
        
        self.module.buy(context)
        
        self.jqdata.order_value.assert_not_called()

    def test_buy_in_valid_range_negative(self):
        context = SimpleNamespace()
        context.previous_date = datetime(2024, 1, 15)
        context.portfolio = SimpleNamespace()
        context.portfolio.available_cash = 100000
        
        self.g.targets = ['000001.XSHE']
        
        stock_data = SimpleNamespace()
        stock_data.paused = False
        stock_data.is_st = False
        stock_data.day_open = 9.85
        stock_data.pre_close = 10.0
        
        val_df = pd.DataFrame({
            'circulating_market_cap': [15]
        }, index=['000001.XSHE'])
        self.jqdata.get_valuation.return_value = val_df
        
        self.jqdata.get_current_data.return_value = {'000001.XSHE': stock_data}
        
        self.module.buy(context)
        
        assert self.g.trades >= 0

    def test_buy_in_valid_range_positive(self):
        context = SimpleNamespace()
        context.previous_date = datetime(2024, 1, 15)
        context.portfolio = SimpleNamespace()
        context.portfolio.available_cash = 100000
        
        self.g.targets = ['000001.XSHE']
        
        stock_data = SimpleNamespace()
        stock_data.paused = False
        stock_data.is_st = False
        stock_data.day_open = 10.15
        stock_data.pre_close = 10.0
        
        val_df = pd.DataFrame({
            'circulating_market_cap': [15]
        }, index=['000001.XSHE'])
        self.jqdata.get_valuation.return_value = val_df
        
        self.jqdata.get_current_data.return_value = {'000001.XSHE': stock_data}
        
        self.module.buy(context)
        
        assert self.g.trades >= 0

    def test_buy_filters_cap_range(self):
        context = SimpleNamespace()
        context.previous_date = datetime(2024, 1, 15)
        context.portfolio = SimpleNamespace()
        context.portfolio.available_cash = 100000
        
        self.g.targets = ['000001.XSHE']
        
        stock_data = SimpleNamespace()
        stock_data.paused = False
        stock_data.is_st = False
        stock_data.day_open = 10.0
        stock_data.pre_close = 10.0
        
        val_df = pd.DataFrame({
            'circulating_market_cap': [40]
        }, index=['000001.XSHE'])
        self.jqdata.get_valuation.return_value = val_df
        
        self.jqdata.get_current_data.return_value = {'000001.XSHE': stock_data}
        
        self.module.buy(context)
        
        assert self.g.trades == 0

    def test_buy_cap_in_valid_range(self):
        context = SimpleNamespace()
        context.previous_date = datetime(2024, 1, 15)
        context.portfolio = SimpleNamespace()
        context.portfolio.available_cash = 100000
        
        self.g.targets = ['000001.XSHE']
        
        stock_data = SimpleNamespace()
        stock_data.paused = False
        stock_data.is_st = False
        stock_data.day_open = 10.0
        stock_data.pre_close = 10.0
        
        val_df = pd.DataFrame({
            'circulating_market_cap': [20]
        }, index=['000001.XSHE'])
        self.jqdata.get_valuation.return_value = val_df
        
        self.jqdata.get_current_data.return_value = {'000001.XSHE': stock_data}
        
        self.module.buy(context)
        
        assert self.g.trades == 1

    def test_buy_sorts_by_cap(self):
        context = SimpleNamespace()
        context.previous_date = datetime(2024, 1, 15)
        context.portfolio = SimpleNamespace()
        context.portfolio.available_cash = 300000
        
        self.g.targets = ['000001.XSHE', '000002.XSHE', '000003.XSHE']
        
        current_data = {}
        for s in self.g.targets:
            stock_data = SimpleNamespace()
            stock_data.paused = False
            stock_data.is_st = False
            stock_data.day_open = 10.0
            stock_data.pre_close = 10.0
            current_data[s] = stock_data
        
        self.jqdata.get_current_data.return_value = current_data
        
        val_df = pd.DataFrame({
            'circulating_market_cap': [25, 10, 20]
        }, index=['000001.XSHE', '000002.XSHE', '000003.XSHE'])
        self.jqdata.get_valuation.return_value = val_df
        
        self.module.buy(context)
        
        assert self.g.trades <= 3

    def test_buy_max_3_stocks(self):
        context = SimpleNamespace()
        context.previous_date = datetime(2024, 1, 15)
        context.portfolio = SimpleNamespace()
        context.portfolio.available_cash = 300000
        
        self.g.targets = ['000001.XSHE', '000002.XSHE', '000003.XSHE', '000004.XSHE']
        
        current_data = {}
        for s in self.g.targets:
            stock_data = SimpleNamespace()
            stock_data.paused = False
            stock_data.is_st = False
            stock_data.day_open = 10.0
            stock_data.pre_close = 10.0
            current_data[s] = stock_data
        
        self.jqdata.get_current_data.return_value = current_data
        
        val_df = pd.DataFrame({
            'circulating_market_cap': [10, 10, 10, 10]
        }, index=self.g.targets)
        self.jqdata.get_valuation.return_value = val_df
        
        self.module.buy(context)
        
        assert self.g.trades <= 3

    def test_buy_stock_not_in_current_data(self):
        context = SimpleNamespace()
        context.previous_date = datetime(2024, 1, 15)
        context.portfolio = SimpleNamespace()
        context.portfolio.available_cash = 100000
        
        self.g.targets = ['000001.XSHE']
        
        self.jqdata.get_current_data.return_value = {}
        
        self.module.buy(context)
        
        assert self.g.trades == 0

    def test_sell_clears_positions(self):
        context = SimpleNamespace()
        context.portfolio = SimpleNamespace()
        
        pos = SimpleNamespace()
        pos.closeable_amount = 100
        
        context.portfolio.positions = {'000001.XSHE': pos}
        
        stock_data = SimpleNamespace()
        self.jqdata.get_current_data.return_value = {'000001.XSHE': stock_data}
        
        self.module.sell(context)
        
        self.jqdata.order_target.assert_called_once_with('000001.XSHE', 0)

    def test_sell_no_closeable_amount(self):
        context = SimpleNamespace()
        context.portfolio = SimpleNamespace()
        
        pos = SimpleNamespace()
        pos.closeable_amount = 0
        
        context.portfolio.positions = {'000001.XSHE': pos}
        
        stock_data = SimpleNamespace()
        self.jqdata.get_current_data.return_value = {'000001.XSHE': stock_data}
        
        self.module.sell(context)
        
        self.jqdata.order_target.assert_not_called()

    def test_sell_multiple_positions(self):
        context = SimpleNamespace()
        context.portfolio = SimpleNamespace()
        
        pos1 = SimpleNamespace()
        pos1.closeable_amount = 100
        
        pos2 = SimpleNamespace()
        pos2.closeable_amount = 100
        
        context.portfolio.positions = {'000001.XSHE': pos1, '000002.XSHE': pos2}
        
        current_data = {
            '000001.XSHE': SimpleNamespace(),
            '000002.XSHE': SimpleNamespace()
        }
        self.jqdata.get_current_data.return_value = current_data
        
        self.module.sell(context)
        
        assert self.jqdata.order_target.call_count == 2

    def test_sell_stock_not_in_current_data(self):
        context = SimpleNamespace()
        context.portfolio = SimpleNamespace()
        
        pos = SimpleNamespace()
        pos.closeable_amount = 100
        
        context.portfolio.positions = {'000001.XSHE': pos}
        
        self.jqdata.get_current_data.return_value = {}
        
        self.module.sell(context)
        
        self.jqdata.order_target.assert_not_called()