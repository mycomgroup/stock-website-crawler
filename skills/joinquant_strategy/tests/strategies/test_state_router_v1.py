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
    portfolio.positions_value = 0
    portfolio.positions = {}
    context.portfolio = portfolio
    return context


class TestStateRouterV1:
    def test_initialize(self, mock_jqdata, mock_g):
        with patch('jqdata.g', mock_g):
            import state_router_v1
            context = SimpleNamespace()
            state_router_v1.initialize(context)
            
            mock_jqdata.set_option.assert_called()
            mock_jqdata.set_benchmark.assert_called()
            assert mock_g.state == "正常"
            assert mock_g.target_position == 70

    def test_classify_breadth_level_1(self, mock_jqdata, mock_g):
        with patch('jqdata.g', mock_g):
            import state_router_v1
            
            assert state_router_v1.classify_breadth(10) == 1
            assert state_router_v1.classify_breadth(14) == 1

    def test_classify_breadth_level_2(self, mock_jqdata, mock_g):
        with patch('jqdata.g', mock_g):
            import state_router_v1
            
            assert state_router_v1.classify_breadth(20) == 2
            assert state_router_v1.classify_breadth(24) == 2

    def test_classify_breadth_level_3(self, mock_jqdata, mock_g):
        with patch('jqdata.g', mock_g):
            import state_router_v1
            
            assert state_router_v1.classify_breadth(30) == 3
            assert state_router_v1.classify_breadth(34) == 3

    def test_classify_breadth_level_4(self, mock_jqdata, mock_g):
        with patch('jqdata.g', mock_g):
            import state_router_v1
            
            assert state_router_v1.classify_breadth(40) == 4
            assert state_router_v1.classify_breadth(100) == 4

    def test_classify_sentiment_level_1(self, mock_jqdata, mock_g):
        with patch('jqdata.g', mock_g):
            import state_router_v1
            
            assert state_router_v1.classify_sentiment(20) == 1
            assert state_router_v1.classify_sentiment(29) == 1

    def test_classify_sentiment_level_2(self, mock_jqdata, mock_g):
        with patch('jqdata.g', mock_g):
            import state_router_v1
            
            assert state_router_v1.classify_sentiment(40) == 2
            assert state_router_v1.classify_sentiment(49) == 2

    def test_classify_sentiment_level_3(self, mock_jqdata, mock_g):
        with patch('jqdata.g', mock_g):
            import state_router_v1
            
            assert state_router_v1.classify_sentiment(60) == 3
            assert state_router_v1.classify_sentiment(79) == 3

    def test_classify_sentiment_level_4(self, mock_jqdata, mock_g):
        with patch('jqdata.g', mock_g):
            import state_router_v1
            
            assert state_router_v1.classify_sentiment(80) == 4
            assert state_router_v1.classify_sentiment(100) == 4

    def test_get_state_position_breadth_1(self, mock_jqdata, mock_g):
        with patch('jqdata.g', mock_g):
            import state_router_v1
            
            state, position = state_router_v1.get_state_position(1, 2)
            assert state == "关闭"
            assert position == 0

    def test_get_state_position_breadth_2_low_sentiment(self, mock_jqdata, mock_g):
        with patch('jqdata.g', mock_g):
            import state_router_v1
            
            state, position = state_router_v1.get_state_position(2, 1)
            assert state == "防守"
            assert position == 30

    def test_get_state_position_breadth_2_high_sentiment(self, mock_jqdata, mock_g):
        with patch('jqdata.g', mock_g):
            import state_router_v1
            
            state, position = state_router_v1.get_state_position(2, 3)
            assert state == "轻仓"
            assert position == 50

    def test_get_state_position_breadth_3_normal(self, mock_jqdata, mock_g):
        with patch('jqdata.g', mock_g):
            import state_router_v1
            
            state, position = state_router_v1.get_state_position(3, 3)
            assert state == "正常"
            assert position == 70

    def test_get_state_position_breadth_3_attack(self, mock_jqdata, mock_g):
        with patch('jqdata.g', mock_g):
            import state_router_v1
            
            state, position = state_router_v1.get_state_position(3, 4)
            assert state == "进攻"
            assert position == 100

    def test_get_state_position_breadth_4_attack(self, mock_jqdata, mock_g):
        with patch('jqdata.g', mock_g):
            import state_router_v1
            
            state, position = state_router_v1.get_state_position(4, 4)
            assert state == "进攻"
            assert position == 100

    def test_calculate_breadth_empty_stocks(self, mock_jqdata, mock_g):
        with patch('jqdata.g', mock_g):
            import state_router_v1
            
            mock_jqdata.get_index_stocks.return_value = []
            
            result = state_router_v1.calculate_breadth("2024-01-15")
            
            assert result == 30

    def test_calculate_sentiment_empty_stocks(self, mock_jqdata, mock_g):
        with patch('jqdata.g', mock_g):
            import state_router_v1
            
            mock_jqdata.get_all_securities.return_value = pd.DataFrame()
            
            result = state_router_v1.calculate_sentiment("2024-01-15")
            
            assert result == 40

    def test_handle_data_zero_position(self, mock_jqdata, mock_g, mock_context):
        with patch('jqdata.g', mock_g):
            import state_router_v1
            
            mock_g.target_position = 0
            
            pos = SimpleNamespace()
            mock_context.portfolio.positions = {'000300.XSHG': pos}
            
            data = SimpleNamespace()
            state_router_v1.handle_data(mock_context, data)
            
            mock_jqdata.order_target_value.assert_called()

    def test_handle_data_normal_position(self, mock_jqdata, mock_g, mock_context):
        with patch('jqdata.g', mock_g):
            import state_router_v1
            
            mock_g.target_position = 70
            
            pos = SimpleNamespace()
            pos.value = 500000
            mock_context.portfolio.positions = {'000300.XSHG': pos}
            
            data = SimpleNamespace()
            state_router_v1.handle_data(mock_context, data)
            
            mock_jqdata.order_value.assert_called()