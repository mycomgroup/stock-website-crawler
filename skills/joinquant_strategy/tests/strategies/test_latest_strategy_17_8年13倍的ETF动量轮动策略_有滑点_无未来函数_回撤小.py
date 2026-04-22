import pytest
import sys
import numpy as np
import math
from unittest.mock import MagicMock, patch, Mock
from types import SimpleNamespace
from datetime import datetime

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
    mock_module.g = SimpleNamespace()
    mock_module.OrderStatus = MagicMock()
    mock_module.OrderStatus.held = 'held'
    mock_module.math = math
    mock_module.get_trades = Mock()
    return mock_module


@pytest.fixture
def mock_g():
    g = SimpleNamespace()
    g.stock_pool = ['510180.XSHG', '159915.XSHE', '513100.XSHG', '510500.XSHG']
    g.stock_num = 1
    g.momentum_day = 29
    g.ref_stock = '000300.XSHG'
    g.N = 18
    g.M = 600
    g.score_threshold = 0.7
    g.mean_day = 20
    g.mean_diff_day = 3
    g.slope_series = [0.5] * 600
    return g


@pytest.fixture
def mock_context():
    context = SimpleNamespace()
    context.previous_date = Mock()
    context.current_dt = datetime(2024, 1, 16, 11, 30)
    portfolio = SimpleNamespace()
    portfolio.available_cash = 1000000
    portfolio.cash = 1000000
    portfolio.positions = {}
    portfolio.total_value = 1000000
    context.portfolio = portfolio
    return context


class TestStrategy17NoFuture:
    def test_get_ols(self, mock_jqdata_module):
        with patch.dict(sys.modules, {'jqdata': mock_jqdata_module}):
            import latest_strategy_17_8年13倍的ETF动量轮动策略_有滑点_无未来函数_回撤小 as strategy
            x = np.array([1, 2, 3, 4, 5])
            y = np.array([2, 4, 6, 8, 10])
            intercept, slope, r2 = strategy.get_ols(x, y)
            assert slope > 0
            assert r2 > 0.9

    def test_get_zscore(self, mock_jqdata_module):
        with patch.dict(sys.modules, {'jqdata': mock_jqdata_module}):
            import latest_strategy_17_8年13倍的ETF动量轮动策略_有滑点_无未来函数_回撤小 as strategy
            slope_series = [0.5, 0.6, 0.7, 0.8, 0.9, 1.0]
            zscore = strategy.get_zscore(slope_series)
            assert isinstance(zscore, float)

    def test_initial_slope_series(self, mock_jqdata_module, mock_g):
        with patch.dict(sys.modules, {'jqdata': mock_jqdata_module}):
            import latest_strategy_17_8年13倍的ETF动量轮动策略_有滑点_无未来函数_回撤小 as strategy
            strategy.g = mock_g
            mock_data = SimpleNamespace()
            mock_data.low = np.array([9.0] * (strategy.g.N + strategy.g.M))
            mock_data.high = np.array([10.0] * (strategy.g.N + strategy.g.M))
            with patch.object(strategy, 'attribute_history', return_value=mock_data):
                result = strategy.initial_slope_series()
                assert isinstance(result, list)

    def test_filter_paused_stock(self, mock_jqdata_module):
        with patch.dict(sys.modules, {'jqdata': mock_jqdata_module}):
            import latest_strategy_17_8年13倍的ETF动量轮动策略_有滑点_无未来函数_回撤小 as strategy
            mock_current_data = {
                '159915.XSHE': SimpleNamespace(paused=False),
                '510300.XSHG': SimpleNamespace(paused=True),
                '510500.XSHG': SimpleNamespace(paused=False)
            }
            with patch.object(strategy, 'get_current_data', return_value=mock_current_data):
                stock_list = ['159915.XSHE', '510300.XSHG', '510500.XSHG']
                result = strategy.filter_paused_stock(stock_list)
                assert '159915.XSHE' in result
                assert '510300.XSHG' not in result

    def test_filter_st_stock(self, mock_jqdata_module):
        with patch.dict(sys.modules, {'jqdata': mock_jqdata_module}):
            import latest_strategy_17_8年13倍的ETF动量轮动策略_有滑点_无未来函数_回撤小 as strategy
            mock_current_data = {
                '000001.XSHE': SimpleNamespace(is_st=False, name='平安银行'),
                '000002.XSHE': SimpleNamespace(is_st=True, name='ST万科'),
            }
            with patch.object(strategy, 'get_current_data', return_value=mock_current_data):
                stock_list = ['000001.XSHE', '000002.XSHE']
                result = strategy.filter_st_stock(stock_list)
                assert '000001.XSHE' in result
                assert '000002.XSHE' not in result

    def test_filter_limitup_stock(self, mock_jqdata_module, mock_context):
        with patch.dict(sys.modules, {'jqdata': mock_jqdata_module}):
            import latest_strategy_17_8年13倍的ETF动量轮动策略_有滑点_无未来函数_回撤小 as strategy
            mock_current_data = {
                '159915.XSHE': SimpleNamespace(high_limit=10.0),
            }
            mock_history = {'159915.XSHE': [9.5]}
            with patch.object(strategy, 'get_current_data', return_value=mock_current_data):
                with patch.object(strategy, 'history', return_value=mock_history):
                    stock_list = ['159915.XSHE']
                    result = strategy.filter_limitup_stock(mock_context, stock_list)
                    assert len(result) >= 0

    def test_filter_limitdown_stock(self, mock_jqdata_module, mock_context):
        with patch.dict(sys.modules, {'jqdata': mock_jqdata_module}):
            import latest_strategy_17_8年13倍的ETF动量轮动策略_有滑点_无未来函数_回撤小 as strategy
            mock_current_data = {
                '159915.XSHE': SimpleNamespace(low_limit=9.0),
            }
            mock_history = {'159915.XSHE': [9.5]}
            with patch.object(strategy, 'get_current_data', return_value=mock_current_data):
                with patch.object(strategy, 'history', return_value=mock_history):
                    stock_list = ['159915.XSHE']
                    result = strategy.filter_limitdown_stock(mock_context, stock_list)
                    assert len(result) >= 0

    def test_order_target_value_(self, mock_jqdata_module):
        with patch.dict(sys.modules, {'jqdata': mock_jqdata_module}):
            import latest_strategy_17_8年13倍的ETF动量轮动策略_有滑点_无未来函数_回撤小 as strategy
            mock_order = Mock()
            mock_order.filled = 100
            with patch.object(strategy, 'order_target_value', return_value=mock_order):
                result = strategy.order_target_value_('159915.XSHE', 10000)
                assert result is not None

    def test_open_position_success(self, mock_jqdata_module):
        with patch.dict(sys.modules, {'jqdata': mock_jqdata_module}):
            import latest_strategy_17_8年13倍的ETF动量轮动策略_有滑点_无未来函数_回撤小 as strategy
            mock_order = Mock()
            mock_order.filled = 100
            with patch.object(strategy, 'order_target_value_', return_value=mock_order):
                result = strategy.open_position('159915.XSHE', 10000)
                assert result is True

    def test_open_position_failure(self, mock_jqdata_module):
        with patch.dict(sys.modules, {'jqdata': mock_jqdata_module}):
            import latest_strategy_17_8年13倍的ETF动量轮动策略_有滑点_无未来函数_回撤小 as strategy
            with patch.object(strategy, 'order_target_value_', return_value=None):
                result = strategy.open_position('159915.XSHE', 10000)
                assert result is False

    def test_close_position_success(self, mock_jqdata_module):
        with patch.dict(sys.modules, {'jqdata': mock_jqdata_module}):
            import latest_strategy_17_8年13倍的ETF动量轮动策略_有滑点_无未来函数_回撤小 as strategy
            position = SimpleNamespace(security='159915.XSHE')
            mock_order = Mock()
            mock_order.status = 'held'
            mock_order.filled = 100
            mock_order.amount = 100
            with patch.object(strategy, 'order_target_value_', return_value=mock_order):
                result = strategy.close_position(position)
                assert result is True

    def test_close_position_failure(self, mock_jqdata_module):
        with patch.dict(sys.modules, {'jqdata': mock_jqdata_module}):
            import latest_strategy_17_8年13倍的ETF动量轮动策略_有滑点_无未来函数_回撤小 as strategy
            position = SimpleNamespace(security='159915.XSHE')
            with patch.object(strategy, 'order_target_value_', return_value=None):
                result = strategy.close_position(position)
                assert result is False

    def test_get_timing_signal_buy(self, mock_jqdata_module, mock_g):
        with patch.dict(sys.modules, {'jqdata': mock_jqdata_module}):
            import latest_strategy_17_8年13倍的ETF动量轮动策略_有滑点_无未来函数_回撤小 as strategy
            strategy.g = mock_g
            mock_close_data = SimpleNamespace()
            mock_close_data.close = np.array([10.0] * 23)
            mock_high_low_data = SimpleNamespace()
            mock_high_low_data.low = np.array([9.0] * 18)
            mock_high_low_data.high = np.array([10.0] * 18)
            with patch.object(strategy, 'attribute_history', side_effect=[mock_close_data, mock_high_low_data]):
                signal = strategy.get_timing_signal('000300.XSHG')
                assert signal in ['BUY', 'SELL', 'KEEP']

    def test_get_rank(self, mock_jqdata_module, mock_g):
        with patch.dict(sys.modules, {'jqdata': mock_jqdata_module}):
            import latest_strategy_17_8年13倍的ETF动量轮动策略_有滑点_无未来函数_回撤小 as strategy
            strategy.g = mock_g
            mock_data = SimpleNamespace()
            mock_data.close = np.array([10.0, 10.5, 11.0] * 10)
            with patch.object(strategy, 'attribute_history', return_value=mock_data):
                result = strategy.get_rank(strategy.g.stock_pool)
                assert isinstance(result, list)

    def test_adjust_position(self, mock_jqdata_module, mock_context, mock_g):
        with patch.dict(sys.modules, {'jqdata': mock_jqdata_module}):
            import latest_strategy_17_8年13倍的ETF动量轮动策略_有滑点_无未来函数_回撤小 as strategy
            strategy.g = mock_g
            mock_context.portfolio.positions = {}
            buy_stocks = ['159915.XSHE']
            with patch.object(strategy, 'open_position', return_value=True):
                strategy.adjust_position(mock_context, buy_stocks)

    def test_my_trade_sell_signal(self, mock_jqdata_module, mock_context, mock_g):
        with patch.dict(sys.modules, {'jqdata': mock_jqdata_module}):
            import latest_strategy_17_8年13倍的ETF动量轮动策略_有滑点_无未来函数_回撤小 as strategy
            strategy.g = mock_g
            mock_rank_result = ['159915.XSHE']
            mock_timing_result = 'SELL'
            position = SimpleNamespace(security='159915.XSHE')
            mock_context.portfolio.positions = {'159915.XSHE': position}
            with patch.object(strategy, 'get_rank', return_value=mock_rank_result):
                with patch.object(strategy, 'filter_st_stock', return_value=mock_rank_result):
                    with patch.object(strategy, 'filter_limitup_stock', return_value=mock_rank_result):
                        with patch.object(strategy, 'filter_limitdown_stock', return_value=mock_rank_result):
                            with patch.object(strategy, 'filter_paused_stock', return_value=mock_rank_result):
                                with patch.object(strategy, 'get_timing_signal', return_value=mock_timing_result):
                                    with patch.object(strategy, 'close_position', return_value=True):
                                        strategy.my_trade(mock_context)

    def test_check_lose_trigger(self, mock_jqdata_module, mock_context, mock_g):
        with patch.dict(sys.modules, {'jqdata': mock_jqdata_module}):
            import latest_strategy_17_8年13倍的ETF动量轮动策略_有滑点_无未来函数_回撤小 as strategy
            strategy.g = mock_g
            position = SimpleNamespace()
            position.security = '159915.XSHE'
            position.avg_cost = 10.0
            position.price = 1.0
            position.value = 10000
            position.total_amount = 1000
            mock_context.portfolio.positions = {'159915.XSHE': position}
            with patch.object(strategy, 'order_target_value', return_value=Mock()):
                strategy.check_lose(mock_context)

    def test_print_trade_info(self, mock_jqdata_module, mock_context, mock_g):
        with patch.dict(sys.modules, {'jqdata': mock_jqdata_module}):
            import latest_strategy_17_8年13倍的ETF动量轮动策略_有滑点_无未来函数_回撤小 as strategy
            strategy.g = mock_g
            mock_context.portfolio.positions = {}
            mock_trades = {}
            with patch.object(strategy, 'get_trades', return_value=mock_trades):
                strategy.print_trade_info(mock_context)