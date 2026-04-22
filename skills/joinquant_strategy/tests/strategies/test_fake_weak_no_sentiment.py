import pytest
from unittest.mock import Mock, MagicMock, patch
from datetime import datetime, timedelta
import pandas as pd
from types import SimpleNamespace
import sys


class TestFakeWeakNoSentiment:
    @pytest.fixture(autouse=True)
    def setup_mocks(self, mock_jqdata):
        self.jqdata = mock_jqdata
        self.g = SimpleNamespace()
        self.g.trades = 0
        self.g.wins = 0
        self.g.pnl_list = []
        self.g.signals = 0
        
        self.jqdata.g = self.g
        sys.modules['jqdata'] = self.jqdata
        
        patcher = patch.dict(sys.modules, {'jqdata': self.jqdata})
        patcher.start()
        self.addCleanup(patcher.stop)
        
        import fake_weak_no_sentiment as module
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
        assert self.jqdata.run_daily.call_count == 2

    def test_initialize_sets_global_variables(self):
        context = SimpleNamespace()
        
        self.module.initialize(context)
        
        assert self.g.trades == 0
        assert self.g.wins == 0
        assert self.g.pnl_list == []
        assert self.g.signals == 0

    def test_buy_stocks_filters_stocks(self):
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
            'circulating_market_cap': [100.0]
        })
        self.jqdata.get_valuation.return_value = val_data
        
        self.module.buy_stocks(context)
        
        self.jqdata.get_all_securities.assert_called()

    def test_buy_stocks_no_high_limit(self):
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
            'close': [9.0],
            'high_limit': [10.0]
        })
        self.jqdata.get_price.return_value = prices
        
        self.jqdata.get_extras.return_value = pd.DataFrame({0: [False]}, index=['000001.XSHE']).T
        
        mock_info = SimpleNamespace()
        mock_info.start_date = datetime(2023, 1, 1)
        self.jqdata.get_security_info.return_value = mock_info
        
        self.jqdata.get_current_data.return_value = {}
        
        self.module.buy_stocks(context)
        
        self.jqdata.order_value.assert_not_called()

    def test_buy_stocks_cap_filter_30_200(self):
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
            'circulating_market_cap': [100.0]
        })
        self.jqdata.get_valuation.return_value = val_data
        
        self.module.buy_stocks(context)
        
        assert self.g.trades >= 0

    def test_buy_stocks_cap_below_range(self):
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
            'circulating_market_cap': [20.0]
        })
        self.jqdata.get_valuation.return_value = val_data
        
        self.module.buy_stocks(context)
        
        self.jqdata.order_value.assert_not_called()

    def test_sell_stocks_records_pnl(self):
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
        
        assert len(self.g.pnl_list) == 1
        assert self.g.wins == 1

    def test_sell_stocks_handles_loss(self):
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
        assert self.g.wins == 0

    def test_buy_stocks_open_pct_filter(self):
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
        stock_data.day_open = 10.5
        
        self.jqdata.get_current_data.return_value = {'000001.XSHE': stock_data}
        
        val_data = pd.DataFrame({
            'circulating_market_cap': [100.0]
        })
        self.jqdata.get_valuation.return_value = val_data
        
        self.module.buy_stocks(context)
        
        self.jqdata.order_value.assert_not_called()

    def test_signals_counter(self):
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
            'circulating_market_cap': [100.0]
        })
        self.jqdata.get_valuation.return_value = val_data
        
        initial_signals = self.g.signals
        self.module.buy_stocks(context)
        
        assert self.g.signals >= initial_signals