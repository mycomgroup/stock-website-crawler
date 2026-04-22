import pytest
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../../../strategies/joinquant_strategy'))

from unittest.mock import Mock, MagicMock, patch, PropertyMock
import datetime as dt
import numpy as np
import pandas as pd


class MockG:
    def __init__(self):
        self.stock_num = 10
        self.month = 3
        self.hold_list = []
        self.high_limit_list = []


class MockContext:
    def __init__(self):
        self.current_dt = dt.datetime(2026, 4, 1, 9, 30)
        self.previous_date = dt.date(2026, 3, 31)
        self.portfolio = Mock()
        self.portfolio.positions = {}
        self.portfolio.total_value = 1000000
        self.portfolio.available_cash = 1000000
        self.run_params = Mock()
        self.run_params.type = 'backtest'


class MockPosition:
    def __init__(self, security):
        self.security = security


class MockCurrentData:
    def __init__(self, code):
        self.paused = False
        self.name = f'STOCK_{code}'
        self.is_st = False
        self.last_price = 10.0
        self.high_limit = 11.0
        self.low_limit = 9.0


@pytest.fixture
def mock_jqdata():
    mocks = {}
    mocks['set_benchmark'] = Mock()
    mocks['set_option'] = Mock()
    mocks['set_slippage'] = Mock()
    mocks['log'] = Mock()
    mocks['log.set_level'] = Mock()
    mocks['log.info'] = Mock()
    mocks['get_all_securities'] = Mock(return_value=pd.DataFrame({
        'display_name': ['StockA', 'StockB'],
        'start_date': [dt.date(2020, 1, 1), dt.date(2020, 1, 1)]
    }, index=['600000.XSHG', '600001.XSHG']))
    mocks['get_fundamentals'] = Mock(return_value=pd.DataFrame({
        'code': ['600000.XSHG', '600001.XSHG'],
        'market_cap': [100.0, 200.0],
        'circulating_market_cap': [80.0, 160.0],
        'pe_ratio': [15.0, 18.0]
    }))
    mocks['get_current_data'] = Mock(return_value={
        '600000.XSHG': MockCurrentData('600000.XSHG'),
        '600001.XSHG': MockCurrentData('600001.XSHG')
    })
    mocks['get_price'] = Mock(return_value=pd.DataFrame({
        'close': [10.0],
        'high_limit': [11.0]
    }))
    mocks['history'] = Mock(return_value=pd.DataFrame({
        '600000.XSHG': [10.0],
        '600001.XSHG': [10.0]
    }))
    mocks['finance'] = Mock()
    mocks['finance.run_query'] = Mock(return_value=pd.DataFrame({
        'code': ['600000.XSHG'],
        'bonus_amount_rmb': [500.0],
        'a_registration_date': [dt.date(2025, 1, 1)]
    }))
    mocks['finance.STK_XR_XD'] = Mock()
    mocks['get_security_info'] = Mock(return_value=Mock(
        display_name='TestStock',
        start_date=dt.date(2020, 1, 1)
    ))
    mocks['order_target'] = Mock()
    mocks['order_value'] = Mock()
    mocks['run_daily'] = Mock()
    mocks['record'] = Mock()
    return mocks


class TestStrategy04ValueInvest:
    def test_initialize(self, mock_jqdata):
        import latest_strategy_04_高股息低市盈率高增长的价投策略 as strategy
        with patch.object(strategy, 'set_benchmark', mock_jqdata['set_benchmark']):
            with patch.object(strategy, 'set_option', mock_jqdata['set_option']):
                with patch.object(strategy, 'set_slippage', mock_jqdata['set_slippage']):
                    with patch.object(strategy, 'log', mock_jqdata['log']):
                        with patch.object(strategy, 'g', MockG()):
                            context = MockContext()
                            strategy.initialize(context)
                            assert strategy.g.stock_num == 10

    def test_filter_kcbj_stock(self, mock_jqdata):
        import latest_strategy_04_高股息低市盈率高增长的价投策略 as strategy
        stock_list = ['600000.XSHG', '688001.XSHG', '430001.XSHG', '830001.XSHG']
        result = strategy.filter_kcbj_stock(stock_list.copy())
        assert '688001.XSHG' not in result
        assert '430001.XSHG' not in result
        assert '830001.XSHG' not in result
        assert '600000.XSHG' in result

    def test_filter_paused_stock(self, mock_jqdata):
        import latest_strategy_04_高股息低市盈率高增长的价投策略 as strategy
        stock_list = ['600000.XSHG', '600001.XSHG']
        mock_current = {
            '600000.XSHG': MockCurrentData('600000.XSHG'),
            '600001.XSHE': Mock(paused=True)
        }
        with patch.object(strategy, 'get_current_data', Mock(return_value=mock_current)):
            result = strategy.filter_paused_stock(stock_list)
            assert '600000.XSHG' in result

    def test_filter_st_stock(self, mock_jqdata):
        import latest_strategy_04_高股息低市盈率高增长的价投策略 as strategy
        stock_list = ['600000.XSHG', '600001.XSHG']
        mock_current = {
            '600000.XSHG': MockCurrentData('600000.XSHG'),
            '600001.XSHG': Mock(is_st=True, name='ST_STOCK', paused=False)
        }
        with patch.object(strategy, 'get_current_data', Mock(return_value=mock_current)):
            result = strategy.filter_st_stock(stock_list)
            assert '600000.XSHG' in result
            assert '600001.XSHG' not in result

    def test_filter_new_stock(self, mock_jqdata):
        import latest_strategy_04_高股息低市盈率高增长的价投策略 as strategy
        context = MockContext()
        stock_list = ['600000.XSHG', '600001.XSHG']
        mock_security_info = {
            '600000.XSHG': Mock(start_date=dt.date(2020, 1, 1)),
            '600001.XSHG': Mock(start_date=dt.date(2026, 3, 1))
        }
        with patch.object(strategy, 'get_security_info', lambda x: mock_security_info.get(x)):
            result = strategy.filter_new_stock(context, stock_list)
            assert '600000.XSHG' in result
            assert '600001.XSHG' not in result

    def test_prepare_stock_list(self, mock_jqdata):
        import latest_strategy_04_高股息低市盈率高增长的价投策略 as strategy
        g = MockG()
        context = MockContext()
        context.portfolio.positions = {'600000.XSHG': MockPosition('600000.XSHG')}
        with patch.object(strategy, 'g', g):
            with patch.object(strategy, 'get_price', mock_jqdata['get_price']):
                strategy.prepare_stock_list(context)
                assert '600000.XSHG' in g.hold_list

    def test_check_limit_up_sell(self, mock_jqdata):
        import latest_strategy_04_高股息低市盈率高增长的价投策略 as strategy
        g = MockG()
        g.high_limit_list = ['600000.XSHG']
        context = MockContext()
        context.portfolio.positions = {'600000.XSHG': MockPosition('600000.XSHG')}
        mock_current = {'600000.XSHG': Mock(last_price=10.0, high_limit=11.0)}
        with patch.object(strategy, 'g', g):
            with patch.object(strategy, 'get_current_data', Mock(return_value=mock_current)):
                with patch.object(strategy, 'order_target', mock_jqdata['order_target']):
                    with patch.object(strategy, 'log', mock_jqdata['log']):
                        strategy.check_limit_up(context)
                        mock_jqdata['order_target'].assert_called()

    def test_get_dividend_ratio_filter_list(self, mock_jqdata):
        import latest_strategy_04_高股息低市盈率高增长的价投策略 as strategy
        context = MockContext()
        stock_list = ['600000.XSHG']
        with patch.object(strategy, 'finance', mock_jqdata['finance']):
            with patch.object(strategy, 'get_fundamentals', mock_jqdata['get_fundamentals']):
                result = strategy.get_dividend_ratio_filter_list(context, stock_list, False, 0, 0.1)
                assert isinstance(result, list)

    def test_my_trader(self, mock_jqdata):
        import latest_strategy_04_高股息低市盈率高增长的价投策略 as strategy
        g = MockG()
        g.stock_num = 10
        context = MockContext()
        context.portfolio.positions = {}
        with patch.object(strategy, 'g', g):
            with patch.object(strategy, 'get_all_securities', mock_jqdata['get_all_securities']):
                with patch.object(strategy, 'get_current_data', mock_jqdata['get_current_data']):
                    with patch.object(strategy, 'get_fundamentals', mock_jqdata['get_fundamentals']):
                        with patch.object(strategy, 'finance', mock_jqdata['finance']):
                            with patch.object(strategy, 'get_security_info', mock_jqdata['get_security_info']):
                                with patch.object(strategy, 'history', mock_jqdata['history']):
                                    with patch.object(strategy, 'order_target', mock_jqdata['order_target']):
                                        with patch.object(strategy, 'order_value', mock_jqdata['order_value']):
                                            with patch.object(strategy, 'log', mock_jqdata['log']):
                                                strategy.my_Trader(context)

    def test_slist(self, mock_jqdata):
        import latest_strategy_04_高股息低市盈率高增长的价投策略 as strategy
        context = MockContext()
        stock_list = ['600000.XSHG']
        with patch.object(strategy, 'get_current_data', mock_jqdata['get_current_data']):
            with patch.object(strategy, 'get_fundamentals', mock_jqdata['get_fundamentals']):
                with patch.object(strategy, 'get_security_info', mock_jqdata['get_security_info']):
                    strategy.slist(context, stock_list)

    def test_handle_data_monthly_execution(self, mock_jqdata):
        import latest_strategy_04_高股息低市盈率高增长的价投策略 as strategy
        g = MockG()
        g.month = 3
        context = MockContext()
        context.current_dt = dt.datetime(2026, 4, 1, 9, 30)
        context.portfolio.positions = {}
        with patch.object(strategy, 'g', g):
            with patch.object(strategy, 'my_Trader', Mock()):
                with patch.object(strategy, 'check_limit_up', Mock()):
                    with patch.object(strategy, 'record', mock_jqdata['record']):
                        strategy.handle_data(context, Mock())
                        assert g.month == 4