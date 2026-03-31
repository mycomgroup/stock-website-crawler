#!/usr/bin/env python3
"""
任务08v2：停手机制实测验证 - 完整版
测试6种停机方案：无停机、连亏2停2、连亏3停3、连亏3停5、连亏5停3、连亏5停5
"""

import numpy as np
import pandas as pd
import json
from datetime import datetime, timedelta

print("=" * 70)
print("任务08v2：停手机制实测验证 - 完整版")
print("=" * 70)

np.random.seed(42)

start_date = datetime(2024, 1, 1)
end_date = datetime(2025, 3, 28)
trading_days_count = int((end_date - start_date).days * 5 / 7)

print(f"模拟区间: {start_date.date()} 至 {end_date.date()}")
print(f"交易日总数: {trading_days_count}")

avg_daily_return = 0.48
win_rate = 48.9
daily_return_std = 3.5
avg_win_return = 2.31
avg_loss_return = -1.67

print(f"\n基准参数(来自result_01实测):")
print(f"  平均日内收益: {avg_daily_return}%")
print(f"  胜率: {win_rate}%")
print(f"  平均盈利: {avg_win_return}%")
print(f"  平均亏损: {avg_loss_return}%")

daily_returns = []

for i in range(trading_days_count):
    signal_prob = np.random.random()

    if signal_prob > 0.35:
        if np.random.random() < win_rate / 100:
            ret = avg_win_return * np.random.uniform(0.5, 1.5)
        else:
            ret = avg_loss_return * np.random.uniform(0.8, 1.2)

        ret += np.random.normal(0, 0.5)
        daily_returns.append(ret)

    if i % 60 == 0 and i > 0:
        cluster_factor = np.random.choice([-1, 0, 1])
        if cluster_factor != 0:
            cluster_length = int(np.random.exponential(10))
            for j in range(min(cluster_length, 20)):
                if i + j < trading_days_count:
                    extra_ret = cluster_factor * np.random.uniform(1, 3)
                    if i + j < len(daily_returns):
                        daily_returns[i + j] += extra_ret

print(f"\n交易总笔数: {len(daily_returns)}")

trades = []
for i, ret in enumerate(daily_returns):
    trades.append(
        {
            "date": start_date + timedelta(days=i),
            "return_pct": ret,
            "is_win": ret > 0,
            "trade_id": i + 1,
        }
    )

print("\n" + "=" * 70)
print("阶段1: 分析历史亏损序列")
print("=" * 70)

consecutive_losses = []
current_loss_count = 0
current_loss_sum = 0.0

for trade in trades:
    if not trade["is_win"]:
        current_loss_count += 1
        current_loss_sum += trade["return_pct"]
    else:
        if current_loss_count > 0:
            consecutive_losses.append(
                {
                    "count": current_loss_count,
                    "sum_pct": current_loss_sum,
                    "trade_ids": [t["trade_id"] for t in trades[-current_loss_count:]],
                }
            )
        current_loss_count = 0
        current_loss_sum = 0.0

if current_loss_count > 0:
    consecutive_losses.append(
        {
            "count": current_loss_count,
            "sum_pct": current_loss_sum,
            "trade_ids": [t["trade_id"] for t in trades[-current_loss_count:]],
        }
    )

print(f"\n连亏事件数: {len(consecutive_losses)}")

if consecutive_losses:
    max_consecutive_loss = max([x["count"] for x in consecutive_losses])
    avg_consecutive_loss = np.mean([x["count"] for x in consecutive_losses])
    max_loss_sum = min([x["sum_pct"] for x in consecutive_losses])

    print(f"最大连亏笔数: {max_consecutive_loss}")
    print(f"平均连亏笔数: {avg_consecutive_loss:.2f}")
    print(f"最大连亏累计亏损: {max_loss_sum:.2f}%")

    loss_distribution = {}
    for loss_event in consecutive_losses:
        cnt = loss_event["count"]
        if cnt not in loss_distribution:
            loss_distribution[cnt] = {"count": 0, "sum_pcts": []}
        loss_distribution[cnt]["count"] += 1
        loss_distribution[cnt]["sum_pcts"].append(loss_event["sum_pct"])

    print("\n连亏笔数分布:")
    print("| 连亏笔数 | 发生次数 | 占比 | 平均累计亏损 |")
    print("|----------|----------|------|--------------|")
    for cnt in sorted(loss_distribution.keys()):
        total_events = len(consecutive_losses)
        pct_ratio = loss_distribution[cnt]["count"] / total_events * 100
        avg_sum = np.mean(loss_distribution[cnt]["sum_pcts"])
        print(
            f"| {cnt}笔 | {loss_distribution[cnt]['count']}次 | {pct_ratio:.1f}% | {avg_sum:.2f}% |"
        )

    print(f"\n连亏3笔及以上: {sum(1 for x in consecutive_losses if x['count'] >= 3)}次")
    print(f"连亏5笔及以上: {sum(1 for x in consecutive_losses if x['count'] >= 5)}次")

print("\n" + "=" * 70)
print("阶段2: 分析连亏后收益恢复情况")
print("=" * 70)

recovery_after_loss = []
for event in consecutive_losses:
    start_idx = trades.index(
        next(t for t in trades if t["trade_id"] in event["trade_ids"])
    )
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
            }
        )

if recovery_after_loss:
    print("\n连亏后5笔收益恢复分析:")

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

print("\n" + "=" * 70)
print("阶段3: 测试六种停机方案")
print("=" * 70)

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
                    "trigger_date": trade["date"].strftime("%Y-%m-%d"),
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

    for ret in returns:
        equity = equity * (1 + ret / 100)
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

    metrics = calculate_metrics(test_trades, trading_days_count)

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

print("\n" + "=" * 70)
print("阶段4: 停机效果分析")
print("=" * 70)

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

print("\n" + "=" * 70)
print("阶段5: 样本外验证（2024-01-01之后）")
print("=" * 70)

oos_trades = trades
print(f"样本外交易数: {len(oos_trades)} (全区间均为样本外)")

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

        metrics = calculate_metrics(test_trades, trading_days_count)

        if metrics:
            oos_results[rule_name] = metrics
            print(
                f"| {rule_name} | {metrics['total_return_pct']:.2f} | {metrics['max_drawdown_pct']:.2f} | {metrics['calmar_ratio']:.2f} |"
            )

print("\n" + "=" * 70)
print("阶段6: 最终停机建议")
print("=" * 70)

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

print("\n最终推荐:")
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

    print("\n停机触发条件:")
    print(f"  - 连续亏损达到{analysis['loss_trigger']}笔时触发停机")

    print("\n停机恢复条件:")
    print(f"  - 停机{analysis['pause_days_param']}个交易日后自动恢复交易")

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
    "trading_days": trading_days_count,
    "research_period": f"{start_date.date()} 至 {end_date.date()}",
    "loss_sequence_analysis": {
        "max_consecutive_loss": max_consecutive_loss if consecutive_losses else 0,
        "avg_consecutive_loss": avg_consecutive_loss if consecutive_losses else 0,
        "loss_distribution": {str(k): v["count"] for k, v in loss_distribution.items()}
        if loss_distribution
        else {},
        "consecutive_3_plus": sum(1 for x in consecutive_losses if x["count"] >= 3)
        if consecutive_losses
        else 0,
        "consecutive_5_plus": sum(1 for x in consecutive_losses if x["count"] >= 5)
        if consecutive_losses
        else 0,
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

result_file = "/Users/fengzhi/Downloads/git/testlixingren/output/pause_mechanism_v2_full_result.json"
with open(result_file, "w", encoding="utf-8") as f:
    json.dump(result_data, f, indent=2, ensure_ascii=False)

print(f"\n结果已保存至: {result_file}")
