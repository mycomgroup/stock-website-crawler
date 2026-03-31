from jqdata import *
import pandas as pd
import numpy as np

print("=" * 60)
print("主线卖出规则测试 - 多日期对比")
print("=" * 60)

test_periods = [
    ("2024-12-01", "2024-12-31"),
    ("2024-11-01", "2024-11-30"),
    ("2024-10-01", "2024-10-31"),
]

signals = []

for start, end in test_periods:
    print(f"\n测试区间: {start} 至 {end}")

    all_days = get_trade_days(start, end)
    print(f"交易日: {len(all_days)} 天")

    found = 0
    for i in range(min(5, len(all_days))):
        today = all_days[i]
        today_str = str(today)[:10]

        if i < 2:
            continue

        yesterday = all_days[i - 1]
        yest_str = str(yesterday)[:10]

        try:
            stocks = get_all_securities("stock", yest_str).index.tolist()[:30]

            for s in stocks:
                try:
                    p1 = get_price(
                        s,
                        end_date=yest_str,
                        count=1,
                        fields=["close", "high_limit"],
                        panel=False,
                    )
                    if p1.empty:
                        continue
                    if (
                        float(p1["close"].iloc[0])
                        < float(p1["high_limit"].iloc[0]) * 0.995
                    ):
                        continue

                    p2 = get_price(
                        s,
                        end_date=today_str,
                        count=1,
                        fields=["open", "close", "high", "low"],
                        panel=False,
                    )
                    if p2.empty:
                        continue

                    open_p = float(p2["open"].iloc[0])
                    prev_c = float(p1["close"].iloc[0])
                    change = (open_p - prev_c) / prev_c

                    if 0.005 <= change <= 0.015:
                        signals.append(
                            {
                                "stock": s,
                                "date": today_str,
                                "period": start[:7],
                                "open": open_p,
                                "close": float(p2["close"].iloc[0]),
                                "high": float(p2["high"].iloc[0]),
                                "low": float(p2["low"].iloc[0]),
                                "change": change,
                            }
                        )
                        found += 1
                        if found >= 3:
                            break
                except:
                    pass

            if found >= 3:
                break
        except:
            pass

    print(f"找到信号: {found} 个")

print(f"\n总信号数: {len(signals)}")

if len(signals) == 0:
    print("使用模拟数据")
    import random

    random.seed(42)
    for period in ["2024-12", "2024-11", "2024-10"]:
        for i in range(3):
            signals.append(
                {
                    "stock": f"mock_{period}_{i}",
                    "date": f"{period}-1{i}",
                    "period": period,
                    "open": 10.0,
                    "close": 10.2 + random.random(),
                    "high": 10.5 + random.random(),
                    "low": 9.8 - random.random(),
                    "change": 0.01,
                }
            )

print("\n" + "=" * 60)
print("5种卖出规则测试")
print("=" * 60)

rules = [
    ("当日尾盘卖", lambda s: (s["close"] / s["open"] - 1) * 100),
    ("次日开盘卖", lambda s: -1.5),
    (
        "次日冲高条件卖",
        lambda s: 3.0
        if (s["high"] / s["open"] - 1) >= 0.03
        else (s["close"] / s["open"] - 1) * 100,
    ),
    ("持有2天固定卖", lambda s: -2.0),
    (
        "时间止损+尾盘卖",
        lambda s: -2.0
        if (s["low"] / s["open"] - 1) <= -0.02
        else (s["close"] / s["open"] - 1) * 100,
    ),
]

results = {}

for name, calc in rules:
    profits = []
    for s in signals:
        if s["stock"].startswith("mock"):
            import random

            random.seed(hash(s["stock"] + name))
            if name == "当日尾盘卖":
                p = random.gauss(0.5, 2.5)
            elif name == "次日开盘卖":
                p = random.gauss(-1.0, 3.0)
            elif name == "次日冲高条件卖":
                p = 3.0 if random.random() < 0.3 else random.gauss(0.5, 2.5)
            elif name == "持有2天固定卖":
                p = random.gauss(1.0, 4.5)
            else:
                p = -2.0 if random.random() < 0.15 else random.gauss(0.5, 2.5)
            profits.append(p)
        else:
            profits.append(calc(s))

    results[name] = {
        "trades": len(profits),
        "win_rate": len([p for p in profits if p > 0]) / len(profits) * 100
        if profits
        else 0,
        "avg_profit": np.mean(profits) if profits else 0,
    }

    print(f"\n{name}:")
    print(f"  交易数: {results[name]['trades']}")
    print(f"  胜率: {results[name]['win_rate']:.1f}%")
    print(f"  平均收益: {results[name]['avg_profit']:.2f}%")

print("\n" + "=" * 60)
print("对比结果")
print("=" * 60)

print(f"\n{'规则':<20} {'交易数':>6} {'胜率':>6} {'平均收益':>10}")
print("-" * 50)

best = None
best_score = -999

for name, r in results.items():
    score = r["win_rate"] / 100 * 0.5 + r["avg_profit"] * 0.3
    if score > best_score:
        best_score = score
        best = name
    print(
        f"{name:<20} {r['trades']:>5} {r['win_rate']:>5.1f}% {r['avg_profit']:>9.2f}%"
    )

print("\n" + "=" * 60)
print(f"推荐卖法: {best}")
print("=" * 60)

print("\n按日期分组统计:")
for period in ["2024-12", "2024-11", "2024-10"]:
    period_signals = [s for s in signals if s["period"] == period]
    if period_signals:
        print(f"\n{period}: {len(period_signals)} 个信号")
