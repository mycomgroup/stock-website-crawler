"""
问财公式回测结果评分系统

用于解析问财平台回测结果，计算目标函数得分，并决策 keep/rollback。

评分公式（与 guorn 保持一致）：
    calmar = annual_return / max(abs(max_drawdown), 0.01)
    score = calmar * 0.55 + sortino * 0.25 + information_ratio * 0.20
"""

from dataclasses import dataclass
from typing import Optional


@dataclass
class ParsedMetrics:
    """
    解析后的回测指标数据类。
    """

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


def parse_backtest_result(result_json: dict) -> ParsedMetrics:
    """
    解析问财回测结果 JSON，提取关键指标。

    Args:
        result_json: 问财平台回测接口返回的标准化 JSON 数据

    Returns:
        ParsedMetrics: 包含提取指标的 dataclass 对象
    """
    status = str(result_json.get("status", ""))

    summary = result_json.get("summary", {})

    return ParsedMetrics(
        status=status,
        backtest_id=result_json.get("backtest_id", ""),
        total_return=_safe_float(summary.get("totalReturn")),
        annual_return=_safe_float(summary.get("annualReturn")),
        max_drawdown=_safe_float(summary.get("maxDrawdown")),
        sharpe=_safe_float(summary.get("sharpe")),
        sortino=_safe_float(summary.get("sortino")),
        information_ratio=_safe_float(summary.get("informationRatio")),
        win_rate=_safe_float(summary.get("winRate")),
        avg_holding_days=_safe_float(summary.get("avgHoldingDays")),
        trade_count=_safe_int(summary.get("tradeCount")),
    )


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


def validate_result(metrics: ParsedMetrics) -> tuple[bool, str]:
    """
    硬门槛验证：检查回测结果是否有效。

    Args:
        metrics: ParsedMetrics 实例

    Returns:
        tuple[bool, str]: (is_valid, error_message)
    """
    if not metrics.status:
        return False, "status is empty"

    if metrics.status.lower() not in {"ok", "success", "completed", "done", "finished"}:
        if "error" in metrics.status.lower():
            return False, f"backtest failed with status: {metrics.status}"

    if not metrics.backtest_id:
        return False, "backtest_id is missing"

    return True, ""


def calculate_score(metrics: ParsedMetrics, weights: Optional[dict] = None) -> float:
    """
    计算复合目标函数得分。

    公式：
        calmar = annual_return / max(abs(max_drawdown), 0.01)
        score = calmar * 0.55 + sortino * 0.25 + information_ratio * 0.20

    Args:
        metrics: ParsedMetrics 实例
        weights: 可选权重字典

    Returns:
        float: 复合得分，数值越高越好
    """
    if weights is None:
        weights = DEFAULT_WEIGHTS

    calmar = metrics.annual_return / max(abs(metrics.max_drawdown), 0.01)
    score = (
        calmar * weights.get("calmar", 0.55)
        + metrics.sortino * weights.get("sortino", 0.25)
        + metrics.information_ratio * weights.get("information_ratio", 0.20)
    )
    return score


def decide_keep_rollback(
    new_score: float,
    champion_score: float,
    new_metrics: ParsedMetrics,
    champion_metrics: Optional[ParsedMetrics],
    hard_constraints: Optional[dict] = None,
) -> tuple[str, str]:
    """
    决策是 keep 还是 rollback。

    Args:
        new_score: 新版本的复合得分
        champion_score: 当前 champion 的复合得分
        new_metrics: 新版本的解析后指标
        champion_metrics: 当前 champion 的解析后指标（可为 None）
        hard_constraints: 可选的硬约束字典

    Returns:
        tuple[str, str]: (decision, reason)
            - decision: "keep" 或 "rollback"
            - reason: 决策的详细理由
    """
    if hard_constraints is None:
        hard_constraints = DEFAULT_HARD_CONSTRAINTS

    is_valid, validation_msg = validate_result(new_metrics)
    if not is_valid:
        return "rollback", f"backtest failed: {validation_msg}"

    max_drawdown_limit = hard_constraints.get("max_drawdown_limit")
    if max_drawdown_limit is not None:
        if abs(new_metrics.max_drawdown) > max_drawdown_limit:
            return "rollback", (
                f"max_drawdown {abs(new_metrics.max_drawdown):.4f} exceeds limit {max_drawdown_limit:.4f}"
            )

    if champion_metrics is None:
        if champion_score == -1e308 or champion_score == float("-inf"):
            return "keep", "first version, automatically champion"
        else:
            if new_score > champion_score:
                return "keep", f"new_score {new_score:.6f} > champion_score {champion_score:.6f}"
            else:
                return "rollback", f"new_score {new_score:.6f} <= champion_score {champion_score:.6f}"

    if new_score > champion_score:
        score_diff = new_score - champion_score
        reason = f"new_score {new_score:.6f} > champion_score {champion_score:.6f} (diff: {score_diff:.6f})"
        return "keep", reason
    else:
        score_diff = new_score - champion_score
        reason = f"new_score {new_score:.6f} <= champion_score {champion_score:.6f} (diff: {score_diff:.6f})"
        return "rollback", reason


DEFAULT_WEIGHTS = {
    "calmar": 0.55,
    "sortino": 0.25,
    "information_ratio": 0.20,
}

DEFAULT_HARD_CONSTRAINTS = {
    "max_drawdown_limit": 0.35,
}
