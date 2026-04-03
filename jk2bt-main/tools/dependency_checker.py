"""
dependency_checker.py
依赖检查脚本，在启动策略前自检依赖完整性。

使用方法:
    python -m src.dependency_checker
    或
    from jk2bt.dependency_checker import check_dependencies, check_ml_dependencies
"""

import sys
import warnings
from typing import Dict, List, Tuple, Optional, Any
from dataclasses import dataclass
from enum import Enum


class DependencyLevel(Enum):
    REQUIRED = "required"
    OPTIONAL = "optional"
    ML_ADVANCED = "ml_advanced"
    NOT_SUPPORTED = "not_supported"


@dataclass
class DependencyInfo:
    name: str
    import_name: str
    level: DependencyLevel
    install_cmd: str
    description: str
    alternative: Optional[str] = None
    version_constraint: Optional[str] = None


DEPENDENCY_REGISTRY: Dict[str, DependencyInfo] = {
    "pandas": DependencyInfo(
        name="pandas",
        import_name="pandas",
        level=DependencyLevel.REQUIRED,
        install_cmd="pip install pandas>=2.0",
        description="核心数据处理库",
        version_constraint=">=2.0",
    ),
    "numpy": DependencyInfo(
        name="numpy",
        import_name="numpy",
        level=DependencyLevel.REQUIRED,
        install_cmd="pip install numpy>=1.24",
        description="数值计算基础库",
        version_constraint=">=1.24",
    ),
    "akshare": DependencyInfo(
        name="akshare",
        import_name="akshare",
        level=DependencyLevel.REQUIRED,
        install_cmd="pip install akshare>=1.10",
        description="A股数据获取接口",
        version_constraint=">=1.10",
    ),
    "backtrader": DependencyInfo(
        name="backtrader",
        import_name="backtrader",
        level=DependencyLevel.REQUIRED,
        install_cmd="pip install backtrader==1.9.78.123",
        description="回测框架",
        version_constraint="==1.9.78.123",
    ),
    "statsmodels": DependencyInfo(
        name="statsmodels",
        import_name="statsmodels",
        level=DependencyLevel.REQUIRED,
        install_cmd="pip install statsmodels>=0.14",
        description="统计建模（RSRS等因子依赖）",
        version_constraint=">=0.14",
    ),
    "matplotlib": DependencyInfo(
        name="matplotlib",
        import_name="matplotlib",
        level=DependencyLevel.OPTIONAL,
        install_cmd="pip install matplotlib>=3.7",
        description="可视化绘图",
        alternative="策略运行不依赖绘图",
        version_constraint=">=3.7",
    ),
    "duckdb": DependencyInfo(
        name="duckdb",
        import_name="duckdb",
        level=DependencyLevel.OPTIONAL,
        install_cmd="pip install duckdb",
        description="分钟数据本地缓存",
        alternative="可跳过，分钟数据将使用akshare实时获取",
    ),
    "pytest": DependencyInfo(
        name="pytest",
        import_name="pytest",
        level=DependencyLevel.OPTIONAL,
        install_cmd="pip install pytest>=7.0",
        description="测试框架",
        alternative="仅开发/测试需要",
        version_constraint=">=7.0",
    ),
    "qlib": DependencyInfo(
        name="qlib",
        import_name="qlib",
        level=DependencyLevel.ML_ADVANCED,
        install_cmd="pip install pyqlib>=0.9",
        description="微软量化因子库（Alpha101/191）",
        alternative="仅使用 qlib_alpha 因子时需要",
        version_constraint=">=0.9",
    ),
    "sklearn": DependencyInfo(
        name="sklearn",
        import_name="sklearn",
        level=DependencyLevel.ML_ADVANCED,
        install_cmd="pip install scikit-learn",
        description="机器学习基础库",
        alternative="仅机器学习策略需要",
    ),
    "xgboost": DependencyInfo(
        name="xgboost",
        import_name="xgboost",
        level=DependencyLevel.ML_ADVANCED,
        install_cmd="pip install xgboost",
        description="梯度提升树",
        alternative="仅XGBoost策略需要",
    ),
    "lightgbm": DependencyInfo(
        name="lightgbm",
        import_name="lightgbm",
        level=DependencyLevel.ML_ADVANCED,
        install_cmd="pip install lightgbm",
        description="轻量梯度提升",
        alternative="仅LightGBM策略需要",
    ),
    "talib": DependencyInfo(
        name="talib",
        import_name="talib",
        level=DependencyLevel.ML_ADVANCED,
        install_cmd="pip install TA-Lib (需先安装底层库)",
        description="技术指标库",
        alternative="可降级用 pandas/numpy 手动计算",
    ),
    "torch": DependencyInfo(
        name="torch",
        import_name="torch",
        level=DependencyLevel.NOT_SUPPORTED,
        install_cmd="pip install torch",
        description="深度学习框架",
        alternative="当前项目未使用，不建议安装",
    ),
    "tensorflow": DependencyInfo(
        name="tensorflow",
        import_name="tensorflow",
        level=DependencyLevel.NOT_SUPPORTED,
        install_cmd="pip install tensorflow",
        description="深度学习框架",
        alternative="当前项目未使用，不建议安装",
    ),
}


def check_single_dependency(dep_info: DependencyInfo) -> Tuple[bool, Optional[str]]:
    try:
        mod = __import__(dep_info.import_name)
        return True, getattr(mod, "__version__", "unknown")
    except ImportError as e:
        return False, str(e)
    except Exception as e:
        return False, str(e)


def check_dependencies(
    level: Optional[DependencyLevel] = None,
    verbose: bool = True,
) -> Dict[str, Tuple[bool, Optional[str]]]:
    results = {}

    for name, dep_info in DEPENDENCY_REGISTRY.items():
        if level and dep_info.level != level:
            continue

        available, version_or_error = check_single_dependency(dep_info)
        results[name] = (available, version_or_error)

        if verbose:
            status = "OK" if available else "MISSING"
            level_str = dep_info.level.value
            if available:
                print(f"[{level_str}] {name}: {status} (v{version_or_error})")
            else:
                print(f"[{level_str}] {name}: {status}")
                if dep_info.alternative:
                    print(f"    -> 替代方案: {dep_info.alternative}")
                print(f"    -> 安装命令: {dep_info.install_cmd}")

    return results


def check_required_dependencies() -> bool:
    results = check_dependencies(level=DependencyLevel.REQUIRED, verbose=False)
    missing = [name for name, (ok, _) in results.items() if not ok]

    if missing:
        print("=" * 60)
        print("缺少核心依赖，策略无法运行:")
        for name in missing:
            dep = DEPENDENCY_REGISTRY[name]
            print(f"  - {name}: {dep.install_cmd}")
        print("=" * 60)
        return False

    return True


def check_ml_dependencies(
    verbose: bool = True,
) -> Dict[str, Tuple[bool, Optional[str]]]:
    ml_deps = [DependencyLevel.ML_ADVANCED, DependencyLevel.OPTIONAL]
    results = {}

    for level in ml_deps:
        level_results = check_dependencies(level=level, verbose=verbose)
        results.update(level_results)

    return results


def get_install_recommendation(use_case: str = "basic") -> List[str]:
    if use_case == "basic":
        return [
            dep.install_cmd
            for dep in DEPENDENCY_REGISTRY.values()
            if dep.level == DependencyLevel.REQUIRED
        ]
    elif use_case == "full":
        return [
            dep.install_cmd
            for dep in DEPENDENCY_REGISTRY.values()
            if dep.level in [DependencyLevel.REQUIRED, DependencyLevel.OPTIONAL]
        ]
    elif use_case == "ml":
        return [
            dep.install_cmd
            for dep in DEPENDENCY_REGISTRY.values()
            if dep.level
            in [
                DependencyLevel.REQUIRED,
                DependencyLevel.OPTIONAL,
                DependencyLevel.ML_ADVANCED,
            ]
        ]
    elif use_case == "qlib":
        return [
            dep.install_cmd
            for dep in DEPENDENCY_REGISTRY.values()
            if dep.name in ["pandas", "numpy", "akshare", "qlib"]
        ]
    return []


def startup_check() -> bool:
    print("=" * 60)
    print("src 依赖自检")
    print("=" * 60)

    required_ok = check_required_dependencies()
    if not required_ok:
        return False

    check_ml_dependencies(verbose=True)

    print("\n依赖检查完成")
    if required_ok:
        print("核心依赖齐全，策略可正常运行")
    print("=" * 60)

    return True


def import_with_check(module_name: str, required: bool = False) -> Optional[Any]:
    dep = DEPENDENCY_REGISTRY.get(module_name)

    if dep is None:
        dep = DependencyInfo(
            name=module_name,
            import_name=module_name,
            level=DependencyLevel.OPTIONAL
            if not required
            else DependencyLevel.REQUIRED,
            install_cmd=f"pip install {module_name}",
            description=f"未知模块: {module_name}",
        )

    try:
        return __import__(module_name)
    except ImportError:
        if required:
            raise ImportError(
                f"缺少必装依赖 {module_name}，请运行: {dep.install_cmd}\n"
                f"说明: {dep.description}"
            )
        else:
            warnings.warn(
                f"可选依赖 {module_name} 未安装，部分功能将受限\n"
                f"安装命令: {dep.install_cmd}\n"
                f"替代方案: {dep.alternative or '无'}"
            )
            return None


def safe_import(module_name: str, fallback: Optional[str] = None) -> Optional[Any]:
    try:
        return __import__(module_name)
    except ImportError:
        if fallback:
            try:
                return __import__(fallback)
            except ImportError:
                pass
        return None


__all__ = [
    "DependencyLevel",
    "DependencyInfo",
    "DEPENDENCY_REGISTRY",
    "check_single_dependency",
    "check_dependencies",
    "check_required_dependencies",
    "check_ml_dependencies",
    "get_install_recommendation",
    "startup_check",
    "import_with_check",
    "safe_import",
]


if __name__ == "__main__":
    success = startup_check()
    sys.exit(0 if success else 1)