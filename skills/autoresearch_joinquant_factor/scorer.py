#!/usr/bin/env python
# coding: utf-8
"""
评分和决策模块
"""

from typing import Dict, Tuple


WEIGHTS = {
    "long_short_return": 0.25,
    "top_sharpe": 0.15,
    "ic_mean": 0.15,
    "icir": 0.10,
    "ic_win_rate": 0.05,
    "monotonicity": 0.10,
    "return_volatility": 0.10,
    "diversity": 0.10,
}


def normalize_score(value: float, scale: float = 1.0) -> float:
    """使用 tanh 归一化"""
    import numpy as np

    return float(np.tanh(value / scale))


def calculate_score(metrics: Dict, weights: Dict = None) -> float:
    """
    计算综合评分

    Args:
        metrics: 包含各指标值的字典
        weights: 权重字典（可选，使用默认权重）

    Returns:
        综合评分 (0-1)
    """
    if weights is None:
        weights = WEIGHTS

    normalized = {
        "long_short_return": normalize_score(metrics.get("long_short_return", 0), 10.0),
        "top_sharpe": normalize_score(metrics.get("top_sharpe", 0), 5.0),
        "ic_mean": normalize_score(metrics.get("ic_mean", 0), 0.1),
        "icir": normalize_score(metrics.get("icir", 0), 2.0),
        "ic_win_rate": metrics.get("ic_win_rate", 0),
        "monotonicity": metrics.get("monotonicity", 0),
        "return_volatility": 1.0 / (1.0 + metrics.get("return_volatility", 0) * 10),
        "diversity": metrics.get("diversity", 0),
    }

    total = sum(normalized[k] * weights.get(k, 0) for k in weights)
    return total


def decide(
    champion_score: float,
    new_score: float,
    new_metrics: Dict,
    consecutive_failures: int = 0,
) -> Tuple[str, str]:
    """
    决策 keep/rollback

    Returns:
        (decision, reason)
        decision: "keep" 或 "rollback"
        reason: 决策原因
    """
    diversity = new_metrics.get("diversity", 0)
    ic_mean = new_metrics.get("ic_mean", 0)

    if diversity < 0.5:
        return "rollback", f"分散度不足 ({diversity:.2f} < 0.5)"

    if ic_mean < 0:
        return "rollback", f"IC均值为负 ({ic_mean:.4f})"

    if new_score > champion_score:
        improvement = new_score - champion_score
        return "keep", f"得分提升 +{improvement:.4f}"

    return "rollback", f"得分未提升 ({new_score:.4f} <= {champion_score:.4f})"
