#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
批量运行器扩展测试脚本

补充测试用例覆盖度:
- 策略扫描器: 语法错误、空文件、多API缺失、handle_data策略
- DuckDB: LRU缓存、批量操作、边界条件、ETF/指数数据
- RunStatus分类: _classify_run_status各种场景、超时、数据缺失
- 并发测试: 多进程并发、高并发场景、缓存一致性
"""

import os
import sys
import json
import glob
import shutil
import tempfile
import unittest
import time
import threading
import pandas as pd
from concurrent.futures import ThreadPoolExecutor

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(
    0,
    os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        "src",
    ),
)

from strategy_scanner import (
    StrategyScanner,
    StrategyStatus,
    quick_scan_strategy,
    batch_scan_strategies,
)
from jk2bt.db.duckdb_manager import DuckDBManager, LocalCache, clear_global_cache


class TestStrategyScannerExtended(unittest.TestCase):
    """策略扫描器扩展测试"""

    SAMPLE_DIR = os.path.join(os.path.dirname(__file__), "sample_strategies")

    def setUp(self):
        self.scanner = StrategyScanner()

    def test_syntax_error_detection(self):
        """06_syntax_error.txt 应被识别为语法错误"""
        result = self.scanner.scan_file(
            os.path.join(self.SAMPLE_DIR, "06_syntax_error.txt")
        )
        self.assertEqual(result.status, StrategyStatus.SYNTAX_ERROR)
        self.assertFalse(result.is_executable)
        self.assertIn("语法错误", result.error_message)

    def test_empty_file_detection(self):
        """07_empty_file.txt 应被识别为空文件"""
        result = self.scanner.scan_file(
            os.path.join(self.SAMPLE_DIR, "07_empty_file.txt")
        )
        self.assertEqual(result.status, StrategyStatus.EMPTY_FILE)
        self.assertFalse(result.is_executable)
        self.assertIn("空文件", result.error_message)

    def test_multiple_missing_api_detection(self):
        """08_multiple_missing_api.txt 应识别多个缺失API"""
        result = self.scanner.scan_file(
            os.path.join(self.SAMPLE_DIR, "08_multiple_missing_api.txt")
        )
        self.assertEqual(result.status, StrategyStatus.MISSING_API)
        self.assertFalse(result.is_executable)
        self.assertIn("get_ticks", result.missing_apis)
        self.assertIn("get_margin_info", result.missing_apis)
        self.assertIn("get_future_contracts", result.missing_apis)
        self.assertEqual(len(result.missing_apis), 3)

    def test_valid_etf_strategy_detection(self):
        """09_valid_etf_strategy.txt 应被识别为有效策略"""
        result = self.scanner.scan_file(
            os.path.join(self.SAMPLE_DIR, "09_valid_etf_strategy.txt")
        )
        self.assertTrue(result.has_initialize)
        self.assertEqual(result.status, StrategyStatus.VALID)
        self.assertTrue(result.is_executable)
        self.assertEqual(len(result.missing_apis), 0)

    def test_handle_data_strategy_detection(self):
        """10_handle_data_strategy.txt 应被识别为有效策略"""
        result = self.scanner.scan_file(
            os.path.join(self.SAMPLE_DIR, "10_handle_data_strategy.txt")
        )
        self.assertTrue(result.has_initialize)
        self.assertTrue(result.has_handle)
        self.assertEqual(result.status, StrategyStatus.VALID)
        self.assertTrue(result.is_executable)

    def test_nonexistent_file(self):
        """不存在的文件应返回 NOT_STRATEGY"""
        result = self.scanner.scan_file("/nonexistent/path/file.txt")
        self.assertEqual(result.status, StrategyStatus.NOT_STRATEGY)
        self.assertFalse(result.is_executable)
        self.assertIn("文件不存在", result.error_message)

    def test_directory_scan(self):
        """测试目录扫描功能"""
        results = self.scanner.scan_directory(self.SAMPLE_DIR, "*.txt")
        self.assertIn("all", results)
        self.assertIn("valid", results)
        self.assertIn("missing_api", results)
        self.assertIn("not_strategy", results)
        self.assertIn("syntax_error", results)
        total = len(results["all"])
        self.assertGreater(total, 0)

    def test_executable_strategies_list(self):
        """测试获取可执行策略列表"""
        executable = self.scanner.get_executable_strategies(self.SAMPLE_DIR, "*.txt")
        self.assertIsInstance(executable, list)
        for filepath in executable:
            result = self.scanner.scan_file(filepath)
            self.assertTrue(result.is_executable)

    def test_quick_scan_function(self):
        """测试快速扫描函数"""
        is_exec, msg = quick_scan_strategy(
            os.path.join(self.SAMPLE_DIR, "01_valid_strategy.txt")
        )
        self.assertTrue(is_exec)

        is_exec, msg = quick_scan_strategy(
            os.path.join(self.SAMPLE_DIR, "03_missing_api_strategy.txt")
        )
        self.assertFalse(is_exec)

    def test_batch_scan_function(self):
        """测试批量扫描函数"""
        results = batch_scan_strategies(self.SAMPLE_DIR, "*.txt")
        self.assertIn("executable", results)
        self.assertIn("invalid", results)
        self.assertGreater(len(results["executable"]), 0)
        self.assertGreater(len(results["invalid"]), 0)

    def test_cache_mechanism(self):
        """测试扫描器缓存机制"""
        filepath = os.path.join(self.SAMPLE_DIR, "01_valid_strategy.txt")
        result1 = self.scanner.scan_file(filepath)
        result2 = self.scanner.scan_file(filepath)
        self.assertEqual(result1.status, result2.status)
        self.assertEqual(result1.file_path, result2.file_path)

    def test_details_extraction(self):
        """测试详情提取"""
        result = self.scanner.scan_file(
            os.path.join(self.SAMPLE_DIR, "01_valid_strategy.txt")
        )
        self.assertIn("defined_funcs", result.details)
        self.assertIn("called_funcs", result.details)
        self.assertIn("code_lines", result.details)
        self.assertIn("initialize", result.details["defined_funcs"])


class TestDuckDBExtended(unittest.TestCase):
    """DuckDB 扩展测试"""

    def setUp(self):
        clear_global_cache()
        self.temp_dir = tempfile.mkdtemp()
        self.db_path = os.path.join(self.temp_dir, "test_extended.db")
        self.manager = DuckDBManager(
            db_path=self.db_path, read_only=False, use_cache=True
        )

    def tearDown(self):
        self.manager.close()
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_lru_cache_eviction(self):
        """测试 LRU 缓存淘汰机制"""
        cache = LocalCache(max_size=3)
        for i in range(5):
            df = pd.DataFrame({"a": [i]})
            cache.set("table", f"stock{i}", "2023-01-01", "2023-12-31", df)

        cached0 = cache.get("table", "stock0", "2023-01-01", "2023-12-31")
        cached1 = cache.get("table", "stock1", "2023-01-01", "2023-12-31")
        cached4 = cache.get("table", "stock4", "2023-01-01", "2023-12-31")

        self.assertIsNone(cached0)
        self.assertIsNone(cached1)
        self.assertIsNotNone(cached4)

    def test_batch_insert(self):
        """测试批量插入"""
        symbols = ["sh600000", "sh600001", "sh600002", "sh600003", "sh600004"]
        dates = pd.date_range("2023-01-01", periods=10, freq="D")

        for symbol in symbols:
            df = pd.DataFrame(
                {
                    "datetime": dates,
                    "open": [100.0 + i for i in range(10)],
                    "high": [101.0 + i for i in range(10)],
                    "low": [99.0 + i for i in range(10)],
                    "close": [100.5 + i for i in range(10)],
                    "volume": [1000000] * 10,
                    "amount": [100000000] * 10,
                }
            )
            self.manager.insert_stock_daily(symbol, df, adjust="qfq")

        total_count = self.manager.count_records("stock_daily")
        self.assertEqual(total_count, 50)

    def test_empty_dataframe_handling(self):
        """测试空 DataFrame 处理"""
        empty_df = pd.DataFrame()
        self.manager.insert_stock_daily("sh999999", empty_df, adjust="qfq")
        count = self.manager.count_records("stock_daily", "sh999999", "qfq")
        self.assertEqual(count, 0)

    def test_duplicate_insert_replace(self):
        """测试重复插入 REPLACE 行为"""
        dates = pd.date_range("2023-01-01", periods=5, freq="D")
        df1 = pd.DataFrame(
            {
                "datetime": dates,
                "open": [100.0] * 5,
                "high": [101.0] * 5,
                "low": [99.0] * 5,
                "close": [100.5] * 5,
                "volume": [1000000] * 5,
                "amount": [100000000] * 5,
            }
        )

        self.manager.insert_stock_daily("sh600100", df1, adjust="qfq")
        count1 = self.manager.count_records("stock_daily", "sh600100", "qfq")

        df2 = pd.DataFrame(
            {
                "datetime": dates,
                "open": [200.0] * 5,
                "high": [201.0] * 5,
                "low": [199.0] * 5,
                "close": [200.5] * 5,
                "volume": [2000000] * 5,
                "amount": [200000000] * 5,
            }
        )

        self.manager.insert_stock_daily("sh600100", df2, adjust="qfq")
        count2 = self.manager.count_records("stock_daily", "sh600100", "qfq")

        self.assertEqual(count1, 5)
        self.assertEqual(count2, 5)

        read_df = self.manager.get_stock_daily(
            "sh600100", "2023-01-01", "2023-01-05", adjust="qfq"
        )
        self.assertEqual(read_df["close"].iloc[0], 200.5)

    def test_etf_daily_operations(self):
        """测试 ETF 日线数据操作"""
        dates = pd.date_range("2023-01-01", periods=10, freq="D")
        df = pd.DataFrame(
            {
                "datetime": dates,
                "open": [50.0 + i for i in range(10)],
                "high": [51.0 + i for i in range(10)],
                "low": [49.0 + i for i in range(10)],
                "close": [50.5 + i for i in range(10)],
                "volume": [5000000] * 10,
                "amount": [250000000] * 10,
            }
        )

        self.manager.insert_etf_daily("510300", df)
        count = self.manager.count_records("etf_daily", "510300")
        self.assertEqual(count, 10)

        read_df = self.manager.get_etf_daily("510300", "2023-01-01", "2023-01-10")
        self.assertEqual(len(read_df), 10)

    def test_index_daily_operations(self):
        """测试指数日线数据操作"""
        dates = pd.date_range("2023-01-01", periods=10, freq="D")
        df = pd.DataFrame(
            {
                "datetime": dates,
                "open": [3000.0 + i for i in range(10)],
                "high": [3010.0 + i for i in range(10)],
                "low": [2990.0 + i for i in range(10)],
                "close": [3005.0 + i for i in range(10)],
                "volume": [10000000] * 10,
                "amount": [30000000000] * 10,
            }
        )

        self.manager.insert_index_daily("000300", df)
        count = self.manager.count_records("index_daily", "000300")
        self.assertEqual(count, 10)

        read_df = self.manager.get_index_daily("000300", "2023-01-01", "2023-01-10")
        self.assertEqual(len(read_df), 10)

    def test_has_data_check(self):
        """测试数据范围检查"""
        dates = pd.date_range("2023-01-01", periods=30, freq="D")
        df = pd.DataFrame(
            {
                "datetime": dates,
                "open": [100.0] * 30,
                "high": [101.0] * 30,
                "low": [99.0] * 30,
                "close": [100.5] * 30,
                "volume": [1000000] * 30,
                "amount": [100000000] * 30,
            }
        )

        self.manager.insert_stock_daily("sh600200", df, adjust="qfq")

        has_full = self.manager.has_data(
            "stock_daily", "sh600200", "2023-01-01", "2023-01-30", adjust="qfq"
        )
        self.assertTrue(has_full)

        has_partial = self.manager.has_data(
            "stock_daily", "sh600200", "2022-12-01", "2023-01-30", adjust="qfq"
        )
        self.assertFalse(has_partial)

        has_no_data = self.manager.has_data(
            "stock_daily", "sh600999", "2023-01-01", "2023-01-30", adjust="qfq"
        )
        self.assertFalse(has_no_data)

    def test_get_symbols(self):
        """测试获取所有代码"""
        dates = pd.date_range("2023-01-01", periods=5, freq="D")
        for symbol in ["sh600001", "sh600002", "sh600003"]:
            df = pd.DataFrame(
                {
                    "datetime": dates,
                    "open": [100.0] * 5,
                    "high": [101.0] * 5,
                    "low": [99.0] * 5,
                    "close": [100.5] * 5,
                    "volume": [1000000] * 5,
                    "amount": [100000000] * 5,
                }
            )
            self.manager.insert_stock_daily(symbol, df, adjust="qfq")

        symbols = self.manager.get_symbols("stock_daily")
        self.assertIn("sh600001", symbols)
        self.assertIn("sh600002", symbols)
        self.assertIn("sh600003", symbols)

    def test_clear_table(self):
        """测试清空表"""
        dates = pd.date_range("2023-01-01", periods=5, freq="D")
        df = pd.DataFrame(
            {
                "datetime": dates,
                "open": [100.0] * 5,
                "high": [101.0] * 5,
                "low": [99.0] * 5,
                "close": [100.5] * 5,
                "volume": [1000000] * 5,
                "amount": [100000000] * 5,
            }
        )

        self.manager.insert_stock_daily("sh600300", df, adjust="qfq")
        count_before = self.manager.count_records("stock_daily", "sh600300", "qfq")
        self.assertEqual(count_before, 5)

        self.manager.clear_table("stock_daily", symbol="sh600300", adjust="qfq")
        count_after = self.manager.count_records("stock_daily", "sh600300", "qfq")
        self.assertEqual(count_after, 0)


class TestRunStatusClassificationExtended(unittest.TestCase):
    """RunStatus 分类扩展测试"""

    def test_classify_with_exception(self):
        """测试异常分类逻辑"""
        from run_strategies_parallel import _classify_run_status, RunStatus

        result = _classify_run_status(
            backtest_result=None,
            exception=RuntimeError("测试异常"),
            has_data=True,
            scan_result=None,
        )
        self.assertEqual(result, RunStatus.RUN_EXCEPTION)

    def test_classify_timeout_exception(self):
        """测试超时分类"""
        from run_strategies_parallel import _classify_run_status, RunStatus

        result = _classify_run_status(
            backtest_result=None,
            exception=TimeoutError("timeout test"),
            has_data=True,
            scan_result=None,
        )
        self.assertEqual(result, RunStatus.TIMEOUT)

    def test_classify_data_missing_exception(self):
        """测试数据缺失分类"""
        from run_strategies_parallel import _classify_run_status, RunStatus

        result = _classify_run_status(
            backtest_result=None,
            exception=RuntimeError("无数据或股票不存在"),
            has_data=False,
            scan_result=None,
        )
        self.assertEqual(result, RunStatus.DATA_MISSING)

    def test_classify_load_failed(self):
        """测试加载失败分类"""
        from run_strategies_parallel import _classify_run_status, RunStatus

        result = _classify_run_status(
            backtest_result=None,
            exception=None,
            has_data=True,
            scan_result=None,
        )
        self.assertEqual(result, RunStatus.LOAD_FAILED)

    def test_classify_success_with_return(self):
        """测试成功有收益分类"""
        from run_strategies_parallel import _classify_run_status, RunStatus

        class MockStrategy:
            navs = [1.0, 1.1, 1.2]

        mock_backtest = {
            "strategy": MockStrategy(),
            "pnl_pct": 10.0,
        }

        result = _classify_run_status(
            backtest_result=mock_backtest,
            exception=None,
            has_data=True,
            scan_result=None,
        )
        self.assertEqual(result, RunStatus.SUCCESS_WITH_RETURN)

    def test_classify_success_zero_return(self):
        """测试成功零收益分类"""
        from run_strategies_parallel import _classify_run_status, RunStatus

        class MockStrategy:
            navs = [1.0, 1.0, 1.0]

        mock_backtest = {
            "strategy": MockStrategy(),
            "pnl_pct": 0.0,
        }

        result = _classify_run_status(
            backtest_result=mock_backtest,
            exception=None,
            has_data=True,
            scan_result=None,
        )
        self.assertEqual(result, RunStatus.SUCCESS_ZERO_RETURN)

    def test_classify_success_no_trade(self):
        """测试成功无交易分类"""
        from run_strategies_parallel import _classify_run_status, RunStatus

        class MockStrategy:
            navs = None

        mock_backtest = {
            "strategy": MockStrategy(),
            "pnl_pct": 0.0,
        }

        result = _classify_run_status(
            backtest_result=mock_backtest,
            exception=None,
            has_data=True,
            scan_result=None,
        )
        self.assertEqual(result, RunStatus.SUCCESS_NO_TRADE)

    def test_success_statuses_only_three(self):
        """验证只有三种成功状态"""
        from run_strategies_parallel import RunStatus

        success_statuses = [
            RunStatus.SUCCESS_WITH_RETURN,
            RunStatus.SUCCESS_ZERO_RETURN,
            RunStatus.SUCCESS_NO_TRADE,
        ]

        all_statuses = list(RunStatus)
        non_success_statuses = [s for s in all_statuses if s not in success_statuses]

        self.assertEqual(len(success_statuses), 3)
        self.assertEqual(len(non_success_statuses), 11)

    def test_status_value_strings(self):
        """测试状态值字符串格式"""
        from run_strategies_parallel import RunStatus

        self.assertEqual(RunStatus.SUCCESS_WITH_RETURN.value, "success_with_return")
        self.assertEqual(RunStatus.RUN_EXCEPTION.value, "run_exception")
        self.assertEqual(RunStatus.SKIPPED_NOT_STRATEGY.value, "skipped_not_strategy")


class TestConcurrencyExtended(unittest.TestCase):
    """并发扩展测试"""

    def setUp(self):
        clear_global_cache()
        self.temp_dir = tempfile.mkdtemp()
        self.db_path = os.path.join(self.temp_dir, "test_concurrency_extended.db")
        self.manager = DuckDBManager(
            db_path=self.db_path, read_only=False, use_cache=False
        )

    def tearDown(self):
        self.manager.close()
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_high_concurrency_read(self):
        """测试高并发读取"""
        dates = pd.date_range("2023-01-01", periods=100, freq="D")
        df = pd.DataFrame(
            {
                "datetime": dates,
                "open": [100.0 + i for i in range(100)],
                "high": [101.0 + i for i in range(100)],
                "low": [99.0 + i for i in range(100)],
                "close": [100.5 + i for i in range(100)],
                "volume": [1000000] * 100,
                "amount": [100000000] * 100,
            }
        )

        self.manager.insert_stock_daily("sh600500", df, adjust="qfq")

        results = {"success": 0, "failure": 0}

        def read_task():
            try:
                reader = DuckDBManager(
                    db_path=self.db_path, read_only=True, use_cache=True
                )
                read_df = reader.get_stock_daily(
                    "sh600500", "2023-01-01", "2023-01-30", adjust="qfq"
                )
                if len(read_df) > 0:
                    results["success"] += 1
                else:
                    results["failure"] += 1
                reader.close()
            except Exception as e:
                results["failure"] += 1

        threads = []
        for i in range(20):
            t = threading.Thread(target=read_task)
            threads.append(t)
            t.start()

        for t in threads:
            t.join(timeout=10)

        self.assertEqual(results["success"], 20)
        self.assertEqual(results["failure"], 0)

    def test_concurrent_cache_consistency(self):
        """测试并发缓存一致性"""
        cache = LocalCache(max_size=50)

        results = {"success": 0, "failure": 0}

        def cache_task(idx):
            try:
                df = pd.DataFrame({"a": [idx]})
                cache.set("table", f"stock{idx}", "2023-01-01", "2023-12-31", df)
                cached = cache.get("table", f"stock{idx}", "2023-01-01", "2023-12-31")
                if cached is not None and cached["a"].iloc[0] == idx:
                    results["success"] += 1
                else:
                    results["failure"] += 1
            except Exception:
                results["failure"] += 1

        threads = []
        for i in range(10):
            t = threading.Thread(target=cache_task, args=(i,))
            threads.append(t)
            t.start()

        for t in threads:
            t.join(timeout=5)

        self.assertEqual(results["success"], 10)

    def test_mixed_read_write_stress(self):
        """测试读写混合压力"""
        dates = pd.date_range("2023-01-01", periods=50, freq="D")

        results = {"read_success": 0, "write_success": 0, "failure": 0}

        def write_task(idx):
            try:
                writer = DuckDBManager(
                    db_path=self.db_path, read_only=False, use_cache=False
                )
                df = pd.DataFrame(
                    {
                        "datetime": dates,
                        "open": [100.0 + idx] * 50,
                        "high": [101.0 + idx] * 50,
                        "low": [99.0 + idx] * 50,
                        "close": [100.5 + idx] * 50,
                        "volume": [1000000] * 50,
                        "amount": [100000000] * 50,
                    }
                )
                writer.insert_stock_daily(f"sh601{idx:03d}", df, adjust="qfq")
                results["write_success"] += 1
                writer.close()
            except Exception:
                results["failure"] += 1

        def read_task():
            try:
                reader = DuckDBManager(
                    db_path=self.db_path, read_only=True, use_cache=True
                )
                symbols = reader.get_symbols("stock_daily")
                if len(symbols) >= 0:
                    results["read_success"] += 1
                reader.close()
            except Exception:
                results["failure"] += 1

        threads = []
        for i in range(5):
            threads.append(threading.Thread(target=write_task, args=(i,)))
            threads.append(threading.Thread(target=read_task))

        for t in threads:
            t.start()

        for t in threads:
            t.join(timeout=15)

        self.assertGreater(results["write_success"], 0)
        self.assertGreater(results["read_success"], 0)


class TestSummaryStatistics(unittest.TestCase):
    """测试汇总统计正确性"""

    def test_summary_counts_calculation(self):
        """测试汇总计数计算"""
        from run_strategies_parallel import RunStatus

        mock_results = [
            {"run_status": RunStatus.SUCCESS_WITH_RETURN.value},
            {"run_status": RunStatus.SUCCESS_WITH_RETURN.value},
            {"run_status": RunStatus.SUCCESS_ZERO_RETURN.value},
            {"run_status": RunStatus.RUN_EXCEPTION.value},
            {"run_status": RunStatus.RUN_EXCEPTION.value},
            {"run_status": RunStatus.TIMEOUT.value},
            {"run_status": RunStatus.SKIPPED_NOT_STRATEGY.value},
        ]

        status_counts = {}
        for r in mock_results:
            rs = r.get("run_status", "unknown")
            status_counts[rs] = status_counts.get(rs, 0) + 1

        success_with_return = status_counts.get(RunStatus.SUCCESS_WITH_RETURN.value, 0)
        success_zero_return = status_counts.get(RunStatus.SUCCESS_ZERO_RETURN.value, 0)
        success_no_trade = status_counts.get(RunStatus.SUCCESS_NO_TRADE.value, 0)
        total_success = success_with_return + success_zero_return + success_no_trade

        run_exception = status_counts.get(RunStatus.RUN_EXCEPTION.value, 0)

        self.assertEqual(success_with_return, 2)
        self.assertEqual(success_zero_return, 1)
        self.assertEqual(total_success, 3)
        self.assertEqual(run_exception, 2)

        self.assertNotEqual(run_exception, 0)
        self.assertNotIn(
            RunStatus.RUN_EXCEPTION.value,
            [
                RunStatus.SUCCESS_WITH_RETURN.value,
                RunStatus.SUCCESS_ZERO_RETURN.value,
                RunStatus.SUCCESS_NO_TRADE.value,
            ],
        )


def run_extended_smoke_test():
    """运行扩展烟雾测试"""
    print("=" * 80)
    print("批量运行器扩展烟雾测试")
    print("=" * 80)

    sample_dir = os.path.join(os.path.dirname(__file__), "sample_strategies")
    scanner = StrategyScanner()

    print("\n[阶段1] 扩展策略扫描测试")
    print("-" * 40)

    extended_files = {
        "06_syntax_error.txt": ("syntax_error", False),
        "07_empty_file.txt": ("empty_file", False),
        "08_multiple_missing_api.txt": ("missing_api", False),
        "09_valid_etf_strategy.txt": ("valid", True),
        "10_handle_data_strategy.txt": ("valid", True),
    }

    all_passed = True
    for filename, (expected_status, expected_exec) in extended_files.items():
        filepath = os.path.join(sample_dir, filename)
        if not os.path.exists(filepath):
            print(f"  ✗ 文件不存在: {filename}")
            all_passed = False
            continue

        result = scanner.scan_file(filepath)
        if (
            result.status.value == expected_status
            and result.is_executable == expected_exec
        ):
            print(
                f"  ✓ {filename}: status={result.status.value}, executable={result.is_executable}"
            )
            if result.missing_apis:
                print(f"    缺失API: {result.missing_apis}")
        else:
            print(
                f"  ✗ {filename}: expected={expected_status}, got={result.status.value}"
            )
            all_passed = False

    print("\n[阶段2] DuckDB 扩展功能测试")
    print("-" * 40)

    temp_dir = tempfile.mkdtemp()
    db_path = os.path.join(temp_dir, "extended_test.db")

    try:
        manager = DuckDBManager(db_path=db_path, read_only=False, use_cache=True)

        # 批量插入测试
        symbols = ["sh600000", "sh600001", "sh600002"]
        dates = pd.date_range("2023-01-01", periods=10, freq="D")
        for symbol in symbols:
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
            manager.insert_stock_daily(symbol, df, adjust="qfq")

        total = manager.count_records("stock_daily")
        if total == 30:
            print("  ✓ 批量插入测试通过: 30条记录")
        else:
            print(f"  ✗ 批量插入测试失败: 预期30条，实际{total}条")
            all_passed = False

        # LRU缓存测试
        cache = LocalCache(max_size=3)
        for i in range(5):
            cache.set(
                "test", f"s{i}", "2023-01-01", "2023-12-31", pd.DataFrame({"a": [i]})
            )

        if cache.get("test", "s0", "2023-01-01", "2023-12-31") is None:
            print("  ✓ LRU缓存淘汰测试通过")
        else:
            print("  ✗ LRU缓存淘汰测试失败")
            all_passed = False

        manager.close()

    except Exception as e:
        print(f"  ✗ DuckDB 扩展测试异常: {e}")
        all_passed = False

    finally:
        shutil.rmtree(temp_dir, ignore_errors=True)

    print("\n[阶段3] RunStatus 分类逻辑测试")
    print("-" * 40)

    from run_strategies_parallel import _classify_run_status, RunStatus

    test_cases = [
        (None, RuntimeError("test"), RunStatus.RUN_EXCEPTION),
        (None, TimeoutError("timeout test"), RunStatus.TIMEOUT),
        (None, RuntimeError("无数据或股票不存在"), RunStatus.DATA_MISSING),
        (None, None, RunStatus.LOAD_FAILED),
    ]

    for backtest, exc, expected in test_cases:
        result = _classify_run_status(backtest, exc, True, None)
        if result == expected:
            print(f"  ✓ 分类测试通过: {expected.value}")
        else:
            print(f"  ✗ 分类测试失败: expected={expected.value}, got={result.value}")
            all_passed = False

    print("\n" + "=" * 80)
    if all_passed:
        print("✅ 扩展烟雾测试全部通过")
    else:
        print("❌ 扩展烟雾测试存在失败项")
    print("=" * 80)

    return all_passed


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="批量运行器扩展测试")
    parser.add_argument("--unit-test", action="store_true", help="运行单元测试")
    parser.add_argument("--smoke", action="store_true", help="运行烟雾测试")
    parser.add_argument("--all", action="store_true", help="运行所有测试")

    args = parser.parse_args()

    if args.all or (not args.unit_test and not args.smoke):
        unittest.main(argv=["first-arg-is-ignored"], exit=False, verbosity=2)
        print("\n")
        run_extended_smoke_test()
    elif args.unit_test:
        unittest.main(argv=["first-arg-is-ignored"], exit=False, verbosity=2)
    elif args.smoke:
        run_extended_smoke_test()
