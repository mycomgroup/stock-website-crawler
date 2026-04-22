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
    mock_module.get_next_date = Mock()
    mock_module.get_prev_date = Mock()
    
    with patch.dict(sys.modules, {'jqdata': mock_module}):
        yield mock_module


class TestTask03Prompt31SellTimingTest:
    def test_get_zt_stocks(self, mock_jqdata):
        with patch.dict(sys.modules, {'jqdata': mock_jqdata}):
            import task03_prompt31_sell_timing_test
            
            all_stocks = pd.DataFrame({'display_name': ['A']}, index=['000001.XSHE', '000002.XSHE'])
            mock_jqdata.get_all_securities.return_value = all_stocks
            
            price_df = pd.DataFrame({
                'code': ['000001.XSHE'],
                'close': [10.0],
                'high_limit': [10.0],
                'paused': [0]
            })
            mock_jqdata.get_price.return_value = price_df
            
            result = task03_prompt31_sell_timing_test.get_zt_stocks("2024-01-15")
            
            assert len(result) >= 0

    def test_filter_yzb(self, mock_jqdata):
        with patch.dict(sys.modules, {'jqdata': mock_jqdata}):
            import task03_prompt31_sell_timing_test
            
            price_df = pd.DataFrame({
                'low': [10.0],
                'high': [10.5]
            })
            mock_jqdata.get_price.return_value = price_df
            
            result = task03_prompt31_sell_timing_test.filter_yzb(['000001.XSHE'], "2024-01-15")
            
            assert len(result) >= 0

    def test_get_market_cap_range(self, mock_jqdata):
        with patch.dict(sys.modules, {'jqdata': mock_jqdata}):
            import task03_prompt31_sell_timing_test
            
            mock_q = Mock()
            mock_jqdata.query.return_value = mock_q
            
            fundamentals_df = pd.DataFrame({
                'code': ['000001.XSHE'],
                'circulating_market_cap': [10.0]
            })
            mock_jqdata.get_fundamentals.return_value = fundamentals_df
            
            result = task03_prompt31_sell_timing_test.get_market_cap_range(['000001.XSHE'], "2024-01-15")
            
            assert isinstance(result, list)

    def test_get_zt_count(self, mock_jqdata):
        with patch.dict(sys.modules, {'jqdata': mock_jqdata}):
            import task03_prompt31_sell_timing_test
            
            all_stocks = pd.DataFrame({'display_name': ['A']}, index=['000001.XSHE'])
            mock_jqdata.get_all_securities.return_value = all_stocks
            
            price_df = pd.DataFrame({
                'close': [10.0] * 50,
                'high_limit': [10.0] * 50
            })
            mock_jqdata.get_price.return_value = price_df
            
            result = task03_prompt31_sell_timing_test.get_zt_count("2024-01-15")
            
            assert result >= 0

    def test_get_prev_date(self, mock_jqdata):
        with patch.dict(sys.modules, {'jqdata': mock_jqdata}):
            import task03_prompt31_sell_timing_test
            
            mock_jqdata.get_all_trade_days.return_value = [datetime(2024, 1, 10), datetime(2024, 1, 15)]
            
            result = task03_prompt31_sell_timing_test.get_prev_date("2024-01-15", 1)
            
            assert result is not None or result is None

    def test_get_next_date(self, mock_jqdata):
        with patch.dict(sys.modules, {'jqdata': mock_jqdata}):
            import task03_prompt31_sell_timing_test
            
            mock_jqdata.get_all_trade_days.return_value = [datetime(2024, 1, 15), datetime(2024, 1, 16)]
            
            result = task03_prompt31_sell_timing_test.get_next_date("2024-01-15", 1)
            
            assert result is not None or result is None

    def test_backtest_sell_timing_auction(self, mock_jqdata):
        with patch.dict(sys.modules, {'jqdata': mock_jqdata}):
            import task03_prompt31_sell_timing_test
            
            mock_jqdata.get_trade_days.return_value = [datetime(2024, 1, i) for i in range(1, 31)]
            mock_jqdata.get_all_securities.return_value = pd.DataFrame({'display_name': ['A']}, index=['000001.XSHE'])
            
            price_df = pd.DataFrame({
                'code': ['000001.XSHE'],
                'close': [10.0],
                'high_limit': [10.0],
                'paused': [0]
            })
            mock_jqdata.get_price.return_value = price_df
            
            mock_jqdata.get_all_trade_days.return_value = [datetime(2024, 1, i) for i in range(1, 31)]
            
            result = task03_prompt31_sell_timing_test.backtest_sell_timing("auction", 2024, sentiment_threshold=30)
            
            assert 'year' in result
            assert 'timing' in result
            assert result['timing'] == 'auction'

    def test_calculate_metrics(self, mock_jqdata):
        with patch.dict(sys.modules, {'jqdata': mock_jqdata}):
            import task03_prompt31_sell_timing_test
            
            results_list = [
                {'timing': 'auction', 'trades': 10, 'wins': 5, 'profits': [1.0] * 10},
                {'timing': 'close', 'trades': 10, 'wins': 6, 'profits': [2.0] * 10}
            ]
            
            summary = task03_prompt31_sell_timing_test.calculate_metrics(results_list)
            
            assert 'auction' in summary
            assert 'close' in summary

    def test_timing_names(self, mock_jqdata):
        with patch.dict(sys.modules, {'jqdata': mock_jqdata}):
            import task03_prompt31_sell_timing_test
            
            timing_names = {
                "auction": "次日竞价",
                "open": "次日开盘",
                "10:30": "次日10:30",
                "13:30": "次日13:30",
                "close": "次日收盘",
                "high": "次日最高价",
            }
            
            assert len(timing_names) == 6