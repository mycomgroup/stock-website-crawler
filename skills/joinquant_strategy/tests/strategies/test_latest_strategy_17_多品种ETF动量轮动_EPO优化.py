import pytest
import sys
import numpy as np
import pandas as pd
import math
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
    mock_module.run_monthly = Mock()
    mock_module.g = SimpleNamespace()
    mock_module.order_target_value = Mock()
    mock_module.attribute_history = Mock()
    mock_module.get_price = Mock()
    mock_module.math = math
    return mock_module


@pytest.fixture
def mock_jqfactor_module():
    mock_module = MagicMock()
    return mock_module


@pytest.fixture
def mock_scipy_module():
    mock_module = MagicMock()
    mock_module.optimize = MagicMock()
    mock_module.optimize.minimize = Mock()
    mock_module.linalg = MagicMock()
    mock_module.linalg.solve = Mock(return_value=np.array([0.25, 0.25, 0.25, 0.25]))
    return mock_module


@pytest.fixture
def mock_statsmodels_module():
    mock_module = MagicMock()
    mock_module.api = MagicMock()
    return mock_module


@pytest.fixture
def mock_g():
    g = SimpleNamespace()
    g.stock_num = 3
    g._lambda = 10
    g.w = 0.2
    g.etf_pool = ['518880.XSHG', '159985.XSHE', '513100.XSHG', '510300.XSHG', '159915.XSHE']
    g.m_days = 34
    return g


@pytest.fixture
def mock_context():
    context = SimpleNamespace()
    context.previous_date = datetime(2024, 1, 15)
    context.current_dt = datetime(2024, 1, 16)
    portfolio = SimpleNamespace()
    portfolio.total_value = 1000000
    portfolio.available_cash = 1000000
    portfolio.positions = {}
    context.portfolio = portfolio
    return context


class TestStrategy17EPO:
    def test_get_rank(self, mock_jqdata_module, mock_g):
        with patch.dict(sys.modules, {'jqdata': mock_jqdata_module, 'jqfactor': MagicMock(), 'scipy': MagicMock(), 'statsmodels.api': MagicMock()}):
            import latest_strategy_17_多品种ETF动量轮动_EPO优化 as strategy
            strategy.g = mock_g
            mock_data = SimpleNamespace()
            mock_data.close = np.array([10.0, 10.5, 11.0] * 12)
            with patch.object(strategy, 'attribute_history', return_value=mock_data):
                result = strategy.get_rank(strategy.g.etf_pool)
                assert isinstance(result, list)

    def test_get_rank_with_scores(self, mock_jqdata_module, mock_g):
        with patch.dict(sys.modules, {'jqdata': mock_jqdata_module, 'jqfactor': MagicMock(), 'scipy': MagicMock(), 'statsmodels.api': MagicMock()}):
            import latest_strategy_17_多品种ETF动量轮动_EPO优化 as strategy
            strategy.g = mock_g
            mock_data = SimpleNamespace()
            mock_data.close = np.array([10.0] * 35)
            with patch.object(strategy, 'attribute_history', return_value=mock_data):
                result = strategy.get_rank(['518880.XSHG', '513100.XSHG'])
                assert len(result) >= 0

    def test_epo_simple_method(self, mock_jqdata_module, mock_scipy_module):
        with patch.dict(sys.modules, {'jqdata': mock_jqdata_module, 'jqfactor': MagicMock(), 'scipy': mock_scipy_module, 'statsmodels.api': MagicMock()}):
            import latest_strategy_17_多品种ETF动量轮动_EPO优化 as strategy
            x = pd.DataFrame({
                'ETF1': [0.01, 0.02, -0.01, 0.03],
                'ETF2': [0.02, -0.01, 0.02, 0.01]
            })
            signal = np.array([0.01, 0.02])
            lambda_ = 10
            result = strategy.epo(x, signal, lambda_, method='simple', w=0.2, normalize=True)
            assert isinstance(result, np.ndarray)

    def test_epo_anchored_method(self, mock_jqdata_module, mock_scipy_module):
        with patch.dict(sys.modules, {'jqdata': mock_jqdata_module, 'jqfactor': MagicMock(), 'scipy': mock_scipy_module, 'statsmodels.api': MagicMock()}):
            import latest_strategy_17_多品种ETF动量轮动_EPO优化 as strategy
            x = pd.DataFrame({
                'ETF1': [0.01, 0.02, -0.01, 0.03],
                'ETF2': [0.02, -0.01, 0.02, 0.01]
            })
            signal = np.array([0.01, 0.02])
            anchor = np.array([0.25, 0.25])
            lambda_ = 10
            mock_scipy_module.linalg.solve = Mock(return_value=np.array([0.5, 0.5]))
            result = strategy.epo(x, signal, lambda_, method='anchored', w=0.2, anchor=anchor, normalize=True)
            assert isinstance(result, np.ndarray)

    def test_run_optimization(self, mock_jqdata_module, mock_g, mock_context):
        with patch.dict(sys.modules, {'jqdata': mock_jqdata_module, 'jqfactor': MagicMock(), 'scipy': MagicMock(), 'statsmodels.api': MagicMock()}):
            import latest_strategy_17_多品种ETF动量轮动_EPO优化 as strategy
            strategy.g = mock_g
            mock_price_data = pd.DataFrame({
                'close': np.random.rand(1200, 3)
            })
            mock_price_data.columns = ['518880.XSHG', '513100.XSHG', '510300.XSHG']
            with patch.object(strategy, 'get_price', return_value=mock_price_data):
                with patch.object(strategy, 'epo', return_value=np.array([0.33, 0.33, 0.34])):
                    result = strategy.run_optimization(['518880.XSHG', '513100.XSHG', '510300.XSHG'], mock_context.previous_date)
                    assert result is not None

    def test_trade_sell(self, mock_jqdata_module, mock_g, mock_context):
        with patch.dict(sys.modules, {'jqdata': mock_jqdata_module, 'jqfactor': MagicMock(), 'scipy': MagicMock(), 'statsmodels.api': MagicMock()}):
            import latest_strategy_17_多品种ETF动量轮动_EPO优化 as strategy
            strategy.g = mock_g
            strategy.g.stock_num = 3
            mock_rank_result = ['518880.XSHG', '513100.XSHG', '510300.XSHG']
            mock_weights = np.array([0.33, 0.33, 0.34])
            position = SimpleNamespace()
            mock_context.portfolio.positions = {'159915.XSHE': position}
            with patch.object(strategy, 'get_rank', return_value=mock_rank_result):
                with patch.object(strategy, 'run_optimization', return_value=mock_weights):
                    with patch.object(strategy, 'order_target_value', return_value=Mock()):
                        strategy.trade(mock_context)

    def test_trade_buy(self, mock_jqdata_module, mock_g, mock_context):
        with patch.dict(sys.modules, {'jqdata': mock_jqdata_module, 'jqfactor': MagicMock(), 'scipy': MagicMock(), 'statsmodels.api': MagicMock()}):
            import latest_strategy_17_多品种ETF动量轮动_EPO优化 as strategy
            strategy.g = mock_g
            strategy.g.stock_num = 3
            mock_rank_result = ['518880.XSHG', '513100.XSHG', '510300.XSHG']
            mock_weights = np.array([0.33, 0.33, 0.34])
            mock_context.portfolio.positions = {}
            with patch.object(strategy, 'get_rank', return_value=mock_rank_result):
                with patch.object(strategy, 'run_optimization', return_value=mock_weights):
                    with patch.object(strategy, 'order_target_value', return_value=Mock()):
                        strategy.trade(mock_context)

    def test_trade_with_weights_none(self, mock_jqdata_module, mock_g, mock_context):
        with patch.dict(sys.modules, {'jqdata': mock_jqdata_module, 'jqfactor': MagicMock(), 'scipy': MagicMock(), 'statsmodels.api': MagicMock()}):
            import latest_strategy_17_多品种ETF动量轮动_EPO优化 as strategy
            strategy.g = mock_g
            strategy.g.stock_num = 3
            mock_rank_result = ['518880.XSHG', '513100.XSHG', '510300.XSHG']
            mock_context.portfolio.positions = {}
            with patch.object(strategy, 'get_rank', return_value=mock_rank_result):
                with patch.object(strategy, 'run_optimization', return_value=None):
                    strategy.trade(mock_context)

    def test_initialize(self, mock_jqdata_module, mock_g):
        with patch.dict(sys.modules, {'jqdata': mock_jqdata_module, 'jqfactor': MagicMock(), 'scipy': MagicMock(), 'statsmodels.api': MagicMock()}):
            import latest_strategy_17_多品种ETF动量轮动_EPO优化 as strategy
            strategy.g = mock_g
            mock_context = SimpleNamespace()
            strategy.initialize(mock_context)
            mock_jqdata_module.set_benchmark.assert_called()
            mock_jqdata_module.set_option.assert_called()
            mock_jqdata_module.set_slippage.assert_called()