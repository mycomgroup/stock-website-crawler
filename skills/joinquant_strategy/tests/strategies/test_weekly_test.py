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
    mock_module.set_benchmark = Mock()
    mock_module.log = MagicMock()
    mock_module.log.set_level = Mock()
    mock_module.log.info = Mock()
    mock_module.run_daily = Mock()
    mock_module.order_value = Mock()
    mock_module.order_target = Mock()
    mock_module.order_target_value = Mock()
    mock_module.get_current_data = Mock()
    mock_module.g = SimpleNamespace()
    
    with patch.dict(sys.modules, {'jqdata': mock_module}):
        yield mock_module


@pytest.fixture
def mock_g():
    g = SimpleNamespace()
    g.trades = 0
    g.wins = 0
    g.pnl_list = []
    return g


@pytest.fixture
def mock_context():
    context = SimpleNamespace()
    context.current_dt = datetime(2024, 1, 16, 9, 35)
    
    portfolio = SimpleNamespace()
    portfolio.available_cash = 1000000
    portfolio.total_value = 1000000
    portfolio.positions = {}
    context.portfolio = portfolio
    return context


class TestWeeklyTest:
    def test_initialize(self, mock_jqdata, mock_g):
        with patch('jqdata.g', mock_g):
            import weekly_test
            mock_context = SimpleNamespace()
            weekly_test.initialize(mock_context)
            
            mock_jqdata.set_option.assert_called()
            mock_jqdata.set_benchmark.assert_called_once_with("000300.XSHG")
            assert mock_g.trades == 0

    def test_handle_data_non_monday(self, mock_jqdata, mock_g, mock_context):
        with patch('jqdata.g', mock_g):
            import weekly_test
            mock_context.current_dt = datetime(2024, 1, 17, 9, 35)
            mock_data = SimpleNamespace()
            
            weekly_test.handle_data(mock_context, mock_data)
            
            mock_jqdata.order.assert_not_called()

    def test_handle_data_wrong_time(self, mock_jqdata, mock_g, mock_context):
        with patch('jqdata.g', mock_g):
            import weekly_test
            mock_context.current_dt = datetime(2024, 1, 15, 10, 0)
            mock_data = SimpleNamespace()
            
            weekly_test.handle_data(mock_context, mock_data)
            
            mock_jqdata.order.assert_not_called()

    def test_handle_data_monday_935(self, mock_jqdata, mock_g, mock_context):
        with patch('jqdata.g', mock_g):
            import weekly_test
            mock_context.current_dt = datetime(2024, 1, 15, 9, 35)
            mock_data = SimpleNamespace()
            
            stock_data = SimpleNamespace()
            stock_data.paused = False
            stock_data.last_price = 10.0
            mock_jqdata.get_current_data.return_value = {
                '000001.XSHE': stock_data,
                '600000.XSHG': stock_data
            }
            
            weekly_test.handle_data(mock_context, mock_data)
            
            mock_jqdata.order.assert_called()

    def test_handle_data_with_positions(self, mock_jqdata, mock_g, mock_context):
        with patch('jqdata.g', mock_g):
            import weekly_test
            mock_context.current_dt = datetime(2024, 1, 15, 9, 35)
            mock_data = SimpleNamespace()
            
            pos = SimpleNamespace()
            pos.closeable_amount = 1000
            pos.avg_cost = 10.0
            mock_context.portfolio.positions = {'000001.XSHE': pos}
            
            stock_data = SimpleNamespace()
            stock_data.paused = False
            stock_data.last_price = 10.5
            mock_jqdata.get_current_data.return_value = {'000001.XSHE': stock_data}
            
            weekly_test.handle_data(mock_context, mock_data)
            
            assert len(mock_g.pnl_list) > 0

    def test_handle_data_december(self, mock_jqdata, mock_g, mock_context):
        with patch('jqdata.g', mock_g):
            import weekly_test
            mock_context.current_dt = datetime(2024, 12, 30, 9, 35)
            mock_data = SimpleNamespace()
            
            stock_data = SimpleNamespace()
            stock_data.paused = False
            stock_data.last_price = 10.0
            mock_jqdata.get_current_data.return_value = {'000001.XSHE': stock_data}
            
            weekly_test.handle_data(mock_context, mock_data)
            
            mock_jqdata.log.info.assert_called()