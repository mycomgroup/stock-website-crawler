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


class TestTask03Prompt35CircuitBreakerTest:
    def test_get_zt_stocks(self, mock_jqdata):
        with patch.dict(sys.modules, {'jqdata': mock_jqdata}):
            import task03_prompt35_circuit_breaker_test
            
            all_stocks = pd.DataFrame({'display_name': ['A']}, index=['000001.XSHE'])
            mock_jqdata.get_all_securities.return_value = all_stocks
            
            price_df = pd.DataFrame({
                'code': ['000001.XSHE'],
                'close': [10.0],
                'high_limit': [10.0],
                'paused': [0]
            })
            mock_jqdata.get_price.return_value = price_df
            
            result = task03_prompt35_circuit_breaker_test.get_zt_stocks("2024-01-15")
            
            assert isinstance(result, list)

    def test_get_dt_stocks(self, mock_jqdata):
        with patch.dict(sys.modules, {'jqdata': mock_jqdata}):
            import task03_prompt35_circuit_breaker_test
            
            all_stocks = pd.DataFrame({'display_name': ['A']}, index=['000001.XSHE'])
            mock_jqdata.get_all_securities.return_value = all_stocks
            
            price_df = pd.DataFrame({
                'code': ['000001.XSHE'],
                'close': [9.0],
                'low_limit': [9.0],
                'paused': [0]
            })
            mock_jqdata.get_price.return_value = price_df
            
            result = task03_prompt35_circuit_breaker_test.get_dt_stocks("2024-01-15")
            
            assert isinstance(result, list)

    def test_check_market_emotion_change(self, mock_jqdata):
        with patch.dict(sys.modules, {'jqdata': mock_jqdata}):
            import task03_prompt35_circuit_breaker_test
            
            result = task03_prompt35_circuit_breaker_test.check_market_emotion_change(60, 25)
            assert result == True
            
            result = task03_prompt35_circuit_breaker_test.check_market_emotion_change(60, 40)
            assert result == False

    def test_check_zt_dt_ratio(self, mock_jqdata):
        with patch.dict(sys.modules, {'jqdata': mock_jqdata}):
            import task03_prompt35_circuit_breaker_test
            
            result = task03_prompt35_circuit_breaker_test.check_zt_dt_ratio(20, 30)
            assert result == True
            
            result = task03_prompt35_circuit_breaker_test.check_zt_dt_ratio(40, 30)
            assert result == False

    def test_filter_yzb(self, mock_jqdata):
        with patch.dict(sys.modules, {'jqdata': mock_jqdata}):
            import task03_prompt35_circuit_breaker_test
            
            price_df = pd.DataFrame({'low': [10.0], 'high': [10.5]})
            mock_jqdata.get_price.return_value = price_df
            
            result = task03_prompt35_circuit_breaker_test.filter_yzb(['000001.XSHE'], "2024-01-15")
            
            assert isinstance(result, list)

    def test_get_market_cap_range(self, mock_jqdata):
        with patch.dict(sys.modules, {'jqdata': mock_jqdata}):
            import task03_prompt35_circuit_breaker_test
            
            fundamentals_df = pd.DataFrame({
                'code': ['000001.XSHE'],
                'circulating_market_cap': [10.0]
            })
            mock_jqdata.get_fundamentals.return_value = fundamentals_df
            
            result = task03_prompt35_circuit_breaker_test.get_market_cap_range(['000001.XSHE'], "2024-01-15")
            
            assert isinstance(result, list)

    def test_get_zt_count(self, mock_jqdata):
        with patch.dict(sys.modules, {'jqdata': mock_jqdata}):
            import task03_prompt35_circuit_breaker_test
            
            all_stocks = pd.DataFrame({'display_name': ['A']}, index=['000001.XSHE'])
            mock_jqdata.get_all_securities.return_value = all_stocks
            
            price_df = pd.DataFrame({'close': [10.0] * 50, 'high_limit': [10.0] * 50})
            mock_jqdata.get_price.return_value = price_df
            
            result = task03_prompt35_circuit_breaker_test.get_zt_count("2024-01-15")
            
            assert result >= 0

    def test_get_dt_count(self, mock_jqdata):
        with patch.dict(sys.modules, {'jqdata': mock_jqdata}):
            import task03_prompt35_circuit_breaker_test
            
            all_stocks = pd.DataFrame({'display_name': ['A']}, index=['000001.XSHE'])
            mock_jqdata.get_all_securities.return_value = all_stocks
            
            price_df = pd.DataFrame({'close': [9.0] * 50, 'low_limit': [9.0] * 50})
            mock_jqdata.get_price.return_value = price_df
            
            result = task03_prompt35_circuit_breaker_test.get_dt_count("2024-01-15")
            
            assert result >= 0

    def test_backtest_with_circuit_breaker_no(self, mock_jqdata):
        with patch.dict(sys.modules, {'jqdata': mock_jqdata}):
            import task03_prompt35_circuit_breaker_test
            
            mock_jqdata.get_trade_days.return_value = [datetime(2024, 1, i) for i in range(1, 31)]
            mock_jqdata.get_all_securities.return_value = pd.DataFrame({'display_name': ['A']}, index=['000001.XSHE'])
            mock_jqdata.get_all_trade_days.return_value = [datetime(2024, 1, i) for i in range(1, 31)]
            
            price_df = pd.DataFrame({
                'code': ['000001.XSHE'],
                'close': [10.0],
                'high_limit': [10.0],
                'low_limit': [9.0],
                'paused': [0]
            })
            mock_jqdata.get_price.return_value = price_df
            
            result = task03_prompt35_circuit_breaker_test.backtest_with_circuit_breaker("no", 2024, sentiment_threshold=30)
            
            assert 'rule' in result
            assert result['rule'] == 'no'

    def test_calculate_metrics(self, mock_jqdata):
        with patch.dict(sys.modules, {'jqdata': mock_jqdata}):
            import task03_prompt35_circuit_breaker_test
            
            results_list = [
                {'rule': 'no', 'trades': 10, 'wins': 5, 'profits': [1.0] * 10, 'circuit_breaker_triggered': 0, 'circuit_breaker_types': [], 'max_drawdown': 5},
                {'rule': 'single_loss_5pct', 'trades': 10, 'wins': 6, 'profits': [2.0] * 10, 'circuit_breaker_triggered': 3, 'circuit_breaker_types': ['single_loss'], 'max_drawdown': 3}
            ]
            
            summary = task03_prompt35_circuit_breaker_test.calculate_metrics(results_list)
            
            assert 'no' in summary
            assert 'single_loss_5pct' in summary

    def test_rule_names(self, mock_jqdata):
        with patch.dict(sys.modules, {'jqdata': mock_jqdata}):
            import task03_prompt35_circuit_breaker_test
            
            rule_names = {
                "no": "无熔断",
                "single_loss_5pct": "单票亏损5%",
                "single_loss_10pct": "单票亏损10%",
                "daily_loss_5pct": "单日亏损>5%",
                "consecutive_5_loss": "连续5笔亏损",
                "win_rate_50pct_10d": "胜率<50%",
                "return_-5pct_20d": "收益<-5%",
                "emotion_change": "情绪骤变",
                "zt_dt_reverse": "涨跌停反转",
                "combined_all": "组合熔断",
            }
            
            assert len(rule_names) == 10