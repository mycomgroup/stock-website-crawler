import pytest
from unittest.mock import Mock, MagicMock, patch
from datetime import datetime
import pandas as pd
from types import SimpleNamespace
import sys


class TestSimpleHlTest:
    @pytest.fixture(autouse=True)
    def setup_mocks(self, mock_jqdata):
        self.jqdata = mock_jqdata
        self.g = SimpleNamespace()
        self.g.trades = 0
        self.g.wins = 0
        self.g.total_pnl = 0
        
        self.jqdata.g = self.g
        sys.modules['jqdata'] = self.jqdata
        
        patcher = patch.dict(sys.modules, {'jqdata': self.jqdata})
        patcher.start()
        self.addCleanup(patcher.stop)
        
        import simple_hl_test as module
        self.module = module

    def addCleanup(self, cleanup):
        cleanup()

    def test_initialize_sets_options(self):
        context = SimpleNamespace()
        
        self.module.initialize(context)
        
        self.jqdata.set_option.assert_any_call("use_real_price", True)
        self.jqdata.set_option.assert_any_call("avoid_future_data", True)
        self.jqdata.log.set_level.assert_called_once_with("system", "error")
        assert self.jqdata.run_daily.call_count == 2

    def test_initialize_sets_global_variables(self):
        context = SimpleNamespace()
        
        self.module.initialize(context)
        
        assert self.g.trades == 0
        assert self.g.wins == 0
        assert self.g.total_pnl == 0

    def test_buy_identifies_limit_up_stocks(self):
        context = SimpleNamespace()
        context.previous_date = datetime(2024, 1, 15)
        context.portfolio = SimpleNamespace()
        context.portfolio.available_cash = 100000
        
        mock_securities = pd.DataFrame({
            'display_name': ['平安银行', '万科A', '浦发银行']
        }, index=['000001.XSHE', '000002.XSHE', '600000.XSHG'])
        self.jqdata.get_all_securities.return_value = mock_securities
        
        df = pd.DataFrame({
            'code': ['000001.XSHE', '000002.XSHE'],
            'close': [10.0, 20.0],
            'high_limit': [10.0, 20.0],
            'paused': [0, 0]
        })
        self.jqdata.get_price.return_value = df
        
        stock_data = SimpleNamespace()
        stock_data.paused = False
        stock_data.last_price = 10.0
        
        self.jqdata.get_current_data.return_value = {
            '000001.XSHE': stock_data,
            '000002.XSHE': stock_data
        }
        
        self.module.buy(context)
        
        self.jqdata.order_value.assert_called()

    def test_buy_filters_excluded_stocks(self):
        context = SimpleNamespace()
        context.previous_date = datetime(2024, 1, 15)
        context.portfolio = SimpleNamespace()
        context.portfolio.available_cash = 100000
        
        mock_securities = pd.DataFrame({
            'display_name': ['Stock1', 'Stock2', 'Stock3', 'Stock4', 'Stock5']
        }, index=['000001.XSHE', '688001.XSHG', '300001.XSHE', '400001.XSHE', '800001.XSHG'])
        self.jqdata.get_all_securities.return_value = mock_securities
        
        df = pd.DataFrame({
            'code': ['000001.XSHE'],
            'close': [10.0],
            'high_limit': [10.0],
            'paused': [0]
        })
        self.jqdata.get_price.return_value = df
        
        stock_data = SimpleNamespace()
        stock_data.paused = False
        stock_data.last_price = 10.0
        
        self.jqdata.get_current_data.return_value = {'000001.XSHE': stock_data}
        
        self.module.buy(context)
        
        call_args = str(self.jqdata.get_all_securities.call_args)

    def test_buy_filters_paused_stocks(self):
        context = SimpleNamespace()
        context.previous_date = datetime(2024, 1, 15)
        context.portfolio = SimpleNamespace()
        context.portfolio.available_cash = 100000
        
        mock_securities = pd.DataFrame({
            'display_name': ['平安银行']
        }, index=['000001.XSHE'])
        self.jqdata.get_all_securities.return_value = mock_securities
        
        df = pd.DataFrame({
            'code': ['000001.XSHE'],
            'close': [10.0],
            'high_limit': [10.0],
            'paused': [1]
        })
        self.jqdata.get_price.return_value = df
        
        self.module.buy(context)
        
        self.jqdata.order_value.assert_not_called()

    def test_buy_filters_non_limit_up(self):
        context = SimpleNamespace()
        context.previous_date = datetime(2024, 1, 15)
        context.portfolio = SimpleNamespace()
        context.portfolio.available_cash = 100000
        
        mock_securities = pd.DataFrame({
            'display_name': ['平安银行']
        }, index=['000001.XSHE'])
        self.jqdata.get_all_securities.return_value = mock_securities
        
        df = pd.DataFrame({
            'code': ['000001.XSHE'],
            'close': [9.0],
            'high_limit': [10.0],
            'paused': [0]
        })
        self.jqdata.get_price.return_value = df
        
        self.module.buy(context)
        
        self.jqdata.order_value.assert_not_called()

    def test_buy_handles_no_limit_up(self):
        context = SimpleNamespace()
        context.previous_date = datetime(2024, 1, 15)
        context.portfolio = SimpleNamespace()
        context.portfolio.available_cash = 100000
        
        mock_securities = pd.DataFrame({
            'display_name': ['平安银行']
        }, index=['000001.XSHE'])
        self.jqdata.get_all_securities.return_value = mock_securities
        
        df = pd.DataFrame({
            'code': [],
            'close': [],
            'high_limit': [],
            'paused': []
        })
        self.jqdata.get_price.return_value = df
        
        self.module.buy(context)
        
        self.jqdata.get_current_data.assert_not_called()

    def test_buy_limits_to_5_stocks(self):
        context = SimpleNamespace()
        context.previous_date = datetime(2024, 1, 15)
        context.portfolio = SimpleNamespace()
        context.portfolio.available_cash = 500000
        
        mock_securities = pd.DataFrame({
            'display_name': ['Stock' + str(i) for i in range(10)]
        }, index=['00000' + str(i) + '.XSHE' for i in range(10)])
        self.jqdata.get_all_securities.return_value = mock_securities
        
        df = pd.DataFrame({
            'code': ['00000' + str(i) + '.XSHE' for i in range(10)],
            'close': [10.0] * 10,
            'high_limit': [10.0] * 10,
            'paused': [0] * 10
        })
        self.jqdata.get_price.return_value = df
        
        stock_data = SimpleNamespace()
        stock_data.paused = False
        stock_data.last_price = 10.0
        
        current_data = {}
        for i in range(10):
            current_data['00000' + str(i) + '.XSHE'] = stock_data
        self.jqdata.get_current_data.return_value = current_data
        
        self.module.buy(context)
        
        assert self.jqdata.order_value.call_count <= 5

    def test_buy_skips_paused_in_current_data(self):
        context = SimpleNamespace()
        context.previous_date = datetime(2024, 1, 15)
        context.portfolio = SimpleNamespace()
        context.portfolio.available_cash = 100000
        
        mock_securities = pd.DataFrame({
            'display_name': ['平安银行']
        }, index=['000001.XSHE'])
        self.jqdata.get_all_securities.return_value = mock_securities
        
        df = pd.DataFrame({
            'code': ['000001.XSHE'],
            'close': [10.0],
            'high_limit': [10.0],
            'paused': [0]
        })
        self.jqdata.get_price.return_value = df
        
        stock_data = SimpleNamespace()
        stock_data.paused = True
        stock_data.last_price = 10.0
        
        self.jqdata.get_current_data.return_value = {'000001.XSHE': stock_data}
        
        self.module.buy(context)
        
        self.jqdata.order_value.assert_not_called()

    def test_buy_increments_trade_count(self):
        context = SimpleNamespace()
        context.previous_date = datetime(2024, 1, 15)
        context.portfolio = SimpleNamespace()
        context.portfolio.available_cash = 100000
        
        mock_securities = pd.DataFrame({
            'display_name': ['平安银行']
        }, index=['000001.XSHE'])
        self.jqdata.get_all_securities.return_value = mock_securities
        
        df = pd.DataFrame({
            'code': ['000001.XSHE'],
            'close': [10.0],
            'high_limit': [10.0],
            'paused': [0]
        })
        self.jqdata.get_price.return_value = df
        
        stock_data = SimpleNamespace()
        stock_data.paused = False
        stock_data.last_price = 10.0
        
        self.jqdata.get_current_data.return_value = {'000001.XSHE': stock_data}
        
        initial_trades = self.g.trades
        self.module.buy(context)
        
        assert self.g.trades > initial_trades

    def test_sell_with_positions(self):
        context = SimpleNamespace()
        context.current_dt = datetime(2024, 1, 16)
        context.portfolio = SimpleNamespace()
        pos = SimpleNamespace()
        pos.closeable_amount = 100
        pos.avg_cost = 10.0
        context.portfolio.positions = {'000001.XSHE': pos}
        
        stock_data = SimpleNamespace()
        stock_data.last_price = 11.0
        self.jqdata.get_current_data.return_value = {'000001.XSHE': stock_data}
        
        self.module.sell(context)
        
        self.jqdata.order_target_value.assert_called_once_with('000001.XSHE', 0)
        assert self.g.total_pnl > 0
        assert self.g.wins == 1

    def test_sell_with_loss(self):
        context = SimpleNamespace()
        context.current_dt = datetime(2024, 1, 16)
        context.portfolio = SimpleNamespace()
        pos = SimpleNamespace()
        pos.closeable_amount = 100
        pos.avg_cost = 11.0
        context.portfolio.positions = {'000001.XSHE': pos}
        
        stock_data = SimpleNamespace()
        stock_data.last_price = 10.0
        self.jqdata.get_current_data.return_value = {'000001.XSHE': stock_data}
        
        self.module.sell(context)
        
        assert self.g.total_pnl < 0
        assert self.g.wins == 0

    def test_sell_without_closeable_amount(self):
        context = SimpleNamespace()
        context.current_dt = datetime(2024, 1, 16)
        context.portfolio = SimpleNamespace()
        pos = SimpleNamespace()
        pos.closeable_amount = 0
        pos.avg_cost = 10.0
        context.portfolio.positions = {'000001.XSHE': pos}
        
        self.module.sell(context)
        
        self.jqdata.order_target_value.assert_not_called()

    def test_sell_multiple_positions(self):
        context = SimpleNamespace()
        context.current_dt = datetime(2024, 1, 16)
        context.portfolio = SimpleNamespace()
        
        pos1 = SimpleNamespace()
        pos1.closeable_amount = 100
        pos1.avg_cost = 10.0
        
        pos2 = SimpleNamespace()
        pos2.closeable_amount = 100
        pos2.avg_cost = 20.0
        
        context.portfolio.positions = {'000001.XSHE': pos1, '000002.XSHE': pos2}
        
        stock_data1 = SimpleNamespace()
        stock_data1.last_price = 11.0
        
        stock_data2 = SimpleNamespace()
        stock_data2.last_price = 21.0
        
        self.jqdata.get_current_data.return_value = {
            '000001.XSHE': stock_data1,
            '000002.XSHE': stock_data2
        }
        
        self.module.sell(context)
        
        assert self.jqdata.order_target_value.call_count == 2
        assert self.g.wins == 2

    def test_sell_logs_on_year_end(self):
        context = SimpleNamespace()
        context.current_dt = datetime(2024, 12, 31)
        context.portfolio = SimpleNamespace()
        pos = SimpleNamespace()
        pos.closeable_amount = 100
        pos.avg_cost = 10.0
        context.portfolio.positions = {'000001.XSHE': pos}
        
        stock_data = SimpleNamespace()
        stock_data.last_price = 11.0
        self.jqdata.get_current_data.return_value = {'000001.XSHE': stock_data}
        
        self.module.sell(context)
        
        self.jqdata.log.info.assert_called()

    def test_sell_no_log_on_non_year_end(self):
        context = SimpleNamespace()
        context.current_dt = datetime(2024, 1, 16)
        context.portfolio = SimpleNamespace()
        pos = SimpleNamespace()
        pos.closeable_amount = 100
        pos.avg_cost = 10.0
        context.portfolio.positions = {'000001.XSHE': pos}
        
        stock_data = SimpleNamespace()
        stock_data.last_price = 11.0
        self.jqdata.get_current_data.return_value = {'000001.XSHE': stock_data}
        
        self.module.sell(context)
        
        self.jqdata.log.info.assert_not_called()

    def test_sell_no_positions(self):
        context = SimpleNamespace()
        context.current_dt = datetime(2024, 1, 16)
        context.portfolio = SimpleNamespace()
        context.portfolio.positions = {}
        
        self.module.sell(context)
        
        self.jqdata.order_target_value.assert_not_called()

    def test_buy_handles_empty_price_data(self):
        context = SimpleNamespace()
        context.previous_date = datetime(2024, 1, 15)
        context.portfolio = SimpleNamespace()
        context.portfolio.available_cash = 100000
        
        mock_securities = pd.DataFrame({
            'display_name': ['平安银行']
        }, index=['000001.XSHE'])
        self.jqdata.get_all_securities.return_value = mock_securities
        
        empty_df = pd.DataFrame(columns=['code', 'close', 'high_limit', 'paused'])
        self.jqdata.get_price.return_value = empty_df
        
        self.module.buy(context)
        
        self.jqdata.get_current_data.assert_not_called()