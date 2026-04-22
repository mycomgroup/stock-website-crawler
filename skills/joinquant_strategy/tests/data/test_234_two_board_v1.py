import pytest
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from unittest.mock import MagicMock, patch
from types import SimpleNamespace
import sys
import os
import importlib.util

DATA_DIR = '/Users/yuping/Downloads/git/stock-website-crawler/skills/joinquant_strategy/data'


def load_module(module_name):
    spec = importlib.util.spec_from_file_location(
        module_name, 
        os.path.join(DATA_DIR, f"{module_name}.py")
    )
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module


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
    g.max_turnover = 30
    g.target_stock = None
    g.ps = 1
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


class TestTwoBoardV1:
    def test_initialize(self, mock_jqdata, mock_g, mock_context):
        mock_jqdata.set_option = MagicMock()
        mock_jqdata.log = MagicMock()
        mock_jqdata.log.set_level = MagicMock()
        mock_jqdata.run_daily = MagicMock()
        
        module = load_module('234_two_board_v1')
        module.g = mock_g
        
        module.initialize(mock_context)
        
        mock_jqdata.set_option.assert_any_call("use_real_price", True)
        assert module.g.max_turnover == 30
        assert module.g.target_stock is None
        assert module.g.ps == 1

    def test_get_hl_stocks_normal_case(self, mock_jqdata):
        module = load_module('234_two_board_v1')
        
        stock_data = pd.DataFrame({
            'code': ['000001.XSHE', '000002.XSHE'],
            'close': [10.0, 20.0],
            'high_limit': [10.0, 21.0]
        })
        mock_jqdata.get_price = MagicMock(return_value=stock_data)
        
        result = module.get_hl_stocks(['000001.XSHE', '000002.XSHE'], '2024-01-15')
        
        assert result == ['000001.XSHE']

    def test_get_hl_stocks_no_limit(self, mock_jqdata):
        module = load_module('234_two_board_v1')
        
        stock_data = pd.DataFrame({
            'code': ['000001.XSHE'],
            'close': [10.0],
            'high_limit': [10.5]
        })
        mock_jqdata.get_price = MagicMock(return_value=stock_data)
        
        result = module.get_hl_stocks(['000001.XSHE'], '2024-01-15')
        
        assert result == []

    def test_get_hl_stocks_empty_df(self, mock_jqdata):
        module = load_module('234_two_board_v1')
        
        mock_jqdata.get_price = MagicMock(return_value=pd.DataFrame())
        
        result = module.get_hl_stocks(['000001.XSHE'], '2024-01-15')
        
        assert result == []

    def test_get_hl_stocks_exception(self, mock_jqdata):
        module = load_module('234_two_board_v1')
        
        mock_jqdata.get_price = MagicMock(side_effect=Exception("error"))
        
        result = module.get_hl_stocks(['000001.XSHE'], '2024-01-15')
        
        assert result == []

    def test_filter_yzb_normal_case(self, mock_jqdata):
        module = load_module('234_two_board_v1')
        
        def mock_get_price(*args, **kwargs):
            if args[0] == '000001.XSHE':
                return pd.DataFrame({'low': [9.5], 'high': [10.5]})
            return pd.DataFrame({'low': [20.0], 'high': [20.0]})
        
        mock_jqdata.get_price = MagicMock(side_effect=mock_get_price)
        
        result = module.filter_yzb(['000001.XSHE', '000002.XSHE'], '2024-01-15')
        
        assert '000001.XSHE' in result
        assert '000002.XSHE' not in result

    def test_filter_yzb_empty_list(self, mock_jqdata):
        module = load_module('234_two_board_v1')
        
        result = module.filter_yzb([], '2024-01-15')
        
        assert result == []

    def test_filter_yzb_exception(self, mock_jqdata):
        module = load_module('234_two_board_v1')
        
        mock_jqdata.get_price = MagicMock(side_effect=Exception("error"))
        
        result = module.filter_yzb(['000001.XSHE'], '2024-01-15')
        
        assert result == []

    def test_get_prev_date_found(self, mock_jqdata):
        module = load_module('234_two_board_v1')
        
        trade_days = [
            datetime(2024, 1, 10),
            datetime(2024, 1, 11),
            datetime(2024, 1, 12),
            datetime(2024, 1, 15),
            datetime(2024, 1, 16),
        ]
        mock_jqdata.get_all_trade_days = MagicMock(return_value=trade_days)
        
        result = module.get_prev_date('2024-01-15')
        
        assert result == '2024-01-12'

    def test_get_prev_date_not_found(self, mock_jqdata):
        module = load_module('234_two_board_v1')
        
        trade_days = [
            datetime(2024, 1, 10),
            datetime(2024, 1, 15),
        ]
        mock_jqdata.get_all_trade_days = MagicMock(return_value=trade_days)
        
        result = module.get_prev_date('2024-01-20')
        
        assert result == '2024-01-20'

    def test_get_prev_date_first_day(self, mock_jqdata):
        module = load_module('234_two_board_v1')
        
        trade_days = [datetime(2024, 1, 10)]
        mock_jqdata.get_all_trade_days = MagicMock(return_value=trade_days)
        
        result = module.get_prev_date('2024-01-10')
        
        assert result == '2024-01-10'

    def test_select_stock_no_target(self, mock_jqdata, mock_g, mock_context):
        module = load_module('234_two_board_v1')
        module.g = mock_g
        
        mock_jqdata.get_all_securities = MagicMock(return_value=pd.DataFrame({
            'display_name': ['股票']
        }, index=['000001.XSHE']))
        mock_jqdata.get_price = MagicMock(side_effect=Exception("error"))
        
        module.select_stock(mock_context)
        
        assert module.g.target_stock is None

    def test_buy_stock_no_target(self, mock_jqdata, mock_g, mock_context):
        module = load_module('234_two_board_v1')
        module.g = mock_g
        module.g.target_stock = None
        
        module.buy_stock(mock_context)

    def test_buy_stock_limit_open(self, mock_jqdata, mock_g, mock_context):
        module = load_module('234_two_board_v1')
        module.g = mock_g
        module.g.target_stock = '000001.XSHE'
        
        mock_stock = SimpleNamespace()
        mock_stock.last_price = 10.5
        mock_stock.high_limit = 10.5
        mock_jqdata.get_current_data = MagicMock(return_value={'000001.XSHE': mock_stock})
        mock_jqdata.log = MagicMock()
        
        module.buy_stock(mock_context)

    def test_buy_stock_normal(self, mock_jqdata, mock_g, mock_context):
        module = load_module('234_two_board_v1')
        module.g = mock_g
        module.g.target_stock = '000001.XSHE'
        mock_context.portfolio.positions = {}
        
        mock_stock = SimpleNamespace()
        mock_stock.last_price = 10.0
        mock_stock.high_limit = 10.5
        mock_jqdata.get_current_data = MagicMock(return_value={'000001.XSHE': mock_stock})
        mock_jqdata.order_value = MagicMock()
        mock_jqdata.log = MagicMock()
        
        module.buy_stock(mock_context)
        
        mock_jqdata.order_value.assert_called_with('000001.XSHE', 100000)

    def test_buy_stock_already_has_position(self, mock_jqdata, mock_g, mock_context):
        module = load_module('234_two_board_v1')
        module.g = mock_g
        module.g.target_stock = '000001.XSHE'
        mock_context.portfolio.positions = {'000002.XSHE': MagicMock()}
        
        mock_stock = SimpleNamespace()
        mock_stock.last_price = 10.0
        mock_stock.high_limit = 10.5
        mock_jqdata.get_current_data = MagicMock(return_value={'000001.XSHE': mock_stock})
        
        module.buy_stock(mock_context)

    def test_sell_stock_limit_hold(self, mock_jqdata, mock_context):
        module = load_module('234_two_board_v1')
        
        mock_stock = SimpleNamespace()
        mock_stock.last_price = 10.5
        mock_stock.high_limit = 10.5
        mock_jqdata.get_current_data = MagicMock(return_value={'000001.XSHE': mock_stock})
        
        mock_position = MagicMock()
        mock_context.portfolio.positions = {'000001.XSHE': mock_position}
        
        module.sell_stock(mock_context)

    def test_sell_stock_normal(self, mock_jqdata, mock_context):
        module = load_module('234_two_board_v1')
        
        mock_stock = SimpleNamespace()
        mock_stock.last_price = 10.0
        mock_stock.high_limit = 10.5
        mock_jqdata.get_current_data = MagicMock(return_value={'000001.XSHE': mock_stock})
        
        mock_position = MagicMock()
        mock_context.portfolio.positions = {'000001.XSHE': mock_position}
        mock_jqdata.order_target_value = MagicMock()
        mock_jqdata.log = MagicMock()
        
        module.sell_stock(mock_context)
        
        mock_jqdata.order_target_value.assert_called_with('000001.XSHE', 0)

    def test_sell_stock_no_positions(self, mock_jqdata, mock_context):
        module = load_module('234_two_board_v1')
        
        mock_context.portfolio.positions = {}
        
        module.sell_stock(mock_context)