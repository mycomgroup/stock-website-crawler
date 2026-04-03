"""
test_execution_mode_unification.py
执行模式统一测试

验证三种运行方式的统一性：
1. 包内导入运行
2. pytest 运行
3. 根目录脚本运行
"""

import pytest
import os
import sys
import subprocess
import tempfile
from pathlib import Path


class TestPackageImportMode:
    """测试包导入模式"""

    def test_main_package_importable(self):
        """测试主包可以正常导入"""
        import jk2bt as pkg

        assert pkg is not None
        assert hasattr(pkg, "__version__")
        assert hasattr(pkg, "__author__")

    def test_core_runner_importable(self):
        """测试核心运行器可以导入"""
        from jk2bt import run_jq_strategy
        from jk2bt import load_jq_strategy

        assert callable(run_jq_strategy)
        assert callable(load_jq_strategy)

    def test_data_api_importable(self):
        """测试数据 API 可以导入"""
        from jk2bt import (
            get_price,
            get_fundamentals,
            get_current_data,
            history,
        )

        assert callable(get_price)
        assert callable(get_fundamentals)

    def test_trading_api_importable(self):
        """测试交易 API 可以导入"""
        from jk2bt import (
            order_shares,
            order_target_percent,
        )

        assert callable(order_shares)
        assert callable(order_target_percent)

    def test_submodule_importable(self):
        """测试子模块可以导入"""
        from jk2bt.core.runner import run_jq_strategy
        from jk2bt.strategy.scanner import StrategyScanner
        from jk2bt.db.duckdb_manager import DuckDBManager

        assert callable(run_jq_strategy)
        assert StrategyScanner is not None
        assert DuckDBManager is not None

    def test_all_exported_symbols_accessible(self):
        """测试所有导出的符号都可以访问"""
        import jk2bt as pkg

        for symbol in pkg.__all__:
            obj = getattr(pkg, symbol, None)
            assert obj is not None, f"Symbol {symbol} in __all__ but not accessible"


class TestRelativeImportMode:
    """测试包内相对导入模式"""

    def test_market_data_relative_import(self):
        """测试 market_data 模块使用相对导入"""
        minute_path = Path(__file__).parent.parent / "src" / "market_data" / "minute.py"

        if minute_path.exists():
            content = minute_path.read_text()
            assert "from ..db" in content or "from ..utils" in content

    def test_finance_data_relative_import(self):
        """测试 finance_data 模块使用相对导入"""
        income_path = (
            Path(__file__).parent.parent / "src" / "finance_data" / "income.py"
        )

        if income_path.exists():
            content = income_path.read_text()
            has_relative_import = "from ..utils" in content or "from utils" in content
            assert has_relative_import


class TestRootScriptImportMode:
    """测试根目录脚本导入模式"""

    def test_run_strategies_parallel_import(self):
        """测试 run_strategies_parallel.py 可以导入"""
        try:
            from run_strategies_parallel import StrategyScanner

            assert StrategyScanner is not None
        except ImportError:
            pytest.skip("Script must be run from root directory")

    def test_run_daily_strategy_batch_import(self):
        """测试 run_daily_strategy_batch.py 可以导入"""
        try:
            from run_daily_strategy_batch import run_jq_strategy

            assert callable(run_jq_strategy)
        except ImportError:
            pytest.skip("Script must be run from root directory")

    def test_validate_strategies_import(self):
        """测试 validate_strategies.py 可以导入"""
        try:
            from validate_strategies import load_jq_strategy

            assert callable(load_jq_strategy)
        except ImportError:
            pytest.skip("Script must be run from root directory")

    def test_no_sys_path_insert_in_scripts(self):
        """测试根目录脚本不使用 sys.path.insert"""
        scripts = [
            "run_strategies_parallel.py",
            "run_daily_strategy_batch.py",
            "validate_strategies.py",
        ]

        for script in scripts:
            script_path = Path(__file__).parent.parent / script
            if script_path.exists():
                content = script_path.read_text()
                assert "sys.path.insert" not in content or "src" not in content


class TestPytestImportMode:
    """测试 pytest 运行模式"""

    def test_pytest_can_import_package(self):
        """pytest 可以正常导入包"""
        import jk2bt as src

        assert src is not None

    def test_pytest_can_import_submodules(self):
        """pytest 可以正常导入子模块"""
        from jk2bt.core.strategy_base import (
            JQ2BTBaseStrategy,
        )
        from jk2bt.strategy.scanner import StrategyScanner

        assert JQ2BTBaseStrategy is not None
        assert StrategyScanner is not None

    def test_pytest_no_sys_path_needed(self):
        """pytest 不需要手动设置 sys.path"""
        import jk2bt as src
        assert src is not None

        test_file_path = Path(__file__)
        content = test_file_path.read_text()

        lines = content.split("\n")
        has_path_insert_code = False
        for line in lines:
            stripped = line.strip()
            if (
                stripped
                and not stripped.startswith("#")
                and '"""' not in stripped
                and "'''" not in stripped
            ):
                if "sys.path.insert" in line and "src" in line:
                    has_path_insert_code = True
                    break

        assert not has_path_insert_code


class TestImportConsistency:
    """测试导入一致性"""

    def test_package_vs_submodule_import(self):
        """测试包导入和子模块导入一致性"""
        from jk2bt import run_jq_strategy as run1
        from jk2bt.core.runner import (
            run_jq_strategy as run2,
        )

        assert run1 == run2


class TestErrorHandling:
    """测试错误处理"""

    def test_import_error_message_friendly(self):
        """测试导入错误有友好提示"""
        temp_script = tempfile.NamedTemporaryFile(mode="w", suffix=".py", delete=False)
        temp_script.write("""
import sys
sys.path.insert(0, '/nonexistent/path')
try:
    from jk2bt import run_jq_strategy
except ImportError as e:
    print(f"ImportError: {e}")
    sys.exit(1)
""")
        temp_script.close()

        result = subprocess.run(
            [sys.executable, temp_script.name],
            capture_output=True,
            text=True,
            cwd=Path(__file__).parent.parent,
        )

        os.unlink(temp_script.name)

        if result.returncode != 0:
            assert "ImportError" in result.stdout or "ImportError" in result.stderr


class TestBackwardCompatibility:
    """测试向后兼容性"""

    def test_runner_has_fallback_import(self):
        """测试 runner 有 fallback 导入机制"""
        runner_path = Path(__file__).parent.parent / "src" / "jq_strategy_runner.py"

        if runner_path.exists():
            content = runner_path.read_text()
            assert "try:" in content and "except ImportError" in content

    def test_old_import_style_compatible(self):
        """测试旧的导入风格仍然兼容"""
        try:
            from jk2bt.core.runner import (
                run_jq_strategy,
            )

            assert callable(run_jq_strategy)
        except ImportError:
            pytest.fail("Old import style should still work")


def test_execution_modes_summary():
    """执行模式统一总结测试"""
    print("\n" + "=" * 60)
    print("执行模式统一验证总结")
    print("=" * 60)

    try:
        import jk2bt as pkg

        print("✅ 包导入模式正常")
    except ImportError as e:
        print(f"❌ 包导入失败: {e}")

    try:
        from jk2bt import run_jq_strategy

        print("✅ pytest 运行模式正常")
    except ImportError as e:
        print(f"❌ pytest 导入失败: {e}")

    try:
        from run_strategies_parallel import StrategyScanner

        print("✅ 根目录脚本导入模式正常")
    except ImportError:
        print("⚠️  根目录脚本导入需要从根目录运行")

    try:
        from jk2bt.market_data.minute import (
            get_stock_minute,
        )

        print("✅ 包内相对导入模式正常")
    except ImportError as e:
        print(f"❌ 相对导入失败: {e}")

    print("=" * 60)
    print("建议运行方式:")
    print("  1. 包导入: python3 -c 'from jk2bt import ...'")
    print("  2. pytest: python3 -m pytest tests/")
    print("  3. 脚本: 在仓库根目录运行 python3 script.py")
    print("=" * 60)


if __name__ == "__main__":
    pytest.main([__file__, "-v", "-s"])
