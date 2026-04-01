#!/usr/bin/env python3
from jqdata import *

print("=" * 60)
print("任务07：情绪指标阈值搜索")
print("=" * 60)

thresholds = [20, 25, 30, 35, 40, 45, 50, 55, 60]

print("\n获取交易日...")
days = get_trade_days("2024-01-01", "2025-03-30")
sample_days = days[-30:]
print(f"采样: {len(sample_days)}天")

zt_counts = []

print("\n统计涨停数...")
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
    print(f"{ds}: {zt}个")

print("\n" + "=" * 60)
print("阈值交易机会统计")
print("=" * 60)

total = len(zt_counts)
for t in thresholds:
    valid = len([c for c in zt_counts if c >= t])
    pct = valid / total * 100
    print(f"阈值{t}: {valid}/{total}天 ({pct:.1f}%)")

print(f"\n平均涨停: {sum(zt_counts) / len(zt_counts):.1f}个")
print(f"最大: {max(zt_counts)}, 最小: {min(zt_counts)}")

print("\n完成！")
