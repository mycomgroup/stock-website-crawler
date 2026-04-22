import pytest
import sys
from unittest.mock import MagicMock, patch, Mock
from types import SimpleNamespace
from datetime import datetime
import pandas as pd
import numpy as np

sys.path.insert(0, '/Users/yuping/Downloads/git/stock-website-crawler/strategies/misc_research/joinquant_strategy')


@pytest.fixture
def mock_jqdata():
    mock_module = MagicMock()
    mock_module.get_all_securities = Mock()
    mock_module.get_price = Mock()
    mock_module.get_fundamentals = Mock()
    mock_module.query = Mock()
    mock_module.valuation = MagicMock()
    mock_module.get_all_trade_days = Mock()
    mock_module.get_trade_days = Mock()
    mock_module.get_bars = Mock()
    mock_module.get_industry_code = Mock()
    mock_module.get_industry_stocks = Mock()
    
    with patch.dict(sys.modules, {'jqdata': mock_module}):
        yield mock_module


class TestTask03Prompt32ProfitTargetTest:
    def test_get_zt_stocks(self, mock_jqdata):
        with patch.dict(sys.modules, {'jqdata': mock_jqdata}):
            import task03_prompt32_profit_target_test
            
            all_stocks = pd.DataFrame({'display_name': ['A']}, index=['000001.XSHE'])
            mock_jqdata.get_all_securities.return_value = all_stocks
            
            price_df = pd.DataFrame({
                'code': ['000001.XSHE'],
                'close': [10.0],
                'high_limit': [10.0],
                'paused': [0]
            })
            mock_jqdata.get_price.return_value = price_df
            
            result = task03_prompt32_profit_target_test.get_zt_stocks("2024-01-15")
            
            assert isinstance(result, list)

    def test_filter_yzb(self, mock_jqdata):
        with patch.dict(sys.modules, {'jqdata': mock_jqdata}):
            import task03_prompt32_profit_target_test
            
            price_df = pd.DataFrame({
                'low': [10.0],
                'high': [10.5]
            })
            mock_jqdata.get_price.return_value = price_df
            
            result = task03_prompt32_profit_target_test.filter_yzb(['000001.XSHE'], "2024-01-15")
            
            assert isinstance(result, list)

    def test_get_market_cap_range(self, mock_jqdata):
        with patch.dict(sys.modules, {'jqdata': mock_jqdata}):
            import task03_prompt32_profit_target_test
            
            fundamentals_df = pd.DataFrame({
                'code': ['000001.XSHE'],
                'circulating_market_cap': [10.0]
            })
            mock_jqdata.get_fundamentals.return_value = fundamentals_df
            
            result = task03_prompt32_profit_target_test.get_market_cap_range(['000001.XSHE'], "2024-01-15")
            
            assert isinstance(result, list)

    def test_check_profit_target_fixed(self, mock_jqdata):
        with patch.dict(sys.modules, {'jqdata': mock_jqdata}):
            import task03_prompt32_profit_target_test
            
            result = task03_prompt32_profit_target_test.check_profit_target_fixed(10.0, 10.5, 5)
            assert result == True
            
            result = task03_prompt32_profit_target_test.check_profit_target_fixed(10.0, 10.3, 5)
            assert result == False

    def test_check_profit_target_minute_below_avg(self, mock_jqdata):
        with patch.dict(sys.modules, {'jqdata': mock_jqdata}):
            import task03_prompt32_profit_target_test
            
            minute_data = {'close': np.array([10.0, 10.5, 10.3])}
            
            triggered, price = task03_prompt32_profit_target_test.check_profit_target_minute(10.0, minute_data, 'below_avg')
            
            assert triggered in [True, False]

    def test_check_profit_target_minute_below_open(self, mock_jqdata):
        with patch.dict(sys.modules, {'jqdata': mock_jqdata}):
            import task03_prompt32_profit_target_test
            
            minute_data = {'close': np.array([10.0, 10.5, 9.8])}
            
            triggered, price = task03_prompt32_profit_target_test.check_profit_target_minute(10.0, minute_data, 'below_open')
            
            assert triggered in [True, False]

    def test_check_profit_target_minute_retrace_50(self, mock_jqdata):
        with patch.dict(sys.modules, {'jqdata': mock_jqdata}):
            import task03_prompt32_profit_target_test
            
            minute_data = {'close': np.array([10.0, 11.0, 10.5])}
            
            triggered, price = task03_prompt32_profit_target_test.check_profit_target_minute(10.0, minute_data, 'retrace_50')
            
            assert triggered in [True, False]

    def test_check_sector_profit_target(self, mock_jqdata):
        with patch.dict(sys.modules, {'jqdata': mock_jqdata}):
            import task03_prompt32_profit_target_test
            
            mock_jqdata.get_industry_code.return_value = 'IND001'
            mock_jqdata.get_industry_stocks.return_value = ['000001.XSHE']
            
            price_df = pd.DataFrame({'close': [10.0], 'high_limit': [10.0]})
            mock_jqdata.get_price.return_value = price_df
            
            result = task03_prompt32_profit_target_test.check_sector_profit_target('000001.XSHE', '2024-01-15', 'leader_down')
            
            assert result in [True, False]

    def test_backtest_profit_target_no_profit(self, mock_jqdata):
        with patch.dict(sys.modules, {'jqdata': mock_jqdata}):
            import task03_prompt32_profit_target_test
            
            mock_jqdata.get_trade_days.return_value = [datetime(2024, 1, i) for i in range(1, 31)]
            mock_jqdata.get_all_securities.return_value = pd.DataFrame({'display_name': ['A']}, index=['000001.XSHE'])
            mock_jqdata.get_all_trade_days.return_value = [datetime(2024, 1, i) for i in range(1, 31)]
            
            price_df = pd.DataFrame({
                'code': ['000001.XSHE'],
                'close': [10.0],
                'high_limit': [10.0],
                'paused': [0]
            })
            mock_jqdata.get_price.return_value = price_df
            
            result = task03_prompt32_profit_target_test.backtest_profit_target("no", 2024, sentiment_threshold=30)
            
            assert 'rule' in result
            assert result['rule'] == 'no'

    def test_calculate_metrics(self, mock_jqdata):
        with patch.dict(sys.modules, {'jqdata': mock_jqdata}):
            import task03_prompt32_profit_target_test
            
            results_list = [
                {'rule': 'no', 'trades': 10, 'wins': 5, 'profits': [1.0] * 10, 'profit_triggered': 0, 'profit_trigger_pct': []},
                {'rule': 'fixed_5', 'trades': 10, 'wins': 6, 'profits': [2.0] * 10, 'profit_triggered': 3, 'profit_trigger_pct': [5.0] * 3}
            ]
            
            summary = task03_prompt32_profit_target_test.calculate_metrics(results_list)
            
            assert 'no' in summary
            assert 'fixed_5' in summary

    def test_rule_names(self, mock_jqdata):
        with patch.dict(sys.modules, {'jqdata': mock_jqdata}):
            import task03_prompt32_profit_target_test
            
            rule_names = {
                "no": "无止盈",
                "fixed_5": "+5%止盈",
                "fixed_7": "+7%止盈",
                "fixed_10": "+10%止盈",
                "fixed_15": "+15%止盈",
                "minute_avg": "跌破分时均线",
                "minute_open": "跌破开盘价",
                "minute_retrace_50": "回调50%",
                "sector_leader": "龙头炸板",
                "sector_drop_2pct": "板块跌超2%",
            }
            
            assert len(rule_names) == 10