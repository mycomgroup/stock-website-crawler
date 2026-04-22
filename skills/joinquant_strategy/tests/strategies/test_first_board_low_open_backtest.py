import pytest
from unittest.mock import Mock, MagicMock, patch
from datetime import datetime, timedelta
import pandas as pd
from types import SimpleNamespace
import sys


class TestFirstBoardLowOpenBacktest:
    @pytest.fixture(autouse=True)
    def setup_mocks(self, mock_jqdata):
        self.jqdata = mock_jqdata
        self.g = SimpleNamespace()
        self.g.trade_count = 0
        self.g.win_count = 0
        self.g.pnl_list = []
        self.g.daily_signals = []
        self.g.first_board_stocks = []
        self.g.target = []
        
        self.jqdata.g = self.g
        sys.modules['jqdata'] = self.jqdata
        
        mock_query = Mock()
        mock_query.filter.return_value = mock_query
        self.jqdata.query = Mock(return_value=mock_query)
        self.jqdata.valuation = Mock()
        self.jqdata.valuation.code = Mock()
        self.jqdata.valuation.circulating_market_cap = Mock()
        
        patcher = patch.dict(sys.modules, {'jqdata': self.jqdata})
        patcher.start()
        self.addCleanup(patcher.stop)
        
        import first_board_low_open_backtest as module
        self.module = module

    def addCleanup(self, cleanup):
        cleanup()

    def test_initialize_sets_options(self):
        context = SimpleNamespace()
        
        self.module.initialize(context)
        
        self.jqdata.set_option.assert_any_call("use_real_price", True)
        self.jqdata.set_option.assert_any_call("avoid_future_data", True)
        self.jqdata.log.set_level.assert_called_once_with("system", "error")
        assert self.jqdata.run_daily.call_count == 4

    def test_initialize_sets_global_variables(self):
        context = SimpleNamespace()
        
        self.module.initialize(context)
        
        assert self.g.trade_count == 0
        assert self.g.win_count == 0
        assert self.g.pnl_list == []
        assert self.g.daily_signals == []

    def test_select_stocks_identifies_first_board(self):
        context = SimpleNamespace()
        context.previous_date = datetime(2024, 1, 15)
        
        mock_securities = pd.DataFrame({
            'display_name': ['平安银行', '万科A', '浦发银行']
        }, index=['000001.XSHE', '000002.XSHE', '600000.XSHG'])
        self.jqdata.get_all_securities.return_value = mock_securities
        
        df = pd.DataFrame({
            'code': ['000001.XSHE', '000002.XSHE'],
            'close': [10.0, 20.0],
            'high_limit': [10.0, 20.0]
        })
        self.jqdata.get_price.return_value = df
        
        self.jqdata.get_trade_days.return_value = [
            datetime(2024, 1, 12),
            datetime(2024, 1, 15)
        ]
        
        prev_df = pd.DataFrame({
            'code': ['000002.XSHE'],
            'close': [20.0],
            'high_limit': [20.0]
        })
        
        self.jqdata.get_price.side_effect = [df, prev_df]
        
        self.module.select_stocks(context)
        
        self.jqdata.get_all_securities.assert_called()

    def test_select_stocks_filters_excluded_stocks(self):
        context = SimpleNamespace()
        context.previous_date = datetime(2024, 1, 15)
        
        mock_securities = pd.DataFrame({
            'display_name': ['Stock1', 'Stock2', 'Stock3', 'Stock4', 'Stock5']
        }, index=['000001.XSHE', '688001.XSHG', '300001.XSHE', '400001.XSHE', '800001.XSHG'])
        self.jqdata.get_all_securities.return_value = mock_securities
        
        df = pd.DataFrame({
            'code': ['000001.XSHE'],
            'close': [10.0],
            'high_limit': [10.0]
        })
        self.jqdata.get_price.return_value = df
        
        self.jqdata.get_trade_days.return_value = [
            datetime(2024, 1, 12),
            datetime(2024, 1, 15)
        ]
        
        self.module.select_stocks(context)
        
        call_args = self.jqdata.get_all_securities.call_args
        stocks_arg = call_args[1]['date']

    def test_select_stocks_handles_empty_zt_stocks(self):
        context = SimpleNamespace()
        context.previous_date = datetime(2024, 1, 15)
        
        mock_securities = pd.DataFrame({
            'display_name': ['平安银行']
        }, index=['000001.XSHE'])
        self.jqdata.get_all_securities.return_value = mock_securities
        
        df = pd.DataFrame({
            'code': ['000001.XSHE'],
            'close': [9.0],
            'high_limit': [10.0]
        })
        self.jqdata.get_price.return_value = df
        
        self.module.select_stocks(context)
        
        assert self.g.first_board_stocks == []

    def test_select_stocks_handles_insufficient_trade_days(self):
        context = SimpleNamespace()
        context.previous_date = datetime(2024, 1, 15)
        
        mock_securities = pd.DataFrame({
            'display_name': ['平安银行']
        }, index=['000001.XSHE'])
        self.jqdata.get_all_securities.return_value = mock_securities
        
        df = pd.DataFrame({
            'code': ['000001.XSHE'],
            'close': [10.0],
            'high_limit': [10.0]
        })
        self.jqdata.get_price.return_value = df
        
        self.jqdata.get_trade_days.return_value = [datetime(2024, 1, 15)]
        
        self.module.select_stocks(context)
        
        assert self.g.first_board_stocks == []

    def test_buy_stocks_no_first_board_stocks(self):
        context = SimpleNamespace()
        context.current_dt = datetime(2024, 1, 16, 9, 35)
        context.portfolio = SimpleNamespace()
        context.portfolio.available_cash = 100000
        
        self.g.first_board_stocks = []
        
        self.module.buy_stocks(context)
        
        self.jqdata.get_current_data.assert_not_called()

    def test_buy_stocks_handles_missing_current_data(self):
        context = SimpleNamespace()
        context.current_dt = datetime(2024, 1, 16, 9, 35)
        context.previous_date = datetime(2024, 1, 15)
        context.portfolio = SimpleNamespace()
        context.portfolio.available_cash = 100000
        
        self.g.first_board_stocks = ['000001.XSHE']
        self.jqdata.get_current_data.return_value = {}
        
        val_data = pd.DataFrame({
            'code': ['000001.XSHE'],
            'circulating_market_cap': [100.0]
        })
        self.jqdata.get_fundamentals.return_value = val_data
        
        pos_df = pd.DataFrame({
            'close': [10.0, 10.5, 10.2, 10.3, 10.4, 10.5, 10.6, 10.7, 10.8, 10.9, 11.0, 11.1, 11.2, 11.3, 11.4]
        })
        self.jqdata.get_price.return_value = pos_df
        
        self.module.buy_stocks(context)
        
        self.jqdata.order.assert_not_called()

    def test_buy_stocks_filters_paused_stocks(self):
        context = SimpleNamespace()
        context.current_dt = datetime(2024, 1, 16, 9, 35)
        context.previous_date = datetime(2024, 1, 15)
        context.portfolio = SimpleNamespace()
        context.portfolio.available_cash = 100000
        
        self.g.first_board_stocks = ['000001.XSHE']
        
        stock_data = SimpleNamespace()
        stock_data.paused = True
        stock_data.pre_close = 10.0
        stock_data.day_open = 10.0
        
        self.jqdata.get_current_data.return_value = {'000001.XSHE': stock_data}
        
        self.module.buy_stocks(context)
        
        self.jqdata.order.assert_not_called()

    def test_buy_stocks_filters_open_pct_range(self):
        context = SimpleNamespace()
        context.current_dt = datetime(2024, 1, 16, 9, 35)
        context.previous_date = datetime(2024, 1, 15)
        context.portfolio = SimpleNamespace()
        context.portfolio.available_cash = 100000
        
        self.g.first_board_stocks = ['000001.XSHE']
        
        stock_data = SimpleNamespace()
        stock_data.paused = False
        stock_data.pre_close = 10.0
        stock_data.day_open = 10.5
        
        self.jqdata.get_current_data.return_value = {'000001.XSHE': stock_data}
        
        self.module.buy_stocks(context)
        
        self.jqdata.order.assert_not_called()

    def test_buy_stocks_filters_market_cap_range(self):
        context = SimpleNamespace()
        context.current_dt = datetime(2024, 1, 16, 9, 35)
        context.previous_date = datetime(2024, 1, 15)
        context.portfolio = SimpleNamespace()
        context.portfolio.available_cash = 100000
        
        self.g.first_board_stocks = ['000001.XSHE']
        
        stock_data = SimpleNamespace()
        stock_data.paused = False
        stock_data.pre_close = 10.0
        stock_data.day_open = 9.9
        
        self.jqdata.get_current_data.return_value = {'000001.XSHE': stock_data}
        
        val_data = pd.DataFrame({
            'code': ['000001.XSHE'],
            'circulating_market_cap': [20.0]
        })
        self.jqdata.get_fundamentals.return_value = val_data
        
        self.module.buy_stocks(context)
        
        self.jqdata.order.assert_not_called()

    def test_buy_stocks_filters_position_range(self):
        context = SimpleNamespace()
        context.current_dt = datetime(2024, 1, 16, 9, 35)
        context.previous_date = datetime(2024, 1, 15)
        context.portfolio = SimpleNamespace()
        context.portfolio.available_cash = 100000
        
        self.g.first_board_stocks = ['000001.XSHE']
        
        stock_data = SimpleNamespace()
        stock_data.paused = False
        stock_data.pre_close = 10.0
        stock_data.day_open = 9.9
        
        self.jqdata.get_current_data.return_value = {'000001.XSHE': stock_data}
        
        val_data = pd.DataFrame({
            'code': ['000001.XSHE'],
            'circulating_market_cap': [10.0]
        })
        self.jqdata.get_fundamentals.return_value = val_data
        
        pos_df = pd.DataFrame({
            'close': [9.0, 9.1, 9.2, 9.3, 9.4, 9.5, 9.6, 9.7, 9.8, 9.9, 10.0, 10.1, 10.2, 10.3, 9.3]
        })
        self.jqdata.get_price.return_value = pos_df
        
        mock_query = Mock()
        mock_query.filter.return_value = mock_query
        self.jqdata.query = Mock(return_value=mock_query)
        self.jqdata.valuation = Mock()
        self.jqdata.valuation.code = Mock()
        self.jqdata.valuation.circulating_market_cap = Mock()
        
        self.module.buy_stocks(context)
        
        self.jqdata.order.assert_not_called()

    def test_buy_stocks_filters_position_range(self):
        context = SimpleNamespace()
        context.current_dt = datetime(2024, 1, 16, 9, 35)
        context.previous_date = datetime(2024, 1, 15)
        context.portfolio = SimpleNamespace()
        context.portfolio.available_cash = 100000
        
        self.g.first_board_stocks = ['000001.XSHE']
        
        stock_data = SimpleNamespace()
        stock_data.paused = False
        stock_data.pre_close = 10.0
        stock_data.day_open = 9.9
        
        self.jqdata.get_current_data.return_value = {'000001.XSHE': stock_data}
        
        val_data = pd.DataFrame({
            'code': ['000001.XSHE'],
            'circulating_market_cap': [10.0]
        })
        self.jqdata.get_fundamentals.return_value = val_data
        
        pos_df = pd.DataFrame({
            'close': [9.0, 9.5, 10.0, 10.5, 11.0]
        })
        self.jqdata.get_price.return_value = pos_df
        
        mock_query = Mock()
        mock_query.filter.return_value = mock_query
        self.jqdata.query = Mock(return_value=mock_query)
        self.jqdata.valuation = Mock()
        self.jqdata.valuation.code = Mock()
        self.jqdata.valuation.circulating_market_cap = Mock()
        
        self.module.buy_stocks(context)
        
        self.jqdata.order.assert_not_called()

    def test_buy_stocks_successful_buy(self):
        context = SimpleNamespace()
        context.current_dt = datetime(2024, 1, 16, 9, 35)
        context.previous_date = datetime(2024, 1, 15)
        context.portfolio = SimpleNamespace()
        context.portfolio.available_cash = 100000
        
        self.g.first_board_stocks = ['000001.XSHE']
        
        stock_data = SimpleNamespace()
        stock_data.paused = False
        stock_data.pre_close = 10.0
        stock_data.day_open = 9.9
        
        self.jqdata.get_current_data.return_value = {'000001.XSHE': stock_data}
        
        val_data = pd.DataFrame({
            'code': ['000001.XSHE'],
            'circulating_market_cap': [10.0]
        })
        self.jqdata.get_fundamentals.return_value = val_data
        
        pos_df = pd.DataFrame({
            'close': [9.0, 9.1, 9.2, 9.3, 9.4, 9.5, 9.6, 9.7, 9.8, 9.9, 10.0, 10.1, 10.2, 10.3, 9.3]
        })
        self.jqdata.get_price.return_value = pos_df
        
        mock_query = Mock()
        mock_query.filter.return_value = mock_query
        self.jqdata.query = Mock(return_value=mock_query)
        self.jqdata.valuation = Mock()
        self.jqdata.valuation.code = Mock()
        self.jqdata.valuation.circulating_market_cap = Mock()
        
        self.module.buy_stocks(context)
        
        self.jqdata.order.assert_called()
        assert self.g.trade_count > 0

    def test_record_signals_with_signals(self):
        context = SimpleNamespace()
        context.current_dt = datetime(2024, 1, 16, 15, 0)
        
        self.g.daily_signals = [
            {
                'date': '2024-01-16',
                'stock': '000001.XSHE',
                'open_pct': -1.0,
                'market_cap': 10.0,
                'position': 0.2,
                'buy_price': 9.9
            }
        ]
        
        self.module.record_signals(context)
        
        self.jqdata.log.info.assert_called()
        assert self.g.daily_signals == []

    def test_record_signals_without_signals(self):
        context = SimpleNamespace()
        context.current_dt = datetime(2024, 1, 16, 15, 0)
        
        self.g.daily_signals = []
        
        self.module.record_signals(context)
        
        assert self.g.daily_signals == []

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
        assert self.g.win_count == 1

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
        assert self.g.win_count == 0

    def test_sell_stocks_no_closeable_amount(self):
        context = SimpleNamespace()
        context.portfolio = SimpleNamespace()
        pos = SimpleNamespace()
        pos.closeable_amount = 0
        pos.avg_cost = 10.0
        context.portfolio.positions = {'000001.XSHE': pos}
        
        self.module.sell_stocks(context)
        
        self.jqdata.order_target.assert_not_called()

    def test_after_trading_end_with_trades(self):
        context = SimpleNamespace()
        
        self.g.trade_count = 10
        self.g.pnl_list = [1.0, 2.0, -1.0, 3.0]
        self.g.win_count = 3
        
        self.module.after_trading_end(context)
        
        self.jqdata.log.info.assert_called()

    def test_after_trading_end_no_trades(self):
        context = SimpleNamespace()
        
        self.g.trade_count = 0
        self.g.pnl_list = []
        self.g.win_count = 0
        
        self.module.after_trading_end(context)
        
        self.jqdata.log.info.assert_not_called()

    def test_buy_stocks_limits_to_5_stocks(self):
        context = SimpleNamespace()
        context.current_dt = datetime(2024, 1, 16, 9, 35)
        context.previous_date = datetime(2024, 1, 15)
        context.portfolio = SimpleNamespace()
        context.portfolio.available_cash = 500000
        
        self.g.first_board_stocks = ['000001.XSHE', '000002.XSHE', '000003.XSHE', 
                                     '000004.XSHE', '000005.XSHE', '000006.XSHE']
        
        stock_data = SimpleNamespace()
        stock_data.paused = False
        stock_data.pre_close = 10.0
        stock_data.day_open = 9.9
        
        current_data = {}
        for s in self.g.first_board_stocks:
            current_data[s] = stock_data
        
        self.jqdata.get_current_data.return_value = current_data
        
        val_data = pd.DataFrame({
            'code': self.g.first_board_stocks,
            'circulating_market_cap': [10.0] * 6
        })
        self.jqdata.get_fundamentals.return_value = val_data
        
        pos_df = pd.DataFrame({
            'close': [9.0, 9.1, 9.2, 9.3, 9.4, 9.5, 9.6, 9.7, 9.8, 9.9, 10.0, 10.1, 10.2, 10.3, 9.3]
        })
        self.jqdata.get_price.return_value = pos_df
        
        self.module.buy_stocks(context)
        
        assert self.jqdata.order.call_count <= 5

    def test_buy_stocks_handles_empty_valuation(self):
        context = SimpleNamespace()
        context.current_dt = datetime(2024, 1, 16, 9, 35)
        context.previous_date = datetime(2024, 1, 15)
        context.portfolio = SimpleNamespace()
        context.portfolio.available_cash = 100000
        
        self.g.first_board_stocks = ['000001.XSHE']
        
        stock_data = SimpleNamespace()
        stock_data.paused = False
        stock_data.pre_close = 10.0
        stock_data.day_open = 9.9
        
        self.jqdata.get_current_data.return_value = {'000001.XSHE': stock_data}
        
        self.jqdata.get_fundamentals.return_value = pd.DataFrame()
        
        self.module.buy_stocks(context)
        
        self.jqdata.order.assert_not_called()