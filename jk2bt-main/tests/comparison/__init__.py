"""
tests/comparison/__init__.py
数据比较框架

用于验证 jk2bt 本地数据与 JoinQuant 平台数据的一致性。
"""

from .config import (
    SAMPLE_STOCKS,
    SAMPLE_INDEXES,
    START_DATE,
    END_DATE,
    COMPARISON_CONFIG,
    OUTPUT_DIR,
)
from .comparator import DataComparator, DiffResult, DataType, quick_compare
from .statistics_analyzer import StatisticsAnalyzer, StatisticsResult, compare_distribution
from .visualizer import DataVisualizer
from .report_generator import ReportGenerator, generate_summary_csv
from .data_collector import DataCollector, generate_jq_data_template
from .run_comparison import ComparisonRunner, run_comparison_cli, quick_comparison

__all__ = [
    # 配置
    "SAMPLE_STOCKS",
    "SAMPLE_INDEXES",
    "START_DATE",
    "END_DATE",
    "COMPARISON_CONFIG",
    "OUTPUT_DIR",
    # 核心类
    "DataComparator",
    "DiffResult",
    "DataType",
    "StatisticsAnalyzer",
    "StatisticsResult",
    "DataVisualizer",
    "ReportGenerator",
    "DataCollector",
    "ComparisonRunner",
    # 便捷函数
    "quick_compare",
    "compare_distribution",
    "generate_summary_csv",
    "generate_jq_data_template",
    "run_comparison_cli",
    "quick_comparison",
]