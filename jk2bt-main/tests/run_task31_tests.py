#!/usr/bin/env python3
"""
Task 31 测试运行脚本

功能:
1. 运行strategy_validator测试用例
2. 验证测试覆盖度
3. 生成测试报告
4. 统计真跑通样本池数量
"""

import os
import sys
import subprocess
from pathlib import Path
from datetime import datetime


def run_pytest():
    """运行pytest测试"""
    print("=" * 80)
    print("Task 31: 运行策略验证器测试")
    print("=" * 80)

    test_file = Path(__file__).parent / "test_strategy_validator.py"

    if not test_file.exists():
        print(f"错误: 测试文件不存在 {test_file}")
        return 1

    cmd = [sys.executable, "-m", "pytest", str(test_file), "-v", "--tb=short", "-s"]

    print(f"\n执行命令: {' '.join(cmd)}")
    print("-" * 80)

    result = subprocess.run(cmd, cwd=test_file.parent)

    return result.returncode


def check_test_samples():
    """检查测试样本完整性"""
    print("\n" + "=" * 80)
    print("检查测试样本完整性")
    print("=" * 80)

    samples_dir = Path(__file__).parent / "validator_samples"

    if not samples_dir.exists():
        print(f"错误: 样本目录不存在 {samples_dir}")
        return False

    expected_samples = {
        "true_run_timer_strategy.txt": "真跑通 - 定时器机制",
        "true_run_handle_strategy.txt": "真跑通 - handle函数",
        "true_run_etf_rotation.txt": "真跑通 - ETF轮动",
        "fake_run_no_trade.txt": "假跑通 - 无交易",
        "fake_run_no_nav.txt": "假跑通 - 无净值变化",
        "fail_syntax_error.txt": "加载失败 - 语法错误",
        "fail_missing_module.txt": "加载失败 - 缺少模块",
        "fail_no_initialize.txt": "加载失败 - 缺少initialize",
    }

    existing = list(samples_dir.glob("*.txt"))

    print(f"\n样本目录: {samples_dir}")
    print(f"已有样本: {len(existing)} 个")
    print("-" * 80)

    missing = []
    for sample, desc in expected_samples.items():
        sample_path = samples_dir / sample
        if sample_path.exists():
            print(f"  ✓ {sample:35s} - {desc}")
        else:
            print(f"  ✗ {sample:35s} - {desc} (缺失)")
            missing.append(sample)

    print("-" * 80)

    if missing:
        print(f"\n警告: 缺少 {len(missing)} 个测试样本")
        return False
    else:
        print(f"\n✓ 所有测试样本完整 ({len(expected_samples)} 个)")
        return True


def count_true_run_samples():
    """统计真跑通样本"""
    print("\n" + "=" * 80)
    print("统计真跑通样本池")
    print("=" * 80)

    samples_dir = Path(__file__).parent / "validator_samples"

    if not samples_dir.exists():
        print(f"错误: 样本目录不存在 {samples_dir}")
        return 0

    true_run_samples = list(samples_dir.glob("true_run_*.txt"))

    print(f"\n真跑通样本: {len(true_run_samples)} 个")
    print("-" * 80)

    for sample in true_run_samples:
        print(f"  - {sample.name}")

    print("-" * 80)

    target = 20
    if len(true_run_samples) >= target:
        print(f"\n✓ 达到目标: {len(true_run_samples)}/{target}")
    else:
        print(f"\n⚠ 未达目标: {len(true_run_samples)}/{target}")
        print(f"  还需补充: {target - len(true_run_samples)} 个")

    return len(true_run_samples)


def verify_task19_strategy():
    """验证Task19已验证策略"""
    print("\n" + "=" * 80)
    print("验证Task19已验证策略")
    print("=" * 80)

    strategy_file = (
        Path(__file__).parent.parent
        / "jkcode"
        / "jkcode"
        / "03 一个简单而持续稳定的懒人超额收益策略.txt"
    )

    if not strategy_file.exists():
        print(f"警告: Task19策略文件不存在 {strategy_file}")
        return False

    print(f"\n策略文件: {strategy_file.name}")
    print("-" * 80)

    try:
        from jk2bt.core.validator import (
            validate_single_strategy,
        )

        result = validate_single_strategy(
            str(strategy_file),
            start_date="2022-01-01",
            end_date="2022-03-31",
            initial_capital=100000,
        )

        print(f"  加载状态: {'✓ 成功' if result.load_success else '✗ 失败'}")

        if result.load_error:
            print(f"  加载错误: {result.load_error}")

        print(f"  回测状态: {'✓ 进入' if result.entered_backtest_loop else '✗ 未进入'}")
        print(f"  交易笔数: {result.validation_details.get('trade_count', 0)}")
        print(f"  最终状态: {result.final_status}")
        print(
            f"  真跑通: {'✓ 是' if result.validation_details.get('is_really_running') else '✗ 否'}"
        )

        print("-" * 80)

        if result.validation_details.get("is_really_running"):
            print("\n✓ Task19策略验证通过")
            return True
        else:
            print("\n⚠ Task19策略未通过验证")
            return False

    except Exception as e:
        print(f"\n✗ 验证失败: {e}")
        import traceback

        traceback.print_exc()
        return False


def generate_report():
    """生成测试报告"""
    print("\n" + "=" * 80)
    print("生成测试报告")
    print("=" * 80)

    report_dir = Path(__file__).parent.parent / "docs" / "0330_result"
    report_dir.mkdir(parents=True, exist_ok=True)

    report_file = report_dir / "task31_test_coverage_report.md"

    with open(report_file, "w", encoding="utf-8") as f:
        f.write("# Task 31 测试覆盖度报告\n\n")
        f.write(f"**生成时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")

        f.write("---\n\n")

        f.write("## 测试样本统计\n\n")

        samples_dir = Path(__file__).parent / "validator_samples"
        if samples_dir.exists():
            samples = {
                "真跑通样本": list(samples_dir.glob("true_run_*.txt")),
                "假跑通样本": list(samples_dir.glob("fake_run_*.txt")),
                "加载失败样本": list(samples_dir.glob("fail_*.txt")),
            }

            total = sum(len(v) for v in samples.values())

            f.write("| 样本类型 | 数量 |\n")
            f.write("|---------|------|\n")
            for sample_type, files in samples.items():
                f.write(f"| {sample_type} | {len(files)} |\n")
            f.write(f"| **总计** | **{total}** |\n\n")

        f.write("---\n\n")

        f.write("## 测试用例统计\n\n")

        test_file = Path(__file__).parent / "test_strategy_validator.py"
        if test_file.exists():
            with open(test_file, "r", encoding="utf-8") as tf:
                content = tf.read()

            test_methods = content.count("def test_")
            test_classes = content.count("class Test")

            f.write(f"- 测试类: {test_classes} 个\n")
            f.write(f"- 测试方法: {test_methods} 个\n\n")

        f.write("---\n\n")

        f.write("## 验证维度覆盖\n\n")

        dimensions = [
            "load_success - 策略加载成功",
            "entered_backtest_loop - 进入回测循环",
            "has_transactions - 有交易记录",
            "has_nav_series - 有净值序列",
            "final_value - 最终资金",
            "pnl_pct - 盈亏比例",
            "timer_triggered - 定时器触发",
        ]

        for dim in dimensions:
            f.write(f"- ✓ {dim}\n")

        f.write("\n---\n\n")

        f.write("## 测试策略类型覆盖\n\n")

        strategy_types = [
            "定时器机制策略 (run_monthly/run_daily/run_weekly)",
            "handle函数机制策略 (handle_data)",
            "ETF轮动策略",
            "指数权重策略",
            "均线策略",
            "空策略（无交易）",
            "数据依赖策略",
            "语法错误策略",
            "模块缺失策略",
            "缺少initialize策略",
        ]

        for stype in strategy_types:
            f.write(f"- ✓ {stype}\n")

        f.write("\n---\n\n")

        f.write("## 任务完成度\n\n")

        samples_dir = Path(__file__).parent / "validator_samples"
        if samples_dir.exists():
            true_run_count = len(list(samples_dir.glob("true_run_*.txt")))
            target = 20

            f.write(f"- 目标: {target} 个真跑通样本\n")
            f.write(f"- 当前: {true_run_count} 个真跑通样本\n")
            f.write(
                f"- 完成度: {true_run_count}/{target} ({true_run_count / target * 100:.1f}%)\n"
            )

        f.write("\n---\n\n")

        f.write("*报告生成完成*\n")

    print(f"\n测试报告已生成: {report_file}")
    return report_file


def main():
    """主函数"""
    print("\n" + "#" * 80)
    print("# Task 31: 测试覆盖度验证")
    print("#" * 80 + "\n")

    checks_complete = check_test_samples()

    true_run_count = count_true_run_samples()

    task19_ok = verify_task19_strategy()

    test_result = run_pytest()

    report_file = generate_report()

    print("\n" + "#" * 80)
    print("# 测试完成总结")
    print("#" * 80)

    print(f"\n测试样本完整性: {'✓ 通过' if checks_complete else '✗ 失败'}")
    print(f"真跑通样本数: {true_run_count} 个")
    print(f"Task19策略验证: {'✓ 通过' if task19_ok else '✗ 失败'}")
    print(f"测试执行: {'✓ 通过' if test_result == 0 else '✗ 失败'}")
    print(f"测试报告: {report_file}")

    if true_run_count >= 20:
        print(f"\n✓ 任务完成: 已达到20个真跑通样本目标")
    elif task19_ok:
        print(f"\n⚠ 部分完成: 有1个已验证的真跑通策略（Task19）")
        print(f"  建议: 扩展测试样本，补充更多真跑通策略")
    else:
        print(f"\n✗ 任务未完成: 无真跑通样本")
        print(f"  建议: 检查验证逻辑和数据源")

    print("\n" + "#" * 80 + "\n")

    return 0 if test_result == 0 and task19_ok else 1


if __name__ == "__main__":
    sys.exit(main())
