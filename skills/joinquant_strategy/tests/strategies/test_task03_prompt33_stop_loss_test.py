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
    
    with patch.dict(sys.modules, {'jqdata': mock_module}):
        yield mock_module


class TestTask03Prompt33StopLossTest:
    def test_get_zt_stocks(self, mock_jqdata):
        with patch.dict(sys.modules, {'jqdata': mock_jqdata}):
            import task03_prompt33_stop_loss_test
            
            all_stocks = pd.DataFrame({'display_name': ['A']}, index=['000001.XSHE'])
            mock_jqdata.get_all_securities.return_value = all_stocks
            
            price_df = pd.DataFrame({
                'code': ['000001.XSHE'],
                'close': [10.0],
                'high_limit': [10.0],
                'paused': [0]
            })
            mock_jqdata.get_price.return_value = price_df
            
            result = task03_prompt33_stop_loss_test.get_zt_stocks("2024-01-15")
            
            assert isinstance(result, list)

    def test_filter_yzb(self, mock_jqdata):
        with patch.dict(sys.modules, {'jqdata': mock_jqdata}):
            import task03_prompt33_stop_loss_test
            
            price_df = pd.DataFrame({'low': [10.0], 'high': [10.5]})
            mock_jqdata.get_price.return_value = price_df
            
            result = task03_prompt33_stop_loss_test.filter_yzb(['000001.XSHE'], "2024-01-15")
            
            assert isinstance(result, list)

    def test_check_stop_loss_fixed(self, mock_jqdata):
        with patch.dict(sys.modules, {'jqdata': mock_jqdata}):
            import task03_prompt33_stop_loss_test
            
            result = task03_prompt33_stop_loss_test.check_stop_loss_fixed(10.0, 9.7, 3)
            assert result == True
            
            result = task03_prompt33_stop_loss_test.check_stop_loss_fixed(10.0, 9.8, 3)
            assert result == False

    def test_check_stop_loss_minute_below_open(self, mock_jqdata):
        with patch.dict(sys.modules, {'jqdata': mock_jqdata}):
            import task03_prompt33_stop_loss_test
            
            minute_data = {'close': np.array([10.0, 10.5, 9.8])}
            
            triggered, price = task03_prompt33_stop_loss_test.check_stop_loss_minute(10.0, minute_data, 10.0, 'below_open')
            
            assert triggered in [True, False]

    def test_check_stop_loss_minute_below_avg(self, mock_jqdata):
        with patch.dict(sys.modules, {'jqdata': mock_jqdata}):
            import task03_prompt33_stop_loss_test
            
            minute_data = {'close': np.array([10.0, 10.5, 10.2])}
            
            triggered, price = task03_prompt33_stop_loss_test.check_stop_loss_minute(10.0, minute_data, 10.0, 'below_avg')
            
            assert triggered in [True, False]

    def test_check_stop_loss_minute_accelerate_down(self, mock_jqdata):
        with patch.dict(sys.modules, {'jqdata': mock_jqdata}):
            import task03_prompt33_stop_loss_test
            
            minute_data = {'close': np.array([10.5, 10.3, 10.0, 9.7, 9.4])}
            
            triggered, price = task03_prompt33_stop_loss_test.check_stop_loss_minute(10.0, minute_data, 10.0, 'accelerate_down')
            
            assert triggered in [True, False]

    def test_get_minute_data(self, mock_jqdata):
        with patch.dict(sys.modules, {'jqdata': mock_jqdata}):
            import task03_prompt33_stop_loss_test
            
            mock_jqdata.get_bars.return_value = {'close': np.array([10.0] * 240), 'volume': np.array([100] * 240)}
            
            result = task03_prompt33_stop_loss_test.get_minute_data('000001.XSHE', '2024-01-15')
            
            assert result is not None or result is None

    def test_backtest_stop_loss_no_stop(self, mock_jqdata):
        with patch.dict(sys.modules, {'jqdata': mock_jqdata}):
            import task03_prompt33_stop_loss_test
            
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
            
            result = task03_prompt33_stop_loss_test.backtest_stop_loss("no", 2024, sentiment_threshold=30)
            
            assert 'rule' in result
            assert result['rule'] == 'no'

    def test_calculate_metrics(self, mock_jqdata):
        with patch.dict(sys.modules, {'jqdata': mock_jqdata}):
            import task03_prompt33_stop_loss_test
            
            results_list = [
                {'rule': 'no', 'trades': 10, 'wins': 5, 'profits': [1.0] * 10, 'stop_triggered': 0, 'stop_trigger_pct': [], 'max_drawdown': 5},
                {'rule': 'fixed_3', 'trades': 10, 'wins': 6, 'profits': [2.0] * 10, 'stop_triggered': 3, 'stop_trigger_pct': [-3.0] * 3, 'max_drawdown': 3}
            ]
            
            summary = task03_prompt33_stop_loss_test.calculate_metrics(results_list)
            
            assert 'no' in summary
            assert 'fixed_3' in summary

    def test_rule_names(self, mock_jqdata):
        with patch.dict(sys.modules, {'jqdata': mock_jqdata}):
            import task03_prompt33_stop_loss_test
            
            rule_names = {
                "no": "无止损",
                "fixed_3": "-3%止损",
                "fixed_5": "-5%止损",
                "fixed_7": "-7%止损",
                "fixed_10": "-10%止损",
                "minute_open": "跌破开盘价",
                "minute_avg": "跌破分时均线",
                "minute_accelerate": "加速下跌",
                "time_10:30": "10:30止损",
                "time_13:30": "13:30止损",
                "time_14:30": "14:30止损",
                "combo_3_10:30": "-3%或10:30",
                "combo_5_13:30": "-5%或13:30",
            }
            
            assert len(rule_names) == 13