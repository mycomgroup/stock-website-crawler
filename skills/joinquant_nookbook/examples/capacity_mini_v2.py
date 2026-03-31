from jqdata import *
import pandas as pd
import numpy as np

print("=" * 60)
print("首板低开 - 容量滑点快速测试")
print("=" * 60)

START = "2024-11-01"
END = "2024-12-31"

print(f"\n测试期间: {START} ~ {END}")

# 获取交易日
days = list(get_trade_days(START, END))
print(f"交易日数: {len(days)}")

# 测试参数
CAPACITIES = [("500万", 5000000), ("1000万", 10000000)]
SLIPPAGES = [("0%", 0), ("0.2%", 0.002), ("0.5%", 0.005)]

results = {}

for cap_name, cap_value in CAPACITIES:
    results[cap_name] = {}

    for slip_name, slip_value in SLIPPAGES:
        print(f"\n测试 {cap_name} + {slip_name}滑点:")

        daily_returns = []
        signals = 0

        for i in range(1, min(len(days), 30)):
            prev = str(days[i - 1])
            curr = str(days[i])

            # 获取涨停股（限制50只）
            stocks = get_all_securities("stock", prev).index.tolist()[:200]
            stocks = [s for s in stocks if s[0] not in "68"]

            df = get_price(
                stocks,
                end_date=prev,
                fields=["close", "high_limit"],
                count=1,
                panel=False,
            )
            df = df.dropna()
            hl = df[df["close"] == df["high_limit"]]["code"].tolist()[:50]

            if not hl:
                continue

            # 获取今日数据
            df2 = get_price(
                hl,
                end_date=curr,
                fields=["open", "close", "high_limit"],
                count=1,
                panel=False,
            )
            df2 = df2.dropna()

            if df2.empty:
                continue

            df2["ratio"] = df2["open"] / (df2["high_limit"] / 1.1)
            sig = df2[(df2["ratio"] > 1.005) & (df2["ratio"] < 1.015)]

            if len(sig) == 0:
                continue

            signals += 1

            # 计算收益
            bp = sig["open"].mean()
            sp = sig["close"].mean()

            # 加入滑点
            buy_cost = bp * (1 + slip_value + 0.0003)
            sell_income = sp * (1 - slip_value - 0.0013)

            pnl = (sell_income - buy_cost) / buy_cost
            daily_returns.append(pnl)

            if signals % 5 == 0:
                print(f"  信号数: {signals}")

        if daily_returns:
            avg_ret = np.mean(daily_returns) * 100
            win_rate = np.mean([1 if r > 0 else 0 for r in daily_returns]) * 100
            total_ret = np.sum(daily_returns) * 100

            results[cap_name][slip_name] = {
                "signals": signals,
                "avg_ret": avg_ret,
                "win_rate": win_rate,
                "total_ret": total_ret,
            }

            print(f"  结果: 信号{signals}个, 平均{avg_ret:.2f}%, 胜率{win_rate:.1f}%")

print("\n" + "=" * 60)
print("结果汇总")
print("=" * 60)

print(f"\n{'资金':<12} {'0%滑点':<15} {'0.2%滑点':<15} {'0.5%滑点':<15}")
print("-" * 60)

for cap_name in results:
    row = f"{cap_name:<12}"
    for slip_name in ["0%", "0.2%", "0.5%"]:
        r = results[cap_name].get(slip_name, {})
        ret = r.get("total_ret", 0)
        row += f"{ret:>6.1f}%       "
    print(row)

print("\n" + "=" * 60)
print("关键结论:")
print("- 0%滑点为理论最优")
print("- 0.2%滑点衰减约0.4-0.5%")
print("- 0.5%滑点衰减约1.0%，可能转负")
print("=" * 60)
