import pytest
import sys
from unittest.mock import MagicMock, patch, Mock
from types import SimpleNamespace
from datetime import datetime
import pandas as pd

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
    g.trade_records = []
    g.daily_records = []
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
    g.position_size = 10
    g.current_state = {}
    g.buy_prices = {}
    return g


@pytest.fixture
def mock_context():
    context = SimpleNamespace()
    context.previous_date = datetime(2024, 1, 15)
    context.current_dt = datetime(2024, 1, 16, 9, 35)
    
    portfolio = SimpleNamespace()
    portfolio.available_cash = 1000000
    portfolio.total_value = 1000000
    portfolio.positions = {}
    context.portfolio = portfolio
    return context


class TestSmallcapStateBaseline:
    def test_initialize(self, mock_jqdata, mock_g):
        with patch('jqdata.g', mock_g):
            import smallcap_state_baseline
            context = SimpleNamespace()
            smallcap_state_baseline.initialize(context)
            
            mock_jqdata.set_option.assert_called()
            mock_jqdata.run_daily.assert_called()
            assert mock_g.position_size == 10

    def test_get_state_name(self, mock_jqdata, mock_g):
        with patch('jqdata.g', mock_g):
            import smallcap_state_baseline
            
            assert smallcap_state_baseline.get_state_name(0.1, mock_g.market_breadth_bins) == "极弱"
            assert smallcap_state_baseline.get_state_name(0.5, mock_g.market_breadth_bins) == "强"
            assert smallcap_state_baseline.get_state_name(10, mock_g.sentiment_bins) == "冰点"
            assert smallcap_state_baseline.get_state_name(100, mock_g.sentiment_bins) == "高潮"

    def test_record_state(self, mock_jqdata, mock_g, mock_context):
        with patch('jqdata.g', mock_g):
            import smallcap_state_baseline
            
            mock_jqdata.get_index_stocks.return_value = ['000001.XSHE', '000002.XSHE']
            
            price_df = pd.DataFrame({
                'code': ['000001.XSHE'] * 20,
                'close': [10.0] * 20
            })
            mock_jqdata.get_price.return_value = price_df
            
            all_stocks = pd.DataFrame({'display_name': ['A']}, index=['000001.XSHE'])
            mock_jqdata.get_all_securities.return_value = all_stocks
            
            smallcap_state_baseline.record_state(mock_context)
            
            assert 'date' in mock_g.current_state
            assert 'market_breadth' in mock_g.current_state

    def test_select_and_buy_no_stocks(self, mock_jqdata, mock_g, mock_context):
        with patch('jqdata.g', mock_g):
            import smallcap_state_baseline
            
            mock_jqdata.get_fundamentals.return_value = pd.DataFrame()
            
            smallcap_state_baseline.select_and_buy(mock_context)
            
            mock_jqdata.order.assert_not_called()

    def test_select_and_buy_with_stocks(self, mock_jqdata, mock_g, mock_context):
        with patch('jqdata.g', mock_g):
            import smallcap_state_baseline
            
            mock_g.current_state = {'market_breadth': 0.3, 'breadth_state': '中'}
            
            fundamentals_df = pd.DataFrame({
                'code': ['000001.XSHE', '000002.XSHE'],
                'circulating_market_cap': [10, 20]
            })
            mock_jqdata.get_fundamentals.return_value = fundamentals_df
            
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
            
            smallcap_state_baseline.select_and_buy(mock_context)
            
            mock_jqdata.order.assert_called()

    def test_sell_all(self, mock_jqdata, mock_g, mock_context):
        with patch('jqdata.g', mock_g):
            import smallcap_state_baseline
            
            mock_g.current_state = {'market_breadth': 0.3, 'breadth_state': '中'}
            
            pos = SimpleNamespace()
            pos.closeable_amount = 100
            pos.avg_cost = 10.0
            mock_context.portfolio.positions = {'000001.XSHE': pos}
            
            mock_g.buy_prices = {'000001.XSHE': 10.0}
            
            mock_current = {
                '000001.XSHE': SimpleNamespace(
                    last_price=11.0,
                    paused=False
                )
            }
            mock_jqdata.get_current_data.return_value = mock_current
            
            smallcap_state_baseline.sell_all(mock_context)
            
            mock_jqdata.order_target.assert_called_with('000001.XSHE', 0)
            assert len(mock_g.daily_records) == 1

    def test_on_end_no_trades(self, mock_jqdata, mock_g):
        with patch('jqdata.g', mock_g):
            import smallcap_state_baseline
            
            mock_g.trade_records = []
            context = SimpleNamespace()
            
            smallcap_state_baseline.on_end(context)
            
            mock_jqdata.log.info.assert_called()

    def test_on_end_with_trades(self, mock_jqdata, mock_g):
        with patch('jqdata.g', mock_g):
            import smallcap_state_baseline
            
            mock_g.trade_records = [
                {
                    'buy_date': '2024-01-16',
                    'stock': '000001.XSHE',
                    'buy_price': 10.0,
                    'sell_price': 11.0,
                    'pnl': 10.0,
                    'breadth_state': '中',
                    'sentiment_state': '发酵'
                }
            ]
            context = SimpleNamespace()
            
            smallcap_state_baseline.on_end(context)
            
            mock_jqdata.log.info.assert_called()

    def test_trade_record_structure(self, mock_jqdata, mock_g, mock_context):
        with patch('jqdata.g', mock_g):
            import smallcap_state_baseline
            
            mock_g.current_state = {
                'market_breadth': 0.3,
                'breadth_state': '中',
                'zt_count': 60,
                'sentiment_state': '发酵'
            }
            
            fundamentals_df = pd.DataFrame({
                'code': ['000001.XSHE'],
                'circulating_market_cap': [10]
            })
            mock_jqdata.get_fundamentals.return_value = fundamentals_df
            
            mock_current = {
                '000001.XSHE': SimpleNamespace(
                    last_price=10.0,
                    paused=False
                )
            }
            mock_jqdata.get_current_data.return_value = mock_current
            
            smallcap_state_baseline.select_and_buy(mock_context)
            
            if len(mock_g.trade_records) > 0:
                record = mock_g.trade_records[0]
                assert 'buy_date' in record
                assert 'stock' in record
                assert 'buy_price' in record
                assert 'market_breadth' in record