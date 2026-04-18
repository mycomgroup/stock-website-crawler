"""评估指标模块 (Tasks 9.1-9.6)

实现因子层、合成层、组合层评估指标，以及稳健性测试和上线闸门验证。

**Validates: Requirements 10, 11 (P9, P10)**
"""

from __future__ import annotations

import logging
import warnings
from typing import Any

import numpy as np
import pandas as pd
from scipy import stats

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Task 9.1: 因子层评估
# ---------------------------------------------------------------------------


def compute_rank_ic(
    factor: pd.Series,
    label: pd.Series,
) -> float:
    """计算截面 rank IC（Spearman 相关系数）。

    Parameters
    ----------
    factor : pd.Series
        因子值，indexed by (date, stock_id) 或 stock_id。
    label : pd.Series
        标签（下期收益），与 factor 对齐。

    Returns
    -------
    float
        Rank IC（Spearman 相关系数）。
    """
    common_idx = factor.index.intersection(label.index)
    if len(common_idx) < 5:
        return float("nan")

    f = factor.loc[common_idx].dropna()
    l = label.loc[common_idx].dropna()
    common = f.index.intersection(l.index)

    if len(common) < 5:
        return float("nan")

    corr, _ = stats.spearmanr(f.loc[common], l.loc[common])
    return float(corr)


def compute_ic_series(
    factor_panel: pd.DataFrame,
    factor_col: str,
    label_col: str,
) -> pd.Series:
    """计算每个截面日期的 rank IC 时间序列。

    Parameters
    ----------
    factor_panel : pd.DataFrame
        含 date / stock_id / factor_col / label_col 的面板数据。
    factor_col : str
        因子列名。
    label_col : str
        标签列名。

    Returns
    -------
    pd.Series
        IC 时间序列，indexed by date。
    """
    ic_list = []
    for date, group in factor_panel.groupby("date"):
        valid = group[[factor_col, label_col]].dropna()
        if len(valid) < 5:
            continue
        corr, _ = stats.spearmanr(valid[factor_col], valid[label_col])
        ic_list.append({"date": date, "ic": corr})

    if not ic_list:
        return pd.Series(dtype=float)

    ic_df = pd.DataFrame(ic_list).set_index("date")["ic"]
    return ic_df


def compute_icir(ic_series: pd.Series) -> float:
    """计算 ICIR（IC 均值 / IC 标准差）。

    Parameters
    ----------
    ic_series : pd.Series
        IC 时间序列。

    Returns
    -------
    float
        ICIR。
    """
    ic_clean = ic_series.dropna()
    if len(ic_clean) < 2:
        return float("nan")
    std = ic_clean.std()
    if std < 1e-8:
        return float("nan")
    return float(ic_clean.mean() / std)


def compute_monotonic_group_returns(
    factor_panel: pd.DataFrame,
    factor_col: str,
    label_col: str,
    n_groups: int = 5,
) -> pd.DataFrame:
    """计算单调分组收益（分位数组合）。

    Parameters
    ----------
    factor_panel : pd.DataFrame
        含 date / stock_id / factor_col / label_col 的面板数据。
    factor_col : str
        因子列名。
    label_col : str
        标签列名。
    n_groups : int
        分组数（默认 5 分位）。

    Returns
    -------
    pd.DataFrame
        各分组的平均收益，columns = [group_1, ..., group_N, spread]。
    """
    results = []
    for date, group in factor_panel.groupby("date"):
        valid = group[[factor_col, label_col]].dropna()
        if len(valid) < n_groups * 2:
            continue

        valid = valid.copy()
        valid["group"] = pd.qcut(
            valid[factor_col], q=n_groups, labels=False, duplicates="drop"
        )
        group_returns = valid.groupby("group")[label_col].mean()

        row = {"date": date}
        for g in range(n_groups):
            row[f"group_{g+1}"] = group_returns.get(g, float("nan"))

        # Spread: top group - bottom group
        row["spread"] = row.get(f"group_{n_groups}", float("nan")) - row.get(
            "group_1", float("nan")
        )
        results.append(row)

    if not results:
        return pd.DataFrame()

    return pd.DataFrame(results).set_index("date")


def evaluate_factor_layer(
    factor_panel: pd.DataFrame,
    factor_cols: list[str],
    label_col: str = "pchg",
) -> dict:
    """因子层评估：rank IC、ICIR、单调分组收益。

    **Validates: Requirements 10.1**

    Parameters
    ----------
    factor_panel : pd.DataFrame
        含 date / stock_id / factor_cols / label_col 的面板数据。
    factor_cols : list[str]
        待评估的因子列名列表。
    label_col : str
        标签列名（默认 'pchg'）。

    Returns
    -------
    dict
        各因子的评估指标字典。
    """
    results = {}
    for col in factor_cols:
        if col not in factor_panel.columns:
            continue

        ic_series = compute_ic_series(factor_panel, col, label_col)
        mean_ic = float(ic_series.mean()) if len(ic_series) > 0 else float("nan")
        icir = compute_icir(ic_series)

        results[col] = {
            "mean_ic": mean_ic,
            "icir": icir,
            "ic_positive_pct": float((ic_series > 0).mean()) if len(ic_series) > 0 else float("nan"),
        }

    logger.info(
        "因子层评估完成：%d 个因子，平均 IC=%.4f",
        len(results),
        np.nanmean([r["mean_ic"] for r in results.values()]),
    )
    return results


# ---------------------------------------------------------------------------
# Task 9.2: 合成层评估
# ---------------------------------------------------------------------------


def compute_decile_spread(
    alpha: pd.Series,
    label: pd.Series,
) -> float:
    """计算 decile spread（top 10% - bottom 10% 平均收益差）。

    Parameters
    ----------
    alpha : pd.Series
        Alpha 预测，indexed by (date, stock_id)。
    label : pd.Series
        标签，indexed by (date, stock_id)。

    Returns
    -------
    float
        Decile spread（年化）。
    """
    common_idx = alpha.index.intersection(label.index)
    if len(common_idx) < 20:
        return float("nan")

    alpha_clean = alpha.loc[common_idx].dropna()
    label_clean = label.loc[common_idx].dropna()
    common = alpha_clean.index.intersection(label_clean.index)

    if len(common) < 20:
        return float("nan")

    a = alpha_clean.loc[common]
    l = label_clean.loc[common]

    top_10pct = a.quantile(0.9)
    bot_10pct = a.quantile(0.1)

    top_returns = l[a >= top_10pct].mean()
    bot_returns = l[a <= bot_10pct].mean()

    return float(top_returns - bot_returns)


def evaluate_synthesis_layer(
    alpha: pd.Series,
    label: pd.Series,
    family_beta_history: list[pd.Series] | None = None,
) -> dict:
    """合成层评估：OOF rank IC、decile spread、家族权重稳定性。

    **Validates: Requirements 10.2**

    Parameters
    ----------
    alpha : pd.Series
        OOF alpha 预测，indexed by (date, stock_id)。
    label : pd.Series
        标签，indexed by (date, stock_id)。
    family_beta_history : list[pd.Series] | None
        历史家族权重列表（用于稳定性评估）。

    Returns
    -------
    dict
        合成层评估指标。
    """
    # OOF rank IC
    oof_ic = compute_rank_ic(alpha, label)

    # Decile spread
    decile_spread = compute_decile_spread(alpha, label)

    # Family weight stability (if available)
    weight_stability = float("nan")
    if family_beta_history and len(family_beta_history) >= 2:
        changes = []
        for i in range(1, len(family_beta_history)):
            prev = family_beta_history[i - 1]
            curr = family_beta_history[i]
            common = prev.index.intersection(curr.index)
            if len(common) > 0:
                change = (curr.loc[common] - prev.loc[common]).abs().mean()
                changes.append(float(change))
        weight_stability = float(np.mean(changes)) if changes else float("nan")

    result = {
        "oof_rank_ic": oof_ic,
        "decile_spread": decile_spread,
        "family_weight_stability": weight_stability,
    }

    logger.info(
        "合成层评估完成：OOF IC=%.4f, decile spread=%.4f",
        oof_ic,
        decile_spread,
    )
    return result


# ---------------------------------------------------------------------------
# Task 9.3: 组合层评估
# ---------------------------------------------------------------------------


def compute_portfolio_returns(
    weights_history: list[pd.Series],
    price_returns: pd.DataFrame,
    transaction_cost: float = 0.002,
) -> pd.Series:
    """计算组合收益时间序列（税费后）。

    Parameters
    ----------
    weights_history : list[pd.Series]
        每个再平衡日的权重 Series 列表（indexed by stock_id）。
    price_returns : pd.DataFrame
        价格收益矩阵，index=date, columns=stock_id。
    transaction_cost : float
        单边交易成本（默认 0.2%）。

    Returns
    -------
    pd.Series
        税费后组合收益时间序列。
    """
    portfolio_returns = []

    for i, weights in enumerate(weights_history):
        if i >= len(price_returns):
            break

        date = price_returns.index[i]
        common_stocks = weights.index.intersection(price_returns.columns)

        if len(common_stocks) == 0:
            portfolio_returns.append({"date": date, "return": 0.0})
            continue

        # Gross return
        gross_return = (
            weights.loc[common_stocks] * price_returns.loc[date, common_stocks]
        ).sum()

        # Transaction cost
        if i > 0:
            prev_weights = weights_history[i - 1].reindex(weights.index, fill_value=0.0)
            turnover = (weights - prev_weights).abs().sum() / 2
            cost = turnover * transaction_cost
        else:
            cost = weights.sum() * transaction_cost

        net_return = gross_return - cost
        portfolio_returns.append({"date": date, "return": net_return})

    if not portfolio_returns:
        return pd.Series(dtype=float)

    df = pd.DataFrame(portfolio_returns).set_index("date")["return"]
    return df


def compute_sharpe_ratio(
    returns: pd.Series,
    risk_free_rate: float = 0.0,
    periods_per_year: int = 52,
) -> float:
    """计算年化 Sharpe 比率。

    Parameters
    ----------
    returns : pd.Series
        收益时间序列（周频）。
    risk_free_rate : float
        年化无风险利率（默认 0）。
    periods_per_year : int
        每年期数（默认 52 周）。

    Returns
    -------
    float
        年化 Sharpe 比率。
    """
    clean = returns.dropna()
    if len(clean) < 2:
        return float("nan")

    excess = clean - risk_free_rate / periods_per_year
    std = excess.std()
    if std < 1e-8:
        return float("nan")

    return float(excess.mean() / std * np.sqrt(periods_per_year))


def compute_max_drawdown(returns: pd.Series) -> float:
    """计算最大回撤。

    Parameters
    ----------
    returns : pd.Series
        收益时间序列。

    Returns
    -------
    float
        最大回撤（负数）。
    """
    clean = returns.dropna()
    if len(clean) == 0:
        return float("nan")

    cumulative = (1 + clean).cumprod()
    rolling_max = cumulative.cummax()
    drawdown = (cumulative - rolling_max) / rolling_max
    return float(drawdown.min())


def evaluate_portfolio_layer(
    returns: pd.Series,
    weights_history: list[pd.Series] | None = None,
) -> dict:
    """组合层评估：税费后 Sharpe/IR、最大回撤、月度胜率、换手率。

    **Validates: Requirements 10.3**

    Parameters
    ----------
    returns : pd.Series
        税费后组合收益时间序列。
    weights_history : list[pd.Series] | None
        权重历史（用于计算换手率）。

    Returns
    -------
    dict
        组合层评估指标。
    """
    sharpe = compute_sharpe_ratio(returns)
    max_dd = compute_max_drawdown(returns)

    # Monthly win rate (approximate: weekly returns > 0)
    clean = returns.dropna()
    win_rate = float((clean > 0).mean()) if len(clean) > 0 else float("nan")

    # Average turnover
    avg_turnover = float("nan")
    if weights_history and len(weights_history) >= 2:
        turnovers = []
        for i in range(1, len(weights_history)):
            prev = weights_history[i - 1]
            curr = weights_history[i]
            all_stocks = prev.index.union(curr.index)
            p = prev.reindex(all_stocks, fill_value=0.0)
            c = curr.reindex(all_stocks, fill_value=0.0)
            turnovers.append(float((c - p).abs().sum() / 2))
        avg_turnover = float(np.mean(turnovers))

    result = {
        "sharpe_ratio": sharpe,
        "max_drawdown": max_dd,
        "win_rate": win_rate,
        "avg_turnover": avg_turnover,
        "annualized_return": float(clean.mean() * 52) if len(clean) > 0 else float("nan"),
    }

    logger.info(
        "组合层评估完成：Sharpe=%.3f, MaxDD=%.3f, WinRate=%.1f%%",
        sharpe,
        max_dd,
        win_rate * 100,
    )
    return result


# ---------------------------------------------------------------------------
# Task 9.4: 稳健性测试 (P9)
# ---------------------------------------------------------------------------


def test_robustness_drop_top_factors(
    factor_panel: pd.DataFrame,
    factor_cols: list[str],
    label_col: str = "pchg",
    drop_pct: float = 0.10,
    threshold: float = 0.80,
) -> dict:
    """P9: 删掉最强 10% 因子后的 OOF IC 衰减测试。

    **Validates: Requirements 11.9 (P9)**

    Parameters
    ----------
    factor_panel : pd.DataFrame
        含 date / stock_id / factor_cols / label_col 的面板数据。
    factor_cols : list[str]
        所有因子列名。
    label_col : str
        标签列名。
    drop_pct : float
        删除比例（默认 10%）。
    threshold : float
        IC 保留比例阈值（默认 0.80，即 IC(top_90%) / IC(all) > 0.80）。

    Returns
    -------
    dict
        稳健性测试结果，包含：
        - "ic_all": 全因子 IC
        - "ic_top90": 删掉最强 10% 后的 IC
        - "ratio": ic_top90 / ic_all
        - "passes": 是否通过（ratio > threshold）
    """
    # Compute IC for each factor
    factor_ics = {}
    for col in factor_cols:
        if col not in factor_panel.columns:
            continue
        ic_series = compute_ic_series(factor_panel, col, label_col)
        factor_ics[col] = abs(ic_series.mean()) if len(ic_series) > 0 else 0.0

    if not factor_ics:
        return {"ic_all": float("nan"), "ic_top90": float("nan"), "ratio": float("nan"), "passes": False}

    # Sort by IC, drop top drop_pct
    sorted_factors = sorted(factor_ics.items(), key=lambda x: x[1], reverse=True)
    n_drop = max(1, int(len(sorted_factors) * drop_pct))
    top_factors = [f for f, _ in sorted_factors]
    remaining_factors = top_factors[n_drop:]  # drop top n_drop

    # Compute IC for all factors (equal-weight composite)
    all_ic_series = compute_ic_series(
        factor_panel.assign(
            composite_all=factor_panel[top_factors].rank(axis=1, pct=True).mean(axis=1)
        ),
        "composite_all",
        label_col,
    )
    ic_all = float(all_ic_series.mean()) if len(all_ic_series) > 0 else float("nan")

    # Compute IC for remaining factors
    if remaining_factors:
        remaining_ic_series = compute_ic_series(
            factor_panel.assign(
                composite_top90=factor_panel[remaining_factors].rank(axis=1, pct=True).mean(axis=1)
            ),
            "composite_top90",
            label_col,
        )
        ic_top90 = float(remaining_ic_series.mean()) if len(remaining_ic_series) > 0 else float("nan")
    else:
        ic_top90 = float("nan")

    ratio = ic_top90 / ic_all if abs(ic_all) > 1e-8 else float("nan")
    passes = ratio > threshold if not np.isnan(ratio) else False

    result = {
        "ic_all": ic_all,
        "ic_top90": ic_top90,
        "ratio": ratio,
        "passes": passes,
        "n_factors_total": len(top_factors),
        "n_factors_dropped": n_drop,
        "n_factors_remaining": len(remaining_factors),
    }

    logger.info(
        "P9 稳健性测试：IC(all)=%.4f, IC(top90%%)=%.4f, ratio=%.3f, passes=%s",
        ic_all,
        ic_top90,
        ratio,
        passes,
    )
    return result


# ---------------------------------------------------------------------------
# Task 9.5: 延迟执行测试 (P10)
# ---------------------------------------------------------------------------


def test_execution_delay(
    weights_history: list[pd.Series],
    price_returns: pd.DataFrame,
    delay_periods: int = 1,
    transaction_cost: float = 0.002,
    threshold: float = 0.85,
) -> dict:
    """P10: 延迟执行测试（延迟 1 天后的 Sharpe 衰减）。

    **Validates: Requirements 11.10 (P10)**

    Parameters
    ----------
    weights_history : list[pd.Series]
        每个再平衡日的权重 Series 列表。
    price_returns : pd.DataFrame
        价格收益矩阵，index=date, columns=stock_id。
    delay_periods : int
        延迟期数（默认 1 周）。
    transaction_cost : float
        单边交易成本（默认 0.2%）。
    threshold : float
        Sharpe 保留比例阈值（默认 0.85）。

    Returns
    -------
    dict
        延迟执行测试结果，包含：
        - "sharpe_no_delay": 无延迟 Sharpe
        - "sharpe_with_delay": 延迟后 Sharpe
        - "ratio": sharpe_with_delay / sharpe_no_delay
        - "passes": 是否通过（ratio > threshold）
    """
    # No delay
    returns_no_delay = compute_portfolio_returns(
        weights_history, price_returns, transaction_cost
    )
    sharpe_no_delay = compute_sharpe_ratio(returns_no_delay)

    # With delay: shift weights by delay_periods
    delayed_weights = weights_history[:-delay_periods] if delay_periods > 0 else weights_history
    delayed_returns_df = price_returns.iloc[delay_periods:]

    returns_with_delay = compute_portfolio_returns(
        delayed_weights, delayed_returns_df, transaction_cost
    )
    sharpe_with_delay = compute_sharpe_ratio(returns_with_delay)

    ratio = (
        sharpe_with_delay / sharpe_no_delay
        if abs(sharpe_no_delay) > 1e-8
        else float("nan")
    )
    passes = ratio > threshold if not np.isnan(ratio) else False

    result = {
        "sharpe_no_delay": sharpe_no_delay,
        "sharpe_with_delay": sharpe_with_delay,
        "ratio": ratio,
        "passes": passes,
        "delay_periods": delay_periods,
    }

    logger.info(
        "P10 延迟执行测试：Sharpe(no_delay)=%.3f, Sharpe(delay=%d)=%.3f, ratio=%.3f, passes=%s",
        sharpe_no_delay,
        delay_periods,
        sharpe_with_delay,
        ratio,
        passes,
    )
    return result


# ---------------------------------------------------------------------------
# Task 9.6: 上线闸门验证
# ---------------------------------------------------------------------------


def check_production_gates(
    portfolio_metrics: dict,
    robustness_p9: dict,
    delay_p10: dict,
    holdout_ic: float | None = None,
    research_oos_ic: float | None = None,
) -> dict:
    """验证 6 项上线闸门。

    **Validates: Requirements 10.5**

    上线闸门（全部通过才允许上线）：
    1. 税费后结果成立（Sharpe > 0.5）
    2. 延迟执行 1 天后结果仍成立（P10 ratio > 0.85）
    3. 容量测试不过度衰减（暂用 P9 代理）
    4. 风险暴露可解释且可控（暂用 Sharpe > 0 代理）
    5. 参数扰动后不脆弱（P9 ratio > 0.80）
    6. final holdout 不弱于 research OOS 的可接受区间

    Parameters
    ----------
    portfolio_metrics : dict
        组合层评估指标（来自 evaluate_portfolio_layer）。
    robustness_p9 : dict
        P9 稳健性测试结果。
    delay_p10 : dict
        P10 延迟执行测试结果。
    holdout_ic : float | None
        Final holdout 上的 OOF IC。
    research_oos_ic : float | None
        Research OOS 上的 OOF IC。

    Returns
    -------
    dict
        上线闸门验证结果，包含各闸门状态和总体结论。
    """
    gates = {}

    # Gate 1: 税费后结果成立
    sharpe = portfolio_metrics.get("sharpe_ratio", float("nan"))
    gates["gate_1_after_cost"] = {
        "description": "税费后 Sharpe > 0.5",
        "value": sharpe,
        "threshold": 0.5,
        "passes": sharpe > 0.5 if not np.isnan(sharpe) else False,
    }

    # Gate 2: 延迟执行成立
    delay_ratio = delay_p10.get("ratio", float("nan"))
    gates["gate_2_execution_delay"] = {
        "description": "延迟执行 Sharpe 保留率 > 0.85",
        "value": delay_ratio,
        "threshold": 0.85,
        "passes": delay_p10.get("passes", False),
    }

    # Gate 3: 容量测试（用 P9 代理：删掉最强因子后 IC 保留率）
    p9_ratio = robustness_p9.get("ratio", float("nan"))
    gates["gate_3_capacity"] = {
        "description": "删掉最强 10% 因子后 IC 保留率 > 0.80",
        "value": p9_ratio,
        "threshold": 0.80,
        "passes": robustness_p9.get("passes", False),
    }

    # Gate 4: 风险暴露可控（Sharpe > 0 代理）
    gates["gate_4_risk_exposure"] = {
        "description": "税费后 Sharpe > 0（风险暴露可控代理）",
        "value": sharpe,
        "threshold": 0.0,
        "passes": sharpe > 0.0 if not np.isnan(sharpe) else False,
    }

    # Gate 5: 参数扰动不脆弱（P9）
    gates["gate_5_robustness"] = {
        "description": "P9 IC 保留率 > 0.80",
        "value": p9_ratio,
        "threshold": 0.80,
        "passes": robustness_p9.get("passes", False),
    }

    # Gate 6: Final holdout 不弱于 research OOS
    if holdout_ic is not None and research_oos_ic is not None:
        holdout_ratio = holdout_ic / research_oos_ic if abs(research_oos_ic) > 1e-8 else float("nan")
        gate_6_passes = holdout_ratio > 0.7 if not np.isnan(holdout_ratio) else False
        gates["gate_6_holdout"] = {
            "description": "Final holdout IC / Research OOS IC > 0.70",
            "value": holdout_ratio,
            "threshold": 0.70,
            "passes": gate_6_passes,
        }
    else:
        gates["gate_6_holdout"] = {
            "description": "Final holdout IC / Research OOS IC > 0.70",
            "value": float("nan"),
            "threshold": 0.70,
            "passes": None,  # Not evaluated
        }

    # Overall verdict
    evaluated_gates = [g for g in gates.values() if g["passes"] is not None]
    all_pass = all(g["passes"] for g in evaluated_gates)
    n_pass = sum(1 for g in evaluated_gates if g["passes"])
    n_total = len(evaluated_gates)

    result = {
        "gates": gates,
        "all_pass": all_pass,
        "n_pass": n_pass,
        "n_total": n_total,
        "verdict": "PASS" if all_pass else "FAIL",
    }

    logger.info(
        "上线闸门验证：%d/%d 通过，总体结论=%s",
        n_pass,
        n_total,
        result["verdict"],
    )

    if not all_pass:
        failed = [name for name, g in gates.items() if g["passes"] is False]
        logger.warning("未通过的闸门：%s", failed)

    return result
