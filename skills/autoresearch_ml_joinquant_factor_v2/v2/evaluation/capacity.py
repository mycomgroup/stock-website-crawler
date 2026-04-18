"""容量评估模块 (Task 10.8) — Phase 2

资金规模放大 10x 后的 alpha 衰减测试。

**Validates: Requirements 10.5 (Gate 3)**
"""

from __future__ import annotations

import logging

import numpy as np
import pandas as pd

logger = logging.getLogger(__name__)


def estimate_capacity_decay(
    alpha: pd.Series,
    adv_series: pd.Series,
    portfolio_size_base: float = 1e8,
    scale_factor: float = 10.0,
    max_adv_participation: float = 0.10,
    decay_threshold: float = 0.30,
) -> dict:
    """估计资金规模放大后的 alpha 衰减。

    **Validates: Requirements 10.5 (Gate 3)**

    Parameters
    ----------
    alpha : pd.Series
        Alpha 分数，indexed by stock_id。
    adv_series : pd.Series
        日均成交额（ADV），indexed by stock_id。
    portfolio_size_base : float
        基础资金规模（默认 1 亿）。
    scale_factor : float
        放大倍数（默认 10x）。
    max_adv_participation : float
        最大 ADV 参与率（默认 10%）。
    decay_threshold : float
        alpha 衰减阈值（默认 30%，超过则容量不足）。

    Returns
    -------
    dict
        容量评估结果，包含：
        - "alpha_base": 基础规模下的有效 alpha
        - "alpha_scaled": 放大规模下的有效 alpha
        - "decay_ratio": alpha 衰减比例
        - "passes": 是否通过（衰减 < threshold）
    """
    common_stocks = alpha.index.intersection(adv_series.index)
    if len(common_stocks) == 0:
        return {
            "alpha_base": float("nan"),
            "alpha_scaled": float("nan"),
            "decay_ratio": float("nan"),
            "passes": False,
            "error": "无公共股票",
        }

    alpha_clean = alpha.loc[common_stocks]
    adv_clean = adv_series.loc[common_stocks]

    # 基础规模：计算可交易的 alpha（受 ADV 参与率约束）
    max_position_base = adv_clean * max_adv_participation
    tradable_base = max_position_base >= portfolio_size_base * 0.01  # 至少 1% 仓位

    # 放大规模
    portfolio_size_scaled = portfolio_size_base * scale_factor
    max_position_scaled = adv_clean * max_adv_participation
    tradable_scaled = max_position_scaled >= portfolio_size_scaled * 0.01

    # 有效 alpha = 可交易股票的 alpha 均值
    alpha_base = float(alpha_clean[tradable_base].mean()) if tradable_base.sum() > 0 else float("nan")
    alpha_scaled = float(alpha_clean[tradable_scaled].mean()) if tradable_scaled.sum() > 0 else float("nan")

    if abs(alpha_base) < 1e-8:
        decay_ratio = float("nan")
        passes = False
    else:
        decay_ratio = 1.0 - alpha_scaled / alpha_base
        passes = decay_ratio < decay_threshold

    result = {
        "alpha_base": alpha_base,
        "alpha_scaled": alpha_scaled,
        "decay_ratio": decay_ratio,
        "passes": passes,
        "n_tradable_base": int(tradable_base.sum()),
        "n_tradable_scaled": int(tradable_scaled.sum()),
        "portfolio_size_base": portfolio_size_base,
        "portfolio_size_scaled": portfolio_size_scaled,
    }

    logger.info(
        "容量评估：alpha_base=%.4f, alpha_scaled=%.4f, decay=%.2f%%, passes=%s",
        alpha_base,
        alpha_scaled,
        (decay_ratio or 0) * 100,
        passes,
    )
    return result
