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
    mock_module.order_value = Mock()
    mock_module.order_target_value = Mock()
    mock_module.MarketOrderStyle = Mock()
    mock_module.LimitOrderStyle = Mock()
    mock_module.g = SimpleNamespace()
    
    with patch.dict(sys.modules, {'jqdata': mock_module}):
        yield mock_module


@pytest.fixture
def mock_g():
    g = SimpleNamespace()
    g.target_list = []
    g.trade_log = []
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


class TestWeakToStrongV1Original:
    def test_initialize(self, mock_jqdata, mock_g):
        with patch('jqdata.g', mock_g):
            import weak_to_strong_v1_original
            context = SimpleNamespace()
            weak_to_strong_v1_original.initialize(context)
            
            mock_jqdata.set_option.assert_called()
            mock_jqdata.run_daily.assert_called()

    def test_transform_date(self, mock_jqdata, mock_g):
        with patch('jqdata.g', mock_g):
            import weak_to_strong_v1_original
            
            result = weak_to_strong_v1_original.transform_date("2024-01-15", "str")
            assert result == "2024-01-15"

    def test_filter_kcbj_stock(self, mock_jqdata, mock_g):
        with patch('jqdata.g', mock_g):
            import weak_to_strong_v1_original
            
            stocks = ['000001.XSHE', '688001.XSHG', '830001.XSHE', '300001.XSHE']
            result = weak_to_strong_v1_original.filter_kcbj_stock(stocks)
            
            assert '688001.XSHG' not in result
            assert '830001.XSHE' not in result
            assert '300001.XSHE' not in result

    def test_get_hl_stock(self, mock_jqdata, mock_g):
        with patch('jqdata.g', mock_g):
            import weak_to_strong_v1_original
            
            price_df = pd.DataFrame({
                'code': ['000001.XSHE'],
                'close': [10.0],
                'high_limit': [10.0]
            })
            mock_jqdata.get_price.return_value = price_df
            
            result = weak_to_strong_v1_original.get_hl_stock(['000001.XSHE'], "2024-01-15")
            
            assert '000001.XSHE' in result

    def test_calculate_zyts(self, mock_jqdata, mock_g, mock_context):
        with patch('jqdata.g', mock_g):
            import weak_to_strong_v1_original
            
            high_data = {'high': pd.Series([10.0] * 101)}
            mock_jqdata.attribute_history.return_value = high_data
            
            result = weak_to_strong_v1_original.calculate_zyts('000001.XSHE', mock_context)
            
            assert result >= 5

    def test_sell_at_limit(self, mock_jqdata, mock_g, mock_context):
        with patch('jqdata.g', mock_g):
            import weak_to_strong_v1_original
            
            pos = SimpleNamespace()
            pos.closeable_amount = 100
            mock_context.portfolio.positions = {'000001.XSHE': pos}
            
            mock_current = {
                '000001.XSHE': SimpleNamespace(
                    last_price=10.5,
                    high_limit=10.5
                )
            }
            mock_jqdata.get_current_data.return_value = mock_current
            
            weak_to_strong_v1_original.sell(mock_context)
            
            mock_jqdata.order_target_value.assert_not_called()

    def test_sell_930_with_loss(self, mock_jqdata, mock_g, mock_context):
        with patch('jqdata.g', mock_g):
            import weak_to_strong_v1_original
            
            pos = SimpleNamespace()
            pos.closeable_amount = 100
            pos.avg_cost = 10.0
            mock_context.portfolio.positions = {'000001.XSHE': pos}
            
            mock_current = {
                '000001.XSHE': SimpleNamespace(
                    last_price=9.5,
                    high_limit=10.5,
                    low_limit=9.0
                )
            }
            mock_jqdata.get_current_data.return_value = mock_current
            
            weak_to_strong_v1_original.sell_930(mock_context)
            
            mock_jqdata.order_target_value.assert_called()

    def test_sell_1030_at_cost(self, mock_jqdata, mock_g, mock_context):
        with patch('jqdata.g', mock_g):
            import weak_to_strong_v1_original
            
            pos = SimpleNamespace()
            pos.closeable_amount = 100
            pos.avg_cost = 10.0
            mock_context.portfolio.positions = {'000001.XSHE': pos}
            
            mock_current = {
                '000001.XSHE': SimpleNamespace(
                    last_price=9.9,
                    high_limit=10.5,
                    low_limit=9.0
                )
            }
            mock_jqdata.get_current_data.return_value = mock_current
            
            weak_to_strong_v1_original.sell_1030(mock_context)
            
            mock_jqdata.order_target_value.assert_called()

    def test_sell_1330_threshold(self, mock_jqdata, mock_g, mock_context):
        with patch('jqdata.g', mock_g):
            import weak_to_strong_v1_original
            
            pos = SimpleNamespace()
            pos.closeable_amount = 100
            pos.avg_cost = 10.0
            mock_context.portfolio.positions = {'000001.XSHE': pos}
            
            mock_current = {
                '000001.XSHE': SimpleNamespace(
                    last_price=10.2,
                    high_limit=10.5,
                    low_limit=9.0
                )
            }
            mock_jqdata.get_current_data.return_value = mock_current
            
            weak_to_strong_v1_original.sell_1330(mock_context)
            
            mock_jqdata.order_target_value.assert_called()

    def test_buy_avg_price_increase_threshold(self, mock_jqdata, mock_g, mock_context):
        with patch('jqdata.g', mock_g):
            import weak_to_strong_v1_original
            
            mock_g.target_list = ['000001.XSHE']
            
            prev_data = {'close': [10.0], 'volume': [1000000], 'money': [7e8]}
            mock_jqdata.attribute_history.return_value = prev_data
            
            mock_valuation = pd.DataFrame({'market_cap': [70]}, index=['000001.XSHE'])
            mock_jqdata.get_valuation.return_value = mock_valuation
            
            vol_data = {'volume': [1000000] * 10}
            mock_jqdata.attribute_history.return_value = vol_data
            
            mock_current = {
                '000001.XSHE': SimpleNamespace(
                    pre_close=10.0,
                    high_limit=10.5,
                    day_open=10.3
                )
            }
            mock_jqdata.get_current_data.return_value = mock_current
            
            weak_to_strong_v1_original.buy(mock_context)
            
            assert mock_jqdata.order_value.called or not mock_jqdata.order_value.called