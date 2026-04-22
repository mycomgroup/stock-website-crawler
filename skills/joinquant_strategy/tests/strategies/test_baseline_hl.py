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
    mock_module.log = MagicMock()
    mock_module.log.set_level = Mock()
    mock_module.run_daily = Mock()
    mock_module.get_all_securities = Mock()
    mock_module.get_price = Mock()
    mock_module.get_current_data = Mock()
    mock_module.get_extras = Mock()
    mock_module.get_security_info = Mock()
    mock_module.order = Mock()
    mock_module.order_target = Mock()
    mock_module.g = SimpleNamespace()
    
    with patch.dict(sys.modules, {'jqdata': mock_module}):
        yield mock_module


@pytest.fixture
def mock_g():
    g = SimpleNamespace()
    g.trades = 0
    g.wins = 0
    g.pnl_list = []
    g.target = []
    return g


@pytest.fixture
def mock_context():
    context = SimpleNamespace()
    context.previous_date = datetime(2024, 1, 15)
    context.current_dt = datetime(2024, 1, 16, 9, 35)
    
    portfolio = SimpleNamespace()
    portfolio.available_cash = 1000000
    portfolio.total_value = 1000000
    portfolio.positions = {}
    context.portfolio = portfolio
    return context


@pytest.fixture
def mock_securities():
    return pd.DataFrame({
        'display_name': ['平安银行', '万科A', '浦发银行', '测试股票']
    }, index=['000001.XSHE', '000002.XSHE', '600000.XSHG', '600001.XSHG'])


@pytest.fixture
def mock_price_df_limit_up():
    return pd.DataFrame({
        'code': ['000001.XSHE', '000002.XSHE', '600000.XSHG'],
        'close': [10.0, 20.0, 15.0],
        'high_limit': [10.0, 20.0, 15.0]
    })


class TestBaselineHl:
    def test_initialize(self, mock_jqdata, mock_g):
        with patch('jqdata.g', mock_g):
            import baseline_hl
            mock_context = SimpleNamespace()
            baseline_hl.initialize(mock_context)
            
            mock_jqdata.set_option.assert_any_call("use_real_price", True)
            assert mock_jqdata.run_daily.call_count == 3

    def test_select_stocks_normal(self, mock_jqdata, mock_g, mock_context, mock_securities, mock_price_df_limit_up):
        with patch('jqdata.g', mock_g):
            import baseline_hl
            
            mock_jqdata.get_all_securities.return_value = mock_securities
            
            mock_security_info = SimpleNamespace()
            mock_security_info.start_date = datetime(2020, 1, 1)
            mock_jqdata.get_security_info.return_value = mock_security_info
            
            st_df = create_st_df(['000001.XSHE', '000002.XSHE', '600000.XSHG', '600001.XSHG'], [False, False, False, False])
            mock_jqdata.get_extras.return_value = st_df
            mock_jqdata.get_price.return_value = mock_price_df_limit_up
            
            baseline_hl.select_stocks(mock_context)
            
            assert len(mock_g.target) == 3

    def test_select_stocks_no_limit_up(self, mock_jqdata, mock_g, mock_context, mock_securities):
        with patch('jqdata.g', mock_g):
            import baseline_hl
            
            mock_jqdata.get_all_securities.return_value = mock_securities
            
            mock_security_info = SimpleNamespace()
            mock_security_info.start_date = datetime(2020, 1, 1)
            mock_jqdata.get_security_info.return_value = mock_security_info
            
            st_df = create_st_df(['000001.XSHE', '000002.XSHE', '600000.XSHG', '600001.XSHG'], [False, False, False, False])
            mock_jqdata.get_extras.return_value = st_df
            
            price_df_no_limit = pd.DataFrame({
                'code': ['000001.XSHE', '000002.XSHE'],
                'close': [9.0, 19.0],
                'high_limit': [10.0, 20.0]
            })
            mock_jqdata.get_price.return_value = price_df_no_limit
            
            baseline_hl.select_stocks(mock_context)
            
            assert mock_g.target == []

    def test_buy_stocks_no_target(self, mock_jqdata, mock_g, mock_context):
        with patch('jqdata.g', mock_g):
            import baseline_hl
            
            mock_g.target = []
            
            baseline_hl.buy_stocks(mock_context)
            
            mock_jqdata.order.assert_not_called()

    def test_buy_stocks_top_three(self, mock_jqdata, mock_g, mock_context):
        with patch('jqdata.g', mock_g):
            import baseline_hl
            
            mock_g.target = ['000001.XSHE', '000002.XSHE', '600000.XSHG']
            
            stock_data = SimpleNamespace()
            stock_data.paused = False
            stock_data.last_price = 10.0
            
            mock_jqdata.get_current_data.return_value = {
                '000001.XSHE': stock_data,
                '000002.XSHE': stock_data,
                '600000.XSHG': stock_data
            }
            
            baseline_hl.buy_stocks(mock_context)
            
            assert mock_jqdata.order.call_count == 3

    def test_buy_stocks_paused_excluded(self, mock_jqdata, mock_g, mock_context):
        with patch('jqdata.g', mock_g):
            import baseline_hl
            
            mock_g.target = ['000001.XSHE', '000002.XSHE']
            
            stock_data_active = SimpleNamespace()
            stock_data_active.paused = False
            stock_data_active.last_price = 10.0
            
            stock_data_paused = SimpleNamespace()
            stock_data_paused.paused = True
            stock_data_paused.last_price = 10.0
            
            mock_jqdata.get_current_data.return_value = {
                '000001.XSHE': stock_data_paused,
                '000002.XSHE': stock_data_active
            }
            
            baseline_hl.buy_stocks(mock_context)
            
            assert mock_jqdata.order.call_count == 1

    def test_buy_stocks_insufficient_cash(self, mock_jqdata, mock_g, mock_context):
        with patch('jqdata.g', mock_g):
            import baseline_hl
            
            mock_g.target = ['000001.XSHE']
            
            stock_data = SimpleNamespace()
            stock_data.paused = False
            stock_data.last_price = 100000.0
            
            mock_jqdata.get_current_data.return_value = {'000001.XSHE': stock_data}
            
            baseline_hl.buy_stocks(mock_context)
            
            mock_jqdata.order.assert_not_called()

    def test_sell_stocks_with_positions(self, mock_jqdata, mock_g, mock_context):
        with patch('jqdata.g', mock_g):
            import baseline_hl
            
            pos = SimpleNamespace()
            pos.closeable_amount = 1000
            pos.avg_cost = 10.0
            
            stock_data = SimpleNamespace()
            stock_data.last_price = 11.0
            
            mock_context.portfolio.positions = {'000001.XSHE': pos}
            mock_jqdata.get_current_data.return_value = {'000001.XSHE': stock_data}
            
            baseline_hl.sell_stocks(mock_context)
            
            mock_jqdata.order_target.assert_called_once()
            assert len(mock_g.pnl_list) == 1
            assert mock_g.wins == 1

    def test_sell_stocks_with_loss(self, mock_jqdata, mock_g, mock_context):
        with patch('jqdata.g', mock_g):
            import baseline_hl
            
            pos = SimpleNamespace()
            pos.closeable_amount = 1000
            pos.avg_cost = 10.0
            
            stock_data = SimpleNamespace()
            stock_data.last_price = 9.0
            
            mock_context.portfolio.positions = {'000001.XSHE': pos}
            mock_jqdata.get_current_data.return_value = {'000001.XSHE': stock_data}
            
            baseline_hl.sell_stocks(mock_context)
            
            assert len(mock_g.pnl_list) == 1
            assert mock_g.wins == 0

    def test_sell_stocks_no_closeable_amount(self, mock_jqdata, mock_g, mock_context):
        with patch('jqdata.g', mock_g):
            import baseline_hl
            
            pos = SimpleNamespace()
            pos.closeable_amount = 0
            pos.avg_cost = 10.0
            
            stock_data = SimpleNamespace()
            stock_data.last_price = 11.0
            
            mock_context.portfolio.positions = {'000001.XSHE': pos}
            mock_jqdata.get_current_data.return_value = {'000001.XSHE': stock_data}
            
            baseline_hl.sell_stocks(mock_context)
            
            mock_jqdata.order_target.assert_not_called()

    def test_select_stocks_filters_new_stocks(self, mock_jqdata, mock_g, mock_context, mock_securities, mock_price_df_limit_up):
        with patch('jqdata.g', mock_g):
            import baseline_hl
            
            mock_jqdata.get_all_securities.return_value = mock_securities
            
            mock_security_info_old = SimpleNamespace()
            mock_security_info_old.start_date = datetime(2020, 1, 1)
            
            mock_security_info_new = SimpleNamespace()
            mock_security_info_new.start_date = datetime(2024, 1, 1)
            
            def get_security_info_side_effect(code):
                return mock_security_info_new if code == '600001.XSHG' else mock_security_info_old
            
            mock_jqdata.get_security_info.side_effect = get_security_info_side_effect
            st_df = create_st_df(['000001.XSHE', '000002.XSHE', '600000.XSHG'], [False, False, False])
            mock_jqdata.get_extras.return_value = st_df
            mock_jqdata.get_price.return_value = mock_price_df_limit_up
            
            baseline_hl.select_stocks(mock_context)
            
            assert '600001.XSHG' not in mock_g.target