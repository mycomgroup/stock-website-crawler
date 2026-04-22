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
    mock_module.log = MagicMock()
    mock_module.log.set_level = Mock()
    mock_module.run_daily = Mock()
    mock_module.g = SimpleNamespace()
    mock_module.order_target_value = Mock()
    mock_module.history = Mock()
    mock_module.attribute_history = Mock()
    mock_module.math = math
    return mock_module


@pytest.fixture
def mock_g():
    g = SimpleNamespace()
    g.etf_pool = ['512660.XSHG', '511010.XSHG', '510880.XSHG', '159915.XSHE', '513050.XSHG']
    g.m_days = 25
    return g


@pytest.fixture
def mock_context():
    context = SimpleNamespace()
    context.previous_date = datetime(2024, 1, 15)
    context.current_dt = datetime(2024, 1, 16, 10, 0)
    portfolio = SimpleNamespace()
    portfolio.total_value = 1000000
    portfolio.available_cash = 1000000
    portfolio.positions = {}
    context.portfolio = portfolio
    return context


class TestStrategy26Volatility:
    def test_min_corr(self, mock_jqdata_module, mock_g):
        with patch.dict(sys.modules, {'jqdata': mock_jqdata_module}):
            import latest_strategy_26_波动率过滤后相关性最小etf轮动 as strategy
            strategy.g = mock_g
            mock_history_data = pd.DataFrame({
                '512660.XSHG': np.random.rand(729),
                '511010.XSHG': np.random.rand(729),
                '510880.XSHG': np.random.rand(729),
                '159915.XSHE': np.random.rand(729),
                '513050.XSHG': np.random.rand(729)
            })
            with patch.object(strategy, 'history', return_value=mock_history_data):
                result = strategy.min_corr(strategy.g.etf_pool)
                assert isinstance(result, list)
                assert len(result) <= 4

    def test_min_corr_with_nans(self, mock_jqdata_module, mock_g):
        with patch.dict(sys.modules, {'jqdata': mock_jqdata_module}):
            import latest_strategy_26_波动率过滤后相关性最小etf轮动 as strategy
            strategy.g = mock_g
            mock_history_data = pd.DataFrame({
                '512660.XSHG': np.random.rand(729),
                '511010.XSHG': np.random.rand(729),
                '510880.XSHG': np.random.rand(729),
                '159915.XSHE': np.random.rand(729),
                '513050.XSHG': np.random.rand(729)
            })
            mock_history_data.iloc[100:105, 0] = np.nan
            with patch.object(strategy, 'history', return_value=mock_history_data):
                result = strategy.min_corr(strategy.g.etf_pool)
                assert isinstance(result, list)

    def test_get_rank(self, mock_jqdata_module, mock_g):
        with patch.dict(sys.modules, {'jqdata': mock_jqdata_module}):
            import latest_strategy_26_波动率过滤后相关性最小etf轮动 as strategy
            strategy.g = mock_g
            strategy.g.m_days = 25
            mock_attr_data = pd.DataFrame({'close': np.array([10.0, 10.5, 11.0] * 9)})
            with patch.object(strategy, 'attribute_history', return_value=mock_attr_data):
                result = strategy.get_rank(['512660.XSHG', '511010.XSHG'])
                assert isinstance(result, list)

    def test_get_rank_with_filtering(self, mock_jqdata_module, mock_g):
        with patch.dict(sys.modules, {'jqdata': mock_jqdata_module}):
            import latest_strategy_26_波动率过滤后相关性最小etf轮动 as strategy
            strategy.g = mock_g
            strategy.g.m_days = 25
            mock_attr_data = pd.DataFrame({'close': np.array([10.0] * 26)})
            with patch.object(strategy, 'attribute_history', return_value=mock_attr_data):
                result = strategy.get_rank(['512660.XSHG', '511010.XSHG'])
                assert isinstance(result, list)

    def test_trade_no_positions(self, mock_jqdata_module, mock_g, mock_context):
        with patch.dict(sys.modules, {'jqdata': mock_jqdata_module}):
            import latest_strategy_26_波动率过滤后相关性最小etf轮动 as strategy
            strategy.g = mock_g
            mock_context.portfolio.positions = {}
            mock_min_corr_result = ['512660.XSHG', '511010.XSHG']
            mock_rank_result = ['512660.XSHG']
            with patch.object(strategy, 'min_corr', return_value=mock_min_corr_result):
                with patch.object(strategy, 'get_rank', return_value=mock_rank_result):
                    with patch.object(strategy, 'order_target_value', return_value=Mock()):
                        strategy.trade(mock_context)

    def test_trade_with_positions_sell(self, mock_jqdata_module, mock_g, mock_context):
        with patch.dict(sys.modules, {'jqdata': mock_jqdata_module}):
            import latest_strategy_26_波动率过滤后相关性最小etf轮动 as strategy
            strategy.g = mock_g
            position = SimpleNamespace(total_amount=1000)
            mock_context.portfolio.positions = {'511010.XSHG': position}
            mock_min_corr_result = ['512660.XSHG', '511010.XSHG']
            mock_rank_result = ['512660.XSHG']
            with patch.object(strategy, 'min_corr', return_value=mock_min_corr_result):
                with patch.object(strategy, 'get_rank', return_value=mock_rank_result):
                    with patch.object(strategy, 'order_target_value', return_value=Mock()):
                        strategy.trade(mock_context)

    def test_trade_with_positions_continue_hold(self, mock_jqdata_module, mock_g, mock_context):
        with patch.dict(sys.modules, {'jqdata': mock_jqdata_module}):
            import latest_strategy_26_波动率过滤后相关性最小etf轮动 as strategy
            strategy.g = mock_g
            position = SimpleNamespace(total_amount=1000)
            mock_context.portfolio.positions = {'512660.XSHG': position}
            mock_min_corr_result = ['512660.XSHG', '511010.XSHG']
            mock_rank_result = ['512660.XSHG']
            with patch.object(strategy, 'min_corr', return_value=mock_min_corr_result):
                with patch.object(strategy, 'get_rank', return_value=mock_rank_result):
                    with patch.object(strategy, 'order_target_value', return_value=Mock()):
                        strategy.trade(mock_context)

    def test_trade_buy_more(self, mock_jqdata_module, mock_g, mock_context):
        with patch.dict(sys.modules, {'jqdata': mock_jqdata_module}):
            import latest_strategy_26_波动率过滤后相关性最小etf轮动 as strategy
            strategy.g = mock_g
            mock_context.portfolio.positions = {}
            mock_min_corr_result = ['512660.XSHG', '511010.XSHG', '510880.XSHG', '159915.XSHE']
            mock_rank_result = ['512660.XSHG', '511010.XSHG', '510880.XSHG', '159915.XSHE']
            with patch.object(strategy, 'min_corr', return_value=mock_min_corr_result):
                with patch.object(strategy, 'get_rank', return_value=mock_rank_result):
                    with patch.object(strategy, 'order_target_value', return_value=Mock()):
                        strategy.trade(mock_context)

    def test_initialize(self, mock_jqdata_module, mock_g):
        with patch.dict(sys.modules, {'jqdata': mock_jqdata_module}):
            import latest_strategy_26_波动率过滤后相关性最小etf轮动 as strategy
            strategy.g = mock_g
            mock_context = SimpleNamespace()
            strategy.initialize(mock_context)
            mock_jqdata_module.set_benchmark.assert_called()
            mock_jqdata_module.set_option.assert_called()
            mock_jqdata_module.run_daily.assert_called()