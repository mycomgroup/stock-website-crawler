"""Freshness Decay 模块 (Task 10.5) — Phase 2

计算 c_{g,t} = exp(-age_{g,t} / tau_g)，作为 stack 输入特征或置信度权重。
禁止直接乘到因子值上。

**Validates: Requirements 13**
"""

from __future__ import annotations

import logging

import numpy as np
import pandas as pd

logger = logging.getLogger(__name__)

# 各家族的特征衰减时间常数（天）
DEFAULT_TAU = {
    "basics": 90,      # 季报，约 90 天
    "emotion": 7,      # 情绪指标，约 1 周
    "growth": 90,      # 季报
    "momentum": 30,    # 动量，约 1 个月
    "pershare": 90,    # 季报
    "quality": 90,     # 季报
    "risk": 30,        # 风险指标，约 1 个月
    "style": 30,       # 风格因子
    "technical": 7,    # 技术指标，约 1 周
}


class FreshnessDecayModule:
    """Freshness Decay 模块（L5 辅助）。

    计算每个因子在每个再平衡日的 age_in_days（距上次更新的天数），
    以及 freshness decay 权重 c_{g,t} = exp(-age_{g,t} / tau_g)。

    **禁止**将 c_{g,t} 直接乘到原始因子值上。
    只允许用于：
    1. 作为额外特征输入模型
    2. 作为组内/组间分数的置信度权重
    3. 作为 horizon calibration 的附加输入

    **Validates: Requirements 13**
    """

    def __init__(self, tau_map: dict[str, float] | None = None):
        """
        Parameters
        ----------
        tau_map : dict[str, float] | None
            家族 → 衰减时间常数（天）的映射。
            默认使用 DEFAULT_TAU。
        """
        self.tau_map = tau_map or DEFAULT_TAU

    def compute_age_in_days(
        self,
        df: pd.DataFrame,
        factor_col: str,
        date_col: str = "date",
        stock_col: str = "stock_id",
    ) -> pd.Series:
        """计算每行（date, stock_id）的因子 age_in_days。

        Age = 当前截面日期 - 该股票该因子最近一次非 NaN 的日期。

        Parameters
        ----------
        df : pd.DataFrame
            因子面板数据。
        factor_col : str
            因子列名。
        date_col : str
            日期列名。
        stock_col : str
            股票 ID 列名。

        Returns
        -------
        pd.Series
            age_in_days，indexed by df.index。
        """
        df_sorted = df.sort_values([stock_col, date_col])
        age = pd.Series(index=df.index, dtype=float)

        for stock, group in df_sorted.groupby(stock_col):
            last_valid_date = None
            for idx, row in group.iterrows():
                if pd.notna(row[factor_col]):
                    last_valid_date = row[date_col]
                    age[idx] = 0.0
                elif last_valid_date is not None:
                    delta = (row[date_col] - last_valid_date).days
                    age[idx] = float(delta)
                else:
                    age[idx] = float("nan")

        return age

    def compute_freshness_weight(
        self,
        age_in_days: pd.Series,
        family_name: str,
    ) -> pd.Series:
        """计算 freshness decay 权重。

        c_{g,t} = exp(-age_{g,t} / tau_g)

        Parameters
        ----------
        age_in_days : pd.Series
            因子 age（天数）。
        family_name : str
            家族名称（用于查找 tau_g）。

        Returns
        -------
        pd.Series
            Freshness 权重，范围 (0, 1]。
        """
        tau = self.tau_map.get(family_name, 30.0)
        weights = np.exp(-age_in_days / tau)
        return weights.clip(0.0, 1.0)
