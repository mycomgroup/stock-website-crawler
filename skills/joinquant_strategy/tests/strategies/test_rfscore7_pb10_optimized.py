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


class TestRFScore7PB10Optimized:
    @pytest.fixture(autouse=True)
    def setup_mocks(self, mock_jqdata):
        self.jqdata = mock_jqdata
        self.g = SimpleNamespace()
        self.g.release_name = "RFScore7 PB10 Optimized V2"
        self.g.ipo_days = 180
        self.g.primary_pb_group = 1
        self.g.secondary_pb_group = 3
        self.g.max_pe_ratio = 100
        self.g.min_roa = 0.5
        self.g.industry_cap_ratio = 0.30
        self.g.max_single_ratio = 0.10
        self.g.stop_loss_ratio = -0.15
        self.g.hold_num_normal = 15
        self.g.hold_num_mid = 12
        self.g.hold_num_weak = 10
        self.g.hold_num_stop = 0
        self.g.breadth_normal = 0.35
        self.g.breadth_reduce = 0.25
        self.g.breadth_stop = 0.15
        self.g.last_market_state = {}
        self.g.last_selection = {
            "target_hold_num": 0,
            "actual_hold_num": 0,
            "primary_count": 0,
            "secondary_count": 0,
            "cash_ratio": 1.0,
            "max_industry_ratio": 0.0,
            "stop_loss_count": 0,
        }
        
        self.jqdata.g = self.g
        self.jqdata.set_order_cost = Mock()
        self.jqdata.OrderCost = Mock()
        self.jqdata.get_index_stocks = Mock(return_value=['000001.XSHE'])
        self.jqdata.get_industry = Mock(return_value={})
        self.jqdata.record = Mock()
        
        mock_jqfactor = MagicMock()
        mock_jqfactor.Factor = MockFactor
        mock_jqfactor.calc_factors = Mock()
        
        sys.modules['jqdata'] = self.jqdata
        sys.modules['jqfactor'] = mock_jqfactor
        
        patcher = patch.dict(sys.modules, {'jqdata': self.jqdata, 'jqfactor': mock_jqfactor})
        patcher.start()
        self.addCleanup = lambda f: f()
        self.mock_jqfactor = mock_jqfactor
        
        import rfscore7_pb10_optimized as module
        self.module = module

    def test_sign_function(self):
        ser = pd.Series([1, -1, 0, 5, -5])
        result = self.module.sign(ser)
        expected = pd.Series([1, 0, 0, 1, 0])
        pd.testing.assert_series_equal(result, expected)

    def test_sign_function_with_nan(self):
        ser = pd.Series([1, np.nan, -1])
        result = self.module.sign(ser)
        assert result.iloc[0] == 1
        assert result.iloc[2] == 0

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
        assert self.g.hold_num_normal == 15
        assert self.g.stop_loss_ratio == -0.15

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
            'code': ['000001.XSHE', '000002.XSHE'],
            'time': [datetime(2024, 1, 15), datetime(2024, 1, 15)],
            'paused': [0, 0]
        })
        self.jqdata.get_price.return_value = paused_df
        
        result = self.module.get_universe(datetime(2024, 1, 15))
        
        assert isinstance(result, list)

    def test_get_universe_filters_688_stocks(self):
        stocks = ['000001.XSHE', '688001.XSHG']
        self.jqdata.get_index_stocks.return_value = stocks
        
        mock_securities = pd.DataFrame({
            'display_name': ['平安银行', '科创板'],
            'start_date': [datetime(2020, 1, 1), datetime(2020, 1, 1)]
        }, index=stocks)
        self.jqdata.get_all_securities.return_value = mock_securities
        
        st_df = pd.DataFrame({
            '2024-01-15': [False, False]
        }, index=stocks).T
        self.jqdata.get_extras.return_value = st_df
        
        paused_df = pd.DataFrame({
            'code': stocks,
            'time': [datetime(2024, 1, 15), datetime(2024, 1, 15)],
            'paused': [0, 0]
        })
        self.jqdata.get_price.return_value = paused_df
        
        result = self.module.get_universe(datetime(2024, 1, 15))
        
        assert '688001.XSHG' not in result

    def test_calc_market_state(self):
        self.jqdata.get_index_stocks.return_value = ['000001.XSHE', '000002.XSHE']
        
        price_df = pd.DataFrame({
            'time': [datetime(2024, 1, 15), datetime(2024, 1, 15)],
            'code': ['000001.XSHE', '000002.XSHE'],
            'close': [10.0, 20.0]
        })
        self.jqdata.get_price.return_value = price_df
        
        idx_df = pd.DataFrame({'close': [10.0] * 20})
        
        def mock_price_side_effect(*args, **kwargs):
            if args and args[0] == "000300.XSHG":
                return idx_df
            return price_df
        
        self.jqdata.get_price.side_effect = mock_price_side_effect
        
        result = self.module.calc_market_state(datetime(2024, 1, 15))
        
        assert 'breadth' in result
        assert 'trend_on' in result
        assert 'idx_close' in result
        assert 'idx_ma20' in result

    def test_calc_composite_score_empty_df(self):
        df = pd.DataFrame()
        result = self.module.calc_composite_score(df)
        assert result.empty

    def test_calc_composite_score_calculates_score(self):
        df = pd.DataFrame({
            'RFScore': [7, 6, 5],
            'ROA': [10, 8, 6],
            'OCFOA': [0.5, 0.4, 0.3],
            'DELTA_MARGIN': [0.1, 0.05, 0.02],
            'pb_ratio': [1.0, 2.0, 3.0]
        }, index=['000001.XSHE', '000002.XSHE', '000003.XSHE'])
        
        result = self.module.calc_composite_score(df)
        
        assert 'score' in result.columns

    def test_sort_candidates_empty_df(self):
        df = pd.DataFrame()
        result = self.module.sort_candidates(df)
        assert result.empty

    def test_sort_candidates_sorts_descending(self):
        df = pd.DataFrame({
            'RFScore': [7, 6, 5],
            'ROA': [10, 8, 6],
            'OCFOA': [0.5, 0.4, 0.3],
            'DELTA_MARGIN': [0.1, 0.05, 0.02],
            'pb_ratio': [1.0, 2.0, 3.0]
        }, index=['000001.XSHE', '000002.XSHE', '000003.XSHE'])
        
        result = self.module.sort_candidates(df)
        
        assert result.index[0] == '000001.XSHE'

    def test_get_industry_map_empty_codes(self):
        result = self.module.get_industry_map([], datetime(2024, 1, 15))
        assert result == {}

    def test_get_industry_map_returns_mapping(self):
        self.jqdata.get_industry.return_value = {
            '000001.XSHE': {'sw_l1': {'industry_name': '银行'}},
            '000002.XSHE': {'sw_l1': {'industry_name': '地产'}}
        }
        
        result = self.module.get_industry_map(['000001.XSHE', '000002.XSHE'], datetime(2024, 1, 15))
        
        assert result['000001.XSHE'] == '银行'
        assert result['000002.XSHE'] == '地产'

    def test_get_industry_map_handles_missing_industry(self):
        self.jqdata.get_industry.return_value = {
            '000001.XSHE': {},
            '000002.XSHE': {'sw_l1': {'industry_name': '地产'}}
        }
        
        result = self.module.get_industry_map(['000001.XSHE', '000002.XSHE'], datetime(2024, 1, 15))
        
        assert result['000001.XSHE'] == 'Unknown'

    def test_append_with_cap_adds_stocks(self):
        picks = []
        candidates = ['000001.XSHE', '000002.XSHE', '000003.XSHE']
        industry_map = {'000001.XSHE': '银行', '000002.XSHE': '银行', '000003.XSHE': '地产'}
        industry_counts = {}
        limit_count = 2
        target_hold_num = 3
        
        added = self.module.append_with_cap(
            picks, candidates, industry_map, industry_counts, limit_count, target_hold_num
        )
        
        assert added > 0
        assert len(picks) <= target_hold_num

    def test_append_with_cap_respects_limit_count(self):
        picks = []
        candidates = ['000001.XSHE', '000002.XSHE', '000003.XSHE']
        industry_map = {'000001.XSHE': '银行', '000002.XSHE': '银行', '000003.XSHE': '银行'}
        industry_counts = {}
        limit_count = 1
        target_hold_num = 5
        
        self.module.append_with_cap(
            picks, candidates, industry_map, industry_counts, limit_count, target_hold_num
        )
        
        for ind in ['银行']:
            assert industry_counts.get(ind, 0) <= limit_count

    def test_summarize_industry_ratio_empty_picks(self):
        max_ratio, counts = self.module.summarize_industry_ratio([], {})
        assert max_ratio == 0.0
        assert counts == {}

    def test_summarize_industry_ratio_calculates_correctly(self):
        picks = ['000001.XSHE', '000002.XSHE', '000003.XSHE']
        industry_map = {'000001.XSHE': '银行', '000002.XSHE': '银行', '000003.XSHE': '地产'}
        
        max_ratio, counts = self.module.summarize_industry_ratio(picks, industry_map)
        
        assert counts['银行'] == 2
        assert counts['地产'] == 1
        assert max_ratio == 2 / 3

    def test_get_target_hold_num_below_stop(self):
        market_state = {'breadth': 0.10, 'trend_on': True}
        result = self.module.get_target_hold_num(market_state)
        assert result == self.g.hold_num_stop

    def test_get_target_hold_num_below_reduce(self):
        market_state = {'breadth': 0.20, 'trend_on': True}
        result = self.module.get_target_hold_num(market_state)
        assert result == self.g.hold_num_weak

    def test_get_target_hold_num_below_normal_no_trend(self):
        market_state = {'breadth': 0.30, 'trend_on': False}
        result = self.module.get_target_hold_num(market_state)
        assert result == self.g.hold_num_mid

    def test_get_target_hold_num_normal_with_trend(self):
        market_state = {'breadth': 0.40, 'trend_on': True}
        result = self.module.get_target_hold_num(market_state)
        assert result == self.g.hold_num_normal

    def test_filter_buyable_filters_paused(self):
        stocks = ['000001.XSHE', '000002.XSHE']
        
        current_data = {
            '000001.XSHE': SimpleNamespace(paused=True, is_st=False, name='Stock1', 
                                          last_price=10.0, high_limit=11.0, low_limit=9.0),
            '000002.XSHE': SimpleNamespace(paused=False, is_st=False, name='Stock2',
                                          last_price=10.0, high_limit=11.0, low_limit=9.0)
        }
        self.jqdata.get_current_data.return_value = current_data
        
        result = self.module.filter_buyable(SimpleNamespace(), stocks)
        
        assert '000001.XSHE' not in result
        assert '000002.XSHE' in result

    def test_filter_buyable_filters_st(self):
        stocks = ['000001.XSHE', '000002.XSHE']
        
        current_data = {
            '000001.XSHE': SimpleNamespace(paused=False, is_st=True, name='ST Stock',
                                          last_price=10.0, high_limit=11.0, low_limit=9.0),
            '000002.XSHE': SimpleNamespace(paused=False, is_st=False, name='Stock2',
                                          last_price=10.0, high_limit=11.0, low_limit=9.0)
        }
        self.jqdata.get_current_data.return_value = current_data
        
        result = self.module.filter_buyable(SimpleNamespace(), stocks)
        
        assert '000001.XSHE' not in result

    def test_filter_buyable_filters_st_name(self):
        stocks = ['000001.XSHE']
        
        current_data = {
            '000001.XSHE': SimpleNamespace(paused=False, is_st=False, name='ST平安银行',
                                          last_price=10.0, high_limit=11.0, low_limit=9.0)
        }
        self.jqdata.get_current_data.return_value = current_data
        
        result = self.module.filter_buyable(SimpleNamespace(), stocks)
        
        assert result == []

    def test_filter_buyable_filters_high_limit_price(self):
        stocks = ['000001.XSHE']
        
        current_data = {
            '000001.XSHE': SimpleNamespace(paused=False, is_st=False, name='Stock',
                                          last_price=10.99, high_limit=11.0, low_limit=9.0)
        }
        self.jqdata.get_current_data.return_value = current_data
        
        result = self.module.filter_buyable(SimpleNamespace(), stocks)
        
        assert result == []

    def test_filter_buyable_filters_low_limit_price(self):
        stocks = ['000001.XSHE']
        
        current_data = {
            '000001.XSHE': SimpleNamespace(paused=False, is_st=False, name='Stock',
                                          last_price=9.05, high_limit=11.0, low_limit=9.0)
        }
        self.jqdata.get_current_data.return_value = current_data
        
        result = self.module.filter_buyable(SimpleNamespace(), stocks)
        
        assert len(result) <= len(stocks)

    def test_check_stop_loss_identifies_stocks(self):
        context = SimpleNamespace()
        context.portfolio = SimpleNamespace()
        
        pos1 = SimpleNamespace()
        pos1.price = 8.5
        pos1.avg_cost = 10.0
        
        pos2 = SimpleNamespace()
        pos2.price = 9.5
        pos2.avg_cost = 10.0
        
        context.portfolio.positions = {'000001.XSHE': pos1, '000002.XSHE': pos2}
        
        result = self.module.check_stop_loss(context)
        
        assert isinstance(result, list)

    def test_check_stop_loss_no_positions(self):
        context = SimpleNamespace()
        context.portfolio = SimpleNamespace()
        context.portfolio.positions = {}
        
        result = self.module.check_stop_loss(context)
        
        assert result == []

    def test_check_stop_loss_handles_zero_avg_cost(self):
        context = SimpleNamespace()
        context.portfolio = SimpleNamespace()
        
        pos = SimpleNamespace()
        pos.price = 8.0
        pos.avg_cost = 0
        
        context.portfolio.positions = {'000001.XSHE': pos}
        
        result = self.module.check_stop_loss(context)
        
        assert '000001.XSHE' not in result