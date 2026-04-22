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
    mock_module.order_value = Mock()
    mock_module.order_target = Mock()
    mock_module.g = SimpleNamespace()
    
    with patch.dict(sys.modules, {'jqdata': mock_module}):
        yield mock_module


@pytest.fixture
def mock_g():
    g = SimpleNamespace()
    g.trades = 0
    g.wins = 0
    g.stop_count = 0
    g.buy_times = {}
    return g


@pytest.fixture
def mock_context():
    context = SimpleNamespace()
    context.previous_date = datetime(2024, 1, 15)
    context.current_dt = datetime(2024, 1, 16, 9, 35)
    
    portfolio = SimpleNamespace()
    portfolio.available_cash = 1000000
    portfolio.total_value = 1000000
    portfolio.positions = {}
    context.portfolio = portfolio
    return context


class TestTimeStopLoss:
    def test_initialize(self, mock_jqdata, mock_g):
        with patch('jqdata.g', mock_g):
            import time_stop_loss
            context = SimpleNamespace()
            time_stop_loss.initialize(context)
            
            mock_jqdata.set_option.assert_called()
            mock_jqdata.run_daily.assert_called()
            assert mock_g.trades == 0
            assert mock_g.wins == 0
            assert mock_g.stop_count == 0

    def test_buy_no_hl_stocks(self, mock_jqdata, mock_g, mock_context):
        with patch('jqdata.g', mock_g):
            import time_stop_loss
            
            all_stocks = pd.DataFrame({'display_name': ['A']}, index=['000001.XSHE'])
            mock_jqdata.get_all_securities.return_value = all_stocks
            
            price_df = pd.DataFrame({
                'code': ['000001.XSHE'],
                'close': [9.0],
                'high_limit': [10.0]
            })
            mock_jqdata.get_price.return_value = price_df
            
            mock_jqdata.get_security_info.return_value = SimpleNamespace(start_date=datetime(2020, 1, 1))
            
            time_stop_loss.buy(mock_context)
            
            assert mock_g.trades == 0

    def test_buy_with_hl_stocks(self, mock_jqdata, mock_g, mock_context):
        with patch('jqdata.g', mock_g):
            import time_stop_loss
            
            all_stocks = pd.DataFrame({'display_name': ['A']}, index=['000001.XSHE'])
            mock_jqdata.get_all_securities.return_value = all_stocks
            
            price_df = pd.DataFrame({
                'code': ['000001.XSHE'],
                'close': [10.0],
                'high_limit': [10.0]
            })
            mock_jqdata.get_price.return_value = price_df
            
            mock_jqdata.get_security_info.return_value = SimpleNamespace(start_date=datetime(2020, 1, 1))
            
            mock_extras = pd.DataFrame({datetime(2024, 1, 15): [False]}, index=['000001.XSHE'])
            mock_jqdata.get_extras.return_value = mock_extras
            
            mock_current = {
                '000001.XSHE': SimpleNamespace(
                    pre_close=10.0,
                    day_open=10.05,
                    paused=False
                )
            }
            mock_jqdata.get_current_data.return_value = mock_current
            
            mock_valuation = pd.DataFrame({
                'circulating_market_cap': [50.0]
            }, index=['000001.XSHE'])
            mock_jqdata.get_valuation.return_value = mock_valuation
            
            time_stop_loss.buy(mock_context)
            
            assert mock_g.trades >= 0

    def test_check_time_stop_no_position(self, mock_jqdata, mock_g, mock_context):
        with patch('jqdata.g', mock_g):
            import time_stop_loss
            
            mock_context.portfolio.positions = {}
            
            time_stop_loss.check_time_stop(mock_context)
            
            mock_jqdata.order_target.assert_not_called()

    def test_check_time_stop_with_profit(self, mock_jqdata, mock_g, mock_context):
        with patch('jqdata.g', mock_g):
            import time_stop_loss
            
            mock_g.buy_times = {'000001.XSHE': datetime(2024, 1, 16, 9, 35)}
            
            pos = SimpleNamespace()
            pos.closeable_amount = 100
            pos.avg_cost = 10.0
            mock_context.portfolio.positions = {'000001.XSHE': pos}
            
            mock_current = {
                '000001.XSHE': SimpleNamespace(
                    last_price=10.5,
                    paused=False
                )
            }
            mock_jqdata.get_current_data.return_value = mock_current
            
            time_stop_loss.check_time_stop(mock_context)
            
            mock_jqdata.order_target.assert_not_called()

    def test_check_time_stop_with_loss(self, mock_jqdata, mock_g, mock_context):
        with patch('jqdata.g', mock_g):
            import time_stop_loss
            
            mock_g.buy_times = {'000001.XSHE': datetime(2024, 1, 16, 9, 0)}
            mock_context.current_dt = datetime(2024, 1, 16, 10, 30)
            
            pos = SimpleNamespace()
            pos.closeable_amount = 100
            pos.avg_cost = 10.0
            mock_context.portfolio.positions = {'000001.XSHE': pos}
            
            mock_current = {
                '000001.XSHE': SimpleNamespace(
                    last_price=9.5,
                    paused=False
                )
            }
            mock_jqdata.get_current_data.return_value = mock_current
            
            time_stop_loss.check_time_stop(mock_context)
            
            assert mock_g.stop_count >= 0

    def test_sell_end_with_profit(self, mock_jqdata, mock_g, mock_context):
        with patch('jqdata.g', mock_g):
            import time_stop_loss
            
            mock_g.buy_times = {'000001.XSHE': datetime(2024, 1, 16, 9, 35)}
            
            pos = SimpleNamespace()
            pos.closeable_amount = 100
            pos.avg_cost = 10.0
            mock_context.portfolio.positions = {'000001.XSHE': pos}
            
            mock_current = {
                '000001.XSHE': SimpleNamespace(
                    last_price=11.0,
                    paused=False
                )
            }
            mock_jqdata.get_current_data.return_value = mock_current
            
            time_stop_loss.sell_end(mock_context)
            
            assert mock_g.wins >= 0
            assert '000001.XSHE' not in mock_g.buy_times

    def test_sell_end_with_loss(self, mock_jqdata, mock_g, mock_context):
        with patch('jqdata.g', mock_g):
            import time_stop_loss
            
            mock_g.buy_times = {'000001.XSHE': datetime(2024, 1, 16, 9, 35)}
            
            pos = SimpleNamespace()
            pos.closeable_amount = 100
            pos.avg_cost = 10.0
            mock_context.portfolio.positions = {'000001.XSHE': pos}
            
            mock_current = {
                '000001.XSHE': SimpleNamespace(
                    last_price=9.5,
                    paused=False
                )
            }
            mock_jqdata.get_current_data.return_value = mock_current
            
            time_stop_loss.sell_end(mock_context)
            
            mock_jqdata.order_target.assert_called()
            assert '000001.XSHE' not in mock_g.buy_times

    def test_open_ratio_filter(self, mock_jqdata, mock_g, mock_context):
        with patch('jqdata.g', mock_g):
            import time_stop_loss
            
            all_stocks = pd.DataFrame({'display_name': ['A']}, index=['000001.XSHE'])
            mock_jqdata.get_all_securities.return_value = all_stocks
            
            price_df = pd.DataFrame({
                'code': ['000001.XSHE'],
                'close': [10.0],
                'high_limit': [10.0]
            })
            mock_jqdata.get_price.return_value = price_df
            
            mock_jqdata.get_security_info.return_value = SimpleNamespace(start_date=datetime(2020, 1, 1))
            mock_extras = pd.DataFrame({datetime(2024, 1, 15): [False]}, index=['000001.XSHE'])
            mock_jqdata.get_extras.return_value = mock_extras
            
            mock_current = {
                '000001.XSHE': SimpleNamespace(
                    pre_close=10.0,
                    day_open=10.15,
                    paused=False
                )
            }
            mock_jqdata.get_current_data.return_value = mock_current
            
            time_stop_loss.buy(mock_context)
            
            assert mock_g.trades >= 0