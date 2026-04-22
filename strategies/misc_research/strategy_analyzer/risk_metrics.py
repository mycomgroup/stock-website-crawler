"""
风险指标计算模块
"""

import pandas as pd
import numpy as np
from typing import Dict, Optional, Tuple


class RiskMetrics:
    """风险指标计算器"""

    def __init__(self, risk_free_rate: float = 0.02, periods_per_year: int = 4):
        """
        Args:
            risk_free_rate: 无风险利率 (年化)
            periods_per_year: 每年期数 (季度=4, 月度=12)
        """
        self.risk_free_rate = risk_free_rate
        self.periods_per_year = periods_per_year

    def annualized_return(self, returns: pd.Series) -> float:
        """计算年化收益率

        Args:
            returns: 定期收益率序列

        Returns:
            年化收益率
        """
        if len(returns) == 0:
            return 0.0
        cum_return = (1 + returns).prod() - 1
        n_periods = len(returns)
        years = n_periods / self.periods_per_year
        if years <= 0:
            return 0.0
        return (1 + cum_return) ** (1 / years) - 1

    def annualized_volatility(self, returns: pd.Series) -> float:
        """计算年化波动率

        Args:
            returns: 定期收益率序列

        Returns:
            年化波动率
        """
        if len(returns) < 2:
            return 0.0
        return returns.std() * np.sqrt(self.periods_per_year)

    def sharpe_ratio(self, returns: pd.Series) -> float:
        """计算夏普比率

        Args:
            returns: 定期收益率序列

        Returns:
            夏普比率
        """
        ann_ret = self.annualized_return(returns)
        ann_vol = self.annualized_volatility(returns)
        if ann_vol == 0:
            return 0.0
        return (ann_ret - self.risk_free_rate) / ann_vol

    def max_drawdown(self, returns: pd.Series) -> Tuple[float, int, int]:
        """计算最大回撤

        Args:
            returns: 定期收益率序列

        Returns:
            (最大回撤, 开始位置, 结束位置)
        """
        if len(returns) == 0:
            return 0.0, 0, 0

        cum_returns = (1 + returns).cumprod()
        running_max = cum_returns.cummax()
        drawdown = (cum_returns - running_max) / running_max

        max_dd = drawdown.min()
        end_idx = drawdown.idxmin()

        # 找到回撤开始位置
        start_idx = cum_returns[:end_idx].idxmax()

        return abs(max_dd), start_idx, end_idx

    def max_drawdown_duration(self, returns: pd.Series) -> int:
        """计算最大回撤持续期数

        Args:
            returns: 定期收益率序列

        Returns:
            最大回撤持续期数
        """
        if len(returns) == 0:
            return 0

        cum_returns = (1 + returns).cumprod()
        running_max = cum_returns.cummax()

        # 计算每次创新高之间的期数
        peak_indices = []
        current_peak_idx = 0

        for i, (cum, running) in enumerate(zip(cum_returns, running_max)):
            if cum >= running:
                if i > current_peak_idx:
                    peak_indices.append(i - current_peak_idx)
                current_peak_idx = i

        # 检查最后一段
        if len(cum_returns) - 1 > current_peak_idx:
            peak_indices.append(len(cum_returns) - 1 - current_peak_idx)

        return max(peak_indices) if peak_indices else 0

    def calmar_ratio(self, returns: pd.Series) -> float:
        """计算Calmar比率

        Args:
            returns: 定期收益率序列

        Returns:
            Calmar比率
        """
        ann_ret = self.annualized_return(returns)
        max_dd, _, _ = self.max_drawdown(returns)
        if max_dd == 0:
            return 0.0
        return ann_ret / max_dd

    def sortino_ratio(self, returns: pd.Series) -> float:
        """计算Sortino比率

        Args:
            returns: 定期收益率序列

        Returns:
            Sortino比率
        """
        ann_ret = self.annualized_return(returns)
        downside_returns = returns[returns < 0]

        if len(downside_returns) < 2:
            return 0.0

        downside_vol = downside_returns.std() * np.sqrt(self.periods_per_year)
        if downside_vol == 0:
            return 0.0

        return (ann_ret - self.risk_free_rate) / downside_vol

    def win_rate(self, returns: pd.Series) -> float:
        """计算胜率

        Args:
            returns: 定期收益率序列

        Returns:
            胜率
        """
        if len(returns) == 0:
            return 0.0
        return (returns > 0).sum() / len(returns)

    def profit_loss_ratio(self, returns: pd.Series) -> float:
        """计算盈亏比

        Args:
            returns: 定期收益率序列

        Returns:
            盈亏比
        """
        wins = returns[returns > 0]
        losses = returns[returns < 0]

        if len(wins) == 0 or len(losses) == 0:
            return 0.0

        avg_win = wins.mean()
        avg_loss = abs(losses.mean())

        if avg_loss == 0:
            return 0.0

        return avg_win / avg_loss

    def calculate_all(self, returns: pd.Series) -> Dict[str, float]:
        """计算所有风险指标

        Args:
            returns: 定期收益率序列

        Returns:
            风险指标字典
        """
        max_dd, dd_start, dd_end = self.max_drawdown(returns)

        return {
            "cumulative_return": (1 + returns).prod() - 1,
            "annualized_return": self.annualized_return(returns),
            "annualized_volatility": self.annualized_volatility(returns),
            "sharpe_ratio": self.sharpe_ratio(returns),
            "sortino_ratio": self.sortino_ratio(returns),
            "max_drawdown": max_dd,
            "max_drawdown_duration": self.max_drawdown_duration(returns),
            "calmar_ratio": self.calmar_ratio(returns),
            "win_rate": self.win_rate(returns),
            "profit_loss_ratio": self.profit_loss_ratio(returns),
            "periods": len(returns),
        }

    def calculate_relative(
        self, strategy_returns: pd.Series, benchmark_returns: pd.Series
    ) -> Dict[str, float]:
        """计算相对基准的风险指标

        Args:
            strategy_returns: 策略收益率序列
            benchmark_returns: 基准收益率序列

        Returns:
            相对风险指标字典
        """
        # 对齐索引
        aligned = pd.DataFrame(
            {"strategy": strategy_returns, "benchmark": benchmark_returns}
        ).dropna()

        if len(aligned) == 0:
            return {}

        excess_returns = aligned["strategy"] - aligned["benchmark"]

        # 跟踪误差
        tracking_error = excess_returns.std() * np.sqrt(self.periods_per_year)

        # 信息比率
        info_ratio = 0.0
        if tracking_error > 0:
            info_ratio = excess_returns.mean() * self.periods_per_year / tracking_error

        # Beta
        cov = aligned.cov().iloc[0, 1]
        var = aligned["benchmark"].var()
        beta = cov / var if var > 0 else 1.0

        # Alpha
        strategy_ann = self.annualized_return(aligned["strategy"])
        benchmark_ann = self.annualized_return(aligned["benchmark"])
        alpha = strategy_ann - (
            self.risk_free_rate + beta * (benchmark_ann - self.risk_free_rate)
        )

        return {
            "excess_return": (1 + excess_returns).prod() - 1,
            "annualized_excess": excess_returns.mean() * self.periods_per_year,
            "tracking_error": tracking_error,
            "information_ratio": info_ratio,
            "beta": beta,
            "alpha": alpha,
        }
