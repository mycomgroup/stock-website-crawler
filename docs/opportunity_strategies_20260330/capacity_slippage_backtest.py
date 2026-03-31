# 首板低开策略 - 容量与滑点完整回测
# 可直接在 JoinQuant 或 RiceQuant Notebook 中运行
# 复制全部代码到 Notebook，按 Shift+Enter 执行

import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# ====================================================================
# 第一部分：参数配置
# ====================================================================

print("=" * 70)
print("首板低开策略 - 容量与滑点完整回测")
print("=" * 70)
print("\n测试参数：")
print("- 资金档位: 500万, 1000万, 3000万, 5000万")
print("- 滑点档位: 0%, 0.2%, 0.5%, 1.0%")
print("- 手续费: 买0.03%, 卖0.03% + 印花税0.1%")
print("- 成交额占比上限: 10%")
print()

# 测试期间
START_DATE = "2024-07-01"
END_DATE = "2025-03-31"

# 资金档位
CAPACITIES = {
    "500万": 5000000,
    "1000万": 10000000,
    "3000万": 30000000,
    "5000万": 50000000,
}

# 滑点档位
SLIPPAGES = {"0%": 0.0, "0.2%": 0.002, "0.5%": 0.005, "1.0%": 0.01}

# 交易成本
BUY_COMMISSION = 0.0003  # 买入手续费
SELL_COMMISSION = 0.0003  # 卖出手续费
STAMP_DUTY = 0.001  # 印花税（仅卖出）

# 成交额占比上限
MAX_VOLUME_RATIO = 0.10

# ====================================================================
# 第二部分：数据获取函数（根据平台选择）
# ====================================================================

# 判断平台并使用对应API
try:
    # JoinQuant
    from jqdata import *

    PLATFORM = "JoinQuant"

    def get_limit_up_stocks(date):
        """获取昨日涨停股"""
        prev_date = (pd.to_datetime(date) - timedelta(days=1)).strftime("%Y-%m-%d")
        trade_days = get_trade_days(prev_date, date)
        if len(trade_days) < 2:
            return []
        prev_date = trade_days[-2]

        all_stocks = get_all_securities("stock", prev_date).index.tolist()
        all_stocks = [s for s in all_stocks if s[0] not in "683"]

        df = get_price(
            all_stocks[:300],
            end_date=prev_date,
            frequency="daily",
            fields=["close", "high_limit"],
            count=1,
            panel=False,
        )
        if df.empty:
            return []

        df = df.dropna()
        df = df[df["close"] == df["high_limit"]]
        return list(df["code"])[:50]  # 限制50只避免超时

    def get_signal_stocks(limit_up_stocks, date):
        """从涨停股中筛选首板低开信号"""
        if not limit_up_stocks:
            return None

        df = get_price(
            limit_up_stocks,
            end_date=date,
            frequency="daily",
            fields=["open", "close", "high_limit", "money"],
            count=1,
            panel=False,
        )

        if df.empty:
            return None

        df = df.dropna()
        # 假弱高开：+0.5% ~ +1.5%
        df["ratio"] = df["open"] / (df["high_limit"] / 1.1)
        signals = df[(df["ratio"] > 1.005) & (df["ratio"] < 1.015)]

        if len(signals) == 0:
            return None

        return signals

    def calculate_actual_cost(buy_price, sell_price, slippage, capital, turnover):
        """计算实际成交成本"""
        # 滑点影响
        actual_buy_price = buy_price * (1 + slippage)
        actual_sell_price = sell_price * (1 - slippage)

        # 成交额占比限制
        max_invest = turnover * MAX_VOLUME_RATIO
        actual_invest = min(capital / 3, max_invest)  # 单票最多1/3资金

        # 手续费
        buy_cost = actual_buy_price * (1 + BUY_COMMISSION)
        sell_income = actual_sell_price * (1 - SELL_COMMISSION - STAMP_DUTY)

        return buy_cost, sell_income, actual_invest

except ImportError:
    # RiceQuant
    PLATFORM = "RiceQuant"

    def get_limit_up_stocks(date):
        """获取昨日涨停股"""
        prev_date = (pd.to_datetime(date) - timedelta(days=1)).strftime("%Y-%m-%d")
        trade_days = get_trading_dates(prev_date, date)
        if len(trade_days) < 2:
            return []
        prev_date = trade_days[-2]

        all_stocks = get_all_securities(["stock"]).index.tolist()
        all_stocks = [s for s in all_stocks if s[:2] not in ["68", "30"]]

        prices = get_price(
            all_stocks[:300], prev_date, date, fields=["close", "high_limit"]
        )
        if prices.empty:
            return []

        prev_close = prices.loc[prev_date, "close"]
        prev_high_limit = prices.loc[prev_date, "high_limit"]

        limit_up = prev_close[prev_close == prev_high_limit].index.tolist()
        return limit_up[:50]

    def get_signal_stocks(limit_up_stocks, date):
        """从涨停股中筛选首板低开信号"""
        if not limit_up_stocks:
            return None

        prices = get_price(
            limit_up_stocks,
            date,
            date,
            fields=["open", "close", "high_limit", "volume"],
        )

        if prices.empty:
            return None

        # 假弱高开：+0.5% ~ +1.5%
        df = prices.loc[date]
        df["ratio"] = df["open"] / (df["high_limit"] / 1.1)
        signals = df[(df["ratio"] > 1.005) & (df["ratio"] < 1.015)]

        if len(signals) == 0:
            return None

        return signals

    def calculate_actual_cost(buy_price, sell_price, slippage, capital, turnover):
        """计算实际成交成本"""
        actual_buy_price = buy_price * (1 + slippage)
        actual_sell_price = sell_price * (1 - slippage)

        max_invest = turnover * MAX_VOLUME_RATIO
        actual_invest = min(capital / 3, max_invest)

        buy_cost = actual_buy_price * (1 + BUY_COMMISSION)
        sell_income = actual_sell_price * (1 - SELL_COMMISSION - STAMP_DUTY)

        return buy_cost, sell_income, actual_invest


print(f"平台: {PLATFORM}")
print()

# ====================================================================
# 第三部分：回测主函数
# ====================================================================


def run_capacity_slippage_backtest(
    capacity_name, capacity_value, slippage_name, slippage_value
):
    """运行单组容量-滑点回测"""

    trade_days_func = get_trade_days if PLATFORM == "JoinQuant" else get_trading_dates
    trade_days = list(trade_days_func(START_DATE, END_DATE))

    daily_returns = []
    signal_count = 0

    for i in range(1, min(len(trade_days), 90)):  # 限制90天避免超时
        date = str(trade_days[i])
        prev_date = str(trade_days[i - 1])

        # 获取昨日涨停股
        limit_up = get_limit_up_stocks(date)

        if not limit_up:
            continue

        # 获取今日信号
        signals = get_signal_stocks(limit_up, date)

        if not signals or len(signals) == 0:
            continue

        signal_count += 1

        # 计算平均收益
        buy_price = signals["open"].mean()
        sell_price = signals["close"].mean()
        avg_turnover = (
            signals["money"].mean() if "money" in signals.columns else 50000000
        )

        # 计算实际成本
        buy_cost, sell_income, actual_invest = calculate_actual_cost(
            buy_price, sell_price, slippage_value, capacity_value, avg_turnover
        )

        # 计算收益
        pnl_pct = (sell_income - buy_cost) / buy_cost
        daily_returns.append(pnl_pct)

    if len(daily_returns) == 0:
        return None

    # 统计结果
    avg_return = np.mean(daily_returns)
    win_rate = np.mean([1 if r > 0 else 0 for r in daily_returns])
    total_return = np.sum(daily_returns)

    # 年化收益（简化估算）
    annual_return = total_return * (252 / len(daily_returns))

    return {
        "signal_days": signal_count,
        "avg_return": avg_return * 100,
        "win_rate": win_rate * 100,
        "total_return": total_return * 100,
        "annual_return": annual_return * 100,
    }


# ====================================================================
# 第四部分：运行全部测试组合
# ====================================================================

print("开始回测（预计耗时5-10分钟）...\n")

results_matrix = {}

for cap_name, cap_value in CAPACITIES.items():
    results_matrix[cap_name] = {}

    for slip_name, slip_value in SLIPPAGES.items():
        print(f"测试: {cap_name} + {slip_name}滑点...", end=" ")

        result = run_capacity_slippage_backtest(
            cap_name, cap_value, slip_name, slip_value
        )

        if result:
            results_matrix[cap_name][slip_name] = result
            print(
                f"✓ 信号日{result['signal_days']}天，年化{result['annual_return']:.1f}%"
            )
        else:
            results_matrix[cap_name][slip_name] = None
            print("✗ 无数据")

# ====================================================================
# 第五部分：结果汇总
# ====================================================================

print("\n" + "=" * 70)
print("容量-滑点收益矩阵（年化收益%）")
print("=" * 70)

header = f"{'资金规模':<12}"
for slip_name in SLIPPAGES.keys():
    header += f"{slip_name:<12}"
print(header)
print("-" * 70)

for cap_name in CAPACITIES.keys():
    row = f"{cap_name:<12}"
    for slip_name in SLIPPAGES.keys():
        result = results_matrix[cap_name].get(slip_name)
        if result:
            row += f"{result['annual_return']:<12.1f}"
        else:
            row += f"{'N/A':<12}"
    print(row)

print("=" * 70)

# ====================================================================
# 第六部分：关键结论
# ====================================================================

print("\n关键结论：")
print("-" * 70)

# 找出失效点
valid_02 = []
valid_05 = []

for cap_name in CAPACITIES.keys():
    r02 = results_matrix[cap_name].get("0.2%")
    r05 = results_matrix[cap_name].get("0.5%")

    if r02 and r02["annual_return"] > 0:
        valid_02.append((cap_name, r02["annual_return"]))

    if r05 and r05["annual_return"] > 0:
        valid_05.append((cap_name, r05["annual_return"]))

print("1. 0.2%滑点下可行资金范围：")
if valid_02:
    for cap, ret in valid_02:
        print(f"   - {cap}: 年化{ret:.1f}% ✓")
else:
    print("   - 无可行组合")

print("\n2. 0.5%滑点下可行资金范围：")
if valid_05:
    for cap, ret in valid_05:
        print(f"   - {cap}: 年化{ret:.1f}% ✓")
else:
    print("   - 全部失效 ✗")

print("\n3. 滑点失效点判断：")
if not valid_05:
    print("   - **>0.5%滑点时策略失效**")
elif len(valid_05) < len(CAPACITIES):
    print("   - **0.5%滑点时部分容量失效**")
else:
    print("   - **0.5%滑点仍可行，但收益衰减**")

print("\n4. 资金容量上限判断：")
if valid_02:
    # 找到年化收益开始明显下降的档位
    prev_ret = valid_02[0][1]
    degrade_point = None
    for i, (cap, ret) in enumerate(valid_02[1:], 1):
        if ret < prev_ret * 0.8:  # 衰减超过20%
            degrade_point = valid_02[i][0]
            break
        prev_ret = ret

    if degrade_point:
        print(f"   - **{degrade_point}后收益明显恶化**")
        print(f"   - 推荐上限: {valid_02[i - 1][0]}")
    else:
        print(f"   - 推荐上限: {valid_02[-1][0]}")

print("=" * 70)

# ====================================================================
# 第七部分：实盘建议
# ====================================================================

print("\n实盘建议：")
print("-" * 70)
print("1. 资金上限: 500万（安全边界）")
print("2. 单票上限: 50万（总资金10%）")
print("3. 滑点控制: ≤0.2%（严格执行）")
print("4. 成交额占比: ≤10%（确保成交）")
print("5. 模拟盘验证: ≥3个月（熟悉执行）")
print("=" * 70)

print("\n回测完成！")
print(f"平台: {PLATFORM}")
print(f"期间: {START_DATE} ~ {END_DATE}")
print(
    f"测试组合: {len(CAPACITIES)} × {len(SLIPPAGES)} = {len(CAPACITIES) * len(SLIPPAGES)}组"
)
print()

# ====================================================================
# 附录：保存结果到本地（可选）
# ====================================================================

import json

output_data = {
    "platform": PLATFORM,
    "start_date": START_DATE,
    "end_date": END_DATE,
    "capacities": list(CAPACITIES.keys()),
    "slippages": list(SLIPPAGES.keys()),
    "results": results_matrix,
    "timestamp": datetime.now().isoformat(),
}

# 保存到JoinQuant Notebook可访问的路径
try:
    output_file = "/Users/fengzhi/Downloads/git/testlixingren/output/capacity_slippage_backtest_results.json"
    with open(output_file, "w") as f:
        json.dump(output_data, f, indent=2, ensure_ascii=False)
    print(f"结果已保存到: {output_file}")
except:
    print("无法保存到本地（Notebook限制）")
    print("请手动记录以上结果")

print("\n" + "=" * 70)
print("END")
print("=" * 70)
