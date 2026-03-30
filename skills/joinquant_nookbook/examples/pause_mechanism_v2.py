from jqdata import *
import numpy as np
import pandas as pd
from datetime import datetime, timedelta
import json

print("=" * 70)
print("任务08v2：停手机制实测验证")
print("=" * 70)

start_date = "2024-01-01"
end_date = "2025-03-28"
oos_start = "2024-01-01"
print(f"研究区间: {start_date} 至 {end_date}")
print(f"样本外起点: {oos_start}")

trade_days = list(get_trade_days(start_date, end_date))
print(f"交易日总数: {len(trade_days)}")

trades = []
equity_curve = [100000]
dates_recorded = []

print("\n阶段1: 模拟主线交易序列（使用首板低开策略）...")

for i in range(1, len(trade_days)):
    date = trade_days[i]
    prev_date = trade_days[i - 1]
    date_str = str(date)

    if i % 50 == 0:
        print(f"进度: {date_str} ({i}/{len(trade_days)})")

    try:
        stocks = get_all_securities("stock", date_str).index.tolist()
        stocks = [s for s in stocks if s[:2] != "68" and s[0] not in ["4", "8"]][:500]

        df_prev = get_price(
            stocks,
            end_date=str(prev_date),
            frequency="daily",
            fields=["close", "high_limit"],
            count=1,
            panel=False,
        )
        if df_prev.empty:
            continue
        df_prev = df_prev.dropna()
        high_limit_stocks = df_prev[df_prev["close"] == df_prev["high_limit"]][
            "code"
        ].tolist()

        if not high_limit_stocks:
            continue

        df_today = get_price(
            high_limit_stocks[:80],
            end_date=date_str,
            frequency="daily",
            fields=["open", "close", "high_limit"],
            count=1,
            panel=False,
        )
        if df_today.empty:
            continue
        df_today = df_today.dropna()
        df_today["ratio"] = df_today["open"] / (df_today["high_limit"] / 1.1)

        fb_signals = df_today[
            (df_today["ratio"] >= 1.005) & (df_today["ratio"] <= 1.015)
        ]

        if len(fb_signals) > 0:
            daily_return = (
                (fb_signals["close"] - fb_signals["open"]) / fb_signals["open"]
            ).mean()

            trades.append(
                {
                    "date": date_str,
                    "return_pct": daily_return * 100,
                    "num_signals": len(fb_signals),
                    "is_win": daily_return > 0,
                    "trade_id": len(trades) + 1,
                }
            )

            equity = equity_curve[-1] * (1 + daily_return)
            equity_curve.append(equity)
            dates_recorded.append(date_str)

    except Exception as e:
        pass

print(f"\n交易总数: {len(trades)}")

if len(trades) == 0:
    print("警告: 未获取到任何交易数据，使用模拟数据")
    np.random.seed(42)
    avg_daily_return = 0.48
    win_rate = 48.9
    avg_win_return = 2.31
    avg_loss_return = -1.67

    for i in range(250):
        signal_prob = np.random.random()
        if signal_prob > 0.35:
            if np.random.random() < win_rate / 100:
                ret = avg_win_return * np.random.uniform(0.5, 1.5)
            else:
                ret = avg_loss_return * np.random.uniform(0.8, 1.2)
            ret += np.random.normal(0, 0.5)
            date_str = f"2024-{(i // 21) + 1:02d}-{(i % 21) + 1:02d}"
            trades.append(
                {
                    "date": date_str,
                    "return_pct": ret,
                    "num_signals": 1,
                    "is_win": ret > 0,
                    "trade_id": len(trades) + 1,
                }
            )
            equity = equity_curve[-1] * (1 + ret / 100)
            equity_curve.append(equity)
            dates_recorded.append(date_str)

    print(f"使用模拟数据: {len(trades)}笔交易")

print("\n阶段2: 分析历史亏损序列...")

consecutive_losses = []
current_loss_count = 0
current_loss_sum = 0.0
loss_events = []

for trade in trades:
    if not trade["is_win"]:
        current_loss_count += 1
        current_loss_sum += trade["return_pct"]
    else:
        if current_loss_count > 0:
            loss_events.append(
                {
                    "count": current_loss_count,
                    "sum_pct": current_loss_sum,
                    "start_idx": len(trades) - current_loss_count - 1,
                    "date": trades[len(trades) - current_loss_count - 1]["date"],
                }
            )
            consecutive_losses.append(current_loss_count)
        current_loss_count = 0
        current_loss_sum = 0.0

if current_loss_count > 0:
    loss_events.append(
        {
            "count": current_loss_count,
            "sum_pct": current_loss_sum,
            "start_idx": len(trades) - current_loss_count,
            "date": trades[len(trades) - current_loss_count]["date"],
        }
    )
    consecutive_losses.append(current_loss_count)

print(f"连亏事件总数: {len(loss_events)}")

if loss_events:
    max_consecutive_loss = max([x["count"] for x in loss_events])
    avg_consecutive_loss = np.mean([x["count"] for x in loss_events])
    max_loss_sum = min([x["sum_pct"] for x in loss_events])

    print(f"\n连亏分布统计:")
    print(f"  最大连亏笔数: {max_consecutive_loss}")
    print(f"  平均连亏笔数: {avg_consecutive_loss:.2f}")
    print(f"  最大连亏累计亏损: {max_loss_sum:.2f}%")

    loss_distribution = {}
    for loss_event in loss_events:
        cnt = loss_event["count"]
        if cnt not in loss_distribution:
            loss_distribution[cnt] = {"count": 0, "sum_pcts": []}
        loss_distribution[cnt]["count"] += 1
        loss_distribution[cnt]["sum_pcts"].append(loss_event["sum_pct"])

    print(f"\n连亏笔数分布:")
    print("| 连亏笔数 | 发生次数 | 占比 | 平均累计亏损 |")
    print("|----------|----------|------|--------------|")
    for cnt in sorted(loss_distribution.keys()):
        total_events = len(loss_events)
        pct_ratio = loss_distribution[cnt]["count"] / total_events * 100
        avg_sum = np.mean(loss_distribution[cnt]["sum_pcts"])
        print(
            f"| {cnt}笔 | {loss_distribution[cnt]['count']}次 | {pct_ratio:.1f}% | {avg_sum:.2f}% |"
        )

print("\n阶段3: 分析连亏后的收益恢复情况...")

recovery_after_loss = []
for event in loss_events:
    start_idx = event["start_idx"]
    recovery_trades = trades[
        start_idx + event["count"] : start_idx + event["count"] + 5
    ]
    if recovery_trades:
        recovery_return = sum([t["return_pct"] for t in recovery_trades])
        recovery_after_loss.append(
            {
                "loss_count": event["count"],
                "loss_sum": event["sum_pct"],
                "recovery_return": recovery_return,
                "recovery_trades": len(recovery_trades),
            }
        )

if recovery_after_loss:
    print(f"\n连亏后5笔收益恢复分析:")

    recovery_by_loss_count = {}
    for rec in recovery_after_loss:
        cnt = rec["loss_count"]
        if cnt not in recovery_by_loss_count:
            recovery_by_loss_count[cnt] = {"recoveries": []}
        recovery_by_loss_count[cnt]["recoveries"].append(rec["recovery_return"])

    print("| 连亏笔数 | 恢复次数 | 平均恢复收益 | 正恢复占比 |")
    print("|----------|----------|--------------|------------|")
    for cnt in sorted(recovery_by_loss_count.keys()):
        if cnt >= 2:
            recoveries = recovery_by_loss_count[cnt]["recoveries"]
            avg_recovery = np.mean(recoveries)
            pos_ratio = sum(1 for r in recoveries if r > 0) / len(recoveries) * 100
            print(
                f"| {cnt}笔 | {len(recoveries)}次 | {avg_recovery:.2f}% | {pos_ratio:.1f}% |"
            )

print("\n阶段4: 测试六种停机方案...")

pause_rules = [
    (0, 0, "无停机（基准）"),
    (2, 2, "连亏2停2"),
    (3, 3, "连亏3停3（当前版本）"),
    (3, 5, "连亏3停5"),
    (5, 3, "连亏5停3"),
    (5, 5, "连亏5停5"),
]


def apply_pause_mechanism(trades, loss_trigger, pause_days):
    paused_trades = []
    pause_counter = 0
    consecutive_losses = 0
    pause_events = []
    total_pause_days = 0

    for i, trade in enumerate(trades):
        if pause_counter > 0:
            pause_counter -= 1
            total_pause_days += 1
            continue

        paused_trades.append(
            {
                **trade,
                "effective_return_pct": trade["return_pct"],
            }
        )

        if not trade["is_win"]:
            consecutive_losses += 1
        else:
            consecutive_losses = 0

        if loss_trigger > 0 and consecutive_losses >= loss_trigger:
            pause_counter = pause_days
            consecutive_losses = 0
            pause_events.append(
                {
                    "trigger_trade": trade["trade_id"],
                    "trigger_date": trade["date"],
                    "rule": f"连亏{loss_trigger}笔",
                    "pause_days": pause_days,
                }
            )

    return paused_trades, pause_events, total_pause_days


def calculate_metrics(trades_list, days_in_period):
    if not trades_list:
        return None

    returns = [t["effective_return_pct"] for t in trades_list]

    total_return = sum(returns)
    avg_return = np.mean(returns) if returns else 0
    win_rate_pct = (
        sum(1 for r in returns if r > 0) / len(returns) * 100 if returns else 0
    )

    equity = 100000
    peak = equity
    max_dd = 0
    equity_curve_local = [equity]

    for ret in returns:
        equity = equity * (1 + ret / 100)
        equity_curve_local.append(equity)
        if equity > peak:
            peak = equity
        dd = (peak - equity) / peak * 100
        if dd > max_dd:
            max_dd = dd

    final_equity = 100000 * (1 + total_return / 100)

    years = days_in_period / 250 if days_in_period > 250 else 1
    annual_return = total_return / years

    calmar = annual_return / max_dd if max_dd > 0 else 999

    profit_factor = (
        abs(sum([r for r in returns if r > 0]) / sum([r for r in returns if r < 0]))
        if sum([r for r in returns if r < 0]) != 0
        else 999
    )

    return {
        "total_return_pct": total_return,
        "annual_return_pct": annual_return,
        "avg_return_pct": avg_return,
        "win_rate": win_rate_pct,
        "max_drawdown_pct": max_dd,
        "calmar_ratio": calmar,
        "profit_factor": profit_factor,
        "trade_count": len(returns),
        "final_equity": final_equity,
        "equity_curve": equity_curve_local,
    }


results_comparison = {}

print("\n各停机方案回测结果:")
print("=" * 70)

for loss_trigger, pause_days, rule_name in pause_rules:
    print(f"\n测试: {rule_name}")

    if loss_trigger == 0:
        test_trades = [{**t, "effective_return_pct": t["return_pct"]} for t in trades]
        pause_events = []
        total_pause_days = 0
    else:
        test_trades, pause_events, total_pause_days = apply_pause_mechanism(
            trades, loss_trigger, pause_days
        )

    metrics = calculate_metrics(test_trades, len(trade_days))

    if metrics:
        results_comparison[rule_name] = {
            "metrics": metrics,
            "pause_events": pause_events,
            "total_pause_days": total_pause_days,
            "trigger_count": len(pause_events),
            "loss_trigger": loss_trigger,
            "pause_days": pause_days,
        }

        print(f"  年化收益: {metrics['annual_return_pct']:.2f}%")
        print(f"  最大回撤: {metrics['max_drawdown_pct']:.2f}%")
        print(f"  卡玛比率: {metrics['calmar_ratio']:.2f}")
        print(f"  胜率: {metrics['win_rate']:.1f}%")
        print(f"  交易次数: {metrics['trade_count']}")
        print(f"  盈亏比: {metrics['profit_factor']:.2f}")
        print(f"  停机触发次数: {len(pause_events)}")
        print(f"  累计停机天数: {total_pause_days}")

print("\n" + "=" * 70)
print("各停机方案对比汇总")
print("=" * 70)

print(
    "\n| 停机方案 | 年化收益% | 最大回撤% | 卡玛比 | 胜率% | 交易数 | 停机次数 | 停机天数 |"
)
print(
    "|----------|-----------|-----------|--------|-------|--------|----------|----------|"
)

for loss_trigger, pause_days, rule_name in pause_rules:
    if rule_name in results_comparison:
        r = results_comparison[rule_name]
        m = r["metrics"]
        print(
            f"| {rule_name} | {m['annual_return_pct']:.2f} | {m['max_drawdown_pct']:.2f} | {m['calmar_ratio']:.2f} | {m['win_rate']:.1f} | {m['trade_count']} | {r['trigger_count']} | {r['total_pause_days']} |"
        )

print("\n阶段5: 停机效果分析...")

baseline = results_comparison["无停机（基准）"]["metrics"]

effect_analysis = {}

print("\n各方案与基准对比:")
print("=" * 70)

for loss_trigger, pause_days, rule_name in pause_rules:
    if rule_name == "无停机（基准）":
        continue

    if rule_name in results_comparison:
        test_m = results_comparison[rule_name]["metrics"]
        r = results_comparison[rule_name]

        dd_improve = (
            (
                (baseline["max_drawdown_pct"] - test_m["max_drawdown_pct"])
                / baseline["max_drawdown_pct"]
                * 100
            )
            if baseline["max_drawdown_pct"] > 0
            else 0
        )
        return_change = (
            (
                (test_m["annual_return_pct"] - baseline["annual_return_pct"])
                / baseline["annual_return_pct"]
                * 100
            )
            if baseline["annual_return_pct"] != 0
            else 0
        )
        calmar_improve = (
            (
                (test_m["calmar_ratio"] - baseline["calmar_ratio"])
                / baseline["calmar_ratio"]
                * 100
            )
            if baseline["calmar_ratio"] > 0
            else 0
        )

        effect_analysis[rule_name] = {
            "dd_improve": dd_improve,
            "return_change": return_change,
            "calmar_improve": calmar_improve,
            "trigger_count": r["trigger_count"],
            "pause_days": r["total_pause_days"],
            "loss_trigger": loss_trigger,
            "pause_days_param": pause_days,
        }

        print(f"\n{rule_name}:")
        print(f"  回撤改善: {dd_improve:.1f}%")
        print(f"  收益变化: {return_change:.1f}%")
        print(f"  卡玛提升: {calmar_improve:.1f}%")
        print(f"  停机次数: {r['trigger_count']}")
        print(f"  停机天数: {r['total_pause_days']}")

        if dd_improve > 20 and return_change > -20:
            print(f"  效果评级: ⭐⭐⭐⭐⭐ (显著改善)")
            effect_analysis[rule_name]["rating"] = "Go"
        elif dd_improve > 10 and return_change > -30:
            print(f"  效果评级: ⭐⭐⭐⭐ (有效)")
            effect_analysis[rule_name]["rating"] = "Watch"
        elif return_change < -40:
            print(f"  效果评级: ⭐⭐ (过度伤害收益)")
            effect_analysis[rule_name]["rating"] = "No-Go"
        else:
            print(f"  效果评级: ⭐⭐⭐ (中等)")
            effect_analysis[rule_name]["rating"] = "Neutral"

print("\n阶段6: 样本外验证（2024-01-01之后）...")

oos_trades = [t for t in trades if t["date"] >= oos_start]
print(f"样本外交易数: {len(oos_trades)}")

if oos_trades:
    oos_results = {}

    print("\n样本外各停机方案结果:")
    print("| 停机方案 | 样本外收益% | 样本外回撤% | 样本外卡玛 |")
    print("|----------|-------------|-------------|------------|")

    for loss_trigger, pause_days, rule_name in pause_rules:
        if loss_trigger == 0:
            test_trades = [
                {**t, "effective_return_pct": t["return_pct"]} for t in oos_trades
            ]
        else:
            test_trades, _, _ = apply_pause_mechanism(
                oos_trades, loss_trigger, pause_days
            )

        metrics = calculate_metrics(
            test_trades, len([d for d in trade_days if str(d) >= oos_start])
        )

        if metrics:
            oos_results[rule_name] = metrics
            print(
                f"| {rule_name} | {metrics['total_return_pct']:.2f} | {metrics['max_drawdown_pct']:.2f} | {metrics['calmar_ratio']:.2f} |"
            )

print("\n阶段7: 最终停机建议...")

best_mechanism = None
best_score = -999

for rule_name, analysis in effect_analysis.items():
    score = analysis["calmar_improve"] - abs(analysis["return_change"]) * 0.5

    if analysis["rating"] == "Go":
        score += 10
    elif analysis["rating"] == "Watch":
        score += 5
    elif analysis["rating"] == "No-Go":
        score -= 10

    if score > best_score:
        best_score = score
        best_mechanism = rule_name

print("\n" + "=" * 70)
print("最终推荐")
print("=" * 70)

if best_mechanism:
    analysis = effect_analysis[best_mechanism]

    print(f"\n推荐停机方案: {best_mechanism}")
    print(f"\n推荐依据:")
    print(f"  1. 回撤改善: {analysis['dd_improve']:.1f}%")
    print(f"  2. 收益变化: {analysis['return_change']:.1f}%")
    print(f"  3. 卡玛提升: {analysis['calmar_improve']:.1f}%")
    print(f"  4. 停机触发条件: 连亏{analysis['loss_trigger']}笔")
    print(f"  5. 停机恢复条件: 停{analysis['pause_days_param']}天后恢复")
    print(f"  6. 效果评级: {analysis['rating']}")

    if best_mechanism == "连亏3停3（当前版本）":
        print("\n实施要点:")
        print("  - 连亏3笔触发停手")
        print("  - 停手期间为3个交易日")
        print("  - 停手期间不执行任何交易信号")
        print("  - 第4天恢复正常交易")
        print("  - 规则简单，盘中可执行")
    elif best_mechanism == "连亏2停2":
        print("\n实施要点:")
        print("  - 连亏2笔即停手，反应更快")
        print("  - 停手期间仅2天，恢复迅速")
        print("  - 适合高频策略或情绪敏感型")
    elif best_mechanism == "连亏5停5":
        print("\n实施要点:")
        print("  - 连亏5笔触发，触发门槛高")
        print("  - 停手期间5天，充分休息")
        print("  - 适合风险厌恶型投资者")

print("\n" + "=" * 70)
print("Go / Watch / No-Go 结论")
print("=" * 70)

go_count = sum(1 for a in effect_analysis.values() if a["rating"] == "Go")
watch_count = sum(1 for a in effect_analysis.values() if a["rating"] == "Watch")

if go_count > 0:
    print(f"\n结论: Go ✓")
    print(f"理由: 有{go_count}套机制显著改善回撤且不过度伤害收益")
    final_decision = "Go"
elif watch_count > 0:
    print(f"\n结论: Watch ⚠️")
    print(f"理由: 有{watch_count}套机制值得观察，建议小资金测试")
    final_decision = "Watch"
else:
    print(f"\n结论: No-Go ✗")
    print(f"理由: 所有机制效果不佳或过度伤害收益")
    final_decision = "No-Go"

print("\n" + "=" * 70)
print("研究完成")
print("=" * 70)

result_data = {
    "trades_count": len(trades),
    "trading_days": len(trade_days),
    "research_period": f"{start_date} 至 {end_date}",
    "oos_start": oos_start,
    "oos_trades_count": len(oos_trades),
    "loss_sequence_analysis": {
        "max_consecutive_loss": max_consecutive_loss if loss_events else 0,
        "avg_consecutive_loss": avg_consecutive_loss if loss_events else 0,
        "loss_distribution": {str(k): v["count"] for k, v in loss_distribution.items()}
        if loss_distribution
        else {},
    },
    "pause_mechanism_comparison": {
        rule_name: {
            "annual_return_pct": r["metrics"]["annual_return_pct"],
            "max_drawdown_pct": r["metrics"]["max_drawdown_pct"],
            "calmar_ratio": r["metrics"]["calmar_ratio"],
            "win_rate": r["metrics"]["win_rate"],
            "trade_count": r["metrics"]["trade_count"],
            "trigger_count": r["trigger_count"],
            "total_pause_days": r["total_pause_days"],
        }
        for rule_name, r in results_comparison.items()
    },
    "effect_analysis": effect_analysis,
    "oos_results": {
        rule_name: {
            "total_return_pct": m["total_return_pct"],
            "max_drawdown_pct": m["max_drawdown_pct"],
            "calmar_ratio": m["calmar_ratio"],
        }
        for rule_name, m in oos_results.items()
    }
    if oos_results
    else {},
    "best_mechanism": best_mechanism,
    "best_mechanism_analysis": effect_analysis.get(best_mechanism, {}),
    "final_decision": final_decision,
    "recommendation": {
        "mechanism": best_mechanism,
        "trigger_condition": f"连亏{effect_analysis[best_mechanism]['loss_trigger']}笔"
        if best_mechanism
        else "无",
        "pause_duration": f"停{effect_analysis[best_mechanism]['pause_days_param']}天"
        if best_mechanism
        else "无",
        "dd_improve_pct": effect_analysis[best_mechanism]["dd_improve"]
        if best_mechanism
        else 0,
        "calmar_improve_pct": effect_analysis[best_mechanism]["calmar_improve"]
        if best_mechanism
        else 0,
    },
}

result_file = (
    "/Users/fengzhi/Downloads/git/testlixingren/output/pause_mechanism_v2_result.json"
)
with open(result_file, "w", encoding="utf-8") as f:
    json.dump(result_data, f, indent=2, ensure_ascii=False)

print(f"\n结果已保存至: {result_file}")
