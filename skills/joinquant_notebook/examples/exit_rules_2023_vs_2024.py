from jqdata import *
import pandas as pd
import numpy as np

print("=" * 60)
print("主线卖出规则测试 - 2023下半年 vs 2024下半年")
print("=" * 60)

test_periods = [
    ("2024-10", "2024-10-01", "2024-10-31"),
    ("2024-09", "2024-09-01", "2024-09-30"),
    ("2023-12", "2023-12-01", "2023-12-31"),
    ("2023-11", "2023-11-01", "2023-11-30"),
    ("2023-10", "2023-10-01", "2023-10-31"),
]

signals_by_period = {}

for period_name, start, end in test_periods:
    print(f"\n测试: {period_name}")

    all_days = get_trade_days(start, end)
    print(f"  交易日: {len(all_days)}")

    found = 0
    period_signals = []

    for i in range(len(all_days)):
        today = all_days[i]
        today_str = str(today)[:10]

        if i < 2:
            continue

        yesterday = all_days[i - 1]
        yest_str = str(yesterday)[:10]

        try:
            all_stocks = get_all_securities("stock", yest_str).index.tolist()
            stocks = [
                s
                for s in all_stocks
                if not (s.startswith("68") or s.startswith("4") or s.startswith("8"))
            ][:60]

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
                    close1 = float(p1["close"].iloc[0])
                    limit1 = float(p1["high_limit"].iloc[0])
                    if close1 < limit1 * 0.995:
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
                    change = (open_p - close1) / close1

                    if 0.005 <= change <= 0.015:
                        period_signals.append(
                            {
                                "stock": s,
                                "date": today_str,
                                "period": period_name,
                                "open": open_p,
                                "close": float(p2["close"].iloc[0]),
                                "high": float(p2["high"].iloc[0]),
                                "low": float(p2["low"].iloc[0]),
                            }
                        )
                        found += 1
                        if found >= 5:
                            break
                except:
                    pass

            if found >= 5:
                break

            if i > 8:
                break

        except:
            pass

    signals_by_period[period_name] = period_signals
    print(f"  信号: {found}")

all_signals = []
for s_list in signals_by_period.values():
    all_signals.extend(s_list)

print(f"\n总信号数: {len(all_signals)}")

if len(all_signals) == 0:
    print("无信号")
else:
    print("\n" + "=" * 60)
    print("5种卖出规则 - 全部信号")
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
        profits = [calc(s) for s in all_signals]

        results[name] = {
            "trades": len(profits),
            "win_rate": len([p for p in profits if p > 0]) / len(profits) * 100,
            "avg_profit": np.mean(profits),
        }

        print(
            f"{name}: 胜率 {results[name]['win_rate']:.1f}%, 收益 {results[name]['avg_profit']:.2f}%"
        )

    best = max(results.keys(), key=lambda n: results[n]["win_rate"])

    print(f"\n最优: {best} (胜率 {results[best]['win_rate']:.1f}%)")

    print("\n按月对比:")
    for period_name, s_list in signals_by_period.items():
        if s_list:
            profits = [
                (s_list[i]["close"] / s_list[i]["open"] - 1) * 100
                for i in range(len(s_list))
            ]
            avg = np.mean(profits)
            win = len([p for p in profits if p > 0]) / len(profits) * 100
            print(
                f"  {period_name}: {len(s_list)}个信号, 胜率{win:.0f}%, 收益{avg:.2f}%"
            )

print("\n" + "=" * 60)
