import pytest
import sys
from unittest.mock import MagicMock, patch, Mock
from types import SimpleNamespace
from datetime import datetime

sys.path.insert(0, '/Users/yuping/Downloads/git/stock-website-crawler/strategies/joinquant_strategy')


@pytest.fixture
def mock_jqdata():
    mock_module = MagicMock()
    mock_module.set_option = Mock()
    mock_module.log = MagicMock()
    mock_module.log.set_level = Mock()
    mock_module.log.info = Mock()
    mock_module.run_daily = Mock()
    mock_module.g = SimpleNamespace()
    
    with patch.dict(sys.modules, {'jqdata': mock_module}):
        yield mock_module


@pytest.fixture
def mock_g():
    g = SimpleNamespace()
    g.count = 0
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
def mock_data():
    return SimpleNamespace()


class TestMinimalTest:
    def test_initialize(self, mock_jqdata, mock_g):
        with patch('jqdata.g', mock_g):
            import minimal_test
            mock_context = SimpleNamespace()
            minimal_test.initialize(mock_context)
            
            mock_jqdata.set_option.assert_called_once_with("use_real_price", True)
            assert mock_g.count == 0

    def test_handle_data_first_call(self, mock_jqdata, mock_g, mock_context, mock_data):
        with patch('jqdata.g', mock_g):
            import minimal_test
            mock_g.count = 0
            minimal_test.handle_data(mock_context, mock_data)
            
            assert mock_g.count == 1
            mock_jqdata.log.info.assert_called_with("策略启动成功")

    def test_handle_data_second_call(self, mock_jqdata, mock_g, mock_context, mock_data):
        with patch('jqdata.g', mock_g):
            import minimal_test
            mock_g.count = 1
            minimal_test.handle_data(mock_context, mock_data)
            
            assert mock_g.count == 2
            mock_jqdata.log.info.assert_not_called()

    def test_handle_data_multiple_calls(self, mock_jqdata, mock_g, mock_context, mock_data):
        with patch('jqdata.g', mock_g):
            import minimal_test
            mock_g.count = 0
            
            for i in range(5):
                minimal_test.handle_data(mock_context, mock_data)
                
            assert mock_g.count == 5
            mock_jqdata.log.info.assert_called_once_with("策略启动成功")