import pytest
import sys
from unittest.mock import MagicMock, patch, Mock
from types import SimpleNamespace
from datetime import datetime

sys.path.insert(0, '/Users/yuping/Downloads/git/stock-website-crawler/strategies/misc_research/joinquant_strategy')


@pytest.fixture
def mock_jqdata():
    mock_module = MagicMock()
    mock_module.set_option = Mock()
    mock_module.set_benchmark = Mock()
    mock_module.log = MagicMock()
    mock_module.log.set_level = Mock()
    mock_module.run_daily = Mock()
    mock_module.get_index_stocks = Mock()
    mock_module.get_price = Mock()
    mock_module.get_current_data = Mock()
    mock_module.order = Mock()
    mock_module.order_target = Mock()
    mock_module.record = Mock()
    mock_module.g = SimpleNamespace()
    
    with patch.dict(sys.modules, {'jqdata': mock_module}):
        yield mock_module


@pytest.fixture
def mock_g():
    g = SimpleNamespace()
    g.target_position = 100
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


class TestStateRouterBaseline:
    def test_initialize(self, mock_jqdata, mock_g):
        with patch('jqdata.g', mock_g):
            import state_router_baseline
            mock_context = SimpleNamespace()
            state_router_baseline.initialize(mock_context)
            
            mock_jqdata.set_option.assert_called()
            mock_jqdata.set_benchmark.assert_called_once_with("000300.XSHG")
            assert mock_g.target_position == 100

    def test_handle_data_no_position(self, mock_jqdata, mock_g, mock_context):
        with patch('jqdata.g', mock_g):
            import state_router_baseline
            mock_context.portfolio.positions = {}
            mock_data = SimpleNamespace()
            
            state_router_baseline.handle_data(mock_context, mock_data)
            
            mock_jqdata.order_value.assert_called()

    def test_handle_data_has_position(self, mock_jqdata, mock_g, mock_context):
        with patch('jqdata.g', mock_g):
            import state_router_baseline
            
            pos = SimpleNamespace()
            pos.value = 1000000
            mock_context.portfolio.positions = {'000300.XSHG': pos}
            mock_data = SimpleNamespace()
            
            state_router_baseline.handle_data(mock_context, mock_data)
            
            mock_jqdata.order_value.assert_not_called()