"""
run_tests.py
测试运行脚本。

运行所有测试或特定测试模块。
"""

import os
import sys
import argparse


def run_all_tests():
    """运行所有测试。"""
    import pytest

    test_dir = os.path.join(os.path.dirname(__file__), "tests")

    return pytest.main(
        [
            test_dir,
            "-v",
            "--tb=short",
            "--warnings-ignore",
        ]
    )


def run_factor_tests():
    """运行因子计算测试。"""
    import pytest

    test_file = os.path.join(
        os.path.dirname(__file__), "tests", "test_factor_formula.py"
    )

    return pytest.main(
        [
            test_file,
            "-v",
            "--tb=short",
        ]
    )


def run_api_tests():
    """运行接口兼容性测试。"""
    import pytest

    test_file = os.path.join(
        os.path.dirname(__file__), "tests", "test_api_compatibility.py"
    )

    return pytest.main(
        [
            test_file,
            "-v",
            "--tb=short",
        ]
    )


def run_comparison_tests():
    """运行回测对比测试。"""
    import pytest

    test_file = os.path.join(
        os.path.dirname(__file__), "tests", "test_backtest_comparison.py"
    )

    return pytest.main(
        [
            test_file,
            "-v",
            "--tb=short",
        ]
    )


def run_existing_tests():
    """运行原有测试文件。"""
    import pytest

    base_dir = os.path.dirname(__file__)

    test_files = [
        os.path.join(base_dir, "test_jqdata_api.py"),
        os.path.join(base_dir, "test_factors.py"),
    ]

    return pytest.main(
        [
            *test_files,
            "-v",
            "--tb=short",
        ]
    )


def main():
    parser = argparse.ArgumentParser(description="运行测试验证体系")
    parser.add_argument("--all", action="store_true", help="运行所有测试")
    parser.add_argument("--factor", action="store_true", help="运行因子计算测试")
    parser.add_argument("--api", action="store_true", help="运行接口兼容性测试")
    parser.add_argument("--comparison", action="store_true", help="运行回测对比测试")
    parser.add_argument("--existing", action="store_true", help="运行原有测试")
    parser.add_argument("--module", type=str, help="运行指定测试模块")

    args = parser.parse_args()

    if args.all:
        return run_all_tests()
    elif args.factor:
        return run_factor_tests()
    elif args.api:
        return run_api_tests()
    elif args.comparison:
        return run_comparison_tests()
    elif args.existing:
        return run_existing_tests()
    elif args.module:
        import pytest

        return pytest.main([args.module, "-v", "--tb=short"])
    else:
        parser.print_help()
        return 0


if __name__ == "__main__":
    sys.exit(main())
