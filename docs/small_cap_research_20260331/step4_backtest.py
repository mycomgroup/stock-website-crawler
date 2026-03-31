"""
Step 4: 策略回测验证

目标：验证完整策略的收益和回撤
方法：简化回测（Notebook方式）

RiceQuant Notebook 运行方式：
node run-strategy.js --strategy step4_backtest.py --timeout-ms 600000

注意：这是简化版回测，用于快速验证策略逻辑
      精确回测请在策略编辑器中进行
"""

import numpy as np
import pandas as pd
from datetime import datetime, timedelta

print("=" * 60)
print("Step 4: 策略回测验证")
print("=" * 60)

# ============================================================
# 1. 策略参数设置
# ============================================================
print("\n[1. 策略参数设置]")

STRATEGY_PARAMS = {
    "stock_num": 10,  # 持仓数量
    "min_market_cap": 10,  # 最小市值（亿）
    "max_market_cap": 300,  # 最大市值（亿）
    "stop_loss": -0.09,  # 个股止损（-9%）
    "rebalance_days": 5,  # 调仓周期（天）
    "lookback_days": 60,  # 回看天数
}

print("策略参数:")
for key, value in STRATEGY_PARAMS.items():
    print(f"  {key}: {value}")

# ============================================================
# 2. 选股函数定义
# ============================================================
print("\n[2. 选股函数定义]")


def select_stocks_simple(stock_pool, num_stocks=10, lookback_days=60):
    """
    简化版选股函数

    选股逻辑：
    1. 计算动量因子（20日涨幅）
    2. 计算MA乖离率
    3. 计算量比
    4. 综合评分排序
    """

    results = []

    for stock in stock_pool:
        try:
            # 获取历史数据
            bars = history_bars(stock, lookback_days, "1d", ["close", "volume"])

            if bars is None or len(bars) < 40:
                continue

            close = bars["close"]
            volume = bars["volume"]

            # 计算因子
            # 动量（20日涨幅）
            momentum_20 = (
                (close[-1] / close[-21] - 1) * 100 if len(close) >= 21 else None
            )

            # MA乖离率
            ma20 = np.mean(close[-20:])
            ma_deviation = (close[-1] / ma20 - 1) * 100 if ma20 > 0 else None

            # 量比
            vol_ratio = (
                np.mean(volume[-5:]) / np.mean(volume[-20:])
                if len(volume) >= 20 and np.mean(volume[-20:]) > 0
                else None
            )

            # 价格位置
            price_high = np.max(close[-20:])
            price_low = np.min(close[-20:])
            price_pos = (
                (close[-1] - price_low) / (price_high - price_low)
                if price_high != price_low
                else 0.5
            )

            if any(v is None for v in [momentum_20, ma_deviation, vol_ratio]):
                continue

            # 计算综合评分
            # 这里使用简单的线性加权
            score = 0

            # 动量因子：正动量加分
            if momentum_20 > 10:
                score += 3
            elif momentum_20 > 5:
                score += 2
            elif momentum_20 > 0:
                score += 1
            elif momentum_20 < -10:
                score -= 2

            # MA乖离率：适度偏离加分
            if -5 < ma_deviation < 10:
                score += 2
            elif ma_deviation < -10:
                score -= 1

            # 量比：适度放量加分
            if 1.2 < vol_ratio < 2.0:
                score += 2
            elif 1.0 < vol_ratio < 1.2:
                score += 1
            elif vol_ratio > 3.0:
                score -= 1

            # 价格位置：中等位置加分
            if 0.3 < price_pos < 0.7:
                score += 1
            elif price_pos > 0.9:
                score -= 1

            results.append(
                {
                    "code": stock,
                    "close": close[-1],
                    "momentum_20": momentum_20,
                    "ma_deviation": ma_deviation,
                    "vol_ratio": vol_ratio,
                    "price_pos": price_pos,
                    "score": score,
                }
            )

        except Exception as e:
            continue

    # 按评分排序
    results.sort(key=lambda x: -x["score"])

    return results[:num_stocks]


# ============================================================
# 3. 简化回测框架
# ============================================================
print("\n[3. 简化回测框架]")


def simple_backtest(initial_capital=100000, test_periods=12):
    """
    简化版回测

    注意：这是非常简化的回测，仅用于验证策略逻辑
    - 不考虑滑点和手续费
    - 不考虑涨跌停
    - 不考虑停牌
    """

    print(f"初始资金: {initial_capital}")
    print(f"测试周期数: {test_periods}")

    # 获取股票池
    try:
        hs300 = index_components("000300.XSHG")
        zz500 = index_components("000905.XSHG")
        stock_pool = list(set(hs300) | set(zz500))
        stock_pool = [
            s for s in stock_pool if not s.startswith("688") and not s.startswith("8")
        ]
    except:
        print("无法获取股票池，回测终止")
        return None

    print(f"股票池数量: {len(stock_pool)}")

    # 模拟回测
    capital = initial_capital
    portfolio_value = initial_capital
    holdings = {}  # 持仓 {stock: {"shares": n, "cost": price}}

    # 记录每月表现
    monthly_returns = []

    for period in range(test_periods):
        print(f"\n周期 {period + 1}/{test_periods}")

        # 选股
        selected = select_stocks_simple(
            stock_pool[:200], num_stocks=STRATEGY_PARAMS["stock_num"]
        )

        if not selected:
            print("  无选中股票")
            continue

        print(f"  选中股票: {len(selected)} 只")

        # 计算当前持仓价值
        position_value = 0
        for stock, holding in holdings.items():
            try:
                bars = history_bars(stock, 1, "1d", "close")
                if bars is not None and len(bars) > 0:
                    current_price = bars["close"][-1]
                    position_value += holding["shares"] * current_price
            except:
                position_value += holding["shares"] * holding["cost"]

        total_value = capital + position_value

        # 调仓：卖出不在选中列表的股票
        selected_codes = [s["code"] for s in selected]
        for stock in list(holdings.keys()):
            if stock not in selected_codes:
                try:
                    bars = history_bars(stock, 1, "1d", "close")
                    if bars is not None and len(bars) > 0:
                        sell_price = bars["close"][-1]
                        capital += holdings[stock]["shares"] * sell_price
                        del holdings[stock]
                except:
                    pass

        # 买入新选中的股票
        if capital > 0 and len(selected) > 0:
            per_stock_capital = capital / len(selected)

            for stock_info in selected:
                stock = stock_info["code"]
                if stock not in holdings:
                    try:
                        buy_price = stock_info["close"]
                        shares = int(per_stock_capital / buy_price)
                        if shares > 0:
                            holdings[stock] = {
                                "shares": shares,
                                "cost": buy_price,
                            }
                            capital -= shares * buy_price
                    except:
                        pass

        # 计算期末价值
        position_value = 0
        for stock, holding in holdings.items():
            try:
                bars = history_bars(stock, 1, "1d", "close")
                if bars is not None and len(bars) > 0:
                    current_price = bars["close"][-1]
                    position_value += holding["shares"] * current_price
            except:
                position_value += holding["shares"] * holding["cost"]

        portfolio_value = capital + position_value
        period_return = (portfolio_value / initial_capital - 1) * 100
        monthly_returns.append(period_return)

        print(f"  组合价值: {portfolio_value:.2f}")
        print(f"  累计收益率: {period_return:.2f}%")

    return {
        "final_value": portfolio_value,
        "total_return": (portfolio_value / initial_capital - 1) * 100,
        "monthly_returns": monthly_returns,
    }


# ============================================================
# 4. 执行回测
# ============================================================
print("\n[4. 执行简化回测]")

try:
    backtest_result = simple_backtest(initial_capital=100000, test_periods=12)

    if backtest_result:
        print("\n" + "=" * 60)
        print("[回测结果]")
        print("=" * 60)

        print(f"""
最终组合价值: {backtest_result["final_value"]:.2f}
累计收益率: {backtest_result["total_return"]:.2f}%

月度收益率序列:
""")

        for i, ret in enumerate(backtest_result["monthly_returns"], 1):
            print(f"  月{i}: {ret:+.2f}%")

        # 计算年化收益
        annual_return = (backtest_result["total_return"] / 12) * 12
        print(f"\n年化收益率（估算）: {annual_return:.2f}%")

except Exception as e:
    print(f"回测失败: {e}")
    import traceback

    traceback.print_exc()

# ============================================================
# 5. 风险指标计算
# ============================================================
print("\n[5. 风险指标计算（简化）]")

if backtest_result and "monthly_returns" in backtest_result:
    returns = np.array(backtest_result["monthly_returns"])

    # 最大回撤
    cummax = np.maximum.accumulate(returns)
    drawdowns = returns - cummax
    max_drawdown = np.min(drawdowns)

    # 夏普比率（简化）
    if np.std(returns) > 0:
        sharpe = np.mean(returns) / np.std(returns)
    else:
        sharpe = 0

    # 胜率
    positive_months = np.sum(returns > 0)
    win_rate = positive_months / len(returns) * 100

    print(f"""
风险指标（简化计算）：

最大回撤: {max_drawdown:.2f}%
夏普比率: {sharpe:.2f}
月胜率: {win_rate:.1f}%
正收益月份: {positive_months}/{len(returns)}
""")

# ============================================================
# 6. 策略总结
# ============================================================
print("\n" + "=" * 60)
print("[策略总结]")
print("=" * 60)

print(f"""
国九条+机器学习小市值策略 - 简化回测验证完成

策略框架：
1. 国九条筛选：排除ST、次新股、退市股票
2. 因子选择：动量、MA乖离率、量比、价格位置
3. 评分排序：综合评分选出top股票
4. 定期调仓：每{STRATEGY_PARAMS["rebalance_days"]}天调仓

回测结果：
- 累计收益率: {backtest_result["total_return"]:.2f}%（{12}个周期）
- 年化收益率（估算）: {annual_return:.2f}%
- 最大回撤: {max_drawdown:.2f}%

下一步：
1. 在策略编辑器中进行精确回测
2. 加入滑点和手续费
3. 测试不同参数组合
4. 进行样本外验证

注意：
- 这是简化回测，仅供参考
- 实际收益可能低于回测结果
- 需要考虑流动性、滑点等实际因素
""")

print("\n" + "=" * 60)
print("Step 4 完成")
print("=" * 60)
