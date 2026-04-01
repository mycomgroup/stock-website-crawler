#!/usr/bin/env python3
"""
任务07：情绪指标阈值搜索 - JoinQuant Notebook格式
按照标准格式：直接执行 + print + try-except
"""

from jqdata import *

print("=" * 60)
print("任务07：情绪指标精细化阈值搜索")
print("=" * 60)

thresholds = [20, 25, 30, 35, 40, 45, 50, 55, 60]

try:
    print("\n获取交易日...")
    days = get_trade_days("2024-01-01", "2025-03-30")
    sample_days = days[-60:]
    print(f"采样: {len(sample_days)}天（最近3个月）")

    zt_counts = []

    print("\n统计每日涨停数...")
    for d in sample_days:
        ds = d.strftime("%Y-%m-%d")

        stocks = get_all_securities("stock", ds).index.tolist()
        stocks = [
            s
            for s in stocks
            if not (s.startswith("68") or s.startswith("4") or s.startswith("8"))
        ]

        df = get_price(
            stocks, end_date=ds, count=1, fields=["close", "high_limit"], panel=False
        )
        df = df.dropna()
        zt = len(df[df["close"] == df["high_limit"]])

        zt_counts.append(zt)
        print(f"{ds}: {zt}个涨停")

    print("\n" + "=" * 60)
    print("阈值交易机会统计")
    print("=" * 60)

    total = len(zt_counts)
    for t in thresholds:
        valid = len([c for c in zt_counts if c >= t])
        pct = valid / total * 100
        print(f"阈值{t:2d}: {valid:2d}/{total}天 ({pct:5.1f}%)")

    print(f"\n平均涨停数: {sum(zt_counts) / len(zt_counts):.1f}")
    print(f"最大涨停数: {max(zt_counts)}")
    print(f"最小涨停数: {min(zt_counts)}")

    print("\n" + "=" * 60)
    print("推荐阈值分析")
    print("=" * 60)

    if sum(zt_counts) / len(zt_counts) >= 30:
        print("当前平均涨停数 >= 30，市场情绪较好")
        print("建议阈值: 30（标准）或 40（严格）")
    else:
        print("当前平均涨停数 < 30，市场情绪偏弱")
        print("建议阈值: 25（宽松）或 30（标准）")

except Exception as e:
    print(f"错误: {e}")
    import traceback

    traceback.print_exc()

print("\n" + "=" * 60)
print("测试完成")
print("=" * 60)
