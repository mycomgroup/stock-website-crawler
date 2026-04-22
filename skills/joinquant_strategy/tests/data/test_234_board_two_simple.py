import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from module_loader import load_data_module, load_strategy_module
import pytest
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from unittest.mock import MagicMock, patch, call
from types import SimpleNamespace
import sys

sys.path.insert(0, '/Users/yuping/Downloads/git/stock-website-crawler/skills/joinquant_strategy/data')


class TestBoardTwoSimple:
    @pytest.fixture
    def setup_mocks(self, mock_g, mock_context):
        with patch.dict(sys.modules, {
            'jqdata': MagicMock(),
            'jqfactor': MagicMock(),
            'jqlib': MagicMock(),
            'jqlib.technical_analysis': MagicMock(),
        }):
            jqdata = sys.modules['jqdata']
            jqdata.set_option = MagicMock()
            jqdata.log = MagicMock()
            jqdata.log.set_level = MagicMock()
            jqdata.log.info = MagicMock()
            jqdata.run_daily = MagicMock()
            jqdata.order_value = MagicMock()
            jqdata.order_target_value = MagicMock()
            jqdata.get_current_data = MagicMock()
            jqdata.get_all_securities = MagicMock()
            jqdata.get_all_trade_days = MagicMock()
            jqdata.get_price = MagicMock()
            jqdata.get_fundamentals = MagicMock()
            jqdata.query = MagicMock()
            jqdata.valuation = MagicMock()
            jqdata.valuation.code = 'code'
            jqdata.valuation.circulating_market_cap = 'circulating_market_cap'
            
            jqlib = sys.modules['jqlib.technical_analysis']
            jqlib.HSL = MagicMock()
            
            yield {
                'jqdata': jqdata,
                'jqlib': jqlib,
                'g': mock_g,
                'context': mock_context
            }

    def test_initialize(self, setup_mocks):
        import importlib
        module = load_data_module("234_board_two_simple")
        module = importlib.import_module('234_board_two_simple', 
                                        package='/Users/yuping/Downloads/git/stock-website-crawler/skills/joinquant_strategy/data')
        module.g = setup_mocks['g']
        
        context = setup_mocks['context']
        module.initialize(context)
        
        setup_mocks['jqdata'].set_option.assert_any_call("use_real_price", True)
        setup_mocks['jqdata'].set_option.assert_any_call("avoid_future_data", True)
        assert setup_mocks['g'].board_level == "two"
        assert setup_mocks['g'].ps == 1

    def test_get_hl_stocks_returns_high_limit(self, setup_mocks):
        import importlib
        module = importlib.import_module('234_board_two_simple', 
                                        package='/Users/yuping/Downloads/git/stock-website-crawler/skills/joinquant_strategy/data')
        
        stock_data = pd.DataFrame({
            'code': ['000001.XSHE', '000002.XSHE', '000003.XSHE'],
            'close': [10.0, 20.0, 30.0],
            'high_limit': [10.0, 20.5, 30.0]
        })
        setup_mocks['jqdata'].get_price.return_value = stock_data
        
        result = module.get_hl_stocks(['000001.XSHE', '000002.XSHE', '000003.XSHE'], '2024-01-15')
        
        assert '000001.XSHE' in result
        assert '000003.XSHE' in result
        assert '000002.XSHE' not in result

    def test_get_hl_stocks_empty_on_exception(self, setup_mocks):
        import importlib
        module = importlib.import_module('234_board_two_simple', 
                                        package='/Users/yuping/Downloads/git/stock-website-crawler/skills/joinquant_strategy/data')
        
        setup_mocks['jqdata'].get_price.side_effect = Exception("error")
        
        result = module.get_hl_stocks(['000001.XSHE'], '2024-01-15')
        
        assert result == []

    def test_filter_yzb_filters_one_price(self, setup_mocks):
        import importlib
        module = importlib.import_module('234_board_two_simple', 
                                        package='/Users/yuping/Downloads/git/stock-website-crawler/skills/joinquant_strategy/data')
        
        def mock_get_price(*args, **kwargs):
            code = args[0] if args else kwargs.get('stock_list', [''])[0]
            if code == '000001.XSHE':
                return pd.DataFrame({'low': [10.0], 'high': [10.0]})
            return pd.DataFrame({'low': [9.5], 'high': [10.5]})
        
        setup_mocks['jqdata'].get_price.side_effect = mock_get_price
        
        result = module.filter_yzb(['000001.XSHE', '000002.XSHE'], '2024-01-15')
        
        assert '000001.XSHE' not in result
        assert '000002.XSHE' in result

    def test_filter_yzb_handles_exception(self, setup_mocks):
        import importlib
        module = importlib.import_module('234_board_two_simple', 
                                        package='/Users/yuping/Downloads/git/stock-website-crawler/skills/joinquant_strategy/data')
        
        setup_mocks['jqdata'].get_price.side_effect = Exception("error")
        
        result = module.filter_yzb(['000001.XSHE'], '2024-01-15')
        
        assert result == []

    def test_get_max_lianban(self, setup_mocks):
        import importlib
        module = importlib.import_module('234_board_two_simple', 
                                        package='/Users/yuping/Downloads/git/stock-website-crawler/skills/joinquant_strategy/data')
        
        setup_mocks['jqdata'].get_all_securities.return_value = pd.DataFrame({
            'display_name': ['股票1']
        }, index=['000001.XSHE'])
        
        def mock_get_price(*args, **kwargs):
            if 'count' in kwargs and kwargs['count'] == 1:
                return pd.DataFrame({
                    'code': ['000001.XSHE'],
                    'close': [10.0],
                    'high_limit': [10.0]
                })
            else:
                return pd.DataFrame({
                    'close': [8.0, 9.0, 10.0, 10.0, 10.0],
                    'high_limit': [8.0, 9.0, 10.0, 10.0, 10.0]
                })
        
        setup_mocks['jqdata'].get_price.side_effect = mock_get_price
        
        result = module.get_max_lianban(datetime(2024, 1, 15))
        
        assert result >= 0

    def test_get_max_lianban_handles_exception(self, setup_mocks):
        import importlib
        module = importlib.import_module('234_board_two_simple', 
                                        package='/Users/yuping/Downloads/git/stock-website-crawler/skills/joinquant_strategy/data')
        
        setup_mocks['jqdata'].get_all_securities.side_effect = Exception("error")
        
        result = module.get_max_lianban(datetime(2024, 1, 15))
        
        assert result == 0

    def test_get_zt_count(self, setup_mocks):
        import importlib
        module = importlib.import_module('234_board_two_simple', 
                                        package='/Users/yuping/Downloads/git/stock-website-crawler/skills/joinquant_strategy/data')
        
        setup_mocks['jqdata'].get_all_securities.return_value = pd.DataFrame({
            'display_name': ['股票1', '股票2']
        }, index=['000001.XSHE', '000002.XSHE'])
        
        setup_mocks['jqdata'].get_price.return_value = pd.DataFrame({
            'code': ['000001.XSHE', '000002.XSHE'],
            'close': [10.0, 20.0],
            'high_limit': [10.0, 20.5]
        })
        
        result = module.get_zt_count(datetime(2024, 1, 15))
        
        assert result == 1

    def test_get_zt_count_handles_exception(self, setup_mocks):
        import importlib
        module = importlib.import_module('234_board_two_simple', 
                                        package='/Users/yuping/Downloads/git/stock-website-crawler/skills/joinquant_strategy/data')
        
        setup_mocks['jqdata'].get_all_securities.side_effect = Exception("error")
        
        result = module.get_zt_count(datetime(2024, 1, 15))
        
        assert result == 0

    def test_get_stock_list_no_sentiment(self, setup_mocks):
        import importlib
        module = importlib.import_module('234_board_two_simple', 
                                        package='/Users/yuping/Downloads/git/stock-website-crawler/skills/joinquant_strategy/data')
        module.g = setup_mocks['g']
        module.g.min_max_board = 3
        module.g.min_zt_count = 30
        
        setup_mocks['jqdata'].get_all_securities.return_value = pd.DataFrame({
            'display_name': ['股票1']
        }, index=['000001.XSHE'])
        
        setup_mocks['jqdata'].get_price.return_value = pd.DataFrame({
            'code': ['000001.XSHE'],
            'close': [10.0],
            'high_limit': [10.5]
        })
        
        setup_mocks['jqdata'].get_all_trade_days.return_value = [
            datetime(2024, 1, 10),
            datetime(2024, 1, 11),
            datetime(2024, 1, 12),
            datetime(2024, 1, 15),
        ]
        
        setup_mocks['jqdata'].get_max_lianban = MagicMock(return_value=2)
        setup_mocks['jqdata'].get_zt_count = MagicMock(return_value=20)
        
        module.get_max_lianban = MagicMock(return_value=2)
        module.get_zt_count = MagicMock(return_value=20)
        
        module.get_stock_list(setup_mocks['context'])
        
        assert module.g.sentiment_ok == False
        assert module.g.target_list == []

    def test_sell_positions(self, setup_mocks):
        import importlib
        module = importlib.import_module('234_board_two_simple', 
                                        package='/Users/yuping/Downloads/git/stock-website-crawler/skills/joinquant_strategy/data')
        
        mock_stock = SimpleNamespace()
        mock_stock.last_price = 10.0
        mock_stock.high_limit = 10.5
        setup_mocks['jqdata'].get_current_data.return_value = {'000001.XSHE': mock_stock}
        
        mock_position = SimpleNamespace()
        setup_mocks['context'].portfolio.positions = {'000001.XSHE': mock_position}
        
        module.sell_positions(setup_mocks['context'])
        
        setup_mocks['jqdata'].order_target_value.assert_called_once_with('000001.XSHE', 0)

    def test_sell_positions_keeps_limit_up(self, setup_mocks):
        import importlib
        module = importlib.import_module('234_board_two_simple', 
                                        package='/Users/yuping/Downloads/git/stock-website-crawler/skills/joinquant_strategy/data')
        
        mock_stock = SimpleNamespace()
        mock_stock.last_price = 10.5
        mock_stock.high_limit = 10.5
        setup_mocks['jqdata'].get_current_data.return_value = {'000001.XSHE': mock_stock}
        
        mock_position = SimpleNamespace()
        setup_mocks['context'].portfolio.positions = {'000001.XSHE': mock_position}
        
        module.sell_positions(setup_mocks['context'])
        
        setup_mocks['jqdata'].order_target_value.assert_not_called()