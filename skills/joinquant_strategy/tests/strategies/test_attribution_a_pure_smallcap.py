import pytest
import sys
from unittest.mock import MagicMock, patch, Mock
from types import SimpleNamespace
from datetime import datetime, timedelta
import pandas as pd

sys.path.insert(0, '/Users/yuping/Downloads/git/stock-website-crawler/strategies/misc_research/joinquant_strategy')


def create_st_df(stocks, is_st_values):
    df = pd.DataFrame({
        stock: [is_st] for stock, is_st in zip(stocks, is_st_values)
    }, index=['2024-01-16'])
    return df


@pytest.fixture
def mock_jqdata():
    mock_module = MagicMock()
    mock_module.set_option = Mock()
    mock_module.set_benchmark = Mock()
    mock_module.log = MagicMock()
    mock_module.log.set_level = Mock()
    mock_module.run_monthly = Mock()
    mock_module.get_all_securities = Mock()
    mock_module.get_price = Mock()
    mock_module.get_current_data = Mock()
    mock_module.get_valuation = Mock()
    mock_module.get_extras = Mock()
    mock_module.get_security_info = Mock()
    mock_module.get_fundamentals = Mock()
    mock_module.order = Mock()
    mock_module.order_target = Mock()
    mock_module.order_target_value = Mock()
    
    mock_query = Mock()
    mock_query.filter.return_value = mock_query
    mock_query.order_by.return_value = mock_query
    mock_query.limit.return_value = mock_query
    mock_module.query = Mock(return_value=mock_query)
    
    mock_valuation = Mock()
    mock_valuation.code = Mock()
    mock_valuation.circulating_market_cap = Mock()
    mock_module.valuation = mock_valuation
    
    mock_module.g = SimpleNamespace()
    
    with patch.dict(sys.modules, {'jqdata': mock_module}):
        yield mock_module


@pytest.fixture
def mock_g():
    g = SimpleNamespace()
    g.trade_count = 0
    g.win_count = 0
    g.pnl_list = []
    return g


@pytest.fixture
def mock_context():
    context = SimpleNamespace()
    context.current_dt = datetime(2024, 1, 16, 9, 35)
    
    portfolio = SimpleNamespace()
    portfolio.available_cash = 1000000
    portfolio.total_value = 1000000
    portfolio.positions = {}
    context.portfolio = portfolio
    return context


@pytest.fixture
def mock_securities():
    return pd.DataFrame({
        'display_name': ['平安银行', '万科A', '浦发银行', '测试股票1', '测试股票2']
    }, index=['000001.XSHE', '000002.XSHE', '600000.XSHG', '600001.XSHG', '600002.XSHG'])


@pytest.fixture
def mock_fundamentals_df():
    return pd.DataFrame({
        'code': ['000001.XSHE', '000002.XSHE', '600000.XSHG'],
        'circulating_market_cap': [5.0, 8.0, 12.0]
    })


class TestAttributionAPureSmallcap:
    def test_initialize(self, mock_jqdata, mock_g):
        with patch('jqdata.g', mock_g):
            import attribution_a_pure_smallcap
            mock_context = SimpleNamespace()
            attribution_a_pure_smallcap.initialize(mock_context)
            
            mock_jqdata.set_option.assert_any_call("use_real_price", True)
            mock_jqdata.set_option.assert_any_call("avoid_future_data", True)
            mock_jqdata.set_benchmark.assert_called_once_with("000300.XSHG")
            mock_jqdata.run_monthly.assert_called_once()

    def test_rebalance_filters_st_stocks(self, mock_jqdata, mock_g, mock_context, mock_securities, mock_fundamentals_df):
        with patch('jqdata.g', mock_g):
            import attribution_a_pure_smallcap
            
            mock_jqdata.get_all_securities.return_value = mock_securities
            
            mock_security_info = SimpleNamespace()
            mock_security_info.start_date = datetime(2020, 1, 1)
            mock_jqdata.get_security_info.return_value = mock_security_info
            
            st_df = create_st_df(['000001.XSHE', '000002.XSHE', '600000.XSHG', '600001.XSHG', '600002.XSHG'], 
                                  [False, False, False, False, False])
            mock_jqdata.get_extras.return_value = st_df
            mock_jqdata.get_fundamentals.return_value = mock_fundamentals_df
            
            attribution_a_pure_smallcap.rebalance(mock_context)
            
            mock_jqdata.get_extras.assert_called_once()

    def test_rebalance_with_empty_fundamentals(self, mock_jqdata, mock_g, mock_context, mock_securities):
        with patch('jqdata.g', mock_g):
            import attribution_a_pure_smallcap
            
            mock_jqdata.get_all_securities.return_value = mock_securities
            
            mock_security_info = SimpleNamespace()
            mock_security_info.start_date = datetime(2020, 1, 1)
            mock_jqdata.get_security_info.return_value = mock_security_info
            
            st_df = create_st_df(['000001.XSHE', '000002.XSHE', '600000.XSHG', '600001.XSHG', '600002.XSHG'], 
                                  [False, False, False, False, False])
            mock_jqdata.get_extras.return_value = st_df
            mock_jqdata.get_fundamentals.return_value = pd.DataFrame()
            
            attribution_a_pure_smallcap.rebalance(mock_context)
            
            mock_jqdata.order_target.assert_not_called()
            mock_jqdata.order_target_value.assert_not_called()

    def test_rebalance_sells_positions_not_in_target(self, mock_jqdata, mock_g, mock_context, mock_securities, mock_fundamentals_df):
        with patch('jqdata.g', mock_g):
            import attribution_a_pure_smallcap
            
            mock_jqdata.get_all_securities.return_value = mock_securities
            
            mock_security_info = SimpleNamespace()
            mock_security_info.start_date = datetime(2020, 1, 1)
            mock_jqdata.get_security_info.return_value = mock_security_info
            
            st_df = create_st_df(['000001.XSHE', '000002.XSHE', '600000.XSHG', '600001.XSHG', '600002.XSHG'], 
                                  [False, False, False, False, False])
            mock_jqdata.get_extras.return_value = st_df
            mock_jqdata.get_fundamentals.return_value = mock_fundamentals_df
            
            pos = SimpleNamespace()
            pos.closeable_amount = 1000
            mock_context.portfolio.positions = {'999999.XSHE': pos}
            
            attribution_a_pure_smallcap.rebalance(mock_context)
            
            mock_jqdata.order_target.assert_called()

    def test_rebalance_buys_target_stocks(self, mock_jqdata, mock_g, mock_context, mock_securities, mock_fundamentals_df):
        with patch('jqdata.g', mock_g):
            import attribution_a_pure_smallcap
            
            mock_jqdata.get_all_securities.return_value = mock_securities
            
            mock_security_info = SimpleNamespace()
            mock_security_info.start_date = datetime(2020, 1, 1)
            mock_jqdata.get_security_info.return_value = mock_security_info
            
            st_df = create_st_df(['000001.XSHE', '000002.XSHE', '600000.XSHG', '600001.XSHG', '600002.XSHG'], 
                                  [False, False, False, False, False])
            mock_jqdata.get_extras.return_value = st_df
            mock_jqdata.get_fundamentals.return_value = mock_fundamentals_df
            
            attribution_a_pure_smallcap.rebalance(mock_context)
            
            mock_jqdata.order_target_value.assert_called()

    def test_rebalance_filters_new_stocks(self, mock_jqdata, mock_g, mock_context, mock_securities, mock_fundamentals_df):
        with patch('jqdata.g', mock_g):
            import attribution_a_pure_smallcap
            
            mock_jqdata.get_all_securities.return_value = mock_securities
            
            mock_security_info_old = SimpleNamespace()
            mock_security_info_old.start_date = datetime(2020, 1, 1)
            
            mock_security_info_new = SimpleNamespace()
            mock_security_info_new.start_date = datetime(2024, 1, 1)
            
            def get_security_info_side_effect(code):
                return mock_security_info_new if code == '600002.XSHG' else mock_security_info_old
            
            mock_jqdata.get_security_info.side_effect = get_security_info_side_effect
            
            st_df = create_st_df(['000001.XSHE', '000002.XSHE', '600000.XSHG', '600001.XSHG'], 
                                  [False, False, False, False])
            mock_jqdata.get_extras.return_value = st_df
            mock_jqdata.get_fundamentals.return_value = mock_fundamentals_df
            
            attribution_a_pure_smallcap.rebalance(mock_context)
            
            assert mock_jqdata.get_security_info.called

    def test_rebalance_filters_bse_stocks(self, mock_jqdata, mock_g, mock_context, mock_fundamentals_df):
        with patch('jqdata.g', mock_g):
            import attribution_a_pure_smallcap
            
            bse_securities = pd.DataFrame({
                'display_name': ['BSE股票']
            }, index=['430001.XSHE', '830001.XSHE', '300001.XSHE', '688001.XSHG'])
            mock_jqdata.get_all_securities.return_value = bse_securities
            
            mock_security_info = SimpleNamespace()
            mock_security_info.start_date = datetime(2020, 1, 1)
            mock_jqdata.get_security_info.return_value = mock_security_info
            
            attribution_a_pure_smallcap.rebalance(mock_context)
            
            mock_jqdata.get_extras.assert_not_called()

    def test_rebalance_calculates_target_count(self, mock_jqdata, mock_g, mock_context, mock_securities):
        with patch('jqdata.g', mock_g):
            import attribution_a_pure_smallcap
            
            mock_jqdata.get_all_securities.return_value = mock_securities
            
            mock_security_info = SimpleNamespace()
            mock_security_info.start_date = datetime(2020, 1, 1)
            mock_jqdata.get_security_info.return_value = mock_security_info
            
            st_df = create_st_df(['000001.XSHE', '000002.XSHE', '600000.XSHG', '600001.XSHG', '600002.XSHG'], 
                                  [False, False, False, False, False])
            mock_jqdata.get_extras.return_value = st_df
            
            fundamentals_with_many = pd.DataFrame({
                'code': [f'00000{i}.XSHE' for i in range(50)],
                'circulating_market_cap': [i * 1.0 for i in range(50)]
            })
            mock_jqdata.get_fundamentals.return_value = fundamentals_with_many
            
            attribution_a_pure_smallcap.rebalance(mock_context)
            
            mock_jqdata.order_target_value.assert_called()

    def test_rebalance_with_single_stock(self, mock_jqdata, mock_g, mock_context, mock_securities):
        with patch('jqdata.g', mock_g):
            import attribution_a_pure_smallcap
            
            mock_jqdata.get_all_securities.return_value = mock_securities
            
            mock_security_info = SimpleNamespace()
            mock_security_info.start_date = datetime(2020, 1, 1)
            mock_jqdata.get_security_info.return_value = mock_security_info
            
            st_df = create_st_df(['000001.XSHE', '000002.XSHE', '600000.XSHG', '600001.XSHG', '600002.XSHG'], 
                                  [False, False, False, False, False])
            mock_jqdata.get_extras.return_value = st_df
            
            fundamentals_single = pd.DataFrame({
                'code': ['000001.XSHE'],
                'circulating_market_cap': [5.0]
            })
            mock_jqdata.get_fundamentals.return_value = fundamentals_single
            
            attribution_a_pure_smallcap.rebalance(mock_context)
            
            mock_jqdata.order_target_value.assert_called()

    def test_rebalance_filters_st_stocks_true(self, mock_jqdata, mock_g, mock_context, mock_securities, mock_fundamentals_df):
        with patch('jqdata.g', mock_g):
            import attribution_a_pure_smallcap
            
            mock_jqdata.get_all_securities.return_value = mock_securities
            
            mock_security_info = SimpleNamespace()
            mock_security_info.start_date = datetime(2020, 1, 1)
            mock_jqdata.get_security_info.return_value = mock_security_info
            
            st_df = create_st_df(['000001.XSHE', '000002.XSHE', '600000.XSHG', '600001.XSHG', '600002.XSHG'], 
                                  [False, True, False, False, False])
            mock_jqdata.get_extras.return_value = st_df
            mock_jqdata.get_fundamentals.return_value = mock_fundamentals_df
            
            attribution_a_pure_smallcap.rebalance(mock_context)
            
            mock_jqdata.get_fundamentals.assert_called()