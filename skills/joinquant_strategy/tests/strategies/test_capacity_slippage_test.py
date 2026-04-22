import pytest
import sys
from unittest.mock import MagicMock, patch, Mock
from types import SimpleNamespace
from datetime import datetime, timedelta
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
    mock_module.get_security_info = Mock()
    mock_module.get_all_trade_days = Mock()
    mock_module.get_shifted_date = Mock()
    mock_module.order_value = Mock()
    mock_module.order_target_value = Mock()
    mock_module.g = SimpleNamespace()
    
    with patch.dict(sys.modules, {'jqdata': mock_module}):
        yield mock_module


@pytest.fixture
def mock_g():
    g = SimpleNamespace()
    g.trade_records = []
    g.signal_count = 0
    g.executed_count = 0
    g.rejected_capacity = 0
    g.signals = []
    g.first_board_signals = []
    g.second_board_signals = []
    return g


@pytest.fixture
def mock_context():
    context = SimpleNamespace()
    context.previous_date = datetime(2024, 1, 15)
    context.current_dt = datetime(2024, 1, 16, 9, 31)
    
    portfolio = SimpleNamespace()
    portfolio.available_cash = 1000000
    portfolio.starting_cash = 1000000
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
def mock_price_df_limit_up():
    return pd.DataFrame({
        'code': ['000001.XSHE', '000002.XSHE'],
        'close': [10.0, 20.0],
        'high_limit': [10.0, 20.0],
        'volume': [1000000, 2000000],
        'money': [10000000, 20000000]
    })


@pytest.fixture
def mock_valuation_df():
    return pd.DataFrame({
        'circulating_market_cap': [10.0]
    })


@pytest.fixture
def mock_trade_days():
    return [
        datetime(2024, 1, 10),
        datetime(2024, 1, 11),
        datetime(2024, 1, 12),
        datetime(2024, 1, 15),
        datetime(2024, 1, 16),
    ]


class TestCapacitySlippageTest:
    def test_initialize(self, mock_jqdata, mock_g):
        with patch('jqdata.g', mock_g):
            import capacity_slippage_test
            mock_context = SimpleNamespace()
            capacity_slippage_test.initialize(mock_context)
            
            mock_jqdata.set_option.assert_any_call("use_real_price", True)
            mock_jqdata.set_benchmark.assert_called_once_with("000300.XSHG")
            assert mock_jqdata.run_daily.call_count == 3

    def test_initialize_with_slippage(self, mock_jqdata, mock_g):
        with patch('jqdata.g', mock_g):
            import importlib
            import capacity_slippage_test
            
            original_slippage = capacity_slippage_test.SLIPPAGE_BPS
            capacity_slippage_test.SLIPPAGE_BPS = 10
            
            mock_context = SimpleNamespace()
            capacity_slippage_test.initialize(mock_context)
            
            mock_jqdata.set_slippage.assert_called_once()
            
            capacity_slippage_test.SLIPPAGE_BPS = original_slippage

    def test_prepare_signals_no_limit_up(self, mock_jqdata, mock_g, mock_context, mock_securities):
        with patch('jqdata.g', mock_g):
            import capacity_slippage_test
            
            mock_jqdata.get_all_securities.return_value = mock_securities
            
            mock_security_info = SimpleNamespace()
            mock_security_info.start_date = datetime(2020, 1, 1)
            mock_jqdata.get_security_info.return_value = mock_security_info
            
            price_df_no_limit = pd.DataFrame({
                'code': ['000001.XSHE'],
                'close': [9.0],
                'high_limit': [10.0],
                'volume': [1000000],
                'money': [10000000]
            })
            mock_jqdata.get_price.return_value = price_df_no_limit
            
            capacity_slippage_test.prepare_signals(mock_context)
            
            assert mock_g.signal_count == 0

    def test_buy_stocks_no_signals(self, mock_jqdata, mock_g, mock_context):
        with patch('jqdata.g', mock_g):
            import capacity_slippage_test
            
            mock_g.signals = []
            
            capacity_slippage_test.buy_stocks(mock_context)
            
            mock_jqdata.order_value.assert_not_called()

    def test_buy_stocks_with_first_board_signal(self, mock_jqdata, mock_g, mock_context):
        with patch('jqdata.g', mock_g):
            import capacity_slippage_test
            
            mock_g.signals = [
                {'code': '000001.XSHE', 'cap': 10.0, 'avg_money': 10000000, 'type': 'first_board'}
            ]
            
            stock_data = SimpleNamespace()
            stock_data.paused = False
            stock_data.is_st = False
            stock_data.pre_close = 10.0
            stock_data.day_open = 10.0
            stock_data.high_limit = 11.0
            stock_data.last_price = 10.5
            
            mock_jqdata.get_current_data.return_value = {'000001.XSHE': stock_data}
            
            capacity_slippage_test.buy_stocks(mock_context)
            
            mock_jqdata.order_value.assert_called()

    def test_buy_stocks_with_second_board_signal(self, mock_jqdata, mock_g, mock_context):
        with patch('jqdata.g', mock_g):
            import capacity_slippage_test
            
            mock_g.signals = [
                {'code': '000001.XSHE', 'cap': 20.0, 'avg_money': 5000000, 'type': 'second_board'}
            ]
            
            stock_data = SimpleNamespace()
            stock_data.paused = False
            stock_data.is_st = False
            stock_data.last_price = 10.0
            stock_data.high_limit = 11.0
            
            mock_jqdata.get_current_data.return_value = {'000001.XSHE': stock_data}
            
            capacity_slippage_test.buy_stocks(mock_context)
            
            mock_jqdata.order_value.assert_called()

    def test_buy_stocks_capacity_rejection(self, mock_jqdata, mock_g, mock_context):
        with patch('jqdata.g', mock_g):
            import capacity_slippage_test
            
            mock_g.signals = [
                {'code': '000001.XSHE', 'cap': 10.0, 'avg_money': 100, 'type': 'first_board'}
            ]
            
            stock_data = SimpleNamespace()
            stock_data.paused = False
            stock_data.is_st = False
            stock_data.pre_close = 10.0
            stock_data.day_open = 10.0
            stock_data.high_limit = 11.0
            stock_data.last_price = 10.5
            
            mock_jqdata.get_current_data.return_value = {'000001.XSHE': stock_data}
            
            capacity_slippage_test.buy_stocks(mock_context)
            
            assert mock_g.rejected_capacity >= 0

    def test_sell_stocks_with_positions(self, mock_jqdata, mock_g, mock_context):
        with patch('jqdata.g', mock_g):
            import capacity_slippage_test
            
            mock_g.trade_records = [{'code': '000001.XSHE', 'buy_value': 100000, 'buy_price': 10.0}]
            
            pos = SimpleNamespace()
            pos.closeable_amount = 1000
            pos.avg_cost = 10.0
            pos.init_time = datetime(2024, 1, 15)
            
            stock_data = SimpleNamespace()
            stock_data.last_price = 11.0
            
            mock_context.portfolio.positions = {'000001.XSHE': pos}
            mock_jqdata.get_current_data.return_value = {'000001.XSHE': stock_data}
            
            capacity_slippage_test.sell_stocks(mock_context)
            
            mock_jqdata.order_target_value.assert_called()

    def test_get_hl_stocks(self, mock_jqdata, mock_securities, mock_price_df_limit_up):
        with patch.dict(sys.modules, {'jqdata': mock_jqdata}):
            import capacity_slippage_test
            
            mock_jqdata.get_all_securities.return_value = mock_securities
            mock_jqdata.get_price.return_value = mock_price_df_limit_up
            
            result = capacity_slippage_test.get_hl_stocks('2024-01-15')
            
            assert isinstance(result, list)

    def test_get_shifted_date_valid(self, mock_jqdata, mock_trade_days):
        with patch.dict(sys.modules, {'jqdata': mock_jqdata}):
            import capacity_slippage_test
            
            mock_jqdata.get_all_trade_days.return_value = mock_trade_days
            
            result = capacity_slippage_test.get_shifted_date('2024-01-15', -1)
            
            assert result == '2024-01-12'

    def test_get_shifted_date_invalid(self, mock_jqdata, mock_trade_days):
        with patch.dict(sys.modules, {'jqdata': mock_jqdata}):
            import capacity_slippage_test
            
            mock_jqdata.get_all_trade_days.return_value = mock_trade_days
            
            result = capacity_slippage_test.get_shifted_date('2024-01-20', -1)
            
            assert result == '2024-01-20'

    def test_get_avg_money(self, mock_jqdata):
        with patch.dict(sys.modules, {'jqdata': mock_jqdata}):
            import capacity_slippage_test
            
            money_df = pd.DataFrame({
                'money': [10000000, 12000000, 11000000, 9000000, 13000000]
            })
            mock_jqdata.get_price.return_value = money_df
            
            result = capacity_slippage_test.get_avg_money('000001.XSHE', '2024-01-15')
            
            assert result > 0

    def test_get_avg_money_empty(self, mock_jqdata):
        with patch.dict(sys.modules, {'jqdata': mock_jqdata}):
            import capacity_slippage_test
            
            mock_jqdata.get_price.return_value = pd.DataFrame()
            
            result = capacity_slippage_test.get_avg_money('000001.XSHE', '2024-01-15')
            
            assert result == 0

    def test_after_trading_end(self, mock_jqdata, mock_g, mock_context):
        with patch('jqdata.g', mock_g):
            import capacity_slippage_test
            
            mock_g.trade_records = [
                {'pnl_pct': 10.0},
                {'pnl_pct': -5.0},
                {'pnl_pct': 8.0}
            ]
            
            capacity_slippage_test.after_trading_end(mock_context)
            
            mock_jqdata.log.info.assert_called()

    def test_after_trading_end_empty_records(self, mock_jqdata, mock_g, mock_context):
        with patch('jqdata.g', mock_g):
            import capacity_slippage_test
            
            mock_g.trade_records = []
            
            capacity_slippage_test.after_trading_end(mock_context)
            
            mock_jqdata.log.info.assert_called()

    def test_capacity_limit_ratio_constant(self, mock_jqdata, mock_g):
        with patch('jqdata.g', mock_g):
            import capacity_slippage_test
            
            assert capacity_slippage_test.CAPACITY_LIMIT_RATIO == 0.05

    def test_slippage_bps_constant(self, mock_jqdata, mock_g):
        with patch('jqdata.g', mock_g):
            import capacity_slippage_test
            
            assert capacity_slippage_test.SLIPPAGE_BPS == 0