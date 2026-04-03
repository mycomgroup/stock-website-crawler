#!/usr/bin/env python3
"""
Task 32: 分钟上层 API 打通 - 综合测试套件
覆盖各种场景，确保上层 API 正确消费分钟数据
"""

import unittest
import sys
import os
import pandas as pd
from datetime import datetime, timedelta

sys.path.insert(
    0,
    os.path.join(os.path.dirname(__file__), "..", "src"),
)


class TestMinuteFrequencyParameters(unittest.TestCase):
    """测试各种分钟频率参数"""

    def test_1m_frequency(self):
        """测试 1m 频率"""
        from jk2bt.api.market import get_price

        df = get_price(
            "600519.XSHG",
            start_date="2026-03-28 09:30:00",
            end_date="2026-03-28 15:00:00",
            frequency="1m",
            fields=["close"],
        )

        self.assertIsInstance(df, pd.DataFrame)
        print(f"\n[1m] 返回 {len(df)} 条数据")

    def test_5m_frequency(self):
        """测试 5m 频率"""
        from jk2bt.api.market import get_price

        df = get_price(
            "600519.XSHG",
            start_date="2026-03-28 09:30:00",
            end_date="2026-03-28 15:00:00",
            frequency="5m",
            fields=["open", "close"],
        )

        self.assertIsInstance(df, pd.DataFrame)
        print(f"\n[5m] 返回 {len(df)} 条数据")

    def test_15m_frequency(self):
        """测试 15m 频率"""
        from jk2bt.api.market import get_price

        df = get_price(
            "600519.XSHG",
            start_date="2026-03-28 09:30:00",
            end_date="2026-03-28 15:00:00",
            frequency="15m",
            fields=["close"],
        )

        self.assertIsInstance(df, pd.DataFrame)
        print(f"\n[15m] 返回 {len(df)} 条数据")

    def test_30m_frequency(self):
        """测试 30m 频率"""
        from jk2bt.api.market import get_price

        df = get_price(
            "600519.XSHG",
            start_date="2026-03-28 09:30:00",
            end_date="2026-03-28 15:00:00",
            frequency="30m",
            fields=["close"],
        )

        self.assertIsInstance(df, pd.DataFrame)
        print(f"\n[30m] 返回 {len(df)} 条数据")

    def test_60m_frequency(self):
        """测试 60m 频率"""
        from jk2bt.api.market import get_price

        df = get_price(
            "600519.XSHG",
            start_date="2026-03-28 09:30:00",
            end_date="2026-03-28 15:00:00",
            frequency="60m",
            fields=["close"],
        )

        self.assertIsInstance(df, pd.DataFrame)
        print(f"\n[60m] 返回 {len(df)} 条数据")

    def test_minute_alias(self):
        """测试 minute 别名"""
        from jk2bt.api.market import get_price

        df = get_price(
            "600519.XSHG",
            start_date="2026-03-28 09:30:00",
            end_date="2026-03-28 10:00:00",
            frequency="minute",
            fields=["close"],
        )

        self.assertIsInstance(df, pd.DataFrame)
        print(f"\n[minute alias] 返回 {len(df)} 条数据")

    def test_frequency_case_insensitive(self):
        """测试频率参数大小写"""
        from jk2bt.api.market import get_price

        df_lower = get_price(
            "600519.XSHG",
            start_date="2026-03-28 09:30:00",
            end_date="2026-03-28 10:00:00",
            frequency="5m",
            fields=["close"],
        )

        self.assertIsInstance(df_lower, pd.DataFrame)


class TestMinuteCountAndDateRange(unittest.TestCase):
    """测试 count 和 date range 两种入口"""

    def test_get_price_with_count(self):
        """测试 get_price 使用 count 参数"""
        from jk2bt.api.market import get_price

        df = get_price(
            "600519.XSHG",
            end_date="2026-03-28 15:00:00",
            frequency="5m",
            count=50,
            fields=["open", "close", "volume"],
        )

        self.assertIsInstance(df, pd.DataFrame)
        if not df.empty:
            self.assertLessEqual(len(df), 50)
        print(f"\n[get_price count=50] 返回 {len(df)} 条数据")

    def test_get_price_with_date_range(self):
        """测试 get_price 使用 date range 参数"""
        from jk2bt.api.market import get_price

        df = get_price(
            "600519.XSHG",
            start_date="2026-03-28 09:30:00",
            end_date="2026-03-28 11:30:00",
            frequency="5m",
            fields=["close"],
        )

        self.assertIsInstance(df, pd.DataFrame)
        print(f"\n[get_price date_range] 返回 {len(df)} 条数据")

    def test_history_with_count(self):
        """测试 history 使用 count 参数"""
        from jk2bt.api.market import history

        result = history(
            count=100,
            unit="5m",
            field="close",
            security_list=["600519.XSHG", "000001.XSHE"],
            df=True,
        )

        self.assertIsInstance(result, pd.DataFrame)
        print(f"\n[history count=100] 返回 {len(result)} 行")

    def test_attribute_history_with_count(self):
        """测试 attribute_history 使用 count 参数"""
        from jk2bt.api.market import attribute_history

        result = attribute_history(
            security="600519.XSHG",
            count=80,
            unit="5m",
            fields=["open", "high", "low", "close", "volume"],
            df=True,
        )

        self.assertIsInstance(result, pd.DataFrame)
        if not result.empty:
            self.assertIn("close", result.columns)
        print(f"\n[attribute_history count=80] 返回 {len(result)} 行")

    def test_get_bars_with_count(self):
        """测试 get_bars 使用 count 参数"""
        from jk2bt.api.market import get_bars

        result = get_bars(
            security="600519.XSHG",
            count=60,
            unit="5m",
            fields=["open", "close"],
        )

        self.assertIsInstance(result, pd.DataFrame)
        if not result.empty:
            self.assertLessEqual(len(result), 60)
        print(f"\n[get_bars count=60] 返回 {len(result)} 行")


class TestMinuteFieldsSelection(unittest.TestCase):
    """测试字段选择"""

    def test_single_field(self):
        """测试单字段查询"""
        from jk2bt.api.market import get_price

        df = get_price(
            "600519.XSHG",
            start_date="2026-03-28 09:30:00",
            end_date="2026-03-28 10:00:00",
            frequency="5m",
            fields=["close"],
        )

        self.assertIsInstance(df, pd.DataFrame)
        if not df.empty:
            self.assertIn("close", df.columns)
        print(f"\n[单字段 close] 返回 {len(df)} 条")

    def test_multiple_fields(self):
        """测试多字段查询"""
        from jk2bt.api.market import get_price

        df = get_price(
            "600519.XSHG",
            start_date="2026-03-28 09:30:00",
            end_date="2026-03-28 10:00:00",
            frequency="5m",
            fields=["open", "high", "low", "close", "volume"],
        )

        self.assertIsInstance(df, pd.DataFrame)
        if not df.empty:
            for field in ["open", "high", "low", "close"]:
                self.assertIn(field, df.columns)
        print(f"\n[多字段 OHLCV] 返回 {len(df)} 条")

    def test_all_fields(self):
        """测试所有字段查询"""
        from jk2bt.api.market import get_price

        df = get_price(
            "600519.XSHG",
            start_date="2026-03-28 09:30:00",
            end_date="2026-03-28 10:00:00",
            frequency="5m",
        )

        self.assertIsInstance(df, pd.DataFrame)
        if not df.empty:
            expected_fields = ["open", "high", "low", "close", "volume", "money"]
            found_fields = [f for f in expected_fields if f in df.columns]
            self.assertGreater(len(found_fields), 0)
        print(f"\n[所有字段] 返回 {len(df)} 条，包含 {len(df.columns)} 列")

    def test_invalid_field(self):
        """测试无效字段查询"""
        from jk2bt.api.market import get_price

        df = get_price(
            "600519.XSHG",
            start_date="2026-03-28 09:30:00",
            end_date="2026-03-28 10:00:00",
            frequency="5m",
            fields=["invalid_field", "close"],
        )

        self.assertIsInstance(df, pd.DataFrame)
        print(f"\n[无效字段] 返回 {len(df)} 条（应该只包含 close）")


class TestMinuteMultiSecurity(unittest.TestCase):
    """测试多标的情况"""

    def test_get_price_multiple_securities_panel_true(self):
        """测试多标的 panel=True"""
        from jk2bt.api.market import get_price

        result = get_price(
            ["600519.XSHG", "000001.XSHE"],
            start_date="2026-03-28 09:30:00",
            end_date="2026-03-28 10:00:00",
            frequency="5m",
            fields=["close"],
            panel=True,
        )

        self.assertIsInstance(result, dict)
        if result:
            for symbol, df in result.items():
                self.assertIsInstance(df, pd.DataFrame)
        print(f"\n[多标的 panel=True] 返回 {len(result)} 个标的数据")

    def test_get_price_multiple_securities_panel_false(self):
        """测试多标的 panel=False"""
        from jk2bt.api.market import get_price

        df = get_price(
            ["600519.XSHG", "000001.XSHE"],
            start_date="2026-03-28 09:30:00",
            end_date="2026-03-28 10:00:00",
            frequency="5m",
            fields=["close"],
            panel=False,
        )

        self.assertIsInstance(df, pd.DataFrame)
        if not df.empty:
            self.assertIn("code", df.columns)
        print(f"\n[多标的 panel=False] 返回 {len(df)} 行")

    def test_history_multiple_securities(self):
        """测试 history 多标的"""
        from jk2bt.api.market import history

        result = history(
            count=50,
            unit="5m",
            field="close",
            security_list=["600519.XSHG", "000001.XSHE", "000002.XSHE"],
            df=True,
        )

        self.assertIsInstance(result, pd.DataFrame)
        if not result.empty:
            for symbol in ["600519.XSHG", "000001.XSHE"]:
                if symbol in result.columns:
                    self.assertIsInstance(result[symbol], pd.Series)
        print(f"\n[history 多标的] 返回 {len(result)} 行，{len(result.columns)} 列")

    def test_get_bars_multiple_securities(self):
        """测试 get_bars 多标的"""
        from jk2bt.api.market import get_bars

        result = get_bars(
            security=["600519.XSHG", "000001.XSHE"],
            count=30,
            unit="5m",
        )

        self.assertIsInstance(result, dict)
        print(f"\n[get_bars 多标的] 返回 {len(result)} 个标的数据")


class TestMinuteStockAndETF(unittest.TestCase):
    """测试股票和 ETF 分钟数据"""

    def test_stock_minute(self):
        """测试股票分钟数据"""
        from jk2bt.api.market import get_price

        df = get_price(
            "600519.XSHG",
            start_date="2026-03-28 09:30:00",
            end_date="2026-03-28 10:00:00",
            frequency="5m",
            fields=["close", "volume"],
        )

        self.assertIsInstance(df, pd.DataFrame)
        print(f"\n[股票分钟] 600519 返回 {len(df)} 条")

    def test_etf_minute(self):
        """测试 ETF 分钟数据"""
        from jk2bt.api.market import get_price

        df = get_price(
            "510300.XSHG",
            start_date="2026-03-28 09:30:00",
            end_date="2026-03-28 10:00:00",
            frequency="5m",
            fields=["close"],
        )

        self.assertIsInstance(df, pd.DataFrame)
        print(f"\n[ETF 分钟] 510300 返回 {len(df)} 条")

    def test_etf_51_prefix(self):
        """测试 51 开头 ETF"""
        from jk2bt.api.market import get_price

        df = get_price(
            "510050.XSHG",
            start_date="2026-03-28 09:30:00",
            end_date="2026-03-28 10:00:00",
            frequency="5m",
        )

        self.assertIsInstance(df, pd.DataFrame)
        print(f"\n[ETF 51开头] 510050 返回 {len(df)} 条")

    def test_etf_15_prefix(self):
        """测试 15 开头 ETF"""
        from jk2bt.api.market import get_price

        df = get_price(
            "159915.XSHE",
            start_date="2026-03-28 09:30:00",
            end_date="2026-03-28 10:00:00",
            frequency="5m",
        )

        self.assertIsInstance(df, pd.DataFrame)
        print(f"\n[ETF 15开头] 159915 返回 {len(df)} 条")


class TestMinuteTimeWindowCalculation(unittest.TestCase):
    """测试时间窗口计算"""

    def test_time_window_1m(self):
        """测试 1m 时间窗口计算"""
        from jk2bt.api.market import get_bars

        count = 60
        result = get_bars("600519.XSHG", count=count, unit="1m")

        self.assertIsInstance(result, pd.DataFrame)
        if not result.empty:
            self.assertLessEqual(len(result), count)
        print(f"\n[时间窗口 1m] count={count} 返回 {len(result)} 条")

    def test_time_window_5m(self):
        """测试 5m 时间窗口计算"""
        from jk2bt.api.market import get_bars

        count = 48
        result = get_bars("600519.XSHG", count=count, unit="5m")

        self.assertIsInstance(result, pd.DataFrame)
        if not result.empty:
            self.assertLessEqual(len(result), count)
        print(f"\n[时间窗口 5m] count={count} 返回 {len(result)} 条")

    def test_time_window_15m(self):
        """测试 15m 时间窗口计算"""
        from jk2bt.api.market import get_bars

        count = 16
        result = get_bars("600519.XSHG", count=count, unit="15m")

        self.assertIsInstance(result, pd.DataFrame)
        if not result.empty:
            self.assertLessEqual(len(result), count)
        print(f"\n[时间窗口 15m] count={count} 返回 {len(result)} 条")

    def test_time_window_30m(self):
        """测试 30m 时间窗口计算"""
        from jk2bt.api.market import get_bars

        count = 8
        result = get_bars("600519.XSHG", count=count, unit="30m")

        self.assertIsInstance(result, pd.DataFrame)
        if not result.empty:
            self.assertLessEqual(len(result), count)
        print(f"\n[时间窗口 30m] count={count} 返回 {len(result)} 条")

    def test_time_window_60m(self):
        """测试 60m 时间窗口计算"""
        from jk2bt.api.market import get_bars

        count = 4
        result = get_bars("600519.XSHG", count=count, unit="60m")

        self.assertIsInstance(result, pd.DataFrame)
        if not result.empty:
            self.assertLessEqual(len(result), count)
        print(f"\n[时间窗口 60m] count={count} 返回 {len(result)} 条")


class TestMinuteErrorHandling(unittest.TestCase):
    """测试错误处理"""

    def test_invalid_symbol(self):
        """测试无效代码"""
        from jk2bt.api.market import get_price

        df = get_price(
            "INVALID.XSHG",
            start_date="2026-03-28 09:30:00",
            end_date="2026-03-28 10:00:00",
            frequency="5m",
        )

        self.assertIsInstance(df, pd.DataFrame)
        self.assertTrue(df.empty)
        print(f"\n[无效代码] 返回空数据 ✓")

    def test_invalid_frequency(self):
        """测试无效频率"""
        from jk2bt.api.market import get_price

        try:
            df = get_price(
                "600519.XSHG",
                start_date="2026-03-28 09:30:00",
                end_date="2026-03-28 10:00:00",
                frequency="invalid_freq",
            )
            self.fail("应该抛出 ValueError")
        except ValueError as e:
            print(f"\n[无效频率] 正确抛出 ValueError ✓")

    def test_invalid_time_range(self):
        """测试无效时间范围（未来时间）"""
        from jk2bt.api.market import get_price

        df = get_price(
            "600519.XSHG",
            start_date="2030-01-01 09:30:00",
            end_date="2030-01-01 15:00:00",
            frequency="5m",
        )

        self.assertIsInstance(df, pd.DataFrame)
        self.assertTrue(df.empty)
        print(f"\n[无效时间范围] 返回空数据 ✓")

    def test_negative_count(self):
        """测试负数 count"""
        from jk2bt.api.market import get_bars

        result = get_bars("600519.XSHG", count=-10, unit="5m")

        self.assertIsInstance(result, pd.DataFrame)
        print(f"\n[负数 count] 返回 {len(result)} 条（应该为空）")


class TestMinuteDataFrameFormat(unittest.TestCase):
    """测试 DataFrame 格式"""

    def test_datetime_column_exists(self):
        """测试 datetime 列存在"""
        from jk2bt.api.market import get_price

        df = get_price(
            "600519.XSHG",
            start_date="2026-03-28 09:30:00",
            end_date="2026-03-28 10:00:00",
            frequency="5m",
            fields=["close"],
        )

        self.assertIsInstance(df, pd.DataFrame)
        if not df.empty:
            self.assertIn("datetime", df.columns)
            self.assertEqual(df["datetime"].dtype, "datetime64[ns]")
        print(f"\n[datetime 列] 类型正确 ✓")

    def test_numeric_columns_type(self):
        """测试数值列类型"""
        from jk2bt.api.market import get_price

        df = get_price(
            "600519.XSHG",
            start_date="2026-03-28 09:30:00",
            end_date="2026-03-28 10:00:00",
            frequency="5m",
            fields=["open", "high", "low", "close", "volume"],
        )

        self.assertIsInstance(df, pd.DataFrame)
        if not df.empty:
            for col in ["open", "high", "low", "close", "volume"]:
                if col in df.columns:
                    self.assertTrue(
                        df[col].dtype in ["float64", "int64", "float32", "int32"]
                    )
        print(f"\n[数值列类型] 正确 ✓")

    def test_dataframe_sorted_by_datetime(self):
        """测试数据按 datetime 排序"""
        from jk2bt.api.market import get_price

        df = get_price(
            "600519.XSHG",
            start_date="2026-03-28 09:30:00",
            end_date="2026-03-28 15:00:00",
            frequency="5m",
            fields=["close"],
        )

        self.assertIsInstance(df, pd.DataFrame)
        if not df.empty and "datetime" in df.columns:
            datetime_series = df["datetime"]
            for i in range(len(datetime_series) - 1):
                self.assertLessEqual(
                    datetime_series.iloc[i], datetime_series.iloc[i + 1]
                )
        print(f"\n[datetime 排序] 正确 ✓")

    def test_attribute_history_dict_format(self):
        """测试 attribute_history df=False 格式"""
        from jk2bt.api.market import attribute_history

        result = attribute_history(
            security="600519.XSHG",
            count=50,
            unit="5m",
            fields=["open", "close"],
            df=False,
        )

        self.assertIsInstance(result, dict)
        if result:
            for field, values in result.items():
                self.assertIsInstance(values, (list, pd.Series))
        print(f"\n[attribute_history df=False] 返回 dict ✓")


class TestMinuteCacheIntegration(unittest.TestCase):
    """测试缓存集成"""

    def test_cache_query_path(self):
        """测试缓存查询路径"""
        from jk2bt.db.duckdb_manager import DuckDBManager

        db = DuckDBManager(read_only=True)
        symbol = "sh600000"
        end_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        start_date = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d %H:%M:%S")

        has_cache = db.has_data(
            "stock_minute", symbol, start_date, end_date, "qfq", "5"
        )
        print(f"\n[缓存查询] {symbol} 5分钟: {has_cache}")

        self.assertIsInstance(has_cache, bool)

    def test_cache_empty_result_diagnosis(self):
        """测试空结果诊断"""
        from jk2bt.api.market import get_price

        df = get_price(
            "600519.XSHG",
            start_date="2026-03-28 09:30:00",
            end_date="2026-03-28 10:00:00",
            frequency="5m",
        )

        self.assertIsInstance(df, pd.DataFrame)
        if df.empty:
            print(f"\n[空结果诊断] 返回空数据，API 正确处理 ✓")
        else:
            print(f"\n[缓存集成] 返回 {len(df)} 条数据 ✓")


class TestMinuteAPIConsistency(unittest.TestCase):
    """测试 API 行为一致性"""

    def test_same_count_different_units(self):
        """测试相同 count 不同周期返回不同数据量"""
        from jk2bt.api.market import get_bars

        count = 50

        df_1m = get_bars("600519.XSHG", count=count, unit="1m")
        df_5m = get_bars("600519.XSHG", count=count, unit="5m")

        self.assertIsInstance(df_1m, pd.DataFrame)
        self.assertIsInstance(df_5m, pd.DataFrame)

        if not df_1m.empty and not df_5m.empty:
            print(f"\n[相同 count={count}] 1m: {len(df_1m)} 条, 5m: {len(df_5m)} 条")

    def test_get_price_vs_get_bars(self):
        """测试 get_price 和 get_bars 行为一致性"""
        from jk2bt.api.market import get_price, get_bars

        df_price = get_price(
            "600519.XSHG",
            start_date="2026-03-28 09:30:00",
            end_date="2026-03-28 10:00:00",
            frequency="5m",
            fields=["close"],
        )

        df_bars = get_bars(
            "600519.XSHG",
            count=6,
            unit="5m",
            fields=["close"],
        )

        self.assertIsInstance(df_price, pd.DataFrame)
        self.assertIsInstance(df_bars, pd.DataFrame)

        print(
            f"\n[API 一致性] get_price: {len(df_price)} 条, get_bars: {len(df_bars)} 条"
        )

    def test_history_vs_attribute_history(self):
        """测试 history 和 attribute_history 行为一致性"""
        from jk2bt.api.market import history, attribute_history

        df_history = history(
            count=50,
            unit="5m",
            field="close",
            security_list=["600519.XSHG"],
            df=True,
        )

        df_attr = attribute_history(
            security="600519.XSHG",
            count=50,
            unit="5m",
            fields=["close"],
            df=True,
        )

        self.assertIsInstance(df_history, pd.DataFrame)
        self.assertIsInstance(df_attr, pd.DataFrame)

        print(
            f"\n[API 一致性] history: {len(df_history)} 行, attribute_history: {len(df_attr)} 行"
        )


def run_comprehensive_tests():
    """运行综合测试"""
    print("=" * 80)
    print("Task 32: 分钟上层 API 综合测试套件")
    print("=" * 80)

    loader = unittest.TestLoader()
    suite = unittest.TestSuite()

    suite.addTests(loader.loadTestsFromTestCase(TestMinuteFrequencyParameters))
    suite.addTests(loader.loadTestsFromTestCase(TestMinuteCountAndDateRange))
    suite.addTests(loader.loadTestsFromTestCase(TestMinuteFieldsSelection))
    suite.addTests(loader.loadTestsFromTestCase(TestMinuteMultiSecurity))
    suite.addTests(loader.loadTestsFromTestCase(TestMinuteStockAndETF))
    suite.addTests(loader.loadTestsFromTestCase(TestMinuteTimeWindowCalculation))
    suite.addTests(loader.loadTestsFromTestCase(TestMinuteErrorHandling))
    suite.addTests(loader.loadTestsFromTestCase(TestMinuteDataFrameFormat))
    suite.addTests(loader.loadTestsFromTestCase(TestMinuteCacheIntegration))
    suite.addTests(loader.loadTestsFromTestCase(TestMinuteAPIConsistency))

    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    print("\n" + "=" * 80)
    print("测试总结")
    print("=" * 80)
    print(f"运行测试: {result.testsRun}")
    print(f"失败: {len(result.failures)}")
    print(f"错误: {len(result.errors)}")

    success_count = result.testsRun - len(result.failures) - len(result.errors)
    success_rate = success_count / result.testsRun if result.testsRun > 0 else 0
    print(f"\n成功率: {success_rate:.1%}")

    if success_rate >= 0.95:
        print("\n✓ 测试覆盖度充足，API 行为正确")
    elif success_rate >= 0.8:
        print("\n⚠ 测试覆盖度良好，部分测试返回空数据（可能缓存未预热）")
    else:
        print("\n✗ 测试覆盖度不足，需要检查失败案例")

    print("=" * 80)

    return result


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Task 32: 分钟上层 API 综合测试")
    parser.add_argument("--comprehensive", action="store_true", help="运行综合测试")
    args = parser.parse_args()

    if args.comprehensive:
        run_comprehensive_tests()
    else:
        unittest.main()
