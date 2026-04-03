"""
衰退检测核心模块
负责策略衰退检测、预警判定和应对措施生成
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, List, Tuple, Optional
from scipy import stats
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class DecayDetector:
    """衰退检测核心类"""

    def __init__(self, is_baseline: Dict):
        """
        初始化衰退检测器

        参数:
        - is_baseline: IS表现基准字典
          {
              'annual_return': 394,  # IS年化收益基准
              'win_rate': 87.95,     # IS胜率基准
              'max_drawdown': 0.60,  # IS最大回撤基准
              'sharpe_ratio': 20,    # IS夏普比率基准
              'profit_loss_ratio': 21.91  # IS盈亏比基准
          }
        """
        self.is_baseline = is_baseline

        self.thresholds = {
            "annual_return": {
                "normal": 300,  # >300% 正常
                "observation": 200,  # 200-300% 观察
                "warning": 100,  # 100-200% 警告
                "failure": 50,  # <50% 失效
            },
            "win_rate": {
                "normal": 80,  # >80% 正常
                "observation": 70,  # 70-80% 观察
                "warning": 60,  # 60-70% 警告
                "failure": 50,  # <50% 失效
            },
            "max_drawdown": {
                "normal": 10,  # <10% 正常
                "observation": 15,  # 10-15% 观察
                "warning": 20,  # 15-20% 警告
                "failure": 25,  # >25% 失效
            },
            "sharpe_ratio": {
                "normal": 3.0,  # >3.0 正常
                "observation": 1.5,  # 1.5-3.0 观察
                "warning": 1.0,  # 1.0-1.5 警告
                "failure": 0.5,  # <0.5 失效
            },
        }

        self.decay_definitions = {
            "light": {"min": 0.10, "max": 0.20},  # 轻度衰退 10-20%
            "medium": {"min": 0.20, "max": 0.40},  # 中度衰退 20-40%
            "severe": {"min": 0.40, "max": 1.00},  # 重度衰退 >40%
        }

    def detect_decay(self, current_metrics: Dict, duration_days: int = 0) -> Dict:
        """
        综合衰退检测

        参数:
        - current_metrics: 当前指标字典
          {
              'annual_return': 年化收益率,
              'win_rate': 胜率,
              'max_drawdown': 最大回撤,
              'sharpe_ratio': 夏普比率,
              ...
          }
        - duration_days: 异常持续天数

        返回:
        - decay_result: 衰退检测结果
        """
        metrics_status = self._evaluate_metrics_status(current_metrics)

        alert_level, triggered_metrics = self._determine_alert_level(
            metrics_status, duration_days
        )

        decay_ratios = self._calculate_decay_ratios(current_metrics)

        decay_degree = self._determine_decay_degree(decay_ratios)

        response_actions = self._get_response_actions(alert_level, triggered_metrics)

        return {
            "alert_level": alert_level,
            "triggered_metrics": triggered_metrics,
            "metrics_status": metrics_status,
            "decay_ratios": decay_ratios,
            "decay_degree": decay_degree,
            "response_actions": response_actions,
            "duration_days": duration_days,
        }

    def _evaluate_metrics_status(self, current_metrics: Dict) -> Dict:
        """
        评估各指标状态

        参数:
        - current_metrics: 当前指标

        返回:
        - metrics_status: 各指标状态
        """
        metrics_status = {}

        for metric, value in current_metrics.items():
            if metric not in self.thresholds:
                metrics_status[metric] = "unknown"
                continue

            if value is None:
                metrics_status[metric] = "missing"
                continue

            thresholds = self.thresholds[metric]

            if metric == "max_drawdown":
                if value < thresholds["normal"]:
                    status = "normal"
                elif value < thresholds["observation"]:
                    status = "observation"
                elif value < thresholds["warning"]:
                    status = "warning"
                else:
                    status = "failure"
            else:
                if value > thresholds["normal"]:
                    status = "normal"
                elif value > thresholds["observation"]:
                    status = "observation"
                elif value > thresholds["warning"]:
                    status = "warning"
                else:
                    status = "failure"

            metrics_status[metric] = status

        return metrics_status

    def _determine_alert_level(
        self, metrics_status: Dict, duration_days: int
    ) -> Tuple[str, List[str]]:
        """
        判定预警级别

        参数:
        - metrics_status: 指标状态
        - duration_days: 持续天数

        返回:
        - alert_level: 预警级别
        - triggered_metrics: 触发指标列表
        """
        normal_count = sum(1 for s in metrics_status.values() if s == "normal")
        observation_count = sum(
            1 for s in metrics_status.values() if s == "observation"
        )
        warning_count = sum(1 for s in metrics_status.values() if s == "warning")
        failure_count = sum(1 for s in metrics_status.values() if s == "failure")

        triggered_metrics = [
            metric
            for metric, status in metrics_status.items()
            if status in ["observation", "warning", "failure"]
        ]

        if failure_count > 0:
            return "red", triggered_metrics

        if warning_count >= 2 and duration_days >= 30:
            return "red", triggered_metrics

        if warning_count > 0 and duration_days >= 30:
            return "orange", triggered_metrics

        if observation_count >= 2 and duration_days >= 14:
            return "orange", triggered_metrics

        if observation_count > 0 and duration_days >= 14:
            return "yellow", triggered_metrics

        return "green", []

    def _calculate_decay_ratios(self, current_metrics: Dict) -> Dict:
        """
        计算衰减比例

        参数:
        - current_metrics: 当前指标

        返回:
        - decay_ratios: 衰减比例
        """
        decay_ratios = {}

        for metric, current_value in current_metrics.items():
            if metric not in self.is_baseline:
                continue

            if current_value is None:
                decay_ratios[metric] = None
                continue

            baseline_value = self.is_baseline[metric]

            if metric == "max_drawdown":
                decay_ratio = (current_value - baseline_value) / baseline_value
            else:
                decay_ratio = (current_value - baseline_value) / baseline_value

            decay_ratios[metric] = decay_ratio

        return decay_ratios

    def _determine_decay_degree(self, decay_ratios: Dict) -> str:
        """
        判定衰退程度

        参数:
        - decay_ratios: 衰减比例

        返回:
        - decay_degree: 衰退程度
        """
        max_decay = 0

        for metric, ratio in decay_ratios.items():
            if ratio is None:
                continue

            if metric == "max_drawdown":
                decay = ratio
            else:
                decay = -ratio

            if decay > max_decay:
                max_decay = decay

        if max_decay < 0.10:
            return "none"
        elif max_decay < 0.20:
            return "light"
        elif max_decay < 0.40:
            return "medium"
        else:
            return "severe"

    def _get_response_actions(
        self, alert_level: str, triggered_metrics: List[str]
    ) -> List[Dict]:
        """
        获取应对措施

        参数:
        - alert_level: 预警级别
        - triggered_metrics: 触发指标

        返回:
        - response_actions: 应对措施列表
        """
        actions = {
            "green": [
                {
                    "action": "正常执行",
                    "description": "按原策略正常执行",
                    "position": "30-40%",
                },
                {
                    "action": "周频监控",
                    "description": "维持原验证频率监控",
                    "frequency": "周频",
                },
            ],
            "yellow": [
                {
                    "action": "加强监控",
                    "description": "验证频率提升至日频",
                    "frequency": "日频",
                },
                {
                    "action": "人工审核",
                    "description": "每日人工审核交易信号",
                    "responsibility": "策略主管",
                },
                {
                    "action": "原因分析",
                    "description": "启动衰退原因分析",
                    "responsibility": "策略团队",
                },
                {
                    "action": "准备预案",
                    "description": "准备降仓应对预案",
                    "responsibility": "风控部门",
                },
            ],
            "orange": [
                {
                    "action": "降仓50%",
                    "description": "立即降低仓位至50%",
                    "position": "15-20%",
                },
                {
                    "action": "暂停新开仓",
                    "description": "暂停新开仓操作（只执行卖出）",
                    "restriction": "仅卖出",
                },
                {
                    "action": "风控介入",
                    "description": "风控部门介入监督",
                    "responsibility": "风控部门",
                },
                {
                    "action": "深度分析",
                    "description": "深度分析衰退根本原因",
                    "responsibility": "策略团队",
                },
                {
                    "action": "改进方案",
                    "description": "制定参数调整/规则优化方案",
                    "responsibility": "策略团队",
                },
            ],
            "red": [
                {
                    "action": "暂停策略",
                    "description": "立即暂停策略执行",
                    "position": "0%",
                },
                {
                    "action": "清空持仓",
                    "description": "开始清空所有持仓",
                    "execution": "立即执行",
                },
                {
                    "action": "全面复盘",
                    "description": "全面复盘分析衰退原因",
                    "responsibility": "策略团队+风控团队",
                },
                {
                    "action": "策略评估",
                    "description": "重新评估策略有效性",
                    "responsibility": "策略委员会",
                },
                {
                    "action": "决策判定",
                    "description": "决定重启或废弃策略",
                    "responsibility": "投资决策委员会",
                },
            ],
        }

        return actions.get(alert_level, [])

    def statistical_test(self, returns: List[float], confidence: float = 0.95) -> Dict:
        """
        统计检验：检验收益是否显著为正

        参数:
        - returns: 收益率序列
        - confidence: 置信水平

        返回:
        - test_result: 检验结果
        """
        try:
            if len(returns) < 2:
                return {
                    "is_significant": False,
                    "p_value": None,
                    "t_stat": None,
                    "error": "样本量不足",
                }

            t_stat, p_value = stats.ttest_1samp(returns, 0)

            alpha = 1 - confidence
            is_significant = p_value < alpha and t_stat > 0

            return {
                "is_significant": is_significant,
                "p_value": p_value,
                "t_stat": t_stat,
                "confidence": confidence,
                "mean_return": np.mean(returns),
                "std_return": np.std(returns),
            }

        except Exception as e:
            logger.error(f"统计检验失败: {e}")
            return {
                "is_significant": False,
                "p_value": None,
                "t_stat": None,
                "error": str(e),
            }

    def trend_detection(self, indicator_series: List[float], window: int = 20) -> Dict:
        """
        趋势检测：识别指标持续恶化

        参数:
        - indicator_series: 指标历史序列
        - window: 观察窗口长度

        返回:
        - trend_result: 趋势检测结果
        """
        try:
            if len(indicator_series) < window:
                return {
                    "trend_direction": "unknown",
                    "deterioration_days": 0,
                    "alert_level": "green",
                    "error": "数据不足",
                }

            recent_values = indicator_series[-window:]

            slope = np.polyfit(range(window), recent_values, 1)[0]

            deterioration_count = 0
            for i in range(window - 1):
                if recent_values[i + 1] < recent_values[i]:
                    deterioration_count += 1
                else:
                    deterioration_count = 0

            if slope > 0 and deterioration_count < 5:
                trend_direction = "rising"
                alert_level = "green"
            elif slope > -0.1 and deterioration_count < 10:
                trend_direction = "stable"
                alert_level = "yellow"
            else:
                trend_direction = "declining"
                alert_level = "orange"

            return {
                "trend_direction": trend_direction,
                "deterioration_days": deterioration_count,
                "slope": slope,
                "alert_level": alert_level,
            }

        except Exception as e:
            logger.error(f"趋势检测失败: {e}")
            return {
                "trend_direction": "unknown",
                "deterioration_days": 0,
                "alert_level": "green",
                "error": str(e),
            }

    def generate_decay_report(self, decay_result: Dict) -> str:
        """
        生成衰退检测报告

        参数:
        - decay_result: 衰退检测结果

        返回:
        - report: Markdown格式报告
        """
        report = f"""# 衰退检测报告

**检测时间**: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

## 一、预警状态

- **当前预警级别**: {decay_result["alert_level"].upper()}
- **异常持续天数**: {decay_result["duration_days"]}天
- **触发指标**: {", ".join(decay_result["triggered_metrics"]) if decay_result["triggered_metrics"] else "无"}

## 二、指标状态

| 指标 | 当前值 | IS基准 | 状态 | 衰减比例 |
|------|--------|--------|------|----------|
"""

        for metric, status in decay_result["metrics_status"].items():
            baseline = self.is_baseline.get(metric, "N/A")
            decay_ratio = decay_result["decay_ratios"].get(metric, "N/A")

            if isinstance(decay_ratio, float):
                decay_ratio_str = f"{decay_ratio * 100:.2f}%"
            else:
                decay_ratio_str = str(decay_ratio)

            report += f"| {metric} | {baseline} | {baseline} | {status} | {decay_ratio_str} |\n"

        report += f"""
## 三、衰退程度

**衰退程度**: {decay_result["decay_degree"]}

## 四、应对措施

"""
        for i, action in enumerate(decay_result["response_actions"], 1):
            report += f"{i}. **{action['action']}**: {action['description']}\n"

        return report


if __name__ == "__main__":
    is_baseline = {
        "annual_return": 394,
        "win_rate": 87.95,
        "max_drawdown": 0.60,
        "sharpe_ratio": 20,
        "profit_loss_ratio": 21.91,
    }

    detector = DecayDetector(is_baseline)

    current_metrics = {
        "annual_return": 350,
        "win_rate": 85,
        "max_drawdown": 3.0,
        "sharpe_ratio": 18,
        "profit_loss_ratio": 20,
    }

    decay_result = detector.detect_decay(current_metrics, duration_days=10)

    print(detector.generate_decay_report(decay_result))
