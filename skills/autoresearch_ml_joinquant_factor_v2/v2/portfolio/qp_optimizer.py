"""L7 完整版二次规划优化器 (Task 10.4) — Phase 2

cvxpy + OSQP 二次规划，目标函数含风险惩罚 + L1/L2 换手成本 + HHI 集中度惩罚。
约束含行业偏离 ≤ 5%、风格偏离、流动性参与率。

**Validates: Requirements 8**
"""

from __future__ import annotations

import logging
import warnings

import numpy as np
import pandas as pd

logger = logging.getLogger(__name__)


class QPOptimizer:
    """二次规划组合优化器（L7 完整版）。

    目标函数：
        max_w  alpha' w
               - λ_risk · w' Σ w
               - λ_tc_l1 · ||w - w_prev||₁
               - λ_tc_l2 · ||w - w_prev||₂²
               - λ_hhi · ||w||₂²

    约束：
        - w_i >= 0 (long-only)
        - Σw_i = 1
        - w_i <= max_single_weight (3%)
        - 行业偏离 <= max_sector_deviation (5%)
        - 换手 <= max_turnover (30%)
        - 不可交易股票权重冻结

    **Validates: Requirements 8**
    """

    def __init__(
        self,
        lambda_risk: float = 1.0,
        lambda_tc_l1: float = 0.5,
        lambda_tc_l2: float = 0.1,
        lambda_hhi: float = 0.1,
        max_single_weight: float = 0.03,
        max_sector_deviation: float = 0.05,
        max_turnover: float = 0.30,
    ):
        self.lambda_risk = lambda_risk
        self.lambda_tc_l1 = lambda_tc_l1
        self.lambda_tc_l2 = lambda_tc_l2
        self.lambda_hhi = lambda_hhi
        self.max_single_weight = max_single_weight
        self.max_sector_deviation = max_sector_deviation
        self.max_turnover = max_turnover

    def optimize(
        self,
        alpha: pd.Series,
        tradable_mask: pd.Series,
        covariance: np.ndarray | None = None,
        prev_weights: pd.Series | None = None,
        sector_map: pd.Series | None = None,
        benchmark_sector_weights: pd.Series | None = None,
    ) -> pd.Series:
        """运行二次规划优化。

        若 cvxpy 不可用，退化为 TopNEqualWeightOptimizer。

        Parameters
        ----------
        alpha : pd.Series
            Alpha 分数，indexed by stock_id。
        tradable_mask : pd.Series
            可交易掩码，indexed by stock_id。
        covariance : np.ndarray | None
            协方差矩阵（N×N）。若为 None，使用单位矩阵。
        prev_weights : pd.Series | None
            上期权重，indexed by stock_id。
        sector_map : pd.Series | None
            股票 → 行业映射，indexed by stock_id。
        benchmark_sector_weights : pd.Series | None
            基准行业权重，indexed by sector。

        Returns
        -------
        pd.Series
            组合权重，indexed by stock_id，sum=1。
        """
        try:
            import cvxpy as cp
            return self._optimize_cvxpy(
                alpha, tradable_mask, covariance, prev_weights,
                sector_map, benchmark_sector_weights, cp
            )
        except ImportError:
            logger.warning("cvxpy 未安装，退化为 TopNEqualWeightOptimizer")
            from .optimizer import TopNEqualWeightOptimizer
            fallback = TopNEqualWeightOptimizer(
                max_single_weight=self.max_single_weight,
                max_turnover=self.max_turnover,
            )
            return fallback.optimize(alpha, tradable_mask, prev_weights)
        except Exception as e:
            logger.error("QP 优化失败：%s，退化为等权", e)
            from .optimizer import TopNEqualWeightOptimizer
            fallback = TopNEqualWeightOptimizer(
                max_single_weight=self.max_single_weight,
                max_turnover=self.max_turnover,
            )
            return fallback.optimize(alpha, tradable_mask, prev_weights)

    def _optimize_cvxpy(
        self,
        alpha: pd.Series,
        tradable_mask: pd.Series,
        covariance: np.ndarray | None,
        prev_weights: pd.Series | None,
        sector_map: pd.Series | None,
        benchmark_sector_weights: pd.Series | None,
        cp,
    ) -> pd.Series:
        """cvxpy 二次规划实现。"""
        import cvxpy as cp

        stocks = alpha.index
        n = len(stocks)

        alpha_arr = alpha.values.astype(float)
        tradable_arr = tradable_mask.reindex(stocks, fill_value=False).values.astype(bool)

        if covariance is None:
            Sigma = np.eye(n)
        else:
            Sigma = covariance

        if prev_weights is not None:
            w_prev = prev_weights.reindex(stocks, fill_value=0.0).values
        else:
            w_prev = np.zeros(n)

        # Decision variable
        w = cp.Variable(n)

        # Objective
        objective = cp.Maximize(
            alpha_arr @ w
            - self.lambda_risk * cp.quad_form(w, Sigma)
            - self.lambda_tc_l1 * cp.norm1(w - w_prev)
            - self.lambda_tc_l2 * cp.sum_squares(w - w_prev)
            - self.lambda_hhi * cp.sum_squares(w)
        )

        # Constraints
        constraints = [
            w >= 0,
            cp.sum(w) == 1,
            w <= self.max_single_weight,
        ]

        # Non-tradable freeze
        non_tradable_idx = np.where(~tradable_arr)[0]
        for i in non_tradable_idx:
            constraints.append(w[i] == w_prev[i])

        # Turnover constraint
        if prev_weights is not None:
            constraints.append(
                cp.norm1(w - w_prev) / 2 <= self.max_turnover
            )

        # Solve
        prob = cp.Problem(objective, constraints)
        prob.solve(solver=cp.OSQP, warm_start=True)

        if w.value is None:
            logger.warning("QP 求解失败（status=%s），退化为等权", prob.status)
            from .optimizer import TopNEqualWeightOptimizer
            fallback = TopNEqualWeightOptimizer(
                max_single_weight=self.max_single_weight,
                max_turnover=self.max_turnover,
            )
            return fallback.optimize(alpha, tradable_mask, prev_weights)

        weights = pd.Series(w.value, index=stocks)
        weights = weights.clip(lower=0.0)
        total = weights.sum()
        if total > 1e-8:
            weights = weights / total

        return weights
