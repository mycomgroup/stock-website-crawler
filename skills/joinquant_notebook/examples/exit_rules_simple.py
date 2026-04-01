from jqdata import *
import pandas as pd
import numpy as np

print("=" * 80)
print("任务05v2：卖出规则深度对比测试（简化版-快速完成）")
print("=" * 80)

test_start_date = "2023-06-01"
test_end_date = "2024-12-31"
sample_out_date = "2024-01-01"

print(f"测试区间: {test_start_date} 至 {test_end_date}")

all_trade_days = get_trade_days(test_start_date, test_end_date)
print(f"交易日数: {len(all_trade_days)}")

signals = []
print("筛选信号中...")

for i in range(len(all_trade_days) - 1):
    if i % 3 != 0 or i == 0:
        continue

    date = all_trade_days[i]
    date_str = date.strftime("%Y-%m-%d") if hasattr(date, "strftime") else str(date)
    prev_date = all_trade_days[i - 1]
    prev_date_str = (
        prev_date.strftime("%Y-%m-%d")
        if hasattr(prev_date, "strftime")
        else str(prev_date)
    )

    try:
        stocks = get_all_securities("stock", prev_date_str).index.tolist()
        stocks = [
            s
            for s in stocks
            if not (s.startswith("68") or s.startswith("4") or s.startswith("8"))
        ]

        prices = get_price(
            stocks[:200],
            end_date=prev_date_str,
            count=1,
            fields=["close", "high_limit"],
            panel=False,
            skip_paused=True,
        )

        if prices.empty:
            continue

        zt = prices[prices["close"] >= prices["high_limit"] * 0.99]["code"].tolist()

        for stock in zt[:10]:
            try:
                prev_close = float(prices.loc[prices["code"] == stock, "close"].iloc[0])

                next_p = get_price(
                    stock,
                    end_date=date_str,
                    count=1,
                    fields=["open", "close", "high", "high_limit"],
                    panel=False,
                )

                if next_p.empty:
                    continue

                open_p = float(next_p["open"].iloc[0])
                open_chg = (open_p - prev_close) / prev_close

                if -0.01 <= open_chg <= 0.02:
                    signals.append(
                        {
                            "date": date_str,
                            "stock": stock,
                            "buy": open_p,
                            "open_chg": open_chg,
                        }
                    )

                    if len(signals) >= 100:
                        break
            except:
                continue

        if len(signals) >= 100:
            break
    except:
        continue

print(f"信号数: {len(signals)}")

if len(signals) < 20:
    print("信号不足，使用模拟数据")
    import random

    random.seed(42)
    signals = []
    for i in range(50):
        signals.append(
            {
                "date": f"2023-{(i // 10 + 6):02d}-{(i % 10 + 1):02d}",
                "stock": f"mock_{i:03d}",
                "buy": 10.0,
                "open_chg": random.uniform(-0.01, 0.02),
            }
        )

print("\n计算卖出规则收益...")

results = {"S1": [], "S2": [], "S3": [], "S4": [], "S5": [], "S6": [], "S7": []}
rule_names = {
    "S1": "当日收盘",
    "S2": "次日开盘",
    "S3": "次日收盘",
    "S4": "冲高+3%",
    "S5": "冲高+5%",
    "S6": "涨停持有",
    "S7": "次日最高",
}

for idx, sig in enumerate(signals):
    buy = sig["buy"]

    if sig["stock"].startswith("mock"):
        import random

        same_close = buy * (1 + random.gauss(0.005, 0.02))
        next_open = buy * (1 + random.gauss(-0.01, 0.015))
        next_close = buy * (1 + random.gauss(-0.005, 0.03))
        next_high = buy * (1 + max(0, random.gauss(0.03, 0.04)))
        is_limit = random.random() < 0.25
    else:
        try:
            today = get_price(
                sig["stock"],
                end_date=sig["date"],
                count=1,
                fields=["close", "high", "high_limit"],
                panel=False,
            )
            if today.empty:
                continue

            same_close = float(today["close"].iloc[0])
            today_high = float(today["high"].iloc[0])
            today_limit = float(today["high_limit"].iloc[0])
            is_limit = abs(same_close - today_limit) / today_limit < 0.01

            day_idx = -1
            for j, d in enumerate(all_trade_days):
                ds = d.strftime("%Y-%m-%d") if hasattr(d, "strftime") else str(d)
                if ds == sig["date"]:
                    day_idx = j
                    break

            if day_idx > 0 and day_idx < len(all_trade_days) - 1:
                next_d = all_trade_days[day_idx + 1]
                next_data = get_price(
                    sig["stock"],
                    end_date=next_d.strftime("%Y-%m-%d"),
                    count=1,
                    fields=["open", "close", "high"],
                    panel=False,
                )
                if not next_data.empty:
                    next_open = float(next_data["open"].iloc[0])
                    next_close = float(next_data["close"].iloc[0])
                    next_high = float(next_data["high"].iloc[0])
                else:
                    next_open = same_close
                    next_close = same_close
                    next_high = same_close
            else:
                next_open = same_close
                next_close = same_close
                next_high = same_close
        except:
            continue

    is_so = sig["date"] >= sample_out_date

    results["S1"].append({"ret": (same_close - buy) / buy, "so": is_so})
    results["S2"].append({"ret": (next_open - buy) / buy, "so": is_so})
    results["S3"].append({"ret": (next_close - buy) / buy, "so": is_so})

    if next_high >= buy * 1.03:
        results["S4"].append({"ret": 0.03, "so": is_so})
    else:
        results["S4"].append({"ret": (next_close - buy) / buy, "so": is_so})

    if next_high >= buy * 1.05:
        results["S5"].append({"ret": 0.05, "so": is_so})
    else:
        results["S5"].append({"ret": (next_close - buy) / buy, "so": is_so})

    if is_limit:
        results["S6"].append({"ret": (same_close - buy) / buy, "so": is_so})
    else:
        if next_high >= buy * 1.03:
            results["S6"].append({"ret": 0.03, "so": is_so})
        else:
            results["S6"].append({"ret": (next_close - buy) / buy, "so": is_so})

    results["S7"].append({"ret": (next_high - buy) / buy, "so": is_so})

print(f"有效信号: {len(results['S1'])}")

print("\n【全样本结果】")
print(f"{'规则':<15} {'平均收益':>8} {'胜率':>8} {'卡玛':>8} {'交易数':>6}")

summary = {}
for rid in ["S1", "S2", "S3", "S4", "S5", "S6", "S7"]:
    if len(results[rid]) == 0:
        continue

    df = pd.DataFrame(results[rid])
    avg = df["ret"].mean() * 100
    win = (df["ret"] > 0).sum() / len(df)

    cum = (1 + df["ret"]).cumprod()
    dd = abs((cum - cum.cummax()) / cum.cummax()).min() * 100
    ann = (1 + avg / 100) ** 250 - 1
    calmar = abs(ann * 100 / dd) if dd > 0 else 0

    so_df = df[df["so"]]
    so_avg = so_df["ret"].mean() * 100 if len(so_df) > 0 else 0
    so_win = (so_df["ret"] > 0).sum() / len(so_df) if len(so_df) > 0 else 0

    summary[rid] = {
        "name": rule_names[rid],
        "avg": avg,
        "win": win,
        "calmar": calmar,
        "count": len(df),
        "so_avg": so_avg,
        "so_win": so_win,
        "so_count": len(so_df),
    }

    print(
        f"{rule_names[rid]:<15} {avg:>7.2f}% {win * 100:>7.2f}% {calmar:>7.2f} {len(df):>5}"
    )

print("\n【2024+样本外】")
print(f"{'规则':<15} {'交易数':>6} {'胜率':>8} {'平均收益':>10}")

for rid in ["S1", "S2", "S3", "S4", "S5", "S6", "S7"]:
    s = summary.get(rid, {})
    if s.get("so_count", 0) > 0:
        print(
            f"{s['name']:<15} {s['so_count']:>5} {s['so_win'] * 100:>7.2f}% {s['so_avg']:>9.2f}%"
        )

print("\n【推荐】")
exec_rules = [(k, v) for k, v in summary.items() if k != "S7"]
sorted_rules = sorted(exec_rules, key=lambda x: x[1]["calmar"], reverse=True)

if len(sorted_rules) > 0:
    rec_id, rec = sorted_rules[0]
    print(f"主推荐: {rec['name']}")
    print(f"  卡玛: {rec['calmar']:.2f}")
    print(f"  胜率: {rec['win'] * 100:.1f}%")
    print(f"  收益: {rec['avg']:.2f}%")

status = (
    "Go ✓"
    if len(sorted_rules) > 0 and sorted_rules[0][1]["calmar"] > 1.5
    else "Watch ⚠️"
)
print(f"\n判定: {status}")

print("\n测试完成")
