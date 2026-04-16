"""
策略扫描器单元测试

测试 jk2bt/strategy/scanner.py 中的 StrategyScanner 类及辅助函数。
覆盖：文件判断、单文件扫描、目录扫描、边界条件、缓存行为等。
"""

import os
import tempfile
import pytest

from jk2bt.strategy.scanner import (
    StrategyScanner,
    StrategyStatus,
    ScanResult,
    quick_scan_strategy,
    batch_scan_strategies,
)


class TestStrategyStatus:
    """测试 StrategyStatus 枚举。"""

    def test_all_statuses_exist(self):
        assert StrategyStatus.VALID.value == "valid"
        assert StrategyStatus.NO_INITIALIZE.value == "no_initialize"
        assert StrategyStatus.MISSING_API.value == "missing_api"
        assert StrategyStatus.NOT_STRATEGY.value == "not_strategy"
        assert StrategyStatus.SYNTAX_ERROR.value == "syntax_error"
        assert StrategyStatus.EMPTY_FILE.value == "empty_file"


class TestScanResult:
    """测试 ScanResult 数据类。"""

    def test_to_dict(self):
        result = ScanResult(
            file_path="/tmp/test.txt",
            file_name="test.txt",
            status=StrategyStatus.VALID,
            has_initialize=True,
            has_handle=True,
            missing_apis=[],
            error_message="",
            is_executable=True,
            details={"defined_funcs": ["initialize", "handle_data"]},
        )
        d = result.to_dict()
        assert d["file_path"] == "/tmp/test.txt"
        assert d["status"] == "valid"
        assert d["has_initialize"] is True
        assert d["is_executable"] is True
        assert d["details"]["defined_funcs"] == ["initialize", "handle_data"]

    def test_to_dict_with_missing_apis(self):
        result = ScanResult(
            file_path="/tmp/test.txt",
            file_name="test.txt",
            status=StrategyStatus.MISSING_API,
            has_initialize=True,
            has_handle=False,
            missing_apis=["get_dividends", "get_splits"],
            error_message="missing_api",
            is_executable=False,
            details={},
        )
        d = result.to_dict()
        assert d["status"] == "missing_api"
        assert d["missing_apis"] == ["get_dividends", "get_splits"]
        assert d["is_executable"] is False


class TestIsStrategyFile:
    """测试 is_strategy_file 方法。"""

    def setup_method(self):
        self.scanner = StrategyScanner()

    def test_py_file_is_strategy(self):
        assert self.scanner.is_strategy_file("/path/to/strategy.py") is True

    def test_txt_file_is_strategy(self):
        assert self.scanner.is_strategy_file("/path/to/strategy.txt") is True

    def test_ipynb_not_strategy(self):
        assert self.scanner.is_strategy_file("/path/to/research.ipynb") is False

    def test_md_not_strategy(self):
        assert self.scanner.is_strategy_file("/path/to/notes.md") is False

    def test_csv_not_strategy(self):
        assert self.scanner.is_strategy_file("/path/to/data.csv") is False

    def test_json_not_strategy(self):
        assert self.scanner.is_strategy_file("/path/to/config.json") is False

    def test_xlsx_not_strategy(self):
        assert self.scanner.is_strategy_file("/path/to/report.xlsx") is False

    def test_log_not_strategy(self):
        assert self.scanner.is_strategy_file("/path/to/app.log") is False

    def test_readme_not_strategy(self):
        assert self.scanner.is_strategy_file("/path/to/README.txt") is False

    def test_test_file_not_strategy(self):
        assert self.scanner.is_strategy_file("/path/to/test_something.py") is False

    def test_tests_file_not_strategy(self):
        assert self.scanner.is_strategy_file("/path/to/tests.py") is False

    def test_underscore_test_not_strategy(self):
        assert self.scanner.is_strategy_file("/path/to/module_test.py") is False

    def test_chinese_research_not_strategy(self):
        assert self.scanner.is_strategy_file("/path/研究笔记.txt") is False

    def test_chinese_notes_not_strategy(self):
        assert self.scanner.is_strategy_file("/path/说明文档.txt") is False

    def test_backup_not_strategy(self):
        assert self.scanner.is_strategy_file("/path/strategy.bak") is False

    def test_old_not_strategy(self):
        assert self.scanner.is_strategy_file("/path/strategy.old") is False

    def test_output_not_strategy(self):
        assert self.scanner.is_strategy_file("/path/output.txt") is False

    def test_result_not_strategy(self):
        assert self.scanner.is_strategy_file("/path/result.txt") is False

    def test_field_map_not_strategy(self):
        assert self.scanner.is_strategy_file("/path/field_map.py") is False

    def test_non_strategy_pattern_not_strategy(self):
        assert self.scanner.is_strategy_file("/path/配套资料.txt") is False

    def test_non_python_ext_not_strategy(self):
        assert self.scanner.is_strategy_file("/path/strategy.java") is False

    def test_case_insensitive_test(self):
        assert self.scanner.is_strategy_file("/path/TEST_file.py") is False


class TestScanFile:
    """测试 scan_file 方法。"""

    def setup_method(self):
        self.scanner = StrategyScanner()

    def _write_temp_file(self, content: str, suffix: str = ".txt") -> str:
        f = tempfile.NamedTemporaryFile(
            mode="w", suffix=suffix, delete=False, encoding="utf-8"
        )
        f.write(content)
        f.flush()
        f.close()
        return f.name

    def test_valid_strategy(self):
        code = """
def initialize(context):
    pass

def handle_data(context, data):
    price = get_price('000001.XSHE', start_date='2020-01-01')
    order('000001.XSHE', 100)
"""
        path = self._write_temp_file(code)
        try:
            result = self.scanner.scan_file(path)
            assert result.status == StrategyStatus.VALID
            assert result.has_initialize is True
            assert result.has_handle is True
            assert result.is_executable is True
            assert result.missing_apis == []
            assert result.error_message == ""
            assert "initialize" in result.details["defined_funcs"]
            assert "handle_data" in result.details["defined_funcs"]
        finally:
            os.unlink(path)

    def test_no_initialize(self):
        code = """
def handle_data(context, data):
    pass
"""
        path = self._write_temp_file(code)
        try:
            result = self.scanner.scan_file(path)
            assert result.status == StrategyStatus.NO_INITIALIZE
            assert result.has_initialize is False
            assert result.has_handle is True
            assert result.is_executable is False
        finally:
            os.unlink(path)

    def test_no_handle_function(self):
        code = """
def initialize(context):
    pass
"""
        path = self._write_temp_file(code)
        try:
            result = self.scanner.scan_file(path)
            assert result.status == StrategyStatus.VALID
            assert result.has_initialize is True
            assert result.has_handle is False
            assert result.is_executable is False
        finally:
            os.unlink(path)

    def test_with_run_daily_is_executable(self):
        code = """
def initialize(context):
    run_daily(context, my_func)

def my_func(context, data):
    pass
"""
        path = self._write_temp_file(code)
        try:
            result = self.scanner.scan_file(path)
            assert result.is_executable is True
        finally:
            os.unlink(path)

    def test_with_run_weekly_is_executable(self):
        code = """
def initialize(context):
    run_weekly(context, my_func)

def my_func(context, data):
    pass
"""
        path = self._write_temp_file(code)
        try:
            result = self.scanner.scan_file(path)
            assert result.is_executable is True
        finally:
            os.unlink(path)

    def test_with_run_monthly_is_executable(self):
        code = """
def initialize(context):
    run_monthly(context, my_func)

def my_func(context, data):
    pass
"""
        path = self._write_temp_file(code)
        try:
            result = self.scanner.scan_file(path)
            assert result.is_executable is True
        finally:
            os.unlink(path)

    def test_missing_api(self):
        code = """
def initialize(context):
    pass

def handle_data(context, data):
    divs = get_dividends('000001.XSHE')
    splits = get_splits('000001.XSHE')
"""
        path = self._write_temp_file(code)
        try:
            result = self.scanner.scan_file(path)
            assert result.status == StrategyStatus.MISSING_API
            assert "get_dividends" in result.missing_apis
            assert "get_splits" in result.missing_apis
            assert result.is_executable is False
        finally:
            os.unlink(path)

    def test_mapped_api_not_missing(self):
        """测试名称映射的 API 不应被视为缺失。"""
        code = """
def initialize(context):
    pass

def handle_data(context, data):
    ticks = get_ticks('000001.XSHE')
    future = get_future_contracts('IF')
"""
        path = self._write_temp_file(code)
        try:
            result = self.scanner.scan_file(path)
            assert "get_ticks" not in result.missing_apis
            assert "get_future_contracts" not in result.missing_apis
        finally:
            os.unlink(path)

    def test_syntax_error(self):
        code = """
def initialize(context):
    pass

def handle_data(context, data):
    if True
        print("missing colon")
"""
        path = self._write_temp_file(code)
        try:
            result = self.scanner.scan_file(path)
            assert result.status == StrategyStatus.SYNTAX_ERROR
            assert result.is_executable is False
            assert "语法错误" in result.error_message
            assert "syntax_error" in result.details
        finally:
            os.unlink(path)

    def test_empty_file(self):
        path = self._write_temp_file("")
        try:
            result = self.scanner.scan_file(path)
            assert result.status == StrategyStatus.EMPTY_FILE
            assert result.is_executable is False
            assert result.error_message == "空文件"
        finally:
            os.unlink(path)

    def test_whitespace_only_file(self):
        path = self._write_temp_file("   \n\n  \t  \n")
        try:
            result = self.scanner.scan_file(path)
            assert result.status == StrategyStatus.EMPTY_FILE
            assert result.is_executable is False
        finally:
            os.unlink(path)

    def test_file_not_exists(self):
        result = self.scanner.scan_file("/nonexistent/path/strategy.txt")
        assert result.status == StrategyStatus.NOT_STRATEGY
        assert result.is_executable is False
        assert result.error_message == "文件不存在"

    def test_non_strategy_file_excluded(self):
        path = self._write_temp_file("some content", suffix=".md")
        try:
            result = self.scanner.scan_file(path)
            assert result.status == StrategyStatus.NOT_STRATEGY
            assert result.is_executable is False
            assert "非策略文件" in result.error_message
        finally:
            os.unlink(path)

    def test_no_function_definitions(self):
        code = """
# just a comment file
x = 1
y = 2
"""
        path = self._write_temp_file(code)
        try:
            result = self.scanner.scan_file(path)
            assert result.status == StrategyStatus.NOT_STRATEGY
            assert result.is_executable is False
            assert result.error_message == "无策略函数定义"
        finally:
            os.unlink(path)

    def test_before_trading_start_detected(self):
        code = """
def initialize(context):
    pass

def before_trading_start(context, data):
    pass
"""
        path = self._write_temp_file(code)
        try:
            result = self.scanner.scan_file(path)
            assert result.has_handle is True
        finally:
            os.unlink(path)

    def test_after_trading_end_detected(self):
        code = """
def initialize(context):
    pass

def after_trading_end(context, data):
    pass
"""
        path = self._write_temp_file(code)
        try:
            result = self.scanner.scan_file(path)
            assert result.has_handle is True
        finally:
            os.unlink(path)

    def test_code_lines_counted(self):
        code = """
def initialize(context):
    pass

def handle_data(context, data):
    pass
"""
        path = self._write_temp_file(code)
        try:
            result = self.scanner.scan_file(path)
            assert result.details["code_lines"] > 0
        finally:
            os.unlink(path)

    def test_called_funcs_collected(self):
        code = """
def initialize(context):
    pass

def handle_data(context, data):
    p = get_price('000001.XSHE')
    order('000001.XSHE', 100)
"""
        path = self._write_temp_file(code)
        try:
            result = self.scanner.scan_file(path)
            called = result.details["called_funcs"]
            assert "get_price" in called
            assert "order" in called
        finally:
            os.unlink(path)

    def test_imported_names_collected(self):
        code = """
import pandas as pd
from numpy import array

def initialize(context):
    pass

def handle_data(context, data):
    pass
"""
        path = self._write_temp_file(code)
        try:
            result = self.scanner.scan_file(path)
            imported = result.details["imported_names"]
            assert "pandas" in imported
            assert "numpy" in imported
            assert "array" in imported
        finally:
            os.unlink(path)

    def test_cache_hit(self):
        code = """
def initialize(context):
    pass

def handle_data(context, data):
    pass
"""
        path = self._write_temp_file(code)
        try:
            result1 = self.scanner.scan_file(path)
            result2 = self.scanner.scan_file(path)
            assert result1 is result2
            assert path in self.scanner._cache
        finally:
            os.unlink(path)

    def test_py_extension_strategy(self):
        code = """
def initialize(context):
    pass

def handle_data(context, data):
    pass
"""
        path = self._write_temp_file(code, suffix=".py")
        try:
            result = self.scanner.scan_file(path)
            assert result.status == StrategyStatus.VALID
            assert result.is_executable is True
        finally:
            os.unlink(path)

    def test_known_api_not_flagged_missing(self):
        """使用已知 API 不应标记为缺失。"""
        code = """
def initialize(context):
    set_benchmark('000300.XSHG')

def handle_data(context, data):
    df = get_price('000001.XSHE')
    order('000001.XSHE', 100)
    log.info("test")
"""
        path = self._write_temp_file(code)
        try:
            result = self.scanner.scan_file(path)
            assert result.missing_apis == []
            assert result.status == StrategyStatus.VALID
        finally:
            os.unlink(path)

    def test_multiple_unimplemented_apis(self):
        code = """
def initialize(context):
    pass

def handle_data(context, data):
    a = get_dividends('000001')
    b = get_splits('000001')
    c = get_shareholder_info('000001')
    d = get_margin_info('000001')
"""
        path = self._write_temp_file(code)
        try:
            result = self.scanner.scan_file(path)
            assert len(result.missing_apis) == 4
            assert result.status == StrategyStatus.MISSING_API
        finally:
            os.unlink(path)

    def test_handle_data_prefix_detected(self):
        code = """
def initialize(context):
    pass

def handle_custom(context, data):
    pass
"""
        path = self._write_temp_file(code)
        try:
            result = self.scanner.scan_file(path)
            assert result.has_handle is True
        finally:
            os.unlink(path)

    def test_trading_prefix_detected(self):
        code = """
def initialize(context):
    pass

def trading_logic(context, data):
    pass
"""
        path = self._write_temp_file(code)
        try:
            result = self.scanner.scan_file(path)
            assert result.has_handle is True
        finally:
            os.unlink(path)


class TestScanDirectory:
    """测试 scan_directory 方法。"""

    def setup_method(self):
        self.scanner = StrategyScanner()

    def _create_temp_dir_with_files(self, files: dict) -> str:
        tmpdir = tempfile.mkdtemp()
        for name, content in files.items():
            path = os.path.join(tmpdir, name)
            with open(path, "w", encoding="utf-8") as f:
                f.write(content)
        return tmpdir

    def test_scan_directory_mixed_files(self):
        files = {
            "strategy1.txt": "def initialize(c): pass\ndef handle_data(c, d): pass",
            "strategy2.txt": "def initialize(c): pass\ndef handle_data(c, d): get_dividends('x')",
            "notes.md": "# research notes",
            "bad.txt": "def initialize(c): pass\nif True\n  pass",
            "empty.txt": "",
        }
        tmpdir = self._create_temp_dir_with_files(files)
        try:
            results = self.scanner.scan_directory(tmpdir, "*.txt")
            assert "valid" in results
            assert "no_initialize" in results
            assert "missing_api" in results
            assert "not_strategy" in results
            assert "syntax_error" in results
            assert "empty_file" in results
            assert "all" in results
            assert len(results["all"]) == 4
            assert len(results["valid"]) >= 1
            assert len(results["missing_api"]) >= 1
            assert len(results["syntax_error"]) >= 1
            assert len(results["empty_file"]) >= 1
        finally:
            for name in files:
                os.unlink(os.path.join(tmpdir, name))
            os.rmdir(tmpdir)

    def test_scan_directory_empty(self):
        tmpdir = tempfile.mkdtemp()
        try:
            results = self.scanner.scan_directory(tmpdir, "*.txt")
            assert len(results["all"]) == 0
        finally:
            os.rmdir(tmpdir)

    def test_scan_directory_all_valid(self):
        files = {
            "s1.txt": "def initialize(c): pass\ndef handle_data(c, d): pass",
            "s2.txt": "def initialize(c): pass\ndef handle_data(c, d): pass",
        }
        tmpdir = self._create_temp_dir_with_files(files)
        try:
            results = self.scanner.scan_directory(tmpdir, "*.txt")
            assert len(results["all"]) == 2
            assert len(results["valid"]) == 2
            assert all(r.is_executable for r in results["valid"])
        finally:
            for name in files:
                os.unlink(os.path.join(tmpdir, name))
            os.rmdir(tmpdir)

    def test_scan_directory_custom_pattern(self):
        files = {
            "s1.py": "def initialize(c): pass\ndef handle_data(c, d): pass",
            "s2.txt": "def initialize(c): pass\ndef handle_data(c, d): pass",
        }
        tmpdir = self._create_temp_dir_with_files(files)
        try:
            results = self.scanner.scan_directory(tmpdir, "*.py")
            assert len(results["all"]) == 1
            assert results["all"][0].file_name == "s1.py"
        finally:
            for name in files:
                os.unlink(os.path.join(tmpdir, name))
            os.rmdir(tmpdir)


class TestGetExecutableStrategies:
    """测试 get_executable_strategies 方法。"""

    def setup_method(self):
        self.scanner = StrategyScanner()

    def _create_temp_dir_with_files(self, files: dict) -> str:
        tmpdir = tempfile.mkdtemp()
        for name, content in files.items():
            path = os.path.join(tmpdir, name)
            with open(path, "w", encoding="utf-8") as f:
                f.write(content)
        return tmpdir

    def test_returns_only_executable(self):
        files = {
            "good.txt": "def initialize(c): pass\ndef handle_data(c, d): pass",
            "bad.txt": "def handle_data(c, d): pass",
            "missing.txt": "def initialize(c): pass\ndef handle_data(c, d): get_dividends('x')",
        }
        tmpdir = self._create_temp_dir_with_files(files)
        try:
            executable = self.scanner.get_executable_strategies(tmpdir, "*.txt")
            assert len(executable) == 1
            assert "good.txt" in executable[0]
        finally:
            for name in files:
                os.unlink(os.path.join(tmpdir, name))
            os.rmdir(tmpdir)

    def test_returns_empty_list_when_none(self):
        files = {
            "bad.txt": "def handle_data(c, d): pass",
        }
        tmpdir = self._create_temp_dir_with_files(files)
        try:
            executable = self.scanner.get_executable_strategies(tmpdir, "*.txt")
            assert executable == []
        finally:
            for name in files:
                os.unlink(os.path.join(tmpdir, name))
            os.rmdir(tmpdir)


class TestQuickScanStrategy:
    """测试 quick_scan_strategy 函数。"""

    def _write_temp_file(self, content: str, suffix: str = ".txt") -> str:
        f = tempfile.NamedTemporaryFile(
            mode="w", suffix=suffix, delete=False, encoding="utf-8"
        )
        f.write(content)
        f.flush()
        f.close()
        return f.name

    def test_valid_strategy(self):
        code = "def initialize(c): pass\ndef handle_data(c, d): pass"
        path = self._write_temp_file(code)
        try:
            executable, msg = quick_scan_strategy(path)
            assert executable is True
            assert msg == "OK"
        finally:
            os.unlink(path)

    def test_invalid_strategy(self):
        code = "def handle_data(c, d): pass"
        path = self._write_temp_file(code)
        try:
            executable, msg = quick_scan_strategy(path)
            assert executable is False
            assert msg != "OK"
        finally:
            os.unlink(path)

    def test_nonexistent_file(self):
        executable, msg = quick_scan_strategy("/nonexistent/file.txt")
        assert executable is False
        assert msg != "OK"


class TestBatchScanStrategies:
    """测试 batch_scan_strategies 函数。"""

    def _create_temp_dir_with_files(self, files: dict) -> str:
        tmpdir = tempfile.mkdtemp()
        for name, content in files.items():
            path = os.path.join(tmpdir, name)
            with open(path, "w", encoding="utf-8") as f:
                f.write(content)
        return tmpdir

    def test_batch_scan_returns_categories(self):
        files = {
            "good.txt": "def initialize(c): pass\ndef handle_data(c, d): pass",
            "bad.txt": "def handle_data(c, d): pass",
        }
        tmpdir = self._create_temp_dir_with_files(files)
        try:
            result = batch_scan_strategies(tmpdir, "*.txt")
            assert "executable" in result
            assert "invalid" in result
            assert "not_strategy" in result
            assert "syntax_error" in result
            assert len(result["executable"]) == 1
            assert len(result["invalid"]) == 1
        finally:
            for name in files:
                os.unlink(os.path.join(tmpdir, name))
            os.rmdir(tmpdir)

    def test_batch_scan_empty_dir(self):
        tmpdir = tempfile.mkdtemp()
        try:
            result = batch_scan_strategies(tmpdir, "*.txt")
            assert result["executable"] == []
            assert result["invalid"] == []
        finally:
            os.rmdir(tmpdir)


class TestPrintSummary:
    """测试 print_summary 方法（确保不抛异常）。"""

    def test_print_summary_no_error(self, caplog):
        import logging

        scanner = StrategyScanner()
        results = {
            "valid": [
                ScanResult(
                    file_path="/tmp/s1.txt",
                    file_name="s1.txt",
                    status=StrategyStatus.VALID,
                    has_initialize=True,
                    has_handle=True,
                    missing_apis=[],
                    error_message="",
                    is_executable=True,
                    details={"defined_funcs": ["initialize", "handle_data"]},
                )
            ],
            "no_initialize": [],
            "missing_api": [],
            "not_strategy": [],
            "syntax_error": [],
            "empty_file": [],
            "all": [
                ScanResult(
                    file_path="/tmp/s1.txt",
                    file_name="s1.txt",
                    status=StrategyStatus.VALID,
                    has_initialize=True,
                    has_handle=True,
                    missing_apis=[],
                    error_message="",
                    is_executable=True,
                    details={"defined_funcs": ["initialize", "handle_data"]},
                )
            ],
        }
        with caplog.at_level(logging.INFO):
            scanner.print_summary(results)
        assert "策略扫描结果摘要" in caplog.text
        assert "总文件数: 1" in caplog.text
        assert "可执行策略: 1" in caplog.text


class TestEdgeCases:
    """测试边界情况。"""

    def setup_method(self):
        self.scanner = StrategyScanner()

    def _write_temp_file(self, content: str, suffix: str = ".txt") -> str:
        f = tempfile.NamedTemporaryFile(
            mode="w", suffix=suffix, delete=False, encoding="utf-8"
        )
        f.write(content)
        f.flush()
        f.close()
        return f.name

    def test_strategy_with_only_comments(self):
        code = """
# This is a strategy
# Just comments, no functions
"""
        path = self._write_temp_file(code)
        try:
            result = self.scanner.scan_file(path)
            assert result.status == StrategyStatus.NOT_STRATEGY
            assert result.is_executable is False
        finally:
            os.unlink(path)

    def test_strategy_with_chinese_comments(self):
        code = """
# 这是一个策略文件
# 只有注释

def initialize(context):
    # 初始化
    pass

def handle_data(context, data):
    # 处理数据
    pass
"""
        path = self._write_temp_file(code)
        try:
            result = self.scanner.scan_file(path)
            assert result.status == StrategyStatus.VALID
            assert result.is_executable is True
        finally:
            os.unlink(path)

    def test_strategy_with_null_bytes(self):
        f = tempfile.NamedTemporaryFile(mode="wb", suffix=".txt", delete=False)
        f.write(b"def initialize(c): pass\x00\ndef handle_data(c, d): pass\x00")
        f.flush()
        f.close()
        path = f.name
        try:
            result = self.scanner.scan_file(path)
            assert result.status == StrategyStatus.VALID
            assert result.is_executable is True
        finally:
            os.unlink(path)

    def test_strategy_with_attribute_api_call(self):
        code = """
def initialize(context):
    pass

def handle_data(context, data):
    df = attribute_history('000001.XSHE', 10, '1d', ['close'])
"""
        path = self._write_temp_file(code)
        try:
            result = self.scanner.scan_file(path)
            assert result.missing_apis == []
            assert result.status == StrategyStatus.VALID
        finally:
            os.unlink(path)

    def test_strategy_with_finance_query(self):
        code = """
def initialize(context):
    pass

def handle_data(context, data):
    q = query(valuation.code).filter(valuation.market_cap > 100)
"""
        path = self._write_temp_file(code)
        try:
            result = self.scanner.scan_file(path)
            assert result.missing_apis == []
        finally:
            os.unlink(path)

    def test_scanner_cache_isolation(self):
        code = "def initialize(c): pass\ndef handle_data(c, d): pass"
        path = self._write_temp_file(code)
        try:
            scanner1 = StrategyScanner()
            scanner2 = StrategyScanner()
            r1 = scanner1.scan_file(path)
            r2 = scanner2.scan_file(path)
            assert r1 is not r2
            assert path in scanner1._cache
            assert path in scanner2._cache
        finally:
            os.unlink(path)

    def test_scan_multiple_times_same_file(self):
        code = "def initialize(c): pass\ndef handle_data(c, d): pass"
        path = self._write_temp_file(code)
        try:
            r1 = self.scanner.scan_file(path)
            r2 = self.scanner.scan_file(path)
            r3 = self.scanner.scan_file(path)
            assert r1 is r2 is r3
        finally:
            os.unlink(path)
