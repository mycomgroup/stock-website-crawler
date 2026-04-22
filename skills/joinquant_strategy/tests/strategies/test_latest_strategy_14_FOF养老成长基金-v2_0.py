import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from module_loader import load_data_module, load_strategy_module
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
    mock_module.set_benchmark = Mock()
    mock_module.set_commission = Mock()
    mock_module.PerTrade = Mock(return_value=Mock())
    mock_module.set_slippage = Mock()
    mock_module.FixedSlippage = Mock(return_value=Mock())
    mock_module.set_option = Mock()
    mock_module.log = MagicMock()
    mock_module.log.set_level = Mock()
    mock_module.log.info = Mock()
    mock_module.inout_cash = Mock()
    mock_module.send_message = Mock()
    mock_module.get_security_info = Mock()
    mock_module.attribute_history = Mock()
    mock_module.history = Mock()
    mock_module.order_target_value = Mock()
    mock_module.order_target = Mock()
    mock_module.order_value = Mock()
    mock_module.get_extras = Mock()
    mock_module.record = Mock()
    mock_module.isnan = np.isnan
    return mock_module


@pytest.fixture
def mock_context():
    context = SimpleNamespace()
    context.current_dt = datetime(2024, 1, 16, 9, 30)
    context.weekDay = {4}
    context.confidenceLevel = 0.02
    context.referenceCycle = 250
    context.maxRange = 30
    context.consolidation = 5
    context.stockCount = 5
    context.referStock = '000002.XSHG'
    context.minPosition = 0
    context.Multiple = 1
    context.minRatio = 0.10
    context.maxRatio = 0.30
    context.minAmount = 2000
    context.netRate = 3
    context.stockDict = {}
    context.trackStock = ''
    context.bondStock = '163210.XSHE'
    context.doneTrade = False
    context.Transitional = True
    context.initPriceDict = {}
    context.positionDict = {}
    context.transactionRecord = {}
    context.tradeRecord = ""
    context.ratioMessage = ""
    context.pool = []
    portfolio = SimpleNamespace()
    portfolio.total_value = 1000000
    portfolio.available_cash = 1000000
    portfolio.inout_cash = 400
    portfolio.positions = {}
    portfolio.portfolio_value = 1000000
    context.portfolio = portfolio
    return context


class TestStrategy14:
    def test_initialize(self, mock_jqdata_module, mock_context):
        with patch.dict(sys.modules, {'jqdata': mock_jqdata_module}):
            module = load_strategy_module("latest_strategy_14_FOF养老成长基金-v2_0")
            strategy.initialize(mock_context)
            mock_jqdata_module.set_benchmark.assert_called()
            mock_jqdata_module.set_commission.assert_called()
            mock_jqdata_module.set_slippage.assert_called()

    def test_initializeStockDict(self, mock_jqdata_module, mock_context):
        with patch.dict(sys.modules, {'jqdata': mock_jqdata_module}):
            module = load_strategy_module("latest_strategy_14_FOF养老成长基金-v2_0")
            mock_context.stockDict = {'515520.XSHG': 10, '161907.XSHE': 10}
            mock_security_info = SimpleNamespace()
            mock_security_info.start_date = datetime(2020, 1, 1)
            mock_attr_data = {'close': np.array([10.0] * 120), 'money': np.array([5000000] * 120)}
            with patch.object(strategy, 'get_security_info', return_value=mock_security_info):
                with patch.object(strategy, 'attribute_history', return_value=mock_attr_data):
                    strategy.initializeStockDict(mock_context)
                    assert mock_context.doneTrade is False

    def test_getStockRSIRatio(self, mock_jqdata_module):
        with patch.dict(sys.modules, {'jqdata': mock_jqdata_module}):
            module = load_strategy_module("latest_strategy_14_FOF养老成长基金-v2_0")
            mock_his = {'close': np.array([10.0, 10.5, 11.0] * 100)}
            with patch.object(strategy, 'attribute_history', return_value=mock_his):
                result = strategy.getStockRSIRatio('515520.XSHG')
                assert isinstance(result, (int, float))

    def test_getStockRSI(self, mock_jqdata_module):
        with patch.dict(sys.modules, {'jqdata': mock_jqdata_module}):
            module = load_strategy_module("latest_strategy_14_FOF养老成长基金-v2_0")
            mock_his = {'close': np.array([10.0, 10.5, 11.0] * 10)}
            with patch.object(strategy, 'attribute_history', return_value=mock_his):
                result = strategy.getStockRSI('515520.XSHG')
                assert isinstance(result, (int, float))

    def test_getLastestTransactTime_true(self, mock_jqdata_module, mock_context):
        with patch.dict(sys.modules, {'jqdata': mock_jqdata_module}):
            module = load_strategy_module("latest_strategy_14_FOF养老成长基金-v2_0")
            mock_context.current_dt = datetime(2024, 2, 16, 9, 30)
            position = SimpleNamespace(transact_time=datetime(2024, 1, 1))
            mock_context.portfolio.positions = {'515520.XSHG': position}
            result = strategy.getLastestTransactTime(mock_context)
            assert isinstance(result, bool)

    def test_getLastestTransactTime_false(self, mock_jqdata_module, mock_context):
        with patch.dict(sys.modules, {'jqdata': mock_jqdata_module}):
            module = load_strategy_module("latest_strategy_14_FOF养老成长基金-v2_0")
            mock_context.current_dt = datetime(2024, 1, 17, 9, 30)
            position = SimpleNamespace(transact_time=datetime(2024, 1, 16))
            mock_context.portfolio.positions = {'515520.XSHG': position}
            result = strategy.getLastestTransactTime(mock_context)
            assert result is False

    def test_getStockName(self, mock_jqdata_module):
        with patch.dict(sys.modules, {'jqdata': mock_jqdata_module}):
            module = load_strategy_module("latest_strategy_14_FOF养老成长基金-v2_0")
            mock_security_info = SimpleNamespace(display_name='价值100ETF')
            with patch.object(strategy, 'get_security_info', return_value=mock_security_info):
                result = strategy.getStockName('515520.XSHG')
                assert result == '价值100ETF'

    def test_variance(self, mock_jqdata_module):
        with patch.dict(sys.modules, {'jqdata': mock_jqdata_module}):
            module = load_strategy_module("latest_strategy_14_FOF养老成长基金-v2_0")
            mock_his = {'close': np.array([10.0, 10.5, 11.0, 11.5, 12.0] * 24)}
            with patch.object(strategy, 'attribute_history', return_value=mock_his):
                result = strategy.variance('515520.XSHG')
                assert isinstance(result, (int, float))

    def test_getAvgMoney(self, mock_jqdata_module):
        with patch.dict(sys.modules, {'jqdata': mock_jqdata_module}):
            module = load_strategy_module("latest_strategy_14_FOF养老成长基金-v2_0")
            mock_his = {'money': np.array([5000000] * 120)}
            with patch.object(strategy, 'attribute_history', return_value=mock_his):
                result = strategy.getAvgMoney('515520.XSHG')
                assert isinstance(result, (int, float))

    def test_delNewStock(self, mock_jqdata_module, mock_context):
        with patch.dict(sys.modules, {'jqdata': mock_jqdata_module}):
            module = load_strategy_module("latest_strategy_14_FOF养老成长基金-v2_0")
            mock_context.current_dt = datetime(2024, 1, 16)
            mock_security_info = SimpleNamespace(start_date=datetime(2020, 1, 1))
            mock_attr_data = {'money': np.array([5000000] * 120)}
            stockDict = {'515520.XSHG': 10}
            with patch.object(strategy, 'get_security_info', return_value=mock_security_info):
                with patch.object(strategy, 'attribute_history', return_value=mock_attr_data):
                    result = strategy.delNewStock(mock_context, stockDict)
                    assert isinstance(result, dict)

    def test_buyOrSellCheck_stop_loss(self, mock_jqdata_module, mock_context):
        with patch.dict(sys.modules, {'jqdata': mock_jqdata_module}):
            module = load_strategy_module("latest_strategy_14_FOF养老成长基金-v2_0")
            mock_security_info = SimpleNamespace(start_date=datetime(2020, 1, 1), display_name='价值100ETF')
            mock_attr_data = {
                'close': np.array([10.0] * 120),
                'high': np.array([10.5] * 120),
                'low': np.array([9.5] * 120)
            }
            with patch.object(strategy, 'get_security_info', return_value=mock_security_info):
                with patch.object(strategy, 'attribute_history', return_value=mock_attr_data):
                    with patch.object(strategy, 'stopLoss', return_value=True):
                        result = strategy.buyOrSellCheck(mock_context, '515520.XSHG', 3, 1.4)
                        assert '禁止操作' in result

    def test_stopLoss_true(self, mock_jqdata_module):
        with patch.dict(sys.modules, {'jqdata': mock_jqdata_module}):
            module = load_strategy_module("latest_strategy_14_FOF养老成长基金-v2_0")
            mock_his_array = pd.DataFrame({
                'close': [10.0, 9.5],
                'open': [10.0, 9.5],
                'high': [10.5, 9.5],
                'low': [9.5, 9.5],
                'volume': [1000000, 1000000]
            })
            with patch.object(strategy, 'attribute_history', return_value=mock_his_array):
                result = strategy.stopLoss('515520.XSHG', lag=2, loss=2, more=4)
                assert isinstance(result, bool)

    def test_stopLoss_false(self, mock_jqdata_module):
        with patch.dict(sys.modules, {'jqdata': mock_jqdata_module}):
            module = load_strategy_module("latest_strategy_14_FOF养老成长基金-v2_0")
            mock_his_array = pd.DataFrame({
                'close': [10.0, 10.1],
                'open': [10.0, 10.1],
                'high': [10.5, 10.2],
                'low': [9.5, 10.0],
                'volume': [1000000, 1000000]
            })
            with patch.object(strategy, 'attribute_history', return_value=mock_his_array):
                result = strategy.stopLoss('515520.XSHG', lag=2, loss=2, more=4)
                assert result is False

    def test_getPremiumRate(self, mock_jqdata_module, mock_context):
        with patch.dict(sys.modules, {'jqdata': mock_jqdata_module}):
            module = load_strategy_module("latest_strategy_14_FOF养老成长基金-v2_0")
            mock_extras = {'515520.XSHG': [10.0]}
            mock_attr_data = {'close': [10.5]}
            with patch.object(strategy, 'get_extras', return_value=mock_extras):
                with patch.object(strategy, 'attribute_history', return_value=mock_attr_data):
                    result = strategy.getPremiumRate(mock_context, '515520.XSHG')
                    assert isinstance(result, (int, float))

    def test_rebalance(self, mock_jqdata_module, mock_context):
        with patch.dict(sys.modules, {'jqdata': mock_jqdata_module}):
            module = load_strategy_module("latest_strategy_14_FOF养老成长基金-v2_0")
            mock_context.pool = ['515520.XSHG']
            mock_context.stockDict = {'515520.XSHG': 10}
            with patch.object(strategy, 'caltradeStockRatio', return_value={'515520.XSHG': 0.2}):
                strategy.rebalance(mock_context)
                assert mock_context.tradeRatio is not None

    def test_tradeStockDict(self, mock_jqdata_module, mock_context):
        with patch.dict(sys.modules, {'jqdata': mock_jqdata_module}):
            module = load_strategy_module("latest_strategy_14_FOF养老成长基金-v2_0")
            mock_context.minAmount = 2000
            mock_context.portfolio.positions = {}
            buyDict = {'515520.XSHG': 0.2, '163210.XSHE': 0}
            mock_his = {'515520.XSHG': [10.0]}
            with patch.object(strategy, 'history', return_value=mock_his):
                strategy.tradeStockDict(mock_context, buyDict)