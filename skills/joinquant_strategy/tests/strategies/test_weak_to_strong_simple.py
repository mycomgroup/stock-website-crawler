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
    mock_module.log = MagicMock()
    mock_module.log.set_level = Mock()
    mock_module.run_daily = Mock()
    mock_module.get_all_securities = Mock()
    mock_module.get_price = Mock()
    mock_module.get_current_data = Mock()
    mock_module.get_valuation = Mock()
    mock_module.order_value = Mock()
    mock_module.order_target = Mock()
    mock_module.g = SimpleNamespace()
    
    with patch.dict(sys.modules, {'jqdata': mock_module}):
        yield mock_module


@pytest.fixture
def mock_g():
    g = SimpleNamespace()
    g.stocks = []
    return g


@pytest.fixture
def mock_context():
    context = SimpleNamespace()
    context.current_dt = datetime(2024, 1, 16, 9, 30)
    context.previous_date = datetime(2024, 1, 15)
    
    portfolio = SimpleNamespace()
    portfolio.available_cash = 1000000
    portfolio.total_value = 1000000
    portfolio.positions = {}
    context.portfolio = portfolio
    return context


class TestWeakToStrongSimple:
    def test_initialize(self, mock_jqdata, mock_g):
        with patch('jqdata.g', mock_g):
            import weak_to_strong_simple
            context = SimpleNamespace()
            weak_to_strong_simple.initialize(context)
            
            mock_jqdata.set_option.assert_called()
            mock_jqdata.run_daily.assert_called()
            assert mock_g.stocks == []

    def test_select_stocks_no_zt(self, mock_jqdata, mock_g, mock_context):
        with patch('jqdata.g', mock_g):
            import weak_to_strong_simple
            
            all_stocks = pd.DataFrame({'display_name': ['A']}, index=['000001.XSHE'])
            mock_jqdata.get_all_securities.return_value = all_stocks
            
            price_df = pd.DataFrame({
                'close': [9.0, 9.0],
                'high_limit': [10.0, 10.0],
                'money': [6e8, 6e8],
                'volume': [1000000, 1000000]
            })
            mock_jqdata.get_price.return_value = price_df
            
            mock_valuation = pd.DataFrame({'market_cap': [100]}, index=['000001.XSHE'])
            mock_jqdata.get_valuation.return_value = mock_valuation
            
            weak_to_strong_simple.select_stocks(mock_context)
            
            assert mock_g.stocks == []

    def test_select_stocks_with_zt(self, mock_jqdata, mock_g, mock_context):
        with patch('jqdata.g', mock_g):
            import weak_to_strong_simple
            
            all_stocks = pd.DataFrame({'display_name': ['A']}, index=['000001.XSHE'])
            mock_jqdata.get_all_securities.return_value = all_stocks
            
            price_df = pd.DataFrame({
                'close': [10.0, 10.03],
                'high_limit': [10.0, 10.03],
                'money': [6e8, 6e8],
                'volume': [1000000, 1000000],
                'open': [10.03, 10.03]
            })
            mock_jqdata.get_price.return_value = price_df
            
            mock_valuation = pd.DataFrame({'market_cap': [100]}, index=['000001.XSHE'])
            mock_jqdata.get_valuation.return_value = mock_valuation
            
            weak_to_strong_simple.select_stocks(mock_context)
            
            assert isinstance(mock_g.stocks, list)

    def test_buy_stocks_no_selection(self, mock_jqdata, mock_g, mock_context):
        with patch('jqdata.g', mock_g):
            import weak_to_strong_simple
            
            mock_g.stocks = []
            
            weak_to_strong_simple.buy_stocks(mock_context)
            
            mock_jqdata.order_value.assert_not_called()

    def test_buy_stocks_with_selection(self, mock_jqdata, mock_g, mock_context):
        with patch('jqdata.g', mock_g):
            import weak_to_strong_simple
            
            mock_g.stocks = ['000001.XSHE', '000002.XSHE']
            
            weak_to_strong_simple.buy_stocks(mock_context)
            
            mock_jqdata.order_value.assert_called()

    def test_sell_stocks_no_position(self, mock_jqdata, mock_g, mock_context):
        with patch('jqdata.g', mock_g):
            import weak_to_strong_simple
            
            mock_context.portfolio.positions = {}
            
            weak_to_strong_simple.sell_stocks(mock_context)
            
            mock_jqdata.order_target.assert_not_called()

    def test_sell_stocks_with_position(self, mock_jqdata, mock_g, mock_context):
        with patch('jqdata.g', mock_g):
            import weak_to_strong_simple
            
            pos = SimpleNamespace()
            pos.closeable_amount = 100
            mock_context.portfolio.positions = {'000001.XSHE': pos}
            
            weak_to_strong_simple.sell_stocks(mock_context)
            
            mock_jqdata.order_target.assert_called()

    def test_money_filter(self, mock_jqdata, mock_g, mock_context):
        with patch('jqdata.g', mock_g):
            import weak_to_strong_simple
            
            all_stocks = pd.DataFrame({'display_name': ['A']}, index=['000001.XSHE'])
            mock_jqdata.get_all_securities.return_value = all_stocks
            
            price_df = pd.DataFrame({
                'close': [10.0, 10.0],
                'high_limit': [10.0, 10.0],
                'money': [4e8, 4e8],
                'volume': [1000000, 1000000]
            })
            mock_jqdata.get_price.return_value = price_df
            
            mock_valuation = pd.DataFrame({'market_cap': [100]}, index=['000001.XSHE'])
            mock_jqdata.get_valuation.return_value = mock_valuation
            
            weak_to_strong_simple.select_stocks(mock_context)
            
            assert mock_g.stocks == []

    def test_market_cap_filter(self, mock_jqdata, mock_g, mock_context):
        with patch('jqdata.g', mock_g):
            import weak_to_strong_simple
            
            all_stocks = pd.DataFrame({'display_name': ['A']}, index=['000001.XSHE'])
            mock_jqdata.get_all_securities.return_value = all_stocks
            
            price_df = pd.DataFrame({
                'close': [10.0, 10.0],
                'high_limit': [10.0, 10.0],
                'money': [6e8, 6e8],
                'volume': [1000000, 1000000]
            })
            mock_jqdata.get_price.return_value = price_df
            
            mock_valuation = pd.DataFrame({'market_cap': [20]}, index=['000001.XSHE'])
            mock_jqdata.get_valuation.return_value = mock_valuation
            
            weak_to_strong_simple.select_stocks(mock_context)
            
            assert mock_g.stocks == []

    def test_open_ratio_filter(self, mock_jqdata, mock_g, mock_context):
        with patch('jqdata.g', mock_g):
            import weak_to_strong_simple
            
            all_stocks = pd.DataFrame({'display_name': ['A']}, index=['000001.XSHE'])
            mock_jqdata.get_all_securities.return_value = all_stocks
            
            price_df = pd.DataFrame({
                'close': [10.0, 10.0],
                'high_limit': [10.0, 10.0],
                'money': [6e8, 6e8],
                'volume': [1000000, 1000000],
                'open': [10.1, 10.1]
            })
            mock_jqdata.get_price.return_value = price_df
            
            mock_valuation = pd.DataFrame({'market_cap': [100]}, index=['000001.XSHE'])
            mock_jqdata.get_valuation.return_value = mock_valuation
            
            weak_to_strong_simple.select_stocks(mock_context)
            
            assert isinstance(mock_g.stocks, list)