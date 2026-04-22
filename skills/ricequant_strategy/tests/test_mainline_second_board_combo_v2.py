"""
测试 mainline_second_board_combo_v2.py - 主线二板组合测试版
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


class TestMainlineSecondBoardComboInit:
    def test_init_sets_default_values(self):
        mock_context = MockContext()
        mock_scheduler = MockScheduler()
        
        with patch.dict(sys.modules, {
            'scheduler': mock_scheduler,
            'market_open': lambda minute: f"market_open_{minute}",
        }):
            import mainline_second_board_combo_v2
            mainline_second_board_combo_v2.init(mock_context)
            
            assert mock_context.mainline_weight == 0.5
            assert mock_context.second_board_weight == 0.5
            assert mock_context.scheme == "C"
            assert mock_context.mainline_trades == []
            assert mock_context.second_board_trades == []
            assert mock_context.combo_trades == []
            assert mock_context.portfolio_value == 1.0
            assert mock_context.daily_signals == {}

    def test_init_schedules_rebalance(self):
        mock_context = MockContext()
        mock_scheduler = MockScheduler()
        
        with patch.dict(sys.modules, {'scheduler': mock_scheduler}):
            import mainline_second_board_combo_v2
            mainline_second_board_combo_v2.init(mock_context)
            
            assert len(mock_scheduler.scheduled_functions) == 1


class TestGetMainlineSignals:
    def test_get_mainline_signals_returns_signals(self):
        mock_context = MockContext()
        mock_context.now = datetime.now()
        
        def mock_all_instruments(type_str):
            return [MockInstrument("000001.XSHE", "平安银行")]
        
        def mock_history_bars(stock, count, freq, fields):
            bars = [
                {"close": 11.0, "high_limit": 11.0},
                {"close": 11.1, "high_limit": 12.0},
            ]
            return bars
        
        mock_bar_dict = MockBarDict()
        mock_bar_dict["000001.XSHE"] = MockBar(open_price=11.05, close=11.1, high=11.15)
        
        with patch.dict(sys.modules, {
            'all_instruments': mock_all_instruments,
            'history_bars': mock_history_bars,
        }):
            import mainline_second_board_combo_v2
            result = mainline_second_board_combo_v2.get_mainline_signals(mock_context, mock_bar_dict)
            
            assert isinstance(result, list)

    def test_get_mainline_signals_empty_result(self):
        mock_context = MockContext()
        
        def mock_all_instruments(type_str):
            return []
        
        with patch.dict(sys.modules, {'all_instruments': mock_all_instruments}):
            import mainline_second_board_combo_v2
            mock_bar_dict = MockBarDict()
            result = mainline_second_board_combo_v2.get_mainline_signals(mock_context, mock_bar_dict)
            
            assert result == []

    def test_get_mainline_signals_filters_non_limit_up(self):
        mock_context = MockContext()
        
        def mock_all_instruments(type_str):
            return [MockInstrument("000001.XSHE", "平安银行")]
        
        def mock_history_bars(stock, count, freq, fields):
            bars = [
                {"close": 10.0, "high_limit": 11.0},
                {"close": 10.5, "high_limit": 11.5},
            ]
            return bars
        
        with patch.dict(sys.modules, {
            'all_instruments': mock_all_instruments,
            'history_bars': mock_history_bars,
        }):
            import mainline_second_board_combo_v2
            mock_bar_dict = MockBarDict()
            mock_bar_dict["000001.XSHE"] = MockBar(open_price=10.1)
            result = mainline_second_board_combo_v2.get_mainline_signals(mock_context, mock_bar_dict)
            
            assert result == []

    def test_get_mainline_signals_open_pct_range(self):
        mock_context = MockContext()
        
        def mock_all_instruments(type_str):
            return [MockInstrument("000001.XSHE", "平安银行")]
        
        def mock_history_bars(stock, count, freq, fields):
            bars = [
                {"close": 11.0, "high_limit": 11.0},
                {"close": 11.1, "high_limit": 12.0},
            ]
            return bars
        
        mock_bar_dict = MockBarDict()
        mock_bar_dict["000001.XSHE"] = MockBar(open_price=11.055, close=11.1, high=11.15)
        
        with patch.dict(sys.modules, {
            'all_instruments': mock_all_instruments,
            'history_bars': mock_history_bars,
        }):
            import mainline_second_board_combo_v2
            result = mainline_second_board_combo_v2.get_mainline_signals(mock_context, mock_bar_dict)
            
            if len(result) > 0:
                assert 0.5 <= result[0]["open_pct"] <= 1.5

    def test_get_mainline_signals_handles_exception(self):
        mock_context = MockContext()
        
        def mock_all_instruments(type_str):
            raise Exception("API Error")
        
        with patch.dict(sys.modules, {'all_instruments': mock_all_instruments}):
            import mainline_second_board_combo_v2
            mock_bar_dict = MockBarDict()
            result = mainline_second_board_combo_v2.get_mainline_signals(mock_context, mock_bar_dict)
            
            assert result == []

    def test_get_mainline_signals_stock_not_in_bar_dict(self):
        mock_context = MockContext()
        
        def mock_all_instruments(type_str):
            return [MockInstrument("000001.XSHE", "平安银行")]
        
        def mock_history_bars(stock, count, freq, fields):
            bars = [
                {"close": 11.0, "high_limit": 11.0},
                {"close": 11.1, "high_limit": 12.0},
            ]
            return bars
        
        mock_bar_dict = {}
        
        with patch.dict(sys.modules, {
            'all_instruments': mock_all_instruments,
            'history_bars': mock_history_bars,
        }):
            import mainline_second_board_combo_v2
            result = mainline_second_board_combo_v2.get_mainline_signals(mock_context, mock_bar_dict)
            
            assert result == []

    def test_get_mainline_signals_null_history_bars(self):
        mock_context = MockContext()
        
        def mock_all_instruments(type_str):
            return [MockInstrument("000001.XSHE", "平安银行")]
        
        def mock_history_bars(stock, count, freq, fields):
            return None
        
        with patch.dict(sys.modules, {
            'all_instruments': mock_all_instruments,
            'history_bars': mock_history_bars,
        }):
            import mainline_second_board_combo_v2
            mock_bar_dict = MockBarDict()
            result = mainline_second_board_combo_v2.get_mainline_signals(mock_context, mock_bar_dict)
            
            assert result == []

    def test_get_mainline_signals_insufficient_history(self):
        mock_context = MockContext()
        
        def mock_all_instruments(type_str):
            return [MockInstrument("000001.XSHE", "平安银行")]
        
        def mock_history_bars(stock, count, freq, fields):
            return [{"close": 11.0, "high_limit": 11.0}]
        
        with patch.dict(sys.modules, {
            'all_instruments': mock_all_instruments,
            'history_bars': mock_history_bars,
        }):
            import mainline_second_board_combo_v2
            mock_bar_dict = MockBarDict()
            result = mainline_second_board_combo_v2.get_mainline_signals(mock_context, mock_bar_dict)
            
            assert result == []


class TestGetSecondBoardSignals:
    def test_get_second_board_signals_returns_signals(self):
        mock_context = MockContext()
        
        def mock_all_instruments(type_str):
            return [MockInstrument("000001.XSHE", "平安银行")]
        
        def mock_history_bars(stock, count, freq, fields):
            bars = [
                {"close": 10.0, "high_limit": 11.0, "low": 10.0, "high": 11.0},
                {"close": 11.0, "high_limit": 11.0, "low": 10.5, "high": 11.5},
                {"close": 12.0, "high_limit": 12.0, "low": 11.0, "high": 12.5},
            ]
            return bars
        
        mock_bar_dict = MockBarDict()
        mock_bar_dict["000001.XSHE"] = MockBar(
            open_price=11.5,
            limit_up=13.0,
            high=12.0,
            close=11.8
        )
        
        with patch.dict(sys.modules, {
            'all_instruments': mock_all_instruments,
            'history_bars': mock_history_bars,
        }):
            import mainline_second_board_combo_v2
            result = mainline_second_board_combo_v2.get_second_board_signals(mock_context, mock_bar_dict)
            
            assert isinstance(result, list)

    def test_get_second_board_signals_empty_result(self):
        mock_context = MockContext()
        
        def mock_all_instruments(type_str):
            return []
        
        with patch.dict(sys.modules, {'all_instruments': mock_all_instruments}):
            import mainline_second_board_combo_v2
            mock_bar_dict = MockBarDict()
            result = mainline_second_board_combo_v2.get_second_board_signals(mock_context, mock_bar_dict)
            
            assert result == []

    def test_get_second_board_signals_filters_one_word_board(self):
        mock_context = MockContext()
        
        def mock_all_instruments(type_str):
            return [MockInstrument("000001.XSHE", "平安银行")]
        
        def mock_history_bars(stock, count, freq, fields):
            bars = [
                {"close": 10.0, "high_limit": 11.0, "low": 11.0, "high": 11.0},
                {"close": 11.0, "high_limit": 11.0, "low": 11.0, "high": 11.0},
                {"close": 12.0, "high_limit": 12.0, "low": 12.0, "high": 12.0},
            ]
            return bars
        
        with patch.dict(sys.modules, {
            'all_instruments': mock_all_instruments,
            'history_bars': mock_history_bars,
        }):
            import mainline_second_board_combo_v2
            mock_bar_dict = MockBarDict()
            mock_bar_dict["000001.XSHE"] = MockBar(open_price=11.5, limit_up=13.0)
            result = mainline_second_board_combo_v2.get_second_board_signals(mock_context, mock_bar_dict)
            
            assert result == []

    def test_get_second_board_signals_handles_exception(self):
        mock_context = MockContext()
        
        def mock_all_instruments(type_str):
            raise Exception("API Error")
        
        with patch.dict(sys.modules, {'all_instruments': mock_all_instruments}):
            import mainline_second_board_combo_v2
            mock_bar_dict = MockBarDict()
            result = mainline_second_board_combo_v2.get_second_board_signals(mock_context, mock_bar_dict)
            
            assert result == []

    def test_get_second_board_signals_stock_not_in_bar_dict(self):
        mock_context = MockContext()
        
        def mock_all_instruments(type_str):
            return [MockInstrument("000001.XSHE", "平安银行")]
        
        def mock_history_bars(stock, count, freq, fields):
            bars = [
                {"close": 10.0, "high_limit": 11.0, "low": 10.0, "high": 11.0},
                {"close": 11.0, "high_limit": 11.0, "low": 10.5, "high": 11.5},
                {"close": 12.0, "high_limit": 12.0, "low": 11.0, "high": 12.5},
            ]
            return bars
        
        mock_bar_dict = {}
        
        with patch.dict(sys.modules, {
            'all_instruments': mock_all_instruments,
            'history_bars': mock_history_bars,
        }):
            import mainline_second_board_combo_v2
            result = mainline_second_board_combo_v2.get_second_board_signals(mock_context, mock_bar_dict)
            
            assert result == []

    def test_get_second_board_signals_null_history(self):
        mock_context = MockContext()
        
        def mock_all_instruments(type_str):
            return [MockInstrument("000001.XSHE", "平安银行")]
        
        def mock_history_bars(stock, count, freq, fields):
            return None
        
        with patch.dict(sys.modules, {
            'all_instruments': mock_all_instruments,
            'history_bars': mock_history_bars,
        }):
            import mainline_second_board_combo_v2
            mock_bar_dict = MockBarDict()
            result = mainline_second_board_combo_v2.get_second_board_signals(mock_context, mock_bar_dict)
            
            assert result == []

    def test_get_second_board_signals_insufficient_history(self):
        mock_context = MockContext()
        
        def mock_all_instruments(type_str):
            return [MockInstrument("000001.XSHE", "平安银行")]
        
        def mock_history_bars(stock, count, freq, fields):
            return [
                {"close": 10.0, "high_limit": 11.0, "low": 10.0, "high": 11.0},
                {"close": 11.0, "high_limit": 11.0, "low": 10.5, "high": 11.5},
            ]
        
        with patch.dict(sys.modules, {
            'all_instruments': mock_all_instruments,
            'history_bars': mock_history_bars,
        }):
            import mainline_second_board_combo_v2
            mock_bar_dict = MockBarDict()
            result = mainline_second_board_combo_v2.get_second_board_signals(mock_context, mock_bar_dict)
            
            assert result == []


class TestExecuteComboStrategy:
    def test_execute_combo_scheme_a_mainline_priority(self):
        mock_context = MockContext()
        mock_context.scheme = "A"
        
        mainline_signals = [{"stock": "ml1", "return": 5.0}]
        second_board_signals = [{"stock": "sb1", "return": 3.0}]
        
        import mainline_second_board_combo_v2
        result = mainline_second_board_combo_v2.execute_combo_strategy(
            mock_context, MockBarDict(), mainline_signals, second_board_signals
        )
        
        assert result[0] == 5.0
        assert result[1] == "mainline"

    def test_execute_combo_scheme_a_mainline_empty(self):
        mock_context = MockContext()
        mock_context.scheme = "A"
        
        mainline_signals = []
        second_board_signals = [{"stock": "sb1", "return": 3.0}]
        
        import mainline_second_board_combo_v2
        result = mainline_second_board_combo_v2.execute_combo_strategy(
            mock_context, MockBarDict(), mainline_signals, second_board_signals
        )
        
        assert result[0] == 3.0
        assert result[1] == "second_board"

    def test_execute_combo_scheme_b_second_board_priority(self):
        mock_context = MockContext()
        mock_context.scheme = "B"
        
        mainline_signals = [{"stock": "ml1", "return": 5.0}]
        second_board_signals = [{"stock": "sb1", "return": 3.0}]
        
        import mainline_second_board_combo_v2
        result = mainline_second_board_combo_v2.execute_combo_strategy(
            mock_context, MockBarDict(), mainline_signals, second_board_signals
        )
        
        assert result[0] == 3.0
        assert result[1] == "second_board"

    def test_execute_combo_scheme_b_second_board_empty(self):
        mock_context = MockContext()
        mock_context.scheme = "B"
        
        mainline_signals = [{"stock": "ml1", "return": 5.0}]
        second_board_signals = []
        
        import mainline_second_board_combo_v2
        result = mainline_second_board_combo_v2.execute_combo_strategy(
            mock_context, MockBarDict(), mainline_signals, second_board_signals
        )
        
        assert result[0] == 5.0
        assert result[1] == "mainline"

    def test_execute_combo_scheme_c_parallel(self):
        mock_context = MockContext()
        mock_context.scheme = "C"
        mock_context.mainline_weight = 0.5
        mock_context.second_board_weight = 0.5
        
        mainline_signals = [{"stock": "ml1", "return": 5.0}, {"stock": "ml2", "return": 3.0}]
        second_board_signals = [{"stock": "sb1", "return": 4.0}]
        
        import mainline_second_board_combo_v2
        result = mainline_second_board_combo_v2.execute_combo_strategy(
            mock_context, MockBarDict(), mainline_signals, second_board_signals
        )
        
        assert result[1] == "both"

    def test_execute_combo_scheme_c_mainline_only(self):
        mock_context = MockContext()
        mock_context.scheme = "C"
        mock_context.mainline_weight = 0.5
        mock_context.second_board_weight = 0.5
        
        mainline_signals = [{"stock": "ml1", "return": 5.0}]
        second_board_signals = []
        
        import mainline_second_board_combo_v2
        result = mainline_second_board_combo_v2.execute_combo_strategy(
            mock_context, MockBarDict(), mainline_signals, second_board_signals
        )
        
        assert result[1] == "both"

    def test_execute_combo_scheme_d_profit_priority_mainline(self):
        mock_context = MockContext()
        mock_context.scheme = "D"
        
        mainline_signals = [{"stock": "ml1", "return": 10.0}]
        second_board_signals = [{"stock": "sb1", "return": 5.0}]
        
        import mainline_second_board_combo_v2
        result = mainline_second_board_combo_v2.execute_combo_strategy(
            mock_context, MockBarDict(), mainline_signals, second_board_signals
        )
        
        assert result[0] == 10.0
        assert result[1] == "mainline"

    def test_execute_combo_scheme_d_profit_priority_second_board(self):
        mock_context = MockContext()
        mock_context.scheme = "D"
        
        mainline_signals = [{"stock": "ml1", "return": 5.0}]
        second_board_signals = [{"stock": "sb1", "return": 10.0}]
        
        import mainline_second_board_combo_v2
        result = mainline_second_board_combo_v2.execute_combo_strategy(
            mock_context, MockBarDict(), mainline_signals, second_board_signals
        )
        
        assert result[0] == 10.0
        assert result[1] == "second_board"

    def test_execute_combo_scheme_d_mainline_only(self):
        mock_context = MockContext()
        mock_context.scheme = "D"
        
        mainline_signals = [{"stock": "ml1", "return": 5.0}]
        second_board_signals = []
        
        import mainline_second_board_combo_v2
        result = mainline_second_board_combo_v2.execute_combo_strategy(
            mock_context, MockBarDict(), mainline_signals, second_board_signals
        )
        
        assert result[0] == 5.0
        assert result[1] == "mainline"

    def test_execute_combo_scheme_d_second_board_only(self):
        mock_context = MockContext()
        mock_context.scheme = "D"
        
        mainline_signals = []
        second_board_signals = [{"stock": "sb1", "return": 5.0}]
        
        import mainline_second_board_combo_v2
        result = mainline_second_board_combo_v2.execute_combo_strategy(
            mock_context, MockBarDict(), mainline_signals, second_board_signals
        )
        
        assert result[0] == 5.0
        assert result[1] == "second_board"

    def test_execute_combo_no_signals(self):
        mock_context = MockContext()
        mock_context.scheme = "A"
        
        mainline_signals = []
        second_board_signals = []
        
        import mainline_second_board_combo_v2
        result = mainline_second_board_combo_v2.execute_combo_strategy(
            mock_context, MockBarDict(), mainline_signals, second_board_signals
        )
        
        assert result == (None, None)

    def test_execute_combo_scheme_c_empty_returns(self):
        mock_context = MockContext()
        mock_context.scheme = "C"
        
        mainline_signals = []
        second_board_signals = []
        
        import mainline_second_board_combo_v2
        result = mainline_second_board_combo_v2.execute_combo_strategy(
            mock_context, MockBarDict(), mainline_signals, second_board_signals
        )
        
        assert result == (None, None)


class TestRebalance:
    def test_rebalance_records_signals(self):
        mock_context = MockContext()
        mock_context.now = datetime.now()
        
        def mock_get_mainline_signals(context, bar_dict):
            return [{"stock": "ml1", "return": 5.0}]
        
        def mock_get_second_board_signals(context, bar_dict):
            return [{"stock": "sb1", "return": 3.0}]
        
        def mock_execute_combo_strategy(context, bar_dict, ml, sb):
            return (5.0, "mainline")
        
        import mainline_second_board_combo_v2
        mainline_second_board_combo_v2.get_mainline_signals = mock_get_mainline_signals
        mainline_second_board_combo_v2.get_second_board_signals = mock_get_second_board_signals
        mainline_second_board_combo_v2.execute_combo_strategy = mock_execute_combo_strategy
        
        mock_bar_dict = MockBarDict()
        mainline_second_board_combo_v2.rebalance(mock_context, mock_bar_dict)
        
        assert len(mock_context.daily_signals) > 0

    def test_rebalance_updates_portfolio_value(self):
        mock_context = MockContext()
        mock_context.now = datetime.now()
        mock_context.portfolio_value = 1.0
        
        def mock_get_mainline_signals(context, bar_dict):
            return [{"stock": "ml1", "return": 5.0}]
        
        def mock_get_second_board_signals(context, bar_dict):
            return []
        
        def mock_execute_combo_strategy(context, bar_dict, ml, sb):
            return (5.0, "mainline")
        
        import mainline_second_board_combo_v2
        mainline_second_board_combo_v2.get_mainline_signals = mock_get_mainline_signals
        mainline_second_board_combo_v2.get_second_board_signals = mock_get_second_board_signals
        mainline_second_board_combo_v2.execute_combo_strategy = mock_execute_combo_strategy
        
        mock_bar_dict = MockBarDict()
        mainline_second_board_combo_v2.rebalance(mock_context, mock_bar_dict)
        
        assert mock_context.portfolio_value == 1.05

    def test_rebalance_no_trade_return(self):
        mock_context = MockContext()
        mock_context.now = datetime.now()
        
        def mock_get_mainline_signals(context, bar_dict):
            return []
        
        def mock_get_second_board_signals(context, bar_dict):
            return []
        
        def mock_execute_combo_strategy(context, bar_dict, ml, sb):
            return (None, None)
        
        import mainline_second_board_combo_v2
        mainline_second_board_combo_v2.get_mainline_signals = mock_get_mainline_signals
        mainline_second_board_combo_v2.get_second_board_signals = mock_get_second_board_signals
        mainline_second_board_combo_v2.execute_combo_strategy = mock_execute_combo_strategy
        
        mock_bar_dict = MockBarDict()
        mainline_second_board_combo_v2.rebalance(mock_context, mock_bar_dict)
        
        assert len(mock_context.combo_trades) == 0

    def test_rebalance_records_trades(self):
        mock_context = MockContext()
        mock_context.now = datetime.now()
        
        def mock_get_mainline_signals(context, bar_dict):
            return [{"stock": "ml1", "return": 5.0, "open_pct": 1.0}]
        
        def mock_get_second_board_signals(context, bar_dict):
            return []
        
        def mock_execute_combo_strategy(context, bar_dict, ml, sb):
            return (5.0, "mainline")
        
        import mainline_second_board_combo_v2
        mainline_second_board_combo_v2.get_mainline_signals = mock_get_mainline_signals
        mainline_second_board_combo_v2.get_second_board_signals = mock_get_second_board_signals
        mainline_second_board_combo_v2.execute_combo_strategy = mock_execute_combo_strategy
        
        mock_bar_dict = MockBarDict()
        mainline_second_board_combo_v2.rebalance(mock_context, mock_bar_dict)
        
        assert len(mock_context.mainline_trades) > 0
        assert len(mock_context.combo_trades) > 0


class TestAfterTrading:
    def test_after_trading_no_trades(self):
        mock_context = MockContext()
        mock_context.now = datetime.now()
        mock_context.combo_trades = []
        
        import mainline_second_board_combo_v2
        mainline_second_board_combo_v2.after_trading(mock_context)

    def test_after_trading_30_trades(self):
        mock_context = MockContext()
        mock_context.now = datetime.now()
        mock_context.combo_trades = [
            {"date": "2024-01-01", "return": 5.0, "source": "mainline"}
        ] * 30
        mock_context.portfolio_value = 1.5
        
        import mainline_second_board_combo_v2
        mainline_second_board_combo_v2.after_trading(mock_context)

    def test_after_trading_prints_statistics(self):
        mock_context = MockContext()
        mock_context.now = datetime.now()
        mock_context.combo_trades = [
            {"date": "2024-01-01", "return": 5.0, "source": "mainline"}
        ] * 60
        mock_context.portfolio_value = 1.5
        
        import mainline_second_board_combo_v2
        mainline_second_board_combo_v2.after_trading(mock_context)


class TestAfterBacktest:
    def test_after_backtest_empty_trades(self):
        mock_context = MockContext()
        mock_context.mainline_trades = []
        mock_context.second_board_trades = []
        mock_context.combo_trades = []
        mock_context.daily_signals = {}
        mock_context.scheme = "C"
        mock_context.portfolio_value = 1.0
        
        indicator = {
            "total_returns": 0,
            "annualized_returns": 0,
            "max_drawdown": 0,
            "sharpe": 0,
        }
        
        import mainline_second_board_combo_v2
        mainline_second_board_combo_v2.after_backtest(mock_context, indicator)

    def test_after_backtest_with_trades(self):
        mock_context = MockContext()
        mock_context.mainline_trades = [
            {"date": "2024-01-01", "stock": "ml1", "return": 5.0}
        ] * 10
        mock_context.second_board_trades = [
            {"date": "2024-01-01", "stock": "sb1", "return": 3.0}
        ] * 10
        mock_context.combo_trades = [
            {"date": "2024-01-01", "return": 5.0, "source": "mainline"}
        ] * 20
        mock_context.daily_signals = {"2024-01-01": {"mainline": 1, "second_board": 1}}
        mock_context.scheme = "C"
        mock_context.portfolio_value = 1.5
        
        indicator = {
            "total_returns": 50.0,
            "annualized_returns": 10.0,
            "max_drawdown": 5.0,
            "sharpe": 1.5,
        }
        
        import mainline_second_board_combo_v2
        mainline_second_board_combo_v2.after_backtest(mock_context, indicator)

    def test_after_backtest_calculates_win_rate(self):
        mock_context = MockContext()
        mock_context.mainline_trades = [
            {"date": "2024-01-01", "stock": "ml1", "return": 5.0},
            {"date": "2024-01-02", "stock": "ml2", "return": -2.0},
            {"date": "2024-01-03", "stock": "ml3", "return": 3.0},
        ]
        mock_context.second_board_trades = []
        mock_context.combo_trades = mock_context.mainline_trades
        mock_context.daily_signals = {}
        mock_context.scheme = "A"
        mock_context.portfolio_value = 1.06
        
        indicator = {}
        
        import mainline_second_board_combo_v2
        mainline_second_board_combo_v2.after_backtest(mock_context, indicator)

    def test_after_backtest_calculates_max_drawdown(self):
        mock_context = MockContext()
        mock_context.mainline_trades = []
        mock_context.second_board_trades = []
        mock_context.combo_trades = [
            {"date": "2024-01-01", "return": 10.0, "source": "mainline"},
            {"date": "2024-01-02", "return": -5.0, "source": "mainline"},
            {"date": "2024-01-03", "return": -3.0, "source": "mainline"},
            {"date": "2024-01-04", "return": 8.0, "source": "mainline"},
        ]
        mock_context.daily_signals = {}
        mock_context.scheme = "C"
        mock_context.portfolio_value = 1.09
        
        indicator = {}
        
        import mainline_second_board_combo_v2
        mainline_second_board_combo_v2.after_backtest(mock_context, indicator)

    def test_after_backtest_signal_distribution(self):
        mock_context = MockContext()
        mock_context.mainline_trades = []
        mock_context.second_board_trades = []
        mock_context.combo_trades = [
            {"date": "2024-01-01", "return": 5.0, "source": "mainline"},
            {"date": "2024-01-02", "return": 3.0, "source": "second_board"},
            {"date": "2024-01-03", "return": 4.0, "source": "both"},
        ] * 10
        mock_context.daily_signals = {}
        mock_context.scheme = "C"
        mock_context.portfolio_value = 1.5
        
        indicator = {}
        
        import mainline_second_board_combo_v2
        mainline_second_board_combo_v2.after_backtest(mock_context, indicator)


class TestEdgeCases:
    def test_zero_return(self):
        mock_context = MockContext()
        mock_context.scheme = "A"
        
        mainline_signals = [{"stock": "ml1", "return": 0.0}]
        second_board_signals = []
        
        import mainline_second_board_combo_v2
        result = mainline_second_board_combo_v2.execute_combo_strategy(
            mock_context, MockBarDict(), mainline_signals, second_board_signals
        )
        
        assert result[0] == 0.0

    def test_negative_return(self):
        mock_context = MockContext()
        mock_context.scheme = "A"
        
        mainline_signals = [{"stock": "ml1", "return": -5.0}]
        second_board_signals = [{"stock": "sb1", "return": -3.0}]
        
        import mainline_second_board_combo_v2
        result = mainline_second_board_combo_v2.execute_combo_strategy(
            mock_context, MockBarDict(), mainline_signals, second_board_signals
        )
        
        assert result[0] == -5.0

    def test_scheme_c_weighted_average(self):
        mock_context = MockContext()
        mock_context.scheme = "C"
        mock_context.mainline_weight = 0.6
        mock_context.second_board_weight = 0.4
        
        mainline_signals = [{"stock": "ml1", "return": 10.0}]
        second_board_signals = [{"stock": "sb1", "return": 5.0}]
        
        import mainline_second_board_combo_v2
        result = mainline_second_board_combo_v2.execute_combo_strategy(
            mock_context, MockBarDict(), mainline_signals, second_board_signals
        )
        
        expected = 10.0 * 0.6 + 5.0 * 0.4
        assert result[0] == expected

    def test_scheme_d_equal_returns(self):
        mock_context = MockContext()
        mock_context.scheme = "D"
        
        mainline_signals = [{"stock": "ml1", "return": 5.0}]
        second_board_signals = [{"stock": "sb1", "return": 5.0}]
        
        import mainline_second_board_combo_v2
        result = mainline_second_board_combo_v2.execute_combo_strategy(
            mock_context, MockBarDict(), mainline_signals, second_board_signals
        )
        
        assert result[0] == 5.0
        assert result[1] == "mainline"

    def test_multiple_signals_scheme_a(self):
        mock_context = MockContext()
        mock_context.scheme = "A"
        
        mainline_signals = [
            {"stock": "ml1", "return": 3.0},
            {"stock": "ml2", "return": 5.0},
            {"stock": "ml3", "return": 2.0},
        ]
        second_board_signals = []
        
        import mainline_second_board_combo_v2
        result = mainline_second_board_combo_v2.execute_combo_strategy(
            mock_context, MockBarDict(), mainline_signals, second_board_signals
        )
        
        assert result[0] == 5.0

    def test_unknown_scheme(self):
        mock_context = MockContext()
        mock_context.scheme = "X"
        
        mainline_signals = [{"stock": "ml1", "return": 5.0}]
        second_board_signals = [{"stock": "sb1", "return": 3.0}]
        
        import mainline_second_board_combo_v2
        result = mainline_second_board_combo_v2.execute_combo_strategy(
            mock_context, MockBarDict(), mainline_signals, second_board_signals
        )
        
        assert result == (None, None)

    def test_zero_high_limit(self):
        mock_context = MockContext()
        
        def mock_all_instruments(type_str):
            return [MockInstrument("000001.XSHE", "平安银行")]
        
        def mock_history_bars(stock, count, freq, fields):
            bars = [
                {"close": 11.0, "high_limit": 0.0},
                {"close": 11.1, "high_limit": 0.0},
            ]
            return bars
        
        with patch.dict(sys.modules, {
            'all_instruments': mock_all_instruments,
            'history_bars': mock_history_bars,
        }):
            import mainline_second_board_combo_v2
            mock_bar_dict = MockBarDict()
            result = mainline_second_board_combo_v2.get_mainline_signals(mock_context, mock_bar_dict)
            
            assert isinstance(result, list)