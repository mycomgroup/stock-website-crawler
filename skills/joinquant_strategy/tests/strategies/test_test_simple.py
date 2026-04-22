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
    mock_module.run_daily = Mock()
    mock_module.order_value = Mock()
    mock_module.order_target_value = Mock()
    mock_module.g = SimpleNamespace()
    
    with patch.dict(sys.modules, {'jqdata': mock_module}):
        yield mock_module


@pytest.fixture
def mock_g():
    g = SimpleNamespace()
    g.stock = "000001.XSHE"
    return g


@pytest.fixture
def mock_context():
    context = SimpleNamespace()
    context.current_dt = datetime(2024, 1, 16, 9, 30)
    
    portfolio = SimpleNamespace()
    portfolio.available_cash = 1000000
    portfolio.positions = {}
    context.portfolio = portfolio
    return context


class TestTestSimple:
    def test_initialize(self, mock_jqdata, mock_g):
        with patch('jqdata.g', mock_g):
            import test_simple
            mock_context = SimpleNamespace()
            test_simple.initialize(mock_context)
            
            mock_jqdata.set_option.assert_called_once_with("use_real_price", True)
            mock_jqdata.log.set_level.assert_called_once_with("system", "error")
            mock_jqdata.run_daily.assert_called_once()

    def test_trade_buy_when_empty_position(self, mock_jqdata, mock_g, mock_context):
        with patch('jqdata.g', mock_g):
            import test_simple
            
            pos = SimpleNamespace()
            pos.total_amount = 0
            mock_context.portfolio.positions = {mock_g.stock: pos}
            
            test_simple.trade(mock_context)
            
            mock_jqdata.order_value.assert_called_once()

    def test_trade_sell_when_has_position(self, mock_jqdata, mock_g, mock_context):
        with patch('jqdata.g', mock_g):
            import test_simple
            
            pos = SimpleNamespace()
            pos.total_amount = 1000
            mock_context.portfolio.positions = {mock_g.stock: pos}
            
            test_simple.trade(mock_context)
            
            mock_jqdata.order_target_value.assert_called_once_with(mock_g.stock, 0)

    def test_stock_setting(self, mock_g):
        import test_simple
        with patch('jqdata.g', mock_g):
            assert mock_g.stock == "000001.XSHE"