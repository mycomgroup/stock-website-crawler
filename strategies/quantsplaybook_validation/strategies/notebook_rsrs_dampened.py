# 钝化 RSRS 择时策略 - RiceQuant Notebook 验证脚本
# 候选2: 钝化 RSRS (V10)
# 构造: RSRS = z_score(beta) * R^2 * quantile(std(return), M)
# 参数: N=18, M=700, 阈值=0.7
# 回测区间: 2015-01-01 至 2024-12-31
# 标的: 沪深300 (000300.XSHG)

import numpy as np
import statsmodels.api as sm
from rqdatac import get_price

print("=== 钝化 RSRS 择时策略验证开始 ===")

# 参数设置
SECURITY = "000300.XSHG"
N = 18  # 回归窗口
M = 700  # 标准分窗口
BUY_THRESHOLD = 0.7
SELL_THRESHOLD = -0.7

# 获取历史数据
prices = get_price(
    SECURITY,
    start_date="2013-01-01",
    end_date="2024-12-31",
    frequency="1d",
    fields=["high", "low", "close", "volume"],
)

if prices is None or len(prices) < M:
    print(f"ERROR: 数据不足, 仅 {len(prices) if prices is not None else 0} 条")
else:
    print(f"获取到 {len(prices)} 条日线数据")

    highs = prices["high"].values
    lows = prices["low"].values
    closes = prices["close"].values

    # 计算 beta 序列和 R2 序列
    beta_history = []
    r2_history = []

    for i in range(N, len(prices)):
        h = highs[i - N : i]
        l = lows[i - N : i]
        X = sm.add_constant(l)
        try:
            model = sm.OLS(h, X).fit()
            beta_history.append(model.params[1])
            r2_history.append(model.rsquared)
        except Exception:
            beta_history.append(np.nan)
            r2_history.append(np.nan)

    beta_arr = np.array(beta_history)
    r2_arr = np.array(r2_history)

    # 计算收益率序列
    returns = np.diff(closes) / closes[:-1]

    # 模拟逐日信号
    signals = []
    positions = []
    pos = False
    entry_idx = None

    valid_count = 0
    trade_count = 0
    wins = 0
    losses = 0

    for i in range(M, len(beta_arr)):
        if np.isnan(beta_arr[i]) or np.isnan(r2_arr[i]):
            continue

        # 计算标准分
        beta_window = beta_arr[max(0, i - M + 1) : i + 1]
        beta_window = beta_window[~np.isnan(beta_window)]

        if len(beta_window) < M * 0.5:
            continue

        mu = np.mean(beta_window)
        sigma = np.std(beta_window)
        if sigma == 0:
            continue

        z = (beta_arr[i] - mu) / sigma
        r2 = r2_arr[i]

        # 计算收益率波动率分位数
        ret_std_window = []
        for j in range(max(0, i - M + 1), min(i + 1, len(returns) - N + 1)):
            if j + N <= len(returns):
                ret_std = np.std(returns[j : j + N])
                ret_std_window.append(ret_std)

        if len(ret_std_window) > 0:
            current_std = (
                np.std(returns[max(0, i - N + 1) : i + 1])
                if i - N + 1 >= 0
                else np.std(returns[: i + 1])
            )
            quantile = np.sum(np.array(ret_std_window) <= current_std) / len(
                ret_std_window
            )
        else:
            quantile = 0.5

        # 钝化 RSRS 指标
        rsrs_dampened = z * r2 * quantile

        # 交易逻辑
        if rsrs_dampened > BUY_THRESHOLD and not pos:
            pos = True
            entry_idx = i
            signals.append(("BUY", i, round(rsrs_dampened, 4)))
        elif rsrs_dampened < SELL_THRESHOLD and pos:
            pos = False
            trade_count += 1
            if entry_idx is not None:
                ret_trade = (closes[i] - closes[entry_idx]) / closes[entry_idx]
                if ret_trade > 0:
                    wins += 1
                else:
                    losses += 1
            signals.append(("SELL", i, round(rsrs_dampened, 4)))

        positions.append(1 if pos else 0)
        valid_count += 1

    # 统计
    positions_arr = np.array(positions)
    total_days = len(positions_arr)
    holding_days = int(np.sum(positions_arr))

    # 计算策略收益 vs 基准
    strategy_returns = []
    benchmark_returns = []
    for i in range(len(positions_arr)):
        idx = i + N
        if idx < len(closes) - 1:
            bench_ret = (closes[idx + 1] - closes[idx]) / closes[idx]
            strat_ret = bench_ret * positions_arr[i]
            strategy_returns.append(strat_ret)
            benchmark_returns.append(bench_ret)

    strategy_returns = np.array(strategy_returns)
    benchmark_returns = np.array(benchmark_returns)

    # 计算指标
    ann_return = float(np.mean(strategy_returns) * 252)
    ann_bench_return = float(np.mean(benchmark_returns) * 252)
    ann_vol = float(np.std(strategy_returns) * np.sqrt(252))
    sharpe = ann_return / ann_vol if ann_vol > 0 else 0

    cum_strategy = np.cumprod(1 + strategy_returns)
    cum_benchmark = np.cumprod(1 + benchmark_returns)

    peak = np.maximum.accumulate(cum_strategy)
    drawdown = (cum_strategy - peak) / peak
    max_dd = float(np.min(drawdown))

    alpha = (ann_return - ann_bench_return) * 100

    print(f"\n=== 钝化 RSRS 择时策略结果 ===")
    print(f"参数: N={N}, M={M}, 阈值=±{BUY_THRESHOLD}")
    print(f"有效交易日: {valid_count}")
    print(f"信号次数: {len(signals)}")
    print(f"交易次数: {trade_count}")
    if trade_count > 0:
        print(f"胜率: {wins / trade_count * 100:.1f}%")
    else:
        print("胜率: N/A")
    print(
        f"持仓天数: {holding_days}/{total_days} ({holding_days / total_days * 100:.1f}%)"
    )
    print(f"年化收益: {ann_return * 100:.2f}%")
    print(f"基准年化: {ann_bench_return * 100:.2f}%")
    print(f"年化波动: {ann_vol * 100:.2f}%")
    print(f"夏普比率: {sharpe:.3f}")
    print(f"最大回撤: {max_dd * 100:.2f}%")
    print(f"Alpha: {alpha:.2f}%")
    print(f"\n=== 验证完成 ===")
