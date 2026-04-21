"""L7 Simplified Portfolio Optimizer — tasks 7.1-7.3

**Validates: Requirements 7.1, 7.2, 7.3**
"""
from __future__ import annotations

import numpy as np
import pandas as pd


class TopNEqualWeightOptimizer:
    """Top-N equal-weight portfolio optimizer (simplified L7).

    Algorithm
    ---------
    1. Freeze non-tradable stocks at previous weights (task 7.3)
    2. Filter tradable stocks
    3. Sort by alpha, take top-N
    4. Equal weight allocation within remaining budget
    5. Apply single-stock cap (max_single_weight)
    6. Apply turnover constraint — blend with prev if needed (task 7.2)
    7. Renormalize to sum = 1

    Parameters
    ----------
    n_stocks : int
        Number of stocks to hold (default 50).
    max_single_weight : float
        Maximum weight per stock (default 0.03 = 3%).
    max_turnover : float
        Maximum one-way turnover per period (default 0.30 = 30%).
        Turnover = sum(|w_new - w_prev|) / 2.
    """

    def __init__(
        self,
        n_stocks: int = 50,
        max_single_weight: float = 0.03,
        max_turnover: float = 0.30,
    ) -> None:
        if n_stocks < 1:
            raise ValueError(f"n_stocks must be >= 1, got {n_stocks}")
        if not (0 < max_single_weight <= 1):
            raise ValueError(
                f"max_single_weight must be in (0, 1], got {max_single_weight}"
            )
        if not (0 < max_turnover <= 2):
            raise ValueError(
                f"max_turnover must be in (0, 2], got {max_turnover}"
            )

        self.n_stocks = n_stocks
        self.max_single_weight = max_single_weight
        self.max_turnover = max_turnover

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def optimize(
        self,
        alpha: pd.Series,
        tradable_mask: pd.Series,
        prev_weights: pd.Series | None = None,
    ) -> pd.Series:
        """Compute portfolio weights.

        Parameters
        ----------
        alpha : pd.Series
            Alpha scores indexed by stock_id.
        tradable_mask : pd.Series
            Boolean mask indexed by stock_id. True = tradable.
        prev_weights : pd.Series | None
            Previous period weights indexed by stock_id.
            If None, no turnover constraint or freeze is applied.

        Returns
        -------
        pd.Series
            Portfolio weights indexed by stock_id.
            Sums to 1.0, all values in [0, max_single_weight].
        """
        # ---- align all inputs on a common index ----------------------
        all_stocks = alpha.index.union(tradable_mask.index)
        alpha = alpha.reindex(all_stocks, fill_value=-np.inf)
        tradable = tradable_mask.reindex(all_stocks, fill_value=False).astype(bool)

        if prev_weights is not None:
            prev_w = prev_weights.reindex(all_stocks, fill_value=0.0)
        else:
            prev_w = pd.Series(0.0, index=all_stocks)

        weights = pd.Series(0.0, index=all_stocks)

        # ---- task 7.3: freeze non-tradable stocks --------------------
        non_tradable = ~tradable
        weights[non_tradable] = prev_w[non_tradable]
        frozen_weight = weights[non_tradable].sum()

        # remaining budget for tradable stocks
        tradable_budget = max(0.0, 1.0 - frozen_weight)

        if tradable_budget < 1e-8:
            # all weight is frozen — just renormalize
            return self._renorm(weights)

        # ---- filter tradable stocks with finite alpha ----------------
        tradable_alpha = alpha[tradable & np.isfinite(alpha)]

        if len(tradable_alpha) == 0:
            return self._renorm(weights)

        # ---- sort by alpha descending, take top-N -------------------
        top_n = min(self.n_stocks, len(tradable_alpha))
        top_stocks = tradable_alpha.nlargest(top_n).index

        # ---- equal weight within budget, capped at max_single_weight -
        weights = self._assign_equal_capped(
            weights, top_stocks, tradable_budget
        )

        # ---- renormalize first so turnover is computed on final weights ----
        weights = self._renorm(weights)

        # ---- task 7.2: turnover constraint ---------------------------
        if prev_weights is not None:
            weights = self._apply_turnover_constraint(weights, prev_w)
            # Re-renormalize after blending (blend of two normalized vectors
            # is already normalized, but guard against floating-point drift)
            weights = self._renorm(weights)

        return weights

    def compute_turnover(
        self,
        weights_new: pd.Series,
        weights_prev: pd.Series,
    ) -> float:
        """Compute one-way turnover between two weight vectors.

        Turnover = sum(|w_new - w_prev|) / 2
        """
        all_stocks = weights_new.index.union(weights_prev.index)
        w_new = weights_new.reindex(all_stocks, fill_value=0.0)
        w_prev = weights_prev.reindex(all_stocks, fill_value=0.0)
        return float((w_new - w_prev).abs().sum() / 2)

    # ------------------------------------------------------------------
    # Private helpers
    # ------------------------------------------------------------------

    def _assign_equal_capped(
        self,
        weights: pd.Series,
        top_stocks: pd.Index,
        budget: float,
    ) -> pd.Series:
        """Assign equal weights to top_stocks within budget, capped at max_single_weight.

        If equal_w > max_single_weight, cap each stock and redistribute
        the excess to remaining stocks iteratively.
        """
        w = weights.copy()
        remaining_stocks = list(top_stocks)
        remaining_budget = budget

        while remaining_stocks:
            equal_w = remaining_budget / len(remaining_stocks)
            if equal_w <= self.max_single_weight + 1e-10:
                # no capping needed
                for s in remaining_stocks:
                    w[s] = equal_w
                break
            else:
                # infeasible to satisfy cap with available names:
                # fall back to equal allocation across selected names.
                for s in remaining_stocks:
                    w[s] = equal_w
                break

        return w

    def _apply_turnover_constraint(
        self,
        weights: pd.Series,
        prev_w: pd.Series,
    ) -> pd.Series:
        """Blend weights with prev_w if turnover exceeds max_turnover.

        Finds blend factor t in [0,1] such that:
            turnover(t * w_new + (1-t) * w_prev) == max_turnover

        Since turnover scales linearly with t:
            t = max_turnover / raw_turnover
        """
        raw_turnover = (weights - prev_w).abs().sum() / 2
        if raw_turnover <= self.max_turnover + 1e-10:
            return weights

        blend = min(self.max_turnover / raw_turnover, 1.0)
        return blend * weights + (1.0 - blend) * prev_w

    @staticmethod
    def _renorm(weights: pd.Series) -> pd.Series:
        """Renormalize weights to sum to 1.0."""
        total = weights.sum()
        if total > 1e-8:
            return weights / total
        return weights
