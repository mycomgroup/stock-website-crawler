"""
任务02：情绪开关2024-2025完整测试（简化版）
在JoinQuant Notebook手动运行
"""

from jqdata import *
import numpy as np

print("=" * 80)
print("任务02：情绪开关2024-2025完整测试")
print("=" * 80)


def get_zt_count(date):
    stocks = get_all_securities("stock", date).index.tolist()
    stocks = [
        s
        for s in stocks
        if not (s.startswith("68") or s.startswith("4") or s.startswith("8"))
    ]
    df = get_price(
        stocks, end_date=date, count=1, fields=["close", "high_limit"], panel=False
    )
    df = df.dropna()
    return len(df[df["close"] == df["high_limit"]])


def test_quarter(start, end, threshold=30):
    dates = get_trade_days(start, end)
    trades, wins, profits, skipped, zt_list = 0, 0, [], 0, []

    for i in range(1, len(dates) - 1):
        try:
            zt = get_zt_count(dates[i - 1])
            zt_list.append(zt)
            if threshold > 0 and zt < threshold:
                skipped += 1
                continue

            stocks = get_all_securities("stock", dates[i - 1]).index.tolist()
            stocks = [
                s
                for s in stocks
                if not (s.startswith("68") or s.startswith("4") or s.startswith("8"))
            ]
            df = get_price(
                stocks,
                end_date=dates[i - 1],
                count=1,
                fields=["close", "high_limit"],
                panel=False,
            )
            zt_stocks = list(df[df["close"] == df["high_limit"]]["code"])[:5]

            for s in zt_stocks:
                try:
                    p1 = get_price(
                        s, end_date=dates[i - 1], count=1, fields=["close"], panel=False
                    )
                    p2 = get_price(
                        s,
                        end_date=dates[i],
                        count=1,
                        fields=["open", "high_limit"],
                        panel=False,
                    )
                    p3 = get_price(
                        s, end_date=dates[i + 1], count=1, fields=["close"], panel=False
                    )
                    if len(p1) > 0 and len(p2) > 0 and len(p3) > 0:
                        pct = (p2.iloc[0]["open"] / p1.iloc[0]["close"] - 1) * 100
                        if (
                            0.5 <= pct <= 1.5
                            and p2.iloc[0]["open"] < p2.iloc[0]["high_limit"]
                        ):
                            profit = (
                                p3.iloc[0]["close"] / (p2.iloc[0]["open"] * 1.005) - 1
                            ) * 100
                            profits.append(profit)
                            trades += 1
                            if profit > 0:
                                wins += 1
                            break
                except:
                    pass
        except:
            pass

    result = {
        "trades": trades,
        "win_rate": wins / trades * 100 if trades > 0 else 0,
        "total_profit": sum(profits),
        "avg_zt": np.mean(zt_list) if zt_list else 0,
        "skipped": skipped,
    }

    if trades > 0:
        print(
            f"{start}: T={trades} WR={result['win_rate']:.1f}% P={result['total_profit']:.1f}% ZT={result['avg_zt']:.0f} Skip={skipped}"
        )

    return result


# 测试各季度
periods = [
    ("2024Q1", "2024-01-01", "2024-06-30"),
    ("2024Q2", "2024-07-01", "2024-12-31"),
    ("2025Q1", "2025-01-01", "2025-03-28"),
]

print("\n【无情绪开关】")
results_no_switch = []
for name, start, end in periods:
    print(f"\n{name}:")
    r = test_quarter(start, end, 0)
    results_no_switch.append((name, r))

print("\n" + "=" * 80)
print("\n【阈值50情绪开关】")
results_switch = []
for name, start, end in periods:
    print(f"\n{name}:")
    r = test_quarter(start, end, 50)
    results_switch.append((name, r))

print("\n" + "=" * 80)
print("汇总对照表")
print("=" * 80)

print("\n无开关:")
for name, r in results_no_switch:
    if r["trades"] > 0:
        print(
            f"  {name}: {r['trades']}笔, 胜率{r['win_rate']:.1f}%, 收益{r['total_profit']:.1f}%"
        )

print("\n阈值50:")
for name, r in results_switch:
    if r["trades"] > 0:
        print(
            f"  {name}: {r['trades']}笔, 胜率{r['win_rate']:.1f}%, 收益{r['total_profit']:.1f}%, 过滤{r['skipped']}天"
        )

print("\n完成!")
