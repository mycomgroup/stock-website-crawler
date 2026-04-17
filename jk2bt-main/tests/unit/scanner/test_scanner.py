"""
Tests for jk2bt/scanner/scanner.py - StrategyScanner
"""

import pytest
import tempfile
import os
from datetime import date, time
from jk2bt.scanner.scanner import (
    StrategyScanner,
    StrategyStatus,
    ScanResult,
    quick_scan_strategy,
    batch_scan_strategies,
)


class TestStrategyScanner:
    """Test StrategyScanner class"""

    def setup_method(self):
        self.scanner = StrategyScanner()
        self.temp_dir = tempfile.mkdtemp()

    def teardown_method(self):
        import shutil

        if os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir)

    def test_is_strategy_file_py(self):
        assert self.scanner.is_strategy_file("strategy.py") is True
        assert self.scanner.is_strategy_file("my_strategy.txt") is True

    def test_is_strategy_file_not_strategy(self):
        assert self.scanner.is_strategy_file("README.md") is False
        assert self.scanner.is_strategy_file("test_strategy.py") is False
        assert self.scanner.is_strategy_file("strategy.ipynb") is False
        assert self.scanner.is_strategy_file("strategy_result.csv") is False

    def test_scan_file_not_exists(self):
        result = self.scanner.scan_file("/nonexistent/path.py")
        assert result.status == StrategyStatus.NOT_STRATEGY
        assert result.is_executable is False
        assert "不存在" in result.error_message

    def test_scan_file_empty_file(self):
        filepath = os.path.join(self.temp_dir, "empty.txt")
        with open(filepath, "w") as f:
            f.write("   ")

        result = self.scanner.scan_file(filepath)
        assert result.status == StrategyStatus.EMPTY_FILE

    def test_scan_file_valid_strategy(self):
        filepath = os.path.join(self.temp_dir, "valid_strategy.py")
        with open(filepath, "w") as f:
            f.write("""
def initialize(context):
    pass

def handle_data(context, data):
    pass
""")

        result = self.scanner.scan_file(filepath)
        assert result.has_initialize is True
        assert result.has_handle is True
        assert result.status == StrategyStatus.VALID
        assert result.is_executable is True

    def test_scan_file_no_initialize(self):
        filepath = os.path.join(self.temp_dir, "no_init.py")
        with open(filepath, "w") as f:
            f.write("""
def handle_data(context, data):
    pass
""")

        result = self.scanner.scan_file(filepath)
        assert result.has_initialize is False
        assert result.status == StrategyStatus.NO_INITIALIZE
        assert result.is_executable is False

    def test_scan_file_syntax_error(self):
        filepath = os.path.join(self.temp_dir, "syntax_error.py")
        with open(filepath, "w") as f:
            f.write(
                "def initialize(context):\n    pass\n\ndef handle_data(context):\n    if"
            )

        result = self.scanner.scan_file(filepath)
        assert result.status == StrategyStatus.SYNTAX_ERROR
        assert result.is_executable is False

    def test_scan_file_with_run_daily(self):
        filepath = os.path.join(self.temp_dir, "run_daily_strategy.py")
        with open(filepath, "w") as f:
            f.write("""
def initialize(context):
    run_daily(timer_func, "09:30")

def timer_func(context):
    pass
""")

        result = self.scanner.scan_file(filepath)
        assert result.has_initialize is True
        assert result.is_executable is True

    def test_scan_directory(self):
        for i in range(3):
            filepath = os.path.join(self.temp_dir, f"strategy_{i}.py")
            with open(filepath, "w") as f:
                f.write(f"""
def initialize(context):
    pass

def handle_data(context, data):
    pass
""")

        results = self.scanner.scan_directory(self.temp_dir, "*.py")
        assert len(results["all"]) == 3
        assert len(results["valid"]) == 3

    def test_get_executable_strategies(self):
        valid_file = os.path.join(self.temp_dir, "valid.py")
        with open(valid_file, "w") as f:
            f.write("""
def initialize(context):
    pass
def handle_data(context, data):
    pass
""")

        invalid_file = os.path.join(self.temp_dir, "invalid.py")
        with open(invalid_file, "w") as f:
            f.write("# No strategy functions")

        executables = self.scanner.get_executable_strategies(self.temp_dir, "*.py")
        assert valid_file in executables
        assert invalid_file not in executables

    def test_scan_result_to_dict(self):
        result = ScanResult(
            file_path="/path/to/file.py",
            file_name="file.py",
            status=StrategyStatus.VALID,
            has_initialize=True,
            has_handle=True,
            missing_apis=[],
            error_message="",
            is_executable=True,
            details={"code_lines": 10},
        )
        d = result.to_dict()
        assert d["status"] == "valid"
        assert d["is_executable"] is True
        assert d["details"]["code_lines"] == 10


class TestQuickScan:
    """Test quick_scan_strategy function"""

    def setup_method(self):
        self.temp_dir = tempfile.mkdtemp()

    def teardown_method(self):
        import shutil

        if os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir)

    def test_quick_scan_valid(self):
        filepath = os.path.join(self.temp_dir, "test.py")
        with open(filepath, "w") as f:
            f.write("""
def initialize(context):
    pass
def handle_data(context, data):
    pass
""")
        is_valid, msg = quick_scan_strategy(filepath)
        assert is_valid is True

    def test_quick_scan_invalid(self):
        filepath = os.path.join(self.temp_dir, "test.py")
        with open(filepath, "w") as f:
            f.write("# Empty file")
        is_valid, msg = quick_scan_strategy(filepath)
        assert is_valid is False


class TestBatchScan:
    """Test batch_scan_strategies function"""

    def setup_method(self):
        self.temp_dir = tempfile.mkdtemp()

    def teardown_method(self):
        import shutil

        if os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir)

    def test_batch_scan_results(self):
        filepath = os.path.join(self.temp_dir, "valid.py")
        with open(filepath, "w") as f:
            f.write("""
def initialize(context):
    pass
def handle_data(context, data):
    pass
""")
        results = batch_scan_strategies(self.temp_dir, "*.py")
        assert "executable" in results
        assert "invalid" in results
        assert len(results["executable"]) == 1


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
