# JoinQuant Notebook使用指南：防守线+进攻线组合测试

## 快速开始

### 方法：直接在JoinQuant Notebook中运行

由于JoinQuant Strategy API服务响应超时，建议使用JoinQuant Notebook直接运行简化版回测。

### 步骤

1. 登录 [JoinQuant](https://www.joinquant.com/)
2. 进入"我的策略" -> "Notebook"
3. 创建新Notebook
4. 复制以下代码到Notebook中
5. 点击"运行全部"

## 代码

```python
from jqdata import *
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# ==========================================
# 配置参数
# ==========================================
START_DATE = '2024-01-01'
END_DATE = '2025-03-30'
INITIAL_CAPITAL = 100000

# ==========================================
# 工具函数
# ==========================================

def get_smallcap_universe(watch_date, min_cap=15, max_cap=60):
    """获取小市值股票池"""
    all_stocks = get_all_securities(types=["stock"], date=watch_date)
    all_stocks = all_stocks[all_stocks["start_date"] <= watch_date - timedelta(days=180)]
    stocks = all_stocks.index.tolist()

    is_st = get_extras("is_st", stocks, end_date=watch_date, count=1).iloc[-1]
    stocks = is_st[is_st == False].index.tolist()

    paused = get_price(stocks, end_date=watch_date, count=1, fields="paused", panel=False)
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

    for code in df["code"].tolist()[:50]:
        try:
            prev_data = get_price(code, end_date=prev_date, count=1,
                                  fields=["close", "high_limit"], panel=False)
            if prev_data.empty:
                continue

            prev_close = float(prev_data["close"].iloc[0])
            prev_high_limit = float(prev_data["high_limit"].iloc[0])

            if abs(prev_close - prev_high_limit) / prev_high_limit > 0.01:
                continue

            curr_data = get_price(code, end_date=watch_date, count=1,
                                  fields=["open", "close"], panel=False)
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
        if i > 0 and positions:
            try:
                prices = get_price(list(positions.keys()), end_date=date, count=1, fields=["close"], panel=False)
                if not prices.empty:
                    price_dict = dict(zip(prices["code"], prices["close"]))
                    portfolio_value = sum(price_dict.get(code, 0) * shares for code, shares in positions.items())
            except:
                pass

        stocks = select_defense_stocks(date, hold_num=10)

        if stocks:
            positions = {}
            value_per_stock = portfolio_value / len(stocks)
            for stock in stocks:
                try:
                    price_data = get_price(stock, end_date=date, count=1, fields=["close"], panel=False)
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

    final_value = portfolio_values[-1][1]
    total_return = (final_value - initial_capital) / initial_capital

    days = (monthly_dates[-1] - monthly_dates[0]).days
    annual_return = (1 + total_return) ** (365.25 / days) - 1 if days > 0 else 0

    max_drawdown = min(drawdowns) if drawdowns else 0

    returns = []
    for i in range(1, len(portfolio_values)):
        daily_return = (portfolio_values[i][1] - portfolio_values[i-1][1]) / portfolio_values[i-1][1]
        returns.append(daily_return)

    if returns:
        mean_return = np.mean(returns)
        std_return = np.std(returns)
        sharpe = (mean_return / std_return) * np.sqrt(12) if std_return > 0 else 0
    else:
        sharpe = 0

    print(f"总收益: {total_return*100:.2f}%")
    print(f"年化收益: {annual_return*100:.2f}%")
    print(f"最大回撤: {max_drawdown*100:.2f}%")
    print(f"夏普比率: {sharpe:.2f}")

    return {
        'strategy': 'Defense_Only',
        'total_return': total_return,
        'annual_return': annual_return,
        'max_drawdown': max_drawdown,
        'sharpe': sharpe
    }

def run_backtest_static_combo(start_date, end_date, defense_weight=0.6, offense_weight=0.4, initial_capital=100000):
    """运行静态权重组合回测"""
    print("\n" + "=" * 60)
    print(f"策略2：静态权重组合（防守{defense_weight*100:.0f}% + 进攻{offense_weight*100:.0f}%）")
    print("=" * 60)

    trades = get_trade_days(start_date=start_date, end_date=end_date)
    monthly_dates = [d for d in trades if d.day == 1 or (d == trades[0])]

    portfolio_value = initial_capital
    positions = {}
    portfolio_values = []
    drawdowns = []

    for i, date in enumerate(monthly_dates):
        if i > 0 and positions:
            try:
                prices = get_price(list(positions.keys()), end_date=date, count=1, fields=["close"], panel=False)
                if not prices.empty:
                    price_dict = dict(zip(prices["code"], prices["close"]))
                    portfolio_value = sum(price_dict.get(code, 0) * shares for code, shares in positions.items())
            except:
                pass

        defense_stocks = select_defense_stocks(date, hold_num=10)
        offense_stocks = select_offense_stocks(date, hold_num=5)

        positions = {}

        if defense_stocks:
            defense_value = portfolio_value * defense_weight
            value_per_defense = defense_value / len(defense_stocks)
            for stock in defense_stocks:
                try:
                    price_data = get_price(stock, end_date=date, count=1, fields=["close"], panel=False)
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
                    price_data = get_price(stock, end_date=date, count=1, fields=["close"], panel=False)
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
        daily_return = (portfolio_values[i][1] - portfolio_values[i-1][1]) / portfolio_values[i-1][1]
        returns.append(daily_return)

    if returns:
        mean_return = np.mean(returns)
        std_return = np.std(returns)
        sharpe = (mean_return / std_return) * np.sqrt(12) if std_return > 0 else 0
    else:
        sharpe = 0

    print(f"总收益: {total_return*100:.2f}%")
    print(f"年化收益: {annual_return*100:.2f}%")
    print(f"最大回撤: {max_drawdown*100:.2f}%")
    print(f"夏普比率: {sharpe:.2f}")

    return {
        'strategy': f'Static_{int(defense_weight*100)}_{int(offense_weight*100)}',
        'total_return': total_return,
        'annual_return': annual_return,
        'max_drawdown': max_drawdown,
        'sharpe': sharpe
    }

# ==========================================
# 主程序
# ==========================================

print("\n" + "=" * 60)
print("防守线 + 进攻线组合测试")
print("测试周期：2024-01-01 至 2025-03-30")
print("初始资金：100,000")
print("=" * 60)

# 运行两个策略对比
results = []

result1 = run_backtest_defense_only(START_DATE, END_DATE, INITIAL_CAPITAL)
results.append(result1)

result2 = run_backtest_static_combo(START_DATE, END_DATE, 0.6, 0.4, INITIAL_CAPITAL)
results.append(result2)

# 对比分析
print("\n" + "=" * 60)
print("对比分析")
print("=" * 60)

print("\n策略对比表：")
print("-" * 80)
print(f"{'策略':<20} {'总收益':<12} {'年化收益':<12} {'最大回撤':<12} {'夏普':<8}")
print("-" * 80)

for r in results:
    print(f"{r['strategy']:<20} {r['total_return']*100:>10.2f}% {r['annual_return']*100:>10.2f}% {r['max_drawdown']*100:>10.2f}% {r['sharpe']:>8.2f}")

print("\n组合效果分析：")
defense = results[0]
static = results[1]

# 静态组合 vs 纯防守线
static_improvement = static['annual_return'] - defense['annual_return']
static_sharpe_diff = static['sharpe'] - defense['sharpe']

print(f"\n静态组合 vs 纯防守线：")
print(f"  年化收益改善: {static_improvement:+.2f}%")
print(f"  夏普改善: {static_sharpe_diff:+.2f}")
if static_improvement > 0 and static_sharpe_diff > 0:
    print(f"  ✅ 组合显著改善了收益和风险调整后收益")
elif static_sharpe_diff > 0:
    print(f"  ✅ 组合改善了风险调整后收益")
else:
    print(f"  ⚠️  当前样本期组合效果不明显")

print("\n" + "=" * 60)
```

## 预期运行时间

- 完整代码运行时间：约5-10分钟
- 如果只需要对比防守线和静态组合，可以注释掉不需要的部分

## 输出示例

```
============================================================
策略1：纯防守线（小市值低估值）
============================================================
总收益: 12.50%
年化收益: 10.20%
最大回撤: -18.50%
夏普比率: 0.55

============================================================
策略2：静态权重组合（防守60% + 进攻40%）
============================================================
总收益: 18.30%
年化收益: 14.80%
最大回撤: -15.20%
夏普比率: 0.85

============================================================
对比分析
============================================================

策略对比表：
--------------------------------------------------------------------------------
策略                 总收益        年化收益        最大回撤        夏普    
--------------------------------------------------------------------------------
Defense_Only          12.50%       10.20%      -18.50%       0.55
Static_60_40          18.30%       14.80%      -15.20%       0.85

组合效果分析：

静态组合 vs 纯防守线：
  年化收益改善: +4.60%
  夏普改善: +0.30
  ✅ 组合显著改善了收益和风险调整后收益

============================================================
```

## 注意事项

1. **运行时间**：完整回测需要5-10分钟，请耐心等待
2. **数据量**：代码限制了检查的股票数量（前50只），加快速度
3. **准确性**：简化版回测未考虑滑点、停牌等细节，结果仅供参考
4. **官方回测**：如需精确结果，建议使用JoinQuant官方回测功能

## 下一步

获取Notebook运行结果后，可以：
1. 对比不同权重配置（70/30, 50/50, 40/60）
2. 测试动态路由组合
3. 更新正式的result_09文档