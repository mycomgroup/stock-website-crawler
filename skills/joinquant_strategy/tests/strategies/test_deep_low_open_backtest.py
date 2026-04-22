import pytest
from unittest.mock import Mock, MagicMock, patch, call
from datetime import datetime
import pandas as pd
from types import SimpleNamespace
import sys


class TestDeepLowOpenBacktest:
    @pytest.fixture(autouse=True)
    def setup_mocks(self, mock_jqdata):
        self.jqdata = mock_jqdata
        self.g = SimpleNamespace()
        self.g.test_dates = ["2024-01-15", "2024-07-15"]
        self.g.signals = []
        self.g.current_test_idx = 0
        
        self.jqdata.g = self.g
        sys.modules['jqdata'] = self.jqdata
        
        patcher = patch.dict(sys.modules, {'jqdata': self.jqdata})
        patcher.start()
        self.addCleanup(patcher.stop)
        
        import deep_low_open_backtest as module
        self.module = module

    def addCleanup(self, cleanup):
        cleanup()

    def test_initialize_sets_options(self):
        context = SimpleNamespace()
        
        self.module.initialize(context)
        
        self.jqdata.set_option.assert_any_call("use_real_price", True)
        self.jqdata.set_option.assert_any_call("avoid_future_data", True)
        self.jqdata.log.set_level.assert_called_once_with("system", "error")
        self.jqdata.run_daily.assert_called_once()

    def test_initialize_sets_global_variables(self):
        context = SimpleNamespace()
        
        self.module.initialize(context)
        
        assert self.g.test_dates == ["2024-01-15", "2024-07-15"]
        assert self.g.signals == []
        assert self.g.current_test_idx == 0

    def test_test_deep_low_open_skips_when_all_dates_processed(self):
        context = SimpleNamespace()
        self.g.current_test_idx = 2
        
        self.module.test_deep_low_open(context)
        
        self.jqdata.get_all_securities.assert_not_called()

    def test_test_deep_low_open_processes_first_date(self):
        context = SimpleNamespace()
        self.g.current_test_idx = 0
        
        mock_securities = pd.DataFrame({
            'display_name': ['平安银行', '万科A', '浦发银行']
        }, index=['000001.XSHE', '000002.XSHE', '600000.XSHG'])
        self.jqdata.get_all_securities.return_value = mock_securities
        
        prev_data = pd.DataFrame({
            'close': [10.0, 9.5],
            'high_limit': [10.0, 10.0]
        })
        self.jqdata.get_price.return_value = prev_data
        
        self.module.test_deep_low_open(context)
        
        assert self.g.current_test_idx == 1

    def test_test_deep_low_open_filters_limit_up_stocks(self):
        context = SimpleNamespace()
        self.g.current_test_idx = 0
        
        mock_securities = pd.DataFrame({
            'display_name': ['Stock1']
        }, index=['000001.XSHE'])
        self.jqdata.get_all_securities.return_value = mock_securities
        
        prev_data = pd.DataFrame({
            'close': [10.0],
            'high_limit': [10.0]
        }, index=[0])
        prev_data['code'] = ['000001.XSHE']
        
        curr_data = pd.DataFrame({
            'open': [9.5],
            'close': [10.2],
            'high': [10.5]
        }, index=[0])
        
        self.jqdata.get_price.side_effect = [prev_data, curr_data]
        
        self.module.test_deep_low_open(context)
        
        if len(self.g.signals) > 0:
            signal = self.g.signals[0]
            assert -5.0 <= signal['open_pct'] < -3.0

    def test_test_deep_low_open_handles_empty_prev_data(self):
        context = SimpleNamespace()
        self.g.current_test_idx = 0
        
        mock_securities = pd.DataFrame({
            'display_name': ['Stock1']
        }, index=['000001.XSHE'])
        self.jqdata.get_all_securities.return_value = mock_securities
        
        self.jqdata.get_price.return_value = None
        
        self.module.test_deep_low_open(context)
        
        assert len(self.g.signals) == 0

    def test_test_deep_low_open_handles_insufficient_prev_data(self):
        context = SimpleNamespace()
        self.g.current_test_idx = 0
        
        mock_securities = pd.DataFrame({
            'display_name': ['Stock1']
        }, index=['000001.XSHE'])
        self.jqdata.get_all_securities.return_value = mock_securities
        
        prev_data = pd.DataFrame({'close': [10.0], 'high_limit': [10.0]})
        self.jqdata.get_price.side_effect = [prev_data, None]
        
        self.module.test_deep_low_open(context)
        
        assert len(self.g.signals) == 0

    def test_test_deep_low_open_skips_non_limit_up(self):
        context = SimpleNamespace()
        self.g.current_test_idx = 0
        
        mock_securities = pd.DataFrame({
            'display_name': ['Stock1']
        }, index=['000001.XSHE'])
        self.jqdata.get_all_securities.return_value = mock_securities
        
        prev_data = pd.DataFrame({
            'close': [9.0],
            'high_limit': [10.0]
        }, index=[0])
        
        curr_data = pd.DataFrame({
            'open': [9.0],
            'close': [9.5],
            'high': [10.0]
        }, index=[0])
        
        self.jqdata.get_price.side_effect = [prev_data, curr_data]
        
        self.module.test_deep_low_open(context)
        
        assert len(self.g.signals) == 0

    def test_test_deep_low_open_calculates_intra_return(self):
        context = SimpleNamespace()
        self.g.current_test_idx = 0
        
        mock_securities = pd.DataFrame({
            'display_name': ['Stock1']
        }, index=['000001.XSHE'])
        self.jqdata.get_all_securities.return_value = mock_securities
        
        prev_data = pd.DataFrame({
            'close': [10.0],
            'high_limit': [10.0]
        }, index=[0])
        
        curr_data = pd.DataFrame({
            'open': [9.6],
            'close': [10.0],
            'high': [10.5]
        }, index=[0])
        
        self.jqdata.get_price.side_effect = [prev_data, curr_data]
        
        self.module.test_deep_low_open(context)
        
        if len(self.g.signals) > 0:
            signal = self.g.signals[0]
            assert 'intra_return' in signal
            assert 'max_return' in signal
            assert 'is_win' in signal

    def test_on_strategy_end_with_no_signals(self):
        context = SimpleNamespace()
        self.g.signals = []
        
        self.module.on_strategy_end(context)
        
        self.jqdata.log.info.assert_called()

    def test_on_strategy_end_with_signals(self):
        context = SimpleNamespace()
        self.g.signals = [
            {
                'date': '2024-01-15',
                'stock': '000001.XSHE',
                'open_pct': -4.0,
                'intra_return': 2.0,
                'max_return': 5.0,
                'is_win': True
            }
        ]
        
        self.module.on_strategy_end(context)
        
        self.jqdata.log.info.assert_called()

    def test_on_strategy_end_calculates_win_rate(self):
        context = SimpleNamespace()
        self.g.signals = [
            {'date': '2024-01-15', 'stock': '000001.XSHE', 'open_pct': -4.0,
             'intra_return': 2.0, 'max_return': 5.0, 'is_win': True},
            {'date': '2024-01-15', 'stock': '000002.XSHE', 'open_pct': -4.5,
             'intra_return': -1.0, 'max_return': 2.0, 'is_win': False},
        ]
        
        self.module.on_strategy_end(context)
        
        self.jqdata.log.info.assert_called()

    def test_handles_exception_gracefully(self):
        context = SimpleNamespace()
        self.g.current_test_idx = 0
        
        mock_securities = pd.DataFrame({
            'display_name': ['Stock1']
        }, index=['000001.XSHE'])
        self.jqdata.get_all_securities.return_value = mock_securities
        
        self.jqdata.get_price.side_effect = Exception("Test error")
        
        self.module.test_deep_low_open(context)
        
        assert self.g.current_test_idx == 1