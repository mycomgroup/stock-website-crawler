"""
策略辅助函数模块
提供策略开发中常用的辅助函数

包括:
1. 技术指标计算辅助函数
2. 数据处理辅助函数
3. 持仓管理辅助函数
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import warnings


def calculate_ma(prices, window):
    """
    计算移动平均线

    参数:
        prices: 价格序列（Series或list）
        window: 窗口期

    返回:
        Series: 移动平均值

    示例:
        ma5 = calculate_ma(df['close'], 5)
    """
    return pd.Series(prices).rolling(window=window).mean()


def calculate_ema(prices, span):
    """
    计算指数移动平均线

    参数:
        prices: 价格序列
        span: 跨度

    返回:
        Series: EMA值

    示例:
        ema12 = calculate_ema(df['close'], 12)
    """
    return pd.Series(prices).ewm(span=span, adjust=False).mean()


def calculate_std(prices, window):
    """
    计算标准差

    参数:
        prices: 价格序列
        window: 窗口期

    返回:
        Series: 标准差

    示例:
        std20 = calculate_std(df['close'], 20)
    """
    return pd.Series(prices).rolling(window=window).std()


def calculate_boll(prices, window=20, num_std=2):
    """
    计算布林线

    参数:
        prices: 价格序列
        window: 窗口期
        num_std: 标准差倍数

    返回:
        dict: {'upper': 上轨, 'middle': 中轨, 'lower': 下轨}

    示例:
        boll = calculate_boll(df['close'])
    """
    series = pd.Series(prices)
    middle = series.rolling(window=window).mean()
    std = series.rolling(window=window).std()

    upper = middle + num_std * std
    lower = middle - num_std * std

    return {
        "upper": upper,
        "middle": middle,
        "lower": lower,
    }


def calculate_rsi(prices, window=14):
    """
    计算RSI指标

    参数:
        prices: 价格序列
        window: 窗口期

    返回:
        Series: RSI值

    示例:
        rsi = calculate_rsi(df['close'])
    """
    series = pd.Series(prices)
    delta = series.diff()

    gain = delta.where(delta > 0, 0)
    loss = -delta.where(delta < 0, 0)

    avg_gain = gain.rolling(window=window).mean()
    avg_loss = loss.rolling(window=window).mean()

    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))

    return rsi


def calculate_macd(prices, fast=12, slow=26, signal=9):
    """
    计算MACD指标

    参数:
        prices: 价格序列
        fast: 快线周期
        slow: 慢线周期
        signal: 信号线周期

    返回:
        dict: {'macd': MACD线, 'signal': 信号线, 'hist': 柱状图}

    示例:
        macd = calculate_macd(df['close'])
    """
    series = pd.Series(prices)

    ema_fast = series.ewm(span=fast, adjust=False).mean()
    ema_slow = series.ewm(span=slow, adjust=False).mean()

    macd_line = ema_fast - ema_slow
    signal_line = macd_line.ewm(span=signal, adjust=False).mean()
    histogram = macd_line - signal_line

    return {
        "macd": macd_line,
        "signal": signal_line,
        "hist": histogram,
    }


def calculate_kdj(highs, lows, closes, n=9, m=3):
    """
    计算KDJ指标

    参数:
        highs: 最高价序列
        lows: 最低价序列
        closes: 收盘价序列
        n: RSV周期
        m: K/D平滑周期

    返回:
        dict: {'k': K值, 'd': D值, 'j': J值}

    示例:
        kdj = calculate_kdj(df['high'], df['low'], df['close'])
    """
    highs = pd.Series(highs)
    lows = pd.Series(lows)
    closes = pd.Series(closes)

    lowest_low = lows.rolling(window=n).min()
    highest_high = highs.rolling(window=n).max()

    rsv = (closes - lowest_low) / (highest_high - lowest_low) * 100

    k = rsv.ewm(alpha=1 / m, adjust=False).mean()
    d = k.ewm(alpha=1 / m, adjust=False).mean()
    j = 3 * k - 2 * d

    return {
        "k": k,
        "d": d,
        "j": j,
    }


def calculate_atr(highs, lows, closes, window=14):
    """
    计算ATR指标

    参数:
        highs: 最高价序列
        lows: 最低价序列
        closes: 收盘价序列
        window: 窗口期

    返回:
        Series: ATR值

    示例:
        atr = calculate_atr(df['high'], df['low'], df['close'])
    """
    highs = pd.Series(highs)
    lows = pd.Series(lows)
    closes = pd.Series(closes)

    prev_closes = closes.shift(1)

    tr1 = highs - lows
    tr2 = highs - prev_closes
    tr3 = prev_closes - lows

    tr = pd.concat([tr1, tr2, tr3], axis=1).max(axis=1)
    atr = tr.rolling(window=window).mean()

    return atr


def normalize_data(data, method="zscore"):
    """
    数据标准化

    参数:
        data: 数据序列
        method: 标准化方法 ('zscore', 'minmax', 'rank')

    返回:
        Series: 标准化后的数据

    示例:
        normalized = normalize_data(df['close'], method='zscore')
    """
    series = pd.Series(data)

    if method == "zscore":
        return (series - series.mean()) / series.std()
    elif method == "minmax":
        return (series - series.min()) / (series.max() - series.min())
    elif method == "rank":
        return series.rank(pct=True)
    else:
        return series


def winsorize(data, lower=0.025, upper=0.975):
    """
    数据去极值

    参数:
        data: 数据序列
        lower: 下限百分位
        upper: 上限百分位

    返回:
        Series: 去极值后的数据

    示例:
        winsorized = winsorize(df['pe_ratio'])
    """
    series = pd.Series(data)

    lower_bound = series.quantile(lower)
    upper_bound = series.quantile(upper)

    return series.clip(lower_bound, upper_bound)


def calculate_sharpe(returns, risk_free_rate=0.0):
    """
    计算夏普比率

    参数:
        returns: 收益率序列
        risk_free_rate: 无风险利率

    返回:
        float: 夏普比率

    示例:
        sharpe = calculate_sharpe(daily_returns)
    """
    returns = pd.Series(returns)

    excess_returns = returns - risk_free_rate / 252

    if excess_returns.std() == 0:
        return 0

    return excess_returns.mean() / excess_returns.std() * np.sqrt(252)


def calculate_max_drawdown(values):
    """
    计算最大回撤

    参数:
        values: 资产净值序列

    返回:
        float: 最大回撤

    示例:
        max_dd = calculate_max_drawdown(nav_series)
    """
    values = pd.Series(values)

    cumulative_max = values.cummax()
    drawdown = (values - cumulative_max) / cumulative_max

    return drawdown.min()


def calculate_drawdown_duration(values):
    """
    计算回撤持续时间

    参数:
        values: 资产净值序列

    返回:
        int: 最大回撤持续天数

    示例:
        duration = calculate_drawdown_duration(nav_series)
    """
    values = pd.Series(values)

    cumulative_max = values.cummax()
    drawdown = (values - cumulative_max) / cumulative_max

    in_drawdown = drawdown < 0

    if not in_drawdown.any():
        return 0

    drawdown_periods = in_drawdown.astype(int).diff()
    drawdown_periods.iloc[0] = 0

    starts = drawdown_periods[drawdown_periods == 1]
    ends = drawdown_periods[drawdown_periods == -1]

    if len(ends) == 0:
        return len(values) - starts.index[0]
    if len(starts) == 0:
        return 0

    durations = []
    for i, start_idx in enumerate(starts.index):
        if i < len(ends):
            end_idx = ends.index[i]
            durations.append(end_idx - start_idx)
        else:
            durations.append(len(values) - start_idx)

    return max(durations) if durations else 0


def calculate_volatility(returns, window=20):
    """
    计算波动率

    参数:
        returns: 收益率序列
        window: 窗口期

    返回:
        Series: 波动率

    示例:
        vol = calculate_volatility(daily_returns)
    """
    returns = pd.Series(returns)
    return returns.rolling(window=window).std() * np.sqrt(252)


def calculate_return_series(values):
    """
    计算收益率序列

    参数:
        values: 资产净值序列

    返回:
        Series: 收益率

    示例:
        returns = calculate_return_series(nav_series)
    """
    values = pd.Series(values)
    return values.pct_change()


def calculate_cumulative_return(values):
    """
    计算累计收益率

    参数:
        values: 资产净值序列

    返回:
        float: 累计收益率

    示例:
        total_return = calculate_cumulative_return(nav_series)
    """
    values = pd.Series(values)

    if len(values) < 2:
        return 0

    return values.iloc[-1] / values.iloc[0] - 1


def calculate_annualized_return(values):
    """
    计算年化收益率

    参数:
        values: 资产净值序列

    返回:
        float: 年化收益率

    示例:
        annual_return = calculate_annualized_return(nav_series)
    """
    values = pd.Series(values)

    if len(values) < 2:
        return 0

    total_return = values.iloc[-1] / values.iloc[0]
    days = len(values)

    return total_return ** (252 / days) - 1


def calculate_position_concentration(weights):
    """
    计算持仓集中度

    参数:
        weights: 持仓权重字典 {股票代码: 权重}

    返回:
        float: 集中度（最大权重）

    示例:
        concentration = calculate_position_concentration({'600519': 0.3, '000858': 0.7})
    """
    if not weights:
        return 0

    return max(weights.values())


def calculate_diversification_index(weights):
    """
    计算分散度指数

    参数:
        weights: 持仓权重字典

    返回:
        float: 分散度（有效持仓数量）

    示例:
        div_index = calculate_diversification_index({'600519': 0.3, '000858': 0.7})
    """
    if not weights:
        return 0

    weights_array = np.array(list(weights.values()))

    herfindahl = np.sum(weights_array**2)

    if herfindahl == 0:
        return 0

    return 1 / herfindahl


def rebalance_equally(stock_list, context):
    """
    等权重新平衡持仓

    参数:
        stock_list: 目标持仓列表
        context: context对象

    示例:
        rebalance_equally(['600519.XSHG', '000858.XSHE'], context)
    """
    from api_enhancements import order_target_percent, rebalance_portfolio

    if not stock_list:
        return

    target_weight = 1.0 / len(stock_list)
    target_weights = {stock: target_weight for stock in stock_list}

    rebalance_portfolio(target_weights, stock_list)


def get_top_holdings(portfolio, top_n=5):
    """
    获取前N大持仓

    参数:
        portfolio: portfolio对象
        top_n: 数量

    返回:
        list: [(股票代码, 持仓市值)]

    示例:
        top_holdings = get_top_holdings(context.portfolio, top_n=3)
    """
    positions = portfolio.positions

    holdings = []
    for stock, pos in positions.items():
        value = pos.size * pos.price
        holdings.append((stock, value))

    holdings.sort(key=lambda x: x[1], reverse=True)

    return holdings[:top_n]


def calculate_portfolio_beta(portfolio_returns, benchmark_returns):
    """
    计算组合Beta

    参数:
        portfolio_returns: 组合收益率序列
        benchmark_returns: 基准收益率序列

    返回:
        float: Beta值

    示例:
        beta = calculate_portfolio_beta(strategy_returns, benchmark_returns)
    """
    portfolio_returns = pd.Series(portfolio_returns)
    benchmark_returns = pd.Series(benchmark_returns)

    covariance = portfolio_returns.cov(benchmark_returns)
    benchmark_variance = benchmark_returns.var()

    if benchmark_variance == 0:
        return 0

    return covariance / benchmark_variance


def calculate_tracking_error(portfolio_returns, benchmark_returns):
    """
    计算跟踪误差

    参数:
        portfolio_returns: 组合收益率序列
        benchmark_returns: 基准收益率序列

    返回:
        float: 跟踪误差

    示例:
        te = calculate_tracking_error(strategy_returns, benchmark_returns)
    """
    portfolio_returns = pd.Series(portfolio_returns)
    benchmark_returns = pd.Series(benchmark_returns)

    excess_returns = portfolio_returns - benchmark_returns

    return excess_returns.std() * np.sqrt(252)
