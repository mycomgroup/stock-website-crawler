"""Block-bootstrap 统计检验模块 (Task 10.6, 10.7) — Phase 2

对 OOF IC 做显著性检验，以及 data snooping 防控（BH 校正）。

**Validates: Requirements 15**
"""

from __future__ import annotations

import logging

import numpy as np
import pandas as pd
from scipy import stats

logger = logging.getLogger(__name__)


def block_bootstrap_ic_test(
    ic_series: pd.Series,
    block_size: int = 4,
    n_bootstrap: int = 1000,
    random_state: int = 42,
) -> dict:
    """Block-bootstrap 对 OOF IC 做显著性检验。

    **Validates: Requirements 15.1**

    Parameters
    ----------
    ic_series : pd.Series
        IC 时间序列。
    block_size : int
        Bootstrap block 大小（默认 4 周）。
    n_bootstrap : int
        Bootstrap 重采样次数（默认 1000）。
    random_state : int
        随机种子。

    Returns
    -------
    dict
        检验结果，包含：
        - "mean_ic": 样本均值
        - "std_ic": 样本标准差
        - "t_stat": t 统计量
        - "p_value": p 值（单侧，H0: IC <= 0）
        - "bootstrap_p_value": bootstrap p 值
        - "is_significant": 是否显著（p < 0.1）
    """
    clean = ic_series.dropna()
    n = len(clean)

    if n < 10:
        return {
            "mean_ic": float("nan"),
            "std_ic": float("nan"),
            "t_stat": float("nan"),
            "p_value": float("nan"),
            "bootstrap_p_value": float("nan"),
            "is_significant": False,
        }

    mean_ic = float(clean.mean())
    std_ic = float(clean.std())

    # t 检验
    t_stat = mean_ic / (std_ic / np.sqrt(n) + 1e-8)
    p_value = float(1 - stats.t.cdf(t_stat, df=n - 1))

    # Block bootstrap
    rng = np.random.default_rng(random_state)
    values = clean.values
    bootstrap_means = []

    for _ in range(n_bootstrap):
        # Moving block bootstrap
        n_blocks = int(np.ceil(n / block_size))
        start_indices = rng.integers(0, max(1, n - block_size + 1), size=n_blocks)
        bootstrap_sample = np.concatenate([
            values[i:i + block_size] for i in start_indices
        ])[:n]
        bootstrap_means.append(float(np.mean(bootstrap_sample)))

    bootstrap_means_arr = np.array(bootstrap_means)
    bootstrap_p_value = float(np.mean(bootstrap_means_arr <= 0))

    return {
        "mean_ic": mean_ic,
        "std_ic": std_ic,
        "t_stat": t_stat,
        "p_value": p_value,
        "bootstrap_p_value": bootstrap_p_value,
        "is_significant": p_value < 0.1,
        "n_periods": n,
    }


def benjamini_hochberg_correction(
    p_values: list[float],
    alpha: float = 0.1,
) -> dict:
    """Benjamini-Hochberg (BH) 多重检验校正。

    **Validates: Requirements 15.2**

    Parameters
    ----------
    p_values : list[float]
        原始 p 值列表。
    alpha : float
        FDR 控制水平（默认 0.1）。

    Returns
    -------
    dict
        校正结果，包含：
        - "adjusted_p_values": BH 校正后的 p 值
        - "rejected": 各假设是否被拒绝（发现显著）
        - "n_significant": 显著结果数量
    """
    n = len(p_values)
    if n == 0:
        return {"adjusted_p_values": [], "rejected": [], "n_significant": 0}

    # BH 校正
    sorted_idx = np.argsort(p_values)
    sorted_p = np.array(p_values)[sorted_idx]

    # BH 临界值：p_(k) <= k/m * alpha
    bh_threshold = np.arange(1, n + 1) / n * alpha
    rejected_sorted = sorted_p <= bh_threshold

    # 找到最大的 k 使得 p_(k) <= k/m * alpha
    if rejected_sorted.any():
        max_k = np.where(rejected_sorted)[0].max()
        rejected_sorted[:max_k + 1] = True

    # 还原原始顺序
    rejected = np.zeros(n, dtype=bool)
    rejected[sorted_idx] = rejected_sorted

    # 计算调整后的 p 值（BH adjusted）
    adjusted_p = np.zeros(n)
    for i, orig_idx in enumerate(sorted_idx):
        adjusted_p[orig_idx] = min(1.0, sorted_p[i] * n / (i + 1))

    return {
        "adjusted_p_values": adjusted_p.tolist(),
        "rejected": rejected.tolist(),
        "n_significant": int(rejected.sum()),
        "n_total": n,
        "fdr_level": alpha,
    }
