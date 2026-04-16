import numpy as np
import pandas as pd
from typing import List, Dict, Tuple
from config import PERIOD_CONFIG


class OverfittingGuard:
    """防过拟合检测器"""

    def __init__(self, period: str = "W"):
        self.config = PERIOD_CONFIG[period]
        self.period = period

    def check_factor_count(self, factors: List[str]) -> Tuple[bool, str]:
        """检查因子数量是否超限"""
        max_factors = self.config["max_factors"]
        if len(factors) > max_factors:
            return False, f"因子数量 {len(factors)} 超过限制 {max_factors}"
        return True, "OK"

    def check_ic_stability(self, ic_series: np.ndarray) -> Tuple[bool, float, str]:
        """检查IC稳定性"""
        window = self.config["ic_rolling_window"]
        if len(ic_series) < window:
            return True, 1.0, "样本不足，暂不检测"

        rolling_std = pd.Series(ic_series).rolling(window).std().mean()
        ic_mean = np.mean(ic_series)
        stability = abs(ic_mean) / (rolling_std + 1e-10)

        threshold = 0.5 if self.period == "W" else (0.6 if self.period == "D" else 0.4)
        if stability < threshold:
            return False, stability, f"IC稳定性 {stability:.2f} 低于阈值 {threshold}"
        return True, stability, "OK"

    def check_train_test_gap(
        self, train_score: float, test_score: float
    ) -> Tuple[bool, float, str]:
        """检查训练集与测试集分数差距"""
        gap = train_score - test_score
        gap_ratio = gap / (train_score + 1e-10)

        if gap_ratio > 0.3:
            return False, gap_ratio, f"训练测试差距 {gap_ratio:.1%} 过大，可能过拟合"
        return True, gap_ratio, "OK"

    def check_turnover(self, turnover_rate: float) -> Tuple[bool, str]:
        """检查换手率"""
        limit = self.config["turnover_limit"]
        if turnover_rate > limit:
            return False, f"换手率 {turnover_rate:.1%} 超过限制 {limit:.1%}"
        return True, "OK"

    def full_check(
        self,
        factors: List[str],
        ic_series: np.ndarray,
        train_score: float,
        test_score: float,
        turnover_rate: float,
    ) -> Dict:
        """完整检查，返回所有检测结果"""
        results = {}

        r1, msg1 = self.check_factor_count(factors)
        results["factor_count"] = {"pass": r1, "message": msg1}

        r2, stability, msg2 = self.check_ic_stability(ic_series)
        results["ic_stability"] = {"pass": r2, "value": stability, "message": msg2}

        r3, gap, msg3 = self.check_train_test_gap(train_score, test_score)
        results["train_test_gap"] = {"pass": r3, "value": gap, "message": msg3}

        r4, msg4 = self.check_turnover(turnover_rate)
        results["turnover"] = {"pass": r4, "message": msg4}

        results["overall_pass"] = all([r1, r2, r3, r4])

        return results


def calculate_rolling_ic_stability(ic_series: np.ndarray, window: int = 20) -> float:
    """计算滚动IC稳定性"""
    if len(ic_series) < window:
        return 1.0
    rolling_std = pd.Series(ic_series).rolling(window).std().mean()
    return abs(np.mean(ic_series)) / (rolling_std + 1e-10)


def calculate_factor_decay(ic_series: np.ndarray) -> float:
    """计算因子衰减率（IC随时间的下降速度）"""
    if len(ic_series) < 10:
        return 0.0
    x = np.arange(len(ic_series))
    slope = np.polyfit(x, ic_series, 1)[0]
    return slope


def apply_regularization_strength(period: str) -> Dict:
    """根据周期返回正则化建议参数"""
    PERIOD_CONFIG[period]
    if period == "D":
        return {"alpha_1": 1e-6, "alpha_2": 1e-6, "lambda_1": 1e-6, "lambda_2": 1e-6}
    elif period == "W":
        return {"alpha_1": 1e-7, "alpha_2": 1e-7, "lambda_1": 1e-7, "lambda_2": 1e-7}
    else:
        return {"alpha_1": 1e-8, "alpha_2": 1e-8, "lambda_1": 1e-8, "lambda_2": 1e-8}
