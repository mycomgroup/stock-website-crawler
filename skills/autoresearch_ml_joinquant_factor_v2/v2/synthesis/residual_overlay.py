"""L5 非线性残差增强模块 (Task 10.1, 10.2) — Phase 2

GBDT 拟合线性主模型残差，提供非线性边际增益。
第一阶段（Phase 1）默认关闭，eta 固定为 0。

**Validates: Requirements 6**
"""

from __future__ import annotations

import logging
import warnings

import numpy as np
import pandas as pd

logger = logging.getLogger(__name__)


class ResidualGBDTOverlay:
    """GBDT 残差增强模块（L5）。

    只拟合线性主模型的残差：r_residual = y - alpha_linear
    最终 alpha：alpha_final = alpha_linear + η · alpha_nonlinear

    η 通过 inner loop 从 [0, 0.05, 0.10, 0.20, 0.30] 选择。
    η=0 必须永远保留为合法选项。

    Phase 1 默认关闭（eta=0）。

    **Validates: Requirements 6**
    """

    ETA_GRID = [0, 0.05, 0.10, 0.20, 0.30]

    def __init__(self, eta: float = 0.0, enabled: bool = False):
        """
        Parameters
        ----------
        eta : float
            混合系数（默认 0，Phase 1 关闭）。
        enabled : bool
            是否启用非线性 overlay（默认 False）。
        """
        if eta not in self.ETA_GRID:
            raise ValueError(f"eta 必须在 {self.ETA_GRID} 中，got {eta}")
        self.eta = eta
        self.enabled = enabled
        self._model = None

    def fit(
        self,
        X_train: pd.DataFrame,
        alpha_linear_train: pd.Series,
        y_train: pd.Series,
    ) -> "ResidualGBDTOverlay":
        """拟合 GBDT 残差模型（OOF）。

        Parameters
        ----------
        X_train : pd.DataFrame
            训练集特征（清洗后因子）。
        alpha_linear_train : pd.Series
            线性主模型的 OOF 预测。
        y_train : pd.Series
            训练集标签。
        """
        if not self.enabled or self.eta == 0:
            logger.info("ResidualGBDTOverlay: 已关闭（eta=0），跳过训练")
            return self

        try:
            from sklearn.ensemble import GradientBoostingRegressor
        except ImportError:
            logger.warning("sklearn 未安装，ResidualGBDTOverlay 无法训练")
            return self

        # 计算残差
        common_idx = alpha_linear_train.index.intersection(y_train.index)
        r_residual = y_train.loc[common_idx] - alpha_linear_train.loc[common_idx]

        X_aligned = X_train.loc[common_idx].fillna(0)
        valid_mask = np.isfinite(r_residual.values) & np.isfinite(X_aligned.values).all(axis=1)

        if valid_mask.sum() < 50:
            logger.warning("ResidualGBDTOverlay: 有效训练样本不足（%d），跳过", valid_mask.sum())
            return self

        self._model = GradientBoostingRegressor(
            max_depth=4,
            n_estimators=100,
            subsample=0.8,
            random_state=42,
        )
        self._model.fit(X_aligned.values[valid_mask], r_residual.values[valid_mask])
        logger.info("ResidualGBDTOverlay: GBDT 残差模型训练完成")
        return self

    def predict(
        self,
        X_test: pd.DataFrame,
        alpha_linear: pd.Series,
    ) -> pd.Series:
        """预测最终 alpha。

        Parameters
        ----------
        X_test : pd.DataFrame
            测试集特征。
        alpha_linear : pd.Series
            线性主模型预测。

        Returns
        -------
        pd.Series
            alpha_final = alpha_linear + eta * alpha_nonlinear
        """
        if not self.enabled or self.eta == 0 or self._model is None:
            return alpha_linear

        X_aligned = X_test.reindex(alpha_linear.index).fillna(0)
        alpha_nl = pd.Series(
            self._model.predict(X_aligned.values),
            index=alpha_linear.index,
        )
        return alpha_linear + self.eta * alpha_nl

    def check_admission_criteria(
        self,
        oof_ir_baseline: float,
        oof_ir_with_overlay: float,
        turnover_baseline: float,
        turnover_with_overlay: float,
        bootstrap_p_value: float = 1.0,
    ) -> bool:
        """检查 L5 准入条件（Task 10.2）。

        准入条件（全部满足才允许 η > 0）：
        1. OOF 成本后 IR 提升 > 5%
        2. block-bootstrap 置信区间支持增益为正（p < 0.1）
        3. 换手增幅 < 20%

        Returns
        -------
        bool
            是否满足准入条件。
        """
        ir_improvement = (oof_ir_with_overlay - oof_ir_baseline) / max(abs(oof_ir_baseline), 1e-8)
        turnover_increase = (turnover_with_overlay - turnover_baseline) / max(turnover_baseline, 1e-8)

        passes = (
            ir_improvement > 0.05
            and bootstrap_p_value < 0.1
            and turnover_increase < 0.20
        )

        logger.info(
            "L5 准入条件：IR提升=%.2f%%, bootstrap_p=%.3f, 换手增幅=%.2f%%, passes=%s",
            ir_improvement * 100,
            bootstrap_p_value,
            turnover_increase * 100,
            passes,
        )
        return passes
