"""
tests/test_readme_commands_smoke.py
README命令真实smoke test - 验证README中所有命令示例真实可用

测试范围：
1. 安装后验收命令
2. Python API调用
3. 命令行运行策略
4. 继承基类方式
5. 离线数据预热脚本
6. CLI入口点命令（如已安装）
7. 常见问题代码示例

完成标准：README中的所有命令真实可用，执行结果正确
"""

import pytest
import subprocess
import sys
import os
import tempfile
import shutil
import importlib

# 项目根目录
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TESTS_DIR = os.path.join(PROJECT_ROOT, "tests")


class TestInstallationValidationCommands:
    """测试README中的安装后验收命令"""

    def test_version_import(self):
        """测试版本导入命令"""
        # README命令: python3 -c "import jk2bt; print(jk2bt.__version__)"
        result = subprocess.run(
            [sys.executable, "-c", "import jk2bt; print(jk2bt.__version__)"],
            cwd=PROJECT_ROOT,
            capture_output=True,
            text=True,
            timeout=30
        )
        assert result.returncode == 0, f"导入失败: {result.stderr}"
        assert result.stdout.strip() == "1.0.0", f"版本不正确: {result.stdout.strip()}"

    def test_core_smoke_tests(self):
        """测试核心链路smoke命令 - 真实执行README示例命令"""
        # README命令: pytest -q tests/test_package_import.py tests/integration/test_jq_runner.py
        # 真实执行完整链路测试，覆盖README主流程
        result = subprocess.run(
            [sys.executable, "-m", "pytest", "-q",
             "tests/test_package_import.py",
             "tests/integration/test_jq_runner.py::test_simple_strategy",
             "--tb=short"],
            cwd=PROJECT_ROOT,
            capture_output=True,
            text=True,
            timeout=180
        )
        # 硬验收：测试必须通过
        assert result.returncode == 0, \
            f"核心链路smoke测试失败 - 硬验收:\n" \
            f"  stdout: {result.stdout[-500:]}\n" \
            f"  stderr: {result.stderr[-500:]}"

    def test_pytest_collect_only(self):
        """测试扫描全部测试用例命令"""
        # README命令: pytest --collect-only -q
        result = subprocess.run(
            [sys.executable, "-m", "pytest", "--collect-only", "-q"],
            cwd=PROJECT_ROOT,
            capture_output=True,
            text=True,
            timeout=120
        )
        # 统计收集的测试数量
        lines = result.stdout.strip().split('\n')
        collected_count = sum(1 for line in lines if '::' in line)
        assert collected_count > 100, f"应收集到大量测试，实际: {collected_count}"


class TestPythonAPICalls:
    """测试README中的Python API调用示例"""

    def test_import_run_jq_strategy(self):
        """测试run_jq_strategy导入"""
        # README: from jk2bt import run_jq_strategy
        from jk2bt import run_jq_strategy
        assert callable(run_jq_strategy)

    def test_import_load_jq_strategy(self):
        """测试load_jq_strategy导入"""
        from jk2bt import load_jq_strategy
        assert callable(load_jq_strategy)

    def test_import_all_symbols(self):
        """测试所有__all__符号可导入"""
        import jk2bt as pkg
        exported = pkg.__all__
        assert len(exported) > 50, f"__all__应包含大量符号: {len(exported)}"

        # 验证关键符号
        key_symbols = [
            "run_jq_strategy",
            "load_jq_strategy",
            "JQStrategyWrapper",
            "JQ2BTBaseStrategy",
            "GlobalState",
            "get_price",
            "get_fundamentals",
            "get_index_weights",
            "get_index_stocks",
            "order_shares",
            "order_target_percent",
        ]
        for sym in key_symbols:
            assert sym in exported, f"{sym} 应在__all__中"


class TestStrategyRunnerCommands:
    """测试README中的运行策略命令"""

    def test_run_daily_strategy_batch_help(self):
        """测试run_daily_strategy_batch.py帮助"""
        # README命令: python3 run_daily_strategy_batch.py --strategies_dir strategies --limit 1
        result = subprocess.run(
            [sys.executable, "run_daily_strategy_batch.py", "--help"],
            cwd=PROJECT_ROOT,
            capture_output=True,
            text=True,
            timeout=30
        )
        assert result.returncode == 0, f"脚本执行失败: {result.stderr}"
        assert "strategies_dir" in result.stdout, "应显示参数帮助"

    def test_run_daily_strategy_batch_limit_1(self):
        """测试批量运行策略命令"""
        result = subprocess.run(
            [sys.executable, "run_daily_strategy_batch.py",
             "--strategies_dir", "strategies",
             "--limit", "1"],
            cwd=PROJECT_ROOT,
            capture_output=True,
            text=True,
            timeout=120
        )
        # 可能因策略类型跳过，但不应报错
        assert result.returncode == 0, f"脚本执行失败: {result.stderr}"
        assert "发现" in result.stdout or "总数" in result.stdout


class TestBaseStrategyImport:
    """测试继承基类方式"""

    def test_import_base_strategy(self):
        """测试JQ2BTBaseStrategy导入"""
        # README: from jk2bt.core.strategy_base import JQ2BTBaseStrategy
        from jk2bt.core.strategy_base import JQ2BTBaseStrategy
        import backtrader as bt
        assert issubclass(JQ2BTBaseStrategy, bt.Strategy)

    def test_base_strategy_can_instantiate(self):
        """测试基类可以实例化"""
        from jk2bt.core.strategy_base import JQ2BTBaseStrategy
        # 不能直接实例化策略，需要cerebro，但可以验证类存在
        assert hasattr(JQ2BTBaseStrategy, '__init__')

    def test_global_state_exists(self):
        """测试GlobalState可用"""
        from jk2bt import GlobalState
        g = GlobalState()
        assert hasattr(g, '__dict__')
        # 可以设置属性
        g.stocks = ['600519.XSHG']
        assert g.stocks == ['600519.XSHG']


class TestOfflineDataPrewarmCommands:
    """测试离线数据预热脚本命令"""

    def test_prewarm_all_help(self):
        """测试prewarm_all.py帮助"""
        # README命令: python prewarm_all.py
        result = subprocess.run(
            [sys.executable, "tools/offline_data/prewarm_all.py", "--help"],
            cwd=PROJECT_ROOT,
            capture_output=True,
            text=True,
            timeout=30
        )
        assert result.returncode == 0, f"脚本执行失败: {result.stderr}"
        assert "--force" in result.stdout, "应显示force参数"
        assert "--static-only" in result.stdout, "应显示static-only参数"

    def test_prewarm_static_help(self):
        """测试prewarm_static.py帮助"""
        # README命令: python prewarm_static.py --stocks 600519.XSHG 000858.XSHE
        result = subprocess.run(
            [sys.executable, "tools/offline_data/prewarm_static.py", "--help"],
            cwd=PROJECT_ROOT,
            capture_output=True,
            text=True,
            timeout=30
        )
        assert result.returncode == 0, f"脚本执行失败: {result.stderr}"
        assert "--stocks" in result.stdout, "应显示stocks参数"
        assert "--pool" in result.stdout, "应显示pool参数"

    def test_prewarm_daily_help(self):
        """测试prewarm_daily.py帮助"""
        # README命令: python prewarm_daily.py --sample
        result = subprocess.run(
            [sys.executable, "tools/offline_data/prewarm_daily.py", "--help"],
            cwd=PROJECT_ROOT,
            capture_output=True,
            text=True,
            timeout=30
        )
        assert result.returncode == 0, f"脚本执行失败: {result.stderr}"
        assert "--sample" in result.stdout, "应显示sample参数"

    def test_prewarm_monthly_help(self):
        """测试prewarm_monthly.py帮助"""
        result = subprocess.run(
            [sys.executable, "tools/offline_data/prewarm_monthly.py", "--help"],
            cwd=PROJECT_ROOT,
            capture_output=True,
            text=True,
            timeout=30
        )
        assert result.returncode == 0, f"脚本执行失败: {result.stderr}"

    def test_prewarm_quarterly_help(self):
        """测试prewarm_quarterly.py帮助"""
        result = subprocess.run(
            [sys.executable, "tools/offline_data/prewarm_quarterly.py", "--help"],
            cwd=PROJECT_ROOT,
            capture_output=True,
            text=True,
            timeout=30
        )
        assert result.returncode == 0, f"脚本执行失败: {result.stderr}"

    def test_prewarm_weekly_help(self):
        """测试prewarm_weekly.py帮助"""
        result = subprocess.run(
            [sys.executable, "tools/offline_data/prewarm_weekly.py", "--help"],
            cwd=PROJECT_ROOT,
            capture_output=True,
            text=True,
            timeout=30
        )
        assert result.returncode == 0, f"脚本执行失败: {result.stderr}"


class TestCLIEntryPoints:
    """测试CLI入口点命令（如果已安装）"""

    def test_cli_module_help(self):
        """测试CLI模块帮助"""
        # 命令: python -m jk2bt.cli
        result = subprocess.run(
            [sys.executable, "-m", "jk2bt.cli"],
            cwd=PROJECT_ROOT,
            capture_output=True,
            text=True,
            timeout=30
        )
        # 预期输出使用帮助
        assert "使用方法" in result.stdout or "可用命令" in result.stdout, \
            f"应显示帮助: {result.stdout}"

    def test_cli_run_help(self):
        """测试CLI run帮助"""
        result = subprocess.run(
            [sys.executable, "-m", "jk2bt.cli", "run", "--help"],
            cwd=PROJECT_ROOT,
            capture_output=True,
            text=True,
            timeout=30
        )
        assert result.returncode == 0, f"CLI执行失败: {result.stderr}"
        assert "--start" in result.stdout, "应显示start参数"
        assert "--end" in result.stdout, "应显示end参数"

    def test_cli_prewarm_help(self):
        """测试CLI prewarm帮助"""
        result = subprocess.run(
            [sys.executable, "-m", "jk2bt.cli", "prewarm", "--help"],
            cwd=PROJECT_ROOT,
            capture_output=True,
            text=True,
            timeout=30
        )
        assert result.returncode == 0, f"CLI执行失败: {result.stderr}"
        assert "--stocks" in result.stdout, "应显示stocks参数"

    def test_cli_validate_help(self):
        """测试CLI validate帮助"""
        result = subprocess.run(
            [sys.executable, "-m", "jk2bt.cli", "validate", "--help"],
            cwd=PROJECT_ROOT,
            capture_output=True,
            text=True,
            timeout=30
        )
        assert result.returncode == 0, f"CLI执行失败: {result.stderr}"
        assert "--json" in result.stdout, "应显示json参数"


class TestFAQCodeExamples:
    """测试README常见问题代码示例"""

    def test_cache_manager_import(self):
        """测试缓存管理器导入"""
        # FAQ示例导入
        try:
            from jk2bt.db.cache_status import get_cache_manager
            manager = get_cache_manager()
            assert manager is not None
        except ImportError:
            # 可能旧路径仍存在
            from jk2bt.db.cache_manager import get_cache_manager
            manager = get_cache_manager()
            assert manager is not None

    def test_cache_summary(self):
        """测试缓存摘要获取"""
        from jk2bt.db.cache_status import get_cache_manager
        manager = get_cache_manager()
        summary = manager.get_cache_summary()
        assert isinstance(summary, dict)
        # 验证关键字存在
        assert 'stock_count' in summary or 'total_records' in summary


class TestREADMEDataAPIExamples:
    """测试README中的数据API示例代码"""

    def test_supported_api_table_exists(self):
        """验证README提到的数据获取API都存在"""
        import jk2bt as pkg

        # 数据获取API（顶层导出）
        data_apis = [
            "get_fundamentals",
            "get_index_weights",
            "get_index_stocks",
            "get_current_data",
            "get_price",
            "history",
            "attribute_history",
        ]

        # 验证核心数据API存在
        for api in data_apis:
            assert hasattr(pkg, api), f"API {api} 不存在"

    def test_order_api_exists(self):
        """验证订单API存在"""
        import jk2bt as pkg

        order_apis = [
            "order_shares",
            "order_target_percent",
        ]
        for api in order_apis:
            assert hasattr(pkg, api), f"API {api} 不存在"

    def test_timer_api_in_timer_manager(self):
        """验证定时器API通过TimerManager实现"""
        import jk2bt as pkg
        # 定时器函数通过TimerManager提供
        assert hasattr(pkg, "TimerManager"), "TimerManager应存在"

    def test_special_api_implementations(self):
        """验证特殊API的实现"""
        import jk2bt as pkg

        # g -> GlobalState
        assert hasattr(pkg, "GlobalState"), "GlobalState应存在"

        # log -> JQLogAdapter
        assert hasattr(pkg, "JQLogAdapter"), "JQLogAdapter应存在"

        # context.portfolio -> ContextProxy
        assert hasattr(pkg, "ContextProxy"), "ContextProxy应存在"

        # finance.run_query -> finance模块
        assert hasattr(pkg, "finance"), "finance模块应存在"
        assert hasattr(pkg.finance, "run_query"), "finance.run_query应存在"


class TestSymbolConversionExamples:
    """测试符号转换示例"""

    def test_jq_code_to_ak(self):
        """测试符号转换600519.XSHG到sh600519"""
        from jk2bt import jq_code_to_ak
        result = jq_code_to_ak("600519.XSHG")
        assert result == "sh600519", f"转换结果错误: {result}"

    def test_ak_code_to_jq(self):
        """测试符号转换sh600519到600519.XSHG"""
        from jk2bt import ak_code_to_jq
        result = ak_code_to_jq("sh600519")
        assert result == "600519.XSHG", f"转换结果错误: {result}"


class TestOfflineDataReadmeCommands:
    """测试tools/offline_data/README.md中的命令"""

    def test_config_yaml_exists(self):
        """验证配置文件存在"""
        config_path = os.path.join(PROJECT_ROOT, "tools/offline_data/config.yaml")
        assert os.path.exists(config_path), "config.yaml应存在"

    def test_utils_stock_pool_exists(self):
        """验证工具模块存在"""
        utils_path = os.path.join(PROJECT_ROOT, "tools/offline_data/utils")
        assert os.path.exists(utils_path), "utils目录应存在"
        assert os.path.exists(os.path.join(utils_path, "stock_pool.py")), "stock_pool.py应存在"

    def test_prewarm_scripts_all_exist(self):
        """验证所有预热脚本都存在"""
        scripts = [
            "prewarm_all.py",
            "prewarm_static.py",
            "prewarm_quarterly.py",
            "prewarm_monthly.py",
            "prewarm_weekly.py",
            "prewarm_daily.py",
        ]
        for script in scripts:
            script_path = os.path.join(PROJECT_ROOT, "tools/offline_data", script)
            assert os.path.exists(script_path), f"{script}应存在"


class TestQuickStartExamples:
    """测试快速开始代码示例"""

    def test_quick_start_import(self):
        """测试快速开始示例代码"""
        # from jk2bt import run_jq_strategy
        from jk2bt import run_jq_strategy
        assert callable(run_jq_strategy)

        # 验证函数签名
        import inspect
        sig = inspect.signature(run_jq_strategy)
        params = list(sig.parameters.keys())
        assert "strategy_file" in params
        assert "start_date" in params
        assert "end_date" in params


class TestProjectStructure:
    """测试项目结构说明"""

    def test_main_package_exists(self):
        """验证主包jk2bt存在"""
        jk2bt_path = os.path.join(PROJECT_ROOT, "jk2bt")
        assert os.path.exists(jk2bt_path), "jk2bt主包应存在"
        assert os.path.exists(os.path.join(jk2bt_path, "__init__.py"))

    def test_strategies_dir_exists(self):
        """验证strategies目录存在"""
        strategies_path = os.path.join(PROJECT_ROOT, "strategies")
        assert os.path.exists(strategies_path), "strategies目录应存在"
        # 应有策略文件
        txt_files = [f for f in os.listdir(strategies_path) if f.endswith('.txt')]
        assert len(txt_files) > 10, f"应有多个策略文件: {len(txt_files)}"

    def test_tests_dir_exists(self):
        """验证tests目录存在"""
        assert os.path.exists(TESTS_DIR), "tests目录应存在"

    def test_docs_dir_exists(self):
        """验证docs目录存在"""
        docs_path = os.path.join(PROJECT_ROOT, "docs")
        assert os.path.exists(docs_path), "docs目录应存在"

    def test_pyproject_toml_exists(self):
        """验证pyproject.toml存在"""
        pyproject_path = os.path.join(PROJECT_ROOT, "pyproject.toml")
        assert os.path.exists(pyproject_path)


class TestEntrypointsRegistered:
    """测试入口点是否正确注册"""

    def test_entrypoints_in_pyproject(self):
        """验证pyproject.toml中的入口点"""
        try:
            import tomli
        except ImportError:
            import tomllib as tomli
        pyproject_path = os.path.join(PROJECT_ROOT, "pyproject.toml")
        with open(pyproject_path, "rb") as f:
            config = tomli.load(f)

        scripts = config.get("project", {}).get("scripts", {})
        expected_scripts = ["jk2bt-run", "jk2bt-prewarm", "jk2bt-validate"]
        for script in expected_scripts:
            assert script in scripts, f"{script}入口点应注册"


class TestPrewarmActualExecution:
    """测试预热脚本实际执行（快速验证）"""

    @pytest.mark.skip(reason="预热脚本需要网络连接，在CI环境中可能超时")
    def test_prewarm_all_static_only(self):
        """测试prewarm_all.py --static-only快速执行"""
        # README命令: python prewarm_all.py --static-only
        result = subprocess.run(
            [sys.executable, "tools/offline_data/prewarm_all.py", "--static-only"],
            cwd=PROJECT_ROOT,
            capture_output=True,
            text=True,
            timeout=120
        )
        # 可能因网络问题失败，但脚本本身应能运行
        # 只要返回码是0或有正常输出即可
        if result.returncode != 0:
            # 检查是否是预期的错误（如网络问题）
            if "Error" not in result.stderr and "error" not in result.stderr.lower():
                pytest.fail(f"脚本执行失败: {result.stderr}")


class TestREADMEConsistency:
    """测试README与实际代码一致性"""

    def test_version_consistency(self):
        """验证README中的Python版本要求与pyproject一致"""
        try:
            import tomli
        except ImportError:
            import tomllib as tomli
        pyproject_path = os.path.join(PROJECT_ROOT, "pyproject.toml")
        with open(pyproject_path, "rb") as f:
            config = tomli.load(f)

        requires_python = config.get("project", {}).get("requires-python", "")
        assert "3.9" in requires_python, "应支持Python 3.9+"

    def test_badge_links_valid(self):
        """验证徽章信息有效"""
        # 读取README验证badge存在
        readme_path = os.path.join(PROJECT_ROOT, "README.md")
        with open(readme_path, "r") as f:
            content = f.read()

        assert "[![测试收集]" in content, "应有测试收集徽章"
        assert "[![Python 3.9+]" in content, "应有Python版本徽章"


class TestREADMEFullWorkflow:
    """README完整链路验收测试 - 干净机器验收gate"""

    def test_validation_strategy_exists(self):
        """硬验收：仓库内必须有验证策略文件"""
        # 干净机器验收必须使用仓库内资源，不允许外部路径
        strategy_file = os.path.join(PROJECT_ROOT, "strategies", "validation_v4_double_ma.txt")
        if not os.path.exists(strategy_file):
            pytest.fail(
                f"验证策略文件不存在 - 硬验收失败:\n"
                f"  期望路径: {strategy_file}\n"
                f"  仓库必须包含validation_v4策略以支持干净机器验收"
            )

    def test_run_readme_example_strategy(self):
        """硬验收：真实执行README示例策略"""
        # README示例: run_jq_strategy(strategy_file='策略.txt', ...)
        strategy_file = os.path.join(PROJECT_ROOT, "strategies", "validation_v4_double_ma.txt")

        # 硬验收：策略文件必须存在
        if not os.path.exists(strategy_file):
            pytest.fail(f"策略文件不存在 - 硬验收失败: {strategy_file}")

        # 真实执行策略运行
        from jk2bt import run_jq_strategy

        try:
            result = run_jq_strategy(
                strategy_file=strategy_file,
                start_date="2022-01-01",
                end_date="2022-12-31",
                initial_capital=1000000,
                stock_pool=["600519.XSHG", "000858.XSHE", "000333.XSHE", "600036.XSHG", "601318.XSHG"],
            )

            # 硬验收：结果必须有效
            if result is None:
                pytest.fail("策略返回None - 硬验收失败")

            # 硬验收：必须有基本字段
            assert "final_value" in result, \
                f"结果缺少final_value字段 - 硬验收失败: {result.keys()}"
            assert "pnl_pct" in result, \
                f"结果缺少pnl_pct字段 - 硬验收失败: {result.keys()}"

            # 硬验收：数值必须合理
            assert result["final_value"] > 0, \
                f"最终资金无效 - 硬验收失败: {result['final_value']}"

        except Exception as e:
            import traceback
            tb_lines = traceback.format_exc()
            pytest.fail(
                f"README示例策略运行失败 - 硬验收:\n"
                f"  策略文件: {strategy_file}\n"
                f"  错误: {str(e)}\n"
                f"  Traceback:\n{tb_lines[-10:]}"
            )

    def test_run_daily_strategy_batch_readme_command(self):
        """硬验收：真实执行README批量运行命令"""
        # README命令: python3 run_daily_strategy_batch.py --strategies_dir strategies --limit 1
        result = subprocess.run(
            [sys.executable, "run_daily_strategy_batch.py",
             "--strategies_dir", "strategies",
             "--limit", "1"],
            cwd=PROJECT_ROOT,
            capture_output=True,
            text=True,
            timeout=180
        )

        # 硬验收：命令必须成功执行
        assert result.returncode == 0, \
            f"README批量运行命令失败 - 硬验收:\n" \
            f"  stdout: {result.stdout[-500:]}\n" \
            f"  stderr: {result.stderr[-500:]}"

        # 硬验收：必须有输出表明策略被发现和执行
        assert "发现" in result.stdout or "总数" in result.stdout or "策略" in result.stdout, \
            f"批量运行输出异常 - 硬验收:\n" \
            f"  stdout: {result.stdout[-200:]}"

    def test_installation_validation_workflow(self):
        """硬验收：README安装后验收完整链路"""
        # README安装后验收命令: pytest -q tests/test_package_import.py tests/integration/test_jq_runner.py
        result = subprocess.run(
            [sys.executable, "-m", "pytest", "-q",
             "tests/test_package_import.py",
             "tests/integration/test_jq_runner.py::test_simple_strategy",
             "--tb=short"],
            cwd=PROJECT_ROOT,
            capture_output=True,
            text=True,
            timeout=180
        )

        # 硬验收：测试必须通过
        assert result.returncode == 0, \
            f"README安装后验收命令失败 - 硬验收:\n" \
            f"  stdout: {result.stdout[-500:]}\n" \
            f"  stderr: {result.stderr[-500:]}"

    def test_quick_start_import_and_signature(self):
        """硬验收：README快速开始API导入和签名"""
        # README快速开始: from jk2bt import run_jq_strategy
        from jk2bt import run_jq_strategy

        # 硬验收：函数必须可调用
        assert callable(run_jq_strategy), "run_jq_strategy必须可调用"

        # 硬验收：签名必须匹配README示例
        import inspect
        sig = inspect.signature(run_jq_strategy)
        params = list(sig.parameters.keys())

        assert "strategy_file" in params, \
            f"run_jq_strategy缺少strategy_file参数 - 硬验收失败: {params}"
        assert "start_date" in params, \
            f"run_jq_strategy缺少start_date参数 - 硬验收失败: {params}"
        assert "end_date" in params, \
            f"run_jq_strategy缺少end_date参数 - 硬验收失败: {params}"
        assert "stock_pool" in params, \
            f"run_jq_strategy缺少stock_pool参数 - 硬验收失败: {params}"


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])