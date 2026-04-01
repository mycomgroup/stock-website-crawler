#!/usr/bin/env python3
"""
任务07：阈值搜索 - 极简统计版
只统计不同阈值下的交易日数量，不做回测
"""

from jqdata import *

print("=" * 80)
print("任务07：阈值搜索 - 涨停统计")
print("=" * 80)

thresholds = [20, 25, 30, 35, 40, 45, 50, 55, 60]
start_date = "2024-01-01"
end_date = "2025-03-30"

print(f"\n阈值范围: {thresholds}")
print(f"测试期间: {start_date} ~ {end_date}")

days = get_trade_days(start_date, end_date)
sample_days = days[-30:]

print(f"\n采样天数: {len(sample_days)}")

zt_counts = []

print("\n统计涨停数...")
for d in sample_days:
    ds = d.strftime("%Y-%m-%d")

    all_stocks = get_all_securities("stock", ds).index.tolist()
    all_stocks = [
        s
        for s in all_stocks
        if not (s.startswith("68") or s.startswith("4") or s.startswith("8"))
    ]

    df = get_price(
        all_stocks,
        end_date=ds,
        count=1,
        fields=["close", "high_limit"],
        panel=False,
    )
    df = df.dropna()
    zt_count = len(df[df["close"] == df["high_limit"]])

    zt_counts.append(zt_count)
    print(f"{ds}: 涨停数={zt_count}")

print("\n" + "=" * 80)
print("阈值交易机会统计")
print("=" * 80)

total_days = len(zt_counts)

for t in thresholds:
    valid_days = len([c for c in zt_counts if c >= t])
    ratio = valid_days / total_days * 100
    print(f"阈值{t}: 可交易天数={valid_days}/{total_days} ({ratio:.1f}%)")

avg_zt = sum(zt_counts) / len(zt_counts)
print(f"\n平均涨停数: {avg_zt:.1f}")
print(f"最大涨停数: {max(zt_counts)}")
print(f"最小涨停数: {min(zt_counts)}")

print("\n统计完成！")
