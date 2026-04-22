import pytest
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../../../strategies/joinquant_strategy'))

from unittest.mock import Mock, MagicMock, patch
import datetime as dt
import numpy as np
import pandas as pd


class MockG:
    def __init__(self):
        self.index = '000300.XSHG'
        self.num = 1
        self.stocks = []


class MockContext:
    def __init__(self):
        self.current_dt = dt.datetime(2026, 4, 1, 9, 45)
        self.portfolio = Mock()
        self.portfolio.positions = {}
        self.portfolio.total_value = 1000000
        self.portfolio.available_cash = 1000000


class MockCurrentData:
    def __init__(self):
        self.paused = False
        self.name = 'TestStock'


@pytest.fixture
def mock_jqdata():
    mocks = {}
    mocks['set_option'] = Mock()
    mocks['log'] = Mock()
    mocks['log.set_level'] = Mock()
    mocks['run_monthly'] = Mock()
    mocks['get_index_stocks'] = Mock(return_value=['600000.XSHG', '600001.XSHG'])
    mocks['get_fundamentals'] = Mock(return_value=pd.DataFrame({
        'code': ['600000.XSHG'],
        'market_cap': [100.0]
    }).set_index('code'))
    mocks['finance'] = Mock()
    mocks['finance.run_query'] = Mock(return_value=pd.DataFrame({
        'code': ['600000.XSHG'],
        'bonus_amount_rmb': [500.0]
    }))
    mocks['get_security_info'] = Mock()
    mocks['get_security_info().display_name'] = 'TestStock'
    mocks['get_current_data'] = Mock(return_value={'600000.XSHG': MockCurrentData()})
    mocks['order_target'] = Mock()
    mocks['order_value'] = Mock()
    return mocks


class TestStrategy04:
    def test_initialize(self, mock_jqdata):
        import latest_strategy_04_红利搬砖_年化29 as strategy
        with patch.object(strategy, 'set_option', mock_jqdata['set_option']):
            with patch.object(strategy, 'log', mock_jqdata['log']):
                with patch.object(strategy, 'run_monthly', mock_jqdata['run_monthly']):
                    with patch.object(strategy, 'g', MockG()):
                        context = MockContext()
                        strategy.initialize(context)
                        assert strategy.g.index == '000300.XSHG'
                        assert strategy.g.num == 1
                        assert strategy.g.stocks == []

    def test_handle_trader_sell(self, mock_jqdata):
        import latest_strategy_04_红利搬砖_年化29 as strategy
        g = MockG()
        g.stocks = ['600001.XSHG']
        context = MockContext()
        context.portfolio.positions = {'600000.XSHG': Mock()}
        with patch.object(strategy, 'g', g):
            with patch.object(strategy, 'get_current_data', mock_jqdata['get_current_data']):
                with patch.object(strategy, 'order_target', mock_jqdata['order_target']):
                    with patch.object(strategy, 'log', mock_jqdata['log']):
                        strategy.handle_trader(context)
                        mock_jqdata['order_target'].assert_called()

    def test_handle_trader_buy(self, mock_jqdata):
        import latest_strategy_04_红利搬砖_年化29 as strategy
        g = MockG()
        g.stocks = ['600000.XSHG']
        context = MockContext()
        context.portfolio.positions = {}
        with patch.object(strategy, 'g', g):
            with patch.object(strategy, 'get_current_data', mock_jqdata['get_current_data']):
                with patch.object(strategy, 'order_value', mock_jqdata['order_value']):
                    with patch.object(strategy, 'log', mock_jqdata['log']):
                        strategy.handle_trader(context)
                        mock_jqdata['order_value'].assert_called()

    def test_choice_stocks(self, mock_jqdata):
        import latest_strategy_04_红利搬砖_年化29 as strategy
        context = MockContext()
        with patch.object(strategy, 'get_index_stocks', mock_jqdata['get_index_stocks']):
            with patch.object(strategy, 'get_fundamentals', mock_jqdata['get_fundamentals']):
                with patch.object(strategy, 'finance', mock_jqdata['finance']):
                    with patch.object(strategy, 'get_security_info', Mock(return_value=Mock(display_name='Test'))):
                        result = strategy.choice_stocks(context, '000300.XSHG', 1)
                        assert isinstance(result, list)