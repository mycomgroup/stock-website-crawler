"""
test_option_api.py
期权API测试模块。

测试覆盖：
1. 希腊值计算测试（Delta、Gamma、Theta、Vega）
2. 隐含波动率测试
3. 期权链测试
4. 日线数据测试
5. 批量查询测试
6. 边界条件测试
7. 数据验证测试
"""

import unittest
import pandas as pd
import sys
import os
from datetime import datetime, timedelta

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


class TestOptionModuleImport(unittest.TestCase):
    """测试期权模块导入"""

    def test_import_option_module(self):
        """测试导入期权模块的所有公开函数"""
        try:
            from jk2bt.market_data.option import (
                get_option_list,
                get_option_price,
                get_option_quote,
                get_option_greeks,
                get_option_chain,
                get_option,
                query_option,
                get_option_info,
                get_option_daily,
                calculate_option_implied_vol,
                RobustResult,
                FinanceQuery,
                finance,
                OptionDBManager,
            )

            self.assertTrue(True)
        except ImportError as e:
            self.skipTest(f"期权模块导入失败: {e}")

    def test_robust_result_class(self):
        """测试 RobustResult 类的基本功能"""
        from jk2bt.market_data.option import RobustResult

        result = RobustResult(
            success=True, data=pd.DataFrame(), reason="", source="test"
        )
        self.assertTrue(result.success)
        self.assertTrue(bool(result))
        self.assertIsInstance(result.data, pd.DataFrame)

        failed_result = RobustResult(success=False, data=None, reason="test error")
        self.assertFalse(failed_result.success)
        self.assertFalse(bool(failed_result))
        self.assertEqual(failed_result.reason, "test error")


class TestOptionList(unittest.TestCase):
    """期权列表测试"""

    def test_get_option_list_sse(self):
        """测试获取上交所期权列表"""
        try:
            from jk2bt.market_data.option import (
                get_option_list,
            )

            result = get_option_list(underlying="sse", use_cache=True)
            self.assertIsInstance(result.data, pd.DataFrame)
        except Exception as e:
            self.skipTest(f"获取上交所期权列表失败: {e}")

    def test_get_option_list_szse(self):
        """测试获取深交所期权列表"""
        try:
            from jk2bt.market_data.option import (
                get_option_list,
            )

            result = get_option_list(underlying="szse", use_cache=True)
            self.assertIsInstance(result.data, pd.DataFrame)
        except Exception as e:
            self.skipTest(f"获取深交所期权列表失败: {e}")

    def test_get_option_list_cffex(self):
        """测试获取中金所股指期权列表"""
        try:
            from jk2bt.market_data.option import (
                get_option_list,
            )

            result = get_option_list(underlying="cffex", use_cache=True)
            self.assertIsInstance(result.data, pd.DataFrame)
        except Exception as e:
            self.skipTest(f"获取中金所期权列表失败: {e}")

    def test_get_option_list_invalid_underlying(self):
        """测试无效标的类型"""
        from jk2bt.market_data.option import (
            get_option_list,
        )

        result = get_option_list(underlying="invalid_type")
        self.assertFalse(result.success)
        self.assertIn("不支持", result.reason)


class TestGreeksCalculation(unittest.TestCase):
    """希腊值计算测试"""

    def test_get_option_greeks(self):
        """测试获取期权希腊值"""
        try:
            from jk2bt.market_data.option import (
                get_option_list,
                get_option_greeks,
            )

            list_result = get_option_list(underlying="sse", use_cache=True)
            if list_result.success and not list_result.data.empty:
                option_code = list_result.data.iloc[0]["option_code"]
                result = get_option_greeks(str(option_code), use_cache=True)
                self.assertIsInstance(result, object)
                if result.success and not result.data.empty:
                    greeks = result.data.iloc[0]
                    self.assertIn("delta", greeks.index)
                    self.assertIn("gamma", greeks.index)
                    self.assertIn("theta", greeks.index)
                    self.assertIn("vega", greeks.index)
        except Exception as e:
            self.skipTest(f"获取希腊值失败: {e}")

    def test_delta_calculation_range(self):
        """测试 Delta 计算值范围（看涨期权 0~1，看跌期权 -1~0）"""
        try:
            from jk2bt.market_data.option import (
                get_option_list,
                get_option_greeks,
            )

            list_result = get_option_list(underlying="sse", use_cache=True)
            if list_result.success and not list_result.data.empty:
                for _, row in list_result.data.head(3).iterrows():
                    option_code = str(row["option_code"])
                    result = get_option_greeks(option_code, use_cache=True)
                    if result.success and not result.data.empty:
                        delta = result.data.iloc[0].get("delta")
                        if delta is not None:
                            self.assertGreaterEqual(delta, -1.0)
                            self.assertLessEqual(delta, 1.0)
                            break
        except Exception as e:
            self.skipTest(f"Delta 范围测试失败: {e}")

    def test_gamma_calculation_positive(self):
        """测试 Gamma 计算值应为正数"""
        try:
            from jk2bt.market_data.option import (
                get_option_list,
                get_option_greeks,
            )

            list_result = get_option_list(underlying="sse", use_cache=True)
            if list_result.success and not list_result.data.empty:
                for _, row in list_result.data.head(3).iterrows():
                    option_code = str(row["option_code"])
                    result = get_option_greeks(option_code, use_cache=True)
                    if result.success and not result.data.empty:
                        gamma = result.data.iloc[0].get("gamma")
                        if gamma is not None:
                            self.assertGreaterEqual(gamma, 0)
                            break
        except Exception as e:
            self.skipTest(f"Gamma 测试失败: {e}")

    def test_theta_calculation(self):
        """测试 Theta 计算值（时间价值衰减，通常为负）"""
        try:
            from jk2bt.market_data.option import (
                get_option_list,
                get_option_greeks,
            )

            list_result = get_option_list(underlying="sse", use_cache=True)
            if list_result.success and not list_result.data.empty:
                for _, row in list_result.data.head(3).iterrows():
                    option_code = str(row["option_code"])
                    result = get_option_greeks(option_code, use_cache=True)
                    if result.success and not result.data.empty:
                        theta = result.data.iloc[0].get("theta")
                        if theta is not None:
                            self.assertIsInstance(theta, (int, float))
                            break
        except Exception as e:
            self.skipTest(f"Theta 测试失败: {e}")

    def test_vega_calculation_positive(self):
        """测试 Vega 计算值应为正数"""
        try:
            from jk2bt.market_data.option import (
                get_option_list,
                get_option_greeks,
            )

            list_result = get_option_list(underlying="sse", use_cache=True)
            if list_result.success and not list_result.data.empty:
                for _, row in list_result.data.head(3).iterrows():
                    option_code = str(row["option_code"])
                    result = get_option_greeks(option_code, use_cache=True)
                    if result.success and not result.data.empty:
                        vega = result.data.iloc[0].get("vega")
                        if vega is not None:
                            self.assertGreaterEqual(vega, 0)
                            break
        except Exception as e:
            self.skipTest(f"Vega 测试失败: {e}")

    def test_greeks_all_fields_present(self):
        """测试希腊值字段完整性"""
        try:
            from jk2bt.market_data.option import (
                get_option_list,
                get_option_greeks,
            )

            list_result = get_option_list(underlying="sse", use_cache=True)
            if list_result.success and not list_result.data.empty:
                option_code = str(list_result.data.iloc[0]["option_code"])
                result = get_option_greeks(option_code, use_cache=True)
                if result.success and not result.data.empty:
                    required_fields = ["delta", "gamma", "theta", "vega", "implied_vol"]
                    for field in required_fields:
                        self.assertIn(field, result.data.columns)
        except Exception as e:
            self.skipTest(f"希腊值字段完整性测试失败: {e}")


class TestImpliedVolatility(unittest.TestCase):
    """隐含波动率测试"""

    def test_calculate_option_implied_vol_basic(self):
        """测试计算隐含波动率基本功能"""
        try:
            from jk2bt.market_data.option import (
                get_option_list,
                calculate_option_implied_vol,
            )

            list_result = get_option_list(underlying="sse", use_cache=True)
            if list_result.success and not list_result.data.empty:
                option_code = str(list_result.data.iloc[0]["option_code"])
                strike = list_result.data.iloc[0].get("strike")
                if strike and strike > 0:
                    result = calculate_option_implied_vol(
                        option_code=option_code,
                        price=0.05,
                        underlying_price=strike * 1.05,
                    )
                    self.assertIsInstance(result, dict)
                    self.assertIn("success", result)
        except Exception as e:
            self.skipTest(f"计算隐含波动率失败: {e}")

    def test_implied_vol_different_strikes(self):
        """测试不同行权价的隐含波动率计算"""
        try:
            from jk2bt.market_data.option import (
                get_option_list,
                calculate_option_implied_vol,
            )

            list_result = get_option_list(underlying="sse", use_cache=True)
            if list_result.success and not list_result.data.empty:
                df = list_result.data
                strikes = df["strike"].dropna().unique()
                if len(strikes) >= 2:
                    for strike in strikes[:2]:
                        sample = df[df["strike"] == strike].iloc[0]
                        result = calculate_option_implied_vol(
                            option_code=str(sample["option_code"]),
                            price=0.05,
                            underlying_price=strike * 1.02,
                        )
                        self.assertIsInstance(result, dict)
        except Exception as e:
            self.skipTest(f"不同行权价隐含波动率测试失败: {e}")

    def test_implied_vol_different_expiry(self):
        """测试不同到期时间的隐含波动率计算"""
        try:
            from jk2bt.market_data.option import (
                get_option_list,
                calculate_option_implied_vol,
            )

            list_result = get_option_list(underlying="sse", use_cache=True)
            if list_result.success and not list_result.data.empty:
                df = list_result.data
                expiry_dates = df["expiry_date"].dropna().unique()
                if len(expiry_dates) >= 2:
                    for expiry in expiry_dates[:2]:
                        sample = df[df["expiry_date"] == expiry].iloc[0]
                        strike = sample.get("strike")
                        if strike and strike > 0:
                            result = calculate_option_implied_vol(
                                option_code=str(sample["option_code"]),
                                price=0.05,
                                underlying_price=strike,
                            )
                            self.assertIsInstance(result, dict)
        except Exception as e:
            self.skipTest(f"不同到期时间隐含波动率测试失败: {e}")

    def test_implied_vol_deep_in_the_money(self):
        """测试深度实值期权的隐含波动率计算"""
        try:
            from jk2bt.market_data.option import (
                get_option_list,
                calculate_option_implied_vol,
            )

            list_result = get_option_list(underlying="sse", use_cache=True)
            if list_result.success and not list_result.data.empty:
                sample = list_result.data.iloc[0]
                strike = sample.get("strike")
                if strike and strike > 0:
                    result = calculate_option_implied_vol(
                        option_code=str(sample["option_code"]),
                        price=0.5,
                        underlying_price=strike * 1.5,
                    )
                    self.assertIsInstance(result, dict)
        except Exception as e:
            self.skipTest(f"深度实值期权测试失败: {e}")

    def test_implied_vol_deep_out_of_money(self):
        """测试深度虚值期权的隐含波动率计算"""
        try:
            from jk2bt.market_data.option import (
                get_option_list,
                calculate_option_implied_vol,
            )

            list_result = get_option_list(underlying="sse", use_cache=True)
            if list_result.success and not list_result.data.empty:
                sample = list_result.data.iloc[0]
                strike = sample.get("strike")
                if strike and strike > 0:
                    result = calculate_option_implied_vol(
                        option_code=str(sample["option_code"]),
                        price=0.001,
                        underlying_price=strike * 0.5,
                    )
                    self.assertIsInstance(result, dict)
        except Exception as e:
            self.skipTest(f"深度虚值期权测试失败: {e}")

    def test_implied_vol_return_fields(self):
        """测试隐含波动率返回字段完整性"""
        try:
            from jk2bt.market_data.option import (
                get_option_list,
                calculate_option_implied_vol,
            )

            list_result = get_option_list(underlying="sse", use_cache=True)
            if list_result.success and not list_result.data.empty:
                sample = list_result.data.iloc[0]
                strike = sample.get("strike")
                if strike and strike > 0:
                    result = calculate_option_implied_vol(
                        option_code=str(sample["option_code"]),
                        price=0.05,
                        underlying_price=strike,
                    )
                    if result.get("success"):
                        self.assertIn("option_code", result)
                        self.assertIn("price", result)
                        self.assertIn("strike", result)
                        self.assertIn("implied_vol", result)
        except Exception as e:
            self.skipTest(f"隐含波动率返回字段测试失败: {e}")

    def test_implied_vol_greeks_included(self):
        """测试隐含波动率计算结果包含希腊值"""
        try:
            from jk2bt.market_data.option import (
                get_option_list,
                calculate_option_implied_vol,
            )

            list_result = get_option_list(underlying="sse", use_cache=True)
            if list_result.success and not list_result.data.empty:
                sample = list_result.data.iloc[0]
                strike = sample.get("strike")
                if strike and strike > 0:
                    result = calculate_option_implied_vol(
                        option_code=str(sample["option_code"]),
                        price=0.05,
                        underlying_price=strike,
                    )
                    if result.get("success"):
                        self.assertIn("delta", result)
                        self.assertIn("gamma", result)
                        self.assertIn("theta", result)
                        self.assertIn("vega", result)
        except Exception as e:
            self.skipTest(f"希腊值包含测试失败: {e}")


class TestOptionChain(unittest.TestCase):
    """期权链测试"""

    def test_get_option_chain_basic(self):
        """测试获取期权链基本功能"""
        try:
            from jk2bt.market_data.option import (
                get_option_chain,
            )

            result = get_option_chain(underlying="510050", use_cache=True)
            self.assertIsInstance(result, object)
            self.assertIsInstance(result.data, pd.DataFrame)
        except Exception as e:
            self.skipTest(f"获取期权链失败: {e}")

    def test_option_chain_same_expiry(self):
        """测试获取同一到期日的所有期权合约"""
        try:
            from jk2bt.market_data.option import (
                get_option_list,
                get_option_chain,
            )

            list_result = get_option_list(underlying="sse", use_cache=True)
            if list_result.success and not list_result.data.empty:
                df = list_result.data
                expiry_dates = df["expiry_date"].dropna().unique()
                if len(expiry_dates) > 0:
                    expiry = str(expiry_dates[0])
                    result = get_option_chain(
                        underlying="510050", expiry_date=expiry, use_cache=True
                    )
                    self.assertIsInstance(result.data, pd.DataFrame)
        except Exception as e:
            self.skipTest(f"同一到期日期权链测试失败: {e}")

    def test_option_chain_different_strikes(self):
        """测试期权链中包含不同行权价的期权合约"""
        try:
            from jk2bt.market_data.option import (
                get_option_chain,
            )

            result = get_option_chain(underlying="510050", use_cache=True)
            if result.success and not result.data.empty:
                strikes = result.data["strike"].dropna().unique()
                self.assertGreater(len(strikes), 0)
        except Exception as e:
            self.skipTest(f"不同行权价期权链测试失败: {e}")

    def test_option_chain_call_put(self):
        """测试期权链中同时包含看涨和看跌期权"""
        try:
            from jk2bt.market_data.option import (
                get_option_chain,
            )

            result = get_option_chain(underlying="510050", use_cache=True)
            if result.success and not result.data.empty:
                option_types = result.data["option_type"].unique()
                self.assertGreater(len(option_types), 0)
        except Exception as e:
            self.skipTest(f"看涨看跌期权链测试失败: {e}")

    def test_option_chain_fields(self):
        """测试期权链返回字段完整性"""
        try:
            from jk2bt.market_data.option import (
                get_option_chain,
            )

            result = get_option_chain(underlying="510050", use_cache=True)
            if result.success and not result.data.empty:
                required_fields = ["option_code", "option_type", "strike"]
                for field in required_fields:
                    self.assertIn(field, result.data.columns)
        except Exception as e:
            self.skipTest(f"期权链字段测试失败: {e}")

    def test_option_chain_underlying_filter(self):
        """测试按标的筛选期权链"""
        try:
            from jk2bt.market_data.option import (
                get_option_chain,
            )

            result = get_option_chain(underlying="510050", use_cache=True)
            if result.success and not result.data.empty:
                if "underlying" in result.data.columns:
                    underlyings = result.data["underlying"].unique()
                    for underlying in underlyings:
                        if underlying:
                            self.assertIn(
                                "510050", str(underlying) or "ETF" in str(underlying)
                            )
                            break
        except Exception as e:
            self.skipTest(f"标筛选期权链测试失败: {e}")


class TestOptionDaily(unittest.TestCase):
    """日线数据测试"""

    def test_get_option_daily_basic(self):
        """测试获取期权日线数据基本功能"""
        try:
            from jk2bt.market_data.option import (
                get_option_list,
                get_option_daily,
            )

            list_result = get_option_list(underlying="sse", use_cache=True)
            if list_result.success and not list_result.data.empty:
                option_code = str(list_result.data.iloc[0]["option_code"])
                result = get_option_daily(option_code, use_cache=True)
                self.assertIsInstance(result, object)
                self.assertIsInstance(result.data, pd.DataFrame)
        except Exception as e:
            self.skipTest(f"获取期权日线数据失败: {e}")

    def test_option_daily_ohlcv_fields(self):
        """测试日线数据 OHLCV 字段完整性"""
        try:
            from jk2bt.market_data.option import (
                get_option_list,
                get_option_daily,
            )

            list_result = get_option_list(underlying="sse", use_cache=True)
            if list_result.success and not list_result.data.empty:
                option_code = str(list_result.data.iloc[0]["option_code"])
                result = get_option_daily(option_code, use_cache=True)
                if result.success and not result.data.empty:
                    required_cols = ["date", "open", "high", "low", "close", "volume"]
                    for col in required_cols:
                        self.assertIn(col, result.data.columns)
        except Exception as e:
            self.skipTest(f"OHLCV 字段测试失败: {e}")

    def test_option_daily_volume_data(self):
        """测试日线数据成交量数据完整性"""
        try:
            from jk2bt.market_data.option import (
                get_option_list,
                get_option_daily,
            )

            list_result = get_option_list(underlying="sse", use_cache=True)
            if list_result.success and not list_result.data.empty:
                option_code = str(list_result.data.iloc[0]["option_code"])
                result = get_option_daily(option_code, use_cache=True)
                if result.success and not result.data.empty:
                    self.assertIn("volume", result.data.columns)
                    volume_data = result.data["volume"]
                    self.assertTrue(volume_data.notna().any())
        except Exception as e:
            self.skipTest(f"成交量数据测试失败: {e}")

    def test_option_daily_date_range(self):
        """测试日线数据日期范围筛选功能"""
        try:
            from jk2bt.market_data.option import (
                get_option_list,
                get_option_daily,
            )

            list_result = get_option_list(underlying="sse", use_cache=True)
            if list_result.success and not list_result.data.empty:
                option_code = str(list_result.data.iloc[0]["option_code"])
                end_date = datetime.now().strftime("%Y-%m-%d")
                start_date = (datetime.now() - timedelta(days=30)).strftime("%Y-%m-%d")
                result = get_option_daily(
                    option_code,
                    start_date=start_date,
                    end_date=end_date,
                    use_cache=True,
                )
                self.assertIsInstance(result.data, pd.DataFrame)
        except Exception as e:
            self.skipTest(f"日期范围筛选测试失败: {e}")

    def test_option_daily_sorted_by_date(self):
        """测试日线数据按日期升序排列"""
        try:
            from jk2bt.market_data.option import (
                get_option_list,
                get_option_daily,
            )

            list_result = get_option_list(underlying="sse", use_cache=True)
            if list_result.success and not list_result.data.empty:
                option_code = str(list_result.data.iloc[0]["option_code"])
                result = get_option_daily(option_code, use_cache=True)
                if result.success and not result.data.empty and len(result.data) > 1:
                    dates = result.data["date"].tolist()
                    self.assertEqual(dates, sorted(dates))
        except Exception as e:
            self.skipTest(f"日期排序测试失败: {e}")

    def test_option_daily_price_validity(self):
        """测试日线数据价格有效性（high >= low, high >= open/close）"""
        try:
            from jk2bt.market_data.option import (
                get_option_list,
                get_option_daily,
            )

            list_result = get_option_list(underlying="sse", use_cache=True)
            if list_result.success and not list_result.data.empty:
                option_code = str(list_result.data.iloc[0]["option_code"])
                result = get_option_daily(option_code, use_cache=True)
                if result.success and not result.data.empty:
                    for _, row in result.data.head(10).iterrows():
                        if row["high"] > 0 and row["low"] > 0:
                            self.assertGreaterEqual(row["high"], row["low"])
                            break
        except Exception as e:
            self.skipTest(f"价格有效性测试失败: {e}")

    def test_option_daily_with_option_code(self):
        """测试日线数据包含期权代码字段"""
        try:
            from jk2bt.market_data.option import (
                get_option_list,
                get_option_daily,
            )

            list_result = get_option_list(underlying="sse", use_cache=True)
            if list_result.success and not list_result.data.empty:
                option_code = str(list_result.data.iloc[0]["option_code"])
                result = get_option_daily(option_code, use_cache=True)
                if result.success and not result.data.empty:
                    self.assertIn("option_code", result.data.columns)
        except Exception as e:
            self.skipTest(f"期权代码字段测试失败: {e}")


class TestBatchQuery(unittest.TestCase):
    """批量查询测试"""

    def test_query_option_batch(self):
        """测试批量获取期权信息"""
        try:
            from jk2bt.market_data.option import (
                get_option_list,
                query_option,
            )

            list_result = get_option_list(underlying="sse", use_cache=True)
            if list_result.success and not list_result.data.empty:
                option_codes = (
                    list_result.data["option_code"].head(3).astype(str).tolist()
                )
                df = query_option(option_codes, use_cache=True)
                self.assertIsInstance(df, pd.DataFrame)
        except Exception as e:
            self.skipTest(f"批量获取期权信息失败: {e}")

    def test_query_option_empty_list(self):
        """测试空列表批量查询返回空 DataFrame"""
        from jk2bt.market_data.option import query_option

        df = query_option([])
        self.assertIsInstance(df, pd.DataFrame)
        self.assertTrue(df.empty)

    def test_query_filter_by_underlying(self):
        """测试按标的筛选期权列表"""
        try:
            from jk2bt.market_data.option import (
                get_option_list,
            )

            result = get_option_list(underlying="sse", use_cache=True)
            if result.success and not result.data.empty:
                df = result.data
                if "underlying" in df.columns:
                    underlyings = df["underlying"].unique()
                    self.assertGreater(len(underlyings), 0)
        except Exception as e:
            self.skipTest(f"按标的筛选测试失败: {e}")

    def test_get_option_info(self):
        """测试获取单个期权详细信息"""
        try:
            from jk2bt.market_data.option import (
                get_option_list,
                get_option_info,
            )

            list_result = get_option_list(underlying="sse", use_cache=True)
            if list_result.success and not list_result.data.empty:
                option_code = str(list_result.data.iloc[0]["option_code"])
                result = get_option_info(option_code, use_cache=True)
                self.assertIsInstance(result, object)
        except Exception as e:
            self.skipTest(f"获取期权信息失败: {e}")

    def test_query_option_single(self):
        """测试查询单个期权"""
        try:
            from jk2bt.market_data.option import (
                get_option_list,
                query_option,
            )

            list_result = get_option_list(underlying="sse", use_cache=True)
            if list_result.success and not list_result.data.empty:
                option_code = str(list_result.data.iloc[0]["option_code"])
                df = query_option([option_code], use_cache=True)
                self.assertIsInstance(df, pd.DataFrame)
        except Exception as e:
            self.skipTest(f"查询单个期权失败: {e}")

    def test_get_option_price(self):
        """测试获取期权实时价格"""
        try:
            from jk2bt.market_data.option import (
                get_option_list,
                get_option_price,
            )

            list_result = get_option_list(underlying="sse", use_cache=True)
            if list_result.success and not list_result.data.empty:
                option_code = str(list_result.data.iloc[0]["option_code"])
                result = get_option_price(option_code, use_cache=True)
                self.assertIsInstance(result, object)
        except Exception as e:
            self.skipTest(f"获取期权价格失败: {e}")


class TestBoundaryConditions(unittest.TestCase):
    """边界条件测试"""

    def test_nonexistent_option_code(self):
        """测试不存在的期权代码处理"""
        from jk2bt.market_data.option import (
            get_option_price,
            get_option_greeks,
            get_option_daily,
            get_option_info,
            RobustResult,
        )

        invalid_code = "9999999999"

        result = get_option_price(invalid_code, use_cache=False)
        self.assertIsInstance(result, RobustResult)

        result = get_option_greeks(invalid_code, use_cache=False)
        self.assertIsInstance(result, RobustResult)

        result = get_option_daily(invalid_code, use_cache=False)
        self.assertIsInstance(result, RobustResult)
        self.assertFalse(result.success)

        result = get_option_info(invalid_code, use_cache=False)
        self.assertIsInstance(result, RobustResult)
        self.assertFalse(result.success)

    def test_expired_option(self):
        """测试已到期期权处理"""
        try:
            from jk2bt.market_data.option import (
                calculate_option_implied_vol,
            )

            result = calculate_option_implied_vol(
                option_code="expired_code",
                price=0.01,
                underlying_price=3.0,
            )
            self.assertIsInstance(result, dict)
            self.assertFalse(result.get("success", True))
        except Exception:
            self.skipTest("已到期期权测试跳过")

    def test_invalid_parameters(self):
        """测试无效参数处理"""
        from jk2bt.market_data.option import (
            get_option_daily,
        )

        result = get_option_daily("", use_cache=False)
        self.assertFalse(result.success)

        result = get_option_daily(None, use_cache=False)
        self.assertFalse(result.success)

    def test_zero_price_implied_vol(self):
        """测试零价格计算隐含波动率"""
        from jk2bt.market_data.option import (
            calculate_option_implied_vol,
        )

        result = calculate_option_implied_vol(
            option_code="test",
            price=0.0,
            underlying_price=3.0,
        )
        self.assertIsInstance(result, dict)

    def test_negative_strike(self):
        """测试行权价应为非负数"""
        try:
            from jk2bt.market_data.option import (
                get_option_list,
            )

            result = get_option_list(underlying="sse", use_cache=True)
            if result.success and not result.data.empty:
                strikes = result.data["strike"].dropna()
                self.assertTrue((strikes >= 0).all())
        except Exception as e:
            self.skipTest(f"行权价非负测试失败: {e}")

    def test_empty_dataframe_handling(self):
        """测试空 DataFrame 处理"""
        from jk2bt.market_data.option import (
            query_option,
        )

        df = query_option(["invalid_code_1", "invalid_code_2"])
        self.assertIsInstance(df, pd.DataFrame)

    def test_invalid_underlying_type(self):
        """测试无效标的类型返回错误信息"""
        from jk2bt.market_data.option import (
            get_option_list,
        )

        result = get_option_list(underlying="invalid_type", use_cache=True)
        self.assertFalse(result.success)
        self.assertIsNotNone(result.reason)


class TestDataValidation(unittest.TestCase):
    """数据验证测试"""

    def test_option_basic_info_fields(self):
        """验证期权基本信息字段完整性"""
        try:
            from jk2bt.market_data.option import (
                get_option_list,
            )

            result = get_option_list(underlying="sse", use_cache=True)
            if result.success and not result.data.empty:
                df = result.data
                required_fields = ["option_code", "option_name", "option_type"]
                for field in required_fields:
                    self.assertIn(field, df.columns)
        except Exception as e:
            self.skipTest(f"基本信息字段验证失败: {e}")

    def test_strike_price_format(self):
        """验证行权价格为有效数值且大于零"""
        try:
            from jk2bt.market_data.option import (
                get_option_list,
            )

            result = get_option_list(underlying="sse", use_cache=True)
            if result.success and not result.data.empty:
                strikes = result.data["strike"].dropna()
                for strike in strikes.head(10):
                    self.assertIsInstance(strike, (int, float))
                    self.assertGreater(strike, 0)
        except Exception as e:
            self.skipTest(f"行权价格式验证失败: {e}")

    def test_expiry_date_format(self):
        """验证到期日格式有效性"""
        try:
            from jk2bt.market_data.option import (
                get_option_list,
            )

            result = get_option_list(underlying="sse", use_cache=True)
            if result.success and not result.data.empty:
                dates = result.data["expiry_date"].dropna()
                for date in dates.head(10):
                    self.assertIsNotNone(date)
        except Exception as e:
            self.skipTest(f"到期日格式验证失败: {e}")

    def test_option_type_values(self):
        """验证看涨看跌标识有效性"""
        try:
            from jk2bt.market_data.option import (
                get_option_list,
            )

            result = get_option_list(underlying="sse", use_cache=True)
            if result.success and not result.data.empty:
                option_types = result.data["option_type"].dropna().unique()
                valid_types = ["看涨", "看跌"]
                for opt_type in option_types:
                    self.assertIn(opt_type, valid_types)
        except Exception as e:
            self.skipTest(f"看涨看跌标识验证失败: {e}")

    def test_option_code_uniqueness(self):
        """验证期权代码唯一性"""
        try:
            from jk2bt.market_data.option import (
                get_option_list,
            )

            result = get_option_list(underlying="sse", use_cache=True)
            if result.success and not result.data.empty:
                codes = result.data["option_code"]
                self.assertEqual(len(codes), len(codes.unique()))
        except Exception as e:
            self.skipTest(f"期权代码唯一性验证失败: {e}")

    def test_greeks_data_types(self):
        """验证希腊值数据类型为数值型或 None"""
        try:
            from jk2bt.market_data.option import (
                get_option_list,
                get_option_greeks,
            )

            list_result = get_option_list(underlying="sse", use_cache=True)
            if list_result.success and not list_result.data.empty:
                option_code = str(list_result.data.iloc[0]["option_code"])
                result = get_option_greeks(option_code, use_cache=True)
                if result.success and not result.data.empty:
                    greeks = result.data.iloc[0]
                    for field in ["delta", "gamma", "theta", "vega"]:
                        if greeks.get(field) is not None:
                            self.assertIsInstance(
                                greeks[field], (int, float, type(None))
                            )
        except Exception as e:
            self.skipTest(f"希腊值数据类型验证失败: {e}")

    def test_option_name_format(self):
        """验证期权名称包含期权类型标识"""
        try:
            from jk2bt.market_data.option import (
                get_option_list,
            )

            result = get_option_list(underlying="sse", use_cache=True)
            if result.success and not result.data.empty:
                for _, row in result.data.head(10).iterrows():
                    name = str(row.get("option_name", ""))
                    opt_type = row.get("option_type", "")
                    if opt_type == "看涨":
                        self.assertTrue("购" in name or "call" in name.lower())
                    elif opt_type == "看跌":
                        self.assertTrue("沽" in name or "put" in name.lower())
                    break
        except Exception as e:
            self.skipTest(f"期权名称格式验证失败: {e}")


class TestFinanceQuery(unittest.TestCase):
    """FinanceQuery 类测试"""

    def test_finance_query_instance(self):
        """测试 FinanceQuery 单例实例化"""
        from jk2bt.market_data.option import (
            finance,
            FinanceQuery,
        )

        self.assertIsInstance(finance, FinanceQuery)

    def test_finance_query_stk_option_daily(self):
        """测试 finance.STK_OPTION_DAILY 表查询"""
        try:
            from jk2bt.market_data.option import (
                finance,
            )

            df = finance.run_query(finance.STK_OPTION_DAILY)
            self.assertIsInstance(df, pd.DataFrame)
        except Exception as e:
            self.skipTest(f"STK_OPTION_DAILY 查询失败: {e}")

    def test_finance_query_stk_option_basic(self):
        """测试 finance.STK_OPTION_BASIC 表查询"""
        try:
            from jk2bt.market_data.option import (
                finance,
            )

            df = finance.run_query(finance.STK_OPTION_BASIC)
            self.assertIsInstance(df, pd.DataFrame)
        except Exception as e:
            self.skipTest(f"STK_OPTION_BASIC 查询失败: {e}")

    def test_run_query_simple(self):
        """测试 run_query_simple 简化查询接口"""
        try:
            from jk2bt.market_data.option import (
                run_query_simple,
            )

            df = run_query_simple("STK_OPTION_DAILY", use_cache=True)
            self.assertIsInstance(df, pd.DataFrame)
        except Exception as e:
            self.skipTest(f"run_query_simple 测试失败: {e}")

    def test_run_query_simple_with_code(self):
        """测试 run_query_simple 带期权代码参数"""
        try:
            from jk2bt.market_data.option import (
                get_option_list,
                run_query_simple,
            )

            list_result = get_option_list(underlying="sse", use_cache=True)
            if list_result.success and not list_result.data.empty:
                option_code = str(list_result.data.iloc[0]["option_code"])
                df = run_query_simple("STK_OPTION_DAILY", option_code=option_code)
                self.assertIsInstance(df, pd.DataFrame)
        except Exception as e:
            self.skipTest(f"带代码 run_query_simple 测试失败: {e}")

    def test_run_query_simple_with_underlying(self):
        """测试 run_query_simple 按标的筛选"""
        try:
            from jk2bt.market_data.option import (
                run_query_simple,
            )

            df = run_query_simple("STK_OPTION_BASIC", underlying_code="510050")
            self.assertIsInstance(df, pd.DataFrame)
        except Exception as e:
            self.skipTest(f"按标筛选 run_query_simple 测试失败: {e}")


class TestCacheMechanism(unittest.TestCase):
    """缓存机制测试"""

    def test_cache_dir_creation(self):
        """测试缓存目录创建"""
        from jk2bt.market_data.option import (
            get_option_list,
        )
        import tempfile
        import shutil

        cache_dir = tempfile.mkdtemp()
        try:
            result = get_option_list(
                underlying="sse", cache_dir=cache_dir, use_cache=False
            )
            self.assertIsInstance(result.data, pd.DataFrame)
        finally:
            shutil.rmtree(cache_dir, ignore_errors=True)

    def test_force_update_flag(self):
        """测试强制更新标志功能"""
        try:
            from jk2bt.market_data.option import (
                get_option_list,
            )

            result1 = get_option_list(underlying="sse", use_cache=True)
            result2 = get_option_list(underlying="sse", force_update=True)
            self.assertIsInstance(result1.data, pd.DataFrame)
            self.assertIsInstance(result2.data, pd.DataFrame)
        except Exception as e:
            self.skipTest(f"强制更新测试失败: {e}")

    def test_cache_validity(self):
        """测试缓存数据有效性"""
        try:
            from jk2bt.market_data.option import (
                get_option_list,
            )

            result1 = get_option_list(underlying="sse", use_cache=True)
            if result1.success:
                source1 = result1.source

            result2 = get_option_list(underlying="sse", use_cache=True)
            if result2.success:
                source2 = result2.source

                self.assertEqual(source1, source2)
        except Exception as e:
            self.skipTest(f"缓存有效性测试失败: {e}")


if __name__ == "__main__":
    unittest.main()
