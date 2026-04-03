"""
jk2bt.validation - 数据验证模块

验证本地数据与 JoinQuant 平台数据的一致性。

模块:
- data_collector: 数据采集器（本地 + JQ）
- comparison_engine: 对比引擎
- validator: 验证执行器
- report_generator: 报告生成器
- config: 配置管理
"""

from .config import ValidationConfig
from .data_collector import LocalDataSource, JQNotebookSource, DataCollector
from .comparison_engine import ComparisonEngine, ComparisonResult
from .validator import DataValidator, ValidationReport
from .report_generator import ReportGenerator

__all__ = [
    # Config
    "ValidationConfig",
    # Data Collector
    "LocalDataSource",
    "JQNotebookSource",
    "DataCollector",
    # Comparison
    "ComparisonEngine",
    "ComparisonResult",
    # Validator
    "DataValidator",
    "ValidationReport",
    # Report
    "ReportGenerator",
]