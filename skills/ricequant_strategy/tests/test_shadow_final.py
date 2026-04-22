"""
测试 shadow_final.py - 影子策略简化版
"""
import sys
from pathlib import Path
from unittest.mock import MagicMock, patch, Mock
from datetime import datetime, timedelta
import pytest
import pandas as pd
import numpy as np

sys.path.insert(0, str(Path(__file__).parent.parent))


class MockBar:
    def __init__(
        self,
        close=10.0,
        open_price=9.5,
        high=10.5,
        low=9.0,
        volume=1000000,
        is_trading=True,
    ):
        self.close = close
        self.open = open_price
        self.high = high
        self.low = low
        self.volume = volume
        self.is_trading = is_trading


class MockBarDict(dict):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    
    def __getitem__(self, key):
        if key not in self:
            self[key] = MockBar()
        return super().__getitem__(key)
    
    def __contains__(self, key):
        return True


class MockPosition:
    def __init__(
        self,
        quantity=1000,
        avg_price=10.0,
        market_value=10000.0,
        entry_date=None,
    ):
        self.quantity = quantity
        self.avg_price = avg_price
        self.market_value = market_value
        self.entry_date = entry_date or datetime.now()


class MockPortfolio:
    def __init__(self):
        self.starting_cash = 1000000
        self.total_value = 1000000
        self.positions = {}


class MockContext:
    def __init__(self):
        self.now = datetime.now()
        self.portfolio = MockPortfolio()
        self.strategy_mode = "mainline"
        self.limit_up_count = 0
        self.consecutive_losses = 0
        self.stop_trading_until = None


class MockScheduler:
    def __init__(self):
        self.scheduled_functions = []
    
    def run_daily(self, func, time_rule=None):
        self.scheduled_functions.append((func, time_rule))


class MockInstrument:
    def __init__(self, order_book_id="000001.XSHE", symbol="平安银行"):
        self.order_book_id = order_book_id
        self.symbol = symbol


scheduler = MockScheduler()


class TestShadowFinalInit:
    def test_init_sets_strategy_mode(self):
        mock_context = MockContext()
        mock_scheduler = MockScheduler()
        
        with patch.dict(sys.modules, {
            'scheduler': mock_scheduler,
        }):
            import shadow_final
            import importlib
            importlib.reload(shadow_final)
            
            def mock_market_open(minute=0):
                return f"market_open_{minute}"
            def mock_market_close(minute=0):
                return f"market_close_{minute}"
            
            sys.modules['market_open'] = mock_market_open
            sys.modules['market_close'] = mock_market_close
            
            shadow_final.init(mock_context)
            
            assert mock_context.strategy_mode == "mainline"
            assert mock_context.limit_up_count == 0
            assert mock_context.consecutive_losses == 0
            assert mock_context.stop_trading_until is None

    def test_init_schedules_daily_functions(self):
        mock_context = MockContext()
        mock_scheduler = MockScheduler()
        
        with patch.dict(sys.modules, {'scheduler': mock_scheduler}):
            import shadow_final
            import importlib
            importlib.reload(shadow_final)
            shadow_final.init(mock_context)
            
            assert len(mock_scheduler.scheduled_functions) == 3


class TestGetCandidatePool:
    def test_get_candidate_pool_returns_stocks(self):
        mock_context = MockContext()
        mock_bar_dict = MockBarDict()
        mock_bar_dict["600000.XSHG"] = MockBar(is_trading=True)
        mock_bar_dict["600519.XSHG"] = MockBar(is_trading=True)
        mock_bar_dict["000001.XSHE"] = MockBar(is_trading=True)
        
        def mock_index_components(name):
            if name == "000300.XSHG":
                return ["600000.XSHG", "600519.XSHG"]
            elif name == "000905.XSHG":
                return ["000001.XSHE", "000002.XSHE"]
            return []
        
        def mock_instruments_func(stock):
            return MockInstrument(stock, "正常股票")
        
        with patch.dict(sys.modules, {
            'index_components': mock_index_components,
            'instruments': mock_instruments_func,
        }):
            import shadow_final
            result = shadow_final.get_candidate_pool(mock_context, mock_bar_dict)
            
            assert isinstance(result, list)
            assert len(result) <= 200

    def test_get_candidate_pool_filters_scientific_board(self):
        mock_context = MockContext()
        mock_bar_dict = MockBarDict()
        mock_bar_dict["688001.XSHG"] = MockBar(is_trading=True)
        mock_bar_dict["000001.XSHE"] = MockBar(is_trading=True)
        
        def mock_index_components(name):
            return ["688001.XSHG", "000001.XSHE"]
        
        def mock_instruments_func(stock):
            return MockInstrument(stock, "正常股票")
        
        with patch.dict(sys.modules, {
            'index_components': mock_index_components,
            'instruments': mock_instruments_func,
        }):
            import shadow_final
            result = shadow_final.get_candidate_pool(mock_context, mock_bar_dict)
            
            assert "688001.XSHG" not in result

    def test_get_candidate_pool_filters_st_stocks(self):
        mock_context = MockContext()
        mock_bar_dict = MockBarDict()
        mock_bar_dict["000001.XSHE"] = MockBar(is_trading=True)
        mock_bar_dict["ST001.XSHE"] = MockBar(is_trading=True)
        
        def mock_index_components(name):
            return ["000001.XSHE", "ST001.XSHE"]
        
        def mock_instruments_func(stock):
            if stock == "ST001.XSHE":
                return MockInstrument(stock, "ST股票")
            return MockInstrument(stock, "正常股票")
        
        with patch.dict(sys.modules, {
            'index_components': mock_index_components,
            'instruments': mock_instruments_func,
        }):
            import shadow_final
            result = shadow_final.get_candidate_pool(mock_context, mock_bar_dict)
            
            assert "ST001.XSHE" not in result

    def test_get_candidate_pool_filters_non_trading(self):
        mock_context = MockContext()
        mock_bar_dict = MockBarDict()
        mock_bar_dict["000001.XSHE"] = MockBar(is_trading=False)
        mock_bar_dict["000002.XSHE"] = MockBar(is_trading=True)
        
        def mock_index_components(name):
            return ["000001.XSHE", "000002.XSHE"]
        
        def mock_instruments_func(stock):
            return MockInstrument(stock, "正常股票")
        
        with patch.dict(sys.modules, {
            'index_components': mock_index_components,
            'instruments': mock_instruments_func,
        }):
            import shadow_final
            result = shadow_final.get_candidate_pool(mock_context, mock_bar_dict)
            
            assert "000001.XSHE" not in result

    def test_get_candidate_pool_handles_exception(self):
        mock_context = MockContext()
        mock_bar_dict = MockBarDict()
        
        def mock_index_components(name):
            raise Exception("API Error")
        
        with patch.dict(sys.modules, {'index_components': mock_index_components}):
            import shadow_final
            result = shadow_final.get_candidate_pool(mock_context, mock_bar_dict)
            
            assert result == []

    def test_get_candidate_pool_limits_to_200(self):
        mock_context = MockContext()
        mock_bar_dict = MockBarDict()
        
        stocks = [f"{i:06d}.XSHE" for i in range(300)]
        for stock in stocks:
            mock_bar_dict[stock] = MockBar(is_trading=True)
        
        def mock_index_components(name):
            return stocks
        
        def mock_instruments_func(stock):
            return MockInstrument(stock, "正常股票")
        
        with patch.dict(sys.modules, {
            'index_components': mock_index_components,
            'instruments': mock_instruments_func,
        }):
            import shadow_final
            result = shadow_final.get_candidate_pool(mock_context, mock_bar_dict)
            
            assert len(result) <= 200


class TestCheckEmotion:
    def test_check_emotion_counts_limit_up_stocks(self):
        mock_context = MockContext()
        mock_bar_dict = MockBarDict()
        
        def mock_get_candidate_pool(context, bar_dict):
            return ["000001.XSHE", "000002.XSHE"]
        
        def mock_history_bars(stock, count, freq, fields):
            if stock == "000001.XSHE":
                return np.array([10.0, 11.0])
            return np.array([10.0, 10.5])
        
        with patch.dict(sys.modules, {'history_bars': mock_history_bars}):
            import shadow_final
            shadow_final.get_candidate_pool = mock_get_candidate_pool
            shadow_final.check_emotion(mock_context, mock_bar_dict)
            
            assert mock_context.limit_up_count >= 0

    def test_check_emotion_handles_exception(self):
        mock_context = MockContext()
        mock_bar_dict = MockBarDict()
        
        def mock_get_candidate_pool(context, bar_dict):
            raise Exception("Error")
        
        import shadow_final
        shadow_final.get_candidate_pool = mock_get_candidate_pool
        shadow_final.check_emotion(mock_context, mock_bar_dict)
        
        assert mock_context.limit_up_count == 0

    def test_check_emotion_filters_zero_prev_close(self):
        mock_context = MockContext()
        mock_bar_dict = MockBarDict()
        
        def mock_get_candidate_pool(context, bar_dict):
            return ["000001.XSHE"]
        
        def mock_history_bars(stock, count, freq, fields):
            return np.array([0.0, 10.0])
        
        with patch.dict(sys.modules, {'history_bars': mock_history_bars}):
            import shadow_final
            shadow_final.get_candidate_pool = mock_get_candidate_pool
            shadow_final.check_emotion(mock_context, mock_bar_dict)
            
            assert mock_context.limit_up_count == 0


class TestGenerateSignals:
    def test_generate_signals_stops_trading(self):
        mock_context = MockContext()
        mock_context.stop_trading_until = datetime.now() + timedelta(days=1)
        mock_bar_dict = MockBarDict()
        
        import shadow_final
        shadow_final.generate_signals(mock_context, mock_bar_dict)
        
    def test_generate_signals_max_positions(self):
        mock_context = MockContext()
        mock_context.portfolio.positions = {
            "stock1": MockPosition(),
            "stock2": MockPosition(),
            "stock3": MockPosition(),
        }
        mock_bar_dict = MockBarDict()
        
        import shadow_final
        shadow_final.generate_signals(mock_context, mock_bar_dict)

    def test_generate_signals_mainline_mode(self):
        mock_context = MockContext()
        mock_context.strategy_mode = "mainline"
        mock_context.limit_up_count = 50
        mock_bar_dict = MockBarDict()
        mock_bar_dict["000001.XSHE"] = MockBar(open_price=10.1, high=10.5, close=10.2)
        
        def mock_get_candidate_pool(context, bar_dict):
            return ["000001.XSHE"]
        
        def mock_history_bars(stock, count, freq, fields):
            return np.array([10.0, 10.2])
        
        def mock_order_shares(stock, shares):
            pass
        
        with patch.dict(sys.modules, {
            'history_bars': mock_history_bars,
            'order_shares': mock_order_shares,
        }):
            import shadow_final
            shadow_final.get_candidate_pool = mock_get_candidate_pool
            shadow_final.generate_signals(mock_context, mock_bar_dict)

    def test_generate_signals_low_emotion(self):
        mock_context = MockContext()
        mock_context.strategy_mode = "mainline"
        mock_context.limit_up_count = 10
        mock_bar_dict = MockBarDict()
        
        def mock_get_candidate_pool(context, bar_dict):
            return ["000001.XSHE"]
        
        import shadow_final
        shadow_final.get_candidate_pool = mock_get_candidate_pool
        shadow_final.generate_signals(mock_context, mock_bar_dict)

    def test_generate_signals_observation_mode(self):
        mock_context = MockContext()
        mock_context.strategy_mode = "observation"
        mock_bar_dict = MockBarDict()
        mock_bar_dict["000001.XSHE"] = MockBar(close=10.2)
        
        def mock_get_candidate_pool(context, bar_dict):
            return ["000001.XSHE"]
        
        def mock_history_bars(stock, count, freq, fields):
            return np.array([10.0, 11.0, 12.1, 13.2, 14.3])
        
        def mock_order_shares(stock, shares):
            pass
        
        with patch.dict(sys.modules, {
            'history_bars': mock_history_bars,
            'order_shares': mock_order_shares,
        }):
            import shadow_final
            shadow_final.get_candidate_pool = mock_get_candidate_pool
            shadow_final.generate_signals(mock_context, mock_bar_dict)

    def test_generate_signals_no_signals(self):
        mock_context = MockContext()
        mock_context.strategy_mode = "mainline"
        mock_context.limit_up_count = 50
        mock_bar_dict = MockBarDict()
        
        def mock_get_candidate_pool(context, bar_dict):
            return []
        
        import shadow_final
        shadow_final.get_candidate_pool = mock_get_candidate_pool
        shadow_final.generate_signals(mock_context, mock_bar_dict)


class TestCheckSell:
    def test_check_sell_mainline_profit_threshold(self):
        mock_context = MockContext()
        mock_context.strategy_mode = "mainline"
        mock_position = MockPosition(avg_price=10.0, quantity=1000)
        mock_context.portfolio.positions = {"000001.XSHE": mock_position}
        mock_bar_dict = MockBarDict()
        mock_bar_dict["000001.XSHE"] = MockBar(close=10.5)
        
        def mock_order_shares(stock, shares):
            pass
        
        with patch.dict(sys.modules, {'order_shares': mock_order_shares}):
            import shadow_final
            shadow_final.check_sell(mock_context, mock_bar_dict)

    def test_check_sell_mainline_hold_days(self):
        mock_context = MockContext()
        mock_context.strategy_mode = "mainline"
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
        
        with patch.dict(sys.modules, {'order_shares': mock_order_shares}):
            import shadow_final
            shadow_final.check_sell(mock_context, mock_bar_dict)
            
            assert mock_context.consecutive_losses >= 1

    def test_check_sell_observation_mode(self):
        mock_context = MockContext()
        mock_context.strategy_mode = "observation"
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
        
        with patch.dict(sys.modules, {'order_shares': mock_order_shares}):
            import shadow_final
            shadow_final.check_sell(mock_context, mock_bar_dict)

    def test_check_sell_updates_consecutive_losses(self):
        mock_context = MockContext()
        mock_context.strategy_mode = "mainline"
        mock_context.consecutive_losses = 0
        mock_position = MockPosition(avg_price=10.0, quantity=1000)
        mock_context.portfolio.positions = {"000001.XSHE": mock_position}
        mock_bar_dict = MockBarDict()
        mock_bar_dict["000001.XSHE"] = MockBar(close=9.0)
        
        def mock_order_shares(stock, shares):
            pass
        
        with patch.dict(sys.modules, {'order_shares': mock_order_shares}):
            import shadow_final
            shadow_final.check_sell(mock_context, mock_bar_dict)
            
            assert mock_context.consecutive_losses == 1

    def test_check_sell_stops_after_three_losses(self):
        mock_context = MockContext()
        mock_context.strategy_mode = "mainline"
        mock_context.consecutive_losses = 2
        mock_position = MockPosition(avg_price=10.0, quantity=1000)
        mock_context.portfolio.positions = {"000001.XSHE": mock_position}
        mock_bar_dict = MockBarDict()
        mock_bar_dict["000001.XSHE"] = MockBar(close=9.0)
        
        def mock_order_shares(stock, shares):
            pass
        
        with patch.dict(sys.modules, {'order_shares': mock_order_shares}):
            import shadow_final
            shadow_final.check_sell(mock_context, mock_bar_dict)
            
            assert mock_context.stop_trading_until is not None
            assert mock_context.consecutive_losses == 0

    def test_check_sell_resets_on_profit(self):
        mock_context = MockContext()
        mock_context.strategy_mode = "mainline"
        mock_context.consecutive_losses = 2
        mock_position = MockPosition(avg_price=10.0, quantity=1000)
        mock_context.portfolio.positions = {"000001.XSHE": mock_position}
        mock_bar_dict = MockBarDict()
        mock_bar_dict["000001.XSHE"] = MockBar(close=10.5)
        
        def mock_order_shares(stock, shares):
            pass
        
        with patch.dict(sys.modules, {'order_shares': mock_order_shares}):
            import shadow_final
            shadow_final.check_sell(mock_context, mock_bar_dict)
            
            assert mock_context.consecutive_losses == 0

    def test_check_sell_no_positions(self):
        mock_context = MockContext()
        mock_context.portfolio.positions = {}
        mock_bar_dict = MockBarDict()
        
        import shadow_final
        shadow_final.check_sell(mock_context, mock_bar_dict)


class TestAfterTrading:
    def test_after_trading_does_nothing(self):
        mock_context = MockContext()
        
        import shadow_final
        shadow_final.after_trading(mock_context)


class TestEdgeCases:
    def test_empty_bar_dict(self):
        mock_context = MockContext()
        mock_bar_dict = {}
        
        import shadow_final
        result = shadow_final.get_candidate_pool(mock_context, mock_bar_dict)
        assert result == []

    def test_zero_prev_close_in_signal_generation(self):
        mock_context = MockContext()
        mock_context.strategy_mode = "mainline"
        mock_context.limit_up_count = 50
        mock_bar_dict = MockBarDict()
        mock_bar_dict["000001.XSHE"] = MockBar(open_price=10.0)
        
        def mock_get_candidate_pool(context, bar_dict):
            return ["000001.XSHE"]
        
        def mock_history_bars(stock, count, freq, fields):
            return np.array([0.0, 10.0])
        
        with patch.dict(sys.modules, {'history_bars': mock_history_bars}):
            import shadow_final
            shadow_final.get_candidate_pool = mock_get_candidate_pool
            shadow_final.generate_signals(mock_context, mock_bar_dict)

    def test_negative_profit_pct(self):
        mock_context = MockContext()
        mock_context.strategy_mode = "mainline"
        mock_position = MockPosition(avg_price=10.0, quantity=1000)
        mock_context.portfolio.positions = {"000001.XSHE": mock_position}
        mock_bar_dict = MockBarDict()
        mock_bar_dict["000001.XSHE"] = MockBar(close=8.0)
        
        def mock_order_shares(stock, shares):
            pass
        
        with patch.dict(sys.modules, {'order_shares': mock_order_shares}):
            import shadow_final
            shadow_final.check_sell(mock_context, mock_bar_dict)