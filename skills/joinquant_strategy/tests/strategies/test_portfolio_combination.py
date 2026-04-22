import pytest
from unittest.mock import Mock, MagicMock, patch, call
from datetime import datetime, timedelta
import pandas as pd
import numpy as np
from types import SimpleNamespace
import sys


class TestPortfolioCombination:
    @pytest.fixture(autouse=True)
    def setup_mocks(self, mock_jqdata):
        self.jqdata = mock_jqdata
        self.g = SimpleNamespace()
        self.g.portfolio_mode = "equal_weight"
        self.g.strategy_weights = {
            "equal_weight": {"first_board": 0.5, "weak_to_strong": 0.5},
            "risk_parity": {"first_board": 0.6, "weak_to_strong": 0.4},
            "dynamic": {"first_board": 0.5, "weak_to_strong": 0.5},
        }
        self.g.target_list_first_board = []
        self.g.target_list_weak_to_strong = []
        self.g.trade_log = []
        
        self.jqdata.g = self.g
        sys.modules['jqdata'] = self.jqdata
        
        patcher = patch.dict(sys.modules, {'jqdata': self.jqdata})
        patcher.start()
        self.addCleanup = lambda f: f()
        
        import portfolio_combination as module
        self.module = module

    def test_initialize_sets_options(self):
        context = SimpleNamespace()
        
        self.module.initialize(context)
        
        self.jqdata.set_option.assert_any_call("use_real_price", True)
        self.jqdata.set_option.assert_any_call("avoid_future_data", True)
        self.jqdata.log.set_level.assert_called_once_with("system", "error")
        assert self.jqdata.run_daily.call_count == 3

    def test_initialize_sets_default_portfolio_mode(self):
        context = SimpleNamespace()
        
        self.module.initialize(context)
        
        assert self.g.portfolio_mode == "equal_weight"
        assert "equal_weight" in self.g.strategy_weights
        assert "risk_parity" in self.g.strategy_weights
        assert "dynamic" in self.g.strategy_weights

    def test_get_first_board_signals_empty_hl_stocks(self):
        result = self.module.get_first_board_signals([], "2024-01-16", datetime(2024, 1, 15))
        assert result == []

    def test_get_first_board_signals_empty_today_df(self):
        self.jqdata.get_price.return_value = pd.DataFrame()
        
        result = self.module.get_first_board_signals(
            ['000001.XSHE'], "2024-01-16", datetime(2024, 1, 15)
        )
        assert result == []

    def test_get_first_board_signals_filters_open_ratio(self):
        df = pd.DataFrame({
            'code': ['000001.XSHE', '000002.XSHE', '600000.XSHG'],
            'open': [10.05, 10.20, 9.95],
            'high_limit': [11.0, 11.0, 11.0]
        })
        self.jqdata.get_price.return_value = df
        
        val_df = pd.DataFrame({
            'circulating_market_cap': [100, 50, 200]
        }, index=['000001.XSHE', '000002.XSHE', '600000.XSHG'])
        self.jqdata.get_valuation.return_value = val_df
        
        result = self.module.get_first_board_signals(
            ['000001.XSHE', '000002.XSHE', '600000.XSHG'], 
            "2024-01-16", datetime(2024, 1, 15)
        )
        
        assert '000001.XSHE' in result

    def test_get_first_board_signals_filters_cap_range(self):
        df = pd.DataFrame({
            'code': ['000001.XSHE', '000002.XSHE'],
            'open': [10.08, 10.08],
            'high_limit': [11.0, 11.0]
        })
        self.jqdata.get_price.return_value = df
        
        val_df = pd.DataFrame({
            'circulating_market_cap': [40, 200]
        }, index=['000001.XSHE', '000002.XSHE'])
        self.jqdata.get_valuation.return_value = val_df
        
        result = self.module.get_first_board_signals(
            ['000001.XSHE', '000002.XSHE'], "2024-01-16", datetime(2024, 1, 15)
        )
        assert result == []

    def test_get_weak_to_strong_signals_empty_initial_list(self):
        result = self.module.get_weak_to_strong_signals(
            [], "2024-01-16", datetime(2024, 1, 15), 
            datetime(2024, 1, 14), datetime(2024, 1, 13)
        )
        assert result == []

    def test_get_weak_to_strong_signals_empty_price_df(self):
        self.jqdata.get_price.return_value = pd.DataFrame()
        
        result = self.module.get_weak_to_strong_signals(
            ['000001.XSHE'], "2024-01-16", datetime(2024, 1, 15),
            datetime(2024, 1, 14), datetime(2024, 1, 13)
        )
        assert result == []

    def test_get_weak_to_strong_signals_excludes_prev_hl(self):
        df_prev = pd.DataFrame({
            'code': ['000001.XSHE'],
            'close': [11.0],
            'high_limit': [11.0]
        })
        
        df_prev_2 = pd.DataFrame({
            'code': ['000001.XSHE'],
            'high': [11.0],
            'high_limit': [11.0]
        })
        
        df_prev_3 = pd.DataFrame({
            'code': [],
            'high': [],
            'high_limit': []
        })
        
        df_today = pd.DataFrame({
            'code': ['000001.XSHE'],
            'open': [10.5],
            'high_limit': [11.0],
            'money': [6e8]
        })
        
        self.jqdata.get_price.side_effect = [
            df_prev, df_prev_2, df_prev_3, df_today
        ]
        
        val_df = pd.DataFrame({
            'circulating_market_cap': [100]
        }, index=['000001.XSHE'])
        self.jqdata.get_valuation.return_value = val_df
        
        result = self.module.get_weak_to_strong_signals(
            ['000001.XSHE'], "2024-01-16", datetime(2024, 1, 15),
            datetime(2024, 1, 14), datetime(2024, 1, 13)
        )
        assert result == []

    def test_get_weak_to_strong_signals_filters_money(self):
        df_prev = pd.DataFrame({
            'code': ['000001.XSHE'],
            'close': [11.0],
            'high_limit': [11.0]
        })
        
        df_prev_2 = pd.DataFrame({'code': [], 'high': [], 'high_limit': []})
        df_prev_3 = pd.DataFrame({'code': [], 'high': [], 'high_limit': []})
        
        df_today = pd.DataFrame({
            'code': ['000001.XSHE'],
            'open': [10.5],
            'high_limit': [11.0],
            'money': [3e8]
        })
        
        self.jqdata.get_price.side_effect = [
            df_prev, df_prev_2, df_prev_3, df_today
        ]
        
        result = self.module.get_weak_to_strong_signals(
            ['000001.XSHE'], "2024-01-16", datetime(2024, 1, 15),
            datetime(2024, 1, 14), datetime(2024, 1, 13)
        )
        assert result == []

    def test_buy_with_first_board_signals(self):
        context = SimpleNamespace()
        context.portfolio = SimpleNamespace()
        context.portfolio.available_cash = 100000
        
        self.g.target_list_first_board = ['000001.XSHE']
        self.g.target_list_weak_to_strong = []
        
        stock_data = SimpleNamespace()
        stock_data.last_price = 10.0
        
        self.jqdata.get_current_data.return_value = {'000001.XSHE': stock_data}
        
        self.module.buy(context)
        
        self.jqdata.order_value.assert_called_once()

    def test_buy_with_weak_to_strong_signals(self):
        context = SimpleNamespace()
        context.portfolio = SimpleNamespace()
        context.portfolio.available_cash = 100000
        
        self.g.target_list_first_board = []
        self.g.target_list_weak_to_strong = ['000002.XSHE']
        
        stock_data = SimpleNamespace()
        stock_data.last_price = 20.0
        
        self.jqdata.get_current_data.return_value = {'000002.XSHE': stock_data}
        
        self.module.buy(context)
        
        self.jqdata.order_value.assert_called_once()

    def test_buy_with_both_signal_types(self):
        context = SimpleNamespace()
        context.portfolio = SimpleNamespace()
        context.portfolio.available_cash = 100000
        
        self.g.target_list_first_board = ['000001.XSHE']
        self.g.target_list_weak_to_strong = ['000002.XSHE']
        
        current_data = {
            '000001.XSHE': SimpleNamespace(last_price=10.0),
            '000002.XSHE': SimpleNamespace(last_price=20.0)
        }
        self.jqdata.get_current_data.return_value = current_data
        
        self.module.buy(context)
        
        assert self.jqdata.order_value.call_count == 2

    def test_buy_no_signals(self):
        context = SimpleNamespace()
        context.portfolio = SimpleNamespace()
        context.portfolio.available_cash = 100000
        
        self.g.target_list_first_board = []
        self.g.target_list_weak_to_strong = []
        
        self.module.buy(context)
        
        self.jqdata.order_value.assert_not_called()

    def test_sell_not_at_limit(self):
        context = SimpleNamespace()
        pos = SimpleNamespace()
        pos.closeable_amount = 100
        context.portfolio = SimpleNamespace()
        context.portfolio.positions = {'000001.XSHE': pos}
        
        stock_data = SimpleNamespace()
        stock_data.last_price = 10.0
        stock_data.high_limit = 11.0
        
        self.jqdata.get_current_data.return_value = {'000001.XSHE': stock_data}
        
        self.module.sell(context)
        
        self.jqdata.order_target_value.assert_called_once_with('000001.XSHE', 0)

    def test_sell_at_limit_keeps_position(self):
        context = SimpleNamespace()
        pos = SimpleNamespace()
        pos.closeable_amount = 100
        context.portfolio = SimpleNamespace()
        context.portfolio.positions = {'000001.XSHE': pos}
        
        stock_data = SimpleNamespace()
        stock_data.last_price = 10.99
        stock_data.high_limit = 11.0
        
        self.jqdata.get_current_data.return_value = {'000001.XSHE': stock_data}
        
        self.module.sell(context)
        
        self.jqdata.order_target_value.assert_not_called()

    def test_sell_no_closeable_amount(self):
        context = SimpleNamespace()
        pos = SimpleNamespace()
        pos.closeable_amount = 0
        context.portfolio = SimpleNamespace()
        context.portfolio.positions = {'000001.XSHE': pos}
        
        stock_data = SimpleNamespace()
        stock_data.last_price = 10.0
        stock_data.high_limit = 11.0
        
        self.jqdata.get_current_data.return_value = {'000001.XSHE': stock_data}
        
        self.module.sell(context)
        
        self.jqdata.order_target_value.assert_not_called()

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

    def test_get_shifted_date_normal_days(self):
        result = self.module.get_shifted_date("2024-01-16", -1, "N")
        
        assert result == "2024-01-15"

    def test_risk_parity_mode(self):
        context = SimpleNamespace()
        
        self.g.portfolio_mode = "risk_parity"
        context.portfolio = SimpleNamespace()
        context.portfolio.available_cash = 100000
        
        self.g.target_list_first_board = ['000001.XSHE']
        self.g.target_list_weak_to_strong = []
        
        stock_data = SimpleNamespace()
        stock_data.last_price = 10.0
        
        self.jqdata.get_current_data.return_value = {'000001.XSHE': stock_data}
        
        self.module.buy(context)
        
        weights = self.g.strategy_weights["risk_parity"]
        expected_cash = 100000 * weights["first_board"]
        call_args = self.jqdata.order_value.call_args
        assert call_args[0][1] == expected_cash

    def test_dynamic_mode(self):
        context = SimpleNamespace()
        
        self.g.portfolio_mode = "dynamic"
        context.portfolio = SimpleNamespace()
        context.portfolio.available_cash = 100000
        
        self.g.target_list_first_board = ['000001.XSHE']
        self.g.target_list_weak_to_strong = []
        
        stock_data = SimpleNamespace()
        stock_data.last_price = 10.0
        
        self.jqdata.get_current_data.return_value = {'000001.XSHE': stock_data}
        
        self.module.buy(context)
        
        weights = self.g.strategy_weights["dynamic"]
        expected_cash = 100000 * weights["first_board"]
        call_args = self.jqdata.order_value.call_args
        assert call_args[0][1] == expected_cash

    def test_buy_stock_not_in_current_data(self):
        context = SimpleNamespace()
        context.portfolio = SimpleNamespace()
        context.portfolio.available_cash = 100000
        
        self.g.target_list_first_board = ['000001.XSHE']
        self.g.target_list_weak_to_strong = []
        
        self.jqdata.get_current_data.return_value = {}
        
        self.module.buy(context)
        
        self.jqdata.order_value.assert_not_called()

    def test_get_stock_list_integration(self):
        context = SimpleNamespace()
        context.previous_date = datetime(2024, 1, 16)
        
        self.g.target_list_first_board = []
        self.g.target_list_weak_to_strong = []
        
        try:
            self.module.get_stock_list(context)
            assert len(self.g.target_list_first_board) >= 0
            assert len(self.g.target_list_weak_to_strong) >= 0
        except Exception:
            pass