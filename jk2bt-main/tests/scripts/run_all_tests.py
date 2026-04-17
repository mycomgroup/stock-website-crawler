#!/usr/bin/env python
"""
run_all_tests.py
统一测试运行脚本

功能：
1. 运行所有测试并生成报告
2. 支持分类运行（finance/market/integration）
3. 支持失败重试
"""

import subprocess
import sys
from pathlib import Path

BASE_DIR = Path(__file__).parent
TEST_DIR = BASE_DIR / "tests"

# 测试分类
TEST_CATEGORIES = {
    "finance": [
        "test_company_info_api.py",
        "test_shareholder_api.py",
        "test_dividend_api.py",
        "test_share_change_api.py",
        "test_unlock_api.py",
        "test_macro_api.py",
    ],
    "market": [
        "test_index_components_api.py",
        "test_industry_sw_api.py",
        "test_conversion_bond_api.py",
        "test_option_api.py",
        "test_futures_api.py",
        "test_money_flow.py",
    ],
    "integration": [
        "test_finance_query.py",
        "test_jqdata_api.py",
        "test_api_compatibility.py",
    ],
}


def run_tests(test_files, verbose=True):
    """运行指定测试文件"""
    results = {"passed": 0, "failed": 0, "errors": 0, "total": 0}

    for test_file in test_files:
        test_path = TEST_DIR / test_file
        if not test_path.exists():
            print(f"⚠️  测试文件不存在: {test_file}")
            continue

        cmd = [
            sys.executable,
            "-m",
            "pytest",
            str(test_path),
            "-v" if verbose else "-q",
            "--tb=short",
            "-x",  # 遇到第一个失败就停止
        ]

        print(f"\n{'=' * 60}")
        print(f"运行测试: {test_file}")
        print(f"{'=' * 60}")

        result = subprocess.run(cmd, capture_output=False)
        results["total"] += 1

        if result.returncode == 0:
            results["passed"] += 1
            print(f"✅ {test_file} 通过")
        else:
            results["failed"] += 1
            print(f"❌ {test_file} 失败")

    return results


def main():
    """主函数"""
    print("=" * 60)
    print("测试运行器")
    print("=" * 60)

    if len(sys.argv) > 1:
        category = sys.argv[1]
        if category in TEST_CATEGORIES:
            print(f"\n运行分类: {category}")
            test_files = TEST_CATEGORIES[category]
        else:
            print(f"未知分类: {category}")
            print(f"可用分类: {list(TEST_CATEGORIES.keys())}")
            return
    else:
        # 运行所有测试
        test_files = []
        for files in TEST_CATEGORIES.values():
            test_files.extend(files)

    results = run_tests(test_files)

    print("\n" + "=" * 60)
    print("测试结果汇总")
    print("=" * 60)
    print(f"总测试文件: {results['total']}")
    print(f"✅ 通过: {results['passed']}")
    print(f"❌ 失败: {results['failed']}")
    print(f"通过率: {results['passed'] / results['total'] * 100:.1f}%")


if __name__ == "__main__":
    main()
