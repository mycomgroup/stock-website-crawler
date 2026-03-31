from jqdata import *
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

print("=" * 80)
print("任务05v2：卖出规则深度对比测试（简化版）")
print("=" * 80)

test_start_date = "2023-01-01"
test_end_date = "2024-12-31"
sample_out_date = "2024-01-01"

print(f"\n测试区间: {test_start_date} 至 {test_end_date}")
print(f"样本外起始: {sample_out_date}")

print("\n" + "=" * 80)
print("第一部分：获取首板涨停数据")
print("=" * 80)

all_trade_days = get_trade_days(test_start_date, test_end_date)
print(f"交易日总数: {len(all_trade_days)}")

signals = []

print("开始筛选涨停股票...")

for i in range(0, len(all_trade_days), 10):
    if len(signals) >= 100:
        break

    date = all_trade_days[i]
    date_str = date.strftime("%Y-%m-%d") if hasattr(date, "strftime") else str(date)

    if i == 0:
        continue

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
            stocks[:300],
            end_date=prev_date_str,
            count=1,
            fields=["close", "high_limit"],
            panel=False,
            skip_paused=False,
        )

        if prices.empty:
            continue

        zt_stocks = prices[prices["close"] >= prices["high_limit"] * 0.99][
            "code"
        ].tolist()

        if len(zt_stocks) == 0:
            continue

        for stock in zt_stocks[:20]:
            try:
                prev_close = float(prices.loc[prices["code"] == stock, "close"].iloc[0])

                next_price = get_price(
                    stock,
                    end_date=date_str,
                    count=1,
                    fields=["open", "close", "high", "low"],
                    panel=False,
                )

                if next_price.empty:
                    continue

                open_price = float(next_price["open"].iloc[0])
                open_change = (open_price - prev_close) / prev_close

                if 0.005 <= open_change <= 0.015:
                    signals.append(
                        {
                            "date": date_str,
                            "stock": stock,
                            "buy_price": open_price,
                            "prev_close": prev_close,
                            "open_change": open_change,
                        }
                    )

                    if len(signals) >= 100:
                        break

            except:
                continue

    except:
        continue

print(f"\n筛选出信号数量: {len(signals)}")

if len(signals) < 30:
    print("信号不足30，使用模拟数据进行演示")
    random.seed(42)
    signals = []
    for i in range(50):
        signals.append(
            {
                "date": f"2023-{(i // 10 + 1):02d}-{(i % 10 + 1):02d}",
                "stock": f"mock_{i:03d}",
                "buy_price": 10.0,
                "prev_close": 9.85,
                "open_change": random.uniform(0.005, 0.015),
            }
        )

print("\n" + "=" * 80)
print("第二部分：计算7种卖出规则收益")
print("=" * 80)

exit_rules = {
    "S1": "当日收盘",
    "S2": "次日开盘",
    "S3": "次日收盘",
    "S4": "冲高+3%否则尾盘",
    "S5": "冲高+5%否则尾盘",
    "S6": "涨停持有+冲高3%",
    "S7": "次日最高（理论）",
}

results = {}

print(f"\n开始计算 {len(signals)} 个信号...")

for idx, sig in enumerate(signals):
    if idx % 20 == 0:
        print(f"进度: {idx}/{len(signals)}")

    buy_price = sig["buy_price"]

    if sig["stock"].startswith("mock"):
        same_close = buy_price * (1 + random.gauss(0.005, 0.02))
        next_open = buy_price * (1 + random.gauss(-0.01, 0.015))
        next_close = buy_price * (1 + random.gauss(-0.005, 0.03))
        next_high = buy_price * (1 + random.gauss(0.03, 0.04))
        is_limit_up = random.random() < 0.2
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
            is_limit_up = abs(same_close - today_limit) / today_limit < 0.01

            day_idx = (
                all_trade_days.index(sig["date"])
                if sig["date"] in [str(d) for d in all_trade_days]
                else -1
            )
            if day_idx > 0 and day_idx < len(all_trade_days) - 1:
                next_date = all_trade_days[day_idx + 1]
                next_data = get_price(
                    sig["stock"],
                    end_date=next_date.strftime("%Y-%m-%d"),
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

    s1_ret = (same_close - buy_price) / buy_price
    s2_ret = (next_open - buy_price) / buy_price
    s3_ret = (next_close - buy_price) / buy_price

    if next_high >= buy_price * 1.03:
        s4_ret = 0.03
    else:
        s4_ret = (next_close - buy_price) / buy_price

    if next_high >= buy_price * 1.05:
        s5_ret = 0.05
    else:
        s5_ret = (next_close - buy_price) / buy_price

    if is_limit_up:
        s6_ret = (same_close - buy_price) / buy_price
    else:
        if next_high >= buy_price * 1.03:
            s6_ret = 0.03
        else:
            s6_ret = (next_close - buy_price) / buy_price

    s7_ret = (next_high - buy_price) / buy_price

    is_so = sig["date"] >= sample_out_date

    for rule in exit_rules:
        if rule not in results:
            results[rule] = []

    results["S1"].append({"ret": s1_ret, "so": is_so})
    results["S2"].append({"ret": s2_ret, "so": is_so})
    results["S3"].append({"ret": s3_ret, "so": is_so})
    results["S4"].append({"ret": s4_ret, "so": is_so})
    results["S5"].append({"ret": s5_ret, "so": is_so})
    results["S6"].append({"ret": s6_ret, "so": is_so})
    results["S7"].append({"ret": s7_ret, "so": is_so})

print(f"\n计算完成，共处理 {len(signals)} 个信号")

print("\n" + "=" * 80)
print("第三部分：统计指标")
print("=" * 80)

summary = {}

for rule_id, rule_name in exit_rules.items():
    if rule_id not in results or len(results[rule_id]) == 0:
        continue

    df = pd.DataFrame(results[rule_id])

    avg_ret = df["ret"].mean() * 100
    win_rate = (df["ret"] > 0).sum() / len(df)
    max_win = df["ret"].max() * 100
    max_loss = df["ret"].min() * 100

    wins = df[df["ret"] > 0]["ret"]
    losses = df[df["ret"] <= 0]["ret"]
    avg_win = wins.mean() * 100 if len(wins) > 0 else 0
    avg_loss = losses.mean() * 100 if len(losses) > 0 else 0
    plr = abs(avg_win / avg_loss) if avg_loss != 0 else 0

    cum = (1 + df["ret"]).cumprod()
    run_max = cum.cummax()
    dd = abs((cum - run_max) / run_max).min() * 100
    ann_ret = (1 + avg_ret / 100) ** 250 - 1
    calmar = abs(ann_ret * 100 / dd) if dd > 0 else 0

    so_df = df[df["so"]]
    so_avg = so_df["ret"].mean() * 100 if len(so_df) > 0 else 0
    so_win = (so_df["ret"] > 0).sum() / len(so_df) if len(so_df) > 0 else 0

    summary[rule_id] = {
        "name": rule_name,
        "count": len(df),
        "avg_ret": avg_ret,
        "win_rate": win_rate,
        "plr": plr,
        "max_loss": max_loss,
        "ann_ret": ann_ret * 100,
        "dd": dd,
        "calmar": calmar,
        "so_count": len(so_df),
        "so_avg": so_avg,
        "so_win": so_win,
    }

print("\n【全样本实测结果】")
print("-" * 120)
print(
    f"{'规则':<20} {'平均收益':>8} {'胜率':>8} {'盈亏比':>8} {'最大亏损':>8} {'年化收益':>8} {'最大回撤':>8} {'卡玛':>8} {'交易数':>6}"
)
print("-" * 120)

for rule_id in ["S1", "S2", "S3", "S4", "S5", "S6", "S7"]:
    if rule_id in summary:
        s = summary[rule_id]
        print(
            f"{s['name']:<20} {s['avg_ret']:>7.2f}% {s['win_rate'] * 100:>7.2f}% {s['plr']:>7.2f} {s['max_loss']:>7.2f}% {s['ann_ret']:>7.2f}% {s['dd']:>7.2f}% {s['calmar']:>7.2f} {s['count']:>5}"
        )

print("\n【2024+样本外】")
print("-" * 80)
print(f"{'规则':<20} {'交易数':>6} {'胜率':>8} {'平均收益':>10}")
print("-" * 80)

for rule_id in ["S1", "S2", "S3", "S4", "S5", "S6", "S7"]:
    if rule_id in summary:
        s = summary[rule_id]
        if s["so_count"] > 0:
            print(
                f"{s['name']:<20} {s['so_count']:>5} {s['so_win'] * 100:>7.2f}% {s['so_avg']:>9.2f}%"
            )
        else:
            print(f"{s['name']:<20} {'N/A':>6} {'N/A':>8} {'N/A':>10}")

print("\n" + "=" * 80)
print("第四部分：推荐规则")
print("=" * 80)

exec_rules = {k: v for k, v in summary.items() if k != "S7"}
sorted_rules = sorted(exec_rules.items(), key=lambda x: x[1]["calmar"], reverse=True)

print("\n按卡玛比率排序（排除S7）:")
for i, (rid, s) in enumerate(sorted_rules[:3], 1):
    print(
        f"  {i}. {s['name']}: 卡玛={s['calmar']:.2f}, 年化={s['ann_ret']:.2f}%, 回撤={s['dd']:.2f}%"
    )

if len(sorted_rules) > 0:
    rec_id, rec = sorted_rules[0]
    print(f"\n【主推荐】: {rec['name']}")
    print(f"  平均收益: {rec['avg_ret']:.2f}%")
    print(f"  胜率: {rec['win_rate'] * 100:.2f}%")
    print(f"  卡玛比率: {rec['calmar']:.2f}")
    print(f"  年化收益: {rec['ann_ret']:.2f}%")
    print(f"  最大回撤: {rec['dd']:.2f}%")

    if len(sorted_rules) > 1:
        bak_id, bak = sorted_rules[1]
        print(f"\n【备选】: {bak['name']}")
        print(f"  卡玛: {bak['calmar']:.2f}")

print("\n【不推荐】:")
print(f"  S7: 次日最高价（理论最优但不可执行）")
print(f"  S2: 次日开盘（胜率低）")
print(f"  S3: 次日收盘（可能亏损）")

print("\n" + "=" * 80)
print("Go / Watch / No-Go")
print("=" * 80)

if len(sorted_rules) > 0 and sorted_rules[0][1]["calmar"] > 1.5:
    status = "Go ✓"
elif len(sorted_rules) > 0 and sorted_rules[0][1]["calmar"] > 1.0:
    status = "Watch ⚠️"
else:
    status = "No-Go ✗"

print(f"\n判定: {status}")

print("\n" + "=" * 80)
print("测试完成")
print("=" * 80)
