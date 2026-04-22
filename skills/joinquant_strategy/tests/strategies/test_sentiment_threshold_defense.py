import pytest
import sys
from unittest.mock import MagicMock, patch, Mock
from types import SimpleNamespace
from datetime import datetime
import pandas as pd

sys.path.insert(0, '/Users/yuping/Downloads/git/stock-website-crawler/strategies/misc_research/joinquant_strategy')


@pytest.fixture
def mock_jqdata():
    mock_module = MagicMock()
    mock_module.set_option = Mock()
    mock_module.set_benchmark = Mock()
    mock_module.log = MagicMock()
    mock_module.log.set_level = Mock()
    mock_module.get_all_securities = Mock()
    mock_module.get_price = Mock()
    mock_module.get_current_data = Mock()
    mock_module.get_fundamentals = Mock()
    mock_module.query = Mock()
    mock_module.valuation = MagicMock()
    mock_module.order_target_value = Mock()
    mock_module.order_value = Mock()
    mock_module.g = SimpleNamespace()
    
    with patch.dict(sys.modules, {'jqdata': mock_module}):
        yield mock_module


@pytest.fixture
def mock_g():
    g = SimpleNamespace()
    g.ps = 10
    g.threshold = 30
    g.rebalance_days = 20
    g.days_counter = 0
    g.zt_count = 0
    g.allow_buy = True
    return g


@pytest.fixture
def mock_context():
    context = SimpleNamespace()
    context.previous_date = datetime(2024, 1, 15)
    context.current_dt = datetime(2024, 1, 16, 9, 30)
    
    portfolio = SimpleNamespace()
    portfolio.available_cash = 1000000
    portfolio.total_value = 1000000
    portfolio.positions = {}
    context.portfolio = portfolio
    return context


class TestSentimentThresholdDefense:
    def test_initialize(self, mock_jqdata, mock_g):
        with patch('jqdata.g', mock_g):
            import sentiment_threshold_defense
            context = SimpleNamespace()
            sentiment_threshold_defense.initialize(context)
            
            mock_jqdata.set_option.assert_called()
            mock_jqdata.set_benchmark.assert_called()
            assert mock_g.ps == 10
            assert mock_g.threshold == 30
            assert mock_g.rebalance_days == 20

    def test_before_trading_start_below_threshold(self, mock_jqdata, mock_g, mock_context):
        with patch('jqdata.g', mock_g):
            import sentiment_threshold_defense
            
            all_stocks = pd.DataFrame({'display_name': ['A']}, index=['000001.XSHE'])
            mock_jqdata.get_all_securities.return_value = all_stocks
            
            price_df = pd.DataFrame({
                'code': ['000001.XSHE'] * 15,
                'close': [10.0] * 15,
                'high_limit': [10.0] * 15,
                'low_limit': [9.0] * 15,
                'paused': [0] * 15
            })
            mock_jqdata.get_price.return_value = price_df
            
            sentiment_threshold_defense.before_trading_start(mock_context)
            
            assert mock_g.zt_count == 15
            assert mock_g.allow_buy == False

    def test_before_trading_start_above_threshold(self, mock_jqdata, mock_g, mock_context):
        with patch('jqdata.g', mock_g):
            import sentiment_threshold_defense
            
            all_stocks = pd.DataFrame({'display_name': ['A']}, index=['000001.XSHE'])
            mock_jqdata.get_all_securities.return_value = all_stocks
            
            price_df = pd.DataFrame({
                'code': ['000001.XSHE'] * 50,
                'close': [10.0] * 50,
                'high_limit': [10.0] * 50,
                'low_limit': [9.0] * 50,
                'paused': [0] * 50
            })
            mock_jqdata.get_price.return_value = price_df
            
            sentiment_threshold_defense.before_trading_start(mock_context)
            
            assert mock_g.zt_count == 50
            assert mock_g.allow_buy == True

    def test_handle_data_rebalance_counter(self, mock_jqdata, mock_g, mock_context):
        with patch('jqdata.g', mock_g):
            import sentiment_threshold_defense
            
            mock_g.days_counter = 10
            mock_g.rebalance_days = 20
            
            data = SimpleNamespace()
            sentiment_threshold_defense.handle_data(mock_context, data)
            
            assert mock_g.days_counter == 11

    def test_handle_data_rebalance_trigger(self, mock_jqdata, mock_g, mock_context):
        with patch('jqdata.g', mock_g):
            import sentiment_threshold_defense
            
            mock_g.days_counter = 20
            mock_g.allow_buy = False
            
            pos = SimpleNamespace()
            mock_context.portfolio.positions = {'000001.XSHE': pos}
            
            data = SimpleNamespace()
            sentiment_threshold_defense.handle_data(mock_context, data)
            
            mock_jqdata.order_target_value.assert_called()
            assert mock_g.days_counter == 0

    def test_handle_data_select_smallcap(self, mock_jqdata, mock_g, mock_context):
        with patch('jqdata.g', mock_g):
            import sentiment_threshold_defense
            
            mock_g.days_counter = 20
            mock_g.allow_buy = True
            
            mock_q = Mock()
            mock_jqdata.query.return_value = mock_q
            mock_jqdata.valuation.code = 'code'
            mock_jqdata.valuation.circulating_market_cap = 'circulating_market_cap'
            mock_jqdata.valuation.pe_ratio = 'pe_ratio'
            mock_jqdata.valuation.pb_ratio = 'pb_ratio'
            
            fundamentals_df = pd.DataFrame({
                'code': ['000001.XSHE', '000002.XSHE'],
                'circulating_market_cap': [20, 40],
                'pe_ratio': [15, 20],
                'pb_ratio': [1.5, 2.0]
            })
            mock_jqdata.get_fundamentals.return_value = fundamentals_df
            
            data = SimpleNamespace()
            sentiment_threshold_defense.handle_data(mock_context, data)
            
            mock_jqdata.order_value.assert_called()
            assert mock_g.days_counter == 0

    def test_handle_data_empty_fundamentals(self, mock_jqdata, mock_g, mock_context):
        with patch('jqdata.g', mock_g):
            import sentiment_threshold_defense
            
            mock_g.days_counter = 20
            mock_g.allow_buy = True
            
            mock_jqdata.get_fundamentals.return_value = pd.DataFrame()
            
            data = SimpleNamespace()
            sentiment_threshold_defense.handle_data(mock_context, data)
            
            mock_jqdata.order_value.assert_not_called()

    def test_threshold_configurable(self, mock_jqdata, mock_g, mock_context):
        with patch('jqdata.g', mock_g):
            import sentiment_threshold_defense
            
            mock_g.threshold = 50
            
            all_stocks = pd.DataFrame({'display_name': ['A']}, index=['000001.XSHE'])
            mock_jqdata.get_all_securities.return_value = all_stocks
            
            price_df = pd.DataFrame({
                'code': ['000001.XSHE'] * 40,
                'close': [10.0] * 40,
                'high_limit': [10.0] * 40,
                'paused': [0] * 40
            })
            mock_jqdata.get_price.return_value = price_df
            
            sentiment_threshold_defense.before_trading_start(mock_context)
            
            assert mock_g.allow_buy == False