"""
tests/comparison/visualizer.py
可视化模块

生成数据比较的图表。
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Optional, Tuple
import warnings

# 尝试导入 matplotlib，用于绑定后端
try:
    import matplotlib
    matplotlib.use('Agg')  # 非交互式后端
    import matplotlib.pyplot as plt
    MATPLOTLIB_AVAILABLE = True
except ImportError:
    MATPLOTLIB_AVAILABLE = False
    warnings.warn("matplotlib 未安装，可视化功能不可用")

# 尝试导入 seaborn
try:
    import seaborn as sns
    SEABORN_AVAILABLE = True
except ImportError:
    SEABORN_AVAILABLE = False


class DataVisualizer:
    """
    数据可视化器

    生成比较结果的图表，包括：
    - 时序对比图
    - 散点对比图
    - 差异分布图
    - 热力图

    使用方式:
        visualizer = DataVisualizer()
        visualizer.plot_comparison(jk2bt_series, jq_series, 'close', 'output.png')
    """

    def __init__(self, style: str = "seaborn-v0_8-whitegrid"):
        """初始化可视化器"""
        if not MATPLOTLIB_AVAILABLE:
            raise ImportError("matplotlib 未安装，无法使用可视化功能")

        # 设置样式
        try:
            plt.style.use(style)
        except Exception:
            pass  # 使用默认样式

        # 设置中文字体
        plt.rcParams["font.sans-serif"] = ["Arial Unicode MS", "SimHei", "DejaVu Sans"]
        plt.rcParams["axes.unicode_minus"] = False

    def plot_comparison(
        self,
        jk2bt_series: pd.Series,
        jq_series: pd.Series,
        title: str,
        save_path: Optional[str] = None,
        figsize: Tuple[int, int] = (14, 10),
    ) -> Optional["plt.Figure"]:
        """
        绘制对比图。

        Parameters
        ----------
        jk2bt_series : pd.Series
            jk2bt 数据
        jq_series : pd.Series
            JQ 数据
        title : str
            图表标题
        save_path : str, optional
            保存路径
        figsize : tuple
            图表大小

        Returns
        -------
        plt.Figure or None
            图表对象
        """
        fig, axes = plt.subplots(2, 2, figsize=figsize)

        # 1. 时序对比
        ax1 = axes[0, 0]
        ax1.plot(jq_series.index, jq_series.values, label='JQ', alpha=0.7, linewidth=1)
        ax1.plot(jk2bt_series.index, jk2bt_series.values, label='jk2bt', alpha=0.7, linewidth=1)
        ax1.set_title(f'{title} - 时间序列对比')
        ax1.set_xlabel('日期')
        ax1.set_ylabel('值')
        ax1.legend()
        ax1.grid(True, alpha=0.3)

        # 2. 散点图
        ax2 = axes[0, 1]
        common_index = jq_series.dropna().index.intersection(jk2bt_series.dropna().index)
        if len(common_index) > 0:
            jq_vals = jq_series.loc[common_index]
            jk2bt_vals = jk2bt_series.loc[common_index]

            ax2.scatter(jq_vals, jk2bt_vals, alpha=0.5, s=10)

            # 添加 y=x 参考线
            min_val = min(jq_vals.min(), jk2bt_vals.min())
            max_val = max(jq_vals.max(), jk2bt_vals.max())
            ax2.plot([min_val, max_val], [min_val, max_val], 'r--', label='y=x', linewidth=2)

            ax2.set_xlabel('JQ')
            ax2.set_ylabel('jk2bt')
            ax2.set_title('散点对比')
            ax2.legend()
        ax2.grid(True, alpha=0.3)

        # 3. 差异分布
        ax3 = axes[1, 0]
        diff = jk2bt_series - jq_series
        diff_clean = diff.dropna()
        if len(diff_clean) > 0:
            ax3.hist(diff_clean, bins=50, edgecolor='black', alpha=0.7)
            ax3.axvline(x=0, color='r', linestyle='--', linewidth=2, label='零线')
            ax3.axvline(x=diff_clean.mean(), color='g', linestyle='-', linewidth=2, label=f'均值: {diff_clean.mean():.4f}')
            ax3.set_xlabel('差异值 (jk2bt - JQ)')
            ax3.set_ylabel('频数')
            ax3.set_title('差异分布')
            ax3.legend()
        ax3.grid(True, alpha=0.3)

        # 4. Q-Q 图
        ax4 = axes[1, 1]
        diff_clean = (jk2bt_series - jq_series).dropna()
        if len(diff_clean) > 10:
            from scipy import stats
            stats.probplot(diff_clean, dist="norm", plot=ax4)
            ax4.set_title('差异 Q-Q 图')
        ax4.grid(True, alpha=0.3)

        plt.suptitle(title, fontsize=14, fontweight='bold')
        plt.tight_layout()

        if save_path:
            plt.savefig(save_path, dpi=150, bbox_inches='tight')

        return fig

    def plot_summary_heatmap(
        self,
        comparison_results: Dict,
        save_path: Optional[str] = None,
        figsize: Tuple[int, int] = (12, 8),
    ) -> Optional["plt.Figure"]:
        """
        绘制比较结果热力图。

        Parameters
        ----------
        comparison_results : Dict
            比较结果
        save_path : str, optional
            保存路径
        figsize : tuple
            图表大小

        Returns
        -------
        plt.Figure or None
        """
        if not comparison_results:
            return None

        # 构建数据矩阵
        fields = list(comparison_results.keys())
        metrics = ["pass_rate", "max_rel_diff", "mean_rel_diff", "diff_count", "nan_diff_count"]

        data = []
        for field in fields:
            result = comparison_results[field]
            row = [
                result.pass_rate,
                result.max_rel_diff,
                result.mean_rel_diff,
                result.diff_count / max(result.total_count, 1),  # 归一化
                result.nan_diff_count / max(result.total_count, 1),  # 归一化
            ]
            data.append(row)

        df = pd.DataFrame(data, index=fields, columns=["通过率", "最大误差", "平均误差", "差异比例", "NaN差异比例"])

        # 绘制热力图
        fig, ax = plt.subplots(figsize=figsize)

        if SEABORN_AVAILABLE:
            sns.heatmap(
                df,
                annot=True,
                fmt='.4f',
                cmap='RdYlGn',
                center=0.5,
                ax=ax,
            )
        else:
            # 没有 seaborn 时的简单实现
            cax = ax.imshow(df.values, cmap='RdYlGn', aspect='auto')
            ax.set_xticks(range(len(df.columns)))
            ax.set_xticklabels(df.columns, rotation=45, ha='right')
            ax.set_yticks(range(len(df.index)))
            ax.set_yticklabels(df.index)
            fig.colorbar(cax, ax=ax)

        ax.set_title('数据比较结果汇总')

        plt.tight_layout()

        if save_path:
            plt.savefig(save_path, dpi=150, bbox_inches='tight')

        return fig

    def plot_statistics_comparison(
        self,
        statistics_results: Dict,
        save_path: Optional[str] = None,
        figsize: Tuple[int, int] = (14, 8),
    ) -> Optional["plt.Figure"]:
        """
        绘制统计特征对比图。

        Parameters
        ----------
        statistics_results : Dict
            统计分析结果
        save_path : str, optional
            保存路径
        figsize : tuple
            图表大小

        Returns
        -------
        plt.Figure or None
        """
        if not statistics_results:
            return None

        fields = list(statistics_results.keys())

        # 提取关键统计量
        jq_means = []
        jk2bt_means = []
        jq_stds = []
        jk2bt_stds = []

        for field in fields:
            result = statistics_results[field]
            jq_means.append(result.statistics.get('mean', {}).get('jq', 0))
            jk2bt_means.append(result.statistics.get('mean', {}).get('jk2bt', 0))
            jq_stds.append(result.statistics.get('std', {}).get('jq', 0))
            jk2bt_stds.append(result.statistics.get('std', {}).get('jk2bt', 0))

        fig, axes = plt.subplots(1, 2, figsize=figsize)

        # 1. 均值对比
        ax1 = axes[0]
        x = range(len(fields))
        width = 0.35
        ax1.bar([i - width/2 for i in x], jq_means, width, label='JQ', alpha=0.7)
        ax1.bar([i + width/2 for i in x], jk2bt_means, width, label='jk2bt', alpha=0.7)
        ax1.set_xlabel('字段')
        ax1.set_ylabel('均值')
        ax1.set_title('均值对比')
        ax1.set_xticks(x)
        ax1.set_xticklabels(fields, rotation=45, ha='right')
        ax1.legend()
        ax1.grid(True, alpha=0.3)

        # 2. 标准差对比
        ax2 = axes[1]
        ax2.bar([i - width/2 for i in x], jq_stds, width, label='JQ', alpha=0.7)
        ax2.bar([i + width/2 for i in x], jk2bt_stds, width, label='jk2bt', alpha=0.7)
        ax2.set_xlabel('字段')
        ax2.set_ylabel('标准差')
        ax2.set_title('标准差对比')
        ax2.set_xticks(x)
        ax2.set_xticklabels(fields, rotation=45, ha='right')
        ax2.legend()
        ax2.grid(True, alpha=0.3)

        plt.suptitle('统计特征对比', fontsize=14, fontweight='bold')
        plt.tight_layout()

        if save_path:
            plt.savefig(save_path, dpi=150, bbox_inches='tight')

        return fig

    def plot_correlation_heatmap(
        self,
        jk2bt_df: pd.DataFrame,
        jq_df: pd.DataFrame,
        save_path: Optional[str] = None,
        figsize: Tuple[int, int] = (10, 8),
    ) -> Optional["plt.Figure"]:
        """
        绘制相关性热力图。

        Parameters
        ----------
        jk2bt_df : pd.DataFrame
            jk2bt 数据
        jq_df : pd.DataFrame
            JQ 数据
        save_path : str, optional
            保存路径
        figsize : tuple
            图表大小

        Returns
        -------
        plt.Figure or None
        """
        # 计算各字段的相关性
        common_cols = list(set(jk2bt_df.columns) & set(jq_df.columns))

        correlations = {}
        for col in common_cols:
            if col in jk2bt_df.columns and col in jq_df.columns:
                common_index = jk2bt_df[col].dropna().index.intersection(jq_df[col].dropna().index)
                if len(common_index) > 1:
                    corr = jk2bt_df.loc[common_index, col].corr(jq_df.loc[common_index, col])
                    correlations[col] = corr

        if not correlations:
            return None

        # 转换为 DataFrame
        corr_df = pd.DataFrame.from_dict(correlations, orient='index', columns=['correlation'])
        corr_df = corr_df.sort_values('correlation', ascending=False)

        # 绘制
        fig, ax = plt.subplots(figsize=figsize)

        colors = ['red' if c < 0.99 else 'green' for c in corr_df['correlation']]
        ax.barh(range(len(corr_df)), corr_df['correlation'], color=colors, alpha=0.7)
        ax.set_yticks(range(len(corr_df)))
        ax.set_yticklabels(corr_df.index)
        ax.set_xlabel('Pearson 相关系数')
        ax.set_title('字段相关性')
        ax.axvline(x=0.99, color='black', linestyle='--', linewidth=1, label='阈值 (0.99)')
        ax.legend()
        ax.grid(True, alpha=0.3)

        plt.tight_layout()

        if save_path:
            plt.savefig(save_path, dpi=150, bbox_inches='tight')

        return fig

    def close(self):
        """关闭所有图表"""
        plt.close('all')