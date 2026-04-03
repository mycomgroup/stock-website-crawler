#!/usr/bin/env python3
"""
Task 14: 分钟策略实际运行测试
在项目根目录下运行，避免导入路径问题
"""

try:
    from jk2bt.core.runner import run_jq_strategy
except ImportError:
    print("请在仓库根目录运行此脚本")
    import sys

    sys.exit(1)


def main():
    print("Task 14: 分钟策略实际运行测试")
    print("=" * 60)

    test_cases = [
        ("jkcode/jkcode/94 小资金短线策略.txt", "1m数据"),
        ("jkcode/jkcode/89 2020年效果很好的策略-龙回头策略v3.0.txt", "1m过滤涨跌停"),
    ]

    results = []
    for filepath, desc in test_cases:
        print(f"\n测试: {filepath}")
        try:
            result = run_jq_strategy(
                strategy_file=filepath,
                start_date="2024-01-15",
                end_date="2024-01-18",
                initial_capital=100000,
                frequency="daily",
            )
            status = "成功" if result else "失败"
            print(f"  结果: {status}")
            results.append((filepath, status))
        except Exception as e:
            print(f"  异常: {str(e)[:100]}")
            results.append((filepath, "异常"))

    print("\n" + "=" * 60)
    print("测试总结:")
    for fp, st in results:
        print(f"  {fp}: {st}")


if __name__ == "__main__":
    main()
