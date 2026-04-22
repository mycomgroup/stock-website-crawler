"""
公共测试配置和fixtures
"""
import sys
from pathlib import Path
from datetime import datetime, timedelta
from unittest.mock import MagicMock, patch
import pytest
import pandas as pd
import numpy as np

project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))


class MockBar:
    def __init__(
        self,
        close=10.0,
        open_price=9.5,
        high=10.5,
        low=9.0,
        volume=1000000,
        is_trading=True,
        last_price=10.0,
        limit_up=11.0,
        limit_down=9.0,
    ):
        self.close = close
        self.open = open_price
        self.high = high
        self.low = low
        self.volume = volume
        self.is_trading = is_trading
        self.last_price = last_price
        self.limit_up = limit_up
        self.limit_down = limit_down


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
        self.daily_pnl = 0
        self.daily_returns = 0.0


class MockContext:
    def __init__(self):
        self.now = datetime.now()
        self.portfolio = MockPortfolio()
        self.subportfolios = []
        self.strategy_mode = "mainline"
        self.limit_up_count = 0
        self.consecutive_losses = 0
        self.stop_trading_until = None
        self.stocks_in_pool = []
        self.trade_count = 0
        self.stock_pool = 200
        self.threshold = 10
        self.volume_ratio = 1.875
        self.mainline_weight = 0.5
        self.second_board_weight = 0.5
        self.scheme = "C"
        self.mainline_trades = []
        self.second_board_trades = []
        self.combo_trades = []
        self.daily_signals = {}


class MockInstrument:
    def __init__(self, order_book_id="000001.XSHE", symbol="平安银行"):
        self.order_book_id = order_book_id
        self.symbol = symbol
        self.display_name = symbol


class MockScheduler:
    def __init__(self):
        self.scheduled_functions = []
    
    def run_daily(self, func, time_rule=None):
        self.scheduled_functions.append((func, time_rule))


class MockLogger:
    def __init__(self):
        self.messages = []
    
    def info(self, msg):
        self.messages.append(("info", msg))
    
    def warning(self, msg):
        self.messages.append(("warning", msg))
    
    def error(self, msg):
        self.messages.append(("error", msg))
    
    def debug(self, msg):
        self.messages.append(("debug", msg))


@pytest.fixture
def mock_context():
    return MockContext()


@pytest.fixture
def mock_bar_dict():
    return MockBarDict()


@pytest.fixture
def mock_scheduler():
    return MockScheduler()


@pytest.fixture
def mock_logger():
    return MockLogger()


@pytest.fixture
def mock_position():
    return MockPosition()


def create_mock_history_bars(num_bars=5, close_prices=None, opens=None, highs=None, lows=None, limit_ups=None):
    bars = []
    for i in range(num_bars):
        bar = {
            "close": close_prices[i] if close_prices else 10.0 + i * 0.1,
            "open": opens[i] if opens else 9.8 + i * 0.1,
            "high": highs[i] if highs else 10.2 + i * 0.1,
            "low": lows[i] if lows else 9.6 + i * 0.1,
            "high_limit": limit_ups[i] if limit_ups else 11.0,
            "limit_up": limit_ups[i] if limit_ups else 11.0,
        }
        bars.append(bar)
    return bars


@pytest.fixture
def mock_history_bars():
    return create_mock_history_bars


@pytest.fixture
def mock_instruments():
    instruments_map = {
        "000001.XSHE": MockInstrument("000001.XSHE", "平安银行"),
        "000002.XSHE": MockInstrument("000002.XSHE", "万科A"),
        "600000.XSHG": MockInstrument("600000.XSHG", "浦发银行"),
        "600519.XSHG": MockInstrument("600519.XSHG", "贵州茅台"),
        "688001.XSHG": MockInstrument("688001.XSHG", "华兴源创"),
    }
    return instruments_map


@pytest.fixture
def setup_mocks(monkeypatch):
    global scheduler, logger, market_open, market_close, index_components
    global history_bars, instruments, order_shares, all_instruments
    global get_factor, order_target_percent
    
    scheduler = MockScheduler()
    logger = MockLogger()
    
    def market_open(minute=0):
        return f"market_open_{minute}"
    
    def market_close(minute=0):
        return f"market_close_{minute}"
    
    def index_components(index_name):
        if index_name == "000300.XSHG":
            return ["600000.XSHG", "600519.XSHG", "000001.XSHE"]
        elif index_name == "000905.XSHG":
            return ["000002.XSHE", "600036.XSHG", "000651.XSHE"]
        return []
    
    def history_bars(stock, bar_count, frequency, fields):
        if isinstance(fields, str):
            if fields == "close":
                return np.array([10.0, 10.5, 11.0, 10.8, 10.9])
            elif fields == "high":
                return np.array([10.5, 11.0, 11.5, 11.2, 11.0])
            elif fields in ["close,limit_up", "close, high_limit"]:
                return create_mock_history_bars(5)
            else:
                return create_mock_history_bars(5, fields=[fields])
        else:
            return create_mock_history_bars(5, fields=fields)
    
    def instruments(stock):
        return MockInstrument(stock, f"股票{stock}")
    
    def order_shares(stock, shares):
        return None
    
    def all_instruments(type_str=None):
        if type_str == "CS":
            return [
                MockInstrument("000001.XSHE", "平安银行"),
                MockInstrument("000002.XSHE", "万科A"),
                MockInstrument("600000.XSHG", "浦发银行"),
                MockInstrument("600519.XSHG", "贵州茅台"),
                MockInstrument("688001.XSHG", "华兴源创"),
            ]
        return []
    
    def get_factor(stock, factor, start_date=None, end_date=None):
        return pd.DataFrame({factor: [50000000000]})
    
    def order_target_percent(stock, percent):
        return None
    
    builtins_module = sys.modules.get("builtins", __import__("builtins"))
    
    monkeypatch.setitem(sys.modules, "scheduler", scheduler)
    monkeypatch.setitem(sys.modules, "logger", logger)
    monkeypatch.setitem(sys.modules, "market_open", market_open)
    monkeypatch.setitem(sys.modules, "market_close", market_close)
    monkeypatch.setitem(sys.modules, "index_components", index_components)
    monkeypatch.setitem(sys.modules, "history_bars", history_bars)
    monkeypatch.setitem(sys.modules, "instruments", instruments)
    monkeypatch.setitem(sys.modules, "order_shares", order_shares)
    monkeypatch.setitem(sys.modules, "all_instruments", all_instruments)
    monkeypatch.setitem(sys.modules, "get_factor", get_factor)
    monkeypatch.setitem(sys.modules, "order_target_percent", order_target_percent)


def create_limit_up_bars(prev_close=10.0, num_days=2):
    bars = []
    for i in range(num_days):
        close = prev_close * (1.10 if i == num_days - 1 else 1.0)
        bars.append({
            "close": close,
            "open": close * 0.98,
            "high": close * 1.02,
            "low": close * 0.97,
            "limit_up": close * 1.1,
            "high_limit": close * 1.1,
        })
    return bars


def create_fake_weak_high_open_bars(prev_close=10.0, open_pct=0.01):
    open_price = prev_close * (1 + open_pct)
    return {
        "close": open_price * 1.02,
        "open": open_price,
        "high": open_price * 1.03,
        "low": open_price * 0.98,
        "prev_close": prev_close,
    }


@pytest.fixture
def rq_mocks():
    """Fixture providing all RiceQuant API mocks"""
    scheduler_mock = MockScheduler()
    logger_mock = MockLogger()
    
    def index_components_mock(index_name):
        if index_name == "000300.XSHG":
            return ["600000.XSHG", "600519.XSHG", "000001.XSHE"]
        elif index_name == "000905.XSHG":
            return ["000002.XSHE", "600036.XSHG", "000651.XSHE"]
        return []
    
    def history_bars_mock(stock, bar_count, frequency, fields):
        return create_mock_history_bars(bar_count)
    
    def instruments_mock(stock):
        return MockInstrument(stock, f"股票{stock}")
    
    def all_instruments_mock(type_str=None):
        if type_str == "CS":
            return [
                MockInstrument("000001.XSHE", "平安银行"),
                MockInstrument("000002.XSHE", "万科A"),
                MockInstrument("600000.XSHG", "浦发银行"),
                MockInstrument("600519.XSHG", "贵州茅台"),
                MockInstrument("688001.XSHG", "华兴源创"),
            ]
        return []
    
    def get_factor_mock(stock, factor, start_date=None, end_date=None):
        return pd.DataFrame({factor: [50000000000]})
    
    mocks = {
        "scheduler": scheduler_mock,
        "logger": logger_mock,
        "index_components": index_components_mock,
        "history_bars": history_bars_mock,
        "instruments": instruments_mock,
        "all_instruments": all_instruments_mock,
        "get_factor": get_factor_mock,
        "order_target_percent": lambda s, p: None,
        "order_target_value": lambda s, v: None,
        "order_shares": lambda s, sh: None,
        "current_snapshot": lambda s: MockBar(),
    }
    return mocks


@pytest.fixture
def mock_factor_df():
    """Create mock factor DataFrame for RFScore7 tests"""
    data = {
        "order_book_id": ["000001.XSHE", "000002.XSHE", "600000.XSHG", "600519.XSHG"],
        "roa": [5.0, 3.0, -1.0, 8.0],
        "roe": [10.0, 5.0, -2.0, 15.0],
        "gross_profit_margin": [30.0, 25.0, 20.0, 40.0],
        "net_profit_margin": [8.0, 5.0, -1.0, 12.0],
        "net_profit_yoy": [15.0, -5.0, 20.0, 10.0],
        "or_yoy": [10.0, 5.0, -10.0, 8.0],
        "pe_ratio": [15.0, -5.0, 20.0, 30.0],
        "pb_ratio": [1.5, 2.0, 0.8, 3.0],
        "return_on_asset": [5.0, 3.0, -1.0, 8.0],
        "return_on_equity": [10.0, 5.0, -2.0, 15.0],
        "market_cap": [50000000000, 30000000000, 8000000000, 200000000000],
        "net_profit_growth_rate": [10.0, 3.0, 25.0, 15.0],
    }
    return pd.DataFrame(data)


@pytest.fixture
def mock_context_rfscore():
    """Create mock context for RFScore7 strategy tests"""
    context = MockContext()
    context.hold_num = 20
    context.pb_pct = 0.10
    context.breadth_reduce = 0.25
    context.breadth_stop = 0.15
    context.reduced_hold_num = 10
    context.last_rebalance_month = -1
    context.run_count = 0
    context.error_count = 0
    context.trade_count = 0
    context.benchmark = "000300.XSHG"
    context.use_real_price = True
    return context