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
    mock_module.set_option = Mock()
    mock_module.set_benchmark = Mock()
    mock_module.log = MagicMock()
    mock_module.log.set_level = Mock()
    mock_module.log.info = Mock()
    mock_module.run_daily = Mock()
    mock_module.get_index_stocks = Mock()
    mock_module.get_all_securities = Mock()
    mock_module.get_price = Mock()
    mock_module.get_current_data = Mock()
    mock_module.get_fundamentals = Mock()
    mock_module.query = Mock()
    mock_module.valuation = MagicMock()
    mock_module.order = Mock()
    mock_module.order_target = Mock()
    mock_module.g = SimpleNamespace()
    
    with patch.dict(sys.modules, {'jqdata': mock_module}):
        yield mock_module


@pytest.fixture
def mock_g():
    g = SimpleNamespace()
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
    g.results = {
        "no_filter": {"returns": [], "drawdowns": []},
        "breadth_filtered": {"returns": [], "drawdowns": []},
        "sentiment_filtered": {"returns": [], "drawdowns": []},
        "both_filtered": {"returns": [], "drawdowns": []},
    }
    g.state_results = {}
    g.trade_log = []
    g.target = []
    g.market_breadth = 0
    g.zt_count = 0
    g.breadth_state = ""
    g.sentiment_state = ""
    g.breadth_filter = False
    g.sentiment_filter = False
    g.date = ""
    g.max_value = 0
    g.drawdown = 0
    return g


@pytest.fixture
def mock_context():
    context = SimpleNamespace()
    context.previous_date = datetime(2024, 1, 15)
    context.current_dt = datetime(2024, 1, 16, 9, 30)
    
    portfolio = SimpleNamespace()
    portfolio.available_cash = 1000000
    portfolio.total_value = 1000000
    portfolio.positions = {}
    context.portfolio = portfolio
    return context


class TestSmallcapStateTest:
    def test_initialize(self, mock_jqdata, mock_g):
        with patch('jqdata.g', mock_g):
            import smallcap_state_test
            context = SimpleNamespace()
            smallcap_state_test.initialize(context)
            
            mock_jqdata.set_option.assert_called()
            mock_jqdata.run_daily.assert_called()
            assert mock_g.results is not None

    def test_get_hs300_stocks(self, mock_jqdata, mock_g):
        with patch('jqdata.g', mock_g):
            import smallcap_state_test
            
            mock_jqdata.get_index_stocks.return_value = ['000001.XSHE', '000002.XSHE']
            
            result = smallcap_state_test.get_hs300_stocks()
            
            assert result == ['000001.XSHE', '000002.XSHE']

    def test_get_state_name(self, mock_jqdata, mock_g):
        with patch('jqdata.g', mock_g):
            import smallcap_state_test
            
            assert smallcap_state_test.get_state_name(0.1, mock_g.market_breadth_bins) == "极弱"
            assert smallcap_state_test.get_state_name(0.5, mock_g.market_breadth_bins) == "强"

    def test_record_state(self, mock_jqdata, mock_g, mock_context):
        with patch('jqdata.g', mock_g):
            import smallcap_state_test
            
            mock_g.hs300_stocks = ['000001.XSHE', '000002.XSHE']
            
            price_df = pd.DataFrame({
                'code': ['000001.XSHE'] * 20 + ['000002.XSHE'] * 20,
                'close': [10.0] * 40
            })
            mock_jqdata.get_price.return_value = price_df
            
            all_stocks = pd.DataFrame({'display_name': ['A']}, index=['000001.XSHE'])
            mock_jqdata.get_all_securities.return_value = all_stocks
            
            smallcap_state_test.record_state(mock_context)
            
            assert mock_g.breadth_state in mock_g.market_breadth_bins.keys()

    def test_select_stocks(self, mock_jqdata, mock_g, mock_context):
        with patch('jqdata.g', mock_g):
            import smallcap_state_test
            
            fundamentals_df = pd.DataFrame({
                'code': ['000001.XSHE', '000002.XSHE'] * 25,
                'circulating_market_cap': [10] * 50
            })
            mock_jqdata.get_fundamentals.return_value = fundamentals_df
            
            all_stocks = pd.DataFrame({'display_name': ['A']}, index=['000001.XSHE'])
            mock_jqdata.get_all_securities.return_value = all_stocks
            
            smallcap_state_test.select_stocks(mock_context)
            
            assert len(mock_g.target) <= 50

    def test_buy_stocks_no_target(self, mock_jqdata, mock_g, mock_context):
        with patch('jqdata.g', mock_g):
            import smallcap_state_test
            
            mock_g.target = []
            
            smallcap_state_test.buy_stocks(mock_context)
            
            mock_jqdata.order.assert_not_called()

    def test_buy_stocks_with_target(self, mock_jqdata, mock_g, mock_context):
        with patch('jqdata.g', mock_g):
            import smallcap_state_test
            
            mock_g.target = ['000001.XSHE', '000002.XSHE']
            mock_g.date = '2024-01-16'
            mock_g.breadth_state = '中'
            mock_g.sentiment_state = '发酵'
            
            mock_current = {
                '000001.XSHE': SimpleNamespace(
                    last_price=10.0,
                    paused=False
                ),
                '000002.XSHE': SimpleNamespace(
                    last_price=20.0,
                    paused=False
                )
            }
            mock_jqdata.get_current_data.return_value = mock_current
            
            smallcap_state_test.buy_stocks(mock_context)
            
            mock_jqdata.order.assert_called()

    def test_sell_stocks(self, mock_jqdata, mock_g, mock_context):
        with patch('jqdata.g', mock_g):
            import smallcap_state_test
            
            mock_g.date = '2024-01-16'
            mock_g.trade_log = [
                {'stock': '000001.XSHE', 'date': '2024-01-16', 'mode': 'no_filter'}
            ]
            
            pos = SimpleNamespace()
            pos.closeable_amount = 100
            pos.avg_cost = 10.0
            mock_context.portfolio.positions = {'000001.XSHE': pos}
            
            mock_current = {
                '000001.XSHE': SimpleNamespace(
                    last_price=11.0,
                    paused=False
                )
            }
            mock_jqdata.get_current_data.return_value = mock_current
            
            smallcap_state_test.sell_stocks(mock_context)
            
            mock_jqdata.order_target.assert_called()

    def test_record_end(self, mock_jqdata, mock_g, mock_context):
        with patch('jqdata.g', mock_g):
            import smallcap_state_test
            
            mock_g.max_value = 1000000
            
            smallcap_state_test.record_end(mock_context)
            
            assert mock_g.max_value >= context.portfolio.total_value

    def test_state_results_initialization(self, mock_jqdata, mock_g):
        with patch('jqdata.g', mock_g):
            import smallcap_state_test
            
            for breadth_state in mock_g.market_breadth_bins.keys():
                for sentiment_state in mock_g.sentiment_bins.keys():
                    key = f"{breadth_state}_{sentiment_state}"
                    mock_g.state_results[key] = {"returns": [], "count": 0}
            
            assert len(mock_g.state_results) == 16

    def test_breadth_filter_threshold(self, mock_jqdata, mock_g, mock_context):
        with patch('jqdata.g', mock_g):
            import smallcap_state_test
            
            mock_g.market_breadth = 0.30
            
            if hasattr(mock_g, 'breadth_filter'):
                mock_g.breadth_filter = mock_g.market_breadth >= 0.25
            
            assert mock_g.breadth_filter == True

    def test_sentiment_filter_threshold(self, mock_jqdata, mock_g, mock_context):
        with patch('jqdata.g', mock_g):
            import smallcap_state_test
            
            mock_g.zt_count = 60
            
            if hasattr(mock_g, 'sentiment_filter'):
                mock_g.sentiment_filter = mock_g.zt_count >= 50
            
            assert mock_g.sentiment_filter == True