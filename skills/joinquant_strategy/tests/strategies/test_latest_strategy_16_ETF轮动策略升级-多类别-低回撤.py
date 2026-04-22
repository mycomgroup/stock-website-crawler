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
from datetime import datetime

sys.path.insert(0, '/Users/yuping/Downloads/git/stock-website-crawler/strategies/misc_research/joinquant_strategy')


@pytest.fixture
def mock_jqdata_module():
    mock_module = MagicMock()
    mock_module.set_params = Mock()
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
    mock_module.order_target = Mock()
    mock_module.order_target_value = Mock()
    mock_module.get_security_info = Mock()
    mock_module.get_price = Mock()
    mock_module.get_current_data = Mock()
    mock_module.get_all_securities = Mock()
    mock_module.get_all_trade_days = Mock()
    mock_module.send_message = Mock()
    mock_module.datetime = __import__('datetime')
    return mock_module


@pytest.fixture
def mock_g():
    g = SimpleNamespace()
    g.purchases = []
    g.sells = []
    g.target_market = '000300.XSHG'
    g.moment_period = 13
    g.ma_period = 10
    g.type_num = 5
    g.ETF_targets = {'000300.XSHG': '510300.XSHG'}
    g.local_stocks = ['510300.XSHG']
    g.global_stocks = []
    g.local_futures = []
    g.global_futures = []
    g.REITs = []
    g.ETFList = {'000300.XSHG': '510300.XSHG'}
    g.holdings = set()
    g.targets = []
    return g


@pytest.fixture
def mock_context():
    context = SimpleNamespace()
    context.previous_date = datetime(2024, 1, 15)
    context.current_dt = datetime(2024, 1, 16, 21, 0)
    portfolio = SimpleNamespace()
    portfolio.total_value = 1000000
    portfolio.available_cash = 1000000
    portfolio.positions = {}
    context.portfolio = portfolio
    return context


class TestStrategy16MultiCategory:
    def test_get_before_after_trade_days_before(self, mock_jqdata_module, mock_g):
        with patch.dict(sys.modules, {'jqdata': mock_jqdata_module}):
            module = load_strategy_module("latest_strategy_16_ETF轮动策略升级-多类别-低回撤")
            strategy.g = mock_g
            mock_all_trade_days = [datetime(2024, 1, 10), datetime(2024, 1, 11), datetime(2024, 1, 15), datetime(2024, 1, 16)]
            with patch.object(strategy, 'get_all_trade_days', return_value=mock_all_trade_days):
                result = strategy.get_before_after_trade_days(datetime(2024, 1, 16), 2, is_before=True)
                assert result is not None

    def test_get_before_after_trade_days_after(self, mock_jqdata_module, mock_g):
        with patch.dict(sys.modules, {'jqdata': mock_jqdata_module}):
            module = load_strategy_module("latest_strategy_16_ETF轮动策略升级-多类别-低回撤")
            strategy.g = mock_g
            mock_all_trade_days = [datetime(2024, 1, 10), datetime(2024, 1, 11), datetime(2024, 1, 15), datetime(2024, 1, 16)]
            with patch.object(strategy, 'get_all_trade_days', return_value=mock_all_trade_days):
                result = strategy.get_before_after_trade_days(datetime(2024, 1, 15), 2, is_before=False)
                assert result is not None

    def test_get_before_after_trade_days_string(self, mock_jqdata_module, mock_g):
        with patch.dict(sys.modules, {'jqdata': mock_jqdata_module}):
            module = load_strategy_module("latest_strategy_16_ETF轮动策略升级-多类别-低回撤")
            strategy.g = mock_g
            mock_all_trade_days = [datetime(2024, 1, 10), datetime(2024, 1, 11), datetime(2024, 1, 15), datetime(2024, 1, 16)]
            with patch.object(strategy, 'get_all_trade_days', return_value=mock_all_trade_days):
                result = strategy.get_before_after_trade_days('2024-01-16', 2, is_before=True)
                assert result is not None

    def test_set_params(self, mock_jqdata_module, mock_g):
        with patch.dict(sys.modules, {'jqdata': mock_jqdata_module}):
            module = load_strategy_module("latest_strategy_16_ETF轮动策略升级-多类别-低回撤")
            strategy.g = mock_g
            mock_security_info = SimpleNamespace(code='510300.XSHG', display_name='沪深300ETF', start_date=datetime(2020, 1, 1))
            with patch.object(strategy, 'get_security_info', return_value=mock_security_info):
                strategy.set_params()
                assert strategy.g.target_market is not None

    def test_before_market_open(self, mock_jqdata_module, mock_g, mock_context):
        with patch.dict(sys.modules, {'jqdata': mock_jqdata_module}):
            module = load_strategy_module("latest_strategy_16_ETF轮动策略升级-多类别-低回撤")
            strategy.g = mock_g
            strategy.g.ETF_targets = {'000300.XSHG': '510300.XSHG'}
            mock_all_funds = pd.DataFrame({
                'display_name': ['沪深300ETF'],
                'start_date': [datetime(2020, 1, 1)]
            }, index=['510300.XSHG'])
            mock_trade_days_result = datetime(2024, 1, 1)
            with patch.object(strategy, 'get_all_securities', return_value=mock_all_funds):
                with patch.object(strategy, 'get_before_after_trade_days', return_value=mock_trade_days_result):
                    strategy.before_market_open(mock_context)

    def test_get_signal(self, mock_jqdata_module, mock_g, mock_context):
        with patch.dict(sys.modules, {'jqdata': mock_jqdata_module}):
            module = load_strategy_module("latest_strategy_16_ETF轮动策略升级-多类别-低回撤")
            strategy.g = mock_g
            strategy.g.ETFList = {'000300.XSHG': '510300.XSHG'}
            strategy.g.local_stocks = ['510300.XSHG']
            mock_security_info = SimpleNamespace(display_name='沪深300ETF')
            mock_price_data = pd.DataFrame({
                'close': [10.0, 10.5, 11.0, 11.5, 12.0, 12.5, 13.0, 13.5, 14.0, 14.5, 15.0],
                'high': [10.5, 11.0, 11.5, 12.0, 12.5, 13.0, 13.5, 14.0, 14.5, 15.0, 15.5],
                'low': [9.5, 10.0, 10.5, 11.0, 11.5, 12.0, 12.5, 13.0, 13.5, 14.0, 14.5]
            })
            mock_current_data = {'510300.XSHG': SimpleNamespace()}
            with patch.object(strategy, 'get_security_info', return_value=mock_security_info):
                with patch.object(strategy, 'get_price', return_value=mock_price_data):
                    with patch.object(strategy, 'get_current_data', return_value=mock_current_data):
                        with patch.object(strategy, 'send_message', return_value=Mock()):
                            strategy.get_signal(mock_context)

    def test_get_signal_empty_etf_list(self, mock_jqdata_module, mock_g, mock_context):
        with patch.dict(sys.modules, {'jqdata': mock_jqdata_module}):
            module = load_strategy_module("latest_strategy_16_ETF轮动策略升级-多类别-低回撤")
            strategy.g = mock_g
            strategy.g.ETFList = {}
            mock_current_data = {}
            with patch.object(strategy, 'get_current_data', return_value=mock_current_data):
                strategy.get_signal(mock_context)

    def test_ETF_trade_with_sells(self, mock_jqdata_module, mock_g, mock_context):
        with patch.dict(sys.modules, {'jqdata': mock_jqdata_module}):
            module = load_strategy_module("latest_strategy_16_ETF轮动策略升级-多类别-低回撤")
            strategy.g = mock_g
            strategy.g.sells = ['510300.XSHG']
            strategy.g.purchases = []
            mock_context.portfolio.positions = {}
            with patch.object(strategy, 'order_target', return_value=Mock()):
                strategy.ETF_trade(mock_context)

    def test_ETF_trade_with_purchases(self, mock_jqdata_module, mock_g, mock_context):
        with patch.dict(sys.modules, {'jqdata': mock_jqdata_module}):
            module = load_strategy_module("latest_strategy_16_ETF轮动策略升级-多类别-低回撤")
            strategy.g = mock_g
            strategy.g.sells = []
            strategy.g.purchases = ['510300.XSHG']
            strategy.g.df_etf = pd.DataFrame({
                '基金代码': ['510300.XSHG'],
                '基金名称': ['沪深300ETF'],
                '涨幅': [5.0],
                '均线状态': [0.5],
                '股数': [1000]
            })
            mock_context.portfolio.positions = {}
            with patch.object(strategy, 'order_target', return_value=Mock()):
                strategy.ETF_trade(mock_context)

    def test_initialize(self, mock_jqdata_module, mock_g):
        with patch.dict(sys.modules, {'jqdata': mock_jqdata_module}):
            module = load_strategy_module("latest_strategy_16_ETF轮动策略升级-多类别-低回撤")
            strategy.g = mock_g
            mock_context = SimpleNamespace()
            mock_security_info = SimpleNamespace(code='510300.XSHG', display_name='沪深300ETF', start_date=datetime(2020, 1, 1))
            with patch.object(strategy, 'get_security_info', return_value=mock_security_info):
                strategy.initialize(mock_context)
                mock_jqdata_module.run_daily.assert_called()