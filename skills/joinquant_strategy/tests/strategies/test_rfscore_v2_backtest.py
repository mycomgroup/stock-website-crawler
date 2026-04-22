import pytest
from unittest.mock import Mock, MagicMock, patch
from datetime import datetime, timedelta
import pandas as pd
import numpy as np
from types import SimpleNamespace
import sys


class MockFactor:
    name = "RFScore"
    max_window = 1
    dependencies = []
    basic = None
    fscore = None
    
    def calc(self, data):
        pass


class TestRFScoreV2Backtest:
    @pytest.fixture(autouse=True)
    def setup_mocks(self, mock_jqdata):
        self.jqdata = mock_jqdata
        self.g = SimpleNamespace()
        self.g.ipo_days = 180
        self.g.base_hold_num = 20
        self.g.primary_pb_group = 1
        self.g.reduced_pb_group = 2
        self.g.rsrs_slope_series = []
        self.g.last_month = 0
        self.g.high_prices = {}
        
        self.jqdata.g = self.g
        
        mock_jqfactor = MagicMock()
        mock_jqfactor.Factor = MockFactor
        mock_jqfactor.calc_factors = Mock()
        
        mock_scipy = MagicMock()
        mock_scipy.stats.linregress = Mock(return_value=(0.5, 0, 0.8, 0, 0))
        
        sys.modules['jqdata'] = self.jqdata
        sys.modules['jqfactor'] = mock_jqfactor
        sys.modules['scipy.stats'] = mock_scipy.stats
        
        patcher = patch.dict(sys.modules, {
            'jqdata': self.jqdata, 
            'jqfactor': mock_jqfactor,
            'scipy.stats': mock_scipy.stats
        })
        patcher.start()
        self.addCleanup = lambda f: f()
        self.mock_scipy = mock_scipy
        
        import rfscore_v2_backtest as module
        self.module = module

    def test_initialize_sets_options(self):
        context = SimpleNamespace()
        
        self.module.initialize(context)
        
        self.jqdata.set_benchmark.assert_called_once_with("000300.XSHG")
        self.jqdata.set_option.assert_any_call("use_real_price", True)
        self.jqdata.set_option.assert_any_call("avoid_future_data", True)

    def test_initialize_sets_order_cost(self):
        context = SimpleNamespace()
        
        self.module.initialize(context)
        
        self.jqdata.set_order_cost.assert_called_once()

    def test_initialize_sets_global_variables(self):
        context = SimpleNamespace()
        
        self.module.initialize(context)
        
        assert self.g.ipo_days == 180
        assert self.g.base_hold_num == 20
        assert self.g.rsrs_slope_series == []

    def test_get_universe_filters_stocks(self):
        self.jqdata.get_index_stocks.return_value = ['000001.XSHE', '000002.XSHE']
        
        mock_securities = pd.DataFrame({
            'display_name': ['平安银行', '万科A'],
            'start_date': [datetime(2020, 1, 1), datetime(2023, 1, 1)]
        }, index=['000001.XSHE', '000002.XSHE'])
        self.jqdata.get_all_securities.return_value = mock_securities
        
        st_df = pd.DataFrame({
            '2024-01-15': [False, False]
        }, index=['000001.XSHE', '000002.XSHE']).T
        self.jqdata.get_extras.return_value = st_df
        
        paused_df = pd.DataFrame({
            'time': [datetime(2024, 1, 15)],
            'code': ['000001.XSHE', '000002.XSHE'],
            'paused': [0, 0]
        })
        self.jqdata.get_price.return_value = paused_df
        
        result = self.module.get_universe(datetime(2024, 1, 15))
        
        assert isinstance(result, list)

    def test_get_universe_filters_excluded_prefixes(self):
        stocks = ['000001.XSHE', '688001.XSHG', '400001.XSHE', '800001.XSHG']
        self.jqdata.get_index_stocks.return_value = stocks
        
        mock_securities = pd.DataFrame({
            'display_name': ['Stock' + str(i) for i in range(4)],
            'start_date': [datetime(2020, 1, 1)] * 4
        }, index=stocks)
        self.jqdata.get_all_securities.return_value = mock_securities
        
        st_df = pd.DataFrame({
            '2024-01-15': [False, False, False, False]
        }, index=stocks).T
        self.jqdata.get_extras.return_value = st_df
        
        paused_df = pd.DataFrame({
            'time': [datetime(2024, 1, 15)],
            'code': stocks,
            'paused': [0, 0, 0, 0]
        })
        self.jqdata.get_price.return_value = paused_df
        
        result = self.module.get_universe(datetime(2024, 1, 15))
        
        for s in result:
            assert not s.startswith(('68', '4', '8'))

    def test_calc_breadth_returns_value(self):
        self.jqdata.get_index_stocks.return_value = ['000001.XSHE', '000002.XSHE']
        
        price_df = pd.DataFrame({
            'time': [datetime(2024, 1, 15)] * 2,
            'code': ['000001.XSHE', '000002.XSHE'],
            'close': [10.0, 20.0]
        })
        self.jqdata.get_price.return_value = price_df
        
        result = self.module.calc_breadth(datetime(2024, 1, 15))
        
        assert isinstance(result, float)
        assert 0 <= result <= 1

    def test_calc_breadth_handles_exception(self):
        self.jqdata.get_index_stocks.side_effect = Exception("Test error")
        
        result = self.module.calc_breadth(datetime(2024, 1, 15))
        
        assert result == 0.5

    def test_calc_rsrs_returns_signal(self):
        price_df = pd.DataFrame({
            'high': [10.5] * 18,
            'low': [9.5] * 18
        })
        self.jqdata.get_price.return_value = price_df
        
        signal, value = self.module.calc_rsrs(datetime(2024, 1, 15))
        
        assert signal in ["BULLISH", "BEARISH", "NEUTRAL"]
        assert isinstance(value, float)

    def test_calc_rsrs_handles_insufficient_data(self):
        price_df = pd.DataFrame({
            'high': [10.5] * 10,
            'low': [9.5] * 10
        })
        self.jqdata.get_price.return_value = price_df
        
        signal, value = self.module.calc_rsrs(datetime(2024, 1, 15))
        
        assert signal == "NEUTRAL"
        assert value == 0.0

    def test_calc_rsrs_handles_exception(self):
        self.jqdata.get_price.side_effect = Exception("Test error")
        
        signal, value = self.module.calc_rsrs(datetime(2024, 1, 15))
        
        assert signal == "NEUTRAL"
        assert value == 0.0

    def test_calc_rsrs_updates_slope_series(self):
        price_df = pd.DataFrame({
            'high': [10.5] * 18,
            'low': [9.5] * 18
        })
        self.jqdata.get_price.return_value = price_df
        
        for _ in range(3):
            self.module.calc_rsrs(datetime(2024, 1, 15))
        
        assert len(self.g.rsrs_slope_series) >= 3

    def test_calc_rsrs_limits_series_length(self):
        price_df = pd.DataFrame({
            'high': [10.5] * 18,
            'low': [9.5] * 18
        })
        self.jqdata.get_price.return_value = price_df
        
        for _ in range(700):
            self.module.calc_rsrs(datetime(2024, 1, 15))
        
        assert len(self.g.rsrs_slope_series) <= 600

    def test_choose_stocks_returns_list(self):
        self.jqdata.get_index_stocks.return_value = ['000001.XSHE']
        
        mock_securities = pd.DataFrame({
            'display_name': ['平安银行'],
            'start_date': [datetime(2020, 1, 1)]
        }, index=['000001.XSHE'])
        self.jqdata.get_all_securities.return_value = mock_securities
        
        st_df = pd.DataFrame({
            '2024-01-15': [False]
        }, index=['000001.XSHE']).T
        self.jqdata.get_extras.return_value = st_df
        
        paused_df = pd.DataFrame({
            'time': [datetime(2024, 1, 15)],
            'code': ['000001.XSHE'],
            'paused': [0]
        })
        self.jqdata.get_price.return_value = paused_df
        
        mock_factor = MockFactor()
        mock_factor.basic = pd.DataFrame({
            'ROA': [5.0],
            'OCFOA': [0.3],
            'DELTA_MARGIN': [0.1],
            'DELTA_TURN': [0.05],
            'RFScore': [7]
        }, index=['000001.XSHE'])
        mock_factor.fscore = pd.Series([7], index=['000001.XSHE'])
        
        self.mock_jqfactor = sys.modules['jqfactor']
        self.mock_jqfactor.calc_factors = Mock()
        
        val_df = pd.DataFrame({
            'code': ['000001.XSHE'],
            'pb_ratio': [1.0],
            'pe_ratio': [10.0]
        })
        self.jqdata.get_valuation.return_value = val_df
        
        result = self.module.choose_stocks(datetime(2024, 1, 15), 10)
        
        assert isinstance(result, list)

    def test_filter_buyable_filters_paused(self):
        stocks = ['000001.XSHE', '000002.XSHE']
        
        current_data = {
            '000001.XSHE': SimpleNamespace(paused=True, is_st=False, name='Stock1',
                                          last_price=10.0, high_limit=11.0),
            '000002.XSHE': SimpleNamespace(paused=False, is_st=False, name='Stock2',
                                          last_price=10.0, high_limit=11.0)
        }
        self.jqdata.get_current_data.return_value = current_data
        
        result = self.module.filter_buyable(SimpleNamespace(), stocks)
        
        assert '000001.XSHE' not in result

    def test_filter_buyable_filters_st(self):
        stocks = ['000001.XSHE', '000002.XSHE']
        
        current_data = {
            '000001.XSHE': SimpleNamespace(paused=False, is_st=True, name='ST Stock',
                                          last_price=10.0, high_limit=11.0),
            '000002.XSHE': SimpleNamespace(paused=False, is_st=False, name='Stock2',
                                          last_price=10.0, high_limit=11.0)
        }
        self.jqdata.get_current_data.return_value = current_data
        
        result = self.module.filter_buyable(SimpleNamespace(), stocks)
        
        assert '000001.XSHE' not in result

    def test_filter_buyable_filters_st_name(self):
        stocks = ['000001.XSHE', '000002.XSHE']
        
        current_data = {
            '000001.XSHE': SimpleNamespace(paused=False, is_st=False, name='ST平安银行',
                                          last_price=10.0, high_limit=11.0),
            '000002.XSHE': SimpleNamespace(paused=False, is_st=False, name='Stock2',
                                          last_price=10.0, high_limit=11.0)
        }
        self.jqdata.get_current_data.return_value = current_data
        
        result = self.module.filter_buyable(SimpleNamespace(), stocks)
        
        assert '000001.XSHE' not in result

    def test_filter_buyable_filters_high_limit_price(self):
        stocks = ['000001.XSHE']
        
        current_data = {
            '000001.XSHE': SimpleNamespace(paused=False, is_st=False, name='Stock',
                                          last_price=10.99, high_limit=11.0)
        }
        self.jqdata.get_current_data.return_value = current_data
        
        result = self.module.filter_buyable(SimpleNamespace(), stocks)
        
        assert result == []

    def test_filter_buyable_stock_not_in_data(self):
        stocks = ['000001.XSHE']
        
        self.jqdata.get_current_data.return_value = {}
        
        result = self.module.filter_buyable(SimpleNamespace(), stocks)
        
        assert result == []

    def test_rebalance_same_month_skips(self):
        context = SimpleNamespace()
        context.previous_date = datetime(2024, 1, 15)
        
        self.g.last_month = 1
        
        self.module.rebalance(context)
        
        self.jqdata.log.info.assert_not_called()

    def test_rebalance_different_month_processes(self):
        context = SimpleNamespace()
        context.previous_date = datetime(2024, 2, 15)
        context.portfolio = SimpleNamespace()
        context.portfolio.total_value = 100000
        context.portfolio.positions = {}
        
        self.g.last_month = 1
        
        self.jqdata.get_index_stocks.return_value = ['000001.XSHE']
        self.jqdata.get_price.return_value = pd.DataFrame({
            'time': [datetime(2024, 2, 15)],
            'code': ['000001.XSHE'],
            'close': [10.0]
        })
        
        self.module.rebalance(context)
        
        assert self.g.last_month == 2

    def test_rebreadths_position_by_breadth(self):
        self.jqdata.get_index_stocks.return_value = ['000001.XSHE']
        
        price_df = pd.DataFrame({
            'time': [datetime(2024, 1, 15)] * 20,
            'code': ['000001.XSHE'] * 20,
            'close': [10.0] * 20
        })
        self.jqdata.get_price.return_value = price_df
        
        breadth = self.module.calc_breadth(datetime(2024, 1, 15))
        
        assert 0 <= breadth <= 1

    def test_handle_data_updates_high_prices(self):
        context = SimpleNamespace()
        context.portfolio = SimpleNamespace()
        
        pos = SimpleNamespace()
        pos.price = 10.5
        pos.avg_cost = 10.0
        
        context.portfolio.positions = {'000001.XSHE': pos}
        
        self.g.high_prices = {'000001.XSHE': 10.0}
        
        self.module.handle_data(context)
        
        assert self.g.high_prices['000001.XSHE'] == 10.5

    def test_handle_data_sets_new_high_price(self):
        context = SimpleNamespace()
        context.portfolio = SimpleNamespace()
        
        pos = SimpleNamespace()
        pos.price = 10.5
        pos.avg_cost = 10.0
        
        context.portfolio.positions = {'000001.XSHE': pos}
        
        self.g.high_prices = {}
        
        self.module.handle_data(context)
        
        assert '000001.XSHE' in self.g.high_prices
        assert self.g.high_prices['000001.XSHE'] == 10.5

    def test_handle_data_stop_loss_triggered(self):
        context = SimpleNamespace()
        context.portfolio = SimpleNamespace()
        
        pos = SimpleNamespace()
        pos.price = 9.0
        pos.avg_cost = 10.0
        
        context.portfolio.positions = {'000001.XSHE': pos}
        
        self.g.high_prices = {'000001.XSHE': 10.0}
        
        self.module.handle_data(context)
        
        self.jqdata.order_target_value.assert_called_with('000001.XSHE', 0)

    def test_handle_data_drawdown_stop_triggered(self):
        context = SimpleNamespace()
        context.portfolio = SimpleNamespace()
        
        pos = SimpleNamespace()
        pos.price = 10.0
        pos.avg_cost = 10.0
        
        context.portfolio.positions = {'000001.XSHE': pos}
        
        self.g.high_prices = {'000001.XSHE': 12.0}
        
        self.module.handle_data(context)
        
        self.jqdata.order_target_value.assert_called_with('000001.XSHE', 0)

    def test_handle_data_skips_zero_avg_cost(self):
        context = SimpleNamespace()
        context.portfolio = SimpleNamespace()
        
        pos = SimpleNamespace()
        pos.price = 9.0
        pos.avg_cost = 0
        
        context.portfolio.positions = {'000001.XSHE': pos}
        
        self.module.handle_data(context)
        
        self.jqdata.order_target_value.assert_not_called()

    def test_handle_data_no_positions(self):
        context = SimpleNamespace()
        context.portfolio = SimpleNamespace()
        context.portfolio.positions = {}
        
        self.module.handle_data(context)
        
        self.jqdata.order_target_value.assert_not_called()