from jqdata import *
import json

print("二板策略2021年Q1实测")


def test_q(year, months):
    all_sig = []
    for m in months:
        start = f"{year}-{m:02d}-01"
        end = f"{year}-{m:02d}-28"

        dates = list(get_trade_days(start_date=start, end_date=end))
        dates = [str(d) if hasattr(d, "strftime") else d for d in dates]
        print(f"\n{year}-{m:02d}: {len(dates)}日")

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
                if len(zt) < 10:
                    continue

                pp = get_price(
                    zt,
                    end_date=d1,
                    count=1,
                    fields=["close", "high_limit"],
                    panel=False,
                )
                if pp.empty:
                    continue

                two_b = [
                    s
                    for s in zt
                    if len(pp[pp["code"] == s]) > 0
                    and abs(
                        pp[pp["code"] == s]["close"].iloc[0]
                        - pp[pp["code"] == s]["high_limit"].iloc[0]
                    )
                    / pp[pp["code"] == s]["high_limit"].iloc[0]
                    < 0.01
                ]

                if not two_b:
                    continue

                vol = get_price(
                    two_b, end_date=d2, count=2, fields=["volume"], panel=False
                )
                shrink = [
                    s
                    for s in two_b
                    if len(vol[vol["code"] == s]) >= 2
                    and vol[vol["code"] == s]["volume"].iloc[-1]
                    <= vol[vol["code"] == s]["volume"].iloc[-2] * 1.875
                ]

                if not shrink:
                    continue

                val = get_fundamentals(
                    query(valuation.code, valuation.circulating_market_cap).filter(
                        valuation.code.in_(shrink)
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

                o, c, hl = (
                    float(curr["open"].iloc[0]),
                    float(curr["close"].iloc[0]),
                    float(curr["high_limit"].iloc[0]),
                )
                if abs(o - hl) / hl < 0.01:
                    continue

                ret = round((c - o) / o * 100, 2)
                all_sig.append({"date": d3, "ret": ret, "win": ret > 0})
                print(f"  {d3}: {ret:+.2f}%")
            except:
                continue

    if all_sig:
        rets = [s["ret"] for s in all_sig]
        wins = sum(1 for s in all_sig if s["win"])
        print(
            f"\n统计: {len(all_sig)}笔, 均值{sum(rets) / len(rets):.2f}%, 胜率{wins / len(all_sig) * 100:.1f}%"
        )
    return all_sig


sig = test_q(2021, [1, 2, 3])
print(f"\n完成! 共{len(sig)}笔")
