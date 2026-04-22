import pytest
from unittest.mock import Mock, MagicMock, patch, call
from datetime import datetime, timedelta
import pandas as pd
from types import SimpleNamespace
import sys


class TestDeepLowOpenStrategy:
    @pytest.fixture(autouse=True)
    def setup_mocks(self, mock_jqdata):
        self.jqdata = mock_jqdata
        self.g = SimpleNamespace()
        self.g.signals = []
        self.g.total_zt = 0
        
        self.jqdata.g = self.g
        sys.modules['jqdata'] = self.jqdata
        
        patcher = patch.dict(sys.modules, {'jqdata': self.jqdata})
        patcher.start()
        self.addCleanup(patcher.stop)
        
        import deep_low_open_strategy as module
        self.module = module

    def addCleanup(self, cleanup):
        cleanup()

    def test_initialize_sets_options(self):
        context = SimpleNamespace()
        
        self.module.initialize(context)
        
        self.jqdata.set_option.assert_any_call("use_real_price", True)
        self.jqdata.log.set_level.assert_called_once_with("system", "error")
        self.jqdata.run_daily.assert_called_once()

    def test_initialize_sets_global_variables(self):
        context = SimpleNamespace()
        
        self.module.initialize(context)
        
        assert hasattr(self.g, 'signals')
        assert hasattr(self.g, 'total_zt')

    def test_count_deep_low_open_processes_data(self):
        context = SimpleNamespace()
        context.current_dt = datetime(2024, 1, 16)
        context.previous_date = datetime(2024, 1, 15)
        
        mock_securities = pd.DataFrame({
            'display_name': ['平安银行']
        }, index=['000001.XSHE'])
        self.jqdata.get_all_securities.return_value = mock_securities
        
        price_prev = pd.DataFrame({
            'code': ['000001.XSHE'],
            'close': [10.0],
            'high_limit': [10.0]
        })
        
        price_curr = pd.DataFrame({
            'code': ['000001.XSHE'],
            'open': [9.5],
            'close': [10.2],
            'high': [10.5]
        })
        
        self.jqdata.get_price.side_effect = [price_prev, price_curr]
        
        self.module.count_deep_low_open(context)
        
        self.jqdata.get_all_securities.assert_called()

    def test_count_deep_low_open_empty_prev_price(self):
        context = SimpleNamespace()
        context.current_dt = datetime(2024, 1, 16)
        context.previous_date = datetime(2024, 1, 15)
        
        mock_securities = pd.DataFrame({
            'display_name': ['平安银行']
        }, index=['000001.XSHE'])
        self.jqdata.get_all_securities.return_value = mock_securities
        
        self.jqdata.get_price.return_value = pd.DataFrame()
        
        self.module.count_deep_low_open(context)
        
        assert self.g.total_zt == 0

    def test_count_deep_low_open_empty_curr_price(self):
        context = SimpleNamespace()
        context.current_dt = datetime(2024, 1, 16)
        context.previous_date = datetime(2024, 1, 15)
        
        mock_securities = pd.DataFrame({
            'display_name': ['平安银行']
        }, index=['000001.XSHE'])
        self.jqdata.get_all_securities.return_value = mock_securities
        
        price_prev = pd.DataFrame({
            'code': ['000001.XSHE'],
            'close': [10.0],
            'high_limit': [10.0]
        })
        
        self.jqdata.get_price.side_effect = [price_prev, pd.DataFrame()]
        
        self.module.count_deep_low_open(context)
        
        assert self.g.total_zt == 1

    def test_count_deep_low_open_filters_deep_low_open(self):
        context = SimpleNamespace()
        context.current_dt = datetime(2024, 1, 16)
        context.previous_date = datetime(2024, 1, 15)
        
        mock_securities = pd.DataFrame({
            'display_name': ['Stock1']
        }, index=['000001.XSHE'])
        self.jqdata.get_all_securities.return_value = mock_securities
        
        price_prev = pd.DataFrame({
            'code': ['000001.XSHE'],
            'close': [10.0],
            'high_limit': [10.0]
        })
        
        price_curr = pd.DataFrame({
            'code': ['000001.XSHE'],
            'open': [9.6],
            'close': [10.0],
            'high': [10.5]
        })
        
        self.jqdata.get_price.side_effect = [price_prev, price_curr]
        
        self.module.count_deep_low_open(context)
        
        if len(self.g.signals) > 0:
            signal = self.g.signals[0]
            assert -5.0 <= signal['open_pct'] < -3.0

    def test_count_deep_low_open_no_limit_stocks(self):
        context = SimpleNamespace()
        context.current_dt = datetime(2024, 1, 16)
        context.previous_date = datetime(2024, 1, 15)
        
        mock_securities = pd.DataFrame({
            'display_name': ['Stock1']
        }, index=['000001.XSHE'])
        self.jqdata.get_all_securities.return_value = mock_securities
        
        price_prev = pd.DataFrame({
            'code': ['000001.XSHE'],
            'close': [9.0],
            'high_limit': [10.0]
        })
        
        self.jqdata.get_price.return_value = price_prev
        
        self.module.count_deep_low_open(context)
        
        assert len(self.g.signals) == 0

    def test_after_trading_does_nothing(self):
        context = SimpleNamespace()
        
        result = self.module.after_trading(context)
        
        assert result is None

    def test_on_strategy_end_with_no_signals(self):
        context = SimpleNamespace()
        self.g.signals = []
        self.g.total_zt = 10
        
        self.module.on_strategy_end(context)
        
        self.jqdata.log.info.assert_called()

    def test_on_strategy_end_with_signals(self):
        context = SimpleNamespace()
        self.g.signals = [
            {'date': '2024-01-16', 'stock': '000001.XSHE', 'open_pct': -4.0, 'intra_return': 2.0}
        ]
        self.g.total_zt = 50
        
        self.module.on_strategy_end(context)
        
        self.jqdata.log.info.assert_called()

    def test_handles_exception_in_stock_processing(self):
        context = SimpleNamespace()
        context.current_dt = datetime(2024, 1, 16)
        context.previous_date = datetime(2024, 1, 15)
        
        mock_securities = pd.DataFrame({
            'display_name': ['Stock1']
        }, index=['000001.XSHE'])
        self.jqdata.get_all_securities.return_value = mock_securities
        
        price_prev = pd.DataFrame({
            'code': ['000001.XSHE'],
            'close': [10.0],
            'high_limit': [10.0]
        })
        
        price_curr = pd.DataFrame({
            'code': ['000001.XSHE'],
            'open': [None],
            'close': [10.0],
            'high': [10.5]
        })
        
        self.jqdata.get_price.side_effect = [price_prev, price_curr]
        
        self.module.count_deep_low_open(context)
        
        assert len(self.g.signals) == 0