from jqdata import *
import json

print("二板2021年1月实测")

dates = list(get_trade_days(start_date="2021-01-01", end_date="2021-01-31"))
dates = [str(d) if hasattr(d, "strftime") else d for d in dates]
print(f"交易日: {len(dates)}")

results = {"signals": [], "zt_counts": []}

for i in range(2, len(dates)):
    d1, d2, d3 = dates[i - 2], dates[i - 1], dates[i]

    try:
        stocks = get_all_securities("stock", d2).index.tolist()
        stocks = [s for s in stocks if not s.startswith(("68", "4", "8"))]

        p = get_price(
            stocks, end_date=d2, count=1, fields=["close", "high_limit"], panel=False
        )
        if p.empty:
            continue

        zt = p[abs(p["close"] - p["high_limit"]) / p["high_limit"] < 0.01][
            "code"
        ].tolist()
        results["zt_counts"].append(len(zt))

        print(f"{d2}: ZT={len(zt)}", end="")

        if len(zt) < 10:
            print(" skip")
            continue

        pp = get_price(
            zt, end_date=d1, count=1, fields=["close", "high_limit"], panel=False
        )
        if pp.empty:
            continue

        two_board = []
        for s in zt:
            row = pp[pp["code"] == s]
            if len(row) == 0:
                continue
            if (
                abs(row["close"].iloc[0] - row["high_limit"].iloc[0])
                / row["high_limit"].iloc[0]
                < 0.01
            ):
                two_board.append(s)

        print(f" 2B={len(two_board)}", end="")

        if len(two_board) == 0:
            print()
            continue

        curr = get_price(
            two_board,
            end_date=d3,
            count=1,
            fields=["open", "close", "high_limit"],
            panel=False,
        )
        if curr.empty:
            continue

        for s in two_board:
            try:
                c = curr[curr["code"] == s]
                if len(c) == 0:
                    continue
                o, cl, hl = (
                    float(c["open"].iloc[0]),
                    float(c["close"].iloc[0]),
                    float(c["high_limit"].iloc[0]),
                )
                if abs(o - hl) / hl < 0.01:
                    continue
                ret = round((cl - o) / o * 100, 2)
                results["signals"].append({"date": d3, "stock": s, "return": ret})
            except:
                continue

        print(f" sig={len([r for r in results['signals'] if r['date'] == d3])}")
    except Exception as e:
        print(f" err:{e}")

if results["signals"]:
    rets = [r["return"] for r in results["signals"]]
    wins = [r for r in rets if r > 0]
    print(
        f"\n统计: 信号{len(rets)}, 收益{sum(rets) / len(rets):.2f}%, 胜率{len(wins) / len(rets) * 100:.1f}%"
    )
else:
    print("\n无信号")

print(json.dumps(results, ensure_ascii=False))
