# 计算龙头底分型信号收益
from jqdata import *
import pandas as pd
import numpy as np

print("=" * 80)
print("计算龙头底分型信号收益")
print("=" * 80)

# 信号列表（前30个）
signals = [
    ("2024-01-05", "600306.XSHG", 12.04),
    ("2024-01-10", "002403.XSHE", 12.91),
    ("2024-01-15", "000017.XSHE", 6.67),
    ("2024-01-18", "000017.XSHE", 9.16),
    ("2024-01-26", "000068.XSHE", 5.48),
    ("2024-01-26", "000070.XSHE", 11.59),
    ("2024-01-31", "600088.XSHG", 25.22),
    ("2024-02-05", "002325.XSHE", 1.20),
    ("2024-02-05", "603958.XSHG", 13.00),
    ("2024-02-26", "000815.XSHE", 9.76),
    ("2024-02-26", "000908.XSHE", 1.67),
    ("2024-02-29", "000586.XSHE", 11.50),
    ("2024-03-05", "002217.XSHE", 1.80),
    ("2024-03-13", "002298.XSHE", 6.36),
    ("2024-04-18", "002835.XSHE", 21.24),
    ("2024-04-26", "001696.XSHE", 11.71),
    ("2024-05-22", "000560.XSHE", 3.57),
    ("2024-05-22", "001267.XSHE", 6.01),
    ("2024-06-13", "000793.XSHE", 1.34),
    ("2024-06-13", "002052.XSHE", 0.88),
]

# 获取交易日
trade_days = get_trade_days("2024-01-01", "2025-12-31")
trade_days_str = [d.strftime("%Y-%m-%d") for d in trade_days]

results = []

print("\n计算收益...")
for i, (date, stock, buy_price) in enumerate(signals):
    try:
        # 找到信号日期的索引
        day_idx = trade_days_str.index(date)

        # 计算1天、3天、5天后的收益
        ret_1d = None
        ret_3d = None
        ret_5d = None

        # 1天后
        if day_idx + 1 < len(trade_days):
            sell_date = trade_days_str[day_idx + 1]
            sell_df = get_price(
                stock, end_date=sell_date, count=1, fields=["close"], panel=False
            )
            if len(sell_df) > 0:
                ret_1d = (sell_df["close"].iloc[0] / buy_price - 1) * 100

        # 3天后
        if day_idx + 3 < len(trade_days):
            sell_date = trade_days_str[day_idx + 3]
            sell_df = get_price(
                stock, end_date=sell_date, count=1, fields=["close"], panel=False
            )
            if len(sell_df) > 0:
                ret_3d = (sell_df["close"].iloc[0] / buy_price - 1) * 100

        # 5天后
        if day_idx + 5 < len(trade_days):
            sell_date = trade_days_str[day_idx + 5]
            sell_df = get_price(
                stock, end_date=sell_date, count=1, fields=["close"], panel=False
            )
            if len(sell_df) > 0:
                ret_5d = (sell_df["close"].iloc[0] / buy_price - 1) * 100

        results.append(
            {
                "date": date,
                "stock": stock,
                "ret_1d": ret_1d,
                "ret_3d": ret_3d,
                "ret_5d": ret_5d,
            }
        )

        print(
            f"{i + 1}. {date} {stock}: 1天={ret_1d:.2f}%, 3天={ret_3d:.2f}%, 5天={ret_5d:.2f}%"
        )

    except Exception as e:
        print(f"{i + 1}. {date} {stock}: 错误 - {str(e)[:30]}")

df = pd.DataFrame(results)

print("\n" + "=" * 80)
print("统计结果")
print("=" * 80)

print(f"\n有效信号数: {len(df)}")

if len(df) > 0:
    # 持有1天
    valid_1d = df[df["ret_1d"].notna()]
    if len(valid_1d) > 0:
        win_rate_1d = (valid_1d["ret_1d"] > 0).sum() / len(valid_1d) * 100
        avg_ret_1d = valid_1d["ret_1d"].mean()
        print(f"\n持有1天:")
        print(f"  胜率: {win_rate_1d:.1f}%")
        print(f"  平均收益: {avg_ret_1d:.2f}%")
        print(f"  盈利次数: {(valid_1d['ret_1d'] > 0).sum()}/{len(valid_1d)}")

    # 持有3天
    valid_3d = df[df["ret_3d"].notna()]
    if len(valid_3d) > 0:
        win_rate_3d = (valid_3d["ret_3d"] > 0).sum() / len(valid_3d) * 100
        avg_ret_3d = valid_3d["ret_3d"].mean()
        print(f"\n持有3天:")
        print(f"  胜率: {win_rate_3d:.1f}%")
        print(f"  平均收益: {avg_ret_3d:.2f}%")
        print(f"  盈利次数: {(valid_3d['ret_3d'] > 0).sum()}/{len(valid_3d)}")

    # 持有5天
    valid_5d = df[df["ret_5d"].notna()]
    if len(valid_5d) > 0:
        win_rate_5d = (valid_5d["ret_5d"] > 0).sum() / len(valid_5d) * 100
        avg_ret_5d = valid_5d["ret_5d"].mean()
        print(f"\n持有5天:")
        print(f"  胜率: {win_rate_5d:.1f}%")
        print(f"  平均收益: {avg_ret_5d:.2f}%")
        print(f"  盈利次数: {(valid_5d['ret_5d'] > 0).sum()}/{len(valid_5d)}")

    # 计算盈亏比
    wins_1d = valid_1d[valid_1d["ret_1d"] > 0]["ret_1d"]
    losses_1d = abs(valid_1d[valid_1d["ret_1d"] < 0]["ret_1d"])

    if len(wins_1d) > 0 and len(losses_1d) > 0:
        profit_loss_ratio = wins_1d.mean() / losses_1d.mean()
        print(f"\n盈亏比: {profit_loss_ratio:.2f}")

    # 最终判断
    print("\n" + "=" * 80)
    print("最终判断:")
    if win_rate_1d >= 50 and avg_ret_1d >= 2:
        print("  ✅ 胜率合格（>=50%）")
        print("  ✅ 平均收益合格（>=2%）")
        if profit_loss_ratio >= 1.5:
            print(f"  ✅ 盈亏比合格（>=1.5，实际{profit_loss_ratio:.2f}）")
            print("\n结论: Go")
        else:
            print(f"  ❌ 盈亏比不足（<1.5，实际{profit_loss_ratio:.2f}）")
            print("\n结论: Watch")
    else:
        print("  ❌ 胜率或收益不足")
        print("\n结论: No-Go")

print("\n计算完成!")
