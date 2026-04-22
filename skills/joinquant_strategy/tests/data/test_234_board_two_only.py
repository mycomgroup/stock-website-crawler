import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from module_loader import load_data_module, load_strategy_module
import pytest
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from unittest.mock import MagicMock, patch
from types import SimpleNamespace
import sys

sys.path.insert(0, '/Users/yuping/Downloads/git/stock-website-crawler/skills/joinquant_strategy/data')


class TestBoardTwoOnly:
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
            jqdata.get_extras = MagicMock()
            jqdata.query = MagicMock()
            jqdata.valuation = MagicMock()
            jqdata.valuation.code = 'code'
            jqdata.valuation.market_cap = 'market_cap'
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
        module = load_data_module("234_board_two_only")
        module.g = setup_mocks['g']
        
        module.initialize(setup_mocks['context'])
        
        setup_mocks['jqdata'].set_option.assert_any_call("use_real_price", True)
        assert setup_mocks['g'].board_level == "two"
        assert setup_mocks['g'].ps == 1

    def test_check_sentiment_all_conditions_met(self, setup_mocks):
        module = load_data_module("234_board_two_only")
        module.g = setup_mocks['g']
        module.g.min_max_board = 3
        module.g.min_zt_count = 30
        module.g.min_promote_rate = 20
        
        setup_mocks['context'].previous_date = datetime(2024, 1, 15)
        
        module.calc_max_lianban = MagicMock(return_value=5)
        module.get_zt_stocks = MagicMock(return_value=['000001.XSHE'] * 80)
        module.calc_promote_rate = MagicMock(return_value=30)
        
        module.check_sentiment(setup_mocks['context'])
        
        assert module.g.sentiment_ok == True
        assert module.g.position_ratio == 1.0

    def test_check_sentiment_medium_conditions(self, setup_mocks):
        module = load_data_module("234_board_two_only")
        module.g = setup_mocks['g']
        module.g.min_max_board = 3
        module.g.min_zt_count = 30
        module.g.min_promote_rate = 20
        
        setup_mocks['context'].previous_date = datetime(2024, 1, 15)
        
        module.calc_max_lianban = MagicMock(return_value=4)
        module.get_zt_stocks = MagicMock(return_value=['000001.XSHE'] * 50)
        module.calc_promote_rate = MagicMock(return_value=30)
        
        module.check_sentiment(setup_mocks['context'])
        
        assert module.g.sentiment_ok == True
        assert module.g.position_ratio == 0.75

    def test_check_sentiment_low_conditions(self, setup_mocks):
        module = load_data_module("234_board_two_only")
        module.g = setup_mocks['g']
        module.g.min_max_board = 3
        module.g.min_zt_count = 30
        module.g.min_promote_rate = 20
        
        setup_mocks['context'].previous_date = datetime(2024, 1, 15)
        
        module.calc_max_lianban = MagicMock(return_value=3)
        module.get_zt_stocks = MagicMock(return_value=['000001.XSHE'] * 35)
        module.calc_promote_rate = MagicMock(return_value=25)
        
        module.check_sentiment(setup_mocks['context'])
        
        assert module.g.sentiment_ok == True
        assert module.g.position_ratio == 0.5

    def test_check_sentiment_not_met(self, setup_mocks):
        module = load_data_module("234_board_two_only")
        module.g = setup_mocks['g']
        module.g.min_max_board = 3
        module.g.min_zt_count = 30
        module.g.min_promote_rate = 20
        
        setup_mocks['context'].previous_date = datetime(2024, 1, 15)
        
        module.calc_max_lianban = MagicMock(return_value=2)
        module.get_zt_stocks = MagicMock(return_value=['000001.XSHE'] * 20)
        module.calc_promote_rate = MagicMock(return_value=15)
        
        module.check_sentiment(setup_mocks['context'])
        
        assert module.g.sentiment_ok == False
        assert module.g.position_ratio == 0

    def test_get_stock_list_no_sentiment(self, setup_mocks):
        module = load_data_module("234_board_two_only")
        module.g = setup_mocks['g']
        module.g.sentiment_ok = False
        
        module.get_stock_list(setup_mocks['context'])
        
        assert module.g.target_list == []

    def test_prepare_stock_list(self, setup_mocks):
        module = load_data_module("234_board_two_only")
        
        setup_mocks['jqdata'].get_all_securities.return_value = pd.DataFrame({
            'display_name': ['股票1', '股票2', '股票3']
        }, index=['000001.XSHE', '688001.XSHG', '000002.XSHE'])
        
        setup_mocks['jqdata'].get_security_info.return_value = SimpleNamespace(
            start_date=datetime(2020, 1, 1)
        )
        
        is_st_df = pd.DataFrame({
            datetime(2024, 1, 15): [False, False, False]
        }, index=['000001.XSHE', '688001.XSHG', '000002.XSHE'])
        setup_mocks['jqdata'].get_extras.return_value = is_st_df
        
        stock_data = pd.DataFrame({
            'code': ['000001.XSHE', '000002.XSHE'],
            'paused': [0, 0]
        })
        setup_mocks['jqdata'].get_price.return_value = stock_data
        
        module.filter_cykcbj_stock = MagicMock(side_effect=lambda x: [s for s in x if s[0] not in ['6', '4', '8', '3']])
        module.filter_new_stock = MagicMock(return_value=['000001.XSHE', '000002.XSHE'])
        module.filter_st_stock = MagicMock(return_value=['000001.XSHE', '000002.XSHE'])
        module.filter_paused_stock = MagicMock(return_value=['000001.XSHE', '000002.XSHE'])
        
        result = module.prepare_stock_list(datetime(2024, 1, 15))
        
        assert isinstance(result, list)

    def test_get_hl_stock(self, setup_mocks):
        module = load_data_module("234_board_two_only")
        
        stock_data = pd.DataFrame({
            'code': ['000001.XSHE', '000002.XSHE', '000003.XSHE'],
            'close': [10.0, 20.0, 30.0],
            'high_limit': [10.0, 20.5, 30.0]
        })
        setup_mocks['jqdata'].get_price.return_value = stock_data
        
        result = module.get_hl_stock(['000001.XSHE', '000002.XSHE', '000003.XSHE'], datetime(2024, 1, 15))
        
        assert '000001.XSHE' in result
        assert '000003.XSHE' in result
        assert '000002.XSHE' not in result

    def test_filter_yzb(self, setup_mocks):
        module = load_data_module("234_board_two_only")
        
        def mock_get_price(*args, **kwargs):
            code = args[0] if args else ''
            if code == '000001.XSHE':
                return pd.DataFrame({'low': [10.0], 'high': [10.0]})
            return pd.DataFrame({'low': [9.5], 'high': [10.5]})
        
        setup_mocks['jqdata'].get_price.side_effect = mock_get_price
        
        result = module.filter_yzb(['000001.XSHE', '000002.XSHE'], datetime(2024, 1, 15))
        
        assert '000001.XSHE' not in result
        assert '000002.XSHE' in result

    def test_get_turnover_ratio(self, setup_mocks):
        module = load_data_module("234_board_two_only")
        
        setup_mocks['jqlib'].HSL.return_value = [{'000001.XSHE': 15.5}]
        
        result = module.get_turnover_ratio('000001.XSHE', datetime(2024, 1, 15))
        
        assert result == 15.5

    def test_get_turnover_ratio_not_found(self, setup_mocks):
        module = load_data_module("234_board_two_only")
        
        setup_mocks['jqlib'].HSL.return_value = [{'000002.XSHE': 15.5}]
        
        result = module.get_turnover_ratio('000001.XSHE', datetime(2024, 1, 15))
        
        assert result == 0

    def test_filter_by_volume_ratio(self, setup_mocks):
        module = load_data_module("234_board_two_only")
        module.g = setup_mocks['g']
        module.g.max_lb_1d = 1.5
        
        def mock_get_price(*args, **kwargs):
            code = args[0] if args else ''
            if code == '000001.XSHE':
                return pd.DataFrame({'volume': [1000000, 800000]})
            return pd.DataFrame({'volume': [1000000, 1200000]})
        
        setup_mocks['jqdata'].get_price.side_effect = mock_get_price
        
        result = module.filter_by_volume_ratio(['000001.XSHE', '000002.XSHE'], datetime(2024, 1, 15))
        
        assert '000001.XSHE' in result
        assert '000002.XSHE' not in result

    def test_sort_by_free_cap(self, setup_mocks):
        module = load_data_module("234_board_two_only")
        
        def mock_get_fundamentals(*args, **kwargs):
            code = args[0].filter.call_args[0][0].right.value if hasattr(args[0], 'filter') else '000001.XSHE'
            if '000001' in str(code):
                return pd.DataFrame({
                    'code': ['000001.XSHE'],
                    'market_cap': [30.0],
                    'circulating_market_cap': [20.0]
                })
            elif '000002' in str(code):
                return pd.DataFrame({
                    'code': ['000002.XSHE'],
                    'market_cap': [50.0],
                    'circulating_market_cap': [15.0]
                })
            return pd.DataFrame({
                'code': ['000003.XSHE'],
                'market_cap': [80.0],
                'circulating_market_cap': [25.0]
            })
        
        setup_mocks['jqdata'].get_fundamentals.side_effect = mock_get_fundamentals
        
        module.get_free_market_cap = MagicMock(side_effect=lambda s, d: 20.0 if s == '000001.XSHE' else (15.0 if s == '000002.XSHE' else 25.0))
        
        result = module.sort_by_free_cap(setup_mocks['context'], ['000001.XSHE', '000002.XSHE', '000003.XSHE'])
        
        assert result[0] == '000002.XSHE'
        assert result[1] == '000001.XSHE'
        assert result[2] == '000003.XSHE'

    def test_get_shifted_date(self, setup_mocks):
        module = load_data_module("234_board_two_only")
        
        trade_days = [
            datetime(2024, 1, 10),
            datetime(2024, 1, 11),
            datetime(2024, 1, 12),
            datetime(2024, 1, 15),
            datetime(2024, 1, 16),
        ]
        setup_mocks['jqdata'].get_all_trade_days.return_value = trade_days
        
        result = module.get_shifted_date('2024-01-15', -1)
        assert result == '2024-01-12'
        
        result = module.get_shifted_date('2024-01-15', 1)
        assert result == '2024-01-16'

    def test_get_shifted_date_out_of_range(self, setup_mocks):
        module = load_data_module("234_board_two_only")
        
        trade_days = [datetime(2024, 1, 15)]
        setup_mocks['jqdata'].get_all_trade_days.return_value = trade_days
        
        result = module.get_shifted_date('2024-01-15', -1)
        assert result == '2024-01-15'

    def test_calc_max_lianban(self, setup_mocks):
        module = load_data_module("234_board_two_only")
        
        setup_mocks['jqdata'].get_all_securities.return_value = pd.DataFrame({
            'display_name': ['股票1']
        }, index=['000001.XSHE'])
        
        setup_mocks['jqdata'].get_price.return_value = pd.DataFrame({
            'close': [8.0, 9.0, 10.0, 10.0, 10.0],
            'high_limit': [8.0, 9.0, 10.0, 10.0, 10.0]
        })
        
        module.get_zt_stocks = MagicMock(return_value=['000001.XSHE'] * 5)
        
        result = module.calc_max_lianban('2024-01-15')
        
        assert result >= 0

    def test_get_zt_stocks(self, setup_mocks):
        module = load_data_module("234_board_two_only")
        
        setup_mocks['jqdata'].get_all_securities.return_value = pd.DataFrame({
            'display_name': ['股票1', '股票2']
        }, index=['000001.XSHE', '000002.XSHE'])
        
        stock_data = pd.DataFrame({
            'code': ['000001.XSHE', '000002.XSHE'],
            'close': [10.0, 20.0],
            'high_limit': [10.0, 20.5]
        })
        setup_mocks['jqdata'].get_price.return_value = stock_data
        
        result = module.get_zt_stocks('2024-01-15')
        
        assert '000001.XSHE' in result
        assert '000002.XSHE' not in result

    def test_calc_promote_rate(self, setup_mocks):
        module = load_data_module("234_board_two_only")
        
        module.get_zt_stocks = MagicMock(side_effect=lambda d: ['000001.XSHE', '000002.XSHE'] if d == '2024-01-15' else ['000001.XSHE', '000003.XSHE'])
        module.get_shifted_date = MagicMock(return_value='2024-01-12')
        
        result = module.calc_promote_rate('2024-01-15')
        
        assert result == 50.0

    def test_calc_promote_rate_no_prev(self, setup_mocks):
        module = load_data_module("234_board_two_only")
        
        module.get_zt_stocks = MagicMock(side_effect=lambda d: [] if d == '2024-01-12' else ['000001.XSHE'])
        module.get_shifted_date = MagicMock(return_value='2024-01-12')
        
        result = module.calc_promote_rate('2024-01-15')
        
        assert result == 0

    def test_filter_cykcbj_stock(self, setup_mocks):
        module = load_data_module("234_board_two_only")
        
        stocks = ['000001.XSHE', '688001.XSHG', '400001.XSBJ', '800001.XSBJ', '300001.XSHE']
        result = module.filter_cykcbj_stock(stocks)
        
        assert '000001.XSHE' in result
        assert '688001.XSHG' not in result
        assert '400001.XSBJ' not in result
        assert '800001.XSBJ' not in result
        assert '300001.XSHE' not in result

    def test_filter_new_stock(self, setup_mocks):
        module = load_data_module("234_board_two_only")
        from datetime import timedelta
        
        stocks = ['000001.XSHE', '000002.XSHE']
        
        def get_security_info_mock(code):
            if code == '000001.XSHE':
                return SimpleNamespace(start_date=datetime(2020, 1, 1))
            return SimpleNamespace(start_date=datetime(2023, 6, 1))
        
        setup_mocks['jqdata'].get_security_info.side_effect = get_security_info_mock
        
        result = module.filter_new_stock(stocks, datetime(2024, 1, 15))
        
        assert '000001.XSHE' in result
        assert '000002.XSHE' not in result

    def test_filter_st_stock(self, setup_mocks):
        module = load_data_module("234_board_two_only")
        
        is_st_df = pd.DataFrame({
            datetime(2024, 1, 15): [False, True, False]
        }, index=['000001.XSHE', '000002.XSHE', '000003.XSHE'])
        setup_mocks['jqdata'].get_extras.return_value = is_st_df
        
        result = module.filter_st_stock(['000001.XSHE', '000002.XSHE', '000003.XSHE'], datetime(2024, 1, 15))
        
        assert '000001.XSHE' in result
        assert '000002.XSHE' not in result
        assert '000003.XSHE' in result

    def test_filter_paused_stock(self, setup_mocks):
        module = load_data_module("234_board_two_only")
        
        stock_data = pd.DataFrame({
            'code': ['000001.XSHE', '000002.XSHE', '000003.XSHE'],
            'paused': [0, 1, 0]
        })
        setup_mocks['jqdata'].get_price.return_value = stock_data
        
        result = module.filter_paused_stock(['000001.XSHE', '000002.XSHE', '000003.XSHE'], datetime(2024, 1, 15))
        
        assert '000001.XSHE' in result
        assert '000002.XSHE' not in result
        assert '000003.XSHE' in result

    def test_buy_stocks_no_sentiment(self, setup_mocks):
        module = load_data_module("234_board_two_only")
        module.g = setup_mocks['g']
        module.g.sentiment_ok = False
        module.g.target_list = ['000001.XSHE']
        
        module.buy_stocks(setup_mocks['context'])
        
        setup_mocks['jqdata'].order_value.assert_not_called()

    def test_buy_stocks_empty_target(self, setup_mocks):
        module = load_data_module("234_board_two_only")
        module.g = setup_mocks['g']
        module.g.sentiment_ok = True
        module.g.target_list = []
        
        module.buy_stocks(setup_mocks['context'])
        
        setup_mocks['jqdata'].order_value.assert_not_called()

    def test_buy_stocks_limit_up_open(self, setup_mocks):
        module = load_data_module("234_board_two_only")
        module.g = setup_mocks['g']
        module.g.sentiment_ok = True
        module.g.position_ratio = 0.5
        module.g.target_list = ['000001.XSHE']
        
        mock_stock = SimpleNamespace()
        mock_stock.last_price = 10.5
        mock_stock.high_limit = 10.5
        setup_mocks['jqdata'].get_current_data.return_value = {'000001.XSHE': mock_stock}
        
        module.buy_stocks(setup_mocks['context'])
        
        setup_mocks['jqdata'].order_value.assert_not_called()

    def test_sell_early_stop_loss(self, setup_mocks):
        module = load_data_module("234_board_two_only")
        module.g = setup_mocks['g']
        
        mock_stock = SimpleNamespace()
        mock_stock.last_price = 9.5
        mock_stock.high_limit = 10.5
        mock_stock.day_open = 9.5
        setup_mocks['jqdata'].get_current_data.return_value = {'000001.XSHE': mock_stock}
        
        mock_position = SimpleNamespace()
        mock_position.closeable_amount = 100
        mock_position.avg_cost = 10.0
        setup_mocks['context'].portfolio.positions = {'000001.XSHE': mock_position}
        
        module.sell_early(setup_mocks['context'])
        
        setup_mocks['jqdata'].order_target_value.assert_called_once_with('000001.XSHE', 0)

    def test_sell_late(self, setup_mocks):
        module = load_data_module("234_board_two_only")
        module.g = setup_mocks['g']
        
        mock_stock = SimpleNamespace()
        mock_stock.last_price = 10.0
        mock_stock.high_limit = 10.5
        setup_mocks['jqdata'].get_current_data.return_value = {'000001.XSHE': mock_stock}
        
        mock_position = SimpleNamespace()
        mock_position.closeable_amount = 100
        mock_position.avg_cost = 9.5
        mock_position.init_time = datetime(2024, 1, 14)
        setup_mocks['context'].portfolio.positions = {'000001.XSHE': mock_position}
        setup_mocks['context'].current_dt = datetime(2024, 1, 16, 14, 50)
        
        module.sell_late(setup_mocks['context'])
        
        setup_mocks['jqdata'].order_target_value.assert_called_once_with('000001.XSHE', 0)