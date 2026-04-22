import pytest
import sys
import pandas as pd
from unittest.mock import MagicMock, patch, Mock
from types import SimpleNamespace
from datetime import datetime, timedelta

sys.path.insert(0, '/Users/yuping/Downloads/git/stock-website-crawler/strategies/misc_research/joinquant_strategy')


@pytest.fixture
def mock_jqdata_module():
    mock_module = MagicMock()
    mock_module.set_benchmark = Mock()
    mock_module.log = MagicMock()
    mock_module.log.set_level = Mock()
    mock_module.log.info = Mock()
    mock_module.set_option = Mock()
    mock_module.set_slippage = Mock()
    mock_module.FixedSlippage = Mock(return_value=Mock())
    mock_module.g = SimpleNamespace()
    mock_module.get_all_securities = Mock()
    mock_module.get_current_data = Mock()
    mock_module.filter_kcbj_stock = Mock()
    mock_module.filter_st_stock = Mock()
    mock_module.filter_new_stock = Mock()
    mock_module.filter_paused_stock = Mock()
    mock_module.filter_limit_stock = Mock()
    mock_module.get_price = Mock()
    mock_module.get_fundamentals = Mock()
    mock_module.query = Mock()
    mock_module.finance = MagicMock()
    mock_module.finance.STK_XR_XD = MagicMock()
    mock_module.finance.run_query = Mock()
    mock_module.valuation = MagicMock()
    mock_module.indicator = MagicMock()
    mock_module.order_target = Mock()
    mock_module.order_value = Mock()
    mock_module.history = Mock()
    mock_module.get_security_info = Mock()
    mock_module.datetime = __import__('datetime')
    mock_module.record = Mock()
    return mock_module


@pytest.fixture
def mock_g():
    g = SimpleNamespace()
    g.stock_num = 10
    g.month = 1
    g.hold_list = []
    g.high_limit_list = []
    return g


@pytest.fixture
def mock_context():
    context = SimpleNamespace()
    context.previous_date = datetime(2024, 1, 15)
    context.current_dt = datetime(2024, 1, 16, 9, 30)
    context.run_params = SimpleNamespace(type='backtest')
    portfolio = SimpleNamespace()
    portfolio.available_cash = 1000000
    portfolio.positions = {}
    portfolio.total_value = 1000000
    context.portfolio = portfolio
    return context


class TestStrategy19ValueInvest:
    def test_initialize(self, mock_jqdata_module, mock_context, mock_g):
        with patch.dict(sys.modules, {'jqdata': mock_jqdata_module}):
            import latest_strategy_19_高股息低市盈率稳健增长的价投策略 as strategy
            strategy.g = mock_g
            strategy.initialize(mock_context)
            mock_jqdata_module.set_benchmark.assert_called()
            mock_jqdata_module.log.set_level.assert_called()

    def test_before_trading_start(self, mock_jqdata_module, mock_context, mock_g):
        with patch.dict(sys.modules, {'jqdata': mock_jqdata_module}):
            import latest_strategy_19_高股息低市盈率稳健增长的价投策略 as strategy
            strategy.g = mock_g
            strategy.g.hold_list = []
            strategy.g.high_limit_list = []
            mock_context.portfolio.positions = {}
            with patch.object(strategy, 'prepare_stock_list', return_value=None):
                strategy.before_trading_start(mock_context)

    def test_prepare_stock_list_empty_positions(self, mock_jqdata_module, mock_context, mock_g):
        with patch.dict(sys.modules, {'jqdata': mock_jqdata_module}):
            import latest_strategy_19_高股息低市盈率稳健增长的价投策略 as strategy
            strategy.g = mock_g
            mock_context.portfolio.positions = {}
            strategy.prepare_stock_list(mock_context)
            assert strategy.g.hold_list == []
            assert strategy.g.high_limit_list == []

    def test_prepare_stock_list_with_positions(self, mock_jqdata_module, mock_context, mock_g):
        with patch.dict(sys.modules, {'jqdata': mock_jqdata_module}):
            import latest_strategy_19_高股息低市盈率稳健增长的价投策略 as strategy
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

    def test_filter_kcbj_stock(self, mock_jqdata_module):
        with patch.dict(sys.modules, {'jqdata': mock_jqdata_module}):
            import latest_strategy_19_高股息低市盈率稳健增长的价投策略 as strategy
            stock_list = ['000001.XSHE', '688001.XSHG', '430001.XSHE', '830001.XSHE']
            result = strategy.filter_kcbj_stock(stock_list)
            assert '000001.XSHE' in result
            assert '688001.XSHG' not in result
            assert '430001.XSHE' not in result
            assert '830001.XSHE' not in result

    def test_filter_paused_stock(self, mock_jqdata_module):
        with patch.dict(sys.modules, {'jqdata': mock_jqdata_module}):
            import latest_strategy_19_高股息低市盈率稳健增长的价投策略 as strategy
            mock_current_data = {
                '000001.XSHE': SimpleNamespace(paused=False),
                '000002.XSHE': SimpleNamespace(paused=True),
            }
            with patch.object(strategy, 'get_current_data', return_value=mock_current_data):
                stock_list = ['000001.XSHE', '000002.XSHE']
                result = strategy.filter_paused_stock(stock_list)
                assert '000001.XSHE' in result
                assert '000002.XSHE' not in result

    def test_filter_st_stock(self, mock_jqdata_module):
        with patch.dict(sys.modules, {'jqdata': mock_jqdata_module}):
            import latest_strategy_19_高股息低市盈率稳健增长的价投策略 as strategy
            mock_current_data = {
                '000001.XSHE': SimpleNamespace(is_st=False, name='平安银行'),
                '000002.XSHE': SimpleNamespace(is_st=True, name='ST万科'),
            }
            with patch.object(strategy, 'get_current_data', return_value=mock_current_data):
                stock_list = ['000001.XSHE', '000002.XSHE']
                result = strategy.filter_st_stock(stock_list)
                assert '000001.XSHE' in result
                assert '000002.XSHE' not in result

    def test_filter_new_stock(self, mock_jqdata_module, mock_context):
        with patch.dict(sys.modules, {'jqdata': mock_jqdata_module}):
            import latest_strategy_19_高股息低市盈率稳健增长的价投策略 as strategy
            mock_security_info = SimpleNamespace(start_date=datetime(2023, 1, 1))
            with patch.object(strategy, 'get_security_info', return_value=mock_security_info):
                stock_list = ['000001.XSHE']
                result = strategy.filter_new_stock(mock_context, stock_list)
                assert isinstance(result, list)

    def test_filter_limit_stock(self, mock_jqdata_module, mock_context):
        with patch.dict(sys.modules, {'jqdata': mock_jqdata_module}):
            import latest_strategy_19_高股息低市盈率稳健增长的价投策略 as strategy
            mock_current_data = {
                '000001.XSHE': SimpleNamespace(low_limit=9.0, high_limit=10.0),
            }
            mock_history = {'000001.XSHE': [9.5]}
            with patch.object(strategy, 'get_current_data', return_value=mock_current_data):
                with patch.object(strategy, 'history', return_value=mock_history):
                    stock_list = ['000001.XSHE']
                    result = strategy.filter_limit_stock(mock_context, stock_list)
                    assert isinstance(result, list)

    def test_check_limit_up_empty_list(self, mock_jqdata_module, mock_context, mock_g):
        with patch.dict(sys.modules, {'jqdata': mock_jqdata_module}):
            import latest_strategy_19_高股息低市盈率稳健增长的价投策略 as strategy
            strategy.g = mock_g
            strategy.g.high_limit_list = []
            strategy.check_limit_up(mock_context)

    def test_check_limit_up_with_list(self, mock_jqdata_module, mock_context, mock_g):
        with patch.dict(sys.modules, {'jqdata': mock_jqdata_module}):
            import latest_strategy_19_高股息低市盈率稳健增长的价投策略 as strategy
            strategy.g = mock_g
            strategy.g.high_limit_list = ['000001.XSHE']
            mock_current_data = {'000001.XSHE': SimpleNamespace(last_price=9.5, high_limit=10.0)}
            with patch.object(strategy, 'get_current_data', return_value=mock_current_data):
                with patch.object(strategy, 'order_target', return_value=Mock()):
                    strategy.check_limit_up(mock_context)

    def test_get_dividend_ratio_filter_list(self, mock_jqdata_module, mock_context):
        with patch.dict(sys.modules, {'jqdata': mock_jqdata_module}):
            import latest_strategy_19_高股息低市盈率稳健增长的价投策略 as strategy
            mock_dividend_df = pd.DataFrame({
                'code': ['000001.XSHE'],
                'a_registration_date': [datetime(2023, 6, 1)],
                'bonus_amount_rmb': [100]
            })
            mock_cap_df = pd.DataFrame({
                'code': ['000001.XSHE'],
                'market_cap': [1000]
            })
            with patch.object(strategy, 'finance.run_query', return_value=mock_dividend_df):
                with patch.object(strategy, 'get_fundamentals', return_value=mock_cap_df):
                    result = strategy.get_dividend_ratio_filter_list(mock_context, ['000001.XSHE'], False, 0, 0.1)
                    assert isinstance(result, list)

    def test_choice_try_A(self, mock_jqdata_module, mock_context):
        with patch.dict(sys.modules, {'jqdata': mock_jqdata_module}):
            import latest_strategy_19_高股息低市盈率稳健增长的价投策略 as strategy
            mock_dividend_result = ['000001.XSHE']
            mock_fundamentals_df = pd.DataFrame({'code': ['000001.XSHE']})
            with patch.object(strategy, 'get_dividend_ratio_filter_list', return_value=mock_dividend_result):
                with patch.object(strategy, 'get_fundamentals', return_value=mock_fundamentals_df):
                    result = strategy.choice_try_A(mock_context, ['000001.XSHE'])
                    assert isinstance(result, list)

    def test_slist(self, mock_jqdata_module, mock_context):
        with patch.dict(sys.modules, {'jqdata': mock_jqdata_module}):
            import latest_strategy_19_高股息低市盈率稳健增长的价投策略 as strategy
            mock_current_data = {'000001.XSHE': SimpleNamespace(last_price=10.0)}
            mock_fundamentals_df = pd.DataFrame({
                'market_cap': [1000],
                'circulating_market_cap': [800],
                'pe_ratio': [10.0]
            })
            mock_security_info = SimpleNamespace(display_name='平安银行')
            with patch.object(strategy, 'get_current_data', return_value=mock_current_data):
                with patch.object(strategy, 'get_fundamentals', return_value=mock_fundamentals_df):
                    with patch.object(strategy, 'get_security_info', return_value=mock_security_info):
                        strategy.slist(mock_context, ['000001.XSHE'])

    def test_my_Trader_sell(self, mock_jqdata_module, mock_context, mock_g):
        with patch.dict(sys.modules, {'jqdata': mock_jqdata_module}):
            import latest_strategy_19_高股息低市盈率稳健增长的价投策略 as strategy
            strategy.g = mock_g
            position = SimpleNamespace()
            mock_context.portfolio.positions = {'000002.XSHE': position}
            mock_stocks = ['000001.XSHE']
            mock_current_data = {
                '000001.XSHE': SimpleNamespace(name='平安银行', last_price=10.0, high_limit=10.5),
                '000002.XSHE': SimpleNamespace(name='万科A', last_price=9.0, high_limit=10.0)
            }
            with patch.object(strategy, 'get_all_securities', return_value=pd.DataFrame(index=['000001.XSHE'])):
                with patch.object(strategy, 'filter_kcbj_stock', return_value=['000001.XSHE']):
                    with patch.object(strategy, 'filter_st_stock', return_value=['000001.XSHE']):
                        with patch.object(strategy, 'filter_new_stock', return_value=['000001.XSHE']):
                            with patch.object(strategy, 'choice_try_A', return_value=['000001.XSHE']):
                                with patch.object(strategy, 'filter_paused_stock', return_value=['000001.XSHE']):
                                    with patch.object(strategy, 'filter_limit_stock', return_value=['000001.XSHE']):
                                        with patch.object(strategy, 'get_current_data', return_value=mock_current_data):
                                            with patch.object(strategy, 'slist', return_value=None):
                                                with patch.object(strategy, 'order_target', return_value=Mock()):
                                                    with patch.object(strategy, 'order_value', return_value=Mock()):
                                                        strategy.my_Trader(mock_context)

    def test_handle_data(self, mock_jqdata_module, mock_context, mock_g):
        with patch.dict(sys.modules, {'jqdata': mock_jqdata_module}):
            import latest_strategy_19_高股息低市盈率稳健增长的价投策略 as strategy
            strategy.g = mock_g
            strategy.g.month = 2
            mock_context.current_dt = datetime(2024, 2, 16, 9, 30)
            with patch.object(strategy, 'my_Trader', return_value=None):
                with patch.object(strategy, 'check_limit_up', return_value=None):
                    strategy.handle_data(mock_context, None)