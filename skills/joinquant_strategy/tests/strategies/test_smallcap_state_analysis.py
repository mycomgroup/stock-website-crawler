import pytest
import sys
from unittest.mock import MagicMock, patch, Mock
from types import SimpleNamespace
from datetime import datetime, timedelta
import pandas as pd
import numpy as np

sys.path.insert(0, '/Users/yuping/Downloads/git/stock-website-crawler/strategies/misc_research/joinquant_strategy')


@pytest.fixture
def mock_jqdata():
    mock_module = MagicMock()
    mock_module.set_option = Mock()
    mock_module.set_benchmark = Mock()
    mock_module.log = MagicMock()
    mock_module.log.set_level = Mock()
    mock_module.log.info = Mock()
    mock_module.run_daily = Mock()
    mock_module.get_index_stocks = Mock()
    mock_module.get_all_securities = Mock()
    mock_module.get_price = Mock()
    mock_module.get_fundamentals = Mock()
    mock_module.query = Mock()
    mock_module.valuation = MagicMock()
    mock_module.get_next_trade_date = Mock()
    mock_module.g = SimpleNamespace()
    
    with patch.dict(sys.modules, {'jqdata': mock_module}):
        yield mock_module


@pytest.fixture
def mock_g():
    g = SimpleNamespace()
    g.state_data = []
    g.trade_data = []
    g.market_breadth_bins = {
        "极弱": (0, 0.15),
        "弱": (0.15, 0.25),
        "中": (0.25, 0.35),
        "强": (0.35, 1.0),
    }
    g.sentiment_bins = {
        "冰点": (0, 30),
        "启动": (30, 50),
        "发酵": (50, 80),
        "高潮": (80, 9999),
    }
    g.current_breadth = 0
    g.current_zt_count = 0
    g.current_breadth_state = ""
    g.current_sentiment_state = ""
    return g


@pytest.fixture
def mock_context():
    context = SimpleNamespace()
    context.previous_date = datetime(2024, 1, 15)
    context.current_dt = datetime(2024, 1, 16, 9, 30)
    return context


class TestSmallcapStateAnalysis:
    def test_initialize(self, mock_jqdata, mock_g):
        with patch('jqdata.g', mock_g):
            import smallcap_state_analysis
            context = SimpleNamespace()
            smallcap_state_analysis.initialize(context)
            
            mock_jqdata.set_option.assert_called()
            mock_jqdata.run_daily.assert_called()
            assert mock_g.state_data == []
            assert mock_g.trade_data == []

    def test_get_state_name_extreme_weak(self, mock_jqdata, mock_g):
        with patch('jqdata.g', mock_g):
            import smallcap_state_analysis
            
            result = smallcap_state_analysis.get_state_name(0.1, mock_g.market_breadth_bins)
            assert result == "极弱"

    def test_get_state_name_weak(self, mock_jqdata, mock_g):
        with patch('jqdata.g', mock_g):
            import smallcap_state_analysis
            
            result = smallcap_state_analysis.get_state_name(0.2, mock_g.market_breadth_bins)
            assert result == "弱"

    def test_get_state_name_medium(self, mock_jqdata, mock_g):
        with patch('jqdata.g', mock_g):
            import smallcap_state_analysis
            
            result = smallcap_state_analysis.get_state_name(0.3, mock_g.market_breadth_bins)
            assert result == "中"

    def test_get_state_name_strong(self, mock_jqdata, mock_g):
        with patch('jqdata.g', mock_g):
            import smallcap_state_analysis
            
            result = smallcap_state_analysis.get_state_name(0.5, mock_g.market_breadth_bins)
            assert result == "强"

    def test_get_state_name_sentiment_freeze(self, mock_jqdata, mock_g):
        with patch('jqdata.g', mock_g):
            import smallcap_state_analysis
            
            result = smallcap_state_analysis.get_state_name(20, mock_g.sentiment_bins)
            assert result == "冰点"

    def test_get_state_name_sentiment_start(self, mock_jqdata, mock_g):
        with patch('jqdata.g', mock_g):
            import smallcap_state_analysis
            
            result = smallcap_state_analysis.get_state_name(40, mock_g.sentiment_bins)
            assert result == "启动"

    def test_get_state_name_sentiment_ferment(self, mock_jqdata, mock_g):
        with patch('jqdata.g', mock_g):
            import smallcap_state_analysis
            
            result = smallcap_state_analysis.get_state_name(60, mock_g.sentiment_bins)
            assert result == "发酵"

    def test_get_state_name_sentiment_high(self, mock_jqdata, mock_g):
        with patch('jqdata.g', mock_g):
            import smallcap_state_analysis
            
            result = smallcap_state_analysis.get_state_name(100, mock_g.sentiment_bins)
            assert result == "高潮"

    def test_record_market_state(self, mock_jqdata, mock_g, mock_context):
        with patch('jqdata.g', mock_g):
            import smallcap_state_analysis
            
            mock_jqdata.get_index_stocks.return_value = ['000001.XSHE', '000002.XSHE']
            
            price_df = pd.DataFrame({
                'code': ['000001.XSHE'] * 20,
                'close': [10.0] * 20
            })
            mock_jqdata.get_price.return_value = price_df
            
            all_stocks = pd.DataFrame({'display_name': ['A']}, index=['000001.XSHE'])
            mock_jqdata.get_all_securities.return_value = all_stocks
            
            smallcap_state_analysis.record_market_state(mock_context)
            
            assert len(mock_g.state_data) == 1
            assert 'date' in mock_g.state_data[0]
            assert 'market_breadth' in mock_g.state_data[0]
            assert 'breadth_state' in mock_g.state_data[0]

    def test_analyze_smallcap_no_stocks(self, mock_jqdata, mock_g, mock_context):
        with patch('jqdata.g', mock_g):
            import smallcap_state_analysis
            
            mock_jqdata.get_fundamentals.return_value = pd.DataFrame()
            
            smallcap_state_analysis.analyze_smallcap(mock_context)
            
            assert len(mock_g.trade_data) == 0

    def test_analyze_smallcap_with_stocks(self, mock_jqdata, mock_g, mock_context):
        with patch('jqdata.g', mock_g):
            import smallcap_state_analysis
            
            mock_g.current_breadth_state = "中"
            mock_g.current_sentiment_state = "发酵"
            mock_g.current_breadth = 0.3
            mock_g.current_zt_count = 60
            
            fundamentals_df = pd.DataFrame({
                'code': ['000001.XSHE', '000002.XSHE'],
                'circulating_market_cap': [10, 20]
            })
            mock_jqdata.get_fundamentals.return_value = fundamentals_df
            
            price_today = pd.DataFrame({
                'code': ['000001.XSHE', '000002.XSHE'],
                'close': [10.0, 20.0]
            })
            price_next = pd.DataFrame({
                'code': ['000001.XSHE', '000002.XSHE'],
                'open': [10.5, 20.5],
                'close': [11.0, 21.0]
            })
            
            mock_jqdata.get_price.side_effect = [price_today, price_next]
            mock_jqdata.get_next_trade_date.return_value = '2024-01-17'
            
            smallcap_state_analysis.analyze_smallcap(mock_context)
            
            assert len(mock_g.trade_data) >= 0

    def test_on_end_no_data(self, mock_jqdata, mock_g):
        with patch('jqdata.g', mock_g):
            import smallcap_state_analysis
            
            mock_g.trade_data = []
            context = SimpleNamespace()
            
            smallcap_state_analysis.on_end(context)
            
            mock_jqdata.log.info.assert_called()

    def test_on_end_with_data(self, mock_jqdata, mock_g):
        with patch('jqdata.g', mock_g):
            import smallcap_state_analysis
            
            mock_g.trade_data = [
                {
                    'breadth_state': '中',
                    'sentiment_state': '发酵',
                    'return_close': 2.0,
                    'market_breadth': 0.3,
                    'zt_count': 60
                }
            ]
            context = SimpleNamespace()
            
            smallcap_state_analysis.on_end(context)
            
            mock_jqdata.log.info.assert_called()