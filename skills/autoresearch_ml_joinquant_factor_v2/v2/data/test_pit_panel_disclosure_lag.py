"""单元测试：apply_disclosure_lag() 和 _check_disclosure_lag_status()

对应任务：Task 1.3 实现财务因子时滞校验
对应需求：需求 1.3（财务因子必须按实际披露日生效，不允许按报告期末提前生效）
"""

from __future__ import annotations

import warnings

import pandas as pd
import pytest

from skills.autoresearch_ml_joinquant_factor_v2.v2.data.pit_panel import (
    _check_disclosure_lag_status,
    _infer_financial_cols,
    apply_disclosure_lag,
)


# ---------------------------------------------------------------------------
# 测试辅助函数
# ---------------------------------------------------------------------------

def _make_df(
    stocks: list[str],
    dates: list[str],
    financial_vals: dict[str, list] | None = None,
    disclosure_col: str | None = None,
    disclosure_dates: list[str] | None = None,
    extra_cols: dict | None = None,
) -> pd.DataFrame:
    """构造测试用 DataFrame。"""
    data: dict = {
        "stock_id": stocks,
        "date": pd.to_datetime(dates),
        "pchg": [0.01] * len(stocks),
    }
    if financial_vals:
        data.update(financial_vals)
    if disclosure_col and disclosure_dates:
        data[disclosure_col] = pd.to_datetime(disclosure_dates)
    if extra_cols:
        data.update(extra_cols)
    df = pd.DataFrame(data)
    df = df.sort_values(["date", "stock_id"]).reset_index(drop=True)
    return df


# ---------------------------------------------------------------------------
# _check_disclosure_lag_status 测试
# ---------------------------------------------------------------------------

class TestCheckDisclosureLagStatus:
    """测试 _check_disclosure_lag_status() 诊断函数。"""

    def test_returns_dict_with_required_keys(self):
        """返回值应包含所有必需的键。"""
        df = _make_df(stocks=["A"], dates=["2020-01-01"])
        result = _check_disclosure_lag_status(df)
        required_keys = {
            "has_disclosure_col",
            "disclosure_col_found",
            "n_financial_cols",
            "financial_cols",
            "risk_level",
            "message",
        }
        assert required_keys.issubset(set(result.keys()))

    def test_no_disclosure_col_returns_high_risk(self):
        """无披露日字段且有财务因子时，风险等级应为 high。"""
        df = _make_df(
            stocks=["A"],
            dates=["2020-01-01"],
            financial_vals={"roa_ttm": [0.1]},
        )
        result = _check_disclosure_lag_status(df)
        assert result["has_disclosure_col"] is False
        assert result["disclosure_col_found"] is None
        assert result["risk_level"] == "high"

    def test_ann_date_col_returns_low_risk(self):
        """有 ann_date 字段时，风险等级应为 low。"""
        df = _make_df(
            stocks=["A"],
            dates=["2020-01-01"],
            financial_vals={"roa_ttm": [0.1]},
            disclosure_col="ann_date",
            disclosure_dates=["2020-01-15"],
        )
        result = _check_disclosure_lag_status(df)
        assert result["has_disclosure_col"] is True
        assert result["disclosure_col_found"] == "ann_date"
        assert result["risk_level"] == "low"

    def test_announcement_date_col_detected(self):
        """有 announcement_date 字段时应被检测到。"""
        df = _make_df(
            stocks=["A"],
            dates=["2020-01-01"],
            disclosure_col="announcement_date",
            disclosure_dates=["2020-01-15"],
        )
        result = _check_disclosure_lag_status(df)
        assert result["disclosure_col_found"] == "announcement_date"

    def test_disclosure_date_col_detected(self):
        """有 disclosure_date 字段时应被检测到。"""
        df = _make_df(
            stocks=["A"],
            dates=["2020-01-01"],
            disclosure_col="disclosure_date",
            disclosure_dates=["2020-01-15"],
        )
        result = _check_disclosure_lag_status(df)
        assert result["disclosure_col_found"] == "disclosure_date"

    def test_no_financial_cols_no_disclosure_returns_low_risk(self):
        """无披露日字段且无财务因子时，风险等级应为 low（无需校验）。"""
        df = pd.DataFrame({
            "stock_id": ["A"],
            "date": pd.to_datetime(["2020-01-01"]),
            "pchg": [0.01],
            "momentum_score": [0.5],  # 非财务类因子
        })
        result = _check_disclosure_lag_status(df)
        assert result["has_disclosure_col"] is False
        assert result["risk_level"] == "low"

    def test_financial_cols_list_is_list(self):
        """financial_cols 字段应为列表类型。"""
        df = _make_df(stocks=["A"], dates=["2020-01-01"])
        result = _check_disclosure_lag_status(df)
        assert isinstance(result["financial_cols"], list)

    def test_n_financial_cols_matches_financial_cols_length(self):
        """n_financial_cols 应与 financial_cols 列表长度一致。"""
        df = _make_df(
            stocks=["A"],
            dates=["2020-01-01"],
            financial_vals={"roa_ttm": [0.1], "roe_ttm": [0.2]},
        )
        result = _check_disclosure_lag_status(df)
        assert result["n_financial_cols"] == len(result["financial_cols"])

    def test_message_is_non_empty_string(self):
        """message 字段应为非空字符串。"""
        df = _make_df(stocks=["A"], dates=["2020-01-01"])
        result = _check_disclosure_lag_status(df)
        assert isinstance(result["message"], str)
        assert len(result["message"]) > 0

    def test_risk_level_valid_values(self):
        """risk_level 应为 'low'、'medium' 或 'high' 之一。"""
        df = _make_df(stocks=["A"], dates=["2020-01-01"])
        result = _check_disclosure_lag_status(df)
        assert result["risk_level"] in {"low", "medium", "high"}


# ---------------------------------------------------------------------------
# apply_disclosure_lag 路径 B（无披露日字段）测试
# ---------------------------------------------------------------------------

class TestApplyDisclosureLagPathB:
    """测试 apply_disclosure_lag() 路径 B：无披露日字段。"""

    def test_issues_user_warning_when_no_disclosure_col(self):
        """无披露日字段时应发出 UserWarning。"""
        df = _make_df(
            stocks=["A"],
            dates=["2020-01-01"],
            financial_vals={"roa_ttm": [0.1]},
        )
        fin_cols = _infer_financial_cols(df)
        with pytest.warns(UserWarning, match="披露日字段"):
            apply_disclosure_lag(df, fin_cols)

    def test_returns_original_df_unchanged_when_no_disclosure_col(self):
        """无披露日字段时应返回原始 df，数据不被修改。"""
        df = _make_df(
            stocks=["A", "B"],
            dates=["2020-01-01", "2020-01-01"],
            financial_vals={"roa_ttm": [0.1, 0.2], "roe_ttm": [0.3, 0.4]},
        )
        fin_cols = _infer_financial_cols(df)
        original_values = df[["roa_ttm", "roe_ttm"]].copy()

        with warnings.catch_warnings():
            warnings.simplefilter("ignore", UserWarning)
            result = apply_disclosure_lag(df, fin_cols)

        pd.testing.assert_frame_equal(result[["roa_ttm", "roe_ttm"]], original_values)

    def test_returns_same_shape_when_no_disclosure_col(self):
        """无披露日字段时返回的 df 形状应与输入一致。"""
        df = _make_df(
            stocks=["A", "B", "C"],
            dates=["2020-01-01"] * 3,
            financial_vals={"roa_ttm": [0.1, 0.2, 0.3]},
        )
        fin_cols = _infer_financial_cols(df)
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", UserWarning)
            result = apply_disclosure_lag(df, fin_cols)
        assert result.shape == df.shape

    def test_warning_message_mentions_risk(self):
        """警告信息应提及风险（look-ahead bias 或未来信息泄漏）。"""
        df = _make_df(
            stocks=["A"],
            dates=["2020-01-01"],
            financial_vals={"roa_ttm": [0.1]},
        )
        fin_cols = _infer_financial_cols(df)
        with pytest.warns(UserWarning) as warning_list:
            apply_disclosure_lag(df, fin_cols)
        warning_text = str(warning_list[0].message)
        # 应提及风险相关词汇
        assert any(kw in warning_text for kw in ["风险", "泄漏", "look-ahead", "bias"])

    def test_no_warning_when_no_financial_cols(self):
        """无财务类因子列时，即使无披露日字段，也不应发出警告（无需校验）。"""
        df = pd.DataFrame({
            "stock_id": ["A"],
            "date": pd.to_datetime(["2020-01-01"]),
            "pchg": [0.01],
            "momentum_score": [0.5],
        })
        # 传入空的 financial_cols
        with warnings.catch_warnings(record=True) as warning_list:
            warnings.simplefilter("always")
            result = apply_disclosure_lag(df, [])
        # 不应有 UserWarning（因为没有财务因子需要校验）
        user_warnings = [w for w in warning_list if issubclass(w.category, UserWarning)]
        assert len(user_warnings) == 0

    def test_empty_df_no_disclosure_col_returns_empty(self):
        """空 DataFrame 无披露日字段时应返回空 DataFrame。"""
        df = pd.DataFrame(columns=["stock_id", "date", "pchg", "roa_ttm"])
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", UserWarning)
            result = apply_disclosure_lag(df, ["roa_ttm"])
        assert len(result) == 0


# ---------------------------------------------------------------------------
# apply_disclosure_lag 路径 A（有披露日字段）测试
# ---------------------------------------------------------------------------

class TestApplyDisclosureLagPathA:
    """测试 apply_disclosure_lag() 路径 A：有披露日字段，按实际披露日对齐。"""

    def test_no_warning_when_disclosure_col_present(self):
        """有披露日字段时不应发出 UserWarning。"""
        df = _make_df(
            stocks=["A"],
            dates=["2020-03-31"],
            financial_vals={"roa_ttm": [0.1]},
            disclosure_col="ann_date",
            disclosure_dates=["2020-04-30"],  # 披露日晚于截面日期
        )
        fin_cols = _infer_financial_cols(df)
        with warnings.catch_warnings(record=True) as warning_list:
            warnings.simplefilter("always")
            apply_disclosure_lag(df, fin_cols)
        user_warnings = [w for w in warning_list if issubclass(w.category, UserWarning)]
        assert len(user_warnings) == 0

    def test_future_disclosure_sets_nan(self):
        """披露日晚于截面日期时，财务因子应置为 NaN（防止未来信息泄漏）。"""
        df = _make_df(
            stocks=["A"],
            dates=["2020-03-31"],
            financial_vals={"roa_ttm": [0.1]},
            disclosure_col="ann_date",
            disclosure_dates=["2020-04-30"],  # 披露日 > 截面日期
        )
        fin_cols = _infer_financial_cols(df)
        result = apply_disclosure_lag(df, fin_cols)
        assert pd.isna(result.loc[0, "roa_ttm"]), "披露日晚于截面日期时，财务因子应为 NaN"

    def test_past_disclosure_keeps_value(self):
        """披露日早于或等于截面日期时，财务因子应保留原值。"""
        df = _make_df(
            stocks=["A"],
            dates=["2020-06-30"],
            financial_vals={"roa_ttm": [0.1]},
            disclosure_col="ann_date",
            disclosure_dates=["2020-04-30"],  # 披露日 < 截面日期
        )
        fin_cols = _infer_financial_cols(df)
        result = apply_disclosure_lag(df, fin_cols)
        assert result.loc[0, "roa_ttm"] == pytest.approx(0.1), "披露日早于截面日期时，财务因子应保留原值"

    def test_same_day_disclosure_keeps_value(self):
        """披露日等于截面日期时，财务因子应保留原值（当天可得）。"""
        df = _make_df(
            stocks=["A"],
            dates=["2020-04-30"],
            financial_vals={"roa_ttm": [0.1]},
            disclosure_col="ann_date",
            disclosure_dates=["2020-04-30"],  # 披露日 == 截面日期
        )
        fin_cols = _infer_financial_cols(df)
        result = apply_disclosure_lag(df, fin_cols)
        assert result.loc[0, "roa_ttm"] == pytest.approx(0.1), "披露日等于截面日期时，财务因子应保留原值"

    def test_mixed_rows_partial_nan(self):
        """部分行披露日晚于截面日期，部分行早于，应分别处理。"""
        df = _make_df(
            stocks=["A", "B", "C"],
            dates=["2020-03-31", "2020-06-30", "2020-03-31"],
            financial_vals={"roa_ttm": [0.1, 0.2, 0.3]},
            disclosure_col="ann_date",
            disclosure_dates=[
                "2020-04-30",  # A: 披露日 > 截面日期 → NaN
                "2020-04-30",  # B: 披露日 < 截面日期 → 保留
                "2020-03-31",  # C: 披露日 == 截面日期 → 保留
            ],
        )
        fin_cols = _infer_financial_cols(df)
        result = apply_disclosure_lag(df, fin_cols)

        # 找到各行
        a_row = result[result["stock_id"] == "A"].iloc[0]
        b_row = result[result["stock_id"] == "B"].iloc[0]
        c_row = result[result["stock_id"] == "C"].iloc[0]

        assert pd.isna(a_row["roa_ttm"]), "A: 披露日晚于截面日期，应为 NaN"
        assert b_row["roa_ttm"] == pytest.approx(0.2), "B: 披露日早于截面日期，应保留原值"
        assert c_row["roa_ttm"] == pytest.approx(0.3), "C: 披露日等于截面日期，应保留原值"

    def test_non_financial_cols_not_affected(self):
        """非财务类因子列（如 pchg）不应被时滞校验影响。"""
        df = _make_df(
            stocks=["A"],
            dates=["2020-03-31"],
            financial_vals={"roa_ttm": [0.1]},
            disclosure_col="ann_date",
            disclosure_dates=["2020-04-30"],
        )
        original_pchg = df["pchg"].copy()
        fin_cols = _infer_financial_cols(df)
        result = apply_disclosure_lag(df, fin_cols)
        pd.testing.assert_series_equal(result["pchg"], original_pchg)

    def test_multiple_financial_cols_all_masked(self):
        """多个财务类因子列，披露日晚于截面日期时，所有列都应置 NaN。"""
        df = _make_df(
            stocks=["A"],
            dates=["2020-03-31"],
            financial_vals={"roa_ttm": [0.1], "roe_ttm": [0.2], "net_profit_ttm": [1000.0]},
            disclosure_col="ann_date",
            disclosure_dates=["2020-04-30"],
        )
        fin_cols = _infer_financial_cols(df)
        result = apply_disclosure_lag(df, fin_cols)
        for col in fin_cols:
            assert pd.isna(result.loc[0, col]), f"列 {col} 应为 NaN（披露日晚于截面日期）"

    def test_returns_copy_not_inplace(self):
        """路径 A 应返回新的 DataFrame，不修改原始 df。"""
        df = _make_df(
            stocks=["A"],
            dates=["2020-03-31"],
            financial_vals={"roa_ttm": [0.1]},
            disclosure_col="ann_date",
            disclosure_dates=["2020-04-30"],
        )
        original_val = df.loc[0, "roa_ttm"]
        fin_cols = _infer_financial_cols(df)
        result = apply_disclosure_lag(df, fin_cols)
        # 原始 df 不应被修改
        assert df.loc[0, "roa_ttm"] == pytest.approx(original_val), "原始 df 不应被修改"
        # 返回的 result 应被修改
        assert pd.isna(result.loc[0, "roa_ttm"]), "返回的 result 应被修改"

    def test_empty_financial_cols_returns_df_unchanged(self):
        """传入空的 financial_cols 时，df 应原样返回。"""
        df = _make_df(
            stocks=["A"],
            dates=["2020-03-31"],
            financial_vals={"roa_ttm": [0.1]},
            disclosure_col="ann_date",
            disclosure_dates=["2020-04-30"],
        )
        result = apply_disclosure_lag(df, [])
        # roa_ttm 不在 financial_cols 中，不应被置 NaN
        assert result.loc[0, "roa_ttm"] == pytest.approx(0.1)

    def test_announcement_date_col_works(self):
        """使用 announcement_date 字段时，路径 A 应正常工作。"""
        df = _make_df(
            stocks=["A"],
            dates=["2020-03-31"],
            financial_vals={"roa_ttm": [0.1]},
            disclosure_col="announcement_date",
            disclosure_dates=["2020-04-30"],
        )
        fin_cols = _infer_financial_cols(df)
        result = apply_disclosure_lag(df, fin_cols)
        assert pd.isna(result.loc[0, "roa_ttm"])

    def test_disclosure_date_col_works(self):
        """使用 disclosure_date 字段时，路径 A 应正常工作。"""
        df = _make_df(
            stocks=["A"],
            dates=["2020-03-31"],
            financial_vals={"roa_ttm": [0.1]},
            disclosure_col="disclosure_date",
            disclosure_dates=["2020-04-30"],
        )
        fin_cols = _infer_financial_cols(df)
        result = apply_disclosure_lag(df, fin_cols)
        assert pd.isna(result.loc[0, "roa_ttm"])

    def test_empty_df_with_disclosure_col_returns_empty(self):
        """空 DataFrame 有披露日字段时应返回空 DataFrame。"""
        df = pd.DataFrame(columns=["stock_id", "date", "pchg", "roa_ttm", "ann_date"])
        result = apply_disclosure_lag(df, ["roa_ttm"])
        assert len(result) == 0

    def test_pit_consistency_no_future_info(self):
        """点时一致性验证：截面日期 t 的财务因子不应包含 t 之后才披露的信息。

        场景：季报在报告期末（3月31日）后约 4 月（4月30日）才披露。
        截面日期为 3月31日时，财务因子应为 NaN（尚未披露）。
        截面日期为 5月1日时，财务因子应可见（已披露）。
        """
        df = pd.DataFrame({
            "stock_id": ["A", "A"],
            "date": pd.to_datetime(["2020-03-31", "2020-05-01"]),
            "pchg": [0.01, 0.02],
            "roa_ttm": [0.1, 0.1],  # 同一报告期的财务数据
            "ann_date": pd.to_datetime(["2020-04-30", "2020-04-30"]),  # 4月30日披露
        })
        df = df.sort_values(["date", "stock_id"]).reset_index(drop=True)
        fin_cols = _infer_financial_cols(df)
        result = apply_disclosure_lag(df, fin_cols)

        # 3月31日截面：披露日(4月30日) > 截面日期(3月31日) → NaN
        row_march = result[result["date"] == pd.Timestamp("2020-03-31")].iloc[0]
        assert pd.isna(row_march["roa_ttm"]), "3月31日截面：财务因子尚未披露，应为 NaN"

        # 5月1日截面：披露日(4月30日) < 截面日期(5月1日) → 保留原值
        row_may = result[result["date"] == pd.Timestamp("2020-05-01")].iloc[0]
        assert row_may["roa_ttm"] == pytest.approx(0.1), "5月1日截面：财务因子已披露，应保留原值"
