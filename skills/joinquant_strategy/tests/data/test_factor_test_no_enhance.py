import pytest
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from unittest.mock import MagicMock, patch
from types import SimpleNamespace
import sys

sys.path.insert(0, '/Users/yuping/Downloads/git/stock-website-crawler/skills/joinquant_strategy/data')


class TestFactorTestNoEnhance:
    @pytest.fixture
    def setup_mocks(self, mock_g, mock_context, mock_stock_data, mock_securities):
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
            jqdata.get_extras = MagicMock()
            jqdata.get_price = MagicMock(return_value=mock_stock_data)
            jqdata.get_fundamentals = MagicMock()
            jqdata.query = MagicMock()
            jqdata.valuation = MagicMock()
            
            yield {
                'jqdata': jqdata,
                'g': mock_g,
                'context': mock_context
            }

    def test_initialize(self, setup_mocks):
        import factor_test_no_enhance as module
        module.g = setup_mocks['g']
        
        module.initialize(setup_mocks['context'])
        
        setup_mocks['jqdata'].set_option.assert_any_call("use_real_price", True)
        setup_mocks['jqdata'].set_option.assert_any_call("avoid_future_data", True)
        assert setup_mocks['g'].ps == 5

    def test_get_stock_list_basic(self, setup_mocks):
        import factor_test_no_enhance as module
        module.g = setup_mocks['g']
        module.g.ps = 5
        
        mock_securities_df = pd.DataFrame({
            'display_name': ['股票1', '股票2', '股票3'],
            'start_date': [datetime(2020, 1, 1), datetime(2020, 1, 1), datetime(2023, 1, 1)]
        }, index=['000001.XSHE', '000002.XSHE', '000003.XSHE'])
        setup_mocks['jqdata'].get_all_securities.return_value = mock_securities_df
        
        setup_mocks['jqdata'].get_security_info.return_value = SimpleNamespace(
            start_date=datetime(2020, 1, 1)
        )
        
        is_st_df = pd.DataFrame({
            datetime(2024, 1, 15): [False, False, False]
        }, index=['000001.XSHE', '000002.XSHE', '000003.XSHE'])
        setup_mocks['jqdata'].get_extras.return_value = is_st_df
        
        stock_data = pd.DataFrame({
            'code': ['000001.XSHE', '000002.XSHE', '000003.XSHE'],
            'close': [10.0, 20.0, 30.0],
            'high_limit': [10.0, 20.0, 30.0]
        })
        setup_mocks['jqdata'].get_price.return_value = stock_data
        
        module.get_stock_list(setup_mocks['context'])
        
        setup_mocks['jqdata'].get_all_securities.assert_called()
        setup_mocks['jqdata'].get_price.assert_called()
        assert len(module.g.target_list) <= 5

    def test_get_stock_list_filters_st_stocks(self, setup_mocks):
        import factor_test_no_enhance as module
        module.g = setup_mocks['g']
        module.g.ps = 5
        
        mock_securities_df = pd.DataFrame({
            'display_name': ['股票1', '股票2'],
            'start_date': [datetime(2020, 1, 1), datetime(2020, 1, 1)]
        }, index=['000001.XSHE', '000002.XSHE'])
        setup_mocks['jqdata'].get_all_securities.return_value = mock_securities_df
        
        setup_mocks['jqdata'].get_security_info.return_value = SimpleNamespace(
            start_date=datetime(2020, 1, 1)
        )
        
        is_st_df = pd.DataFrame({
            datetime(2024, 1, 15): [False, True]
        }, index=['000001.XSHE', '000002.XSHE'])
        setup_mocks['jqdata'].get_extras.return_value = is_st_df
        
        stock_data = pd.DataFrame({
            'code': ['000001.XSHE', '000002.XSHE'],
            'close': [10.0, 20.0],
            'high_limit': [10.0, 20.0]
        })
        setup_mocks['jqdata'].get_price.return_value = stock_data
        
        module.get_stock_list(setup_mocks['context'])
        
        assert '000002.XSHE' not in module.g.target_list

    def test_get_stock_list_filters_new_stocks(self, setup_mocks):
        import factor_test_no_enhance as module
        module.g = setup_mocks['g']
        module.g.ps = 5
        
        mock_securities_df = pd.DataFrame({
            'display_name': ['股票1', '股票2'],
            'start_date': [datetime(2020, 1, 1), datetime(2023, 6, 1)]
        }, index=['000001.XSHE', '000002.XSHE'])
        setup_mocks['jqdata'].get_all_securities.return_value = mock_securities_df
        
        def get_security_info_mock(code):
            if code == '000001.XSHE':
                return SimpleNamespace(start_date=datetime(2020, 1, 1))
            return SimpleNamespace(start_date=datetime(2023, 6, 1))
        
        setup_mocks['jqdata'].get_security_info.side_effect = get_security_info_mock
        
        is_st_df = pd.DataFrame({
            datetime(2024, 1, 15): [False, False]
        }, index=['000001.XSHE', '000002.XSHE'])
        setup_mocks['jqdata'].get_extras.return_value = is_st_df
        
        stock_data = pd.DataFrame({
            'code': ['000001.XSHE', '000002.XSHE'],
            'close': [10.0, 20.0],
            'high_limit': [10.0, 20.0]
        })
        setup_mocks['jqdata'].get_price.return_value = stock_data
        
        module.get_stock_list(setup_mocks['context'])
        
        setup_mocks['jqdata'].get_security_info.assert_called()

    def test_get_stock_list_only_high_limit(self, setup_mocks):
        import factor_test_no_enhance as module
        module.g = setup_mocks['g']
        module.g.ps = 5
        
        mock_securities_df = pd.DataFrame({
            'display_name': ['股票1', '股票2', '股票3'],
            'start_date': [datetime(2020, 1, 1), datetime(2020, 1, 1), datetime(2020, 1, 1)]
        }, index=['000001.XSHE', '000002.XSHE', '000003.XSHE'])
        setup_mocks['jqdata'].get_all_securities.return_value = mock_securities_df
        
        setup_mocks['jqdata'].get_security_info.return_value = SimpleNamespace(
            start_date=datetime(2020, 1, 1)
        )
        
        is_st_df = pd.DataFrame({
            datetime(2024, 1, 15): [False, False, False]
        }, index=['000001.XSHE', '000002.XSHE', '000003.XSHE'])
        setup_mocks['jqdata'].get_extras.return_value = is_st_df
        
        stock_data = pd.DataFrame({
            'code': ['000001.XSHE', '000002.XSHE', '000003.XSHE'],
            'close': [10.0, 20.0, 30.0],
            'high_limit': [10.0, 20.5, 30.0]
        })
        setup_mocks['jqdata'].get_price.return_value = stock_data
        
        module.get_stock_list(setup_mocks['context'])
        
        assert '000002.XSHE' not in module.g.target_list

    def test_buy(self, setup_mocks):
        import factor_test_no_enhance as module
        module.g = setup_mocks['g']
        module.g.target_list = ['000001.XSHE', '000002.XSHE']
        setup_mocks['context'].portfolio.available_cash = 100000
        setup_mocks['context'].portfolio.total_value = 100000
        
        module.buy(setup_mocks['context'])
        
        assert setup_mocks['jqdata'].order_value.call_count == 2

    def test_buy_insufficient_cash(self, setup_mocks):
        import factor_test_no_enhance as module
        module.g = setup_mocks['g']
        module.g.target_list = ['000001.XSHE', '000002.XSHE']
        setup_mocks['context'].portfolio.available_cash = 50
        
        module.buy(setup_mocks['context'])
        
        setup_mocks['jqdata'].order_value.assert_not_called()

    def test_sell(self, setup_mocks):
        import factor_test_no_enhance as module
        module.g = setup_mocks['g']
        
        mock_stock = SimpleNamespace()
        mock_stock.last_price = 10.0
        mock_stock.high_limit = 10.5
        setup_mocks['jqdata'].get_current_data.return_value = {'000001.XSHE': mock_stock}
        
        mock_position = SimpleNamespace()
        setup_mocks['context'].portfolio.positions = {'000001.XSHE': mock_position}
        
        module.sell(setup_mocks['context'])
        
        setup_mocks['jqdata'].order_target_value.assert_called_once_with('000001.XSHE', 0)

    def test_sell_keeps_limit_up(self, setup_mocks):
        import factor_test_no_enhance as module
        module.g = setup_mocks['g']
        
        mock_stock = SimpleNamespace()
        mock_stock.last_price = 10.5
        mock_stock.high_limit = 10.5
        setup_mocks['jqdata'].get_current_data.return_value = {'000001.XSHE': mock_stock}
        
        mock_position = SimpleNamespace()
        setup_mocks['context'].portfolio.positions = {'000001.XSHE': mock_position}
        
        module.sell(setup_mocks['context'])
        
        setup_mocks['jqdata'].order_target_value.assert_not_called()

    def test_empty_target_list(self, setup_mocks):
        import factor_test_no_enhance as module
        module.g = setup_mocks['g']
        module.g.target_list = []
        
        module.buy(setup_mocks['context'])
        
        setup_mocks['jqdata'].order_value.assert_not_called()

    def test_filters_68_prefix(self, setup_mocks):
        import factor_test_no_enhance as module
        module.g = setup_mocks['g']
        module.g.ps = 5
        
        mock_securities_df = pd.DataFrame({
            'display_name': ['股票1', '股票2'],
            'start_date': [datetime(2020, 1, 1), datetime(2020, 1, 1)]
        }, index=['000001.XSHE', '688001.XSHG'])
        setup_mocks['jqdata'].get_all_securities.return_value = mock_securities_df
        
        setup_mocks['jqdata'].get_security_info.return_value = SimpleNamespace(
            start_date=datetime(2020, 1, 1)
        )
        
        is_st_df = pd.DataFrame({
            datetime(2024, 1, 15): [False, False]
        }, index=['000001.XSHE', '688001.XSHG'])
        setup_mocks['jqdata'].get_extras.return_value = is_st_df
        
        stock_data = pd.DataFrame({
            'code': ['000001.XSHE'],
            'close': [10.0],
            'high_limit': [10.0]
        })
        setup_mocks['jqdata'].get_price.return_value = stock_data
        
        module.get_stock_list(setup_mocks['context'])
        
        assert '688001.XSHG' not in str(setup_mocks['jqdata'].get_price.call_args)

    def test_filters_4_8_prefix(self, setup_mocks):
        import factor_test_no_enhance as module
        module.g = setup_mocks['g']
        module.g.ps = 5
        
        mock_securities_df = pd.DataFrame({
            'display_name': ['股票1', '股票2', '股票3'],
            'start_date': [datetime(2020, 1, 1), datetime(2020, 1, 1), datetime(2020, 1, 1)]
        }, index=['000001.XSHE', '400001.XSBJ', '800001.XSBJ'])
        setup_mocks['jqdata'].get_all_securities.return_value = mock_securities_df
        
        setup_mocks['jqdata'].get_security_info.return_value = SimpleNamespace(
            start_date=datetime(2020, 1, 1)
        )
        
        is_st_df = pd.DataFrame({
            datetime(2024, 1, 15): [False, False, False]
        }, index=['000001.XSHE', '400001.XSBJ', '800001.XSBJ'])
        setup_mocks['jqdata'].get_extras.return_value = is_st_df
        
        stock_data = pd.DataFrame({
            'code': ['000001.XSHE'],
            'close': [10.0],
            'high_limit': [10.0]
        })
        setup_mocks['jqdata'].get_price.return_value = stock_data
        
        module.get_stock_list(setup_mocks['context'])
        
        setup_mocks['jqdata'].get_price.assert_called()