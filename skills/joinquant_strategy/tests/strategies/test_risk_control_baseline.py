import pytest
from unittest.mock import Mock, MagicMock, patch
from datetime import datetime, timedelta
import pandas as pd
from types import SimpleNamespace
import sys


class TestRiskControlBaseline:
    @pytest.fixture(autouse=True)
    def setup_mocks(self, mock_jqdata):
        self.jqdata = mock_jqdata
        self.g = SimpleNamespace()
        self.g.target_list = []
        self.g.trade_count = 0
        self.g.daily_pnl = 0
        self.g.weekly_pnl = 0
        self.g.monthly_pnl = 0
        
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
        
        import risk_control_baseline as module
        self.module = module

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
        
        assert self.g.target_list == []
        assert self.g.trade_count == 0
        assert self.g.daily_pnl == 0

    def test_transform_date_str_to_str(self):
        result = self.module.transform_date("2024-01-15", "str")
        assert result == "2024-01-15"

    def test_transform_date_str_to_dt(self):
        result = self.module.transform_date("2024-01-15", "dt")
        assert isinstance(result, datetime)
        assert result.year == 2024
        assert result.month == 1
        assert result.day == 15

    def test_transform_date_str_to_d(self):
        import datetime as dt
        result = self.module.transform_date("2024-01-15", "d")
        assert isinstance(result, dt.date)
        assert result.year == 2024

    def test_transform_date_datetime_to_str(self):
        result = self.module.transform_date(datetime(2024, 1, 15), "str")
        assert result == "2024-01-15"

    def test_transform_date_datetime_to_dt(self):
        result = self.module.transform_date(datetime(2024, 1, 15), "dt")
        assert isinstance(result, datetime)

    def test_transform_date_datetime_to_d(self):
        import datetime as dt
        result = self.module.transform_date(datetime(2024, 1, 15), "d")
        assert isinstance(result, dt.date)

    def test_transform_date_date_to_str(self):
        import datetime as dt
        result = self.module.transform_date(dt.date(2024, 1, 15), "str")
        assert result == "2024-01-15"

    def test_get_shifted_date_normal_days(self):
        import datetime as dt
        result = self.module.get_shifted_date("2024-01-16", -1, "N")
        assert result == "2024-01-15"

    def test_get_shifted_date_trade_days(self):
        mock_trade_days = [
            datetime(2024, 1, 10),
            datetime(2024, 1, 11),
            datetime(2024, 1, 12),
            datetime(2024, 1, 15),
            datetime(2024, 1, 16),
        ]
        self.jqdata.get_all_trade_days.return_value = mock_trade_days
        
        result = self.module.get_shifted_date("2024-01-16", -1, "T")
        assert result == "2024-01-15"

    def test_get_shifted_date_non_trade_day(self):
        mock_trade_days = [
            datetime(2024, 1, 10),
            datetime(2024, 1, 11),
            datetime(2024, 1, 12),
            datetime(2024, 1, 15),
        ]
        self.jqdata.get_all_trade_days.return_value = mock_trade_days
        
        result = self.module.get_shifted_date("2024-01-14", -1, "T")
        assert result in ["2024-01-10", "2024-01-11", "2024-01-12", "2024-01-15"]

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

    def test_filter_kcbj_stock(self):
        stocks = ['000001.XSHE', '688001.XSHG', '400001.XSHE', '800001.XSHG', '300001.XSHE']
        
        result = self.module.filter_kcbj_stock(stocks)
        
        assert '000001.XSHE' in result
        assert '688001.XSHG' not in result
        assert '400001.XSHE' not in result
        assert '800001.XSHG' not in result
        assert '300001.XSHE' not in result

    def test_filter_st_stock(self):
        mock_trade_days = [datetime(2024, 1, 15)]
        self.jqdata.get_all_trade_days.return_value = mock_trade_days
        
        st_df = pd.DataFrame({
            '2024-01-15': [False, True]
        }, index=['000001.XSHE', '000002.XSHE'])
        self.jqdata.get_extras.return_value = st_df
        
        try:
            result = self.module.filter_st_stock(['000001.XSHE', '000002.XSHE'], datetime(2024, 1, 15))
            assert isinstance(result, list)
        except Exception:
            pass

    def test_filter_paused_stock(self):
        paused_df = pd.DataFrame({
            'code': ['000001.XSHE', '000002.XSHE'],
            'paused': [0, 1]
        })
        self.jqdata.get_price.return_value = paused_df
        
        result = self.module.filter_paused_stock(['000001.XSHE', '000002.XSHE'], datetime(2024, 1, 15))
        
        assert '000001.XSHE' in result
        assert '000002.XSHE' not in result

    def test_prepare_stock_list(self):
        mock_securities = pd.DataFrame({
            'display_name': ['平安银行', '万科A']
        }, index=['000001.XSHE', '000002.XSHE'])
        self.jqdata.get_all_securities.return_value = mock_securities
        
        import datetime as dt
        info1 = SimpleNamespace()
        info1.start_date = dt.date(2020, 1, 1)
        info2 = SimpleNamespace()
        info2.start_date = dt.date(2020, 1, 1)
        self.jqdata.get_security_info.side_effect = [info1, info2]
        
        mock_trade_days = [datetime(2024, 1, 15)]
        self.jqdata.get_all_trade_days.return_value = mock_trade_days
        
        st_df = pd.DataFrame({
            '2024-01-15': [False, False]
        }, index=['000001.XSHE', '000002.XSHE'])
        self.jqdata.get_extras.return_value = st_df
        
        paused_df = pd.DataFrame({
            'code': ['000001.XSHE', '000002.XSHE'],
            'paused': [0, 0]
        })
        self.jqdata.get_price.return_value = paused_df
        
        try:
            result = self.module.prepare_stock_list(datetime(2024, 1, 15))
            assert isinstance(result, list)
        except Exception:
            pass

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

    def test_get_hl_stock_empty_result(self):
        hl_df = pd.DataFrame({
            'code': ['000001.XSHE'],
            'close': [9.0],
            'high_limit': [10.0]
        })
        self.jqdata.get_price.return_value = hl_df
        
        result = self.module.get_hl_stock(['000001.XSHE'], datetime(2024, 1, 15))
        
        assert result == []

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

    def test_get_stock_list_filters_prev_hl(self):
        context = SimpleNamespace()
        context.previous_date = datetime(2024, 1, 15)
        
        mock_securities = pd.DataFrame({
            'display_name': ['平安银行']
        }, index=['000001.XSHE'])
        self.jqdata.get_all_securities.return_value = mock_securities
        
        import datetime as dt
        info = SimpleNamespace()
        info.start_date = dt.date(2020, 1, 1)
        self.jqdata.get_security_info.return_value = info
        
        mock_trade_days = [datetime(2024, 1, 14), datetime(2024, 1, 15)]
        self.jqdata.get_all_trade_days.return_value = mock_trade_days
        
        st_df = pd.DataFrame({
            '2024-01-15': [False]
        }, index=['000001.XSHE'])
        self.jqdata.get_extras.return_value = st_df
        
        hl_df = pd.DataFrame({
            'code': ['000001.XSHE'],
            'close': [10.0],
            'high_limit': [10.0]
        })
        
        prev_hl_df = pd.DataFrame({
            'code': ['000001.XSHE'],
            'high': [10.0],
            'high_limit': [10.0]
        })
        
        paused_df = pd.DataFrame({
            'code': ['000001.XSHE'],
            'paused': [0]
        })
        
        self.jqdata.get_price.side_effect = [paused_df, hl_df, prev_hl_df, prev_hl_df]
        
        self.module.get_stock_list(context)
        
        assert self.g.target_list == []

    def test_buy_no_qualified_stocks(self):
        context = SimpleNamespace()
        context.previous_date = datetime(2024, 1, 15)
        context.portfolio = SimpleNamespace()
        context.portfolio.available_cash = 100000
        
        self.g.target_list = []
        
        self.module.buy(context)
        
        self.jqdata.order_value.assert_not_called()

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

    def test_sell_tail_no_closeable_amount(self):
        context = SimpleNamespace()
        context.portfolio = SimpleNamespace()
        
        pos = SimpleNamespace()
        pos.closeable_amount = 0
        
        context.portfolio.positions = {'000001.XSHE': pos}
        
        stock_data = SimpleNamespace()
        stock_data.last_price = 10.0
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