"""
JoinQuant Notebook版本：防守线+进攻线组合测试（简化版）

可以直接复制此代码到JoinQuant Notebook中运行
测试周期：2024-01-01 至 2025-03-30
测试策略：
1. 纯防守线（小市值低估值）
2. 静态权重组合（60防守/40进攻）
3. 动态路由组合（状态自适应）
"""

from jqdata import *
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# ==========================================
# 配置参数
# ==========================================
START_DATE = "2024-01-01"
END_DATE = "2025-03-30"
INITIAL_CAPITAL = 100000

# ==========================================
# 工具函数
# ==========================================


def get_smallcap_universe(watch_date, min_cap=15, max_cap=60):
    """获取小市值股票池"""
    all_stocks = get_all_securities(types=["stock"], date=watch_date)
    all_stocks = all_stocks[
        all_stocks["start_date"] <= watch_date - timedelta(days=180)
    ]
    stocks = all_stocks.index.tolist()

    is_st = get_extras("is_st", stocks, end_date=watch_date, count=1).iloc[-1]
    stocks = is_st[is_st == False].index.tolist()

    paused = get_price(
        stocks, end_date=watch_date, count=1, fields="paused", panel=False
    )
    paused = paused.pivot(index="time", columns="code", values="paused").iloc[-1]
    stocks = paused[paused == 0].index.tolist()

    stocks = [s for s in stocks if not s.startswith("688")]

    q = query(valuation.code, valuation.market_cap).filter(
        valuation.code.in_(stocks),
        valuation.market_cap >= min_cap,
        valuation.market_cap <= max_cap,
    )

    df = get_fundamentals(q, date=watch_date)
    if len(df) == 0:
        return []

    df["cap_rank"] = df["market_cap"].rank(pct=True)
    small_stocks = df[df["cap_rank"] <= 0.3]["code"].tolist()

    return small_stocks


def select_defense_stocks(watch_date, hold_num=10):
    """防守线选股：小市值+低估值"""
    stocks = get_smallcap_universe(watch_date)
    if len(stocks) < 5:
        return []

    q = query(
        valuation.code,
        valuation.market_cap,
        valuation.pe_ratio,
        valuation.pb_ratio,
        indicator.roe,
    ).filter(
        valuation.code.in_(stocks),
        valuation.pe_ratio > 0,
        valuation.pe_ratio < 20,
        valuation.pb_ratio > 0,
        valuation.pb_ratio < 1.5,
    )

    df = get_fundamentals(q, date=watch_date)
    if len(df) == 0:
        return []

    df = df.drop_duplicates("code")
    df = df.replace([np.inf, -np.inf], np.nan)
    df = df.dropna()

    if len(df) == 0:
        return []

    df["pb_rank"] = df["pb_ratio"].rank(pct=True)
    df["pe_rank"] = df["pe_ratio"].rank(pct=True)
    df["value_score"] = (df["pb_rank"] + df["pe_rank"]) / 2

    df = df.sort_values("value_score", ascending=True)

    return df["code"].tolist()[:hold_num]


def select_offense_stocks(watch_date, hold_num=5):
    """进攻线选股：首板低开假弱高开"""
    prev_date = watch_date - timedelta(days=1)

    q = query(
        valuation.code,
        valuation.circulating_market_cap,
    ).filter(
        valuation.circulating_market_cap >= 50,
        valuation.circulating_market_cap <= 150,
    )

    df = get_fundamentals(q, date=watch_date)
    if len(df) == 0:
        return []

    candidates = []

    for code in df["code"].tolist()[:50]:  # 限制检查数量加快速度
        try:
            prev_data = get_price(
                code,
                end_date=prev_date,
                count=1,
                fields=["close", "high_limit"],
                panel=False,
            )
            if prev_data.empty:
                continue

            prev_close = float(prev_data["close"].iloc[0])
            prev_high_limit = float(prev_data["high_limit"].iloc[0])

            if abs(prev_close - prev_high_limit) / prev_high_limit > 0.01:
                continue

            curr_data = get_price(
                code,
                end_date=watch_date,
                count=1,
                fields=["open", "close"],
                panel=False,
            )
            if curr_data.empty:
                continue

            curr_open = float(curr_data["open"].iloc[0])
            open_pct = (curr_open - prev_close) / prev_close * 100

            if not (0.5 <= open_pct <= 1.5):
                continue

            candidates.append(code)

        except Exception as e:
            continue

    return candidates[:hold_num]


def calculate_market_state(watch_date):
    """计算市场状态（简化版）"""
    try:
        # 计算市场宽度
        all_stocks = get_all_securities(types=["stock"], date=watch_date)
        test_stocks = [
            s for s in all_stocks.index.tolist()[:300] if not s.startswith("688")
        ]

        prices = get_price(
            test_stocks, end_date=watch_date, count=2, fields=["close"], panel=False
        )
        if prices.empty:
            return "中", 0.3

        price_pivot = prices.pivot(index="time", columns="code", values="close")
        if len(price_pivot) < 2:
            return "中", 0.3

        prev_close = price_pivot.iloc[-2]
        curr_close = price_pivot.iloc[-1]
        up_count = (curr_close > prev_close).sum()
        breadth = up_count / len(test_stocks)

        # 计算趋势
        benchmark = get_price(
            "000852.XSHG", end_date=watch_date, count=20, fields=["close"], panel=False
        )
        if benchmark.empty or len(benchmark) < 20:
            return "中", breadth

        closes = benchmark["close"].values
        recent_return = (closes[-1] - closes[-5]) / closes[-5]

        if breadth < 0.25 and recent_return < 0:
            return "弱", breadth
        elif breadth > 0.55 and recent_return > 0.02:
            return "强", breadth
        else:
            return "中", breadth

    except Exception as e:
        return "中", 0.3


def run_backtest_defense_only(start_date, end_date, initial_capital=100000):
    """运行纯防守线回测"""
    print("=" * 60)
    print("策略1：纯防守线（小市值低估值）")
    print("=" * 60)

    trades = get_trade_days(start_date=start_date, end_date=end_date)
    monthly_dates = [d for d in trades if d.day == 1 or (d == trades[0])]

    portfolio_value = initial_capital
    positions = {}
    portfolio_values = []
    drawdowns = []

    for i, date in enumerate(monthly_dates):
        if i > 0:
            # 计算当日持仓市值
            if positions:
                try:
                    prices = get_price(
                        list(positions.keys()),
                        end_date=date,
                        count=1,
                        fields=["close"],
                        panel=False,
                    )
                    if not prices.empty:
                        price_dict = dict(zip(prices["code"], prices["close"]))
                        portfolio_value = sum(
                            price_dict.get(code, 0) * shares
                            for code, shares in positions.items()
                        )
                except:
                    pass

        # 选股调仓
        stocks = select_defense_stocks(date, hold_num=10)

        if stocks:
            positions = {}
            value_per_stock = portfolio_value / len(stocks)
            for stock in stocks:
                try:
                    price_data = get_price(
                        stock, end_date=date, count=1, fields=["close"], panel=False
                    )
                    if not price_data.empty:
                        price = float(price_data["close"].iloc[0])
                        shares = int(value_per_stock / price / 100) * 100
                        if shares > 0:
                            positions[stock] = shares
                except:
                    continue

        portfolio_values.append((date, portfolio_value))

        if len(portfolio_values) > 1:
            peak = max([v for _, v in portfolio_values])
            drawdown = (portfolio_value - peak) / peak
            drawdowns.append(drawdown)

    # 计算指标
    final_value = portfolio_values[-1][1]
    total_return = (final_value - initial_capital) / initial_capital

    days = (monthly_dates[-1] - monthly_dates[0]).days
    annual_return = (1 + total_return) ** (365.25 / days) - 1 if days > 0 else 0

    max_drawdown = min(drawdowns) if drawdowns else 0

    returns = []
    for i in range(1, len(portfolio_values)):
        daily_return = (
            portfolio_values[i][1] - portfolio_values[i - 1][1]
        ) / portfolio_values[i - 1][1]
        returns.append(daily_return)

    if returns:
        mean_return = np.mean(returns)
        std_return = np.std(returns)
        sharpe = (mean_return / std_return) * np.sqrt(12) if std_return > 0 else 0
    else:
        sharpe = 0

    print(f"总收益: {total_return * 100:.2f}%")
    print(f"年化收益: {annual_return * 100:.2f}%")
    print(f"最大回撤: {max_drawdown * 100:.2f}%")
    print(f"夏普比率: {sharpe:.2f}")

    return {
        "strategy": "Defense_Only",
        "total_return": total_return,
        "annual_return": annual_return,
        "max_drawdown": max_drawdown,
        "sharpe": sharpe,
    }


def run_backtest_static_combo(
    start_date, end_date, defense_weight=0.6, offense_weight=0.4, initial_capital=100000
):
    """运行静态权重组合回测"""
    print("\n" + "=" * 60)
    print(
        f"策略2：静态权重组合（防守{defense_weight * 100:.0f}% + 进攻{offense_weight * 100:.0f}%）"
    )
    print("=" * 60)

    trades = get_trade_days(start_date=start_date, end_date=end_date)
    monthly_dates = [d for d in trades if d.day == 1 or (d == trades[0])]

    portfolio_value = initial_capital
    positions = {}
    portfolio_values = []
    drawdowns = []

    for i, date in enumerate(monthly_dates):
        if i > 0:
            if positions:
                try:
                    prices = get_price(
                        list(positions.keys()),
                        end_date=date,
                        count=1,
                        fields=["close"],
                        panel=False,
                    )
                    if not prices.empty:
                        price_dict = dict(zip(prices["code"], prices["close"]))
                        portfolio_value = sum(
                            price_dict.get(code, 0) * shares
                            for code, shares in positions.items()
                        )
                except:
                    pass

        # 选股
        defense_stocks = select_defense_stocks(date, hold_num=10)
        offense_stocks = select_offense_stocks(date, hold_num=5)

        positions = {}

        if defense_stocks:
            defense_value = portfolio_value * defense_weight
            value_per_defense = defense_value / len(defense_stocks)
            for stock in defense_stocks:
                try:
                    price_data = get_price(
                        stock, end_date=date, count=1, fields=["close"], panel=False
                    )
                    if not price_data.empty:
                        price = float(price_data["close"].iloc[0])
                        shares = int(value_per_defense / price / 100) * 100
                        if shares > 0:
                            positions[stock] = shares
                except:
                    continue

        if offense_stocks:
            offense_value = portfolio_value * offense_weight
            value_per_offense = offense_value / len(offense_stocks)
            for stock in offense_stocks:
                try:
                    price_data = get_price(
                        stock, end_date=date, count=1, fields=["close"], panel=False
                    )
                    if not price_data.empty:
                        price = float(price_data["close"].iloc[0])
                        shares = int(value_per_offense / price / 100) * 100
                        if shares > 0:
                            positions[stock] = shares
                except:
                    continue

        portfolio_values.append((date, portfolio_value))

        if len(portfolio_values) > 1:
            peak = max([v for _, v in portfolio_values])
            drawdown = (portfolio_value - peak) / peak
            drawdowns.append(drawdown)

    final_value = portfolio_values[-1][1]
    total_return = (final_value - initial_capital) / initial_capital

    days = (monthly_dates[-1] - monthly_dates[0]).days
    annual_return = (1 + total_return) ** (365.25 / days) - 1 if days > 0 else 0

    max_drawdown = min(drawdowns) if drawdowns else 0

    returns = []
    for i in range(1, len(portfolio_values)):
        daily_return = (
            portfolio_values[i][1] - portfolio_values[i - 1][1]
        ) / portfolio_values[i - 1][1]
        returns.append(daily_return)

    if returns:
        mean_return = np.mean(returns)
        std_return = np.std(returns)
        sharpe = (mean_return / std_return) * np.sqrt(12) if std_return > 0 else 0
    else:
        sharpe = 0

    print(f"总收益: {total_return * 100:.2f}%")
    print(f"年化收益: {annual_return * 100:.2f}%")
    print(f"最大回撤: {max_drawdown * 100:.2f}%")
    print(f"夏普比率: {sharpe:.2f}")

    return {
        "strategy": f"Static_{int(defense_weight * 100)}_{int(offense_weight * 100)}",
        "total_return": total_return,
        "annual_return": annual_return,
        "max_drawdown": max_drawdown,
        "sharpe": sharpe,
    }


def run_backtest_dynamic(start_date, end_date, initial_capital=100000):
    """运行动态路由组合回测"""
    print("\n" + "=" * 60)
    print("策略3：动态路由组合（状态自适应）")
    print("=" * 60)

    trades = get_trade_days(start_date=start_date, end_date=end_date)
    monthly_dates = [d for d in trades if d.day == 1 or (d == trades[0])]

    portfolio_value = initial_capital
    positions = {}
    portfolio_values = []
    drawdowns = []
    state_history = []

    STATE_CONFIGS = {
        "弱": {"total_position": 0.30, "defense_weight": 1.0, "offense_weight": 0.0},
        "中": {"total_position": 0.50, "defense_weight": 0.7, "offense_weight": 0.3},
        "强": {"total_position": 0.70, "defense_weight": 0.5, "offense_weight": 0.5},
    }

    for i, date in enumerate(monthly_dates):
        if i > 0:
            if positions:
                try:
                    prices = get_price(
                        list(positions.keys()),
                        end_date=date,
                        count=1,
                        fields=["close"],
                        panel=False,
                    )
                    if not prices.empty:
                        price_dict = dict(zip(prices["code"], prices["close"]))
                        portfolio_value = sum(
                            price_dict.get(code, 0) * shares
                            for code, shares in positions.items()
                        )
                except:
                    pass

        # 确定市场状态
        state, breadth = calculate_market_state(date)
        state_history.append((date, state, breadth))
        config = STATE_CONFIGS.get(state, STATE_CONFIGS["中"])

        if config["total_position"] == 0:
            positions = {}
        else:
            defense_stocks = select_defense_stocks(date, hold_num=10)
            offense_stocks = select_offense_stocks(date, hold_num=5)

            positions = {}
            position_value = portfolio_value * config["total_position"]

            if defense_stocks and config["defense_weight"] > 0:
                defense_value = position_value * config["defense_weight"]
                value_per_defense = defense_value / len(defense_stocks)
                for stock in defense_stocks:
                    try:
                        price_data = get_price(
                            stock, end_date=date, count=1, fields=["close"], panel=False
                        )
                        if not price_data.empty:
                            price = float(price_data["close"].iloc[0])
                            shares = int(value_per_defense / price / 100) * 100
                            if shares > 0:
                                positions[stock] = shares
                    except:
                        continue

            if offense_stocks and config["offense_weight"] > 0:
                offense_value = position_value * config["offense_weight"]
                value_per_offense = offense_value / len(offense_stocks)
                for stock in offense_stocks:
                    try:
                        price_data = get_price(
                            stock, end_date=date, count=1, fields=["close"], panel=False
                        )
                        if not price_data.empty:
                            price = float(price_data["close"].iloc[0])
                            shares = int(value_per_offense / price / 100) * 100
                            if shares > 0:
                                positions[stock] = shares
                    except:
                        continue

        portfolio_values.append((date, portfolio_value))

        if len(portfolio_values) > 1:
            peak = max([v for _, v in portfolio_values])
            drawdown = (portfolio_value - peak) / peak
            drawdowns.append(drawdown)

    final_value = portfolio_values[-1][1]
    total_return = (final_value - initial_capital) / initial_capital

    days = (monthly_dates[-1] - monthly_dates[0]).days
    annual_return = (1 + total_return) ** (365.25 / days) - 1 if days > 0 else 0

    max_drawdown = min(drawdowns) if drawdowns else 0

    returns = []
    for i in range(1, len(portfolio_values)):
        daily_return = (
            portfolio_values[i][1] - portfolio_values[i - 1][1]
        ) / portfolio_values[i - 1][1]
        returns.append(daily_return)

    if returns:
        mean_return = np.mean(returns)
        std_return = np.std(returns)
        sharpe = (mean_return / std_return) * np.sqrt(12) if std_return > 0 else 0
    else:
        sharpe = 0

    # 统计状态分布
    state_counts = {}
    for _, state, _ in state_history:
        state_counts[state] = state_counts.get(state, 0) + 1

    print(f"总收益: {total_return * 100:.2f}%")
    print(f"年化收益: {annual_return * 100:.2f}%")
    print(f"最大回撤: {max_drawdown * 100:.2f}%")
    print(f"夏普比率: {sharpe:.2f}")
    print(f"\n状态分布:")
    for state, count in state_counts.items():
        print(f"  {state}: {count}个月 ({count / len(state_history) * 100:.1f}%)")

    return {
        "strategy": "Dynamic_Router",
        "total_return": total_return,
        "annual_return": annual_return,
        "max_drawdown": max_drawdown,
        "sharpe": sharpe,
        "state_distribution": state_counts,
    }


# ==========================================
# 主程序
# ==========================================

print("\n" + "=" * 60)
print("防守线 + 进攻线组合测试")
print("测试周期：2024-01-01 至 2025-03-30")
print("初始资金：100,000")
print("=" * 60)

# 运行三个策略
results = []

result1 = run_backtest_defense_only(START_DATE, END_DATE, INITIAL_CAPITAL)
results.append(result1)

result2 = run_backtest_static_combo(START_DATE, END_DATE, 0.6, 0.4, INITIAL_CAPITAL)
results.append(result2)

result3 = run_backtest_dynamic(START_DATE, END_DATE, INITIAL_CAPITAL)
results.append(result3)

# 对比分析
print("\n" + "=" * 60)
print("对比分析")
print("=" * 60)

print("\n策略对比表：")
print("-" * 80)
print(f"{'策略':<20} {'总收益':<12} {'年化收益':<12} {'最大回撤':<12} {'夏普':<8}")
print("-" * 80)

for r in results:
    print(
        f"{r['strategy']:<20} {r['total_return'] * 100:>10.2f}% {r['annual_return'] * 100:>10.2f}% {r['max_drawdown'] * 100:>10.2f}% {r['sharpe']:>8.2f}"
    )

print("\n组合效果分析：")
defense = results[0]
static = results[1]
dynamic = results[2]

# 静态组合 vs 纯防守线
static_improvement = static["annual_return"] - defense["annual_return"]
static_sharpe_diff = static["sharpe"] - defense["sharpe"]

print(f"\n静态组合 vs 纯防守线：")
print(f"  年化收益改善: {static_improvement:+.2f}%")
print(f"  夏普改善: {static_sharpe_diff:+.2f}")
if static_improvement > 0 and static_sharpe_diff > 0:
    print(f"  ✅ 组合显著改善了收益和风险调整后收益")

# 动态路由 vs 静态组合
dynamic_improvement = dynamic["annual_return"] - static["annual_return"]
dynamic_sharpe_diff = dynamic["sharpe"] - static["sharpe"]
dynamic_drawdown_diff = dynamic["max_drawdown"] - static["max_drawdown"]

print(f"\n动态路由 vs 静态组合：")
print(f"  年化收益改善: {dynamic_improvement:+.2f}%")
print(f"  夏普改善: {dynamic_sharpe_diff:+.2f}")
print(f"  回撤改善: {dynamic_drawdown_diff:+.2f}%")

if dynamic_sharpe_diff > 0:
    print(f"  ✅ 动态路由显著改善了夏普比率")

print("\n" + "=" * 60)
print("结论")
print("=" * 60)

if dynamic["sharpe"] > static["sharpe"] and dynamic["sharpe"] > defense["sharpe"]:
    print(f"\n✅ 推荐：动态路由组合")
    print(f"   - 夏普最优: {dynamic['sharpe']:.2f}")
    print(f"   - 年化收益: {dynamic['annual_return'] * 100:.2f}%")
    print(f"   - 最大回撤: {dynamic['max_drawdown'] * 100:.2f}%")
elif static["sharpe"] > defense["sharpe"]:
    print(f"\n✅ 推荐：静态权重组合（60/40）")
    print(f"   - 夏普: {static['sharpe']:.2f}")
    print(f"   - 年化收益: {static['annual_return'] * 100:.2f}%")
    print(f"   - 最大回撤: {static['max_drawdown'] * 100:.2f}%")
else:
    print(f"\n⚠️  当前样本期内纯防守线表现最好")
    print(f"   - 需要更多样本验证组合效果")

print("\n" + "=" * 60)
