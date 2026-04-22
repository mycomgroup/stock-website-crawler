import pytest
import sys
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from unittest.mock import MagicMock, patch
from types import SimpleNamespace

sys.path.insert(0, '/Users/yuping/Downloads/git/stock-website-crawler/skills/joinquant_strategy/data')


@pytest.fixture
def mock_jqdata():
    with patch.dict(sys.modules, {
        'jqdata': MagicMock(),
        'jqfactor': MagicMock(),
        'jqlib': MagicMock(),
        'jqlib.technical_analysis': MagicMock(),
    }):
        yield sys.modules['jqdata']


@pytest.fixture
def mock_g():
    g = SimpleNamespace()
    g.max_cap = 50
    g.ps = 5
    g.max_turnover = 30
    g.max_turnover_ratio = 15
    g.max_lb_1d = 1.5
    g.min_max_board = 3
    g.min_zt_count = 30
    g.min_promote_rate = 20
    g.board_level = "two"
    g.target_list = []
    g.sentiment_ok = False
    g.position_ratio = 0
    g.target_stock = None
    g.test_mode = "double_factor"
    g.count = 0
    return g


@pytest.fixture
def mock_context():
    context = SimpleNamespace()
    context.previous_date = datetime(2024, 1, 15)
    context.current_dt = datetime(2024, 1, 16, 9, 30)
    context.portfolio = SimpleNamespace()
    context.portfolio.available_cash = 100000
    context.portfolio.total_value = 100000
    context.portfolio.positions = {}
    return context


@pytest.fixture
def mock_stock_data():
    return pd.DataFrame({
        'code': ['000001.XSHE', '000002.XSHE', '000003.XSHE'],
        'close': [10.0, 20.0, 30.0],
        'high_limit': [10.0, 20.0, 31.0],
        'low': [9.5, 19.5, 29.5],
        'high': [10.5, 20.5, 30.5],
        'volume': [1000000, 2000000, 1500000],
        'paused': [0, 0, 0]
    })


@pytest.fixture
def mock_valuation_data():
    return pd.DataFrame({
        'code': ['000001.XSHE', '000002.XSHE', '000003.XSHE'],
        'circulating_market_cap': [20.0, 40.0, 60.0],
        'market_cap': [30.0, 50.0, 80.0]
    })


@pytest.fixture
def mock_securities():
    return pd.DataFrame({
        'display_name': ['平安银行', '万科A', '测试股票'],
        'start_date': [datetime(2020, 1, 1), datetime(2020, 1, 1), datetime(2023, 6, 1)]
    }, index=['000001.XSHE', '000002.XSHE', '000003.XSHE'])


@pytest.fixture
def mock_is_st():
    return pd.DataFrame({
        '2024-01-15': [False, False, True]
    }, index=['000001.XSHE', '000002.XSHE', '000003.XSHE'])


@pytest.fixture
def mock_current_data():
    def _mock_current_data(stock_codes):
        data = {}
        for code in stock_codes:
            stock_data = SimpleNamespace()
            stock_data.last_price = 10.0
            stock_data.high_limit = 10.5
            stock_data.day_open = 10.0
            stock_data.low = 9.5
            stock_data.high = 10.5
            data[code] = stock_data
        return data
    return _mock_current_data


@pytest.fixture
def mock_trade_days():
    return [
        datetime(2024, 1, 10),
        datetime(2024, 1, 11),
        datetime(2024, 1, 12),
        datetime(2024, 1, 15),
        datetime(2024, 1, 16),
    ]