import pathlib
import sys

import numpy as np
import pandas as pd


sys.path.append(str(pathlib.Path(__file__).resolve().parent))
from weak_factor_portfolio import EPS, standardize_factors


def test_standardize_without_group_zscore():
    idx = pd.MultiIndex.from_product(
        [pd.to_datetime(["2024-01-01", "2024-01-02"]), ["A", "B", "C"]],
        names=["date", "stock"],
    )
    df = pd.DataFrame({"f1": [1, 2, 3, 4, 5, 6], "f2": [10, 20, 30, 40, 50, 60]}, index=idx)

    out = standardize_factors(df, method="zscore")
    expected = df.groupby(level="date").transform(lambda x: (x - x.mean()) / (x.std(ddof=0) + EPS))

    pd.testing.assert_frame_equal(out, expected)


def test_standardize_with_group_on_multiindex_rank():
    idx = pd.MultiIndex.from_product(
        [pd.to_datetime(["2024-01-01", "2024-01-02"]), ["A", "B", "C", "D"]],
        names=["date", "stock"],
    )
    df = pd.DataFrame({"f1": [1, 2, 3, 4, 5, 6, 7, 8]}, index=idx)
    sector = pd.Series({"A": "g1", "B": "g1", "C": "g2", "D": "g2"})

    out = standardize_factors(df, method="rank", group_col=sector)
    expected = (
        df.groupby([df.index.get_level_values("date"), df.index.get_level_values("stock").map(sector)])
        .transform(lambda x: x.rank(pct=True) * 2 - 1)
    )

    pd.testing.assert_frame_equal(out, expected)


def test_standardize_with_missing_group_on_date_column():
    df = pd.DataFrame(
        {
            "date": pd.to_datetime(["2024-01-01", "2024-01-01", "2024-01-01", "2024-01-01"]),
            "factor": [1.0, 2.0, 3.0, 4.0],
            "group": ["g1", "g1", None, None],
        }
    )

    out = standardize_factors(df, method="rank", group_col="group")

    expected = pd.Series([0.0, 1.0, 0.0, 1.0], name="factor")
    pd.testing.assert_series_equal(out["factor"], expected)
    assert out["group"].isna().sum() == 2


def test_standardize_constant_column_returns_zero():
    idx = pd.MultiIndex.from_product(
        [pd.to_datetime(["2024-01-01"]), ["A", "B", "C"]],
        names=["date", "stock"],
    )
    df = pd.DataFrame({"f_const": [5.0, 5.0, 5.0]}, index=idx)

    out = standardize_factors(df, method="zscore")
    assert np.allclose(out["f_const"].to_numpy(), 0.0)
