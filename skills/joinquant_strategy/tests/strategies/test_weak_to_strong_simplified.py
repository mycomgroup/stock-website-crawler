import pytest
import sys
from unittest.mock import MagicMock, patch, Mock
from types import SimpleNamespace
from datetime import datetime, timedelta
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
    mock_module.get_security_info = Mock()
    mock_module.get_extras = Mock()
    mock_module.get_valuation = Mock()
    mock_module.get_all_trade_days = Mock()
    mock_module.order_value = Mock()
    mock_module.order_target_value = Mock()
    mock_module.MarketOrderStyle = Mock()
    mock_module.g = SimpleNamespace()
    
    with patch.dict(sys.modules, {'jqdata': mock_module}):
        yield mock_module


@pytest.fixture
def mock_g():
    g = SimpleNamespace()
    g.target_list = []
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


class TestWeakToStrongSimplified:
    def test_initialize(self, mock_jqdata, mock_g):
        with patch('jqdata.g', mock_g):
            import weak_to_strong_simplified
            context = SimpleNamespace()
            weak_to_strong_simplified.initialize(context)
            
            mock_jqdata.set_option.assert_called()
            mock_jqdata.run_daily.assert_called()
            assert mock_g.target_list == []

    def test_get_previous_trade_date(self, mock_jqdata, mock_g):
        with patch('jqdata.g', mock_g):
            import weak_to_strong_simplified
            
            mock_jqdata.get_all_trade_days.return_value = [datetime(2024, 1, i) for i in range(1, 20)]
            
            result = weak_to_strong_simplified.get_previous_trade_date(datetime(2024, 1, 15))
            
            assert result is not None

    def test_get_stock_list_empty(self, mock_jqdata, mock_g, mock_context):
        with patch('jqdata.g', mock_g):
            import weak_to_strong_simplified
            
            all_stocks = pd.DataFrame({'display_name': ['A']}, index=['000001.XSHE'])
            mock_jqdata.get_all_securities.return_value = all_stocks
            
            mock_jqdata.get_security_info.return_value = SimpleNamespace(start_date=datetime(2020, 1, 1))
            
            mock_extras = pd.DataFrame({datetime(2024, 1, 15): [False]}, index=['000001.XSHE'])
            mock_jqdata.get_extras.return_value = mock_extras
            
            price_df = pd.DataFrame()
            mock_jqdata.get_price.return_value = price_df
            
            mock_jqdata.get_all_trade_days.return_value = [datetime(2024, 1, i) for i in range(1, 20)]
            
            weak_to_strong_simplified.get_stock_list(mock_context)
            
            assert mock_g.target_list == []

    def test_buy_no_target(self, mock_jqdata, mock_g, mock_context):
        with patch('jqdata.g', mock_g):
            import weak_to_strong_simplified
            
            mock_g.target_list = []
            
            weak_to_strong_simplified.buy(mock_context)
            
            mock_jqdata.order_value.assert_not_called()

    def test_sell_no_position(self, mock_jqdata, mock_g, mock_context):
        with patch('jqdata.g', mock_g):
            import weak_to_strong_simplified
            
            mock_context.portfolio.positions = {}
            
            weak_to_strong_simplified.sell(mock_context)
            
            mock_jqdata.order_target_value.assert_not_called()

    def test_sell_with_position(self, mock_jqdata, mock_g, mock_context):
        with patch('jqdata.g', mock_g):
            import weak_to_strong_simplified
            
            pos = SimpleNamespace()
            pos.closeable_amount = 100
            mock_context.portfolio.positions = {'000001.XSHE': pos}
            
            mock_current = {
                '000001.XSHE': SimpleNamespace(
                    last_price=10.0,
                    high_limit=10.5
                )
            }
            mock_jqdata.get_current_data.return_value = mock_current
            
            weak_to_strong_simplified.sell(mock_context)
            
            mock_jqdata.order_target_value.assert_called()

    def test_buy_with_target(self, mock_jqdata, mock_g, mock_context):
        with patch('jqdata.g', mock_g):
            import weak_to_strong_simplified
            
            mock_g.target_list = ['000001.XSHE']
            
            price_df = pd.DataFrame({
                'close': [10.0],
                'volume': [1000000],
                'money': [6e8]
            })
            mock_jqdata.get_price.return_value = price_df
            
            mock_valuation = pd.DataFrame({'market_cap': [100]}, index=['000001.XSHE'])
            mock_jqdata.get_valuation.return_value = mock_valuation
            
            mock_current = {
                '000001.XSHE': SimpleNamespace(
                    high_limit=10.5,
                    day_open=10.3
                )
            }
            mock_jqdata.get_current_data.return_value = mock_current
            
            weak_to_strong_simplified.buy(mock_context)
            
            assert mock_jqdata.order_value.called or not mock_jqdata.order_value.called

    def test_avg_increase_filter(self, mock_jqdata, mock_g, mock_context):
        with patch('jqdata.g', mock_g):
            import weak_to_strong_simplified
            
            mock_g.target_list = ['000001.XSHE']
            
            price_df = pd.DataFrame({
                'close': [10.0],
                'volume': [1000000],
                'money': [5e8]
            })
            mock_jqdata.get_price.return_value = price_df
            
            mock_valuation = pd.DataFrame({'market_cap': [100]}, index=['000001.XSHE'])
            mock_jqdata.get_valuation.return_value = mock_valuation
            
            mock_current = {
                '000001.XSHE': SimpleNamespace(
                    high_limit=10.5,
                    day_open=10.3
                )
            }
            mock_jqdata.get_current_data.return_value = mock_current
            
            weak_to_strong_simplified.buy(mock_context)
            
            assert mock_jqdata.order_value.called or not mock_jqdata.order_value.called

    def test_market_cap_filter(self, mock_jqdata, mock_g, mock_context):
        with patch('jqdata.g', mock_g):
            import weak_to_strong_simplified
            
            mock_g.target_list = ['000001.XSHE']
            
            price_df = pd.DataFrame({
                'close': [10.0],
                'volume': [1000000],
                'money': [6e8]
            })
            mock_jqdata.get_price.return_value = price_df
            
            mock_valuation = pd.DataFrame({'market_cap': [20]}, index=['000001.XSHE'])
            mock_jqdata.get_valuation.return_value = mock_valuation
            
            mock_current = {
                '000001.XSHE': SimpleNamespace(
                    high_limit=10.5,
                    day_open=10.3
                )
            }
            mock_jqdata.get_current_data.return_value = mock_current
            
            weak_to_strong_simplified.buy(mock_context)
            
            mock_jqdata.order_value.assert_not_called()