"""
test_market_data_futures.py
期货数据获取模块单元测试

覆盖:
- parse_future_contract: 合约代码解析
- get_future_contracts: 获取合约列表 (CFFEX 路径无需网络)
- get_dominant_contract: 获取主力合约
- get_contract_multiplier: 合约乘数
- get_margin_rate: 保证金比例
- calculate_position_value: 持仓价值计算
- calculate_required_margin: 保证金计算
- get_future_daily: 期货日线数据
- get_future_spot: 期货实时行情
- _generate_index_future_months: 月份生成
- _get_expire_date: 到期日计算
"""

import unittest
import pandas as pd
import numpy as np
from datetime import datetime
from unittest.mock import patch, MagicMock
import warnings

warnings.filterwarnings("ignore")

from jk2bt.market_data.futures import (
    parse_future_contract,
    get_future_contracts,
    get_dominant_contract,
    get_contract_multiplier,
    get_margin_rate,
    calculate_position_value,
    calculate_required_margin,
    get_future_daily,
    get_future_spot,
    CHINA_FUTURE_EXCHANGE_INFO,
    INDEX_FUTURE_PRODUCT_MAP,
    PRODUCT_TO_INDEX_CODE,
    _generate_index_future_months,
    _get_expire_date,
)


class TestParseFutureContract(unittest.TestCase):
    """测试合约代码解析"""

    def test_parse_index_future_if(self):
        result = parse_future_contract("IF2312")
        self.assertIsNotNone(result)
        self.assertEqual(result["product"], "IF")
        self.assertEqual(result["year"], "23")
        self.assertEqual(result["month"], "12")
        self.assertEqual(result["exchange"], "CFFEX")
        self.assertEqual(result["full_code"], "IF2312")

    def test_parse_index_future_ic(self):
        result = parse_future_contract("IC2401")
        self.assertIsNotNone(result)
        self.assertEqual(result["product"], "IC")
        self.assertEqual(result["exchange"], "CFFEX")

    def test_parse_index_future_ih(self):
        result = parse_future_contract("IH2306")
        self.assertIsNotNone(result)
        self.assertEqual(result["product"], "IH")
        self.assertEqual(result["exchange"], "CFFEX")

    def test_parse_index_future_im(self):
        result = parse_future_contract("IM2403")
        self.assertIsNotNone(result)
        self.assertEqual(result["product"], "IM")
        self.assertEqual(result["exchange"], "CFFEX")

    def test_parse_commodity_shfe(self):
        result = parse_future_contract("AU2312")
        self.assertIsNotNone(result)
        self.assertEqual(result["product"], "AU")
        self.assertEqual(result["exchange"], "SHFE")

    def test_parse_commodity_dce(self):
        result = parse_future_contract("M2401")
        self.assertIsNotNone(result)
        self.assertEqual(result["product"], "M")
        self.assertEqual(result["exchange"], "DCE")

    def test_parse_commodity_czce(self):
        result = parse_future_contract("CF2312")
        self.assertIsNotNone(result)
        self.assertEqual(result["product"], "CF")
        self.assertEqual(result["exchange"], "CZCE")

    def test_parse_commodity_ine(self):
        result = parse_future_contract("SC2401")
        self.assertIsNotNone(result)
        self.assertEqual(result["product"], "SC")
        self.assertEqual(result["exchange"], "INE")

    def test_parse_with_ccfx_suffix(self):
        result = parse_future_contract("IF2312.CCFX")
        self.assertIsNotNone(result)
        self.assertEqual(result["product"], "IF")
        self.assertEqual(result["full_code"], "IF2312")

    def test_parse_lowercase(self):
        result = parse_future_contract("if2312")
        self.assertIsNotNone(result)
        self.assertEqual(result["product"], "IF")

    def test_parse_with_whitespace(self):
        result = parse_future_contract("  IF2312  ")
        self.assertIsNotNone(result)
        self.assertEqual(result["product"], "IF")

    def test_parse_invalid_format(self):
        result = parse_future_contract("INVALID")
        self.assertIsNone(result)

    def test_parse_invalid_format2(self):
        result = parse_future_contract("IF23")
        self.assertIsNone(result)

    def test_parse_invalid_format3(self):
        result = parse_future_contract("IF23123")
        self.assertIsNone(result)

    def test_parse_unknown_product(self):
        result = parse_future_contract("XX2312")
        self.assertIsNotNone(result)
        self.assertEqual(result["product"], "XX")
        self.assertIsNone(result["exchange"])


class TestGenerateIndexFutureMonths(unittest.TestCase):
    """测试股指期货月份生成"""

    def test_generate_months_normal(self):
        months = _generate_index_future_months(2023, 12)
        self.assertEqual(len(months), 4)
        self.assertIn((2023, 12), months)

    def test_generate_months_mid_year(self):
        months = _generate_index_future_months(2023, 6)
        self.assertEqual(len(months), 4)
        self.assertIn((2023, 6), months)

    def test_generate_months_quarter(self):
        months = _generate_index_future_months(2023, 3)
        self.assertEqual(len(months), 4)
        self.assertIn((2023, 3), months)

    def test_generate_months_january(self):
        months = _generate_index_future_months(2024, 1)
        self.assertEqual(len(months), 4)
        self.assertIn((2024, 1), months)


class TestGetExpireDate(unittest.TestCase):
    """测试到期日计算"""

    def test_expire_date_known(self):
        expire = _get_expire_date(2023, 12)
        self.assertEqual(expire.day, 15)

    def test_expire_date_known2(self):
        expire = _get_expire_date(2024, 3)
        self.assertEqual(expire.day, 15)

    def test_expire_date_is_friday(self):
        expire = _get_expire_date(2023, 12)
        self.assertEqual(expire.weekday(), 4)

    def test_expire_date_type(self):
        expire = _get_expire_date(2024, 6)
        self.assertIsInstance(expire, datetime)


class TestGetFutureContracts(unittest.TestCase):
    """测试获取期货合约列表"""

    def test_get_cffex_contracts_by_product(self):
        df = get_future_contracts(product="IF", date="2023-12-01")
        self.assertIsInstance(df, pd.DataFrame)
        self.assertFalse(df.empty)
        self.assertIn("contract", df.columns)
        self.assertIn("product", df.columns)
        self.assertIn("exchange", df.columns)
        self.assertTrue(all(c.startswith("IF") for c in df["contract"]))
        self.assertTrue(all(e == "CFFEX" for e in df["exchange"]))

    def test_get_cffex_all_products(self):
        df = get_future_contracts(exchange="CFFEX", date="2023-12-01")
        self.assertIsInstance(df, pd.DataFrame)
        self.assertFalse(df.empty)
        products = df["product"].unique()
        for p in ["IF", "IC", "IH", "IM"]:
            self.assertIn(p, products)

    def test_get_contracts_include_expired(self):
        df = get_future_contracts(product="IF", date="2023-01-01", include_expired=True)
        self.assertIsInstance(df, pd.DataFrame)

    def test_get_contracts_exclude_expired(self):
        df = get_future_contracts(
            product="IF", date="2023-01-01", include_expired=False
        )
        self.assertIsInstance(df, pd.DataFrame)

    def test_get_contracts_columns(self):
        df = get_future_contracts(product="IC", date="2024-06-01")
        expected_cols = {
            "contract",
            "product",
            "exchange",
            "year",
            "month",
            "is_trading",
            "expire_date",
        }
        self.assertTrue(expected_cols.issubset(set(df.columns)))

    def test_get_contracts_invalid_product(self):
        df = get_future_contracts(product="ZZ", date="2023-12-01")
        self.assertIsInstance(df, pd.DataFrame)
        self.assertTrue(df.empty)

    @patch("jk2bt.market_data.futures._get_adapter")
    def test_get_exchange_contracts_empty_adapter(self, mock_get_adapter):
        mock_adapter = MagicMock()
        mock_adapter.get_futures_spot.return_value = pd.DataFrame()
        mock_get_adapter.return_value = mock_adapter

        df = get_future_contracts(exchange="SHFE", date="2023-12-01")
        self.assertIsInstance(df, pd.DataFrame)
        self.assertTrue(df.empty)

    @patch("jk2bt.market_data.futures._get_adapter")
    def test_get_exchange_contracts_with_data(self, mock_get_adapter):
        spot_df = pd.DataFrame(
            {
                "symbol": ["AU2312", "AG2401", "CU2312"],
                "exchange": ["XSHFE", "XSHFE", "XSHFE"],
                "volume": [1000, 2000, 3000],
            }
        )
        mock_adapter = MagicMock()
        mock_adapter.get_futures_spot.return_value = spot_df
        mock_get_adapter.return_value = mock_adapter

        df = get_future_contracts(exchange="SHFE", date="2023-12-01")
        self.assertIsInstance(df, pd.DataFrame)
        self.assertFalse(df.empty)
        self.assertTrue(all(e == "SHFE" for e in df["exchange"]))

    @patch("jk2bt.market_data.futures._get_adapter")
    def test_get_all_contracts_adapter_empty(self, mock_get_adapter):
        mock_adapter = MagicMock()
        mock_adapter.get_futures_spot.return_value = pd.DataFrame()
        mock_get_adapter.return_value = mock_adapter

        df = get_future_contracts(date="2023-12-01")
        self.assertIsInstance(df, pd.DataFrame)


class TestGetDominantContract(unittest.TestCase):
    """测试获取主力合约"""

    @patch("jk2bt.market_data.futures._get_adapter")
    def test_get_index_dominant_with_spot_data(self, mock_get_adapter):
        spot_df = pd.DataFrame(
            {
                "symbol": ["IF2312", "IF2401", "IF2403"],
                "volume": [10000, 50000, 20000],
            }
        )
        mock_adapter = MagicMock()
        mock_adapter.get_futures_spot.return_value = spot_df
        mock_get_adapter.return_value = mock_adapter

        contract = get_dominant_contract("IF", date="2023-12-01")
        self.assertIsNotNone(contract)
        self.assertTrue(contract.startswith("IF"))

    @patch("jk2bt.market_data.futures._get_adapter")
    def test_get_index_dominant_empty_spot(self, mock_get_adapter):
        mock_adapter = MagicMock()
        mock_adapter.get_futures_spot.return_value = pd.DataFrame()
        mock_get_adapter.return_value = mock_adapter

        contract = get_dominant_contract("IF", date="2023-12-01")
        self.assertIsNotNone(contract)
        self.assertTrue(contract.startswith("IF"))

    @patch("jk2bt.market_data.futures._get_adapter")
    def test_get_commodity_dominant(self, mock_get_adapter):
        spot_df = pd.DataFrame(
            {
                "symbol": ["AU2312", "AU2401", "AU2403"],
                "volume": [10000, 50000, 20000],
            }
        )
        mock_adapter = MagicMock()
        mock_adapter.get_futures_spot.return_value = spot_df
        mock_get_adapter.return_value = mock_adapter

        contract = get_dominant_contract("AU")
        self.assertIsNotNone(contract)
        self.assertTrue(contract.startswith("AU"))

    @patch("jk2bt.market_data.futures._get_adapter")
    def test_get_commodity_dominant_empty(self, mock_get_adapter):
        mock_adapter = MagicMock()
        mock_adapter.get_futures_spot.return_value = pd.DataFrame()
        mock_get_adapter.return_value = mock_adapter

        contract = get_dominant_contract("AU")
        self.assertIsNone(contract)

    @patch("jk2bt.market_data.futures._get_adapter")
    def test_get_dominant_exception_handling(self, mock_get_adapter):
        mock_adapter = MagicMock()
        mock_adapter.get_futures_spot.side_effect = Exception("network error")
        mock_get_adapter.return_value = mock_adapter

        contract = get_dominant_contract("IF", date="2023-12-01")
        self.assertIsNotNone(contract)
        self.assertTrue(contract.startswith("IF"))


class TestContractMultiplier(unittest.TestCase):
    """测试合约乘数"""

    def test_if_multiplier(self):
        self.assertEqual(get_contract_multiplier("IF2312"), 300)

    def test_ic_multiplier(self):
        self.assertEqual(get_contract_multiplier("IC2401"), 200)

    def test_ih_multiplier(self):
        self.assertEqual(get_contract_multiplier("IH2306"), 300)

    def test_im_multiplier(self):
        self.assertEqual(get_contract_multiplier("IM2403"), 200)

    def test_au_multiplier(self):
        self.assertEqual(get_contract_multiplier("AU2312"), 1000)

    def test_rb_multiplier(self):
        self.assertEqual(get_contract_multiplier("RB2312"), 10)

    def test_sc_multiplier(self):
        self.assertEqual(get_contract_multiplier("SC2401"), 1000)

    def test_invalid_contract(self):
        self.assertIsNone(get_contract_multiplier("INVALID"))

    def test_unknown_product(self):
        self.assertIsNone(get_contract_multiplier("XX2312"))

    def test_with_ccfx_suffix(self):
        self.assertEqual(get_contract_multiplier("IF2312.CCFX"), 300)


class TestMarginRate(unittest.TestCase):
    """测试保证金比例"""

    def test_if_margin(self):
        self.assertEqual(get_margin_rate("IF2312"), 0.12)

    def test_ic_margin(self):
        self.assertEqual(get_margin_rate("IC2401"), 0.14)

    def test_ih_margin(self):
        self.assertEqual(get_margin_rate("IH2306"), 0.12)

    def test_im_margin(self):
        self.assertEqual(get_margin_rate("IM2403"), 0.14)

    def test_au_margin(self):
        self.assertEqual(get_margin_rate("AU2312"), 0.08)

    def test_sc_margin(self):
        self.assertEqual(get_margin_rate("SC2401"), 0.10)

    def test_invalid_contract(self):
        self.assertIsNone(get_margin_rate("INVALID"))

    def test_unknown_product(self):
        self.assertIsNone(get_margin_rate("XX2312"))


class TestPositionValueCalculation(unittest.TestCase):
    """测试持仓价值计算"""

    def test_basic_calculation(self):
        value = calculate_position_value(4000, 10, "IF2312")
        self.assertEqual(value, 4000 * 300 * 10)

    def test_negative_quantity(self):
        value = calculate_position_value(4000, -10, "IF2312")
        self.assertEqual(value, 4000 * 300 * 10)

    def test_single_contract(self):
        value = calculate_position_value(5000, 1, "IC2401")
        self.assertEqual(value, 5000 * 200 * 1)

    def test_commodity_future(self):
        value = calculate_position_value(500, 5, "AU2312")
        self.assertEqual(value, 500 * 1000 * 5)

    def test_invalid_contract(self):
        self.assertIsNone(calculate_position_value(4000, 10, "INVALID"))

    def test_zero_quantity(self):
        value = calculate_position_value(4000, 0, "IF2312")
        self.assertEqual(value, 0)

    def test_float_price(self):
        value = calculate_position_value(3999.5, 10, "IF2312")
        self.assertAlmostEqual(value, 3999.5 * 300 * 10)


class TestRequiredMarginCalculation(unittest.TestCase):
    """测试保证金计算"""

    def test_basic_margin(self):
        margin = calculate_required_margin(4000, 10, "IF2312")
        expected = 4000 * 300 * 10 * 0.12
        self.assertEqual(margin, expected)

    def test_ic_margin(self):
        margin = calculate_required_margin(5000, 5, "IC2401")
        expected = 5000 * 200 * 5 * 0.14
        self.assertEqual(margin, expected)

    def test_commodity_margin(self):
        margin = calculate_required_margin(500, 5, "AU2312")
        expected = 500 * 1000 * 5 * 0.08
        self.assertEqual(margin, expected)

    def test_invalid_contract(self):
        self.assertIsNone(calculate_required_margin(4000, 10, "INVALID"))


class TestGetFutureDaily(unittest.TestCase):
    """测试期货日线数据"""

    @patch("jk2bt.market_data.futures._get_adapter")
    def test_get_future_daily_basic(self, mock_get_adapter):
        daily_df = pd.DataFrame(
            {
                "date": ["2023-11-01", "2023-11-02", "2023-11-03"],
                "open": [3800, 3850, 3900],
                "high": [3850, 3900, 3950],
                "low": [3780, 3820, 3870],
                "close": [3830, 3880, 3920],
                "volume": [10000, 12000, 11000],
                "openinterest": [5000, 5100, 5200],
                "settle": [3825, 3875, 3915],
            }
        )
        mock_adapter = MagicMock()
        mock_adapter.get_futures_daily.return_value = daily_df
        mock_get_adapter.return_value = mock_adapter

        df = get_future_daily("IF2312", start_date="2023-11-01", end_date="2023-11-03")
        self.assertIsInstance(df, pd.DataFrame)
        self.assertFalse(df.empty)
        self.assertIn("datetime", df.columns)
        self.assertIn("close", df.columns)
        self.assertEqual(len(df), 3)

    @patch("jk2bt.market_data.futures._get_adapter")
    def test_get_future_daily_chinese_columns(self, mock_get_adapter):
        daily_df = pd.DataFrame(
            {
                "日期": ["2023-11-01", "2023-11-02"],
                "开盘": [3800, 3850],
                "最高": [3850, 3900],
                "最低": [3780, 3820],
                "收盘": [3830, 3880],
                "成交量": [10000, 12000],
                "持仓量": [5000, 5100],
                "结算价": [3825, 3875],
            }
        )
        mock_adapter = MagicMock()
        mock_adapter.get_futures_daily.return_value = daily_df
        mock_get_adapter.return_value = mock_adapter

        df = get_future_daily("IF2312", start_date="2023-11-01", end_date="2023-11-02")
        self.assertFalse(df.empty)
        self.assertIn("datetime", df.columns)
        self.assertIn("open", df.columns)
        self.assertIn("high", df.columns)
        self.assertIn("low", df.columns)
        self.assertIn("close", df.columns)
        self.assertIn("volume", df.columns)

    @patch("jk2bt.market_data.futures._get_adapter")
    def test_get_future_daily_empty(self, mock_get_adapter):
        mock_adapter = MagicMock()
        mock_adapter.get_futures_daily.return_value = pd.DataFrame()
        mock_get_adapter.return_value = mock_adapter

        df = get_future_daily("IF2312")
        self.assertIsInstance(df, pd.DataFrame)
        self.assertTrue(df.empty)

    @patch("jk2bt.market_data.futures._get_adapter")
    def test_get_future_daily_date_filter(self, mock_get_adapter):
        daily_df = pd.DataFrame(
            {
                "date": ["2023-10-01", "2023-11-01", "2023-12-01"],
                "open": [3700, 3800, 3900],
                "high": [3750, 3850, 3950],
                "low": [3680, 3780, 3870],
                "close": [3730, 3830, 3920],
                "volume": [9000, 10000, 11000],
            }
        )
        mock_adapter = MagicMock()
        mock_adapter.get_futures_daily.return_value = daily_df
        mock_get_adapter.return_value = mock_adapter

        df = get_future_daily("IF2312", start_date="2023-11-01", end_date="2023-11-30")
        self.assertEqual(len(df), 1)

    @patch("jk2bt.market_data.futures._get_adapter")
    def test_get_future_daily_sorted(self, mock_get_adapter):
        daily_df = pd.DataFrame(
            {
                "date": ["2023-11-03", "2023-11-01", "2023-11-02"],
                "open": [3900, 3800, 3850],
                "high": [3950, 3850, 3900],
                "low": [3870, 3780, 3820],
                "close": [3920, 3830, 3880],
                "volume": [11000, 10000, 12000],
            }
        )
        mock_adapter = MagicMock()
        mock_adapter.get_futures_daily.return_value = daily_df
        mock_get_adapter.return_value = mock_adapter

        df = get_future_daily("IF2312")
        dates = df["datetime"].tolist()
        self.assertLessEqual(dates[0], dates[1])
        self.assertLessEqual(dates[1], dates[2])

    @patch("jk2bt.market_data.futures._get_adapter")
    def test_get_future_daily_missing_openinterest(self, mock_get_adapter):
        daily_df = pd.DataFrame(
            {
                "date": ["2023-11-01"],
                "open": [3800],
                "high": [3850],
                "low": [3780],
                "close": [3830],
                "volume": [10000],
            }
        )
        mock_adapter = MagicMock()
        mock_adapter.get_futures_daily.return_value = daily_df
        mock_get_adapter.return_value = mock_adapter

        df = get_future_daily("IF2312")
        self.assertIn("openinterest", df.columns)
        self.assertEqual(df["openinterest"].iloc[0], 0)

    @patch("jk2bt.market_data.futures._get_adapter")
    def test_get_future_daily_with_ccfx_suffix(self, mock_get_adapter):
        daily_df = pd.DataFrame(
            {
                "date": ["2023-11-01"],
                "open": [3800],
                "high": [3850],
                "low": [3780],
                "close": [3830],
                "volume": [10000],
            }
        )
        mock_adapter = MagicMock()
        mock_adapter.get_futures_daily.return_value = daily_df
        mock_get_adapter.return_value = mock_adapter

        df = get_future_daily("IF2312.CCFX")
        mock_adapter.get_futures_daily.assert_called_once_with(symbol="IF2312")

    @patch("jk2bt.market_data.futures._get_adapter")
    def test_get_future_daily_exception(self, mock_get_adapter):
        mock_adapter = MagicMock()
        mock_adapter.get_futures_daily.side_effect = Exception("API error")
        mock_get_adapter.return_value = mock_adapter

        df = get_future_daily("IF2312")
        self.assertIsInstance(df, pd.DataFrame)
        self.assertTrue(df.empty)


class TestGetFutureSpot(unittest.TestCase):
    """测试期货实时行情"""

    @patch("jk2bt.market_data.futures._get_adapter")
    def test_get_future_spot_basic(self, mock_get_adapter):
        spot_df = pd.DataFrame(
            {
                "symbol": ["IF2312", "IC2401", "AU2312"],
                "exchange": ["CFFEX", "CFFEX", "XSHFE"],
                "open": [3800, 5000, 450],
                "high": [3850, 5050, 455],
                "low": [3780, 4980, 448],
                "last_price": [3830, 5020, 452],
                "volume": [10000, 12000, 8000],
                "openinterest": [5000, 6000, 4000],
                "settle": [3825, 5015, 451],
            }
        )
        mock_adapter = MagicMock()
        mock_adapter.get_futures_spot.return_value = spot_df
        mock_get_adapter.return_value = mock_adapter

        df = get_future_spot()
        self.assertIsInstance(df, pd.DataFrame)
        self.assertFalse(df.empty)
        self.assertIn("symbol", df.columns)
        self.assertEqual(len(df), 3)

    @patch("jk2bt.market_data.futures._get_adapter")
    def test_get_future_spot_filter_by_contract(self, mock_get_adapter):
        spot_df = pd.DataFrame(
            {
                "symbol": ["IF2312", "IC2401", "AU2312"],
                "exchange": ["CFFEX", "CFFEX", "XSHFE"],
                "open": [3800, 5000, 450],
                "high": [3850, 5050, 455],
                "low": [3780, 4980, 448],
                "last_price": [3830, 5020, 452],
                "volume": [10000, 12000, 8000],
            }
        )
        mock_adapter = MagicMock()
        mock_adapter.get_futures_spot.return_value = spot_df
        mock_get_adapter.return_value = mock_adapter

        df = get_future_spot("IF2312")
        self.assertEqual(len(df), 1)
        self.assertEqual(df.iloc[0]["symbol"], "IF2312")

    @patch("jk2bt.market_data.futures._get_adapter")
    def test_get_future_spot_empty(self, mock_get_adapter):
        mock_adapter = MagicMock()
        mock_adapter.get_futures_spot.return_value = pd.DataFrame()
        mock_get_adapter.return_value = mock_adapter

        df = get_future_spot()
        self.assertIsInstance(df, pd.DataFrame)
        self.assertTrue(df.empty)

    @patch("jk2bt.market_data.futures._get_adapter")
    def test_get_future_spot_chinese_columns(self, mock_get_adapter):
        spot_df = pd.DataFrame(
            {
                "symbol": ["IF2312"],
                "exchange": ["CFFEX"],
                "开盘价": [3800],
                "最高价": [3850],
                "最低价": [3780],
                "最新价": [3830],
                "成交量": [10000],
                "持仓量": [5000],
                "结算价": [3825],
            }
        )
        mock_adapter = MagicMock()
        mock_adapter.get_futures_spot.return_value = spot_df
        mock_get_adapter.return_value = mock_adapter

        df = get_future_spot()
        self.assertFalse(df.empty)
        self.assertIn("open", df.columns)
        self.assertIn("high", df.columns)
        self.assertIn("low", df.columns)
        self.assertIn("last_price", df.columns)

    @patch("jk2bt.market_data.futures._get_adapter")
    def test_get_future_spot_exception(self, mock_get_adapter):
        mock_adapter = MagicMock()
        mock_adapter.get_futures_spot.side_effect = Exception("API error")
        mock_get_adapter.return_value = mock_adapter

        df = get_future_spot()
        self.assertIsInstance(df, pd.DataFrame)
        self.assertTrue(df.empty)


class TestConstants(unittest.TestCase):
    """测试常量定义"""

    def test_cffex_info(self):
        cffex = CHINA_FUTURE_EXCHANGE_INFO["CFFEX"]
        self.assertEqual(cffex["name"], "中国金融期货交易所")
        self.assertIn("IF", cffex["products"])
        self.assertEqual(cffex["multipliers"]["IF"], 300)
        self.assertEqual(cffex["margin_rates"]["IF"], 0.12)

    def test_all_exchanges_have_multipliers(self):
        for exchange, info in CHINA_FUTURE_EXCHANGE_INFO.items():
            for product in info["products"]:
                self.assertIn(product, info["multipliers"])

    def test_all_exchanges_have_margin_rates(self):
        for exchange, info in CHINA_FUTURE_EXCHANGE_INFO.items():
            for product in info["products"]:
                self.assertIn(product, info["margin_rates"])

    def test_index_future_product_map(self):
        self.assertEqual(INDEX_FUTURE_PRODUCT_MAP["IF"], "沪深300股指期货")
        self.assertEqual(INDEX_FUTURE_PRODUCT_MAP["IC"], "中证500股指期货")
        self.assertEqual(INDEX_FUTURE_PRODUCT_MAP["IH"], "上证50股指期货")
        self.assertEqual(INDEX_FUTURE_PRODUCT_MAP["IM"], "中证1000股指期货")

    def test_product_to_index_code(self):
        self.assertEqual(PRODUCT_TO_INDEX_CODE["IF"], "000300.XSHG")
        self.assertEqual(PRODUCT_TO_INDEX_CODE["IC"], "000905.XSHG")
        self.assertEqual(PRODUCT_TO_INDEX_CODE["IH"], "000016.XSHG")
        self.assertEqual(PRODUCT_TO_INDEX_CODE["IM"], "000852.XSHG")


if __name__ == "__main__":
    unittest.main(verbosity=2)
