"""
任务02补充：情绪开关快速测试
只测试关键月份
"""

from jqdata import *
import numpy as np

print("=" * 80)
print("任务02补充：情绪开关快速测试")
print("=" * 80)


def get_zt_count(date):
    all_stocks = get_all_securities("stock", date).index.tolist()
    all_stocks = [
        s
        for s in all_stocks
        if not (s.startswith("68") or s.startswith("4") or s.startswith("8"))
    ]
    df = get_price(
        all_stocks,
        end_date=date,
        count=1,
        fields=["close", "high_limit"],
        panel=False,
        fill_paused=False,
    )
    df = df.dropna()
    return len(df[df["close"] == df["high_limit"]])


def quick_test(start, end, threshold=30):
    dates = get_trade_days(start, end)
    trades, wins, profits, skipped = 0, 0, [], 0
    zt_counts = []

    for i in range(1, len(dates) - 1, 2):  # 每隔一天测试
        try:
            zt = get_zt_count(dates[i - 1])
            zt_counts.append(zt)

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
            df = df.dropna()
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
                        open_pct = (p2.iloc[0]["open"] / p1.iloc[0]["close"] - 1) * 100
                        if (
                            0.5 <= open_pct <= 1.5
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

    if trades > 0:
        print(
            f"  {start}: 交易{trades} 胜率{wins / trades * 100:.1f}% 收益{sum(profits):.1f}% ZT均值{np.mean(zt_counts):.0f} 过滤{skipped}"
        )
    return {
        "trades": trades,
        "win_rate": wins / trades * 100 if trades > 0 else 0,
        "profit": sum(profits),
    }


print("\n2024年各季度测试:")
print("无开关:")
quick_test("2024-01-01", "2024-03-31", 0)
quick_test("2024-04-01", "2024-06-30", 0)
quick_test("2024-07-01", "2024-09-30", 0)
quick_test("2024-10-01", "2024-12-31", 0)

print("\n阈值50:")
quick_test("2024-01-01", "2024-03-31", 50)
quick_test("2024-04-01", "2024-06-30", 50)
quick_test("2024-07-01", "2024-09-30", 50)
quick_test("2024-10-01", "2024-12-31", 50)

print("\n2025年Q1测试:")
print("无开关:")
quick_test("2025-01-01", "2025-03-28", 0)
print("阈值50:")
quick_test("2025-01-01", "2025-03-28", 50)

print("\n完成!")
