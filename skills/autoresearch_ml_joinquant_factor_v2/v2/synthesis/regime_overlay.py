"""L6 软性 Regime Overlay 模块 (Task 10.3) — Phase 2

单一全局调节系数，先压缩 regime 指标为 1~2 个状态变量，
再用低自由度映射（adj_t = clip(a + b·z, 0.9, 1.1)）。
Phase 1 默认关闭。

**Validates: Requirements 7**
"""

from __future__ import annotations

import logging

import numpy as np
import pandas as pd

logger = logging.getLogger(__name__)


class SoftRegimeOverlay:
    """软性 Regime Overlay（L6）。

    输出单一全局调节系数 adj_t，不对不同家族做独立调节。
    调节系数：adj_t = clip(a + b · z_regime_t, lower, upper)
    默认区间 [0.9, 1.1]。

    Phase 1 默认关闭。

    **Validates: Requirements 7**
    """

    def __init__(
        self,
        enabled: bool = False,
        lower: float = 0.9,
        upper: float = 1.1,
    ):
        self.enabled = enabled
        self.lower = lower
        self.upper = upper
        self._a = 1.0
        self._b = 0.0

    def fit(
        self,
        regime_indicators: pd.DataFrame,
        alpha: pd.Series,
        label: pd.Series,
    ) -> "SoftRegimeOverlay":
        """拟合 regime overlay 参数（inner loop 中选择）。"""
        if not self.enabled:
            logger.info("SoftRegimeOverlay: 已关闭，跳过训练")
            return self

        # TODO: Phase 2 实现完整的 regime 参数拟合
        # 当前 stub：a=1.0, b=0.0（无调节）
        logger.info("SoftRegimeOverlay: stub 实现，a=1.0, b=0.0（无调节）")
        return self

    def adjust(
        self,
        alpha: pd.Series,
        regime_indicators: pd.DataFrame | None = None,
    ) -> pd.Series:
        """应用 regime 调节。

        Parameters
        ----------
        alpha : pd.Series
            合成 alpha。
        regime_indicators : pd.DataFrame | None
            当前 regime 指标。

        Returns
        -------
        pd.Series
            调节后的 alpha。
        """
        if not self.enabled:
            return alpha

        if regime_indicators is None or regime_indicators.empty:
            return alpha

        # 压缩 regime 指标为单一状态变量（PCA 第一主成分）
        try:
            from sklearn.decomposition import PCA
            pca = PCA(n_components=1)
            z = pca.fit_transform(regime_indicators.fillna(0).values).flatten()
            z_mean = float(np.mean(z))
        except Exception:
            z_mean = 0.0

        adj = float(np.clip(self._a + self._b * z_mean, self.lower, self.upper))
        logger.debug("SoftRegimeOverlay: adj_t=%.4f", adj)
        return alpha * adj
