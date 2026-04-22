import pytest
import sys
from unittest.mock import MagicMock, patch, Mock
from types import SimpleNamespace
from datetime import datetime
import pandas as pd

sys.path.insert(0, '/Users/yuping/Downloads/git/stock-website-crawler/strategies/misc_research/joinquant_strategy')


def create_st_df(stocks, is_st_values):
    df = pd.DataFrame({
        stock: [is_st] for stock, is_st in zip(stocks, is_st_values)
    }, index=['2024-01-15'])
    return df


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
    mock_module.get_valuation = Mock()
    mock_module.get_extras = Mock()
    mock_module.get_security_info = Mock()
    mock_module.get_fundamentals = Mock()
    mock_module.order = Mock()
    mock_module.order_target = Mock()
    
    mock_query = Mock()
    mock_query.filter.return_value = mock_query
    mock_module.query = Mock(return_value=mock_query)
    
    mock_valuation = Mock()
    mock_valuation.code = Mock()
    mock_valuation.circulating_market_cap = Mock()
    mock_module.valuation = mock_valuation
    
    mock_module.g = SimpleNamespace()
    
    with patch.dict(sys.modules, {'jqdata': mock_module}):
        yield mock_module


@pytest.fixture
def mock_g():
    g = SimpleNamespace()
    g.trade_count = 0
    g.win_count = 0
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
        'code': ['000001.XSHE', '000002.XSHE'],
        'circulating_market_cap': [8.0, 12.0]
    })


@pytest.fixture
def mock_price_df_limit_up():
    return pd.DataFrame({
        'code': ['000001.XSHE', '000002.XSHE'],
        'close': [10.0, 20.0],
        'high_limit': [10.0, 20.0]
    })


class TestAttributionBSimple2024:
    def test_initialize(self, mock_jqdata, mock_g):
        with patch('jqdata.g', mock_g):
            import attribution_b_simple_2024
            mock_context = SimpleNamespace()
            attribution_b_simple_2024.initialize(mock_context)
            
            mock_jqdata.set_option.assert_any_call("use_real_price", True)
            mock_jqdata.set_benchmark.assert_called_once_with("000300.XSHG")
            assert mock_jqdata.run_daily.call_count == 3

    def test_select_stocks_normal(self, mock_jqdata, mock_g, mock_context, mock_securities, mock_valuation_df, mock_price_df_limit_up):
        with patch('jqdata.g', mock_g):
            import attribution_b_simple_2024
            
            mock_jqdata.get_all_securities.return_value = mock_securities
            
            mock_security_info = SimpleNamespace()
            mock_security_info.start_date = datetime(2020, 1, 1)
            mock_jqdata.get_security_info.return_value = mock_security_info
            
            st_df = create_st_df(['000001.XSHE', '000002.XSHE', '600000.XSHG'], [False, False, False])
            mock_jqdata.get_extras.return_value = st_df
            mock_jqdata.get_fundamentals.return_value = mock_valuation_df
            mock_jqdata.get_price.return_value = mock_price_df_limit_up
            
            attribution_b_simple_2024.select_stocks(mock_context)
            
            assert len(mock_g.target) == 2

    def test_select_stocks_empty_valuation(self, mock_jqdata, mock_g, mock_context, mock_securities):
        with patch('jqdata.g', mock_g):
            import attribution_b_simple_2024
            
            mock_jqdata.get_all_securities.return_value = mock_securities
            
            mock_security_info = SimpleNamespace()
            mock_security_info.start_date = datetime(2020, 1, 1)
            mock_jqdata.get_security_info.return_value = mock_security_info
            
            st_df = create_st_df(['000001.XSHE', '000002.XSHE', '600000.XSHG'], [False, False, False])
            mock_jqdata.get_extras.return_value = st_df
            mock_jqdata.get_fundamentals.return_value = pd.DataFrame()
            
            attribution_b_simple_2024.select_stocks(mock_context)
            
            assert mock_g.target == []

    def test_buy_stocks_no_target(self, mock_jqdata, mock_g, mock_context):
        with patch('jqdata.g', mock_g):
            import attribution_b_simple_2024
            
            mock_g.target = []
            
            attribution_b_simple_2024.buy_stocks(mock_context)
            
            mock_jqdata.order.assert_not_called()

    def test_buy_stocks_paused_stock(self, mock_jqdata, mock_g, mock_context):
        with patch('jqdata.g', mock_g):
            import attribution_b_simple_2024
            
            mock_g.target = ['000001.XSHE']
            
            stock_data = SimpleNamespace()
            stock_data.paused = True
            stock_data.day_open = 10.0
            stock_data.pre_close = 10.0
            stock_data.last_price = 10.0
            
            mock_jqdata.get_current_data.return_value = {'000001.XSHE': stock_data}
            
            attribution_b_simple_2024.buy_stocks(mock_context)
            
            mock_jqdata.order.assert_not_called()

    def test_buy_stocks_open_pct_out_of_range(self, mock_jqdata, mock_g, mock_context):
        with patch('jqdata.g', mock_g):
            import attribution_b_simple_2024
            
            mock_g.target = ['000001.XSHE']
            
            stock_data = SimpleNamespace()
            stock_data.paused = False
            stock_data.day_open = 12.0
            stock_data.pre_close = 10.0
            stock_data.last_price = 10.5
            
            mock_jqdata.get_current_data.return_value = {'000001.XSHE': stock_data}
            
            attribution_b_simple_2024.buy_stocks(mock_context)
            
            mock_jqdata.order.assert_not_called()

    def test_buy_stocks_normal(self, mock_jqdata, mock_g, mock_context):
        with patch('jqdata.g', mock_g):
            import attribution_b_simple_2024
            
            mock_g.target = ['000001.XSHE']
            
            stock_data = SimpleNamespace()
            stock_data.paused = False
            stock_data.day_open = 10.0
            stock_data.pre_close = 10.0
            stock_data.last_price = 10.0
            
            mock_jqdata.get_current_data.return_value = {'000001.XSHE': stock_data}
            
            attribution_b_simple_2024.buy_stocks(mock_context)
            
            mock_jqdata.order.assert_called_once()

    def test_buy_stocks_zero_prev_close(self, mock_jqdata, mock_g, mock_context):
        with patch('jqdata.g', mock_g):
            import attribution_b_simple_2024
            
            mock_g.target = ['000001.XSHE']
            
            stock_data = SimpleNamespace()
            stock_data.paused = False
            stock_data.day_open = 10.0
            stock_data.pre_close = 0
            stock_data.last_price = 10.0
            
            mock_jqdata.get_current_data.return_value = {'000001.XSHE': stock_data}
            
            attribution_b_simple_2024.buy_stocks(mock_context)
            
            mock_jqdata.order.assert_not_called()

    def test_buy_stocks_low_open_in_range(self, mock_jqdata, mock_g, mock_context):
        with patch('jqdata.g', mock_g):
            import attribution_b_simple_2024
            
            mock_g.target = ['000001.XSHE']
            
            stock_data = SimpleNamespace()
            stock_data.paused = False
            stock_data.day_open = 9.85
            stock_data.pre_close = 10.0
            stock_data.last_price = 10.0
            
            mock_jqdata.get_current_data.return_value = {'000001.XSHE': stock_data}
            
            attribution_b_simple_2024.buy_stocks(mock_context)
            
            mock_jqdata.order.assert_called_once()

    def test_buy_stocks_very_low_open(self, mock_jqdata, mock_g, mock_context):
        with patch('jqdata.g', mock_g):
            import attribution_b_simple_2024
            
            mock_g.target = ['000001.XSHE']
            
            stock_data = SimpleNamespace()
            stock_data.paused = False
            stock_data.day_open = 9.6
            stock_data.pre_close = 10.0
            stock_data.last_price = 10.0
            
            mock_jqdata.get_current_data.return_value = {'000001.XSHE': stock_data}
            
            attribution_b_simple_2024.buy_stocks(mock_context)
            
            mock_jqdata.order.assert_not_called()

    def test_sell_stocks_with_positions(self, mock_jqdata, mock_g, mock_context):
        with patch('jqdata.g', mock_g):
            import attribution_b_simple_2024
            
            pos = SimpleNamespace()
            pos.closeable_amount = 1000
            pos.avg_cost = 10.0
            
            stock_data = SimpleNamespace()
            stock_data.last_price = 11.0
            
            mock_context.portfolio.positions = {'000001.XSHE': pos}
            mock_jqdata.get_current_data.return_value = {'000001.XSHE': stock_data}
            
            attribution_b_simple_2024.sell_stocks(mock_context)
            
            mock_jqdata.order_target.assert_called_once()
            assert len(mock_g.pnl_list) == 1
            assert mock_g.win_count == 1

    def test_sell_stocks_negative_pnl(self, mock_jqdata, mock_g, mock_context):
        with patch('jqdata.g', mock_g):
            import attribution_b_simple_2024
            
            pos = SimpleNamespace()
            pos.closeable_amount = 1000
            pos.avg_cost = 10.0
            
            stock_data = SimpleNamespace()
            stock_data.last_price = 9.0
            
            mock_context.portfolio.positions = {'000001.XSHE': pos}
            mock_jqdata.get_current_data.return_value = {'000001.XSHE': stock_data}
            
            attribution_b_simple_2024.sell_stocks(mock_context)
            
            assert len(mock_g.pnl_list) == 1
            assert mock_g.win_count == 0

    def test_sell_stocks_no_positions(self, mock_jqdata, mock_g, mock_context):
        with patch('jqdata.g', mock_g):
            import attribution_b_simple_2024
            
            mock_context.portfolio.positions = {}
            
            attribution_b_simple_2024.sell_stocks(mock_context)
            
            mock_jqdata.order_target.assert_not_called()

    def test_sell_stocks_no_closeable_amount(self, mock_jqdata, mock_g, mock_context):
        with patch('jqdata.g', mock_g):
            import attribution_b_simple_2024
            
            pos = SimpleNamespace()
            pos.closeable_amount = 0
            pos.avg_cost = 10.0
            
            stock_data = SimpleNamespace()
            stock_data.last_price = 11.0
            
            mock_context.portfolio.positions = {'000001.XSHE': pos}
            mock_jqdata.get_current_data.return_value = {'000001.XSHE': stock_data}
            
            attribution_b_simple_2024.sell_stocks(mock_context)
            
            mock_jqdata.order_target.assert_not_called()