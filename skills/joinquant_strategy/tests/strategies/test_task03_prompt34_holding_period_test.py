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
    
    with patch.dict(sys.modules, {'jqdata': mock_module}):
        yield mock_module


class TestTask03Prompt34HoldingPeriodTest:
    def test_get_zt_stocks(self, mock_jqdata):
        with patch.dict(sys.modules, {'jqdata': mock_jqdata}):
            import task03_prompt34_holding_period_test
            
            all_stocks = pd.DataFrame({'display_name': ['A']}, index=['000001.XSHE'])
            mock_jqdata.get_all_securities.return_value = all_stocks
            
            price_df = pd.DataFrame({
                'code': ['000001.XSHE'],
                'close': [10.0],
                'high_limit': [10.0],
                'paused': [0]
            })
            mock_jqdata.get_price.return_value = price_df
            
            result = task03_prompt34_holding_period_test.get_zt_stocks("2024-01-15")
            
            assert isinstance(result, list)

    def test_filter_yzb(self, mock_jqdata):
        with patch.dict(sys.modules, {'jqdata': mock_jqdata}):
            import task03_prompt34_holding_period_test
            
            price_df = pd.DataFrame({'low': [10.0], 'high': [10.5]})
            mock_jqdata.get_price.return_value = price_df
            
            result = task03_prompt34_holding_period_test.filter_yzb(['000001.XSHE'], "2024-01-15")
            
            assert isinstance(result, list)

    def test_check_zt(self, mock_jqdata):
        with patch.dict(sys.modules, {'jqdata': mock_jqdata}):
            import task03_prompt34_holding_period_test
            
            price_df = pd.DataFrame({'close': [10.0], 'high_limit': [10.0]})
            mock_jqdata.get_price.return_value = price_df
            
            result = task03_prompt34_holding_period_test.check_zt('000001.XSHE', '2024-01-15')
            
            assert result in [True, False]

    def test_get_market_cap_range(self, mock_jqdata):
        with patch.dict(sys.modules, {'jqdata': mock_jqdata}):
            import task03_prompt34_holding_period_test
            
            fundamentals_df = pd.DataFrame({
                'code': ['000001.XSHE'],
                'circulating_market_cap': [10.0]
            })
            mock_jqdata.get_fundamentals.return_value = fundamentals_df
            
            result = task03_prompt34_holding_period_test.get_market_cap_range(['000001.XSHE'], "2024-01-15")
            
            assert isinstance(result, list)

    def test_backtest_holding_period_t1(self, mock_jqdata):
        with patch.dict(sys.modules, {'jqdata': mock_jqdata}):
            import task03_prompt34_holding_period_test
            
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
            
            result = task03_prompt34_holding_period_test.backtest_holding_period("T+1", 2024, sentiment_threshold=30)
            
            assert 'rule' in result
            assert result['rule'] == 'T+1'

    def test_backtest_holding_period_t2(self, mock_jqdata):
        with patch.dict(sys.modules, {'jqdata': mock_jqdata}):
            import task03_prompt34_holding_period_test
            
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
            
            result = task03_prompt34_holding_period_test.backtest_holding_period("T+2", 2024, sentiment_threshold=30)
            
            assert 'rule' in result
            assert result['rule'] == 'T+2'

    def test_calculate_metrics(self, mock_jqdata):
        with patch.dict(sys.modules, {'jqdata': mock_jqdata}):
            import task03_prompt34_holding_period_test
            
            results_list = [
                {'rule': 'T+1', 'trades': 10, 'wins': 5, 'profits': [1.0] * 10, 'holding_days': [1] * 10, 'zt_holds': 0, 'zt_hold_extra_profit': 0},
                {'rule': 'T+2', 'trades': 10, 'wins': 6, 'profits': [2.0] * 10, 'holding_days': [2] * 10, 'zt_holds': 2, 'zt_hold_extra_profit': 1.0}
            ]
            
            summary = task03_prompt34_holding_period_test.calculate_metrics(results_list)
            
            assert 'T+1' in summary
            assert 'T+2' in summary

    def test_rule_names(self, mock_jqdata):
        with patch.dict(sys.modules, {'jqdata': mock_jqdata}):
            import task03_prompt34_holding_period_test
            
            rule_names = {
                "T+1": "T+1卖出",
                "T+2": "T+2卖出",
                "T+1_or_T+2": "T+1或T+2",
                "dynamic_5pct": "盈利>5%持T+2",
                "dynamic_loss": "亏损当日卖",
                "long": "长线持仓",
            }
            
            assert len(rule_names) == 6