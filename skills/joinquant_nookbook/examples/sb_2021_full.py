from jqdata import *
import json

print("二板策略实测 - 完整规则版")
print("=" * 60)
print("规则: 二板+情绪>=10+缩量+市值最小+非涨停开盘")
print("=" * 60)


def test_month(year, month):
    start = f"{year}-{month:02d}-01"
    end = f"{year}-{month:02d}-28"

    dates = list(get_trade_days(start_date=start, end_date=end))
    dates = [str(d) if hasattr(d, "strftime") else d for d in dates]

    print(f"\n{year}-{month:02d}: {len(dates)}交易日")

    signals = []

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

            zt = p[abs(p["close"] - p["high_limit"]) / p["high_limit"] < 0.01][
                "code"
            ].tolist()
            zt_count = len(zt)

            if zt_count < 10:
                continue

            pp = get_price(
                zt,
                end_date=d1,
                count=1,
                fields=["close", "high_limit", "volume"],
                panel=False,
            )
            if pp.empty:
                continue

            two_board = []
            for s in zt:
                row = pp[pp["code"] == s]
                if len(row) == 0:
                    continue
                pp_close = float(row["close"].iloc[0])
                pp_limit = float(row["high_limit"].iloc[0])
                if abs(pp_close - pp_limit) / pp_limit >= 0.01:
                    continue
                two_board.append(s)

            if len(two_board) == 0:
                continue

            vol_df = get_price(
                two_board, end_date=d2, count=2, fields=["volume"], panel=False
            )
            shrink = []
            for s in two_board:
                v = vol_df[vol_df["code"] == s]["volume"]
                if len(v) >= 2 and v.iloc[-1] <= v.iloc[-2] * 1.875:
                    shrink.append(s)

            if len(shrink) == 0:
                continue

            val = get_fundamentals(
                query(valuation.code, valuation.circulating_market_cap).filter(
                    valuation.code.in_(shrink)
                ),
                date=d3,
            )

            if val.empty:
                continue

            val = val.sort_values("circulating_market_cap")
            target = val.iloc[0]["code"]

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
            signals.append({"date": d3, "stock": target, "return": ret, "win": ret > 0})
            print(f"  {d3}: {target} {ret:+.2f}%")

        except Exception as e:
            continue

    if signals:
        rets = [s["return"] for s in signals]
        wins = sum(1 for s in signals if s["win"])
        avg = sum(rets) / len(rets)
        wr = wins / len(signals) * 100
        print(f"  小计: {len(signals)}笔, 收益{avg:.2f}%, 胜率{wr:.1f}%")
        return {
            "count": len(signals),
            "avg_return": round(avg, 2),
            "win_rate": round(wr, 1),
            "signals": signals,
        }
    else:
        print(f"  无信号")
        return {"count": 0, "avg_return": 0, "win_rate": 0, "signals": []}


results = {}
for m in range(1, 13):
    results[f"2021-{m:02d}"] = test_month(2021, m)

total_sig = sum(r["count"] for r in results.values())
total_ret = sum(
    r["avg_return"] * r["count"] for r in results.values() if r["count"] > 0
)
total_win = sum(1 for r in results.values() for s in r["signals"] if s["win"])

if total_sig > 0:
    print(
        f"\n2021年总计: {total_sig}笔, 收益{total_ret / total_sig:.2f}%, 胜率{total_win / total_sig * 100:.1f}%"
    )
else:
    print(f"\n2021年无信号")

print("\n完成!")
