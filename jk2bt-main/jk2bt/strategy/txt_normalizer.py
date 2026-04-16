"""
TXT策略文本标准化工具

DEPRECATED: 已合并到 txt_strategy_normalizer.py

此模块仅为向后兼容，请直接使用:
    from jk2bt.strategy.txt_strategy_normalizer import TxtStrategyNormalizer, normalize_strategy_file
"""

import warnings

warnings.warn(
    "jk2bt.strategy.txt_normalizer is deprecated, use jk2bt.strategy.txt_strategy_normalizer instead",
    DeprecationWarning,
    stacklevel=2,
)

from jk2bt.strategy.txt_strategy_normalizer import (
    TxtStrategyNormalizer,
    NormalizationResult,
    NormalizationIssue,
    IssueType,
    Severity,
    normalize_strategy_file,
    batch_normalize_strategies,
)


# 兼容别名：旧 API -> 新 API
class TxtNormalizer(TxtStrategyNormalizer):
    """兼容别名: 等同于 TxtStrategyNormalizer"""

    pass


def normalize_strategy_text(file_path, output_dir=None):
    """
    兼容别名: 等同于 normalize_strategy_file

    返回 (normalized_path, result) 元组以兼容旧版调用方式。
    """
    result = normalize_strategy_file(file_path, output_dir)
    return result.normalized_file, result


__all__ = [
    "TxtNormalizer",
    "NormalizationResult",
    "NormalizationIssue",
    "normalize_strategy_text",
    # 新 API 也导出
    "TxtStrategyNormalizer",
    "IssueType",
    "Severity",
    "normalize_strategy_file",
    "batch_normalize_strategies",
]
