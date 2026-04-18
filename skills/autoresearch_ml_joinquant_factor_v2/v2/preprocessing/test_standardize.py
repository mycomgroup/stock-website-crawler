"""
Tests for standardize_factors() — task 2.3

Covers:
  - Rank values are in range [-0.5, +0.5]
  - Rank of N values: min ≈ -0.5*(N-1)/N, max ≈ +0.5*(N-1)/N
  - Zscore of median value = 0
  - Per-date operation (different dates have different statistics)
  - NaN handling
  - Idempotency of rank standardization (P2)
  - Empty factor_cols returns copies

**Validates: Requirements 2.3**
"""

from __future__ import annotations

import numpy as np
import pandas as pd
import pytest
from hypothesis import given, settings
from hypothesis import strategies as st
from hypothesis.extra.pandas import column, data_frames

from skills.autoresearch_ml_joinquant_factor_v2.v2.preprocessing.factor_preprocessor import (
    standardize_factors,
)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def make_df(
    dates: list[str],
    n_stocks_per_date: int,
    factor_values: dict[str, list[float]] | None = None,
    seed: int = 42,
) -> pd.DataFrame:
    """Build a simple panel DataFrame for testing."""
    rng = np.random.default_rng(seed)
    rows = []
    for date in dates:
        for i in range(n_stocks_per_date):
            row = {"date": date, "stock_id": f"S{i:03d}"}
            if factor_values:
                for col, vals in factor_values.items():
                    row[col] = vals[len(rows) % len(vals)]
            else:
                row["f1"] = rng.standard_normal()
            rows.append(row)
    return pd.DataFrame(rows)


# ---------------------------------------------------------------------------
# Unit tests
# ---------------------------------------------------------------------------

class TestRankBounds:
    """Rank values must lie in (-0.5, +0.5)."""

    def test_rank_values_in_range(self):
        df = make_df(["2020-01-01"], n_stocks_per_date=10)
        df_rank, _ = standardize_factors(df, ["f1"])
        vals = df_rank["f1"].dropna()
        assert (vals >= -0.5).all(), "Rank values must be >= -0.5"
        assert (vals <= 0.5).all(), "Rank values must be <= +0.5"

    def test_rank_min_max_formula(self):
        """For N distinct values, min = 1/(N+1) - 0.5, max = N/(N+1) - 0.5."""
        n = 10
        df = pd.DataFrame({
            "date": ["2020-01-01"] * n,
            "stock_id": [f"S{i}" for i in range(n)],
            "f1": list(range(n)),  # distinct values
        })
        df_rank, _ = standardize_factors(df, ["f1"])
        vals = df_rank["f1"].sort_values().values

        # rank(x)/(N+1) - 0.5: min rank=1, max rank=N
        expected_min = 1 / (n + 1) - 0.5
        expected_max = n / (n + 1) - 0.5

        assert abs(vals[0] - expected_min) < 1e-10, (
            f"Expected min {expected_min}, got {vals[0]}"
        )
        assert abs(vals[-1] - expected_max) < 1e-10, (
            f"Expected max {expected_max}, got {vals[-1]}"
        )

    def test_rank_formula_various_n(self):
        """Check min/max formula for several cross-section sizes."""
        for n in [5, 20, 100]:
            df = pd.DataFrame({
                "date": ["2020-01-01"] * n,
                "stock_id": [f"S{i}" for i in range(n)],
                "f1": list(range(n)),
            })
            df_rank, _ = standardize_factors(df, ["f1"])
            vals = df_rank["f1"].sort_values().values

            expected_min = 1 / (n + 1) - 0.5
            expected_max = n / (n + 1) - 0.5
            assert abs(vals[0] - expected_min) < 1e-10
            assert abs(vals[-1] - expected_max) < 1e-10


class TestZscoreMedianZero:
    """Zscore of the median value should be 0."""

    def test_zscore_median_is_zero(self):
        """The median stock's zscore should be 0."""
        n = 11  # odd number so median is exact
        values = list(range(n))
        df = pd.DataFrame({
            "date": ["2020-01-01"] * n,
            "stock_id": [f"S{i}" for i in range(n)],
            "f1": values,
        })
        _, df_zscore = standardize_factors(df, ["f1"])
        # median value is 5 (index 5)
        median_stock_zscore = df_zscore.loc[df_zscore["f1"] == 0.0, "f1"]
        # After zscore, the median input maps to zscore=0
        # Find the row with original value == median(values) = 5
        original_median = np.median(values)
        # The zscore of the median value is 0
        # We need to check the zscore output for the stock that had the median value
        # Re-check: zscore = (x - median) / (MAD + eps), so x=median → zscore=0
        # The stock with f1=5 (original median) should have zscore≈0
        # But df_zscore["f1"] is already the zscore, not the original value
        # We need to find which stock had original value = median
        original_median_idx = df[df["f1"] == original_median].index
        zscore_at_median = df_zscore.loc[original_median_idx, "f1"].values
        assert abs(zscore_at_median[0]) < 1e-10, (
            f"Zscore of median value should be 0, got {zscore_at_median[0]}"
        )

    def test_zscore_median_zero_even_n(self):
        """Even N: the two middle values average to median, their zscores are symmetric."""
        n = 10
        values = list(range(n))  # 0..9, median = 4.5
        df = pd.DataFrame({
            "date": ["2020-01-01"] * n,
            "stock_id": [f"S{i}" for i in range(n)],
            "f1": values,
        })
        _, df_zscore = standardize_factors(df, ["f1"])
        # Values 4 and 5 are equidistant from median 4.5
        z4 = df_zscore.loc[df["f1"] == 4, "f1"].values[0]
        z5 = df_zscore.loc[df["f1"] == 5, "f1"].values[0]
        assert abs(z4 + z5) < 1e-10, "Symmetric values around median should have opposite zscores"


class TestPerDateOperation:
    """Different dates must have independent statistics."""

    def test_different_dates_independent(self):
        """Two dates with different scales should produce same rank structure."""
        df = pd.DataFrame({
            "date": ["2020-01-01"] * 5 + ["2020-01-08"] * 5,
            "stock_id": [f"S{i}" for i in range(5)] * 2,
            "f1": [1.0, 2.0, 3.0, 4.0, 5.0,   # date 1: small values
                   100.0, 200.0, 300.0, 400.0, 500.0],  # date 2: large values
        })
        df_rank, df_zscore = standardize_factors(df, ["f1"])

        # Both dates should have the same rank structure (same relative ordering)
        rank_d1 = df_rank[df_rank["date"] == "2020-01-01"]["f1"].sort_values().values
        rank_d2 = df_rank[df_rank["date"] == "2020-01-08"]["f1"].sort_values().values
        np.testing.assert_allclose(rank_d1, rank_d2, atol=1e-10)

        # Zscore: both dates should have median=0 and same structure
        zscore_d1 = df_zscore[df_zscore["date"] == "2020-01-01"]["f1"].sort_values().values
        zscore_d2 = df_zscore[df_zscore["date"] == "2020-01-08"]["f1"].sort_values().values
        np.testing.assert_allclose(zscore_d1, zscore_d2, atol=1e-10)

    def test_per_date_statistics_differ(self):
        """Dates with different distributions should produce different zscore scales."""
        df = pd.DataFrame({
            "date": ["2020-01-01"] * 5 + ["2020-01-08"] * 5,
            "stock_id": [f"S{i}" for i in range(5)] * 2,
            "f1": [1.0, 2.0, 3.0, 4.0, 5.0,    # MAD = 1.0
                   10.0, 20.0, 30.0, 40.0, 50.0],  # MAD = 10.0
        })
        _, df_zscore = standardize_factors(df, ["f1"])

        # Both dates should have the same zscore values (same relative structure)
        # because the values are proportional
        zscore_d1 = df_zscore[df_zscore["date"] == "2020-01-01"]["f1"].sort_values().values
        zscore_d2 = df_zscore[df_zscore["date"] == "2020-01-08"]["f1"].sort_values().values
        np.testing.assert_allclose(zscore_d1, zscore_d2, atol=1e-10)


class TestNaNHandling:
    """NaN values must remain NaN after standardization."""

    def test_nan_stays_nan_rank(self):
        df = pd.DataFrame({
            "date": ["2020-01-01"] * 5,
            "stock_id": list("ABCDE"),
            "f1": [1.0, np.nan, 3.0, np.nan, 5.0],
        })
        df_rank, _ = standardize_factors(df, ["f1"])
        assert df_rank.loc[df["f1"].isna(), "f1"].isna().all()

    def test_nan_stays_nan_zscore(self):
        df = pd.DataFrame({
            "date": ["2020-01-01"] * 5,
            "stock_id": list("ABCDE"),
            "f1": [1.0, np.nan, 3.0, np.nan, 5.0],
        })
        _, df_zscore = standardize_factors(df, ["f1"])
        assert df_zscore.loc[df["f1"].isna(), "f1"].isna().all()

    def test_non_nan_values_computed_correctly_with_nans(self):
        """Non-NaN values should be computed using only non-NaN cross-section members."""
        df = pd.DataFrame({
            "date": ["2020-01-01"] * 5,
            "stock_id": list("ABCDE"),
            "f1": [1.0, np.nan, 3.0, np.nan, 5.0],
        })
        df_rank, _ = standardize_factors(df, ["f1"])
        # N = 3 (non-NaN values: 1, 3, 5)
        # ranks: 1→1, 3→2, 5→3
        # rank repr: 1/(3+1)-0.5=-0.25, 2/4-0.5=0.0, 3/4-0.5=0.25
        valid_ranks = df_rank.loc[df["f1"].notna(), "f1"].sort_values().values
        expected = np.array([-0.25, 0.0, 0.25])
        np.testing.assert_allclose(valid_ranks, expected, atol=1e-10)

    def test_all_nan_cross_section(self):
        """All-NaN cross-section should return all NaN."""
        df = pd.DataFrame({
            "date": ["2020-01-01"] * 3,
            "stock_id": list("ABC"),
            "f1": [np.nan, np.nan, np.nan],
        })
        df_rank, df_zscore = standardize_factors(df, ["f1"])
        assert df_rank["f1"].isna().all()
        assert df_zscore["f1"].isna().all()


class TestEmptyFactorCols:
    """Empty factor_cols should return copies of the input."""

    def test_empty_factor_cols_returns_copies(self):
        df = pd.DataFrame({
            "date": ["2020-01-01"] * 3,
            "stock_id": list("ABC"),
            "f1": [1.0, 2.0, 3.0],
        })
        df_rank, df_zscore = standardize_factors(df, [])
        pd.testing.assert_frame_equal(df_rank, df)
        pd.testing.assert_frame_equal(df_zscore, df)

    def test_empty_factor_cols_are_independent_copies(self):
        """Modifying the output should not affect the input."""
        df = pd.DataFrame({
            "date": ["2020-01-01"] * 3,
            "stock_id": list("ABC"),
            "f1": [1.0, 2.0, 3.0],
        })
        df_rank, df_zscore = standardize_factors(df, [])
        df_rank["f1"] = 999.0
        assert df["f1"].iloc[0] == 1.0, "Input should not be modified"


class TestNonFactorColumnsPreserved:
    """Non-factor columns must be copied unchanged to both outputs."""

    def test_non_factor_cols_unchanged(self):
        df = pd.DataFrame({
            "date": ["2020-01-01"] * 3,
            "stock_id": list("ABC"),
            "industry": ["tech", "fin", "tech"],
            "f1": [1.0, 2.0, 3.0],
        })
        df_rank, df_zscore = standardize_factors(df, ["f1"])
        pd.testing.assert_series_equal(df_rank["date"], df["date"])
        pd.testing.assert_series_equal(df_rank["stock_id"], df["stock_id"])
        pd.testing.assert_series_equal(df_rank["industry"], df["industry"])
        pd.testing.assert_series_equal(df_zscore["date"], df["date"])
        pd.testing.assert_series_equal(df_zscore["stock_id"], df["stock_id"])
        pd.testing.assert_series_equal(df_zscore["industry"], df["industry"])


class TestTiesHandling:
    """Tied values should use average rank."""

    def test_ties_use_average_rank(self):
        """Two equal values should both get the average of their ranks."""
        df = pd.DataFrame({
            "date": ["2020-01-01"] * 4,
            "stock_id": list("ABCD"),
            "f1": [1.0, 2.0, 2.0, 3.0],  # two tied at 2.0
        })
        df_rank, _ = standardize_factors(df, ["f1"])
        # N=4, ranks: 1→1, 2→2.5, 2→2.5, 3→4
        # rank repr: 1/5-0.5=-0.3, 2.5/5-0.5=0.0, 2.5/5-0.5=0.0, 4/5-0.5=0.3
        tied_vals = df_rank.loc[df["f1"] == 2.0, "f1"].values
        assert abs(tied_vals[0] - tied_vals[1]) < 1e-10, "Tied values should have equal rank"
        assert abs(tied_vals[0] - 0.0) < 1e-10, "Average rank of tied values at positions 2,3 of 4 should be 0.0"


# ---------------------------------------------------------------------------
# Property-Based Tests (P2: Idempotency of rank standardization)
# ---------------------------------------------------------------------------

@given(
    values=st.lists(
        st.floats(min_value=-1e6, max_value=1e6, allow_nan=False, allow_infinity=False),
        min_size=3,
        max_size=50,
    )
)
@settings(max_examples=200)
def test_rank_idempotency_property(values):
    """
    **Validates: Requirements 2.3 — P2 Idempotency**

    Applying rank standardization twice should give the same result as applying it once
    (within numerical precision). This holds because rank is a monotone transformation,
    and rank of already-ranked values is itself a linear transformation.
    """
    n = len(values)
    df = pd.DataFrame({
        "date": ["2020-01-01"] * n,
        "stock_id": [f"S{i}" for i in range(n)],
        "f1": values,
    })

    # First application
    df_rank1, _ = standardize_factors(df, ["f1"])

    # Second application (on the rank output)
    df_rank2, _ = standardize_factors(df_rank1, ["f1"])

    # Results should be equal within numerical precision
    np.testing.assert_allclose(
        df_rank1["f1"].values,
        df_rank2["f1"].values,
        atol=1e-10,
        err_msg="Rank standardization should be idempotent",
    )


@given(
    values=st.lists(
        st.floats(min_value=-1e6, max_value=1e6, allow_nan=False, allow_infinity=False),
        min_size=3,
        max_size=50,
    )
)
@settings(max_examples=200)
def test_rank_bounds_property(values):
    """
    **Validates: Requirements 2.3 — Rank values in (-0.5, +0.5)**

    For any cross-section of N non-NaN values, all rank values must lie in [-0.5, +0.5].
    """
    n = len(values)
    df = pd.DataFrame({
        "date": ["2020-01-01"] * n,
        "stock_id": [f"S{i}" for i in range(n)],
        "f1": values,
    })

    df_rank, _ = standardize_factors(df, ["f1"])
    valid = df_rank["f1"].dropna()

    assert (valid >= -0.5).all(), f"Rank values below -0.5 found: {valid[valid < -0.5].values}"
    assert (valid <= 0.5).all(), f"Rank values above +0.5 found: {valid[valid > 0.5].values}"


@given(
    values=st.lists(
        st.floats(min_value=-1e6, max_value=1e6, allow_nan=False, allow_infinity=False),
        min_size=3,
        max_size=50,
    )
)
@settings(max_examples=200)
def test_zscore_median_zero_property(values):
    """
    **Validates: Requirements 2.3 — Zscore of median value = 0**

    For any cross-section, the stock with the median value should have zscore = 0.
    """
    n = len(values)
    df = pd.DataFrame({
        "date": ["2020-01-01"] * n,
        "stock_id": [f"S{i}" for i in range(n)],
        "f1": values,
    })

    _, df_zscore = standardize_factors(df, ["f1"])

    # Find the index of the median value in the original data
    median_val = np.median(values)
    # Find a stock whose original value equals the median
    median_indices = df.index[df["f1"] == median_val].tolist()

    if median_indices:
        zscore_at_median = df_zscore.loc[median_indices[0], "f1"]
        assert abs(zscore_at_median) < 1e-8, (
            f"Zscore of median value should be 0, got {zscore_at_median}"
        )


@given(
    values1=st.lists(
        st.floats(min_value=-100.0, max_value=100.0, allow_nan=False, allow_infinity=False),
        min_size=3,
        max_size=30,
    ).filter(lambda v: len(set(v)) > 1),  # require at least 2 distinct values
    scale=st.floats(min_value=2.0, max_value=100.0, allow_nan=False, allow_infinity=False),
    shift=st.floats(min_value=1000.0, max_value=2000.0, allow_nan=False, allow_infinity=False),
)
@settings(max_examples=100)
def test_per_date_independence_property(values1, scale, shift):
    """
    **Validates: Requirements 2.3 — Per-date cross-section operation**

    Two dates where one is a linear transformation of the other (same relative ordering
    and same tie structure) should produce identical rank representations, since rank
    is invariant to monotone transforms that preserve the tie structure.
    """
    n = len(values1)
    # values2 is a scaled+shifted version of values1 → same relative ordering
    values2 = [v * scale + shift for v in values1]

    # Verify that the tie structure is preserved after transformation
    # Two values are tied in v1 iff they are tied in v2
    def tie_structure(vals):
        """Return a frozenset of frozensets of indices with equal values."""
        from collections import defaultdict
        groups = defaultdict(list)
        for i, v in enumerate(vals):
            groups[v].append(i)
        return frozenset(frozenset(g) for g in groups.values())

    if tie_structure(values1) != tie_structure(values2):
        # Tie structure changed due to floating point — skip this example
        return

    df = pd.DataFrame({
        "date": ["2020-01-01"] * n + ["2020-01-08"] * n,
        "stock_id": [f"S{i}" for i in range(n)] * 2,
        "f1": values1 + values2,
    })

    df_rank, _ = standardize_factors(df, ["f1"])

    rank_d1 = df_rank[df_rank["date"] == "2020-01-01"]["f1"].values
    rank_d2 = df_rank[df_rank["date"] == "2020-01-08"]["f1"].values

    np.testing.assert_allclose(
        rank_d1, rank_d2, atol=1e-10,
        err_msg="Dates with same relative ordering should have identical rank representations",
    )
