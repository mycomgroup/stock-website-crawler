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
    mock_module.set_slippage = Mock()
    mock_module.FixedSlippage = Mock(return_value=Mock())
    mock_module.set_option = Mock()
    mock_module.log = MagicMock()
    mock_module.log.info = Mock()
    mock_module.set_benchmark = Mock()
    mock_module.set_order_cost = Mock()
    mock_module.OrderCost = Mock(return_value=Mock())
    mock_module.run_daily = Mock()
    mock_module.g = SimpleNamespace()
    mock_module.order_target = Mock()
    mock_module.order_value = Mock()
    mock_module.get_all_securities = Mock()
    mock_module.get_bars = Mock()
    mock_module.get_all_trade_days = Mock()
    mock_module.datetime = __import__('datetime')
    return mock_module


@pytest.fixture
def mock_jqlib_module():
    mock_module = MagicMock()
    mock_module.technical_analysis = MagicMock()
    mock_module.technical_analysis.BBI = Mock(return_value={'000300.XSHG': 10.0})
    mock_module.technical_analysis.EMA = Mock(return_value={'000300.XSHG': 10.5})
    return mock_module


@pytest.fixture
def mock_g():
    g = SimpleNamespace()
    g.dapan_threshold = 0
    g.signal = 'BUY'
    g.niu_signal = 1
    g.position = 1
    g.lag1 = 20
    g.decrease_days = 0
    g.increase_days = 0
    g.unit = '30m'
    g.zs_list = ['000001.XSHG', '399001.XSHE', '000300.XSHG']
    g.ETF_list = {'000300.XSHG': '510300.XSHG', '399006.XSHE': '159915.XSHE'}
    g.not_ipo_list = {'000300.XSHG': '510300.XSHG', '399006.XSHE': '159915.XSHE'}
    g.available_indexs = ['000300.XSHG']
    return g


@pytest.fixture
def mock_context():
    context = SimpleNamespace()
    context.previous_date = datetime(2024, 1, 15)
    context.current_dt = datetime(2024, 1, 16, 11, 15)
    portfolio = SimpleNamespace()
    portfolio.total_value = 1000000
    portfolio.available_cash = 1000000
    portfolio.positions = {}
    context.portfolio = portfolio
    return context


class TestStrategy13:
    def test_get_before_after_trade_days_before(self, mock_jqdata_module, mock_g):
        with patch.dict(sys.modules, {'jqdata': mock_jqdata_module, 'jqlib.technical_analysis': MagicMock()}):
            import latest_strategy_13_不含未来宽基etf轮动8年50倍年化60 as strategy
            strategy.g = mock_g
            mock_all_trade_days = [datetime(2024, 1, 10), datetime(2024, 1, 11), datetime(2024, 1, 15), datetime(2024, 1, 16)]
            with patch.object(strategy, 'get_all_trade_days', return_value=mock_all_trade_days):
                result = strategy.get_before_after_trade_days(datetime(2024, 1, 16), 2, is_before=True)
                assert result is not None

    def test_get_before_after_trade_days_after(self, mock_jqdata_module, mock_g):
        with patch.dict(sys.modules, {'jqdata': mock_jqdata_module, 'jqlib.technical_analysis': MagicMock()}):
            import latest_strategy_13_不含未来宽基etf轮动8年50倍年化60 as strategy
            strategy.g = mock_g
            mock_all_trade_days = [datetime(2024, 1, 10), datetime(2024, 1, 11), datetime(2024, 1, 15), datetime(2024, 1, 16)]
            with patch.object(strategy, 'get_all_trade_days', return_value=mock_all_trade_days):
                result = strategy.get_before_after_trade_days(datetime(2024, 1, 15), 2, is_before=False)
                assert result is not None

    def test_get_before_after_trade_days_string(self, mock_jqdata_module, mock_g):
        with patch.dict(sys.modules, {'jqdata': mock_jqdata_module, 'jqlib.technical_analysis': MagicMock()}):
            import latest_strategy_13_不含未来宽基etf轮动8年50倍年化60 as strategy
            strategy.g = mock_g
            mock_all_trade_days = [datetime(2024, 1, 10), datetime(2024, 1, 11), datetime(2024, 1, 15), datetime(2024, 1, 16)]
            with patch.object(strategy, 'get_all_trade_days', return_value=mock_all_trade_days):
                result = strategy.get_before_after_trade_days('2024-01-16', 2, is_before=True)
                assert result is not None

    def test_make_sure_etf_ipo_empty(self, mock_jqdata_module, mock_g, mock_context):
        with patch.dict(sys.modules, {'jqdata': mock_jqdata_module, 'jqlib.technical_analysis': MagicMock()}):
            import latest_strategy_13_不含未来宽基etf轮动8年50倍年化60 as strategy
            strategy.g = mock_g
            strategy.g.not_ipo_list = {}
            result = strategy.make_sure_etf_ipo(mock_context)
            assert result is None

    def test_make_sure_etf_ipo_with_list(self, mock_jqdata_module, mock_g, mock_context):
        with patch.dict(sys.modules, {'jqdata': mock_jqdata_module, 'jqlib.technical_analysis': MagicMock()}):
            import latest_strategy_13_不含未来宽基etf轮动8年50倍年化60 as strategy
            strategy.g = mock_g
            strategy.g.not_ipo_list = {'000300.XSHG': '510300.XSHG'}
            mock_all_funds = pd.DataFrame({
                'display_name': ['沪深300ETF'],
                'start_date': [datetime(2020, 1, 1)]
            }, index=['510300.XSHG'])
            mock_all_idxes = pd.DataFrame({
                'display_name': ['沪深300'],
                'start_date': [datetime(2020, 1, 1)]
            }, index=['000300.XSHG'])
            mock_trade_days_result = datetime(2024, 1, 1)
            with patch.object(strategy, 'get_all_securities', side_effect=[mock_all_funds, mock_all_idxes]):
                with patch.object(strategy, 'get_before_after_trade_days', return_value=mock_trade_days_result):
                    strategy.make_sure_etf_ipo(mock_context)

    def test_market_buy_clear_signal(self, mock_jqdata_module, mock_g, mock_context):
        with patch.dict(sys.modules, {'jqdata': mock_jqdata_module, 'jqlib.technical_analysis': MagicMock()}):
            import latest_strategy_13_不含未来宽基etf轮动8年50倍年化60 as strategy
            strategy.g = mock_g
            strategy.g.signal = 'CLEAR'
            mock_context.portfolio.positions = {'510300.XSHG': SimpleNamespace()}
            with patch.object(strategy, 'order_target', return_value=Mock()):
                strategy.market_buy(mock_context)

    def test_market_buy_buy_signal(self, mock_jqdata_module, mock_g, mock_context):
        with patch.dict(sys.modules, {'jqdata': mock_jqdata_module, 'jqlib.technical_analysis': MagicMock()}):
            import latest_strategy_13_不含未来宽基etf轮动8年50倍年化60 as strategy
            strategy.g = mock_g
            strategy.g.signal = 'BUY'
            strategy.g.available_indexs = ['000300.XSHG']
            mock_bbi_result = {'000300.XSHG': 10.0}
            mock_bars_result = {'close': [10.0]}
            mock_incre_df = pd.DataFrame({
                '大盘代码': ['000300.XSHG'],
                '周期涨幅': [0.05],
                '当前价格': [10.0]
            })
            mock_index_df = pd.DataFrame({
                '指数代码': ['000300.XSHG'],
                '周期动量': [0.9]
            })
            mock_BBI = Mock(return_value=mock_bbi_result)
            mock_get_bars = Mock(return_value=mock_bars_result)
            with patch('jqlib.technical_analysis.BBI', mock_BBI):
                with patch.object(strategy, 'get_bars', mock_get_bars):
                    with patch.object(strategy, 'order_target', return_value=Mock()):
                        with patch.object(strategy, 'order_value', return_value=Mock()):
                            strategy.market_buy(mock_context)

    def test_update_niu_signal_buy(self, mock_jqdata_module, mock_g, mock_context):
        with patch.dict(sys.modules, {'jqdata': mock_jqdata_module, 'jqlib.technical_analysis': MagicMock()}):
            import latest_strategy_13_不含未来宽基etf轮动8年50倍年化60 as strategy
            strategy.g = mock_g
            mock_ema_result = {'000300.XSHG': 10.5}
            mock_ema_result_prev = {'000300.XSHG': 10.0}
            mock_EMA = Mock(side_effect=[mock_ema_result, mock_ema_result_prev])
            mock_get_bars = Mock(return_value={'close': [10.5]})
            with patch('jqlib.technical_analysis.EMA', mock_EMA):
                with patch.object(strategy, 'get_bars', mock_get_bars):
                    strategy.update_niu_signal(mock_context, '000300.XSHG')
                    assert strategy.g.niu_signal in [0, 1]

    def test_initialize(self, mock_jqdata_module, mock_g):
        with patch.dict(sys.modules, {'jqdata': mock_jqdata_module, 'jqlib.technical_analysis': MagicMock()}):
            import latest_strategy_13_不含未来宽基etf轮动8年50倍年化60 as strategy
            strategy.g = mock_g
            mock_context = SimpleNamespace()
            strategy.initialize(mock_context)
            mock_jqdata_module.set_slippage.assert_called()
            mock_jqdata_module.set_option.assert_called()
            mock_jqdata_module.set_benchmark.assert_called()