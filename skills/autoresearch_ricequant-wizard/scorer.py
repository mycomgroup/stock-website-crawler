"""
向导式策略优化器（autoresearch-ricequant-wizard）独立评分模块

用于解析 RiceQuant 平台回测结果，计算目标函数得分，并决策 keep/rollback。

⚠️  本模块为 autoresearch-ricequant-wizard 的独立实现，
    与 skills/autoresearch/scorer.py 逻辑相同，但不依赖后者，
    可独立运行，无需 autoresearch 包存在。
"""

from dataclasses import dataclass
from typing import Optional


@dataclass
class ParsedMetrics:
    """
    解析后的回测指标数据类。

    Attributes:
        status: 回测状态，如 "finished", "error_exit" 等
        backtest_id: 回测唯一标识符
        total_return: 总收益率
        annual_return: 年化收益率
        max_drawdown: 最大回撤（RiceQuant 返回正值，如 0.15 表示 -15% 回撤）
        sharpe: 夏普比率
        sortino: Sortino 比率（只惩罚下行波动，比 sharpe 更关注亏损端）
        information_ratio: 信息比率（超额收益/跟踪误差，衡量选股能力）
        alpha: Alpha 收益
        beta: Beta 风险系数
    """
    status: str
    backtest_id: str
    total_return: float
    annual_return: float
    max_drawdown: float
    sharpe: float
    sortino: float
    information_ratio: float
    alpha: float
    beta: float


def _safe_float(value, default: float = 0.0) -> float:
    """
    安全地将值转换为 float 类型。

    Args:
        value: 待转换的值
        default: 转换失败时的默认值

    Returns:
        float: 转换后的浮点数，转换失败返回 default
    """
    if value is None:
        return default
    try:
        return float(value)
    except (TypeError, ValueError):
        return default


def parse_backtest_result(result_json: dict) -> ParsedMetrics:
    """
    解析 RiceQuant 回测结果 JSON，提取关键指标。

    Args:
        result_json: RiceQuant 平台回测接口返回的完整 JSON 数据

    Returns:
        ParsedMetrics: 包含提取指标的 dataclass 对象

    Raises:
        KeyError: 如果必需的字段在 JSON 中不存在
        ValueError: 如果字段类型无法转换

    Note:
        RiceQuant 返回的 JSON 字段名为 camelCase（如 totalReturn, annualReturn）
        本函数负责将其映射到 snake_case 的 ParsedMetrics 属性
    """
    return ParsedMetrics(
        status=str(result_json.get("status", "")),
        backtest_id=str(result_json.get("backtestId", "")),
        total_return=_safe_float(result_json.get("totalReturn")),
        annual_return=_safe_float(result_json.get("annualReturn")),
        max_drawdown=_safe_float(result_json.get("maxDrawdown")),
        sharpe=_safe_float(result_json.get("sharpe")),
        sortino=_safe_float(result_json.get("sortino")),
        information_ratio=_safe_float(result_json.get("informationRatio")),
        alpha=_safe_float(result_json.get("alpha")),
        beta=_safe_float(result_json.get("beta")),
    )


def validate_result(metrics: ParsedMetrics) -> tuple[bool, str]:
    """
    硬门槛验证：检查回测结果是否有效。

    验证规则（按优先级）：
    1. status 必须存在且非空
    2. status 必须是成功完成状态（如 "finished"）
    3. 不能是错误退出状态（如 "error_exit"）
    4. 必须有 backtestId（用于追溯）

    Args:
        metrics: ParsedMetrics 实例，包含回测指标

    Returns:
        tuple[bool, str]: (is_valid, error_message)
            - is_valid: True 表示通过验证，False 表示未通过
            - error_message: 未通过时的具体错误原因，通过时为空字符串
    """
    # 检查 status 是否存在且非空
    if not metrics.status:
        return False, "status is empty or missing"

    # 检查是否是成功完成状态
    success_statuses = {"finished", "success", "completed", "done", "success_exit", "normal_exit"}
    if metrics.status.lower() not in success_statuses:
        return False, f"backtest failed with status: {metrics.status}"

    # 检查 backtestId 是否存在（用于追溯）
    if not metrics.backtest_id:
        return False, "backtestId is missing - cannot trace this backtest"

    return True, ""


def calculate_score(metrics: ParsedMetrics, weights: Optional[dict] = None) -> float:
    """
    计算复合目标函数得分。

    公式（量纲对齐版）：
        calmar = annual_return / max(abs(max_drawdown), 0.01)
        score = calmar * 0.55 + sortino * 0.25 + information_ratio * 0.20

    设计原则：
    - calmar（年化收益/最大回撤）天然量纲对齐，收益和回撤绑定在一起
    - sortino 只惩罚下行波动，比 sharpe 更关注实际亏损风险
    - information_ratio 衡量超额收益能力，三者量纲相近（均在 1~5 范围）

    Args:
        metrics: ParsedMetrics 实例
        weights: 可选权重字典，支持键: calmar, sortino, information_ratio
                 如果为 None，使用默认权重。

    Returns:
        float: 复合得分，数值越高越好。
    """
    if weights is None:
        weights = {
            "calmar": 0.55,
            "sortino": 0.25,
            "information_ratio": 0.20,
        }

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
    决策是 keep（保留新版本）还是 rollback（回滚到 champion）。

    决策规则：
    1. 如果平台回测失败（new_metrics.status 异常），直接 rollback
    2. 可选的硬约束检查（如 max_drawdown_limit）
    3. 如果没有 champion（首个版本），则 keep
    4. 新分数必须严格好于 champion 分数才 keep（严格大于，不是 >=）

    Args:
        new_score: 新版本的复合得分
        champion_score: 当前 champion 的复合得分
        new_metrics: 新版本的解析后指标
        champion_metrics: 当前 champion 的解析后指标（可为 None，表示尚无 champion）
        hard_constraints: 可选的硬约束字典，支持的键:
            - max_drawdown_limit: 最大回撤上限，超过则强制 rollback

    Returns:
        tuple[str, str]: (decision, reason)
            - decision: "keep" 或 "rollback"
            - reason: 决策的详细理由
    """
    if hard_constraints is None:
        hard_constraints = {}

    # 规则 1：检查新版本是否回测成功
    is_valid, validation_msg = validate_result(new_metrics)
    if not is_valid:
        return "rollback", f"backtest failed: {validation_msg}"

    # 规则 2：可选的 max_drawdown 硬约束检查
    max_drawdown_limit = hard_constraints.get("max_drawdown_limit")
    if max_drawdown_limit is not None:
        if abs(new_metrics.max_drawdown) > max_drawdown_limit:
            return "rollback", (
                f"max_drawdown {abs(new_metrics.max_drawdown):.4f} exceeds limit {max_drawdown_limit:.4f}"
            )

    # 规则 3：如果没有 champion（首个版本），则 keep
    if champion_metrics is None:
        return "keep", "first version, automatically champion"

    # 规则 4：新分数必须严格好于 champion 才 keep
    if new_score > champion_score:
        score_diff = new_score - champion_score
        reason = (
            f"new_score {new_score:.6f} > champion_score {champion_score:.6f} "
            f"(diff: {score_diff:.6f})"
        )
        return "keep", reason
    else:
        score_diff = new_score - champion_score
        reason = (
            f"new_score {new_score:.6f} <= champion_score {champion_score:.6f} "
            f"(diff: {score_diff:.6f})"
        )
        return "rollback", reason


# 默认权重常量（供外部引用）
DEFAULT_WEIGHTS = {"calmar": 0.55, "sortino": 0.25, "information_ratio": 0.20}

# 默认硬约束（供外部引用）
DEFAULT_HARD_CONSTRAINTS = {"max_drawdown_limit": 0.35}
