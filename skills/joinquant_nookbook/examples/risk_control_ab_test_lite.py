#!/usr/bin/env python3
"""风控A/B测试 - Notebook简化版
使用日级数据模拟三组风控效果
"""

from jqdata import *
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import json

print("=" * 80)
print("风控 A/B 测试 - 弱转强竞价策略（简化版）")
print("=" * 80)

BACKTEST_START = "2022-01-01"
BACKTEST_END = "2024-01-01"
SAMPLE_OUT_START = "2023-01-01"
INITIAL_CAPITAL = 100000

print(f"\n回测参数:")
print(f"  回测期间: {BACKTEST_START} 至 {BACKTEST_END}")
print(f"  样本外起始: {SAMPLE_OUT_START}")
print(f"  初始资金: {INITIAL_CAPITAL}")

all_trade_days = get_trade_days(BACKTEST_START, BACKTEST_END)
sample_out_start_idx = all_trade_days.index(pd.Timestamp(SAMPLE_OUT_START))

print(f"\n总交易日: {len(all_trade_days)}")
print(f"样本外起始索引: {sample_out_start_idx}")

test_limit = min(150, len(all_trade_days))
test_days = all_trade_days[:test_limit]

print(f"\n实际测试天数: {len(test_days)}")


def simulate_backtest_with_risk_control(test_days, risk_control_type="A"):
    """
    模拟回测
    risk_control_type:
      A = 仅尾盘清仓
      B = 增加10:30时间止损
      C = 增加组合熔断
    """

    trades = []
    capital = INITIAL_CAPITAL
    cool_down_days = 0
    weekly_pnl_pct = 0
    week_start_day_idx = 0

    for day_idx, date in enumerate(test_days):
        date_str = date.strftime("%Y-%m-%d")

        if cool_down_days > 0:
            cool_down_days -= 1
            continue

        try:
            prev_date = test_days[day_idx - 1] if day_idx > 0 else None
            if prev_date is None:
                continue

            prev_date_str = prev_date.strftime("%Y-%m-%d")

            all_stocks = get_all_securities("stock", date_str).index.tolist()
            all_stocks = [
                s for s in all_stocks if s[:2] != "68" and s[0] not in ["3", "4", "8"]
            ]

            prev_day_prices = get_price(
                all_stocks,
                end_date=prev_date_str,
                count=1,
                fields=["close", "high_limit", "money", "volume"],
                panel=False,
            )

            if prev_day_prices.empty:
                continue

            hl_stocks = prev_day_prices[
                prev_day_prices["close"] == prev_day_prices["high_limit"]
            ]
            hl_stocks = hl_stocks[hl_stocks["money"] > 7e8]

            if len(hl_stocks) == 0:
                continue

            day_prices = get_price(
                hl_stocks["code"].tolist(),
                end_date=date_str,
                count=1,
                fields=["open", "close", "high", "high_limit", "low"],
                panel=False,
            )

            if day_prices.empty:
                continue

            qualified = []
            for _, row in day_prices.iterrows():
                stock = row["code"]
                open_price = row["open"]
                high_limit = row["high_limit"]

                if open_price <= 0 or high_limit <= 0:
                    continue

                open_ratio = open_price / (high_limit / 1.1)

                if 1 < open_ratio < 1.06:
                    qualified.append(
                        {
                            "stock": stock,
                            "open_price": open_price,
                            "high_limit": high_limit,
                            "close": row["close"],
                            "high": row["high"],
                            "low": row["low"],
                        }
                    )

            if len(qualified) == 0:
                continue

            adjusted_capital = capital
            if risk_control_type == "C" and cool_down_days == -1:
                adjusted_capital = capital * 0.5

            per_stock_capital = adjusted_capital / len(qualified)

            next_date_idx = day_idx + 1
            if next_date_idx >= len(test_days):
                continue

            next_date = test_days[next_date_idx]
            next_date_str = next_date.strftime("%Y-%m-%d")

            for q in qualified[:5]:
                stock = q["stock"]
                open_price = q["open_price"]

                try:
                    next_day_prices = get_price(
                        stock,
                        end_date=next_date_str,
                        count=1,
                        fields=["open", "close", "high", "high_limit", "low"],
                        panel=False,
                    )

                    if next_day_prices.empty:
                        continue

                    next_open = next_day_prices["open"].iloc[-1]
                    next_close = next_day_prices["close"].iloc[-1]
                    next_high = next_day_prices["high"].iloc[-1]
                    next_high_limit = next_day_prices["high_limit"].iloc[-1]

                    sell_price = None
                    sell_reason = None

                    if risk_control_type in ["B", "C"]:
                        if next_open < open_price * 0.97:
                            sell_price = next_open
                            sell_reason = "开盘跳空止损"
                        elif next_close < open_price * 1.0:
                            sell_price = next_close
                            sell_reason = "时间止损模拟"

                    if sell_price is None:
                        if next_close == next_high_limit:
                            sell_price = next_high
                            sell_reason = "涨停持有"
                        else:
                            sell_price = next_close
                            sell_reason = "尾盘清仓"

                    pnl_pct = (sell_price - open_price) / open_price
                    pnl = per_stock_capital * pnl_pct

                    trades.append(
                        {
                            "buy_date": date_str,
                            "sell_date": next_date_str,
                            "stock": stock,
                            "buy_price": open_price,
                            "sell_price": sell_price,
                            "sell_reason": sell_reason,
                            "pnl_pct": pnl_pct,
                            "pnl": pnl,
                        }
                    )

                    capital += pnl

                except Exception as e:
                    continue

            daily_pnl_pct = sum(
                [t["pnl_pct"] for t in trades if t["buy_date"] == date_str]
            )
            weekly_pnl_pct += daily_pnl_pct

            if risk_control_type == "C":
                if day_idx - week_start_day_idx >= 5:
                    if weekly_pnl_pct < -0.08 and cool_down_days == 0:
                        cool_down_days = 3
                        print(
                            f"  [C组] 周亏损 {weekly_pnl_pct * 100:.2f}% 触发熔断，休息3天"
                        )
                    weekly_pnl_pct = 0
                    week_start_day_idx = day_idx

        except Exception as e:
            continue

    return trades, capital


print("\n" + "=" * 80)
print("开始运行三组回测...")
print("=" * 80)

print("\n【运行A组：基线版】")
trades_a, capital_a = simulate_backtest_with_risk_control(test_days, "A")
print(f"完成，交易次数: {len(trades_a)}")

print("\n【运行B组：单票止损版】")
trades_b, capital_b = simulate_backtest_with_risk_control(test_days, "B")
print(f"完成，交易次数: {len(trades_b)}")

print("\n【运行C组：组合熔断版】")
trades_c, capital_c = simulate_backtest_with_risk_control(test_days, "C")
print(f"完成，交易次数: {len(trades_c)}")


def calculate_metrics(trades, initial_capital):
    if len(trades) == 0:
        return {
            "total_trades": 0,
            "win_trades": 0,
            "loss_trades": 0,
            "win_rate": 0,
            "avg_win_pct": 0,
            "avg_loss_pct": 0,
            "profit_loss_ratio": 0,
            "total_return_pct": 0,
            "max_win_pct": 0,
            "max_loss_pct": 0,
        }

    wins = [t for t in trades if t["pnl_pct"] > 0]
    losses = [t for t in trades if t["pnl_pct"] <= 0]

    total_trades = len(trades)
    win_trades = len(wins)
    loss_trades = len(losses)
    win_rate = win_trades / total_trades if total_trades > 0 else 0

    avg_win_pct = np.mean([t["pnl_pct"] for t in wins]) if wins else 0
    avg_loss_pct = np.mean([t["pnl_pct"] for t in losses]) if losses else 0
    profit_loss_ratio = abs(avg_win_pct / avg_loss_pct) if avg_loss_pct != 0 else 0

    total_return_pct = (sum([t["pnl"] for t in trades]) / initial_capital) * 100
    max_win_pct = max([t["pnl_pct"] for t in trades]) if trades else 0
    max_loss_pct = min([t["pnl_pct"] for t in trades]) if trades else 0

    return {
        "total_trades": total_trades,
        "win_trades": win_trades,
        "loss_trades": loss_trades,
        "win_rate": win_rate,
        "avg_win_pct": avg_win_pct,
        "avg_loss_pct": avg_loss_pct,
        "profit_loss_ratio": profit_loss_ratio,
        "total_return_pct": total_return_pct,
        "max_win_pct": max_win_pct,
        "max_loss_pct": max_loss_pct,
    }


sample_out_trades_a = [
    t for t in trades_a if pd.Timestamp(t["buy_date"]) >= pd.Timestamp(SAMPLE_OUT_START)
]
sample_out_trades_b = [
    t for t in trades_b if pd.Timestamp(t["buy_date"]) >= pd.Timestamp(SAMPLE_OUT_START)
]
sample_out_trades_c = [
    t for t in trades_c if pd.Timestamp(t["buy_date"]) >= pd.Timestamp(SAMPLE_OUT_START)
]

metrics_a_full = calculate_metrics(trades_a, INITIAL_CAPITAL)
metrics_b_full = calculate_metrics(trades_b, INITIAL_CAPITAL)
metrics_c_full = calculate_metrics(trades_c, INITIAL_CAPITAL)

metrics_a_sample = calculate_metrics(sample_out_trades_a, INITIAL_CAPITAL)
metrics_b_sample = calculate_metrics(sample_out_trades_b, INITIAL_CAPITAL)
metrics_c_sample = calculate_metrics(sample_out_trades_c, INITIAL_CAPITAL)

print("\n" + "=" * 80)
print("三组风控对比结果（全周期）")
print("=" * 80)

print("\n【A组：基线版（仅尾盘清仓）】")
print(f"  交易次数: {metrics_a_full['total_trades']}")
print(f"  胜率: {metrics_a_full['win_rate'] * 100:.2f}%")
print(f"  平均盈利: {metrics_a_full['avg_win_pct'] * 100:.2f}%")
print(f"  平均亏损: {metrics_a_full['avg_loss_pct'] * 100:.2f}%")
print(f"  盈亏比: {metrics_a_full['profit_loss_ratio']:.2f}")
print(f"  总收益: {metrics_a_full['total_return_pct']:.2f}%")
print(f"  最大单笔盈利: {metrics_a_full['max_win_pct'] * 100:.2f}%")
print(f"  最大单笔亏损: {metrics_a_full['max_loss_pct'] * 100:.2f}%")

print("\n【B组：单票时间止损版】")
print(f"  交易次数: {metrics_b_full['total_trades']}")
print(f"  胜率: {metrics_b_full['win_rate'] * 100:.2f}%")
print(f"  平均盈利: {metrics_b_full['avg_win_pct'] * 100:.2f}%")
print(f"  平均亏损: {metrics_b_full['avg_loss_pct'] * 100:.2f}%")
print(f"  盈亏比: {metrics_b_full['profit_loss_ratio']:.2f}")
print(f"  总收益: {metrics_b_full['total_return_pct']:.2f}%")
print(f"  最大单笔盈利: {metrics_b_full['max_win_pct'] * 100:.2f}%")
print(f"  最大单笔亏损: {metrics_b_full['max_loss_pct'] * 100:.2f}%")

print("\n【C组：单票+组合熔断版】")
print(f"  交易次数: {metrics_c_full['total_trades']}")
print(f"  胜率: {metrics_c_full['win_rate'] * 100:.2f}%")
print(f"  平均盈利: {metrics_c_full['avg_win_pct'] * 100:.2f}%")
print(f"  平均亏损: {metrics_c_full['avg_loss_pct'] * 100:.2f}%")
print(f"  盈亏比: {metrics_c_full['profit_loss_ratio']:.2f}")
print(f"  总收益: {metrics_c_full['total_return_pct']:.2f}%")
print(f"  最大单笔盈利: {metrics_c_full['max_win_pct'] * 100:.2f}%")
print(f"  最大单笔亏损: {metrics_c_full['max_loss_pct'] * 100:.2f}%")

print("\n" + "=" * 80)
print(f"样本外结果 ({SAMPLE_OUT_START} 后)")
print("=" * 80)

print("\n【A组样本外】")
print(f"  交易次数: {metrics_a_sample['total_trades']}")
print(f"  胜率: {metrics_a_sample['win_rate'] * 100:.2f}%")
print(f"  总收益: {metrics_a_sample['total_return_pct']:.2f}%")

print("\n【B组样本外】")
print(f"  交易次数: {metrics_b_sample['total_trades']}")
print(f"  胜率: {metrics_b_sample['win_rate'] * 100:.2f}%")
print(f"  总收益: {metrics_b_sample['total_return_pct']:.2f}%")

print("\n【C组样本外】")
print(f"  交易次数: {metrics_c_sample['total_trades']}")
print(f"  胜率: {metrics_c_sample['win_rate'] * 100:.2f}%")
print(f"  总收益: {metrics_c_sample['total_return_pct']:.2f}%")

print("\n" + "=" * 80)
print("对比分析")
print("=" * 80)

b_vs_a = {
    "return_change": metrics_b_full["total_return_pct"]
    - metrics_a_full["total_return_pct"],
    "winrate_change": (metrics_b_full["win_rate"] - metrics_a_full["win_rate"]) * 100,
    "max_loss_improve": metrics_b_full["max_loss_pct"] - metrics_a_full["max_loss_pct"],
}

c_vs_a = {
    "return_change": metrics_c_full["total_return_pct"]
    - metrics_a_full["total_return_pct"],
    "winrate_change": (metrics_c_full["win_rate"] - metrics_a_full["win_rate"]) * 100,
    "max_loss_improve": metrics_c_full["max_loss_pct"] - metrics_a_full["max_loss_pct"],
}

print(f"\nB组 vs A组:")
print(f"  收益变化: {b_vs_a['return_change']:.2f}%")
print(f"  胜率变化: {b_vs_a['winrate_change']:.2f}%")
print(f"  最大亏损改善: {b_vs_a['max_loss_improve'] * 100:.2f}%")

print(f"\nC组 vs A组:")
print(f"  收益变化: {c_vs_a['return_change']:.2f}%")
print(f"  胜率变化: {c_vs_a['winrate_change']:.2f}%")
print(f"  最大亏损改善: {c_vs_a['max_loss_improve'] * 100:.2f}%")

stop_loss_count_b = len([t for t in trades_b if "止损" in t["sell_reason"]])
stop_loss_count_c = len([t for t in trades_c if "止损" in t["sell_reason"]])

print(f"\n止损触发次数:")
print(f"  B组: {stop_loss_count_b} 次")
print(f"  C组: {stop_loss_count_c} 次")

print("\n" + "=" * 80)
print("最终结论")
print("=" * 80)

recommendation = "未确定"
reason = []

if metrics_b_full["total_return_pct"] >= metrics_a_full["total_return_pct"] * 0.8:
    if metrics_b_full["win_rate"] >= metrics_a_full["win_rate"]:
        recommendation = "B组（单票时间止损）为主方案"
        reason.append("收益保留 >= 80%，胜率不降或提升")
        if metrics_b_full["max_loss_pct"] > metrics_a_full["max_loss_pct"]:
            reason.append("最大亏损改善")
else:
    recommendation = "A组（基线）暂为主方案"
    reason.append("B组收益损失过大")

if metrics_c_full["total_return_pct"] < metrics_a_full["total_return_pct"] * 0.6:
    reason.append("C组过于保守，仅作为备选")
elif metrics_c_full["total_return_pct"] >= metrics_a_full["total_return_pct"] * 0.8:
    reason.append("C组可作为保守型主方案")

print(f"\n推荐方案: {recommendation}")
print(f"理由:")
for r in reason:
    print(f"  - {r}")

print("\n" + "=" * 80)
print("判定: Go / Watch / No-Go")
print("=" * 80)

if metrics_a_full["total_trades"] > 20 and metrics_b_full["total_trades"] > 20:
    if metrics_b_full["win_rate"] > 0.5:
        print("\n判定: Go")
        print("理由: 有足够交易样本，B组性价比最高")
    else:
        print("\n判定: Watch")
        print("理由: 样本足够但胜率偏低，需进一步优化")
else:
    print("\n判定: Watch")
    print("理由: 交易样本不足，需扩大测试范围")

results = {
    "test_info": {
        "period": f"{BACKTEST_START} 至 {BACKTEST_END}",
        "test_days": len(test_days),
        "sample_out_start": SAMPLE_OUT_START,
    },
    "full_period": {
        "A_baseline": metrics_a_full,
        "B_single_stop": metrics_b_full,
        "C_combo_circuit": metrics_c_full,
    },
    "sample_out": {
        "A_baseline": metrics_a_sample,
        "B_single_stop": metrics_b_sample,
        "C_combo_circuit": metrics_c_sample,
    },
    "comparison": {
        "B_vs_A": b_vs_a,
        "C_vs_A": c_vs_a,
        "stop_loss_count_B": stop_loss_count_b,
        "stop_loss_count_C": stop_loss_count_c,
    },
    "recommendation": recommendation,
    "reasons": reason,
}

result_file = (
    "/Users/fengzhi/Downloads/git/testlixingren/output/risk_control_ab_test_result.json"
)
with open(result_file, "w") as f:
    json.dump(results, f, indent=2, ensure_ascii=False)

print(f"\n结果已保存至: {result_file}")
print("=" * 80)
