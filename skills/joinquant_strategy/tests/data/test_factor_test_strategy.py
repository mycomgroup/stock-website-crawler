import pytest
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from unittest.mock import MagicMock, patch
from types import SimpleNamespace
import sys

sys.path.insert(0, '/Users/yuping/Downloads/git/stock-website-crawler/skills/joinquant_strategy/data')


class TestFactorTestStrategy:
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
        import factor_test_strategy as module
        module.g = setup_mocks['g']
        
        module.initialize(setup_mocks['context'])
        
        setup_mocks['jqdata'].set_option.assert_any_call("use_real_price", True)
        assert setup_mocks['g'].test_mode == "double_factor"

    def test_initialize_modes(self, setup_mocks):
        import factor_test_strategy as module
        module.g = setup_mocks['g']
        
        modes = ['no_enhance', 'single_factor', 'double_factor', 'multi_factor']
        for mode in modes:
            module.g.test_mode = mode
            module.initialize(setup_mocks['context'])
            assert module.g.test_mode == mode

    def test_get_stock_list_no_enhance_mode(self, setup_mocks):
        import factor_test_strategy as module
        module.g = setup_mocks['g']
        module.g.test_mode = "no_enhance"
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
            'high_limit': [10.0, 20.0, 30.0]
        })
        setup_mocks['jqdata'].get_price.return_value = stock_data
        
        module.get_stock_list(setup_mocks['context'])
        
        assert len(module.g.target_list) <= 5

    def test_get_stock_list_single_factor_mode(self, setup_mocks):
        import factor_test_strategy as module
        module.g = setup_mocks['g']
        module.g.test_mode = "single_factor"
        module.g.max_cap = 50
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
            'high_limit': [10.0, 20.0, 30.0]
        })
        setup_mocks['jqdata'].get_price.return_value = stock_data
        
        cap_data = pd.DataFrame({
            'code': ['000001.XSHE', '000002.XSHE', '000003.XSHE'],
            'circulating_market_cap': [20.0, 40.0, 60.0]
        })
        setup_mocks['jqdata'].get_fundamentals.return_value = cap_data
        
        module.get_stock_list(setup_mocks['context'])
        
        setup_mocks['jqdata'].get_fundamentals.assert_called()
        assert '000003.XSHE' not in module.g.target_list

    def test_get_stock_list_double_factor_mode(self, setup_mocks):
        import factor_test_strategy as module
        module.g = setup_mocks['g']
        module.g.test_mode = "double_factor"
        module.g.max_cap = 50
        module.g.max_turnover = 30
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
            datetime(2024, 1, 15): [False, False]
        }, index=['000001.XSHE', '000002.XSHE'])
        setup_mocks['jqdata'].get_extras.return_value = is_st_df
        
        stock_data = pd.DataFrame({
            'code': ['000001.XSHE', '000002.XSHE'],
            'close': [10.0, 20.0],
            'high_limit': [10.0, 20.0]
        })
        setup_mocks['jqdata'].get_price.return_value = stock_data
        
        cap_data = pd.DataFrame({
            'code': ['000001.XSHE', '000002.XSHE'],
            'circulating_market_cap': [20.0, 40.0]
        })
        setup_mocks['jqdata'].get_fundamentals.return_value = cap_data
        
        setup_mocks['jqlib'].HSL.return_value = [{'000001.XSHE': 20.0, '000002.XSHE': 35.0}]
        
        module.get_stock_list(setup_mocks['context'])
        
        setup_mocks['jqlib'].HSL.assert_called()
        assert '000002.XSHE' not in module.g.target_list

    def test_get_stock_list_multi_factor_mode(self, setup_mocks):
        import factor_test_strategy as module
        module.g = setup_mocks['g']
        module.g.test_mode = "multi_factor"
        module.g.max_cap = 50
        module.g.max_turnover = 30
        module.g.ps = 3
        
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
            'high_limit': [10.0, 20.0, 30.0]
        })
        setup_mocks['jqdata'].get_price.return_value = stock_data
        
        cap_data = pd.DataFrame({
            'code': ['000001.XSHE', '000002.XSHE', '000003.XSHE'],
            'circulating_market_cap': [20.0, 40.0, 30.0]
        })
        setup_mocks['jqdata'].get_fundamentals.return_value = cap_data
        
        setup_mocks['jqlib'].HSL.return_value = [{'000001.XSHE': 20.0, '000002.XSHE': 25.0, '000003.XSHE': 15.0}]
        
        module.get_stock_list(setup_mocks['context'])
        
        assert len(module.g.target_list) <= 3

    def test_filter_by_market_cap(self, setup_mocks):
        import factor_test_strategy as module
        
        cap_data = pd.DataFrame({
            'code': ['000001.XSHE', '000002.XSHE', '000003.XSHE'],
            'circulating_market_cap': [20.0, 40.0, 60.0]
        })
        setup_mocks['jqdata'].get_fundamentals.return_value = cap_data
        
        result = module.filter_by_market_cap(['000001.XSHE', '000002.XSHE', '000003.XSHE'], '2024-01-15', 50)
        
        assert '000001.XSHE' in result
        assert '000002.XSHE' in result
        assert '000003.XSHE' not in result

    def test_filter_by_market_cap_empty_list(self, setup_mocks):
        import factor_test_strategy as module
        
        result = module.filter_by_market_cap([], '2024-01-15', 50)
        
        assert result == []

    def test_filter_by_turnover(self, setup_mocks):
        import factor_test_strategy as module
        
        setup_mocks['jqlib'].HSL.return_value = [{'000001.XSHE': 20.0, '000002.XSHE': 35.0}]
        
        result = module.filter_by_turnover(['000001.XSHE', '000002.XSHE'], '2024-01-15', 30)
        
        assert '000001.XSHE' in result
        assert '000002.XSHE' not in result

    def test_filter_by_turnover_empty_list(self, setup_mocks):
        import factor_test_strategy as module
        
        result = module.filter_by_turnover([], '2024-01-15', 30)
        
        assert result == []

    def test_filter_by_turnover_handles_exception(self, setup_mocks):
        import factor_test_strategy as module
        
        setup_mocks['jqlib'].HSL.side_effect = Exception("HSL error")
        
        result = module.filter_by_turnover(['000001.XSHE'], '2024-01-15', 30)
        
        assert result == []

    def test_sort_by_multi_factors(self, setup_mocks):
        import factor_test_strategy as module
        
        cap_data_small = pd.DataFrame({'circulating_market_cap': [20.0]}, index=['000001.XSHE'])
        cap_data_medium = pd.DataFrame({'circulating_market_cap': [40.0]}, index=['000002.XSHE'])
        cap_data_large = pd.DataFrame({'circulating_market_cap': [30.0]}, index=['000003.XSHE'])
        
        def mock_get_fundamentals(q, date):
            if hasattr(q, 'filter'):
                code = '000001.XSHE'
                if '000001' in str(q):
                    return cap_data_small
                elif '000002' in str(q):
                    return cap_data_medium
                elif '000003' in str(q):
                    return cap_data_large
            return cap_data_small
        
        setup_mocks['jqdata'].get_fundamentals.side_effect = mock_get_fundamentals
        
        setup_mocks['jqlib'].HSL.return_value = [{'000001.XSHE': 15.0, '000002.XSHE': 25.0, '000003.XSHE': 20.0}]
        
        result = module.sort_by_multi_factors(['000001.XSHE', '000002.XSHE', '000003.XSHE'], '2024-01-15')
        
        assert len(result) == 3
        assert result[0] in ['000001.XSHE', '000002.XSHE', '000003.XSHE']

    def test_sort_by_multi_factors_empty_list(self, setup_mocks):
        import factor_test_strategy as module
        
        result = module.sort_by_multi_factors([], '2024-01-15')
        
        assert result == []

    def test_sort_by_multi_factors_handles_exception(self, setup_mocks):
        import factor_test_strategy as module
        
        setup_mocks['jqdata'].get_fundamentals.side_effect = Exception("error")
        setup_mocks['jqlib'].HSL.side_effect = Exception("error")
        
        result = module.sort_by_multi_factors(['000001.XSHE'], '2024-01-15')
        
        assert len(result) == 1

    def test_buy(self, setup_mocks):
        import factor_test_strategy as module
        module.g = setup_mocks['g']
        module.g.target_list = ['000001.XSHE', '000002.XSHE']
        setup_mocks['context'].portfolio.available_cash = 100000
        setup_mocks['context'].portfolio.total_value = 100000
        
        mock_stock = SimpleNamespace()
        mock_stock.last_price = 10.0
        mock_stock.high_limit = 10.5
        setup_mocks['jqdata'].get_current_data.return_value = {'000001.XSHE': mock_stock, '000002.XSHE': mock_stock}
        
        module.buy(setup_mocks['context'])
        
        assert setup_mocks['jqdata'].order_value.call_count == 2

    def test_buy_insufficient_cash(self, setup_mocks):
        import factor_test_strategy as module
        module.g = setup_mocks['g']
        module.g.target_list = ['000001.XSHE', '000002.XSHE']
        setup_mocks['context'].portfolio.available_cash = 50
        
        module.buy(setup_mocks['context'])
        
        setup_mocks['jqdata'].order_value.assert_not_called()

    def test_sell(self, setup_mocks):
        import factor_test_strategy as module
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
        import factor_test_strategy as module
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
        import factor_test_strategy as module
        module.g = setup_mocks['g']
        module.g.target_list = []
        
        module.buy(setup_mocks['context'])
        
        setup_mocks['jqdata'].order_value.assert_not_called()

    def test_score_calculation(self, setup_mocks):
        import factor_test_strategy as module
        
        cap_data = pd.DataFrame({'circulating_market_cap': [25.0]}, index=['000001.XSHE'])
        setup_mocks['jqdata'].get_fundamentals.return_value = cap_data
        setup_mocks['jqlib'].HSL.return_value = [{'000001.XSHE': 15.0}]
        
        result = module.sort_by_multi_factors(['000001.XSHE'], '2024-01-15')
        
        assert len(result) == 1
        assert result[0] == '000001.XSHE'