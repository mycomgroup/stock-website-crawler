"""
策略回放正确性验证器（使用包导入）
"""

import os
import sys
import json
import pandas as pd
import numpy as np
from datetime import datetime
from typing import Dict, List

try:
    jk2bt..core.runner as runner

    load_jq_strategy = runner.load_jq_strategy
    run_jq_strategy = runner.run_jq_strategy
    print("✓ 成功导入src包")
except ImportError as e:
    print(f"导入失败: {e}")
    sys.exit(1)


def validate_strategy_simple(
    strategy_file: str, start_date: str = "2022-01-01", end_date: str = "2022-03-31"
):
    """简单验证策略"""

    print(f"\n{'=' * 60}")
    print(f"验证策略: {os.path.basename(strategy_file)}")
    print(f"{'=' * 60}")

    result = {
        "strategy_file": strategy_file,
        "strategy_name": os.path.basename(strategy_file),
        "timestamp": datetime.now().isoformat(),
    }

    try:
        functions, source = load_jq_strategy(strategy_file)
        result["load_success"] = True
        result["functions"] = list(functions.keys()) if functions else []
        print(f"[1] 加载成功，发现函数: {result['functions']}")
    except Exception as e:
        result["load_success"] = False
        result["load_error"] = str(e)
        print(f"[1] 加载失败: {e}")
        return result

    if not functions:
        print("[1] 未定义任何函数")
        return result

    try:
        print(f"\n[2] 开始运行回测 ({start_date} ~ {end_date})...")

        run_result = run_jq_strategy(
            strategy_file,
            start_date=start_date,
            end_date=end_date,
            initial_capital=100000,
            auto_discover_stocks=True,
        )

        if run_result is None:
            result["run_success"] = False
            result["run_error"] = "run_jq_strategy返回None"
            print(f"[2] 运行失败: {result['run_error']}")
            return result

        result["run_success"] = True
        result["final_value"] = run_result.get("final_value", 0)
        result["pnl"] = run_result.get("pnl", 0)
        result["pnl_pct"] = run_result.get("pnl_pct", 0)

        print(f"[2] 运行成功")
        print(f"    最终资金: {result['final_value']:,.2f}")
        print(f"    盈亏: {result['pnl']:,.2f} ({result['pnl_pct']:.2f}%)")

        # 检查策略是否有实际运行（通过最终资金判断）
        has_change = result["final_value"] != 100000

        # 判定真跑通：资金有变化
        result["is_really_running"] = has_change

        print(f"\n[3] 验证结果:")
        print(f"    资金变化: {has_change}")
        print(f"    真跑通判定: {result['is_really_running']}")

    except Exception as e:
        import traceback

        result["run_success"] = False
        result["run_error"] = f"{str(e)}"
        print(f"[2] 运行异常: {e}")

    return result


def main():
    """主函数"""

    strategy_files = [
        "jkcode/jkcode/03 一个简单而持续稳定的懒人超额收益策略.txt",
        "jkcode/jkcode/04 红利搬砖_简化测试版.txt",
    ]

    print(f"\n{'#' * 60}")
    print(f"策略回放正确性验证（使用包导入）")
    print(f"{'#' * 60}\n")

    results = []
    for strategy_file in strategy_files:
        if os.path.exists(strategy_file):
            result = validate_strategy_simple(strategy_file)
            results.append(result)
        else:
            print(f"\n策略文件不存在: {strategy_file}")

    print(f"\n{'#' * 60}")
    print(f"验证总结")
    print(f"{'#' * 60}\n")

    for r in results:
        status = "真跑通" if r.get("is_really_running") else "假跑通/失败"
        load = "✓" if r.get("load_success") else "✗"
        run = "✓" if r.get("run_success") else "✗"
        pnl = r.get("pnl_pct", 0)

        print(f"{r['strategy_name'][:40]}")
        print(f"  加载:{load} 运行:{run} 盈亏:{pnl:.2f}%")
        print(f"  状态: {status}")

    really_running = [r for r in results if r.get("is_really_running")]
    print(f"\n真跑通策略: {len(really_running)}/{len(results)}")

    output_file = "docs/0330_result/task19_validation_result.json"
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(
            {"validation_time": datetime.now().isoformat(), "results": results},
            f,
            ensure_ascii=False,
            indent=2,
        )

    print(f"\n结果已保存: {output_file}")


if __name__ == "__main__":
    main()
