"""
Unit tests for impute_factors() — task 2.2

覆盖以下验收标准：
  1. 财务类因子（basics/quality/growth/pershare）用行业内中位数填补
  2. 微观结构类因子（emotion/technical）用前推（forward fill）
  3. 缺失率 > 30% 的因子降权（weight=0.5），否则 weight=1.0
  4. 禁止对所有因子统一 fillna(0)
  5. 预处理后缺失率不高于预处理前（单调性约束）
"""

from __future__ import annotations

import numpy as np
import pandas as pd
import pytest

from skills.autoresearch_ml_joinquant_factor_v2.v2.preprocessing.factor_preprocessor import (
    impute_factors,
)


# ---------------------------------------------------------------------------
# 辅助构造函数
# ---------------------------------------------------------------------------

def make_panel(
    dates: list[str],
    stocks: list[str],
    factor_values: dict[str, list[float]],
    industry_values: list[str] | None = None,
) -> pd.DataFrame:
    """构造简单面板 DataFrame，行顺序为 (date, stock) 笛卡尔积。"""
    rows = [(d, s) for d in dates for s in stocks]
    df = pd.DataFrame(rows, columns=["date", "stock_id"])
    for col, vals in factor_values.items():
        df[col] = vals
    if industry_values is not None:
        df["industry"] = industry_values
    return df


# ---------------------------------------------------------------------------
# 1. 财务类因子：行业内中位数填补
# ---------------------------------------------------------------------------

class TestFinancialImputation:
    """财务类因子（quality/basics/growth/pershare）的行业内中位数填补。"""

    def test_nan_filled_by_industry_median(self):
        """同行业内的 NaN 应被该行业的中位数填补。"""
        df = pd.DataFrame({
            "date": ["2020-01-01"] * 4,
            "stock_id": ["A", "B", "C", "D"],
            "industry": ["tech", "tech", "fin", "fin"],
            "roe": [0.1, np.nan, 0.2, 0.4],
        })
        df_out, weights = impute_factors(
            df, ["roe"], factor_family_map={"roe": "quality"}
        )
        # tech 行业中位数 = 0.1（只有 A 有值），B 应被填为 0.1
        assert df_out.loc[df_out["stock_id"] == "B", "roe"].iloc[0] == pytest.approx(0.1)
        # fin 行业中位数 = median([0.2, 0.4]) = 0.3，无 NaN，不变
        assert df_out.loc[df_out["stock_id"] == "C", "roe"].iloc[0] == pytest.approx(0.2)
        assert df_out.loc[df_out["stock_id"] == "D", "roe"].iloc[0] == pytest.approx(0.4)

    def test_industry_median_uses_cross_section_per_date(self):
        """行业中位数应按日期截面独立计算，不跨日期混用。"""
        df = pd.DataFrame({
            "date": ["2020-01-01", "2020-01-01", "2020-01-08", "2020-01-08"],
            "stock_id": ["A", "B", "A", "B"],
            "industry": ["tech", "tech", "tech", "tech"],
            "roe": [0.1, np.nan, 0.5, np.nan],
        })
        df_out, _ = impute_factors(
            df, ["roe"], factor_family_map={"roe": "quality"}
        )
        # 2020-01-01：tech 中位数 = 0.1，B 填为 0.1
        b_jan1 = df_out[(df_out["stock_id"] == "B") & (df_out["date"] == "2020-01-01")]["roe"].iloc[0]
        assert b_jan1 == pytest.approx(0.1)
        # 2020-01-08：tech 中位数 = 0.5，B 填为 0.5
        b_jan8 = df_out[(df_out["stock_id"] == "B") & (df_out["date"] == "2020-01-08")]["roe"].iloc[0]
        assert b_jan8 == pytest.approx(0.5)

    def test_fallback_to_cross_section_median_when_no_industry_col(self):
        """无 industry 列时，财务类因子退化为截面中位数填补。"""
        df = pd.DataFrame({
            "date": ["2020-01-01"] * 4,
            "stock_id": ["A", "B", "C", "D"],
            "roe": [0.1, 0.3, np.nan, 0.5],
        })
        df_out, _ = impute_factors(
            df, ["roe"], factor_family_map={"roe": "quality"}
        )
        # 截面中位数 = median([0.1, 0.3, 0.5]) = 0.3
        assert df_out.loc[df_out["stock_id"] == "C", "roe"].iloc[0] == pytest.approx(0.3)

    def test_remaining_nan_filled_by_cross_section_median(self):
        """行业内全为 NaN 时，应退化为截面中位数填补（不留 NaN）。"""
        df = pd.DataFrame({
            "date": ["2020-01-01"] * 4,
            "stock_id": ["A", "B", "C", "D"],
            "industry": ["tech", "tech", "fin", "fin"],
            "roe": [np.nan, np.nan, 0.2, 0.4],
        })
        df_out, _ = impute_factors(
            df, ["roe"], factor_family_map={"roe": "quality"}
        )
        # tech 行业全 NaN，退化为截面中位数 = median([0.2, 0.4]) = 0.3
        assert df_out.loc[df_out["stock_id"] == "A", "roe"].iloc[0] == pytest.approx(0.3)
        assert df_out.loc[df_out["stock_id"] == "B", "roe"].iloc[0] == pytest.approx(0.3)

    def test_all_financial_families_treated_as_financial(self):
        """basics/quality/growth/pershare 均应走行业中位数路径。"""
        for family in ["basics", "quality", "growth", "pershare"]:
            df = pd.DataFrame({
                "date": ["2020-01-01"] * 3,
                "stock_id": ["A", "B", "C"],
                "industry": ["tech", "tech", "tech"],
                "f": [1.0, np.nan, 3.0],
            })
            df_out, _ = impute_factors(
                df, ["f"], factor_family_map={"f": family}
            )
            # tech 中位数 = median([1.0, 3.0]) = 2.0
            assert df_out.loc[df_out["stock_id"] == "B", "f"].iloc[0] == pytest.approx(2.0), \
                f"family={family} 未正确走行业中位数路径"

    def test_no_fillna_zero_for_financial(self):
        """财务类因子填补后不应出现 0.0 替代 NaN（除非中位数本身为 0）。"""
        df = pd.DataFrame({
            "date": ["2020-01-01"] * 3,
            "stock_id": ["A", "B", "C"],
            "industry": ["tech", "tech", "tech"],
            "roe": [0.1, np.nan, 0.3],
        })
        df_out, _ = impute_factors(
            df, ["roe"], factor_family_map={"roe": "quality"}
        )
        # 中位数 = 0.2，不应为 0
        filled_val = df_out.loc[df_out["stock_id"] == "B", "roe"].iloc[0]
        assert filled_val != 0.0
        assert filled_val == pytest.approx(0.2)


# ---------------------------------------------------------------------------
# 2. 微观结构类因子：前推（forward fill）
# ---------------------------------------------------------------------------

class TestMicrostructureImputation:
    """微观结构类因子（emotion/technical）的前推填补。"""

    def test_forward_fill_per_stock(self):
        """每只股票的 NaN 应被该股票最近的历史值前推填补。"""
        df = pd.DataFrame({
            "date": ["2020-01-01", "2020-01-08", "2020-01-15"] * 2,
            "stock_id": ["A", "A", "A", "B", "B", "B"],
            "rsi": [50.0, np.nan, np.nan, 60.0, np.nan, 70.0],
        })
        df_out, _ = impute_factors(
            df, ["rsi"], factor_family_map={"rsi": "technical"}
        )
        # A：50 → 50（前推）→ 50（前推）
        a_vals = df_out[df_out["stock_id"] == "A"].sort_values("date")["rsi"].tolist()
        assert a_vals == pytest.approx([50.0, 50.0, 50.0])
        # B：60 → 60（前推）→ 70
        b_vals = df_out[df_out["stock_id"] == "B"].sort_values("date")["rsi"].tolist()
        assert b_vals == pytest.approx([60.0, 60.0, 70.0])

    def test_forward_fill_does_not_backfill(self):
        """前推不应回填：股票第一个时间点的 NaN 应保持 NaN。"""
        df = pd.DataFrame({
            "date": ["2020-01-01", "2020-01-08"],
            "stock_id": ["A", "A"],
            "rsi": [np.nan, 55.0],
        })
        df_out, _ = impute_factors(
            df, ["rsi"], factor_family_map={"rsi": "technical"}
        )
        # 第一个时间点无历史值，应保持 NaN
        first_val = df_out[df_out["date"] == "2020-01-01"]["rsi"].iloc[0]
        assert np.isnan(first_val)
        # 第二个时间点有值，不变
        second_val = df_out[df_out["date"] == "2020-01-08"]["rsi"].iloc[0]
        assert second_val == pytest.approx(55.0)

    def test_forward_fill_independent_per_stock(self):
        """不同股票的前推应相互独立，不跨股票传播。"""
        df = pd.DataFrame({
            "date": ["2020-01-01", "2020-01-08"] * 2,
            "stock_id": ["A", "A", "B", "B"],
            "macd": [10.0, np.nan, np.nan, 20.0],
        })
        df_out, _ = impute_factors(
            df, ["macd"], factor_family_map={"macd": "emotion"}
        )
        # A：10 → 10（前推）
        a_jan8 = df_out[(df_out["stock_id"] == "A") & (df_out["date"] == "2020-01-08")]["macd"].iloc[0]
        assert a_jan8 == pytest.approx(10.0)
        # B：NaN（无历史值）→ NaN
        b_jan1 = df_out[(df_out["stock_id"] == "B") & (df_out["date"] == "2020-01-01")]["macd"].iloc[0]
        assert np.isnan(b_jan1)

    def test_all_microstructure_families_treated_as_microstructure(self):
        """emotion/technical 均应走前推路径，而非行业中位数。"""
        for family in ["emotion", "technical"]:
            df = pd.DataFrame({
                "date": ["2020-01-01", "2020-01-08"],
                "stock_id": ["A", "A"],
                "industry": ["tech", "tech"],
                "f": [42.0, np.nan],
            })
            df_out, _ = impute_factors(
                df, ["f"], factor_family_map={"f": family}
            )
            # 前推：第二行应为 42.0（不是行业中位数）
            val = df_out[df_out["date"] == "2020-01-08"]["f"].iloc[0]
            assert val == pytest.approx(42.0), \
                f"family={family} 未正确走前推路径"


# ---------------------------------------------------------------------------
# 3. 缺失率阈值与权重
# ---------------------------------------------------------------------------

class TestMissingRateWeights:
    """缺失率 > 30% 时降权（0.5），否则权重为 1.0。"""

    def test_weight_1_when_missing_rate_below_threshold(self):
        """缺失率 ≤ 30% 时权重应为 1.0。"""
        # 4 行，1 个 NaN → 缺失率 25%
        df = pd.DataFrame({
            "date": ["2020-01-01"] * 4,
            "stock_id": ["A", "B", "C", "D"],
            "roe": [0.1, 0.2, np.nan, 0.4],
        })
        _, weights = impute_factors(df, ["roe"], factor_family_map={"roe": "quality"})
        assert weights["roe"] == 1.0

    def test_weight_05_when_missing_rate_above_threshold(self):
        """缺失率 > 30% 时权重应为 0.5。"""
        # 4 行，2 个 NaN → 缺失率 50%（填补前计算）
        # 注意：权重基于填补后的缺失率
        # 构造填补后仍有 NaN 的情况：全截面 NaN，无法填补
        df = pd.DataFrame({
            "date": ["2020-01-01"] * 4,
            "stock_id": ["A", "B", "C", "D"],
            "rsi": [np.nan, np.nan, np.nan, np.nan],  # 全 NaN，前推无法填补
        })
        _, weights = impute_factors(df, ["rsi"], factor_family_map={"rsi": "technical"})
        assert weights["rsi"] == 0.5

    def test_weight_threshold_boundary(self):
        """恰好等于阈值（30%）时权重应为 1.0（不超过阈值）。"""
        # 10 行，3 个 NaN → 缺失率 30%（不超过）
        # 但填补后可能为 0，取决于实现；这里构造填补后仍有 NaN 的情况
        # 使用微观结构因子，首个时间点 NaN 无法前推
        dates = ["2020-01-01", "2020-01-08", "2020-01-15",
                 "2020-01-22", "2020-01-29", "2020-02-05",
                 "2020-02-12", "2020-02-19", "2020-02-26", "2020-03-04"]
        df = pd.DataFrame({
            "date": dates,
            "stock_id": ["A"] * 10,
            "rsi": [np.nan, np.nan, np.nan, 50.0, 51.0, 52.0, 53.0, 54.0, 55.0, 56.0],
        })
        # 前推后：前3个仍为 NaN（无历史值），缺失率 = 3/10 = 30%
        _, weights = impute_factors(df, ["rsi"], factor_family_map={"rsi": "technical"})
        assert weights["rsi"] == 1.0  # 30% 不超过阈值

    def test_custom_threshold(self):
        """自定义阈值应被正确使用。"""
        df = pd.DataFrame({
            "date": ["2020-01-01"] * 5,
            "stock_id": ["A", "B", "C", "D", "E"],
            "rsi": [np.nan, np.nan, np.nan, np.nan, np.nan],  # 全 NaN
        })
        # 阈值设为 0.5，缺失率 100% > 50%，应降权
        _, weights = impute_factors(
            df, ["rsi"],
            factor_family_map={"rsi": "technical"},
            missing_rate_threshold=0.5,
        )
        assert weights["rsi"] == 0.5

    def test_weights_returned_for_all_factor_cols(self):
        """返回的权重字典应包含所有 factor_cols 中的因子。"""
        df = pd.DataFrame({
            "date": ["2020-01-01"] * 3,
            "stock_id": ["A", "B", "C"],
            "roe": [0.1, 0.2, 0.3],
            "rsi": [50.0, 60.0, 70.0],
        })
        _, weights = impute_factors(
            df, ["roe", "rsi"],
            factor_family_map={"roe": "quality", "rsi": "technical"},
        )
        assert set(weights.keys()) == {"roe", "rsi"}


# ---------------------------------------------------------------------------
# 4. 单调性约束：填补后缺失率 ≤ 填补前缺失率
# ---------------------------------------------------------------------------

class TestMonotonicity:
    """预处理后缺失率不高于预处理前（单调性约束）。"""

    def test_missing_rate_non_increasing_financial(self):
        """财务类因子填补后缺失率应 ≤ 填补前缺失率。"""
        df = pd.DataFrame({
            "date": ["2020-01-01"] * 6,
            "stock_id": ["A", "B", "C", "D", "E", "F"],
            "industry": ["tech", "tech", "tech", "fin", "fin", "fin"],
            "roe": [0.1, np.nan, 0.3, np.nan, 0.5, 0.6],
        })
        missing_before = df["roe"].isna().mean()
        df_out, _ = impute_factors(df, ["roe"], factor_family_map={"roe": "quality"})
        missing_after = df_out["roe"].isna().mean()
        assert missing_after <= missing_before

    def test_missing_rate_non_increasing_microstructure(self):
        """微观结构类因子填补后缺失率应 ≤ 填补前缺失率。"""
        df = pd.DataFrame({
            "date": ["2020-01-01", "2020-01-08", "2020-01-15"] * 2,
            "stock_id": ["A", "A", "A", "B", "B", "B"],
            "rsi": [50.0, np.nan, np.nan, np.nan, 60.0, np.nan],
        })
        missing_before = df["rsi"].isna().mean()
        df_out, _ = impute_factors(df, ["rsi"], factor_family_map={"rsi": "technical"})
        missing_after = df_out["rsi"].isna().mean()
        assert missing_after <= missing_before

    def test_no_new_nans_introduced(self):
        """填补操作不应引入新的 NaN（原本有值的位置不应变为 NaN）。"""
        df = pd.DataFrame({
            "date": ["2020-01-01"] * 4,
            "stock_id": ["A", "B", "C", "D"],
            "industry": ["tech", "tech", "fin", "fin"],
            "roe": [0.1, 0.2, 0.3, 0.4],
        })
        df_out, _ = impute_factors(df, ["roe"], factor_family_map={"roe": "quality"})
        assert df_out["roe"].isna().sum() == 0


# ---------------------------------------------------------------------------
# 5. 未知家族保守处理
# ---------------------------------------------------------------------------

class TestUnknownFamily:
    """未知家族应保守处理为财务类（行业中位数填补）。"""

    def test_unknown_family_treated_as_financial(self):
        """factor_family_map 中不存在的因子应走财务类路径。"""
        df = pd.DataFrame({
            "date": ["2020-01-01"] * 3,
            "stock_id": ["A", "B", "C"],
            "industry": ["tech", "tech", "tech"],
            "mystery_factor": [1.0, np.nan, 3.0],
        })
        df_out, _ = impute_factors(
            df, ["mystery_factor"],
            factor_family_map={"mystery_factor": "unknown_family"},
        )
        # 应走行业中位数路径：tech 中位数 = median([1.0, 3.0]) = 2.0
        filled = df_out.loc[df_out["stock_id"] == "B", "mystery_factor"].iloc[0]
        assert filled == pytest.approx(2.0)

    def test_none_family_map_treated_as_financial(self):
        """factor_family_map=None 时所有因子应走财务类路径。"""
        df = pd.DataFrame({
            "date": ["2020-01-01"] * 3,
            "stock_id": ["A", "B", "C"],
            "industry": ["tech", "tech", "tech"],
            "f": [10.0, np.nan, 30.0],
        })
        df_out, _ = impute_factors(df, ["f"], factor_family_map=None)
        filled = df_out.loc[df_out["stock_id"] == "B", "f"].iloc[0]
        assert filled == pytest.approx(20.0)


# ---------------------------------------------------------------------------
# 6. 边界情况与鲁棒性
# ---------------------------------------------------------------------------

class TestEdgeCases:
    """边界情况与鲁棒性测试。"""

    def test_empty_factor_cols_returns_copy(self):
        """factor_cols 为空时应返回 df 副本和空权重字典。"""
        df = pd.DataFrame({
            "date": ["2020-01-01"],
            "stock_id": ["A"],
            "roe": [0.1],
        })
        df_out, weights = impute_factors(df, [])
        assert weights == {}
        pd.testing.assert_frame_equal(df_out, df)

    def test_no_nans_unchanged(self):
        """无 NaN 的因子列应保持不变。"""
        df = pd.DataFrame({
            "date": ["2020-01-01"] * 3,
            "stock_id": ["A", "B", "C"],
            "industry": ["tech", "tech", "fin"],
            "roe": [0.1, 0.2, 0.3],
        })
        df_out, weights = impute_factors(df, ["roe"], factor_family_map={"roe": "quality"})
        pd.testing.assert_series_equal(df_out["roe"], df["roe"])
        assert weights["roe"] == 1.0

    def test_original_df_not_modified(self):
        """函数不应修改原始 DataFrame（返回副本）。"""
        df = pd.DataFrame({
            "date": ["2020-01-01"] * 3,
            "stock_id": ["A", "B", "C"],
            "industry": ["tech", "tech", "tech"],
            "roe": [0.1, np.nan, 0.3],
        })
        original_roe = df["roe"].copy()
        impute_factors(df, ["roe"], factor_family_map={"roe": "quality"})
        pd.testing.assert_series_equal(df["roe"], original_roe)

    def test_missing_required_column_raises(self):
        """缺少 date 或 stock_id 列时应抛出 ValueError。"""
        df = pd.DataFrame({"stock_id": ["A"], "roe": [0.1]})
        with pytest.raises(ValueError, match="date"):
            impute_factors(df, ["roe"])

    def test_missing_factor_column_raises(self):
        """factor_cols 中包含不存在的列时应抛出 ValueError。"""
        df = pd.DataFrame({
            "date": ["2020-01-01"],
            "stock_id": ["A"],
            "roe": [0.1],
        })
        with pytest.raises(ValueError):
            impute_factors(df, ["nonexistent_factor"])

    def test_mixed_financial_and_microstructure(self):
        """同时含财务类和微观结构类因子时，两者应分别走各自路径。"""
        df = pd.DataFrame({
            "date": ["2020-01-01", "2020-01-08"] * 2,
            "stock_id": ["A", "A", "B", "B"],
            "industry": ["tech", "tech", "tech", "tech"],
            "roe": [0.1, np.nan, np.nan, 0.3],   # 财务类
            "rsi": [50.0, np.nan, np.nan, 60.0],  # 微观结构类
        })
        df_out, weights = impute_factors(
            df, ["roe", "rsi"],
            factor_family_map={"roe": "quality", "rsi": "technical"},
        )
        # roe（财务类）：截面中位数填补
        # 2020-01-01：A=0.1, B=NaN → 截面中位数=0.1，B填为0.1
        b_roe_jan1 = df_out[(df_out["stock_id"] == "B") & (df_out["date"] == "2020-01-01")]["roe"].iloc[0]
        assert b_roe_jan1 == pytest.approx(0.1)

        # rsi（微观结构类）：前推
        # A：2020-01-01=50.0，2020-01-08=NaN → 前推为 50.0
        a_rsi_jan8 = df_out[(df_out["stock_id"] == "A") & (df_out["date"] == "2020-01-08")]["rsi"].iloc[0]
        assert a_rsi_jan8 == pytest.approx(50.0)

        assert set(weights.keys()) == {"roe", "rsi"}

    def test_return_type_is_tuple(self):
        """函数应返回 (DataFrame, dict) 元组。"""
        df = pd.DataFrame({
            "date": ["2020-01-01"],
            "stock_id": ["A"],
            "roe": [0.1],
        })
        result = impute_factors(df, ["roe"])
        assert isinstance(result, tuple)
        assert len(result) == 2
        assert isinstance(result[0], pd.DataFrame)
        assert isinstance(result[1], dict)
