from jqdata import *
import numpy as np
import pandas as pd
from datetime import datetime, timedelta
import json

print("=" * 60)
print("任务05：主线连亏期与停手机制研究")
print("=" * 60)

start_date = "2024-01-01"
end_date = "2025-03-28"
print(f"研究区间: {start_date} 至 {end_date}")

trade_days = list(get_trade_days(start_date, end_date))
print(f"交易日总数: {len(trade_days)}")

trades = []
equity_curve = [100000]
dates_recorded = []

print("\n阶段1: 模拟主线交易序列...")

for i in range(1, len(trade_days)):
    date = trade_days[i]
    prev_date = trade_days[i - 1]
    date_str = str(date)

    if i % 30 == 0:
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
                }
            )

            equity = equity_curve[-1] * (1 + daily_return)
            equity_curve.append(equity)
            dates_recorded.append(date_str)

    except Exception as e:
        pass

print(f"\n交易总数: {len(trades)}")

if len(trades) == 0:
    print("警告: 未获取到任何交易数据")
    trades = []

print("\n阶段2: 统计连续亏损分布...")

if trades:
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
                        "start_idx": len(trades) - current_loss_count - 1,
                    }
                )
            current_loss_count = 0
            current_loss_sum = 0.0

    if current_loss_count > 0:
        consecutive_losses.append(
            {
                "count": current_loss_count,
                "sum_pct": current_loss_sum,
                "start_idx": len(trades) - current_loss_count - 1,
            }
        )

    print(f"连亏事件数: {len(consecutive_losses)}")

    if consecutive_losses:
        max_consecutive_loss = max([x["count"] for x in consecutive_losses])
        avg_consecutive_loss = np.mean([x["count"] for x in consecutive_losses])
        print(f"最大连亏笔数: {max_consecutive_loss}")
        print(f"平均连亏笔数: {avg_consecutive_loss:.2f}")

        loss_distribution = {}
        for loss_event in consecutive_losses:
            cnt = loss_event["count"]
            if cnt not in loss_distribution:
                loss_distribution[cnt] = 0
            loss_distribution[cnt] += 1

        print("\n连亏笔数分布:")
        for cnt in sorted(loss_distribution.keys()):
            print(f"  连亏{cnt}笔: {loss_distribution[cnt]}次")

print("\n阶段3: 计算回撤区间...")

if equity_curve and len(equity_curve) > 1:
    peak = equity_curve[0]
    max_drawdown_pct = 0.0
    drawdown_periods = []
    current_dd_start = None

    for i, equity in enumerate(equity_curve):
        if equity > peak:
            peak = equity
            if current_dd_start is not None:
                dd_end_idx = i - 1
                dd_days = dd_end_idx - current_dd_start + 1
                drawdown_periods.append(
                    {
                        "start_idx": current_dd_start,
                        "end_idx": dd_end_idx,
                        "days": dd_days,
                        "max_dd_pct": max_drawdown_pct,
                    }
                )
                current_dd_start = None
                max_drawdown_pct = 0.0

        dd_pct = (peak - equity) / peak * 100

        if dd_pct > 0 and current_dd_start is None:
            current_dd_start = i

        if dd_pct > max_drawdown_pct:
            max_drawdown_pct = dd_pct

    if current_dd_start is not None:
        drawdown_periods.append(
            {
                "start_idx": current_dd_start,
                "end_idx": len(equity_curve) - 1,
                "days": len(equity_curve) - current_dd_start,
                "max_dd_pct": max_drawdown_pct,
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

        for dd in severe_drawdowns[:5]:
            start_date_dd = (
                dates_recorded[dd["start_idx"]]
                if dd["start_idx"] < len(dates_recorded)
                else "N/A"
            )
            print(f"  {start_date_dd}: 回撤{dd['max_dd_pct']:.2f}%, 持续{dd['days']}天")

print("\n阶段4: 统计坏月份分布...")

if trades:
    monthly_returns = {}
    for trade in trades:
        month_key = trade["date"][:7]
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

    if bad_months:
        print("\n最差月份:")
        sorted_bad_months = sorted(bad_months.items(), key=lambda x: x[1]["total_pct"])[
            :5
        ]
        for month, data in sorted_bad_months:
            print(
                f"  {month}: 月度收益{data['total_pct']:.2f}%, 交易{data['trade_count']}次, 胜率{data['win_rate']:.1f}%"
            )

print("\n阶段5: 测试停手机制...")


def apply_pause_mechanism(trades, pause_rule):
    paused_trades = []
    pause_counter = 0
    consecutive_losses = 0
    recent_10_returns = []
    half_position_mode = False

    for i, trade in enumerate(trades):
        if pause_counter > 0:
            pause_counter -= 1
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

        elif pause_rule == "pause_4_5":
            if consecutive_losses >= 4:
                pause_counter = 5
                consecutive_losses = 0

        elif pause_rule == "half_position_neg_10":
            if len(recent_10_returns) == 10:
                sum_recent = sum(recent_10_returns)
                if sum_recent < 0:
                    half_position_mode = True
                else:
                    half_position_mode = False

    return paused_trades


def calculate_metrics(trades_list):
    if not trades_list:
        return None

    returns = [t["effective_return_pct"] for t in trades_list]

    total_return = sum(returns)
    avg_return = np.mean(returns)
    win_rate = sum(1 for r in returns if r > 0) / len(returns) * 100

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
        "win_rate": win_rate,
        "max_drawdown_pct": max_dd,
        "calmar_ratio": calmar,
        "trade_count": len(returns),
        "final_equity": final_equity,
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
    else:
        test_trades = apply_pause_mechanism(trades, rule_key)

    metrics = calculate_metrics(test_trades)

    if metrics:
        results_comparison[rule_key] = metrics
        print(f"  总收益: {metrics['total_return_pct']:.2f}%")
        print(f"  最大回撤: {metrics['max_drawdown_pct']:.2f}%")
        print(f"  卡玛比率: {metrics['calmar_ratio']:.2f}")
        print(f"  胜率: {metrics['win_rate']:.1f}%")
        print(f"  交易次数: {metrics['trade_count']}")

        skipped = len(trades) - metrics["trade_count"]
        print(f"  休息天数(跳过交易): {skipped}")

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

if "no_pause" in results_comparison and "pause_3_3" in results_comparison:
    baseline = results_comparison["no_pause"]
    pause3 = results_comparison["pause_3_3"]

    dd_improve = (
        (baseline["max_drawdown_pct"] - pause3["max_drawdown_pct"])
        / baseline["max_drawdown_pct"]
        * 100
    )
    return_damage = (
        (baseline["total_return_pct"] - pause3["total_return_pct"])
        / baseline["total_return_pct"]
        * 100
    )

    print(f"\n1. 连亏3停3天:")
    print(f"   回撤改善: {dd_improve:.1f}%")
    print(f"   收益损失: {return_damage:.1f}%")
    print(f"   休息天数: {len(trades) - pause3['trade_count']}天")

    if dd_improve > 20 and return_damage < 20:
        print("   结论: ✓ 值得实施")
    elif dd_improve > 10 and return_damage < 30:
        print("   结论: ? 可考虑")
    else:
        print("   结论: ✗ 不推荐")

if "no_pause" in results_comparison and "pause_4_5" in results_comparison:
    baseline = results_comparison["no_pause"]
    pause4 = results_comparison["pause_4_5"]

    dd_improve = (
        (baseline["max_drawdown_pct"] - pause4["max_drawdown_pct"])
        / baseline["max_drawdown_pct"]
        * 100
    )
    return_damage = (
        (baseline["total_return_pct"] - pause4["total_return_pct"])
        / baseline["total_return_pct"]
        * 100
    )

    print(f"\n2. 连亏4停5天:")
    print(f"   回撤改善: {dd_improve:.1f}%")
    print(f"   收益损失: {return_damage:.1f}%")
    print(f"   休息天数: {len(trades) - pause4['trade_count']}天")

    if dd_improve > 25 and return_damage < 15:
        print("   结论: ✓ 值得实施")
    elif return_damage > 30:
        print("   结论: ✗ 过度伤害收益")
    else:
        print("   结论: ? 可考虑")

if "no_pause" in results_comparison and "half_position_neg_10" in results_comparison:
    baseline = results_comparison["no_pause"]
    half_pos = results_comparison["half_position_neg_10"]

    dd_improve = (
        (baseline["max_drawdown_pct"] - half_pos["max_drawdown_pct"])
        / baseline["max_drawdown_pct"]
        * 100
    )
    return_damage = (
        (baseline["total_return_pct"] - half_pos["total_return_pct"])
        / baseline["total_return_pct"]
        * 100
    )

    print(f"\n3. 近10笔转负半仓:")
    print(f"   回撤改善: {dd_improve:.1f}%")
    print(f"   收益损失: {return_damage:.1f}%")
    print(f"   半仓天数: {len(trades) - half_pos['trade_count']}天")

    if dd_improve > 15 and return_damage < 25:
        print("   结论: ✓ 可辅助使用")
    else:
        print("   结论: ? 效果不明显")

best_mechanism = None
best_score = -999

for rule_key in ["pause_3_3", "pause_4_5", "half_position_neg_10"]:
    if rule_key in results_comparison:
        m = results_comparison[rule_key]
        score = m["calmar_ratio"] - (len(trades) - m["trade_count"]) * 0.01
        if score > best_score:
            best_score = score
            best_mechanism = rule_key

print("\n" + "=" * 60)
print("最终推荐")
print("=" * 60)

if best_mechanism:
    print(f"\n最优停手机制: {pause_rules[best_mechanism]}")

    if best_mechanism == "pause_3_3":
        print("\n实施建议:")
        print("  1. 连亏3笔触发停手")
        print("  2. 停手期间为3个交易日")
        print("  3. 盘中可执行: 连续亏损计数即可判断")
        print("  4. 规则简单: 仅需记录连亏笔数")

    elif best_mechanism == "pause_4_5":
        print("\n实施建议:")
        print("  1. 连亏4笔触发停手")
        print("  2. 停手期间为5个交易日")
        print("  3. 更保守,适合风险厌恶型")
        print("  4. 注意:收益损失较大")

    elif best_mechanism == "half_position_neg_10":
        print("\n实施建议:")
        print("  1. 近10笔累计收益转负触发")
        print("  2. 半仓运行而非全停")
        print("  3. 保持参与,降低风险")
        print("  4. 可与连亏停手配合使用")

print("\n是否建议实装:")
if best_mechanism in ["pause_3_3", "pause_4_5"]:
    print("  ✓ 建议实装 - 能明显减少回撤尾部")
else:
    print("  ? 视实盘表现决定")

print("\n" + "=" * 60)
print("研究完成")
print("=" * 60)

result_data = {
    "trades_count": len(trades),
    "trades": trades[:20] if trades else [],
    "consecutive_losses_distribution": {},
    "drawdown_periods": [],
    "bad_months": {},
    "pause_mechanism_comparison": results_comparison,
    "best_mechanism": best_mechanism,
    "recommendation": {
        "mechanism": pause_rules.get(best_mechanism, "无"),
        "dd_improve_pct": 0,
        "return_damage_pct": 0,
        "implentable": best_mechanism in ["pause_3_3", "pause_4_5"],
    },
}

if trades and consecutive_losses:
    for loss_event in consecutive_losses:
        cnt = loss_event["count"]
        if cnt not in result_data["consecutive_losses_distribution"]:
            result_data["consecutive_losses_distribution"][cnt] = 0
        result_data["consecutive_losses_distribution"][cnt] += 1

if drawdown_periods:
    result_data["drawdown_periods"] = drawdown_periods[:10]

if bad_months:
    result_data["bad_months"] = {k: v for k, v in list(bad_months.items())[:10]}

if best_mechanism and "no_pause" in results_comparison:
    baseline = results_comparison["no_pause"]
    best = results_comparison[best_mechanism]
    result_data["recommendation"]["dd_improve_pct"] = (
        (baseline["max_drawdown_pct"] - best["max_drawdown_pct"])
        / baseline["max_drawdown_pct"]
        * 100
    )
    result_data["recommendation"]["return_damage_pct"] = (
        (baseline["total_return_pct"] - best["total_return_pct"])
        / baseline["total_return_pct"]
        * 100
    )

result_file = "/Users/fengzhi/Downloads/git/testlixingren/output/mainline_pause_mechanism_result.json"
with open(result_file, "w") as f:
    json.dump(result_data, f, indent=2)

print(f"\n结果已保存至: {result_file}")
