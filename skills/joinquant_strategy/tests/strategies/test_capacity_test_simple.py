import pytest
import sys
from unittest.mock import MagicMock, patch, Mock
from types import SimpleNamespace
from datetime import datetime
import pandas as pd

sys.path.insert(0, '/Users/yuping/Downloads/git/stock-website-crawler/strategies/misc_research/joinquant_strategy')


def create_price_df_limit_up(num_stocks=30):
    codes = [f'00000{i}.XSHE' for i in range(num_stocks)]
    return pd.DataFrame({
        'code': codes,
        'close': [10.0] * num_stocks,
        'high_limit': [10.0] * num_stocks
    })


@pytest.fixture
def mock_jqdata():
    mock_module = MagicMock()
    mock_module.set_option = Mock()
    mock_module.set_benchmark = Mock()
    mock_module.set_slippage = Mock()
    mock_module.FixedSlippage = Mock()
    mock_module.log = MagicMock()
    mock_module.log.info = Mock()
    mock_module.log.set_level = Mock()
    mock_module.run_daily = Mock()
    mock_module.get_all_securities = Mock()
    mock_module.get_price = Mock()
    mock_module.get_current_data = Mock()
    mock_module.get_valuation = Mock()
    mock_module.order = Mock()
    mock_module.order_target = Mock()
    mock_module.g = SimpleNamespace()
    
    with patch.dict(sys.modules, {'jqdata': mock_module}):
        yield mock_module


@pytest.fixture
def mock_g():
    g = SimpleNamespace()
    g.trades = 0
    g.pnl_list = []
    g.target = []
    return g


@pytest.fixture
def mock_context():
    context = SimpleNamespace()
    context.previous_date = datetime(2024, 1, 15)
    context.current_dt = datetime(2024, 1, 16, 9, 31)
    
    portfolio = SimpleNamespace()
    portfolio.available_cash = 1000000
    portfolio.total_value = 1000000
    portfolio.positions = {}
    context.portfolio = portfolio
    return context


@pytest.fixture
def mock_securities():
    return pd.DataFrame({
        'display_name': ['平安银行', '万科A', '浦发银行']
    }, index=['000001.XSHE', '000002.XSHE', '600000.XSHG'])


@pytest.fixture
def mock_valuation_df():
    return pd.DataFrame({
        'circulating_market_cap': [10.0]
    })


class TestCapacityTestSimple:
    def test_initialize(self, mock_jqdata, mock_g):
        with patch('jqdata.g', mock_g):
            import capacity_test_simple
            mock_context = SimpleNamespace()
            capacity_test_simple.initialize(mock_context)
            
            mock_jqdata.set_option.assert_any_call("use_real_price", True)
            mock_jqdata.set_benchmark.assert_called_once_with("000300.XSHG")
            assert mock_jqdata.run_daily.call_count == 3

    def test_initialize_with_slippage(self, mock_jqdata, mock_g):
        with patch('jqdata.g', mock_g):
            import importlib
            import capacity_test_simple
            
            original_slippage = capacity_test_simple.SLIPPAGE_BPS
            capacity_test_simple.SLIPPAGE_BPS = 10
            
            mock_context = SimpleNamespace()
            capacity_test_simple.initialize(mock_context)
            
            mock_jqdata.set_slippage.assert_called_once()
            
            capacity_test_simple.SLIPPAGE_BPS = original_slippage

    def test_select_stocks_normal(self, mock_jqdata, mock_g, mock_context, mock_securities):
        with patch('jqdata.g', mock_g):
            import capacity_test_simple
            
            mock_jqdata.get_all_securities.return_value = mock_securities
            mock_jqdata.get_price.return_value = create_price_df_limit_up(30)
            
            capacity_test_simple.select_stocks(mock_context)
            
            assert len(mock_g.target) == 30

    def test_select_stocks_exception(self, mock_jqdata, mock_g, mock_context, mock_securities):
        with patch('jqdata.g', mock_g):
            import capacity_test_simple
            
            mock_jqdata.get_all_securities.return_value = mock_securities
            mock_jqdata.get_price.side_effect = Exception("test error")
            
            capacity_test_simple.select_stocks(mock_context)
            
            mock_jqdata.log.info.assert_called()

    def test_buy_stocks_no_target(self, mock_jqdata, mock_g, mock_context):
        with patch('jqdata.g', mock_g):
            import capacity_test_simple
            
            mock_g.target = []
            
            capacity_test_simple.buy_stocks(mock_context)
            
            mock_jqdata.order.assert_not_called()

    def test_buy_stocks_with_target(self, mock_jqdata, mock_g, mock_context, mock_valuation_df):
        with patch('jqdata.g', mock_g):
            import capacity_test_simple
            
            mock_g.target = ['000001.XSHE'] * 20
            
            stock_data = SimpleNamespace()
            stock_data.paused = False
            stock_data.is_st = False
            stock_data.pre_close = 10.0
            stock_data.day_open = 10.0
            stock_data.last_price = 10.0
            
            mock_jqdata.get_current_data.return_value = {'000001.XSHE': stock_data}
            mock_jqdata.get_valuation.return_value = mock_valuation_df
            
            capacity_test_simple.buy_stocks(mock_context)
            
            assert mock_jqdata.order.call_count <= 3

    def test_buy_stocks_paused(self, mock_jqdata, mock_g, mock_context):
        with patch('jqdata.g', mock_g):
            import capacity_test_simple
            
            mock_g.target = ['000001.XSHE']
            
            stock_data = SimpleNamespace()
            stock_data.paused = True
            stock_data.is_st = False
            
            mock_jqdata.get_current_data.return_value = {'000001.XSHE': stock_data}
            
            capacity_test_simple.buy_stocks(mock_context)
            
            mock_jqdata.order.assert_not_called()

    def test_buy_stocks_is_st(self, mock_jqdata, mock_g, mock_context):
        with patch('jqdata.g', mock_g):
            import capacity_test_simple
            
            mock_g.target = ['000001.XSHE']
            
            stock_data = SimpleNamespace()
            stock_data.paused = False
            stock_data.is_st = True
            
            mock_jqdata.get_current_data.return_value = {'000001.XSHE': stock_data}
            
            capacity_test_simple.buy_stocks(mock_context)
            
            mock_jqdata.order.assert_not_called()

    def test_buy_stocks_open_pct_in_range(self, mock_jqdata, mock_g, mock_context, mock_valuation_df):
        with patch('jqdata.g', mock_g):
            import capacity_test_simple
            
            mock_g.target = ['000001.XSHE']
            
            stock_data = SimpleNamespace()
            stock_data.paused = False
            stock_data.is_st = False
            stock_data.pre_close = 10.0
            stock_data.day_open = 10.0
            stock_data.last_price = 10.0
            
            mock_jqdata.get_current_data.return_value = {'000001.XSHE': stock_data}
            mock_jqdata.get_valuation.return_value = mock_valuation_df
            
            capacity_test_simple.buy_stocks(mock_context)
            
            mock_jqdata.order.assert_called()

    def test_buy_stocks_open_pct_out_of_range(self, mock_jqdata, mock_g, mock_context):
        with patch('jqdata.g', mock_g):
            import capacity_test_simple
            
            mock_g.target = ['000001.XSHE']
            
            stock_data = SimpleNamespace()
            stock_data.paused = False
            stock_data.is_st = False
            stock_data.pre_close = 10.0
            stock_data.day_open = 12.0
            stock_data.last_price = 12.0
            
            mock_jqdata.get_current_data.return_value = {'000001.XSHE': stock_data}
            
            capacity_test_simple.buy_stocks(mock_context)
            
            mock_jqdata.order.assert_not_called()

    def test_buy_stocks_cap_out_of_range(self, mock_jqdata, mock_g, mock_context):
        with patch('jqdata.g', mock_g):
            import capacity_test_simple
            
            mock_g.target = ['000001.XSHE']
            
            stock_data = SimpleNamespace()
            stock_data.paused = False
            stock_data.is_st = False
            stock_data.pre_close = 10.0
            stock_data.day_open = 10.0
            stock_data.last_price = 10.0
            
            valuation_df_large = pd.DataFrame({
                'circulating_market_cap': [50.0]
            })
            
            mock_jqdata.get_current_data.return_value = {'000001.XSHE': stock_data}
            mock_jqdata.get_valuation.return_value = valuation_df_large
            
            capacity_test_simple.buy_stocks(mock_context)
            
            mock_jqdata.order.assert_not_called()

    def test_buy_stocks_zero_prev_close(self, mock_jqdata, mock_g, mock_context):
        with patch('jqdata.g', mock_g):
            import capacity_test_simple
            
            mock_g.target = ['000001.XSHE']
            
            stock_data = SimpleNamespace()
            stock_data.paused = False
            stock_data.is_st = False
            stock_data.pre_close = 0
            stock_data.day_open = 10.0
            
            mock_jqdata.get_current_data.return_value = {'000001.XSHE': stock_data}
            
            capacity_test_simple.buy_stocks(mock_context)
            
            mock_jqdata.order.assert_not_called()

    def test_buy_stocks_valuation_exception(self, mock_jqdata, mock_g, mock_context):
        with patch('jqdata.g', mock_g):
            import capacity_test_simple
            
            mock_g.target = ['000001.XSHE']
            
            stock_data = SimpleNamespace()
            stock_data.paused = False
            stock_data.is_st = False
            stock_data.pre_close = 10.0
            stock_data.day_open = 10.0
            stock_data.last_price = 10.0
            
            mock_jqdata.get_current_data.return_value = {'000001.XSHE': stock_data}
            mock_jqdata.get_valuation.side_effect = Exception("test error")
            
            capacity_test_simple.buy_stocks(mock_context)
            
            mock_jqdata.order.assert_not_called()

    def test_sell_stocks_with_positions(self, mock_jqdata, mock_g, mock_context):
        with patch('jqdata.g', mock_g):
            import capacity_test_simple
            
            pos = SimpleNamespace()
            pos.closeable_amount = 1000
            pos.avg_cost = 10.0
            
            stock_data = SimpleNamespace()
            stock_data.last_price = 11.0
            
            mock_context.portfolio.positions = {'000001.XSHE': pos}
            mock_jqdata.get_current_data.return_value = {'000001.XSHE': stock_data}
            
            capacity_test_simple.sell_stocks(mock_context)
            
            mock_jqdata.order_target.assert_called_once()
            assert len(mock_g.pnl_list) == 1

    def test_sell_stocks_zero_prices(self, mock_jqdata, mock_g, mock_context):
        with patch('jqdata.g', mock_g):
            import capacity_test_simple
            
            pos = SimpleNamespace()
            pos.closeable_amount = 1000
            pos.avg_cost = 0
            
            stock_data = SimpleNamespace()
            stock_data.last_price = 0
            
            mock_context.portfolio.positions = {'000001.XSHE': pos}
            mock_jqdata.get_current_data.return_value = {'000001.XSHE': stock_data}
            
            capacity_test_simple.sell_stocks(mock_context)
            
            assert len(mock_g.pnl_list) == 0

    def test_sell_stocks_no_closeable_amount(self, mock_jqdata, mock_g, mock_context):
        with patch('jqdata.g', mock_g):
            import capacity_test_simple
            
            pos = SimpleNamespace()
            pos.closeable_amount = 0
            pos.avg_cost = 10.0
            
            stock_data = SimpleNamespace()
            stock_data.last_price = 11.0
            
            mock_context.portfolio.positions = {'000001.XSHE': pos}
            mock_jqdata.get_current_data.return_value = {'000001.XSHE': stock_data}
            
            capacity_test_simple.sell_stocks(mock_context)
            
            assert len(mock_g.pnl_list) == 0

    def test_after_trading_end_with_pnl(self, mock_jqdata, mock_g, mock_context):
        with patch('jqdata.g', mock_g):
            import capacity_test_simple
            
            mock_g.pnl_list = [10.0, -5.0, 8.0]
            
            capacity_test_simple.after_trading_end(mock_context)
            
            mock_jqdata.log.info.assert_called()

    def test_after_trading_end_empty_pnl(self, mock_jqdata, mock_g, mock_context):
        with patch('jqdata.g', mock_g):
            import capacity_test_simple
            
            mock_g.pnl_list = []
            
            capacity_test_simple.after_trading_end(mock_context)
            
            mock_jqdata.log.info.assert_not_called()

    def test_slippage_bps_constant(self, mock_jqdata, mock_g):
        with patch('jqdata.g', mock_g):
            import capacity_test_simple
            
            assert capacity_test_simple.SLIPPAGE_BPS == 0