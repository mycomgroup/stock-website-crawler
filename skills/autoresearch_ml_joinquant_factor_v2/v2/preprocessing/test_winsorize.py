"""
Unit tests for winsorize_cross_section()

验收标准（需求 2.1）：
  - 基本 winsor 正确性
  - 超出边界的值被截断
  - 边界内的值保持不变
  - 按日截面操作（不同日期有不同边界）
  - 全 NaN 截面优雅处理
  - MAD=0（所有值相同）时不做截断
  - 不使用全局 clip（通过验证不同日期边界不同来确认）
"""

import numpy as np
import pandas as pd
import pytest

from skills.autoresearch_ml_joinquant_factor_v2.v2.preprocessing.factor_preprocessor import (
    winsorize_cross_section,
)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def make_df(dates, stock_ids, values, col="factor1"):
    """构造测试用 DataFrame。"""
    rows = []
    for date, stocks, vals in zip(dates, stock_ids, values):
        for sid, v in zip(stocks, vals):
            rows.append({"date": date, "stock_id": sid, col: v})
    return pd.DataFrame(rows)


# ---------------------------------------------------------------------------
# Test 1: 基本 winsor 正确性
# ---------------------------------------------------------------------------

class TestBasicWinsorization:
    def test_outlier_is_clipped(self):
        """极端值应被截断到 median ± 5*MAD。"""
        # 截面: [1, 2, 3, 4, 100]
        # median=3, MAD=median(|[1,2,3,4,100]-3|)=median([2,1,0,1,97])=1
        # upper = 3 + 5*1 = 8, lower = 3 - 5*1 = -2
        df = pd.DataFrame({
            "date": ["2020-01-01"] * 5,
            "stock_id": list("ABCDE"),
            "factor1": [1.0, 2.0, 3.0, 4.0, 100.0],
        })
        result = winsorize_cross_section(df, ["factor1"])
        assert result["factor1"].max() == pytest.approx(8.0), (
            "极端值 100 应被截断到 upper=8"
        )

    def test_lower_outlier_is_clipped(self):
        """下方极端值应被截断到 lower = median - 5*MAD。"""
        # 截面: [-100, 1, 2, 3, 4]
        # median=2, MAD=median([102,1,0,1,2])=1
        # lower = 2 - 5*1 = -3
        df = pd.DataFrame({
            "date": ["2020-01-01"] * 5,
            "stock_id": list("ABCDE"),
            "factor1": [-100.0, 1.0, 2.0, 3.0, 4.0],
        })
        result = winsorize_cross_section(df, ["factor1"])
        assert result["factor1"].min() == pytest.approx(-3.0), (
            "极端值 -100 应被截断到 lower=-3"
        )

    def test_returns_new_dataframe(self):
        """函数不应修改原始 DataFrame（返回副本）。"""
        df = pd.DataFrame({
            "date": ["2020-01-01"] * 3,
            "stock_id": list("ABC"),
            "factor1": [1.0, 2.0, 100.0],
        })
        original_values = df["factor1"].copy()
        _ = winsorize_cross_section(df, ["factor1"])
        pd.testing.assert_series_equal(df["factor1"], original_values)

    def test_non_factor_cols_unchanged(self):
        """非因子列（date、stock_id 等）不应被修改。"""
        df = pd.DataFrame({
            "date": ["2020-01-01"] * 3,
            "stock_id": list("ABC"),
            "factor1": [1.0, 2.0, 100.0],
            "label": [0.1, 0.2, 0.3],
        })
        result = winsorize_cross_section(df, ["factor1"])
        pd.testing.assert_series_equal(result["label"], df["label"])
        pd.testing.assert_series_equal(result["date"], df["date"])
        pd.testing.assert_series_equal(result["stock_id"], df["stock_id"])


# ---------------------------------------------------------------------------
# Test 2: 边界内的值保持不变
# ---------------------------------------------------------------------------

class TestValuesInsideBoundsUnchanged:
    def test_normal_values_unchanged(self):
        """在 median ± 5*MAD 范围内的值不应被修改。"""
        # 截面: [1, 2, 3, 4, 5]
        # median=3, MAD=median([2,1,0,1,2])=1
        # bounds: [-2, 8]，所有值都在范围内
        df = pd.DataFrame({
            "date": ["2020-01-01"] * 5,
            "stock_id": list("ABCDE"),
            "factor1": [1.0, 2.0, 3.0, 4.0, 5.0],
        })
        result = winsorize_cross_section(df, ["factor1"])
        pd.testing.assert_series_equal(
            result["factor1"].reset_index(drop=True),
            df["factor1"].reset_index(drop=True),
        )

    def test_boundary_values_unchanged(self):
        """恰好在边界上的值不应被修改（clip 是闭区间）。"""
        # median=3, MAD=1 → bounds=[-2, 8]
        # 添加恰好在边界上的值 8 和 -2
        df = pd.DataFrame({
            "date": ["2020-01-01"] * 7,
            "stock_id": list("ABCDEFG"),
            "factor1": [1.0, 2.0, 3.0, 4.0, 5.0, 8.0, -2.0],
        })
        result = winsorize_cross_section(df, ["factor1"])
        # 边界值 8 和 -2 应保持不变
        assert 8.0 in result["factor1"].values
        assert -2.0 in result["factor1"].values


# ---------------------------------------------------------------------------
# Test 3: 按日截面操作（不同日期有不同边界）
# ---------------------------------------------------------------------------

class TestPerDateOperation:
    def test_different_dates_have_different_bounds(self):
        """不同日期的截面应使用各自的 median 和 MAD，边界不同。"""
        # 日期1: [1, 2, 3, 4, 100] → median=3, MAD=1, upper=8
        # 日期2: [10, 20, 30, 40, 1000] → median=30, MAD=10, upper=80
        df = pd.DataFrame({
            "date": ["2020-01-01"] * 5 + ["2020-01-02"] * 5,
            "stock_id": list("ABCDE") * 2,
            "factor1": [1.0, 2.0, 3.0, 4.0, 100.0,
                        10.0, 20.0, 30.0, 40.0, 1000.0],
        })
        result = winsorize_cross_section(df, ["factor1"])

        date1_vals = result[result["date"] == "2020-01-01"]["factor1"]
        date2_vals = result[result["date"] == "2020-01-02"]["factor1"]

        # 日期1 的极端值 100 → 截断到 8
        assert date1_vals.max() == pytest.approx(8.0)
        # 日期2 的极端值 1000 → 截断到 80
        assert date2_vals.max() == pytest.approx(80.0)

    def test_global_clip_not_used(self):
        """验证不使用全局 clip：不同日期的上界应不同。"""
        # 如果使用全局 clip，两个日期的极端值会被截断到同一个值
        # 如果使用截面 clip，两个日期的极端值会被截断到不同的值
        df = pd.DataFrame({
            "date": ["2020-01-01"] * 5 + ["2020-01-02"] * 5,
            "stock_id": list("ABCDE") * 2,
            "factor1": [1.0, 2.0, 3.0, 4.0, 100.0,
                        10.0, 20.0, 30.0, 40.0, 1000.0],
        })
        result = winsorize_cross_section(df, ["factor1"])

        date1_max = result[result["date"] == "2020-01-01"]["factor1"].max()
        date2_max = result[result["date"] == "2020-01-02"]["factor1"].max()

        # 两个日期的上界不同，证明使用了截面统计而非全局统计
        assert date1_max != date2_max, (
            "不同日期的截断上界应不同，若相同则说明使用了全局 clip（违反需求 2.1）"
        )

    def test_each_date_uses_own_median(self):
        """每个日期使用自己截面的 median，而非全局 median。"""
        # 日期1 的 median=3，日期2 的 median=300
        # 如果使用全局 median，结果会不同
        df = pd.DataFrame({
            "date": ["2020-01-01"] * 5 + ["2020-01-02"] * 5,
            "stock_id": list("ABCDE") * 2,
            "factor1": [1.0, 2.0, 3.0, 4.0, 5.0,
                        100.0, 200.0, 300.0, 400.0, 500.0],
        })
        result = winsorize_cross_section(df, ["factor1"])

        # 日期1 的值都在 [-2, 8] 内，不应被截断
        date1_vals = result[result["date"] == "2020-01-01"]["factor1"].tolist()
        assert sorted(date1_vals) == pytest.approx([1.0, 2.0, 3.0, 4.0, 5.0])

        # 日期2 的值都在 [100, 500] 内，不应被截断
        date2_vals = result[result["date"] == "2020-01-02"]["factor1"].tolist()
        assert sorted(date2_vals) == pytest.approx([100.0, 200.0, 300.0, 400.0, 500.0])


# ---------------------------------------------------------------------------
# Test 4: 全 NaN 截面优雅处理
# ---------------------------------------------------------------------------

class TestAllNanCrossSection:
    def test_all_nan_cross_section_returns_nan(self):
        """全 NaN 截面应原样返回（不抛出异常，NaN 保持 NaN）。"""
        df = pd.DataFrame({
            "date": ["2020-01-01"] * 3,
            "stock_id": list("ABC"),
            "factor1": [np.nan, np.nan, np.nan],
        })
        result = winsorize_cross_section(df, ["factor1"])
        assert result["factor1"].isna().all(), "全 NaN 截面应保持全 NaN"

    def test_mixed_nan_and_valid(self):
        """含 NaN 的截面：NaN 保持 NaN，有效值正常 winsor。"""
        # 有效值: [1, 2, 3, 100]，NaN 1 个
        # median=2.5, MAD=median([1.5, 0.5, 0.5, 97.5])=1.0
        # upper = 2.5 + 5*1.0 = 7.5
        df = pd.DataFrame({
            "date": ["2020-01-01"] * 5,
            "stock_id": list("ABCDE"),
            "factor1": [1.0, 2.0, 3.0, 100.0, np.nan],
        })
        result = winsorize_cross_section(df, ["factor1"])

        # NaN 应保持 NaN
        nan_mask = df["factor1"].isna()
        assert result["factor1"][nan_mask].isna().all()

        # 极端值 100 应被截断
        assert result["factor1"].max() < 100.0

    def test_all_nan_multiple_dates(self):
        """多日期中某日全 NaN，其他日期正常处理。"""
        df = pd.DataFrame({
            "date": ["2020-01-01"] * 3 + ["2020-01-02"] * 3,
            "stock_id": list("ABC") * 2,
            "factor1": [np.nan, np.nan, np.nan, 1.0, 2.0, 100.0],
        })
        result = winsorize_cross_section(df, ["factor1"])

        # 日期1 全 NaN，保持不变
        date1_vals = result[result["date"] == "2020-01-01"]["factor1"]
        assert date1_vals.isna().all()

        # 日期2 正常 winsor
        date2_vals = result[result["date"] == "2020-01-02"]["factor1"]
        assert date2_vals.max() < 100.0


# ---------------------------------------------------------------------------
# Test 5: MAD=0 时不做截断
# ---------------------------------------------------------------------------

class TestMadZeroCase:
    def test_all_identical_values_unchanged(self):
        """当截面所有值相同（MAD=0）时，不做截断，值保持不变。"""
        df = pd.DataFrame({
            "date": ["2020-01-01"] * 5,
            "stock_id": list("ABCDE"),
            "factor1": [3.0, 3.0, 3.0, 3.0, 3.0],
        })
        result = winsorize_cross_section(df, ["factor1"])
        pd.testing.assert_series_equal(
            result["factor1"].reset_index(drop=True),
            df["factor1"].reset_index(drop=True),
        )

    def test_mad_zero_with_nan(self):
        """含 NaN 的截面，有效值全相同（MAD=0），有效值不变，NaN 保持 NaN。"""
        df = pd.DataFrame({
            "date": ["2020-01-01"] * 5,
            "stock_id": list("ABCDE"),
            "factor1": [5.0, 5.0, 5.0, 5.0, np.nan],
        })
        result = winsorize_cross_section(df, ["factor1"])

        # 有效值保持不变
        valid_mask = df["factor1"].notna()
        assert (result["factor1"][valid_mask] == 5.0).all()

        # NaN 保持 NaN
        assert result["factor1"].iloc[-1] != result["factor1"].iloc[-1]  # NaN != NaN


# ---------------------------------------------------------------------------
# Test 6: 多因子列同时处理
# ---------------------------------------------------------------------------

class TestMultipleFactorCols:
    def test_multiple_factors_processed_independently(self):
        """多个因子列应各自独立 winsor，互不影响。"""
        df = pd.DataFrame({
            "date": ["2020-01-01"] * 5,
            "stock_id": list("ABCDE"),
            "factor1": [1.0, 2.0, 3.0, 4.0, 100.0],
            "factor2": [10.0, 20.0, 30.0, 40.0, 1000.0],
        })
        result = winsorize_cross_section(df, ["factor1", "factor2"])

        # factor1: median=3, MAD=1, upper=8
        assert result["factor1"].max() == pytest.approx(8.0)

        # factor2: median=30, MAD=10, upper=80
        assert result["factor2"].max() == pytest.approx(80.0)

    def test_empty_factor_cols_returns_copy(self):
        """空因子列表应返回原始 DataFrame 的副本，不做任何修改。"""
        df = pd.DataFrame({
            "date": ["2020-01-01"] * 3,
            "stock_id": list("ABC"),
            "factor1": [1.0, 2.0, 100.0],
        })
        result = winsorize_cross_section(df, [])
        pd.testing.assert_frame_equal(result, df)


# ---------------------------------------------------------------------------
# Test 7: 自定义 mad_multiplier
# ---------------------------------------------------------------------------

class TestCustomMadMultiplier:
    def test_custom_multiplier_3(self):
        """使用 mad_multiplier=3 时，截断范围更窄。"""
        # 截面: [1, 2, 3, 4, 100]
        # median=3, MAD=1
        # mad_multiplier=3: upper = 3 + 3*1 = 6
        # mad_multiplier=5: upper = 3 + 5*1 = 8
        df = pd.DataFrame({
            "date": ["2020-01-01"] * 5,
            "stock_id": list("ABCDE"),
            "factor1": [1.0, 2.0, 3.0, 4.0, 100.0],
        })
        result_3 = winsorize_cross_section(df, ["factor1"], mad_multiplier=3.0)
        result_5 = winsorize_cross_section(df, ["factor1"], mad_multiplier=5.0)

        assert result_3["factor1"].max() == pytest.approx(6.0)
        assert result_5["factor1"].max() == pytest.approx(8.0)
        # multiplier=3 的上界更窄
        assert result_3["factor1"].max() < result_5["factor1"].max()


# ---------------------------------------------------------------------------
# Test 8: 错误处理
# ---------------------------------------------------------------------------

class TestErrorHandling:
    def test_missing_date_column_raises(self):
        """缺少 date 列时应抛出 ValueError。"""
        df = pd.DataFrame({
            "stock_id": list("ABC"),
            "factor1": [1.0, 2.0, 3.0],
        })
        with pytest.raises(ValueError, match="date"):
            winsorize_cross_section(df, ["factor1"])

    def test_missing_factor_col_raises(self):
        """指定的因子列不存在时应抛出 ValueError。"""
        df = pd.DataFrame({
            "date": ["2020-01-01"] * 3,
            "stock_id": list("ABC"),
            "factor1": [1.0, 2.0, 3.0],
        })
        with pytest.raises(ValueError):
            winsorize_cross_section(df, ["nonexistent_factor"])


# ---------------------------------------------------------------------------
# Test 9: 单值截面（只有一只股票）
# ---------------------------------------------------------------------------

class TestSingleValueCrossSection:
    def test_single_stock_per_date(self):
        """每个日期只有一只股票时，MAD=0，值不变。"""
        df = pd.DataFrame({
            "date": ["2020-01-01", "2020-01-02"],
            "stock_id": ["A", "B"],
            "factor1": [5.0, 10.0],
        })
        result = winsorize_cross_section(df, ["factor1"])
        pd.testing.assert_series_equal(
            result["factor1"].reset_index(drop=True),
            df["factor1"].reset_index(drop=True),
        )
