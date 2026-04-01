from jqdata import *
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

print("=" * 80)
print("任务05v2：卖出规则深度对比测试（扩大范围版）")
print("=" * 80)

test_start_date = "2022-01-01"
test_end_date = "2024-12-31"
sample_out_date = "2024-01-01"

print(f"\n测试区间: {test_start_date} 至 {test_end_date}")
print(f"样本外起始: {sample_out_date}")

print("\n" + "=" * 80)
print("第一部分：扩大范围筛选信号")
print("=" * 80)

all_trade_days = get_trade_days(test_start_date, test_end_date)
print(f"交易日总数: {len(all_trade_days)}")

signals = []
processed = 0
max_signals = 300

print("\n优化策略：")
print("1. 扩大开盘涨幅范围：-1% ~ +2%（原+0.5%~+1.5%）")
print("2. 增加股票池：500只（原100只）")
print("3. 每5天筛选一次（原每10天）")
print("4. 放宽涨停定义：收盘价≥涨停价99%（原99.5%）")

print("\n开始筛选首板低开信号...")

for i in range(len(all_trade_days) - 1):
    if processed >= max_signals:
        print(f"\n已达到最大信号数 {max_signals}，停止筛选")
        break

    if i % 5 != 0:
        continue

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
        if processed % 20 == 0:
            print(
                f"进度: {processed}/{max_signals}, 处理日期: {prev_date_str}...",
                end=" ",
            )

        stocks = get_all_securities("stock", prev_date_str).index.tolist()
        stocks = [
            s
            for s in stocks
            if not (s.startswith("68") or s.startswith("4") or s.startswith("8"))
        ]

        if len(stocks) == 0:
            continue

        prices = get_price(
            stocks[:500],
            end_date=prev_date_str,
            count=1,
            fields=["close", "high_limit"],
            panel=False,
            skip_paused=True,
        )

        if prices.empty:
            continue

        zt_stocks = prices[prices["close"] >= prices["high_limit"] * 0.99][
            "code"
        ].tolist()

        if len(zt_stocks) == 0:
            if processed % 20 == 0:
                print("无涨停股")
            continue

        if processed % 20 == 0:
            print(f"涨停股: {len(zt_stocks)}只")

        for stock in zt_stocks[:30]:
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

                if -0.01 <= open_change <= 0.02:
                    signals.append(
                        {
                            "date": date_str,
                            "stock": stock,
                            "buy_price": open_price,
                            "prev_close": prev_close,
                            "open_change": open_change,
                        }
                    )
                    processed += 1

                    if processed >= max_signals:
                        break

            except Exception as e:
                continue

    except Exception as e:
        if processed % 20 == 0:
            print(f"错误: {e}")
        continue

print(f"\n共筛选出信号数量: {len(signals)}")

if len(signals) < 50:
    print(f"\n警告: 信号数量仍然不足 ({len(signals)} < 50)")
    print("继续使用现有信号进行测试...")

print("\n" + "=" * 80)
print("第二部分：按开盘涨幅分组统计")
print("=" * 80)

open_groups = {
    "深度低开": (-0.01, 0.0),
    "平开": (0.0, 0.005),
    "假弱高开": (0.005, 0.015),
    "真高开": (0.015, 0.02),
}

print(f"\n信号分组统计:")
for group_name, (low, high) in open_groups.items():
    count = sum(1 for s in signals if low <= s["open_change"] < high)
    pct = count / len(signals) * 100 if len(signals) > 0 else 0
    print(
        f"  {group_name} ({low * 100:.1f}%~{high * 100:.1f}%): {count}个 ({pct:.1f}%)"
    )

print("\n" + "=" * 80)
print("第三部分：计算7种卖出规则收益")
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

results = {k: [] for k in exit_rules}

print(f"\n计算 {len(signals)} 个信号的收益...")

for idx, sig in enumerate(signals):
    if idx % 30 == 0:
        print(f"进度: {idx}/{len(signals)}")

    buy_price = sig["buy_price"]
    stock = sig["stock"]
    date_str = sig["date"]

    try:
        today_price = get_price(
            stock,
            end_date=date_str,
            count=1,
            fields=["close", "high", "high_limit"],
            panel=False,
        )

        if today_price.empty:
            continue

        same_close = float(today_price["close"].iloc[0])
        today_high = float(today_price["high"].iloc[0])
        today_limit = float(today_price["high_limit"].iloc[0])
        is_limit_up = abs(same_close - today_limit) / today_limit < 0.01

        day_idx = -1
        for j, d in enumerate(all_trade_days):
            if (
                d.strftime("%Y-%m-%d") if hasattr(d, "strftime") else str(d)
            ) == date_str:
                day_idx = j
                break

        if day_idx > 0 and day_idx < len(all_trade_days) - 1:
            next_date = all_trade_days[day_idx + 1]
            next_date_str = (
                next_date.strftime("%Y-%m-%d")
                if hasattr(next_date, "strftime")
                else str(next_date)
            )

            next_price = get_price(
                stock,
                end_date=next_date_str,
                count=1,
                fields=["open", "close", "high"],
                panel=False,
            )

            if not next_price.empty:
                next_open = float(next_price["open"].iloc[0])
                next_close = float(next_price["close"].iloc[0])
                next_high = float(next_price["high"].iloc[0])
            else:
                next_open = same_close
                next_close = same_close
                next_high = same_close
        else:
            next_open = same_close
            next_close = same_close
            next_high = same_close

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

        is_so = date_str >= sample_out_date

        results["S1"].append(
            {"ret": s1_ret, "so": is_so, "open_change": sig["open_change"]}
        )
        results["S2"].append(
            {"ret": s2_ret, "so": is_so, "open_change": sig["open_change"]}
        )
        results["S3"].append(
            {"ret": s3_ret, "so": is_so, "open_change": sig["open_change"]}
        )
        results["S4"].append(
            {"ret": s4_ret, "so": is_so, "open_change": sig["open_change"]}
        )
        results["S5"].append(
            {"ret": s5_ret, "so": is_so, "open_change": sig["open_change"]}
        )
        results["S6"].append(
            {"ret": s6_ret, "so": is_so, "open_change": sig["open_change"]}
        )
        results["S7"].append(
            {"ret": s7_ret, "so": is_so, "open_change": sig["open_change"]}
        )

    except Exception as e:
        continue

print(f"\n计算完成，有效信号数: {len(results['S1'])}")

print("\n" + "=" * 80)
print("第四部分：统计各规则指标")
print("=" * 80)

summary = {}

for rule_id, rule_name in exit_rules.items():
    if len(results[rule_id]) == 0:
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
    dd_series = (cum - run_max) / run_max
    dd = abs(dd_series.min()) * 100

    ann_ret = (1 + avg_ret / 100) ** 250 - 1
    calmar = abs(ann_ret * 100 / dd) if dd > 0 else 0

    so_df = df[df["so"]]
    so_count = len(so_df)
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
        "so_count": so_count,
        "so_avg": so_avg,
        "so_win": so_win,
    }

print("\n【全样本实测结果】")
print("-" * 120)
print(
    f"{'卖出规则':<22} {'平均收益':>8} {'胜率':>8} {'盈亏比':>8} {'最大亏损':>8} {'年化收益':>8} {'最大回撤':>8} {'卡玛':>8} {'交易数':>6}"
)
print("-" * 120)

for rule_id in ["S1", "S2", "S3", "S4", "S5", "S6", "S7"]:
    if rule_id in summary:
        s = summary[rule_id]
        print(
            f"{s['name']:<22} {s['avg_ret']:>7.2f}% {s['win_rate'] * 100:>7.2f}% {s['plr']:>7.2f} {s['max_loss']:>7.2f}% {s['ann_ret']:>7.2f}% {s['dd']:>7.2f}% {s['calmar']:>7.2f} {s['count']:>5}"
        )

print("\n【2024+样本外】")
print("-" * 80)
print(f"{'卖出规则':<22} {'交易数':>6} {'胜率':>8} {'平均收益':>10}")
print("-" * 80)

for rule_id in ["S1", "S2", "S3", "S4", "S5", "S6", "S7"]:
    if rule_id in summary:
        s = summary[rule_id]
        if s["so_count"] > 0:
            print(
                f"{s['name']:<22} {s['so_count']:>5} {s['so_win'] * 100:>7.2f}% {s['so_avg']:>9.2f}%"
            )
        else:
            print(f"{s['name']:<22} {'N/A':>6} {'N/A':>8} {'N/A':>10}")

print("\n" + "=" * 80)
print("第五部分：按开盘涨幅分组对比")
print("=" * 80)

print("\n各组信号在不同卖出规则下的表现:")
print("-" * 100)
print(
    f"{'开盘类型':<12} {'交易数':>6} {'S1收益':>8} {'S4收益':>8} {'S7收益':>8} {'S4胜率':>8} {'S7胜率':>8}"
)
print("-" * 100)

for group_name, (low, high) in open_groups.items():
    s4_results = [r for r in results["S4"] if low <= r["open_change"] < high]
    s7_results = [r for r in results["S7"] if low <= r["open_change"] < high]

    if len(s4_results) > 0:
        s4_avg = np.mean([r["ret"] for r in s4_results]) * 100
        s4_win = sum(1 for r in s4_results if r["ret"] > 0) / len(s4_results) * 100
    else:
        s4_avg = 0
        s4_win = 0

    if len(s7_results) > 0:
        s7_avg = np.mean([r["ret"] for r in s7_results]) * 100
        s7_win = sum(1 for r in s7_results if r["ret"] > 0) / len(s7_results) * 100
    else:
        s7_avg = 0
        s7_win = 0

    s1_results = [r for r in results["S1"] if low <= r["open_change"] < high]
    s1_avg = np.mean([r["ret"] for r in s1_results]) * 100 if len(s1_results) > 0 else 0

    count = len([s for s in signals if low <= s["open_change"] < high])

    print(
        f"{group_name:<12} {count:>5} {s1_avg:>7.2f}% {s4_avg:>7.2f}% {s7_avg:>7.2f}% {s4_win:>7.2f}% {s7_win:>7.2f}%"
    )

print("\n" + "=" * 80)
print("第六部分：可执行性与推荐")
print("=" * 80)

exec_analysis = {
    "S1": {"exec": True, "diff": "最容易", "reason": "时间明确"},
    "S2": {"exec": True, "diff": "容易", "reason": "次日开盘"},
    "S3": {"exec": True, "diff": "容易", "reason": "次日收盘"},
    "S4": {"exec": True, "diff": "中等", "reason": "需条件单"},
    "S5": {"exec": True, "diff": "较难", "reason": "触发率低"},
    "S6": {"exec": True, "diff": "中等", "reason": "判断涨停"},
    "S7": {"exec": False, "diff": "不可执行", "reason": "未来函数"},
}

print("\n可执行性评估:")
for rule_id in ["S1", "S2", "S3", "S4", "S5", "S6", "S7"]:
    if rule_id in summary:
        a = exec_analysis[rule_id]
        status = "✓" if a["exec"] else "✗"
        print(
            f"  {rule_id} {summary[rule_id]['name']:<18}: {status} ({a['diff']}) - {a['reason']}"
        )

exec_rules = [(k, v) for k, v in summary.items() if exec_analysis[k]["exec"]]
sorted_exec = sorted(exec_rules, key=lambda x: x[1]["calmar"], reverse=True)

print("\n按卡玛排序（可执行规则）:")
for i, (rid, s) in enumerate(sorted_exec[:3], 1):
    print(
        f"  {i}. {s['name']}: 卡玛={s['calmar']:.2f}, 年化={s['ann_ret']:.2f}%, 胜率={s['win_rate'] * 100:.1f}%"
    )

if len(sorted_exec) > 0:
    rec_id, rec = sorted_exec[0]
    print(f"\n【主推荐】: {rec['name']}")
    print(f"  卡玛比率: {rec['calmar']:.2f}")
    print(f"  年化收益: {rec['ann_ret']:.2f}%")
    print(f"  胜率: {rec['win_rate'] * 100:.2f}%")
    print(f"  平均收益: {rec['avg_ret']:.2f}%")
    print(f"  最大回撤: {rec['dd']:.2f}%")
    print(f"  交易次数: {rec['count']}")

print("\n" + "=" * 80)
print("Go / Watch / No-Go")
print("=" * 80)

best_calmar = sorted_exec[0][1]["calmar"] if len(sorted_exec) > 0 else 0
best_win_rate = sorted_exec[0][1]["win_rate"] if len(sorted_exec) > 0 else 0

if best_calmar > 1.5 and best_win_rate > 0.5:
    status = "Go ✓"
    reason = f"卡玛{best_calmar:.2f}>1.5，胜率{best_win_rate * 100:.1f}%>50%"
elif best_calmar > 1.0 or best_win_rate > 0.5:
    status = "Watch ⚠️"
    reason = f"卡玛{best_calmar:.2f}或胜率{best_win_rate * 100:.1f}%表现一般"
else:
    status = "No-Go ✗"
    reason = f"卡玛{best_calmar:.2f}，胜率{best_win_rate * 100:.1f}%不达标"

print(f"\n判定: {status}")
print(f"理由: {reason}")

if rec_id in summary and summary[rec_id]["so_count"] > 0:
    print(f"\n样本外验证:")
    print(f"  交易数: {summary[rec_id]['so_count']}次")
    print(f"  胜率: {summary[rec_id]['so_win'] * 100:.2f}%")
    print(f"  平均收益: {summary[rec_id]['so_avg']:.2f}%")

    if summary[rec_id]["so_win"] > 0.5:
        print(f"  判定: ✓ 样本外稳定")
    else:
        print(f"  判定: ⚠️ 需关注")

print("\n" + "=" * 80)
print("测试完成")
print("=" * 80)

print(f"\n总结:")
print(f"  - 测试区间: {test_start_date} 至 {test_end_date}")
print(f"  - 信号总数: {len(signals)}个")
print(f"  - 有效信号: {len(results['S1'])}个")
print(f"  - 开盘范围: -1% ~ +2%")
print(f"  - 判定: {status}")
print(f"  - 推荐: {rec['name'] if len(sorted_exec) > 0 else 'N/A'}")
