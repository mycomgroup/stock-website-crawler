#!/usr/bin/env python3
"""
任务07：阈值搜索 - RiceQuant版本（修正API）
"""

import numpy as np

print("=" * 80)
print("任务07：情绪指标阈值搜索（RiceQuant版）")
print("=" * 80)

thresholds = [20, 25, 30, 35, 40, 45, 50, 55, 60]
start_date = "2024-01-01"
end_date = "2025-03-30"

print(f"\n阈值范围: {thresholds}")
print(f"测试期间: {start_date} ~ {end_date}")

print("\n获取交易日...")
try:
    days = get_trading_dates(start_date, end_date)
    sample_days = days[-30:]
    print(f"采样天数: {len(sample_days)}")
except Exception as e:
    print(f"获取交易日失败: {e}")
    sample_days = []

zt_counts = []

print("\n统计涨停数...")
for i in range(min(len(sample_days), 30)):
    d = sample_days[i]
    ds = d.strftime("%Y-%m-%d") if hasattr(d, "strftime") else str(d)

    try:
        all_stocks = get_all_securities(["stock"])
        all_stocks = [
            s
            for s in all_stocks.index.tolist()
            if not (s.startswith("68") or s.startswith("4") or s.startswith("8"))
        ]

        test_stocks = all_stocks[:100]

        zt_count = 0
        for stock in test_stocks:
            try:
                bars = history_bars(stock, 1, "1d", ["close"], dt=ds, include_now=True)
                if bars is not None and len(bars) > 0:
                    close = bars["close"][0]
                    limit_price = get_next_price_limit(stock, ds)
                    if (
                        limit_price
                        and abs(close - limit_price[1]) / limit_price[1] < 0.01
                    ):
                        zt_count += 1
            except:
                pass

        zt_counts.append(zt_count * (len(all_stocks) // 100))
        print(f"{ds}: 涨停数≈{zt_count * (len(all_stocks) // 100)}")
    except Exception as e:
        print(f"{ds}: 错误 {e}")

print("\n" + "=" * 80)
print("阈值交易机会统计")
print("=" * 80)

if len(zt_counts) > 0:
    total_days = len(zt_counts)

    for t in thresholds:
        valid_days = len([c for c in zt_counts if c >= t])
        ratio = valid_days / total_days * 100
        print(f"阈值{t}: 可交易天数={valid_days}/{total_days} ({ratio:.1f}%)")

    avg_zt = sum(zt_counts) / len(zt_counts)
    print(f"\n平均涨停数: {avg_zt:.1f}")
    print(f"最大涨停数: {max(zt_counts)}")
    print(f"最小涨停数: {min(zt_counts)}")
else:
    print("未能获取涨停数据")

print("\n统计完成！")
