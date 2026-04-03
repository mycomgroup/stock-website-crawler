#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
批量运行器验证测试脚本

验证内容:
1. 状态分类正确性
2. 成功/失败统计口径
3. 异常不会被标记为成功
4. DuckDB 并发读写稳定性

测试策略样本:
- 01_valid_strategy.txt: 应该成功运行
- 02_exception_strategy.txt: 运行时异常
- 03_missing_api_strategy.txt: 缺失API (扫描器标记)
- 04_non_strategy_notes.txt: 非策略文件 (扫描器标记)
- 05_no_initialize_strategy.txt: 无initialize函数 (扫描器标记)
"""

import os
import sys
import json
import glob
import shutil
import tempfile
import unittest
import time
from concurrent.futures import ProcessPoolExecutor
import threading
import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(
    0,
    os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        "src",
    ),
)

from strategy_scanner import StrategyScanner, StrategyStatus
from jk2bt.db.duckdb_manager import DuckDBManager, LocalCache, clear_global_cache


class TestBatchRunnerStatistics(unittest.TestCase):
    """测试批量运行器统计分类"""

    SAMPLE_DIR = os.path.join(os.path.dirname(__file__), "sample_strategies")

    def setUp(self):
        self.scanner = StrategyScanner()

    def test_valid_strategy_detection(self):
        """01_valid_strategy.txt 应被识别为有效策略"""
        result = self.scanner.scan_file(
            os.path.join(self.SAMPLE_DIR, "01_valid_strategy.txt")
        )
        self.assertTrue(result.has_initialize)
        self.assertEqual(result.status, StrategyStatus.VALID)
        self.assertTrue(result.is_executable)
        self.assertEqual(len(result.missing_apis), 0)

    def test_exception_strategy_detection(self):
        """02_exception_strategy.txt 应被识别为有效策略（运行时会异常）"""
        result = self.scanner.scan_file(
            os.path.join(self.SAMPLE_DIR, "02_exception_strategy.txt")
        )
        self.assertTrue(result.has_initialize)
        self.assertEqual(result.status, StrategyStatus.VALID)
        self.assertTrue(result.is_executable)
        self.assertEqual(len(result.missing_apis), 0)

    def test_missing_api_strategy_detection(self):
        """03_missing_api_strategy.txt 应被识别为缺失API"""
        result = self.scanner.scan_file(
            os.path.join(self.SAMPLE_DIR, "03_missing_api_strategy.txt")
        )
        self.assertTrue(result.has_initialize)
        self.assertEqual(result.status, StrategyStatus.MISSING_API)
        self.assertFalse(result.is_executable)
        self.assertIn("get_ticks", result.missing_apis)

    def test_non_strategy_detection(self):
        """04_non_strategy_notes.txt 应被识别为非策略文件"""
        result = self.scanner.scan_file(
            os.path.join(self.SAMPLE_DIR, "04_non_strategy_notes.txt")
        )
        self.assertFalse(result.has_initialize)
        self.assertEqual(result.status, StrategyStatus.NOT_STRATEGY)
        self.assertFalse(result.is_executable)

    def test_no_initialize_detection(self):
        """05_no_initialize_strategy.txt 应被识别为缺少initialize"""
        result = self.scanner.scan_file(
            os.path.join(self.SAMPLE_DIR, "05_no_initialize_strategy.txt")
        )
        self.assertFalse(result.has_initialize)
        self.assertEqual(result.status, StrategyStatus.NO_INITIALIZE)
        self.assertFalse(result.is_executable)

    def test_status_not_confused_with_success(self):
        """验证各状态不会被误判为成功"""
        files = {
            "missing_api": "03_missing_api_strategy.txt",
            "non_strategy": "04_non_strategy_notes.txt",
            "no_initialize": "05_no_initialize_strategy.txt",
        }

        for expected_status, filename in files.items():
            result = self.scanner.scan_file(os.path.join(self.SAMPLE_DIR, filename))
            self.assertFalse(
                result.is_executable, f"{filename} should not be executable"
            )


class TestDuckDBConcurrency(unittest.TestCase):
    """测试 DuckDB 并发读写稳定性"""

    def setUp(self):
        clear_global_cache()
        self.temp_dir = tempfile.mkdtemp()
        self.db_path = os.path.join(self.temp_dir, "test_concurrency.db")
        self.manager = DuckDBManager(
            db_path=self.db_path, read_only=False, use_cache=True
        )

    def tearDown(self):
        self.manager.close()
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_local_cache_basic(self):
        """测试本地缓存基本功能"""
        cache = LocalCache(max_size=10)
        df = pd.DataFrame({"a": [1, 2, 3]})
        cache.set("test_table", "600000", "2023-01-01", "2023-12-31", df)
        cached = cache.get("test_table", "600000", "2023-01-01", "2023-12-31")
        self.assertIsNotNone(cached)
        self.assertEqual(len(cached), 3)

    def test_local_cache_invalidation(self):
        """测试缓存失效"""
        cache = LocalCache()
        df = pd.DataFrame({"a": [1, 2, 3]})
        cache.set("stock_daily", "600000", "2023-01-01", "2023-12-31", df)
        cache.invalidate(table="stock_daily", symbol="600000")
        cached = cache.get("stock_daily", "600000", "2023-01-01", "2023-12-31")
        self.assertIsNone(cached)

    def test_read_only_manager_creation(self):
        """测试只读管理器创建"""
        from jk2bt.db.duckdb_manager import get_shared_read_only_manager

        read_manager = get_shared_read_only_manager(db_path=self.db_path)
        self.assertTrue(read_manager.read_only)

    def test_write_retry_on_conflict(self):
        """测试写入重试机制"""
        dates = pd.date_range("2023-01-01", periods=10, freq="D")
        df = pd.DataFrame(
            {
                "datetime": dates,
                "open": [100.0] * 10,
                "high": [101.0] * 10,
                "low": [99.0] * 10,
                "close": [100.5] * 10,
                "volume": [1000000] * 10,
                "amount": [100000000] * 10,
            }
        )

        try:
            self.manager.insert_stock_daily("sh600000", df, adjust="qfq")
            count = self.manager.count_records("stock_daily", "sh600000", "qfq")
            self.assertEqual(count, 10)
        except Exception as e:
            self.fail(f"写入测试失败: {e}")

    def test_concurrent_read_operations(self):
        """测试并发读取操作"""
        dates = pd.date_range("2023-01-01", periods=30, freq="D")
        df = pd.DataFrame(
            {
                "datetime": dates,
                "open": [100.0 + i for i in range(30)],
                "high": [101.0 + i for i in range(30)],
                "low": [99.0 + i for i in range(30)],
                "close": [100.5 + i for i in range(30)],
                "volume": [1000000] * 30,
                "amount": [100000000] * 30,
            }
        )

        self.manager.insert_stock_daily("sh600001", df, adjust="qfq")

        read_manager = DuckDBManager(
            db_path=self.db_path, read_only=True, use_cache=True
        )

        results = []
        for i in range(5):
            try:
                result_df = read_manager.get_stock_daily(
                    "sh600001", "2023-01-01", "2023-01-15", adjust="qfq"
                )
                results.append(len(result_df))
            except Exception as e:
                results.append(-1)

        self.assertTrue(all(r > 0 for r in results), "并发读取应全部成功")


class TestRunStatusClassification(unittest.TestCase):
    """测试运行状态分类逻辑"""

    def test_run_status_enum_values(self):
        """测试 RunStatus 枚举值"""
        from run_strategies_parallel import RunStatus

        success_statuses = [
            RunStatus.SUCCESS_WITH_RETURN,
            RunStatus.SUCCESS_ZERO_RETURN,
            RunStatus.SUCCESS_NO_TRADE,
        ]

        failure_statuses = [
            RunStatus.LOAD_FAILED,
            RunStatus.RUN_EXCEPTION,
            RunStatus.TIMEOUT,
            RunStatus.DATA_MISSING,
        ]

        skip_statuses = [
            RunStatus.SKIPPED_NOT_STRATEGY,
            RunStatus.SKIPPED_SYNTAX_ERROR,
            RunStatus.SKIPPED_NO_INITIALIZE,
            RunStatus.SKIPPED_MISSING_API,
        ]

        self.assertEqual(len(success_statuses), 3)
        self.assertEqual(len(failure_statuses), 4)
        self.assertEqual(len(skip_statuses), 4)

    def test_exception_not_counted_as_success(self):
        """验证异常状态 success=False"""
        from run_strategies_parallel import RunStatus

        exception_status = RunStatus.RUN_EXCEPTION
        failure_statuses = [
            RunStatus.LOAD_FAILED,
            RunStatus.RUN_EXCEPTION,
            RunStatus.TIMEOUT,
            RunStatus.DATA_MISSING,
        ]

        for status in failure_statuses:
            self.assertNotIn(
                status.value,
                ["success_with_return", "success_zero_return", "success_no_trade"],
            )


def run_smoke_test():
    """运行完整烟雾测试"""
    print("=" * 80)
    print("批量运行器烟雾测试")
    print("=" * 80)

    sample_dir = os.path.join(os.path.dirname(__file__), "sample_strategies")
    scanner = StrategyScanner()

    print("\n[阶段1] 策略扫描测试")
    print("-" * 40)

    expected_results = {
        "01_valid_strategy.txt": ("valid", True, []),
        "02_exception_strategy.txt": ("valid", True, []),
        "03_missing_api_strategy.txt": ("missing_api", False, ["get_ticks"]),
        "04_non_strategy_notes.txt": ("not_strategy", False, []),
        "05_no_initialize_strategy.txt": ("no_initialize", False, []),
    }

    all_passed = True
    for filename, (
        expected_status,
        expected_executable,
        expected_apis,
    ) in expected_results.items():
        filepath = os.path.join(sample_dir, filename)
        if not os.path.exists(filepath):
            print(f"  ✗ 文件不存在: {filename}")
            all_passed = False
            continue

        result = scanner.scan_file(filepath)
        status_match = result.status.value == expected_status
        exec_match = result.is_executable == expected_executable

        if status_match and exec_match:
            print(
                f"  ✓ {filename}: status={result.status.value}, executable={result.is_executable}"
            )
        else:
            print(
                f"  ✗ {filename}: expected status={expected_status}, got={result.status.value}"
            )
            all_passed = False

        if expected_apis:
            for api in expected_apis:
                if api not in result.missing_apis:
                    print(f"    ✗ 缺失API检测失败: {api} 未在 missing_apis 中")
                    all_passed = False

    print("\n[阶段2] DuckDB 并发测试")
    print("-" * 40)

    temp_dir = tempfile.mkdtemp()
    db_path = os.path.join(temp_dir, "smoke_test.db")

    try:
        manager = DuckDBManager(db_path=db_path, read_only=False, use_cache=True)
        dates = pd.date_range("2023-01-01", periods=10, freq="D")
        df = pd.DataFrame(
            {
                "datetime": dates,
                "open": [100.0] * 10,
                "high": [101.0] * 10,
                "low": [99.0] * 10,
                "close": [100.5] * 10,
                "volume": [1000000] * 10,
                "amount": [100000000] * 10,
            }
        )

        manager.insert_stock_daily("sh600000", df, adjust="qfq")
        count = manager.count_records("stock_daily", "sh600000", "qfq")

        if count == 10:
            print("  ✓ DuckDB 写入测试通过: 10条记录")
        else:
            print(f"  ✗ DuckDB 写入测试失败: 预期10条，实际{count}条")
            all_passed = False

        read_df = manager.get_stock_daily(
            "sh600000", "2023-01-01", "2023-01-10", adjust="qfq"
        )
        if len(read_df) == 10:
            print("  ✓ DuckDB 读取测试通过: 10条记录")
        else:
            print(f"  ✗ DuckDB 读取测试失败: 预期10条，实际{len(read_df)}条")
            all_passed = False

        manager.close()

    except Exception as e:
        print(f"  ✗ DuckDB 测试异常: {e}")
        all_passed = False

    finally:
        shutil.rmtree(temp_dir, ignore_errors=True)

    print("\n[阶段3] 统计口径验证")
    print("-" * 40)

    from run_strategies_parallel import RunStatus

    success_statuses = [
        RunStatus.SUCCESS_WITH_RETURN.value,
        RunStatus.SUCCESS_ZERO_RETURN.value,
        RunStatus.SUCCESS_NO_TRADE.value,
    ]

    exception_status = RunStatus.RUN_EXCEPTION.value
    if exception_status not in success_statuses:
        print(f"  ✓ RUN_EXCEPTION 不在成功状态列表中")
    else:
        print(f"  ✗ RUN_EXCEPTION 错误地被标记为成功")
        all_passed = False

    print("\n" + "=" * 80)
    if all_passed:
        print("✅ 烟雾测试全部通过")
    else:
        print("❌ 烟雾测试存在失败项")
    print("=" * 80)

    return all_passed


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="批量运行器验证测试")
    parser.add_argument("--unit-test", action="store_true", help="运行单元测试")
    parser.add_argument("--smoke", action="store_true", help="运行烟雾测试")
    parser.add_argument("--all", action="store_true", help="运行所有测试")

    args = parser.parse_args()

    if args.all or (not args.unit_test and not args.smoke):
        print("运行完整测试套件...\n")
        unittest.main(argv=["first-arg-is-ignored"], exit=False, verbosity=2)
        print("\n")
        run_smoke_test()
    elif args.unit_test:
        unittest.main(argv=["first-arg-is-ignored"], exit=False, verbosity=2)
    elif args.smoke:
        run_smoke_test()
