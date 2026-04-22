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
    mock_module.run_daily = Mock()
    mock_module.get_index_stocks = Mock()
    mock_module.get_all_securities = Mock()
    mock_module.get_price = Mock()
    mock_module.order_value = Mock()
    mock_module.order_target_value = Mock()
    mock_module.g = SimpleNamespace()
    
    with patch.dict(sys.modules, {'jqdata': mock_module}):
        yield mock_module


@pytest.fixture
def mock_g():
    g = SimpleNamespace()
    g.state = "正常"
    g.target_position = 70
    g.hs300_stocks = []
    g.breadth_pct = 30
    g.zt_count = 50
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


class TestStateRouterV1Fast:
    def test_initialize(self, mock_jqdata, mock_g):
        with patch('jqdata.g', mock_g):
            import state_router_v1_fast
            context = SimpleNamespace()
            state_router_v1_fast.initialize(context)
            
            mock_jqdata.set_option.assert_called()
            mock_jqdata.set_benchmark.assert_called()
            mock_jqdata.run_daily.assert_called()
            assert mock_g.hs300_stocks == []

    def test_update_hs300(self, mock_jqdata, mock_g, mock_context):
        with patch('jqdata.g', mock_g):
            import state_router_v1_fast
            
            mock_jqdata.get_index_stocks.return_value = ['000001.XSHE', '000002.XSHE', '000003.XSHG']
            
            state_router_v1_fast.update_hs300(mock_context)
            
            assert len(mock_g.hs300_stocks) <= 30

    def test_classify_breadth(self, mock_jqdata, mock_g):
        with patch('jqdata.g', mock_g):
            import state_router_v1_fast
            
            assert state_router_v1_fast.classify_breadth(10) == 1
            assert state_router_v1_fast.classify_breadth(20) == 2
            assert state_router_v1_fast.classify_breadth(30) == 3
            assert state_router_v1_fast.classify_breadth(40) == 4

    def test_classify_sentiment(self, mock_jqdata, mock_g):
        with patch('jqdata.g', mock_g):
            import state_router_v1_fast
            
            assert state_router_v1_fast.classify_sentiment(20) == 1
            assert state_router_v1_fast.classify_sentiment(40) == 2
            assert state_router_v1_fast.classify_sentiment(60) == 3
            assert state_router_v1_fast.classify_sentiment(80) == 4

    def test_get_state_position(self, mock_jqdata, mock_g):
        with patch('jqdata.g', mock_g):
            import state_router_v1_fast
            
            state, position = state_router_v1_fast.get_state_position(1, 2)
            assert state == "关闭"
            assert position == 0
            
            state, position = state_router_v1_fast.get_state_position(4, 4)
            assert state == "进攻"
            assert position == 100

    def test_calculate_breadth_simple_empty(self, mock_jqdata, mock_g):
        with patch('jqdata.g', mock_g):
            import state_router_v1_fast
            
            mock_g.hs300_stocks = []
            mock_jqdata.get_index_stocks.return_value = []
            
            result = state_router_v1_fast.calculate_breadth_simple("2024-01-15")
            
            assert result == 30

    def test_calculate_breadth_simple_with_stocks(self, mock_jqdata, mock_g):
        with patch('jqdata.g', mock_g):
            import state_router_v1_fast
            
            mock_g.hs300_stocks = ['000001.XSHE', '000002.XSHE']
            
            price_df = pd.DataFrame({
                'close': [10.0] * 21
            })
            mock_jqdata.get_price.return_value = price_df
            
            result = state_router_v1_fast.calculate_breadth_simple("2024-01-15")
            
            assert result >= 0

    def test_get_zt_count_cached_empty(self, mock_jqdata, mock_g):
        with patch('jqdata.g', mock_g):
            import state_router_v1_fast
            
            mock_jqdata.get_all_securities.return_value = pd.DataFrame()
            mock_jqdata.get_price.return_value = pd.DataFrame()
            
            result = state_router_v1_fast.get_zt_count_cached("2024-01-15")
            
            assert result == 40

    def test_get_zt_count_cached_with_data(self, mock_jqdata, mock_g):
        with patch('jqdata.g', mock_g):
            import state_router_v1_fast
            
            all_stocks = pd.DataFrame({'display_name': ['A']}, index=['000001.XSHE'])
            mock_jqdata.get_all_securities.return_value = all_stocks
            
            price_df = pd.DataFrame({
                'code': ['000001.XSHE'] * 50,
                'close': [10.0] * 50,
                'high_limit': [10.0] * 50
            })
            mock_jqdata.get_price.return_value = price_df
            
            result = state_router_v1_fast.get_zt_count_cached("2024-01-15")
            
            assert result >= 0

    def test_handle_data_zero_position(self, mock_jqdata, mock_g, mock_context):
        with patch('jqdata.g', mock_g):
            import state_router_v1_fast
            
            mock_g.target_position = 0
            
            pos = SimpleNamespace()
            mock_context.portfolio.positions = {'000300.XSHG': pos}
            
            data = SimpleNamespace()
            state_router_v1_fast.handle_data(mock_context, data)
            
            mock_jqdata.order_target_value.assert_called()

    def test_handle_data_normal_position(self, mock_jqdata, mock_g, mock_context):
        with patch('jqdata.g', mock_g):
            import state_router_v1_fast
            
            mock_g.target_position = 70
            
            pos = SimpleNamespace()
            pos.value = 500000
            mock_context.portfolio.positions = {'000300.XSHG': pos}
            
            data = SimpleNamespace()
            state_router_v1_fast.handle_data(mock_context, data)
            
            mock_jqdata.order_value.assert_called()

    def test_before_trading_start(self, mock_jqdata, mock_g, mock_context):
        with patch('jqdata.g', mock_g):
            import state_router_v1_fast
            
            mock_g.hs300_stocks = ['000001.XSHE']
            
            price_df = pd.DataFrame({'close': [10.0] * 21})
            mock_jqdata.get_price.return_value = price_df
            
            all_stocks = pd.DataFrame({'display_name': ['A']}, index=['000001.XSHE'])
            mock_jqdata.get_all_securities.return_value = all_stocks
            
            state_router_v1_fast.before_trading_start(mock_context)
            
            assert mock_g.state is not None
            assert mock_g.target_position is not None