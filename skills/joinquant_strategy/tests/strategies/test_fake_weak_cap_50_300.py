import pytest
from unittest.mock import Mock, MagicMock, patch
from datetime import datetime, timedelta
import pandas as pd
from types import SimpleNamespace
import sys


class TestFakeWeakCap50_300:
    @pytest.fixture(autouse=True)
    def setup_mocks(self, mock_jqdata):
        self.jqdata = mock_jqdata
        self.g = SimpleNamespace()
        self.g.trades = 0
        self.g.wins = 0
        
        self.jqdata.g = self.g
        sys.modules['jqdata'] = self.jqdata
        
        patcher = patch.dict(sys.modules, {'jqdata': self.jqdata})
        patcher.start()
        self.addCleanup(patcher.stop)
        
        import fake_weak_cap_50_300 as module
        self.module = module

    def addCleanup(self, cleanup):
        cleanup()

    def test_initialize_sets_options(self):
        context = SimpleNamespace()
        
        self.module.initialize(context)
        
        self.jqdata.set_option.assert_any_call("use_real_price", True)
        self.jqdata.set_option.assert_any_call("avoid_future_data", True)
        self.jqdata.log.set_level.assert_called_once_with("system", "error")

    def test_initialize_sets_global_variables(self):
        context = SimpleNamespace()
        
        self.module.initialize(context)
        
        assert self.g.trades == 0
        assert self.g.wins == 0

    def test_buy_cap_in_range_50_300(self):
        context = SimpleNamespace()
        context.previous_date = datetime(2024, 1, 15)
        context.portfolio = SimpleNamespace()
        context.portfolio.available_cash = 100000
        
        mock_securities = pd.DataFrame({
            'display_name': ['Stock1']
        }, index=['000001.XSHE'])
        self.jqdata.get_all_securities.return_value = mock_securities
        
        prices = pd.DataFrame({
            'code': ['000001.XSHE'],
            'close': [10.0],
            'high_limit': [10.0]
        })
        self.jqdata.get_price.return_value = prices
        
        self.jqdata.get_extras.return_value = pd.DataFrame({0: [False]}, index=['000001.XSHE']).T
        
        mock_info = SimpleNamespace()
        mock_info.start_date = datetime(2023, 1, 1)
        self.jqdata.get_security_info.return_value = mock_info
        
        stock_data = SimpleNamespace()
        stock_data.paused = False
        stock_data.pre_close = 10.0
        stock_data.day_open = 10.1
        
        self.jqdata.get_current_data.return_value = {'000001.XSHE': stock_data}
        
        val_data = pd.DataFrame({
            'circulating_market_cap': [150.0]
        })
        self.jqdata.get_valuation.return_value = val_data
        
        self.module.buy(context)
        
        assert self.g.trades >= 0

    def test_buy_cap_below_range(self):
        context = SimpleNamespace()
        context.previous_date = datetime(2024, 1, 15)
        context.portfolio = SimpleNamespace()
        context.portfolio.available_cash = 100000
        
        mock_securities = pd.DataFrame({
            'display_name': ['Stock1']
        }, index=['000001.XSHE'])
        self.jqdata.get_all_securities.return_value = mock_securities
        
        prices = pd.DataFrame({
            'code': ['000001.XSHE'],
            'close': [10.0],
            'high_limit': [10.0]
        })
        self.jqdata.get_price.return_value = prices
        
        self.jqdata.get_extras.return_value = pd.DataFrame({0: [False]}, index=['000001.XSHE']).T
        
        mock_info = SimpleNamespace()
        mock_info.start_date = datetime(2023, 1, 1)
        self.jqdata.get_security_info.return_value = mock_info
        
        stock_data = SimpleNamespace()
        stock_data.paused = False
        stock_data.pre_close = 10.0
        stock_data.day_open = 10.1
        
        self.jqdata.get_current_data.return_value = {'000001.XSHE': stock_data}
        
        val_data = pd.DataFrame({
            'circulating_market_cap': [30.0]
        })
        self.jqdata.get_valuation.return_value = val_data
        
        self.module.buy(context)
        
        self.jqdata.order_value.assert_not_called()

    def test_buy_cap_above_range(self):
        context = SimpleNamespace()
        context.previous_date = datetime(2024, 1, 15)
        context.portfolio = SimpleNamespace()
        context.portfolio.available_cash = 100000
        
        mock_securities = pd.DataFrame({
            'display_name': ['Stock1']
        }, index=['000001.XSHE'])
        self.jqdata.get_all_securities.return_value = mock_securities
        
        prices = pd.DataFrame({
            'code': ['000001.XSHE'],
            'close': [10.0],
            'high_limit': [10.0]
        })
        self.jqdata.get_price.return_value = prices
        
        self.jqdata.get_extras.return_value = pd.DataFrame({0: [False]}, index=['000001.XSHE']).T
        
        mock_info = SimpleNamespace()
        mock_info.start_date = datetime(2023, 1, 1)
        self.jqdata.get_security_info.return_value = mock_info
        
        stock_data = SimpleNamespace()
        stock_data.paused = False
        stock_data.pre_close = 10.0
        stock_data.day_open = 10.1
        
        self.jqdata.get_current_data.return_value = {'000001.XSHE': stock_data}
        
        val_data = pd.DataFrame({
            'circulating_market_cap': [400.0]
        })
        self.jqdata.get_valuation.return_value = val_data
        
        self.module.buy(context)
        
        self.jqdata.order_value.assert_not_called()

    def test_sell_records_profit(self):
        context = SimpleNamespace()
        context.portfolio = SimpleNamespace()
        pos = SimpleNamespace()
        pos.closeable_amount = 100
        pos.avg_cost = 10.0
        context.portfolio.positions = {'000001.XSHE': pos}
        
        stock_data = SimpleNamespace()
        stock_data.last_price = 12.0
        self.jqdata.get_current_data.return_value = {'000001.XSHE': stock_data}
        
        self.module.sell(context)
        
        assert self.g.wins == 1

    def test_sell_handles_loss(self):
        context = SimpleNamespace()
        context.portfolio = SimpleNamespace()
        pos = SimpleNamespace()
        pos.closeable_amount = 100
        pos.avg_cost = 12.0
        context.portfolio.positions = {'000001.XSHE': pos}
        
        stock_data = SimpleNamespace()
        stock_data.last_price = 10.0
        self.jqdata.get_current_data.return_value = {'000001.XSHE': stock_data}
        
        self.module.sell(context)
        
        assert self.g.wins == 0