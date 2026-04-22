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
    mock_module.log.info = Mock()
    mock_module.run_daily = Mock()
    mock_module.get_all_securities = Mock()
    mock_module.get_price = Mock()
    mock_module.get_current_data = Mock()
    mock_module.order_value = Mock()
    mock_module.order_target_value = Mock()
    mock_module.g = SimpleNamespace()
    
    with patch.dict(sys.modules, {'jqdata': mock_module}):
        yield mock_module


@pytest.fixture
def mock_g():
    g = SimpleNamespace()
    g.ps = 3
    g.use_position = True
    g.prev_zt = []
    g.zt_count = 0
    g.dt_count = 0
    g.zt_dt_ratio = 0
    g.max_lianban = 0
    g.position_ratio = 1.0
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


class TestSentimentSwitchPosition:
    def test_initialize(self, mock_jqdata, mock_g):
        with patch('jqdata.g', mock_g):
            import sentiment_switch_position
            context = SimpleNamespace()
            sentiment_switch_position.initialize(context)
            
            mock_jqdata.set_option.assert_called()
            assert mock_g.ps == 3
            assert mock_g.use_position == True
            mock_jqdata.run_daily.assert_called()

    def test_get_stock_list(self, mock_jqdata, mock_g, mock_context):
        with patch('jqdata.g', mock_g):
            import sentiment_switch_position
            
            all_stocks = pd.DataFrame({'display_name': ['A']}, index=['000001.XSHE'])
            mock_jqdata.get_all_securities.return_value = all_stocks
            
            price_df = pd.DataFrame({
                'code': ['000001.XSHE'],
                'close': [10.0],
                'high_limit': [10.0],
                'low_limit': [9.0],
                'paused': [0]
            })
            mock_jqdata.get_price.return_value = price_df
            
            sentiment_switch_position.get_stock_list(mock_context)
            
            assert mock_g.prev_zt == ['000001.XSHE']
            assert mock_g.zt_count == 1

    def test_calc_sentiment_high_position(self, mock_jqdata, mock_g, mock_context):
        with patch('jqdata.g', mock_g):
            import sentiment_switch_position
            
            mock_g.prev_zt = ['000001.XSHE']
            mock_g.zt_count = 50
            
            price_df = pd.DataFrame({
                'code': ['000001.XSHE'] * 5,
                'close': [10.0] * 5,
                'high_limit': [10.0] * 5
            })
            mock_jqdata.get_price.return_value = price_df
            
            sentiment_switch_position.calc_sentiment(mock_context)
            
            assert mock_g.position_ratio == 0.3

    def test_calc_sentiment_normal_position(self, mock_jqdata, mock_g, mock_context):
        with patch('jqdata.g', mock_g):
            import sentiment_switch_position
            
            mock_g.prev_zt = ['000001.XSHE']
            mock_g.zt_count = 30
            
            price_df = pd.DataFrame({
                'code': ['000001.XSHE'] * 3,
                'close': [10.0] * 3,
                'high_limit': [10.0] * 3
            })
            mock_jqdata.get_price.return_value = price_df
            
            sentiment_switch_position.calc_sentiment(mock_context)
            
            assert mock_g.position_ratio == 1.0

    def test_calc_sentiment_medium_position(self, mock_jqdata, mock_g, mock_context):
        with patch('jqdata.g', mock_g):
            import sentiment_switch_position
            
            mock_g.prev_zt = ['000001.XSHE']
            mock_g.zt_count = 20
            
            price_df = pd.DataFrame({
                'code': ['000001.XSHE'] * 2,
                'close': [10.0] * 2,
                'high_limit': [10.0] * 2
            })
            mock_jqdata.get_price.return_value = price_df
            
            sentiment_switch_position.calc_sentiment(mock_context)
            
            assert mock_g.position_ratio == 0.5

    def test_calc_sentiment_zero_position(self, mock_jqdata, mock_g, mock_context):
        with patch('jqdata.g', mock_g):
            import sentiment_switch_position
            
            mock_g.prev_zt = ['000001.XSHE']
            mock_g.zt_count = 10
            
            price_df = pd.DataFrame({
                'code': ['000001.XSHE'],
                'close': [10.0],
                'high_limit': [10.0]
            })
            mock_jqdata.get_price.return_value = price_df
            
            sentiment_switch_position.calc_sentiment(mock_context)
            
            assert mock_g.position_ratio == 0.0

    def test_buy_zero_position_ratio(self, mock_jqdata, mock_g, mock_context):
        with patch('jqdata.g', mock_g):
            import sentiment_switch_position
            
            mock_g.position_ratio = 0
            
            result = sentiment_switch_position.buy(mock_context)
            
            assert result is None

    def test_buy_with_position(self, mock_jqdata, mock_g, mock_context):
        with patch('jqdata.g', mock_g):
            import sentiment_switch_position
            
            mock_g.prev_zt = ['000001.XSHE']
            mock_g.position_ratio = 0.5
            
            mock_current = {
                '000001.XSHE': SimpleNamespace(
                    pre_close=10.0,
                    day_open=9.7,
                    low_limit=9.0,
                    paused=False
                )
            }
            mock_jqdata.get_current_data.return_value = mock_current
            
            sentiment_switch_position.buy(mock_context)
            
            mock_jqdata.order_value.assert_called()

    def test_sell_all_positions(self, mock_jqdata, mock_g, mock_context):
        with patch('jqdata.g', mock_g):
            import sentiment_switch_position
            
            pos = SimpleNamespace()
            pos.closeable_amount = 100
            mock_context.portfolio.positions = {'000001.XSHE': pos}
            
            mock_current = {
                '000001.XSHE': SimpleNamespace(
                    last_price=10.0,
                    paused=False
                )
            }
            mock_jqdata.get_current_data.return_value = mock_current
            
            sentiment_switch_position.sell(mock_context)
            
            mock_jqdata.order_target_value.assert_called_with('000001.XSHE', 0)

    def test_position_disabled(self, mock_jqdata, mock_g, mock_context):
        with patch('jqdata.g', mock_g):
            import sentiment_switch_position
            
            mock_g.use_position = False
            mock_g.zt_count = 10
            
            sentiment_switch_position.calc_sentiment(mock_context)
            
            assert mock_g.position_ratio == 1.0