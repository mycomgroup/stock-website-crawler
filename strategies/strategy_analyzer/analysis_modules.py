"""
分析模块集合
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Optional, Tuple
from .market_classifier import MarketStateClassifier
from .risk_metrics import RiskMetrics


class AnalysisModules:
    """分析模块集合"""

    def __init__(self, config):
        """
        Args:
            config: AnalyzerConfig 配置对象
        """
        self.config = config
        self.classifier = MarketStateClassifier(config.get_thresholds())
        self.risk_calc = RiskMetrics(
            risk_free_rate=config.risk_free_rate,
            periods_per_year=12 if config.freq == "monthly" else 4,
        )

    def yearly_analysis(
        self,
        df: pd.DataFrame,
        strategy_cols: List[str],
        benchmark_cols: List[str] = None,
    ) -> pd.DataFrame:
        """按年度统计各策略累计收益

        Args:
            df: 数据框 (需包含 date 列)
            strategy_cols: 策略收益列名列表
            benchmark_cols: 基准收益列名列表

        Returns:
            年度统计结果
        """
        df = df.copy()
        df["year"] = df["date"].dt.year

        all_cols = strategy_cols.copy()
        if benchmark_cols:
            all_cols.extend(benchmark_cols)

        agg_dict = {}
        for col in all_cols:
            agg_dict[col] = (
                lambda x: (1 + x.dropna()).prod() - 1 if len(x.dropna()) > 0 else 0
            )

        yearly = df.groupby("year").agg(agg_dict).round(4)
        return yearly

    def regime_analysis(
        self, df: pd.DataFrame, strategy_cols: List[str], benchmark_ret_col: str
    ) -> Dict[str, Dict]:
        """按市场状态分类统计

        Args:
            df: 数据框
            strategy_cols: 策略收益列名列表
            benchmark_ret_col: 基准收益列名

        Returns:
            {regime: {strategy: {mean_ret, cum_ret, count, positive_rate}}}
        """
        df = df.copy()
        df["regime"] = self.classifier.classify_series(df[benchmark_ret_col])

        results = {}
        for regime in self.classifier.get_all_states():
            subset = df[df["regime"] == regime]
            if len(subset) == 0:
                continue

            label = self.classifier.get_state_label(regime)
            results[label] = {"count": len(subset)}

            for col in strategy_cols:
                rets = subset[col]
                results[label][col] = {
                    "mean_ret": rets.mean(),
                    "cum_ret": (1 + rets).prod() - 1 if len(rets) > 0 else 0,
                    "count": len(rets),
                    "positive_rate": (rets > 0).sum() / len(rets)
                    if len(rets) > 0
                    else 0,
                    "std": rets.std() if len(rets) > 1 else 0,
                }

        return results

    def timing_analysis(
        self, df: pd.DataFrame, strategy_cols: List[str], benchmark_ret_col: str
    ) -> Dict[str, Dict]:
        """择时效果对比

        Args:
            df: 数据框
            strategy_cols: 策略收益列名列表
            benchmark_ret_col: 基准收益列名

        Returns:
            {strategy: {timing_mode: {cum_ret, ann_ret, periods, pct}}}
        """
        df = df.copy()
        df["benchmark_lag1"] = df[benchmark_ret_col].shift(1)

        total_periods = len(df)

        results = {}
        for col in strategy_cols:
            results[col] = {}

            # 不择时
            all_rets = df[col]
            results[col]["不择时"] = {
                "cum_ret": (1 + all_rets).prod() - 1,
                "ann_ret": self.risk_calc.annualized_return(all_rets),
                "periods": total_periods,
                "pct": 1.0,
            }

            # 各种择时阈值
            for threshold in self.config.timing_thresholds:
                if threshold >= 0:
                    label = f"前季>{threshold:.0%}做"
                    mask = df["benchmark_lag1"] > threshold
                else:
                    label = f"前季<{threshold:.0%}做"
                    mask = df["benchmark_lag1"] < threshold

                timing_rets = df.loc[mask, col]
                timing_periods = len(timing_rets)

                if timing_periods > 0:
                    results[col][label] = {
                        "cum_ret": (1 + timing_rets).prod() - 1,
                        "ann_ret": self.risk_calc.annualized_return(timing_rets),
                        "periods": timing_periods,
                        "pct": timing_periods / total_periods,
                    }

        return results

    def lag_analysis(
        self,
        df: pd.DataFrame,
        strategy_cols: List[str],
        benchmark_ret_col: str,
        lag_periods: List[int] = [1],
    ) -> Dict:
        """前N期涨跌对后续收益的影响

        Args:
            df: 数据框
            strategy_cols: 策略收益列名列表
            benchmark_ret_col: 基准收益列名
            lag_periods: 滞后期数列表

        Returns:
            {lag: {condition: {strategy: mean_ret}}}
        """
        df = df.copy()

        results = {}
        for lag in lag_periods:
            lag_col = f"benchmark_lag{lag}"
            df[lag_col] = df[benchmark_ret_col].shift(lag)

            results[f"前{lag}期"] = {}

            # 上涨
            up_mask = df[lag_col] > 0.05
            if up_mask.sum() > 0:
                results[f"前{lag}期"]["涨幅>5%"] = {
                    col: df.loc[up_mask, col].mean() for col in strategy_cols
                }
                results[f"前{lag}期"]["涨幅>5%"]["count"] = int(up_mask.sum())

            # 下跌
            down_mask = df[lag_col] < -0.05
            if down_mask.sum() > 0:
                results[f"前{lag}期"]["跌幅>5%"] = {
                    col: df.loc[down_mask, col].mean() for col in strategy_cols
                }
                results[f"前{lag}期"]["跌幅>5%"]["count"] = int(down_mask.sum())

            # 震荡
            neutral_mask = (df[lag_col] >= -0.05) & (df[lag_col] <= 0.05)
            if neutral_mask.sum() > 0:
                results[f"前{lag}期"]["波动<5%"] = {
                    col: df.loc[neutral_mask, col].mean() for col in strategy_cols
                }
                results[f"前{lag}期"]["波动<5%"]["count"] = int(neutral_mask.sum())

        return results

    def recent_analysis(
        self,
        df: pd.DataFrame,
        strategy_cols: List[str],
        benchmark_cols: List[str] = None,
    ) -> Dict:
        """近期表现分析

        Args:
            df: 数据框
            strategy_cols: 策略收益列名列表
            benchmark_cols: 基准收益列名列表

        Returns:
            近期分析结果
        """
        recent = df[df["date"] >= self.config.recent_since].copy()

        results = {
            "periods": len(recent),
            "since": self.config.recent_since,
        }

        # 各策略累计收益
        for col in strategy_cols:
            rets = recent[col]
            results[col] = {
                "cum_ret": (1 + rets).prod() - 1,
                "mean_ret": rets.mean(),
                "win_rate": (rets > 0).sum() / len(rets) if len(rets) > 0 else 0,
            }

        # 基准收益
        if benchmark_cols:
            for col in benchmark_cols:
                rets = recent[col]
                results[col] = {
                    "cum_ret": (1 + rets.dropna()).prod() - 1
                    if len(rets.dropna()) > 0
                    else 0,
                    "mean_ret": rets.mean(),
                }

        # 逐期明细
        period_details = []
        for _, row in recent.iterrows():
            detail = {"date": row["date"].strftime("%Y-%m")}
            for col in strategy_cols + (benchmark_cols or []):
                detail[col] = row.get(col, 0)
            period_details.append(detail)

        results["details"] = period_details

        return results

    def condition_summary(
        self, df: pd.DataFrame, strategy_col: str, benchmark_ret_col: str
    ) -> Dict:
        """适合做的条件总结

        Args:
            df: 数据框
            strategy_col: 策略收益列名
            benchmark_ret_col: 基准收益列名

        Returns:
            正/负收益期的市场特征
        """
        df = df.copy()
        df["benchmark_lag1"] = df[benchmark_ret_col].shift(1)

        positive = df[df[strategy_col] > 0]
        negative = df[df[strategy_col] < 0]

        results = {
            "positive": {
                "count": len(positive),
                "pct": len(positive) / len(df) if len(df) > 0 else 0,
                "benchmark_current_mean": positive[benchmark_ret_col].mean()
                if len(positive) > 0
                else 0,
                "benchmark_lag1_mean": positive["benchmark_lag1"].mean()
                if len(positive) > 0
                else 0,
            },
            "negative": {
                "count": len(negative),
                "pct": len(negative) / len(df) if len(df) > 0 else 0,
                "benchmark_current_mean": negative[benchmark_ret_col].mean()
                if len(negative) > 0
                else 0,
                "benchmark_lag1_mean": negative["benchmark_lag1"].mean()
                if len(negative) > 0
                else 0,
            },
        }

        return results

    def risk_analysis(
        self,
        df: pd.DataFrame,
        strategy_cols: List[str],
        benchmark_cols: List[str] = None,
    ) -> Dict[str, Dict]:
        """风险指标分析

        Args:
            df: 数据框
            strategy_cols: 策略收益列名列表
            benchmark_cols: 基准收益列名列表

        Returns:
            {strategy: {指标: 值}}
        """
        results = {}

        # 策略风险指标
        for col in strategy_cols:
            results[col] = self.risk_calc.calculate_all(df[col])

        # 相对基准风险指标
        if benchmark_cols:
            for strat_col in strategy_cols:
                for bench_col in benchmark_cols:
                    key = f"{strat_col}_vs_{bench_col}"
                    results[key] = self.risk_calc.calculate_relative(
                        df[strat_col], df[bench_col]
                    )

        return results
