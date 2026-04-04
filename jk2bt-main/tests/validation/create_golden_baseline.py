#!/usr/bin/env python3
"""
tests/validation/create_golden_baseline.py
创建金标基准脚本

用途：
1. 首次预热数据后，运行此脚本生成基准结果
2. 将基准值保存到golden_baseline.json
3. 后续CI运行时对比基准值进行验收

使用方法：
    # 1. 先预热数据
    python tools/offline_data/prewarm_daily.py --stocks 600519.XSHG 000858.XSHE --start 2023-01-01 --end 2023-12-31

    # 2. 生成基准
    python tests/validation/create_golden_baseline.py

    # 3. 验证基准
    pytest tests/validation/test_golden_benchmark.py -v

基准值说明：
- final_value: 最终资金（误差容忍5%）
- pnl_pct: 收益率（误差容忍10%绝对误差）

注意：
- 基准值依赖数据源和数据完整性
- 如果数据源变化，需要重新生成基准
- 基准文件不要提交到CI，每个环境独立维护
"""

import os
import sys
import json
import datetime
import time

_project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if _project_root not in sys.path:
    sys.path.insert(0, _project_root)

from jk2bt import run_jq_strategy


# 金标基准配置
GOLDEN_BENCHMARK_CONFIG = {
    "strategy_file": "strategies/validation_v4_double_ma.txt",
    "start_date": "2023-01-01",
    "end_date": "2023-12-31",
    "stock_pool": ["600519.XSHG", "000858.XSHE"],
    "initial_capital": 1000000,
}


def main():
    """创建金标基准"""

    print("=" * 80)
    print("金标基准生成脚本")
    print("=" * 80)

    # 检查策略文件
    strategy_file = GOLDEN_BENCHMARK_CONFIG["strategy_file"]
    if not strategy_file.startswith("strategies/"):
        strategy_file = os.path.join("strategies", strategy_file)

    full_path = os.path.join(_project_root, strategy_file)

    if not os.path.exists(full_path):
        print(f"错误: 策略文件不存在: {full_path}")
        print("请确保策略文件存在")
        return 1

    print(f"\n配置信息:")
    print(f"  策略文件: {strategy_file}")
    print(f"  日期区间: {GOLDEN_BENCHMARK_CONFIG['start_date']} ~ {GOLDEN_BENCHMARK_CONFIG['end_date']}")
    print(f"  股票池: {GOLDEN_BENCHMARK_CONFIG['stock_pool']}")
    print(f"  初始资金: {GOLDEN_BENCHMARK_CONFIG['initial_capital']}")

    # 提示预热
    print("\n提示: 如果数据未预热，运行可能较慢")
    print("建议运行: python tools/offline_data/prewarm_daily.py --stocks 600519.XSHG 000858.XSHE")

    # 运行策略
    print("\n运行策略...")
    start_time = time.time()

    try:
        result = run_jq_strategy(
            strategy_file=full_path,
            start_date=GOLDEN_BENCHMARK_CONFIG["start_date"],
            end_date=GOLDEN_BENCHMARK_CONFIG["end_date"],
            initial_capital=GOLDEN_BENCHMARK_CONFIG["initial_capital"],
            stock_pool=GOLDEN_BENCHMARK_CONFIG["stock_pool"],
            auto_discover_stocks=False,
        )
    except Exception as e:
        import traceback
        print(f"\n错误: 策略运行失败")
        print(f"  错误: {str(e)}")
        print(f"  Traceback:")
        traceback.print_exc()
        return 1

    run_time = time.time() - start_time

    if result is None:
        print("\n错误: 策略返回None")
        print("可能原因: 数据加载失败")
        return 1

    # 输出结果
    print("\n运行结果:")
    print(f"  运行时间: {run_time:.2f}秒")
    print(f"  最终资金: {result['final_value']:,.2f}")
    print(f"  收益率: {result['pnl_pct']:.2f}%")

    # 检查数据有效性
    if result['final_value'] <= 0:
        print("\n警告: 最终资金<=0，数据可能有问题")
        return 1

    if abs(result['pnl_pct']) > 100:
        print("\n警告: 收益率异常（>{100}%），数据可能有问题")

    # 检查运行时错误
    runtime_errors = result.get('runtime_errors', [])
    if runtime_errors:
        print(f"\n警告: 策略存在 {len(runtime_errors)} 个运行时错误:")
        for err in runtime_errors[:5]:
            print(f"  - {err.get('function', 'unknown')}: {err.get('error_type', 'unknown')} - {err.get('error', '')[:50]}")
        if len(runtime_errors) > 5:
            print(f"  ... 还有 {len(runtime_errors) - 5} 个错误")
        print("\n警告: 基准包含运行时错误，建议修复后再保存基准!")
        # 仍然保存基准，但记录错误

    # 保存基准
    baseline_file = os.path.join(_project_root, "tests/validation/golden_baseline.json")

    baseline_data = {
        "strategy_file": GOLDEN_BENCHMARK_CONFIG["strategy_file"],
        "start_date": GOLDEN_BENCHMARK_CONFIG["start_date"],
        "end_date": GOLDEN_BENCHMARK_CONFIG["end_date"],
        "stock_pool": GOLDEN_BENCHMARK_CONFIG["stock_pool"],
        "initial_capital": GOLDEN_BENCHMARK_CONFIG["initial_capital"],
        "final_value": result['final_value'],
        "pnl_pct": result['pnl_pct'],
        "runtime_errors": runtime_errors,  # GATE-2: 记录运行时错误
        "run_time_seconds": run_time,
        "baseline_updated": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "run_environment": "local",
    }

    with open(baseline_file, "w", encoding="utf-8") as f:
        json.dump(baseline_data, f, indent=2, ensure_ascii=False)

    print(f"\n基准已保存至: {baseline_file}")
    print("=" * 80)

    # 提示下一步
    print("\n下一步:")
    print("  1. 验证基准: pytest tests/validation/test_golden_benchmark.py -v")
    print("  2. 运行CI验收: pytest tests/validation/ -v")

    return 0


if __name__ == "__main__":
    sys.exit(main())