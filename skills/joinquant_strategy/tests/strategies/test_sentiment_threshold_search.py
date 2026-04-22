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
    mock_module.order_target_value = Mock()
    mock_module.order_value = Mock()
    mock_module.g = SimpleNamespace()
    
    with patch.dict(sys.modules, {'jqdata': mock_module}):
        yield mock_module


@pytest.fixture
def mock_g():
    g = SimpleNamespace()
    g.ps = 3
    g.threshold = 30
    g.prev_zt = []
    g.zt_count = 0
    g.dt_count = 0
    g.zt_dt_ratio = 0
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


class TestSentimentThresholdSearch:
    def test_initialize(self, mock_jqdata, mock_g):
        with patch('jqdata.g', mock_g):
            import sentiment_threshold_search
            context = SimpleNamespace()
            sentiment_threshold_search.initialize(context)
            
            mock_jqdata.set_option.assert_called()
            mock_jqdata.set_benchmark.assert_called()
            assert mock_g.ps == 3
            assert mock_g.threshold == 30

    def test_before_trading_start_zt_dt_ratio(self, mock_jqdata, mock_g, mock_context):
        with patch('jqdata.g', mock_g):
            import sentiment_threshold_search
            
            all_stocks = pd.DataFrame({'display_name': ['A']}, index=['000001.XSHE'])
            mock_jqdata.get_all_securities.return_value = all_stocks
            
            price_df = pd.DataFrame({
                'code': ['000001.XSHE'] * 50 + ['000002.XSHE'] * 10,
                'close': [10.0] * 50 + [9.0] * 10,
                'high_limit': [10.0] * 60,
                'low_limit': [9.0] * 60,
                'paused': [0] * 60
            })
            mock_jqdata.get_price.return_value = price_df
            
            sentiment_threshold_search.before_trading_start(mock_context)
            
            assert mock_g.zt_count == 50
            assert mock_g.dt_count == 10
            assert mock_g.zt_dt_ratio == 5

    def test_before_trading_start_zero_dt(self, mock_jqdata, mock_g, mock_context):
        with patch('jqdata.g', mock_g):
            import sentiment_threshold_search
            
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
            
            sentiment_threshold_search.before_trading_start(mock_context)
            
            assert mock_g.dt_count == 0
            assert mock_g.zt_dt_ratio == 50

    def test_before_trading_start_allow_buy_threshold(self, mock_jqdata, mock_g, mock_context):
        with patch('jqdata.g', mock_g):
            import sentiment_threshold_search
            
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
            
            sentiment_threshold_search.before_trading_start(mock_context)
            
            assert mock_g.allow_buy == True

    def test_before_trading_start_block_buy(self, mock_jqdata, mock_g, mock_context):
        with patch('jqdata.g', mock_g):
            import sentiment_threshold_search
            
            all_stocks = pd.DataFrame({'display_name': ['A']}, index=['000001.XSHE'])
            mock_jqdata.get_all_securities.return_value = all_stocks
            
            price_df = pd.DataFrame({
                'code': ['000001.XSHE'] * 20,
                'close': [10.0] * 20,
                'high_limit': [10.0] * 20,
                'low_limit': [9.0] * 20,
                'paused': [0] * 20
            })
            mock_jqdata.get_price.return_value = price_df
            
            sentiment_threshold_search.before_trading_start(mock_context)
            
            assert mock_g.allow_buy == False

    def test_handle_data_blocked(self, mock_jqdata, mock_g, mock_context):
        with patch('jqdata.g', mock_g):
            import sentiment_threshold_search
            
            mock_g.allow_buy = False
            
            data = SimpleNamespace()
            result = sentiment_threshold_search.handle_data(mock_context, data)
            
            assert result is None

    def test_handle_data_no_prev_zt(self, mock_jqdata, mock_g, mock_context):
        with patch('jqdata.g', mock_g):
            import sentiment_threshold_search
            
            mock_g.allow_buy = True
            mock_g.prev_zt = []
            
            data = SimpleNamespace()
            result = sentiment_threshold_search.handle_data(mock_context, data)
            
            assert result is None

    def test_handle_data_select_stocks(self, mock_jqdata, mock_g, mock_context):
        with patch('jqdata.g', mock_g):
            import sentiment_threshold_search
            
            mock_g.allow_buy = True
            mock_g.prev_zt = ['000001.XSHE', '000002.XSHE']
            
            mock_current = {
                '000001.XSHE': SimpleNamespace(
                    pre_close=10.0,
                    day_open=9.7,
                    low_limit=9.0,
                    paused=False
                ),
                '000002.XSHE': SimpleNamespace(
                    pre_close=10.0,
                    day_open=9.7,
                    low_limit=9.0,
                    paused=False
                )
            }
            mock_jqdata.get_current_data.return_value = mock_current
            
            data = SimpleNamespace()
            sentiment_threshold_search.handle_data(mock_context, data)
            
            mock_jqdata.order_value.assert_called()

    def test_handle_data_clear_positions(self, mock_jqdata, mock_g, mock_context):
        with patch('jqdata.g', mock_g):
            import sentiment_threshold_search
            
            mock_g.allow_buy = True
            mock_g.prev_zt = ['000001.XSHE']
            
            pos = SimpleNamespace()
            mock_context.portfolio.positions = {'000003.XSHG': pos}
            
            mock_current = {
                '000001.XSHE': SimpleNamespace(
                    pre_close=10.0,
                    day_open=9.7,
                    low_limit=9.0,
                    paused=False
                )
            }
            mock_jqdata.get_current_data.return_value = mock_current
            
            data = SimpleNamespace()
            sentiment_threshold_search.handle_data(mock_context, data)
            
            mock_jqdata.order_target_value.assert_called_with('000003.XSHG', 0)

    def test_threshold_custom_value(self, mock_jqdata, mock_g, mock_context):
        with patch('jqdata.g', mock_g):
            import sentiment_threshold_search
            
            mock_g.threshold = 100
            
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
            
            sentiment_threshold_search.before_trading_start(mock_context)
            
            assert mock_g.allow_buy == False