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
    g.use_switch = True
    g.prev_zt = []
    g.zt_count = 0
    g.dt_count = 0
    g.zt_dt_ratio = 0
    g.max_lianban = 0
    g.allow_buy = False
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


@pytest.fixture
def mock_price_data_with_zt_dt():
    return pd.DataFrame({
        'code': ['000001.XSHE', '000002.XSHE', '600000.XSHG', '600001.XSHG'],
        'close': [10.0, 10.0, 9.0, 8.0],
        'high_limit': [10.0, 10.0, 10.0, 10.0],
        'low_limit': [9.0, 9.0, 9.0, 9.0],
        'paused': [0, 0, 0, 0]
    })


@pytest.fixture
def mock_lianban_data():
    return pd.DataFrame({
        'code': ['000001.XSHE'] * 3,
        'close': [10.0, 10.0, 10.0],
        'high_limit': [10.0, 10.0, 10.0]
    })


class TestSentimentSwitchHard:
    def test_initialize(self, mock_jqdata, mock_g):
        with patch('jqdata.g', mock_g):
            import sentiment_switch_hard
            context = SimpleNamespace()
            sentiment_switch_hard.initialize(context)
            
            mock_jqdata.set_option.assert_called()
            mock_jqdata.set_benchmark.assert_called_with("000300.XSHG")
            assert mock_g.ps == 3
            assert mock_g.use_switch == True

    def test_before_trading_start_calculate_zt_dt(self, mock_jqdata, mock_g, mock_context, mock_price_data_with_zt_dt):
        with patch('jqdata.g', mock_g):
            import sentiment_switch_hard
            
            all_stocks = pd.DataFrame({'display_name': ['A']}, index=['000001.XSHE'])
            mock_jqdata.get_all_securities.return_value = all_stocks
            mock_jqdata.get_price.return_value = mock_price_data_with_zt_dt
            
            sentiment_switch_hard.before_trading_start(mock_context)
            
            assert mock_g.zt_count == 2
            assert mock_g.dt_count >= 1

    def test_before_trading_allow_buy_conditions_met(self, mock_jqdata, mock_g, mock_context, mock_lianban_data):
        with patch('jqdata.g', mock_g):
            import sentiment_switch_hard
            
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
            
            sentiment_switch_hard.before_trading_start(mock_context)
            
            assert mock_g.allow_buy == True

    def test_before_trading_block_buy_low_lianban(self, mock_jqdata, mock_g, mock_context):
        with patch('jqdata.g', mock_g):
            import sentiment_switch_hard
            
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
            
            sentiment_switch_hard.before_trading_start(mock_context)
            
            assert mock_g.max_lianban == 1
            assert mock_g.allow_buy == False

    def test_before_trading_switch_disabled(self, mock_jqdata, mock_g, mock_context):
        with patch('jqdata.g', mock_g):
            import sentiment_switch_hard
            
            mock_g.use_switch = False
            
            all_stocks = pd.DataFrame({'display_name': ['A']}, index=['000001.XSHE'])
            mock_jqdata.get_all_securities.return_value = all_stocks
            
            price_df = pd.DataFrame({
                'code': ['000001.XSHE'],
                'close': [9.0],
                'high_limit': [10.0],
                'low_limit': [9.0],
                'paused': [0]
            })
            mock_jqdata.get_price.return_value = price_df
            
            sentiment_switch_hard.before_trading_start(mock_context)
            
            assert mock_g.allow_buy == True

    def test_handle_data_blocked(self, mock_jqdata, mock_g, mock_context):
        with patch('jqdata.g', mock_g):
            import sentiment_switch_hard
            
            mock_g.allow_buy = False
            data = SimpleNamespace()
            
            result = sentiment_switch_hard.handle_data(mock_context, data)
            
            assert result is None

    def test_handle_data_no_prev_zt(self, mock_jqdata, mock_g, mock_context):
        with patch('jqdata.g', mock_g):
            import sentiment_switch_hard
            
            mock_g.allow_buy = True
            mock_g.prev_zt = []
            data = SimpleNamespace()
            
            result = sentiment_switch_hard.handle_data(mock_context, data)
            
            assert result is None

    def test_handle_data_select_stocks(self, mock_jqdata, mock_g, mock_context):
        with patch('jqdata.g', mock_g):
            import sentiment_switch_hard
            
            mock_g.allow_buy = True
            mock_g.prev_zt = ['000001.XSHE', '000002.XSHE']
            mock_g.ps = 2
            
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
            sentiment_switch_hard.handle_data(mock_context, data)
            
            mock_jqdata.order_value.assert_called()

    def test_handle_data_clear_positions(self, mock_jqdata, mock_g, mock_context):
        with patch('jqdata.g', mock_g):
            import sentiment_switch_hard
            
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
            sentiment_switch_hard.handle_data(mock_context, data)
            
            mock_jqdata.order_target_value.assert_called_with('000003.XSHG', 0)

    def test_open_ratio_filter(self, mock_jqdata, mock_g, mock_context):
        with patch('jqdata.g', mock_g):
            import sentiment_switch_hard
            
            mock_g.allow_buy = True
            mock_g.prev_zt = ['000001.XSHE']
            
            mock_current = {
                '000001.XSHE': SimpleNamespace(
                    pre_close=10.0,
                    day_open=10.5,
                    low_limit=9.0,
                    paused=False
                )
            }
            mock_jqdata.get_current_data.return_value = mock_current
            
            data = SimpleNamespace()
            sentiment_switch_hard.handle_data(mock_context, data)
            
            mock_jqdata.order_value.assert_not_called()