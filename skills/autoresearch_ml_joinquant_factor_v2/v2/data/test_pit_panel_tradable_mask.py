"""单元测试：compute_tradable_mask() 和 _count_trading_days_since_listing()

对应任务：Task 1.2 实现可交易掩码
对应需求：需求 1.2（可交易掩码过滤 ST/*ST、停牌、涨跌停一字板、新股冷启动、退市整理）
"""

from __future__ import annotations

import pandas as pd
import pytest

from skills.autoresearch_ml_joinquant_factor_v2.v2.data.pit_panel import (
    _count_trading_days_since_listing,
    compute_tradable_mask,
)


# ---------------------------------------------------------------------------
# 测试辅助函数
# ---------------------------------------------------------------------------

def _make_df(
    stocks: list[str],
    dates: list[str],
    pchg: list[float] | None = None,
    extra_cols: dict | None = None,
) -> pd.DataFrame:
    """构造测试用 DataFrame，按 [date, stock_id] 排序并 reset_index。"""
    n = len(stocks)
    data = {
        "stock_id": stocks,
        "date": pd.to_datetime(dates),
    }
    if pchg is not None:
        data["pchg"] = pchg
    if extra_cols:
        data.update(extra_cols)
    df = pd.DataFrame(data)
    df = df.sort_values(["date", "stock_id"]).reset_index(drop=True)
    return df


# ---------------------------------------------------------------------------
# _count_trading_days_since_listing 测试
# ---------------------------------------------------------------------------

class TestCountTradingDaysSinceListing:
    """测试 _count_trading_days_since_listing() 辅助函数。"""

    def test_single_stock_sequential_dates(self):
        """单只股票，连续出现 3 个截面日期，交易日数应为 0, 1, 2。"""
        df = _make_df(
            stocks=["A", "A", "A"],
            dates=["2020-01-01", "2020-01-08", "2020-01-15"],
        )
        result = _count_trading_days_since_listing(df)
        assert result.tolist() == [0, 1, 2]

    def test_two_stocks_same_start(self):
        """两只股票同时首次出现，各自的交易日数应从 0 开始。"""
        df = _make_df(
            stocks=["A", "B", "A", "B"],
            dates=["2020-01-01", "2020-01-01", "2020-01-08", "2020-01-08"],
        )
        result = _count_trading_days_since_listing(df)
        # 排序后：A@01-01=0, B@01-01=0, A@01-08=1, B@01-08=1
        assert result.tolist() == [0, 0, 1, 1]

    def test_new_stock_appears_later(self):
        """新股在第 2 个截面才出现，其首次出现日期的交易日数应为 0。"""
        df = _make_df(
            stocks=["A", "A", "B"],
            dates=["2020-01-01", "2020-01-08", "2020-01-08"],
        )
        result = _count_trading_days_since_listing(df)
        # 排序后：A@01-01=0, A@01-08=1, B@01-08=0
        assert result.tolist() == [0, 1, 0]

    def test_result_index_aligned_with_df(self):
        """返回的 Series 索引应与 df.index 一致。"""
        df = _make_df(
            stocks=["X", "Y", "X"],
            dates=["2020-01-01", "2020-01-01", "2020-01-08"],
        )
        result = _count_trading_days_since_listing(df)
        assert list(result.index) == list(df.index)

    def test_missing_columns_returns_zeros(self):
        """缺少 stock_id 或 date 列时，应返回全 0 序列。"""
        df = pd.DataFrame({"value": [1, 2, 3]})
        result = _count_trading_days_since_listing(df)
        assert (result == 0).all()
        assert len(result) == 3

    def test_non_negative_values(self):
        """所有交易日数应 >= 0。"""
        df = _make_df(
            stocks=["A", "B", "C", "A", "B"],
            dates=["2020-01-01", "2020-01-08", "2020-01-15",
                   "2020-01-08", "2020-01-15"],
        )
        result = _count_trading_days_since_listing(df)
        assert (result >= 0).all()

    def test_first_appearance_always_zero(self):
        """每只股票首次出现时，交易日数应为 0。"""
        df = _make_df(
            stocks=["A", "B", "C", "A", "B", "C"],
            dates=["2020-01-01", "2020-01-08", "2020-01-15",
                   "2020-01-08", "2020-01-15", "2020-01-22"],
        )
        result = _count_trading_days_since_listing(df)
        # 每只股票首次出现的行
        # 每只股票首次出现的行
        first_rows = df.groupby("stock_id")["date"].apply(lambda g: g.index[0])
        for idx in first_rows:
            assert result[idx] == 0, f"股票首次出现时交易日数应为 0，但得到 {result[idx]}"


# ---------------------------------------------------------------------------
# compute_tradable_mask 测试
# ---------------------------------------------------------------------------

class TestComputeTradableMask:
    """测试 compute_tradable_mask() 主函数。"""

    def test_returns_bool_series(self):
        """返回值应为布尔类型的 pd.Series。"""
        df = _make_df(
            stocks=["A", "B"],
            dates=["2020-01-01", "2020-01-01"],
            pchg=[0.01, 0.02],
        )
        result = compute_tradable_mask(df, new_stock_cooldown_days=0)
        assert isinstance(result, pd.Series)
        assert result.dtype == bool

    def test_index_aligned_with_df(self):
        """返回的 Series 索引应与 df.index 一致。"""
        df = _make_df(
            stocks=["A", "B", "C"],
            dates=["2020-01-01", "2020-01-01", "2020-01-08"],
            pchg=[0.01, 0.02, 0.03],
        )
        result = compute_tradable_mask(df, new_stock_cooldown_days=0)
        assert list(result.index) == list(df.index)

    def test_length_matches_df(self):
        """返回的 Series 长度应与 df 行数一致。"""
        df = _make_df(
            stocks=["A", "B", "C"],
            dates=["2020-01-01", "2020-01-01", "2020-01-08"],
            pchg=[0.01, 0.02, 0.03],
        )
        result = compute_tradable_mask(df, new_stock_cooldown_days=0)
        assert len(result) == len(df)

    # ------------------------------------------------------------------
    # 过滤 1：ST/*ST 股票
    # ------------------------------------------------------------------

    def test_st_filter_with_is_st_column(self):
        """is_st=True 的行应被过滤（mask=False）。"""
        df = _make_df(
            stocks=["A", "B", "C"],
            dates=["2020-01-01", "2020-01-01", "2020-01-01"],
            pchg=[0.01, 0.02, 0.03],
            extra_cols={"is_st": [True, False, False]},
        )
        result = compute_tradable_mask(df, new_stock_cooldown_days=0)
        assert result.tolist() == [False, True, True]

    def test_st_filter_with_st_status_column(self):
        """st_status=True 的行应被过滤。"""
        df = _make_df(
            stocks=["A", "B"],
            dates=["2020-01-01", "2020-01-01"],
            pchg=[0.01, 0.02],
            extra_cols={"st_status": [False, True]},
        )
        result = compute_tradable_mask(df, new_stock_cooldown_days=0)
        assert result.tolist() == [True, False]

    def test_no_st_column_skips_filter(self, caplog):
        """无 ST 列时应跳过过滤并记录警告，不抛出异常。"""
        df = _make_df(
            stocks=["A", "B"],
            dates=["2020-01-01", "2020-01-01"],
            pchg=[0.01, 0.02],
        )
        import logging
        with caplog.at_level(logging.WARNING):
            result = compute_tradable_mask(df, new_stock_cooldown_days=0)
        assert "ST过滤" in caplog.text
        # 无 ST 列时不应因 ST 过滤而减少可交易行
        assert result.sum() == 2

    # ------------------------------------------------------------------
    # 过滤 2：停牌股票
    # ------------------------------------------------------------------

    def test_suspended_filter_with_is_suspended_column(self):
        """is_suspended=True 的行应被过滤。"""
        df = _make_df(
            stocks=["A", "B", "C"],
            dates=["2020-01-01", "2020-01-01", "2020-01-01"],
            pchg=[0.01, 0.02, 0.03],
            extra_cols={"is_suspended": [False, True, False]},
        )
        result = compute_tradable_mask(df, new_stock_cooldown_days=0)
        assert result.tolist() == [True, False, True]

    def test_suspended_filter_with_paused_column(self):
        """paused=True 的行应被过滤。"""
        df = _make_df(
            stocks=["A", "B"],
            dates=["2020-01-01", "2020-01-01"],
            pchg=[0.01, 0.02],
            extra_cols={"paused": [True, False]},
        )
        result = compute_tradable_mask(df, new_stock_cooldown_days=0)
        assert result.tolist() == [False, True]

    def test_no_suspended_column_skips_filter(self, caplog):
        """无停牌列时应跳过过滤并记录警告。"""
        df = _make_df(
            stocks=["A"],
            dates=["2020-01-01"],
            pchg=[0.01],
        )
        import logging
        with caplog.at_level(logging.WARNING):
            result = compute_tradable_mask(df, new_stock_cooldown_days=0)
        assert "停牌过滤" in caplog.text

    # ------------------------------------------------------------------
    # 过滤 3：涨跌停一字板
    # ------------------------------------------------------------------

    def test_limit_filter_using_high_low_equal(self):
        """high == low 时应被过滤（一字板）。"""
        df = _make_df(
            stocks=["A", "B", "C"],
            dates=["2020-01-01", "2020-01-01", "2020-01-01"],
            pchg=[0.10, 0.02, -0.10],
            extra_cols={
                "high": [11.0, 10.5, 9.0],
                "low":  [11.0, 10.0, 9.0],  # A 和 C 是一字板
            },
        )
        result = compute_tradable_mask(df, new_stock_cooldown_days=0)
        assert result.tolist() == [False, True, False]

    def test_limit_filter_using_pchg_when_no_high_low(self):
        """无 high/low 且 |pchg| 明显接近 20% 板时应被保守过滤。"""
        df = _make_df(
            stocks=["A", "B", "C", "D"],
            dates=["2020-01-01"] * 4,
            pchg=[0.20, 0.05, -0.20, 0.02],
        )
        result = compute_tradable_mask(df, new_stock_cooldown_days=0)
        # A/C: |pchg| >= 0.195 → 过滤
        # B/D: |pchg| < 0.195 → 保留
        assert result.tolist() == [False, True, False, True]

    def test_limit_filter_20pct_threshold(self):
        """|pchg| >= 0.195 时应被过滤（科创板/创业板 ±20% 限制）。"""
        df = _make_df(
            stocks=["A", "B"],
            dates=["2020-01-01", "2020-01-01"],
            pchg=[0.20, 0.15],
        )
        result = compute_tradable_mask(df, new_stock_cooldown_days=0)
        assert result.tolist() == [False, True]

    def test_high_low_takes_priority_over_pchg(self):
        """当 high 和 low 列同时存在时，应使用 high==low 而非 pchg。"""
        df = _make_df(
            stocks=["A", "B"],
            dates=["2020-01-01", "2020-01-01"],
            pchg=[0.10, 0.10],  # 两者 pchg 都在涨停
            extra_cols={
                "high": [11.0, 11.0],
                "low":  [10.5, 11.0],  # A: high != low（非一字板），B: high == low（一字板）
            },
        )
        result = compute_tradable_mask(df, new_stock_cooldown_days=0)
        # 使用 high==low：A 保留，B 过滤
        assert result.tolist() == [True, False]

    # ------------------------------------------------------------------
    # 过滤 4：新股冷启动
    # ------------------------------------------------------------------

    def test_new_stock_cooldown_filters_early_rows(self):
        """上市不足 cooldown 天的股票应被过滤。"""
        df = _make_df(
            stocks=["A", "A", "A", "A"],
            dates=["2020-01-01", "2020-01-08", "2020-01-15", "2020-01-22"],
            pchg=[0.01, 0.02, 0.03, 0.04],
        )
        # cooldown=2：前 2 个截面（交易日数 0, 1）被过滤，第 3 个（交易日数 2）开始可交易
        result = compute_tradable_mask(df, new_stock_cooldown_days=2)
        assert result.tolist() == [False, False, True, True]

    def test_new_stock_cooldown_zero_keeps_all(self):
        """cooldown=0 时不应因新股冷启动过滤任何行。"""
        df = _make_df(
            stocks=["A", "B"],
            dates=["2020-01-01", "2020-01-01"],
            pchg=[0.01, 0.02],
        )
        result = compute_tradable_mask(df, new_stock_cooldown_days=0)
        assert result.all()

    def test_new_stock_cooldown_default_60(self):
        """默认 cooldown=60，前 60 个截面应被过滤。"""
        # 构造 65 个截面日期
        dates = pd.date_range("2020-01-01", periods=65, freq="W").strftime("%Y-%m-%d").tolist()
        df = _make_df(
            stocks=["A"] * 65,
            dates=dates,
            pchg=[0.01] * 65,
        )
        result = compute_tradable_mask(df)  # 默认 cooldown=60
        # 前 60 行（交易日数 0~59）被过滤，后 5 行（60~64）可交易
        assert result[:60].sum() == 0
        assert result[60:].sum() == 5

    def test_new_stock_cooldown_always_computed(self):
        """新股冷启动过滤应始终执行，无需额外列。"""
        df = _make_df(
            stocks=["A"],
            dates=["2020-01-01"],
            pchg=[0.01],
        )
        # 即使没有任何额外列，新股冷启动过滤也应执行
        result = compute_tradable_mask(df, new_stock_cooldown_days=1)
        # 只有 1 行，交易日数=0 < 1，应被过滤
        assert result.tolist() == [False]

    # ------------------------------------------------------------------
    # 过滤 5：退市整理期
    # ------------------------------------------------------------------

    def test_delisting_filter_with_is_delisting_column(self):
        """is_delisting=True 的行应被过滤。"""
        df = _make_df(
            stocks=["A", "B", "C"],
            dates=["2020-01-01", "2020-01-01", "2020-01-01"],
            pchg=[0.01, 0.02, 0.03],
            extra_cols={"is_delisting": [False, False, True]},
        )
        result = compute_tradable_mask(df, new_stock_cooldown_days=0)
        assert result.tolist() == [True, True, False]

    def test_delisting_filter_with_delisting_column(self):
        """delisting=True 的行应被过滤。"""
        df = _make_df(
            stocks=["A", "B"],
            dates=["2020-01-01", "2020-01-01"],
            pchg=[0.01, 0.02],
            extra_cols={"delisting": [True, False]},
        )
        result = compute_tradable_mask(df, new_stock_cooldown_days=0)
        assert result.tolist() == [False, True]

    def test_no_delisting_column_skips_filter(self, caplog):
        """无退市列时应跳过过滤并记录警告。"""
        df = _make_df(
            stocks=["A"],
            dates=["2020-01-01"],
            pchg=[0.01],
        )
        import logging
        with caplog.at_level(logging.WARNING):
            result = compute_tradable_mask(df, new_stock_cooldown_days=0)
        assert "退市整理过滤" in caplog.text

    # ------------------------------------------------------------------
    # 组合过滤测试
    # ------------------------------------------------------------------

    def test_combined_filters_all_active(self):
        """多个过滤条件同时激活时，应取所有条件的交集（AND 逻辑）。"""
        df = _make_df(
            stocks=["A", "B", "C", "D"],
            dates=["2020-01-01"] * 4,
            pchg=[0.01, 0.10, 0.02, 0.03],
            extra_cols={
                "is_st": [True, False, False, False],
                "is_suspended": [False, False, True, False],
            },
        )
        result = compute_tradable_mask(df, new_stock_cooldown_days=0)
        # A: ST → 过滤
        # B: 无 high/low 且 pchg=0.10，不应被 20% 板保守过滤
        # C: suspended → 过滤
        # D: 全部通过 → 可交易
        assert result.tolist() == [False, True, False, True]

    def test_empty_dataframe(self):
        """空 DataFrame 应返回空 Series。"""
        df = pd.DataFrame(columns=["stock_id", "date", "pchg"])
        result = compute_tradable_mask(df, new_stock_cooldown_days=0)
        assert len(result) == 0
        assert result.dtype == bool

    def test_all_tradable_when_no_filters_triggered(self):
        """无任何过滤条件触发时，所有行应可交易。"""
        df = _make_df(
            stocks=["A", "B", "C"],
            dates=["2020-01-01"] * 3,
            pchg=[0.01, 0.02, 0.03],
        )
        result = compute_tradable_mask(df, new_stock_cooldown_days=0)
        assert result.all()
