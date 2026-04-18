"""PBT 测试 P5 及 L2 因子家族模块单元测试

**Validates: Requirements 3.1, 3.2, 3.3, 3.4, 3.5**

测试覆盖：
- P5: 家族完备性（union(families) == set(all_factors)，无重叠，无遗漏）
- 有效维度计算正确性
- 冗余因子对检测
- 因子准入/淘汰三段式流程
- validate_family_map() 通过

测试框架：hypothesis（PBT）+ pytest（单元测试）
"""

from __future__ import annotations

import numpy as np
import pandas as pd
import pytest
from hypothesis import given, settings
from hypothesis import strategies as st

from skills.autoresearch_ml_joinquant_factor_v2.v2.family.family_map import (
    ALL_FACTORS,
    FACTOR_TO_FAMILY,
    FAMILY_DECAY_SPEED,
    FAMILY_MAP,
    get_factor_family,
    get_family_factors,
    validate_family_map,
)
from skills.autoresearch_ml_joinquant_factor_v2.v2.family.redundancy import (
    FactorAdmissionManager,
    compute_effective_dimension,
    compute_family_effective_dimensions,
    detect_redundant_pairs,
)


# ===========================================================================
# PBT 测试 P5：家族完备性
# **Validates: Requirements 3.5**
# ===========================================================================


class TestP5FamilyCompleteness:
    """PBT 测试 P5：家族完备性验证。

    **Validates: Requirements 3.5**

    验证：
    - union(family_map.values()) == set(all_factors)
    - 无重叠（每个因子恰好属于一个家族）
    - 无遗漏（所有因子都在某个家族中）
    """

    def test_union_of_families_equals_all_factors(self) -> None:
        """P5: union(families) == set(all_factors)。

        **Validates: Requirements 3.5**
        """
        union_of_families = set()
        for factors in FAMILY_MAP.values():
            union_of_families.update(factors)

        all_factors_set = set(ALL_FACTORS)
        assert union_of_families == all_factors_set, (
            f"家族并集与 ALL_FACTORS 不一致。"
            f"仅在家族中: {union_of_families - all_factors_set}，"
            f"仅在 ALL_FACTORS 中: {all_factors_set - union_of_families}"
        )

    def test_no_overlaps_between_families(self) -> None:
        """P5: 无重叠——每个因子恰好属于一个家族。

        **Validates: Requirements 3.5**
        """
        seen: dict[str, str] = {}
        overlaps: list[str] = []

        for family, factors in FAMILY_MAP.items():
            for factor in factors:
                if factor in seen:
                    overlaps.append(f"{factor} (in {seen[factor]} and {family})")
                else:
                    seen[factor] = family

        assert len(overlaps) == 0, (
            f"发现 {len(overlaps)} 个重叠因子: {overlaps}"
        )

    def test_no_omissions_all_factors_in_some_family(self) -> None:
        """P5: 无遗漏——ALL_FACTORS 中的每个因子都在某个家族中。

        **Validates: Requirements 3.5**
        """
        all_family_factors = set(
            factor
            for factors in FAMILY_MAP.values()
            for factor in factors
        )
        for factor in ALL_FACTORS:
            assert factor in all_family_factors, (
                f"因子 '{factor}' 在 ALL_FACTORS 中但不属于任何家族"
            )

    @given(st.sampled_from(list(FAMILY_MAP.keys())))
    @settings(max_examples=9, deadline=5000)
    def test_pbt_each_family_factor_has_reverse_mapping(self, family: str) -> None:
        """P5 PBT: 每个家族的每个因子都有正确的反向映射。

        **Validates: Requirements 3.5**
        """
        for factor in FAMILY_MAP[family]:
            assert factor in FACTOR_TO_FAMILY, (
                f"因子 '{factor}' 在家族 '{family}' 中，但不在 FACTOR_TO_FAMILY 中"
            )
            assert FACTOR_TO_FAMILY[factor] == family, (
                f"因子 '{factor}' 的反向映射为 '{FACTOR_TO_FAMILY[factor]}'，"
                f"期望 '{family}'"
            )

    @given(st.sampled_from(ALL_FACTORS))
    @settings(max_examples=50, deadline=5000)
    def test_pbt_every_factor_belongs_to_exactly_one_family(
        self, factor: str
    ) -> None:
        """P5 PBT: 每个因子恰好属于一个家族。

        **Validates: Requirements 3.5**
        """
        families_containing_factor = [
            family
            for family, factors in FAMILY_MAP.items()
            if factor in factors
        ]
        assert len(families_containing_factor) == 1, (
            f"因子 '{factor}' 属于 {len(families_containing_factor)} 个家族: "
            f"{families_containing_factor}（应恰好属于 1 个）"
        )


# ===========================================================================
# 家族映射基础测试
# **Validates: Requirements 3.1**
# ===========================================================================


class TestFamilyMapBasics:
    """家族映射基础测试。

    **Validates: Requirements 3.1**
    """

    def test_total_factor_count_is_260(self) -> None:
        """因子总数应为 260。

        **Validates: Requirements 3.1**
        """
        assert len(ALL_FACTORS) == 260, (
            f"因子总数应为 260，实际为 {len(ALL_FACTORS)}"
        )

    def test_basics_family_has_37_factors(self) -> None:
        """basics 家族应有 37 个因子。

        **Validates: Requirements 3.1**
        """
        assert len(FAMILY_MAP["basics"]) == 37, (
            f"basics 家族应有 37 个因子，实际有 {len(FAMILY_MAP['basics'])}"
        )

    def test_quality_family_has_71_factors(self) -> None:
        """quality 家族应有 71 个因子。

        **Validates: Requirements 3.1**
        """
        assert len(FAMILY_MAP["quality"]) == 71, (
            f"quality 家族应有 71 个因子，实际有 {len(FAMILY_MAP['quality'])}"
        )

    def test_nine_families_exist(self) -> None:
        """应有 9 个经济家族。

        **Validates: Requirements 3.1**
        """
        expected_families = {
            "basics", "emotion", "growth", "momentum", "pershare",
            "quality", "risk", "style", "technical",
        }
        assert set(FAMILY_MAP.keys()) == expected_families, (
            f"家族集合不符：期望 {expected_families}，实际 {set(FAMILY_MAP.keys())}"
        )

    def test_family_sizes_match_spec(self) -> None:
        """各家族因子数量应符合规格。

        **Validates: Requirements 3.1**
        """
        expected = {
            "basics": 37,
            "emotion": 36,
            "growth": 9,
            "momentum": 34,
            "pershare": 15,
            "quality": 71,
            "risk": 12,
            "style": 30,
            "technical": 16,
        }
        for family, expected_count in expected.items():
            actual = len(FAMILY_MAP[family])
            assert actual == expected_count, (
                f"家族 '{family}' 因子数量不符：期望 {expected_count}，实际 {actual}"
            )

    def test_validate_family_map_passes(self) -> None:
        """validate_family_map() 应通过所有检查。

        **Validates: Requirements 3.1**
        """
        result = validate_family_map()
        assert result["valid"], (
            f"validate_family_map() 验证失败，错误: {result['errors']}"
        )
        assert result["total_factors"] == 260
        assert len(result["overlaps"]) == 0

    def test_get_family_factors_returns_correct_list(self) -> None:
        """get_family_factors() 应返回正确的因子列表。

        **Validates: Requirements 3.1**
        """
        growth_factors = get_family_factors("growth")
        assert "eps_growth" in growth_factors
        assert "net_profit_growth_rate" in growth_factors
        assert len(growth_factors) == 9

    def test_get_family_factors_raises_for_unknown_family(self) -> None:
        """get_family_factors() 对未知家族应抛出 KeyError。

        **Validates: Requirements 3.1**
        """
        with pytest.raises(KeyError):
            get_family_factors("nonexistent_family")

    def test_get_factor_family_returns_correct_family(self) -> None:
        """get_factor_family() 应返回正确的家族名称。

        **Validates: Requirements 3.1**
        """
        assert get_factor_family("MACD") == "emotion"
        assert get_factor_family("eps_growth") == "growth"
        assert get_factor_family("RSI14") == "technical"
        assert get_factor_family("market_cap") == "basics"
        assert get_factor_family("gross_profit_margin") == "quality"

    def test_get_factor_family_raises_for_unknown_factor(self) -> None:
        """get_factor_family() 对未知因子应抛出 KeyError。

        **Validates: Requirements 3.1**
        """
        with pytest.raises(KeyError):
            get_factor_family("nonexistent_factor_xyz")

    def test_family_decay_speed_covers_all_families(self) -> None:
        """FAMILY_DECAY_SPEED 应覆盖所有 9 个家族。

        **Validates: Requirements 3.1**
        """
        assert set(FAMILY_DECAY_SPEED.keys()) == set(FAMILY_MAP.keys())
        for family, speed in FAMILY_DECAY_SPEED.items():
            assert speed in ("fast", "medium", "slow"), (
                f"家族 '{family}' 的衰减速度 '{speed}' 无效"
            )

    def test_all_factors_list_has_no_duplicates(self) -> None:
        """ALL_FACTORS 中不应有重复因子。

        **Validates: Requirements 3.1**
        """
        assert len(ALL_FACTORS) == len(set(ALL_FACTORS)), (
            f"ALL_FACTORS 中有重复因子，总数 {len(ALL_FACTORS)}，"
            f"去重后 {len(set(ALL_FACTORS))}"
        )


# ===========================================================================
# 有效维度计算测试
# **Validates: Requirements 3.2**
# ===========================================================================


class TestEffectiveDimension:
    """有效维度计算测试。

    **Validates: Requirements 3.2**
    """

    def test_identity_matrix_gives_full_dimension(self) -> None:
        """单位矩阵（完全独立因子）的有效维度应等于因子数。

        **Validates: Requirements 3.2**
        """
        n = 5
        corr = np.eye(n)
        n_eff = compute_effective_dimension(corr)
        assert abs(n_eff - n) < 1e-6, (
            f"单位矩阵的有效维度应为 {n}，实际为 {n_eff:.6f}"
        )

    def test_all_ones_matrix_gives_dimension_one(self) -> None:
        """全 1 矩阵（完全共线因子）的有效维度应接近 1。

        **Validates: Requirements 3.2**
        """
        n = 5
        corr = np.ones((n, n))
        n_eff = compute_effective_dimension(corr)
        assert abs(n_eff - 1.0) < 1e-6, (
            f"全 1 矩阵的有效维度应为 1，实际为 {n_eff:.6f}"
        )

    def test_effective_dimension_bounded_by_matrix_size(self) -> None:
        """有效维度应在 [1, K] 范围内。

        **Validates: Requirements 3.2**
        """
        rng = np.random.default_rng(42)
        n = 10
        # 生成随机正定相关矩阵
        A = rng.standard_normal((n, n))
        corr = np.corrcoef(A)
        n_eff = compute_effective_dimension(corr)
        assert 1.0 <= n_eff <= n + 1e-6, (
            f"有效维度 {n_eff:.4f} 超出范围 [1, {n}]"
        )

    def test_effective_dimension_decreases_with_correlation(self) -> None:
        """相关性越高，有效维度越低。

        **Validates: Requirements 3.2**
        """
        n = 4
        # 低相关矩阵
        low_corr = np.array([
            [1.0, 0.1, 0.1, 0.1],
            [0.1, 1.0, 0.1, 0.1],
            [0.1, 0.1, 1.0, 0.1],
            [0.1, 0.1, 0.1, 1.0],
        ])
        # 高相关矩阵
        high_corr = np.array([
            [1.0, 0.9, 0.9, 0.9],
            [0.9, 1.0, 0.9, 0.9],
            [0.9, 0.9, 1.0, 0.9],
            [0.9, 0.9, 0.9, 1.0],
        ])
        n_eff_low = compute_effective_dimension(low_corr)
        n_eff_high = compute_effective_dimension(high_corr)
        assert n_eff_low > n_eff_high, (
            f"低相关矩阵有效维度 ({n_eff_low:.4f}) 应大于高相关矩阵 ({n_eff_high:.4f})"
        )

    def test_effective_dimension_raises_for_non_square(self) -> None:
        """非方阵应抛出 ValueError。

        **Validates: Requirements 3.2**
        """
        with pytest.raises(ValueError):
            compute_effective_dimension(np.ones((3, 4)))

    def test_effective_dimension_raises_for_nan(self) -> None:
        """含 NaN 的矩阵应抛出 ValueError。

        **Validates: Requirements 3.2**
        """
        corr = np.eye(3)
        corr[0, 1] = np.nan
        with pytest.raises(ValueError):
            compute_effective_dimension(corr)

    @given(st.integers(min_value=2, max_value=20))
    @settings(max_examples=20, deadline=10000)
    def test_pbt_effective_dimension_leq_family_size(self, n: int) -> None:
        """PBT: 有效维度 ≤ 家族因子数。

        **Validates: Requirements 3.2, 3.5**
        """
        rng = np.random.default_rng(n)
        # 生成随机相关矩阵
        A = rng.standard_normal((n, n))
        corr = np.corrcoef(A)
        n_eff = compute_effective_dimension(corr)
        assert n_eff <= n + 1e-6, (
            f"有效维度 {n_eff:.4f} 超过家族大小 {n}"
        )


# ===========================================================================
# 冗余因子对检测测试
# **Validates: Requirements 3.3**
# ===========================================================================


class TestDetectRedundantPairs:
    """冗余因子对检测测试。

    **Validates: Requirements 3.3**
    """

    def _make_factor_panel(
        self,
        n_dates: int = 30,
        n_stocks: int = 50,
        seed: int = 42,
    ) -> pd.DataFrame:
        """生成测试用因子面板。"""
        rng = np.random.default_rng(seed)
        base_date = pd.Timestamp("2020-01-01")
        dates = [base_date + pd.Timedelta(weeks=i) for i in range(n_dates)]
        stocks = [f"stock_{i:03d}" for i in range(n_stocks)]

        rows = []
        for date in dates:
            # 生成截面因子值
            f1 = rng.standard_normal(n_stocks)
            f2 = f1 * 0.95 + rng.standard_normal(n_stocks) * 0.1  # 高相关
            f3 = rng.standard_normal(n_stocks)  # 独立因子
            for i, stock in enumerate(stocks):
                rows.append({
                    "date": date,
                    "stock_id": stock,
                    "factor_high_corr_1": f1[i],
                    "factor_high_corr_2": f2[i],
                    "factor_independent": f3[i],
                })

        return pd.DataFrame(rows)

    def test_detects_highly_correlated_pair(self) -> None:
        """应检测到高相关因子对。

        **Validates: Requirements 3.3**
        """
        df = self._make_factor_panel()
        factor_cols = ["factor_high_corr_1", "factor_high_corr_2", "factor_independent"]
        pairs = detect_redundant_pairs(df, factor_cols, threshold=0.8, min_periods=20)

        # 应检测到高相关对
        assert len(pairs) >= 1, "应检测到至少一个高相关因子对"
        # 第一个对应该是高相关对
        assert "factor_high_corr_1" in pairs[0][:2]
        assert "factor_high_corr_2" in pairs[0][:2]

    def test_no_redundant_pairs_for_independent_factors(self) -> None:
        """独立因子之间不应检测到冗余对。

        **Validates: Requirements 3.3**
        """
        rng = np.random.default_rng(42)
        n_dates, n_stocks = 30, 50
        base_date = pd.Timestamp("2020-01-01")
        dates = [base_date + pd.Timedelta(weeks=i) for i in range(n_dates)]
        stocks = [f"stock_{i:03d}" for i in range(n_stocks)]

        rows = []
        for date in dates:
            for i, stock in enumerate(stocks):
                rows.append({
                    "date": date,
                    "stock_id": stock,
                    "f1": rng.standard_normal(),
                    "f2": rng.standard_normal(),
                    "f3": rng.standard_normal(),
                })
        df = pd.DataFrame(rows)
        pairs = detect_redundant_pairs(df, ["f1", "f2", "f3"], threshold=0.8)
        assert len(pairs) == 0, (
            f"独立因子不应有冗余对，但检测到 {len(pairs)} 对"
        )

    def test_returns_empty_for_single_factor(self) -> None:
        """单因子不应有冗余对。

        **Validates: Requirements 3.3**
        """
        df = self._make_factor_panel()
        pairs = detect_redundant_pairs(df, ["factor_high_corr_1"])
        assert pairs == []

    def test_sorted_by_correlation_descending(self) -> None:
        """结果应按相关性从高到低排序。

        **Validates: Requirements 3.3**
        """
        df = self._make_factor_panel()
        factor_cols = ["factor_high_corr_1", "factor_high_corr_2", "factor_independent"]
        pairs = detect_redundant_pairs(df, factor_cols, threshold=0.5)
        if len(pairs) >= 2:
            for i in range(len(pairs) - 1):
                assert abs(pairs[i][2]) >= abs(pairs[i + 1][2]), (
                    "结果应按相关性绝对值从高到低排序"
                )

    def test_raises_for_missing_columns(self) -> None:
        """缺失因子列应抛出 ValueError。

        **Validates: Requirements 3.3**
        """
        df = self._make_factor_panel()
        with pytest.raises(ValueError):
            detect_redundant_pairs(df, ["nonexistent_factor"])

    def test_returns_empty_for_insufficient_dates(self) -> None:
        """日期数不足时应返回空列表。

        **Validates: Requirements 3.3**
        """
        df = self._make_factor_panel(n_dates=5)
        factor_cols = ["factor_high_corr_1", "factor_high_corr_2"]
        pairs = detect_redundant_pairs(df, factor_cols, min_periods=20)
        assert pairs == [], "日期数不足时应返回空列表"


# ===========================================================================
# 因子准入/淘汰三段式流程测试
# **Validates: Requirements 3.4**
# ===========================================================================


class TestFactorAdmissionManager:
    """因子准入/淘汰三段式流程测试。

    **Validates: Requirements 3.4**
    """

    def test_add_to_shadow_pool(self) -> None:
        """新因子应进入影子池。

        **Validates: Requirements 3.4**
        """
        manager = FactorAdmissionManager()
        manager.add_to_shadow_pool("factor_a", "fast")
        assert "factor_a" in manager.factors
        assert manager.factors["factor_a"].stage == "shadow_pool"

    def test_shadow_pool_advances_to_observation_on_update(self) -> None:
        """影子池因子在第一次 update 后应进入观察期。

        **Validates: Requirements 3.4**
        """
        manager = FactorAdmissionManager()
        manager.add_to_shadow_pool("factor_a", "fast")
        manager.update(0, {"factor_a": 0.01})
        assert manager.factors["factor_a"].stage == "observation"

    def test_observation_advances_to_active_after_min_periods(self) -> None:
        """观察期满且贡献为正时，因子应晋升为 active。

        **Validates: Requirements 3.4**
        """
        manager = FactorAdmissionManager()
        manager.add_to_shadow_pool("factor_a", "fast")

        # fast 的最小观察期为 6 个窗口
        for i in range(7):  # 1 次进入观察期 + 6 次观察
            manager.update(i, {"factor_a": 0.01})

        assert manager.factors["factor_a"].stage == "active", (
            f"观察期满后应为 active，实际为 {manager.factors['factor_a'].stage}"
        )

    def test_active_factor_retires_after_consecutive_negative_contributions(
        self,
    ) -> None:
        """活跃因子连续负贡献超过阈值后应被淘汰。

        **Validates: Requirements 3.4**
        """
        manager = FactorAdmissionManager(retirement_streak_threshold=5)
        manager.add_to_shadow_pool("factor_a", "fast")

        # 先晋升到 active
        for i in range(7):
            manager.update(i, {"factor_a": 0.01})
        assert manager.factors["factor_a"].stage == "active"

        # 连续 5 个窗口负贡献
        for i in range(7, 12):
            manager.update(i, {"factor_a": -0.01})

        assert manager.factors["factor_a"].stage == "retired", (
            f"连续负贡献后应为 retired，实际为 {manager.factors['factor_a'].stage}"
        )

    def test_negative_streak_resets_on_positive_contribution(self) -> None:
        """正贡献应重置负贡献连续计数。

        **Validates: Requirements 3.4**
        """
        manager = FactorAdmissionManager(retirement_streak_threshold=5)
        manager.add_to_shadow_pool("factor_a", "fast")

        # 晋升到 active
        for i in range(7):
            manager.update(i, {"factor_a": 0.01})

        # 4 个负贡献（未达阈值）
        for i in range(7, 11):
            manager.update(i, {"factor_a": -0.01})
        assert manager.factors["factor_a"].stage == "active"
        assert manager.factors["factor_a"].negative_contribution_streak == 4

        # 1 个正贡献，重置计数
        manager.update(11, {"factor_a": 0.01})
        assert manager.factors["factor_a"].negative_contribution_streak == 0
        assert manager.factors["factor_a"].stage == "active"

    def test_get_active_factors_returns_observation_and_active(self) -> None:
        """get_active_factors() 应返回 observation 和 active 阶段的因子。

        **Validates: Requirements 3.4**
        """
        manager = FactorAdmissionManager()
        manager.add_to_shadow_pool("factor_a", "fast")
        manager.add_to_shadow_pool("factor_b", "slow")

        # factor_a 进入观察期
        manager.update(0, {"factor_a": 0.01, "factor_b": 0.01})

        active = manager.get_active_factors()
        assert "factor_a" in active
        assert "factor_b" in active

    def test_get_status_report_structure(self) -> None:
        """get_status_report() 应返回正确结构的报告。

        **Validates: Requirements 3.4**
        """
        manager = FactorAdmissionManager()
        manager.add_to_shadow_pool("factor_a", "fast")
        manager.update(0, {"factor_a": 0.01})

        report = manager.get_status_report()
        assert "current_window" in report
        assert "stage_counts" in report
        assert "factors" in report
        assert "factor_a" in report["factors"]
        assert report["stage_counts"]["observation"] == 1

    def test_add_duplicate_factor_raises(self) -> None:
        """重复添加因子应抛出 ValueError。

        **Validates: Requirements 3.4**
        """
        manager = FactorAdmissionManager()
        manager.add_to_shadow_pool("factor_a", "fast")
        with pytest.raises(ValueError):
            manager.add_to_shadow_pool("factor_a", "slow")

    def test_slow_factor_has_longer_observation_period(self) -> None:
        """慢衰减因子的观察期应比快衰减因子更长。

        **Validates: Requirements 3.4**
        """
        manager = FactorAdmissionManager()
        manager.add_to_shadow_pool("fast_factor", "fast")
        manager.add_to_shadow_pool("slow_factor", "slow")

        # 经过 12 个窗口（fast 最大观察期）
        for i in range(13):
            manager.update(i, {"fast_factor": 0.01, "slow_factor": 0.01})

        # fast 因子应已晋升
        assert manager.factors["fast_factor"].stage == "active"
        # slow 因子仍在观察期（最小 18 个窗口）
        assert manager.factors["slow_factor"].stage == "observation"

    def test_observation_retires_after_max_periods_with_no_contribution(
        self,
    ) -> None:
        """超过最大观察期仍无正贡献时，因子应被淘汰。

        **Validates: Requirements 3.4**
        """
        manager = FactorAdmissionManager()
        manager.add_to_shadow_pool("factor_a", "fast")

        # fast 最大观察期为 12 个窗口，持续负贡献
        for i in range(14):
            manager.update(i, {"factor_a": -0.01})

        assert manager.factors["factor_a"].stage == "retired", (
            f"超过最大观察期仍无正贡献，应为 retired，"
            f"实际为 {manager.factors['factor_a'].stage}"
        )
