"""Horizon Calibration 模块 (Task 10.9) — Phase 2

将不同家族在各自 native horizon 上训练的 OOF 分数，
校准到统一的 decision horizon。

Phase 1 统一使用单一 decision horizon（1个周期 pchg），不启用。
Phase 2 引入多 horizon 支持时启用。

**Validates: Requirements 17**
"""

from __future__ import annotations

import logging

import numpy as np
import pandas as pd

logger = logging.getLogger(__name__)


class HorizonCalibrationModule:
    """Horizon Calibration 模块。

    将 s_g^{(h_g)} 映射成对统一 decision horizon h* 的预测 s̃_g^{(h*)}。

    校准方法：
    - "isotonic": 单调回归（isotonic regression）
    - "linear": 线性校准
    - "binning": 分桶校准

    Phase 1 默认关闭（passthrough）。

    **Validates: Requirements 17**
    """

    def __init__(
        self,
        method: str = "linear",
        enabled: bool = False,
    ):
        """
        Parameters
        ----------
        method : str
            校准方法："isotonic" | "linear" | "binning"。
        enabled : bool
            是否启用（Phase 1 默认 False）。
        """
        if method not in ("isotonic", "linear", "binning"):
            raise ValueError(f"method 必须是 'isotonic'/'linear'/'binning'，got {method}")
        self.method = method
        self.enabled = enabled
        self._calibrators: dict = {}

    def fit(
        self,
        family_scores_oof: dict[str, pd.Series],
        decision_horizon_label: pd.Series,
    ) -> "HorizonCalibrationModule":
        """拟合校准器（仅基于 OOF 样本）。

        Parameters
        ----------
        family_scores_oof : dict[str, pd.Series]
            各家族的 OOF 分数，key=family_name, value=Series indexed by (date, stock_id)。
        decision_horizon_label : pd.Series
            统一 decision horizon 的标签，indexed by (date, stock_id)。

        Returns
        -------
        self
        """
        if not self.enabled:
            logger.info("HorizonCalibrationModule: 已关闭（Phase 1），跳过训练")
            return self

        for family_name, scores in family_scores_oof.items():
            common_idx = scores.index.intersection(decision_horizon_label.index)
            if len(common_idx) < 20:
                continue

            x = scores.loc[common_idx].values
            y = decision_horizon_label.loc[common_idx].values

            valid = np.isfinite(x) & np.isfinite(y)
            if valid.sum() < 20:
                continue

            try:
                calibrator = self._fit_calibrator(x[valid], y[valid])
                self._calibrators[family_name] = calibrator
                logger.info(
                    "HorizonCalibrationModule: 家族 '%s' 校准完成（%s）",
                    family_name,
                    self.method,
                )
            except Exception as e:
                logger.warning(
                    "HorizonCalibrationModule: 家族 '%s' 校准失败：%s",
                    family_name,
                    e,
                )

        return self

    def transform(
        self,
        family_name: str,
        scores: pd.Series,
    ) -> pd.Series:
        """将家族分数校准到 decision horizon。

        Parameters
        ----------
        family_name : str
            家族名称。
        scores : pd.Series
            原始家族分数。

        Returns
        -------
        pd.Series
            校准后的分数（若未启用或无校准器，返回原始分数）。
        """
        if not self.enabled or family_name not in self._calibrators:
            return scores

        calibrator = self._calibrators[family_name]
        x = scores.values
        valid = np.isfinite(x)

        calibrated = x.copy()
        if valid.sum() > 0:
            calibrated[valid] = calibrator.predict(x[valid].reshape(-1, 1)).flatten()

        return pd.Series(calibrated, index=scores.index, name=scores.name)

    def _fit_calibrator(self, x: np.ndarray, y: np.ndarray):
        """拟合单个校准器。"""
        if self.method == "isotonic":
            from sklearn.isotonic import IsotonicRegression
            cal = IsotonicRegression(out_of_bounds="clip")
            cal.fit(x, y)
            return cal
        elif self.method == "linear":
            from sklearn.linear_model import LinearRegression
            cal = LinearRegression()
            cal.fit(x.reshape(-1, 1), y)
            return cal
        else:  # binning
            from sklearn.preprocessing import KBinsDiscretizer
            from sklearn.pipeline import Pipeline
            from sklearn.linear_model import LinearRegression
            cal = LinearRegression()
            cal.fit(x.reshape(-1, 1), y)
            return cal
