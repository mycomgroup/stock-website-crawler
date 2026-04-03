#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
测试运行10个聚宽策略txt文件
"""

import os

try:
    from jk2bt.core.runner import run_jq_strategy
except ImportError:
    print("请在仓库根目录运行此脚本")
    import sys

    sys.exit(1)

strategies = [
    "jkcode/jkcode/01 7年40倍模拟超过两年年化高回撤低.txt",
    "jkcode/jkcode/01 wywy1995大侠的小市值AI因子选股 5组参数50股.txt",
    "jkcode/jkcode/01 一颗耀眼的星—【回顾2】小市值成长股策略更新—改.txt",
    "jkcode/jkcode/01 首板低开策略.txt",
    "jkcode/jkcode/01 龙回头3.0回测速度优化版.txt",
    "jkcode/jkcode/02 7年40倍绩优低价超跌缩量小盘 扩容到50只.txt",
    "jkcode/jkcode/02 ETF动量轮动RSRS择时-魔改3小优化.txt",
    "jkcode/jkcode/02 连板龙头策略.txt",
    "jkcode/jkcode/02 龙头底分型战法-两年23倍.txt",
    "jkcode/jkcode/03 5年15倍的收益，年化79.93%，可实盘，拿走不谢！.txt",
]

stock_pool = [
    "600519.XSHG",
    "000858.XSHE",
    "000333.XSHE",
    "600036.XSHG",
    "601318.XSHG",
]


def main():
    print("=" * 80)
    print("开始测试运行10个聚宽策略文件")
    print("=" * 80)

    results = []
    for i, strategy_file in enumerate(strategies, 1):
        print(f"\n\n[{i}/10] 测试策略: {os.path.basename(strategy_file)}")
        print("-" * 80)

        if not os.path.exists(strategy_file):
            print(f"文件不存在: {strategy_file}")
            results.append(
                {"strategy": strategy_file, "status": "文件不存在", "success": False}
            )
            continue

        try:
            result = run_jq_strategy(
                strategy_file=strategy_file,
                start_date="2022-01-01",
                end_date="2022-03-31",
                initial_capital=1000000,
                stock_pool=stock_pool,
            )

            if result:
                results.append(
                    {
                        "strategy": os.path.basename(strategy_file),
                        "status": "运行成功",
                        "success": True,
                        "final_value": result["final_value"],
                        "pnl_pct": result["pnl_pct"],
                    }
                )
                print(
                    f"✓ 运行成功: 最终资金 {result['final_value']:,.2f}, 收益率 {result['pnl_pct']:.2f}%"
                )
            else:
                results.append(
                    {
                        "strategy": os.path.basename(strategy_file),
                        "status": "运行失败",
                        "success": False,
                    }
                )
                print(f"✗ 运行失败")
        except Exception as e:
            results.append(
                {
                    "strategy": os.path.basename(strategy_file),
                    "status": f"异常: {str(e)[:50]}",
                    "success": False,
                }
            )
            print(f"✗ 运行异常: {e}")
            import traceback

            traceback.print_exc()

    print("\n\n" + "=" * 80)
    print("测试结果汇总")
    print("=" * 80)

    success_count = sum(1 for r in results if r["success"])
    print(f"\n总计: {len(results)} 个策略")
    print(f"成功: {success_count} 个")
    print(f"失败: {len(results) - success_count} 个")

    print("\n详细结果:")
    for i, r in enumerate(results, 1):
        status = "✓" if r["success"] else "✗"
        print(f"{i}. [{status}] {r['strategy'][:50]}")
        if r["success"]:
            print(f"   最终资金: {r['final_value']:,.2f}, 收益率: {r['pnl_pct']:.2f}%")
        else:
            print(f"   状态: {r['status']}")


if __name__ == "__main__":
    main()
