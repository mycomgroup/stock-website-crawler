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
    mock_module.set_option = Mock()
    mock_module.log = MagicMock()
    mock_module.log.set_level = Mock()
    mock_module.log.info = Mock()
    mock_module.run_weekly = Mock()
    mock_module.unschedule_all = Mock()
    mock_module.history = Mock()
    mock_module.get_all_securities = Mock()
    mock_module.order_target = Mock()
    mock_module.order_value = Mock()
    mock_module.get_current_data = Mock()
    mock_module.cov = Mock()
    return mock_module


@pytest.fixture
def mock_context():
    context = SimpleNamespace()
    context.current_dt = datetime(2024, 1, 16, 9, 30)
    portfolio = SimpleNamespace()
    portfolio.total_value = 1000000
    portfolio.available_cash = 1000000
    portfolio.positions = {}
    context.portfolio = portfolio
    context.run_params = SimpleNamespace(type='backtest')
    return context


class TestStrategy12:
    def test_initialize(self, mock_jqdata_module):
        with patch.dict(sys.modules, {'jqdata': mock_jqdata_module}):
            module = load_strategy_module("latest_strategy_12_致敬市场--5_定投ETF之躺平赢")
            mock_context = SimpleNamespace()
            strategy.initialize(mock_context)
            mock_jqdata_module.log.set_level.assert_called()

    def test_after_code_changed(self, mock_jqdata_module, mock_context):
        with patch.dict(sys.modules, {'jqdata': mock_jqdata_module}):
            module = load_strategy_module("latest_strategy_12_致敬市场--5_定投ETF之躺平赢")
            strategy.after_code_changed(mock_context)
            mock_jqdata_module.unschedule_all.assert_called()
            mock_jqdata_module.run_weekly.assert_called()

    def test_iTrader_basic(self, mock_jqdata_module, mock_context):
        with patch.dict(sys.modules, {'jqdata': mock_jqdata_module}):
            module = load_strategy_module("latest_strategy_12_致敬市场--5_定投ETF之躺平赢")
            mock_all_fund = pd.DataFrame({
                'display_name': ['ETF1', 'ETF2'],
                'start_date': [datetime(2020, 1, 1), datetime(2020, 1, 1)]
            }, index=['510300.XSHG', '159915.XSHE'])
            mock_history_money = pd.Series([1e6, 2e6], index=['510300.XSHG', '159915.XSHE'])
            mock_history_close = pd.DataFrame({
                '510300.XSHG': [10.0, 10.5, 11.0],
                '159915.XSHE': [20.0, 20.5, 21.0],
                '399300.XSHE': [15.0, 15.5, 16.0]
            })
            mock_current_data = {
                '510300.XSHG': SimpleNamespace(name='沪深300ETF'),
                '159915.XSHE': SimpleNamespace(name='创业板ETF')
            }
            mock_cov_result = np.array([[0.01, 0.005], [0.005, 0.02]])
            with patch.object(strategy, 'get_all_securities', return_value=mock_all_fund):
                with patch.object(strategy, 'history', side_effect=[mock_history_money, mock_history_close]):
                    with patch.object(strategy, 'cov', return_value=mock_cov_result):
                        with patch.object(strategy, 'get_current_data', return_value=mock_current_data):
                            with patch.object(strategy, 'order_target', return_value=Mock()):
                                with patch.object(strategy, 'order_value', return_value=Mock()):
                                    strategy.iTrader(mock_context)

    def test_iTrader_with_positions(self, mock_jqdata_module, mock_context):
        with patch.dict(sys.modules, {'jqdata': mock_jqdata_module}):
            module = load_strategy_module("latest_strategy_12_致敬市场--5_定投ETF之躺平赢")
            mock_context.portfolio.positions = {'510300.XSHG': SimpleNamespace()}
            mock_all_fund = pd.DataFrame({
                'display_name': ['ETF1'],
                'start_date': [datetime(2020, 1, 1)]
            }, index=['510300.XSHG'])
            mock_history_money = pd.Series([1e6], index=['510300.XSHG'])
            mock_history_close = pd.DataFrame({
                '510300.XSHG': [10.0, 10.5, 11.0],
                '399300.XSHE': [15.0, 15.5, 16.0]
            })
            mock_current_data = {'510300.XSHG': SimpleNamespace(name='沪深300ETF')}
            mock_cov_result = np.array([[0.01]])
            with patch.object(strategy, 'get_all_securities', return_value=mock_all_fund):
                with patch.object(strategy, 'history', side_effect=[mock_history_money, mock_history_close]):
                    with patch.object(strategy, 'cov', return_value=mock_cov_result):
                        with patch.object(strategy, 'get_current_data', return_value=mock_current_data):
                            with patch.object(strategy, 'order_target', return_value=Mock()):
                                with patch.object(strategy, 'order_value', return_value=Mock()):
                                    strategy.iTrader(mock_context)

    def test_iTrader_no_funds(self, mock_jqdata_module, mock_context):
        with patch.dict(sys.modules, {'jqdata': mock_jqdata_module}):
            module = load_strategy_module("latest_strategy_12_致敬市场--5_定投ETF之躺平赢")
            mock_all_fund = pd.DataFrame({
                'display_name': [],
                'start_date': []
            }, index=[])
            with patch.object(strategy, 'get_all_securities', return_value=mock_all_fund):
                strategy.iTrader(mock_context)