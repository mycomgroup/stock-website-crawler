"""L3 Intra-family synthesis — tasks 5.1-5.4"""
from __future__ import annotations
import numpy as np
import pandas as pd
from sklearn.linear_model import Ridge


def equal_rank_score(
    df: pd.DataFrame,
    factor_cols: list[str],
) -> pd.Series:
    """Family-level rank equal-weight average (robust baseline).

    For each cross-section (date), rank each factor to [0,1] (pct rank),
    then average across factors. Returns score centered around 0 after
    subtracting 0.5.

    Parameters
    ----------
    df : pd.DataFrame
        Panel data with date, stock_id, and factor columns.
    factor_cols : list[str]
        Factor columns to include in the equal-weight average.

    Returns
    -------
    pd.Series
        Equal-weight rank score, indexed by (date, stock_id).
    """
    if not factor_cols:
        raise ValueError("factor_cols cannot be empty")

    missing = [c for c in ["date", "stock_id"] + factor_cols if c not in df.columns]
    if missing:
        raise ValueError(f"Missing columns: {missing}")

    result = df.copy()

    # Per-date rank normalization: rank to [0,1] then center at 0
    for col in factor_cols:
        result[col] = result.groupby("date")[col].transform(
            lambda s: s.rank(pct=True, na_option="keep") - 0.5
        )

    # Equal-weight average across factors
    score = result[factor_cols].mean(axis=1)
    score.index = pd.MultiIndex.from_frame(df[["date", "stock_id"]])
    score.name = "equal_rank_score"
    return score


def ridge_family_score(
    df: pd.DataFrame,
    factor_cols: list[str],
    label_col: str,
    min_train_periods: int = 52,
    test_block: int = 13,
    step: int = 4,
    embargo: int = 1,
    alpha: float = 1.0,
) -> pd.Series:
    """Rolling ridge OOF prediction for family score.

    Uses walk-forward splits to generate OOF predictions.
    For each outer fold: fit ridge regression on train, predict on test.

    Parameters
    ----------
    df : pd.DataFrame
        Panel data with date, stock_id, factor columns, and label column.
    factor_cols : list[str]
        Factor columns to use as features.
    label_col : str
        Label column (e.g., 'pchg').
    min_train_periods : int
        Minimum training periods (default 52 weeks).
    test_block : int
        Test block size (default 13 weeks).
    step : int
        Step size between splits (default 4 weeks).
    embargo : int
        Embargo periods (default 1 week).
    alpha : float
        Ridge regularization strength (default 1.0).

    Returns
    -------
    pd.Series
        OOF ridge predictions, indexed by (date, stock_id).
    """
    missing = [c for c in ["date", "stock_id", label_col] + factor_cols if c not in df.columns]
    if missing:
        raise ValueError(f"Missing columns: {missing}")

    dates = sorted(df["date"].unique())
    n_dates = len(dates)

    if n_dates < min_train_periods + embargo + 1:
        # Not enough data, return equal rank score as fallback
        return equal_rank_score(df, factor_cols)

    all_preds: dict = {}

    # Walk-forward splits
    train_end = min_train_periods - 1
    while True:
        embargo_end = train_end + embargo
        test_start = embargo_end + 1
        test_end = test_start + test_block - 1

        if test_end >= n_dates:
            break

        train_dates = dates[: train_end + 1]
        test_dates = dates[test_start : test_end + 1]

        train_df = df[df["date"].isin(train_dates)]
        test_df = df[df["date"].isin(test_dates)]

        # Prepare features and labels
        X_train = train_df[factor_cols].fillna(0).values
        y_train = train_df[label_col].fillna(0).values
        X_test = test_df[factor_cols].fillna(0).values

        if len(X_train) < 10:
            train_end += step
            continue

        try:
            model = Ridge(alpha=alpha, fit_intercept=True)
            model.fit(X_train, y_train)
            preds = model.predict(X_test)

            for i, (_, row) in enumerate(test_df.iterrows()):
                key = (row["date"], row["stock_id"])
                if key not in all_preds:
                    all_preds[key] = preds[i]
        except Exception:
            pass

        train_end += step

    if not all_preds:
        return equal_rank_score(df, factor_cols)

    index = pd.MultiIndex.from_tuples(list(all_preds.keys()), names=["date", "stock_id"])
    return pd.Series(list(all_preds.values()), index=index, name="ridge_family_score")


def pc1_score_with_sign_anchor(
    df: pd.DataFrame,
    factor_cols: list[str],
    anchor_score: pd.Series | None = None,
    eigenvalue_ratio_threshold: float = 1.5,
    cross_period_corr_threshold: float = 0.7,
    min_periods: int = 5,
) -> pd.Series:
    """PC1 score with sign anchoring and instability handling.

    Computes PC1 of factor cross-section per date.
    Sign anchor: if corr(PC1_t, PC1_{t-1}) < 0, flip sign.
    First window uses anchor_score (equal-rank baseline) as direction anchor.
    Instability: if eigenvalue ratio < 1.5 or cross-period corr < 0.7, downweight.

    Parameters
    ----------
    df : pd.DataFrame
        Panel data with date, stock_id, and factor columns.
    factor_cols : list[str]
        Factor columns to use for PCA.
    anchor_score : pd.Series | None
        Anchor score for sign determination (first window).
        If None, uses equal_rank_score.
    eigenvalue_ratio_threshold : float
        Minimum ratio of first to second eigenvalue for stability (default 1.5).
    cross_period_corr_threshold : float
        Minimum cross-period correlation for stability (default 0.7).
    min_periods : int
        Minimum stocks per cross-section (default 5).

    Returns
    -------
    pd.Series
        PC1 score, indexed by (date, stock_id).
    """
    missing = [c for c in ["date", "stock_id"] + factor_cols if c not in df.columns]
    if missing:
        raise ValueError(f"Missing columns: {missing}")

    if anchor_score is None:
        anchor_score = equal_rank_score(df, factor_cols)

    dates = sorted(df["date"].unique())
    all_scores: dict = {}
    prev_pc1_scores: dict | None = None

    for date in dates:
        cross_section = df[df["date"] == date][["stock_id"] + factor_cols].copy()
        cross_section = cross_section.dropna(subset=factor_cols)

        if len(cross_section) < min_periods:
            continue

        X = cross_section[factor_cols].values

        # Standardize per cross-section
        X_centered = X - X.mean(axis=0)
        X_std = X_centered.std(axis=0)
        X_std[X_std < 1e-8] = 1.0
        X_norm = X_centered / X_std

        # PCA via SVD
        try:
            U, S_vals, Vt = np.linalg.svd(X_norm, full_matrices=False)
            eigenvalues = S_vals ** 2 / max(len(cross_section) - 1, 1)
            pc1_scores = U[:, 0] * S_vals[0]
        except np.linalg.LinAlgError:
            continue

        # Check eigenvalue ratio stability
        is_stable = True
        if len(eigenvalues) >= 2 and eigenvalues[1] > 1e-8:
            ratio = eigenvalues[0] / eigenvalues[1]
            if ratio < eigenvalue_ratio_threshold:
                is_stable = False

        # Sign anchoring
        stocks = cross_section["stock_id"].tolist()

        if prev_pc1_scores is not None:
            # Align stocks between periods
            prev_stocks = set(prev_pc1_scores.keys())
            curr_stocks = set(stocks)
            common_stocks = list(prev_stocks & curr_stocks)

            if len(common_stocks) >= 5:
                prev_vals = np.array([prev_pc1_scores[s] for s in common_stocks])
                curr_vals = np.array([
                    pc1_scores[stocks.index(s)] for s in common_stocks
                ])

                cross_corr = np.corrcoef(prev_vals, curr_vals)[0, 1]

                if np.isfinite(cross_corr) and cross_corr < cross_period_corr_threshold:
                    is_stable = False

                if np.isfinite(cross_corr) and cross_corr < 0:
                    pc1_scores = -pc1_scores
        else:
            # First window: use anchor_score for sign
            anchor_vals = []
            pc1_vals = []
            for i, stock in enumerate(stocks):
                key = (date, stock)
                if key in anchor_score.index:
                    anchor_vals.append(anchor_score[key])
                    pc1_vals.append(pc1_scores[i])

            if len(anchor_vals) >= 5:
                anchor_corr = np.corrcoef(anchor_vals, pc1_vals)[0, 1]
                if np.isfinite(anchor_corr) and anchor_corr < 0:
                    pc1_scores = -pc1_scores

        # Store current scores for next iteration
        prev_pc1_scores = {s: pc1_scores[i] for i, s in enumerate(stocks)}

        # If unstable, downweight (blend with equal-rank anchor)
        weight = 1.0 if is_stable else 0.3

        for i, stock in enumerate(stocks):
            key = (date, stock)
            eq_val = 0.0
            if hasattr(anchor_score, "get"):
                eq_val = anchor_score.get(key, 0.0)
            elif key in anchor_score.index:
                eq_val = float(anchor_score[key])
            all_scores[key] = weight * pc1_scores[i] + (1 - weight) * eq_val

    if not all_scores:
        return equal_rank_score(df, factor_cols)

    index = pd.MultiIndex.from_tuples(list(all_scores.keys()), names=["date", "stock_id"])
    return pd.Series(list(all_scores.values()), index=index, name="pc1_score")


def stack_family_scores_oof(
    eq_score: pd.Series,
    ridge_score: pd.Series,
    pc1_score: pd.Series,
    label: pd.Series,
    alpha: float = 1.0,
) -> pd.Series:
    """Non-negative ridge stacking of three sub-scores (OOF).

    Stacks equal-rank, ridge, and PC1 sub-scores using non-negative ridge.
    Weights determined by OOF, not in-sample.

    Parameters
    ----------
    eq_score, ridge_score, pc1_score : pd.Series
        Sub-scores indexed by (date, stock_id).
    label : pd.Series
        Target labels indexed by (date, stock_id).
    alpha : float
        Ridge regularization strength (default 1.0).

    Returns
    -------
    pd.Series
        Stacked family score, indexed by (date, stock_id).
    """
    # Align all scores on common index
    common_idx = (
        eq_score.index
        .intersection(ridge_score.index)
        .intersection(pc1_score.index)
        .intersection(label.index)
    )

    if len(common_idx) == 0:
        return eq_score  # Fallback to equal-rank

    X = np.column_stack([
        eq_score.loc[common_idx].values,
        ridge_score.loc[common_idx].values,
        pc1_score.loc[common_idx].values,
    ])
    y = label.loc[common_idx].values

    # Handle NaN
    valid_mask = np.isfinite(X).all(axis=1) & np.isfinite(y)
    if valid_mask.sum() < 10:
        return eq_score

    X_valid = X[valid_mask]
    y_valid = y[valid_mask]

    # Non-negative ridge: sklearn Ridge with positive=True
    try:
        model = Ridge(alpha=alpha, fit_intercept=False, positive=True)
        model.fit(X_valid, y_valid)
        weights = model.coef_
    except Exception:
        # Fallback: equal weights
        weights = np.array([1 / 3, 1 / 3, 1 / 3])

    # Ensure non-negative and normalize
    weights = np.maximum(weights, 0)
    if weights.sum() > 1e-8:
        weights = weights / weights.sum()
    else:
        weights = np.array([1 / 3, 1 / 3, 1 / 3])

    # Apply weights to all common index
    stacked = (
        weights[0] * eq_score.loc[common_idx].fillna(0)
        + weights[1] * ridge_score.loc[common_idx].fillna(0)
        + weights[2] * pc1_score.loc[common_idx].fillna(0)
    )
    stacked.name = "stacked_family_score"
    return stacked
