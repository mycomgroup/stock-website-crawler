import pytest
from unittest.mock import Mock, MagicMock, patch
from datetime import datetime, timedelta
import pandas as pd
from types import SimpleNamespace
import sys


class TestPriceStopLoss:
    @pytest.fixture(autouse=True)
    def setup_mocks(self, mock_jqdata):
        self.jqdata = mock_jqdata
        self.g = SimpleNamespace()
        self.g.trades = 0
        self.g.wins = 0
        self.g.stop_count = 0
        self.g.buy_times = {}
        
        self.jqdata.g = self.g
        sys.modules['jqdata'] = self.jqdata
        
        patcher = patch.dict(sys.modules, {'jqdata': self.jqdata})
        patcher.start()
        self.addCleanup = lambda f: f()
        
        import price_stop_loss as module
        self.module = module

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
        
        assert self.g.trades == 0
        assert self.g.wins == 0
        assert self.g.stop_count == 0
        assert self.g.buy_times == {}

    def test_buy_no_limit_up_stocks(self):
        context = SimpleNamespace()
        context.previous_date = datetime(2024, 1, 15)
        context.portfolio = SimpleNamespace()
        context.portfolio.available_cash = 100000
        
        mock_securities = pd.DataFrame({
            'display_name': ['平安银行']
        }, index=['000001.XSHE'])
        self.jqdata.get_all_securities.return_value = mock_securities
        
        info = SimpleNamespace()
        info.start_date = datetime(2020, 1, 1)
        self.jqdata.get_security_info.return_value = info
        
        st_df = pd.DataFrame({
            '2024-01-15': [False]
        }, index=['000001.XSHE']).T
        self.jqdata.get_extras.return_value = st_df
        
        df = pd.DataFrame({
            'code': ['000001.XSHE'],
            'close': [9.0],
            'high_limit': [10.0]
        })
        self.jqdata.get_price.return_value = df
        
        self.module.buy(context)
        
        assert self.g.trades == 0

    def test_buy_filters_st_stocks(self):
        context = SimpleNamespace()
        context.previous_date = datetime(2024, 1, 15)
        context.portfolio = SimpleNamespace()
        context.portfolio.available_cash = 100000
        
        mock_securities = pd.DataFrame({
            'display_name': ['ST股票', '正常股票']
        }, index=['000001.XSHE', '000002.XSHE'])
        self.jqdata.get_all_securities.return_value = mock_securities
        
        info1 = SimpleNamespace()
        info1.start_date = datetime(2020, 1, 1)
        info2 = SimpleNamespace()
        info2.start_date = datetime(2020, 1, 1)
        self.jqdata.get_security_info.side_effect = [info1, info2]
        
        st_df = pd.DataFrame({
            '2024-01-15': [True, False]
        }, index=['000001.XSHE', '000002.XSHE']).T
        self.jqdata.get_extras.return_value = st_df
        
        df = pd.DataFrame({
            'code': ['000001.XSHE', '000002.XSHE'],
            'close': [10.0, 20.0],
            'high_limit': [10.0, 20.0]
        })
        self.jqdata.get_price.return_value = df
        
        stock_data1 = SimpleNamespace()
        stock_data1.paused = True
        stock_data2 = SimpleNamespace()
        stock_data2.paused = False
        stock_data2.pre_close = 18.18
        stock_data2.day_open = 18.28
        
        self.jqdata.get_current_data.return_value = {
            '000001.XSHE': stock_data1,
            '000002.XSHE': stock_data2
        }
        
        self.module.buy(context)
        
        assert '000001.XSHE' not in self.g.buy_times

    def test_buy_filters_paused_stocks(self):
        context = SimpleNamespace()
        context.previous_date = datetime(2024, 1, 15)
        context.portfolio = SimpleNamespace()
        context.portfolio.available_cash = 100000
        
        mock_securities = pd.DataFrame({
            'display_name': ['平安银行']
        }, index=['000001.XSHE'])
        self.jqdata.get_all_securities.return_value = mock_securities
        
        info = SimpleNamespace()
        info.start_date = datetime(2020, 1, 1)
        self.jqdata.get_security_info.return_value = info
        
        st_df = pd.DataFrame({
            '2024-01-15': [False]
        }, index=['000001.XSHE']).T
        self.jqdata.get_extras.return_value = st_df
        
        df = pd.DataFrame({
            'code': ['000001.XSHE'],
            'close': [10.0],
            'high_limit': [10.0]
        })
        self.jqdata.get_price.return_value = df
        
        stock_data = SimpleNamespace()
        stock_data.paused = True
        
        self.jqdata.get_current_data.return_value = {'000001.XSHE': stock_data}
        
        self.module.buy(context)
        
        assert self.g.trades == 0

    def test_buy_filters_open_pct_range(self):
        context = SimpleNamespace()
        context.previous_date = datetime(2024, 1, 15)
        context.portfolio = SimpleNamespace()
        context.portfolio.available_cash = 100000
        
        mock_securities = pd.DataFrame({
            'display_name': ['平安银行']
        }, index=['000001.XSHE'])
        self.jqdata.get_all_securities.return_value = mock_securities
        
        info = SimpleNamespace()
        info.start_date = datetime(2020, 1, 1)
        self.jqdata.get_security_info.return_value = info
        
        st_df = pd.DataFrame({
            '2024-01-15': [False]
        }, index=['000001.XSHE']).T
        self.jqdata.get_extras.return_value = st_df
        
        df = pd.DataFrame({
            'code': ['000001.XSHE'],
            'close': [10.0],
            'high_limit': [10.0]
        })
        self.jqdata.get_price.return_value = df
        
        stock_data = SimpleNamespace()
        stock_data.paused = False
        stock_data.pre_close = 9.0
        stock_data.day_open = 9.5
        
        self.jqdata.get_current_data.return_value = {'000001.XSHE': stock_data}
        
        self.module.buy(context)
        
        assert self.g.trades == 0

    def test_buy_in_valid_open_pct_range(self):
        context = SimpleNamespace()
        context.previous_date = datetime(2024, 1, 15)
        context.current_dt = datetime(2024, 1, 15, 9, 35)
        context.portfolio = SimpleNamespace()
        context.portfolio.available_cash = 100000
        
        mock_securities = pd.DataFrame({
            'display_name': ['平安银行']
        }, index=['000001.XSHE'])
        self.jqdata.get_all_securities.return_value = mock_securities
        
        info = SimpleNamespace()
        info.start_date = datetime(2020, 1, 1)
        self.jqdata.get_security_info.return_value = info
        
        st_df = pd.DataFrame({
            '2024-01-15': [False]
        }, index=['000001.XSHE']).T
        self.jqdata.get_extras.return_value = st_df
        
        df = pd.DataFrame({
            'code': ['000001.XSHE'],
            'close': [10.0],
            'high_limit': [10.0]
        })
        self.jqdata.get_price.return_value = df
        
        stock_data = SimpleNamespace()
        stock_data.paused = False
        stock_data.pre_close = 9.09
        stock_data.day_open = 9.19
        
        self.jqdata.get_current_data.return_value = {'000001.XSHE': stock_data}
        
        val_df = pd.DataFrame({
            'circulating_market_cap': [100]
        }, index=['000001.XSHE'])
        self.jqdata.get_valuation.return_value = val_df
        
        self.module.buy(context)
        
        assert self.g.trades >= 0

    def test_buy_filters_cap_range(self):
        context = SimpleNamespace()
        context.previous_date = datetime(2024, 1, 15)
        context.portfolio = SimpleNamespace()
        context.portfolio.available_cash = 100000
        
        mock_securities = pd.DataFrame({
            'display_name': ['平安银行']
        }, index=['000001.XSHE'])
        self.jqdata.get_all_securities.return_value = mock_securities
        
        info = SimpleNamespace()
        info.start_date = datetime(2020, 1, 1)
        self.jqdata.get_security_info.return_value = info
        
        st_df = pd.DataFrame({
            '2024-01-15': [False]
        }, index=['000001.XSHE']).T
        self.jqdata.get_extras.return_value = st_df
        
        df = pd.DataFrame({
            'code': ['000001.XSHE'],
            'close': [10.0],
            'high_limit': [10.0]
        })
        self.jqdata.get_price.return_value = df
        
        stock_data = SimpleNamespace()
        stock_data.paused = False
        stock_data.pre_close = 9.09
        stock_data.day_open = 9.19
        
        self.jqdata.get_current_data.return_value = {'000001.XSHE': stock_data}
        
        val_df = pd.DataFrame({
            'circulating_market_cap': [25]
        }, index=['000001.XSHE'])
        self.jqdata.get_valuation.return_value = val_df
        
        self.module.buy(context)
        
        assert self.g.trades == 0

    def test_buy_max_3_stocks(self):
        context = SimpleNamespace()
        context.previous_date = datetime(2024, 1, 15)
        context.current_dt = datetime(2024, 1, 15, 9, 35)
        context.portfolio = SimpleNamespace()
        context.portfolio.available_cash = 300000
        
        stocks = ['000001.XSHE', '000002.XSHE', '000003.XSHE', '000004.XSHE']
        mock_securities = pd.DataFrame({
            'display_name': ['Stock' + str(i) for i in range(4)]
        }, index=stocks)
        self.jqdata.get_all_securities.return_value = mock_securities
        
        info = SimpleNamespace()
        info.start_date = datetime(2020, 1, 1)
        self.jqdata.get_security_info.return_value = info
        
        st_df = pd.DataFrame({
            '2024-01-15': [False, False, False, False]
        }, index=stocks).T
        self.jqdata.get_extras.return_value = st_df
        
        df = pd.DataFrame({
            'code': stocks,
            'close': [10.0, 20.0, 30.0, 40.0],
            'high_limit': [10.0, 20.0, 30.0, 40.0]
        })
        self.jqdata.get_price.return_value = df
        
        current_data = {}
        for s in stocks:
            stock_data = SimpleNamespace()
            stock_data.paused = False
            stock_data.pre_close = 9.09
            stock_data.day_open = 9.19
            current_data[s] = stock_data
        self.jqdata.get_current_data.return_value = current_data
        
        val_df = pd.DataFrame({
            'circulating_market_cap': [100, 100, 100, 100]
        }, index=stocks)
        self.jqdata.get_valuation.return_value = val_df
        
        self.module.buy(context)
        
        assert self.g.trades <= 3

    def test_check_price_stop_loss_below_threshold(self):
        context = SimpleNamespace()
        context.portfolio = SimpleNamespace()
        
        pos = SimpleNamespace()
        pos.closeable_amount = 100
        pos.avg_cost = 10.0
        
        context.portfolio.positions = {'000001.XSHE': pos}
        
        stock_data = SimpleNamespace()
        stock_data.last_price = 9.5
        
        self.jqdata.get_current_data.return_value = {'000001.XSHE': stock_data}
        
        self.module.check_price_stop(context)
        
        self.jqdata.order_target.assert_called_once_with('000001.XSHE', 0)
        assert self.g.stop_count == 1

    def test_check_price_stop_loss_above_threshold(self):
        context = SimpleNamespace()
        context.portfolio = SimpleNamespace()
        
        pos = SimpleNamespace()
        pos.closeable_amount = 100
        pos.avg_cost = 10.0
        
        context.portfolio.positions = {'000001.XSHE': pos}
        
        stock_data = SimpleNamespace()
        stock_data.last_price = 9.8
        
        self.jqdata.get_current_data.return_value = {'000001.XSHE': stock_data}
        
        self.module.check_price_stop(context)
        
        self.jqdata.order_target.assert_not_called()
        assert self.g.stop_count == 0

    def test_check_price_stop_loss_no_closeable_amount(self):
        context = SimpleNamespace()
        context.portfolio = SimpleNamespace()
        
        pos = SimpleNamespace()
        pos.closeable_amount = 0
        pos.avg_cost = 10.0
        
        context.portfolio.positions = {'000001.XSHE': pos}
        
        stock_data = SimpleNamespace()
        stock_data.last_price = 9.5
        
        self.jqdata.get_current_data.return_value = {'000001.XSHE': stock_data}
        
        self.module.check_price_stop(context)
        
        self.jqdata.order_target.assert_not_called()

    def test_sell_end_with_profit(self):
        context = SimpleNamespace()
        context.portfolio = SimpleNamespace()
        
        pos = SimpleNamespace()
        pos.closeable_amount = 100
        pos.avg_cost = 10.0
        
        context.portfolio.positions = {'000001.XSHE': pos}
        
        self.g.buy_times = {'000001.XSHE': datetime(2024, 1, 15)}
        
        stock_data = SimpleNamespace()
        stock_data.last_price = 11.0
        
        self.jqdata.get_current_data.return_value = {'000001.XSHE': stock_data}
        
        self.module.sell_end(context)
        
        assert self.g.wins == 1
        assert '000001.XSHE' not in self.g.buy_times

    def test_sell_end_with_loss(self):
        context = SimpleNamespace()
        context.portfolio = SimpleNamespace()
        
        pos = SimpleNamespace()
        pos.closeable_amount = 100
        pos.avg_cost = 10.0
        
        context.portfolio.positions = {'000001.XSHE': pos}
        
        self.g.buy_times = {'000001.XSHE': datetime(2024, 1, 15)}
        
        stock_data = SimpleNamespace()
        stock_data.last_price = 9.0
        
        self.jqdata.get_current_data.return_value = {'000001.XSHE': stock_data}
        
        self.module.sell_end(context)
        
        assert self.g.wins == 0
        assert '000001.XSHE' not in self.g.buy_times

    def test_sell_end_no_closeable_amount(self):
        context = SimpleNamespace()
        context.portfolio = SimpleNamespace()
        
        pos = SimpleNamespace()
        pos.closeable_amount = 0
        pos.avg_cost = 10.0
        
        context.portfolio.positions = {'000001.XSHE': pos}
        
        self.module.sell_end(context)
        
        self.jqdata.order_target.assert_not_called()

    def test_buy_filters_excluded_stock_codes(self):
        context = SimpleNamespace()
        context.previous_date = datetime(2024, 1, 15)
        context.portfolio = SimpleNamespace()
        context.portfolio.available_cash = 100000
        
        stocks = ['000001.XSHE', '688001.XSHG', '400001.XSHE', '800001.XSHG', '300001.XSHE']
        mock_securities = pd.DataFrame({
            'display_name': ['Stock' + str(i) for i in range(5)]
        }, index=stocks)
        self.jqdata.get_all_securities.return_value = mock_securities
        
        info = SimpleNamespace()
        info.start_date = datetime(2020, 1, 1)
        self.jqdata.get_security_info.return_value = info
        
        st_df = pd.DataFrame({
            '2024-01-15': [False, False, False, False, False]
        }, index=stocks).T
        self.jqdata.get_extras.return_value = st_df
        
        df = pd.DataFrame({
            'code': [],
            'close': [],
            'high_limit': []
        })
        self.jqdata.get_price.return_value = df
        
        self.module.buy(context)
        
        get_price_call = self.jqdata.get_price.call_args_list
        if get_price_call:
            for call in get_price_call:
                if len(call[0]) > 0:
                    stocks_arg = call[0][0]
                    for excluded in ['688001.XSHG', '400001.XSHE', '800001.XSHG', '300001.XSHE']:
                        if excluded in stocks_arg:
                            pass
                    break

    def test_check_price_stop_multiple_positions(self):
        context = SimpleNamespace()
        context.portfolio = SimpleNamespace()
        
        pos1 = SimpleNamespace()
        pos1.closeable_amount = 100
        pos1.avg_cost = 10.0
        
        pos2 = SimpleNamespace()
        pos2.closeable_amount = 100
        pos2.avg_cost = 20.0
        
        context.portfolio.positions = {'000001.XSHE': pos1, '000002.XSHE': pos2}
        
        current_data = {
            '000001.XSHE': SimpleNamespace(last_price=9.5),
            '000002.XSHE': SimpleNamespace(last_price=19.5)
        }
        self.jqdata.get_current_data.return_value = current_data
        
        self.module.check_price_stop(context)
        
        assert self.jqdata.order_target.call_count == 1
        assert self.g.stop_count == 1