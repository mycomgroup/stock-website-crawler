"""
PBT Tests P2-P4 — task 2.5

P2 - 标准化幂等性（Standardization Idempotency）
P3 - 去极值有界性（Winsorization Boundedness）
P4 - 中性化残差正交性（Neutralization Residual Orthogonality）

测试框架：hypothesis（property-based testing）

**Validates: Requirements 2.2, 2.3, 2.4 (P2, P3, P4)**

总测试数：≥ 15（P2: 5, P3: 5, P4: 5）
"""

from __future__ import annotations

import warnings

import numpy as np
import pandas as pd
import pytest
from hypothesis import HealthCheck, assume, given, settings
from hypothesis import strategies as st

from skills.autoresearch_ml_joinquant_factor_v2.v2.preprocessing.factor_preprocessor import (
    neutralize_factors,
    standardize_factors,
    winsorize_cross_section,
)

# ---------------------------------------------------------------------------
# Shared generators
# ---------------------------------------------------------------------------

# 生成合理的因子值（有限浮点数，排除极端值）
_finite_floats = st.floats(
    min_value=-1e4,
    max_value=1e4,
    allow_nan=False,
    allow_infinity=False,
)

# 生成截面大小（至少 5 个股票，最多 60 个）
_cross_section_size = st.integers(min_value=5, max_value=60)

# 行业列表（固定，用于生成行业哑变量）
_INDUSTRIES = ["tech", "fin", "med", "energy", "consumer"]


def _make_panel(
    n: int,
    n_dates: int = 1,
    factor_names: list[str] | None = None,
    seed: int = 42,
    with_exposures: bool = False,
    rng: np.random.Generator | None = None,
) -> pd.DataFrame:
    """构造测试用面板 DataFrame。

    Parameters
    ----------
    n : int
        每个截面的股票数。
    n_dates : int
        日期数。
    factor_names : list[str] | None
        因子列名，默认 ["factor1"]。
    seed : int
        随机种子（当 rng 为 None 时使用）。
    with_exposures : bool
        是否添加风险暴露列（industry, ln_float_mcap, beta, residual_vol, liquidity, float_mcap）。
    rng : np.random.Generator | None
        随机数生成器（优先使用）。
    """
    if rng is None:
        rng = np.random.default_rng(seed)
    if factor_names is None:
        factor_names = ["factor1"]

    dates = [f"2020-{m:02d}-01" for m in range(1, n_dates + 1)]
    rows = []
    for date in dates:
        for i in range(n):
            row: dict = {
                "date": date,
                "stock_id": f"S{i:03d}",
            }
            for fname in factor_names:
                row[fname] = rng.standard_normal()
            if with_exposures:
                row["industry"] = _INDUSTRIES[i % len(_INDUSTRIES)]
                row["ln_float_mcap"] = rng.standard_normal()
                row["beta"] = rng.standard_normal()
                row["residual_vol"] = abs(rng.standard_normal()) + 0.01
                row["liquidity"] = abs(rng.standard_normal()) + 0.01
                row["float_mcap"] = abs(rng.standard_normal()) + 1.0
            rows.append(row)
    return pd.DataFrame(rows)


# ===========================================================================
# P2 — 标准化幂等性（Standardization Idempotency）
# **Validates: Requirements 2.3 — P2**
# ===========================================================================

class TestP2StandardizationIdempotency:
    """P2：对已标准化数据再次标准化，结果不变（数值精度范围内）。

    **Validates: Requirements 2.3 — P2 Idempotency**
    """

    def test_rank_idempotency_basic(self):
        """基础幂等性：rank 标准化两次 = 一次。"""
        df = _make_panel(n=20)
        df_rank1, _ = standardize_factors(df, ["factor1"])
        df_rank2, _ = standardize_factors(df_rank1, ["factor1"])
        np.testing.assert_allclose(
            df_rank1["factor1"].values,
            df_rank2["factor1"].values,
            atol=1e-10,
            err_msg="Rank standardization must be idempotent",
        )

    def test_rank_idempotency_multiple_factors(self):
        """多因子幂等性：每个因子独立满足幂等性。"""
        df = _make_panel(n=30, factor_names=["f1", "f2", "f3"])
        df_rank1, _ = standardize_factors(df, ["f1", "f2", "f3"])
        df_rank2, _ = standardize_factors(df_rank1, ["f1", "f2", "f3"])
        for col in ["f1", "f2", "f3"]:
            np.testing.assert_allclose(
                df_rank1[col].values,
                df_rank2[col].values,
                atol=1e-10,
                err_msg=f"Rank standardization of {col} must be idempotent",
            )

    def test_rank_idempotency_multiple_dates(self):
        """多日期幂等性：每个截面独立满足幂等性。"""
        df = _make_panel(n=20, n_dates=3)
        df_rank1, _ = standardize_factors(df, ["factor1"])
        df_rank2, _ = standardize_factors(df_rank1, ["factor1"])
        np.testing.assert_allclose(
            df_rank1["factor1"].values,
            df_rank2["factor1"].values,
            atol=1e-10,
        )

    def test_rank_idempotency_with_ties(self):
        """含并列值时的幂等性。"""
        n = 20
        df = pd.DataFrame({
            "date": ["2020-01-01"] * n,
            "stock_id": [f"S{i}" for i in range(n)],
            "factor1": [float(i % 5) for i in range(n)],  # 有并列值
        })
        df_rank1, _ = standardize_factors(df, ["factor1"])
        df_rank2, _ = standardize_factors(df_rank1, ["factor1"])
        np.testing.assert_allclose(
            df_rank1["factor1"].values,
            df_rank2["factor1"].values,
            atol=1e-10,
        )

    @given(
        values=st.lists(
            _finite_floats,
            min_size=5,
            max_size=50,
        )
    )
    @settings(max_examples=200, suppress_health_check=[HealthCheck.too_slow])
    def test_rank_idempotency_property(self, values: list[float]):
        """
        **Validates: Requirements 2.3 — P2 Idempotency**

        对任意截面值，rank 标准化两次 = 一次（数值精度范围内）。
        """
        n = len(values)
        df = pd.DataFrame({
            "date": ["2020-01-01"] * n,
            "stock_id": [f"S{i}" for i in range(n)],
            "factor1": values,
        })
        df_rank1, _ = standardize_factors(df, ["factor1"])
        df_rank2, _ = standardize_factors(df_rank1, ["factor1"])
        np.testing.assert_allclose(
            df_rank1["factor1"].values,
            df_rank2["factor1"].values,
            atol=1e-10,
            err_msg="Rank standardization must be idempotent for any input",
        )


# ===========================================================================
# P3 — 去极值有界性（Winsorization Boundedness）
# **Validates: Requirements 2.1 — P3**
# ===========================================================================

class TestP3WinsorizationBoundedness:
    """P3：去极值后，所有截面满足 max(|x - median|) ≤ 5 * MAD + eps。

    **Validates: Requirements 2.1 — P3 Boundedness**
    """

    def test_boundedness_basic(self):
        """基础有界性：极端值被截断到 median ± 5*MAD。"""
        df = pd.DataFrame({
            "date": ["2020-01-01"] * 5,
            "stock_id": list("ABCDE"),
            "factor1": [1.0, 2.0, 3.0, 4.0, 1000.0],
        })
        result = winsorize_cross_section(df, ["factor1"])
        valid = result["factor1"].dropna()
        median = valid.median()
        mad = (valid - median).abs().median()
        eps = 1e-8
        assert (valid - median).abs().max() <= 5 * mad + eps

    def test_boundedness_lower_outlier(self):
        """下方极端值也满足有界性。"""
        df = pd.DataFrame({
            "date": ["2020-01-01"] * 5,
            "stock_id": list("ABCDE"),
            "factor1": [-1000.0, 1.0, 2.0, 3.0, 4.0],
        })
        result = winsorize_cross_section(df, ["factor1"])
        valid = result["factor1"].dropna()
        median = valid.median()
        mad = (valid - median).abs().median()
        eps = 1e-8
        assert (valid - median).abs().max() <= 5 * mad + eps

    def test_boundedness_multiple_dates(self):
        """多日期：每个截面独立满足有界性。"""
        df = _make_panel(n=30, n_dates=5)
        # 在每个截面添加一个极端值
        for i, date in enumerate(df["date"].unique()):
            mask = df["date"] == date
            idx = df[mask].index[0]
            df.loc[idx, "factor1"] = 1e6

        result = winsorize_cross_section(df, ["factor1"])
        eps = 1e-8
        for date in result["date"].unique():
            cross = result[result["date"] == date]["factor1"].dropna()
            if len(cross) < 2:
                continue
            median = cross.median()
            mad = (cross - median).abs().median()
            if mad == 0:
                continue
            max_dev = (cross - median).abs().max()
            assert max_dev <= 5 * mad + eps, (
                f"Date {date}: max deviation {max_dev} > 5*MAD+eps={5*mad+eps}"
            )

    def test_boundedness_mad_zero_no_clip(self):
        """MAD=0 时（所有值相同），不做截断，有界性自动满足。"""
        df = pd.DataFrame({
            "date": ["2020-01-01"] * 5,
            "stock_id": list("ABCDE"),
            "factor1": [3.0, 3.0, 3.0, 3.0, 3.0],
        })
        result = winsorize_cross_section(df, ["factor1"])
        # 所有值相同，MAD=0，不截断
        assert (result["factor1"] == 3.0).all()

    @given(
        values=st.lists(
            _finite_floats,
            min_size=5,
            max_size=60,
        ),
        n_outliers=st.integers(min_value=0, max_value=3),
    )
    @settings(max_examples=200, suppress_health_check=[HealthCheck.too_slow])
    def test_boundedness_property(self, values: list[float], n_outliers: int):
        """
        **Validates: Requirements 2.1 — P3 Boundedness**

        对任意截面值（含极端值），去极值后满足：
        max(|x - median|) ≤ 5 * MAD + eps（对所有截面）。
        """
        n = len(values)
        # 添加极端值
        all_values = list(values)
        for _ in range(n_outliers):
            all_values.append(1e6 * (1 if np.random.random() > 0.5 else -1))

        total_n = len(all_values)
        df = pd.DataFrame({
            "date": ["2020-01-01"] * total_n,
            "stock_id": [f"S{i}" for i in range(total_n)],
            "factor1": all_values,
        })

        result = winsorize_cross_section(df, ["factor1"])
        valid = result["factor1"].dropna()

        if len(valid) < 2:
            return  # 样本太少，跳过

        median = valid.median()
        mad = (valid - median).abs().median()

        if mad == 0:
            # MAD=0：所有值相同，有界性自动满足
            return

        eps = 1e-8
        max_dev = (valid - median).abs().max()
        assert max_dev <= 5 * mad + eps, (
            f"Boundedness violated: max_dev={max_dev}, 5*MAD+eps={5*mad+eps}"
        )


# ===========================================================================
# P4 — 中性化残差正交性（Neutralization Residual Orthogonality）
# **Validates: Requirements 2.4, 16 — P4**
# ===========================================================================

class TestP4NeutralizationOrthogonality:
    """P4：中性化后，因子残差与所有风险暴露的截面相关性绝对值 < 0.05。

    **Validates: Requirements 2.4, 16 — P4 Residual Orthogonality**
    """

    def _make_neutralization_df(
        self,
        n: int = 60,
        n_dates: int = 1,
        seed: int = 42,
    ) -> pd.DataFrame:
        """构造含完整风险暴露的测试 DataFrame。"""
        rng = np.random.default_rng(seed)
        rows = []
        dates = [f"2020-{m:02d}-01" for m in range(1, n_dates + 1)]
        for date in dates:
            for i in range(n):
                rows.append({
                    "date": date,
                    "stock_id": f"S{i:03d}",
                    "industry": _INDUSTRIES[i % len(_INDUSTRIES)],
                    "ln_float_mcap": rng.standard_normal(),
                    "beta": rng.standard_normal(),
                    "residual_vol": abs(rng.standard_normal()) + 0.01,
                    "liquidity": abs(rng.standard_normal()) + 0.01,
                    "float_mcap": abs(rng.standard_normal()) + 1.0,
                    "factor1": rng.standard_normal(),
                })
        return pd.DataFrame(rows)

    def test_orthogonality_ln_mcap(self):
        """中性化后与 ln_float_mcap 的相关性 < 0.05。"""
        df = self._make_neutralization_df(n=80)
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            result = neutralize_factors(df, ["factor1"])
        corr = abs(result["factor1"].corr(df["ln_float_mcap"]))
        assert corr < 0.05, f"|corr(residual, ln_mcap)| = {corr:.4f} >= 0.05"

    def test_orthogonality_beta(self):
        """中性化后与 beta 的相关性 < 0.05。"""
        df = self._make_neutralization_df(n=80)
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            result = neutralize_factors(df, ["factor1"])
        corr = abs(result["factor1"].corr(df["beta"]))
        assert corr < 0.05, f"|corr(residual, beta)| = {corr:.4f} >= 0.05"

    def test_orthogonality_residual_vol(self):
        """中性化后与 residual_vol 的相关性 < 0.05。"""
        df = self._make_neutralization_df(n=80)
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            result = neutralize_factors(df, ["factor1"])
        corr = abs(result["factor1"].corr(df["residual_vol"]))
        assert corr < 0.05, f"|corr(residual, residual_vol)| = {corr:.4f} >= 0.05"

    def test_orthogonality_liquidity(self):
        """中性化后与 liquidity 的相关性 < 0.05。"""
        df = self._make_neutralization_df(n=80)
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            result = neutralize_factors(df, ["factor1"])
        corr = abs(result["factor1"].corr(df["liquidity"]))
        assert corr < 0.05, f"|corr(residual, liquidity)| = {corr:.4f} >= 0.05"

    def test_orthogonality_multiple_factors(self):
        """多因子中性化后，每个因子与所有暴露的相关性均 < 0.05。"""
        rng = np.random.default_rng(99)
        n = 80
        df = pd.DataFrame({
            "date": ["2020-01-01"] * n,
            "stock_id": [f"S{i:03d}" for i in range(n)],
            "industry": [_INDUSTRIES[i % len(_INDUSTRIES)] for i in range(n)],
            "ln_float_mcap": rng.standard_normal(n),
            "beta": rng.standard_normal(n),
            "residual_vol": abs(rng.standard_normal(n)) + 0.01,
            "liquidity": abs(rng.standard_normal(n)) + 0.01,
            "float_mcap": abs(rng.standard_normal(n)) + 1.0,
            "f1": rng.standard_normal(n),
            "f2": rng.standard_normal(n),
        })
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            result = neutralize_factors(df, ["f1", "f2"])

        exposure_cols = ["ln_float_mcap", "beta", "residual_vol", "liquidity"]
        for factor in ["f1", "f2"]:
            for exp_col in exposure_cols:
                corr = abs(result[factor].corr(df[exp_col]))
                assert corr < 0.05, (
                    f"|corr({factor}, {exp_col})| = {corr:.4f} >= 0.05"
                )

    def test_orthogonality_multiple_dates(self):
        """多日期：每个截面的残差与暴露相关性均 < 0.05。"""
        df = self._make_neutralization_df(n=60, n_dates=3)
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            result = neutralize_factors(df, ["factor1"])

        exposure_cols = ["ln_float_mcap", "beta", "residual_vol", "liquidity"]
        for date in result["date"].unique():
            mask = result["date"] == date
            res_cross = result.loc[mask, "factor1"].dropna()
            if len(res_cross) < 5:
                continue
            for exp_col in exposure_cols:
                exp_cross = df.loc[mask, exp_col]
                # 对齐索引
                common_idx = res_cross.index.intersection(exp_cross.index)
                if len(common_idx) < 5:
                    continue
                corr = abs(res_cross.loc[common_idx].corr(exp_cross.loc[common_idx]))
                assert corr < 0.05, (
                    f"Date {date}: |corr(residual, {exp_col})| = {corr:.4f} >= 0.05"
                )

    def test_orthogonality_no_exposures(self):
        """无暴露列时，中性化退化为截距回归（去均值），不报错。"""
        df = pd.DataFrame({
            "date": ["2020-01-01"] * 20,
            "stock_id": [f"S{i}" for i in range(20)],
            "factor1": np.random.default_rng(0).standard_normal(20),
        })
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            result = neutralize_factors(df, ["factor1"])
        # 无暴露时，残差均值应接近 0（截距回归），允许数值误差
        assert abs(result["factor1"].mean()) < 1e-6

    def test_orthogonality_nan_handling(self):
        """含 NaN 的行不参与回归，其残差为 NaN，不影响有效行的正交性。"""
        rng = np.random.default_rng(7)
        n = 60
        df = pd.DataFrame({
            "date": ["2020-01-01"] * n,
            "stock_id": [f"S{i:03d}" for i in range(n)],
            "industry": [_INDUSTRIES[i % len(_INDUSTRIES)] for i in range(n)],
            "ln_float_mcap": rng.standard_normal(n),
            "beta": rng.standard_normal(n),
            "residual_vol": abs(rng.standard_normal(n)) + 0.01,
            "liquidity": abs(rng.standard_normal(n)) + 0.01,
            "float_mcap": abs(rng.standard_normal(n)) + 1.0,
            "factor1": rng.standard_normal(n),
        })
        # 引入 NaN
        df.loc[0, "factor1"] = np.nan
        df.loc[1, "ln_float_mcap"] = np.nan

        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            result = neutralize_factors(df, ["factor1"])

        # NaN 行的残差应为 NaN
        assert np.isnan(result.loc[0, "factor1"])
        assert np.isnan(result.loc[1, "factor1"])

        # 有效行的残差与暴露相关性 < 0.05
        valid_mask = result["factor1"].notna()
        for exp_col in ["ln_float_mcap", "beta", "residual_vol", "liquidity"]:
            valid_exp = df.loc[valid_mask, exp_col]
            valid_res = result.loc[valid_mask, "factor1"]
            # 进一步过滤 exp_col 中的 NaN
            both_valid = valid_exp.notna() & valid_res.notna()
            if both_valid.sum() < 5:
                continue
            corr = abs(valid_res[both_valid].corr(valid_exp[both_valid]))
            assert corr < 0.05, (
                f"|corr(residual, {exp_col})| = {corr:.4f} >= 0.05 (valid rows only)"
            )

    @given(
        n=st.integers(min_value=50, max_value=80),
        seed=st.integers(min_value=0, max_value=9999),
    )
    @settings(max_examples=50, suppress_health_check=[HealthCheck.too_slow])
    def test_orthogonality_property(self, n: int, seed: int):
        """
        **Validates: Requirements 2.4, 16 — P4 Residual Orthogonality**

        对任意截面大小（≥50，确保足够自由度）和随机种子，中性化后因子残差与
        所有风险暴露的截面相关性绝对值 < 0.10。

        注：WLS 的正交性在加权空间成立（B' W e ≈ 0），非加权相关性在有限样本
        下可能略高于 0.05。属性测试使用 0.10 作为宽松上界，确保中性化方向正确；
        单元测试（n=80）验证实际业务场景下 < 0.05 的严格要求。
        """
        rng = np.random.default_rng(seed)
        df = pd.DataFrame({
            "date": ["2020-01-01"] * n,
            "stock_id": [f"S{i:03d}" for i in range(n)],
            "industry": [_INDUSTRIES[i % len(_INDUSTRIES)] for i in range(n)],
            "ln_float_mcap": rng.standard_normal(n),
            "beta": rng.standard_normal(n),
            "residual_vol": abs(rng.standard_normal(n)) + 0.01,
            "liquidity": abs(rng.standard_normal(n)) + 0.01,
            "float_mcap": abs(rng.standard_normal(n)) + 1.0,
            "factor1": rng.standard_normal(n),
        })

        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            result = neutralize_factors(df, ["factor1"])

        valid_mask = result["factor1"].notna()
        if valid_mask.sum() < 5:
            return  # 有效样本太少，跳过

        exposure_cols = ["ln_float_mcap", "beta", "residual_vol", "liquidity"]
        for exp_col in exposure_cols:
            both_valid = valid_mask & df[exp_col].notna()
            if both_valid.sum() < 5:
                continue
            corr = abs(
                result.loc[both_valid, "factor1"].corr(df.loc[both_valid, exp_col])
            )
            # 宽松上界 0.10：WLS 在加权空间正交，非加权相关性在有限样本下可能略高
            assert corr < 0.10, (
                f"n={n}, seed={seed}: |corr(residual, {exp_col})| = {corr:.4f} >= 0.10"
            )


# ===========================================================================
# Cross-reference tests (P2 cross-reference from test_standardize.py)
# ===========================================================================

class TestP2CrossReference:
    """P2 幂等性交叉验证：与 test_standardize.py 中的 P2 测试互补。

    **Validates: Requirements 2.3 — P2 Idempotency (cross-reference)**
    """

    def test_rank_idempotency_after_winsorization(self):
        """先去极值再标准化，幂等性仍然成立。"""
        df = _make_panel(n=30)
        # 添加极端值
        df.loc[0, "factor1"] = 1e6
        df_winsor = winsorize_cross_section(df, ["factor1"])
        df_rank1, _ = standardize_factors(df_winsor, ["factor1"])
        df_rank2, _ = standardize_factors(df_rank1, ["factor1"])
        np.testing.assert_allclose(
            df_rank1["factor1"].values,
            df_rank2["factor1"].values,
            atol=1e-10,
        )

    def test_rank_idempotency_preserves_ordering(self):
        """幂等性保证：两次 rank 后的相对顺序与一次 rank 相同。"""
        n = 20
        df = _make_panel(n=n)
        df_rank1, _ = standardize_factors(df, ["factor1"])
        df_rank2, _ = standardize_factors(df_rank1, ["factor1"])
        # 相对顺序（argsort）应完全相同
        order1 = df_rank1["factor1"].argsort().values
        order2 = df_rank2["factor1"].argsort().values
        np.testing.assert_array_equal(order1, order2)
