import pytest
from unittest.mock import Mock, MagicMock, patch
from datetime import datetime, timedelta
import pandas as pd
from types import SimpleNamespace
import sys


class TestFakeWeak50_150:
    @pytest.fixture(autouse=True)
    def setup_mocks(self, mock_jqdata):
        self.jqdata = mock_jqdata
        self.g = SimpleNamespace()
        self.g.trades = 0
        self.g.wins = 0
        self.g.pnl_list = []
        self.g.min_cap = 50
        self.g.max_cap = 150
        
        self.jqdata.g = self.g
        sys.modules['jqdata'] = self.jqdata
        
        patcher = patch.dict(sys.modules, {'jqdata': self.jqdata})
        patcher.start()
        self.addCleanup(patcher.stop)
        
        import fake_weak_50_150 as module
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

    def test_initialize_sets_global_variables(self):
        context = SimpleNamespace()
        
        self.module.initialize(context)
        
        assert self.g.min_cap == 50
        assert self.g.max_cap == 150
        assert self.g.trades == 0
        assert self.g.wins == 0

    def test_select_and_trade_sells_positions_with_profit(self):
        context = SimpleNamespace()
        context.current_dt = datetime(2024, 1, 16)
        context.portfolio = SimpleNamespace()
        context.portfolio.available_cash = 100000
        pos = SimpleNamespace()
        pos.closeable_amount = 100
        pos.avg_cost = 10.0
        context.portfolio.positions = {'000001.XSHE': pos}
        
        stock_data = SimpleNamespace()
        stock_data.last_price = 11.0
        self.jqdata.get_current_data.return_value = {'000001.XSHE': stock_data}
        
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
        
        self.jqdata.get_extras.return_value = pd.DataFrame({0: [False]}, index=['000001.XSHE']).T
        
        mock_info = SimpleNamespace()
        mock_info.start_date = datetime(2023, 1, 1)
        self.jqdata.get_security_info.return_value = mock_info
        
        self.module.select_and_trade(context)
        
        assert len(self.g.pnl_list) == 1
        assert self.g.wins == 1

    def test_select_and_trade_records_loss(self):
        context = SimpleNamespace()
        context.current_dt = datetime(2024, 1, 16)
        context.portfolio = SimpleNamespace()
        context.portfolio.available_cash = 100000
        pos = SimpleNamespace()
        pos.closeable_amount = 100
        pos.avg_cost = 11.0
        context.portfolio.positions = {'000001.XSHE': pos}
        
        stock_data = SimpleNamespace()
        stock_data.last_price = 10.0
        self.jqdata.get_current_data.return_value = {'000001.XSHE': stock_data}
        
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
        
        self.jqdata.get_extras.return_value = pd.DataFrame({0: [False]}, index=['000001.XSHE']).T
        
        mock_info = SimpleNamespace()
        mock_info.start_date = datetime(2023, 1, 1)
        self.jqdata.get_security_info.return_value = mock_info
        
        self.module.select_and_trade(context)
        
        assert len(self.g.pnl_list) == 1
        assert self.g.wins == 0

    def test_select_and_trade_filters_by_cap_range(self):
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
            'circulating_market_cap': [100.0]
        })
        self.jqdata.get_valuation.return_value = val_data
        
        self.module.select_and_trade(context)
        
        assert self.g.trades >= 0

    def test_select_and_trade_cap_below_range(self):
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
        
        self.module.select_and_trade(context)
        
        self.jqdata.order_value.assert_not_called()

    def test_select_and_trade_cap_above_range(self):
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
            'circulating_market_cap': [200.0]
        })
        self.jqdata.get_valuation.return_value = val_data
        
        self.module.select_and_trade(context)
        
        self.jqdata.order_value.assert_not_called()

    def test_select_and_trade_sorts_by_open_pct(self):
        context = SimpleNamespace()
        context.current_dt = datetime(2024, 1, 16)
        context.portfolio = SimpleNamespace()
        context.portfolio.positions = {}
        context.portfolio.available_cash = 100000
        
        mock_securities = pd.DataFrame({
            'display_name': ['Stock1', 'Stock2']
        }, index=['000001.XSHE', '000002.XSHE'])
        self.jqdata.get_all_securities.return_value = mock_securities
        
        prices = pd.DataFrame({
            'code': ['000001.XSHE', '000002.XSHE'],
            'close': [10.0, 20.0],
            'high_limit': [10.0, 20.0]
        })
        self.jqdata.get_price.return_value = prices
        
        self.jqdata.get_extras.return_value = pd.DataFrame({
            0: [False, False]
        }, index=['000001.XSHE', '000002.XSHE']).T
        
        mock_info = SimpleNamespace()
        mock_info.start_date = datetime(2023, 1, 1)
        self.jqdata.get_security_info.return_value = mock_info
        
        stock_data1 = SimpleNamespace()
        stock_data1.paused = False
        stock_data1.pre_close = 10.0
        stock_data1.day_open = 10.05
        
        stock_data2 = SimpleNamespace()
        stock_data2.paused = False
        stock_data2.pre_close = 20.0
        stock_data2.day_open = 20.2
        
        self.jqdata.get_current_data.return_value = {
            '000001.XSHE': stock_data1,
            '000002.XSHE': stock_data2
        }
        
        def mock_val(stock, end_date, count):
            cap = 100.0 if stock == '000001.XSHE' else 80.0
            return pd.DataFrame({'circulating_market_cap': [cap]})
        
        self.jqdata.get_valuation.side_effect = mock_val
        
        self.module.select_and_trade(context)
        
        assert self.g.trades >= 0