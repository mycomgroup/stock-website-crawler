"""
情绪冰点捕捉测试 - 精简版
只测试2025年最近数据，快速验证冰点次日反弹效果
"""

from jqdata import *
import pandas as pd

print("=" * 80)
print("情绪冰点捕捉测试 - 精简版")
print("=" * 80)

START_DATE = "2025-01-01"
END_DATE = "2025-12-31"

print(f"测试范围: {START_DATE} 至 {END_DATE}")

trade_days = get_trade_days(START_DATE, END_DATE)
print(f"交易日: {len(trade_days)}个")

print("\n【1】统计涨停数据")
zt_stats = []

for i, date in enumerate(trade_days[:100]):
    if i % 10 == 0:
        print(f"进度: {i}/{len(trade_days[:100])}")

    all_stocks = get_all_securities(types=["stock"], date=date)
    stocks = [
        s
        for s in all_stocks.index.tolist()
        if not (
            s.startswith("688")
            or s.startswith("300")
            or s.startswith("4")
            or s.startswith("8")
        )
    ]

    df = get_price(
        stocks[:500],
        end_date=date,
        frequency="daily",
        fields=["close", "high_limit"],
        count=1,
        panel=False,
    )
    df = df.dropna()

    zt_count = len(df[df["close"] == df["high_limit"]])

    zt_stats.append({"date": date, "zt_count": zt_count})

print(f"\n收集涨停数据: {len(zt_stats)}天")

df_zt = pd.DataFrame(zt_stats)
print(f"平均涨停数: {df_zt['zt_count'].mean():.1f}")
print(f"最小涨停数: {df_zt['zt_count'].min()}")
print(f"最大涨停数: {df_zt['zt_count'].max()}")

print("\n【2】识别冰点日")
ice_days = df_zt[df_zt["zt_count"] < 10]["date"].tolist()
print(f"冰点日（涨停<10）: {len(ice_days)}天")

print("\n【3】识别冰点次日")
ice_next_days = []
for i, date in enumerate(trade_days[:100]):
    idx = trade_days.index(date)
    if idx > 0 and trade_days[idx - 1] in ice_days:
        ice_next_days.append(date)

print(f"冰点次日: {len(ice_next_days)}天")

print("\n【4】对比收益")

group_a_rets = []
group_b_rets = []

for i, date in enumerate(trade_days[:100]):
    prev_dates = get_trade_days(end_date=date, count=2)
    if len(prev_dates) < 2:
        continue

    prev_date = prev_dates[0]

    stocks = get_all_securities(types=["stock"], date=date)
    stocks_list = [
        s
        for s in stocks.index.tolist()
        if not (
            s.startswith("688")
            or s.startswith("300")
            or s.startswith("4")
            or s.startswith("8")
        )
    ][:200]

    df_prev = get_price(
        stocks_list,
        end_date=prev_date,
        frequency="daily",
        fields=["close", "high_limit"],
        count=1,
        panel=False,
    )
    df_prev = df_prev.dropna()
    zt_stocks = df_prev[df_prev["close"] == df_prev["high_limit"]]["code"].tolist()

    if not zt_stocks:
        continue

    df_today = get_price(
        zt_stocks,
        end_date=date,
        frequency="daily",
        fields=["open", "close", "pre_close"],
        count=1,
        panel=False,
    )
    df_today = df_today.dropna()

    low_open = df_today[
        (df_today["open"] < df_today["pre_close"])
        & ((df_today["pre_close"] - df_today["open"]) / df_today["pre_close"] < 0.05)
    ]

    if len(low_open) > 0:
        rets = (low_open["close"] - low_open["open"]) / low_open["open"] * 100

        zt_today = (
            df_zt[df_zt["date"] == date]["zt_count"].iloc[0]
            if date in df_zt["date"].values
            else 0
        )

        if zt_today >= 30:
            group_a_rets.extend(rets.tolist()[:3])

        if date in ice_next_days:
            group_b_rets.extend(rets.tolist()[:3])

print(f"\nA组（原始情绪开关，涨停>=30）:")
print(f"  交易次数: {len(group_a_rets)}")
if group_a_rets:
    print(f"  平均收益: {pd.Series(group_a_rets).mean():.2f}%")
    print(
        f"  胜率: {len([r for r in group_a_rets if r > 0]) / len(group_a_rets) * 100:.1f}%"
    )

print(f"\nB组（冰点次日开仓）:")
print(f"  交易次数: {len(group_b_rets)}")
if group_b_rets:
    print(f"  平均收益: {pd.Series(group_b_rets).mean():.2f}%")
    print(
        f"  胜率: {len([r for r in group_b_rets if r > 0]) / len(group_b_rets) * 100:.1f}%"
    )

print("\n【5】冰点次日反弹统计")

ice_next_zt = df_zt[df_zt["date"].isin(ice_next_days)]["zt_count"].tolist()
prev_ice_zt = [
    df_zt[df_zt["date"] == trade_days[trade_days.index(d) - 1]]["zt_count"].iloc[0]
    for d in ice_next_days
    if trade_days.index(d) > 0 and d in trade_days
]

if ice_next_zt and prev_ice_zt:
    rebound_count = len(
        [i for i in range(len(ice_next_zt)) if ice_next_zt[i] > prev_ice_zt[i]]
    )
    print(
        f"冰点次日涨停数增加: {rebound_count}/{len(ice_next_zt)} ({rebound_count / len(ice_next_zt) * 100:.1f}%)"
    )

print("\n" + "=" * 80)
print("测试完成")
print("=" * 80)
