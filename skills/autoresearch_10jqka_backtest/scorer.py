"""
问财公式回测结果评分系统 v4 - 多窗口鲁棒评分版

用于解析问财平台回测结果，计算目标函数得分，并决策 keep/rollback。
"""

from dataclasses import dataclass
from typing import Optional
import math
import re

MAX_OVERFIT_PENALTY = 1.5


@dataclass
class WindowMetrics:
    """单窗口回测指标数据类，包含窗口名称标识。"""

    window_name: str
    status: str
    backtest_id: str
    total_return: float
    annual_return: float
    max_drawdown: float
    sharpe: float
    sortino: float
    information_ratio: float
    win_rate: float
    avg_holding_days: float
    trade_count: int
    max_positions: int = 0
    daily_buy_count: int = 0


@dataclass
class ParsedMetrics:
    """解析后的回测指标数据类（向后兼容）。"""

    status: str
    backtest_id: str
    total_return: float
    annual_return: float
    max_drawdown: float
    sharpe: float
    sortino: float
    information_ratio: float
    win_rate: float
    avg_holding_days: float
    trade_count: int
    max_positions: int = 0
    daily_buy_count: int = 0
    window_name: str = ""


def _safe_float(value, default: float = 0.0) -> float:
    if value is None:
        return default
    try:
        return float(value)
    except (TypeError, ValueError):
        return default


def _safe_int(value, default: int = 0) -> int:
    if value is None:
        return default
    try:
        return int(value)
    except (TypeError, ValueError):
        return default


def _extract_nested_value(data: dict, *paths: tuple) -> Optional[object]:
    for path in paths:
        current = data
        found = True
        for key in path:
            if isinstance(current, dict) and key in current:
                current = current[key]
            else:
                found = False
                break
        if found and current is not None:
            return current
    return None


def _select_raw_backtest_variant(result_json: dict) -> dict:
    raw_result = _extract_nested_value(
        result_json,
        ("full_result", "raw", "result"),
        ("raw", "result"),
        ("full_result", "result"),
    )
    if not isinstance(raw_result, dict):
        return {}

    backtest_data = raw_result.get("backtestData")
    if not isinstance(backtest_data, list) or not backtest_data:
        return {}

    report_data = raw_result.get("reportData", {}) if isinstance(raw_result.get("reportData"), dict) else {}
    preferred_strategy = None
    max_annual = report_data.get("maxAnnualYield")
    if isinstance(max_annual, list) and len(max_annual) >= 2:
        preferred_strategy = _safe_int(max_annual[1], default=-1)

    if preferred_strategy is not None and preferred_strategy >= 0:
        for item in backtest_data:
            if _safe_int(item.get("daySaleStrategy"), default=-1) == preferred_strategy:
                return item

    return max(backtest_data, key=lambda item: _safe_float(item.get("annualYield"), default=-1e9))


def _should_prefer_raw(summary_value: float, raw_value: float) -> bool:
    if raw_value == 0:
        return False
    if summary_value == 0:
        return True
    if summary_value in (0.0, 1.0) and abs(raw_value - summary_value) > 0.05:
        return True
    return False


def parse_backtest_result(result_json: dict, window_name: str = "") -> ParsedMetrics:
    """
    解析问财回测结果 JSON，优先使用 summary，必要时回退到原始 raw.backtestData。
    """
    status = str(
        result_json.get("status")
        or _extract_nested_value(result_json, ("full_result", "status"))
        or ""
    )

    summary = result_json.get("summary", {}) if isinstance(result_json.get("summary"), dict) else {}
    full_result = result_json.get("full_result", {}) if isinstance(result_json.get("full_result"), dict) else {}
    raw_config = full_result.get("config", {}) if isinstance(full_result.get("config"), dict) else {}
    raw_variant = _select_raw_backtest_variant(result_json)

    max_positions = _safe_int(raw_config.get("stock_hold"))
    if max_positions <= 0:
        max_positions = _safe_int(raw_config.get("maxPositions"))

    daily_buy_count = _safe_int(raw_config.get("day_buy_stock_num"))
    if daily_buy_count <= 0:
        daily_buy_count = _safe_int(raw_config.get("dailyBuyCount"))

    annual_return_summary = _safe_float(summary.get("annualReturn"))
    annual_return_raw = _safe_float(raw_variant.get("annualYield"))
    annual_return = annual_return_raw if _should_prefer_raw(annual_return_summary, annual_return_raw) else annual_return_summary

    total_return_summary = _safe_float(summary.get("totalReturn"))
    total_return = total_return_summary
    if total_return == 0 and annual_return_raw != 0:
        total_return = annual_return_raw

    max_drawdown_summary = _safe_float(summary.get("maxDrawdown"))
    max_drawdown_raw = _safe_float(raw_variant.get("maxDrawDown"))
    max_drawdown = max_drawdown_raw if max_drawdown_summary <= 0 and max_drawdown_raw > 0 else max_drawdown_summary

    sharpe_summary = _safe_float(summary.get("sharpe"))
    sharpe_raw = _safe_float(raw_variant.get("sharpeRatio"))
    sharpe = sharpe_raw if sharpe_summary == 0 and sharpe_raw != 0 else sharpe_summary

    sortino = _safe_float(summary.get("sortino"))
    information_ratio = _safe_float(summary.get("informationRatio"))

    win_rate_summary = _safe_float(summary.get("winRate"))
    win_rate_raw = _safe_float(raw_variant.get("winRate"))
    win_rate = win_rate_raw if win_rate_summary == 0 and win_rate_raw != 0 else win_rate_summary

    avg_holding_days = _safe_float(summary.get("avgHoldingDays"))
    if avg_holding_days <= 0 and raw_variant:
        avg_holding_days = _safe_float(raw_variant.get("daySaleStrategy"))

    trade_count_summary = _safe_int(summary.get("tradeCount"))
    trade_count_raw = _safe_int(raw_variant.get("totalTradeTimes"))
    trade_count = trade_count_summary if trade_count_summary > 0 else trade_count_raw

    return ParsedMetrics(
        status=status,
        backtest_id=str(result_json.get("backtest_id", "")),
        total_return=total_return,
        annual_return=annual_return,
        max_drawdown=max_drawdown,
        sharpe=sharpe,
        sortino=sortino,
        information_ratio=information_ratio,
        win_rate=win_rate,
        avg_holding_days=avg_holding_days,
        trade_count=trade_count,
        max_positions=max_positions,
        daily_buy_count=daily_buy_count,
        window_name=window_name,
    )


def validate_result(metrics: ParsedMetrics) -> tuple[bool, str]:
    """硬门槛验证：检查回测结果是否有效。"""
    if not metrics.status:
        return False, "status is empty"

    if metrics.status.lower() not in {"ok", "success", "completed", "done", "finished"}:
        if "error" in metrics.status.lower():
            return False, f"backtest failed with status: {metrics.status}"

    if not metrics.backtest_id:
        return False, "backtest_id is missing"

    return True, ""


def _cap_score(value: float, cap: float) -> float:
    return max(-cap, min(cap, value))


def _compute_trade_count_penalty(trade_count: int) -> float:
    if trade_count >= 20:
        return 0.0
    if trade_count >= 10:
        return (20 - trade_count) * 0.05
    return (20 - trade_count) * 0.15


def _compute_concentration_penalty(max_positions: int) -> float:
    if max_positions >= 5:
        return 0.0
    if max_positions == 4:
        return 0.3
    if max_positions == 3:
        return 0.8
    if max_positions == 2:
        return 1.5
    return 2.5


def _compute_sensitivity_penalty(neighbor_scores: list[float]) -> float:
    if len(neighbor_scores) < 2:
        return 0.0

    mean = sum(neighbor_scores) / len(neighbor_scores)
    if abs(mean) < 0.01:
        return 0.0

    variance = sum((s - mean) ** 2 for s in neighbor_scores) / len(neighbor_scores)
    std_dev = math.sqrt(variance)
    coefficient_of_variation = abs(std_dev / mean)

    if coefficient_of_variation > 1.5:
        return 1.0
    if coefficient_of_variation > 1.0:
        return 0.5
    if coefficient_of_variation > 0.5:
        return 0.2
    return 0.0


def _compute_duplicate_penalty(formula: list[str]) -> float:
    if len(formula) <= 1:
        return 0.0

    from formula_mutator import canonicalize_formula

    canonical = canonicalize_formula(formula)
    unique_conditions = set(canonical)
    duplicate_ratio = 1.0 - (len(unique_conditions) / len(formula))
    return duplicate_ratio * 1.5


def calculate_window_score(metrics: ParsedMetrics) -> float:
    capped_annual_return = _cap_score(metrics.annual_return, 3.0)

    max_d = abs(metrics.max_drawdown)
    if max_d < 0.01:
        max_d = 0.01
    capped_calmar = _cap_score(metrics.annual_return / max_d, 5.0)

    capped_sortino = _cap_score(metrics.sortino, 3.0)
    capped_information_ratio = _cap_score(metrics.information_ratio, 3.0)

    score = (
        capped_sortino * 0.35
        + capped_calmar * 0.30
        + capped_information_ratio * 0.15
        + metrics.win_rate * 0.10
    )

    if metrics.trade_count >= 20:
        score += 0.05
    elif metrics.trade_count < 10:
        score -= 0.15

    if metrics.avg_holding_days > 0:
        if metrics.avg_holding_days < 3:
            score -= 0.1
        elif metrics.avg_holding_days > 60:
            score -= 0.1

    return score


def calculate_robust_score_multi_window(
    results_by_window: dict[str, dict],
    neighbor_scores: Optional[list[float]] = None,
    formula: Optional[list[str]] = None,
    config: Optional[dict] = None,
) -> float:
    """多窗口加权鲁棒评分。"""
    window_weights = {
        "recent_6m": 0.35,
        "recent_12m": 0.35,
        "prior_12m": 0.15,
        "full_24m": 0.15,
    }

    weighted_score = 0.0
    total_weight = 0.0
    primary_metrics = None

    for window_name, weight in window_weights.items():
        if window_name not in results_by_window:
            continue

        data = results_by_window[window_name]
        metrics = data.get("metrics") if isinstance(data, dict) and "metrics" in data else data
        if isinstance(metrics, dict) and not isinstance(metrics, ParsedMetrics):
            metrics = ParsedMetrics(**metrics)

        if not isinstance(metrics, ParsedMetrics):
            continue

        weighted_score += calculate_window_score(metrics) * weight
        total_weight += weight

        if window_name == "recent_12m":
            primary_metrics = metrics

    if total_weight == 0:
        return 0.0

    weighted_score /= total_weight

    if primary_metrics is None:
        for data in results_by_window.values():
            metrics = data.get("metrics") if isinstance(data, dict) and "metrics" in data else data
            if isinstance(metrics, dict) and not isinstance(metrics, ParsedMetrics):
                metrics = ParsedMetrics(**metrics)
            if isinstance(metrics, ParsedMetrics):
                primary_metrics = metrics
                break

    penalty_sensitivity = _compute_sensitivity_penalty(neighbor_scores or [])
    penalty_duplicate = 0.0
    penalty_complexity = 0.0
    penalty_concentration = 0.0
    penalty_trade_count = 0.0

    if config is not None:
        penalty_complexity = min(calculate_complexity(config) / 10.0, 1.0) * DEFAULT_WEIGHTS.get("complexity_penalty", 0.10)
        if formula is None:
            formula = config.get("formula", [])

    if formula is not None:
        penalty_duplicate = _compute_duplicate_penalty(formula)

    if primary_metrics is not None:
        max_positions = primary_metrics.max_positions
        if max_positions <= 0 and config:
            max_positions = _safe_int(config.get("maxPositions"))
        penalty_concentration = _compute_concentration_penalty(max_positions)
        penalty_trade_count = _compute_trade_count_penalty(primary_metrics.trade_count)

    return (
        weighted_score
        - penalty_sensitivity
        - penalty_complexity
        - penalty_concentration
        - penalty_duplicate
        - penalty_trade_count
    )


def calculate_score(
    metrics: ParsedMetrics,
    weights: Optional[dict] = None,
    complexity: int = 0,
    config: Optional[dict] = None,
) -> float:
    """计算复合目标函数得分（单窗口版，向后兼容）。"""
    if weights is None:
        weights = DEFAULT_WEIGHTS

    capped_annual_return = _cap_score(metrics.annual_return, 3.0)

    max_d = abs(metrics.max_drawdown)
    if max_d < 0.01:
        max_d = 0.01
    capped_calmar = _cap_score(metrics.annual_return / max_d, 5.0)

    capped_sortino = _cap_score(metrics.sortino, 3.0)
    capped_information_ratio = _cap_score(metrics.information_ratio, 3.0)

    complexity_penalty = min(complexity / 10.0, 1.0)

    max_positions = metrics.max_positions
    if max_positions <= 0 and config:
        max_positions = _safe_int(config.get("maxPositions"))

    concentration_penalty = _compute_concentration_penalty(max_positions)
    trade_count_penalty = _compute_trade_count_penalty(metrics.trade_count)
    overfit_penalty = calculate_overfit_penalty(metrics, max_positions)

    score = (
        capped_sortino * weights.get("sortino", 0.35)
        + capped_calmar * weights.get("calmar", 0.30)
        + capped_information_ratio * weights.get("information_ratio", 0.15)
        + metrics.win_rate * weights.get("win_rate", 0.10)
        - trade_count_penalty
        - concentration_penalty
        - complexity_penalty * weights.get("complexity_penalty", 0.10)
        - overfit_penalty
    )
    return score


def calculate_complexity(config: dict) -> int:
    """计算配置复杂度。"""
    formula = config.get("formula", [])
    if isinstance(formula, str):
        formula = [formula]

    formula_count = len(formula)
    tuning_params = [
        "takeProfit",
        "stopLoss",
        "trailingStopLoss",
        "maxPositions",
        "dailyBuyCount",
        "daysForSaleStrategy",
    ]
    params_count = sum(1 for p in tuning_params if p in config and config[p] is not None)
    return formula_count + params_count


def classify_direction_status(
    recent6_score: float,
    recent12_score: float,
    baseline_scores: Optional[dict] = None,
) -> tuple[str, str, float]:
    """基于 recent_6m / recent_12m 相对 baseline 的表现判断方向状态。"""
    baseline_scores = baseline_scores or {}
    baseline6 = _safe_float(baseline_scores.get("recent_6m"), 0.0)
    baseline12 = _safe_float(baseline_scores.get("recent_12m"), 0.0)

    env_slack = max(0.08, 0.15 * abs(baseline12 - baseline6))
    recent_floor = -0.15

    if (
        recent6_score < baseline6 - env_slack
        and recent12_score < baseline12 - env_slack
        and recent6_score <= recent_floor
        and recent12_score <= recent_floor
    ):
        return "INACTIVE", "recent_6m 和 recent_12m 均明显低于 baseline", env_slack

    if (
        recent6_score >= baseline6 - env_slack
        and recent12_score >= baseline12 - env_slack
        and max(recent6_score, recent12_score) > recent_floor
    ):
        return "ACTIVE", "recent_6m / recent_12m 均未明显弱于 baseline", env_slack

    return "WATCH", "近期仍有信号，但相对 baseline 不够稳定", env_slack


def check_hard_constraints(
    metrics_by_window: dict[str, ParsedMetrics],
    champion_robust_score: Optional[float] = None,
    config: Optional[dict] = None,
) -> tuple[bool, str, str]:
    """检查硬约束。"""
    primary_metrics = metrics_by_window.get("recent_12m") or metrics_by_window.get("recent_6m")
    if primary_metrics is None:
        for metric in metrics_by_window.values():
            primary_metrics = metric
            break

    if primary_metrics is None:
        return True, "keep", "no metrics available for hard constraint check"

    primary_limit = DEFAULT_HARD_CONSTRAINTS.get("primary_max_drawdown_limit", 0.25)
    if abs(primary_metrics.max_drawdown) > primary_limit:
        return False, "rollback", f"primary window max_drawdown {abs(primary_metrics.max_drawdown):.4f} exceeds {primary_limit:.2f}"

    recent12m = metrics_by_window.get("recent_12m")
    if recent12m and recent12m.trade_count < DEFAULT_HARD_CONSTRAINTS.get("recent_12m_min_trade_count", 20):
        return False, "rollback", f"recent_12m trade_count {recent12m.trade_count} < 20"

    recent6m = metrics_by_window.get("recent_6m")
    if recent6m and recent6m.trade_count < DEFAULT_HARD_CONSTRAINTS.get("recent_6m_min_trade_count", 8):
        return False, "rollback", f"recent_6m trade_count {recent6m.trade_count} < 8"

    if recent6m and recent12m and recent6m.annual_return <= 0 and recent12m.annual_return <= 0:
        return False, "rollback", "recent_6m 和 recent_12m 均无正收益"

    full24m = metrics_by_window.get("full_24m")
    if full24m and abs(full24m.max_drawdown) > DEFAULT_HARD_CONSTRAINTS.get("full_24m_max_drawdown_limit", 0.30):
        return False, "rollback", f"full_24m max_drawdown {abs(full24m.max_drawdown):.4f} exceeds 0.30"

    max_positions = primary_metrics.max_positions
    if max_positions <= 0 and config:
        max_positions = _safe_int(config.get("maxPositions"))

    if 0 < max_positions < DEFAULT_HARD_CONSTRAINTS.get("min_max_positions", 4):
        return False, "rollback", f"maxPositions {max_positions} < 4"

    return True, "keep", "passed all hard constraints"


def decide_keep_rollback(
    new_score: float,
    champion_score: float,
    new_metrics: ParsedMetrics,
    champion_metrics: Optional[ParsedMetrics],
    hard_constraints: Optional[dict] = None,
    new_robust_score: Optional[float] = None,
    champion_robust_score: Optional[float] = None,
    epsilon_absolute: float = 0.15,
    epsilon_relative: float = 0.03,
) -> tuple[str, str]:
    """决策是 keep 还是 rollback（使用 epsilon 比较的升级版）。"""
    if hard_constraints is None:
        hard_constraints = DEFAULT_HARD_CONSTRAINTS

    is_valid, validation_msg = validate_result(new_metrics)
    if not is_valid:
        return "rollback", f"backtest failed: {validation_msg}"

    max_drawdown_limit = hard_constraints.get("max_drawdown_limit", 0.25)
    if abs(new_metrics.max_drawdown) > max_drawdown_limit:
        return "rollback", f"max_drawdown {abs(new_metrics.max_drawdown):.4f} exceeds limit {max_drawdown_limit:.4f}"

    if champion_metrics is None:
        if champion_score in (-1e308, float("-inf")):
            return "keep", "first version, automatically champion"
        if new_score > champion_score:
            return "keep", f"new_score {new_score:.6f} > champion_score {champion_score:.6f}"
        return "rollback", f"new_score {new_score:.6f} <= champion_score {champion_score:.6f}"

    if new_robust_score is not None and champion_robust_score is not None:
        score_diff = new_robust_score - champion_robust_score
        relative_diff = score_diff / abs(champion_robust_score) if champion_robust_score != 0 else 0

        if score_diff >= epsilon_absolute or relative_diff >= epsilon_relative:
            return "keep", (
                f"robust_score {new_robust_score:.6f} > champion {champion_robust_score:.6f} "
                f"(diff: {score_diff:.6f}, relative: {relative_diff:.4f})"
            )

        new_complexity = calculate_complexity_from_metrics(new_metrics)
        champion_complexity = calculate_complexity_from_metrics(champion_metrics)

        if new_complexity < champion_complexity and abs(score_diff) < epsilon_absolute:
            return "keep", (
                f"new config is simpler ({new_complexity} < {champion_complexity}) "
                f"and scores are close (diff: {score_diff:.6f})"
            )

        if score_diff < 0 and abs(score_diff) < epsilon_absolute:
            return "rollback", (
                f"robust_score {new_robust_score:.6f} <= champion {champion_robust_score:.6f} "
                f"(diff: {score_diff:.6f})"
            )

    if new_score > champion_score:
        score_diff = new_score - champion_score
        return "keep", f"new_score {new_score:.6f} > champion_score {champion_score:.6f} (diff: {score_diff:.6f})"

    score_diff = new_score - champion_score
    return "rollback", f"new_score {new_score:.6f} <= champion_score {champion_score:.6f} (diff: {score_diff:.6f})"


def calculate_complexity_from_metrics(metrics: ParsedMetrics, config: Optional[dict] = None) -> int:
    if config:
        return calculate_complexity(config)
    base = 1
    if metrics.max_positions > 0:
        base += 1
    if metrics.daily_buy_count > 0:
        base += 1
    return base


DEFAULT_WEIGHTS = {
    "sortino": 0.35,
    "calmar": 0.30,
    "information_ratio": 0.15,
    "win_rate": 0.10,
    "complexity_penalty": 0.10,
}

DEFAULT_HARD_CONSTRAINTS = {
    "max_drawdown_limit": 0.25,
    "primary_max_drawdown_limit": 0.25,
    "full_24m_max_drawdown_limit": 0.30,
    "recent_12m_min_trade_count": 20,
    "recent_6m_min_trade_count": 8,
    "min_max_positions": 4,
}


def calculate_overfit_penalty(metrics: ParsedMetrics, max_positions: int) -> float:
    if max_positions <= 0 or max_positions >= 5:
        return 0.0

    required_win_rate = 0.65 - max_positions * 0.05
    if metrics.win_rate >= required_win_rate:
        return 0.0

    deficit = required_win_rate - metrics.win_rate
    penalty = deficit * (5 - max_positions) * 3.0
    return min(penalty, MAX_OVERFIT_PENALTY)


def calculate_score_delta(new_score: float, champion_score: float) -> float:
    if champion_score in (float("-inf"), -1e308):
        return 1.0 if new_score > float("-inf") else 0.0
    return new_score - champion_score
