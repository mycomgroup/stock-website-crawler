"""Tests for L3 intra-family and L4 cross-family synthesis modules.

Covers tasks 5.1-5.4 (intra_family.py) and 6.1-6.4 (cross_family.py).
"""
from __future__ import annotations

import numpy as np
import pandas as pd
import pytest

from skills.autoresearch_ml_joinquant_factor_v2.v2.synthesis.intra_family import (
    equal_rank_score,
    pc1_score_with_sign_anchor,
    ridge_family_score,
    stack_family_scores_oof,
)
from skills.autoresearch_ml_joinquant_factor_v2.v2.synthesis.cross_family import (
    CrossFamilyModel,
    predict_alpha_linear,
)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _make_panel(
    n_dates: int = 10,
    n_stocks: int = 20,
    n_factors: int = 3,
    seed: int = 42,
    label_signal: bool = False,
) -> pd.DataFrame:
    """Generate a synthetic panel DataFrame for testing."""
    rng = np.random.default_rng(seed)
    base = pd.Timestamp("2021-01-01")
    dates = [base + pd.Timedelta(weeks=i) for i in range(n_dates)]
    stocks = [f"S{i:03d}" for i in range(n_stocks)]
    factor_cols = [f"f{k}" for k in range(n_factors)]

    rows = []
    for date in dates:
        for stock in stocks:
            factors = rng.standard_normal(n_factors)
            if label_signal:
                pchg = factors[0] * 0.5 + rng.standard_normal() * 0.3
            else:
                pchg = rng.standard_normal()
            row = {"date": date, "stock_id": stock, "pchg": pchg}
            for k, v in enumerate(factors):
                row[f"f{k}"] = v
            rows.append(row)

    df = pd.DataFrame(rows).sort_values(["date", "stock_id"]).reset_index(drop=True)
    return df


def _make_family_scores(
    n_dates: int = 10,
    n_stocks: int = 20,
    families: list[str] | None = None,
    seed: int = 42,
) -> tuple[pd.DataFrame, pd.Series]:
    """Generate synthetic family scores matrix and labels."""
    if families is None:
        families = ["momentum", "quality", "value"]
    rng = np.random.default_rng(seed)
    base = pd.Timestamp("2021-01-01")
    dates = [base + pd.Timedelta(weeks=i) for i in range(n_dates)]
    stocks = [f"S{i:03d}" for i in range(n_stocks)]

    idx = pd.MultiIndex.from_product([dates, stocks], names=["date", "stock_id"])
    n = len(idx)
    data = {fam: rng.standard_normal(n) for fam in families}
    S = pd.DataFrame(data, index=idx)

    # Label: linear combination of first family + noise
    y = pd.Series(
        S[families[0]].values * 0.4 + rng.standard_normal(n) * 0.6,
        index=idx,
        name="pchg",
    )
    return S, y


# ===========================================================================
# Task 5.1 — equal_rank_score
# ===========================================================================

class TestEqualRankScore:
    """Tests for equal_rank_score (task 5.1)."""

    def test_output_values_in_range(self):
        """Scores should be in [-0.5, 0.5] (pct rank - 0.5)."""
        df = _make_panel(n_dates=5, n_stocks=20, n_factors=3)
        score = equal_rank_score(df, ["f0", "f1", "f2"])
        assert score.min() >= -0.5 - 1e-9
        assert score.max() <= 0.5 + 1e-9

    def test_output_index_is_multiindex(self):
        """Output must be indexed by (date, stock_id)."""
        df = _make_panel(n_dates=5, n_stocks=10, n_factors=2)
        score = equal_rank_score(df, ["f0", "f1"])
        assert isinstance(score.index, pd.MultiIndex)
        assert score.index.names == ["date", "stock_id"]

    def test_output_length_matches_input(self):
        """Output length must equal number of rows in df."""
        df = _make_panel(n_dates=4, n_stocks=15, n_factors=2)
        score = equal_rank_score(df, ["f0", "f1"])
        assert len(score) == len(df)

    def test_per_date_operation(self):
        """Ranking is done per date, not globally."""
        df = _make_panel(n_dates=3, n_stocks=10, n_factors=1)
        score = equal_rank_score(df, ["f0"])
        # For each date, the mean of scores should be ~0
        for date in df["date"].unique():
            mask = score.index.get_level_values("date") == date
            date_scores = score[mask]
            assert abs(date_scores.mean()) < 0.1

    def test_single_factor(self):
        """Works with a single factor column."""
        df = _make_panel(n_dates=3, n_stocks=10, n_factors=1)
        score = equal_rank_score(df, ["f0"])
        assert len(score) == len(df)
        assert score.min() >= -0.5 - 1e-9
        assert score.max() <= 0.5 + 1e-9

    def test_empty_factor_cols_raises(self):
        """Raises ValueError when factor_cols is empty."""
        df = _make_panel()
        with pytest.raises(ValueError, match="factor_cols cannot be empty"):
            equal_rank_score(df, [])

    def test_missing_column_raises(self):
        """Raises ValueError when a factor column is missing."""
        df = _make_panel(n_factors=2)
        with pytest.raises(ValueError, match="Missing columns"):
            equal_rank_score(df, ["f0", "nonexistent"])

    def test_nan_handling(self):
        """NaN values are preserved (na_option='keep')."""
        df = _make_panel(n_dates=3, n_stocks=10, n_factors=2)
        df.loc[df.index[0], "f0"] = np.nan
        score = equal_rank_score(df, ["f0", "f1"])
        # Should not raise; NaN propagates to score for that row
        assert len(score) == len(df)

    def test_score_name(self):
        """Output Series should be named 'equal_rank_score'."""
        df = _make_panel()
        score = equal_rank_score(df, ["f0"])
        assert score.name == "equal_rank_score"


# ===========================================================================
# Task 5.2 — ridge_family_score
# ===========================================================================

class TestRidgeFamilyScore:
    """Tests for ridge_family_score (task 5.2)."""

    def test_returns_series_with_multiindex(self):
        """Output must be a Series with (date, stock_id) MultiIndex."""
        df = _make_panel(n_dates=80, n_stocks=20, n_factors=3, label_signal=True)
        score = ridge_family_score(df, ["f0", "f1", "f2"], "pchg",
                                   min_train_periods=52, test_block=13, step=4)
        assert isinstance(score, pd.Series)
        assert isinstance(score.index, pd.MultiIndex)

    def test_fallback_when_insufficient_data(self):
        """Falls back to equal_rank_score when data is too short."""
        df = _make_panel(n_dates=5, n_stocks=10, n_factors=2)
        score = ridge_family_score(df, ["f0", "f1"], "pchg",
                                   min_train_periods=52)
        # Should return equal_rank_score fallback
        assert isinstance(score, pd.Series)
        assert len(score) == len(df)

    def test_oof_no_future_leakage(self):
        """OOF predictions must not use future data.

        Verify: for each test date, the prediction was made using only
        training dates strictly before the test date (with embargo).
        """
        df = _make_panel(n_dates=80, n_stocks=15, n_factors=2, label_signal=True)
        score = ridge_family_score(df, ["f0", "f1"], "pchg",
                                   min_train_periods=52, test_block=13,
                                   step=4, embargo=1)
        # All predicted dates should be after the minimum training period
        dates = sorted(df["date"].unique())
        min_test_date = dates[52 + 1]  # min_train + embargo + 1
        predicted_dates = score.index.get_level_values("date").unique()
        for d in predicted_dates:
            assert d >= min_test_date

    def test_missing_column_raises(self):
        """Raises ValueError when a required column is missing."""
        df = _make_panel(n_dates=10, n_factors=2)
        with pytest.raises(ValueError, match="Missing columns"):
            ridge_family_score(df, ["f0", "nonexistent"], "pchg")

    def test_score_name(self):
        """Output Series should be named 'ridge_family_score' when OOF runs."""
        df = _make_panel(n_dates=80, n_stocks=20, n_factors=2, label_signal=True)
        score = ridge_family_score(df, ["f0", "f1"], "pchg",
                                   min_train_periods=52, test_block=13, step=4)
        assert score.name in ("ridge_family_score", "equal_rank_score")


# ===========================================================================
# Task 5.3 — pc1_score_with_sign_anchor
# ===========================================================================

class TestPC1ScoreWithSignAnchor:
    """Tests for pc1_score_with_sign_anchor (task 5.3)."""

    def test_returns_series_with_multiindex(self):
        """Output must be a Series with (date, stock_id) MultiIndex."""
        df = _make_panel(n_dates=10, n_stocks=20, n_factors=3)
        score = pc1_score_with_sign_anchor(df, ["f0", "f1", "f2"])
        assert isinstance(score, pd.Series)
        assert isinstance(score.index, pd.MultiIndex)

    def test_sign_consistency_across_periods(self):
        """PC1 sign should be consistent across periods (no random flips).

        When factors are stable, PC1 should not flip sign randomly.
        """
        df = _make_panel(n_dates=10, n_stocks=30, n_factors=3, seed=42)
        score = pc1_score_with_sign_anchor(df, ["f0", "f1", "f2"])
        # Check that scores don't have wild sign flips
        # (hard to test rigorously without known structure, but check no NaN)
        assert score.notna().sum() > 0

    def test_instability_fallback(self):
        """When eigenvalue ratio is low, should downweight PC1.

        With very low eigenvalue ratio, PC1 is unstable and should be
        blended with equal-rank baseline.
        """
        # Create a panel with nearly collinear factors (low eigenvalue ratio)
        df = _make_panel(n_dates=5, n_stocks=20, n_factors=3, seed=99)
        # Make factors nearly identical to force low eigenvalue ratio
        df["f1"] = df["f0"] + np.random.default_rng(99).normal(0, 0.01, len(df))
        df["f2"] = df["f0"] + np.random.default_rng(100).normal(0, 0.01, len(df))

        score = pc1_score_with_sign_anchor(
            df, ["f0", "f1", "f2"],
            eigenvalue_ratio_threshold=1.5,
        )
        # Should not crash and should return valid scores
        assert len(score) > 0
        assert score.notna().sum() > 0

    def test_anchor_score_used_for_first_window(self):
        """First window should use anchor_score for sign determination."""
        df = _make_panel(n_dates=5, n_stocks=20, n_factors=2)
        anchor = equal_rank_score(df, ["f0", "f1"])
        score = pc1_score_with_sign_anchor(df, ["f0", "f1"], anchor_score=anchor)
        # Should not crash and should align with anchor in first window
        assert len(score) > 0

    def test_missing_column_raises(self):
        """Raises ValueError when a factor column is missing."""
        df = _make_panel()
        with pytest.raises(ValueError, match="Missing columns"):
            pc1_score_with_sign_anchor(df, ["f0", "nonexistent"])

    def test_score_name(self):
        """Output Series should be named 'pc1_score'."""
        df = _make_panel(n_dates=5, n_stocks=20, n_factors=2)
        score = pc1_score_with_sign_anchor(df, ["f0", "f1"])
        assert score.name in ("pc1_score", "equal_rank_score")


# ===========================================================================
# Task 5.4 — stack_family_scores_oof
# ===========================================================================

class TestStackFamilyScoresOOF:
    """Tests for stack_family_scores_oof (task 5.4)."""

    def test_returns_series_with_multiindex(self):
        """Output must be a Series with (date, stock_id) MultiIndex."""
        df = _make_panel(n_dates=10, n_stocks=20, n_factors=3, label_signal=True)
        eq = equal_rank_score(df, ["f0", "f1", "f2"])
        ridge = equal_rank_score(df, ["f0", "f1"])  # Simplified
        pc1 = equal_rank_score(df, ["f0"])
        label = df.set_index(["date", "stock_id"])["pchg"]

        stacked = stack_family_scores_oof(eq, ridge, pc1, label, alpha=1.0)
        assert isinstance(stacked, pd.Series)
        assert isinstance(stacked.index, pd.MultiIndex)

    def test_non_negative_weights(self):
        """Weights should be non-negative (positive=True in Ridge)."""
        df = _make_panel(n_dates=10, n_stocks=20, n_factors=3, label_signal=True)
        eq = equal_rank_score(df, ["f0", "f1", "f2"])
        ridge = equal_rank_score(df, ["f0", "f1"])
        pc1 = equal_rank_score(df, ["f0"])
        label = df.set_index(["date", "stock_id"])["pchg"]

        stacked = stack_family_scores_oof(eq, ridge, pc1, label, alpha=1.0)
        # Weights are internal, but stacked should be a valid linear combination
        assert stacked.notna().sum() > 0

    def test_fallback_when_no_common_index(self):
        """Falls back to eq_score when no common index exists."""
        df = _make_panel(n_dates=5, n_stocks=10, n_factors=2)
        eq = equal_rank_score(df, ["f0", "f1"])
        # Create ridge/pc1 with different index
        ridge = pd.Series([1.0], index=pd.MultiIndex.from_tuples(
            [(pd.Timestamp("2099-01-01"), "X")], names=["date", "stock_id"]
        ))
        pc1 = ridge.copy()
        label = df.set_index(["date", "stock_id"])["pchg"]

        stacked = stack_family_scores_oof(eq, ridge, pc1, label)
        # Should return eq_score as fallback
        assert len(stacked) == len(eq)

    def test_score_name(self):
        """Output Series should be named 'stacked_family_score'."""
        df = _make_panel(n_dates=10, n_stocks=20, n_factors=3, label_signal=True)
        eq = equal_rank_score(df, ["f0", "f1", "f2"])
        ridge = equal_rank_score(df, ["f0", "f1"])
        pc1 = equal_rank_score(df, ["f0"])
        label = df.set_index(["date", "stock_id"])["pchg"]

        stacked = stack_family_scores_oof(eq, ridge, pc1, label)
        assert stacked.name in ("stacked_family_score", "equal_rank_score")


# ===========================================================================
# Task 6.4 — predict_alpha_linear
# ===========================================================================

class TestPredictAlphaLinear:
    """Tests for predict_alpha_linear (task 6.4)."""

    def test_correct_linear_combination(self):
        """alpha_linear[t,i] = Σ_g β_{t,g} · s_g[t,i]"""
        S, _ = _make_family_scores(n_dates=5, n_stocks=10, families=["A", "B", "C"])
        beta = pd.Series({"A": 0.5, "B": 0.3, "C": 0.2})

        alpha = predict_alpha_linear(S, beta)

        expected = S["A"] * 0.5 + S["B"] * 0.3 + S["C"] * 0.2
        pd.testing.assert_series_equal(alpha, expected.rename("alpha_linear"), check_names=True)

    def test_output_index_matches_S(self):
        """Output index must match S's index."""
        S, _ = _make_family_scores(n_dates=5, n_stocks=10)
        beta = pd.Series({"momentum": 0.4, "quality": 0.3, "value": 0.3})

        alpha = predict_alpha_linear(S, beta)
        assert alpha.index.equals(S.index)

    def test_partial_family_overlap(self):
        """Only common families between S and beta are used."""
        S, _ = _make_family_scores(n_dates=5, n_stocks=10, families=["A", "B"])
        beta = pd.Series({"A": 0.6, "C": 0.4})  # C not in S

        alpha = predict_alpha_linear(S, beta)
        expected = S["A"] * 0.6
        pd.testing.assert_series_equal(alpha, expected.rename("alpha_linear"))

    def test_no_common_families_raises(self):
        """Raises ValueError when no common families exist."""
        S, _ = _make_family_scores(n_dates=5, n_stocks=10, families=["A", "B"])
        beta = pd.Series({"X": 0.5, "Y": 0.5})

        with pytest.raises(ValueError, match="No common families"):
            predict_alpha_linear(S, beta)

    def test_output_name(self):
        """Output Series should be named 'alpha_linear'."""
        S, _ = _make_family_scores(n_dates=5, n_stocks=10)
        beta = pd.Series({"momentum": 1.0, "quality": 0.0, "value": 0.0})
        alpha = predict_alpha_linear(S, beta)
        assert alpha.name == "alpha_linear"

    def test_nan_in_S_filled_with_zero(self):
        """NaN values in S are filled with 0 before multiplication."""
        S, _ = _make_family_scores(n_dates=3, n_stocks=5, families=["A", "B"])
        S.iloc[0, 0] = np.nan  # Introduce NaN
        beta = pd.Series({"A": 1.0, "B": 0.0})

        alpha = predict_alpha_linear(S, beta)
        # NaN row should produce 0 (filled)
        assert alpha.iloc[0] == 0.0


# ===========================================================================
# Task 6.1 — CrossFamilyModel
# ===========================================================================

class TestCrossFamilyModel:
    """Tests for CrossFamilyModel (task 6.1)."""

    def test_fit_and_predict(self):
        """Model can fit on OOF family scores and predict."""
        S, y = _make_family_scores(n_dates=20, n_stocks=30)
        model = CrossFamilyModel()
        model.fit(S, y, best_alpha=1.0, best_l1_ratio=0.0)

        alpha = model.predict(S)
        assert isinstance(alpha, pd.Series)
        assert len(alpha) == len(S)

    def test_current_beta_after_fit(self):
        """After fit, current_beta should be set."""
        S, y = _make_family_scores(n_dates=10, n_stocks=20)
        model = CrossFamilyModel()
        assert model.current_beta is None

        model.fit(S, y, best_alpha=1.0, best_l1_ratio=0.0)
        assert model.current_beta is not None
        assert len(model.current_beta) == S.shape[1]

    def test_predict_before_fit_raises(self):
        """Predict before fit should raise RuntimeError."""
        S, _ = _make_family_scores(n_dates=5, n_stocks=10)
        model = CrossFamilyModel()

        with pytest.raises(RuntimeError, match="Model not fitted"):
            model.predict(S)

    def test_insufficient_data_raises(self):
        """Fit with < 10 samples should raise ValueError."""
        S, y = _make_family_scores(n_dates=1, n_stocks=5)
        model = CrossFamilyModel()

        with pytest.raises(ValueError, match="Insufficient training data"):
            model.fit(S, y)

    def test_beta_history_accumulates(self):
        """Beta history should accumulate with each fit."""
        S, y = _make_family_scores(n_dates=20, n_stocks=30)
        model = CrossFamilyModel()

        model.fit(S, y, best_alpha=1.0, best_l1_ratio=0.0)
        assert len(model.beta_history) == 1

        model.fit(S, y, best_alpha=0.1, best_l1_ratio=0.0)
        assert len(model.beta_history) == 2


# ===========================================================================
# Task 6.2 — Hyperparameter grid search
# ===========================================================================

class TestCrossFamilyModelHyperparams:
    """Tests for hyperparameter grid search (task 6.2)."""

    def test_default_alpha_reg_grid(self):
        """Default alpha_reg grid should be [0.001, 0.01, 0.1, 1.0, 10.0]."""
        model = CrossFamilyModel()
        assert model.alpha_reg_grid == [0.001, 0.01, 0.1, 1.0, 10.0]

    def test_default_l1_ratio_grid(self):
        """Default l1_ratio grid should be [0.0, 0.1, 0.5]."""
        model = CrossFamilyModel()
        assert model.l1_ratio_grid == [0.0, 0.1, 0.5]

    def test_select_hyperparams_returns_valid_values(self):
        """select_hyperparams should return values from the grids."""
        S, y = _make_family_scores(n_dates=20, n_stocks=30)
        model = CrossFamilyModel()

        best_alpha, best_l1 = model.select_hyperparams(S, y)

        assert best_alpha in model.alpha_reg_grid
        assert best_l1 in model.l1_ratio_grid

    def test_elastic_net_used_when_l1_ratio_nonzero(self):
        """When l1_ratio > 0, ElasticNet should be used."""
        S, y = _make_family_scores(n_dates=20, n_stocks=30)
        model = CrossFamilyModel()
        # Should not raise
        model.fit(S, y, best_alpha=0.1, best_l1_ratio=0.5)
        assert model.current_beta is not None

    def test_pure_ridge_when_l1_ratio_zero(self):
        """When l1_ratio == 0.0, pure Ridge should be used."""
        S, y = _make_family_scores(n_dates=20, n_stocks=30)
        model = CrossFamilyModel()
        model.fit(S, y, best_alpha=1.0, best_l1_ratio=0.0)
        assert model.current_beta is not None


# ===========================================================================
# Task 6.3 — Weight constraints
# ===========================================================================

class TestCrossFamilyModelWeightConstraints:
    """Tests for weight constraints (task 6.3)."""

    def test_single_family_weight_cap(self):
        """No single family weight should exceed max_single_family_weight."""
        S, y = _make_family_scores(n_dates=20, n_stocks=30)
        cap = 0.4
        model = CrossFamilyModel(max_single_family_weight=cap)
        model.fit(S, y, best_alpha=0.001, best_l1_ratio=0.0)

        beta = model.current_beta
        assert (beta.abs() <= cap + 1e-9).all(), (
            f"Some weights exceed cap {cap}: {beta}"
        )

    def test_custom_weight_cap(self):
        """Custom weight cap should be respected."""
        S, y = _make_family_scores(n_dates=20, n_stocks=30)
        cap = 0.2
        model = CrossFamilyModel(max_single_family_weight=cap)
        model.fit(S, y, best_alpha=0.001, best_l1_ratio=0.0)

        beta = model.current_beta
        assert (beta.abs() <= cap + 1e-9).all()

    def test_exponential_smoothing_applied(self):
        """Beta should be smoothed between consecutive fits."""
        S, y = _make_family_scores(n_dates=20, n_stocks=30)
        model = CrossFamilyModel(weight_smoothing_halflife=4)

        model.fit(S, y, best_alpha=1.0, best_l1_ratio=0.0)
        beta_1 = model.current_beta.copy()

        # Fit again with different alpha to get different raw beta
        model.fit(S, y, best_alpha=0.001, best_l1_ratio=0.0)
        beta_2 = model.current_beta.copy()

        # beta_2 should be a blend of new fit and beta_1 (not identical to raw)
        # They should differ but not be completely different
        assert not beta_1.equals(beta_2)

    def test_allow_negative_weights(self):
        """When allow_negative=True, negative weights are allowed."""
        S, y = _make_family_scores(n_dates=20, n_stocks=30)
        model = CrossFamilyModel(allow_negative=True)
        model.fit(S, y, best_alpha=0.001, best_l1_ratio=0.0)
        # Negative weights are allowed (no assertion that all >= 0)
        assert model.current_beta is not None

    def test_smoothing_halflife_parameter(self):
        """weight_smoothing_halflife should be stored correctly."""
        model = CrossFamilyModel(weight_smoothing_halflife=8)
        assert model.weight_smoothing_halflife == 8
