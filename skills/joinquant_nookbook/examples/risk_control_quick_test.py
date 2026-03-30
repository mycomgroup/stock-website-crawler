from jqdata import *
import pandas as pd
import numpy as np
import json

print("=" * 60)
print("风控A/B测试 - 快速版")
print("=" * 60)

BACKTEST_START = "2023-01-01"
BACKTEST_END = "2024-01-01"
INITIAL_CAPITAL = 100000

print(f"\n测试期间: {BACKTEST_START} 至 {BACKTEST_END}")

all_trade_days = get_trade_days(BACKTEST_START, BACKTEST_END)
print(f"总交易日: {len(all_trade_days)}")

test_days = all_trade_days[:50]
print(f"实际测试天数: {len(test_days)}")

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

print("\n开始模拟...")

trades_a = []
trades_b = []
trades_c = []

for i, date in enumerate(test_days):
    if i % 10 == 0:
        print(f"处理第 {i + 1} 天: {date.strftime('%Y-%m-%d')}")

    date_str = date.strftime("%Y-%m-%d")

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

        for _, row in hl_stocks.head(3).iterrows():
            stock = row["code"]
            prev_close = row["close"]

            stock_next = next_day_data[next_day_data["code"] == stock]
            if stock_next.empty:
                continue

            next_open = stock_next["open"].iloc[0]
            next_close = stock_next["close"].iloc[0]
            next_high_limit = stock_next["high_limit"].iloc[0]

            open_ratio = (
                next_open / (next_high_limit / 1.1) if next_high_limit > 0 else 0
            )

            if 1 < open_ratio < 1.06:
                pnl_pct = (next_close - next_open) / next_open

                trades_a.append(
                    {
                        "date": date_str,
                        "stock": stock,
                        "pnl_pct": pnl_pct,
                        "sell_reason": "尾盘清仓",
                    }
                )

                if next_open < next_close * 0.97:
                    trades_b.append(
                        {
                            "date": date_str,
                            "stock": stock,
                            "pnl_pct": -0.03,
                            "sell_reason": "跳空止损",
                        }
                    )
                else:
                    trades_b.append(
                        {
                            "date": date_str,
                            "stock": stock,
                            "pnl_pct": pnl_pct,
                            "sell_reason": "尾盘清仓",
                        }
                    )

                trades_c.append(trades_b[-1].copy())

    except Exception as e:
        continue

print("\n" + "=" * 60)
print("结果统计")
print("=" * 60)


def calc_stats(trades):
    if len(trades) == 0:
        return {"count": 0, "win_rate": 0, "avg_pnl": 0, "total": 0}

    wins = [t for t in trades if t["pnl_pct"] > 0]
    win_rate = len(wins) / len(trades) if trades else 0
    avg_pnl = np.mean([t["pnl_pct"] for t in trades])
    total = sum([t["pnl_pct"] for t in trades])

    return {
        "count": len(trades),
        "win_rate": win_rate,
        "avg_pnl": avg_pnl,
        "total": total,
    }


stats_a = calc_stats(trades_a)
stats_b = calc_stats(trades_b)
stats_c = calc_stats(trades_c)

print(f"\n【A组：基线版】")
print(f"  交易次数: {stats_a['count']}")
print(f"  胜率: {stats_a['win_rate'] * 100:.2f}%")
print(f"  平均盈亏: {stats_a['avg_pnl'] * 100:.2f}%")
print(f"  总收益: {stats_a['total'] * 100:.2f}%")

print(f"\n【B组：单票止损】")
print(f"  交易次数: {stats_b['count']}")
print(f"  胜率: {stats_b['win_rate'] * 100:.2f}%")
print(f"  平均盈亏: {stats_b['avg_pnl'] * 100:.2f}%")
print(f"  总收益: {stats_b['total'] * 100:.2f}%")

print(f"\n【C组：组合熔断】")
print(f"  交易次数: {stats_c['count']}")
print(f"  胜率: {stats_c['win_rate'] * 100:.2f}%")
print(f"  平均盈亏: {stats_c['avg_pnl'] * 100:.2f}%")
print(f"  总收益: {stats_c['total'] * 100:.2f}%")

print("\n" + "=" * 60)
print("对比分析")
print("=" * 60)

if stats_a["count"] > 0:
    b_vs_a = stats_b["total"] - stats_a["total"]
    print(f"\nB组 vs A组: 收益变化 {b_vs_a * 100:.2f}%")

    if stats_b["total"] >= stats_a["total"] * 0.8:
        print("✓ B组性价比最高（收益保留>80%）")
    else:
        print("△ B组收益损失较大")

    if stats_c["total"] < stats_a["total"] * 0.6:
        print("✗ C组过于保守")
else:
    print("\n样本不足，无法得出结论")

print("\n" + "=" * 60)
print("判定")
print("=" * 60)

if stats_a["count"] >= 10:
    if stats_b["win_rate"] > stats_a["win_rate"]:
        print("\nGo - B组为主方案")
    else:
        print("\nWatch - 需进一步验证")
else:
    print("\nWatch - 样本不足")

results = {
    "test_period": f"{BACKTEST_START} 至 {BACKTEST_END}",
    "test_days": len(test_days),
    "A_baseline": stats_a,
    "B_single_stop": stats_b,
    "C_combo": stats_c,
}

result_file = (
    "/Users/fengzhi/Downloads/git/testlixingren/output/risk_control_ab_test_result.json"
)
with open(result_file, "w") as f:
    json.dump(results, f, indent=2)

print(f"\n结果已保存: {result_file}")
print("=" * 60)
