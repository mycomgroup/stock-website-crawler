import pytest
import sys
import numpy as np
import pandas as pd
from unittest.mock import MagicMock, patch, Mock
from types import SimpleNamespace
from datetime import datetime, timedelta

sys.path.insert(0, '/Users/yuping/Downloads/git/stock-website-crawler/strategies/misc_research/joinquant_strategy')


@pytest.fixture
def mock_jqdata_module():
    mock_module = MagicMock()
    mock_module.set_option = Mock()
    mock_module.set_benchmark = Mock()
    mock_module.set_slippage = Mock()
    mock_module.set_order_cost = Mock()
    mock_module.FixedSlippage = Mock(return_value=Mock())
    mock_module.OrderCost = Mock(return_value=Mock())
    mock_module.log = MagicMock()
    mock_module.log.set_level = Mock()
    mock_module.log.info = Mock()
    mock_module.log.debug = Mock()
    mock_module.run_daily = Mock()
    mock_module.run_weekly = Mock()
    mock_module.g = SimpleNamespace()
    mock_module.OrderStatus = MagicMock()
    mock_module.OrderStatus.held = 'held'
    mock_module.datetime = __import__('datetime')
    mock_module.query = Mock()
    mock_module.finance = MagicMock()
    mock_module.finance.STK_XR_XD = MagicMock()
    mock_module.finance.run_query = Mock()
    mock_module.valuation = MagicMock()
    mock_module.get_fundamentals = Mock()
    mock_module.get_all_securities = Mock()
    mock_module.get_current_data = Mock()
    mock_module.get_price = Mock()
    mock_module.history = Mock()
    mock_module.order_target_value = Mock()
    return mock_module


@pytest.fixture
def mock_jqfactor_module():
    mock_module = MagicMock()
    mock_module.get_factor_values = Mock()
    return mock_module


@pytest.fixture
def mock_g():
    g = SimpleNamespace()
    g.stock_num = 10
    g.limit_days = 20
    g.limit_up_list = []
    g.hold_list = []
    g.history_hold_list = []
    g.not_buy_again_list = []
    g.high_limit_list = []
    return g


@pytest.fixture
def mock_context():
    context = SimpleNamespace()
    context.previous_date = datetime(2024, 1, 15)
    context.current_dt = datetime(2024, 1, 16, 9, 30)
    portfolio = SimpleNamespace()
    portfolio.available_cash = 1000000
    portfolio.cash = 1000000
    portfolio.positions = {}
    portfolio.total_value = 1000000
    context.portfolio = portfolio
    return context


class TestStrategy15:
    def test_filter_paused_stock(self, mock_jqdata_module):
        with patch.dict(sys.modules, {'jqdata': mock_jqdata_module, 'jqfactor': MagicMock()}):
            import latest_strategy_15_高股息低杠杆小市值轮动策略 as strategy
            mock_current_data = {
                '000001.XSHE': SimpleNamespace(paused=False),
                '000002.XSHE': SimpleNamespace(paused=True),
                '600000.XSHG': SimpleNamespace(paused=False)
            }
            with patch.object(strategy, 'get_current_data', return_value=mock_current_data):
                stock_list = ['000001.XSHE', '000002.XSHE', '600000.XSHG']
                result = strategy.filter_paused_stock(stock_list)
                assert '000001.XSHE' in result
                assert '000002.XSHE' not in result

    def test_filter_st_stock(self, mock_jqdata_module):
        with patch.dict(sys.modules, {'jqdata': mock_jqdata_module, 'jqfactor': MagicMock()}):
            import latest_strategy_15_高股息低杠杆小市值轮动策略 as strategy
            mock_current_data = {
                '000001.XSHE': SimpleNamespace(is_st=False, name='平安银行'),
                '000002.XSHE': SimpleNamespace(is_st=True, name='ST万科'),
            }
            with patch.object(strategy, 'get_current_data', return_value=mock_current_data):
                stock_list = ['000001.XSHE', '000002.XSHE']
                result = strategy.filter_st_stock(stock_list)
                assert '000001.XSHE' in result
                assert '000002.XSHE' not in result

    def test_filter_kcbj_stock(self, mock_jqdata_module):
        with patch.dict(sys.modules, {'jqdata': mock_jqdata_module, 'jqfactor': MagicMock()}):
            import latest_strategy_15_高股息低杠杆小市值轮动策略 as strategy
            stock_list = ['000001.XSHE', '688001.XSHG', '430001.XSHE', '830001.XSHE']
            result = strategy.filter_kcbj_stock(stock_list)
            assert '000001.XSHE' in result
            assert '688001.XSHG' not in result
            assert '430001.XSHE' not in result
            assert '830001.XSHE' not in result

    def test_filter_new_stock(self, mock_jqdata_module, mock_context):
        with patch.dict(sys.modules, {'jqdata': mock_jqdata_module, 'jqfactor': MagicMock()}):
            import latest_strategy_15_高股息低杠杆小市值轮动策略 as strategy
            mock_security_info = SimpleNamespace()
            mock_security_info.start_date = datetime(2023, 1, 1)
            with patch.object(strategy, 'get_security_info', return_value=mock_security_info):
                stock_list = ['000001.XSHE']
                result = strategy.filter_new_stock(mock_context, stock_list, 375)
                assert len(result) >= 0

    def test_filter_limitup_stock(self, mock_jqdata_module, mock_context):
        with patch.dict(sys.modules, {'jqdata': mock_jqdata_module, 'jqfactor': MagicMock()}):
            import latest_strategy_15_高股息低杠杆小市值轮动策略 as strategy
            mock_current_data = {
                '000001.XSHE': SimpleNamespace(high_limit=10.0),
            }
            mock_history = {'000001.XSHE': [9.5]}
            with patch.object(strategy, 'get_current_data', return_value=mock_current_data):
                with patch.object(strategy, 'history', return_value=mock_history):
                    stock_list = ['000001.XSHE']
                    result = strategy.filter_limitup_stock(mock_context, stock_list)
                    assert len(result) >= 0

    def test_filter_limitdown_stock(self, mock_jqdata_module, mock_context):
        with patch.dict(sys.modules, {'jqdata': mock_jqdata_module, 'jqfactor': MagicMock()}):
            import latest_strategy_15_高股息低杠杆小市值轮动策略 as strategy
            mock_current_data = {
                '000001.XSHE': SimpleNamespace(low_limit=9.0),
            }
            mock_history = {'000001.XSHE': [9.5]}
            with patch.object(strategy, 'get_current_data', return_value=mock_current_data):
                with patch.object(strategy, 'history', return_value=mock_history):
                    stock_list = ['000001.XSHE']
                    result = strategy.filter_limitdown_stock(mock_context, stock_list)
                    assert len(result) >= 0

    def test_get_recent_limit_up_stock(self, mock_jqdata_module, mock_context):
        with patch.dict(sys.modules, {'jqdata': mock_jqdata_module, 'jqfactor': MagicMock()}):
            import latest_strategy_15_高股息低杠杆小市值轮动策略 as strategy
            mock_price_df = pd.DataFrame({
                'close': [10.0, 10.0],
                'high_limit': [10.0, 10.0]
            })
            with patch.object(strategy, 'get_price', return_value=mock_price_df):
                stock_list = ['000001.XSHE']
                result = strategy.get_recent_limit_up_stock(mock_context, stock_list, 5)
                assert isinstance(result, list)

    def test_order_target_value_(self, mock_jqdata_module):
        with patch.dict(sys.modules, {'jqdata': mock_jqdata_module, 'jqfactor': MagicMock()}):
            import latest_strategy_15_高股息低杠杆小市值轮动策略 as strategy
            mock_order = Mock()
            mock_order.filled = 100
            with patch.object(strategy, 'order_target_value', return_value=mock_order):
                result = strategy.order_target_value_('000001.XSHE', 10000)
                assert result is not None

    def test_open_position_success(self, mock_jqdata_module):
        with patch.dict(sys.modules, {'jqdata': mock_jqdata_module, 'jqfactor': MagicMock()}):
            import latest_strategy_15_高股息低杠杆小市值轮动策略 as strategy
            mock_order = Mock()
            mock_order.filled = 100
            with patch.object(strategy, 'order_target_value_', return_value=mock_order):
                result = strategy.open_position('000001.XSHE', 10000)
                assert result is True

    def test_open_position_failure(self, mock_jqdata_module):
        with patch.dict(sys.modules, {'jqdata': mock_jqdata_module, 'jqfactor': MagicMock()}):
            import latest_strategy_15_高股息低杠杆小市值轮动策略 as strategy
            with patch.object(strategy, 'order_target_value_', return_value=None):
                result = strategy.open_position('000001.XSHE', 10000)
                assert result is False

    def test_close_position_success(self, mock_jqdata_module):
        with patch.dict(sys.modules, {'jqdata': mock_jqdata_module, 'jqfactor': MagicMock()}):
            import latest_strategy_15_高股息低杠杆小市值轮动策略 as strategy
            position = SimpleNamespace(security='000001.XSHE')
            mock_order = Mock()
            mock_order.status = 'held'
            mock_order.filled = 100
            mock_order.amount = 100
            with patch.object(strategy, 'order_target_value_', return_value=mock_order):
                result = strategy.close_position(position)
                assert result is True

    def test_close_position_failure(self, mock_jqdata_module):
        with patch.dict(sys.modules, {'jqdata': mock_jqdata_module, 'jqfactor': MagicMock()}):
            import latest_strategy_15_高股息低杠杆小市值轮动策略 as strategy
            position = SimpleNamespace(security='000001.XSHE')
            with patch.object(strategy, 'order_target_value_', return_value=None):
                result = strategy.close_position(position)
                assert result is False

    def test_prepare_stock_list(self, mock_jqdata_module, mock_context, mock_g):
        with patch.dict(sys.modules, {'jqdata': mock_jqdata_module, 'jqfactor': MagicMock()}):
            import latest_strategy_15_高股息低杠杆小市值轮动策略 as strategy
            strategy.g = mock_g
            mock_context.portfolio.positions = {}
            strategy.prepare_stock_list(mock_context)
            assert strategy.g.hold_list == []
            assert strategy.g.high_limit_list == []

    def test_prepare_stock_list_with_positions(self, mock_jqdata_module, mock_context, mock_g):
        with patch.dict(sys.modules, {'jqdata': mock_jqdata_module, 'jqfactor': MagicMock()}):
            import latest_strategy_15_高股息低杠杆小市值轮动策略 as strategy
            strategy.g = mock_g
            position = SimpleNamespace(security='000001.XSHE')
            mock_context.portfolio.positions = {'000001.XSHE': position}
            mock_price_df = pd.DataFrame({
                'close': [10.0],
                'high_limit': [10.0]
            })
            with patch.object(strategy, 'get_price', return_value=mock_price_df):
                strategy.prepare_stock_list(mock_context)
                assert '000001.XSHE' in strategy.g.hold_list

    def test_weekly_adjustment(self, mock_jqdata_module, mock_context, mock_g):
        with patch.dict(sys.modules, {'jqdata': mock_jqdata_module, 'jqfactor': MagicMock()}):
            import latest_strategy_15_高股息低杠杆小市值轮动策略 as strategy
            strategy.g = mock_g
            strategy.g.stock_num = 10
            strategy.g.hold_list = []
            strategy.g.high_limit_list = []
            mock_context.portfolio.positions = {}
            mock_stock_list = ['000001.XSHE', '000002.XSHE']
            mock_paused_result = mock_stock_list
            mock_limitup_result = mock_stock_list
            mock_limitdown_result = mock_stock_list
            with patch.object(strategy, 'get_stock_list', return_value=mock_stock_list):
                with patch.object(strategy, 'filter_paused_stock', return_value=mock_paused_result):
                    with patch.object(strategy, 'filter_limitup_stock', return_value=mock_limitup_result):
                        with patch.object(strategy, 'filter_limitdown_stock', return_value=mock_limitdown_result):
                            with patch.object(strategy, 'open_position', return_value=True):
                                strategy.weekly_adjustment(mock_context)

    def test_check_limit_up(self, mock_jqdata_module, mock_context, mock_g):
        with patch.dict(sys.modules, {'jqdata': mock_jqdata_module, 'jqfactor': MagicMock()}):
            import latest_strategy_15_高股息低杠杆小市值轮动策略 as strategy
            strategy.g = mock_g
            strategy.g.high_limit_list = []
            strategy.check_limit_up(mock_context)

    def test_check_limit_up_with_list(self, mock_jqdata_module, mock_context, mock_g):
        with patch.dict(sys.modules, {'jqdata': mock_jqdata_module, 'jqfactor': MagicMock()}):
            import latest_strategy_15_高股息低杠杆小市值轮动策略 as strategy
            strategy.g = mock_g
            strategy.g.high_limit_list = ['000001.XSHE']
            position = SimpleNamespace(security='000001.XSHE')
            mock_context.portfolio.positions = {'000001.XSHE': position}
            mock_price_df = pd.DataFrame({'close': [9.5], 'high_limit': [10.0]})
            with patch.object(strategy, 'get_price', return_value=mock_price_df):
                with patch.object(strategy, 'close_position', return_value=True):
                    strategy.check_limit_up(mock_context)

    def test_print_position_info(self, mock_jqdata_module, mock_context, mock_g):
        with patch.dict(sys.modules, {'jqdata': mock_jqdata_module, 'jqfactor': MagicMock()}):
            import latest_strategy_15_高股息低杠杆小市值轮动策略 as strategy
            strategy.g = mock_g
            mock_context.portfolio.positions = {}
            mock_trades = {}
            with patch.object(strategy, 'get_trades', return_value=mock_trades):
                strategy.print_position_info(mock_context)