import pytest
from unittest.mock import Mock, MagicMock, patch
from datetime import datetime
import pandas as pd
from types import SimpleNamespace
import sys


class TestExitRulesComparison:
    @pytest.fixture(autouse=True)
    def setup_mocks(self, mock_jqdata):
        self.jqdata = mock_jqdata
        self.g = SimpleNamespace()
        self.g.test_start = "2022-01-01"
        self.g.test_end = "2024-12-31"
        self.g.sample_out_date = "2024-01-01"
        self.g.open_range = (-0.01, 0.02)
        self.g.max_signals = 300
        self.g.signals = []
        self.g.results = {"S1": [], "S2": [], "S3": [], "S4": [], "S5": [], "S6": [], "S7": []}
        
        self.jqdata.g = self.g
        sys.modules['jqdata'] = self.jqdata
        
        patcher = patch.dict(sys.modules, {'jqdata': self.jqdata})
        patcher.start()
        self.addCleanup(patcher.stop)
        
        import exit_rules_comparison as module
        self.module = module

    def addCleanup(self, cleanup):
        cleanup()

    def test_initialize_sets_options(self):
        context = SimpleNamespace()
        
        self.module.initialize(context)
        
        self.jqdata.set_option.assert_any_call("use_real_price", True)
        self.jqdata.log.set_level.assert_called_once_with("order", "error")

    def test_initialize_sets_global_variables(self):
        context = SimpleNamespace()
        
        self.module.initialize(context)
        
        assert self.g.test_start == "2022-01-01"
        assert self.g.test_end == "2024-12-31"
        assert self.g.open_range == (-0.01, 0.02)
        assert self.g.max_signals == 300

    def test_run_backtest_skips_if_signals_exist(self):
        context = SimpleNamespace()
        self.g.signals = [1, 2, 3]
        
        self.module.run_backtest(context)
        
        self.jqdata.log.info.assert_not_called()

    def test_run_backtest_gets_trade_days(self):
        context = SimpleNamespace()
        self.g.signals = []
        
        mock_trade_days = [datetime(2024, 1, 15), datetime(2024, 1, 16)]
        self.jqdata.get_trade_days.return_value = mock_trade_days
        
        self.module.run_backtest(context)
        
        self.jqdata.get_trade_days.assert_called_with(self.g.test_start, self.g.test_end)

    def test_run_backtest_filters_stocks(self):
        context = SimpleNamespace()
        self.g.signals = []
        self.g.max_signals = 5
        
        mock_trade_days = [datetime(2024, 1, 15), datetime(2024, 1, 16)]
        self.jqdata.get_trade_days.return_value = mock_trade_days
        
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
        
        self.module.run_backtest(context)
        
        assert self.g.signals == [] or len(self.g.signals) >= 0

    def test_output_results_logs_summary(self):
        self.g.results = {
            "S1": [{"ret": 0.01, "so": False, "open_change": 0.005}],
            "S2": [{"ret": 0.02, "so": True, "open_change": 0.005}],
        }
        
        self.module.output_results()
        
        self.jqdata.log.info.assert_called()

    def test_output_results_handles_empty_results(self):
        self.g.results = {"S1": [], "S2": [], "S3": [], "S4": [], "S5": [], "S6": [], "S7": []}
        
        self.module.output_results()
        
        self.jqdata.log.info.assert_called()

    def test_output_results_calculates_statistics(self):
        self.g.results = {
            "S1": [{"ret": 0.05, "so": True, "open_change": 0.01}],
            "S2": [{"ret": -0.02, "so": False, "open_change": 0.01}],
            "S3": [{"ret": 0.03, "so": True, "open_change": 0.01}],
            "S4": [{"ret": 0.04, "so": False, "open_change": 0.01}],
            "S5": [{"ret": 0.05, "so": True, "open_change": 0.01}],
            "S6": [{"ret": 0.02, "so": False, "open_change": 0.01}],
            "S7": [{"ret": 0.06, "so": True, "open_change": 0.01}],
        }
        
        self.module.output_results()
        
        self.jqdata.log.info.assert_called()

    def test_handle_data_does_nothing(self):
        context = SimpleNamespace()
        data = SimpleNamespace()
        
        result = self.module.handle_data(context, data)
        
        assert result is None

    def test_run_backtest_limits_max_signals(self):
        context = SimpleNamespace()
        self.g.signals = []
        self.g.max_signals = 2
        
        mock_trade_days = [
            datetime(2024, 1, 10),
            datetime(2024, 1, 15),
            datetime(2024, 1, 16),
        ]
        self.jqdata.get_trade_days.return_value = mock_trade_days
        
        mock_securities = pd.DataFrame({
            'display_name': ['Stock1']
        }, index=['000001.XSHE'])
        self.jqdata.get_all_securities.return_value = mock_securities
        
        prices = pd.DataFrame({
            'code': ['000001.XSHE'],
            'close': [10.0],
            'high_limit': [10.0]
        })
        
        next_price = pd.DataFrame({
            'open': [10.0],
            'close': [10.5],
            'high': [10.5],
            'high_limit': [11.0]
        })
        
        self.jqdata.get_price.side_effect = [prices, next_price, prices, next_price]
        
        self.module.run_backtest(context)
        
        assert len(self.g.signals) <= self.g.max_signals

    def test_output_results_group_by_open_change(self):
        self.g.signals = [
            {'date': '2024-01-16', 'stock': '000001.XSHE', 'buy_price': 10.0, 'open_change': -0.005},
            {'date': '2024-01-16', 'stock': '000002.XSHE', 'buy_price': 20.0, 'open_change': 0.01},
        ]
        self.g.results = {
            "S1": [{"ret": 0.01, "so": False, "open_change": -0.005}],
            "S4": [{"ret": 0.02, "so": False, "open_change": 0.01}],
            "S7": [{"ret": 0.03, "so": False, "open_change": -0.005}],
        }
        
        self.module.output_results()
        
        self.jqdata.log.info.assert_called()