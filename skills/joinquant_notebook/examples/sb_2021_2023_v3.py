from jqdata import *
import pandas as pd

print("=" * 60)
print("二板策略2021-2023实测验证 - Notebook版")
print("=" * 60)

YEARS = [2021, 2022, 2023]
all_results = {}

for year in YEARS:
    print(f"\n处理 {year} 年...")

    dates = list(get_trade_days(start_date=f"{year}-01-01", end_date=f"{year}-12-31"))
    dates = [str(d) if hasattr(d, "strftime") else d for d in dates]

    print(f"  交易日: {len(dates)}")

    signals = []
    zt_counts = []

    for i in range(2, len(dates)):
        d1, d2, d3 = dates[i - 2], dates[i - 1], dates[i]

        try:
            stocks = get_all_securities("stock", d2).index.tolist()
            stocks = [s for s in stocks if not s.startswith(("68", "4", "8"))]

            p = get_price(
                stocks,
                end_date=d2,
                count=1,
                fields=["close", "high_limit"],
                panel=False,
            )
            if p.empty:
                continue

            zt_df = p[abs(p["close"] - p["high_limit"]) / p["high_limit"] < 0.01]
            zt_stocks = zt_df["code"].tolist()
            zt_count = len(zt_stocks)
            zt_counts.append(zt_count)

            if zt_count < 10:
                continue

            pp = get_price(
                zt_stocks,
                end_date=d1,
                count=1,
                fields=["close", "high_limit"],
                panel=False,
            )
            if pp.empty:
                continue

            two_board = []
            for s in zt_stocks:
                row = pp[pp["code"] == s]
                if len(row) == 0:
                    continue
                if (
                    abs(row["close"].iloc[0] - row["high_limit"].iloc[0])
                    / row["high_limit"].iloc[0]
                    < 0.01
                ):
                    two_board.append(s)

            if len(two_board) == 0:
                continue

            val = get_fundamentals(
                query(valuation.code, valuation.circulating_market_cap).filter(
                    valuation.code.in_(two_board)
                ),
                date=d3,
            )

            if val.empty:
                continue

            target = val.sort_values("circulating_market_cap").iloc[0]["code"]

            curr = get_price(
                target,
                end_date=d3,
                count=1,
                fields=["open", "close", "high_limit"],
                panel=False,
            )
            if curr.empty:
                continue

            o = float(curr["open"].iloc[0])
            c = float(curr["close"].iloc[0])
            hl = float(curr["high_limit"].iloc[0])

            if abs(o - hl) / hl < 0.01:
                continue

            ret = round((c - o) / o * 100, 2)
            signals.append({"date": d3, "return": ret, "win": ret > 0})

        except Exception as e:
            continue

    if signals:
        df = pd.DataFrame(signals)
        wins = df["win"].sum()
        avg_ret = df["return"].mean()
        win_rate = wins / len(signals) * 100

        all_results[year] = {
            "count": len(signals),
            "avg_return": round(avg_ret, 2),
            "win_rate": round(win_rate, 1),
            "avg_zt": round(sum(zt_counts) / len(zt_counts), 1) if zt_counts else 0,
        }

        print(f"  信号: {len(signals)}, 收益: {avg_ret:.2f}%, 胜率: {win_rate:.1f}%")
        print(f"  平均涨停: {all_results[year]['avg_zt']}")
    else:
        print(f"  无信号")
        all_results[year] = {"count": 0, "avg_return": 0, "win_rate": 0, "avg_zt": 0}

print("\n" + "=" * 60)
print("汇总")
print("=" * 60)

print(f"\n{'年份':<8} {'信号数':<10} {'收益%':<10} {'胜率%':<10} {'平均涨停':<10}")
print("-" * 50)

for year, r in all_results.items():
    print(
        f"{year:<8} {r['count']:<10} {r['avg_return']:<10} {r['win_rate']:<10} {r['avg_zt']:<10}"
    )

if len(all_results) >= 2:
    returns = [r["avg_return"] for r in all_results.values()]
    winrates = [r["win_rate"] for r in all_results.values()]
    positive = sum(1 for r in returns if r > 0)
    wr_diff = max(winrates) - min(winrates)

    print(f"\n稳定性:")
    print(f"  正收益年: {positive}/3")
    print(f"  胜率差异: {wr_diff:.1f}%")

print("\n完成!")
