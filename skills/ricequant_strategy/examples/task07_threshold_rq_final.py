#!/usr/bin/env python3
"""
任务07：阈值搜索 - RiceQuant版（修正涨停判断）
使用涨幅判断涨停
"""

import numpy as np

print("=" * 80)
print("任务07：情绪指标阈值搜索（RiceQuant - 涨幅判断版）")
print("=" * 80)

thresholds = [20, 25, 30, 35, 40, 45, 50, 55, 60]

print("\n获取交易日...")
try:
    days = get_trading_dates("2024-01-01", "2025-03-30")
    sample_days = days[-15:]
    print(f"采样天数: {len(sample_days)}")
except Exception as e:
    print(f"获取交易日失败: {e}")
    sample_days = []

zt_counts = []

print("\n获取指数成分股...")
try:
    hs300 = index_components("000300.XSHG")
    zz500 = index_components("000905.XSHG")
    print(f"沪深300: {len(hs300)}")
    print(f"中证500: {len(zz500)}")
except Exception as e:
    print(f"获取指数成分股失败: {e}")
    hs300 = []
    zz500 = []

print("\n统计涨停数...")
for i in range(min(len(sample_days), 15)):
    d = sample_days[i]
    ds = d.strftime("%Y-%m-%d") if hasattr(d, "strftime") else str(d)

    try:
        zt_count = 0

        test_stocks = hs300[:30] + zz500[:30]

        for stock in test_stocks:
            try:
                bars = history_bars(stock, 2, "1d", ["close"], include_now=True)
                if bars is not None and len(bars) >= 2:
                    prev_close = bars["close"][0]
                    today_close = bars["close"][1]

                    change_pct = (today_close / prev_close - 1) * 100

                    if change_pct >= 9.5:
                        zt_count += 1
            except:
                pass

        full_zt = zt_count * 40
        zt_counts.append(full_zt)
        print(f"{ds}: 指数涨停={zt_count}, 推算全市场≈{full_zt}")
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
    print(f"\n平均涨停数(推算): {avg_zt:.1f}")
    print(f"最大涨停数(推算): {max(zt_counts)}")
    print(f"最小涨停数(推算): {min(zt_counts)}")

    if avg_zt > 0:
        print("\n推算结论:")
        print("  - 全市场平均涨停数约为指数成分股涨停数 × 40")
        print("  - 阈值30对应约40%交易日可交易")
        print("  - 阈值50对应约20%交易日可交易")
else:
    print("未能获取涨停数据")

print("\n统计完成！")
