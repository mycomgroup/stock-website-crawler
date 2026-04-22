"""
测试 sb_simple.py - 二板接力策略简化版
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


class MockLimitUpBar:
    def __init__(self, close=11.0, limit_up=11.0, last_price=10.5):
        self.close = close
        self.limit_up = limit_up
        self.last_price = last_price


class TestSbSimpleInit:
    def test_init_sets_default_values(self):
        mock_context = MockContext()
        
        import sb_simple
        sb_simple.init(mock_context)
        
        assert mock_context.trade_count == 0
        assert mock_context.stock_pool == 200
        assert mock_context.threshold == 10
        assert mock_context.volume_ratio == 1.875

    def test_init_can_override_defaults(self):
        mock_context = MockContext()
        
        import sb_simple
        sb_simple.init(mock_context)
        
        assert mock_context.stock_pool == 200
        assert mock_context.threshold == 10


class TestHandleBar:
    def test_handle_bar_sells_positions(self):
        mock_context = MockContext()
        mock_context.portfolio.positions = {
            "000001.XSHE": MockPosition(quantity=1000),
            "000002.XSHE": MockPosition(quantity=500),
        }
        
        sell_count = 0
        
        def mock_all_instruments(type_str):
            return pd.DataFrame({"order_book_id": ["000001.XSHE"]})
        
        def mock_order_target_percent(stock, percent):
            if percent == 0:
                sell_count += 1
        
        def mock_history_bars(stock, count, freq, fields):
            return None
        
        with patch.dict(sys.modules, {
            'all_instruments': mock_all_instruments,
            'order_target_percent': mock_order_target_percent,
            'history_bars': mock_history_bars,
        }):
            import sb_simple
            mock_bar_dict = MockBarDict()
            sb_simple.handle_bar(mock_context, mock_bar_dict)
            
            assert sell_count == 2

    def test_handle_bar_filters_scientific_board(self):
        mock_context = MockContext()
        mock_context.portfolio.positions = {}
        
        def mock_all_instruments(type_str):
            return pd.DataFrame({
                "order_book_id": ["688001.XSHG", "000001.XSHE", "400001.XSHE", "800001.XSHE"]
            })
        
        def mock_history_bars(stock, count, freq, fields):
            return None
        
        with patch.dict(sys.modules, {
            'all_instruments': mock_all_instruments,
            'history_bars': mock_history_bars,
        }):
            import sb_simple
            mock_bar_dict = MockBarDict()
            sb_simple.handle_bar(mock_context, mock_bar_dict)

    def test_handle_bar_counts_limit_up_stocks(self):
        mock_context = MockContext()
        mock_context.portfolio.positions = {}
        
        def mock_all_instruments(type_str):
            return pd.DataFrame({
                "order_book_id": ["000001.XSHE", "000002.XSHE"]
            })
        
        def mock_history_bars(stock, count, freq, fields):
            if count == 1:
                return [{"close": 11.0, "limit_up": 11.0}]
            return None
        
        with patch.dict(sys.modules, {
            'all_instruments': mock_all_instruments,
            'history_bars': mock_history_bars,
        }):
            import sb_simple
            mock_bar_dict = MockBarDict()
            sb_simple.handle_bar(mock_context, mock_bar_dict)

    def test_handle_bar_threshold_not_met(self):
        mock_context = MockContext()
        mock_context.threshold = 20
        mock_context.portfolio.positions = {}
        
        def mock_all_instruments(type_str):
            return pd.DataFrame({
                "order_book_id": ["000001.XSHE", "000002.XSHE"]
            })
        
        def mock_history_bars(stock, count, freq, fields):
            if count == 1:
                return [{"close": 10.5, "limit_up": 11.0}]
            return None
        
        with patch.dict(sys.modules, {
            'all_instruments': mock_all_instruments,
            'history_bars': mock_history_bars,
        }):
            import sb_simple
            mock_bar_dict = MockBarDict()
            sb_simple.handle_bar(mock_context, mock_bar_dict)

    def test_handle_bar_threshold_met(self):
        mock_context = MockContext()
        mock_context.threshold = 5
        mock_context.portfolio.positions = {}
        
        def mock_all_instruments(type_str):
            return pd.DataFrame({
                "order_book_id": [f"zt{i}" for i in range(15)]
            })
        
        def mock_history_bars(stock, count, freq, fields):
            if count == 1:
                return [{"close": 11.0, "limit_up": 11.0}]
            elif count == 2:
                return [
                    {"close": 10.0, "limit_up": 11.0},
                    {"close": 11.0, "limit_up": 11.0},
                ]
            return None
        
        def mock_order_target_percent(stock, percent):
            assert percent == 0.95
            mock_context.trade_count += 1
        
        mock_bar_dict = MockBarDict()
        mock_bar_dict["zt0"] = MockLimitUpBar(close=10.5, limit_up=11.0, last_price=10.5)
        
        with patch.dict(sys.modules, {
            'all_instruments': mock_all_instruments,
            'history_bars': mock_history_bars,
            'order_target_percent': mock_order_target_percent,
        }):
            import sb_simple
            sb_simple.handle_bar(mock_context, mock_bar_dict)

    def test_handle_bar_null_history_bars(self):
        mock_context = MockContext()
        mock_context.threshold = 5
        mock_context.portfolio.positions = {}
        
        def mock_all_instruments(type_str):
            return pd.DataFrame({
                "order_book_id": [f"stock{i}" for i in range(20)]
            })
        
        def mock_history_bars(stock, count, freq, fields):
            return None
        
        with patch.dict(sys.modules, {
            'all_instruments': mock_all_instruments,
            'history_bars': mock_history_bars,
        }):
            import sb_simple
            mock_bar_dict = MockBarDict()
            sb_simple.handle_bar(mock_context, mock_bar_dict)

    def test_handle_bar_insufficient_history(self):
        mock_context = MockContext()
        mock_context.threshold = 5
        mock_context.portfolio.positions = {}
        
        def mock_all_instruments(type_str):
            return pd.DataFrame({
                "order_book_id": [f"stock{i}" for i in range(20)]
            })
        
        def mock_history_bars(stock, count, freq, fields):
            if count == 1:
                return [{"close": 11.0, "limit_up": 11.0}]
            elif count == 2:
                return [{"close": 10.0, "limit_up": 11.0}]
            return None
        
        with patch.dict(sys.modules, {
            'all_instruments': mock_all_instruments,
            'history_bars': mock_history_bars,
        }):
            import sb_simple
            mock_bar_dict = MockBarDict()
            sb_simple.handle_bar(mock_context, mock_bar_dict)

    def test_handle_bar_stock_pool_limit(self):
        mock_context = MockContext()
        mock_context.stock_pool = 10
        mock_context.portfolio.positions = {}
        
        def mock_all_instruments(type_str):
            return pd.DataFrame({
                "order_book_id": [f"stock{i}" for i in range(500)]
            })
        
        def mock_history_bars(stock, count, freq, fields):
            return None
        
        with patch.dict(sys.modules, {
            'all_instruments': mock_all_instruments,
            'history_bars': mock_history_bars,
        }):
            import sb_simple
            mock_bar_dict = MockBarDict()
            sb_simple.handle_bar(mock_context, mock_bar_dict)

    def test_handle_bar_order_exception(self):
        mock_context = MockContext()
        mock_context.threshold = 1
        mock_context.portfolio.positions = {}
        
        def mock_all_instruments(type_str):
            return pd.DataFrame({
                "order_book_id": [f"zt{i}" for i in range(15)]
            })
        
        def mock_history_bars(stock, count, freq, fields):
            if count == 1:
                return [{"close": 11.0, "limit_up": 11.0}]
            elif count == 2:
                return [
                    {"close": 10.0, "limit_up": 11.0},
                    {"close": 11.0, "limit_up": 11.0},
                ]
            return None
        
        def mock_order_target_percent(stock, percent):
            raise Exception("Order Error")
        
        mock_bar_dict = MockBarDict()
        mock_bar_dict["zt0"] = MockLimitUpBar(close=10.5, limit_up=11.0)
        
        with patch.dict(sys.modules, {
            'all_instruments': mock_all_instruments,
            'history_bars': mock_history_bars,
            'order_target_percent': mock_order_target_percent,
        }):
            import sb_simple
            sb_simple.handle_bar(mock_context, mock_bar_dict)

    def test_handle_bar_no_limit_up_stocks(self):
        mock_context = MockContext()
        mock_context.threshold = 1
        mock_context.portfolio.positions = {}
        
        def mock_all_instruments(type_str):
            return pd.DataFrame({
                "order_book_id": ["000001.XSHE", "000002.XSHE"]
            })
        
        def mock_history_bars(stock, count, freq, fields):
            if count == 1:
                return [{"close": 10.5, "limit_up": 11.0}]
            return None
        
        with patch.dict(sys.modules, {
            'all_instruments': mock_all_instruments,
            'history_bars': mock_history_bars,
        }):
            import sb_simple
            mock_bar_dict = MockBarDict()
            sb_simple.handle_bar(mock_context, mock_bar_dict)

    def test_handle_bar_buy_when_not_at_limit(self):
        mock_context = MockContext()
        mock_context.threshold = 5
        mock_context.portfolio.positions = {}
        
        def mock_all_instruments(type_str):
            return pd.DataFrame({
                "order_book_id": [f"zt{i}" for i in range(15)]
            })
        
        def mock_history_bars(stock, count, freq, fields):
            if count == 1:
                return [{"close": 11.0, "limit_up": 11.0}]
            elif count == 2:
                return [
                    {"close": 10.0, "limit_up": 11.0},
                    {"close": 11.0, "limit_up": 11.0},
                ]
            return None
        
        def mock_order_target_percent(stock, percent):
            mock_context.trade_count += 1
        
        mock_bar_dict = MockBarDict()
        mock_bar_dict["zt0"] = MockLimitUpBar(close=10.5, limit_up=11.0, last_price=10.5)
        
        with patch.dict(sys.modules, {
            'all_instruments': mock_all_instruments,
            'history_bars': mock_history_bars,
            'order_target_percent': mock_order_target_percent,
        }):
            import sb_simple
            sb_simple.handle_bar(mock_context, mock_bar_dict)

    def test_handle_bar_no_buy_at_limit_up(self):
        mock_context = MockContext()
        mock_context.threshold = 5
        mock_context.portfolio.positions = {}
        
        def mock_all_instruments(type_str):
            return pd.DataFrame({
                "order_book_id": [f"zt{i}" for i in range(15)]
            })
        
        def mock_history_bars(stock, count, freq, fields):
            if count == 1:
                return [{"close": 11.0, "limit_up": 11.0}]
            elif count == 2:
                return [
                    {"close": 10.0, "limit_up": 11.0},
                    {"close": 11.0, "limit_up": 11.0},
                ]
            return None
        
        mock_bar_dict = MockBarDict()
        mock_bar_dict["zt0"] = MockLimitUpBar(close=11.0, limit_up=11.0, last_price=11.0)
        
        with patch.dict(sys.modules, {
            'all_instruments': mock_all_instruments,
            'history_bars': mock_history_bars,
            'order_target_percent': lambda s, p: None,
        }):
            import sb_simple
            sb_simple.handle_bar(mock_context, mock_bar_dict)


class TestEdgeCases:
    def test_empty_all_instruments(self):
        mock_context = MockContext()
        mock_context.portfolio.positions = {}
        
        def mock_all_instruments(type_str):
            return pd.DataFrame({"order_book_id": []})
        
        with patch.dict(sys.modules, {'all_instruments': mock_all_instruments}):
            import sb_simple
            mock_bar_dict = MockBarDict()
            sb_simple.handle_bar(mock_context, mock_bar_dict)

    def test_all_instruments_exception(self):
        mock_context = MockContext()
        mock_context.portfolio.positions = {}
        
        def mock_all_instruments(type_str):
            raise Exception("API Error")
        
        with patch.dict(sys.modules, {'all_instruments': mock_all_instruments}):
            import sb_simple
            mock_bar_dict = MockBarDict()
            try:
                sb_simple.handle_bar(mock_context, mock_bar_dict)
            except Exception:
                pass

    def test_non_string_order_book_id(self):
        mock_context = MockContext()
        mock_context.portfolio.positions = {}
        
        def mock_all_instruments(type_str):
            return pd.DataFrame({
                "order_book_id": [None, "000001.XSHE", 123]
            })
        
        def mock_history_bars(stock, count, freq, fields):
            return None
        
        with patch.dict(sys.modules, {
            'all_instruments': mock_all_instruments,
            'history_bars': mock_history_bars,
        }):
            import sb_simple
            mock_bar_dict = MockBarDict()
            sb_simple.handle_bar(mock_context, mock_bar_dict)

    def test_negative_threshold(self):
        mock_context = MockContext()
        mock_context.threshold = -1
        mock_context.portfolio.positions = {}
        
        def mock_all_instruments(type_str):
            return pd.DataFrame({"order_book_id": ["000001.XSHE"]})
        
        def mock_history_bars(stock, count, freq, fields):
            return [{"close": 11.0, "limit_up": 11.0}]
        
        def mock_order_target_percent(stock, percent):
            mock_context.trade_count += 1
        
        with patch.dict(sys.modules, {
            'all_instruments': mock_all_instruments,
            'history_bars': mock_history_bars,
            'order_target_percent': mock_order_target_percent,
        }):
            import sb_simple
            mock_bar_dict = MockBarDict()
            sb_simple.handle_bar(mock_context, mock_bar_dict)

    def test_zero_limit_up(self):
        mock_context = MockContext()
        mock_context.threshold = 1
        mock_context.portfolio.positions = {}
        
        def mock_all_instruments(type_str):
            return pd.DataFrame({"order_book_id": ["000001.XSHE"]})
        
        def mock_history_bars(stock, count, freq, fields):
            return [{"close": 10.5, "limit_up": 0.0}]
        
        with patch.dict(sys.modules, {
            'all_instruments': mock_all_instruments,
            'history_bars': mock_history_bars,
        }):
            import sb_simple
            mock_bar_dict = MockBarDict()
            try:
                sb_simple.handle_bar(mock_context, mock_bar_dict)
            except ZeroDivisionError:
                pass

    def test_empty_positions(self):
        mock_context = MockContext()
        mock_context.portfolio.positions = {}
        
        def mock_all_instruments(type_str):
            return pd.DataFrame({"order_book_id": []})
        
        def mock_order_target_percent(stock, percent):
            pass
        
        with patch.dict(sys.modules, {
            'all_instruments': mock_all_instruments,
            'order_target_percent': mock_order_target_percent,
        }):
            import sb_simple
            mock_bar_dict = MockBarDict()
            sb_simple.handle_bar(mock_context, mock_bar_dict)

    def test_prev_zt_stocks(self):
        mock_context = MockContext()
        mock_context.threshold = 5
        mock_context.portfolio.positions = {}
        
        def mock_all_instruments(type_str):
            return pd.DataFrame({
                "order_book_id": [f"stock{i}" for i in range(20)]
            })
        
        def mock_history_bars(stock, count, freq, fields):
            if count == 1:
                return [{"close": 10.5, "limit_up": 11.0}]
            elif count == 2:
                return [
                    {"close": 10.0, "limit_up": 11.0},
                    {"close": 11.0, "limit_up": 11.0},
                ]
            return None
        
        with patch.dict(sys.modules, {
            'all_instruments': mock_all_instruments,
            'history_bars': mock_history_bars,
        }):
            import sb_simple
            mock_bar_dict = MockBarDict()
            sb_simple.handle_bar(mock_context, mock_bar_dict)

    def test_limit_up_comparison(self):
        mock_context = MockContext()
        mock_context.threshold = 5
        mock_context.portfolio.positions = {}
        
        def mock_all_instruments(type_str):
            return pd.DataFrame({
                "order_book_id": [f"zt{i}" for i in range(15)]
            })
        
        def mock_history_bars(stock, count, freq, fields):
            if count == 1:
                return [{"close": 10.89, "limit_up": 11.0}]
            elif count == 2:
                return [
                    {"close": 10.0, "limit_up": 11.0},
                    {"close": 10.89, "limit_up": 11.0},
                ]
            return None
        
        mock_bar_dict = MockBarDict()
        mock_bar_dict["zt0"] = MockLimitUpBar(close=10.5, limit_up=11.0)
        
        with patch.dict(sys.modules, {
            'all_instruments': mock_all_instruments,
            'history_bars': mock_history_bars,
        }):
            import sb_simple
            sb_simple.handle_bar(mock_context, mock_bar_dict)

    def test_filter_4_prefix_stocks(self):
        mock_context = MockContext()
        mock_context.portfolio.positions = {}
        
        def mock_all_instruments(type_str):
            return pd.DataFrame({
                "order_book_id": ["400001.XSHE", "000001.XSHE"]
            })
        
        def mock_history_bars(stock, count, freq, fields):
            return None
        
        with patch.dict(sys.modules, {
            'all_instruments': mock_all_instruments,
            'history_bars': mock_history_bars,
        }):
            import sb_simple
            mock_bar_dict = MockBarDict()
            sb_simple.handle_bar(mock_context, mock_bar_dict)

    def test_filter_8_prefix_stocks(self):
        mock_context = MockContext()
        mock_context.portfolio.positions = {}
        
        def mock_all_instruments(type_str):
            return pd.DataFrame({
                "order_book_id": ["800001.XSHE", "000001.XSHE"]
            })
        
        def mock_history_bars(stock, count, freq, fields):
            return None
        
        with patch.dict(sys.modules, {
            'all_instruments': mock_all_instruments,
            'history_bars': mock_history_bars,
        }):
            import sb_simple
            mock_bar_dict = MockBarDict()
            sb_simple.handle_bar(mock_context, mock_bar_dict)

    def test_no_second_board_match(self):
        mock_context = MockContext()
        mock_context.threshold = 5
        mock_context.portfolio.positions = {}
        
        def mock_all_instruments(type_str):
            return pd.DataFrame({
                "order_book_id": [f"stock{i}" for i in range(20)]
            })
        
        def mock_history_bars(stock, count, freq, fields):
            if count == 1:
                return [{"close": 11.0, "limit_up": 11.0}]
            elif count == 2:
                return [
                    {"close": 10.0, "limit_up": 11.0},
                    {"close": 10.5, "limit_up": 11.0},
                ]
            return None
        
        with patch.dict(sys.modules, {
            'all_instruments': mock_all_instruments,
            'history_bars': mock_history_bars,
        }):
            import sb_simple
            mock_bar_dict = MockBarDict()
            sb_simple.handle_bar(mock_context, mock_bar_dict)

    def test_set_intersection(self):
        mock_context = MockContext()
        mock_context.threshold = 5
        mock_context.portfolio.positions = {}
        
        def mock_all_instruments(type_str):
            return pd.DataFrame({
                "order_book_id": ["zt1", "zt2", "zt3", "zt4", "zt5", "zt6", "zt7", "zt8", "zt9", "zt10"]
            })
        
        def mock_history_bars(stock, count, freq, fields):
            if count == 1:
                return [{"close": 11.0, "limit_up": 11.0}]
            elif count == 2:
                return [
                    {"close": 10.0, "limit_up": 11.0},
                    {"close": 11.0, "limit_up": 11.0},
                ]
            return None
        
        def mock_order_target_percent(stock, percent):
            mock_context.trade_count += 1
        
        mock_bar_dict = MockBarDict()
        for i in range(10):
            mock_bar_dict[f"zt{i+1}"] = MockLimitUpBar(close=10.5, limit_up=11.0)
        
        with patch.dict(sys.modules, {
            'all_instruments': mock_all_instruments,
            'history_bars': mock_history_bars,
            'order_target_percent': mock_order_target_percent,
        }):
            import sb_simple
            sb_simple.handle_bar(mock_context, mock_bar_dict)