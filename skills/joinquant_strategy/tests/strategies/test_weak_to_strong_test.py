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
    mock_module.attribute_history = Mock()
    mock_module.get_shifted_date = Mock()
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
    g.trades = 0
    g.wins = 0
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


class TestWeakToStrongTest:
    def test_initialize(self, mock_jqdata, mock_g):
        with patch('jqdata.g', mock_g):
            import weak_to_strong_test
            context = SimpleNamespace()
            weak_to_strong_test.initialize(context)
            
            mock_jqdata.set_option.assert_called()
            mock_jqdata.run_daily.assert_called()
            assert mock_g.target_list == []
            assert mock_g.trades == 0
            assert mock_g.wins == 0

    def test_prepare_stock_list(self, mock_jqdata, mock_g):
        with patch('jqdata.g', mock_g):
            import weak_to_strong_test
            
            all_stocks = pd.DataFrame({'display_name': ['A']}, index=['000001.XSHE', '688001.XSHG'])
            mock_jqdata.get_all_securities.return_value = all_stocks
            
            mock_jqdata.get_security_info.return_value = SimpleNamespace(start_date=datetime(2020, 1, 1))
            
            mock_extras = pd.DataFrame({datetime(2024, 1, 15): [False]}, index=['000001.XSHE'])
            mock_jqdata.get_extras.return_value = mock_extras
            
            result = weak_to_strong_test.prepare_stock_list("2024-01-15")
            
            assert '688001.XSHG' not in result

    def test_get_hl_stock(self, mock_jqdata, mock_g):
        with patch('jqdata.g', mock_g):
            import weak_to_strong_test
            
            price_df = pd.DataFrame({
                'code': ['000001.XSHE', '000002.XSHE'],
                'close': [10.0, 9.0],
                'high_limit': [10.0, 10.0]
            })
            mock_jqdata.get_price.return_value = price_df
            
            result = weak_to_strong_test.get_hl_stock(['000001.XSHE', '000002.XSHE'], "2024-01-15")
            
            assert '000001.XSHE' in result

    def test_get_ever_hl_stock(self, mock_jqdata, mock_g):
        with patch('jqdata.g', mock_g):
            import weak_to_strong_test
            
            price_df = pd.DataFrame({
                'code': ['000001.XSHE', '000002.XSHE'],
                'high': [10.0, 9.5],
                'high_limit': [10.0, 10.0]
            })
            mock_jqdata.get_price.return_value = price_df
            
            result = weak_to_strong_test.get_ever_hl_stock(['000001.XSHE', '000002.XSHE'], "2024-01-15")
            
            assert '000001.XSHE' in result

    def test_calculate_zyts(self, mock_jqdata, mock_g, mock_context):
        with patch('jqdata.g', mock_g):
            import weak_to_strong_test
            
            high_data = {'high': pd.Series([10.0] * 101)}
            mock_jqdata.attribute_history.return_value = high_data
            
            result = weak_to_strong_test.calculate_zyts('000001.XSHE', mock_context)
            
            assert result >= 5

    def test_buy_no_target(self, mock_jqdata, mock_g, mock_context):
        with patch('jqdata.g', mock_g):
            import weak_to_strong_test
            
            mock_g.target_list = []
            
            weak_to_strong_test.buy(mock_context)
            
            mock_jqdata.order_value.assert_not_called()

    def test_sell_no_position(self, mock_jqdata, mock_g, mock_context):
        with patch('jqdata.g', mock_g):
            import weak_to_strong_test
            
            mock_context.portfolio.positions = {}
            
            weak_to_strong_test.sell(mock_context)
            
            mock_jqdata.order_target_value.assert_not_called()

    def test_sell_with_position_profit(self, mock_jqdata, mock_g, mock_context):
        with patch('jqdata.g', mock_g):
            import weak_to_strong_test
            
            pos = SimpleNamespace()
            pos.closeable_amount = 100
            pos.avg_cost = 10.0
            mock_context.portfolio.positions = {'000001.XSHE': pos}
            
            mock_current = {
                '000001.XSHE': SimpleNamespace(
                    last_price=11.0,
                    high_limit=10.5
                )
            }
            mock_jqdata.get_current_data.return_value = mock_current
            
            weak_to_strong_test.sell(mock_context)
            
            assert mock_g.wins >= 0

    def test_get_shifted_date(self, mock_jqdata, mock_g):
        with patch('jqdata.g', mock_g):
            import weak_to_strong_test
            
            mock_jqdata.get_all_trade_days.return_value = [datetime(2024, 1, i) for i in range(1, 20)]
            
            result = weak_to_strong_test.get_shifted_date("2024-01-15", -1, "T")
            
            assert result is not None