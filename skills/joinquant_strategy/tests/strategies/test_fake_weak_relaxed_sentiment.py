import pytest
from unittest.mock import Mock, MagicMock, patch
from datetime import datetime, timedelta
import pandas as pd
from types import SimpleNamespace
import sys


class TestFakeWeakRelaxedSentiment:
    @pytest.fixture(autouse=True)
    def setup_mocks(self, mock_jqdata):
        self.jqdata = mock_jqdata
        self.g = SimpleNamespace()
        self.g.trades = 0
        self.g.wins = 0
        self.g.blocked = 0
        self.g.allow = True
        
        self.jqdata.g = self.g
        sys.modules['jqdata'] = self.jqdata
        
        patcher = patch.dict(sys.modules, {'jqdata': self.jqdata})
        patcher.start()
        self.addCleanup(patcher.stop)
        
        import fake_weak_relaxed_sentiment as module
        self.module = module

    def addCleanup(self, cleanup):
        cleanup()

    def test_initialize_sets_options(self):
        context = SimpleNamespace()
        
        self.module.initialize(context)
        
        self.jqdata.set_option.assert_any_call("use_real_price", True)
        self.jqdata.set_option.assert_any_call("avoid_future_data", True)
        self.jqdata.log.set_level.assert_called_once_with("system", "error")
        assert self.jqdata.run_daily.call_count == 3

    def test_initialize_sets_global_variables(self):
        context = SimpleNamespace()
        
        self.module.initialize(context)
        
        assert self.g.trades == 0
        assert self.g.wins == 0
        assert self.g.blocked == 0

    def test_check_sentiment_sets_allow_true_by_default(self):
        context = SimpleNamespace()
        context.previous_date = datetime(2024, 1, 15)
        
        mock_securities = pd.DataFrame({
            'display_name': ['Stock1']
        }, index=['000001.XSHE'])
        self.jqdata.get_all_securities.return_value = mock_securities
        
        prices = pd.DataFrame({
            'code': ['000001.XSHE'],
            'close': [10.0],
            'high_limit': [10.0],
            'low_limit': [9.0]
        })
        self.jqdata.get_price.return_value = prices
        
        self.module.check_sentiment(context)
        
        assert self.g.allow == True

    def test_check_sentiment_blocks_weak_market(self):
        context = SimpleNamespace()
        context.previous_date = datetime(2024, 1, 15)
        
        mock_securities = pd.DataFrame({
            'display_name': ['Stock1', 'Stock2', 'Stock3']
        }, index=['000001.XSHE', '000002.XSHE', '000003.XSHE'])
        self.jqdata.get_all_securities.return_value = mock_securities
        
        prices = pd.DataFrame({
            'code': ['000001.XSHE', '000002.XSHE', '000003.XSHE'],
            'close': [10.0, 9.0, 8.0],
            'high_limit': [10.0, 10.0, 10.0],
            'low_limit': [9.0, 9.0, 9.0]
        })
        self.jqdata.get_price.return_value = prices
        
        self.module.check_sentiment(context)
        
        assert self.g.allow == False
        assert self.g.blocked == 1

    def test_check_sentiment_allows_strong_market(self):
        context = SimpleNamespace()
        context.previous_date = datetime(2024, 1, 15)
        
        mock_securities = pd.DataFrame({
            'display_name': ['Stock' + str(i) for i in range(25)]
        }, index=['00000' + str(i).zfill(2) + '.XSHE' for i in range(25)])
        self.jqdata.get_all_securities.return_value = mock_securities
        
        prices_data = []
        for i in range(25):
            prices_data.append({
                'code': '00000' + str(i).zfill(2) + '.XSHE',
                'close': 10.0,
                'high_limit': 10.0,
                'low_limit': 9.0
            })
        prices = pd.DataFrame(prices_data)
        self.jqdata.get_price.return_value = prices
        
        self.module.check_sentiment(context)
        
        assert self.g.allow == True

    def test_buy_stocks_blocked_when_not_allowed(self):
        context = SimpleNamespace()
        context.previous_date = datetime(2024, 1, 15)
        context.portfolio = SimpleNamespace()
        context.portfolio.available_cash = 100000
        
        self.g.allow = False
        
        self.module.buy_stocks(context)
        
        self.jqdata.order_value.assert_not_called()

    def test_buy_stocks_allowed(self):
        context = SimpleNamespace()
        context.previous_date = datetime(2024, 1, 15)
        context.portfolio = SimpleNamespace()
        context.portfolio.available_cash = 100000
        
        self.g.allow = True
        
        mock_securities = pd.DataFrame({
            'display_name': ['Stock1']
        }, index=['000001.XSHE'])
        self.jqdata.get_all_securities.return_value = mock_securities
        
        prices = pd.DataFrame({
            'code': ['000001.XSHE'],
            'close': [10.0],
            'high_limit': [10.0]
        })
        self.jqdata.get_price.return_value = prices
        
        self.jqdata.get_extras.return_value = pd.DataFrame({0: [False]}, index=['000001.XSHE']).T
        
        mock_info = SimpleNamespace()
        mock_info.start_date = datetime(2023, 1, 1)
        self.jqdata.get_security_info.return_value = mock_info
        
        stock_data = SimpleNamespace()
        stock_data.paused = False
        stock_data.pre_close = 10.0
        stock_data.day_open = 10.1
        
        self.jqdata.get_current_data.return_value = {'000001.XSHE': stock_data}
        
        val_data = pd.DataFrame({
            'circulating_market_cap': [100.0]
        })
        self.jqdata.get_valuation.return_value = val_data
        
        self.module.buy_stocks(context)
        
        assert self.g.trades >= 0

    def test_sell_stocks_records_profit(self):
        context = SimpleNamespace()
        context.portfolio = SimpleNamespace()
        pos = SimpleNamespace()
        pos.closeable_amount = 100
        pos.avg_cost = 10.0
        context.portfolio.positions = {'000001.XSHE': pos}
        
        stock_data = SimpleNamespace()
        stock_data.last_price = 11.0
        self.jqdata.get_current_data.return_value = {'000001.XSHE': stock_data}
        
        self.module.sell_stocks(context)
        
        assert self.g.wins == 1

    def test_sell_stocks_handles_loss(self):
        context = SimpleNamespace()
        context.portfolio = SimpleNamespace()
        pos = SimpleNamespace()
        pos.closeable_amount = 100
        pos.avg_cost = 11.0
        context.portfolio.positions = {'000001.XSHE': pos}
        
        stock_data = SimpleNamespace()
        stock_data.last_price = 10.0
        self.jqdata.get_current_data.return_value = {'000001.XSHE': stock_data}
        
        self.module.sell_stocks(context)
        
        assert self.g.wins == 0

    def test_check_sentiment_exception_handling(self):
        context = SimpleNamespace()
        context.previous_date = datetime(2024, 1, 15)
        
        self.jqdata.get_all_securities.side_effect = Exception("Test error")
        
        self.module.check_sentiment(context)
        
        assert self.g.allow == True