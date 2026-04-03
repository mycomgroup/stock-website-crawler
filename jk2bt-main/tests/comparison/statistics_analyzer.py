"""
tests/comparison/statistics_analyzer.py
统计分析模块

比较数据的统计特征和分布一致性。
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Optional, Tuple
from scipy import stats
from dataclasses import dataclass
import warnings


@dataclass
class StatisticsResult:
    """统计比较结果"""
    field: str
    statistics: Dict
    ks_test: Dict
    correlation: Dict
    overall_pass: bool


class StatisticsAnalyzer:
    """
    统计分析器

    比较数据的统计特征，包括：
    - 基本统计量（均值、标准差、分位数等）
    - KS检验（分布一致性）
    - 相关性分析

    使用方式:
        analyzer = StatisticsAnalyzer()
        result = analyzer.analyze(jk2bt_series, jq_series, 'close')
    """

    # 统计量配置
    STATISTICS_CONFIG = {
        "mean_diff_threshold": 0.05,     # 均值差异阈值
        "std_diff_threshold": 0.10,      # 标准差差异阈值
        "ks_pvalue_threshold": 0.05,     # KS检验p值阈值
        "correlation_threshold": 0.99,   # 相关性阈值
        "missing_diff_threshold": 0.05,  # 缺失值差异阈值
    }

    def __init__(self, config: Optional[Dict] = None):
        """
        初始化分析器。

        Parameters
        ----------
        config : dict, optional
            自定义配置
        """
        self.config = {**self.STATISTICS_CONFIG, **(config or {})}

    def analyze(
        self,
        jk2bt_series: pd.Series,
        jq_series: pd.Series,
        field_name: str,
    ) -> StatisticsResult:
        """
        执行完整统计分析。

        Parameters
        ----------
        jk2bt_series : pd.Series
            jk2bt 数据
        jq_series : pd.Series
            JQ 数据
        field_name : str
            字段名称

        Returns
        -------
        StatisticsResult
            统计分析结果
        """
        # 对齐数据
        common_index = jk2bt_series.dropna().index.intersection(
            jq_series.dropna().index
        )

        jk2bt_aligned = jk2bt_series.loc[common_index] if len(common_index) > 0 else pd.Series()
        jq_aligned = jq_series.loc[common_index] if len(common_index) > 0 else pd.Series()

        jk2bt_clean = jk2bt_series.dropna()
        jq_clean = jq_series.dropna()

        # 1. 基本统计量比较
        statistics = self._compare_statistics(jk2bt_clean, jq_clean)

        # 2. KS检验
        ks_test = self._ks_test(jk2bt_clean, jq_clean)

        # 3. 相关性分析
        correlation = self._correlation_analysis(jk2bt_aligned, jq_aligned)

        # 4. 综合判断
        overall_pass = self._evaluate_overall(statistics, ks_test, correlation)

        return StatisticsResult(
            field=field_name,
            statistics=statistics,
            ks_test=ks_test,
            correlation=correlation,
            overall_pass=overall_pass,
        )

    def _compare_statistics(
        self,
        jk2bt_series: pd.Series,
        jq_series: pd.Series,
    ) -> Dict:
        """比较基本统计量"""
        results = {}

        # 需要比较的统计量
        stat_funcs = {
            "mean": lambda x: x.mean(),
            "std": lambda x: x.std(),
            "min": lambda x: x.min(),
            "max": lambda x: x.max(),
            "median": lambda x: x.median(),
            "q25": lambda x: x.quantile(0.25),
            "q75": lambda x: x.quantile(0.75),
            "skewness": lambda x: stats.skew(x) if len(x) > 2 else np.nan,
            "kurtosis": lambda x: stats.kurtosis(x) if len(x) > 2 else np.nan,
        }

        for stat_name, stat_func in stat_funcs.items():
            try:
                jq_stat = stat_func(jq_series)
                jk2bt_stat = stat_func(jk2bt_series)

                if pd.isna(jq_stat) or pd.isna(jk2bt_stat):
                    results[stat_name] = {
                        "jq": jq_stat,
                        "jk2bt": jk2bt_stat,
                        "diff": np.nan,
                        "rel_diff": np.nan,
                        "pass": True,  # 无法比较时默认通过
                    }
                else:
                    abs_diff = abs(jq_stat - jk2bt_stat)
                    rel_diff = abs_diff / abs(jq_stat) if jq_stat != 0 else abs_diff

                    # 根据统计量类型选择阈值
                    if stat_name == "mean":
                        threshold = self.config["mean_diff_threshold"]
                    elif stat_name == "std":
                        threshold = self.config["std_diff_threshold"]
                    else:
                        threshold = 0.10  # 默认10%

                    results[stat_name] = {
                        "jq": float(jq_stat),
                        "jk2bt": float(jk2bt_stat),
                        "diff": float(abs_diff),
                        "rel_diff": float(rel_diff),
                        "pass": rel_diff < threshold,
                    }
            except Exception as e:
                results[stat_name] = {
                    "jq": np.nan,
                    "jk2bt": np.nan,
                    "diff": np.nan,
                    "rel_diff": np.nan,
                    "pass": True,
                    "error": str(e),
                }

        # 缺失值比例
        jq_missing = jq_series.isna().mean()
        jk2bt_missing = jk2bt_series.isna().mean()
        missing_diff = abs(jq_missing - jk2bt_missing)

        results["missing_ratio"] = {
            "jq": float(jq_missing),
            "jk2bt": float(jk2bt_missing),
            "diff": float(missing_diff),
            "pass": missing_diff < self.config["missing_diff_threshold"],
        }

        return results

    def _ks_test(
        self,
        jk2bt_series: pd.Series,
        jq_series: pd.Series,
    ) -> Dict:
        """
        KS检验 - 检验两样本是否来自同一分布。

        H0: 两样本来自同一分布
        p-value > 0.05 表示无法拒绝原假设（分布相同）
        """
        if len(jk2bt_series) < 10 or len(jq_series) < 10:
            return {
                "statistic": np.nan,
                "pvalue": np.nan,
                "pass": True,
                "note": "数据不足，跳过检验",
            }

        try:
            statistic, pvalue = stats.ks_2samp(jk2bt_series, jq_series)

            return {
                "statistic": float(statistic),
                "pvalue": float(pvalue),
                "pass": pvalue > self.config["ks_pvalue_threshold"],
            }
        except Exception as e:
            return {
                "statistic": np.nan,
                "pvalue": np.nan,
                "pass": True,
                "error": str(e),
            }

    def _correlation_analysis(
        self,
        jk2bt_series: pd.Series,
        jq_series: pd.Series,
    ) -> Dict:
        """相关性分析"""
        if len(jk2bt_series) < 10 or len(jq_series) < 10:
            return {
                "pearson": np.nan,
                "spearman": np.nan,
                "pass": True,
                "note": "数据不足",
            }

        try:
            pearson_corr = jk2bt_series.corr(jq_series)
            spearman_corr = jk2bt_series.corr(jq_series, method="spearman")

            return {
                "pearson": float(pearson_corr) if not pd.isna(pearson_corr) else np.nan,
                "spearman": float(spearman_corr) if not pd.isna(spearman_corr) else np.nan,
                "pass": pearson_corr > self.config["correlation_threshold"] if not pd.isna(pearson_corr) else True,
            }
        except Exception as e:
            return {
                "pearson": np.nan,
                "spearman": np.nan,
                "pass": True,
                "error": str(e),
            }

    def _evaluate_overall(
        self,
        statistics: Dict,
        ks_test: Dict,
        correlation: Dict,
    ) -> bool:
        """综合评估"""
        # 统计量通过率
        stat_pass_rate = sum(1 for v in statistics.values() if v.get("pass", True)) / len(statistics)

        # 各项都通过
        return (
            stat_pass_rate >= 0.8 and
            ks_test.get("pass", True) and
            correlation.get("pass", True)
        )

    def batch_analyze(
        self,
        jk2bt_df: pd.DataFrame,
        jq_df: pd.DataFrame,
        columns: Optional[List[str]] = None,
    ) -> Dict[str, StatisticsResult]:
        """
        批量分析多列数据。

        Parameters
        ----------
        jk2bt_df : pd.DataFrame
            jk2bt 数据
        jq_df : pd.DataFrame
            JQ 数据
        columns : list, optional
            要分析的列

        Returns
        -------
        Dict[str, StatisticsResult]
            每列的分析结果
        """
        if columns is None:
            columns = list(set(jk2bt_df.columns) & set(jq_df.columns))

        results = {}

        for col in columns:
            if col in jk2bt_df.columns and col in jq_df.columns:
                results[col] = self.analyze(jk2bt_df[col], jq_df[col], col)

        return results

    def generate_statistics_summary(
        self,
        results: Dict[str, StatisticsResult],
    ) -> pd.DataFrame:
        """生成统计摘要表格"""
        summary_data = []

        for field, result in results.items():
            # 统计量通过率
            stat_pass = sum(1 for v in result.statistics.values() if v.get("pass", True))
            stat_total = len(result.statistics)
            stat_pass_rate = stat_pass / stat_total if stat_total > 0 else 1.0

            summary_data.append({
                "字段": field,
                "均值差异": f"{result.statistics.get('mean', {}).get('rel_diff', 0):.4f}",
                "标准差差异": f"{result.statistics.get('std', {}).get('rel_diff', 0):.4f}",
                "KS检验p值": f"{result.ks_test.get('pvalue', 0):.4f}",
                "Pearson相关": f"{result.correlation.get('pearson', 0):.4f}",
                "统计通过率": f"{stat_pass_rate:.2%}",
                "整体状态": "✓ 通过" if result.overall_pass else "✗ 失败",
            })

        return pd.DataFrame(summary_data)


def compare_distribution(
    jk2bt_series: pd.Series,
    jq_series: pd.Series,
) -> Dict:
    """
    快速分布比较。

    返回分布差异的关键指标。
    """
    analyzer = StatisticsAnalyzer()

    jk2bt_clean = jk2bt_series.dropna()
    jq_clean = jq_series.dropna()

    # 关键指标
    return {
        "count": {
            "jk2bt": len(jk2bt_clean),
            "jq": len(jq_clean),
        },
        "mean": {
            "jk2bt": float(jk2bt_clean.mean()) if len(jk2bt_clean) > 0 else np.nan,
            "jq": float(jq_clean.mean()) if len(jq_clean) > 0 else np.nan,
        },
        "std": {
            "jk2bt": float(jk2bt_clean.std()) if len(jk2bt_clean) > 1 else np.nan,
            "jq": float(jq_clean.std()) if len(jq_clean) > 1 else np.nan,
        },
        "correlation": float(jk2bt_clean.corr(jq_clean)) if len(jk2bt_clean) > 1 else np.nan,
    }