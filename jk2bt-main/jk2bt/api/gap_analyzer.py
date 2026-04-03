"""
src/api/gap_analyzer.py — 兼容层（已迁移至 tools/gap_analyzer.py）

此文件仅作向后兼容保留，请使用新路径：
    from tools.gap_analyzer import APIGapAnalyzer, APIUsageInfo, analyze_api_gaps
"""

import warnings

warnings.warn(
    "src.api.gap_analyzer 已迁移至 tools.gap_analyzer，"
    "请更新导入路径：from tools.gap_analyzer import ...",
    DeprecationWarning,
    stacklevel=2,
)

from tools.gap_analyzer import (  # noqa: E402, F401
    APIUsageInfo,
    APIGapAnalyzer,
    analyze_api_gaps,
)

__all__ = ["APIUsageInfo", "APIGapAnalyzer", "analyze_api_gaps"]
