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
    mock_module.log = MagicMock()
    mock_module.log.set_level = Mock()
    mock_module.run_daily = Mock()
    mock_module.get_all_securities = Mock()
    mock_module.get_price = Mock()
    mock_module.get_current_data = Mock()
    mock_module.order_value = Mock()
    mock_module.order_target = Mock()
    mock_module.g = SimpleNamespace()
    
    with patch.dict(sys.modules, {'jqdata': mock_module}):
        yield mock_module


@pytest.fixture
def mock_g():
    g = SimpleNamespace()
    g.trades = 0
    return g


@pytest.fixture
def mock_context():
    context = SimpleNamespace()
    context.previous_date = datetime(2024, 1, 15)
    context.current_dt = datetime(2024, 1, 16, 9, 31)
    
    portfolio = SimpleNamespace()
    portfolio.available_cash = 1000000
    portfolio.positions = {}
    context.portfolio = portfolio
    return context


@pytest.fixture
def mock_securities():
    return pd.DataFrame({
        'display_name': ['平安银行', '万科A', '测试股票']
    }, index=['000001.XSHE', '000002.XSHE', '000003.XSHE'])


@pytest.fixture
def mock_price_df():
    return pd.DataFrame({
        'code': ['000001.XSHE', '000002.XSHE'],
        'close': [10.0, 20.0],
        'high_limit': [10.0, 20.0]
    })


class TestUltraSimple:
    def test_initialize(self, mock_jqdata, mock_g):
        with patch('jqdata.g', mock_g):
            import ultra_simple
            mock_context = SimpleNamespace()
            ultra_simple.initialize(mock_context)
            
            mock_jqdata.set_option.assert_called()
            mock_jqdata.set_benchmark.assert_called_once_with("000300.XSHG")
            mock_jqdata.run_daily.assert_called()

    def test_buy_with_limit_up_stocks(self, mock_jqdata, mock_g, mock_context, mock_securities, mock_price_df):
        with patch('jqdata.g', mock_g):
            import ultra_simple
            
            mock_jqdata.get_all_securities.return_value = mock_securities
            mock_jqdata.get_price.return_value = mock_price_df
            
            stock_data = SimpleNamespace()
            stock_data.paused = False
            stock_data.is_st = False
            stock_data.day_open = 10.0
            stock_data.pre_close = 10.0
            
            mock_jqdata.get_current_data.return_value = {'000001.XSHE': stock_data}
            
            ultra_simple.buy(mock_context)
            
            assert mock_g.trades > 0

    def test_buy_with_no_targets(self, mock_jqdata, mock_g, mock_context):
        with patch('jqdata.g', mock_g):
            import ultra_simple
            
            mock_jqdata.get_price.side_effect = Exception("error")
            
            mock_stock = SimpleNamespace()
            mock_stock.paused = False
            mock_stock.is_st = False
            mock_stock.day_open = 10.0
            mock_stock.pre_close = 10.0
            
            mock_jqdata.get_current_data.return_value = {'000001.XSHE': mock_stock}
            
            ultra_simple.buy(mock_context)
            
            mock_jqdata.order_value.assert_called()

    def test_sell_with_positions(self, mock_jqdata, mock_g, mock_context):
        with patch('jqdata.g', mock_g):
            import ultra_simple
            
            pos = SimpleNamespace()
            pos.closeable_amount = 1000
            mock_context.portfolio.positions = {'000001.XSHE': pos}
            
            ultra_simple.sell(mock_context)
            
            mock_jqdata.order_target.assert_called()

    def test_sell_without_positions(self, mock_jqdata, mock_g, mock_context):
        with patch('jqdata.g', mock_g):
            import ultra_simple
            mock_context.portfolio.positions = {}
            
            ultra_simple.sell(mock_context)
            
            mock_jqdata.order_target.assert_not_called()