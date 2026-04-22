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
    mock_module.get_index_stocks = Mock()
    mock_module.get_price = Mock()
    mock_module.get_all_securities = Mock()
    mock_module.get_current_data = Mock()
    mock_module.order_value = Mock()
    mock_module.order_target_value = Mock()
    mock_module.g = SimpleNamespace()
    
    with patch.dict(sys.modules, {'jqdata': mock_module}):
        yield mock_module


@pytest.fixture
def mock_g():
    g = SimpleNamespace()
    g.state = "正常"
    g.target_position = 70
    g.hs300_stocks = []
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


class TestStateRouterV1Minimal:
    def test_initialize(self, mock_jqdata, mock_g):
        with patch('jqdata.g', mock_g):
            import state_router_v1_minimal
            mock_context = SimpleNamespace()
            state_router_v1_minimal.initialize(mock_context)
            
            mock_jqdata.set_option.assert_called()
            mock_jqdata.set_benchmark.assert_called_once_with("000300.XSHG")
            assert mock_g.target_position == 70

    def test_before_trading_start_2022_q1(self, mock_jqdata, mock_g, mock_context):
        with patch('jqdata.g', mock_g):
            import state_router_v1_minimal
            mock_context.previous_date = datetime(2022, 2, 15)
            
            state_router_v1_minimal.before_trading_start(mock_context)
            
            assert mock_g.target_position == 0

    def test_before_trading_start_2022_q2(self, mock_jqdata, mock_g, mock_context):
        with patch('jqdata.g', mock_g):
            import state_router_v1_minimal
            mock_context.previous_date = datetime(2022, 5, 15)
            
            state_router_v1_minimal.before_trading_start(mock_context)
            
            assert mock_g.target_position == 100

    def test_before_trading_start_2023(self, mock_jqdata, mock_g, mock_context):
        with patch('jqdata.g', mock_g):
            import state_router_v1_minimal
            mock_context.previous_date = datetime(2023, 3, 15)
            
            state_router_v1_minimal.before_trading_start(mock_context)
            
            assert mock_g.target_position == 50

    def test_before_trading_start_2024_q1(self, mock_jqdata, mock_g, mock_context):
        with patch('jqdata.g', mock_g):
            import state_router_v1_minimal
            mock_context.previous_date = datetime(2024, 1, 15)
            
            state_router_v1_minimal.before_trading_start(mock_context)
            
            assert mock_g.target_position == 30

    def test_before_trading_start_2024_q2(self, mock_jqdata, mock_g, mock_context):
        with patch('jqdata.g', mock_g):
            import state_router_v1_minimal
            mock_context.previous_date = datetime(2024, 6, 15)
            
            state_router_v1_minimal.before_trading_start(mock_context)
            
            assert mock_g.target_position == 70

    def test_handle_data_with_zero_target(self, mock_jqdata, mock_g, mock_context):
        with patch('jqdata.g', mock_g):
            import state_router_v1_minimal
            
            mock_g.target_position = 0
            mock_g.stock = "510300.XSHG"
            
            pos = SimpleNamespace()
            pos.closeable_amount = 1000
            mock_context.portfolio.positions = {mock_g.stock: pos}
            mock_data = SimpleNamespace()
            
            state_router_v1_minimal.handle_data(mock_context, mock_data)
            
            mock_jqdata.order_value.assert_called()

    def test_handle_data_with_position(self, mock_jqdata, mock_g, mock_context):
        with patch('jqdata.g', mock_g):
            import state_router_v1_minimal
            
            mock_g.target_position = 70
            mock_g.stock = "510300.XSHG"
            
            pos = SimpleNamespace()
            pos.value = 700000
            mock_context.portfolio.positions = {mock_g.stock: pos}
            mock_data = SimpleNamespace()
            
            state_router_v1_minimal.handle_data(mock_context, mock_data)
            
            mock_jqdata.order_value.assert_called()