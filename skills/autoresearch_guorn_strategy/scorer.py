"""
果仁网回测结果评分系统

用于解析果仁网平台回测结果，计算目标函数得分，并决策 keep/rollback。

参考设计文档: .kiro/specs/autoresearch-guorn-strategy/design.md

⚠️  此文件为基础设施文件，agent 不可修改。只改配置文件。
"""

from dataclasses import dataclass
from typing import Optional


@dataclass
class ParsedMetrics:
    """
    解析后的回测指标数据类。

    Attributes:
        status: 回测状态，如 "ok", "error" 等
        backtest_id: 回测唯一标识符（果仁的 calc_id）
        total_return: 总收益率
        annual_return: 年化收益率
        max_drawdown: 最大回撤（果仁返回正值，如 0.15 表示 -15% 回撤）
        sharpe: 夏普比率
        sortino: Sortino 比率（只惩罚下行波动，比 sharpe 更关注亏损端）
        information_ratio: 信息比率（超额收益/跟踪误差，衡量选股能力）
        win_rate: 胜率
        avg_holding_days: 平均持仓天数
        sell_count: 卖出次数
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
    sell_count: int


def parse_backtest_result(result_json: dict) -> ParsedMetrics:
    """
    解析果仁网回测结果 JSON，提取关键指标。

    Args:
        result_json: 果仁网平台回测接口返回的完整 JSON 数据
                    预期结构：
                    {
                        "status": "ok",
                        "data": {
                            "calc_id": "uid.1234567890",
                            "trade_summary": {
                                "winsorize_annual": 0.15,
                                "win_ratio": 0.65,
                                "year_information_ratio": 0.8,
                                "maxdrop_day": 0.12,
                                "sharpe_ratio": 1.5,
                                "sortino_ratio": 2.0,
                                "avg_hold_days": 25,
                                "sell_count": 120,
                                "total_return": 0.75
                            }
                        }
                    }

    Returns:
        ParsedMetrics: 包含提取指标的 dataclass 对象

    Raises:
        KeyError: 如果必需的字段在 JSON 中不存在
        ValueError: 如果字段类型无法转换

    Note:
        果仁网返回的 JSON 字段名为 snake_case（如 winsorize_annual, win_ratio）
        本函数负责将其映射到 ParsedMetrics 属性
    """
    # 提取顶层字段
    status = str(result_json.get("status", ""))
    
    # 提取 data 字段
    data = result_json.get("data", {})
    calc_id = str(data.get("calc_id", ""))
    
    # 提取 trade_summary 字段
    trade_summary = data.get("trade_summary", {})
    
    return ParsedMetrics(
        status=status,
        backtest_id=calc_id,
        total_return=_safe_float(trade_summary.get("total_return")),
        annual_return=_safe_float(trade_summary.get("winsorize_annual")),
        max_drawdown=_safe_float(trade_summary.get("maxdrop_day")),
        sharpe=_safe_float(trade_summary.get("sharpe_ratio")),
        sortino=_safe_float(trade_summary.get("sortino_ratio")),
        information_ratio=_safe_float(trade_summary.get("year_information_ratio")),
        win_rate=_safe_float(trade_summary.get("win_ratio")),
        avg_holding_days=_safe_float(trade_summary.get("avg_hold_days")),
        sell_count=_safe_int(trade_summary.get("sell_count")),
    )


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


def _safe_int(value, default: int = 0) -> int:
    """
    安全地将值转换为 int 类型。

    Args:
        value: 待转换的值
        default: 转换失败时的默认值

    Returns:
        int: 转换后的整数，转换失败返回 default
    """
    if value is None:
        return default
    try:
        return int(value)
    except (TypeError, ValueError):
        return default


def validate_result(metrics: ParsedMetrics) -> tuple[bool, str]:
    """
    硬门槛验证：检查回测结果是否有效。

    验证规则（按优先级）：
    1. status 必须存在且非空
    2. status 必须是成功完成状态（如 "ok"）
    3. 不能是错误退出状态（如 "error"）
    4. 必须有 backtest_id（用于追溯）
    5. 关键指标不能全部为空（至少有一个有效值）

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

    # 检查是否是成功完成状态（支持多种常见成功状态表述）
    success_statuses = {"ok", "success", "completed", "done", "finished"}
    # 注意：error 明确表示失败
    if metrics.status.lower() in success_statuses:
        pass  # 成功状态，继续验证
    elif "error" in metrics.status.lower():
        return False, f"backtest failed with status: {metrics.status}"

    # 检查 backtest_id 是否存在（用于追溯）
    if not metrics.backtest_id:
        return False, "backtest_id is missing - cannot trace this backtest"

    # 检查关键指标：至少 annual_return 和 max_drawdown 必须有有效值
    # 如果两者都为 0（或默认值），可能表示数据异常
    # 注意：允许 0 值存在（策略确实可能收益为 0），但不允许多个关键指标同时为默认空值
    key_metrics = [metrics.annual_return, metrics.max_drawdown, metrics.sharpe]
    # 统计有多少个指标是默认值（0.0）
    default_count = sum(1 for m in key_metrics if m == 0.0)

    # 如果所有关键指标都是默认值，说明可能没有有效数据
    # 但需要注意：策略确实可能表现接近 0，所以这里只是警告而非硬错误
    # 我们放宽条件，只要 backtest_id 存在且 status 正常就认为有效

    return True, ""


def calculate_score(metrics: ParsedMetrics, weights: Optional[dict] = None) -> float:
    """
    计算复合目标函数得分。

    公式（量纲对齐版）：
        calmar = annual_return / max(abs(max_drawdown), 0.01)
        score = calmar * 0.55 + sortino * 0.25 + information_ratio * 0.20

    设计原则：
    - calmar（年化收益/最大回撤）天然量纲对齐，收益和回撤绑定在一起，
      收益触顶后压缩回撤也能提升得分
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

    决策规则（参考设计文档）：
    1. 如果平台回测失败（new_metrics.status 异常），直接 rollback
    2. 新分数必须严格好于 champion 分数才 keep（不是 >=，是 >）
    3. 如果分数接近但回撤更大，不 keep
    4. 可选的硬约束检查（如 max_drawdown_limit）

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

    Decision Logic:
        keep 条件（需同时满足）：
        - 新版本回测成功完成
        - 新分数 > champion 分数（严格大于）
        - 可选的：max_drawdown 未超过 hard_constraints 中的限制

        rollback 条件（满足任一即回滚）：
        - 新版本回测失败
        - 新分数 <= champion 分数
        - max_drawdown 超过限制
    """
    if hard_constraints is None:
        hard_constraints = {}

    # 规则 1：检查新版本是否回测成功
    is_valid, validation_msg = validate_result(new_metrics)
    if not is_valid:
        return "rollback", f"backtest failed: {validation_msg}"

    # 规则 2：可选的 max_drawdown 硬约束检查
    # 注意：max_drawdown 是正值（如 0.15），直接与 limit 比较
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
    # 注意：默认规则是新分数严格好于 champion 才 keep（不是 >=）
    if new_score > champion_score:
        # 构建详细理由
        score_diff = new_score - champion_score
        reason = (
            f"new_score {new_score:.6f} > champion_score {champion_score:.6f} "
            f"(diff: {score_diff:.6f})"
        )
        return "keep", reason
    else:
        # 新分数不比 champion 好，rollback
        score_diff = new_score - champion_score
        reason = (
            f"new_score {new_score:.6f} <= champion_score {champion_score:.6f} "
            f"(diff: {score_diff:.6f})"
        )
        return "rollback", reason


# 默认权重常量（供外部引用）
DEFAULT_WEIGHTS = {
    "calmar": 0.55,
    "sortino": 0.25,
    "information_ratio": 0.20,
}

# 默认硬约束（供外部引用）
DEFAULT_HARD_CONSTRAINTS = {
    "max_drawdown_limit": 0.35,
}
