#!/usr/bin/env python
# coding: utf-8
"""
多指标计算模块
计算因子组合的各项评价指标
"""

import numpy as np
import pandas as pd
from scipy.stats import spearmanr
from typing import List, Tuple, Dict
from config import PERIOD_CONFIG


def calculate_cumulative_returns(
    factor_df: pd.DataFrame, ret_df: pd.DataFrame, num_layers: int = 10
) -> pd.DataFrame:
    """
    计算各层累计收益

    Returns:
        DataFrame包含各层的累计收益序列
    """
    layer_returns = {}

    for layer_idx in range(num_layers):
        layer_returns[f"Group_{layer_idx + 1}"] = []

    dates = []

    for date in factor_df.index:
        factors = factor_df.loc[date].dropna()
        returns = ret_df.loc[date].dropna()

        common_stocks = factors.index.intersection(returns.index)
        if len(common_stocks) < num_layers:
            continue

        f = factors[common_stocks]
        r = returns[common_stocks]

        combined = pd.DataFrame({"factor": f, "return": r})
        combined = combined.sort_values("factor", ascending=False)

        n = len(combined)
        group_size = n // num_layers
        remainder = n % num_layers

        start = 0
        for layer_idx in range(num_layers):
            end = start + group_size + (1 if layer_idx < remainder else 0)
            group = combined.iloc[start:end]
            layer_returns[f"Group_{layer_idx + 1}"].append(group["return"].mean())
            start = end

        dates.append(date)

    result = pd.DataFrame(layer_returns, index=dates)
    return result


def calculate_annual_return(
    factor_df: pd.DataFrame,
    ret_df: pd.DataFrame,
    num_layers: int = 10,
    period: str = "W",
) -> float:
    """
    计算顶层年化收益率

    Args:
        period: 周期类型，D/W/M

    Returns:
        年化收益率（基于顶层Group_1）
    """
    layer_returns = calculate_cumulative_returns(factor_df, ret_df, num_layers)

    if layer_returns.empty:
        return 0.0

    top_returns = layer_returns["Group_1"]

    if len(top_returns) < 2:
        return 0.0

    cumulative = (1 + top_returns).cumprod()
    total_return = cumulative.iloc[-1] - 1

    num_periods = len(top_returns)
    periods_per_year = PERIOD_CONFIG[period]["periods_per_year"]

    annual_return = (1 + total_return) ** (periods_per_year / num_periods) - 1

    return float(annual_return)


def calculate_max_drawdown(
    factor_df: pd.DataFrame, ret_df: pd.DataFrame, num_layers: int = 10
) -> float:
    """
    计算顶层最大回撤

    Returns:
        最大回撤比例（0-1之间，越大表示回撤越严重）
    """
    layer_returns = calculate_cumulative_returns(factor_df, ret_df, num_layers)

    if layer_returns.empty:
        return 0.0

    top_returns = layer_returns["Group_1"]

    if len(top_returns) < 2:
        return 0.0

    cumulative = (1 + top_returns).cumprod()

    peak = cumulative.expanding(min_periods=1).max()
    drawdown = (cumulative - peak) / peak

    max_dd = drawdown.min()

    return float(abs(max_dd))


def calculate_long_short_return(
    factor_df: pd.DataFrame,
    ret_df: pd.DataFrame,
    num_layers: int = 10,
    period: str = "W",
) -> float:
    """
    计算顶层夏普比率

    Args:
        period: 周期类型，D/W/M
    """
    top_returns = []

    for date in factor_df.index:
        factors = factor_df.loc[date].dropna()
        returns = ret_df.loc[date].dropna()

        common_stocks = factors.index.intersection(returns.index)
        if len(common_stocks) < num_layers:
            continue

        f = factors[common_stocks]
        r = returns[common_stocks]

        combined = pd.DataFrame({"factor": f, "return": r})
        combined = combined.sort_values("factor", ascending=False)

        n = len(combined)
        group_size = n // num_layers

        top_group = combined.iloc[:group_size]
        top_returns.append(top_group["return"].mean())

    if len(top_returns) < 2:
        return 0.0

    top_returns = np.array(top_returns)
    periods_per_year = PERIOD_CONFIG[period]["periods_per_year"]
    sharpe = (
        np.mean(top_returns) / (np.std(top_returns) + 1e-10) * np.sqrt(periods_per_year)
    )

    return sharpe


def calculate_top_sharpe(
    factor_df: pd.DataFrame,
    ret_df: pd.DataFrame,
    num_layers: int = 10,
    period: str = "W",
) -> float:
    """
    计算顶层夏普比率（calculate_long_short_return的别名）

    Args:
        period: 周期类型，D/W/M
    """
    return calculate_long_short_return(factor_df, ret_df, num_layers, period)


def calculate_ic_series(factor_df: pd.DataFrame, ret_df: pd.DataFrame) -> np.ndarray:
    """
    计算 IC 序列（每日因子值与收益率的秩相关系数）
    """
    ic_list = []

    for date in factor_df.index:
        factors = factor_df.loc[date].dropna()
        returns = ret_df.loc[date].dropna()

        common_stocks = factors.index.intersection(returns.index)
        if len(common_stocks) < 10:
            continue

        f = factors[common_stocks]
        r = returns[common_stocks]

        ic, _ = spearmanr(f, r)
        if not np.isnan(ic):
            ic_list.append(ic)

    return np.array(ic_list)


def calculate_ic_mean(ic_series: np.ndarray) -> float:
    """IC 均值"""
    return np.mean(ic_series) if len(ic_series) > 0 else 0.0


def calculate_icir(ic_series: np.ndarray) -> float:
    """ICIR = IC均值 / IC标准差"""
    if len(ic_series) < 2:
        return 0.0
    std = np.std(ic_series)
    if std < 1e-10:
        return 0.0
    return np.mean(ic_series) / std


def calculate_ic_win_rate(ic_series: np.ndarray) -> float:
    """IC 胜率"""
    if len(ic_series) == 0:
        return 0.0
    return np.sum(ic_series > 0) / len(ic_series)


def calculate_monotonicity(
    factor_df: pd.DataFrame, ret_df: pd.DataFrame, num_layers: int = 10
) -> float:
    """
    计算分层单调性
    返回 0-1 之间的值，1 表示完全单调递减
    """
    all_group_means = []

    for date in factor_df.index:
        factors = factor_df.loc[date].dropna()
        returns = ret_df.loc[date].dropna()

        common_stocks = factors.index.intersection(returns.index)
        if len(common_stocks) < num_layers:
            continue

        f = factors[common_stocks]
        r = returns[common_stocks]

        combined = pd.DataFrame({"factor": f, "return": r})
        combined = combined.sort_values("factor", ascending=False)

        n = len(combined)
        group_size = n // num_layers
        remainder = n % num_layers

        group_means = []
        start = 0
        for i in range(num_layers):
            end = start + group_size + (1 if i < remainder else 0)
            group = combined.iloc[start:end]
            group_means.append(group["return"].mean())
            start = end

        all_group_means.append(group_means)

    if len(all_group_means) == 0:
        return 0.0

    avg_group_means = np.mean(all_group_means, axis=0)

    monotonic_count = 0
    for i in range(num_layers - 1):
        if avg_group_means[i] > avg_group_means[i + 1]:
            monotonic_count += 1

    return monotonic_count / (num_layers - 1)


def calculate_return_volatility(
    factor_df: pd.DataFrame, ret_df: pd.DataFrame, num_layers: int = 10
) -> float:
    """
    计算顶层收益波动率（越低越好）
    """
    top_returns = []

    for date in factor_df.index:
        factors = factor_df.loc[date].dropna()
        returns = ret_df.loc[date].dropna()

        common_stocks = factors.index.intersection(returns.index)
        if len(common_stocks) < num_layers:
            continue

        f = factors[common_stocks]
        r = returns[common_stocks]

        combined = pd.DataFrame({"factor": f, "return": r})
        combined = combined.sort_values("factor", ascending=False)

        n = len(combined)
        group_size = n // num_layers

        top_group = combined.iloc[:group_size]
        top_returns.append(top_group["return"].mean())

    if len(top_returns) < 2:
        return 1.0

    return np.std(top_returns)


def calculate_composite_score(
    factor_df: pd.DataFrame,
    ret_df: pd.DataFrame,
    diversity: float,
    num_layers: int = 10,
    period: str = "W",
) -> Dict[str, float]:
    """
    计算综合评分及各分项指标（包含annual_return和max_drawdown）

    Args:
        period: 周期类型，D/W/M

    Returns:
        包含所有指标的字典
    """
    ic_series = calculate_ic_series(factor_df, ret_df)

    metrics = {
        "long_short_return": calculate_long_short_return(
            factor_df, ret_df, num_layers, period
        ),
        "top_sharpe": calculate_top_sharpe(factor_df, ret_df, num_layers, period),
        "ic_mean": calculate_ic_mean(ic_series),
        "icir": calculate_icir(ic_series),
        "ic_win_rate": calculate_ic_win_rate(ic_series),
        "monotonicity": calculate_monotonicity(factor_df, ret_df, num_layers),
        "return_volatility": calculate_return_volatility(factor_df, ret_df, num_layers),
        "diversity": diversity,
        "annual_return": calculate_annual_return(factor_df, ret_df, num_layers, period),
        "max_drawdown": calculate_max_drawdown(factor_df, ret_df, num_layers),
        "period": period,
    }

    weights = {
        "long_short_return": 0.25,
        "top_sharpe": 0.15,
        "ic_mean": 0.15,
        "icir": 0.10,
        "ic_win_rate": 0.05,
        "monotonicity": 0.10,
        "return_volatility": 0.10,
        "diversity": 0.10,
    }

    normalized = {}

    normalized["long_short_return"] = np.tanh(metrics["long_short_return"] / 10.0)
    normalized["top_sharpe"] = np.tanh(metrics["top_sharpe"] / 5.0)
    normalized["ic_mean"] = np.tanh(metrics["ic_mean"] / 0.1)
    normalized["icir"] = np.tanh(metrics["icir"] / 2.0)
    normalized["ic_win_rate"] = metrics["ic_win_rate"]
    normalized["monotonicity"] = metrics["monotonicity"]
    normalized["return_volatility"] = 1.0 / (1.0 + metrics["return_volatility"] * 10)
    normalized["diversity"] = metrics["diversity"]

    total_score = sum(normalized[k] * weights[k] for k in weights)

    metrics["normalized"] = normalized
    metrics["total_score"] = total_score

    return metrics


def adjust_returns_for_cost(returns, period: str = "W", turnover_rate: float = 0.5):
    """
    交易成本扣减

    Args:
        returns: 收益率序列
        period: 周期类型，D/W/M
        turnover_rate: 换手率

    Returns:
        扣减后的收益率
    """
    config = PERIOD_CONFIG[period]
    cost_per_period = config["trading_cost"] * turnover_rate
    return returns - cost_per_period
