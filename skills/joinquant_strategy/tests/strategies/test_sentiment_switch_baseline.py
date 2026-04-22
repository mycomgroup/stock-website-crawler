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
    g.target = []
    g.prev_zt = []
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
def mock_zt_price_data():
    return pd.DataFrame({
        'code': ['000001.XSHE', '000002.XSHE', '600000.XSHG'],
        'close': [10.0, 10.0, 10.0],
        'high_limit': [10.0, 10.0, 10.0],
        'paused': [0, 0, 0]
    })


@pytest.fixture
def mock_current_data():
    def _create(stocks, open_pct=-0.03):
        data = {}
        for stock in stocks:
            stock_data = SimpleNamespace()
            stock_data.pre_close = 10.0
            stock_data.day_open = 10.0 * (1 + open_pct)
            stock_data.low_limit = 9.0
            stock_data.paused = False
            data[stock] = stock_data
        return data
    return _create


class TestSentimentSwitchBaseline:
    def test_initialize(self, mock_jqdata, mock_g):
        with patch('jqdata.g', mock_g):
            import sentiment_switch_baseline
            context = SimpleNamespace()
            sentiment_switch_baseline.initialize(context)
            
            mock_jqdata.set_option.assert_called()
            assert mock_g.ps == 3
            assert mock_g.target == []

    def test_before_trading_no_zt(self, mock_jqdata, mock_g, mock_context, mock_zt_price_data):
        with patch('jqdata.g', mock_g):
            import sentiment_switch_baseline
            
            all_stocks = pd.DataFrame({'display_name': ['A', 'B']}, index=['000001.XSHE', '000002.XSHE'])
            mock_jqdata.get_all_securities.return_value = all_stocks
            
            price_data = pd.DataFrame({
                'code': ['000001.XSHE'],
                'close': [9.0],
                'high_limit': [10.0],
                'paused': [0]
            })
            mock_jqdata.get_price.return_value = price_data
            
            sentiment_switch_baseline.before_trading(mock_context)
            
            assert mock_g.prev_zt == []
            assert mock_g.target == []

    def test_before_trading_with_zt(self, mock_jqdata, mock_g, mock_context, mock_zt_price_data):
        with patch('jqdata.g', mock_g):
            import sentiment_switch_baseline
            
            all_stocks = pd.DataFrame({'display_name': ['A', 'B']}, index=['000001.XSHE', '000002.XSHE'])
            mock_jqdata.get_all_securities.return_value = all_stocks
            mock_jqdata.get_price.return_value = mock_zt_price_data
            
            sentiment_switch_baseline.before_trading(mock_context)
            
            assert len(mock_g.prev_zt) == 3

    def test_handle_data_no_prev_zt(self, mock_jqdata, mock_g, mock_context):
        with patch('jqdata.g', mock_g):
            import sentiment_switch_baseline
            
            mock_g.prev_zt = []
            data = SimpleNamespace()
            
            result = sentiment_switch_baseline.handle_data(mock_context, data)
            
            assert result is None

    def test_handle_data_clear_positions(self, mock_jqdata, mock_g, mock_context):
        with patch('jqdata.g', mock_g):
            import sentiment_switch_baseline
            
            mock_g.prev_zt = ['000001.XSHE']
            
            pos = SimpleNamespace()
            pos.closeable_amount = 100
            mock_context.portfolio.positions = {'000001.XSHE': pos}
            
            mock_current = {'000001.XSHE': SimpleNamespace(
                pre_close=10.0,
                day_open=9.7,
                low_limit=9.0,
                paused=False
            )}
            mock_jqdata.get_current_data.return_value = mock_current
            
            data = SimpleNamespace()
            sentiment_switch_baseline.handle_data(mock_context, data)
            
            mock_jqdata.order_target_value.assert_called()

    def test_handle_data_select_low_open(self, mock_jqdata, mock_g, mock_context, mock_current_data):
        with patch('jqdata.g', mock_g):
            import sentiment_switch_baseline
            
            mock_g.prev_zt = ['000001.XSHE', '000002.XSHE', '600000.XSHG']
            mock_g.ps = 2
            
            mock_context.portfolio.positions = {}
            
            mock_current = mock_current_data(mock_g.prev_zt, open_pct=-0.03)
            mock_jqdata.get_current_data.return_value = mock_current
            
            data = SimpleNamespace()
            sentiment_switch_baseline.handle_data(mock_context, data)
            
            mock_jqdata.order_value.assert_called()
            assert len(mock_g.target) <= mock_g.ps

    def test_handle_data_filter_high_open(self, mock_jqdata, mock_g, mock_context, mock_current_data):
        with patch('jqdata.g', mock_g):
            import sentiment_switch_baseline
            
            mock_g.prev_zt = ['000001.XSHE']
            mock_context.portfolio.positions = {}
            
            mock_current = mock_current_data(mock_g.prev_zt, open_pct=0.05)
            mock_jqdata.get_current_data.return_value = mock_current
            
            data = SimpleNamespace()
            sentiment_switch_baseline.handle_data(mock_context, data)
            
            assert mock_g.target == []

    def test_handle_data_filter_limit_down(self, mock_jqdata, mock_g, mock_context):
        with patch('jqdata.g', mock_g):
            import sentiment_switch_baseline
            
            mock_g.prev_zt = ['000001.XSHE']
            mock_context.portfolio.positions = {}
            
            mock_current = {
                '000001.XSHE': SimpleNamespace(
                    pre_close=10.0,
                    day_open=9.0,
                    low_limit=9.0,
                    paused=False
                )
            }
            mock_jqdata.get_current_data.return_value = mock_current
            
            data = SimpleNamespace()
            sentiment_switch_baseline.handle_data(mock_context, data)
            
            assert mock_g.target == []

    def test_stock_filter_bjb(self, mock_jqdata, mock_g, mock_context):
        with patch('jqdata.g', mock_g):
            import sentiment_switch_baseline
            
            all_stocks = pd.DataFrame({'display_name': ['A']}, index=['830001.XSHE'])
            mock_jqdata.get_all_securities.return_value = all_stocks
            
            price_df = pd.DataFrame({
                'code': ['830001.XSHE'],
                'close': [10.0],
                'high_limit': [10.0],
                'paused': [0]
            })
            mock_jqdata.get_price.return_value = price_df
            
            sentiment_switch_baseline.before_trading(mock_context)
            
            assert '830001.XSHE' not in mock_g.prev_zt

    def test_stock_filter_kcb(self, mock_jqdata, mock_g, mock_context):
        with patch('jqdata.g', mock_g):
            import sentiment_switch_baseline
            
            all_stocks = pd.DataFrame({'display_name': ['A']}, index=['688001.XSHG'])
            mock_jqdata.get_all_securities.return_value = all_stocks
            
            price_df = pd.DataFrame({
                'code': ['688001.XSHG'],
                'close': [10.0],
                'high_limit': [10.0],
                'paused': [0]
            })
            mock_jqdata.get_price.return_value = price_df
            
            sentiment_switch_baseline.before_trading(mock_context)
            
            assert '688001.XSHG' not in mock_g.prev_zt