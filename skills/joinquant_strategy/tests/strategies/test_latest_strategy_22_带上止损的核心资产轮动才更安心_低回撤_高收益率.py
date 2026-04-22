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
    mock_module.run_daily = Mock()
    mock_module.g = SimpleNamespace()
    mock_module.order_target_value = Mock()
    mock_module.attribute_history = Mock()
    mock_module.record = Mock()
    mock_module.math = math
    return mock_module


@pytest.fixture
def mock_g():
    g = SimpleNamespace()
    g.etf_pool = ['518880.XSHG', '513100.XSHG', '159915.XSHE', '510180.XSHG']
    g.m_days = 25
    g.etf_info = {
        '518880.XSHG': [10.0] * 100,
        '513100.XSHG': [20.0] * 100,
        '159915.XSHE': [15.0] * 100,
        '510180.XSHG': [12.0] * 100
    }
    g.etf_pre = None
    return g


@pytest.fixture
def mock_context():
    context = SimpleNamespace()
    context.previous_date = datetime(2024, 1, 15)
    context.current_dt = datetime(2024, 1, 16, 9, 30)
    portfolio = SimpleNamespace()
    portfolio.total_value = 1000000
    portfolio.available_cash = 1000000
    portfolio.positions = {}
    context.portfolio = portfolio
    return context


class TestStrategy22CoreAssets:
    def test_initial_etf_info(self, mock_jqdata_module, mock_g):
        with patch.dict(sys.modules, {'jqdata': mock_jqdata_module}):
            import latest_strategy_22_带上止损的核心资产轮动才更安心_低回撤_高收益率 as strategy
            strategy.g = mock_g
            mock_attr_data = pd.DataFrame({'close': np.array([10.0] * 100)})
            with patch.object(strategy, 'attribute_history', return_value=mock_attr_data):
                result = strategy.initial_etf_info(['518880.XSHG'], 100)
                assert isinstance(result, dict)
                assert '518880.XSHG' in result

    def test_update_etf_table(self, mock_jqdata_module, mock_g, mock_context):
        with patch.dict(sys.modules, {'jqdata': mock_jqdata_module}):
            import latest_strategy_22_带上止损的核心资产轮动才更安心_低回撤_高收益率 as strategy
            strategy.g = mock_g
            strategy.g.etf_pool = ['518880.XSHG']
            strategy.g.etf_info = {'518880.XSHG': [10.0] * 100}
            mock_attr_data = pd.DataFrame({'close': [10.5]})
            with patch.object(strategy, 'attribute_history', return_value=mock_attr_data):
                strategy.update_etf_table(mock_context)
                assert len(strategy.g.etf_info['518880.XSHG']) == 100

    def test_evaluate_etf_worth_none(self, mock_jqdata_module, mock_g):
        with patch.dict(sys.modules, {'jqdata': mock_jqdata_module}):
            import latest_strategy_22_带上止损的核心资产轮动才更安心_低回撤_高收益率 as strategy
            strategy.g = mock_g
            result = strategy.evaluate_etf_worth(None, is_hold=1)
            assert result == 0

    def test_evaluate_etf_worth_hold_sell(self, mock_jqdata_module, mock_g):
        with patch.dict(sys.modules, {'jqdata': mock_jqdata_module}):
            import latest_strategy_22_带上止损的核心资产轮动才更安心_低回撤_高收益率 as strategy
            strategy.g = mock_g
            strategy.g.etf_info = {'518880.XSHG': [10.0, 10.5, 11.0, 11.5, 12.0] * 20}
            result = strategy.evaluate_etf_worth('518880.XSHG', is_hold=1)
            assert isinstance(result, int)
            assert result in [0, 1]

    def test_evaluate_etf_worth_buy(self, mock_jqdata_module, mock_g):
        with patch.dict(sys.modules, {'jqdata': mock_jqdata_module}):
            import latest_strategy_22_带上止损的核心资产轮动才更安心_低回撤_高收益率 as strategy
            strategy.g = mock_g
            strategy.g.etf_info = {'518880.XSHG': [10.0, 10.5, 11.0, 11.5, 12.0] * 20}
            result = strategy.evaluate_etf_worth('518880.XSHG', is_hold=0)
            assert isinstance(result, int)
            assert result in [0, 1]

    def test_get_rank(self, mock_jqdata_module, mock_g):
        with patch.dict(sys.modules, {'jqdata': mock_jqdata_module}):
            import latest_strategy_22_带上止损的核心资产轮动才更安心_低回撤_高收益率 as strategy
            strategy.g = mock_g
            strategy.g.m_days = 25
            mock_attr_data = pd.DataFrame({'close': np.array([10.0, 10.5, 11.0] * 9)})
            with patch.object(strategy, 'attribute_history', return_value=mock_attr_data):
                result = strategy.get_rank(['518880.XSHG', '513100.XSHG'])
                assert isinstance(result, list)

    def test_trade_no_positions(self, mock_jqdata_module, mock_g, mock_context):
        with patch.dict(sys.modules, {'jqdata': mock_jqdata_module}):
            import latest_strategy_22_带上止损的核心资产轮动才更安心_低回撤_高收益率 as strategy
            strategy.g = mock_g
            strategy.g.etf_info = {
                '518880.XSHG': [10.0] * 100,
                '513100.XSHG': [20.0] * 100,
                '159915.XSHE': [15.0] * 100,
                '510180.XSHG': [12.0] * 100
            }
            strategy.g.etf_pre = None
            mock_context.portfolio.positions = {}
            mock_rank_result = ['518880.XSHG', '513100.XSHG', '159915.XSHE', '510180.XSHG']
            with patch.object(strategy, 'get_rank', return_value=mock_rank_result):
                with patch.object(strategy, 'evaluate_etf_worth', return_value=1):
                    with patch.object(strategy, 'order_target_value', return_value=Mock()):
                        strategy.trade(mock_context)

    def test_trade_with_positions_sell(self, mock_jqdata_module, mock_g, mock_context):
        with patch.dict(sys.modules, {'jqdata': mock_jqdata_module}):
            import latest_strategy_22_带上止损的核心资产轮动才更安心_低回撤_高收益率 as strategy
            strategy.g = mock_g
            strategy.g.etf_info = {
                '518880.XSHG': [10.0] * 100,
                '513100.XSHG': [20.0] * 100,
                '159915.XSHE': [15.0] * 100,
                '510180.XSHG': [12.0] * 100
            }
            strategy.g.etf_pre = '518880.XSHG'
            position = SimpleNamespace()
            mock_context.portfolio.positions = {'518880.XSHG': position}
            mock_rank_result = ['513100.XSHG', '518880.XSHG', '159915.XSHE', '510180.XSHG']
            with patch.object(strategy, 'get_rank', return_value=mock_rank_result):
                with patch.object(strategy, 'evaluate_etf_worth', side_effect=[1, 0]):
                    with patch.object(strategy, 'order_target_value', return_value=Mock()):
                        strategy.trade(mock_context)

    def test_trade_with_positions_continue_hold(self, mock_jqdata_module, mock_g, mock_context):
        with patch.dict(sys.modules, {'jqdata': mock_jqdata_module}):
            import latest_strategy_22_带上止损的核心资产轮动才更安心_低回撤_高收益率 as strategy
            strategy.g = mock_g
            strategy.g.etf_info = {
                '518880.XSHG': [10.0] * 100,
                '513100.XSHG': [20.0] * 100,
                '159915.XSHE': [15.0] * 100,
                '510180.XSHG': [12.0] * 100
            }
            strategy.g.etf_pre = '518880.XSHG'
            position = SimpleNamespace()
            mock_context.portfolio.positions = {'518880.XSHG': position}
            mock_rank_result = ['518880.XSHG', '513100.XSHG', '159915.XSHE', '510180.XSHG']
            with patch.object(strategy, 'get_rank', return_value=mock_rank_result):
                with patch.object(strategy, 'evaluate_etf_worth', return_value=1):
                    with patch.object(strategy, 'order_target_value', return_value=Mock()):
                        strategy.trade(mock_context)

    def test_trade_recover_buy(self, mock_jqdata_module, mock_g, mock_context):
        with patch.dict(sys.modules, {'jqdata': mock_jqdata_module}):
            import latest_strategy_22_带上止损的核心资产轮动才更安心_低回撤_高收益率 as strategy
            strategy.g = mock_g
            strategy.g.etf_info = {
                '518880.XSHG': [10.0] * 100,
                '513100.XSHG': [20.0] * 100,
                '159915.XSHE': [15.0] * 100,
                '510180.XSHG': [12.0] * 100
            }
            strategy.g.etf_pre = '518880.XSHG'
            mock_context.portfolio.positions = {}
            mock_rank_result = ['518880.XSHG', '513100.XSHG', '159915.XSHE', '510180.XSHG']
            with patch.object(strategy, 'get_rank', return_value=mock_rank_result):
                with patch.object(strategy, 'evaluate_etf_worth', return_value=1):
                    with patch.object(strategy, 'order_target_value', return_value=Mock()):
                        strategy.trade(mock_context)

    def test_initialize(self, mock_jqdata_module, mock_g):
        with patch.dict(sys.modules, {'jqdata': mock_jqdata_module}):
            import latest_strategy_22_带上止损的核心资产轮动才更安心_低回撤_高收益率 as strategy
            strategy.g = mock_g
            mock_attr_data = pd.DataFrame({'close': np.array([10.0] * 100)})
            mock_context = SimpleNamespace()
            with patch.object(strategy, 'attribute_history', return_value=mock_attr_data):
                strategy.initialize(mock_context)
                mock_jqdata_module.set_benchmark.assert_called()
                mock_jqdata_module.set_option.assert_called()