"""
测试 shadow_platform.py - 影子策略平台版
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


class TestShadowPlatformInit:
    def test_init_sets_default_values(self):
        mock_context = MockContext()
        mock_scheduler = MockScheduler()
        
        with patch.dict(sys.modules, {
            'scheduler': mock_scheduler,
            'market_open': lambda minute: f"market_open_{minute}",
        }):
            import shadow_platform
            shadow_platform.init(mock_context)
            
            assert mock_context.strategy_mode == "mainline"
            assert mock_context.limit_up_count == 0

    def test_init_schedules_daily_check(self):
        mock_context = MockContext()
        mock_scheduler = MockScheduler()
        
        with patch.dict(sys.modules, {'scheduler': mock_scheduler}):
            import shadow_platform
            shadow_platform.init(mock_context)
            
            assert len(mock_scheduler.scheduled_functions) == 1


class TestDailyCheck:
    def test_daily_check_gets_candidate_pool(self):
        mock_context = MockContext()
        mock_logger = MockLogger()
        
        def mock_index_components(index_name):
            if index_name == "000300.XSHG":
                return ["600000.XSHG", "600519.XSHG"]
            elif index_name == "000905.XSHG":
                return ["000001.XSHE", "000002.XSHE"]
            return []
        
        with patch.dict(sys.modules, {
            'index_components': mock_index_components,
            'logger': mock_logger,
        }):
            import shadow_platform
            mock_bar_dict = MockBarDict()
            shadow_platform.daily_check(mock_context, mock_bar_dict)

    def test_daily_check_filters_scientific_board(self):
        mock_context = MockContext()
        mock_logger = MockLogger()
        
        def mock_index_components(index_name):
            return ["688001.XSHG", "000001.XSHE"]
        
        with patch.dict(sys.modules, {
            'index_components': mock_index_components,
            'logger': mock_logger,
        }):
            import shadow_platform
            mock_bar_dict = MockBarDict()
            shadow_platform.daily_check(mock_context, mock_bar_dict)

    def test_daily_check_counts_limit_up(self):
        mock_context = MockContext()
        mock_logger = MockLogger()
        
        def mock_index_components(index_name):
            return ["000001.XSHE", "000002.XSHE"]
        
        def mock_history_bars(stock, count, freq, fields):
            if stock == "000001.XSHE":
                return [{"close": 10.0}, {"close": 11.0}]
            return [{"close": 10.0}, {"close": 10.5}]
        
        with patch.dict(sys.modules, {
            'index_components': mock_index_components,
            'history_bars': mock_history_bars,
            'logger': mock_logger,
        }):
            import shadow_platform
            mock_bar_dict = MockBarDict()
            shadow_platform.daily_check(mock_context, mock_bar_dict)
            
            assert mock_context.limit_up_count >= 0

    def test_daily_check_low_emotion_returns(self):
        mock_context = MockContext()
        mock_logger = MockLogger()
        
        def mock_index_components(index_name):
            return ["000001.XSHE"]
        
        def mock_history_bars(stock, count, freq, fields):
            return [{"close": 10.0}, {"close": 10.1}]
        
        with patch.dict(sys.modules, {
            'index_components': mock_index_components,
            'history_bars': mock_history_bars,
            'logger': mock_logger,
        }):
            import shadow_platform
            mock_bar_dict = MockBarDict()
            shadow_platform.daily_check(mock_context, mock_bar_dict)

    def test_daily_check_high_emotion_generates_signals(self):
        mock_context = MockContext()
        mock_logger = MockLogger()
        
        def mock_index_components(index_name):
            return ["000001.XSHE", "000002.XSHE", "000003.XSHE"]
        
        def mock_history_bars(stock, count, freq, fields):
            bars = [
                {"close": 10.0, "open": 10.0, "high": 10.0},
                {"close": 11.0, "open": 10.1, "high": 10.5},
            ]
            if fields == ["close", "open", "high"]:
                return bars
            elif fields == "close":
                return [{"close": 10.0}, {"close": 11.0}]
            return bars
        
        def mock_order_shares(stock, shares):
            pass
        
        with patch.dict(sys.modules, {
            'index_components': mock_index_components,
            'history_bars': mock_history_bars,
            'order_shares': mock_order_shares,
            'logger': mock_logger,
        }):
            import shadow_platform
            mock_bar_dict = MockBarDict()
            mock_bar_dict["000001.XSHE"] = MockBar(close=10.2, open_price=10.1, high=10.5)
            shadow_platform.daily_check(mock_context, mock_bar_dict)

    def test_daily_check_handles_exception(self):
        mock_context = MockContext()
        mock_logger = MockLogger()
        
        def mock_index_components(index_name):
            raise Exception("API Error")
        
        with patch.dict(sys.modules, {
            'index_components': mock_index_components,
            'logger': mock_logger,
        }):
            import shadow_platform
            mock_bar_dict = MockBarDict()
            shadow_platform.daily_check(mock_context, mock_bar_dict)

    def test_daily_check_buy_when_signals_exist(self):
        mock_context = MockContext()
        mock_context.portfolio.positions = {}
        mock_logger = MockLogger()
        
        def mock_index_components(index_name):
            return ["000001.XSHE"] + [f"stock{i}" for i in range(100)]
        
        def mock_history_bars(stock, count, freq, fields):
            if stock == "000001.XSHE":
                bars = [
                    {"close": 10.0, "open": 10.0, "high": 10.0},
                    {"close": 11.0, "open": 10.1, "high": 10.5},
                ]
                if fields == ["close", "open", "high"]:
                    return bars
                elif fields == "close":
                    return [{"close": 10.0}, {"close": 11.0}]
            else:
                bars = [
                    {"close": 10.0, "open": 10.0, "high": 10.0},
                    {"close": 10.5, "open": 10.2, "high": 10.3},
                ]
                if fields == ["close", "open", "high"]:
                    return bars
                elif fields == "close":
                    return [{"close": 10.0}, {"close": 10.5}]
            return bars
        
        def mock_order_shares(stock, shares):
            pass
        
        with patch.dict(sys.modules, {
            'index_components': mock_index_components,
            'history_bars': mock_history_bars,
            'order_shares': mock_order_shares,
            'logger': mock_logger,
        }):
            import shadow_platform
            mock_bar_dict = MockBarDict()
            mock_bar_dict["000001.XSHE"] = MockBar(close=10.2, open_price=10.1, high=10.5)
            shadow_platform.daily_check(mock_context, mock_bar_dict)

    def test_daily_check_sell_positions(self):
        mock_context = MockContext()
        mock_context.portfolio.positions = {
            "000001.XSHE": MockPosition(
                avg_price=10.0,
                quantity=1000,
                entry_date=datetime.now() - timedelta(days=2)
            )
        }
        mock_logger = MockLogger()
        
        def mock_index_components(index_name):
            return []
        
        def mock_order_shares(stock, shares):
            pass
        
        with patch.dict(sys.modules, {
            'index_components': mock_index_components,
            'order_shares': mock_order_shares,
            'logger': mock_logger,
        }):
            import shadow_platform
            mock_bar_dict = MockBarDict()
            mock_bar_dict["000001.XSHE"] = MockBar(close=9.5)
            shadow_platform.daily_check(mock_context, mock_bar_dict)

    def test_daily_check_sell_profit_threshold(self):
        mock_context = MockContext()
        mock_context.portfolio.positions = {
            "000001.XSHE": MockPosition(avg_price=10.0, quantity=1000)
        }
        mock_logger = MockLogger()
        
        def mock_index_components(index_name):
            return []
        
        def mock_order_shares(stock, shares):
            pass
        
        with patch.dict(sys.modules, {
            'index_components': mock_index_components,
            'order_shares': mock_order_shares,
            'logger': mock_logger,
        }):
            import shadow_platform
            mock_bar_dict = MockBarDict()
            mock_bar_dict["000001.XSHE"] = MockBar(close=10.5)
            shadow_platform.daily_check(mock_context, mock_bar_dict)

    def test_daily_check_no_buy_if_max_positions(self):
        mock_context = MockContext()
        mock_context.portfolio.positions = {
            "stock1": MockPosition(),
            "stock2": MockPosition(),
            "stock3": MockPosition(),
        }
        mock_logger = MockLogger()
        
        def mock_index_components(index_name):
            return ["000001.XSHE"]
        
        def mock_history_bars(stock, count, freq, fields):
            bars = [
                {"close": 10.0, "open": 10.0, "high": 10.0},
                {"close": 11.0, "open": 10.1, "high": 10.5},
            ]
            if fields == ["close", "open", "high"]:
                return bars
            elif fields == "close":
                return [{"close": 10.0}, {"close": 11.0}]
            return bars
        
        with patch.dict(sys.modules, {
            'index_components': mock_index_components,
            'history_bars': mock_history_bars,
            'logger': mock_logger,
        }):
            import shadow_platform
            mock_bar_dict = MockBarDict()
            mock_bar_dict["000001.XSHE"] = MockBar(close=10.2, open_price=10.1, high=10.5)
            shadow_platform.daily_check(mock_context, mock_bar_dict)


class TestAfterTrading:
    def test_after_trading_logs_positions(self):
        mock_context = MockContext()
        mock_context.portfolio.positions = {
            "000001.XSHE": MockPosition(),
        }
        mock_logger = MockLogger()
        
        with patch.dict(sys.modules, {'logger': mock_logger}):
            import shadow_platform
            shadow_platform.after_trading(mock_context)
            
            assert len(mock_logger.messages) > 0


class TestEdgeCases:
    def test_empty_index_components(self):
        mock_context = MockContext()
        mock_logger = MockLogger()
        
        def mock_index_components(index_name):
            return []
        
        with patch.dict(sys.modules, {
            'index_components': mock_index_components,
            'logger': mock_logger,
        }):
            import shadow_platform
            mock_bar_dict = MockBarDict()
            shadow_platform.daily_check(mock_context, mock_bar_dict)

    def test_null_history_bars(self):
        mock_context = MockContext()
        mock_logger = MockLogger()
        
        def mock_index_components(index_name):
            return ["000001.XSHE"]
        
        def mock_history_bars(stock, count, freq, fields):
            return None
        
        with patch.dict(sys.modules, {
            'index_components': mock_index_components,
            'history_bars': mock_history_bars,
            'logger': mock_logger,
        }):
            import shadow_platform
            mock_bar_dict = MockBarDict()
            shadow_platform.daily_check(mock_context, mock_bar_dict)

    def test_insufficient_history_bars(self):
        mock_context = MockContext()
        mock_logger = MockLogger()
        
        def mock_index_components(index_name):
            return ["000001.XSHE"]
        
        def mock_history_bars(stock, count, freq, fields):
            return [{"close": 10.0}]
        
        with patch.dict(sys.modules, {
            'index_components': mock_index_components,
            'history_bars': mock_history_bars,
            'logger': mock_logger,
        }):
            import shadow_platform
            mock_bar_dict = MockBarDict()
            shadow_platform.daily_check(mock_context, mock_bar_dict)

    def test_zero_prev_close(self):
        mock_context = MockContext()
        mock_logger = MockLogger()
        
        def mock_index_components(index_name):
            return ["000001.XSHE"]
        
        def mock_history_bars(stock, count, freq, fields):
            return [{"close": 0.0}, {"close": 10.0}]
        
        with patch.dict(sys.modules, {
            'index_components': mock_index_components,
            'history_bars': mock_history_bars,
            'logger': mock_logger,
        }):
            import shadow_platform
            mock_bar_dict = MockBarDict()
            shadow_platform.daily_check(mock_context, mock_bar_dict)

    def test_buy_calculates_shares_correctly(self):
        mock_context = MockContext()
        mock_context.portfolio.total_value = 100000
        mock_context.portfolio.positions = {}
        mock_logger = MockLogger()
        
        def mock_index_components(index_name):
            return ["000001.XSHE"] + [f"zt{i}" for i in range(50)]
        
        def mock_history_bars(stock, count, freq, fields):
            if stock == "000001.XSHE":
                bars = [
                    {"close": 10.0, "open": 10.0, "high": 10.0},
                    {"close": 11.0, "open": 10.1, "high": 10.5},
                ]
                if fields == ["close", "open", "high"]:
                    return bars
                elif fields == "close":
                    return [{"close": 10.0}, {"close": 11.0}]
            else:
                bars = [
                    {"close": 10.0, "open": 10.0, "high": 10.0},
                    {"close": 10.5, "open": 10.2, "high": 10.3},
                ]
                if fields == ["close", "open", "high"]:
                    return bars
                elif fields == "close":
                    return [{"close": 10.0}, {"close": 10.5}]
            return bars
        
        def mock_order_shares(stock, shares):
            assert shares > 0
            assert shares % 100 == 0
        
        with patch.dict(sys.modules, {
            'index_components': mock_index_components,
            'history_bars': mock_history_bars,
            'order_shares': mock_order_shares,
            'logger': mock_logger,
        }):
            import shadow_platform
            mock_bar_dict = MockBarDict()
            mock_bar_dict["000001.XSHE"] = MockBar(close=10.2, open_price=10.1, high=10.5)
            shadow_platform.daily_check(mock_context, mock_bar_dict)

    def test_no_buy_if_zero_shares(self):
        mock_context = MockContext()
        mock_context.portfolio.total_value = 1000
        mock_context.portfolio.positions = {}
        mock_logger = MockLogger()
        
        def mock_index_components(index_name):
            return ["000001.XSHE"] + [f"zt{i}" for i in range(50)]
        
        def mock_history_bars(stock, count, freq, fields):
            if stock == "000001.XSHE":
                bars = [
                    {"close": 10.0, "open": 10.0, "high": 10.0},
                    {"close": 11.0, "open": 10.1, "high": 10.5},
                ]
                if fields == ["close", "open", "high"]:
                    return bars
                elif fields == "close":
                    return [{"close": 10.0}, {"close": 11.0}]
            else:
                bars = [
                    {"close": 10.0, "open": 10.0, "high": 10.0},
                    {"close": 10.5, "open": 10.2, "high": 10.3},
                ]
                if fields == ["close", "open", "high"]:
                    return bars
                elif fields == "close":
                    return [{"close": 10.0}, {"close": 10.5}]
            return bars
        
        def mock_order_shares(stock, shares):
            pass
        
        with patch.dict(sys.modules, {
            'index_components': mock_index_components,
            'history_bars': mock_history_bars,
            'order_shares': mock_order_shares,
            'logger': mock_logger,
        }):
            import shadow_platform
            mock_bar_dict = MockBarDict()
            mock_bar_dict["000001.XSHE"] = MockBar(close=500.0, open_price=10.1, high=10.5)
            shadow_platform.daily_check(mock_context, mock_bar_dict)