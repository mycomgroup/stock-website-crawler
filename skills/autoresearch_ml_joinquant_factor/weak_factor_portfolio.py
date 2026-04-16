"""弱因子组合量化策略的完整实现。

该模块将《弱因子组合量化策略技术方案》中的核心功能落地为可复用代码：
- 因子标准化与动态激活
- 等权 / 风险平价 / 机器学习三套信号
- 固定与动态信号融合
- 头寸管理、波动率目标、止损与头寸约束
- 样本外充分性验证
- 一体化组合类 WeakFactorPortfolio
"""

from __future__ import annotations

from dataclasses import dataclass
import numpy as np
import pandas as pd


EPS = 1e-8


def standardize_factors(
    factors_df: pd.DataFrame,
    method: str = "zscore",
    clip_value: float = 3.0,
) -> pd.DataFrame:
    """按日期截面标准化因子矩阵。"""
    if factors_df.empty:
        return factors_df.copy()

    result = factors_df.copy()
    if method not in {"zscore", "rank"}:
        raise ValueError("method 必须是 'zscore' 或 'rank'")

    if isinstance(result.index, pd.MultiIndex) and "date" in result.index.names:
        group_level = result.index.names.index("date")
        grouped = result.groupby(level=group_level)
        if method == "zscore":
            result = grouped.transform(lambda x: (x - x.mean()) / (x.std(ddof=0) + EPS))
        else:
            result = grouped.transform(lambda x: x.rank(pct=True) * 2 - 1)
    elif "date" in result.columns:
        idx = result.index
        dates = result["date"]
        vals = result.drop(columns=["date"])
        if method == "zscore":
            vals = vals.groupby(dates).transform(lambda x: (x - x.mean()) / (x.std(ddof=0) + EPS))
        else:
            vals = vals.groupby(dates).transform(lambda x: x.rank(pct=True) * 2 - 1)
        vals["date"] = dates.values
        vals.index = idx
        result = vals
    else:
        if method == "zscore":
            result = (result - result.mean()) / (result.std(ddof=0) + EPS)
        else:
            result = result.rank(pct=True) * 2 - 1

    return result.clip(-clip_value, clip_value)


def strategy_equal_weighted(factors_df: pd.DataFrame, normalize_window: int = 252) -> pd.Series:
    """等权融合信号。"""
    signal = factors_df.mean(axis=1, skipna=True)
    return _rolling_normalize(signal, window=normalize_window)


def strategy_risk_parity(
    factors_df: pd.DataFrame,
    window: int = 252,
    normalize_window: int = 252,
) -> pd.Series:
    """风险平价融合信号（波动率倒数加权）。"""
    factor_vols = factors_df.rolling(window, min_periods=max(20, window // 5)).std()
    inv_vols = 1.0 / (factor_vols + EPS)
    weights = inv_vols.div(inv_vols.sum(axis=1), axis=0).fillna(0)
    signal = (factors_df * weights).sum(axis=1, skipna=True)
    return _rolling_normalize(signal, window=normalize_window)


def strategy_ml_weighted(
    factors_df: pd.DataFrame,
    target_return: pd.Series,
    retrain_freq: int = 21,
    train_window: int = 500,
    min_train: int = 250,
    normalize_window: int = 252,
) -> pd.Series:
    """机器学习滚动训练信号（仅使用历史信息）。"""
    from lightgbm import LGBMRegressor

    signal = pd.Series(np.nan, index=factors_df.index, dtype=float)
    dates = factors_df.index

    for i in range(min_train, len(dates)):
        if (i - min_train) % retrain_freq != 0:
            continue

        train_start = max(0, i - train_window)
        X_train = factors_df.iloc[train_start:i].fillna(0)
        y_train = target_return.iloc[train_start:i]

        valid = ~y_train.isna()
        X_train = X_train.loc[valid]
        y_train = y_train.loc[valid]
        if len(y_train) < 100:
            continue

        model = LGBMRegressor(
            num_leaves=31,
            max_depth=5,
            learning_rate=0.05,
            n_estimators=100,
            subsample=0.8,
            colsample_bytree=0.7,
            reg_alpha=0.1,
            reg_lambda=0.1,
            verbose=-1,
            random_state=42,
        )
        model.fit(X_train.values, y_train.values)

        pred_end = min(i + retrain_freq, len(dates))
        X_pred = factors_df.iloc[i:pred_end].fillna(0)
        signal.iloc[i:pred_end] = model.predict(X_pred.values)

    signal = signal.ffill()
    return _rolling_normalize(signal, window=normalize_window)


def combine_signals_fixed(
    s_equal: pd.Series,
    s_rp: pd.Series,
    s_ml: pd.Series,
    weights: tuple[float, float, float] = (0.4, 0.3, 0.3),
    normalize_window: int = 252,
) -> pd.Series:
    """固定权重融合三个信号。"""
    w = np.array(weights, dtype=float)
    if not np.isclose(w.sum(), 1.0):
        w = w / (w.sum() + EPS)

    s_eq = _rolling_normalize(s_equal, window=normalize_window)
    s_rp_n = _rolling_normalize(s_rp, window=normalize_window)
    s_ml_n = _rolling_normalize(s_ml, window=normalize_window)
    return s_eq * w[0] + s_rp_n * w[1] + s_ml_n * w[2]


def combine_signals_dynamic(
    s_equal: pd.Series,
    s_rp: pd.Series,
    s_ml: pd.Series,
    target_return: pd.Series,
    eval_window: int = 63,
) -> pd.Series:
    """按近期 IC 表现动态调整权重。"""
    signals = {"equal": s_equal, "rp": s_rp, "ml": s_ml}
    index = s_equal.index
    weights_ts = pd.DataFrame(index=index, columns=list(signals.keys()), dtype=float)

    forward_ret = target_return.shift(-1)
    for i in range(eval_window, len(index)):
        recent_ics: dict[str, float] = {}
        for name, sig in signals.items():
            corr = sig.iloc[i - eval_window : i].corr(forward_ret.iloc[i - eval_window : i])
            recent_ics[name] = max(float(corr) if pd.notna(corr) else 0.0, 0.0)

        total_ic = sum(recent_ics.values())
        if total_ic <= EPS:
            for name in signals.keys():
                weights_ts.loc[index[i], name] = 1 / len(signals)
        else:
            for name, ic in recent_ics.items():
                weights_ts.loc[index[i], name] = ic / total_ic

    weights_ts = weights_ts.ffill().fillna(1 / len(signals))
    return (
        s_equal * weights_ts["equal"]
        + s_rp * weights_ts["rp"]
        + s_ml * weights_ts["ml"]
    )


def dynamic_position_sizing(signal: pd.Series, lookback: int = 252) -> pd.Series:
    """按置信度动态缩放仓位。"""
    signal_std = signal.rolling(lookback, min_periods=max(20, lookback // 5)).std()
    position_scale = np.clip(np.abs(signal) / (signal_std + EPS), 0.5, 1.5)
    return np.sign(signal) * position_scale


def volatility_targeting(
    portfolio_return: pd.Series,
    target_vol: float = 0.15,
    lookback: int = 63,
) -> tuple[pd.Series, pd.Series]:
    """波动率目标制与杠杆序列。"""
    realized_vol = portfolio_return.rolling(lookback, min_periods=max(20, lookback // 3)).std() * np.sqrt(252)
    leverage = target_vol / np.maximum(realized_vol, 0.02)
    leverage = pd.Series(np.clip(leverage, 0.5, 2.0), index=portfolio_return.index)
    adjusted_return = portfolio_return * leverage.shift(1).fillna(1.0)
    return adjusted_return, leverage


def apply_position_limits(
    weights: pd.Series,
    max_single: float = 0.03,
    max_top10: float = 0.20,
) -> pd.Series:
    """单票与前十集中度约束。"""
    w = weights.copy().clip(-max_single, max_single)
    gross = np.abs(w).sum()
    if gross > EPS:
        w = w / gross

    abs_w = np.abs(w).sort_values(ascending=False)
    top10_sum = abs_w.head(10).sum()
    if top10_sum > max_top10 and top10_sum > EPS:
        threshold = abs_w.head(10).min()
        large_mask = np.abs(w) >= threshold
        scale = max_top10 / top10_sum
        w.loc[large_mask] = w.loc[large_mask] * scale
        gross2 = np.abs(w).sum()
        if gross2 > EPS:
            w = w / gross2
    return w


def apply_stop_loss(
    signal: pd.Series,
    portfolio_return: pd.Series,
    monthly_dd_threshold: float = -0.03,
) -> pd.Series:
    """月度回撤止损：回撤超阈值后将信号减半。"""
    adjusted_signal = signal.copy()
    monthly_cum_return = portfolio_return.rolling(22, min_periods=10).sum()
    stop_triggered = monthly_cum_return < monthly_dd_threshold
    adjusted_signal.loc[stop_triggered] = adjusted_signal.loc[stop_triggered] * 0.5
    return adjusted_signal


def get_active_factors(
    all_factors_df: pd.DataFrame,
    ic_history: pd.DataFrame,
    n_active: int = 70,
    recent_window: int = 63,
) -> pd.DataFrame:
    """基于近期 IC 动态激活因子。"""
    if ic_history.empty:
        return all_factors_df
    recent_ic = ic_history.tail(recent_window).mean().abs().sort_values(ascending=False)
    top_factors = recent_ic.head(min(n_active, len(recent_ic))).index.tolist()
    selected_cols = [c for c in top_factors if c in all_factors_df.columns]
    return all_factors_df[selected_cols]


def validate_backtest_sufficiency(train_metrics: dict, test_metrics: dict) -> tuple[dict[str, bool], int]:
    """验证回测充分性，返回检查结果与通过项数量。"""
    def ratio_ok(a: float, b: float, threshold: float) -> bool:
        if abs(b) <= EPS:
            return False
        return (a / b) > threshold

    checks = {
        "IC保留率 > 70%": ratio_ok(test_metrics.get("ic", 0.0), train_metrics.get("ic", 0.0), 0.70),
        "夏普比保留率 > 75%": ratio_ok(test_metrics.get("sharpe", 0.0), train_metrics.get("sharpe", 0.0), 0.75),
        "月度胜率 > 50%": test_metrics.get("win_rate", 0.0) > 0.50,
        "连续亏损月 < 6个月": test_metrics.get("max_consecutive_loss_months", 999) < 6,
        "最大回撤 < 20%": abs(test_metrics.get("max_drawdown", 1.0)) < 0.20,
        "IC稳定性（std增幅<30%）": test_metrics.get("ic_std", 1.0) < train_metrics.get("ic_std", 0.0) * 1.30,
    }
    passed = int(sum(checks.values()))
    return checks, passed


@dataclass
class RiskManager:
    """组合风险管理器。"""

    target_vol: float = 0.15
    max_drawdown_stop: float = 0.03

    def apply_all(
        self,
        raw_signal: pd.Series,
        portfolio_return: pd.Series | None = None,
        is_cross_section_weights: bool = False,
    ) -> pd.Series:
        """应用风险控制到组合时间序列信号或单日截面权重。

        参数
        ----
        raw_signal:
            - 当 is_cross_section_weights=False（默认）时，表示组合层时间序列信号（按日期索引的一维序列）。
            - 当 is_cross_section_weights=True 时，表示单个日期的股票层截面权重（按股票索引的一维序列）。
        portfolio_return:
            组合收益时间序列。仅对组合层时间序列信号生效，用于波动率目标与止损。
        is_cross_section_weights:
            是否将 raw_signal 视为股票层截面权重。
        """
        signal = raw_signal.copy()
        if is_cross_section_weights:
            signal = apply_position_limits(signal)
        signal = dynamic_position_sizing(signal)
        if portfolio_return is not None:
            _, leverage = volatility_targeting(portfolio_return, target_vol=self.target_vol)
            signal = signal * leverage.shift(1).fillna(1.0)
            signal = apply_stop_loss(
                signal,
                portfolio_return=portfolio_return,
                monthly_dd_threshold=-abs(self.max_drawdown_stop),
            )
        return signal

    def apply_all_cross_section_matrix(
        self,
        raw_signal_matrix: pd.DataFrame,
        portfolio_return: pd.Series | None = None,
    ) -> pd.DataFrame:
        """对截面权重矩阵逐日应用风控（先头寸约束，再缩放）。"""
        if raw_signal_matrix.empty:
            return raw_signal_matrix.copy()

        adjusted = raw_signal_matrix.apply(
            lambda row: self.apply_all(row, is_cross_section_weights=True),
            axis=1,
        )
        if portfolio_return is not None:
            _, leverage = volatility_targeting(portfolio_return, target_vol=self.target_vol)
            adjusted = adjusted.mul(leverage.shift(1).fillna(1.0), axis=0)
            monthly_cum_return = portfolio_return.rolling(22, min_periods=10).sum()
            stop_triggered = monthly_cum_return < -abs(self.max_drawdown_stop)
            adjusted.loc[stop_triggered] = adjusted.loc[stop_triggered] * 0.5
        return adjusted


class WeakFactorPortfolio:
    """弱因子组合策略完整框架。"""

    def __init__(
        self,
        factors_df: pd.DataFrame,
        target_return: pd.Series,
        target_vol: float = 0.15,
        n_active_factors: int = 120,
        retrain_freq: int = 21,
        market_phases: dict[str, tuple[str | pd.Timestamp, str | pd.Timestamp]] | None = None,
    ):
        self.factors = factors_df.copy()
        self.target = target_return.reindex(self.factors.index)
        self.target_vol = target_vol
        self.n_active = n_active_factors
        self.retrain_freq = retrain_freq
        self.market_phases = market_phases or {
            "full_sample": (self.factors.index.min(), self.factors.index.max())
        }
        self.risk_manager = RiskManager(target_vol=target_vol)
        self.valid_factors: list[str] = []
        self.cyclical_factors: list[str] = []
        self.phase_factor_ic: pd.DataFrame = pd.DataFrame()
        self.phase_factor_ic_detail: pd.DataFrame = pd.DataFrame()
        self.phase_summary: pd.DataFrame = pd.DataFrame()
        self.active_factor_audit: pd.DataFrame = pd.DataFrame()

    def _rolling_ic(self, factor: pd.Series, target: pd.Series, window: int = 60) -> pd.Series:
        """滚动 IC（仅使用 as-of 当日及历史信息）。"""
        # 将因子滞后一期以预测下一期收益，避免在 as-of 日期使用未来收益。
        return factor.shift(1).rolling(window, min_periods=max(20, window // 2)).corr(target)

    def _phase_slice(self, start: str | pd.Timestamp, end: str | pd.Timestamp) -> pd.Index:
        start_ts = pd.Timestamp(start)
        end_ts = pd.Timestamp(end)
        return self.factors.loc[(self.factors.index >= start_ts) & (self.factors.index <= end_ts)].index

    def evaluate_phase_factor_ic(self, window: int = 60) -> pd.DataFrame:
        """分阶段评估每个因子的 IC，输出 phase_factor_ic（阶段 x 因子）。"""
        phase_ic_values: dict[str, dict[str, float]] = {}
        phase_detail_rows: list[dict[str, float | str]] = []

        for phase_name, (start, end) in self.market_phases.items():
            idx = self._phase_slice(start, end)
            phase_ic_values[phase_name] = {}
            for col in self.factors.columns:
                ic_series = self._rolling_ic(self.factors[col], self.target, window=window).reindex(idx).dropna()
                median_abs_ic = float(ic_series.abs().median()) if not ic_series.empty else 0.0
                mean_ic = float(ic_series.mean()) if not ic_series.empty else 0.0
                flip_rate = float((ic_series * ic_series.shift(1) < 0).mean()) if not ic_series.empty else 1.0

                phase_ic_values[phase_name][col] = mean_ic
                phase_detail_rows.append(
                    {
                        "phase": phase_name,
                        "factor": col,
                        "mean_ic": mean_ic,
                        "median_abs_ic": median_abs_ic,
                        "flip_rate": flip_rate,
                        "sample_size": int(ic_series.shape[0]),
                    }
                )

        self.phase_factor_ic = pd.DataFrame(phase_ic_values).T
        self.phase_factor_ic_detail = pd.DataFrame(phase_detail_rows)
        return self.phase_factor_ic

    def prescreen_factors(
        self,
        min_ic: float = 0.02,
        max_flip_rate: float = 0.30,
    ) -> list[str]:
        self.evaluate_phase_factor_ic(window=60)
        valid_factors: list[str] = []
        cyclical_factors: list[str] = []

        phase_detail = self.phase_factor_ic_detail

        for col in self.factors.columns:
            ic_series = self._rolling_ic(self.factors[col], self.target, window=60)
            median_abs_ic = float(ic_series.abs().median()) if not ic_series.dropna().empty else 0.0
            flip_rate = float((ic_series * ic_series.shift(1) < 0).mean()) if not ic_series.dropna().empty else 1.0
            if median_abs_ic >= min_ic and flip_rate <= max_flip_rate:
                valid_factors.append(col)
                continue

            factor_phase = phase_detail[phase_detail["factor"] == col]
            phase_strong = (
                not factor_phase.empty
                and ((factor_phase["median_abs_ic"] >= min_ic) & (factor_phase["flip_rate"] <= max_flip_rate)).any()
            )
            if phase_strong:
                cyclical_factors.append(col)
                valid_factors.append(col)

        self.valid_factors = valid_factors
        self.cyclical_factors = cyclical_factors

        if phase_detail.empty:
            self.phase_summary = pd.DataFrame()
        else:
            summary_rows: list[dict[str, float | str | int]] = []
            for phase_name, grp in phase_detail.groupby("phase"):
                strong_count = int(
                    ((grp["median_abs_ic"] >= min_ic) & (grp["flip_rate"] <= max_flip_rate)).sum()
                )
                summary_rows.append(
                    {
                        "phase": phase_name,
                        "avg_abs_ic": float(grp["median_abs_ic"].mean()),
                        "strong_factor_count": strong_count,
                        "sample_size_median": int(grp["sample_size"].median()),
                    }
                )
            self.phase_summary = pd.DataFrame(summary_rows).set_index("phase")
        return valid_factors

    def _get_active_factors(self, as_of_date: pd.Timestamp) -> list[str]:
        if not self.valid_factors:
            return []
        ic_history = pd.DataFrame(
            {col: self._rolling_ic(self.factors[col], self.target, window=63) for col in self.valid_factors}
        )
        recent = ic_history.loc[:as_of_date].tail(63).mean().abs().sort_values(ascending=False)
        return recent.head(min(self.n_active, len(recent))).index.tolist()

    def _get_current_phase(self, as_of_date: pd.Timestamp) -> str | None:
        for phase_name, (start, end) in self.market_phases.items():
            if pd.Timestamp(start) <= as_of_date <= pd.Timestamp(end):
                return phase_name
        return None

    def _get_phase_priority_factors(self, as_of_date: pd.Timestamp) -> list[str]:
        if self.phase_factor_ic.empty:
            return []
        phase_name = self._get_current_phase(as_of_date)
        if phase_name is None or phase_name not in self.phase_factor_ic.index:
            return []
        phase_rank = self.phase_factor_ic.loc[phase_name].abs().sort_values(ascending=False)
        selected = [c for c in phase_rank.index if c in self.valid_factors]
        return selected[: min(self.n_active, len(selected))]

    def signal_equal_weighted(self, factors_subset: pd.DataFrame) -> pd.Series:
        return strategy_equal_weighted(factors_subset)
    def _build_rebalance_dates(self, index: pd.Index, rebalance_freq: str | int = 21) -> pd.Index:
        """根据频率生成再平衡日期序列。支持交易日步长或时间规则。"""
        if len(index) == 0:
            return index

        if isinstance(rebalance_freq, int):
            if rebalance_freq <= 0:
                raise ValueError("rebalance_freq 为整数时必须 > 0")
            return index[::rebalance_freq]

        if not isinstance(index, pd.DatetimeIndex):
            raise TypeError("rebalance_freq 为字符串规则时，index 必须为 DatetimeIndex")

        grouped = pd.Series(index=index, data=index).groupby(pd.Grouper(freq=rebalance_freq)).last().dropna()
        return pd.Index(grouped.values)

    def build_active_factor_timeline(
        self,
        factors_subset: pd.DataFrame,
        rebalance_freq: str | int = 21,
        audit_top_n: int = 10,
    ) -> tuple[pd.DataFrame, pd.DataFrame]:
        """生成时变 active 因子掩码与再平衡对账表。"""
        if factors_subset.empty:
            empty_mask = pd.DataFrame(index=factors_subset.index, columns=factors_subset.columns, dtype=bool)
            return empty_mask, pd.DataFrame(columns=["rebalance_date", "n_active", "top_factors"])

        rebalance_dates = self._build_rebalance_dates(factors_subset.index, rebalance_freq=rebalance_freq)
        if len(rebalance_dates) == 0 or rebalance_dates[0] != factors_subset.index[0]:
            rebalance_dates = pd.Index([factors_subset.index[0]]).append(rebalance_dates).drop_duplicates()
        if len(rebalance_dates) == 0 or rebalance_dates[-1] != factors_subset.index[-1]:
            rebalance_dates = rebalance_dates.append(pd.Index([factors_subset.index[-1]])).drop_duplicates()

        active_mask = pd.DataFrame(False, index=factors_subset.index, columns=factors_subset.columns)
        audit_rows: list[dict[str, object]] = []

        for i, rebalance_date in enumerate(rebalance_dates):
            active = self._get_active_factors(pd.Timestamp(rebalance_date))
            active = [c for c in active if c in factors_subset.columns]

            start = rebalance_date
            if i + 1 < len(rebalance_dates):
                end = rebalance_dates[i + 1]
                period_idx = factors_subset.index[(factors_subset.index >= start) & (factors_subset.index < end)]
            else:
                period_idx = factors_subset.index[factors_subset.index >= start]

            if len(period_idx) and active:
                active_mask.loc[period_idx, active] = True

            audit_rows.append(
                {
                    "rebalance_date": pd.Timestamp(rebalance_date),
                    "n_active": len(active),
                    "top_factors": ", ".join(active[: max(1, audit_top_n)]),
                }
            )

        audit_df = pd.DataFrame(audit_rows).set_index("rebalance_date")
        return active_mask, audit_df

    def _apply_active_mask(
        self,
        factors_subset: pd.DataFrame,
        active_mask: pd.DataFrame | None = None,
    ) -> pd.DataFrame:
        if active_mask is None:
            return factors_subset
        mask = active_mask.reindex(index=factors_subset.index, columns=factors_subset.columns).fillna(False)
        return factors_subset.where(mask)

    def signal_equal_weighted(
        self,
        factors_subset: pd.DataFrame,
        active_mask: pd.DataFrame | None = None,
    ) -> pd.Series:
        return strategy_equal_weighted(self._apply_active_mask(factors_subset, active_mask=active_mask))

    def signal_risk_parity(
        self,
        factors_subset: pd.DataFrame,
        window: int = 252,
        active_mask: pd.DataFrame | None = None,
    ) -> pd.Series:
        return strategy_risk_parity(
            self._apply_active_mask(factors_subset, active_mask=active_mask),
            window=window,
        )

    def signal_ml(
        self,
        factors_subset: pd.DataFrame,
        active_mask: pd.DataFrame | None = None,
    ) -> pd.Series:
        masked_factors = self._apply_active_mask(factors_subset, active_mask=active_mask)
        return strategy_ml_weighted(
            masked_factors,
            target_return=self.target,
            retrain_freq=self.retrain_freq,
            train_window=500,
            min_train=250,
        )

    def combine_signals(self, s_eq: pd.Series, s_rp: pd.Series, s_ml: pd.Series) -> pd.Series:
        return combine_signals_fixed(s_eq, s_rp, s_ml, weights=(0.4, 0.3, 0.3))

    def apply_risk_management(
        self,
        signal: pd.Series | pd.DataFrame,
        portfolio_return: pd.Series | None = None,
    ) -> pd.Series | pd.DataFrame:
        """根据信号形态路由到对应风控分支。"""
        if isinstance(signal, pd.DataFrame):
            return self.risk_manager.apply_all_cross_section_matrix(
                signal,
                portfolio_return=portfolio_return,
            )
        return self.risk_manager.apply_all(signal, portfolio_return=portfolio_return)

    def run(
        self,
        use_dynamic_factors: bool = True,
        portfolio_return: pd.Series | None = None,
        phase_priority: bool = False,
        rebalance_freq: str | int = 21,
        audit_top_n: int = 10,
        print_audit: bool = True,
    ) -> pd.Series:
        self.prescreen_factors()
        if not self.valid_factors:
            raise ValueError("预筛选后无可用因子，请降低筛选阈值。")

        factors_to_use = self.factors[self.valid_factors]
        active_mask: pd.DataFrame | None = None
        if use_dynamic_factors:
            as_of_date = factors_to_use.index[-1]
            active = self._get_phase_priority_factors(as_of_date) if phase_priority else []
            if not active:
                active = self._get_active_factors(as_of_date)
            if active:
                factors_to_use = factors_to_use[active]
            active_mask, audit_df = self.build_active_factor_timeline(
                factors_to_use,
                rebalance_freq=rebalance_freq,
                audit_top_n=audit_top_n,
            )
            self.active_factor_audit = audit_df
            if print_audit and not audit_df.empty:
                print("[ActiveFactorAudit] 再平衡点 active 因子对账（数量与Top名单）")
                print(audit_df[["n_active", "top_factors"]])
        else:
            self.active_factor_audit = pd.DataFrame()

        s_eq = self.signal_equal_weighted(factors_to_use, active_mask=active_mask)
        s_rp = self.signal_risk_parity(factors_to_use, active_mask=active_mask)
        s_ml = self.signal_ml(factors_to_use, active_mask=active_mask)

        combined = self.combine_signals(s_eq, s_rp, s_ml)
        final = self.apply_risk_management(combined, portfolio_return=portfolio_return)

        if not self.phase_summary.empty:
            print("[Phase Evaluation Summary]")
            print(self.phase_summary.to_string())
            if self.cyclical_factors:
                print(f"[Cyclical Factors Retained] {len(self.cyclical_factors)}")
        return final


def _rolling_normalize(series: pd.Series, window: int = 252) -> pd.Series:
    mean = series.rolling(window, min_periods=max(20, window // 4)).mean()
    std = series.rolling(window, min_periods=max(20, window // 4)).std()
    return (series - mean) / (std + EPS)
