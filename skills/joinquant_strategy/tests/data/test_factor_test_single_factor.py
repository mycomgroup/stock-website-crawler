import pytest
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from unittest.mock import MagicMock, patch, call
from types import SimpleNamespace
import sys

sys.path.insert(0, '/Users/yuping/Downloads/git/stock-website-crawler/skills/joinquant_strategy/data')


class TestFactorTestSingleFactor:
    @pytest.fixture
    def mock_jq_functions(self, mock_g, mock_context, mock_stock_data, mock_valuation_data, mock_securities, mock_is_st):
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
            jqdata.get_all_securities = MagicMock(return_value=mock_securities)
            jqdata.get_security_info = MagicMock()
            jqdata.get_extras = MagicMock(return_value=mock_is_st)
            jqdata.get_price = MagicMock(return_value=mock_stock_data)
            jqdata.get_fundamentals = MagicMock(return_value=mock_valuation_data)
            jqdata.query = MagicMock()
            jqdata.valuation = MagicMock()
            jqdata.valuation.code = 'code'
            jqdata.valuation.circulating_market_cap = 'circulating_market_cap'
            jqdata.g = mock_g
            yield jqdata

    def test_initialize_sets_options(self, mock_jq_functions, mock_g):
        import factor_test_single_factor as module
        module.g = mock_g
        
        context = SimpleNamespace()
        module.initialize(context)
        
        mock_jq_functions.set_option.assert_any_call("use_real_price", True)
        mock_jq_functions.set_option.assert_any_call("avoid_future_data", True)
        assert mock_g.ps == 5
        assert mock_g.max_cap == 50

    def test_initialize_calls_run_daily(self, mock_jq_functions, mock_g):
        import factor_test_single_factor as module
        module.g = mock_g
        
        context = SimpleNamespace()
        module.initialize(context)
        
        assert mock_jq_functions.run_daily.call_count == 3

    def test_get_stock_list_filters_stocks(self, mock_jq_functions, mock_g, mock_context, mock_securities):
        import factor_test_single_factor as module
        module.g = mock_g
        module.g = SimpleNamespace()
        module.g.max_cap = 50
        module.g.ps = 5
        
        mock_jq_functions.get_all_securities.return_value = mock_securities
        
        stock_data = pd.DataFrame({
            'code': ['000001.XSHE', '000002.XSHE'],
            'close': [10.0, 20.0],
            'high_limit': [10.0, 20.0]
        })
        mock_jq_functions.get_price.return_value = stock_data
        
        cap_data = pd.DataFrame({
            'code': ['000001.XSHE', '000002.XSHE'],
            'circulating_market_cap': [20.0, 40.0]
        })
        mock_jq_functions.get_fundamentals.return_value = cap_data
        
        mock_jq_functions.get_security_info.return_value = SimpleNamespace(
            start_date=datetime(2020, 1, 1)
        )
        
        is_st_df = pd.DataFrame({datetime(2024, 1, 15): [False, False]}, 
                                index=['000001.XSHE', '000002.XSHE'])
        mock_jq_functions.get_extras.return_value = is_st_df
        
        module.get_stock_list(mock_context)
        
        mock_jq_functions.get_all_securities.assert_called()
        mock_jq_functions.get_price.assert_called()

    def test_buy_orders_stocks(self, mock_jq_functions, mock_g, mock_context):
        import factor_test_single_factor as module
        module.g = mock_g
        module.g.target_list = ['000001.XSHE', '000002.XSHE']
        mock_context.portfolio.available_cash = 100000
        mock_context.portfolio.total_value = 100000
        
        module.buy(mock_context)
        
        assert mock_jq_functions.order_value.call_count == 2

    def test_buy_skips_when_insufficient_cash(self, mock_jq_functions, mock_g, mock_context):
        import factor_test_single_factor as module
        module.g = mock_g
        module.g.target_list = ['000001.XSHE', '000002.XSHE']
        mock_context.portfolio.available_cash = 50
        
        module.buy(mock_context)
        
        mock_jq_functions.order_value.assert_not_called()

    def test_sell_closes_positions(self, mock_jq_functions, mock_g, mock_context):
        import factor_test_single_factor as module
        module.g = mock_g
        
        mock_stock = SimpleNamespace()
        mock_stock.last_price = 10.0
        mock_stock.high_limit = 10.5
        mock_jq_functions.get_current_data.return_value = {'000001.XSHE': mock_stock}
        
        mock_position = SimpleNamespace()
        mock_context.portfolio.positions = {'000001.XSHE': mock_position}
        
        module.sell(mock_context)
        
        mock_jq_functions.order_target_value.assert_called_once_with('000001.XSHE', 0)

    def test_sell_keeps_limit_up_positions(self, mock_jq_functions, mock_g, mock_context):
        import factor_test_single_factor as module
        module.g = mock_g
        
        mock_stock = SimpleNamespace()
        mock_stock.last_price = 10.5
        mock_stock.high_limit = 10.5
        mock_jq_functions.get_current_data.return_value = {'000001.XSHE': mock_stock}
        
        mock_position = SimpleNamespace()
        mock_context.portfolio.positions = {'000001.XSHE': mock_position}
        
        module.sell(mock_context)
        
        mock_jq_functions.order_target_value.assert_not_called()

    def test_empty_target_list(self, mock_jq_functions, mock_g, mock_context):
        import factor_test_single_factor as module
        module.g = mock_g
        module.g.target_list = []
        
        module.buy(mock_context)
        
        mock_jq_functions.order_value.assert_not_called()

    def test_filters_new_stocks(self, mock_jq_functions, mock_g, mock_context):
        import factor_test_single_factor as module
        module.g = mock_g
        module.g.max_cap = 50
        module.g.ps = 5
        
        mock_securities_new = pd.DataFrame({
            'display_name': ['平安银行', '新股'],
            'start_date': [datetime(2020, 1, 1), datetime(2023, 12, 1)]
        }, index=['000001.XSHE', '000002.XSHE'])
        mock_jq_functions.get_all_securities.return_value = mock_securities_new
        
        def mock_get_security_info(code):
            if code == '000001.XSHE':
                return SimpleNamespace(start_date=datetime(2020, 1, 1))
            return SimpleNamespace(start_date=datetime(2023, 12, 1))
        
        mock_jq_functions.get_security_info.side_effect = mock_get_security_info
        
        stock_data = pd.DataFrame({
            'code': ['000001.XSHE'],
            'close': [10.0],
            'high_limit': [10.0]
        })
        mock_jq_functions.get_price.return_value = stock_data
        
        cap_data = pd.DataFrame({
            'code': ['000001.XSHE'],
            'circulating_market_cap': [20.0]
        })
        mock_jq_functions.get_fundamentals.return_value = cap_data
        
        is_st_df = pd.DataFrame({datetime(2024, 1, 15): [False]}, 
                                index=['000001.XSHE'])
        mock_jq_functions.get_extras.return_value = is_st_df
        
        module.get_stock_list(mock_context)
        
        assert len(module.g.target_list) <= 5

    def test_filters_by_market_cap(self, mock_jq_functions, mock_g, mock_context):
        import factor_test_single_factor as module
        module.g = mock_g
        module.g.max_cap = 50
        module.g.ps = 5
        
        cap_data = pd.DataFrame({
            'code': ['000001.XSHE', '000002.XSHE', '000003.XSHE'],
            'circulating_market_cap': [20.0, 40.0, 60.0]
        })
        mock_jq_functions.get_fundamentals.return_value = cap_data
        
        stock_data = pd.DataFrame({
            'code': ['000001.XSHE', '000002.XSHE', '000003.XSHE'],
            'close': [10.0, 20.0, 30.0],
            'high_limit': [10.0, 20.0, 30.0]
        })
        mock_jq_functions.get_price.return_value = stock_data
        
        mock_securities_all = pd.DataFrame({
            'display_name': ['股票1', '股票2', '股票3'],
            'start_date': [datetime(2020, 1, 1), datetime(2020, 1, 1), datetime(2020, 1, 1)]
        }, index=['000001.XSHE', '000002.XSHE', '000003.XSHE'])
        mock_jq_functions.get_all_securities.return_value = mock_securities_all
        
        mock_jq_functions.get_security_info.return_value = SimpleNamespace(
            start_date=datetime(2020, 1, 1)
        )
        
        is_st_df = pd.DataFrame({
            datetime(2024, 1, 15): [False, False, False]
        }, index=['000001.XSHE', '000002.XSHE', '000003.XSHE'])
        mock_jq_functions.get_extras.return_value = is_st_df
        
        module.get_stock_list(mock_context)
        
        mock_jq_functions.get_fundamentals.assert_called()