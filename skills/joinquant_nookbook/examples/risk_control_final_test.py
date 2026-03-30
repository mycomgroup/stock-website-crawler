from jqdata import *
import pandas as pd
import numpy as np
import json

print("=" * 60)
print("风控A/B测试 - 快速版v2")
print("=" * 60)

BACKTEST_START = "2023-01-01"
BACKTEST_END = "2024-01-01"
SAMPLE_OUT_START = "2023-07-01"
INITIAL_CAPITAL = 100000

print(f"\n测试期间: {BACKTEST_START} 至 {BACKTEST_END}")
print(f"样本外起始: {SAMPLE_OUT_START}")

all_trade_days = get_trade_days(BACKTEST_START, BACKTEST_END)
print(f"总交易日: {len(all_trade_days)}")

test_days = all_trade_days[:80]
print(f"实际测试天数: {len(test_days)}")

sample_out_start_idx = None
for i, d in enumerate(test_days):
    if d >= pd.Timestamp(SAMPLE_OUT_START):
        sample_out_start_idx = i
        break

print(f"样本外起始索引: {sample_out_start_idx}")

print("\n准备数据...")
all_stocks = get_all_securities("stock", "2024-01-01").index.tolist()
all_stocks = [s for s in all_stocks if s[:2] != "68" and s[0] not in ["3", "4", "8"]][
    :1000
]
print(f"股票池: {len(all_stocks)}")

print("\n获取历史数据...")
prev_data = get_price(
    all_stocks,
    end_date="2023-12-31",
    count=250,
    fields=["open", "close", "high_limit", "money"],
    panel=False,
)
print(f"历史数据量: {len(prev_data)}")

print("\n开始模拟三组策略...")

trades_a = []
trades_b = []
trades_c = []
capital_c = INITIAL_CAPITAL
cool_down_days = 0
weekly_pnl = 0
week_start_idx = 0

for i, date in enumerate(test_days):
    if i % 20 == 0:
        print(f"处理第 {i + 1} 天: {date.strftime('%Y-%m-%d')}")

    date_str = date.strftime("%Y-%m-%d")

    if cool_down_days > 0:
        cool_down_days -= 1
        continue

    if i == 0:
        continue

    prev_date = test_days[i - 1]
    prev_date_str = prev_date.strftime("%Y-%m-%d")

    try:
        day_data = prev_data[prev_data["time"] == prev_date_str]

        hl_stocks = day_data[
            (day_data["close"] == day_data["high_limit"]) & (day_data["money"] > 7e8)
        ]

        if len(hl_stocks) == 0:
            continue

        next_idx = min(i + 1, len(test_days) - 1)
        next_date = test_days[next_idx]
        next_date_str = next_date.strftime("%Y-%m-%d")

        next_day_data = prev_data[prev_data["time"] == next_date_str]

        daily_pnl_a = 0
        daily_pnl_b = 0
        daily_pnl_c = 0

        for _, row in hl_stocks.head(5).iterrows():
            stock = row["code"]

            stock_next = next_day_data[next_day_data["code"] == stock]
            if stock_next.empty:
                continue

            next_open = stock_next["open"].iloc[0]
            next_close = stock_next["close"].iloc[0]
            next_high_limit = stock_next["high_limit"].iloc[0]

            if next_high_limit <= 0:
                continue

            open_ratio = next_open / (next_high_limit / 1.1)

            if 1 < open_ratio < 1.06:
                sell_price_a = next_close
                pnl_pct_a = (sell_price_a - next_open) / next_open

                trades_a.append(
                    {
                        "date": date_str,
                        "stock": stock,
                        "buy_price": next_open,
                        "sell_price": sell_price_a,
                        "pnl_pct": pnl_pct_a,
                        "sell_reason": "尾盘清仓",
                        "is_sample_out": i >= sample_out_start_idx
                        if sample_out_start_idx
                        else False,
                    }
                )
                daily_pnl_a += pnl_pct_a

                sell_price_b = next_close
                pnl_pct_b = pnl_pct_a
                sell_reason_b = "尾盘清仓"

                if pnl_pct_a < -0.03:
                    sell_price_b = next_open * 0.97
                    pnl_pct_b = -0.03
                    sell_reason_b = "止损"

                trades_b.append(
                    {
                        "date": date_str,
                        "stock": stock,
                        "buy_price": next_open,
                        "sell_price": sell_price_b,
                        "pnl_pct": pnl_pct_b,
                        "sell_reason": sell_reason_b,
                        "is_sample_out": i >= sample_out_start_idx
                        if sample_out_start_idx
                        else False,
                    }
                )
                daily_pnl_b += pnl_pct_b

                sell_price_c = sell_price_b
                pnl_pct_c = pnl_pct_b

                trades_c.append(
                    {
                        "date": date_str,
                        "stock": stock,
                        "buy_price": next_open,
                        "sell_price": sell_price_c,
                        "pnl_pct": pnl_pct_c,
                        "sell_reason": sell_reason_b,
                        "is_sample_out": i >= sample_out_start_idx
                        if sample_out_start_idx
                        else False,
                    }
                )
                daily_pnl_c += pnl_pct_c

    except Exception as e:
        continue

    weekly_pnl += daily_pnl_c

    if i - week_start_idx >= 5:
        if weekly_pnl < -0.08 and cool_down_days == 0:
            cool_down_days = 3
            print(f"  [C组] 周亏损{weekly_pnl * 100:.1f}%触发熔断")
        weekly_pnl = 0
        week_start_idx = i

print("\n" + "=" * 60)
print("结果统计")
print("=" * 60)


def calc_stats(trades, sample_out_only=False):
    if sample_out_only:
        trades = [t for t in trades if t.get("is_sample_out", False)]

    if len(trades) == 0:
        return {
            "count": 0,
            "win_rate": 0,
            "avg_pnl": 0,
            "total": 0,
            "avg_win": 0,
            "avg_loss": 0,
            "max_win": 0,
            "max_loss": 0,
        }

    wins = [t for t in trades if t["pnl_pct"] > 0]
    losses = [t for t in trades if t["pnl_pct"] <= 0]

    return {
        "count": len(trades),
        "win_rate": len(wins) / len(trades) if trades else 0,
        "avg_pnl": np.mean([t["pnl_pct"] for t in trades]),
        "total": sum([t["pnl_pct"] for t in trades]),
        "avg_win": np.mean([t["pnl_pct"] for t in wins]) if wins else 0,
        "avg_loss": np.mean([t["pnl_pct"] for t in losses]) if losses else 0,
        "max_win": max([t["pnl_pct"] for t in trades]) if trades else 0,
        "max_loss": min([t["pnl_pct"] for t in trades]) if trades else 0,
    }


stats_a_full = calc_stats(trades_a)
stats_b_full = calc_stats(trades_b)
stats_c_full = calc_stats(trades_c)

stats_a_sample = calc_stats(trades_a, sample_out_only=True)
stats_b_sample = calc_stats(trades_b, sample_out_only=True)
stats_c_sample = calc_stats(trades_c, sample_out_only=True)

print(f"\n【全周期结果】")
print(f"\nA组（基线版）:")
print(f"  交易次数: {stats_a_full['count']}")
print(f"  胜率: {stats_a_full['win_rate'] * 100:.1f}%")
print(f"  平均盈亏: {stats_a_full['avg_pnl'] * 100:.2f}%")
print(f"  总收益: {stats_a_full['total'] * 100:.2f}%")
print(f"  平均盈利: {stats_a_full['avg_win'] * 100:.2f}%")
print(f"  平均亏损: {stats_a_full['avg_loss'] * 100:.2f}%")

print(f"\nB组（单票止损）:")
print(f"  交易次数: {stats_b_full['count']}")
print(f"  胜率: {stats_b_full['win_rate'] * 100:.1f}%")
print(f"  平均盈亏: {stats_b_full['avg_pnl'] * 100:.2f}%")
print(f"  总收益: {stats_b_full['total'] * 100:.2f}%")
print(f"  平均盈利: {stats_b_full['avg_win'] * 100:.2f}%")
print(f"  平均亏损: {stats_b_full['avg_loss'] * 100:.2f}%")

stop_count_b = len([t for t in trades_b if "止损" in t["sell_reason"]])
print(f"  止损次数: {stop_count_b}")

print(f"\nC组（组合熔断）:")
print(f"  交易次数: {stats_c_full['count']}")
print(f"  胜率: {stats_c_full['win_rate'] * 100:.1f}%")
print(f"  总收益: {stats_c_full['total'] * 100:.2f}%")

print(f"\n【样本外结果 ({SAMPLE_OUT_START}后)】")
print(
    f"\nA组样本外: 交易{stats_a_sample['count']}次, 胜率{stats_a_sample['win_rate'] * 100:.1f}%, 收益{stats_a_sample['total'] * 100:.2f}%"
)
print(
    f"B组样本外: 交易{stats_b_sample['count']}次, 胜率{stats_b_sample['win_rate'] * 100:.1f}%, 收益{stats_b_sample['total'] * 100:.2f}%"
)
print(
    f"C组样本外: 交易{stats_c_sample['count']}次, 胜率{stats_c_sample['win_rate'] * 100:.1f}%, 收益{stats_c_sample['total'] * 100:.2f}%"
)

print("\n" + "=" * 60)
print("对比分析")
print("=" * 60)

if stats_a_full["count"] > 0 and stats_b_full["count"] > 0:
    return_change = stats_b_full["total"] - stats_a_full["total"]
    winrate_change = (stats_b_full["win_rate"] - stats_a_full["win_rate"]) * 100
    max_loss_improve = stats_b_full["max_loss"] - stats_a_full["max_loss"]

    print(f"\nB组 vs A组:")
    print(f"  收益变化: {return_change * 100:.2f}%")
    print(f"  胜率变化: {winrate_change:.1f}%")
    print(f"  最大亏损变化: {max_loss_improve * 100:.2f}%")

    if stats_b_full["total"] >= stats_a_full["total"] * 0.8:
        print("  ✓ 收益保留 >= 80%")
        if stats_b_full["win_rate"] >= stats_a_full["win_rate"]:
            print("  ✓ 胜率提升或不降")
            print("\n推荐: B组为主方案")
        else:
            print("  △ 胜率下降")
            print("\n推荐: Watch - 需权衡")
    else:
        print("  △ 收益损失过大")
        print("\n推荐: A组暂为主方案")

    if stats_c_full["total"] < stats_a_full["total"] * 0.6:
        print("\nC组: 过于保守，仅作备选")

print("\n" + "=" * 60)
print("最终判定")
print("=" * 60)

if stats_a_full["count"] >= 20:
    if (
        stats_b_full["total"] >= stats_a_full["total"] * 0.8
        and stats_b_full["win_rate"] >= stats_a_full["win_rate"]
    ):
        print("\n【Go】")
        print("理由: B组性价比最高，收益保留且风险可控")
    elif stats_b_full["win_rate"] > stats_a_full["win_rate"]:
        print("\n【Watch】")
        print("理由: B组胜率提升但收益下降，需进一步验证")
    else:
        print("\n【Watch】")
        print("理由: 结果不明确，需更多样本")
else:
    print("\n【Watch】")
    print("理由: 样本不足")

results = {
    "test_info": {
        "period": f"{BACKTEST_START} 至 {BACKTEST_END}",
        "test_days": len(test_days),
        "sample_out_start": SAMPLE_OUT_START,
    },
    "full_period": {
        "A_baseline": stats_a_full,
        "B_single_stop": stats_b_full,
        "C_combo": stats_c_full,
    },
    "sample_out": {
        "A_baseline": stats_a_sample,
        "B_single_stop": stats_b_sample,
        "C_combo": stats_c_sample,
    },
    "comparison": {
        "return_change_pct": return_change * 100 if "return_change" in dir() else 0,
        "winrate_change_pct": winrate_change if "winrate_change" in dir() else 0,
        "stop_loss_count_b": stop_count_b,
    },
}

result_file = (
    "/Users/fengzhi/Downloads/git/testlixingren/output/risk_control_ab_test_result.json"
)
with open(result_file, "w") as f:
    json.dump(results, f, indent=2, ensure_ascii=False)

print(f"\n结果已保存: {result_file}")
print("=" * 60)
