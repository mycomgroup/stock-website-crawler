#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Task 18 验证测试脚本
验证批量运行结果真值化改进
"""

import os
import sys
import json
from datetime import datetime

# 添加项目根目录到路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from run_strategies_parallel import run_strategies_parallel, RunStatus


def test_validation():
    """测试验证样本"""

    strategy_dir = "jkcode/jkcode"

    test_strategies = [
        "01 龙回头3.0回测速度优化版.txt",
        "03 一个简单而持续稳定的懒人超额收益策略.txt",
        "04 高股息低市盈率高增长的价投策略.txt",
        "08 国九条后中小板微盘小改，年化135.40%.txt",
        "100 配套资料说明.txt",
    ]

    strategy_files = [
        os.path.join(strategy_dir, s)
        for s in test_strategies
        if os.path.exists(os.path.join(strategy_dir, s))
    ]

    print("=" * 80)
    print("Task 18 验证测试")
    print("=" * 80)
    print(f"测试策略数量: {len(strategy_files)}")
    print(f"测试策略:")
    for i, f in enumerate(strategy_files, 1):
        print(f"  {i}. {os.path.basename(f)}")
    print("=" * 80)

    summary = run_strategies_parallel(
        strategy_files=strategy_files,
        max_workers=2,
        timeout_per_strategy=60,
        start_date="2022-01-01",
        end_date="2022-03-31",
        initial_capital=100000,
        skip_scan=False,
    )

    print("\n" + "=" * 80)
    print("验证结果分析")
    print("=" * 80)

    results = summary.get("results", [])

    print(f"\n总策略数: {len(results)}")
    print(f"成功总数: {summary['summary']['success_total']}")
    print(f"失败总数: {summary['summary']['failed_total']}")
    print(f"可恢复失败: {summary['summary']['recoverable_failures']}")
    print(f"不可恢复失败: {summary['summary']['unrecoverable_failures']}")

    print("\n状态分类:")
    for status, count in summary["summary"]["status_counts"].items():
        print(f"  {status}: {count}")

    print("\n归因分析:")
    print("  可恢复:")
    for cause, count in summary["attribution_summary"]["recoverable"].items():
        if count > 0:
            print(f"    {cause}: {count}")
    print("  不可恢复:")
    for cause, count in summary["attribution_summary"]["unrecoverable"].items():
        if count > 0:
            print(f"    {cause}: {count}")

    print("\n详细结果（前5个）:")
    for i, r in enumerate(results[:5], 1):
        print(f"\n{i}. {r['strategy']}")
        print(f"  状态: {r['run_status']}")
        print(f"  成功: {r['success']}")
        print(f"  收益率: {r.get('pnl_pct', 0):.2f}%")

        evidence = r.get("evidence", {})
        print(f"  证据:")
        print(f"    - 已加载: {evidence.get('loaded', False)}")
        print(f"    - 进入回测循环: {evidence.get('entered_backtest_loop', False)}")
        print(f"    - 有交易: {evidence.get('has_transactions', False)}")
        print(f"    - 有净值序列: {evidence.get('has_nav_series', False)}")
        print(f"    - 净值长度: {evidence.get('nav_series_length', 0)}")

        attribution = r.get("attribution", {})
        if attribution.get("failure_root_cause"):
            print(f"  根本原因: {attribution['failure_root_cause']}")
        if attribution.get("error_category"):
            print(f"  错误类别: {attribution['error_category']}")
        if attribution.get("recoverable"):
            print(f"  可恢复: {attribution['recoverable']}")
        if attribution.get("recommendation"):
            print(f"  建议: {attribution['recommendation']}")

    print("\n" + "=" * 80)
    print("验证完成")
    print("=" * 80)

    log_dir = os.path.join("logs", "strategy_runs", summary["run_id"])
    print(f"\n结果已保存到:")
    print(f"  - summary.json: {log_dir}/summary.json")
    print(f"  - report.txt: {log_dir}/report.txt")
    print(f"  - scan_results.json: {log_dir}/scan_results.json")
    print(f"  - main.log: {log_dir}/main.log")

    return summary


if __name__ == "__main__":
    test_validation()
