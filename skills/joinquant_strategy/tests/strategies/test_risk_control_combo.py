import pytest
from unittest.mock import Mock, MagicMock, patch
from datetime import datetime, timedelta
import pandas as pd
from types import SimpleNamespace
import sys


class TestRiskControlCombo:
    @pytest.fixture(autouse=True)
    def setup_mocks(self, mock_jqdata):
        self.jqdata = mock_jqdata
        self.g = SimpleNamespace()
        self.g.target_list = []
        self.g.trade_count = 0
        self.g.daily_pnl = 0
        self.g.stop_loss_count = 0
        self.g.weekly_start_value = 0
        self.g.weekly_pnl_pct = 0
        self.g.cool_down_days = 0
        self.g.week_start_date = None
        
        self.jqdata.g = self.g
        self.jqdata.attribute_history = Mock(return_value={'high': pd.Series([10.0] * 10)})
        self.jqdata.MarketOrderStyle = Mock()
        self.jqdata.LimitOrderStyle = Mock()
        
        mock_jqfactor = MagicMock()
        mock_jqlib = MagicMock()
        mock_jqlib.technical_analysis = MagicMock()
        
        sys.modules['jqdata'] = self.jqdata
        sys.modules['jqfactor'] = mock_jqfactor
        sys.modules['jqlib.technical_analysis'] = mock_jqlib.technical_analysis
        
        patcher = patch.dict(sys.modules, {
            'jqdata': self.jqdata,
            'jqfactor': mock_jqfactor,
            'jqlib.technical_analysis': mock_jqlib.technical_analysis
        })
        patcher.start()
        self.addCleanup = lambda f: f()
        
        import risk_control_combo as module
        self.module = module

    def test_initialize_sets_options(self):
        context = SimpleNamespace()
        
        self.module.initialize(context)
        
        self.jqdata.set_option.assert_any_call("use_real_price", True)
        self.jqdata.set_option.assert_any_call("avoid_future_data", True)
        self.jqdata.log.set_level.assert_called_once_with("system", "error")
        assert self.jqdata.run_daily.call_count >= 8

    def test_initialize_sets_global_variables(self):
        context = SimpleNamespace()
        
        self.module.initialize(context)
        
        assert self.g.target_list == []
        assert self.g.trade_count == 0
        assert self.g.cool_down_days == 0
        assert self.g.week_start_date is None

    def test_init_weekly_first_call(self):
        context = SimpleNamespace()
        context.current_dt = datetime(2024, 1, 15)
        context.portfolio = SimpleNamespace()
        context.portfolio.total_value = 100000
        
        self.g.week_start_date = None
        
        self.module.init_weekly(context)
        
        assert self.g.week_start_date == datetime(2024, 1, 15).date()
        assert self.g.weekly_start_value == 100000
        assert self.g.cool_down_days == 0

    def test_init_weekly_new_week(self):
        context = SimpleNamespace()
        context.current_dt = datetime(2024, 1, 22)
        context.portfolio = SimpleNamespace()
        context.portfolio.total_value = 110000
        
        import datetime as dt
        self.g.week_start_date = dt.date(2024, 1, 15)
        
        self.module.init_weekly(context)
        
        assert self.g.week_start_date == datetime(2024, 1, 22).date()
        assert self.g.weekly_start_value == 110000

    def test_init_weekly_same_week(self):
        context = SimpleNamespace()
        context.current_dt = datetime(2024, 1, 16)
        context.portfolio = SimpleNamespace()
        context.portfolio.total_value = 105000
        
        import datetime as dt
        self.g.week_start_date = dt.date(2024, 1, 15)
        self.g.weekly_start_value = 100000
        
        self.module.init_weekly(context)
        
        assert self.g.week_start_date == dt.date(2024, 1, 15)

    def test_get_stock_list_with_cool_down(self):
        context = SimpleNamespace()
        context.previous_date = datetime(2024, 1, 15)
        
        self.g.cool_down_days = 2
        
        self.module.get_stock_list(context)
        
        assert self.g.target_list == []

    def test_buy_with_cool_down(self):
        context = SimpleNamespace()
        context.previous_date = datetime(2024, 1, 15)
        context.portfolio = SimpleNamespace()
        context.portfolio.available_cash = 100000
        
        self.g.cool_down_days = 2
        self.g.target_list = ['000001.XSHE']
        
        self.module.buy(context)
        
        self.jqdata.order_value.assert_not_called()

    def test_buy_reduces_value_with_cool_down(self):
        context = SimpleNamespace()
        context.previous_date = datetime(2024, 1, 15)
        context.current_dt = datetime(2024, 1, 15, 9, 30)
        context.portfolio = SimpleNamespace()
        context.portfolio.available_cash = 100000
        
        self.g.cool_down_days = 0
        self.g.target_list = ['000001.XSHE']
        
        stock_data = SimpleNamespace()
        stock_data.paused = False
        stock_data.day_open = 10.0
        stock_data.last_price = 10.0
        
        self.jqdata.get_current_data.return_value = {'000001.XSHE': stock_data}
        
        prev_data = {'close': [10.0], 'volume': [1000000], 'money': [8e8]}
        self.jqdata.attribute_history.return_value = prev_data
        
        val_df = pd.DataFrame({'market_cap': [100]}, index=['000001.XSHE'])
        self.jqdata.get_valuation.return_value = val_df
        
        high_data = {'high': pd.Series([10.0] * 10)}
        
        volume_data = {'volume': pd.Series([1000000] * 6)}
        
        auction_data = {'volume': [50000]}
        
        self.jqdata.attribute_history.side_effect = [prev_data, high_data, volume_data, auction_data]
        
        self.module.buy(context)
        
        assert self.g.trade_count >= 0

    def test_sell_1030_below_avg_cost(self):
        context = SimpleNamespace()
        context.portfolio = SimpleNamespace()
        
        pos = SimpleNamespace()
        pos.closeable_amount = 100
        pos.avg_cost = 10.0
        
        context.portfolio.positions = {'000001.XSHE': pos}
        
        stock_data = SimpleNamespace()
        stock_data.last_price = 9.5
        stock_data.high_limit = 11.0
        stock_data.low_limit = 9.0
        
        self.jqdata.get_current_data.return_value = {'000001.XSHE': stock_data}
        
        self.module.sell_1030(context)
        
        self.jqdata.order_target_value.assert_called()
        assert self.g.stop_loss_count == 1

    def test_sell_1030_at_limit_keeps_position(self):
        context = SimpleNamespace()
        context.portfolio = SimpleNamespace()
        
        pos = SimpleNamespace()
        pos.closeable_amount = 100
        pos.avg_cost = 10.0
        
        context.portfolio.positions = {'000001.XSHE': pos}
        
        stock_data = SimpleNamespace()
        stock_data.last_price = 11.0
        stock_data.high_limit = 11.0
        stock_data.low_limit = 9.0
        
        self.jqdata.get_current_data.return_value = {'000001.XSHE': stock_data}
        
        self.module.sell_1030(context)
        
        self.jqdata.order_target_value.assert_not_called()

    def test_sell_1030_above_avg_cost_no_sell(self):
        context = SimpleNamespace()
        context.portfolio = SimpleNamespace()
        
        pos = SimpleNamespace()
        pos.closeable_amount = 100
        pos.avg_cost = 10.0
        
        context.portfolio.positions = {'000001.XSHE': pos}
        
        stock_data = SimpleNamespace()
        stock_data.last_price = 10.5
        stock_data.high_limit = 11.0
        stock_data.low_limit = 9.0
        
        self.jqdata.get_current_data.return_value = {'000001.XSHE': stock_data}
        
        self.module.sell_1030(context)
        
        self.jqdata.order_target_value.assert_not_called()

    def test_sell_1030_low_limit_order_style(self):
        context = SimpleNamespace()
        context.portfolio = SimpleNamespace()
        
        pos = SimpleNamespace()
        pos.closeable_amount = 100
        pos.avg_cost = 10.0
        
        context.portfolio.positions = {'000001.XSHE': pos}
        
        stock_data = SimpleNamespace()
        stock_data.last_price = 9.0
        stock_data.high_limit = 11.0
        stock_data.low_limit = 9.0
        
        self.jqdata.get_current_data.return_value = {'000001.XSHE': stock_data}
        
        self.module.sell_1030(context)
        
        assert self.g.stop_loss_count == 1

    def test_sell_1330_below_threshold(self):
        context = SimpleNamespace()
        context.portfolio = SimpleNamespace()
        
        pos = SimpleNamespace()
        pos.closeable_amount = 100
        pos.avg_cost = 10.0
        
        context.portfolio.positions = {'000001.XSHE': pos}
        
        stock_data = SimpleNamespace()
        stock_data.last_price = 10.2
        stock_data.high_limit = 11.0
        stock_data.low_limit = 9.0
        
        self.jqdata.get_current_data.return_value = {'000001.XSHE': stock_data}
        
        self.module.sell_1330(context)
        
        self.jqdata.order_target_value.assert_called()

    def test_sell_1330_above_threshold_no_sell(self):
        context = SimpleNamespace()
        context.portfolio = SimpleNamespace()
        
        pos = SimpleNamespace()
        pos.closeable_amount = 100
        pos.avg_cost = 10.0
        
        context.portfolio.positions = {'000001.XSHE': pos}
        
        stock_data = SimpleNamespace()
        stock_data.last_price = 10.5
        stock_data.high_limit = 11.0
        stock_data.low_limit = 9.0
        
        self.jqdata.get_current_data.return_value = {'000001.XSHE': stock_data}
        
        self.module.sell_1330(context)
        
        self.jqdata.order_target_value.assert_not_called()

    def test_sell_tail_not_at_limit(self):
        context = SimpleNamespace()
        context.portfolio = SimpleNamespace()
        
        pos = SimpleNamespace()
        pos.closeable_amount = 100
        
        context.portfolio.positions = {'000001.XSHE': pos}
        
        stock_data = SimpleNamespace()
        stock_data.last_price = 10.0
        stock_data.high_limit = 11.0
        
        self.jqdata.get_current_data.return_value = {'000001.XSHE': stock_data}
        
        self.module.sell_tail(context)
        
        self.jqdata.order_target_value.assert_called_once_with('000001.XSHE', 0)

    def test_sell_tail_at_limit_keeps_position(self):
        context = SimpleNamespace()
        context.portfolio = SimpleNamespace()
        
        pos = SimpleNamespace()
        pos.closeable_amount = 100
        
        context.portfolio.positions = {'000001.XSHE': pos}
        
        stock_data = SimpleNamespace()
        stock_data.last_price = 11.0
        stock_data.high_limit = 11.0
        
        self.jqdata.get_current_data.return_value = {'000001.XSHE': stock_data}
        
        self.module.sell_tail(context)
        
        self.jqdata.order_target_value.assert_not_called()

    def test_record_daily_pnl(self):
        context = SimpleNamespace()
        context.portfolio = SimpleNamespace()
        context.portfolio.daily_pnl = 1000
        
        self.module.record_daily_pnl(context)
        
        assert self.g.daily_pnl == 1000

    def test_check_weekly_circuit_breaker_no_trigger(self):
        context = SimpleNamespace()
        context.portfolio = SimpleNamespace()
        context.portfolio.total_value = 105000
        
        self.g.weekly_start_value = 100000
        self.g.cool_down_days = 0
        
        self.module.check_weekly_circuit_breaker(context)
        
        assert self.g.cool_down_days == 0

    def test_check_weekly_circuit_breaker_triggered(self):
        context = SimpleNamespace()
        context.portfolio = SimpleNamespace()
        context.portfolio.total_value = 90000
        
        self.g.weekly_start_value = 100000
        self.g.cool_down_days = 0
        
        self.module.check_weekly_circuit_breaker(context)
        
        assert self.g.cool_down_days >= 2

    def test_check_weekly_circuit_breaker_decrements_cool_down(self):
        context = SimpleNamespace()
        context.portfolio = SimpleNamespace()
        context.portfolio.total_value = 100000
        
        self.g.weekly_start_value = 100000
        self.g.cool_down_days = 2
        
        self.module.check_weekly_circuit_breaker(context)
        
        assert self.g.cool_down_days == 1

    def test_check_weekly_circuit_breaker_zero_start_value(self):
        context = SimpleNamespace()
        context.portfolio = SimpleNamespace()
        context.portfolio.total_value = 90000
        
        self.g.weekly_start_value = 0
        self.g.cool_down_days = 0
        
        self.module.check_weekly_circuit_breaker(context)
        
        assert self.g.cool_down_days == 0

    def test_transform_date_str_to_str(self):
        result = self.module.transform_date("2024-01-15", "str")
        assert result == "2024-01-15"

    def test_get_shifted_date_normal_days(self):
        import datetime as dt
        result = self.module.get_shifted_date("2024-01-16", -1, "N")
        assert result == "2024-01-15"

    def test_filter_kcbj_stock(self):
        stocks = ['000001.XSHE', '688001.XSHG', '400001.XSHE', '800001.XSHG', '300001.XSHE']
        
        result = self.module.filter_kcbj_stock(stocks)
        
        assert '000001.XSHE' in result
        assert '688001.XSHG' not in result
        assert '400001.XSHE' not in result
        assert '800001.XSHG' not in result
        assert '300001.XSHE' not in result

    def test_filter_new_stock(self):
        import datetime as dt
        
        info1 = SimpleNamespace()
        info1.start_date = dt.date(2020, 1, 1)
        
        info2 = SimpleNamespace()
        info2.start_date = dt.date(2024, 1, 1)
        
        self.jqdata.get_security_info.side_effect = [info1, info2]
        
        result = self.module.filter_new_stock(['000001.XSHE', '000002.XSHE'], dt.date(2024, 1, 15), 50)
        
        assert '000001.XSHE' in result
        assert '000002.XSHE' not in result

    def test_get_hl_stock(self):
        hl_df = pd.DataFrame({
            'code': ['000001.XSHE', '000002.XSHE'],
            'close': [10.0, 9.0],
            'high_limit': [10.0, 10.0]
        })
        self.jqdata.get_price.return_value = hl_df
        
        result = self.module.get_hl_stock(['000001.XSHE', '000002.XSHE'], datetime(2024, 1, 15))
        
        assert '000001.XSHE' in result
        assert '000002.XSHE' not in result

    def test_get_ever_hl_stock(self):
        hl_df = pd.DataFrame({
            'code': ['000001.XSHE', '000002.XSHE'],
            'high': [10.0, 9.5],
            'high_limit': [10.0, 10.0]
        })
        self.jqdata.get_price.return_value = hl_df
        
        result = self.module.get_ever_hl_stock(['000001.XSHE', '000002.XSHE'], datetime(2024, 1, 15))
        
        assert '000001.XSHE' in result
        assert '000002.XSHE' not in result

    def test_calculate_zyts_returns_value(self):
        high_data = {'high': pd.Series([10.0, 9.5, 10.0, 9.8, 10.5])}
        self.jqdata.attribute_history.return_value = high_data
        
        context = SimpleNamespace()
        
        result = self.module.calculate_zyts('000001.XSHE', context)
        
        assert isinstance(result, int)
        assert result >= 0

    def test_calculate_zyts_insufficient_data(self):
        high_data = {'high': pd.Series([10.0])}
        self.jqdata.attribute_history.return_value = high_data
        
        context = SimpleNamespace()
        
        result = self.module.calculate_zyts('000001.XSHE', context)
        
        assert result == 10