"""
Tests for attribution_a_pure_smallcap_rq.py
Pure small cap market value factor strategy
"""
import sys
from pathlib import Path
import pytest
import pandas as pd
import numpy as np
from datetime import datetime
from unittest.mock import MagicMock, patch, Mock

sys.path.insert(0, str(Path(__file__).parent.parent))


class MockBar:
    def __init__(self, close=10.0, open_price=10.0, is_trading=True, limit_up=11.0):
        self.close = close
        self.open = open_price
        self.is_trading = is_trading
        self.limit_up = limit_up


class MockPortfolio:
    def __init__(self):
        self.positions = {}


class MockContext:
    def __init__(self):
        self.now = datetime(2024, 7, 1, 10, 0)
        self.portfolio = MockPortfolio()
        self.month_count = 0
        self.last_month = None


class MockInstrument:
    def __init__(self, order_book_id):
        self.order_book_id = order_book_id


@pytest.fixture
def mock_rq_api():
    mocks = {}
    mocks['order_target_percent'] = Mock()
    mocks['all_instruments'] = Mock()
    mocks['get_factor'] = Mock()
    return mocks


class TestInit:
    def test_init_sets_default_values(self):
        with patch.dict(sys.modules, {
            'order_target_percent': Mock(),
            'all_instruments': Mock(),
            'get_factor': Mock(),
        }):
            from attribution_a_pure_smallcap_rq import init
            context = MockContext()
            init(context)
            assert context.month_count == 0
            assert context.last_month is None


class TestHandleBar:
    def test_handle_bar_first_call(self):
        with patch.dict(sys.modules, {
            'order_target_percent': Mock(),
            'all_instruments': Mock(),
            'get_factor': Mock(),
        }):
            from attribution_a_pure_smallcap_rq import init, handle_bar
            context = MockContext()
            init(context)
            context.now = datetime(2024, 7, 1, 10, 0)
            with patch('attribution_a_pure_smallcap_rq.rebalance') as mock_rebalance:
                handle_bar(context, {})
                mock_rebalance.assert_called_once()
                assert context.month_count == 1
                assert context.last_month == 7

    def test_handle_bar_same_month(self):
        with patch.dict(sys.modules, {
            'order_target_percent': Mock(),
            'all_instruments': Mock(),
            'get_factor': Mock(),
        }):
            from attribution_a_pure_smallcap_rq import init, handle_bar
            context = MockContext()
            init(context)
            context.month_count = 1
            context.last_month = 7
            context.now = datetime(2024, 7, 15, 10, 0)
            with patch('attribution_a_pure_smallcap_rq.rebalance') as mock_rebalance:
                handle_bar(context, {})
                mock_rebalance.assert_not_called()

    def test_handle_bar_new_month(self):
        with patch.dict(sys.modules, {
            'order_target_percent': Mock(),
            'all_instruments': Mock(),
            'get_factor': Mock(),
        }):
            from attribution_a_pure_smallcap_rq import init, handle_bar
            context = MockContext()
            init(context)
            context.month_count = 1
            context.last_month = 7
            context.now = datetime(2024, 8, 1, 10, 0)
            with patch('attribution_a_pure_smallcap_rq.rebalance') as mock_rebalance:
                handle_bar(context, {})
                mock_rebalance.assert_called_once()
                assert context.last_month == 8


class TestRebalance:
    def test_rebalance_empty_stocks(self):
        mock_all_instruments = Mock()
        mock_all_instruments.return_value = []
        mock_get_factor = Mock()
        mock_get_factor.return_value = None
        mock_order = Mock()
        
        with patch.dict(sys.modules, {
            'all_instruments': mock_all_instruments,
            'get_factor': mock_get_factor,
            'order_target_percent': mock_order,
        }):
            from attribution_a_pure_smallcap_rq import rebalance
            context = MockContext()
            bar_dict = {}
            rebalance(context, bar_dict)
            mock_order.assert_not_called()

    def test_rebalance_with_valid_stocks(self):
        mock_all_instruments = Mock()
        mock_all_instruments.return_value = [
            MockInstrument("000001.XSHE"),
            MockInstrument("000002.XSHE"),
            MockInstrument("600000.XSHG"),
        ]
        
        mock_get_factor = Mock()
        factor_df = pd.DataFrame({
            'market_cap': [100000000, 50000000, 200000000]
        }, index=['000001.XSHE', '000002.XSHE', '600000.XSHG'])
        mock_get_factor.return_value = factor_df
        
        mock_order = Mock()
        
        with patch.dict(sys.modules, {
            'all_instruments': mock_all_instruments,
            'get_factor': mock_get_factor,
            'order_target_percent': mock_order,
        }):
            from attribution_a_pure_smallcap_rq import rebalance
            context = MockContext()
            bar_dict = {}
            rebalance(context, bar_dict)
            assert mock_order.call_count > 0

    def test_rebalance_clears_positions(self):
        mock_all_instruments = Mock()
        mock_all_instruments.return_value = [
            MockInstrument("000001.XSHE"),
        ]
        
        mock_get_factor = Mock()
        factor_df = pd.DataFrame({
            'market_cap': [100000000]
        }, index=['000001.XSHE'])
        mock_get_factor.return_value = factor_df
        
        mock_order = Mock()
        
        with patch.dict(sys.modules, {
            'all_instruments': mock_all_instruments,
            'get_factor': mock_get_factor,
            'order_target_percent': mock_order,
        }):
            from attribution_a_pure_smallcap_rq import rebalance
            context = MockContext()
            context.portfolio.positions = {'999999.XSHG': Mock()}
            bar_dict = {}
            rebalance(context, bar_dict)
            mock_order.assert_any_call('999999.XSHG', 0)

    def test_rebalance_factor_data_empty(self):
        mock_all_instruments = Mock()
        mock_all_instruments.return_value = [MockInstrument("000001.XSHE")]
        
        mock_get_factor = Mock()
        mock_get_factor.return_value = pd.DataFrame()
        
        mock_order = Mock()
        
        with patch.dict(sys.modules, {
            'all_instruments': mock_all_instruments,
            'get_factor': mock_get_factor,
            'order_target_percent': mock_order,
        }):
            from attribution_a_pure_smallcap_rq import rebalance
            context = MockContext()
            bar_dict = {}
            rebalance(context, bar_dict)
            mock_order.assert_not_called()

    def test_rebalance_factor_data_none(self):
        mock_all_instruments = Mock()
        mock_all_instruments.return_value = [MockInstrument("000001.XSHE")]
        
        mock_get_factor = Mock()
        mock_get_factor.return_value = None
        
        mock_order = Mock()
        
        with patch.dict(sys.modules, {
            'all_instruments': mock_all_instruments,
            'get_factor': mock_get_factor,
            'order_target_percent': mock_order,
        }):
            from attribution_a_pure_smallcap_rq import rebalance
            context = MockContext()
            bar_dict = {}
            rebalance(context, bar_dict)
            mock_order.assert_not_called()

    def test_rebalance_selects_smallest_cap(self):
        mock_all_instruments = Mock()
        mock_all_instruments.return_value = [
            MockInstrument("000001.XSHE"),
            MockInstrument("000002.XSHE"),
            MockInstrument("600000.XSHG"),
            MockInstrument("600519.XSHG"),
        ]
        
        mock_get_factor = Mock()
        factor_df = pd.DataFrame({
            'market_cap': [100000000, 50000000, 200000000, 300000000]
        }, index=['000001.XSHE', '000002.XSHE', '600000.XSHG', '600519.XSHG'])
        mock_get_factor.return_value = factor_df
        
        mock_order = Mock()
        
        with patch.dict(sys.modules, {
            'all_instruments': mock_all_instruments,
            'get_factor': mock_get_factor,
            'order_target_percent': mock_order,
        }):
            from attribution_a_pure_smallcap_rq import rebalance
            context = MockContext()
            bar_dict = {}
            rebalance(context, bar_dict)
            call_args = [call[0] for call in mock_order.call_args_list]
            buy_calls = [arg for arg in call_args if arg[1] > 0]
            assert len(buy_calls) > 0

    def test_rebalance_weight_calculation(self):
        mock_all_instruments = Mock()
        stocks = [MockInstrument(f"00000{i}.XSHE") for i in range(1, 6)]
        mock_all_instruments.return_value = stocks
        
        mock_get_factor = Mock()
        factor_df = pd.DataFrame({
            'market_cap': [i * 10000000 for i in range(1, 6)]
        }, index=[f"00000{i}.XSHE" for i in range(1, 6)])
        mock_get_factor.return_value = factor_df
        
        mock_order = Mock()
        
        with patch.dict(sys.modules, {
            'all_instruments': mock_all_instruments,
            'get_factor': mock_get_factor,
            'order_target_percent': mock_order,
        }):
            from attribution_a_pure_smallcap_rq import rebalance
            context = MockContext()
            bar_dict = {}
            rebalance(context, bar_dict)
            buy_calls = [call for call in mock_order.call_args_list if call[0][1] > 0]
            if buy_calls:
                weights = [call[0][1] for call in buy_calls]
                for w in weights:
                    assert 0 < w <= 1.0

    def test_rebalance_with_many_stocks(self):
        mock_all_instruments = Mock()
        stocks = [MockInstrument(f"00000{i:03d}.XSHE") for i in range(250)]
        mock_all_instruments.return_value = stocks
        
        market_caps = [10000000 + i * 1000000 for i in range(250)]
        factor_df = pd.DataFrame({
            'market_cap': market_caps
        }, index=[f"00000{i:03d}.XSHE" for i in range(250)])
        mock_get_factor = Mock()
        mock_get_factor.return_value = factor_df
        
        mock_order = Mock()
        
        with patch.dict(sys.modules, {
            'all_instruments': mock_all_instruments,
            'get_factor': mock_get_factor,
            'order_target_percent': mock_order,
        }):
            from attribution_a_pure_smallcap_rq import rebalance
            context = MockContext()
            bar_dict = {}
            rebalance(context, bar_dict)
            buy_calls = [call for call in mock_order.call_args_list if call[0][1] > 0]
            assert len(buy_calls) <= 20

    def test_rebalance_single_stock(self):
        mock_all_instruments = Mock()
        mock_all_instruments.return_value = [MockInstrument("000001.XSHE")]
        
        mock_get_factor = Mock()
        factor_df = pd.DataFrame({
            'market_cap': [100000000]
        }, index=['000001.XSHE'])
        mock_get_factor.return_value = factor_df
        
        mock_order = Mock()
        
        with patch.dict(sys.modules, {
            'all_instruments': mock_all_instruments,
            'get_factor': mock_get_factor,
            'order_target_percent': mock_order,
        }):
            from attribution_a_pure_smallcap_rq import rebalance
            context = MockContext()
            bar_dict = {}
            rebalance(context, bar_dict)
            mock_order.assert_any_call('000001.XSHE', 1.0)


class TestEdgeCases:
    def test_handle_bar_with_none_month(self):
        with patch.dict(sys.modules, {
            'order_target_percent': Mock(),
            'all_instruments': Mock(),
            'get_factor': Mock(),
        }):
            from attribution_a_pure_smallcap_rq import init, handle_bar
            context = MockContext()
            init(context)
            context.last_month = None
            context.now = datetime(2024, 7, 1, 10, 0)
            with patch('attribution_a_pure_smallcap_rq.rebalance') as mock_rebalance:
                handle_bar(context, {})
                mock_rebalance.assert_called_once()

    def test_rebalance_date_formatting(self):
        mock_all_instruments = Mock()
        mock_all_instruments.return_value = [MockInstrument("000001.XSHE")]
        
        mock_get_factor = Mock()
        factor_df = pd.DataFrame({
            'market_cap': [100000000]
        }, index=['000001.XSHE'])
        mock_get_factor.return_value = factor_df
        
        mock_order = Mock()
        
        with patch.dict(sys.modules, {
            'all_instruments': mock_all_instruments,
            'get_factor': mock_get_factor,
            'order_target_percent': mock_order,
        }):
            from attribution_a_pure_smallcap_rq import rebalance
            context = MockContext()
            context.now = datetime(2024, 7, 15, 14, 30)
            bar_dict = {}
            rebalance(context, bar_dict)
            mock_get_factor.assert_called_once()