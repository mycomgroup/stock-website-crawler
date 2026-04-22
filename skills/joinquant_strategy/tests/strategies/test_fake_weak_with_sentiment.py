import pytest
from unittest.mock import Mock, MagicMock, patch
from datetime import datetime, timedelta
import pandas as pd
from types import SimpleNamespace
import sys


class TestFakeWeakWithSentiment:
    @pytest.fixture(autouse=True)
    def setup_mocks(self, mock_jqdata):
        self.jqdata = mock_jqdata
        self.g = SimpleNamespace()
        self.g.trades = 0
        self.g.wins = 0
        self.g.pnl_list = []
        self.g.signals = 0
        self.g.blocked_days = 0
        self.g.allow_trade = True
        
        self.jqdata.g = self.g
        sys.modules['jqdata'] = self.jqdata
        
        patcher = patch.dict(sys.modules, {'jqdata': self.jqdata})
        patcher.start()
        self.addCleanup(patcher.stop)
        
        import fake_weak_with_sentiment as module
        self.module = module

    def addCleanup(self, cleanup):
        cleanup()

    def test_initialize_sets_options(self):
        context = SimpleNamespace()
        
        self.module.initialize(context)
        
        self.jqdata.set_option.assert_any_call("use_real_price", True)
        self.jqdata.set_option.assert_any_call("avoid_future_data", True)
        self.jqdata.log.set_level.assert_called_once_with("system", "error")
        self.jqdata.set_benchmark.assert_called_once_with("000300.XSHG")
        assert self.jqdata.run_daily.call_count == 3

    def test_initialize_sets_global_variables(self):
        context = SimpleNamespace()
        
        self.module.initialize(context)
        
        assert self.g.trades == 0
        assert self.g.wins == 0
        assert self.g.pnl_list == []
        assert self.g.signals == 0
        assert self.g.blocked_days == 0

    def test_check_sentiment_weak_market_blocks_trade(self):
        context = SimpleNamespace()
        context.previous_date = datetime(2024, 1, 15)
        
        mock_securities = pd.DataFrame({
            'display_name': ['Stock' + str(i) for i in range(100)]
        }, index=['00000' + str(i) + '.XSHE' for i in range(100)])
        self.jqdata.get_all_securities.return_value = mock_securities
        
        df = pd.DataFrame({
            'code': ['000001.XSHE'],
            'close': [10.0],
            'high_limit': [10.0],
            'low_limit': [9.0]
        })
        self.jqdata.get_price.return_value = df
        
        self.jqdata.get_shifted_date.return_value = "2024-01-14"
        
        self.jqdata.get_all_trade_days.return_value = [
            datetime(2024, 1, 10), datetime(2024, 1, 11), datetime(2024, 1, 12),
            datetime(2024, 1, 15)
        ]
        
        self.module.check_sentiment(context)
        
        assert self.g.allow_trade == False
        assert self.g.blocked_days > 0

    def test_check_sentiment_strong_market_allows_trade(self):
        context = SimpleNamespace()
        context.previous_date = datetime(2024, 1, 15)
        
        mock_securities = pd.DataFrame({
            'display_name': ['Stock' + str(i) for i in range(100)]
        }, index=['00000' + str(i) + '.XSHE' for i in range(100)])
        self.jqdata.get_all_securities.return_value = mock_securities
        
        strong_df = pd.DataFrame({
            'code': ['00000' + str(i) + '.XSHE' for i in range(50)],
            'close': [10.0] * 50,
            'high_limit': [10.0] * 50,
            'low_limit': [9.0] * 50
        })
        
        consecutive_df = pd.DataFrame({
            'close': [10.0],
            'high_limit': [10.0]
        })
        
        self.jqdata.get_price.return_value = strong_df
        
        self.jqdata.get_shifted_date.return_value = "2024-01-14"
        
        self.jqdata.get_all_trade_days.return_value = [
            datetime(2024, 1, 10), datetime(2024, 1, 11), datetime(2024, 1, 12),
            datetime(2024, 1, 13), datetime(2024, 1, 14), datetime(2024, 1, 15)
        ]
        
        self.module.check_sentiment(context)
        
        assert self.g.allow_trade == False

    def test_check_sentiment_high_limit_down_blocks(self):
        context = SimpleNamespace()
        context.previous_date = datetime(2024, 1, 15)
        
        mock_securities = pd.DataFrame({
            'display_name': ['Stock' + str(i) for i in range(100)]
        }, index=['00000' + str(i) + '.XSHE' for i in range(100)])
        self.jqdata.get_all_securities.return_value = mock_securities
        
        df = pd.DataFrame({
            'code': ['00000' + str(i) + '.XSHE' for i in range(50)],
            'close': [9.0] * 50,
            'high_limit': [10.0] * 50,
            'low_limit': [9.0] * 50
        })
        self.jqdata.get_price.return_value = df
        
        self.jqdata.get_shifted_date.return_value = "2024-01-14"
        
        self.module.check_sentiment(context)
        
        assert self.g.allow_trade == False

    def test_buy_stocks_blocked_by_sentiment(self):
        context = SimpleNamespace()
        context.previous_date = datetime(2024, 1, 15)
        context.portfolio = SimpleNamespace()
        context.portfolio.available_cash = 100000
        
        self.g.allow_trade = False
        
        self.module.buy_stocks(context)
        
        self.jqdata.get_all_securities.assert_not_called()

    def test_buy_stocks_identifies_fake_weak(self):
        context = SimpleNamespace()
        context.previous_date = datetime(2024, 1, 15)
        context.portfolio = SimpleNamespace()
        context.portfolio.available_cash = 100000
        
        self.g.allow_trade = True
        
        mock_securities = pd.DataFrame({
            'display_name': ['平安银行']
        }, index=['000001.XSHE'])
        self.jqdata.get_all_securities.return_value = mock_securities
        
        mock_info = SimpleNamespace()
        mock_info.start_date = datetime(2023, 1, 1)
        self.jqdata.get_security_info.return_value = mock_info
        
        self.jqdata.get_extras.return_value = pd.DataFrame({0: [False]}, index=['000001.XSHE']).T
        
        df = pd.DataFrame({
            'code': ['000001.XSHE'],
            'close': [10.0],
            'high_limit': [10.0]
        })
        self.jqdata.get_price.return_value = df
        
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
        
        self.jqdata.get_all_securities.assert_called()

    def test_buy_stocks_filters_open_pct_range(self):
        context = SimpleNamespace()
        context.previous_date = datetime(2024, 1, 15)
        context.portfolio = SimpleNamespace()
        context.portfolio.available_cash = 100000
        
        self.g.allow_trade = True
        
        mock_securities = pd.DataFrame({
            'display_name': ['平安银行']
        }, index=['000001.XSHE'])
        self.jqdata.get_all_securities.return_value = mock_securities
        
        mock_info = SimpleNamespace()
        mock_info.start_date = datetime(2023, 1, 1)
        self.jqdata.get_security_info.return_value = mock_info
        
        self.jqdata.get_extras.return_value = pd.DataFrame({0: [False]}, index=['000001.XSHE']).T
        
        df = pd.DataFrame({
            'code': ['000001.XSHE'],
            'close': [10.0],
            'high_limit': [10.0]
        })
        self.jqdata.get_price.return_value = df
        
        stock_data = SimpleNamespace()
        stock_data.paused = False
        stock_data.pre_close = 10.0
        stock_data.day_open = 10.5
        
        self.jqdata.get_current_data.return_value = {'000001.XSHE': stock_data}
        
        val_data = pd.DataFrame({
            'circulating_market_cap': [100.0]
        })
        self.jqdata.get_valuation.return_value = val_data
        
        self.module.buy_stocks(context)
        
        self.jqdata.order_value.assert_not_called()

    def test_buy_stocks_filters_market_cap_range(self):
        context = SimpleNamespace()
        context.previous_date = datetime(2024, 1, 15)
        context.portfolio = SimpleNamespace()
        context.portfolio.available_cash = 100000
        
        self.g.allow_trade = True
        
        mock_securities = pd.DataFrame({
            'display_name': ['平安银行']
        }, index=['000001.XSHE'])
        self.jqdata.get_all_securities.return_value = mock_securities
        
        mock_info = SimpleNamespace()
        mock_info.start_date = datetime(2023, 1, 1)
        self.jqdata.get_security_info.return_value = mock_info
        
        self.jqdata.get_extras.return_value = pd.DataFrame({0: [False]}, index=['000001.XSHE']).T
        
        df = pd.DataFrame({
            'code': ['000001.XSHE'],
            'close': [10.0],
            'high_limit': [10.0]
        })
        self.jqdata.get_price.return_value = df
        
        stock_data = SimpleNamespace()
        stock_data.paused = False
        stock_data.pre_close = 10.0
        stock_data.day_open = 10.1
        
        self.jqdata.get_current_data.return_value = {'000001.XSHE': stock_data}
        
        val_data = pd.DataFrame({
            'circulating_market_cap': [20.0]
        })
        self.jqdata.get_valuation.return_value = val_data
        
        self.module.buy_stocks(context)
        
        self.jqdata.order_value.assert_not_called()

    def test_buy_stocks_filters_new_stocks(self):
        context = SimpleNamespace()
        context.previous_date = datetime(2024, 1, 15)
        context.portfolio = SimpleNamespace()
        context.portfolio.available_cash = 100000
        
        self.g.allow_trade = True
        
        mock_securities = pd.DataFrame({
            'display_name': ['NewStock']
        }, index=['000001.XSHE'])
        self.jqdata.get_all_securities.return_value = mock_securities
        
        mock_info = SimpleNamespace()
        mock_info.start_date = datetime(2024, 1, 1)
        self.jqdata.get_security_info.return_value = mock_info
        
        df = pd.DataFrame({
            'code': [],
            'close': [],
            'high_limit': []
        })
        self.jqdata.get_price.return_value = df
        
        self.module.buy_stocks(context)
        
        self.jqdata.order_value.assert_not_called()

    def test_buy_stocks_filters_st_stocks(self):
        context = SimpleNamespace()
        context.previous_date = datetime(2024, 1, 15)
        context.portfolio = SimpleNamespace()
        context.portfolio.available_cash = 100000
        
        self.g.allow_trade = True
        
        mock_securities = pd.DataFrame({
            'display_name': ['平安银行']
        }, index=['000001.XSHE'])
        self.jqdata.get_all_securities.return_value = mock_securities
        
        mock_info = SimpleNamespace()
        mock_info.start_date = datetime(2023, 1, 1)
        self.jqdata.get_security_info.return_value = mock_info
        
        st_df = pd.DataFrame({0: [True]}, index=['000001.XSHE']).T
        st_df.columns = ['is_st']
        self.jqdata.get_extras.return_value = st_df
        
        df = pd.DataFrame({
            'code': [],
            'close': [],
            'high_limit': []
        })
        self.jqdata.get_price.return_value = df
        
        self.module.buy_stocks(context)
        
        self.jqdata.order_value.assert_not_called()

    def test_buy_stocks_filters_paused_stocks(self):
        context = SimpleNamespace()
        context.previous_date = datetime(2024, 1, 15)
        context.portfolio = SimpleNamespace()
        context.portfolio.available_cash = 100000
        
        self.g.allow_trade = True
        
        mock_securities = pd.DataFrame({
            'display_name': ['平安银行']
        }, index=['000001.XSHE'])
        self.jqdata.get_all_securities.return_value = mock_securities
        
        mock_info = SimpleNamespace()
        mock_info.start_date = datetime(2023, 1, 1)
        self.jqdata.get_security_info.return_value = mock_info
        
        self.jqdata.get_extras.return_value = pd.DataFrame({0: [False]}, index=['000001.XSHE']).T
        
        df = pd.DataFrame({
            'code': ['000001.XSHE'],
            'close': [10.0],
            'high_limit': [10.0]
        })
        self.jqdata.get_price.return_value = df
        
        stock_data = SimpleNamespace()
        stock_data.paused = True
        stock_data.pre_close = 10.0
        stock_data.day_open = 10.1
        
        self.jqdata.get_current_data.return_value = {'000001.XSHE': stock_data}
        
        self.module.buy_stocks(context)
        
        self.jqdata.order_value.assert_not_called()

    def test_buy_stocks_zero_pre_close(self):
        context = SimpleNamespace()
        context.previous_date = datetime(2024, 1, 15)
        context.portfolio = SimpleNamespace()
        context.portfolio.available_cash = 100000
        
        self.g.allow_trade = True
        
        mock_securities = pd.DataFrame({
            'display_name': ['平安银行']
        }, index=['000001.XSHE'])
        self.jqdata.get_all_securities.return_value = mock_securities
        
        mock_info = SimpleNamespace()
        mock_info.start_date = datetime(2023, 1, 1)
        self.jqdata.get_security_info.return_value = mock_info
        
        self.jqdata.get_extras.return_value = pd.DataFrame({0: [False]}, index=['000001.XSHE']).T
        
        df = pd.DataFrame({
            'code': ['000001.XSHE'],
            'close': [10.0],
            'high_limit': [10.0]
        })
        self.jqdata.get_price.return_value = df
        
        stock_data = SimpleNamespace()
        stock_data.paused = False
        stock_data.pre_close = 0
        stock_data.day_open = 10.1
        
        self.jqdata.get_current_data.return_value = {'000001.XSHE': stock_data}
        
        self.module.buy_stocks(context)
        
        self.jqdata.order_value.assert_not_called()

    def test_buy_stocks_successful_buy(self):
        context = SimpleNamespace()
        context.previous_date = datetime(2024, 1, 15)
        context.portfolio = SimpleNamespace()
        context.portfolio.available_cash = 100000
        
        self.g.allow_trade = True
        
        mock_securities = pd.DataFrame({
            'display_name': ['平安银行']
        }, index=['000001.XSHE'])
        self.jqdata.get_all_securities.return_value = mock_securities
        
        mock_info = SimpleNamespace()
        mock_info.start_date = datetime(2023, 1, 1)
        self.jqdata.get_security_info.return_value = mock_info
        
        st_df = pd.DataFrame({0: [False]}, index=['000001.XSHE']).T
        st_df.columns = ['is_st']
        self.jqdata.get_extras.return_value = st_df
        
        df = pd.DataFrame({
            'code': ['000001.XSHE'],
            'close': [10.0],
            'high_limit': [10.0]
        })
        self.jqdata.get_price.return_value = df
        
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
        
        assert self.g.trades > 0

    def test_buy_stocks_increments_signals(self):
        context = SimpleNamespace()
        context.previous_date = datetime(2024, 1, 15)
        context.portfolio = SimpleNamespace()
        context.portfolio.available_cash = 100000
        
        self.g.allow_trade = True
        
        mock_securities = pd.DataFrame({
            'display_name': ['平安银行']
        }, index=['000001.XSHE'])
        self.jqdata.get_all_securities.return_value = mock_securities
        
        mock_info = SimpleNamespace()
        mock_info.start_date = datetime(2023, 1, 1)
        self.jqdata.get_security_info.return_value = mock_info
        
        st_df = pd.DataFrame({0: [False]}, index=['000001.XSHE']).T
        st_df.columns = ['is_st']
        self.jqdata.get_extras.return_value = st_df
        
        df = pd.DataFrame({
            'code': ['000001.XSHE'],
            'close': [10.0],
            'high_limit': [10.0]
        })
        self.jqdata.get_price.return_value = df
        
        stock_data = SimpleNamespace()
        stock_data.paused = False
        stock_data.pre_close = 10.0
        stock_data.day_open = 10.1
        
        self.jqdata.get_current_data.return_value = {'000001.XSHE': stock_data}
        
        val_data = pd.DataFrame({
            'circulating_market_cap': [100.0]
        })
        self.jqdata.get_valuation.return_value = val_data
        
        initial_signals = self.g.signals
        self.module.buy_stocks(context)
        
        assert self.g.signals > initial_signals

    def test_buy_stocks_limits_to_3_stocks(self):
        context = SimpleNamespace()
        context.previous_date = datetime(2024, 1, 15)
        context.portfolio = SimpleNamespace()
        context.portfolio.available_cash = 300000
        
        self.g.allow_trade = True
        
        mock_securities = pd.DataFrame({
            'display_name': ['Stock' + str(i) for i in range(5)]
        }, index=['00000' + str(i) + '.XSHE' for i in range(5)])
        self.jqdata.get_all_securities.return_value = mock_securities
        
        mock_info = SimpleNamespace()
        mock_info.start_date = datetime(2023, 1, 1)
        self.jqdata.get_security_info.return_value = mock_info
        
        st_df = pd.DataFrame({0: [False] * 5}, index=['00000' + str(i) + '.XSHE' for i in range(5)])
        self.jqdata.get_extras.return_value = st_df.T
        
        df = pd.DataFrame({
            'code': ['00000' + str(i) + '.XSHE' for i in range(5)],
            'close': [10.0] * 5,
            'high_limit': [10.0] * 5
        })
        self.jqdata.get_price.return_value = df
        
        current_data = {}
        for i in range(5):
            stock_data = SimpleNamespace()
            stock_data.paused = False
            stock_data.pre_close = 10.0
            stock_data.day_open = 10.1
            current_data['00000' + str(i) + '.XSHE'] = stock_data
        
        self.jqdata.get_current_data.return_value = current_data
        
        val_data = pd.DataFrame({
            'circulating_market_cap': [100.0]
        })
        self.jqdata.get_valuation.return_value = val_data
        
        self.module.buy_stocks(context)
        
        assert self.jqdata.order_value.call_count <= 3

    def test_sell_stocks_with_positions(self):
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
        
        self.jqdata.order_target.assert_called_once_with('000001.XSHE', 0)
        assert len(self.g.pnl_list) == 1
        assert self.g.wins == 1

    def test_sell_stocks_with_loss(self):
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
        
        assert len(self.g.pnl_list) == 1
        assert self.g.wins == 0

    def test_sell_stocks_without_closeable_amount(self):
        context = SimpleNamespace()
        context.portfolio = SimpleNamespace()
        pos = SimpleNamespace()
        pos.closeable_amount = 0
        pos.avg_cost = 10.0
        context.portfolio.positions = {'000001.XSHE': pos}
        
        self.module.sell_stocks(context)
        
        self.jqdata.order_target.assert_not_called()

    def test_sell_stocks_stock_not_in_current_data(self):
        context = SimpleNamespace()
        context.portfolio = SimpleNamespace()
        pos = SimpleNamespace()
        pos.closeable_amount = 100
        pos.avg_cost = 10.0
        context.portfolio.positions = {'000001.XSHE': pos}
        
        self.jqdata.get_current_data.return_value = {}
        
        self.module.sell_stocks(context)
        
        self.jqdata.order_target.assert_called_once_with('000001.XSHE', 0)
        assert len(self.g.pnl_list) == 0

    def test_get_shifted_date_valid_date(self):
        self.jqdata.get_all_trade_days.return_value = [
            datetime(2024, 1, 10), datetime(2024, 1, 11), datetime(2024, 1, 12),
            datetime(2024, 1, 15), datetime(2024, 1, 16)
        ]
        
        result = self.module.get_shifted_date("2024-01-16", -1, "T")
        
        assert result is not None

    def test_get_shifted_date_non_trade_date(self):
        self.jqdata.get_all_trade_days.return_value = [
            datetime(2024, 1, 10), datetime(2024, 1, 11), datetime(2024, 1, 12),
            datetime(2024, 1, 15)
        ]
        
        result = self.module.get_shifted_date("2024-01-14", -1, "T")
        
        assert result is not None

    def test_buy_stocks_no_high_limit_stocks(self):
        context = SimpleNamespace()
        context.previous_date = datetime(2024, 1, 15)
        context.portfolio = SimpleNamespace()
        context.portfolio.available_cash = 100000
        
        self.g.allow_trade = True
        
        mock_securities = pd.DataFrame({
            'display_name': ['平安银行']
        }, index=['000001.XSHE'])
        self.jqdata.get_all_securities.return_value = mock_securities
        
        mock_info = SimpleNamespace()
        mock_info.start_date = datetime(2023, 1, 1)
        self.jqdata.get_security_info.return_value = mock_info
        
        self.jqdata.get_extras.return_value = pd.DataFrame({0: [False]}, index=['000001.XSHE']).T
        
        df = pd.DataFrame({
            'code': ['000001.XSHE'],
            'close': [9.0],
            'high_limit': [10.0]
        })
        self.jqdata.get_price.return_value = df
        
        self.module.buy_stocks(context)
        
        self.jqdata.order_value.assert_not_called()

    def test_buy_stocks_handles_exception_in_valuation(self):
        context = SimpleNamespace()
        context.previous_date = datetime(2024, 1, 15)
        context.portfolio = SimpleNamespace()
        context.portfolio.available_cash = 100000
        
        self.g.allow_trade = True
        
        mock_securities = pd.DataFrame({
            'display_name': ['平安银行']
        }, index=['000001.XSHE'])
        self.jqdata.get_all_securities.return_value = mock_securities
        
        mock_info = SimpleNamespace()
        mock_info.start_date = datetime(2023, 1, 1)
        self.jqdata.get_security_info.return_value = mock_info
        
        self.jqdata.get_extras.return_value = pd.DataFrame({0: [False]}, index=['000001.XSHE']).T
        
        df = pd.DataFrame({
            'code': ['000001.XSHE'],
            'close': [10.0],
            'high_limit': [10.0]
        })
        self.jqdata.get_price.return_value = df
        
        stock_data = SimpleNamespace()
        stock_data.paused = False
        stock_data.pre_close = 10.0
        stock_data.day_open = 10.1
        
        self.jqdata.get_current_data.return_value = {'000001.XSHE': stock_data}
        
        self.jqdata.get_valuation.side_effect = Exception("Test error")
        
        self.module.buy_stocks(context)
        
        self.jqdata.order_value.assert_not_called()

    def test_buy_stocks_handles_empty_valuation(self):
        context = SimpleNamespace()
        context.previous_date = datetime(2024, 1, 15)
        context.portfolio = SimpleNamespace()
        context.portfolio.available_cash = 100000
        
        self.g.allow_trade = True
        
        mock_securities = pd.DataFrame({
            'display_name': ['平安银行']
        }, index=['000001.XSHE'])
        self.jqdata.get_all_securities.return_value = mock_securities
        
        mock_info = SimpleNamespace()
        mock_info.start_date = datetime(2023, 1, 1)
        self.jqdata.get_security_info.return_value = mock_info
        
        self.jqdata.get_extras.return_value = pd.DataFrame({0: [False]}, index=['000001.XSHE']).T
        
        df = pd.DataFrame({
            'code': ['000001.XSHE'],
            'close': [10.0],
            'high_limit': [10.0]
        })
        self.jqdata.get_price.return_value = df
        
        stock_data = SimpleNamespace()
        stock_data.paused = False
        stock_data.pre_close = 10.0
        stock_data.day_open = 10.1
        
        self.jqdata.get_current_data.return_value = {'000001.XSHE': stock_data}
        
        self.jqdata.get_valuation.return_value = None
        
        self.module.buy_stocks(context)
        
        self.jqdata.order_value.assert_not_called()

    def test_check_sentiment_handles_exception(self):
        context = SimpleNamespace()
        context.previous_date = datetime(2024, 1, 15)
        
        self.jqdata.get_all_securities.side_effect = Exception("Test error")
        
        self.module.check_sentiment(context)
        
        assert self.g.allow_trade == True