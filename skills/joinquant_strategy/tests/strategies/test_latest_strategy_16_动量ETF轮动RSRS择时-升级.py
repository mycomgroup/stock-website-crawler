import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from module_loader import load_data_module, load_strategy_module
import pytest
import sys
import numpy as np
from unittest.mock import MagicMock, patch, Mock
from types import SimpleNamespace
from datetime import datetime

sys.path.insert(0, '/Users/yuping/Downloads/git/stock-website-crawler/strategies/misc_research/joinquant_strategy')


@pytest.fixture
def mock_jqdata_module():
    mock_module = MagicMock()
    mock_module.set_benchmark = Mock()
    mock_module.set_option = Mock()
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
    mock_module.order_target_value = Mock()
    mock_module.attribute_history = Mock()
    return mock_module


@pytest.fixture
def mock_kalman_module():
    mock_module = MagicMock()
    mock_module.KalmanFilter = Mock()
    return mock_module


@pytest.fixture
def mock_g():
    g = SimpleNamespace()
    g.stock_pool = ['510050.XSHG', '159928.XSHE', '510300.XSHG', '159949.XSHE', '510500.XSHG', '159915.XSHE']
    g.stock_num = 1
    g.momentum_day = 10
    g.ref_stock = '000300.XSHG'
    g.N = 18
    g.M = 1100
    g.score_threshold = 0.7
    g.slope_series = [0.5] * 1100
    g.checktime = '13:00'
    g.checktime2 = '13:50'
    g.hold = ''
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


class TestStrategy16RSRS:
    def test_get_ols(self, mock_jqdata_module):
        with patch.dict(sys.modules, {'jqdata': mock_jqdata_module, 'pykalman': MagicMock()}):
            module = load_strategy_module("latest_strategy_16_动量ETF轮动RSRS择时-升级")
            x = np.array([1, 2, 3, 4, 5])
            y = np.array([2, 4, 6, 8, 10])
            intercept, slope, r2 = strategy.get_ols(x, y)
            assert slope > 0
            assert r2 > 0.9

    def test_get_zscore(self, mock_jqdata_module):
        with patch.dict(sys.modules, {'jqdata': mock_jqdata_module, 'pykalman': MagicMock()}):
            module = load_strategy_module("latest_strategy_16_动量ETF轮动RSRS择时-升级")
            slope_series = [0.5, 0.6, 0.7, 0.8, 0.9, 1.0]
            zscore = strategy.get_zscore(slope_series)
            assert isinstance(zscore, float)

    def test_initial_slope_series(self, mock_jqdata_module, mock_g):
        with patch.dict(sys.modules, {'jqdata': mock_jqdata_module, 'pykalman': MagicMock()}):
            module = load_strategy_module("latest_strategy_16_动量ETF轮动RSRS择时-升级")
            strategy.g = mock_g
            mock_data = SimpleNamespace()
            mock_data.low = np.array([9.0] * (strategy.g.N + strategy.g.M))
            mock_data.high = np.array([10.0] * (strategy.g.N + strategy.g.M))
            with patch.object(strategy, 'attribute_history', return_value=mock_data):
                result = strategy.initial_slope_series()
                assert isinstance(result, list)

    def test_get_timing_signal_buy(self, mock_jqdata_module, mock_g):
        with patch.dict(sys.modules, {'jqdata': mock_jqdata_module, 'pykalman': MagicMock()}):
            module = load_strategy_module("latest_strategy_16_动量ETF轮动RSRS择时-升级")
            strategy.g = mock_g
            mock_data = SimpleNamespace()
            mock_data.low = np.array([9.0] * 18)
            mock_data.high = np.array([10.0] * 18)
            mock_data.close = np.array([10.0] * 62)
            mock_data.volume = np.array([1000000] * 18)
            with patch.object(strategy, 'attribute_history', return_value=mock_data):
                signal = strategy.get_timing_signal(mock_context, '000300.XSHG')
                assert signal in ['BUY', 'SELL', 'KEEP']

    def test_get_rank(self, mock_jqdata_module, mock_g, mock_context):
        with patch.dict(sys.modules, {'jqdata': mock_jqdata_module, 'pykalman': MagicMock()}):
            module = load_strategy_module("latest_strategy_16_动量ETF轮动RSRS择时-升级")
            strategy.g = mock_g
            mock_data = SimpleNamespace()
            mock_data.close = np.array([10.0] * 100)
            with patch.object(strategy, 'attribute_history', return_value=mock_data):
                with patch.object(strategy, 'kalman_filter', return_value=np.array([1.0] * 20)):
                    result = strategy.get_rank(mock_context, strategy.g.stock_pool)
                    assert isinstance(result, list)

    def test_hold_check_no_positions(self, mock_jqdata_module, mock_g, mock_context):
        with patch.dict(sys.modules, {'jqdata': mock_jqdata_module, 'pykalman': MagicMock()}):
            module = load_strategy_module("latest_strategy_16_动量ETF轮动RSRS择时-升级")
            strategy.g = mock_g
            mock_context.portfolio.positions = {}
            strategy.hold_check(mock_context)

    def test_hold_check_with_positions(self, mock_jqdata_module, mock_g, mock_context):
        with patch.dict(sys.modules, {'jqdata': mock_jqdata_module, 'pykalman': MagicMock()}):
            module = load_strategy_module("latest_strategy_16_动量ETF轮动RSRS择时-升级")
            strategy.g = mock_g
            strategy.g.checktime = '13:00'
            mock_context.current_dt = datetime(2024, 1, 16, 13, 0)
            position = SimpleNamespace()
            mock_context.portfolio.positions = {'510300.XSHG': position}
            mock_attr_data = SimpleNamespace()
            mock_attr_data.close = np.array([10.0] * 22)
            with patch.object(strategy, 'attribute_history', return_value=mock_attr_data):
                with patch.object(strategy, 'order_target_value', return_value=Mock()):
                    strategy.hold_check(mock_context)

    def test_order_target_value_(self, mock_jqdata_module):
        with patch.dict(sys.modules, {'jqdata': mock_jqdata_module, 'pykalman': MagicMock()}):
            module = load_strategy_module("latest_strategy_16_动量ETF轮动RSRS择时-升级")
            mock_order = Mock()
            mock_order.filled = 100
            with patch.object(strategy, 'order_target_value', return_value=mock_order):
                result = strategy.order_target_value_('510300.XSHG', 10000)
                assert result is not None

    def test_open_position_success(self, mock_jqdata_module):
        with patch.dict(sys.modules, {'jqdata': mock_jqdata_module, 'pykalman': MagicMock()}):
            module = load_strategy_module("latest_strategy_16_动量ETF轮动RSRS择时-升级")
            mock_order = Mock()
            mock_order.filled = 100
            with patch.object(strategy, 'order_target_value_', return_value=mock_order):
                result = strategy.open_position('510300.XSHG', 10000)
                assert result is True

    def test_open_position_failure(self, mock_jqdata_module):
        with patch.dict(sys.modules, {'jqdata': mock_jqdata_module, 'pykalman': MagicMock()}):
            module = load_strategy_module("latest_strategy_16_动量ETF轮动RSRS择时-升级")
            with patch.object(strategy, 'order_target_value_', return_value=None):
                result = strategy.open_position('510300.XSHG', 10000)
                assert result is False

    def test_close_position_success(self, mock_jqdata_module):
        with patch.dict(sys.modules, {'jqdata': mock_jqdata_module, 'pykalman': MagicMock()}):
            module = load_strategy_module("latest_strategy_16_动量ETF轮动RSRS择时-升级")
            position = SimpleNamespace(security='510300.XSHG')
            mock_order = Mock()
            mock_order.status = 'held'
            mock_order.filled = 100
            mock_order.amount = 100
            with patch.object(strategy, 'order_target_value_', return_value=mock_order):
                result = strategy.close_position(position)
                assert result is True

    def test_close_position_failure(self, mock_jqdata_module):
        with patch.dict(sys.modules, {'jqdata': mock_jqdata_module, 'pykalman': MagicMock()}):
            module = load_strategy_module("latest_strategy_16_动量ETF轮动RSRS择时-升级")
            position = SimpleNamespace(security='510300.XSHG')
            with patch.object(strategy, 'order_target_value_', return_value=None):
                result = strategy.close_position(position)
                assert result is False

    def test_adjust_position(self, mock_jqdata_module, mock_context, mock_g):
        with patch.dict(sys.modules, {'jqdata': mock_jqdata_module, 'pykalman': MagicMock()}):
            module = load_strategy_module("latest_strategy_16_动量ETF轮动RSRS择时-升级")
            strategy.g = mock_g
            mock_context.portfolio.positions = {}
            buy_stocks = ['510300.XSHG', 0.5]
            with patch.object(strategy, 'close_position', return_value=True):
                with patch.object(strategy, 'open_position', return_value=True):
                    strategy.adjust_position(mock_context, buy_stocks)

    def test_my_trade_sell_signal(self, mock_jqdata_module, mock_context, mock_g):
        with patch.dict(sys.modules, {'jqdata': mock_jqdata_module, 'pykalman': MagicMock()}):
            module = load_strategy_module("latest_strategy_16_动量ETF轮动RSRS择时-升级")
            strategy.g = mock_g
            mock_context.current_dt = datetime(2024, 1, 16, 9, 30)
            mock_rank_result = ['510300.XSHG', 0.5]
            mock_signal_result = 'SELL'
            position = SimpleNamespace(security='510300.XSHG')
            mock_context.portfolio.positions = {'510300.XSHG': position}
            with patch.object(strategy, 'get_rank', return_value=mock_rank_result):
                with patch.object(strategy, 'get_timing_signal', return_value=mock_signal_result):
                    with patch.object(strategy, 'close_position', return_value=True):
                        strategy.my_trade(mock_context)

    def test_my_trade_buy_signal(self, mock_jqdata_module, mock_context, mock_g):
        with patch.dict(sys.modules, {'jqdata': mock_jqdata_module, 'pykalman': MagicMock()}):
            module = load_strategy_module("latest_strategy_16_动量ETF轮动RSRS择时-升级")
            strategy.g = mock_g
            mock_context.current_dt = datetime(2024, 1, 16, 9, 30)
            mock_rank_result = ['510300.XSHG', 0.5]
            mock_signal_result = 'BUY'
            mock_context.portfolio.positions = {}
            with patch.object(strategy, 'get_rank', return_value=mock_rank_result):
                with patch.object(strategy, 'get_timing_signal', return_value=mock_signal_result):
                    with patch.object(strategy, 'adjust_position', return_value=None):
                        strategy.my_trade(mock_context)

    def test_check_lose(self, mock_jqdata_module, mock_context, mock_g):
        with patch.dict(sys.modules, {'jqdata': mock_jqdata_module, 'pykalman': MagicMock()}):
            module = load_strategy_module("latest_strategy_16_动量ETF轮动RSRS择时-升级")
            strategy.g = mock_g
            position = SimpleNamespace()
            position.security = '510300.XSHG'
            position.avg_cost = 10.0
            position.price = 1.0
            position.value = 10000
            position.total_amount = 1000
            mock_context.portfolio.positions = {'510300.XSHG': position}
            with patch.object(strategy, 'order_target_value', return_value=Mock()):
                strategy.check_lose(mock_context)

    def test_kalman_filter(self, mock_jqdata_module, mock_kalman_module):
        with patch.dict(sys.modules, {'jqdata': mock_jqdata_module, 'pykalman': mock_kalman_module}):
            module = load_strategy_module("latest_strategy_16_动量ETF轮动RSRS择时-升级")
            observations = np.array([1.0, 1.01, 1.02, 1.03, 1.04])
            mock_kf = Mock()
            mock_kf.smooth = Mock(return_value=(np.array([1.0, 1.01, 1.02, 1.03, 1.04]), np.array([0.1] * 5)))
            mock_kalman_module.KalmanFilter = Mock(return_value=mock_kf)
            result = strategy.kalman_filter(observations, damping=1)
            assert isinstance(result, np.ndarray)