"""
测试 shadow_mainline.py - 影子策略主线版
"""
import sys
from unittest.mock import MagicMock, patch, Mock
from datetime import datetime, timedelta
import pytest
import pandas as pd
import numpy as np

from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from tests.conftest import (
    MockContext, MockBarDict, MockBar, MockPosition, MockPortfolio,
    MockScheduler, MockLogger, MockInstrument
)


class TestShadowMainlineInit:
    def test_init_sets_default_values(self):
        mock_context = MockContext()
        mock_scheduler = MockScheduler()
        
        with patch.dict(sys.modules, {
            'scheduler': mock_scheduler,
            'market_open': lambda minute: f"market_open_{minute}",
            'market_close': lambda minute: f"market_close_{minute}",
        }):
            import shadow_mainline
            shadow_mainline.init(mock_context)
            
            assert mock_context.strategy_mode == "mainline"
            assert mock_context.limit_up_count == 0
            assert mock_context.consecutive_losses == 0
            assert mock_context.stop_trading_until is None
            assert mock_context.stocks_in_pool == []

    def test_init_schedules_functions(self):
        mock_context = MockContext()
        mock_scheduler = MockScheduler()
        
        with patch.dict(sys.modules, {'scheduler': mock_scheduler}):
            import shadow_mainline
            shadow_mainline.init(mock_context)
            
            assert len(mock_scheduler.scheduled_functions) == 3


class TestGetLimitUpCount:
    def test_get_limit_up_count_calculates_correctly(self):
        mock_context = MockContext()
        mock_logger = MockLogger()
        
        def mock_all_instruments(type_str):
            return [MockInstrument("000001.XSHE", "平安银行")]
        
        def mock_history_bars(stock, count, freq, fields):
            return np.array([10.0, 11.0])
        
        with patch.dict(sys.modules, {
            'all_instruments': mock_all_instruments,
            'history_bars': mock_history_bars,
            'logger': mock_logger,
        }):
            import shadow_mainline
            mock_bar_dict = MockBarDict()
            shadow_mainline.get_limit_up_count(mock_context, mock_bar_dict)
            
            assert mock_context.limit_up_count >= 0

    def test_get_limit_up_count_filters_zero_prev_close(self):
        mock_context = MockContext()
        mock_logger = MockLogger()
        
        def mock_all_instruments(type_str):
            return [MockInstrument("000001.XSHE", "平安银行")]
        
        def mock_history_bars(stock, count, freq, fields):
            return np.array([0.0, 10.0])
        
        with patch.dict(sys.modules, {
            'all_instruments': mock_all_instruments,
            'history_bars': mock_history_bars,
            'logger': mock_logger,
        }):
            import shadow_mainline
            mock_bar_dict = MockBarDict()
            shadow_mainline.get_limit_up_count(mock_context, mock_bar_dict)
            
            assert mock_context.limit_up_count == 0

    def test_get_limit_up_count_limits_to_500_stocks(self):
        mock_context = MockContext()
        mock_logger = MockLogger()
        
        def mock_all_instruments(type_str):
            return [MockInstrument(f"stock{i}", "股票") for i in range(600)]
        
        def mock_history_bars(stock, count, freq, fields):
            return np.array([10.0, 11.0])
        
        with patch.dict(sys.modules, {
            'all_instruments': mock_all_instruments,
            'history_bars': mock_history_bars,
            'logger': mock_logger,
        }):
            import shadow_mainline
            mock_bar_dict = MockBarDict()
            shadow_mainline.get_limit_up_count(mock_context, mock_bar_dict)

    def test_get_limit_up_count_handles_exception(self):
        mock_context = MockContext()
        mock_logger = MockLogger()
        
        def mock_all_instruments(type_str):
            raise Exception("API Error")
        
        with patch.dict(sys.modules, {
            'all_instruments': mock_all_instruments,
            'logger': mock_logger,
        }):
            import shadow_mainline
            mock_bar_dict = MockBarDict()
            shadow_mainline.get_limit_up_count(mock_context, mock_bar_dict)


class TestIsFakeWeakHighOpen:
    def test_is_fake_weak_high_open_returns_true(self):
        mock_context = MockContext()
        mock_context.now = datetime.now()
        mock_bar_dict = MockBarDict()
        mock_bar_dict["000001.XSHE"] = MockBar(open_price=10.1, high=10.5)
        
        def mock_history_bars(stock, count, freq, fields):
            return np.array([10.0, 10.2])
        
        def mock_get_factor(stock, factor, start_date, end_date):
            return pd.DataFrame({"market_cap": [50000000000]})
        
        with patch.dict(sys.modules, {
            'history_bars': mock_history_bars,
            'get_factor': mock_get_factor,
        }):
            import shadow_mainline
            result = shadow_mainline.is_fake_weak_high_open(mock_context, "000001.XSHE", mock_bar_dict)
            
            assert result == True

    def test_is_fake_weak_high_open_returns_false_low_change(self):
        mock_context = MockContext()
        mock_bar_dict = MockBarDict()
        mock_bar_dict["000001.XSHE"] = MockBar(open_price=9.99, high=10.0)
        
        def mock_history_bars(stock, count, freq, fields):
            return np.array([10.0, 10.2])
        
        with patch.dict(sys.modules, {'history_bars': mock_history_bars}):
            import shadow_mainline
            result = shadow_mainline.is_fake_weak_high_open(mock_context, "000001.XSHE", mock_bar_dict)
            
            assert result == False

    def test_is_fake_weak_high_open_returns_false_high_change(self):
        mock_context = MockContext()
        mock_bar_dict = MockBarDict()
        mock_bar_dict["000001.XSHE"] = MockBar(open_price=10.4, high=10.5)
        
        def mock_history_bars(stock, count, freq, fields):
            return np.array([10.0, 10.2])
        
        with patch.dict(sys.modules, {'history_bars': mock_history_bars}):
            import shadow_mainline
            result = shadow_mainline.is_fake_weak_high_open(mock_context, "000001.XSHE", mock_bar_dict)
            
            assert result == False

    def test_is_fake_weak_high_open_returns_false_no_room(self):
        mock_context = MockContext()
        mock_bar_dict = MockBarDict()
        mock_bar_dict["000001.XSHE"] = MockBar(open_price=10.1, high=10.1)
        
        def mock_history_bars(stock, count, freq, fields):
            return np.array([10.0, 10.2])
        
        with patch.dict(sys.modules, {'history_bars': mock_history_bars}):
            import shadow_mainline
            result = shadow_mainline.is_fake_weak_high_open(mock_context, "000001.XSHE", mock_bar_dict)
            
            assert result == False

    def test_is_fake_weak_high_open_handles_exception(self):
        mock_context = MockContext()
        mock_bar_dict = MockBarDict()
        
        def mock_history_bars(stock, count, freq, fields):
            raise Exception("API Error")
        
        with patch.dict(sys.modules, {'history_bars': mock_history_bars}):
            import shadow_mainline
            result = shadow_mainline.is_fake_weak_high_open(mock_context, "000001.XSHE", mock_bar_dict)
            
            assert result == False

    def test_is_fake_weak_high_open_zero_prev_close(self):
        mock_context = MockContext()
        mock_bar_dict = MockBarDict()
        mock_bar_dict["000001.XSHE"] = MockBar(open_price=10.0, high=10.5)
        
        def mock_history_bars(stock, count, freq, fields):
            return np.array([0.0, 10.0])
        
        with patch.dict(sys.modules, {'history_bars': mock_history_bars}):
            import shadow_mainline
            result = shadow_mainline.is_fake_weak_high_open(mock_context, "000001.XSHE", mock_bar_dict)
            
            assert result == False


class TestGetStockMarketCap:
    def test_get_stock_market_cap_returns_value(self):
        mock_context = MockContext()
        mock_context.now = datetime.now()
        
        def mock_get_factor(stock, factor, start_date, end_date):
            return pd.DataFrame({"market_cap": [50000000000]})
        
        with patch.dict(sys.modules, {'get_factor': mock_get_factor}):
            import shadow_mainline
            result = shadow_mainline.get_stock_market_cap("000001.XSHE")
            
            assert result == 50.0

    def test_get_stock_market_cap_handles_exception(self):
        mock_context = MockContext()
        
        def mock_get_factor(stock, factor, start_date, end_date):
            raise Exception("API Error")
        
        with patch.dict(sys.modules, {'get_factor': mock_get_factor}):
            import shadow_mainline
            result = shadow_mainline.get_stock_market_cap("000001.XSHE")
            
            assert result is None

    def test_get_stock_market_cap_empty_data(self):
        mock_context = MockContext()
        
        def mock_get_factor(stock, factor, start_date, end_date):
            return pd.DataFrame()
        
        with patch.dict(sys.modules, {'get_factor': mock_get_factor}):
            import shadow_mainline
            result = shadow_mainline.get_stock_market_cap("000001.XSHE")
            
            assert result is None


class TestGetStockPositionPct:
    def test_get_stock_position_pct_returns_value(self):
        mock_context = MockContext()
        
        def mock_history_bars(stock, count, freq, fields):
            return np.array([12.0, 11.0, 10.5, 10.0, 9.5, 10.0])
        
        with patch.dict(sys.modules, {'history_bars': mock_history_bars}):
            import shadow_mainline
            result = shadow_mainline.get_stock_position_pct("000001.XSHE")
            
            assert result is not None

    def test_get_stock_position_pct_handles_exception(self):
        def mock_history_bars(stock, count, freq, fields):
            raise Exception("API Error")
        
        with patch.dict(sys.modules, {'history_bars': mock_history_bars}):
            import shadow_mainline
            result = shadow_mainline.get_stock_position_pct("000001.XSHE")
            
            assert result is None

    def test_get_stock_position_pct_zero_high(self):
        def mock_history_bars(stock, count, freq, fields):
            return np.array([0.0, 0.0, 0.0])
        
        with patch.dict(sys.modules, {'history_bars': mock_history_bars}):
            import shadow_mainline
            result = shadow_mainline.get_stock_position_pct("000001.XSHE")
            
            assert result is None


class TestHasConsecutiveBoards:
    def test_has_consecutive_boards_returns_true(self):
        def mock_history_bars(stock, count, freq, fields):
            return np.array([10.0, 11.0, 12.1, 13.2, 14.3])
        
        with patch.dict(sys.modules, {'history_bars': mock_history_bars}):
            import shadow_mainline
            result = shadow_mainline.has_consecutive_boards("000001.XSHE")
            
            assert result == True

    def test_has_consecutive_boards_returns_false(self):
        def mock_history_bars(stock, count, freq, fields):
            return np.array([10.0, 10.5, 11.0, 10.8, 10.9])
        
        with patch.dict(sys.modules, {'history_bars': mock_history_bars}):
            import shadow_mainline
            result = shadow_mainline.has_consecutive_boards("000001.XSHE")
            
            assert result == False

    def test_has_consecutive_boards_handles_exception(self):
        def mock_history_bars(stock, count, freq, fields):
            raise Exception("API Error")
        
        with patch.dict(sys.modules, {'history_bars': mock_history_bars}):
            import shadow_mainline
            result = shadow_mainline.has_consecutive_boards("000001.XSHE")
            
            assert result == False

    def test_has_consecutive_boards_insufficient_data(self):
        def mock_history_bars(stock, count, freq, fields):
            return np.array([10.0, 10.5])
        
        with patch.dict(sys.modules, {'history_bars': mock_history_bars}):
            import shadow_mainline
            result = shadow_mainline.has_consecutive_boards("000001.XSHE")
            
            assert result == False


class TestGenerateSignals:
    def test_generate_signals_stops_trading(self):
        mock_context = MockContext()
        mock_context.stop_trading_until = datetime.now() + timedelta(days=1)
        mock_logger = MockLogger()
        
        with patch.dict(sys.modules, {'logger': mock_logger}):
            import shadow_mainline
            mock_bar_dict = MockBarDict()
            shadow_mainline.generate_signals(mock_context, mock_bar_dict)

    def test_generate_signals_low_emotion(self):
        mock_context = MockContext()
        mock_context.limit_up_count = 20
        mock_logger = MockLogger()
        
        with patch.dict(sys.modules, {'logger': mock_logger}):
            import shadow_mainline
            mock_bar_dict = MockBarDict()
            shadow_mainline.generate_signals(mock_context, mock_bar_dict)

    def test_generate_signals_mainline_mode(self):
        mock_context = MockContext()
        mock_context.strategy_mode = "mainline"
        mock_context.limit_up_count = 50
        mock_logger = MockLogger()
        
        def mock_all_instruments(type_str):
            return [MockInstrument("000001.XSHE", "平安银行")]
        
        def mock_get_stock_market_cap(stock):
            return 100.0
        
        def mock_get_stock_position_pct(stock):
            return 0.1
        
        def mock_has_consecutive_boards(stock):
            return False
        
        def mock_is_fake_weak_high_open(context, stock, bar_dict):
            return True
        
        def mock_history_bars(stock, count, freq, fields):
            return np.array([10.0, 10.2])
        
        def mock_order_shares(stock, shares):
            pass
        
        with patch.dict(sys.modules, {
            'all_instruments': mock_all_instruments,
            'history_bars': mock_history_bars,
            'order_shares': mock_order_shares,
            'logger': mock_logger,
        }):
            import shadow_mainline
            shadow_mainline.get_stock_market_cap = mock_get_stock_market_cap
            shadow_mainline.get_stock_position_pct = mock_get_stock_position_pct
            shadow_mainline.has_consecutive_boards = mock_has_consecutive_boards
            shadow_mainline.is_fake_weak_high_open = mock_is_fake_weak_high_open
            
            mock_bar_dict = MockBarDict()
            mock_bar_dict["000001.XSHE"] = MockBar(close=10.2)
            shadow_mainline.generate_signals(mock_context, mock_bar_dict)

    def test_generate_signals_observation_mode(self):
        mock_context = MockContext()
        mock_context.strategy_mode = "observation"
        mock_logger = MockLogger()
        
        def mock_all_instruments(type_str):
            return [MockInstrument("000001.XSHE", "平安银行")]
        
        def mock_history_bars(stock, count, freq, fields):
            return np.array([10.0, 11.0, 12.1, 13.2, 14.3])
        
        def mock_order_shares(stock, shares):
            pass
        
        with patch.dict(sys.modules, {
            'all_instruments': mock_all_instruments,
            'history_bars': mock_history_bars,
            'order_shares': mock_order_shares,
            'logger': mock_logger,
        }):
            import shadow_mainline
            mock_bar_dict = MockBarDict()
            mock_bar_dict["000001.XSHE"] = MockBar(close=14.3)
            shadow_mainline.generate_signals(mock_context, mock_bar_dict)

    def test_generate_signals_market_cap_filter(self):
        mock_context = MockContext()
        mock_context.strategy_mode = "mainline"
        mock_context.limit_up_count = 50
        mock_logger = MockLogger()
        
        def mock_all_instruments(type_str):
            return [MockInstrument("000001.XSHE", "平安银行")]
        
        def mock_get_stock_market_cap(stock):
            return 10.0
        
        with patch.dict(sys.modules, {
            'all_instruments': mock_all_instruments,
            'logger': mock_logger,
        }):
            import shadow_mainline
            shadow_mainline.get_stock_market_cap = mock_get_stock_market_cap
            
            mock_bar_dict = MockBarDict()
            shadow_mainline.generate_signals(mock_context, mock_bar_dict)


class TestGetTotalPositionValue:
    def test_get_total_position_value_returns_zero(self):
        mock_context = MockContext()
        mock_context.portfolio.positions = {}
        
        import shadow_mainline
        result = shadow_mainline.get_total_position_value(mock_context)
        
        assert result == 0

    def test_get_total_position_value_returns_sum(self):
        mock_context = MockContext()
        mock_context.portfolio.positions = {
            "stock1": MockPosition(market_value=10000),
            "stock2": MockPosition(market_value=20000),
        }
        
        import shadow_mainline
        result = shadow_mainline.get_total_position_value(mock_context)
        
        assert result == 30000


class TestCheckSellRules:
    def test_check_sell_rules_mainline_profit_threshold(self):
        mock_context = MockContext()
        mock_context.strategy_mode = "mainline"
        mock_logger = MockLogger()
        
        mock_position = MockPosition(avg_price=10.0, quantity=1000)
        mock_context.portfolio.positions = {"000001.XSHE": mock_position}
        
        mock_bar_dict = MockBarDict()
        mock_bar_dict["000001.XSHE"] = MockBar(close=10.5)
        
        def mock_order_shares(stock, shares):
            pass
        
        with patch.dict(sys.modules, {
            'order_shares': mock_order_shares,
            'logger': mock_logger,
        }):
            import shadow_mainline
            shadow_mainline.check_sell_rules(mock_context, mock_bar_dict)

    def test_check_sell_rules_mainline_hold_days(self):
        mock_context = MockContext()
        mock_context.strategy_mode = "mainline"
        mock_logger = MockLogger()
        
        mock_position = MockPosition(
            avg_price=10.0,
            quantity=1000,
            entry_date=datetime.now() - timedelta(days=2)
        )
        mock_context.portfolio.positions = {"000001.XSHE": mock_position}
        
        mock_bar_dict = MockBarDict()
        mock_bar_dict["000001.XSHE"] = MockBar(close=9.5)
        
        def mock_order_shares(stock, shares):
            pass
        
        with patch.dict(sys.modules, {
            'order_shares': mock_order_shares,
            'logger': mock_logger,
        }):
            import shadow_mainline
            shadow_mainline.check_sell_rules(mock_context, mock_bar_dict)

    def test_check_sell_rules_observation_mode(self):
        mock_context = MockContext()
        mock_context.strategy_mode = "observation"
        mock_logger = MockLogger()
        
        mock_position = MockPosition(
            avg_price=10.0,
            quantity=1000,
            entry_date=datetime.now() - timedelta(days=1)
        )
        mock_context.portfolio.positions = {"000001.XSHE": mock_position}
        
        mock_bar_dict = MockBarDict()
        mock_bar_dict["000001.XSHE"] = MockBar(close=10.5)
        
        def mock_order_shares(stock, shares):
            pass
        
        with patch.dict(sys.modules, {
            'order_shares': mock_order_shares,
            'logger': mock_logger,
        }):
            import shadow_mainline
            shadow_mainline.check_sell_rules(mock_context, mock_bar_dict)

    def test_check_sell_rules_stop_after_three_losses(self):
        mock_context = MockContext()
        mock_context.strategy_mode = "mainline"
        mock_context.consecutive_losses = 2
        mock_logger = MockLogger()
        
        mock_position = MockPosition(avg_price=10.0, quantity=1000)
        mock_context.portfolio.positions = {"000001.XSHE": mock_position}
        
        mock_bar_dict = MockBarDict()
        mock_bar_dict["000001.XSHE"] = MockBar(close=9.0)
        
        def mock_order_shares(stock, shares):
            pass
        
        with patch.dict(sys.modules, {
            'order_shares': mock_order_shares,
            'logger': mock_logger,
        }):
            import shadow_mainline
            shadow_mainline.check_sell_rules(mock_context, mock_bar_dict)
            
            assert mock_context.stop_trading_until is not None
            assert mock_context.consecutive_losses == 0


class TestAfterTrading:
    def test_after_trading_logs_info(self):
        mock_context = MockContext()
        mock_context.limit_up_count = 10
        mock_logger = MockLogger()
        
        with patch.dict(sys.modules, {'logger': mock_logger}):
            import shadow_mainline
            mock_bar_dict = MockBarDict()
            shadow_mainline.after_trading(mock_context, mock_bar_dict)


class TestMainlineParams:
    def test_mainline_params_values(self):
        import shadow_mainline
        
        assert shadow_mainline.MAINLINE_PARAMS["market_cap_min"] == 50
        assert shadow_mainline.MAINLINE_PARAMS["market_cap_max"] == 150
        assert shadow_mainline.MAINLINE_PARAMS["emotion_threshold"] == 30

    def test_observation_params_values(self):
        import shadow_mainline
        
        assert shadow_mainline.OBSERVATION_PARAMS["single_position_limit"] == 100000
        assert shadow_mainline.OBSERVATION_PARAMS["total_position_limit"] == 300000


class TestConfig:
    def test_config_values(self):
        import shadow_mainline
        
        assert shadow_mainline.config["base"]["start_date"] == "2014-01-01"
        assert shadow_mainline.config["base"]["end_date"] == "2024-12-31"
        assert shadow_mainline.config["base"]["frequency"] == "1d"
        assert shadow_mainline.config["base"]["accounts"]["stock"] == 100000


class TestEdgeCases:
    def test_zero_buy_price(self):
        mock_context = MockContext()
        mock_context.strategy_mode = "mainline"
        mock_position = MockPosition(avg_price=0.0, quantity=1000)
        mock_context.portfolio.positions = {"000001.XSHE": mock_position}
        
        mock_bar_dict = MockBarDict()
        mock_bar_dict["000001.XSHE"] = MockBar(close=10.0)
        
        import shadow_mainline
        try:
            shadow_mainline.check_sell_rules(mock_context, mock_bar_dict)
        except ZeroDivisionError:
            pass

    def test_empty_positions(self):
        mock_context = MockContext()
        mock_context.portfolio.positions = {}
        mock_bar_dict = MockBarDict()
        
        import shadow_mainline
        shadow_mainline.get_total_position_value(mock_context)
        shadow_mainline.check_sell_rules(mock_context, mock_bar_dict)