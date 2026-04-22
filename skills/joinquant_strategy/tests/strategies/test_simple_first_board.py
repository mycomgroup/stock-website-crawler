import pytest
from unittest.mock import Mock, MagicMock, patch
from datetime import datetime, timedelta
import pandas as pd
from types import SimpleNamespace
import sys


class TestSimpleFirstBoard:
    @pytest.fixture(autouse=True)
    def setup_mocks(self, mock_jqdata):
        self.jqdata = mock_jqdata
        self.g = SimpleNamespace()
        self.g.target_list = []
        self.g.trade_count = 0
        
        self.jqdata.g = self.g
        sys.modules['jqdata'] = self.jqdata
        
        patcher = patch.dict(sys.modules, {'jqdata': self.jqdata})
        patcher.start()
        self.addCleanup(patcher.stop)
        
        import simple_first_board as module
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
        
        assert self.g.target_list == []
        assert self.g.trade_count == 0

    def test_get_stock_list_identifies_limit_up(self):
        context = SimpleNamespace()
        context.previous_date = datetime(2024, 1, 15)
        
        mock_securities = pd.DataFrame({
            'display_name': ['平安银行', '万科A', '浦发银行']
        }, index=['000001.XSHE', '000002.XSHE', '600000.XSHG'])
        self.jqdata.get_all_securities.return_value = mock_securities
        
        mock_info = SimpleNamespace()
        mock_info.start_date = datetime(2023, 1, 1)
        self.jqdata.get_security_info.return_value = mock_info
        
        df = pd.DataFrame({
            'code': ['000001.XSHE', '000002.XSHE'],
            'close': [10.0, 20.0],
            'high_limit': [10.0, 20.0]
        })
        self.jqdata.get_price.return_value = df
        
        self.module.get_stock_list(context)
        
        assert len(self.g.target_list) > 0

    def test_get_stock_list_filters_excluded_stocks(self):
        context = SimpleNamespace()
        context.previous_date = datetime(2024, 1, 15)
        
        mock_securities = pd.DataFrame({
            'display_name': ['Stock1', 'Stock2', 'Stock3', 'Stock4', 'Stock5']
        }, index=['000001.XSHE', '688001.XSHG', '300001.XSHE', '400001.XSHE', '800001.XSHG'])
        self.jqdata.get_all_securities.return_value = mock_securities
        
        mock_info = SimpleNamespace()
        mock_info.start_date = datetime(2023, 1, 1)
        self.jqdata.get_security_info.return_value = mock_info
        
        df = pd.DataFrame({
            'code': ['000001.XSHE'],
            'close': [10.0],
            'high_limit': [10.0]
        })
        self.jqdata.get_price.return_value = df
        
        self.module.get_stock_list(context)
        
        assert '688001.XSHG' not in self.g.target_list
        assert '300001.XSHE' not in self.g.target_list
        assert '400001.XSHE' not in self.g.target_list
        assert '800001.XSHG' not in self.g.target_list

    def test_get_stock_list_filters_new_stocks(self):
        context = SimpleNamespace()
        context.previous_date = datetime(2024, 1, 15)
        
        mock_securities = pd.DataFrame({
            'display_name': ['OldStock', 'NewStock']
        }, index=['000001.XSHE', '000002.XSHE'])
        self.jqdata.get_all_securities.return_value = mock_securities
        
        mock_info_old = SimpleNamespace()
        mock_info_old.start_date = datetime(2023, 1, 1)
        
        mock_info_new = SimpleNamespace()
        mock_info_new.start_date = datetime(2024, 1, 1)
        
        def get_security_info_side_effect(code):
            if code == '000001.XSHE':
                return mock_info_old
            else:
                return mock_info_new
        
        self.jqdata.get_security_info.side_effect = get_security_info_side_effect
        
        df = pd.DataFrame({
            'code': ['000001.XSHE'],
            'close': [10.0],
            'high_limit': [10.0]
        })
        self.jqdata.get_price.return_value = df
        
        self.module.get_stock_list(context)
        
        assert '000002.XSHE' not in self.g.target_list
        assert '000001.XSHE' in self.g.target_list

    def test_get_stock_list_handles_empty_result(self):
        context = SimpleNamespace()
        context.previous_date = datetime(2024, 1, 15)
        
        mock_securities = pd.DataFrame({
            'display_name': ['平安银行']
        }, index=['000001.XSHE'])
        self.jqdata.get_all_securities.return_value = mock_securities
        
        mock_info = SimpleNamespace()
        mock_info.start_date = datetime(2023, 1, 1)
        self.jqdata.get_security_info.return_value = mock_info
        
        df = pd.DataFrame({
            'code': ['000001.XSHE'],
            'close': [9.0],
            'high_limit': [10.0]
        })
        self.jqdata.get_price.return_value = df
        
        self.module.get_stock_list(context)
        
        assert self.g.target_list == []

    def test_buy_no_target_list(self):
        context = SimpleNamespace()
        context.previous_date = datetime(2024, 1, 16)
        context.portfolio = SimpleNamespace()
        context.portfolio.available_cash = 100000
        
        self.g.target_list = []
        
        self.module.buy(context)
        
        self.jqdata.get_current_data.assert_not_called()

    def test_buy_filters_paused_stocks(self):
        context = SimpleNamespace()
        context.previous_date = datetime(2024, 1, 16)
        context.portfolio = SimpleNamespace()
        context.portfolio.available_cash = 100000
        
        self.g.target_list = ['000001.XSHE']
        
        stock_data = SimpleNamespace()
        stock_data.paused = True
        stock_data.is_st = False
        stock_data.pre_close = 10.0
        stock_data.high_limit = 11.0
        stock_data.day_open = 10.0
        
        self.jqdata.get_current_data.return_value = {'000001.XSHE': stock_data}
        
        self.module.buy(context)
        
        self.jqdata.order_value.assert_not_called()

    def test_buy_filters_st_stocks(self):
        context = SimpleNamespace()
        context.previous_date = datetime(2024, 1, 16)
        context.portfolio = SimpleNamespace()
        context.portfolio.available_cash = 100000
        
        self.g.target_list = ['000001.XSHE']
        
        stock_data = SimpleNamespace()
        stock_data.paused = False
        stock_data.is_st = True
        stock_data.pre_close = 10.0
        stock_data.high_limit = 11.0
        stock_data.day_open = 10.0
        
        self.jqdata.get_current_data.return_value = {'000001.XSHE': stock_data}
        
        self.module.buy(context)
        
        self.jqdata.order_value.assert_not_called()

    def test_buy_filters_zero_pre_close(self):
        context = SimpleNamespace()
        context.previous_date = datetime(2024, 1, 16)
        context.portfolio = SimpleNamespace()
        context.portfolio.available_cash = 100000
        
        self.g.target_list = ['000001.XSHE']
        
        stock_data = SimpleNamespace()
        stock_data.paused = False
        stock_data.is_st = False
        stock_data.pre_close = 0
        stock_data.high_limit = 11.0
        stock_data.day_open = 10.0
        
        self.jqdata.get_current_data.return_value = {'000001.XSHE': stock_data}
        
        self.module.buy(context)
        
        self.jqdata.order_value.assert_not_called()

    def test_buy_filters_open_ratio_range(self):
        context = SimpleNamespace()
        context.previous_date = datetime(2024, 1, 16)
        context.portfolio = SimpleNamespace()
        context.portfolio.available_cash = 100000
        
        self.g.target_list = ['000001.XSHE']
        
        stock_data = SimpleNamespace()
        stock_data.paused = False
        stock_data.is_st = False
        stock_data.pre_close = 10.0
        stock_data.high_limit = 11.0
        stock_data.day_open = 10.5
        stock_data.last_price = 10.5
        
        self.jqdata.get_current_data.return_value = {'000001.XSHE': stock_data}
        
        val_data = pd.DataFrame({
            'circulating_market_cap': [100.0]
        })
        self.jqdata.get_valuation.return_value = val_data
        
        self.module.buy(context)
        
        self.jqdata.order_value.assert_not_called()

    def test_buy_in_valid_open_ratio_range(self):
        context = SimpleNamespace()
        context.previous_date = datetime(2024, 1, 16)
        context.portfolio = SimpleNamespace()
        context.portfolio.available_cash = 100000
        
        self.g.target_list = ['000001.XSHE']
        
        stock_data = SimpleNamespace()
        stock_data.paused = False
        stock_data.is_st = False
        stock_data.pre_close = 10.0
        stock_data.high_limit = 11.0
        stock_data.day_open = 10.1
        stock_data.last_price = 10.1
        
        self.jqdata.get_current_data.return_value = {'000001.XSHE': stock_data}
        
        val_data = pd.DataFrame({
            'circulating_market_cap': [100.0]
        })
        self.jqdata.get_valuation.return_value = val_data
        
        self.module.buy(context)
        
        self.jqdata.order_value.assert_called()
        assert self.g.trade_count > 0

    def test_buy_filters_market_cap_range(self):
        context = SimpleNamespace()
        context.previous_date = datetime(2024, 1, 16)
        context.portfolio = SimpleNamespace()
        context.portfolio.available_cash = 100000
        
        self.g.target_list = ['000001.XSHE']
        
        stock_data = SimpleNamespace()
        stock_data.paused = False
        stock_data.is_st = False
        stock_data.pre_close = 10.0
        stock_data.high_limit = 11.0
        stock_data.day_open = 10.1
        stock_data.last_price = 10.1
        
        self.jqdata.get_current_data.return_value = {'000001.XSHE': stock_data}
        
        val_data = pd.DataFrame({
            'circulating_market_cap': [20.0]
        })
        self.jqdata.get_valuation.return_value = val_data
        
        self.module.buy(context)
        
        self.jqdata.order_value.assert_not_called()

    def test_buy_market_cap_in_range_50_150(self):
        context = SimpleNamespace()
        context.previous_date = datetime(2024, 1, 16)
        context.portfolio = SimpleNamespace()
        context.portfolio.available_cash = 100000
        
        self.g.target_list = ['000001.XSHE']
        
        stock_data = SimpleNamespace()
        stock_data.paused = False
        stock_data.is_st = False
        stock_data.pre_close = 10.0
        stock_data.high_limit = 11.0
        stock_data.day_open = 10.1
        stock_data.last_price = 10.1
        
        self.jqdata.get_current_data.return_value = {'000001.XSHE': stock_data}
        
        val_data = pd.DataFrame({
            'circulating_market_cap': [100.0]
        })
        self.jqdata.get_valuation.return_value = val_data
        
        self.module.buy(context)
        
        self.jqdata.order_value.assert_called()

    def test_buy_handles_empty_valuation(self):
        context = SimpleNamespace()
        context.previous_date = datetime(2024, 1, 16)
        context.portfolio = SimpleNamespace()
        context.portfolio.available_cash = 100000
        
        self.g.target_list = ['000001.XSHE']
        
        stock_data = SimpleNamespace()
        stock_data.paused = False
        stock_data.is_st = False
        stock_data.pre_close = 10.0
        stock_data.high_limit = 11.0
        stock_data.day_open = 10.1
        stock_data.last_price = 10.1
        
        self.jqdata.get_current_data.return_value = {'000001.XSHE': stock_data}
        
        self.jqdata.get_valuation.return_value = None
        
        self.module.buy(context)
        
        self.jqdata.order_value.assert_not_called()

    def test_buy_handles_valuation_empty_dataframe(self):
        context = SimpleNamespace()
        context.previous_date = datetime(2024, 1, 16)
        context.portfolio = SimpleNamespace()
        context.portfolio.available_cash = 100000
        
        self.g.target_list = ['000001.XSHE']
        
        stock_data = SimpleNamespace()
        stock_data.paused = False
        stock_data.is_st = False
        stock_data.pre_close = 10.0
        stock_data.high_limit = 11.0
        stock_data.day_open = 10.1
        stock_data.last_price = 10.1
        
        self.jqdata.get_current_data.return_value = {'000001.XSHE': stock_data}
        
        self.jqdata.get_valuation.return_value = pd.DataFrame()
        
        self.module.buy(context)
        
        self.jqdata.order_value.assert_not_called()

    def test_buy_missing_in_current_data(self):
        context = SimpleNamespace()
        context.previous_date = datetime(2024, 1, 16)
        context.portfolio = SimpleNamespace()
        context.portfolio.available_cash = 100000
        
        self.g.target_list = ['000001.XSHE']
        
        self.jqdata.get_current_data.return_value = {}
        
        self.module.buy(context)
        
        self.jqdata.order_value.assert_not_called()

    def test_buy_multiple_qualified_stocks(self):
        context = SimpleNamespace()
        context.previous_date = datetime(2024, 1, 16)
        context.portfolio = SimpleNamespace()
        context.portfolio.available_cash = 200000
        
        self.g.target_list = ['000001.XSHE', '000002.XSHE']
        
        stock_data1 = SimpleNamespace()
        stock_data1.paused = False
        stock_data1.is_st = False
        stock_data1.pre_close = 10.0
        stock_data1.high_limit = 11.0
        stock_data1.day_open = 10.1
        stock_data1.last_price = 10.1
        
        stock_data2 = SimpleNamespace()
        stock_data2.paused = False
        stock_data2.is_st = False
        stock_data2.pre_close = 20.0
        stock_data2.high_limit = 22.0
        stock_data2.day_open = 20.2
        stock_data2.last_price = 20.2
        
        self.jqdata.get_current_data.return_value = {
            '000001.XSHE': stock_data1,
            '000002.XSHE': stock_data2
        }
        
        val_data = pd.DataFrame({
            'circulating_market_cap': [100.0]
        })
        self.jqdata.get_valuation.return_value = val_data
        
        self.module.buy(context)
        
        assert self.jqdata.order_value.call_count == 2

    def test_sell_with_positions(self):
        context = SimpleNamespace()
        context.portfolio = SimpleNamespace()
        pos = SimpleNamespace()
        pos.closeable_amount = 100
        context.portfolio.positions = {'000001.XSHE': pos}
        
        self.module.sell(context)
        
        self.jqdata.order_target_value.assert_called_once_with('000001.XSHE', 0)

    def test_sell_without_closeable_amount(self):
        context = SimpleNamespace()
        context.portfolio = SimpleNamespace()
        pos = SimpleNamespace()
        pos.closeable_amount = 0
        context.portfolio.positions = {'000001.XSHE': pos}
        
        self.module.sell(context)
        
        self.jqdata.order_target_value.assert_not_called()

    def test_sell_multiple_positions(self):
        context = SimpleNamespace()
        context.portfolio = SimpleNamespace()
        
        pos1 = SimpleNamespace()
        pos1.closeable_amount = 100
        
        pos2 = SimpleNamespace()
        pos2.closeable_amount = 100
        
        context.portfolio.positions = {'000001.XSHE': pos1, '000002.XSHE': pos2}
        
        self.module.sell(context)
        
        assert self.jqdata.order_target_value.call_count == 2

    def test_sell_no_positions(self):
        context = SimpleNamespace()
        context.portfolio = SimpleNamespace()
        context.portfolio.positions = {}
        
        self.module.sell(context)
        
        self.jqdata.order_target_value.assert_not_called()

    def test_buy_insufficient_cash(self):
        context = SimpleNamespace()
        context.previous_date = datetime(2024, 1, 16)
        context.portfolio = SimpleNamespace()
        context.portfolio.available_cash = 50
        
        self.g.target_list = ['000001.XSHE']
        
        stock_data = SimpleNamespace()
        stock_data.paused = False
        stock_data.is_st = False
        stock_data.pre_close = 10.0
        stock_data.high_limit = 11.0
        stock_data.day_open = 10.1
        stock_data.last_price = 10.1
        
        self.jqdata.get_current_data.return_value = {'000001.XSHE': stock_data}
        
        val_data = pd.DataFrame({
            'circulating_market_cap': [100.0]
        })
        self.jqdata.get_valuation.return_value = val_data
        
        self.module.buy(context)
        
        self.jqdata.order_value.assert_not_called()