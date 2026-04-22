import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from module_loader import load_data_module, load_strategy_module
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
    mock_module.run_daily = Mock()
    mock_module.g = SimpleNamespace()
    mock_module.OrderStatus = MagicMock()
    mock_module.OrderStatus.held = 'held'
    mock_module.send_message = Mock()
    mock_module.math = math
    return mock_module


@pytest.fixture
def mock_jqlib_module():
    mock_module = MagicMock()
    mock_module.technical_analysis = MagicMock()
    mock_module.technical_analysis.WR = Mock(return_value=({'000300.XSHG': 50}, {'000300.XSHG': 50}))
    return mock_module


@pytest.fixture
def mock_g():
    g = SimpleNamespace()
    g.stock_pool = ['510300.XSHG', '510050.XSHG', '159949.XSHE', '159928.XSHE']
    g.stock_num = 1
    g.momentum_day = 20
    g.ref_stock = '000300.XSHG'
    g.N = 18
    g.M = 600
    g.K = 8
    g.biasN = 90
    g.lossN = 20
    g.lossFactor = 1.005
    g.SwitchFactor = 1.04
    g.Motion_1diff = 19
    g.raiser_thr = 4.8
    g.hold_stock = 'null'
    g.score_thr = -0.68
    g.score_fall_thr = -0.43
    g.idex_slope_raise_thr = 12
    g.slope_series = [0.5] * 600
    g.rsrs_score_history = [0.5] * 8
    g.stock_motion = {'510300.XSHG': [0.5], '510050.XSHG': [0.5]}
    g.check_out_list = ['510300.XSHG', 0.5, 0.0]
    g.timing_signal = 'BUY'
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


class TestStrategy10:
    def test_get_ols(self, mock_jqdata_module):
        with patch.dict(sys.modules, {'jqdata': mock_jqdata_module}):
            module = load_strategy_module("latest_strategy_10_多因子宽基ETF择时轮动改进版-高收益大资金低回撤")
            x = np.array([1, 2, 3, 4, 5])
            y = np.array([2, 4, 6, 8, 10])
            intercept, slope, r2 = strategy.get_ols(x, y)
            assert slope > 0
            assert r2 > 0.9

    def test_get_zscore(self, mock_jqdata_module):
        with patch.dict(sys.modules, {'jqdata': mock_jqdata_module}):
            module = load_strategy_module("latest_strategy_10_多因子宽基ETF择时轮动改进版-高收益大资金低回撤")
            slope_series = [0.5, 0.6, 0.7, 0.8, 0.9, 1.0]
            zscore = strategy.get_zscore(slope_series)
            assert isinstance(zscore, float)

    def test_get_zscore_slope(self, mock_jqdata_module):
        with patch.dict(sys.modules, {'jqdata': mock_jqdata_module}):
            module = load_strategy_module("latest_strategy_10_多因子宽基ETF择时轮动改进版-高收益大资金低回撤")
            z_scores = np.array([0.1, 0.2, 0.3, 0.4, 0.5])
            slope = strategy.get_zscore_slope(z_scores)
            assert isinstance(slope, float)

    def test_open_position_success(self, mock_jqdata_module):
        with patch.dict(sys.modules, {'jqdata': mock_jqdata_module}):
            module = load_strategy_module("latest_strategy_10_多因子宽基ETF择时轮动改进版-高收益大资金低回撤")
            mock_order = Mock()
            mock_order.filled = 100
            with patch.object(strategy, 'order_target_value', return_value=mock_order):
                result = strategy.open_position('510300.XSHG', 10000)
                assert result is True

    def test_open_position_failure(self, mock_jqdata_module):
        with patch.dict(sys.modules, {'jqdata': mock_jqdata_module}):
            module = load_strategy_module("latest_strategy_10_多因子宽基ETF择时轮动改进版-高收益大资金低回撤")
            with patch.object(strategy, 'order_target_value', return_value=None):
                result = strategy.open_position('510300.XSHG', 10000)
                assert result is False

    def test_close_position_success(self, mock_jqdata_module):
        with patch.dict(sys.modules, {'jqdata': mock_jqdata_module}):
            module = load_strategy_module("latest_strategy_10_多因子宽基ETF择时轮动改进版-高收益大资金低回撤")
            position = SimpleNamespace(security='510300.XSHG')
            mock_order = Mock()
            mock_order.status = 'held'
            mock_order.filled = 100
            mock_order.amount = 100
            with patch.object(strategy, 'order_target_value', return_value=mock_order):
                result = strategy.close_position(position)
                assert result is True

    def test_close_position_failure(self, mock_jqdata_module):
        with patch.dict(sys.modules, {'jqdata': mock_jqdata_module}):
            module = load_strategy_module("latest_strategy_10_多因子宽基ETF择时轮动改进版-高收益大资金低回撤")
            position = SimpleNamespace(security='510300.XSHG')
            with patch.object(strategy, 'order_target_value', return_value=None):
                result = strategy.close_position(position)
                assert result is False

    def test_adjust_position(self, mock_jqdata_module, mock_context, mock_g):
        with patch.dict(sys.modules, {'jqdata': mock_jqdata_module}):
            module = load_strategy_module("latest_strategy_10_多因子宽基ETF择时轮动改进版-高收益大资金低回撤")
            strategy.g = mock_g
            mock_context.portfolio.positions = {}
            buy_stocks = ['510300.XSHG', 0.5, 0.0]
            with patch.object(strategy, 'close_position', return_value=True):
                with patch.object(strategy, 'open_position', return_value=True):
                    strategy.adjust_position(mock_context, buy_stocks)

    def test_buy_stocks(self, mock_jqdata_module, mock_context, mock_g):
        with patch.dict(sys.modules, {'jqdata': mock_jqdata_module}):
            module = load_strategy_module("latest_strategy_10_多因子宽基ETF择时轮动改进版-高收益大资金低回撤")
            strategy.g = mock_g
            mock_context.portfolio.positions = {}
            buy_stocks = ['510300.XSHG', 0.5, 0.0]
            with patch.object(strategy, 'open_position', return_value=True):
                strategy.buy_stocks(mock_context, buy_stocks)

    def test_check_lose_trigger(self, mock_jqdata_module, mock_context, mock_g):
        with patch.dict(sys.modules, {'jqdata': mock_jqdata_module}):
            module = load_strategy_module("latest_strategy_10_多因子宽基ETF择时轮动改进版-高收益大资金低回撤")
            strategy.g = mock_g
            position = SimpleNamespace()
            position.security = '510300.XSHG'
            position.avg_cost = 10.0
            position.price = 0.5
            position.value = 10000
            position.total_amount = 1000
            mock_context.portfolio.positions = {'510300.XSHG': position}
            with patch.object(strategy, 'order_target_value', return_value=Mock()):
                strategy.check_lose(mock_context)

    def test_pre_hold_check(self, mock_jqdata_module, mock_context, mock_g):
        with patch.dict(sys.modules, {'jqdata': mock_jqdata_module}):
            module = load_strategy_module("latest_strategy_10_多因子宽基ETF择时轮动改进版-高收益大资金低回撤")
            strategy.g = mock_g
            mock_attr_data = SimpleNamespace()
            mock_attr_data.close = np.array([10.0] * 22)
            mock_attr_data.man = np.array([0.9, 0.95, 1.0])
            position = SimpleNamespace(security='510300.XSHG')
            mock_context.portfolio.positions = {'510300.XSHG': position}
            with patch.object(strategy, 'attribute_history', return_value=mock_attr_data):
                strategy.pre_hold_check(mock_context)

    def test_hold_check_sell(self, mock_jqdata_module, mock_context, mock_g):
        with patch.dict(sys.modules, {'jqdata': mock_jqdata_module}):
            module = load_strategy_module("latest_strategy_10_多因子宽基ETF择时轮动改进版-高收益大资金低回撤")
            strategy.g = mock_g
            strategy.g.lossFactor = 1.005
            position = SimpleNamespace(security='510300.XSHG', closeable_amount=100)
            mock_context.portfolio.positions = {'510300.XSHG': position}
            mock_attr_data = SimpleNamespace()
            mock_attr_data.close = np.array([10.0] * 22)
            mock_attr_data.man = np.array([0.9, 0.95, 0.98])
            mock_yesterday_data = SimpleNamespace()
            mock_yesterday_data.close = np.array([10.0])
            mock_current_data = {'510300.XSHG': SimpleNamespace(last_price=9.5)}
            with patch.object(strategy, 'attribute_history', side_effect=[mock_yesterday_data, mock_attr_data]):
                with patch.object(strategy, 'get_current_data', return_value=mock_current_data):
                    with patch.object(strategy, 'order_target_value', return_value=Mock()):
                        strategy.hold_check(mock_context)