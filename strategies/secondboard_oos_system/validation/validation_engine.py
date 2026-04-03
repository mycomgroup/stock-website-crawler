"""
自动化验证核心模块
负责策略验证的自动化执行、指标计算和结果存储
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
import logging
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from data.data_manager import DataManager
from core.decay_detector import DecayDetector

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class PerformanceCalculator:
    """性能指标计算器"""

    @staticmethod
    def calculate_return(trade_records: pd.DataFrame) -> Dict:
        """
        计算收益率指标

        参数:
        - trade_records: 交易记录DataFrame

        返回:
        - return_metrics: 收益指标字典
        """
        if trade_records.empty or "profit_loss_pct" not in trade_records.columns:
            return {"cumulative_return": 0, "annual_return": 0, "avg_trade_return": 0}

        returns = trade_records["profit_loss_pct"].dropna()

        cumulative_return = (1 + returns).prod() - 1

        if "signal_date" in trade_records.columns and len(trade_records) > 0:
            start_date = pd.to_datetime(trade_records["signal_date"].min())
            end_date = pd.to_datetime(trade_records["signal_date"].max())
            days = (end_date - start_date).days + 1

            if days > 0:
                annual_return = (1 + cumulative_return) ** (365 / days) - 1
            else:
                annual_return = 0
        else:
            annual_return = 0

        avg_trade_return = returns.mean() if len(returns) > 0 else 0

        return {
            "cumulative_return": cumulative_return,
            "annual_return": annual_return * 100,
            "avg_trade_return": avg_trade_return * 100,
        }

    @staticmethod
    def calculate_risk_metrics(
        trade_records: pd.DataFrame, daily_returns: Optional[pd.DataFrame] = None
    ) -> Dict:
        """
        计算风险指标

        参数:
        - trade_records: 交易记录DataFrame
        - daily_returns: 日收益DataFrame（可选）

        返回:
        - risk_metrics: 风险指标字典
        """
        if trade_records.empty:
            return {"max_drawdown": 0, "volatility": 0, "downside_volatility": 0}

        if daily_returns is not None and not daily_returns.empty:
            returns = (
                daily_returns["return"].dropna()
                if "return" in daily_returns.columns
                else []
            )
        else:
            returns = (
                trade_records["profit_loss_pct"].dropna()
                if "profit_loss_pct" in trade_records.columns
                else []
            )

        if len(returns) == 0:
            return {"max_drawdown": 0, "volatility": 0, "downside_volatility": 0}

        cumulative = (1 + returns).cumprod()
        running_max = cumulative.expanding().max()
        drawdown = (cumulative - running_max) / running_max
        max_drawdown = abs(drawdown.min()) * 100

        volatility = returns.std() * np.sqrt(252) * 100 if len(returns) > 1 else 0

        negative_returns = returns[returns < 0]
        downside_volatility = (
            negative_returns.std() * np.sqrt(252) * 100
            if len(negative_returns) > 1
            else 0
        )

        return {
            "max_drawdown": max_drawdown,
            "volatility": volatility,
            "downside_volatility": downside_volatility,
        }

    @staticmethod
    def calculate_risk_adjusted_metrics(
        return_metrics: Dict, risk_metrics: Dict, risk_free_rate: float = 0.03
    ) -> Dict:
        """
        计算风险调整收益指标

        参数:
        - return_metrics: 收益指标
        - risk_metrics: 风险指标
        - risk_free_rate: 无风险利率

        返回:
        - risk_adjusted_metrics: 风险调整收益指标
        """
        annual_return = return_metrics.get("annual_return", 0) / 100
        volatility = risk_metrics.get("volatility", 0) / 100
        max_drawdown = risk_metrics.get("max_drawdown", 0) / 100

        if volatility > 0:
            sharpe_ratio = (annual_return - risk_free_rate) / volatility
        else:
            sharpe_ratio = 0

        if max_drawdown > 0:
            calmar_ratio = annual_return / max_drawdown
        else:
            calmar_ratio = 0

        return {"sharpe_ratio": sharpe_ratio, "calmar_ratio": calmar_ratio}

    @staticmethod
    def calculate_trade_quality(trade_records: pd.DataFrame) -> Dict:
        """
        计算交易质量指标

        参数:
        - trade_records: 交易记录DataFrame

        返回:
        - trade_quality: 交易质量指标
        """
        if trade_records.empty or "profit_loss_pct" not in trade_records.columns:
            return {
                "win_rate": 0,
                "profit_loss_ratio": 0,
                "trade_count": 0,
                "avg_holding_days": 0,
            }

        returns = trade_records["profit_loss_pct"].dropna()

        win_count = (returns > 0).sum()
        total_count = len(returns)
        win_rate = (win_count / total_count * 100) if total_count > 0 else 0

        avg_profit = returns[returns > 0].mean() if win_count > 0 else 0
        loss_count = (returns < 0).sum()
        avg_loss = abs(returns[returns < 0].mean()) if loss_count > 0 else 0
        profit_loss_ratio = (avg_profit / avg_loss) if avg_loss > 0 else 0

        if (
            "signal_date" in trade_records.columns
            and "sell_date" in trade_records.columns
        ):
            holding_days = (
                pd.to_datetime(trade_records["sell_date"])
                - pd.to_datetime(trade_records["signal_date"])
            ).dt.days
            avg_holding_days = holding_days.mean() if len(holding_days) > 0 else 0
        else:
            avg_holding_days = 0

        return {
            "win_rate": win_rate,
            "profit_loss_ratio": profit_loss_ratio,
            "trade_count": total_count,
            "avg_holding_days": avg_holding_days,
        }


class ValidationEngine:
    """验证引擎"""

    def __init__(self, db_path: str = "secondboard_oos.db"):
        self.data_manager = DataManager(db_path)

        self.is_baseline = {
            "annual_return": 394,
            "win_rate": 87.95,
            "max_drawdown": 0.60,
            "sharpe_ratio": 20,
            "profit_loss_ratio": 21.91,
        }

        self.decay_detector = DecayDetector(self.is_baseline)
        self.performance_calculator = PerformanceCalculator()

    def run_daily_validation(self, date: str) -> Dict:
        """
        执行日频验证

        参数:
        - date: 验证日期

        返回:
        - validation_result: 验证结果
        """
        logger.info(f"开始日频验证: {date}")

        trade_records = self.data_manager.query_trade_records(date, date)

        return_metrics = self.performance_calculator.calculate_return(trade_records)
        risk_metrics = self.performance_calculator.calculate_risk_metrics(trade_records)
        trade_quality = self.performance_calculator.calculate_trade_quality(
            trade_records
        )

        validation_result = {
            "validation_date": date,
            "validation_type": "daily",
            "window_type": "single_day",
            **return_metrics,
            **risk_metrics,
            **trade_quality,
            "alert_level": "green",
            "triggered_metrics": [],
        }

        self._save_validation_result(validation_result)

        logger.info(f"日频验证完成: {date}")
        return validation_result

    def run_weekly_validation(self, end_date: str) -> Dict:
        """
        执行周频验证

        参数:
        - end_date: 周末日期

        返回:
        - validation_result: 验证结果
        """
        logger.info(f"开始周频验证: {end_date}")

        start_date = self._get_week_start(end_date)

        trade_records = self.data_manager.query_trade_records(start_date, end_date)

        rolling_start = self._get_rolling_start(end_date, 20)
        rolling_records = self.data_manager.query_trade_records(rolling_start, end_date)

        return_metrics = self.performance_calculator.calculate_return(rolling_records)
        risk_metrics = self.performance_calculator.calculate_risk_metrics(
            rolling_records
        )
        risk_adjusted = self.performance_calculator.calculate_risk_adjusted_metrics(
            return_metrics, risk_metrics
        )
        trade_quality = self.performance_calculator.calculate_trade_quality(
            rolling_records
        )

        current_metrics = {
            "annual_return": return_metrics.get("annual_return", 0),
            "win_rate": trade_quality.get("win_rate", 0),
            "max_drawdown": risk_metrics.get("max_drawdown", 0),
            "sharpe_ratio": risk_adjusted.get("sharpe_ratio", 0),
            "profit_loss_ratio": trade_quality.get("profit_loss_ratio", 0),
        }

        decay_result = self.decay_detector.detect_decay(current_metrics)

        validation_result = {
            "validation_date": end_date,
            "validation_type": "weekly",
            "window_type": "rolling_20d",
            **return_metrics,
            **risk_metrics,
            **risk_adjusted,
            **trade_quality,
            "alert_level": decay_result["alert_level"],
            "triggered_metrics": decay_result["triggered_metrics"],
        }

        self._save_validation_result(validation_result)

        logger.info(f"周频验证完成: {end_date}")
        return validation_result

    def run_monthly_validation(self, end_date: str) -> Dict:
        """
        执行月频验证

        参数:
        - end_date: 月末日期

        返回:
        - validation_result: 验证结果
        """
        logger.info(f"开始月频验证: {end_date}")

        start_date = self._get_month_start(end_date)

        trade_records = self.data_manager.query_trade_records(start_date, end_date)

        rolling_start = self._get_rolling_start(end_date, 60)
        rolling_records = self.data_manager.query_trade_records(rolling_start, end_date)

        return_metrics = self.performance_calculator.calculate_return(rolling_records)
        risk_metrics = self.performance_calculator.calculate_risk_metrics(
            rolling_records
        )
        risk_adjusted = self.performance_calculator.calculate_risk_adjusted_metrics(
            return_metrics, risk_metrics
        )
        trade_quality = self.performance_calculator.calculate_trade_quality(
            rolling_records
        )

        current_metrics = {
            "annual_return": return_metrics.get("annual_return", 0),
            "win_rate": trade_quality.get("win_rate", 0),
            "max_drawdown": risk_metrics.get("max_drawdown", 0),
            "sharpe_ratio": risk_adjusted.get("sharpe_ratio", 0),
            "profit_loss_ratio": trade_quality.get("profit_loss_ratio", 0),
        }

        decay_result = self.decay_detector.detect_decay(
            current_metrics, duration_days=30
        )

        if not rolling_records.empty and "profit_loss_pct" in rolling_records.columns:
            returns = rolling_records["profit_loss_pct"].dropna().tolist()
            statistical_result = self.decay_detector.statistical_test(returns)
        else:
            statistical_result = {"is_significant": False, "p_value": None}

        validation_result = {
            "validation_date": end_date,
            "validation_type": "monthly",
            "window_type": "rolling_60d",
            **return_metrics,
            **risk_metrics,
            **risk_adjusted,
            **trade_quality,
            "alert_level": decay_result["alert_level"],
            "triggered_metrics": decay_result["triggered_metrics"],
            "decay_result": decay_result,
            "statistical_result": statistical_result,
        }

        self._save_validation_result(validation_result)

        logger.info(f"月频验证完成: {end_date}")
        return validation_result

    def _get_week_start(self, end_date: str) -> str:
        """获取周初日期"""
        date = pd.to_datetime(end_date)
        week_start = date - timedelta(days=date.weekday())
        return week_start.strftime("%Y-%m-%d")

    def _get_month_start(self, end_date: str) -> str:
        """获取月初日期"""
        date = pd.to_datetime(end_date)
        month_start = date.replace(day=1)
        return month_start.strftime("%Y-%m-%d")

    def _get_rolling_start(self, end_date: str, days: int) -> str:
        """获取滚动窗口起始日期"""
        date = pd.to_datetime(end_date)
        rolling_start = date - timedelta(days=days)
        return rolling_start.strftime("%Y-%m-%d")

    def _save_validation_result(self, result: Dict):
        """保存验证结果"""
        try:
            cursor = self.data_manager.conn.cursor()

            cursor.execute(
                """
                INSERT INTO validation_results
                (validation_date, validation_type, window_type,
                 annual_return, cumulative_return, win_rate, profit_loss_ratio,
                 max_drawdown, sharpe_ratio, alert_level, triggered_metrics)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
                (
                    result.get("validation_date"),
                    result.get("validation_type"),
                    result.get("window_type"),
                    result.get("annual_return"),
                    result.get("cumulative_return"),
                    result.get("win_rate"),
                    result.get("profit_loss_ratio"),
                    result.get("max_drawdown"),
                    result.get("sharpe_ratio"),
                    result.get("alert_level"),
                    str(result.get("triggered_metrics", [])),
                ),
            )

            self.data_manager.conn.commit()

        except Exception as e:
            logger.error(f"保存验证结果失败: {e}")

    def close(self):
        """关闭连接"""
        self.data_manager.close()


if __name__ == "__main__":
    engine = ValidationEngine("test_secondboard_oos.db")

    result = engine.run_daily_validation("2024-01-01")
    print(f"日频验证结果: {result['alert_level']}")

    engine.close()
