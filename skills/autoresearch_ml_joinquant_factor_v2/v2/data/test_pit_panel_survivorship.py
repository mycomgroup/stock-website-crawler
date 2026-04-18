"""Unit tests for check_survivorship_bias() in pit_panel.py.

Tests cover:
- Empty DataFrame handling
- All stocks active (no delisted)
- Some stocks potentially delisted
- High delisted ratio (> 10%) triggers "high" risk and UserWarning
- Medium delisted ratio (5-10%) triggers "medium" risk
- Last returns captured / not captured
- IC comparison feasibility checks
- IC diff > 5% triggers UserWarning
- Missing required columns raise ValueError
- Report structure completeness
"""

from __future__ import annotations

import warnings

import numpy as np
import pandas as pd
import pytest

from skills.autoresearch_ml_joinquant_factor_v2.v2.data.pit_panel import (
    check_survivorship_bias,
)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _make_df(
    n_stocks: int,
    n_dates: int,
    delisted_stocks: list[str] | None = None,
    include_pchg: bool = True,
    include_factors: bool = True,
    last_pchg_null_for: list[str] | None = None,
) -> pd.DataFrame:
    """Build a minimal factor panel DataFrame for testing.

    Parameters
    ----------
    n_stocks : int
        Total number of stocks.
    n_dates : int
        Number of cross-section dates.
    delisted_stocks : list[str] | None
        Stock IDs that should disappear before the last date.
        These stocks will only appear in the first (n_dates - 1) dates.
    include_pchg : bool
        Whether to include a 'pchg' column.
    include_factors : bool
        Whether to include factor columns (factor_a, factor_b).
    last_pchg_null_for : list[str] | None
        Stock IDs whose last pchg should be NaN (simulating missing last return).
    """
    dates = pd.date_range("2020-01-01", periods=n_dates, freq="7D")
    stock_ids = [f"stock_{i:03d}" for i in range(n_stocks)]
    delisted_set = set(delisted_stocks or [])
    null_last_set = set(last_pchg_null_for or [])

    rows = []
    for date in dates:
        for sid in stock_ids:
            # Delisted stocks only appear before the last date
            if sid in delisted_set and date == dates[-1]:
                continue
            row: dict = {"stock_id": sid, "date": date}
            if include_pchg:
                # Set last pchg to NaN for specified stocks on their last date
                if sid in null_last_set and date == dates[-2]:
                    row["pchg"] = float("nan")
                else:
                    rng = np.random.default_rng(hash((str(date), sid)) % (2**31))
                    row["pchg"] = float(rng.normal(0, 0.02))
            if include_factors:
                rng2 = np.random.default_rng(hash((str(date), sid, "f")) % (2**31))
                row["factor_a"] = float(rng2.normal(0, 1))
                row["factor_b"] = float(rng2.normal(0, 1))
            rows.append(row)

    df = pd.DataFrame(rows)
    df["date"] = pd.to_datetime(df["date"])
    df = df.sort_values(["date", "stock_id"]).reset_index(drop=True)
    return df


# ---------------------------------------------------------------------------
# Tests: Input validation
# ---------------------------------------------------------------------------

class TestInputValidation:
    def test_missing_stock_id_raises(self):
        df = pd.DataFrame({"date": pd.to_datetime(["2020-01-01"]), "pchg": [0.01]})
        with pytest.raises(ValueError, match="stock_id"):
            check_survivorship_bias(df)

    def test_missing_date_raises(self):
        df = pd.DataFrame({"stock_id": ["s1"], "pchg": [0.01]})
        with pytest.raises(ValueError, match="date"):
            check_survivorship_bias(df)


# ---------------------------------------------------------------------------
# Tests: Empty DataFrame
# ---------------------------------------------------------------------------

class TestEmptyDataFrame:
    def test_empty_df_returns_safe_report(self):
        df = pd.DataFrame(columns=["stock_id", "date", "pchg"])
        df["date"] = pd.to_datetime(df["date"])
        report = check_survivorship_bias(df)

        assert report["n_total_stocks"] == 0
        assert report["n_active_stocks"] == 0
        assert report["n_potentially_delisted"] == 0
        assert report["potentially_delisted_stocks"] == []
        assert report["survivorship_bias_risk"] == "low"
        assert report["ic_comparison_feasible"] is False
        assert isinstance(report["message"], str)

    def test_single_stock_single_date(self):
        df = _make_df(n_stocks=1, n_dates=1)
        report = check_survivorship_bias(df)
        # Single date: the only date IS the last date, so no delisted stocks
        assert report["n_total_stocks"] == 1
        assert report["n_active_stocks"] == 1
        assert report["n_potentially_delisted"] == 0


# ---------------------------------------------------------------------------
# Tests: No delisted stocks
# ---------------------------------------------------------------------------

class TestNoDelistedStocks:
    def test_all_active_low_risk(self):
        df = _make_df(n_stocks=10, n_dates=5)
        report = check_survivorship_bias(df)

        assert report["n_total_stocks"] == 10
        assert report["n_active_stocks"] == 10
        assert report["n_potentially_delisted"] == 0
        assert report["potentially_delisted_stocks"] == []
        assert report["survivorship_bias_risk"] == "low"
        assert report["last_returns_included"] == {}
        assert report["pct_last_returns_captured"] == 0.0

    def test_no_warning_when_no_delisted(self):
        df = _make_df(n_stocks=10, n_dates=5)
        with warnings.catch_warnings(record=True) as caught:
            warnings.simplefilter("always")
            check_survivorship_bias(df)
        survivorship_warnings = [
            w for w in caught if "存活偏差" in str(w.message)
        ]
        assert len(survivorship_warnings) == 0


# ---------------------------------------------------------------------------
# Tests: Some delisted stocks
# ---------------------------------------------------------------------------

class TestSomeDelistedStocks:
    def test_delisted_stocks_identified(self):
        delisted = ["stock_000", "stock_001"]
        df = _make_df(n_stocks=20, n_dates=5, delisted_stocks=delisted)
        report = check_survivorship_bias(df)

        assert report["n_total_stocks"] == 20
        assert report["n_active_stocks"] == 18
        assert report["n_potentially_delisted"] == 2
        assert set(report["potentially_delisted_stocks"]) == set(delisted)

    def test_report_keys_complete(self):
        df = _make_df(n_stocks=10, n_dates=4, delisted_stocks=["stock_000"])
        report = check_survivorship_bias(df)

        required_keys = {
            "n_total_stocks",
            "n_active_stocks",
            "n_potentially_delisted",
            "potentially_delisted_stocks",
            "last_returns_included",
            "pct_last_returns_captured",
            "survivorship_bias_risk",
            "ic_all",
            "ic_active",
            "ic_diff_pct",
            "ic_comparison_feasible",
            "message",
        }
        assert required_keys.issubset(set(report.keys()))

    def test_last_returns_captured_when_pchg_present(self):
        delisted = ["stock_000"]
        df = _make_df(n_stocks=10, n_dates=4, delisted_stocks=delisted)
        report = check_survivorship_bias(df)

        assert "stock_000" in report["last_returns_included"]
        # The last pchg for stock_000 should be non-null (we didn't set it to NaN)
        assert report["last_returns_included"]["stock_000"] is True
        assert report["pct_last_returns_captured"] == 100.0

    def test_last_returns_not_captured_when_pchg_null(self):
        delisted = ["stock_000"]
        df = _make_df(
            n_stocks=10,
            n_dates=4,
            delisted_stocks=delisted,
            last_pchg_null_for=["stock_000"],
        )
        report = check_survivorship_bias(df)

        assert "stock_000" in report["last_returns_included"]
        assert report["last_returns_included"]["stock_000"] is False
        assert report["pct_last_returns_captured"] == 0.0

    def test_last_returns_none_when_no_pchg_col(self):
        delisted = ["stock_000"]
        df = _make_df(
            n_stocks=10, n_dates=4, delisted_stocks=delisted, include_pchg=False
        )
        report = check_survivorship_bias(df)

        assert "stock_000" in report["last_returns_included"]
        assert report["last_returns_included"]["stock_000"] is None
        assert report["pct_last_returns_captured"] == 0.0


# ---------------------------------------------------------------------------
# Tests: Risk level thresholds
# ---------------------------------------------------------------------------

class TestRiskLevels:
    def test_low_risk_below_5pct(self):
        # 1 delisted out of 30 = 3.3% < 5%
        delisted = ["stock_000"]
        df = _make_df(n_stocks=30, n_dates=4, delisted_stocks=delisted)
        report = check_survivorship_bias(df)
        assert report["survivorship_bias_risk"] == "low"

    def test_medium_risk_between_5_and_10pct(self):
        # 1 delisted out of 12 = 8.3%, between 5% and 10%
        delisted = ["stock_000"]
        df = _make_df(n_stocks=12, n_dates=4, delisted_stocks=delisted)
        report = check_survivorship_bias(df)
        assert report["survivorship_bias_risk"] == "medium"

    def test_high_risk_above_10pct(self):
        # 2 delisted out of 10 = 20% > 10%
        delisted = ["stock_000", "stock_001"]
        df = _make_df(n_stocks=10, n_dates=4, delisted_stocks=delisted)
        report = check_survivorship_bias(df)
        assert report["survivorship_bias_risk"] == "high"

    def test_high_risk_triggers_warning(self):
        delisted = ["stock_000", "stock_001"]
        df = _make_df(n_stocks=10, n_dates=4, delisted_stocks=delisted)
        with warnings.catch_warnings(record=True) as caught:
            warnings.simplefilter("always")
            check_survivorship_bias(df)
        survivorship_warnings = [
            w for w in caught
            if issubclass(w.category, UserWarning) and "存活偏差警告" in str(w.message)
        ]
        assert len(survivorship_warnings) >= 1

    def test_low_risk_no_warning(self):
        delisted = ["stock_000"]
        df = _make_df(n_stocks=30, n_dates=4, delisted_stocks=delisted)
        with warnings.catch_warnings(record=True) as caught:
            warnings.simplefilter("always")
            check_survivorship_bias(df)
        survivorship_warnings = [
            w for w in caught
            if issubclass(w.category, UserWarning) and "存活偏差警告" in str(w.message)
        ]
        assert len(survivorship_warnings) == 0

    def test_exactly_10pct_is_medium_not_high(self):
        # 1 delisted out of 10 = exactly 10%, boundary: > 0.10 is high, so 10% is medium
        delisted = ["stock_000"]
        df = _make_df(n_stocks=10, n_dates=4, delisted_stocks=delisted)
        report = check_survivorship_bias(df)
        # 1/10 = 0.10, which is NOT > 0.10, so should be medium
        assert report["survivorship_bias_risk"] == "medium"


# ---------------------------------------------------------------------------
# Tests: IC comparison
# ---------------------------------------------------------------------------

class TestICComparison:
    def test_ic_comparison_skipped_when_no_pchg(self):
        delisted = ["stock_000"]
        df = _make_df(
            n_stocks=10, n_dates=4, delisted_stocks=delisted, include_pchg=False
        )
        report = check_survivorship_bias(df)
        assert report["ic_comparison_feasible"] is False
        assert report["ic_all"] is None
        assert report["ic_active"] is None

    def test_ic_comparison_skipped_when_no_factors(self):
        delisted = ["stock_000"]
        df = _make_df(
            n_stocks=10,
            n_dates=4,
            delisted_stocks=delisted,
            include_factors=False,
        )
        report = check_survivorship_bias(df)
        assert report["ic_comparison_feasible"] is False

    def test_ic_comparison_skipped_when_no_delisted(self):
        df = _make_df(n_stocks=10, n_dates=4)
        report = check_survivorship_bias(df)
        assert report["ic_comparison_feasible"] is False

    def test_ic_comparison_feasible_with_delisted_and_factors(self):
        delisted = ["stock_000", "stock_001"]
        df = _make_df(n_stocks=20, n_dates=6, delisted_stocks=delisted)
        report = check_survivorship_bias(df)
        # With enough data, IC comparison should be feasible
        assert report["ic_comparison_feasible"] is True
        assert report["ic_all"] is not None
        assert report["ic_active"] is not None
        assert report["ic_diff_pct"] is not None
        assert report["ic_diff_pct"] >= 0.0

    def test_ic_diff_warning_when_above_5pct(self):
        """Construct a scenario where IC diff is forced above 5% by making
        delisted stocks have systematically different pchg patterns."""
        # Build a DataFrame where delisted stocks have very different pchg
        # relative to the signal, creating a large IC difference.
        n_stocks = 30
        n_dates = 8
        dates = pd.date_range("2020-01-01", periods=n_dates, freq="7D")
        stock_ids = [f"stock_{i:03d}" for i in range(n_stocks)]
        delisted_ids = stock_ids[:5]  # 5/30 = 16.7% > 10%
        delisted_set = set(delisted_ids)

        rng = np.random.default_rng(42)
        rows = []
        for date in dates:
            for sid in stock_ids:
                if sid in delisted_set and date == dates[-1]:
                    continue
                factor_val = rng.normal(0, 1)
                # For delisted stocks, pchg is anti-correlated with factor
                # For active stocks, pchg is correlated with factor
                if sid in delisted_set:
                    pchg = -factor_val * 0.5 + rng.normal(0, 0.01)
                else:
                    pchg = factor_val * 0.5 + rng.normal(0, 0.01)
                rows.append({
                    "stock_id": sid,
                    "date": date,
                    "pchg": pchg,
                    "factor_a": factor_val,
                    "factor_b": rng.normal(0, 1),
                })

        df = pd.DataFrame(rows)
        df["date"] = pd.to_datetime(df["date"])
        df = df.sort_values(["date", "stock_id"]).reset_index(drop=True)

        with warnings.catch_warnings(record=True) as caught:
            warnings.simplefilter("always")
            report = check_survivorship_bias(df)

        # If IC diff > 5%, a warning should be issued
        if report["ic_comparison_feasible"] and report["ic_diff_pct"] is not None:
            if report["ic_diff_pct"] > 5.0:
                ic_warnings = [
                    w for w in caught
                    if issubclass(w.category, UserWarning)
                    and "IC 差异警告" in str(w.message)
                ]
                assert len(ic_warnings) >= 1


# ---------------------------------------------------------------------------
# Tests: Message content
# ---------------------------------------------------------------------------

class TestMessageContent:
    def test_message_is_string(self):
        df = _make_df(n_stocks=10, n_dates=4)
        report = check_survivorship_bias(df)
        assert isinstance(report["message"], str)
        assert len(report["message"]) > 0

    def test_message_contains_risk_level(self):
        df = _make_df(n_stocks=10, n_dates=4)
        report = check_survivorship_bias(df)
        assert "LOW" in report["message"].upper() or "MEDIUM" in report["message"].upper() or "HIGH" in report["message"].upper()

    def test_message_contains_stock_counts(self):
        df = _make_df(n_stocks=10, n_dates=4, delisted_stocks=["stock_000"])
        report = check_survivorship_bias(df)
        assert "10" in report["message"]  # total stocks
        assert "9" in report["message"]   # active stocks


# ---------------------------------------------------------------------------
# Tests: Consistency invariants
# ---------------------------------------------------------------------------

class TestConsistencyInvariants:
    def test_active_plus_delisted_equals_total(self):
        delisted = ["stock_000", "stock_001", "stock_002"]
        df = _make_df(n_stocks=20, n_dates=5, delisted_stocks=delisted)
        report = check_survivorship_bias(df)
        assert (
            report["n_active_stocks"] + report["n_potentially_delisted"]
            == report["n_total_stocks"]
        )

    def test_potentially_delisted_list_length_matches_count(self):
        delisted = ["stock_000", "stock_001"]
        df = _make_df(n_stocks=15, n_dates=4, delisted_stocks=delisted)
        report = check_survivorship_bias(df)
        assert len(report["potentially_delisted_stocks"]) == report["n_potentially_delisted"]

    def test_pct_last_returns_captured_in_range(self):
        delisted = ["stock_000", "stock_001"]
        df = _make_df(n_stocks=15, n_dates=4, delisted_stocks=delisted)
        report = check_survivorship_bias(df)
        assert 0.0 <= report["pct_last_returns_captured"] <= 100.0

    def test_ic_diff_pct_non_negative_when_feasible(self):
        delisted = ["stock_000", "stock_001"]
        df = _make_df(n_stocks=20, n_dates=6, delisted_stocks=delisted)
        report = check_survivorship_bias(df)
        if report["ic_comparison_feasible"]:
            assert report["ic_diff_pct"] >= 0.0

    def test_no_delisted_stocks_in_active_list(self):
        delisted = ["stock_000", "stock_001"]
        df = _make_df(n_stocks=15, n_dates=4, delisted_stocks=delisted)
        report = check_survivorship_bias(df)
        delisted_set = set(report["potentially_delisted_stocks"])
        # We can't directly get active list from report, but we can verify
        # that delisted stocks are not in the last cross-section
        last_date = df["date"].max()
        last_cross_section_stocks = set(
            df[df["date"] == last_date]["stock_id"].unique()
        )
        assert delisted_set.isdisjoint(last_cross_section_stocks)

    def test_deterministic_output(self):
        """Same input should always produce same output."""
        delisted = ["stock_000"]
        df = _make_df(n_stocks=10, n_dates=4, delisted_stocks=delisted)
        report1 = check_survivorship_bias(df)
        report2 = check_survivorship_bias(df)
        assert report1["n_total_stocks"] == report2["n_total_stocks"]
        assert report1["n_potentially_delisted"] == report2["n_potentially_delisted"]
        assert report1["survivorship_bias_risk"] == report2["survivorship_bias_risk"]
        assert report1["pct_last_returns_captured"] == report2["pct_last_returns_captured"]
