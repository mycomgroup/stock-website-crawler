"""L4 Cross-family synthesis — tasks 6.1-6.4"""
from __future__ import annotations
import numpy as np
import pandas as pd


def _ridge_fit(
    X: np.ndarray,
    y: np.ndarray,
    alpha: float,
) -> np.ndarray:
    """Fit ridge regression coefficients with NumPy."""
    n_features = X.shape[1]
    reg = float(alpha) * np.eye(n_features)
    return np.linalg.solve(X.T @ X + reg, X.T @ y)


def predict_alpha_linear(
    S: pd.DataFrame,
    beta: pd.Series,
) -> pd.Series:
    """Compute linear alpha: alpha_linear[t,i] = Σ_g β_{t,g} · s_g[t,i]

    Parameters
    ----------
    S : pd.DataFrame
        Family scores matrix, columns = family names, index = (date, stock_id).
    beta : pd.Series
        Family weights, index = family names.

    Returns
    -------
    pd.Series
        Linear alpha, indexed by (date, stock_id).
    """
    common_families = [c for c in S.columns if c in beta.index]
    if not common_families:
        raise ValueError("No common families between S and beta")

    alpha = S[common_families].fillna(0) @ beta[common_families]
    alpha.name = "alpha_linear"
    return alpha


class CrossFamilyModel:
    """Rolling ridge/elastic net for cross-family synthesis (L4).

    Input: OOF family scores matrix S[t, i, G]
    Output: alpha_linear[t, i]

    Must use OOF family scores (not in-sample).

    Parameters
    ----------
    alpha_reg_grid : list[float]
        Grid of regularization strengths.
        Default: [0.001, 0.01, 0.1, 1.0, 10.0]
    l1_ratio_grid : list[float]
        Grid of L1 ratios (0.0 = pure ridge).
        Default: [0.0, 0.1, 0.5]
    max_single_family_weight : float
        Maximum absolute weight for any single family (default 0.4).
    weight_smoothing_halflife : int
        Half-life for exponential smoothing of weights (default 4 periods).
    allow_negative : bool
        Whether to allow mild negative weights (default True).
    """

    def __init__(
        self,
        alpha_reg_grid: list[float] | None = None,
        l1_ratio_grid: list[float] | None = None,
        max_single_family_weight: float = 0.4,
        weight_smoothing_halflife: int = 4,
        allow_negative: bool = True,
    ):
        self.alpha_reg_grid = alpha_reg_grid or [0.001, 0.01, 0.1, 1.0, 10.0]
        self.l1_ratio_grid = l1_ratio_grid or [0.0, 0.1, 0.5]
        self.max_single_family_weight = max_single_family_weight
        self.weight_smoothing_halflife = weight_smoothing_halflife
        self.allow_negative = allow_negative

        self._beta_history: list[pd.Series] = []
        self._current_beta: pd.Series | None = None

    def fit(
        self,
        S_train: pd.DataFrame,
        y_train: pd.Series,
        best_alpha: float = 1.0,
        best_l1_ratio: float = 0.0,
    ) -> "CrossFamilyModel":
        """Fit the cross-family model on OOF family scores.

        Parameters
        ----------
        S_train : pd.DataFrame
            OOF family scores matrix (must be OOF, not in-sample).
            Columns = family names, index = (date, stock_id).
        y_train : pd.Series
            Target labels (decision horizon returns).
        best_alpha : float
            Regularization strength (from inner loop).
        best_l1_ratio : float
            L1 ratio (0.0 = pure ridge, from inner loop).

        Returns
        -------
        self
        """
        common_idx = S_train.index.intersection(y_train.index)
        if len(common_idx) < 10:
            raise ValueError(f"Insufficient training data: {len(common_idx)} samples")

        X = S_train.loc[common_idx].fillna(0).values
        y = y_train.loc[common_idx].fillna(0).values

        # 当前本地实现不依赖 sklearn：统一使用 ridge 闭式解。
        raw_coef = _ridge_fit(X=X, y=y, alpha=best_alpha)
        raw_beta = pd.Series(raw_coef, index=S_train.columns)

        # Apply weight constraints (single-family cap)
        beta = self._apply_weight_constraints(raw_beta)

        # Exponential smoothing with previous beta
        if self._current_beta is not None:
            beta = self._smooth_beta(beta, self._current_beta)

        self._beta_history.append(beta.copy())
        self._current_beta = beta

        return self

    def predict(self, S_test: pd.DataFrame) -> pd.Series:
        """Predict alpha_linear on test family scores.

        Parameters
        ----------
        S_test : pd.DataFrame
            Family scores matrix for test period.

        Returns
        -------
        pd.Series
            Linear alpha predictions.
        """
        if self._current_beta is None:
            raise RuntimeError("Model not fitted. Call fit() first.")

        return predict_alpha_linear(S_test, self._current_beta)

    def _apply_weight_constraints(self, beta: pd.Series) -> pd.Series:
        """Apply single-family weight cap (task 6.3).

        Single family cap: 0.4
        Allow mild negative weights when allow_negative=True.
        """
        lower = -self.max_single_family_weight if self.allow_negative else 0.0
        upper = self.max_single_family_weight
        return beta.clip(lower=lower, upper=upper)

    def _smooth_beta(self, beta_new: pd.Series, beta_prev: pd.Series) -> pd.Series:
        """Exponential smoothing of beta weights (task 6.3).

        Half-life = weight_smoothing_halflife rebalancing periods.
        alpha_smooth = 1 - 0.5^(1/halflife)
        """
        alpha_smooth = 1.0 - 0.5 ** (1.0 / self.weight_smoothing_halflife)
        prev_aligned = beta_prev.reindex(beta_new.index, fill_value=0.0)
        smoothed = alpha_smooth * beta_new + (1.0 - alpha_smooth) * prev_aligned
        return smoothed

    def select_hyperparams(
        self,
        S_train: pd.DataFrame,
        y_train: pd.Series,
        validation_fraction: float = 0.2,
    ) -> tuple[float, float]:
        """Select best hyperparameters via inner loop CV (task 6.2).

        Grid search over alpha_reg_grid × l1_ratio_grid.
        Uses rank IC on validation set as selection criterion.

        Returns
        -------
        tuple[float, float]
            (best_alpha_reg, best_l1_ratio)
        """
        dates = sorted(S_train.index.get_level_values("date").unique())
        n_val = max(1, int(len(dates) * validation_fraction))

        train_dates = dates[:-n_val]
        val_dates = dates[-n_val:]

        train_mask = S_train.index.get_level_values("date").isin(train_dates)
        val_mask = S_train.index.get_level_values("date").isin(val_dates)

        S_inner_train = S_train[train_mask]
        y_inner_train = y_train[y_train.index.isin(S_inner_train.index)]
        S_inner_val = S_train[val_mask]
        y_inner_val = y_train[y_train.index.isin(S_inner_val.index)]

        best_score = -np.inf
        best_alpha = self.alpha_reg_grid[0]
        best_l1 = self.l1_ratio_grid[0]

        for alpha_reg in self.alpha_reg_grid:
            for l1_ratio in self.l1_ratio_grid:
                model_copy = CrossFamilyModel(
                    alpha_reg_grid=[alpha_reg],
                    l1_ratio_grid=[l1_ratio],
                    max_single_family_weight=self.max_single_family_weight,
                    allow_negative=self.allow_negative,
                )
                model_copy.fit(S_inner_train, y_inner_train, alpha_reg, l1_ratio)
                preds = model_copy.predict(S_inner_val)

                common = preds.index.intersection(y_inner_val.index)
                if len(common) < 5:
                    continue

                # Rank IC as selection criterion
                ic = preds.loc[common].rank().corr(y_inner_val.loc[common].rank())
                if np.isfinite(ic) and ic > best_score:
                    best_score = ic
                    best_alpha = alpha_reg
                    best_l1 = l1_ratio

        return best_alpha, best_l1

    @property
    def current_beta(self) -> pd.Series | None:
        """Current (most recent) family weights."""
        return self._current_beta

    @property
    def beta_history(self) -> list[pd.Series]:
        """History of all fitted beta vectors."""
        return self._beta_history
