#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
测试任务10: 批量运行器与并发存储修复

覆盖:
1. strategy_scanner.py - 策略扫描器
2. run_strategies_parallel.py - 运行状态分类
3. duckdb_manager.py - 缓存和并发
"""

import os
import sys
import tempfile
import unittest
from unittest.mock import patch, MagicMock
import pandas as pd
import threading
import time

sys.path.insert(
    0,
    os.path.join(os.path.dirname(__file__), "..", "src"),
)


class TestStrategyScanner(unittest.TestCase):
    """测试策略扫描器"""

    def setUp(self):
        from strategy_scanner import StrategyScanner, StrategyStatus

        self.scanner = StrategyScanner()
        self.StrategyStatus = StrategyStatus

    def test_scan_valid_strategy(self):
        """测试有效策略识别"""
        strategy_code = """
def initialize(context):
    set_option('use_real_price', True)
    run_daily(my_trade, 'open')

def my_trade(context):
    order_value('600519.XSHG', 10000)
"""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".txt", delete=False) as f:
            f.write(strategy_code)
            f.flush()
            result = self.scanner.scan_file(f.name)

            self.assertTrue(result.has_initialize)
            self.assertTrue(result.is_executable)
            self.assertEqual(result.status, self.StrategyStatus.VALID)
            self.assertEqual(len(result.missing_apis), 0)

            os.unlink(f.name)

    def test_scan_valid_strategy_with_handle(self):
        """测试带handle_data的有效策略"""
        strategy_code = """
def initialize(context):
    pass

def handle_data(context, data):
    order('600519.XSHG', 100)
"""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".txt", delete=False) as f:
            f.write(strategy_code)
            f.flush()
            result = self.scanner.scan_file(f.name)

            self.assertTrue(result.has_initialize)
            self.assertTrue(result.has_handle)
            self.assertTrue(result.is_executable)

            os.unlink(f.name)

    def test_scan_no_initialize(self):
        """测试缺少initialize的策略"""
        strategy_code = """
def my_trade(context):
    order_value('600519.XSHG', 10000)
"""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".txt", delete=False) as f:
            f.write(strategy_code)
            f.flush()
            result = self.scanner.scan_file(f.name)

            self.assertFalse(result.has_initialize)
            self.assertEqual(result.status, self.StrategyStatus.NO_INITIALIZE)

            os.unlink(f.name)

    def test_scan_missing_api(self):
        """测试缺失API的策略"""
        strategy_code = """
def initialize(context):
    pass

def handle_data(context, data):
    ticks = get_ticks('600519.XSHG')
"""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".txt", delete=False) as f:
            f.write(strategy_code)
            f.flush()
            result = self.scanner.scan_file(f.name)

            self.assertTrue(result.has_initialize)
            self.assertIn("get_ticks", result.missing_apis)
            self.assertEqual(result.status, self.StrategyStatus.MISSING_API)

            os.unlink(f.name)

    def test_scan_syntax_error(self):
        """测试语法错误的策略"""
        strategy_code = """
def initialize(context):
    log.info('test'
    # 缺少括号
"""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".txt", delete=False) as f:
            f.write(strategy_code)
            f.flush()
            result = self.scanner.scan_file(f.name)

            self.assertEqual(result.status, self.StrategyStatus.SYNTAX_ERROR)
            self.assertIn("语法错误", result.error_message)

            os.unlink(f.name)

    def test_scan_empty_file(self):
        """测试空文件"""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".txt", delete=False) as f:
            f.write("")
            f.flush()
            result = self.scanner.scan_file(f.name)

            self.assertEqual(result.status, self.StrategyStatus.EMPTY_FILE)

            os.unlink(f.name)

    def test_scan_file_not_exist(self):
        """测试文件不存在"""
        result = self.scanner.scan_file("/nonexistent/path/strategy.txt")

        self.assertFalse(result.is_executable)
        self.assertEqual(result.status, self.StrategyStatus.NOT_STRATEGY)

    def test_scan_gbk_encoding(self):
        """测试GBK编码策略"""
        strategy_code = """
def initialize(context):
    log.info('中文测试')
"""
        with tempfile.NamedTemporaryFile(mode="wb", suffix=".txt", delete=False) as f:
            f.write(strategy_code.encode("gbk"))
            f.flush()
            result = self.scanner.scan_file(f.name)

            self.assertTrue(result.has_initialize)

            os.unlink(f.name)

    def test_is_strategy_file(self):
        """测试策略文件判断"""
        self.assertTrue(self.scanner.is_strategy_file("strategy.txt"))
        self.assertTrue(self.scanner.is_strategy_file("my_strategy.py"))
        self.assertFalse(self.scanner.is_strategy_file("README.md"))
        self.assertFalse(self.scanner.is_strategy_file("研究.txt"))
        self.assertFalse(self.scanner.is_strategy_file("notebook.ipynb"))

    def test_scan_directory(self):
        """测试目录扫描"""
        with tempfile.TemporaryDirectory() as tmpdir:
            valid_file = os.path.join(tmpdir, "valid.txt")
            invalid_file = os.path.join(tmpdir, "invalid.txt")

            with open(valid_file, "w") as f:
                f.write("def initialize(c): pass\n")
            with open(invalid_file, "w") as f:
                f.write("# just comment\n")

            results = self.scanner.scan_directory(tmpdir, "*.txt")

            self.assertEqual(len(results["all"]), 2)
            self.assertEqual(len(results["valid"]), 1)

    def test_get_executable_strategies(self):
        """测试获取可执行策略列表"""
        with tempfile.TemporaryDirectory() as tmpdir:
            valid_file = os.path.join(tmpdir, "valid.txt")
            with open(valid_file, "w") as f:
                f.write(
                    'def initialize(c): pass\nrun_daily(trade, "open")\ndef trade(c): pass\n'
                )

            executables = self.scanner.get_executable_strategies(tmpdir, "*.txt")

            self.assertEqual(len(executables), 1)
            self.assertEqual(executables[0], valid_file)

    def test_null_bytes_handling(self):
        """测试null字节处理"""
        strategy_code = "def initialize(c): pass\n\x00def handle(c): pass"
        with tempfile.NamedTemporaryFile(mode="wb", suffix=".txt", delete=False) as f:
            f.write(strategy_code.encode("utf-8"))
            f.flush()

            result = self.scanner.scan_file(f.name)
            self.assertTrue(result.has_initialize)

            os.unlink(f.name)


class TestRunStatusClassification(unittest.TestCase):
    """测试运行状态分类"""

    def test_run_status_enum(self):
        """测试运行状态枚举"""
        from run_strategies_parallel import RunStatus

        self.assertEqual(RunStatus.SUCCESS_WITH_RETURN.value, "success_with_return")
        self.assertEqual(RunStatus.SUCCESS_ZERO_RETURN.value, "success_zero_return")
        self.assertEqual(RunStatus.SUCCESS_NO_TRADE.value, "success_no_trade")
        self.assertEqual(RunStatus.LOAD_FAILED.value, "load_failed")
        self.assertEqual(RunStatus.RUN_EXCEPTION.value, "run_exception")
        self.assertEqual(RunStatus.TIMEOUT.value, "timeout")
        self.assertEqual(RunStatus.DATA_MISSING.value, "data_missing")

    def test_classify_run_status_success_with_return(self):
        """测试成功有收益状态分类"""
        from run_strategies_parallel import _classify_run_status, RunStatus

        backtest_result = {
            "final_value": 1100000,
            "pnl": 100000,
            "pnl_pct": 10.0,
            "strategy": MagicMock(navs={"2022-01-01": 1.0, "2022-01-02": 1.1}),
        }

        status = _classify_run_status(backtest_result, None, True, None)
        self.assertEqual(status, RunStatus.SUCCESS_WITH_RETURN)

    def test_classify_run_status_success_zero_return(self):
        """测试成功零收益状态分类"""
        from run_strategies_parallel import _classify_run_status, RunStatus

        backtest_result = {
            "final_value": 1000000,
            "pnl": 0,
            "pnl_pct": 0.0,
            "strategy": MagicMock(navs={"2022-01-01": 1.0, "2022-01-02": 1.0}),
        }

        status = _classify_run_status(backtest_result, None, True, None)
        self.assertEqual(status, RunStatus.SUCCESS_ZERO_RETURN)

    def test_classify_run_status_success_no_trade(self):
        """测试成功无交易状态分类"""
        from run_strategies_parallel import _classify_run_status, RunStatus

        backtest_result = {
            "final_value": 1000000,
            "pnl": 0,
            "pnl_pct": 0.0,
            "strategy": MagicMock(navs=None),
        }

        status = _classify_run_status(backtest_result, None, True, None)
        self.assertEqual(status, RunStatus.SUCCESS_NO_TRADE)

    def test_classify_run_status_timeout(self):
        """测试超时状态分类"""
        from run_strategies_parallel import _classify_run_status, RunStatus
        from concurrent.futures import TimeoutError as FuturesTimeoutError

        status = _classify_run_status(None, FuturesTimeoutError(), True, None)
        self.assertEqual(status, RunStatus.TIMEOUT)

    def test_classify_run_status_run_exception(self):
        """测试运行异常状态分类"""
        from run_strategies_parallel import _classify_run_status, RunStatus

        status = _classify_run_status(None, ValueError("test error"), True, None)
        self.assertEqual(status, RunStatus.RUN_EXCEPTION)

    def test_classify_run_status_load_failed(self):
        """测试加载失败状态分类"""
        from run_strategies_parallel import _classify_run_status, RunStatus

        status = _classify_run_status(None, None, True, None)
        self.assertEqual(status, RunStatus.LOAD_FAILED)

    def test_classify_run_status_data_missing(self):
        """测试数据缺失状态分类"""
        from run_strategies_parallel import _classify_run_status, RunStatus

        exception = Exception("无数据")
        status = _classify_run_status(None, exception, True, None)
        self.assertEqual(status, RunStatus.DATA_MISSING)


class TestLocalCache(unittest.TestCase):
    """测试本地缓存"""

    def setUp(self):
        from jk2bt.db.duckdb_manager import LocalCache

        self.cache = LocalCache(max_size=3)

    def test_cache_set_and_get(self):
        """测试缓存存取"""
        df = pd.DataFrame({"a": [1, 2, 3]})
        self.cache.set("stock_daily", "600000", "2023-01-01", "2023-12-31", df)

        cached = self.cache.get("stock_daily", "600000", "2023-01-01", "2023-12-31")

        self.assertIsNotNone(cached)
        pd.testing.assert_frame_equal(cached, df)

    def test_cache_miss(self):
        """测试缓存未命中"""
        cached = self.cache.get("stock_daily", "999999", "2023-01-01", "2023-12-31")
        self.assertIsNone(cached)

    def test_cache_with_adjust_param(self):
        """测试带adjust参数的缓存"""
        df = pd.DataFrame({"a": [1, 2, 3]})
        self.cache.set(
            "stock_daily", "600000", "2023-01-01", "2023-12-31", df, adjust="qfq"
        )

        cached_qfq = self.cache.get(
            "stock_daily", "600000", "2023-01-01", "2023-12-31", adjust="qfq"
        )
        cached_hfq = self.cache.get(
            "stock_daily", "600000", "2023-01-01", "2023-12-31", adjust="hfq"
        )

        self.assertIsNotNone(cached_qfq)
        self.assertIsNone(cached_hfq)

    def test_cache_invalidate_symbol(self):
        """测试缓存失效（按symbol）"""
        df = pd.DataFrame({"a": [1, 2, 3]})
        self.cache.set("stock_daily", "600000", "2023-01-01", "2023-12-31", df)
        self.cache.set("stock_daily", "600001", "2023-01-01", "2023-12-31", df)

        self.cache.invalidate(table="stock_daily", symbol="600000")

        self.assertIsNone(
            self.cache.get("stock_daily", "600000", "2023-01-01", "2023-12-31")
        )
        self.assertIsNotNone(
            self.cache.get("stock_daily", "600001", "2023-01-01", "2023-12-31")
        )

    def test_cache_invalidate_table(self):
        """测试缓存失效（按table）"""
        df = pd.DataFrame({"a": [1, 2, 3]})
        self.cache.set("stock_daily", "600000", "2023-01-01", "2023-12-31", df)
        self.cache.set("etf_daily", "510300", "2023-01-01", "2023-12-31", df)

        self.cache.invalidate(table="stock_daily")

        self.assertIsNone(
            self.cache.get("stock_daily", "600000", "2023-01-01", "2023-12-31")
        )
        self.assertIsNotNone(
            self.cache.get("etf_daily", "510300", "2023-01-01", "2023-12-31")
        )

    def test_cache_clear(self):
        """测试缓存清空"""
        df = pd.DataFrame({"a": [1, 2, 3]})
        self.cache.set("stock_daily", "600000", "2023-01-01", "2023-12-31", df)

        self.cache.clear()

        self.assertIsNone(
            self.cache.get("stock_daily", "600000", "2023-01-01", "2023-12-31")
        )

    def test_cache_max_size_eviction(self):
        """测试缓存容量限制"""
        df = pd.DataFrame({"a": [1]})

        self.cache.set("t", "s1", "d1", "d2", df)
        self.cache.set("t", "s2", "d1", "d2", df)
        self.cache.set("t", "s3", "d1", "d2", df)
        self.cache.set("t", "s4", "d1", "d2", df)

        self.assertIsNone(self.cache.get("t", "s1", "d1", "d2"))
        self.assertIsNotNone(self.cache.get("t", "s4", "d1", "d2"))

    def test_cache_thread_safety(self):
        """测试缓存线程安全"""
        df = pd.DataFrame({"a": [1]})
        errors = []

        def writer(i):
            try:
                for j in range(100):
                    self.cache.set("t", f"s{i}_{j}", "d1", "d2", df)
            except Exception as e:
                errors.append(e)

        def reader(i):
            try:
                for j in range(100):
                    self.cache.get("t", f"s{i}_{j}", "d1", "d2")
            except Exception as e:
                errors.append(e)

        threads = []
        for i in range(5):
            threads.append(threading.Thread(target=writer, args=(i,)))
            threads.append(threading.Thread(target=reader, args=(i,)))

        for t in threads:
            t.start()
        for t in threads:
            t.join()

        self.assertEqual(len(errors), 0)


class TestDuckDBManagerConcurrency(unittest.TestCase):
    """测试DuckDB并发优化"""

    def setUp(self):
        self.db_path = tempfile.mktemp(suffix=".db")
        self.teardown_paths = [self.db_path]

    def tearDown(self):
        for path in self.teardown_paths:
            if os.path.exists(path):
                try:
                    os.remove(path)
                except:
                    pass

    def test_read_only_mode(self):
        """测试只读模式"""
        from jk2bt.db.duckdb_manager import DuckDBManager

        writer = DuckDBManager(db_path=self.db_path, read_only=False)
        writer.close()

        reader = DuckDBManager(db_path=self.db_path, read_only=True)
        self.assertTrue(reader.read_only)
        reader.close()

    def test_use_cache_option(self):
        """测试缓存选项"""
        from jk2bt.db.duckdb_manager import DuckDBManager

        manager_with_cache = DuckDBManager(db_path=self.db_path, use_cache=True)
        self.assertTrue(manager_with_cache.use_cache)
        manager_with_cache.close()

        manager_no_cache = DuckDBManager(db_path=self.db_path, use_cache=False)
        self.assertFalse(manager_no_cache.use_cache)
        manager_no_cache.close()

    def test_independent_connections(self):
        """测试独立连接"""
        from jk2bt.db.duckdb_manager import DuckDBManager

        manager = DuckDBManager(db_path=self.db_path, read_only=False)

        with manager._get_connection(read_only=True) as conn1:
            with manager._get_connection(read_only=True) as conn2:
                self.assertIsNot(conn1, conn2)

        manager.close()

    def test_get_shared_read_only_manager(self):
        """测试工厂函数"""
        from jk2bt.db.duckdb_manager import get_shared_read_only_manager

        reader = get_shared_read_only_manager(db_path=self.db_path)
        self.assertTrue(reader.read_only)
        reader.close()

    def test_get_writer_manager(self):
        """测试写入管理器工厂函数"""
        from jk2bt.db.duckdb_manager import get_writer_manager

        writer = get_writer_manager(db_path=self.db_path)
        self.assertFalse(writer.read_only)
        writer.close()

    def test_clear_cache_method(self):
        """测试清除缓存方法"""
        from jk2bt.db.duckdb_manager import DuckDBManager

        manager = DuckDBManager(db_path=self.db_path, use_cache=True)
        manager.clear_cache()
        manager.close()

    def test_insert_with_retry(self):
        """测试写入重试"""
        from jk2bt.db.duckdb_manager import DuckDBManager

        manager = DuckDBManager(db_path=self.db_path, read_only=False)

        df = pd.DataFrame(
            {
                "datetime": pd.date_range("2023-01-01", periods=3),
                "open": [10.0, 11.0, 12.0],
                "high": [10.5, 11.5, 12.5],
                "low": [9.5, 10.5, 11.5],
                "close": [10.2, 11.2, 12.2],
                "volume": [1000, 1100, 1200],
            }
        )

        manager.insert_stock_daily("sh600000", df, adjust="qfq")

        result = manager.get_stock_daily("sh600000", "2023-01-01", "2023-01-03")
        self.assertEqual(len(result), 3)

        manager.close()


class TestQuickScanFunction(unittest.TestCase):
    """测试快速扫描函数"""

    def test_quick_scan_valid(self):
        """测试快速扫描有效策略"""
        from strategy_scanner import quick_scan_strategy

        with tempfile.NamedTemporaryFile(mode="w", suffix=".txt", delete=False) as f:
            f.write(
                'def initialize(c): pass\nrun_daily(trade, "open")\ndef trade(c): pass\n'
            )
            f.flush()

            is_executable, message = quick_scan_strategy(f.name)
            self.assertTrue(is_executable)
            self.assertEqual(message, "OK")

            os.unlink(f.name)

    def test_quick_scan_invalid(self):
        """测试快速扫描无效策略"""
        from strategy_scanner import quick_scan_strategy

        with tempfile.NamedTemporaryFile(mode="w", suffix=".txt", delete=False) as f:
            f.write("# just a comment\n")
            f.flush()

            is_executable, message = quick_scan_strategy(f.name)
            self.assertFalse(is_executable)

            os.unlink(f.name)


class TestBatchScanStrategies(unittest.TestCase):
    """测试批量扫描函数"""

    def test_batch_scan(self):
        """测试批量扫描"""
        from strategy_scanner import batch_scan_strategies

        with tempfile.TemporaryDirectory() as tmpdir:
            valid = os.path.join(tmpdir, "valid.txt")
            invalid = os.path.join(tmpdir, "invalid.txt")

            with open(valid, "w") as f:
                f.write(
                    'def initialize(c): pass\nrun_daily(trade, "open")\ndef trade(c): pass\n'
                )
            with open(invalid, "w") as f:
                f.write("# comment\n")

            results = batch_scan_strategies(tmpdir, "*.txt")

            self.assertIn(valid, results["executable"])
            self.assertIn(invalid, results["invalid"])


class TestScanResult(unittest.TestCase):
    """测试扫描结果数据类"""

    def test_scan_result_dataclass(self):
        """测试扫描结果数据类"""
        from strategy_scanner import ScanResult, StrategyStatus

        result = ScanResult(
            file_path="/path/to/strategy.txt",
            file_name="strategy.txt",
            status=StrategyStatus.VALID,
            has_initialize=True,
            has_handle=True,
            missing_apis=[],
            error_message="",
            is_executable=True,
            details={"defined_funcs": ["initialize"]},
        )

        self.assertEqual(result.file_name, "strategy.txt")
        self.assertTrue(result.is_executable)


if __name__ == "__main__":
    unittest.main(verbosity=2)
