from jqdata import *
import pandas as pd
import numpy as np

"""
v2任务01: 主线容量与滑点实测
测试不同仓位规模下的实际成交情况
"""

print("=" * 60)
print("v2任务01: 主线容量与滑点实测")
print("=" * 60)

test_dates = list(get_trade_days(end_date="2024-12-31", count=250))
test_dates = [str(d) for d in test_dates if str(d) >= "2024-01-02"]

signals = []

print(f"\n研究期间: {test_dates[0]} 至 {test_dates[-1]}")
print(f"交易日数: {len(test_dates)}")

for i in range(1, len(test_dates)):
    prev_date = test_dates[i - 1]
    curr_date = test_dates[i]

    if i % 50 == 0:
        print(f"进度: {i}/{len(test_dates)}")

    try:
        all_stocks = get_all_securities("stock", prev_date).index.tolist()

        price_prev = get_price(
            all_stocks[:2000],
            end_date=prev_date,
            count=1,
            fields=["close", "high_limit", "volume", "money"],
            panel=False,
        )

        if price_prev.empty:
            continue

        limit_stocks = price_prev[
            abs(price_prev["close"] - price_prev["high_limit"])
            / price_prev["high_limit"]
            < 0.01
        ]

        for _, row in limit_stocks.iterrows():
            stock = row["code"]
            try:
                price_curr = get_price(
                    stock,
                    end_date=curr_date,
                    count=1,
                    fields=["open", "close", "high", "volume", "money"],
                    panel=False,
                )

                if price_curr.empty:
                    continue

                q = query(valuation.code, valuation.circulating_market_cap).filter(
                    valuation.code == stock
                )
                val = get_fundamentals(q, date=curr_date)

                if val.empty:
                    continue

                market_cap = float(val["circulating_market_cap"].iloc[0])

                if not (50 <= market_cap <= 150):
                    continue

                prev_close = row["close"]
                curr_open = float(price_curr["open"].iloc[0])
                curr_volume = float(price_curr["volume"].iloc[0])
                curr_money = float(price_curr["money"].iloc[0])

                open_pct = (curr_open - prev_close) / prev_close * 100

                if 0.5 <= open_pct <= 1.5:
                    signals.append(
                        {
                            "date": curr_date,
                            "stock": stock,
                            "open_pct": open_pct,
                            "volume": curr_volume,
                            "turnover": curr_money,
                            "market_cap": market_cap,
                        }
                    )
            except:
                continue
    except:
        continue

print(f"\n找到假弱高开信号: {len(signals)}个")

if len(signals) == 0:
    print("无信号数据，退出")
else:
    df = pd.DataFrame(signals)

    print("\n" + "=" * 60)
    print("容量分析")
    print("=" * 60)

    position_sizes = [10, 30, 50, 100, 200, 500]

    results = []

    for size in position_sizes:
        size_wan = size

        avg_volume = df["volume"].mean()
        avg_turnover = df["turnover"].mean()
        avg_price = avg_turnover / avg_volume if avg_volume > 0 else 10

        shares_needed = int(size_wan * 10000 / avg_price)

        volume_ratio = shares_needed / avg_volume * 100

        estimated_slippage = max(0, min(2, volume_ratio / 20))

        success_rate = max(0, 100 - volume_ratio * 2)

        results.append(
            {
                "position": f"{size}万",
                "avg_volume": int(avg_volume),
                "shares_needed": shares_needed,
                "volume_ratio": f"{volume_ratio:.1f}%",
                "slippage": f"{estimated_slippage:.2f}%",
                "success_rate": f"{success_rate:.1f}%",
            }
        )

    print("\n不同仓位下的成交分析:")
    print("-" * 60)
    print(
        f"{'仓位':<10} {'平均成交量':<12} {'需买入股数':<12} {'占比':<10} {'预估滑点':<10} {'成功率':<10}"
    )
    print("-" * 60)
    for r in results:
        print(
            f"{r['position']:<10} {r['avg_volume']:<12} {r['shares_needed']:<12} {r['volume_ratio']:<10} {r['slippage']:<10} {r['success_rate']:<10}"
        )

    print("\n" + "=" * 60)
    print("容量结论")
    print("=" * 60)

    safe_capacity = max(
        [
            size
            for size, r in zip(position_sizes, results)
            if float(r["slippage"].replace("%", "")) < 0.5
        ],
        default=10,
    )

    critical_capacity = max(
        [
            size
            for size, r in zip(position_sizes, results)
            if float(r["slippage"].replace("%", "")) < 1.0
        ],
        default=30,
    )

    print(f"\n安全容量（滑点<0.5%）: {safe_capacity}万元")
    print(f"临界容量（滑点<1.0%）: {critical_capacity}万元")
    print(f"平均每日成交量: {int(avg_volume)}股")
    print(f"平均成交额: {int(avg_turnover / 10000)}万元")

    print("\n建议:")
    if critical_capacity <= 50:
        print("  信号流动性较差，建议仓位控制在50万以内")
    else:
        print(f"  信号流动性良好，可支持{critical_capacity}万仓位")

print("\n分析完成！")
