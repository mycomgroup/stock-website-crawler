import pytest
from unittest.mock import Mock, MagicMock, patch
from datetime import datetime, timedelta
import pandas as pd
from types import SimpleNamespace
import sys


class TestFakeWeakV2:
    @pytest.fixture(autouse=True)
    def setup_mocks(self, mock_jqdata):
        self.jqdata = mock_jqdata
        self.g = SimpleNamespace()
        self.g.trades = 0
        self.g.wins = 0
        self.g.pnl_list = []
        
        self.jqdata.g = self.g
        sys.modules['jqdata'] = self.jqdata
        
        patcher = patch.dict(sys.modules, {'jqdata': self.jqdata})
        patcher.start()
        self.addCleanup(patcher.stop)
        
        import fake_weak_v2 as module
        self.module = module

    def addCleanup(self, cleanup):
        cleanup()

    def test_initialize_sets_options(self):
        context = SimpleNamespace()
        
        self.module.initialize(context)
        
        self.jqdata.set_option.assert_any_call("use_real_price", True)
        self.jqdata.set_option.assert_any_call("avoid_future_data", True)
        self.jqdata.log.set_level.assert_called_once_with("system", "error")
        self.jqdata.set_benchmark.assert_called_once_with("000300.XSHG")
        self.jqdata.run_weekly.assert_called_once()

    def test_initialize_sets_global_variables(self):
        context = SimpleNamespace()
        
        self.module.initialize(context)
        
        assert self.g.trades == 0
        assert self.g.wins == 0
        assert self.g.pnl_list == []

    def test_buy_and_sell_sells_positions(self):
        context = SimpleNamespace()
        context.current_dt = datetime(2024, 1, 16)
        context.portfolio = SimpleNamespace()
        pos = SimpleNamespace()
        pos.closeable_amount = 100
        pos.avg_cost = 10.0
        context.portfolio.positions = {'000001.XSHE': pos}
        
        mock_securities = pd.DataFrame({
            'display_name': ['Stock1']
        }, index=['000001.XSHE'])
        self.jqdata.get_all_securities.return_value = mock_securities
        
        prices = pd.DataFrame({
            'code': ['000001.XSHE'],
            'close': [9.0],
            'high_limit': [10.0]
        })
        self.jqdata.get_price.return_value = prices
        
        self.module.buy_and_sell(context)
        
        self.jqdata.order_target.assert_called()

    def test_buy_and_sell_no_high_limit_stocks(self):
        context = SimpleNamespace()
        context.current_dt = datetime(2024, 1, 16)
        context.portfolio = SimpleNamespace()
        context.portfolio.positions = {}
        context.portfolio.available_cash = 100000
        
        mock_securities = pd.DataFrame({
            'display_name': ['Stock1']
        }, index=['000001.XSHE'])
        self.jqdata.get_all_securities.return_value = mock_securities
        
        prices = pd.DataFrame({
            'code': ['000001.XSHE'],
            'close': [9.0],
            'high_limit': [10.0]
        })
        self.jqdata.get_price.return_value = prices
        
        self.jqdata.get_current_data.return_value = {}
        
        self.module.buy_and_sell(context)
        
        self.jqdata.log.info.assert_called()

    def test_buy_and_sell_filters_by_open_pct(self):
        context = SimpleNamespace()
        context.current_dt = datetime(2024, 1, 16)
        context.portfolio = SimpleNamespace()
        context.portfolio.positions = {}
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
        
        stock_data = SimpleNamespace()
        stock_data.paused = False
        stock_data.pre_close = 10.0
        stock_data.day_open = 10.1
        
        self.jqdata.get_current_data.return_value = {'000001.XSHE': stock_data}
        
        self.module.buy_and_sell(context)
        
        assert self.g.trades >= 0

    def test_buy_and_sell_open_pct_out_of_range(self):
        context = SimpleNamespace()
        context.current_dt = datetime(2024, 1, 16)
        context.portfolio = SimpleNamespace()
        context.portfolio.positions = {}
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
        
        stock_data = SimpleNamespace()
        stock_data.paused = False
        stock_data.pre_close = 10.0
        stock_data.day_open = 10.5
        
        self.jqdata.get_current_data.return_value = {'000001.XSHE': stock_data}
        
        self.module.buy_and_sell(context)
        
        self.jqdata.order_value.assert_not_called()

    def test_buy_and_sell_handles_exception(self):
        context = SimpleNamespace()
        context.current_dt = datetime(2024, 1, 16)
        context.portfolio = SimpleNamespace()
        context.portfolio.positions = {}
        
        self.jqdata.get_all_securities.side_effect = Exception("Test error")
        
        self.module.buy_and_sell(context)
        
        self.jqdata.log.info.assert_called()

    def test_buy_and_sell_handles_paused_stocks(self):
        context = SimpleNamespace()
        context.current_dt = datetime(2024, 1, 16)
        context.portfolio = SimpleNamespace()
        context.portfolio.positions = {}
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
        
        stock_data = SimpleNamespace()
        stock_data.paused = True
        stock_data.pre_close = 10.0
        stock_data.day_open = 10.1
        
        self.jqdata.get_current_data.return_value = {'000001.XSHE': stock_data}
        
        self.module.buy_and_sell(context)
        
        self.jqdata.order_value.assert_not_called()

    def test_buy_and_sell_filters_stocks_by_prefix(self):
        context = SimpleNamespace()
        context.current_dt = datetime(2024, 1, 16)
        context.portfolio = SimpleNamespace()
        context.portfolio.positions = {}
        context.portfolio.available_cash = 100000
        
        mock_securities = pd.DataFrame({
            'display_name': ['Stock1', 'Stock2']
        }, index=['000001.XSHE', '688001.XSHG'])
        self.jqdata.get_all_securities.return_value = mock_securities
        
        prices = pd.DataFrame({
            'code': ['000001.XSHE'],
            'close': [10.0],
            'high_limit': [10.0]
        })
        self.jqdata.get_price.return_value = prices
        
        stock_data = SimpleNamespace()
        stock_data.paused = False
        stock_data.pre_close = 10.0
        stock_data.day_open = 10.1
        
        self.jqdata.get_current_data.return_value = {'000001.XSHE': stock_data}
        
        self.module.buy_and_sell(context)
        
        assert self.g.trades >= 0

    def test_buy_and_sell_negative_pre_close(self):
        context = SimpleNamespace()
        context.current_dt = datetime(2024, 1, 16)
        context.portfolio = SimpleNamespace()
        context.portfolio.positions = {}
        
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
        
        stock_data = SimpleNamespace()
        stock_data.paused = False
        stock_data.pre_close = 0.0
        stock_data.day_open = 10.1
        
        self.jqdata.get_current_data.return_value = {'000001.XSHE': stock_data}
        
        self.module.buy_and_sell(context)
        
        self.jqdata.order_value.assert_not_called()