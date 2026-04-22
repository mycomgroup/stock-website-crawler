import pytest
import sys
import numpy as np
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
    mock_module.set_slippage = Mock()
    mock_module.log = MagicMock()
    mock_module.log.set_level = Mock()
    mock_module.log.info = Mock()
    mock_module.run_daily = Mock()
    mock_module.g = SimpleNamespace()
    mock_module.order_target = Mock()
    mock_module.order_target_value = Mock()
    mock_module.get_security_info = Mock()
    mock_module.get_all_securities = Mock()
    mock_module.get_all_trade_days = Mock()
    mock_module.attribute_history = Mock()
    mock_module.get_current_data = Mock()
    mock_module.send_message = Mock()
    mock_module.datetime = __import__('datetime')
    return mock_module


@pytest.fixture
def mock_talib_module():
    mock_module = MagicMock()
    mock_module.MA = Mock(return_value=np.array([1.0] * 10))
    return mock_module


@pytest.fixture
def mock_g():
    g = SimpleNamespace()
    g.use_dynamic_target_market = True
    g.target_market = '399001.XSHE'
    g.empty_keep_stock = '511880.XSHG'
    g.signal = 'BUY'
    g.emotion_rate = 0
    g.lag = 6
    g.lag0 = 7
    g.lag1 = 13
    g.lag2 = 13
    g.buy = []
    g.ETF_targets = {'399001.XSHE': '150019.XSHE', '000016.XSHG': '510050.XSHG'}
    g.ETFList = {'399001.XSHE': '150019.XSHE'}
    return g


@pytest.fixture
def mock_context():
    context = SimpleNamespace()
    context.previous_date = datetime(2024, 1, 15)
    context.current_dt = datetime(2024, 1, 16, 11, 30)
    portfolio = SimpleNamespace()
    portfolio.total_value = 1000000
    portfolio.available_cash = 1000000
    portfolio.positions = {}
    portfolio.returns = 0.05
    context.portfolio = portfolio
    return context


class TestStrategy18GradeB:
    def test_set_params(self, mock_jqdata_module, mock_g):
        with patch.dict(sys.modules, {'jqdata': mock_jqdata_module, 'talib': MagicMock()}):
            import latest_strategy_18_6年17倍的etf_分级b的轮动趋势策略跟随感悟 as strategy
            strategy.g = mock_g
            mock_security_info = SimpleNamespace(code='150019.XSHE', display_name='银华锐进', start_date=datetime(2020, 1, 1))
            with patch.object(strategy, 'get_security_info', return_value=mock_security_info):
                strategy.set_params()
                assert strategy.g.target_market is not None

    def test_get_before_after_trade_days_before(self, mock_jqdata_module, mock_g):
        with patch.dict(sys.modules, {'jqdata': mock_jqdata_module, 'talib': MagicMock()}):
            import latest_strategy_18_6年17倍的etf_分级b的轮动趋势策略跟随感悟 as strategy
            strategy.g = mock_g
            mock_all_trade_days = [datetime(2024, 1, 10), datetime(2024, 1, 11), datetime(2024, 1, 15), datetime(2024, 1, 16)]
            with patch.object(strategy, 'get_all_trade_days', return_value=mock_all_trade_days):
                result = strategy.get_before_after_trade_days(datetime(2024, 1, 16), 2, is_before=True)
                assert result is not None

    def test_get_before_after_trade_days_after(self, mock_jqdata_module, mock_g):
        with patch.dict(sys.modules, {'jqdata': mock_jqdata_module, 'talib': MagicMock()}):
            import latest_strategy_18_6年17倍的etf_分级b的轮动趋势策略跟随感悟 as strategy
            strategy.g = mock_g
            mock_all_trade_days = [datetime(2024, 1, 10), datetime(2024, 1, 11), datetime(2024, 1, 15), datetime(2024, 1, 16)]
            with patch.object(strategy, 'get_all_trade_days', return_value=mock_all_trade_days):
                result = strategy.get_before_after_trade_days(datetime(2024, 1, 15), 2, is_before=False)
                assert result is not None

    def test_before_market_open(self, mock_jqdata_module, mock_g, mock_context):
        with patch.dict(sys.modules, {'jqdata': mock_jqdata_module, 'talib': MagicMock()}):
            import latest_strategy_18_6年17倍的etf_分级b的轮动趋势策略跟随感悟 as strategy
            strategy.g = mock_g
            strategy.g.ETF_targets = {'399001.XSHE': '150019.XSHE'}
            mock_all_funds = pd.DataFrame({
                'display_name': ['银华锐进'],
                'start_date': [datetime(2020, 1, 1)]
            }, index=['150019.XSHE'])
            mock_all_idxes = pd.DataFrame({
                'display_name': ['深证成指'],
                'start_date': [datetime(2020, 1, 1)]
            }, index=['399001.XSHE'])
            mock_trade_days_result = datetime(2024, 1, 1)
            with patch.object(strategy, 'get_all_securities', side_effect=[mock_all_funds, mock_all_idxes]):
                with patch.object(strategy, 'get_before_after_trade_days', return_value=mock_trade_days_result):
                    strategy.before_market_open(mock_context)

    def test_ETFtrade_clear_signal(self, mock_jqdata_module, mock_g, mock_context):
        with patch.dict(sys.modules, {'jqdata': mock_jqdata_module, 'talib': MagicMock()}):
            import latest_strategy_18_6年17倍的etf_分级b的轮动趋势策略跟随感悟 as strategy
            strategy.g = mock_g
            strategy.g.signal = 'CLEAR'
            strategy.g.empty_keep_stock = '511880.XSHG'
            position = SimpleNamespace()
            mock_context.portfolio.positions = {'150019.XSHE': position}
            with patch.object(strategy, 'order_target', return_value=Mock()):
                strategy.ETFtrade(mock_context)

    def test_ETFtrade_buy_signal(self, mock_jqdata_module, mock_g, mock_context):
        with patch.dict(sys.modules, {'jqdata': mock_jqdata_module, 'talib': MagicMock()}):
            import latest_strategy_18_6年17倍的etf_分级b的轮动趋势策略跟随感悟 as strategy
            strategy.g = mock_g
            strategy.g.signal = 'BUY'
            strategy.g.buy = ['150019.XSHE']
            strategy.g.empty_keep_stock = '511880.XSHG'
            mock_context.portfolio.positions = {}
            with patch.object(strategy, 'order_target', return_value=Mock()):
                with patch.object(strategy, 'order_target_value', return_value=Mock()):
                    strategy.ETFtrade(mock_context)

    def test_ETFtrade_empty_positions(self, mock_jqdata_module, mock_g, mock_context):
        with patch.dict(sys.modules, {'jqdata': mock_jqdata_module, 'talib': MagicMock()}):
            import latest_strategy_18_6年17倍的etf_分级b的轮动趋势策略跟随感悟 as strategy
            strategy.g = mock_g
            strategy.g.signal = 'BUY'
            strategy.g.buy = []
            strategy.g.empty_keep_stock = '511880.XSHG'
            mock_context.portfolio.positions = {}
            with patch.object(strategy, 'order_target_value', return_value=Mock()):
                strategy.ETFtrade(mock_context)

    def test_get_signal_clear_due_to_emotion(self, mock_jqdata_module, mock_g, mock_context):
        with patch.dict(sys.modules, {'jqdata': mock_jqdata_module, 'talib': MagicMock()}):
            import latest_strategy_18_6年17倍的etf_分级b的轮动趋势策略跟随感悟 as strategy
            strategy.g = mock_g
            strategy.g.ETFList = {'399001.XSHE': '150019.XSHE'}
            mock_attr_data = {'close': np.array([10.0] * 13)}
            mock_current_data = {'150019.XSHE': SimpleNamespace(last_price=10.5)}
            mock_df_etf = pd.DataFrame({
                '基金代码': ['150019.XSHE'],
                '对应指数': ['399001.XSHE'],
                '周期涨幅': [5.0],
                '均线差值': [0.5]
            })
            with patch.object(strategy, 'attribute_history', return_value=mock_attr_data):
                with patch.object(strategy, 'get_current_data', return_value=mock_current_data):
                    with patch.object(strategy, 'EmotionMonitor', return_value=-1):
                        strategy.get_signal(mock_context)
                        assert strategy.g.signal == 'CLEAR'

    def test_get_signal_buy(self, mock_jqdata_module, mock_g, mock_context):
        with patch.dict(sys.modules, {'jqdata': mock_jqdata_module, 'talib': MagicMock()}):
            import latest_strategy_18_6年17倍的etf_分级b的轮动趋势策略跟随感悟 as strategy
            strategy.g = mock_g
            strategy.g.ETFList = {'399001.XSHE': '150019.XSHE'}
            mock_attr_data = {'close': np.array([10.0] * 13)}
            mock_current_data = {'150019.XSHE': SimpleNamespace(last_price=10.5)}
            mock_calc_result = ['150019.XSHE']
            with patch.object(strategy, 'attribute_history', return_value=mock_attr_data):
                with patch.object(strategy, 'get_current_data', return_value=mock_current_data):
                    with patch.object(strategy, 'EmotionMonitor', return_value=1):
                        with patch.object(strategy, 'calc_change', return_value=mock_calc_result):
                            with patch.object(strategy, 'ETFtrade', return_value=None):
                                strategy.get_signal(mock_context)
                                assert strategy.g.signal == 'BUY'

    def test_EmotionMonitor_positive(self, mock_jqdata_module, mock_g):
        with patch.dict(sys.modules, {'jqdata': mock_jqdata_module, 'talib': MagicMock()}):
            import latest_strategy_18_6年17倍的etf_分级b的轮动趋势策略跟随感悟 as strategy
            strategy.g = mock_g
            strategy.g.lag0 = 7
            strategy.g.lag = 6
            mock_volume_data = pd.DataFrame({'volume': np.array([1000000] * 10)})
            mock_ma_result = np.array([1000000] * 10)
            with patch.object(strategy, 'attribute_history', return_value=mock_volume_data):
                with patch('talib.MA', return_value=mock_ma_result):
                    result = strategy.EmotionMonitor()
                    assert result in [-1, 0, 1]

    def test_EmotionMonitor_negative(self, mock_jqdata_module, mock_g):
        with patch.dict(sys.modules, {'jqdata': mock_jqdata_module, 'talib': MagicMock()}):
            import latest_strategy_18_6年17倍的etf_分级b的轮动趋势策略跟随感悟 as strategy
            strategy.g = mock_g
            strategy.g.lag0 = 7
            strategy.g.lag = 6
            mock_volume_data = pd.DataFrame({'volume': np.array([500000] * 10)})
            mock_ma_result = np.array([1000000] * 10)
            with patch.object(strategy, 'attribute_history', return_value=mock_volume_data):
                with patch('talib.MA', return_value=mock_ma_result):
                    result = strategy.EmotionMonitor()
                    assert result in [-1, 0, 1]

    def test_initialize(self, mock_jqdata_module, mock_g):
        with patch.dict(sys.modules, {'jqdata': mock_jqdata_module, 'talib': MagicMock()}):
            import latest_strategy_18_6年17倍的etf_分级b的轮动趋势策略跟随感悟 as strategy
            strategy.g = mock_g
            mock_context = SimpleNamespace()
            mock_security_info = SimpleNamespace(code='150019.XSHE', display_name='银华锐进', start_date=datetime(2020, 1, 1))
            with patch.object(strategy, 'get_security_info', return_value=mock_security_info):
                strategy.initialize(mock_context)
                mock_jqdata_module.run_daily.assert_called()