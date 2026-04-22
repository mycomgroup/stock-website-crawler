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
    mock_module.set_slippage = Mock()
    mock_module.FixedSlippage = Mock()
    mock_module.log = MagicMock()
    mock_module.log.set_level = Mock()
    mock_module.log.info = Mock()
    mock_module.run_daily = Mock()
    mock_module.order_value = Mock()
    mock_module.order_target = Mock()
    mock_module.g = SimpleNamespace()
    
    with patch.dict(sys.modules, {'jqdata': mock_module}):
        yield mock_module


@pytest.fixture
def mock_g():
    g = SimpleNamespace()
    return g


@pytest.fixture
def mock_context():
    context = SimpleNamespace()
    context.previous_date = datetime(2024, 1, 15)
    context.current_dt = datetime(2024, 1, 16, 9, 35)
    
    portfolio = SimpleNamespace()
    portfolio.available_cash = 1000000
    portfolio.total_value = 1000000
    
    pos1 = SimpleNamespace()
    pos1.closeable_amount = 1000
    portfolio.positions = {'000001.XSHE': pos1}
    context.portfolio = portfolio
    return context


class TestSlippageTest:
    def test_initialize_with_zero_slippage(self, mock_jqdata, mock_g):
        with patch('jqdata.g', mock_g):
            import slippage_test
            mock_context = SimpleNamespace()
            slippage_test.initialize(mock_context)
            
            mock_jqdata.set_option.assert_called_once_with("use_real_price", True)
            mock_jqdata.set_benchmark.assert_called_once_with("000300.XSHG")
            mock_jqdata.set_slippage.assert_not_called()
            mock_jqdata.run_daily.assert_called()

    def test_initialize_with_positive_slippage(self, mock_jqdata, mock_g):
        with patch('jqdata.g', mock_g):
            import slippage_test
            original_slippage = slippage_test.SLIPPAGE_BPS
            slippage_test.SLIPPAGE_BPS = 100
            
            mock_context = SimpleNamespace()
            slippage_test.initialize(mock_context)
            
            mock_jqdata.set_slippage.assert_called_once()
            slippage_test.SLIPPAGE_BPS = original_slippage

    def test_buy_empty_positions(self, mock_jqdata, mock_g, mock_context):
        with patch('jqdata.g', mock_g):
            import slippage_test
            mock_context.portfolio.positions = {}
            
            slippage_test.buy(mock_context)
            
            assert mock_jqdata.order_value.call_count == 2

    def test_buy_with_existing_positions(self, mock_jqdata, mock_g, mock_context):
        with patch('jqdata.g', mock_g):
            import slippage_test
            
            slippage_test.buy(mock_context)
            
            mock_jqdata.order_value.assert_not_called()

    def test_sell_with_closeable_amount(self, mock_jqdata, mock_g, mock_context):
        with patch('jqdata.g', mock_g):
            import slippage_test
            
            slippage_test.sell(mock_context)
            
            mock_jqdata.order_target.assert_called()

    def test_sell_without_closeable_amount(self, mock_jqdata, mock_g, mock_context):
        with patch('jqdata.g', mock_g):
            import slippage_test
            pos = SimpleNamespace()
            pos.closeable_amount = 0
            mock_context.portfolio.positions = {'000001.XSHE': pos}
            
            slippage_test.sell(mock_context)
            
            mock_jqdata.order_target.assert_not_called()

    def test_slippage_bps_constant(self):
        import slippage_test
        assert slippage_test.SLIPPAGE_BPS == 0