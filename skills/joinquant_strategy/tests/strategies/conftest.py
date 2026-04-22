import pytest
import sys
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from unittest.mock import MagicMock, patch, Mock
from types import SimpleNamespace

sys.path.insert(0, '/Users/yuping/Downloads/git/stock-website-crawler/strategies/misc_research/joinquant_strategy')


@pytest.fixture
def mock_jqdata():
    mock_module = MagicMock()
    mock_module.set_option = Mock()
    mock_module.set_benchmark = Mock()
    mock_module.log = MagicMock()
    mock_module.log.set_level = Mock()
    mock_module.log.info = Mock()
    mock_module.log.warn = Mock()
    mock_module.run_daily = Mock()
    mock_module.run_weekly = Mock()
    mock_module.get_all_securities = Mock()
    mock_module.get_price = Mock()
    mock_module.get_current_data = Mock()
    mock_module.get_valuation = Mock()
    mock_module.get_extras = Mock()
    mock_module.get_security_info = Mock()
    mock_module.get_fundamentals = Mock()
    mock_module.get_trade_days = Mock()
    mock_module.get_all_trade_days = Mock()
    mock_module.get_shifted_date = Mock()
    mock_module.order = Mock()
    mock_module.order_value = Mock()
    mock_module.order_target = Mock()
    mock_module.order_target_value = Mock()
    mock_module.g = SimpleNamespace()
    
    with patch.dict(sys.modules, {'jqdata': mock_module}):
        yield mock_module


@pytest.fixture
def mock_g():
    g = SimpleNamespace()
    g.test_dates = ["2024-01-15", "2024-07-15"]
    g.signals = []
    g.current_test_idx = 0
    g.total_zt = 0
    g.trades = 0
    g.wins = 0
    g.pnl_list = []
    g.day = 0
    g.bought = False
    g.test_start = "2022-01-01"
    g.test_end = "2024-12-31"
    g.sample_out_date = "2024-01-01"
    g.open_range = (-0.01, 0.02)
    g.max_signals = 300
    g.results = {"S1": [], "S2": [], "S3": [], "S4": [], "S5": [], "S6": [], "S7": []}
    g.target = []
    g.signals = 0
    g.daily_trades = []
    g.blocked = 0
    g.blocked_days = 0
    g.allow = True
    g.allow_trade = True
    g.target_list = []
    g.trade_count = 0
    g.win_count = 0
    g.daily_signals = []
    g.count = 0
    g.total_pnl = 0
    g.first_board_stocks = []
    g.min_cap = 50
    g.max_cap = 150
    return g


@pytest.fixture
def mock_context():
    context = SimpleNamespace()
    context.previous_date = datetime(2024, 1, 15)
    context.current_dt = datetime(2024, 1, 16, 9, 30)
    
    portfolio = SimpleNamespace()
    portfolio.available_cash = 1000000
    portfolio.total_value = 1000000
    portfolio.positions = {}
    
    pos1 = SimpleNamespace()
    pos1.closeable_amount = 1000
    pos1.avg_cost = 10.0
    pos1.quantity = 1000
    portfolio.positions['000001.XSHE'] = pos1
    
    context.portfolio = portfolio
    return context


@pytest.fixture
def mock_stock_data_dataframe():
    return pd.DataFrame({
        'code': ['000001.XSHE', '000002.XSHE', '600000.XSHG'],
        'close': [10.0, 20.0, 15.0],
        'high_limit': [10.0, 20.0, 15.0],
        'low_limit': [9.0, 18.0, 13.5],
        'low': [9.5, 19.5, 14.5],
        'high': [10.5, 20.5, 15.5],
        'open': [10.0, 19.5, 14.8],
        'volume': [1000000, 2000000, 1500000],
        'paused': [0, 0, 0]
    })


@pytest.fixture
def mock_price_data():
    def _create_price_data(stocks, fields=None, include_limit_up=True):
        data = []
        for stock in stocks:
            row = {'code': stock}
            if 'close' in (fields or ['close']):
                row['close'] = 10.0 if include_limit_up else 9.0
            if 'high_limit' in (fields or ['high_limit']):
                row['high_limit'] = 10.0
            if 'low_limit' in (fields or []):
                row['low_limit'] = 9.0
            if 'open' in (fields or []):
                row['open'] = 9.7
            if 'high' in (fields or []):
                row['high'] = 10.5
            if 'low' in (fields or []):
                row['low'] = 9.5
            if 'paused' in (fields or []):
                row['paused'] = 0
            data.append(row)
        return pd.DataFrame(data)
    return _create_price_data


@pytest.fixture
def mock_valuation_data():
    def _create_valuation(caps=None):
        if caps is None:
            caps = [50, 100, 150]
        return pd.DataFrame({
            'code': ['000001.XSHE', '000002.XSHE', '600000.XSHG'][:len(caps)],
            'circulating_market_cap': caps,
            'market_cap': [c * 1.3 for c in caps]
        })
    return _create_valuation


@pytest.fixture
def mock_securities():
    return pd.DataFrame({
        'display_name': ['平安银行', '万科A', '浦发银行'],
        'start_date': [datetime(2020, 1, 1), datetime(2020, 1, 1), datetime(2020, 1, 1)]
    }, index=['000001.XSHE', '000002.XSHE', '600000.XSHG'])


@pytest.fixture
def mock_current_data():
    def _create_current_data(stocks, open_pct=0.0, paused=False):
        data = {}
        for stock in stocks:
            stock_data = SimpleNamespace()
            stock_data.last_price = 10.0
            stock_data.high_limit = 10.5
            stock_data.day_open = 10.0 + open_pct * 0.1
            stock_data.low = 9.5
            stock_data.high = 10.5
            stock_data.pre_close = 10.0
            stock_data.paused = paused
            stock_data.is_st = False
            data[stock] = stock_data
        return data
    return _create_current_data


@pytest.fixture
def mock_trade_days():
    return [
        datetime(2024, 1, 10),
        datetime(2024, 1, 11),
        datetime(2024, 1, 12),
        datetime(2024, 1, 15),
        datetime(2024, 1, 16),
        datetime(2024, 1, 17),
    ]


@pytest.fixture
def mock_security_info():
    def _create_security_info(days_old=500):
        info = SimpleNamespace()
        info.start_date = datetime(2024, 1, 16) - timedelta(days=days_old)
        return info
    return _create_security_info


@pytest.fixture
def mock_is_st_false():
    return pd.DataFrame({
        '2024-01-15': [False, False, False]
    }, index=['000001.XSHE', '000002.XSHE', '600000.XSHG']).T


@pytest.fixture
def mock_data():
    return {
        '000001.XSHE': SimpleNamespace(
            last_price=10.5,
            paused=False,
            is_st=False
        )
    }