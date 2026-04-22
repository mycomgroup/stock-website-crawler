import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from module_loader import load_data_module, load_strategy_module
import pytest
import sys
import pandas as pd
from unittest.mock import MagicMock, patch, Mock
from types import SimpleNamespace
from datetime import datetime

sys.path.insert(0, '/Users/yuping/Downloads/git/stock-website-crawler/strategies/misc_research/joinquant_strategy')


@pytest.fixture
def mock_jqdata_module():
    mock_module = MagicMock()
    mock_module.set_params = Mock()
    mock_module.set_option = Mock()
    mock_module.set_benchmark = Mock()
    mock_module.log = MagicMock()
    mock_module.log.set_level = Mock()
    mock_module.log.info = Mock()
    mock_module.run_daily = Mock()
    mock_module.g = SimpleNamespace()
    mock_module.order_target = Mock()
    mock_module.order_target_value = Mock()
    mock_module.get_current_data = Mock()
    mock_module.send_message = Mock()
    mock_module.query = Mock()
    mock_module.finance = MagicMock()
    mock_module.finance.STK_ML_QUOTA = MagicMock()
    mock_module.finance.STK_HK_HOLD_INFO = MagicMock()
    mock_module.finance.run_query = Mock()
    mock_module.record = Mock()
    return mock_module


@pytest.fixture
def mock_g():
    g = SimpleNamespace()
    g.use_dynamic_target_market = True
    g.target_market = '000300.XSHG'
    g.empty_keep_stock = '511880.XSHG'
    g.signal = 'BUY'
    g.north_money = 0
    g.max_stock_count = 15
    g.buy = []
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
    portfolio.returns = 0.05
    context.portfolio = portfolio
    return context


class TestStrategy21NorthMoney:
    def test_set_params(self, mock_jqdata_module, mock_g):
        with patch.dict(sys.modules, {'jqdata': mock_jqdata_module}):
            module = load_strategy_module("latest_strategy_21_北向资金股票轮动-优质策略可直接实盘")
            strategy.g = mock_g
            strategy.set_params()
            assert strategy.g.target_market is not None
            assert strategy.g.empty_keep_stock is not None

    def test_initialize(self, mock_jqdata_module, mock_g):
        with patch.dict(sys.modules, {'jqdata': mock_jqdata_module}):
            module = load_strategy_module("latest_strategy_21_北向资金股票轮动-优质策略可直接实盘")
            strategy.g = mock_g
            mock_context = SimpleNamespace()
            strategy.initialize(mock_context)
            mock_jqdata_module.run_daily.assert_called()

    def test_EFTtrade_clear_signal(self, mock_jqdata_module, mock_g, mock_context):
        with patch.dict(sys.modules, {'jqdata': mock_jqdata_module}):
            module = load_strategy_module("latest_strategy_21_北向资金股票轮动-优质策略可直接实盘")
            strategy.g = mock_g
            strategy.g.signal = 'CLEAR'
            strategy.g.empty_keep_stock = '511880.XSHG'
            position = SimpleNamespace()
            mock_context.portfolio.positions = {'000001.XSHE': position, '511880.XSHG': position}
            with patch.object(strategy, 'order_target', return_value=Mock()):
                strategy.ETFtrade(mock_context)

    def test_EFTtrade_buy_signal(self, mock_jqdata_module, mock_g, mock_context):
        with patch.dict(sys.modules, {'jqdata': mock_jqdata_module}):
            module = load_strategy_module("latest_strategy_21_北向资金股票轮动-优质策略可直接实盘")
            strategy.g = mock_g
            strategy.g.signal = 'BUY'
            strategy.g.buy = ['000001.XSHE', '000002.XSHE']
            strategy.g.empty_keep_stock = '511880.XSHG'
            mock_context.portfolio.positions = {}
            mock_current_data = {
                '000001.XSHE': SimpleNamespace(name='平安银行'),
                '000002.XSHE': SimpleNamespace(name='万科A')
            }
            with patch.object(strategy, 'get_current_data', return_value=mock_current_data):
                with patch.object(strategy, 'order_target', return_value=Mock()):
                    with patch.object(strategy, 'order_target_value', return_value=Mock()):
                        strategy.ETFtrade(mock_context)

    def test_EFTtrade_empty_positions(self, mock_jqdata_module, mock_g, mock_context):
        with patch.dict(sys.modules, {'jqdata': mock_jqdata_module}):
            module = load_strategy_module("latest_strategy_21_北向资金股票轮动-优质策略可直接实盘")
            strategy.g = mock_g
            strategy.g.signal = 'BUY'
            strategy.g.buy = []
            strategy.g.empty_keep_stock = '511880.XSHG'
            mock_context.portfolio.positions = {}
            with patch.object(strategy, 'order_target_value', return_value=Mock()):
                strategy.ETFtrade(mock_context)

    def test_trade_positive_north_money(self, mock_jqdata_module, mock_g, mock_context):
        with patch.dict(sys.modules, {'jqdata': mock_jqdata_module}):
            module = load_strategy_module("latest_strategy_21_北向资金股票轮动-优质策略可直接实盘")
            strategy.g = mock_g
            mock_n_sh = pd.DataFrame({
                'buy_amount': [100, 100, 100],
                'sell_amount': [50, 50, 50]
            })
            mock_n_sz = pd.DataFrame({
                'buy_amount': [100, 100, 100],
                'sell_amount': [50, 50, 50]
            })
            with patch.object(strategy, 'finance.run_query', side_effect=[mock_n_sh, mock_n_sz]):
                with patch.object(strategy, 'send_message', return_value=None):
                    strategy.trade(mock_context)
                    assert strategy.g.north_money > 0

    def test_trade_negative_north_money(self, mock_jqdata_module, mock_g, mock_context):
        with patch.dict(sys.modules, {'jqdata': mock_jqdata_module}):
            module = load_strategy_module("latest_strategy_21_北向资金股票轮动-优质策略可直接实盘")
            strategy.g = mock_g
            mock_n_sh = pd.DataFrame({
                'buy_amount': [10, 10, 10],
                'sell_amount': [100, 100, 100]
            })
            mock_n_sz = pd.DataFrame({
                'buy_amount': [10, 10, 10],
                'sell_amount': [100, 100, 100]
            })
            with patch.object(strategy, 'finance.run_query', side_effect=[mock_n_sh, mock_n_sz]):
                with patch.object(strategy, 'send_message', return_value=None):
                    strategy.trade(mock_context)
                    assert strategy.g.north_money < 0

    def test_get_signal_clear_due_to_north_money(self, mock_jqdata_module, mock_g, mock_context):
        with patch.dict(sys.modules, {'jqdata': mock_jqdata_module}):
            module = load_strategy_module("latest_strategy_21_北向资金股票轮动-优质策略可直接实盘")
            strategy.g = mock_g
            strategy.g.north_money = -20
            mock_calc_result = ['000001.XSHE']
            with patch.object(strategy, 'calc_change', return_value=mock_calc_result):
                with patch.object(strategy, 'ETFtrade', return_value=None):
                    strategy.get_signal(mock_context)
                    assert strategy.g.signal == 'CLEAR'

    def test_get_signal_buy(self, mock_jqdata_module, mock_g, mock_context):
        with patch.dict(sys.modules, {'jqdata': mock_jqdata_module}):
            module = load_strategy_module("latest_strategy_21_北向资金股票轮动-优质策略可直接实盘")
            strategy.g = mock_g
            strategy.g.north_money = 10
            mock_calc_result = ['000001.XSHE', '000002.XSHE']
            with patch.object(strategy, 'calc_change', return_value=mock_calc_result):
                with patch.object(strategy, 'ETFtrade', return_value=None):
                    strategy.get_signal(mock_context)
                    assert strategy.g.signal == 'BUY'

    def test_calc_change(self, mock_jqdata_module, mock_g, mock_context):
        with patch.dict(sys.modules, {'jqdata': mock_jqdata_module}):
            module = load_strategy_module("latest_strategy_21_北向资金股票轮动-优质策略可直接实盘")
            strategy.g = mock_g
            strategy.g.max_stock_count = 15
            mock_hk_hold_df = pd.DataFrame({
                'day': [datetime(2024, 1, 15)],
                'name': ['平安银行', '万科A'],
                'code': ['000001.XSHE', '000002.XSHE'],
                'share_ratio': [5.0, 4.0]
            })
            with patch.object(strategy, 'finance.run_query', return_value=mock_hk_hold_df):
                result = strategy.calc_change(mock_context)
                assert isinstance(result, list)
                assert len(result) <= strategy.g.max_stock_count

    def test_calc_change_with_filter(self, mock_jqdata_module, mock_g, mock_context):
        with patch.dict(sys.modules, {'jqdata': mock_jqdata_module}):
            module = load_strategy_module("latest_strategy_21_北向资金股票轮动-优质策略可直接实盘")
            strategy.g = mock_g
            strategy.g.max_stock_count = 5
            mock_hk_hold_df = pd.DataFrame({
                'day': [datetime(2024, 1, 15)] * 20,
                'name': ['Stock' + str(i) for i in range(20)],
                'code': ['00000' + str(i) + '.XSHE' for i in range(20)],
                'share_ratio': [float(i) for i in range(20, 0, -1)]
            })
            with patch.object(strategy, 'finance.run_query', return_value=mock_hk_hold_df):
                result = strategy.calc_change(mock_context)
                assert len(result) <= strategy.g.max_stock_count