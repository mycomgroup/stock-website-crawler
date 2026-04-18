"""L2 因子冗余检测与准入管理模块 (redundancy.py)

实现：
1. 有效维度计算 (compute_effective_dimension)
2. 冗余因子对检测 (detect_redundant_pairs)
3. 因子准入/淘汰三段式流程 (FactorAdmissionManager)

**Validates: Requirements 3.2, 3.3, 3.4**
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Literal

import numpy as np
import pandas as pd
from scipy import stats


# ---------------------------------------------------------------------------
# 有效维度计算
# ---------------------------------------------------------------------------


def compute_effective_dimension(corr_matrix: np.ndarray) -> float:
    """计算相关矩阵的有效维度。

    有效维度公式：n_eff = (Σλ_j)² / Σλ_j²
    其中 λ_j 是相关矩阵的特征值。

    有效维度衡量因子集合的独立信息量：
    - n_eff = K：所有因子完全独立
    - n_eff = 1：所有因子完全共线
    - 1 < n_eff < K：存在部分冗余

    **Validates: Requirements 3.2**

    参数
    ----
    corr_matrix : np.ndarray
        相关矩阵（K×K），应为对称正定矩阵

    返回
    ----
    float
        有效维度 n_eff，范围 [1, K]

    异常
    ----
    ValueError
        若输入不是方阵或包含 NaN/Inf
    """
    if corr_matrix.ndim != 2:
        raise ValueError(f"相关矩阵必须是二维数组，实际维度: {corr_matrix.ndim}")

    if corr_matrix.shape[0] != corr_matrix.shape[1]:
        raise ValueError(
            f"相关矩阵必须是方阵，实际形状: {corr_matrix.shape}"
        )

    if not np.isfinite(corr_matrix).all():
        raise ValueError("相关矩阵包含 NaN 或 Inf")

    # 计算特征值（只需特征值，不需特征向量）
    eigenvalues = np.linalg.eigvalsh(corr_matrix)

    # 过滤负特征值（数值误差导致）
    eigenvalues = eigenvalues[eigenvalues > 1e-10]

    if len(eigenvalues) == 0:
        return 1.0

    # 有效维度公式
    sum_eig = np.sum(eigenvalues)
    sum_eig_sq = np.sum(eigenvalues**2)

    if sum_eig_sq < 1e-10:
        return 1.0

    n_eff = (sum_eig**2) / sum_eig_sq
    return float(n_eff)


def compute_family_effective_dimensions(
    df: pd.DataFrame,
    family_map: dict[str, list[str]],
    min_periods: int = 20,
) -> dict[str, float]:
    """计算各家族的有效维度。

    对每个家族，计算其因子集合的截面 rank 相关矩阵，
    然后计算有效维度 n_eff。

    **Validates: Requirements 3.2**

    参数
    ----
    df : pd.DataFrame
        因子面板数据，包含 date / stock_id / factor_* 列
    family_map : dict[str, list[str]]
        家族映射字典，family_name → list of factor names
    min_periods : int
        计算相关矩阵所需的最小截面数（默认 20）

    返回
    ----
    dict[str, float]
        各家族的有效维度，family_name → n_eff

    异常
    ----
    ValueError
        若某家族的因子列在 df 中不存在
    """
    result: dict[str, float] = {}

    for family, factors in family_map.items():
        # 检查因子列是否存在
        missing = [f for f in factors if f not in df.columns]
        if missing:
            raise ValueError(
                f"家族 '{family}' 的因子列在数据中不存在: {missing[:5]}..."
            )

        # 提取因子数据
        factor_data = df[factors].copy()

        # 按截面计算 rank（归一化到 [0, 1]）
        dates = df["date"].unique() if "date" in df.columns else [0]
        if len(dates) < min_periods:
            result[family] = float(len(factors))  # 样本不足，返回因子数
            continue

        # 计算截面 rank 相关矩阵
        rank_corr_list = []
        for date in dates:
            if "date" in df.columns:
                cross_section = df[df["date"] == date][factors]
            else:
                cross_section = factor_data

            # 截面 rank 归一化
            ranked = cross_section.rank(axis=0, pct=True)
            if ranked.notna().sum().min() >= 5:  # 至少 5 个有效样本
                rank_corr_list.append(ranked)

        if len(rank_corr_list) < min_periods:
            result[family] = float(len(factors))
            continue

        # 合并所有截面，计算相关矩阵
        all_ranks = pd.concat(rank_corr_list, axis=0)
        corr_matrix = all_ranks.corr(method="spearman").values

        # 处理 NaN（用单位矩阵替代）
        if np.isnan(corr_matrix).any():
            corr_matrix = np.eye(len(factors))

        # 计算有效维度
        n_eff = compute_effective_dimension(corr_matrix)
        result[family] = n_eff

    return result


# ---------------------------------------------------------------------------
# 冗余因子对检测
# ---------------------------------------------------------------------------


def detect_redundant_pairs(
    df: pd.DataFrame,
    factor_cols: list[str],
    threshold: float = 0.8,
    min_periods: int = 20,
) -> list[tuple[str, str, float]]:
    """识别长期截面相关性高于阈值的因子对。

    计算因子对之间的 rolling 截面 rank IC 相关性，
    识别长期平均相关性超过阈值的因子对。

    **Validates: Requirements 3.3**

    参数
    ----
    df : pd.DataFrame
        因子面板数据，包含 date / stock_id / factor_* 列
    factor_cols : list[str]
        待检测的因子列名列表
    threshold : float
        冗余阈值（默认 0.8），相关性超过此值视为冗余
    min_periods : int
        计算相关性所需的最小截面数（默认 20）

    返回
    ----
    list[tuple[str, str, float]]
        冗余因子对列表，每个元素为 (factor1, factor2, correlation)
        按相关性从高到低排序

    异常
    ----
    ValueError
        若因子列在 df 中不存在
    """
    # 检查因子列是否存在
    missing = [f for f in factor_cols if f not in df.columns]
    if missing:
        raise ValueError(f"因子列在数据中不存在: {missing[:5]}...")

    if len(factor_cols) < 2:
        return []

    # 按日期分组，计算截面 rank
    if "date" not in df.columns:
        # 无日期列，视为单截面
        ranked = df[factor_cols].rank(axis=0, pct=True)
        corr_matrix = ranked.corr(method="spearman")
    else:
        dates = sorted(df["date"].unique())
        if len(dates) < min_periods:
            return []

        # 计算所有截面的 rank，然后计算相关矩阵
        rank_list = []
        for date in dates:
            cross_section = df[df["date"] == date][factor_cols]
            ranked = cross_section.rank(axis=0, pct=True)
            if ranked.notna().sum().min() >= 5:
                rank_list.append(ranked)

        if len(rank_list) < min_periods:
            return []

        all_ranks = pd.concat(rank_list, axis=0)
        corr_matrix = all_ranks.corr(method="spearman")

    # 提取上三角（避免重复和自相关）
    redundant_pairs: list[tuple[str, str, float]] = []
    n = len(factor_cols)
    for i in range(n):
        for j in range(i + 1, n):
            corr = corr_matrix.iloc[i, j]
            if not np.isnan(corr) and abs(corr) > threshold:
                redundant_pairs.append(
                    (factor_cols[i], factor_cols[j], float(corr))
                )

    # 按相关性绝对值从高到低排序
    redundant_pairs.sort(key=lambda x: abs(x[2]), reverse=True)
    return redundant_pairs


# ---------------------------------------------------------------------------
# 因子准入/淘汰三段式流程
# ---------------------------------------------------------------------------

DecaySpeed = Literal["fast", "medium", "slow"]


@dataclass
class FactorStatus:
    """因子状态记录。"""

    factor_name: str
    decay_speed: DecaySpeed
    stage: Literal["shadow_pool", "observation", "active", "retired"]
    observation_start_date: int | None = None  # 进入观察期的窗口索引
    observation_periods: int = 0  # 已观察的窗口数
    negative_contribution_streak: int = 0  # 连续负贡献窗口数
    cumulative_ic_contribution: float = 0.0  # 累积 IC 贡献


@dataclass
class FactorAdmissionManager:
    """因子准入/淘汰三段式管理器。

    三个阶段：
    1. shadow_pool：新因子进入影子池，不参与实际合成
    2. observation：观察期，参与合成但权重受限，评估增量贡献
    3. active：正式纳入，全权重参与合成
    4. retired：淘汰，连续 4~6 个窗口负贡献后退出

    观察期长度（窗口数）：
    - fast: 6~12 个月（假设月度再平衡，6~12 个窗口）
    - medium: 12~18 个月（12~18 个窗口）
    - slow: 18~24 个月（18~24 个窗口）

    淘汰条件：
    - 连续 4~6 个评估窗口 OOF 增量贡献为负

    **Validates: Requirements 3.4**
    """

    factors: dict[str, FactorStatus] = field(default_factory=dict)
    current_window: int = 0
    observation_periods_map: dict[DecaySpeed, tuple[int, int]] = field(
        default_factory=lambda: {
            "fast": (6, 12),
            "medium": (12, 18),
            "slow": (18, 24),
        }
    )
    retirement_streak_threshold: int = 5  # 连续负贡献窗口数阈值

    def add_to_shadow_pool(
        self, factor_name: str, decay_speed: DecaySpeed
    ) -> None:
        """将新因子加入影子池。

        参数
        ----
        factor_name : str
            因子名称
        decay_speed : DecaySpeed
            衰减速度（"fast" / "medium" / "slow"）

        异常
        ----
        ValueError
            若因子已存在
        """
        if factor_name in self.factors:
            raise ValueError(f"因子 '{factor_name}' 已存在于管理器中")

        self.factors[factor_name] = FactorStatus(
            factor_name=factor_name,
            decay_speed=decay_speed,
            stage="shadow_pool",
        )

    def update(
        self, date: int, oof_ic_contribution: dict[str, float]
    ) -> None:
        """更新因子状态（每个再平衡窗口调用一次）。

        参数
        ----
        date : int
            当前窗口索引（从 0 开始递增）
        oof_ic_contribution : dict[str, float]
            各因子的 OOF 增量 IC 贡献（factor_name → IC）

        流程：
        1. shadow_pool → observation：自动晋升
        2. observation → active：观察期满且累积贡献为正
        3. active → retired：连续负贡献超过阈值
        """
        self.current_window = date

        for factor_name, status in list(self.factors.items()):
            ic_contrib = oof_ic_contribution.get(factor_name, 0.0)

            # 更新累积贡献
            status.cumulative_ic_contribution += ic_contrib

            # 更新负贡献连续计数
            if ic_contrib < 0:
                status.negative_contribution_streak += 1
            else:
                status.negative_contribution_streak = 0

            # 状态转移逻辑
            if status.stage == "shadow_pool":
                # 自动晋升到观察期
                status.stage = "observation"
                status.observation_start_date = date
                status.observation_periods = 0

            elif status.stage == "observation":
                status.observation_periods += 1
                min_periods, max_periods = self.observation_periods_map[
                    status.decay_speed
                ]

                # 观察期满，评估是否晋升
                if status.observation_periods >= min_periods:
                    if status.cumulative_ic_contribution > 0:
                        status.stage = "active"
                    elif status.observation_periods >= max_periods:
                        # 超过最大观察期仍无正贡献，淘汰
                        status.stage = "retired"

            elif status.stage == "active":
                # 检查是否需要淘汰
                if (
                    status.negative_contribution_streak
                    >= self.retirement_streak_threshold
                ):
                    status.stage = "retired"

    def get_active_factors(self) -> list[str]:
        """返回当前活跃因子列表（observation + active）。

        返回
        ----
        list[str]
            活跃因子名称列表
        """
        return [
            name
            for name, status in self.factors.items()
            if status.stage in ("observation", "active")
        ]

    def get_status_report(self) -> dict:
        """返回完整状态报告。

        返回
        ----
        dict
            包含各阶段因子数量、详细状态列表等信息
        """
        stage_counts = {
            "shadow_pool": 0,
            "observation": 0,
            "active": 0,
            "retired": 0,
        }
        for status in self.factors.values():
            stage_counts[status.stage] += 1

        return {
            "current_window": self.current_window,
            "stage_counts": stage_counts,
            "factors": {
                name: {
                    "stage": status.stage,
                    "decay_speed": status.decay_speed,
                    "observation_periods": status.observation_periods,
                    "negative_streak": status.negative_contribution_streak,
                    "cumulative_ic": status.cumulative_ic_contribution,
                }
                for name, status in self.factors.items()
            },
        }
