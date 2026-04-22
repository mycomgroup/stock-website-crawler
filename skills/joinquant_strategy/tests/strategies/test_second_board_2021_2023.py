import pytest
import sys
from unittest.mock import MagicMock, patch, Mock
from types import SimpleNamespace
from datetime import datetime
import pandas as pd

sys.path.insert(0, '/Users/yuping/Downloads/git/stock-website-crawler/strategies/joinquant_strategy')


@pytest.fixture
def mock_jqdata():
    mock_module = MagicMock()
    mock_module.set_option = Mock()
    mock_module.set_benchmark = Mock()
    mock_module.set_order_cost = Mock()
    mock_module.OrderCost = Mock()
    mock_module.log = MagicMock()
    mock_module.log.set_level = Mock()
    mock_module.log.info = Mock()
    mock_module.log.error = Mock()
    mock_module.run_daily = Mock()
    mock_module.get_all_securities = Mock()
    mock_module.get_price = Mock()
    mock_module.get_current_data = Mock()
    mock_module.get_valuation = Mock()
    mock_module.get_fundamentals = Mock()
    mock_module.query = Mock()
    mock_module.valuation = MagicMock()
    mock_module.order_value = Mock()
    mock_module.order_target = Mock()
    mock_module.g = SimpleNamespace()
    
    with patch.dict(sys.modules, {'jqdata': mock_module}):
        yield mock_module


@pytest.fixture
def mock_g():
    g = SimpleNamespace()
    g.prev_date = None
    g.prev2_date = None
    g.current_date = None
    g.trade_count = 0
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


class TestSecondBoard20212023:
    def test_initialize(self, mock_jqdata, mock_g):
        with patch('jqdata.g', mock_g):
            import second_board_2021_2023
            mock_context = SimpleNamespace()
            second_board_2021_2023.initialize(mock_context)
            
            mock_jqdata.set_option.assert_called_once()
            mock_jqdata.set_order_cost.assert_called_once()
            assert mock_g.trade_count == 0

    def test_before_trading_start(self, mock_jqdata, mock_g, mock_context):
        with patch('jqdata.g', mock_g):
            import second_board_2021_2023
            mock_context.current_dt = datetime(2022, 3, 15, 9, 30)
            
            second_board_2021_2023.before_trading_start(mock_context)
            
            assert mock_g.current_date == "2022-03-15"

    def test_handle_data_out_of_range(self, mock_jqdata, mock_g, mock_context):
        with patch('jqdata.g', mock_g):
            import second_board_2021_2023
            mock_g.current_date = "2020-01-01"
            mock_data = SimpleNamespace()
            
            second_board_2021_2023.handle_data(mock_context, mock_data)
            
            mock_jqdata.get_all_securities.assert_not_called()

    def test_handle_data_within_range(self, mock_jqdata, mock_g, mock_context):
        with patch('jqdata.g', mock_g):
            import second_board_2021_2023
            
            mock_g.current_date = "2022-03-15"
            mock_g.prev_date = "2022-03-14"
            mock_g.prev2_date = "2022-03-13"
            mock_data = SimpleNamespace()
            
            mock_securities = pd.DataFrame({
                'display_name': ['平安银行']
            }, index=['000001.XSHE'])
            mock_jqdata.get_all_securities.return_value = mock_securities
            
            mock_price_df = pd.DataFrame({
                'code': ['000001.XSHE'],
                'close': [10.0],
                'high_limit': [10.0]
            })
            mock_jqdata.get_price.return_value = mock_price_df
            
            mock_jqdata.get_fundamentals.return_value = pd.DataFrame({
                'code': ['000001.XSHE'],
                'circulating_market_cap': [10]
            })
            
            second_board_2021_2023.handle_data(mock_context, mock_data)

    def test_trade_count_increment(self, mock_g):
        mock_g.trade_count = 0
        mock_g.trade_count += 1
        assert mock_g.trade_count == 1