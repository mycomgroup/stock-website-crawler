"""
test_dependency_checker.py
依赖检查脚本的单元测试

覆盖:
- DEPENDENCY_REGISTRY 数据完整性
- check_single_dependency 单包检查
- check_dependencies 全量检查
- check_required_dependencies 必装检查
- check_ml_dependencies ML依赖检查
- get_install_recommendation 安装建议
- import_with_check 安全导入
- safe_import 降级导入
- startup_check 启动自检
"""

import pytest
import sys
import warnings
from unittest.mock import patch, MagicMock


class TestDependencyRegistry:
    """测试依赖注册表完整性"""

    def test_registry_has_required_deps(self):
        from jk2bt.dependency_checker import (
            DEPENDENCY_REGISTRY,
            DependencyLevel,
        )

        required_names = ["pandas", "numpy", "akshare", "backtrader", "statsmodels"]
        for name in required_names:
            assert name in DEPENDENCY_REGISTRY
            assert DEPENDENCY_REGISTRY[name].level == DependencyLevel.REQUIRED

    def test_registry_has_optional_deps(self):
        from jk2bt.dependency_checker import (
            DEPENDENCY_REGISTRY,
            DependencyLevel,
        )

        optional_names = ["matplotlib", "duckdb", "pytest"]
        for name in optional_names:
            assert name in DEPENDENCY_REGISTRY
            assert DEPENDENCY_REGISTRY[name].level == DependencyLevel.OPTIONAL

    def test_registry_has_ml_advanced_deps(self):
        from jk2bt.dependency_checker import (
            DEPENDENCY_REGISTRY,
            DependencyLevel,
        )

        ml_names = ["qlib", "sklearn", "xgboost", "lightgbm", "talib"]
        for name in ml_names:
            assert name in DEPENDENCY_REGISTRY
            assert DEPENDENCY_REGISTRY[name].level == DependencyLevel.ML_ADVANCED

    def test_registry_has_not_supported_deps(self):
        from jk2bt.dependency_checker import (
            DEPENDENCY_REGISTRY,
            DependencyLevel,
        )

        not_supported = ["torch", "tensorflow"]
        for name in not_supported:
            assert name in DEPENDENCY_REGISTRY
            assert DEPENDENCY_REGISTRY[name].level == DependencyLevel.NOT_SUPPORTED

    def test_each_dep_has_install_cmd(self):
        from jk2bt.dependency_checker import (
            DEPENDENCY_REGISTRY,
        )

        for name, dep in DEPENDENCY_REGISTRY.items():
            assert dep.install_cmd, f"{name} 缺少 install_cmd"
            assert "pip install" in dep.install_cmd or name == "talib"

    def test_each_dep_has_description(self):
        from jk2bt.dependency_checker import (
            DEPENDENCY_REGISTRY,
        )

        for name, dep in DEPENDENCY_REGISTRY.items():
            assert dep.description, f"{name} 缺少 description"


class TestCheckSingleDependency:
    """测试单包检查"""

    def test_check_pandas_exists(self):
        from jk2bt.dependency_checker import (
            check_single_dependency,
            DEPENDENCY_REGISTRY,
        )

        ok, version = check_single_dependency(DEPENDENCY_REGISTRY["pandas"])
        assert ok is True
        assert version is not None

    def test_check_numpy_exists(self):
        from jk2bt.dependency_checker import (
            check_single_dependency,
            DEPENDENCY_REGISTRY,
        )

        ok, version = check_single_dependency(DEPENDENCY_REGISTRY["numpy"])
        assert ok is True
        assert version is not None

    def test_check_missing_package(self):
        from jk2bt.dependency_checker import (
            check_single_dependency,
            DependencyInfo,
            DependencyLevel,
        )

        fake_dep = DependencyInfo(
            name="fake_package_xyz",
            import_name="fake_package_xyz",
            level=DependencyLevel.OPTIONAL,
            install_cmd="pip install fake_package_xyz",
            description="测试用假包",
        )

        ok, error = check_single_dependency(fake_dep)
        assert ok is False
        assert error is not None

    def test_check_sklearn_import_name(self):
        from jk2bt.dependency_checker import (
            check_single_dependency,
            DEPENDENCY_REGISTRY,
        )

        ok, version = check_single_dependency(DEPENDENCY_REGISTRY["sklearn"])
        assert isinstance(ok, bool)


class TestCheckDependencies:
    """测试全量检查"""

    def test_check_all_returns_dict(self):
        from jk2bt.dependency_checker import (
            check_dependencies,
        )

        results = check_dependencies(verbose=False)
        assert isinstance(results, dict)
        assert len(results) > 0

    def test_check_by_level_required(self):
        from jk2bt.dependency_checker import (
            check_dependencies,
            DependencyLevel,
        )

        results = check_dependencies(level=DependencyLevel.REQUIRED, verbose=False)
        assert all(
            name in ["pandas", "numpy", "akshare", "backtrader", "statsmodels"]
            for name in results.keys()
        )

    def test_check_by_level_optional(self):
        from jk2bt.dependency_checker import (
            check_dependencies,
            DependencyLevel,
        )

        results = check_dependencies(level=DependencyLevel.OPTIONAL, verbose=False)
        assert all(
            name in ["matplotlib", "duckdb", "pytest"] for name in results.keys()
        )

    def test_check_verbose_output(self, capsys):
        from jk2bt.dependency_checker import (
            check_dependencies,
            DependencyLevel,
        )

        check_dependencies(level=DependencyLevel.REQUIRED, verbose=True)
        captured = capsys.readouterr()
        assert "pandas" in captured.out or len(captured.out) > 0


class TestCheckRequiredDependencies:
    """测试必装依赖检查"""

    def test_required_deps_present(self):
        from jk2bt.dependency_checker import (
            check_required_dependencies,
        )

        result = check_required_dependencies()
        assert result is True

    def test_required_missing_returns_false(self):
        from jk2bt.dependency_checker import (
            check_required_dependencies,
            DEPENDENCY_REGISTRY,
            DependencyLevel,
        )

        original_pandas = DEPENDENCY_REGISTRY["pandas"]

        with patch.dict(DEPENDENCY_REGISTRY, {"pandas": MagicMock()}):
            mock_dep = MagicMock()
            mock_dep.level = DependencyLevel.REQUIRED
            mock_dep.install_cmd = "pip install pandas"
            mock_dep.import_name = "nonexistent_package"

            with patch(
                "src.dependency_checker.check_single_dependency",
                return_value=(False, "No module"),
            ):
                result = check_required_dependencies()
                assert result is False


class TestCheckMLDependencies:
    """测试ML依赖检查"""

    def test_ml_check_returns_dict(self):
        from jk2bt.dependency_checker import (
            check_ml_dependencies,
        )

        results = check_ml_dependencies(verbose=False)
        assert isinstance(results, dict)

    def test_ml_check_includes_optional(self):
        from jk2bt.dependency_checker import (
            check_ml_dependencies,
        )

        results = check_ml_dependencies(verbose=False)
        assert "matplotlib" in results
        assert "duckdb" in results

    def test_ml_check_includes_advanced(self):
        from jk2bt.dependency_checker import (
            check_ml_dependencies,
        )

        results = check_ml_dependencies(verbose=False)
        assert "qlib" in results
        assert "sklearn" in results
        assert "xgboost" in results


class TestGetInstallRecommendation:
    """测试安装建议"""

    def test_basic_recommendation(self):
        from jk2bt.dependency_checker import (
            get_install_recommendation,
        )

        cmds = get_install_recommendation("basic")
        assert len(cmds) >= 5
        assert any("pandas" in cmd for cmd in cmds)

    def test_full_recommendation(self):
        from jk2bt.dependency_checker import (
            get_install_recommendation,
        )

        cmds = get_install_recommendation("full")
        assert len(cmds) >= 8
        assert any("matplotlib" in cmd for cmd in cmds)

    def test_ml_recommendation(self):
        from jk2bt.dependency_checker import (
            get_install_recommendation,
        )

        cmds = get_install_recommendation("ml")
        assert len(cmds) >= 12
        assert any("sklearn" in cmd or "scikit-learn" in cmd for cmd in cmds)

    def test_qlib_recommendation(self):
        from jk2bt.dependency_checker import (
            get_install_recommendation,
        )

        cmds = get_install_recommendation("qlib")
        assert "qlib" in cmds or any("qlib" in cmd for cmd in cmds)

    def test_unknown_use_case(self):
        from jk2bt.dependency_checker import (
            get_install_recommendation,
        )

        cmds = get_install_recommendation("unknown_xyz")
        assert cmds == []


class TestImportWithCheck:
    """测试安全导入"""

    def test_import_existing_package(self):
        from jk2bt.dependency_checker import (
            import_with_check,
        )

        pd = import_with_check("pandas", required=False)
        assert pd is not None
        assert hasattr(pd, "DataFrame")

    def test_import_missing_optional_warns(self):
        from jk2bt.dependency_checker import (
            import_with_check,
        )

        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            result = import_with_check("nonexistent_pkg", required=False)
            assert result is None
            assert len(w) >= 1

    def test_import_missing_required_raises(self):
        from jk2bt.dependency_checker import (
            import_with_check,
        )

        with pytest.raises(ImportError) as exc_info:
            import_with_check("nonexistent_pkg", required=True)

        assert "缺少必装依赖" in str(exc_info.value)

    def test_import_unknown_module_warns(self):
        from jk2bt.dependency_checker import (
            import_with_check,
        )

        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            result = import_with_check("fake_unknown_module_xyz", required=False)
            assert result is None


class TestSafeImport:
    """测试降级导入"""

    def test_safe_import_existing(self):
        from jk2bt.dependency_checker import (
            safe_import,
        )

        pd = safe_import("pandas")
        assert pd is not None

    def test_safe_import_missing_returns_none(self):
        from jk2bt.dependency_checker import (
            safe_import,
        )

        result = safe_import("nonexistent_pkg")
        assert result is None

    def test_safe_import_with_fallback_missing(self):
        from jk2bt.dependency_checker import (
            safe_import,
        )

        result = safe_import("nonexistent_pkg", fallback="also_nonexistent")
        assert result is None

    def test_safe_import_fallback_used(self):
        from jk2bt.dependency_checker import (
            safe_import,
        )

        result = safe_import("nonexistent_xyz", fallback="pandas")
        assert result is not None
        assert hasattr(result, "DataFrame")


class TestStartupCheck:
    """测试启动自检"""

    def test_startup_check_returns_bool(self):
        from jk2bt.dependency_checker import (
            startup_check,
        )

        result = startup_check()
        assert isinstance(result, bool)

    def test_startup_check_prints_header(self, capsys):
        from jk2bt.dependency_checker import (
            startup_check,
        )

        startup_check()
        captured = capsys.readouterr()
        assert "依赖自检" in captured.out
        assert "=" in captured.out

    def test_startup_check_reports_missing_ml(self, capsys):
        from jk2bt.dependency_checker import (
            startup_check,
        )

        startup_check()
        captured = capsys.readouterr()
        assert (
            "qlib" in captured.out or "MISSING" in captured.out or "OK" in captured.out
        )


class TestDependencyLevelEnum:
    """测试依赖层级枚举"""

    def test_level_values(self):
        from jk2bt.dependency_checker import (
            DependencyLevel,
        )

        assert DependencyLevel.REQUIRED.value == "required"
        assert DependencyLevel.OPTIONAL.value == "optional"
        assert DependencyLevel.ML_ADVANCED.value == "ml_advanced"
        assert DependencyLevel.NOT_SUPPORTED.value == "not_supported"


class TestDependencyInfoDataclass:
    """测试依赖信息数据类"""

    def test_create_dependency_info(self):
        from jk2bt.dependency_checker import (
            DependencyInfo,
            DependencyLevel,
        )

        dep = DependencyInfo(
            name="test_pkg",
            import_name="test_pkg",
            level=DependencyLevel.OPTIONAL,
            install_cmd="pip install test_pkg",
            description="测试包",
            alternative="可跳过",
        )

        assert dep.name == "test_pkg"
        assert dep.level == DependencyLevel.OPTIONAL
        assert dep.alternative == "可跳过"

    def test_dependency_info_without_optional_fields(self):
        from jk2bt.dependency_checker import (
            DependencyInfo,
            DependencyLevel,
        )

        dep = DependencyInfo(
            name="test_pkg",
            import_name="test_pkg",
            level=DependencyLevel.REQUIRED,
            install_cmd="pip install test_pkg",
            description="必装包",
        )

        assert dep.alternative is None
        assert dep.version_constraint is None


class TestEdgeCases:
    """边界情况测试"""

    def test_empty_registry_check(self):
        from jk2bt.dependency_checker import (
            check_dependencies,
        )

        with patch(
            "src.dependency_checker.DEPENDENCY_REGISTRY",
            {},
        ):
            results = check_dependencies(verbose=False)
            assert results == {}

    def test_check_with_import_error_variants(self):
        from jk2bt.dependency_checker import (
            check_single_dependency,
            DependencyInfo,
            DependencyLevel,
        )

        dep = DependencyInfo(
            name="error_pkg",
            import_name="error_pkg",
            level=DependencyLevel.OPTIONAL,
            install_cmd="pip install error_pkg",
            description="测试导入错误的包",
        )

        with patch("builtins.__import__", side_effect=ImportError("mock error")):
            ok, error = check_single_dependency(dep)
            assert ok is False
            assert "mock error" in error

    def test_check_with_general_exception(self):
        from jk2bt.dependency_checker import (
            check_single_dependency,
            DependencyInfo,
            DependencyLevel,
        )

        dep = DependencyInfo(
            name="exception_pkg",
            import_name="exception_pkg",
            level=DependencyLevel.OPTIONAL,
            install_cmd="pip install exception_pkg",
            description="测试异常的包",
        )

        with patch("builtins.__import__", side_effect=RuntimeError("unexpected")):
            ok, error = check_single_dependency(dep)
            assert ok is False

    def test_module_without_version(self):
        from jk2bt.dependency_checker import (
            check_single_dependency,
            DEPENDENCY_REGISTRY,
        )

        ok, version = check_single_dependency(DEPENDENCY_REGISTRY["backtrader"])
        assert ok is True
        assert version is not None


class TestIntegrationWithRealEnvironment:
    """真实环境集成测试"""

    def test_pandas_version_check(self):
        from jk2bt.dependency_checker import (
            check_single_dependency,
            DEPENDENCY_REGISTRY,
        )

        ok, version = check_single_dependency(DEPENDENCY_REGISTRY["pandas"])
        if ok:
            import pandas

            assert version == pandas.__version__ or version == "unknown"

    def test_numpy_version_check(self):
        from jk2bt.dependency_checker import (
            check_single_dependency,
            DEPENDENCY_REGISTRY,
        )

        ok, version = check_single_dependency(DEPENDENCY_REGISTRY["numpy"])
        if ok:
            import numpy

            assert version == numpy.__version__ or version == "unknown"

    def test_akshare_version_check(self):
        from jk2bt.dependency_checker import (
            check_single_dependency,
            DEPENDENCY_REGISTRY,
        )

        ok, version = check_single_dependency(DEPENDENCY_REGISTRY["akshare"])
        if ok:
            import akshare

            assert version == akshare.__version__ or version == "unknown"

    def test_statsmodels_version_check(self):
        from jk2bt.dependency_checker import (
            check_single_dependency,
            DEPENDENCY_REGISTRY,
        )

        ok, version = check_single_dependency(DEPENDENCY_REGISTRY["statsmodels"])
        if ok:
            import statsmodels

            assert version == statsmodels.__version__ or version == "unknown"


class TestAllExportedFunctions:
    """测试所有导出函数"""

    def test_all_exports_exist(self):
        from jk2bt.dependency_checker import __all__

        expected_exports = [
            "DependencyLevel",
            "DependencyInfo",
            "DEPENDENCY_REGISTRY",
            "check_dependencies",
            "check_required_dependencies",
            "check_ml_dependencies",
            "get_install_recommendation",
            "startup_check",
            "import_with_check",
            "safe_import",
        ]

        for export in expected_exports:
            assert export in __all__

    def test_all_exports_callable(self):
        import jk2bt.dependency_checker as dc

        for name in dc.__all__:
            obj = getattr(dc, name)
            if (
                name.endswith("dependencies")
                or name.endswith("check")
                or name.endswith("recommendation")
            ):
                assert callable(obj)
