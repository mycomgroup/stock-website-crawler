"""
问财公式回测结果评分系统

用于解析问财平台回测结果，计算目标函数得分，并决策 keep/rollback。

评分公式（v3 - 防过拟合优化版）：
    calmar = annual_return / max(abs(max_drawdown), 0.01)
    score = sortino * 0.40 + calmar * 0.25 + information_ratio * 0.15 + win_rate * 0.10
          - complexity_penalty * 0.10 - position_penalty - overfit_penalty

复杂度惩罚：
    complexity = formula_conditions_count + tuning_params_count
    penalty = min(complexity / 10, 1.0)  # 最多惩罚 1.0

过拟合惩罚（v3新增）：
    持股少于5支时，胜率必须足够高，否则判定为过拟合
    - 持股1支：需要胜率≥60%
    - 持股2支：需要胜率≥55%
    - 持股3支：需要胜率≥50%
    - 持股4支：需要胜率≥45%
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
    max_positions: int = 0
    daily_buy_count: int = 0


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

    full_result = result_json.get("full_result", {})
    raw_config = full_result.get("config", {})

    max_positions = _safe_int(raw_config.get("stock_hold"))
    daily_buy_count = _safe_int(raw_config.get("day_buy_stock_num"))

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
        max_positions=max_positions,
        daily_buy_count=daily_buy_count,
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


def calculate_score(
    metrics: ParsedMetrics,
    weights: Optional[dict] = None,
    complexity: int = 0,
    config: Optional[dict] = None,
) -> float:
    """
    计算复合目标函数得分。

    公式（v2）：
        calmar = annual_return / max(abs(max_drawdown), 0.01)
        complexity_penalty = min(complexity / 10, 1.0)
        position_penalty = 双边软约束惩罚
        score = sortino * 0.40 + calmar * 0.25 + information_ratio * 0.15
              + win_rate * 0.10 - complexity_penalty * 0.10 - position_penalty

    选股数量惩罚（方案C - 双边软约束）：
        if max_positions < 5:
            penalty = (5 - max_positions) ** 2 * 0.1  # 选1支扣1.6分
        elif max_positions > 15:
            penalty = (max_positions - 15) ** 2 * 0.01  # 选50支扣1.2分
        else:
            penalty = 0

    Args:
        metrics: ParsedMetrics 实例
        weights: 可选权重字典
        complexity: 配置复杂度（formula条件数 + 调优参数数）
        config: 配置字典（可选，用于获取 maxPositions）

    Returns:
        float: 复合得分，数值越高越好
    """
    if weights is None:
        weights = DEFAULT_WEIGHTS

    calmar = metrics.annual_return / max(abs(metrics.max_drawdown), 0.01)

    complexity_penalty = min(complexity / 10.0, 1.0)

    max_positions = metrics.max_positions
    if max_positions <= 0 and config:
        max_positions = config.get("maxPositions", 0)

    position_penalty = 0.0
    if max_positions > 0:
        if max_positions < 5:
            position_penalty = (5 - max_positions) ** 2 * 0.1
        elif max_positions > 15:
            position_penalty = (max_positions - 15) ** 2 * 0.01

    overfit_penalty = calculate_overfit_penalty(metrics, max_positions)

    score = (
        metrics.sortino * weights.get("sortino", 0.40)
        + calmar * weights.get("calmar", 0.25)
        + metrics.information_ratio * weights.get("information_ratio", 0.15)
        + metrics.win_rate * weights.get("win_rate", 0.10)
        - complexity_penalty * weights.get("complexity_penalty", 0.10)
        - position_penalty
        - overfit_penalty
    )
    return score


def calculate_complexity(config: dict) -> int:
    """
    计算配置复杂度。

    公式：
        complexity = formula条件数 + 调优参数数

    Args:
        config: 公式策略配置

    Returns:
        int: 复杂度数值
    """
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
    "sortino": 0.40,
    "calmar": 0.25,
    "information_ratio": 0.15,
    "win_rate": 0.10,
    "complexity_penalty": 0.10,
}

DEFAULT_HARD_CONSTRAINTS = {
    "max_drawdown_limit": 0.35,
}


def calculate_overfit_penalty(metrics: ParsedMetrics, max_positions: int) -> float:
    """
    计算过拟合惩罚。

    核心逻辑：持股数少时，必须有足够高的胜率支撑，否则是过拟合。

    规则：
        - 持股1支：需要胜率≥60%
        - 持股2支：需要胜率≥55%
        - 持股3支：需要胜率≥50%
        - 持股4支：需要胜率≥45%
        - 持股≥5支：无限制

    Args:
        metrics: ParsedMetrics 实例
        max_positions: 最大持仓数

    Returns:
        float: 过拟合惩罚值（非负）
    """
    if max_positions <= 0 or max_positions >= 5:
        return 0.0

    required_win_rate = 0.65 - max_positions * 0.05  # 1支=60%, 2支=55%, 3支=50%, 4支=45%

    if metrics.win_rate >= required_win_rate:
        return 0.0

    deficit = required_win_rate - metrics.win_rate
    penalty = deficit * (5 - max_positions) * 3.0

    return penalty


def calculate_score_delta(new_score: float, champion_score: float) -> float:
    """
    计算相对于 champion 的得分变化。

    Args:
        new_score: 新配置的得分
        champion_score: 当前 champion 的得分

    Returns:
        float: 得分变化值（正数表示提升，负数表示下降）
    """
    if champion_score == float("-inf") or champion_score == -1e308:
        return 1.0 if new_score > float("-inf") else 0.0
    return new_score - champion_score
