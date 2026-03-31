#!/usr/bin/env python3
import numpy as np
import pandas as pd
import json
from datetime import datetime, timedelta

print("=" * 60)
print("任务05：主线连亏期与停手机制研究 (本地模拟)")
print("=" * 60)

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

print(f"\n基准参数(来自result_01):")
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

print("\n阶段2: 统计连续亏损分布...")

consecutive_losses = []
current_loss_count = 0
current_loss_sum = 0.0

for i, trade in enumerate(trades):
    if not trade["is_win"]:
        current_loss_count += 1
        current_loss_sum += trade["return_pct"]
    else:
        if current_loss_count > 0:
            start_idx = i - current_loss_count
            end_idx = i
            consecutive_losses.append(
                {
                    "count": current_loss_count,
                    "sum_pct": current_loss_sum,
                    "trade_ids": [t["trade_id"] for t in trades[start_idx:end_idx]],
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

print(f"连亏事件数: {len(consecutive_losses)}")

if consecutive_losses:
    max_consecutive_loss = max([x["count"] for x in consecutive_losses])
    avg_consecutive_loss = np.mean([x["count"] for x in consecutive_losses])
    max_loss_sum = min([x["sum_pct"] for x in consecutive_losses])

    print(f"最大连亏笔数: {max_consecutive_loss}")
    print(f"平均连亏笔数: {avg_consecutive_loss:.2f}")
    print(f"最大连亏累计亏损: {abs(max_loss_sum):.2f}%")

    loss_distribution = {}
    for loss_event in consecutive_losses:
        cnt = loss_event["count"]
        if cnt not in loss_distribution:
            loss_distribution[cnt] = 0
        loss_distribution[cnt] += 1

    print("\n连亏笔数分布:")
    for cnt in sorted(loss_distribution.keys()):
        print(
            f"  连亏{cnt}笔: {loss_distribution[cnt]}次 (占比{loss_distribution[cnt] / len(consecutive_losses) * 100:.1f}%)"
        )

print("\n阶段3: 计算回撤区间...")

equity_curve = [100000]
peak = 100000
max_drawdown_pct = 0.0
drawdown_periods = []
current_dd_start = None
current_dd_peak = peak

for i, trade in enumerate(trades):
    equity = equity_curve[-1] * (1 + trade["return_pct"] / 100)
    equity_curve.append(equity)

    if equity > peak:
        if current_dd_start is not None:
            drawdown_periods.append(
                {
                    "start_trade": current_dd_start,
                    "end_trade": i,
                    "trades_count": i - current_dd_start,
                    "max_dd_pct": max_drawdown_pct,
                    "peak_equity": current_dd_peak,
                    "bottom_equity": min(equity_curve[current_dd_start : i + 1]),
                }
            )
            current_dd_start = None
            max_drawdown_pct = 0.0

        peak = equity
        current_dd_peak = peak

    dd_pct = (peak - equity) / peak * 100

    if dd_pct > 0 and current_dd_start is None:
        current_dd_start = i
        current_dd_peak = peak

    if dd_pct > max_drawdown_pct:
        max_drawdown_pct = dd_pct

if current_dd_start is not None:
    drawdown_periods.append(
        {
            "start_trade": current_dd_start,
            "end_trade": len(trades),
            "trades_count": len(trades) - current_dd_start,
            "max_dd_pct": max_drawdown_pct,
            "peak_equity": current_dd_peak,
            "bottom_equity": min(equity_curve[current_dd_start:]),
        }
    )

overall_max_dd = (
    max([x["max_dd_pct"] for x in drawdown_periods]) if drawdown_periods else 0
)

print(f"整体最大回撤: {overall_max_dd:.2f}%")
print(f"回撤区间数: {len(drawdown_periods)}")

if drawdown_periods:
    severe_drawdowns = [x for x in drawdown_periods if x["max_dd_pct"] > 5]
    print(f"严重回撤区间(>5%): {len(severe_drawdowns)}次")

    print("\n前5次严重回撤详情:")
    for dd in severe_drawdowns[:5]:
        print(
            f"  第{dd['start_trade'] + 1}笔起: 回撤{dd['max_dd_pct']:.2f}%, 持续{dd['trades_count']}笔交易"
        )

    extreme_drawdowns = [x for x in drawdown_periods if x["max_dd_pct"] > 10]
    print(f"\n极端回撤区间(>10%): {len(extreme_drawdowns)}次")
    if extreme_drawdowns:
        for dd in extreme_drawdowns:
            print(f"  第{dd['start_trade'] + 1}笔起: 回撤{dd['max_dd_pct']:.2f}%")

print("\n阶段4: 统计坏月份分布...")

monthly_returns = {}
for trade in trades:
    month_key = trade["date"].strftime("%Y-%m")
    if month_key not in monthly_returns:
        monthly_returns[month_key] = []
    monthly_returns[month_key].append(trade["return_pct"])

monthly_summary = {}
for month, returns in monthly_returns.items():
    monthly_summary[month] = {
        "total_pct": sum(returns),
        "avg_pct": np.mean(returns),
        "trade_count": len(returns),
        "win_rate": sum(1 for r in returns if r > 0) / len(returns) * 100,
    }

bad_months = {m: v for m, v in monthly_summary.items() if v["total_pct"] < 0}

print(f"总月份数: {len(monthly_summary)}")
print(f"坏月份数: {len(bad_months)}")
print(f"坏月份占比: {len(bad_months) / len(monthly_summary) * 100:.1f}%")

if bad_months:
    print("\n最差月份:")
    sorted_bad_months = sorted(bad_months.items(), key=lambda x: x[1]["total_pct"])[:5]
    for month, data in sorted_bad_months:
        print(
            f"  {month}: 月度收益{data['total_pct']:.2f}%, 交易{data['trade_count']}笔, 胜率{data['win_rate']:.1f}%"
        )

    worst_month = sorted_bad_months[0]
    print(f"\n最差单月: {worst_month[0]}, 亏损{worst_month[1]['total_pct']:.2f}%")

print("\n阶段5: 测试停手机制...")


def apply_pause_mechanism(trades, pause_rule):
    paused_trades = []
    pause_counter = 0
    consecutive_losses = 0
    recent_10_returns = []
    half_position_mode = False
    pause_events = []

    for i, trade in enumerate(trades):
        if pause_counter > 0:
            pause_counter -= 1
            pause_events.append({"trade_id": trade["trade_id"], "paused": True})
            continue

        effective_return = trade["return_pct"]

        if half_position_mode:
            effective_return = trade["return_pct"] * 0.5

        paused_trades.append(
            {
                **trade,
                "effective_return_pct": effective_return,
                "half_position": half_position_mode,
            }
        )

        recent_10_returns.append(effective_return)
        if len(recent_10_returns) > 10:
            recent_10_returns.pop(0)

        if not trade["is_win"]:
            consecutive_losses += 1
        else:
            consecutive_losses = 0

        if pause_rule == "pause_3_3":
            if consecutive_losses >= 3:
                pause_counter = 3
                consecutive_losses = 0
                pause_events.append(
                    {
                        "trigger_trade": trade["trade_id"],
                        "rule": "连亏3笔",
                        "pause_days": 3,
                    }
                )

        elif pause_rule == "pause_4_5":
            if consecutive_losses >= 4:
                pause_counter = 5
                consecutive_losses = 0
                pause_events.append(
                    {
                        "trigger_trade": trade["trade_id"],
                        "rule": "连亏4笔",
                        "pause_days": 5,
                    }
                )

        elif pause_rule == "half_position_neg_10":
            if len(recent_10_returns) == 10:
                sum_recent = sum(recent_10_returns)
                if sum_recent < 0 and not half_position_mode:
                    half_position_mode = True
                    pause_events.append(
                        {
                            "trigger_trade": trade["trade_id"],
                            "rule": "近10笔转负",
                            "action": "进入半仓",
                        }
                    )
                elif sum_recent >= 0 and half_position_mode:
                    half_position_mode = False
                    pause_events.append(
                        {
                            "trigger_trade": trade["trade_id"],
                            "rule": "近10笔转正",
                            "action": "恢复正常仓位",
                        }
                    )

    return paused_trades, pause_events


def calculate_metrics(trades_list):
    if not trades_list:
        return None

    returns = [t["effective_return_pct"] for t in trades_list]

    total_return = sum(returns)
    avg_return = np.mean(returns)
    win_rate_pct = sum(1 for r in returns if r > 0) / len(returns) * 100

    equity = 100000
    peak = equity
    max_dd = 0
    equity_curve = [equity]

    for ret in returns:
        equity = equity * (1 + ret / 100)
        equity_curve.append(equity)
        if equity > peak:
            peak = equity
        dd = (peak - equity) / peak * 100
        if dd > max_dd:
            max_dd = dd

    final_equity = 100000 * (1 + total_return / 100)

    trading_days_per_year = 250
    years = (
        len(returns) / trading_days_per_year
        if len(returns) > trading_days_per_year
        else 1
    )
    annual_return = total_return / years

    calmar = annual_return / max_dd if max_dd > 0 else 999

    return {
        "total_return_pct": total_return,
        "avg_return_pct": avg_return,
        "win_rate": win_rate_pct,
        "max_drawdown_pct": max_dd,
        "calmar_ratio": calmar,
        "trade_count": len(returns),
        "final_equity": final_equity,
        "equity_curve": equity_curve,
    }


pause_rules = {
    "no_pause": "无停手机制",
    "pause_3_3": "连亏3笔停3天",
    "pause_4_5": "连亏4笔停5天",
    "half_position_neg_10": "近10笔收益转负则半仓",
}

results_comparison = {}

print("\n测试四种机制:")
for rule_key, rule_name in pause_rules.items():
    print(f"\n测试: {rule_name}")

    if rule_key == "no_pause":
        test_trades = [
            {**t, "effective_return_pct": t["return_pct"], "half_position": False}
            for t in trades
        ]
        pause_events = []
    else:
        test_trades, pause_events = apply_pause_mechanism(trades, rule_key)

    metrics = calculate_metrics(test_trades)

    if metrics:
        results_comparison[rule_key] = metrics
        print(f"  总收益: {metrics['total_return_pct']:.2f}%")
        print(f"  最大回撤: {metrics['max_drawdown_pct']:.2f}%")
        print(f"  卡玛比率: {metrics['calmar_ratio']:.2f}")
        print(f"  胜率: {metrics['win_rate']:.1f}%")
        print(f"  交易次数: {metrics['trade_count']}")
        print(f"  最终资金: {metrics['final_equity']:.0f}元")

        skipped = len(trades) - metrics["trade_count"]
        print(f"  休息天数(跳过交易): {skipped}")

        if pause_events and rule_key != "no_pause":
            print(f"  停手触发次数: {len([e for e in pause_events if 'rule' in e])}")

print("\n" + "=" * 60)
print("对比总结")
print("=" * 60)

print("\n| 停手机制 | 总收益% | 最大回撤% | 卡玛比 | 胜率% | 交易数 | 休息天数 |")
print("|----------|---------|-----------|--------|-------|--------|----------|")

for rule_key, rule_name in pause_rules.items():
    if rule_key in results_comparison:
        m = results_comparison[rule_key]
        skipped = len(trades) - m["trade_count"]
        print(
            f"| {rule_name} | {m['total_return_pct']:.2f} | {m['max_drawdown_pct']:.2f} | {m['calmar_ratio']:.2f} | {m['win_rate']:.1f} | {m['trade_count']} | {skipped} |"
        )

print("\n关键发现:")

baseline = results_comparison["no_pause"]

recommendations = {}

for rule_key in ["pause_3_3", "pause_4_5", "half_position_neg_10"]:
    if rule_key in results_comparison:
        test_m = results_comparison[rule_key]

        dd_improve = (
            (baseline["max_drawdown_pct"] - test_m["max_drawdown_pct"])
            / baseline["max_drawdown_pct"]
            * 100
        )
        return_damage = (
            (baseline["total_return_pct"] - test_m["total_return_pct"])
            / baseline["total_return_pct"]
            * 100
        )
        calmar_improve = (
            (test_m["calmar_ratio"] - baseline["calmar_ratio"])
            / baseline["calmar_ratio"]
            * 100
        )

        recommendations[rule_key] = {
            "dd_improve": dd_improve,
            "return_damage": return_damage,
            "calmar_improve": calmar_improve,
            "skipped_days": len(trades) - test_m["trade_count"],
        }

        rule_name = pause_rules[rule_key]

        print(f"\n{rule_name}:")
        print(f"  回撤改善: {dd_improve:.1f}%")
        print(f"  收益损失: {return_damage:.1f}%")
        print(f"  卡玛提升: {calmar_improve:.1f}%")
        print(f"  休息天数: {recommendations[rule_key]['skipped_days']}")

        if dd_improve > 20 and return_damage < 20:
            print("  结论: ✓ 值得实施")
            recommendations[rule_key]["rating"] = "Go"
        elif dd_improve > 10 and return_damage < 30:
            print("  结论: ? 可考虑")
            recommendations[rule_key]["rating"] = "Watch"
        elif return_damage > 40:
            print("  结论: ✗ 过度伤害收益")
            recommendations[rule_key]["rating"] = "No-Go"
        else:
            print("  结论: ~ 效果不明显")
            recommendations[rule_key]["rating"] = "Neutral"

best_mechanism = None
best_score = -999

for rule_key in ["pause_3_3", "pause_4_5", "half_position_neg_10"]:
    if rule_key in results_comparison:
        m = results_comparison[rule_key]
        score = m["calmar_ratio"] - (len(trades) - m["trade_count"]) * 0.005

        if recommendations[rule_key]["rating"] == "Go":
            score += 2
        elif recommendations[rule_key]["rating"] == "Watch":
            score += 1

        if score > best_score:
            best_score = score
            best_mechanism = rule_key

print("\n" + "=" * 60)
print("最终推荐")
print("=" * 60)

if best_mechanism:
    print(f"\n最优停手机制: {pause_rules[best_mechanism]}")

    best_rec = recommendations[best_mechanism]

    print(f"\n实施效果预估:")
    print(f"  回撤改善: {best_rec['dd_improve']:.1f}%")
    print(f"  收益损失: {best_rec['return_damage']:.1f}%")
    print(f"  卡玛提升: {best_rec['calmar_improve']:.1f}%")
    print(f"  年均休息天数: {best_rec['skipped_days'] / 1.3:.1f}天")

    if best_mechanism == "pause_3_3":
        print("\n具体实施建议:")
        print("  1. 连亏3笔触发停手")
        print("  2. 停手期间为3个交易日")
        print("  3. 盘中可执行: 连续亏损计数即可判断")
        print("  4. 规则简单: 仅需记录连亏笔数")
        print("  5. 适用场景: 大多数机会仓策略")
        print("  6. 优势: 平衡回撤控制与收益保留")

    elif best_mechanism == "pause_4_5":
        print("\n具体实施建议:")
        print("  1. 连亏4笔触发停手")
        print("  2. 停手期间为5个交易日")
        print("  3. 更保守,适合风险厌恶型投资者")
        print("  4. 注意:收益损失较大,需权衡")
        print("  5. 适用场景: 大资金或风险厌恶型")
        print("  6. 优势: 回撤控制更强")

    elif best_mechanism == "half_position_neg_10":
        print("\n具体实施建议:")
        print("  1. 近10笔累计收益转负触发")
        print("  2. 半仓运行而非全停")
        print("  3. 保持市场参与,降低风险")
        print("  4. 可与连亏停手配合使用")
        print("  5. 适用场景: 情绪波动期或震荡市")
        print("  6. 优势: 不会完全错过机会")

print("\n是否建议实装:")

go_count = sum(1 for rec in recommendations.values() if rec["rating"] == "Go")
watch_count = sum(1 for rec in recommendations.values() if rec["rating"] == "Watch")

if go_count > 0:
    print(f"  ✓ 建议实装 - 有{go_count}套机制通过评估")
    print("  能明显减少回撤尾部,不严重伤害收益")
elif watch_count > 0:
    print(f"  ? 可考虑实装 - 有{watch_count}套机制值得观察")
    print("  建议实盘小资金测试后决定")
else:
    print("  ✗ 不建议实装 - 所有机制效果不佳")

print("\n组合使用建议:")

if "pause_3_3" in recommendations and recommendations["pause_3_3"]["rating"] == "Go":
    print("  主方案: 连亏3停3天")

    if "half_position_neg_10" in recommendations:
        print("  辅助方案: 可叠加近10笔半仓机制")
        print("  组合效果: 双层风控,进一步降低极端回撤风险")

print("\n" + "=" * 60)
print("研究完成")
print("=" * 60)

result_data = {
    "trades_count": len(trades),
    "trading_days": trading_days_count,
    "baseline_metrics": results_comparison.get("no_pause"),
    "consecutive_losses_distribution": {
        cnt: loss_distribution.get(cnt, 0) for cnt in range(1, 10)
    },
    "max_consecutive_loss": max_consecutive_loss,
    "avg_consecutive_loss": avg_consecutive_loss,
    "overall_max_dd": overall_max_dd,
    "severe_dd_count": len(severe_drawdowns) if drawdown_periods else 0,
    "bad_months_count": len(bad_months),
    "bad_months_ratio": len(bad_months) / len(monthly_summary) * 100,
    "worst_month": sorted(bad_months.items(), key=lambda x: x[1]["total_pct"])[0]
    if bad_months
    else None,
    "pause_mechanism_comparison": {
        k: {
            "total_return_pct": v["total_return_pct"],
            "max_drawdown_pct": v["max_drawdown_pct"],
            "calmar_ratio": v["calmar_ratio"],
            "win_rate": v["win_rate"],
            "trade_count": v["trade_count"],
        }
        for k, v in results_comparison.items()
    },
    "recommendations": recommendations,
    "best_mechanism": best_mechanism,
    "best_mechanism_name": pause_rules.get(best_mechanism, "无"),
    "final_recommendation": {
        "mechanism": pause_rules.get(best_mechanism, "无"),
        "implentable": best_mechanism
        in ["pause_3_3", "pause_4_5", "half_position_neg_10"],
        "dd_improve_pct": recommendations[best_mechanism]["dd_improve"]
        if best_mechanism
        else 0,
        "return_damage_pct": recommendations[best_mechanism]["return_damage"]
        if best_mechanism
        else 0,
        "rating": recommendations[best_mechanism]["rating"]
        if best_mechanism
        else "N/A",
    },
}

result_file = "/Users/fengzhi/Downloads/git/testlixingren/output/mainline_pause_mechanism_result.json"
with open(result_file, "w", encoding="utf-8") as f:
    json.dump(result_data, f, indent=2, ensure_ascii=False)

print(f"\n结果已保存至: {result_file}")
