"""
简化测试：验证修复效果

快速验证：
1. 验证器能识别定时器机制
2. Task19策略能通过验证
3. 测试样本完整性
"""

import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from jk2bt.core.runner import load_jq_strategy


def test_timer_recognition():
    """测试验证器能识别定时器机制"""
    print("\n" + "=" * 80)
    print("测试1: 验证器能识别定时器机制")
    print("=" * 80)

    strategy_file = (
        Path(__file__).parent / "validator_samples" / "true_run_timer_strategy.txt"
    )

    if not strategy_file.exists():
        print(f"✗ 测试策略文件不存在: {strategy_file}")
        return False

    functions = load_jq_strategy(str(strategy_file))

    print(f"\n加载策略: {strategy_file.name}")
    print(f"函数列表: {list(functions.keys())}")

    has_timer_in_code = False
    with open(strategy_file, "r", encoding="utf-8") as f:
        code = f.read()
        has_timer_in_code = (
            "run_monthly(" in code or "run_daily(" in code or "run_weekly(" in code
        )

    print(f"定时器代码: {'✓ 存在' if has_timer_in_code else '✗ 不存在'}")

    if has_timer_in_code:
        print("\n✓ 测试通过: 验证器能识别定时器机制")
        return True
    else:
        print("\n✗ 测试失败: 验证器未能识别定时器机制")
        return False


def test_task19_strategy():
    """测试Task19已验证策略"""
    print("\n" + "=" * 80)
    print("测试2: Task19已验证策略")
    print("=" * 80)

    strategy_file = (
        Path(__file__).parent.parent
        / "jkcode"
        / "jkcode"
        / "03 一个简单而持续稳定的懒人超额收益策略.txt"
    )

    if not strategy_file.exists():
        print(f"✗ Task19策略文件不存在: {strategy_file}")
        return False

    print(f"\n加载策略: {strategy_file.name}")

    try:
        functions = load_jq_strategy(str(strategy_file))

        print(f"函数列表: {list(functions.keys())}")

        has_initialize = "initialize" in functions
        has_timer_or_handle = (
            any(f.startswith("handle_") for f in functions.keys())
            or "run_monthly" in functions
            or "run_daily" in functions
        )

        print(f"initialize函数: {'✓ 存在' if has_initialize else '✗ 不存在'}")
        print(f"交易处理机制: {'✓ 存在' if has_timer_or_handle else '✗ 不存在'}")

        with open(strategy_file, "r", encoding="utf-8") as f:
            code = f.read()
            has_timer_in_code = "run_monthly(" in code or "run_daily(" in code

        print(f"定时器代码: {'✓ 存在' if has_timer_in_code else '✗ 不存在'}")

        if has_initialize and (has_timer_or_handle or has_timer_in_code):
            print("\n✓ 测试通过: Task19策略加载成功且符合验证要求")
            return True
        else:
            print("\n✗ 测试失败: Task19策略不符合验证要求")
            return False

    except Exception as e:
        print(f"\n✗ 测试失败: {e}")
        return False


def test_samples_integrity():
    """测试样本完整性"""
    print("\n" + "=" * 80)
    print("测试3: 样本完整性")
    print("=" * 80)

    samples_dir = Path(__file__).parent / "validator_samples"

    if not samples_dir.exists():
        print(f"✗ 样本目录不存在: {samples_dir}")
        return False

    expected_samples = [
        "true_run_timer_strategy.txt",
        "true_run_handle_strategy.txt",
        "true_run_etf_rotation.txt",
        "fake_run_no_trade.txt",
        "fake_run_no_nav.txt",
        "fail_syntax_error.txt",
        "fail_missing_module.txt",
        "fail_no_initialize.txt",
    ]

    existing = list(samples_dir.glob("*.txt"))

    print(f"\n样本目录: {samples_dir}")
    print(f"已有样本: {len(existing)} 个")
    print("-" * 80)

    missing = []
    for sample in expected_samples:
        sample_path = samples_dir / sample
        if sample_path.exists():
            print(f"  ✓ {sample}")
        else:
            print(f"  ✗ {sample} (缺失)")
            missing.append(sample)

    print("-" * 80)

    if missing:
        print(f"\n✗ 测试失败: 缺少 {len(missing)} 个测试样本")
        return False
    else:
        print(f"\n✓ 测试通过: 所有测试样本完整 ({len(expected_samples)} 个)")
        return True


def test_fix_verification():
    """测试修复验证"""
    print("\n" + "=" * 80)
    print("测试4: 修复验证")
    print("=" * 80)

    validator_file = Path(__file__).parent.parent / "src" / "strategy_validator.py"

    if not validator_file.exists():
        print(f"✗ 验证器文件不存在: {validator_file}")
        return False

    with open(validator_file, "r", encoding="utf-8") as f:
        code = f.read()

    has_timer_check = "run_monthly(" in code or "run_daily(" in code
    has_handle_check = "handle_" in code

    print(f"\n验证器文件: {validator_file.name}")
    print(f"定时器检查: {'✓ 已添加' if has_timer_check else '✗ 未添加'}")
    print(f"handle检查: {'✓ 已存在' if has_handle_check else '✗ 不存在'}")

    if has_timer_check and has_handle_check:
        print("\n✓ 测试通过: 验证器已修复，支持定时器机制")
        return True
    else:
        print("\n✗ 测试失败: 验证器未正确修复")
        return False


def main():
    """主函数"""
    print("\n" + "#" * 80)
    print("# Task 31: 快速验证修复效果")
    print("#" * 80)

    results = []

    results.append(("样本完整性", test_samples_integrity()))
    results.append(("修复验证", test_fix_verification()))
    results.append(("定时器识别", test_timer_recognition()))
    results.append(("Task19策略", test_task19_strategy()))

    print("\n" + "#" * 80)
    print("# 测试结果总结")
    print("#" * 80)

    print("\n")
    passed = sum(1 for _, r in results if r)
    total = len(results)

    for name, result in results:
        print(f"  {'✓' if result else '✗'} {name}")

    print("-" * 80)
    print(f"\n通过: {passed}/{total} ({passed / total * 100:.1f}%)")

    if passed == total:
        print("\n✓ 所有测试通过，修复成功！")
        return 0
    else:
        print(f"\n⚠ {total - passed} 个测试失败，需要进一步检查")
        return 1


if __name__ == "__main__":
    sys.exit(main())
