from jqdata import *
import numpy as np
import pandas as pd
from datetime import datetime, timedelta
import json

print("=" * 60)
print("任务05：主线连亏期与停手机制 - 聚宽真实回测")
print("=" * 60)

start_date = "2024-01-01"
end_date = "2024-12-31"
print(f"回测区间: {start_date} 至 {end_date}")

trade_days = list(get_trade_days(start_date, end_date))
print(f"交易日总数: {len(trade_days)}")

trades = []
equity_curve = [100000]
dates_recorded = []

print("\n阶段1: 模拟主线交易序列（真实数据）...")

for i in range(1, len(trade_days)):
    date = trade_days[i]
    prev_date = trade_days[i - 1]
    date_str = str(date)

    if i % 20 == 0:
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
                    "start_date": trades[len(trades) - current_loss_count - 1]["date"]
                    if len(trades) - current_loss_count - 1 < len(trades)
                    else "N/A",
                }
            )
        current_loss_count = 0
        current_loss_sum = 0.0

if current_loss_count > 0:
    consecutive_losses.append(
        {
            "count": current_loss_count,
            "sum_pct": current_loss_sum,
            "start_date": trades[-current_loss_count]["date"]
            if len(trades) - current_loss_count >= 0
            else "N/A",
        }
    )

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

print("\n阶段3: 计算回撤...")

if equity_curve and len(equity_curve) > 1:
    peak = equity_curve[0]
    max_drawdown_pct = 0.0

    for equity in equity_curve:
        if equity > peak:
            peak = equity
        dd_pct = (peak - equity) / peak * 100
        if dd_pct > max_drawdown_pct:
            max_drawdown_pct = dd_pct

    print(f"整体最大回撤: {max_drawdown_pct:.2f}%")

print("\n阶段4: 测试停手机制...")


def apply_pause_mechanism(trades, pause_rule):
    paused_trades = []
    pause_counter = 0
    consecutive_losses = 0

    for trade in trades:
        if pause_counter > 0:
            pause_counter -= 1
            continue

        paused_trades.append({**trade, "effective_return_pct": trade["return_pct"]})

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
    }


pause_rules = {
    "no_pause": "无停手机制",
    "pause_3_3": "连亏3笔停3天",
    "pause_4_5": "连亏4笔停5天",
}

results_comparison = {}

print("\n测试三种机制:")
for rule_key, rule_name in pause_rules.items():
    print(f"\n测试: {rule_name}")

    if rule_key == "no_pause":
        test_trades = [{**t, "effective_return_pct": t["return_pct"]} for t in trades]
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
        print(f"  休息天数: {skipped}")

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

print("\n" + "=" * 60)
print("回测完成")
print("=" * 60)

result_data = {
    "trades_count": len(trades),
    "consecutive_losses_count": len(consecutive_losses),
    "max_consecutive_loss": max_consecutive_loss if consecutive_losses else 0,
    "max_drawdown_pct": max_drawdown_pct if equity_curve else 0,
    "pause_mechanism_comparison": results_comparison,
    "trades_sample": trades[:10],
}

result_file = "/Users/fengzhi/Downloads/git/testlixingren/output/joinquant_pause_mechanism_2024.json"
try:
    with open(result_file, "w") as f:
        json.dump(result_data, f, indent=2)
    print(f"\n结果已保存至: {result_file}")
except Exception as e:
    print(f"\n保存失败: {e}")
    print("结果将输出到控制台")
    print(json.dumps(result_data, indent=2))
