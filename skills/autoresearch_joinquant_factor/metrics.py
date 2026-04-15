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


def calculate_long_short_return(
    factor_df: pd.DataFrame, ret_df: pd.DataFrame, num_layers: int = 10
) -> float:
    """
    计算分层多空收益

    Returns:
        多空收益累计和
    """
    backtest_results = pd.DataFrame()

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

        backtest_results.loc[date, "long_short"] = group_means[0] - group_means[-1]

    return backtest_results["long_short"].sum()


def calculate_top_sharpe(
    factor_df: pd.DataFrame, ret_df: pd.DataFrame, num_layers: int = 10
) -> float:
    """
    计算顶层夏普比率
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
    sharpe = np.mean(top_returns) / (np.std(top_returns) + 1e-10) * np.sqrt(252)

    return sharpe


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
) -> Dict[str, float]:
    """
    计算综合评分及各分项指标

    Returns:
        包含所有指标的字典
    """
    ic_series = calculate_ic_series(factor_df, ret_df)

    metrics = {
        "long_short_return": calculate_long_short_return(factor_df, ret_df, num_layers),
        "top_sharpe": calculate_top_sharpe(factor_df, ret_df, num_layers),
        "ic_mean": calculate_ic_mean(ic_series),
        "icir": calculate_icir(ic_series),
        "ic_win_rate": calculate_ic_win_rate(ic_series),
        "monotonicity": calculate_monotonicity(factor_df, ret_df, num_layers),
        "return_volatility": calculate_return_volatility(factor_df, ret_df, num_layers),
        "diversity": diversity,
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
