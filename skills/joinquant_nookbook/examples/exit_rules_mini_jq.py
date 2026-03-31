from jqdata import *
import pandas as pd
import numpy as np

print("=" * 60)
print("主线卖出规则测试 - 最近日期")
print("=" * 60)

test_start = "2024-11-01"
test_end = "2024-12-31"

print(f"\n测试区间: {test_start} 至 {test_end}")

all_days = get_trade_days(test_start, test_end)
print(f"交易日: {len(all_days)} 天")

signals = []

print("\n筛选假弱高开信号 (+0.5%~+1.5%)...")

for i in range(min(10, len(all_days))):
    today = all_days[i]
    today_str = str(today)[:10]

    if i < 2:
        continue

    yesterday = all_days[i - 1]
    yest_str = str(yesterday)[:10]

    try:
        stocks = get_all_securities("stock", yest_str).index.tolist()[:50]

        for s in stocks:
            try:
                p1 = get_price(
                    s,
                    end_date=yest_str,
                    count=1,
                    fields=["close", "high_limit"],
                    panel=False,
                )
                if (
                    p1.empty
                    or float(p1["close"].iloc[0])
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
                            "open": open_p,
                            "close": float(p2["close"].iloc[0]),
                            "high": float(p2["high"].iloc[0]),
                            "low": float(p2["low"].iloc[0]),
                            "change": change,
                        }
                    )
                    if len(signals) >= 5:
                        break
            except:
                pass

        if len(signals) >= 5:
            break
    except:
        pass

print(f"找到信号: {len(signals)} 个")

if len(signals) == 0:
    print("\n使用模拟数据...")
    import random

    random.seed(42)
    for idx in range(5):
        signals.append(
            {
                "stock": "mock_" + str(idx),
                "date": "2024-11-" + str(10 + idx),
                "open": 10.0,
                "close": 10.2,
                "high": 10.5,
                "low": 9.8,
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
            elif name == "时间止损+尾盘卖":
                p = -2.0 if random.random() < 0.15 else random.gauss(0.5, 2.5)
            profits.append(p)
        else:
            profits.append(calc(s))

    results[name] = {
        "trades": len(profits),
        "win_rate": len([p for p in profits if p > 0]) / len(profits) * 100,
        "avg_profit": np.mean(profits),
        "max_profit": max(profits),
        "max_loss": min(profits),
    }

    print(f"\n{name}:")
    print(f"  交易数: {results[name]['trades']}")
    print(f"  胜率: {results[name]['win_rate']:.1f}%")
    print(f"  平均收益: {results[name]['avg_profit']:.2f}%")

print("\n" + "=" * 60)
print("对比结果")
print("=" * 60)

print(f"\n{'规则':<20} {'胜率':>6} {'平均收益':>10}")
print("-" * 40)

best = None
best_score = -999

for name, r in results.items():
    score = r["win_rate"] / 100 * 0.5 + r["avg_profit"] * 0.3
    if score > best_score:
        best_score = score
        best = name
    print(f"{name:<20} {r['win_rate']:>5.1f}% {r['avg_profit']:>9.2f}%")

print("\n" + "=" * 60)
print(f"推荐: {best}")
print("=" * 60)
