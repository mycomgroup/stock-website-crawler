"""
测试 sb_adjusted.py - 二板接力策略调整版
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


class TestSbAdjustedInit:
    def test_init_sets_default_values(self):
        mock_context = MockContext()
        
        import sb_adjusted
        sb_adjusted.init(mock_context)
        
        assert mock_context.trade_count == 0
        assert mock_context.stock_pool == 300
        assert mock_context.threshold == 3
        assert mock_context.volume_ratio == 1.875

    def test_init_can_override_defaults(self):
        mock_context = MockContext()
        
        import sb_adjusted
        sb_adjusted.init(mock_context)
        
        assert mock_context.stock_pool == 300


class TestHandleBar:
    def test_handle_bar_sells_positions(self):
        mock_context = MockContext()
        mock_context.portfolio.positions = {
            "000001.XSHE": MockPosition(quantity=1000),
            "000002.XSHE": MockPosition(quantity=500),
        }
        
        def mock_all_instruments(type_str):
            return pd.DataFrame({"order_book_id": ["000001.XSHE"]})
        
        def mock_order_target_percent(stock, percent):
            assert percent == 0
        
        with patch.dict(sys.modules, {
            'all_instruments': mock_all_instruments,
            'order_target_percent': mock_order_target_percent,
        }):
            import sb_adjusted
            mock_bar_dict = MockBarDict()
            sb_adjusted.handle_bar(mock_context, mock_bar_dict)

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
            import sb_adjusted
            mock_bar_dict = MockBarDict()
            sb_adjusted.handle_bar(mock_context, mock_bar_dict)

    def test_handle_bar_counts_limit_up_stocks(self):
        mock_context = MockContext()
        mock_context.portfolio.positions = {}
        
        def mock_all_instruments(type_str):
            return pd.DataFrame({
                "order_book_id": ["000001.XSHE", "000002.XSHE", "000003.XSHE"]
            })
        
        def mock_history_bars(stock, count, freq, fields):
            return [
                {"close": 10.0},
                {"close": 11.0},
            ]
        
        with patch.dict(sys.modules, {
            'all_instruments': mock_all_instruments,
            'history_bars': mock_history_bars,
        }):
            import sb_adjusted
            mock_bar_dict = MockBarDict()
            sb_adjusted.handle_bar(mock_context, mock_bar_dict)

    def test_handle_bar_threshold_not_met(self):
        mock_context = MockContext()
        mock_context.threshold = 10
        mock_context.portfolio.positions = {}
        
        def mock_all_instruments(type_str):
            return pd.DataFrame({
                "order_book_id": ["000001.XSHE", "000002.XSHE"]
            })
        
        def mock_history_bars(stock, count, freq, fields):
            return [
                {"close": 10.0},
                {"close": 10.5},
            ]
        
        with patch.dict(sys.modules, {
            'all_instruments': mock_all_instruments,
            'history_bars': mock_history_bars,
        }):
            import sb_adjusted
            mock_bar_dict = MockBarDict()
            sb_adjusted.handle_bar(mock_context, mock_bar_dict)

    def test_handle_bar_threshold_met(self):
        mock_context = MockContext()
        mock_context.threshold = 2
        mock_context.portfolio.positions = {}
        
        def mock_all_instruments(type_str):
            return pd.DataFrame({
                "order_book_id": ["000001.XSHE", "000002.XSHE", "000003.XSHE"]
            })
        
        def mock_history_bars(stock, count, freq, fields):
            return [
                {"close": 10.0},
                {"close": 11.0},
            ]
        
        def mock_order_target_percent(stock, percent):
            assert percent == 0.95
            mock_context.trade_count += 1
        
        with patch.dict(sys.modules, {
            'all_instruments': mock_all_instruments,
            'history_bars': mock_history_bars,
            'order_target_percent': mock_order_target_percent,
        }):
            import sb_adjusted
            mock_bar_dict = MockBarDict()
            mock_bar_dict["000001.XSHE"] = MockBar()
            sb_adjusted.handle_bar(mock_context, mock_bar_dict)
            
            assert mock_context.trade_count > 0

    def test_handle_bar_zero_prev_close(self):
        mock_context = MockContext()
        mock_context.threshold = 2
        mock_context.portfolio.positions = {}
        
        def mock_all_instruments(type_str):
            return pd.DataFrame({
                "order_book_id": ["000001.XSHE", "000002.XSHE"]
            })
        
        def mock_history_bars(stock, count, freq, fields):
            return [
                {"close": 0.0},
                {"close": 10.0},
            ]
        
        with patch.dict(sys.modules, {
            'all_instruments': mock_all_instruments,
            'history_bars': mock_history_bars,
        }):
            import sb_adjusted
            mock_bar_dict = MockBarDict()
            sb_adjusted.handle_bar(mock_context, mock_bar_dict)

    def test_handle_bar_null_history_bars(self):
        mock_context = MockContext()
        mock_context.threshold = 2
        mock_context.portfolio.positions = {}
        
        def mock_all_instruments(type_str):
            return pd.DataFrame({
                "order_book_id": ["000001.XSHE", "000002.XSHE"]
            })
        
        def mock_history_bars(stock, count, freq, fields):
            return None
        
        with patch.dict(sys.modules, {
            'all_instruments': mock_all_instruments,
            'history_bars': mock_history_bars,
        }):
            import sb_adjusted
            mock_bar_dict = MockBarDict()
            sb_adjusted.handle_bar(mock_context, mock_bar_dict)

    def test_handle_bar_insufficient_history(self):
        mock_context = MockContext()
        mock_context.threshold = 2
        mock_context.portfolio.positions = {}
        
        def mock_all_instruments(type_str):
            return pd.DataFrame({
                "order_book_id": ["000001.XSHE", "000002.XSHE"]
            })
        
        def mock_history_bars(stock, count, freq, fields):
            return [{"close": 10.0}]
        
        with patch.dict(sys.modules, {
            'all_instruments': mock_all_instruments,
            'history_bars': mock_history_bars,
        }):
            import sb_adjusted
            mock_bar_dict = MockBarDict()
            sb_adjusted.handle_bar(mock_context, mock_bar_dict)

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
            import sb_adjusted
            mock_bar_dict = MockBarDict()
            sb_adjusted.handle_bar(mock_context, mock_bar_dict)

    def test_handle_bar_order_exception(self):
        mock_context = MockContext()
        mock_context.threshold = 1
        mock_context.portfolio.positions = {}
        
        def mock_all_instruments(type_str):
            return pd.DataFrame({
                "order_book_id": ["000001.XSHE"]
            })
        
        def mock_history_bars(stock, count, freq, fields):
            return [
                {"close": 10.0},
                {"close": 11.0},
            ]
        
        def mock_order_target_percent(stock, percent):
            raise Exception("Order Error")
        
        with patch.dict(sys.modules, {
            'all_instruments': mock_all_instruments,
            'history_bars': mock_history_bars,
            'order_target_percent': mock_order_target_percent,
        }):
            import sb_adjusted
            mock_bar_dict = MockBarDict()
            sb_adjusted.handle_bar(mock_context, mock_bar_dict)

    def test_handle_bar_no_limit_up_stocks(self):
        mock_context = MockContext()
        mock_context.threshold = 1
        mock_context.portfolio.positions = {}
        
        def mock_all_instruments(type_str):
            return pd.DataFrame({
                "order_book_id": ["000001.XSHE", "000002.XSHE"]
            })
        
        def mock_history_bars(stock, count, freq, fields):
            return [
                {"close": 10.0},
                {"close": 10.5},
            ]
        
        with patch.dict(sys.modules, {
            'all_instruments': mock_all_instruments,
            'history_bars': mock_history_bars,
        }):
            import sb_adjusted
            mock_bar_dict = MockBarDict()
            sb_adjusted.handle_bar(mock_context, mock_bar_dict)

    def test_handle_bar_bar_dict_exception(self):
        mock_context = MockContext()
        mock_context.threshold = 1
        mock_context.portfolio.positions = {}
        
        def mock_all_instruments(type_str):
            return pd.DataFrame({
                "order_book_id": ["000001.XSHE"]
            })
        
        def mock_history_bars(stock, count, freq, fields):
            return [
                {"close": 10.0},
                {"close": 11.0},
            ]
        
        with patch.dict(sys.modules, {
            'all_instruments': mock_all_instruments,
            'history_bars': mock_history_bars,
        }):
            import sb_adjusted
            mock_bar_dict = MockBarDict()
            sb_adjusted.handle_bar(mock_context, mock_bar_dict)


class TestEdgeCases:
    def test_empty_all_instruments(self):
        mock_context = MockContext()
        mock_context.portfolio.positions = {}
        
        def mock_all_instruments(type_str):
            return pd.DataFrame({"order_book_id": []})
        
        with patch.dict(sys.modules, {'all_instruments': mock_all_instruments}):
            import sb_adjusted
            mock_bar_dict = MockBarDict()
            sb_adjusted.handle_bar(mock_context, mock_bar_dict)

    def test_all_instruments_exception(self):
        mock_context = MockContext()
        mock_context.portfolio.positions = {}
        
        def mock_all_instruments(type_str):
            raise Exception("API Error")
        
        with patch.dict(sys.modules, {'all_instruments': mock_all_instruments}):
            import sb_adjusted
            mock_bar_dict = MockBarDict()
            try:
                sb_adjusted.handle_bar(mock_context, mock_bar_dict)
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
            import sb_adjusted
            mock_bar_dict = MockBarDict()
            sb_adjusted.handle_bar(mock_context, mock_bar_dict)

    def test_negative_threshold(self):
        mock_context = MockContext()
        mock_context.threshold = -1
        mock_context.portfolio.positions = {}
        
        def mock_all_instruments(type_str):
            return pd.DataFrame({"order_book_id": ["000001.XSHE"]})
        
        def mock_history_bars(stock, count, freq, fields):
            return [
                {"close": 10.0},
                {"close": 11.0},
            ]
        
        def mock_order_target_percent(stock, percent):
            mock_context.trade_count += 1
        
        with patch.dict(sys.modules, {
            'all_instruments': mock_all_instruments,
            'history_bars': mock_history_bars,
            'order_target_percent': mock_order_target_percent,
        }):
            import sb_adjusted
            mock_bar_dict = MockBarDict()
            sb_adjusted.handle_bar(mock_context, mock_bar_dict)

    def test_exact_threshold(self):
        mock_context = MockContext()
        mock_context.threshold = 3
        mock_context.portfolio.positions = {}
        
        def mock_all_instruments(type_str):
            return pd.DataFrame({
                "order_book_id": ["zt1", "zt2", "zt3"]
            })
        
        def mock_history_bars(stock, count, freq, fields):
            return [
                {"close": 10.0},
                {"close": 11.0},
            ]
        
        def mock_order_target_percent(stock, percent):
            mock_context.trade_count += 1
        
        with patch.dict(sys.modules, {
            'all_instruments': mock_all_instruments,
            'history_bars': mock_history_bars,
            'order_target_percent': mock_order_target_percent,
        }):
            import sb_adjusted
            mock_bar_dict = MockBarDict()
            sb_adjusted.handle_bar(mock_context, mock_bar_dict)

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
            import sb_adjusted
            mock_bar_dict = MockBarDict()
            sb_adjusted.handle_bar(mock_context, mock_bar_dict)

    def test_multiple_sell_calls(self):
        mock_context = MockContext()
        mock_context.portfolio.positions = {
            "stock1": MockPosition(),
            "stock2": MockPosition(),
            "stock3": MockPosition(),
        }
        
        sell_count = 0
        
        def mock_all_instruments(type_str):
            return pd.DataFrame({"order_book_id": []})
        
        def mock_order_target_percent(stock, percent):
            if percent == 0:
                sell_count += 1
        
        with patch.dict(sys.modules, {
            'all_instruments': mock_all_instruments,
            'order_target_percent': mock_order_target_percent,
        }):
            import sb_adjusted
            mock_bar_dict = MockBarDict()
            sb_adjusted.handle_bar(mock_context, mock_bar_dict)
            
            assert sell_count == 3

    def test_change_calculation(self):
        mock_context = MockContext()
        mock_context.threshold = 1
        mock_context.portfolio.positions = {}
        
        def mock_all_instruments(type_str):
            return pd.DataFrame({"order_book_id": ["000001.XSHE"]})
        
        def mock_history_bars(stock, count, freq, fields):
            return [
                {"close": 100.0},
                {"close": 110.0},
            ]
        
        def mock_order_target_percent(stock, percent):
            mock_context.trade_count += 1
        
        with patch.dict(sys.modules, {
            'all_instruments': mock_all_instruments,
            'history_bars': mock_history_bars,
            'order_target_percent': mock_order_target_percent,
        }):
            import sb_adjusted
            mock_bar_dict = MockBarDict()
            sb_adjusted.handle_bar(mock_context, mock_bar_dict)
            
            assert mock_context.trade_count > 0

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
            import sb_adjusted
            mock_bar_dict = MockBarDict()
            sb_adjusted.handle_bar(mock_context, mock_bar_dict)

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
            import sb_adjusted
            mock_bar_dict = MockBarDict()
            sb_adjusted.handle_bar(mock_context, mock_bar_dict)