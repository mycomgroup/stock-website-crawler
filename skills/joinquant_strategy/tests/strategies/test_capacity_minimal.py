import pytest
import sys
from unittest.mock import MagicMock, patch, Mock
from types import SimpleNamespace
from datetime import datetime
import pandas as pd

sys.path.insert(0, '/Users/yuping/Downloads/git/stock-website-crawler/strategies/misc_research/joinquant_strategy')


def create_price_df_limit_up(num_stocks=10):
    codes = [f'60000{i}.XSHG' for i in range(num_stocks)]
    return pd.DataFrame({
        'code': codes,
        'close': [10.0] * num_stocks,
        'high_limit': [10.0] * num_stocks
    })


@pytest.fixture
def mock_jqdata():
    mock_module = MagicMock()
    mock_module.set_option = Mock()
    mock_module.set_benchmark = Mock()
    mock_module.set_slippage = Mock()
    mock_module.FixedSlippage = Mock()
    mock_module.log = MagicMock()
    mock_module.log.set_level = Mock()
    mock_module.run_daily = Mock()
    mock_module.get_all_securities = Mock()
    mock_module.get_price = Mock()
    mock_module.get_current_data = Mock()
    mock_module.order_value = Mock()
    mock_module.order_target = Mock()
    mock_module.g = SimpleNamespace()
    
    with patch.dict(sys.modules, {'jqdata': mock_module}):
        yield mock_module


@pytest.fixture
def mock_g():
    return SimpleNamespace()


@pytest.fixture
def mock_context():
    context = SimpleNamespace()
    context.previous_date = datetime(2024, 1, 15)
    context.current_dt = datetime(2024, 1, 16, 9, 31)
    
    portfolio = SimpleNamespace()
    portfolio.available_cash = 1000000
    portfolio.positions = {}
    context.portfolio = portfolio
    return context


@pytest.fixture
def mock_securities():
    return pd.DataFrame({
        'display_name': ['平安银行', '万科A', '浦发银行']
    }, index=['000001.XSHE', '000002.XSHE', '600000.XSHG'])


class TestCapacityMinimal:
    def test_initialize_no_slippage(self, mock_jqdata, mock_g):
        with patch('jqdata.g', mock_g):
            import capacity_minimal
            mock_context = SimpleNamespace()
            capacity_minimal.initialize(mock_context)
            
            mock_jqdata.set_option.assert_any_call("use_real_price", True)
            mock_jqdata.set_benchmark.assert_called_once_with("000300.XSHG")
            assert mock_jqdata.run_daily.call_count == 2
            mock_jqdata.set_slippage.assert_not_called()

    def test_initialize_with_slippage(self, mock_jqdata, mock_g):
        with patch('jqdata.g', mock_g):
            import importlib
            import capacity_minimal
            
            capacity_minimal.SLIPPAGE_BPS = 10
            
            mock_context = SimpleNamespace()
            capacity_minimal.initialize(mock_context)
            
            mock_jqdata.set_slippage.assert_called_once()
            
            capacity_minimal.SLIPPAGE_BPS = 0

    def test_buy_no_limit_up(self, mock_jqdata, mock_g, mock_context, mock_securities):
        with patch('jqdata.g', mock_g):
            import capacity_minimal
            
            mock_jqdata.get_all_securities.return_value = mock_securities
            
            price_df_no_limit = pd.DataFrame({
                'code': ['000001.XSHE'],
                'close': [9.0],
                'high_limit': [10.0]
            })
            mock_jqdata.get_price.return_value = price_df_no_limit
            
            capacity_minimal.buy(mock_context)
            
            mock_jqdata.order_value.assert_not_called()

    def test_buy_with_limit_up(self, mock_jqdata, mock_g, mock_context, mock_securities):
        with patch('jqdata.g', mock_g):
            import capacity_minimal
            
            mock_jqdata.get_all_securities.return_value = mock_securities
            mock_jqdata.get_price.return_value = create_price_df_limit_up(10)
            
            stock_data = SimpleNamespace()
            stock_data.paused = False
            stock_data.is_st = False
            stock_data.day_open = 10.0
            stock_data.pre_close = 10.0
            
            current_data = {}
            for i in range(10):
                current_data[f'60000{i}.XSHG'] = stock_data
            
            mock_jqdata.get_current_data.return_value = current_data
            
            capacity_minimal.buy(mock_context)
            
            assert mock_jqdata.order_value.call_count > 0

    def test_buy_filters_paused(self, mock_jqdata, mock_g, mock_context, mock_securities):
        with patch('jqdata.g', mock_g):
            import capacity_minimal
            
            mock_jqdata.get_all_securities.return_value = mock_securities
            mock_jqdata.get_price.return_value = create_price_df_limit_up(10)
            
            stock_data_paused = SimpleNamespace()
            stock_data_paused.paused = True
            stock_data_paused.is_st = False
            
            mock_jqdata.get_current_data.return_value = {'000001.XSHE': stock_data_paused}
            
            capacity_minimal.buy(mock_context)
            
            mock_jqdata.order_value.assert_not_called()

    def test_buy_filters_st(self, mock_jqdata, mock_g, mock_context, mock_securities):
        with patch('jqdata.g', mock_g):
            import capacity_minimal
            
            mock_jqdata.get_all_securities.return_value = mock_securities
            mock_jqdata.get_price.return_value = create_price_df_limit_up(10)
            
            stock_data_st = SimpleNamespace()
            stock_data_st.paused = False
            stock_data_st.is_st = True
            
            mock_jqdata.get_current_data.return_value = {'000001.XSHE': stock_data_st}
            
            capacity_minimal.buy(mock_context)
            
            mock_jqdata.order_value.assert_not_called()

    def test_buy_open_pct_in_range(self, mock_jqdata, mock_g, mock_context, mock_securities):
        with patch('jqdata.g', mock_g):
            import capacity_minimal
            
            mock_jqdata.get_all_securities.return_value = mock_securities
            mock_jqdata.get_price.return_value = create_price_df_limit_up(10)
            
            stock_data = SimpleNamespace()
            stock_data.paused = False
            stock_data.is_st = False
            stock_data.day_open = 10.0
            stock_data.pre_close = 10.0
            
            current_data = {}
            for i in range(5):
                current_data[f'60000{i}.XSHG'] = stock_data
            
            mock_jqdata.get_current_data.return_value = current_data
            
            capacity_minimal.buy(mock_context)
            
            assert mock_jqdata.order_value.call_count <= 3

    def test_buy_open_pct_out_of_range(self, mock_jqdata, mock_g, mock_context, mock_securities):
        with patch('jqdata.g', mock_g):
            import capacity_minimal
            
            mock_jqdata.get_all_securities.return_value = mock_securities
            mock_jqdata.get_price.return_value = create_price_df_limit_up(10)
            
            stock_data = SimpleNamespace()
            stock_data.paused = False
            stock_data.is_st = False
            stock_data.day_open = 11.0
            stock_data.pre_close = 10.0
            
            mock_jqdata.get_current_data.return_value = {'000001.XSHE': stock_data}
            
            capacity_minimal.buy(mock_context)
            
            mock_jqdata.order_value.assert_not_called()

    def test_sell_with_positions(self, mock_jqdata, mock_g, mock_context):
        with patch('jqdata.g', mock_g):
            import capacity_minimal
            
            pos = SimpleNamespace()
            pos.closeable_amount = 1000
            
            mock_context.portfolio.positions = {'000001.XSHE': pos}
            
            capacity_minimal.sell(mock_context)
            
            mock_jqdata.order_target.assert_called_once_with('000001.XSHE', 0)

    def test_sell_no_positions(self, mock_jqdata, mock_g, mock_context):
        with patch('jqdata.g', mock_g):
            import capacity_minimal
            
            mock_context.portfolio.positions = {}
            
            capacity_minimal.sell(mock_context)
            
            mock_jqdata.order_target.assert_not_called()

    def test_sell_no_closeable_amount(self, mock_jqdata, mock_g, mock_context):
        with patch('jqdata.g', mock_g):
            import capacity_minimal
            
            pos = SimpleNamespace()
            pos.closeable_amount = 0
            
            mock_context.portfolio.positions = {'000001.XSHE': pos}
            
            capacity_minimal.sell(mock_context)
            
            mock_jqdata.order_target.assert_not_called()

    def test_slippage_bps_constant(self, mock_jqdata, mock_g):
        with patch('jqdata.g', mock_g):
            import capacity_minimal
            
            assert capacity_minimal.SLIPPAGE_BPS == 0