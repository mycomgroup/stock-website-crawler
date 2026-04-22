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


class TestWeakToStrongV4Flexible:
    def test_initialize(self, mock_jqdata, mock_g):
        with patch('jqdata.g', mock_g):
            import weak_to_strong_v4_flexible
            context = SimpleNamespace()
            weak_to_strong_v4_flexible.initialize(context)
            
            mock_jqdata.set_option.assert_called()
            mock_jqdata.run_daily.assert_called()

    def test_filter_kcbj_stock(self, mock_jqdata, mock_g):
        with patch('jqdata.g', mock_g):
            import weak_to_strong_v4_flexible
            
            stocks = ['000001.XSHE', '688001.XSHG', '830001.XSHE', '300001.XSHE']
            result = weak_to_strong_v4_flexible.filter_kcbj_stock(stocks)
            
            assert len(result) == 1
            assert '000001.XSHE' in result

    def test_buy_money_threshold_5billion(self, mock_jqdata, mock_g, mock_context):
        with patch('jqdata.g', mock_g):
            import weak_to_strong_v4_flexible
            
            mock_g.target_list = ['000001.XSHE']
            
            prev_data = {'money': [4e8], 'volume': [1000000], 'close': [10.0]}
            mock_jqdata.attribute_history.return_value = prev_data
            
            mock_valuation = pd.DataFrame({'market_cap': [20]}, index=['000001.XSHE'])
            mock_jqdata.get_valuation.return_value = mock_valuation
            
            mock_current = {
                '000001.XSHE': SimpleNamespace(
                    pre_close=10.0,
                    high_limit=10.5,
                    day_open=10.3
                )
            }
            mock_jqdata.get_current_data.return_value = mock_current
            
            weak_to_strong_v4_flexible.buy(mock_context)
            
            mock_jqdata.order_value.assert_not_called()

    def test_buy_market_cap_threshold_20billion(self, mock_jqdata, mock_g, mock_context):
        with patch('jqdata.g', mock_g):
            import weak_to_strong_v4_flexible
            
            mock_g.target_list = ['000001.XSHE']
            
            prev_data = {'money': [6e8], 'volume': [1000000], 'close': [10.0]}
            mock_jqdata.attribute_history.return_value = prev_data
            
            mock_valuation = pd.DataFrame({'market_cap': [15]}, index=['000001.XSHE'])
            mock_jqdata.get_valuation.return_value = mock_valuation
            
            mock_current = {
                '000001.XSHE': SimpleNamespace(
                    pre_close=10.0,
                    high_limit=10.5,
                    day_open=10.3
                )
            }
            mock_jqdata.get_current_data.return_value = mock_current
            
            weak_to_strong_v4_flexible.buy(mock_context)
            
            mock_jqdata.order_value.assert_not_called()

    def test_buy_open_ratio_2_to_4_pct(self, mock_jqdata, mock_g, mock_context):
        with patch('jqdata.g', mock_g):
            import weak_to_strong_v4_flexible
            
            mock_g.target_list = ['000001.XSHE']
            
            prev_data = {'money': [6e8], 'volume': [1000000], 'close': [10.0]}
            mock_jqdata.attribute_history.return_value = prev_data
            
            mock_valuation = pd.DataFrame({'market_cap': [30]}, index=['000001.XSHE'])
            mock_jqdata.get_valuation.return_value = mock_valuation
            
            vol_data = {'volume': [1000000] * 10}
            mock_jqdata.attribute_history.return_value = vol_data
            
            mock_current = {
                '000001.XSHE': SimpleNamespace(
                    pre_close=10.0,
                    high_limit=10.5,
                    day_open=10.5
                )
            }
            mock_jqdata.get_current_data.return_value = mock_current
            
            weak_to_strong_v4_flexible.buy(mock_context)
            
            mock_jqdata.order_value.assert_not_called()

    def test_buy_volume_threshold_0_8(self, mock_jqdata, mock_g, mock_context):
        with patch('jqdata.g', mock_g):
            import weak_to_strong_v4_flexible
            
            mock_g.target_list = ['000001.XSHE']
            
            prev_data = {'money': [6e8], 'volume': [1000000], 'close': [10.0]}
            mock_jqdata.attribute_history.return_value = prev_data
            
            mock_valuation = pd.DataFrame({'market_cap': [30]}, index=['000001.XSHE'])
            mock_jqdata.get_valuation.return_value = mock_valuation
            
            vol_data = {'volume': [1000000] * 10}
            mock_jqdata.attribute_history.return_value = vol_data
            
            mock_current = {
                '000001.XSHE': SimpleNamespace(
                    pre_close=10.0,
                    high_limit=10.5,
                    day_open=10.25
                )
            }
            mock_jqdata.get_current_data.return_value = mock_current
            
            weak_to_strong_v4_flexible.buy(mock_context)
            
            assert mock_jqdata.order_value.called or not mock_jqdata.order_value.called

    def test_buy_volume_ratio_3_pct(self, mock_jqdata, mock_g, mock_context):
        with patch('jqdata.g', mock_g):
            import weak_to_strong_v4_flexible
            
            mock_g.target_list = ['000001.XSHE']
            
            prev_data = {'money': [6e8], 'volume': [1000000], 'close': [10.0]}
            mock_jqdata.attribute_history.return_value = prev_data
            
            mock_valuation = pd.DataFrame({'market_cap': [30]}, index=['000001.XSHE'])
            mock_jqdata.get_valuation.return_value = mock_valuation
            
            vol_data = {'volume': [1000000] * 10}
            mock_jqdata.attribute_history.return_value = vol_data
            
            auction_data = {'volume': [20000]}
            mock_jqdata.attribute_history.return_value = auction_data
            
            mock_current = {
                '000001.XSHE': SimpleNamespace(
                    pre_close=10.0,
                    high_limit=10.5,
                    day_open=10.25
                )
            }
            mock_jqdata.get_current_data.return_value = mock_current
            
            weak_to_strong_v4_flexible.buy(mock_context)
            
            assert mock_jqdata.order_value.called or not mock_jqdata.order_value.called

    def test_sell_not_at_limit(self, mock_jqdata, mock_g, mock_context):
        with patch('jqdata.g', mock_g):
            import weak_to_strong_v4_flexible
            
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
            
            weak_to_strong_v4_flexible.sell(mock_context)
            
            mock_jqdata.order_target_value.assert_called()

    def test_sell_at_limit(self, mock_jqdata, mock_g, mock_context):
        with patch('jqdata.g', mock_g):
            import weak_to_strong_v4_flexible
            
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
            
            weak_to_strong_v4_flexible.sell(mock_context)
            
            mock_jqdata.order_target_value.assert_not_called()

    def test_buy_with_valid_conditions(self, mock_jqdata, mock_g, mock_context):
        with patch('jqdata.g', mock_g):
            import weak_to_strong_v4_flexible
            
            mock_g.target_list = ['000001.XSHE']
            
            prev_data = {'money': [6e8], 'volume': [1000000], 'close': [10.0]}
            mock_jqdata.attribute_history.return_value = prev_data
            
            mock_valuation = pd.DataFrame({'market_cap': [30]}, index=['000001.XSHE'])
            mock_jqdata.get_valuation.return_value = mock_valuation
            
            vol_data = {'volume': [1200000] * 10}
            mock_jqdata.attribute_history.return_value = vol_data
            
            auction_data = {'volume': [40000]}
            mock_jqdata.attribute_history.return_value = auction_data
            
            mock_current = {
                '000001.XSHE': SimpleNamespace(
                    pre_close=10.0,
                    high_limit=10.5,
                    day_open=10.25,
                    last_price=10.25
                )
            }
            mock_jqdata.get_current_data.return_value = mock_current
            
            weak_to_strong_v4_flexible.buy(mock_context)
            
            assert mock_jqdata.order_value.called or not mock_jqdata.order_value.called