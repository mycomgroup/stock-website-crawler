# -*- coding: utf-8 -*-
"""
因子对比实验模块
用于统一比较不同因子的有效性
"""

import pandas as pd
import numpy as np
from scipy import stats
import matplotlib.pyplot as plt


class FactorComparison:
    """因子对比实验器"""

    def __init__(self):
        """初始化因子对比器"""
        self.factors = {}
        self.ic_results = {}
        self.performance_results = {}

    def add_factor(self, name, factor_data, description=""):
        """
        添加因子

        Args:
            name: 因子名称
            factor_data: 因子数据DataFrame
            description: 因子描述
        """
        self.factors[name] = {"data": factor_data, "description": description}
        print(f"已添加因子: {name}")

    def calculate_ic(self, forward_returns, factor_names=None):
        """
        计算各因子的IC值

        Args:
            forward_returns: 未来收益率数据
            factor_names: 要计算的因子名称列表

        Returns:
            dict: IC计算结果
        """
        factor_names = factor_names or list(self.factors.keys())

        for name in factor_names:
            if name not in self.factors:
                print(f"警告: 因子 {name} 不存在，跳过")
                continue

            factor_data = self.factors[name]["data"]

            # 对齐数据
            common_dates = factor_data.index.intersection(forward_returns.index)
            common_codes = factor_data.columns.intersection(forward_returns.columns)

            if len(common_dates) == 0 or len(common_codes) == 0:
                print(f"警告: 因子 {name} 与收益率数据无交集，跳过")
                continue

            factor_aligned = factor_data.loc[common_dates, common_codes]
            returns_aligned = forward_returns.loc[common_dates, common_codes]

            # 计算每日IC
            ic_series = pd.Series(index=common_dates, dtype=float)
            for date in common_dates:
                daily_factor = factor_aligned.loc[date].dropna()
                daily_returns = returns_aligned.loc[date].dropna()

                # 取交集
                common = daily_factor.index.intersection(daily_returns.index)
                if len(common) > 2:
                    ic = daily_factor[common].corr(daily_returns[common])
                    ic_series[date] = ic

            # 计算统计指标
            ic_clean = ic_series.dropna()
            self.ic_results[name] = {
                "mean": ic_clean.mean(),
                "std": ic_clean.std(),
                "icir": ic_clean.mean() / ic_clean.std() if ic_clean.std() > 0 else 0,
                "positive_ratio": (ic_clean > 0).mean(),
                "abs_mean": ic_clean.abs().mean(),
                "series": ic_clean,
            }

        return self.ic_results

    def compare_factors(self, factor_names=None):
        """
        对比各因子的IC表现

        Args:
            factor_names: 要对比的因子名称列表

        Returns:
            pd.DataFrame: 对比结果
        """
        factor_names = factor_names or list(self.ic_results.keys())

        results = []
        for name in factor_names:
            if name not in self.ic_results:
                continue

            ic_result = self.ic_results[name]
            results.append(
                {
                    "factor": name,
                    "ic_mean": ic_result["mean"],
                    "ic_std": ic_result["std"],
                    "icir": ic_result["icir"],
                    "positive_ratio": ic_result["positive_ratio"],
                    "abs_ic_mean": ic_result["abs_mean"],
                }
            )

        df = pd.DataFrame(results)

        if len(df) > 0:
            df = df.sort_values("icir", ascending=False)

        return df

    def plot_ic_comparison(self, factor_names=None, save_path=None):
        """
        绘制IC对比图

        Args:
            factor_names: 要绘制的因子名称列表
            save_path: 保存路径
        """
        factor_names = factor_names or list(self.ic_results.keys())

        fig, axes = plt.subplots(2, 2, figsize=(14, 10))

        # 1. IC均值对比
        ax1 = axes[0, 0]
        ic_means = [
            self.ic_results[name]["mean"]
            for name in factor_names
            if name in self.ic_results
        ]
        ax1.bar(range(len(ic_means)), ic_means)
        ax1.set_xticks(range(len(ic_means)))
        ax1.set_xticklabels(
            [name for name in factor_names if name in self.ic_results], rotation=45
        )
        ax1.set_title("IC均值对比", fontsize=14)
        ax1.axhline(y=0, color="r", linestyle="--", alpha=0.5)
        ax1.grid(True, alpha=0.3)

        # 2. ICIR对比
        ax2 = axes[0, 1]
        icirs = [
            self.ic_results[name]["icir"]
            for name in factor_names
            if name in self.ic_results
        ]
        ax2.bar(range(len(icirs)), icirs)
        ax2.set_xticks(range(len(icirs)))
        ax2.set_xticklabels(
            [name for name in factor_names if name in self.ic_results], rotation=45
        )
        ax2.set_title("ICIR对比", fontsize=14)
        ax2.axhline(y=0, color="r", linestyle="--", alpha=0.5)
        ax2.grid(True, alpha=0.3)

        # 3. IC正比例对比
        ax3 = axes[1, 0]
        positive_ratios = [
            self.ic_results[name]["positive_ratio"]
            for name in factor_names
            if name in self.ic_results
        ]
        ax3.bar(range(len(positive_ratios)), positive_ratios)
        ax3.set_xticks(range(len(positive_ratios)))
        ax3.set_xticklabels(
            [name for name in factor_names if name in self.ic_results], rotation=45
        )
        ax3.set_title("IC正比例对比", fontsize=14)
        ax3.axhline(y=0.5, color="r", linestyle="--", alpha=0.5)
        ax3.grid(True, alpha=0.3)

        # 4. IC时序图
        ax4 = axes[1, 1]
        for name in factor_names:
            if name in self.ic_results:
                ic_series = self.ic_results[name]["series"]
                ax4.plot(ic_series.index, ic_series.values, label=name, alpha=0.7)
        ax4.set_title("IC时序图", fontsize=14)
        ax4.legend(loc="best")
        ax4.axhline(y=0, color="r", linestyle="--", alpha=0.5)
        ax4.grid(True, alpha=0.3)

        plt.tight_layout()

        if save_path:
            plt.savefig(save_path, dpi=150, bbox_inches="tight")
            print(f"图表已保存到 {save_path}")

        plt.show()

    def calculate_half_life(self, factor_name, max_lag=20):
        """
        计算因子半衰期

        Args:
            factor_name: 因子名称
            max_lag: 最大滞后阶数

        Returns:
            float: 半衰期
        """
        if factor_name not in self.factors:
            raise ValueError(f"因子 {factor_name} 不存在")

        from statsmodels.tsa.stattools import acf

        factor_data = self.factors[factor_name]["data"]

        # 对每只ETF计算半衰期，然后取平均
        half_lives = []
        for code in factor_data.columns:
            series = factor_data[code].dropna()
            if len(series) < max_lag * 2:
                continue

            autocorr = acf(series, nlags=max_lag)

            for lag in range(1, len(autocorr)):
                if autocorr[lag] < 0.5:
                    half_lives.append(lag)
                    break

        if half_lives:
            return np.mean(half_lives)
        return np.nan

    def generate_report(self, save_path=None):
        """
        生成因子对比报告

        Args:
            save_path: 保存路径

        Returns:
            str: 报告文本
        """
        comparison_df = self.compare_factors()

        report = f"""
因子对比实验报告
{"=" * 60}

因子IC对比结果
{"=" * 60}
{comparison_df.to_string(index=False)}

因子详细信息
{"=" * 60}
"""

        for name, factor_info in self.factors.items():
            report += f"\n{name}\n"
            report += f"描述: {factor_info['description']}\n"
            report += f"数据形状: {factor_info['data'].shape}\n"

            if name in self.ic_results:
                ic_result = self.ic_results[name]
                report += f"IC均值: {ic_result['mean']:.4f}\n"
                report += f"IC标准差: {ic_result['std']:.4f}\n"
                report += f"ICIR: {ic_result['icir']:.4f}\n"
                report += f"IC正比例: {ic_result['positive_ratio']:.2%}\n"

            half_life = self.calculate_half_life(name)
            if not np.isnan(half_life):
                report += f"半衰期: {half_life:.1f} 天\n"

            report += "-" * 40 + "\n"

        if save_path:
            with open(save_path, "w", encoding="utf-8") as f:
                f.write(report)
            print(f"报告已保存到 {save_path}")

        return report

    def save_results(self, filepath):
        """保存对比结果到文件"""
        comparison_df = self.compare_factors()
        comparison_df.to_csv(filepath, index=False)
        print(f"结果已保存到 {filepath}")
