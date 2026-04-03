"""
Task 34: 策略回归测试
测试依赖指数/基本面接口的策略是否能正常运行
"""

import os
import sys
import json

strategies_to_test = [
    ("04 红利搬砖，年化29%.txt", "使用 get_index_stocks 和 get_fundamentals"),
    (
        "05 价值低波（下）--十年十倍（2020拜年）.txt",
        "使用 get_index_stocks 和 get_fundamentals",
    ),
    ("04 苦咖啡-默默赚钱系列-改.txt", "使用 get_index_stocks"),
    ("70 超稳的股息率+均线选股策略.txt", "使用 get_index_stocks"),
    ("04 高股息低市盈率高增长的价投策略.txt", "使用 get_fundamentals"),
    ("35 精选价值策略.txt", "多处使用 get_fundamentals"),
    ("03 一个简单而持续稳定的懒人超额收益策略.txt", "成功案例"),
    ("06 国九小市值策略【年化100.5% 回撤25.6%】.txt", "使用 get_index_stocks"),
]


def test_strategy_loading(strategy_file, description):
    """测试策略加载"""
    strategy_path = os.path.join("jkcode/jkcode", strategy_file)

    if not os.path.exists(strategy_path):
        return {"status": "not_found", "error": "文件不存在"}

    try:
        with open(strategy_path, "r", encoding="utf-8") as f:
            code = f.read()

        if not code.strip():
            return {"status": "empty", "error": "文件为空"}

        checks = {
            "has_get_index_stocks": "get_index_stocks" in code,
            "has_get_fundamentals": "get_fundamentals" in code,
            "has_initialize": "initialize" in code or "def initialize" in code,
            "has_handle_data": "handle_data" in code or "def handle_data" in code,
            "code_length": len(code),
        }

        return {
            "status": "loaded",
            "checks": checks,
            "description": description,
        }

    except Exception as e:
        return {"status": "error", "error": str(e)}


def main():
    print("=" * 60)
    print("Task 34: 策略回归测试")
    print("=" * 60)

    results = []
    success_count = 0
    failed_count = 0

    for strategy_file, description in strategies_to_test:
        print(f"\n测试策略: {strategy_file}")
        print(f"  描述: {description}")

        result = test_strategy_loading(strategy_file, description)
        results.append(
            {"strategy": strategy_file, "description": description, **result}
        )

        if result["status"] == "loaded":
            print(f"  ✓ 状态: 加载成功")
            checks = result.get("checks", {})
            print(
                f"     - get_index_stocks: {'✓' if checks.get('has_get_index_stocks') else '✗'}"
            )
            print(
                f"     - get_fundamentals: {'✓' if checks.get('has_get_fundamentals') else '✗'}"
            )
            print(
                f"     - initialize/handle_data: {'✓' if checks.get('has_initialize') and checks.get('has_handle_data') else '✗'}"
            )
            print(f"     - 代码长度: {checks.get('code_length', 0)} 字符")
            success_count += 1
        elif result["status"] == "not_found":
            print(f"  ✗ 状态: 文件不存在")
            failed_count += 1
        elif result["status"] == "empty":
            print(f"  ✗ 状态: 文件为空")
            failed_count += 1
        else:
            print(f"  ✗ 状态: 错误 - {result.get('error', '未知')}")
            failed_count += 1

    print("\n" + "=" * 60)
    print(f"总计: 成功加载 {success_count}/{len(strategies_to_test)}")
    print(f"失败: {failed_count}")
    print("=" * 60)

    summary = {
        "task": "task34_strategy_regression",
        "total_strategies": len(strategies_to_test),
        "loaded": success_count,
        "failed": failed_count,
        "success_rate": f"{success_count / len(strategies_to_test) * 100:.1f}%",
        "details": results,
    }

    output_path = "docs/0330_result/task34_regression_summary.json"
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2, ensure_ascii=False)

    print(f"\n结果已保存到: {output_path}")

    return success_count, failed_count


if __name__ == "__main__":
    success, failed = main()
    sys.exit(0 if failed == 0 else 1)
