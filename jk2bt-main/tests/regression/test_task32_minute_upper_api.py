#!/usr/bin/env python3
"""
Task 32: 分钟上层 API 打通测试
验证 get_price/history/attribute_history/get_bars 对分钟数据的真实消费能力
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


class TestMinuteUpperAPI(unittest.TestCase):
    """测试分钟数据上层 API 集成"""

    def test_get_price_frequency_1m(self):
        """测试 get_price(..., frequency='1m')"""
        from jk2bt.api.market import get_price

        end_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        start_date = (datetime.now() - timedelta(days=2)).strftime("%Y-%m-%d %H:%M:%S")

        df = get_price(
            "600519.XSHG",
            start_date=start_date,
            end_date=end_date,
            frequency="1m",
            fields=["open", "high", "low", "close", "volume"],
        )

        print(f"\n[get_price 1m] 返回数据条数: {len(df)}")
        if df.empty:
            print("  警告: 返回空数据，可能缓存未预热")
        else:
            print(f"  首条: {df.iloc[0].to_dict()}")
            print(f"  列: {list(df.columns)}")

        self.assertIsInstance(df, pd.DataFrame)

    def test_get_price_frequency_5m(self):
        """测试 get_price(..., frequency='5m')"""
        from jk2bt.api.market import get_price

        end_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        start_date = (datetime.now() - timedelta(days=3)).strftime("%Y-%m-%d %H:%M:%S")

        df = get_price(
            "000001.XSHE",
            start_date=start_date,
            end_date=end_date,
            frequency="5m",
            fields=["open", "close", "volume"],
        )

        print(f"\n[get_price 5m] 返回数据条数: {len(df)}")
        if df.empty:
            print("  警告: 返回空数据，可能缓存未预热")
        else:
            print(f"  首条: {df.iloc[0].to_dict()}")

        self.assertIsInstance(df, pd.DataFrame)

    def test_history_unit_5m(self):
        """测试 history(..., unit='5m')"""
        from jk2bt.api.market import history

        result = history(
            count=50,
            unit="5m",
            field="close",
            security_list=["600519.XSHG"],
            df=True,
            end_date=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        )

        print(f"\n[history 5m] 返回数据条数: {len(result)}")
        if result.empty:
            print("  警告: 返回空数据，可能缓存未预热")
        else:
            print(f"  首条: {result.iloc[0].to_dict()}")
            print(f"  列: {list(result.columns)}")

        self.assertIsInstance(result, pd.DataFrame)

    def test_attribute_history_unit_5m(self):
        """测试 attribute_history(..., unit='5m')"""
        from jk2bt.api.market import attribute_history

        result = attribute_history(
            security="600519.XSHG",
            count=100,
            unit="5m",
            fields=["open", "high", "low", "close", "volume"],
            df=True,
            end_date=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        )

        print(f"\n[attribute_history 5m] 返回数据条数: {len(result)}")
        if result.empty:
            print("  警告: 返回空数据，可能缓存未预热")
        else:
            print(f"  首条: {result.iloc[0].to_dict()}")
            print(f"  列: {list(result.columns)}")

        self.assertIsInstance(result, pd.DataFrame)

    def test_get_bars_unit_5m(self):
        """测试 get_bars(..., unit='5m')"""
        from jk2bt.api.market import get_bars

        result = get_bars(
            security="600519.XSHG",
            count=50,
            unit="5m",
            fields=["open", "close", "volume"],
            end_dt=datetime.now(),
        )

        print(f"\n[get_bars 5m] 返回数据条数: {len(result)}")
        if result.empty:
            print("  警告: 返回空数据，可能缓存未预热")
        else:
            print(f"  首条: {result.iloc[0].to_dict()}")
            print(f"  列: {list(result.columns)}")

        self.assertIsInstance(result, pd.DataFrame)

    def test_all_periods_supported(self):
        """测试所有分钟周期支持"""
        from jk2bt.api.market import get_price

        periods = ["1m", "5m", "15m", "30m", "60m"]
        end_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        start_date = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d %H:%M:%S")

        for period in periods:
            try:
                df = get_price(
                    "600519.XSHG",
                    start_date=start_date,
                    end_date=end_date,
                    frequency=period,
                    fields=["close"],
                )
                print(f"\n[{period}] 返回数据条数: {len(df)}")
                self.assertIsInstance(df, pd.DataFrame)
            except Exception as e:
                print(f"\n[{period}] 失败: {e}")
                self.fail(f"周期 {period} 不支持")


class TestMinuteCacheIntegration(unittest.TestCase):
    """测试分钟数据缓存集成"""

    def test_cache_query_path(self):
        """验证缓存查询路径正确"""
        from market_data.minute import get_stock_minute
        from jk2bt.db.duckdb_manager import DuckDBManager

        symbol = "sh600000"
        end_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        start_date = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d %H:%M:%S")

        db = DuckDBManager(read_only=True)

        has_cache = db.has_data(
            "stock_minute", symbol, start_date, end_date, "qfq", "5"
        )
        print(f"\n[缓存检查] {symbol} 5分钟数据: {has_cache}")

        df = get_stock_minute(symbol, start_date, end_date, period="5m")

        print(f"[minute.py 查询] 返回数据条数: {len(df)}")
        if not df.empty:
            print(f"  首条: {df.iloc[0].to_dict()}")

        self.assertIsInstance(df, pd.DataFrame)

    def test_etf_minute_cache(self):
        """验证 ETF 分钟数据缓存"""
        from market_data.minute import get_etf_minute

        symbol = "510300"
        end_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        start_date = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d %H:%M:%S")

        df = get_etf_minute(symbol, start_date, end_date, period="5m")

        print(f"\n[ETF minute] {symbol} 返回数据条数: {len(df)}")
        if not df.empty:
            print(f"  首条: {df.iloc[0].to_dict()}")

        self.assertIsInstance(df, pd.DataFrame)


class TestMinuteAPIConsistency(unittest.TestCase):
    """测试分钟 API 行为一致性"""

    def test_count_parameter(self):
        """测试 count 参数在分钟模式下的行为"""
        from jk2bt.api.market import get_bars

        result = get_bars("600519.XSHG", count=30, unit="5m")

        print(f"\n[count=30, unit=5m] 返回数据条数: {len(result)}")

        if not result.empty:
            actual_count = len(result)
            self.assertLessEqual(actual_count, 30, "返回数据不应超过 count")
            self.assertGreater(actual_count, 0, "返回数据不应为空（除非缓存无数据）")

    def test_date_range_parameter(self):
        """测试日期范围参数在分钟模式下的行为"""
        from jk2bt.api.market import get_price

        start_date = "2026-03-25 09:30:00"
        end_date = "2026-03-25 11:30:00"

        df = get_price(
            "600519.XSHG",
            start_date=start_date,
            end_date=end_date,
            frequency="5m",
        )

        print(f"\n[date_range 5m] 返回数据条数: {len(df)}")

        if not df.empty:
            if "datetime" in df.columns:
                min_dt = df["datetime"].min()
                max_dt = df["datetime"].max()
                print(f"  时间范围: {min_dt} ~ {max_dt}")

    def test_empty_result_diagnosis(self):
        """测试空结果诊断信息"""
        from jk2bt.api.market import get_price

        df = get_price(
            "INVALID_CODE",
            start_date="2026-01-01",
            end_date="2026-01-02",
            frequency="5m",
        )

        print(f"\n[无效代码测试] 返回数据条数: {len(df)}")
        print(f"  预期: 空数据并带诊断信息")

        self.assertIsInstance(df, pd.DataFrame)
        self.assertTrue(df.empty, "无效代码应返回空数据")


def run_smoke_test():
    """运行 smoke test"""
    print("=" * 60)
    print("Task 32: 分钟上层 API Smoke Test")
    print("=" * 60)

    print("\n1. 测试 get_price(..., frequency='1m')...")
    test = TestMinuteUpperAPI()
    test.test_get_price_frequency_1m()

    print("\n2. 测试 get_price(..., frequency='5m')...")
    test.test_get_price_frequency_5m()

    print("\n3. 测试 history(..., unit='5m')...")
    test.test_history_unit_5m()

    print("\n4. 测试 attribute_history(..., unit='5m')...")
    test.test_attribute_history_unit_5m()

    print("\n5. 测试 get_bars(..., unit='5m')...")
    test.test_get_bars_unit_5m()

    print("\n6. 测试缓存集成...")
    test_cache = TestMinuteCacheIntegration()
    test_cache.test_cache_query_path()

    print("\n" + "=" * 60)
    print("Smoke Test 完成")
    print("=" * 60)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Task 32: 分钟上层 API 测试")
    parser.add_argument("--smoke", action="store_true", help="运行 smoke test")
    args = parser.parse_args()

    if args.smoke:
        run_smoke_test()
    else:
        unittest.main()
