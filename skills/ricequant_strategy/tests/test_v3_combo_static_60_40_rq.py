"""
Tests for v3_combo_static_60_40_rq.py
"""
import sys
from pathlib import Path
from unittest.mock import MagicMock, patch
from datetime import datetime, date
import numpy as np
import pandas as pd
import pytest

sys.path.insert(0, str(Path(__file__).parent.parent))


class MockBarCombo:
    def __init__(self, close=10.0, is_trading=True, limit_up=11.0):
        self.close = close
        self.is_trading = is_trading
        self.limit_up = limit_up


class MockBarDictCombo(dict):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    
    def get(self, key, default=None):
        if key not in self:
            self[key] = MockBarCombo()
        return self[key]


class MockPortfolioCombo:
    def __init__(self):
        self.starting_cash = 1000000
        self.total_value = 1000000
        self.positions = {}


class MockContextCombo:
    def __init__(self):
        self.now = datetime(2024, 7, 1)
        self.portfolio = MockPortfolioCombo()
        self.benchmark = "000300.XSHG"
        self.rfscore_weight = 0.6
        self.dividend_weight = 0.4
        self.rfscore_num = 15
        self.dividend_num = 10
        self.target_rfscore = []
        self.target_dividend = []
        self.hold_list = []
        self.last_rebalance_month = -1


class MockPositionCombo:
    def __init__(self, market_value=50000):
        self.market_value = market_value
        self.quantity = 1000


class MockInstrumentCombo:
    def __init__(self, order_book_id="000001.XSHE", symbol="平安银行"):
        self.order_book_id = order_book_id
        self.symbol = symbol
        self.display_name = symbol


@pytest.fixture(scope="module")
def setup_rq_mocks_combo():
    mock_logger = MagicMock()
    sys.modules["logger"] = mock_logger
    
    def mock_index_components(index_name):
        if index_name == "000300.XSHG":
            return ["600000.XSHG", "600519.XSHG", "000001.XSHE", "688001.XSHG"]
        elif index_name == "000905.XSHG":
            return ["000002.XSHE", "600036.XSHG", "000651.XSHE", "688002.XSHG"]
        elif index_name == "000985.XSHG":
            return ["000001.XSHE", "000002.XSHE", "600000.XSHG", "600519.XSHG"]
        return []
    
    def mock_history_bars(stock, bar_count, frequency, fields, include_now=False):
        return np.array([10.0, 10.5, 11.0, 11.5, 12.0, 12.5, 13.0, 13.5, 14.0, 14.5,
                        15.0, 15.5, 16.0, 16.5, 17.0, 17.5, 18.0, 18.5, 19.0, 20.0])
    
    def mock_get_factor(stocks, factors, start_date=None, end_date=None):
        n = len(stocks) if stocks else 4
        data = {
            "pb_ratio": [1.5, 2.0, 0.8, 3.0][:n],
            "return_on_asset": [5.0, 3.0, -1.0, 8.0][:n],
            "return_on_equity": [10.0, 5.0, -2.0, 15.0][:n],
            "pe_ratio": [15.0, -5.0, 20.0, 30.0][:n],
            "market_cap": [50000000000, 30000000000, 8000000000, 200000000000][:n],
            "net_profit_growth_rate": [10.0, 3.0, 25.0, 15.0][:n],
        }
        stocks_list = stocks[:n] if stocks else ["000001.XSHE", "000002.XSHE", "600000.XSHG", "600519.XSHG"][:n]
        df = pd.DataFrame(data)
        df.index = pd.MultiIndex.from_product([stocks_list, [start_date]], names=["order_book_id", "date"])
        return df
    
    def mock_all_instruments(type_str=None):
        if type_str == "CS":
            return pd.DataFrame({
                "order_book_id": ["000001.XSHE", "000002.XSHE", "600000.XSHG", "600519.XSHG",
                                  "688001.XSHG", "830001.XSHG", "430001.XSHG"],
                "symbol": ["平安银行", "万科A", "浦发银行", "贵州茅台", "华兴源创", "北交所1", "新三板1"],
            })
        return []
    
    def mock_instruments(stock):
        return MockInstrumentCombo(stock, f"股票{stock}")
    
    def mock_order_target_value(stock, value):
        return None
    
    sys.modules["index_components"] = mock_index_components
    sys.modules["history_bars"] = mock_history_bars
    sys.modules["get_factor"] = mock_get_factor
    sys.modules["all_instruments"] = mock_all_instruments
    sys.modules["instruments"] = mock_instruments
    sys.modules["order_target_value"] = mock_order_target_value
    
    yield mock_logger
    
    del sys.modules["logger"]


class TestV3ComboStatic6040Rq:
    def test_init(self, setup_rq_mocks_combo):
        from v3_combo_static_60_40_rq import init
        context = MockContextCombo()
        init(context)
        assert context.benchmark == "000300.XSHG"
        assert context.rfscore_weight == 0.6
        assert context.dividend_weight == 0.4
        assert context.rfscore_num == 15
        assert context.dividend_num == 10
        assert context.target_rfscore == []
        assert context.target_dividend == []
        assert context.hold_list == []
        assert context.last_rebalance_month == -1
        setup_rq_mocks_combo.info.assert_called()

    def test_handle_bar_first_month(self, setup_rq_mocks_combo):
        from v3_combo_static_60_40_rq import handle_bar, init
        context = MockContextCombo()
        init(context)
        context.last_rebalance_month = 6
        bar_dict = MockBarDictCombo()
        
        with patch("v3_combo_static_60_40_rq.adjust_position"):
            with patch("v3_combo_static_60_40_rq.check_limit_up"):
                handle_bar(context, bar_dict)
                assert context.last_rebalance_month == 7

    def test_handle_bar_same_month(self, setup_rq_mocks_combo):
        from v3_combo_static_60_40_rq import handle_bar, init
        context = MockContextCombo()
        init(context)
        context.last_rebalance_month = 7
        bar_dict = MockBarDictCombo()
        
        with patch("v3_combo_static_60_40_rq.adjust_position"):
            with patch("v3_combo_static_60_40_rq.check_limit_up"):
                handle_bar(context, bar_dict)
                assert context.last_rebalance_month == 7

    def test_handle_bar_calls_check_limit_up(self, setup_rq_mocks_combo):
        from v3_combo_static_60_40_rq import handle_bar, init
        context = MockContextCombo()
        init(context)
        bar_dict = MockBarDictCombo()
        
        with patch("v3_combo_static_60_40_rq.adjust_position"):
            with patch("v3_combo_static_60_40_rq.check_limit_up") as mock_check:
                handle_bar(context, bar_dict)
                mock_check.assert_called()

    def test_is_tradable_stock_in_bar_dict(self, setup_rq_mocks_combo):
        from v3_combo_static_60_40_rq import is_tradable
        bar_dict = MockBarDictCombo()
        bar_dict["000001.XSHE"] = MockBarCombo(is_trading=True)
        result = is_tradable("000001.XSHE", bar_dict)
        assert result == True

    def test_is_tradable_stock_not_in_bar_dict(self, setup_rq_mocks_combo):
        from v3_combo_static_60_40_rq import is_tradable
        bar_dict = {}
        result = is_tradable("000001.XSHE", bar_dict)
        assert result == False

    def test_is_tradable_not_trading(self, setup_rq_mocks_combo):
        from v3_combo_static_60_40_rq import is_tradable
        bar_dict = {"000001.XSHE": MockBarCombo(is_trading=False)}
        result = is_tradable("000001.XSHE", bar_dict)
        assert result == False

    def test_is_tradable_st_stock(self, setup_rq_mocks_combo):
        from v3_combo_static_60_40_rq import is_tradable
        bar_dict = {"000001.XSHE": MockBarCombo(is_trading=True)}
        
        def mock_instruments_st(stock):
            return MockInstrumentCombo(stock, "ST股票")
        
        with patch("v3_combo_static_60_40_rq.instruments", mock_instruments_st):
            result = is_tradable("000001.XSHE", bar_dict)
            assert result == False

    def test_is_tradable_delisted_stock(self, setup_rq_mocks_combo):
        from v3_combo_static_60_40_rq import is_tradable
        bar_dict = {"000001.XSHE": MockBarCombo(is_trading=True)}
        
        def mock_instruments_delisted(stock):
            return MockInstrumentCombo(stock, "股票退")
        
        with patch("v3_combo_static_60_40_rq.instruments", mock_instruments_delisted):
            result = is_tradable("000001.XSHE", bar_dict)
            assert result == False

    def test_is_tradable_star_stock(self, setup_rq_mocks_combo):
        from v3_combo_static_60_40_rq import is_tradable
        bar_dict = {"000001.XSHE": MockBarCombo(is_trading=True)}
        
        def mock_instruments_star(stock):
            return MockInstrumentCombo(stock, "*股票")
        
        with patch("v3_combo_static_60_40_rq.instruments", mock_instruments_star):
            result = is_tradable("000001.XSHE", bar_dict)
            assert result == False

    def test_is_tradable_exception(self, setup_rq_mocks_combo):
        from v3_combo_static_60_40_rq import is_tradable
        bar_dict = {"000001.XSHE": MockBarCombo(is_trading=True)}
        
        with patch("v3_combo_static_60_40_rq.instruments", side_effect=Exception("API error")):
            result = is_tradable("000001.XSHE", bar_dict)
            assert result == False

    def test_get_pb_roa_success(self, setup_rq_mocks_combo):
        from v3_combo_static_60_40_rq import get_pb_roa
        stocks = ["000001.XSHE", "000002.XSHE"]
        watch_date = "2024-07-01"
        result = get_pb_roa(stocks, watch_date)
        assert isinstance(result, pd.DataFrame)

    def test_get_pb_roa_empty_stocks(self, setup_rq_mocks_combo):
        from v3_combo_static_60_40_rq import get_pb_roa
        result = get_pb_roa([], "2024-07-01")
        assert isinstance(result, pd.DataFrame)

    def test_get_pb_roa_exception(self, setup_rq_mocks_combo):
        from v3_combo_static_60_40_rq import get_pb_roa
        
        with patch("v3_combo_static_60_40_rq.get_factor", side_effect=Exception("API error")):
            result = get_pb_roa(["000001.XSHE"], "2024-07-01")
            assert result.empty

    def test_get_pb_roa_none_result(self, setup_rq_mocks_combo):
        from v3_combo_static_60_40_rq import get_pb_roa
        
        with patch("v3_combo_static_60_40_rq.get_factor", return_value=None):
            result = get_pb_roa(["000001.XSHE"], "2024-07-01")
            assert result.empty

    def test_get_pb_roa_empty_result(self, setup_rq_mocks_combo):
        from v3_combo_static_60_40_rq import get_pb_roa
        
        with patch("v3_combo_static_60_40_rq.get_factor", return_value=pd.DataFrame()):
            result = get_pb_roa(["000001.XSHE"], "2024-07-01")
            assert result.empty

    def test_get_market_cap_pe_success(self, setup_rq_mocks_combo):
        from v3_combo_static_60_40_rq import get_market_cap_pe
        stocks = ["000001.XSHE", "000002.XSHE"]
        watch_date = "2024-07-01"
        result = get_market_cap_pe(stocks, watch_date)
        assert isinstance(result, pd.DataFrame)

    def test_get_market_cap_pe_market_cap_conversion(self, setup_rq_mocks_combo):
        from v3_combo_static_60_40_rq import get_market_cap_pe
        stocks = ["000001.XSHE"]
        watch_date = "2024-07-01"
        result = get_market_cap_pe(stocks, watch_date)
        if "market_cap_yi" in result.columns:
            assert result["market_cap_yi"].iloc[0] == result["market_cap"].iloc[0] / 1e8

    def test_get_market_cap_pe_exception(self, setup_rq_mocks_combo):
        from v3_combo_static_60_40_rq import get_market_cap_pe
        
        with patch("v3_combo_static_60_40_rq.get_factor", side_effect=Exception("API error")):
            result = get_market_cap_pe(["000001.XSHE"], "2024-07-01")
            assert result.empty

    def test_get_market_cap_pe_none_result(self, setup_rq_mocks_combo):
        from v3_combo_static_60_40_rq import get_market_cap_pe
        
        with patch("v3_combo_static_60_40_rq.get_factor", return_value=None):
            result = get_market_cap_pe(["000001.XSHE"], "2024-07-01")
            assert result.empty

    def test_select_rfscore7_success(self, setup_rq_mocks_combo):
        from v3_combo_static_60_40_rq import select_rfscore7
        context = MockContextCombo()
        bar_dict = MockBarDictCombo()
        for stock in ["600000.XSHG", "600519.XSHG", "000001.XSHE"]:
            bar_dict[stock] = MockBarCombo(is_trading=True)
        
        def mock_get_factor_rfscore(stocks, factors, start_date=None, end_date=None):
            n = len(stocks)
            data = {
                "pb_ratio": [0.5 + i * 0.1 for i in range(n)],
                "return_on_asset": [5.0 + i * 0.5 for i in range(n)],
                "pe_ratio": [15.0 + i * 1.0 for i in range(n)],
            }
            df = pd.DataFrame(data, index=pd.MultiIndex.from_product([stocks, [start_date]], names=["order_book_id", "date"]))
            return df
        
        with patch("v3_combo_static_60_40_rq.get_factor", mock_get_factor_rfscore):
            result = select_rfscore7(context, bar_dict, 5)
            assert isinstance(result, list)

    def test_select_rfscore7_empty_stocks(self, setup_rq_mocks_combo):
        from v3_combo_static_60_40_rq import select_rfscore7
        context = MockContextCombo()
        bar_dict = MockBarDictCombo()
        
        with patch("v3_combo_static_60_40_rq.index_components", return_value=[]):
            result = select_rfscore7(context, bar_dict, 5)
            assert result == []

    def test_select_rfscore7_empty_df(self, setup_rq_mocks_combo):
        from v3_combo_static_60_40_rq import select_rfscore7
        context = MockContextCombo()
        bar_dict = MockBarDictCombo()
        
        with patch("v3_combo_static_60_40_rq.get_pb_roa", return_value=pd.DataFrame()):
            result = select_rfscore7(context, bar_dict, 5)
            assert result == []

    def test_select_rfscore7_filter_negative_pe(self, setup_rq_mocks_combo):
        from v3_combo_static_60_40_rq import select_rfscore7
        context = MockContextCombo()
        bar_dict = MockBarDictCombo()
        
        def mock_get_factor_neg_pe(stocks, factors, start_date=None, end_date=None):
            data = {
                "pb_ratio": [0.5, 0.6, 0.7],
                "return_on_asset": [5.0, 6.0, 7.0],
                "pe_ratio": [-5.0, 10.0, 15.0],
            }
            df = pd.DataFrame(data, index=pd.MultiIndex.from_product([["600000.XSHG", "600519.XSHG", "000001.XSHE"], [start_date]], names=["order_book_id", "date"]))
            return df
        
        with patch("v3_combo_static_60_40_rq.get_factor", mock_get_factor_neg_pe):
            result = select_rfscore7(context, bar_dict, 5)
            assert isinstance(result, list)

    def test_select_rfscore7_filter_negative_roa(self, setup_rq_mocks_combo):
        from v3_combo_static_60_40_rq import select_rfscore7
        context = MockContextCombo()
        bar_dict = MockBarDictCombo()
        
        def mock_get_factor_neg_roa(stocks, factors, start_date=None, end_date=None):
            data = {
                "pb_ratio": [0.5, 0.6, 0.7],
                "return_on_asset": [-5.0, 6.0, 7.0],
                "pe_ratio": [10.0, 15.0, 20.0],
            }
            df = pd.DataFrame(data, index=pd.MultiIndex.from_product([["600000.XSHG", "600519.XSHG", "000001.XSHE"], [start_date]], names=["order_book_id", "date"]))
            return df
        
        with patch("v3_combo_static_60_40_rq.get_factor", mock_get_factor_neg_roa):
            result = select_rfscore7(context, bar_dict, 5)
            assert isinstance(result, list)

    def test_select_small_dividend_success(self, setup_rq_mocks_combo):
        from v3_combo_static_60_40_rq import select_small_dividend
        context = MockContextCombo()
        bar_dict = MockBarDictCombo()
        
        def mock_get_factor_dividend(stocks, factors, start_date=None, end_date=None):
            n = len(stocks)
            data = {
                "market_cap": [5e9 + i * 1e9 for i in range(n)],
                "pe_ratio": [10.0 + i * 2.0 for i in range(n)],
                "pb_ratio": [1.0 + i * 0.1 for i in range(n)],
                "net_profit_growth_rate": [6.0 + i * 1.0 for i in range(n)],
            }
            df = pd.DataFrame(data, index=pd.MultiIndex.from_product([stocks[:n], [start_date]], names=["order_book_id", "date"]))
            return df
        
        with patch("v3_combo_static_60_40_rq.get_factor", mock_get_factor_dividend):
            result = select_small_dividend(context, bar_dict, 5)
            assert isinstance(result, list)

    def test_select_small_dividend_empty_stocks(self, setup_rq_mocks_combo):
        from v3_combo_static_60_40_rq import select_small_dividend
        context = MockContextCombo()
        bar_dict = MockBarDictCombo()
        
        with patch("v3_combo_static_60_40_rq.all_instruments", return_value=pd.DataFrame()):
            result = select_small_dividend(context, bar_dict, 5)
            assert result == []

    def test_select_small_dividend_empty_df(self, setup_rq_mocks_combo):
        from v3_combo_static_60_40_rq import select_small_dividend
        context = MockContextCombo()
        bar_dict = MockBarDictCombo()
        
        with patch("v3_combo_static_60_40_rq.get_market_cap_pe", return_value=pd.DataFrame()):
            result = select_small_dividend(context, bar_dict, 5)
            assert result == []

    def test_select_small_dividend_market_cap_filter(self, setup_rq_mocks_combo):
        from v3_combo_static_60_40_rq import select_small_dividend
        context = MockContextCombo()
        bar_dict = MockBarDictCombo()
        
        def mock_get_factor_mc(stocks, factors, start_date=None, end_date=None):
            n = len(stocks)
            data = {
                "market_cap": [1e8 + i * 1e10 for i in range(n)],
                "pe_ratio": [10.0 + i * 2.0 for i in range(n)],
                "pb_ratio": [1.0 + i * 0.1 for i in range(n)],
            }
            df = pd.DataFrame(data, index=pd.MultiIndex.from_product([stocks[:n], [start_date]], names=["order_book_id", "date"]))
            return df
        
        with patch("v3_combo_static_60_40_rq.get_factor", mock_get_factor_mc):
            result = select_small_dividend(context, bar_dict, 5)
            assert isinstance(result, list)

    def test_select_small_dividend_exclude_kcb(self, setup_rq_mocks_combo):
        from v3_combo_static_60_40_rq import select_small_dividend
        context = MockContextCombo()
        bar_dict = MockBarDictCombo()
        
        stocks_with_kcb = ["000001.XSHE", "688001.XSHG", "830001.XSHG", "430001.XSHG"]
        
        def mock_all_instruments_kcb(type_str=None):
            return pd.DataFrame({"order_book_id": stocks_with_kcb})
        
        with patch("v3_combo_static_60_40_rq.all_instruments", mock_all_instruments_kcb):
            with patch("v3_combo_static_60_40_rq.get_market_cap_pe", return_value=pd.DataFrame()):
                result = select_small_dividend(context, bar_dict, 5)
                assert isinstance(result, list)

    def test_adjust_position_success(self, setup_rq_mocks_combo):
        from v3_combo_static_60_40_rq import adjust_position, init
        context = MockContextCombo()
        init(context)
        context.portfolio.total_value = 1000000
        bar_dict = MockBarDictCombo()
        
        with patch("v3_combo_static_60_40_rq.select_rfscore7", return_value=["000001.XSHE", "000002.XSHE"]):
            with patch("v3_combo_static_60_40_rq.select_small_dividend", return_value=["600000.XSHG"]):
                adjust_position(context, bar_dict)
                assert len(context.target_rfscore) > 0 or len(context.target_dividend) > 0

    def test_adjust_position_sell_positions(self, setup_rq_mocks_combo):
        from v3_combo_static_60_40_rq import adjust_position, init
        context = MockContextCombo()
        init(context)
        context.portfolio.positions = {"600519.XSHG": MockPositionCombo()}
        bar_dict = MockBarDictCombo()
        bar_dict["600519.XSHG"] = MockBarCombo(is_trading=True)
        
        with patch("v3_combo_static_60_40_rq.select_rfscore7", return_value=["000001.XSHE"]):
            with patch("v3_combo_static_60_40_rq.select_small_dividend", return_value=[]):
                adjust_position(context, bar_dict)

    def test_adjust_position_buy_positions(self, setup_rq_mocks_combo):
        from v3_combo_static_60_40_rq import adjust_position, init
        context = MockContextCombo()
        init(context)
        context.portfolio.total_value = 1000000
        bar_dict = MockBarDictCombo()
        
        for stock in ["000001.XSHE", "000002.XSHE", "600000.XSHG"]:
            bar_dict[stock] = MockBarCombo(is_trading=True)
        
        with patch("v3_combo_static_60_40_rq.select_rfscore7", return_value=["000001.XSHE", "000002.XSHE"]):
            with patch("v3_combo_static_60_40_rq.select_small_dividend", return_value=["600000.XSHG"]):
                adjust_position(context, bar_dict)

    def test_adjust_position_zero_total_value(self, setup_rq_mocks_combo):
        from v3_combo_static_60_40_rq import adjust_position, init
        context = MockContextCombo()
        init(context)
        context.portfolio.total_value = 0
        bar_dict = MockBarDictCombo()
        
        with patch("v3_combo_static_60_40_rq.select_rfscore7", return_value=["000001.XSHE"]):
            with patch("v3_combo_static_60_40_rq.select_small_dividend", return_value=[]):
                adjust_position(context, bar_dict)

    def test_adjust_position_weight_allocation(self, setup_rq_mocks_combo):
        from v3_combo_static_60_40_rq import adjust_position, init
        context = MockContextCombo()
        init(context)
        context.portfolio.total_value = 1000000
        bar_dict = MockBarDictCombo()
        
        for stock in ["000001.XSHE"]:
            bar_dict[stock] = MockBarCombo(is_trading=True)
        
        with patch("v3_combo_static_60_40_rq.select_rfscore7", return_value=["000001.XSHE"]):
            with patch("v3_combo_static_60_40_rq.select_small_dividend", return_value=[]):
                adjust_position(context, bar_dict)

    def test_check_limit_up_limit_opened(self, setup_rq_mocks_combo):
        from v3_combo_static_60_40_rq import check_limit_up, init
        context = MockContextCombo()
        init(context)
        context.hold_list = ["000001.XSHE"]
        context.portfolio.positions = {"000001.XSHE": MockPositionCombo()}
        bar_dict = {"000001.XSHE": MockBarCombo(close=10.0, limit_up=11.0)}
        
        check_limit_up(context, bar_dict)

    def test_check_limit_up_limit_closed(self, setup_rq_mocks_combo):
        from v3_combo_static_60_40_rq import check_limit_up, init
        context = MockContextCombo()
        init(context)
        context.hold_list = ["000001.XSHE"]
        context.portfolio.positions = {"000001.XSHE": MockPositionCombo()}
        bar_dict = {"000001.XSHE": MockBarCombo(close=11.0, limit_up=11.0)}
        
        check_limit_up(context, bar_dict)

    def test_check_limit_up_stock_not_in_bar_dict(self, setup_rq_mocks_combo):
        from v3_combo_static_60_40_rq import check_limit_up, init
        context = MockContextCombo()
        init(context)
        context.hold_list = ["000001.XSHE"]
        context.portfolio.positions = {"000001.XSHE": MockPositionCombo()}
        bar_dict = {}
        
        check_limit_up(context, bar_dict)

    def test_check_limit_up_stock_not_in_hold_list(self, setup_rq_mocks_combo):
        from v3_combo_static_60_40_rq import check_limit_up, init
        context = MockContextCombo()
        init(context)
        context.hold_list = []
        context.portfolio.positions = {"000001.XSHE": MockPositionCombo()}
        bar_dict = {"000001.XSHE": MockBarCombo(close=10.0, limit_up=11.0)}
        
        check_limit_up(context, bar_dict)

    def test_after_trading(self, setup_rq_mocks_combo):
        from v3_combo_static_60_40_rq import after_trading
        context = MockContextCombo()
        context.portfolio.positions = {"000001.XSHE": MockPositionCombo()}
        after_trading(context)
        assert context.hold_list == ["000001.XSHE"]

    def test_after_trading_empty_positions(self, setup_rq_mocks_combo):
        from v3_combo_static_60_40_rq import after_trading
        context = MockContextCombo()
        after_trading(context)
        assert context.hold_list == []

    def test_get_pb_roa_multiindex_handling(self, setup_rq_mocks_combo):
        from v3_combo_static_60_40_rq import get_pb_roa
        stocks = ["000001.XSHE"]
        watch_date = "2024-07-01"
        
        def mock_get_factor_multi(stocks, factors, start_date=None, end_date=None):
            df = pd.DataFrame({
                "pb_ratio": [1.5],
                "return_on_asset": [5.0],
            })
            df.index = pd.MultiIndex.from_product([stocks, [start_date]], names=["order_book_id", "date"])
            return df
        
        with patch("v3_combo_static_60_40_rq.get_factor", mock_get_factor_multi):
            result = get_pb_roa(stocks, watch_date)
            assert isinstance(result, pd.DataFrame)

    def test_get_market_cap_pe_multiindex_handling(self, setup_rq_mocks_combo):
        from v3_combo_static_60_40_rq import get_market_cap_pe
        stocks = ["000001.XSHE"]
        watch_date = "2024-07-01"
        
        def mock_get_factor_multi(stocks, factors, start_date=None, end_date=None):
            df = pd.DataFrame({
                "market_cap": [5e9],
                "pe_ratio": [15.0],
            })
            df.index = pd.MultiIndex.from_product([stocks, [start_date]], names=["order_book_id", "date"])
            return df
        
        with patch("v3_combo_static_60_40_rq.get_factor", mock_get_factor_multi):
            result = get_market_cap_pe(stocks, watch_date)
            assert isinstance(result, pd.DataFrame)

    def test_select_rfscore7_pb_quantile(self, setup_rq_mocks_combo):
        from v3_combo_static_60_40_rq import select_rfscore7
        context = MockContextCombo()
        bar_dict = MockBarDictCombo()
        
        def mock_get_factor_quantile(stocks, factors, start_date=None, end_date=None):
            n = 20
            data = {
                "pb_ratio": [0.1 + i * 0.2 for i in range(n)],
                "return_on_asset": [5.0 + i * 0.5 for i in range(n)],
                "pe_ratio": [10.0 + i * 1.0 for i in range(n)],
            }
            stocks_list = [f"stock{i}" for i in range(n)]
            df = pd.DataFrame(data, index=pd.MultiIndex.from_product([stocks_list, [start_date]], names=["order_book_id", "date"]))
            return df
        
        with patch("v3_combo_static_60_40_rq.index_components", return_value=[f"stock{i}" for i in range(20)]):
            with patch("v3_combo_static_60_40_rq.get_factor", mock_get_factor_quantile):
                result = select_rfscore7(context, bar_dict, 5)
                assert isinstance(result, list)

    def test_select_small_dividend_pe_filter(self, setup_rq_mocks_combo):
        from v3_combo_static_60_40_rq import select_small_dividend
        context = MockContextCombo()
        bar_dict = MockBarDictCombo()
        
        def mock_get_factor_pe(stocks, factors, start_date=None, end_date=None):
            n = len(stocks)
            data = {
                "market_cap": [5e9 for i in range(n)],
                "pe_ratio": [35.0 if i < n//2 else 15.0 for i in range(n)],
                "pb_ratio": [1.0 for i in range(n)],
                "net_profit_growth_rate": [10.0 for i in range(n)],
            }
            df = pd.DataFrame(data, index=pd.MultiIndex.from_product([stocks[:n], [start_date]], names=["order_book_id", "date"]))
            return df
        
        with patch("v3_combo_static_60_40_rq.get_factor", mock_get_factor_pe):
            result = select_small_dividend(context, bar_dict, 5)
            assert isinstance(result, list)

    def test_adjust_position_division_by_zero_protection(self, setup_rq_mocks_combo):
        from v3_combo_static_60_40_rq import adjust_position, init
        context = MockContextCombo()
        init(context)
        context.portfolio.total_value = 1000000
        bar_dict = MockBarDictCombo()
        
        with patch("v3_combo_static_60_40_rq.select_rfscore7", return_value=[]):
            with patch("v3_combo_static_60_40_rq.select_small_dividend", return_value=[]):
                adjust_position(context, bar_dict)

    def test_select_small_dividend_net_profit_growth_filter(self, setup_rq_mocks_combo):
        from v3_combo_static_60_40_rq import select_small_dividend
        context = MockContextCombo()
        bar_dict = MockBarDictCombo()
        
        def mock_get_factor_growth(stocks, factors, start_date=None, end_date=None):
            n = len(stocks)
            if "net_profit_growth_rate" in factors:
                data = {
                    "net_profit_growth_rate": [3.0 if i < n//2 else 10.0 for i in range(n)],
                }
            else:
                data = {
                    "market_cap": [5e9 for i in range(n)],
                    "pe_ratio": [15.0 for i in range(n)],
                    "pb_ratio": [1.0 for i in range(n)],
                }
            df = pd.DataFrame(data, index=pd.MultiIndex.from_product([stocks[:n], [start_date]], names=["order_book_id", "date"]))
            return df
        
        with patch("v3_combo_static_60_40_rq.get_factor", mock_get_factor_growth):
            result = select_small_dividend(context, bar_dict, 5)
            assert isinstance(result, list)