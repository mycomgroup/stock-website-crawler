"""
Factor Preprocessing and Scoring Shell

提供多因子预处理与打分的一站式解决方案。

快速开始:
    >>> from strategy_kits.signals.factor_preprocess import (
    ...     FactorPreprocessPipeline,
    ...     PreprocessConfig,
    ...     ScoreConfig
    ... )
    >>> config = PreprocessConfig()
    >>> score_config = ScoreConfig(method="equal")
    >>> pipeline = FactorPreprocessPipeline(
    ...     factor_cols=["roe", "pe", "pb"],
    ...     preprocess_config=config,
    ...     score_config=score_config
    ... )
    >>> score_df = pipeline.fit_transform(raw_df)

分步使用:
    >>> from strategy_kits.signals.factor_preprocess import (
    ...     fill_missing_by_group,
    ...     winsorize_features,
    ...     standardize_features,
    ...     build_score_frame
    ... )
    >>> df = fill_missing_by_group(raw_df, ["roe", "pe"], group_col="industry")
    >>> df = winsorize_features(df, ["roe", "pe"])
    >>> df = standardize_features(df, ["roe", "pe"])
    >>> score_df = build_score_frame(df, ["roe", "pe"], method="equal")
"""

from .config import PreprocessConfig, ScoreConfig
from .cleaners import fill_missing_by_group
from .transformers import winsorize_features, standardize_features
from .scoring import build_score_frame, register_scoring_method
from .pipeline import FactorPreprocessPipeline
from .stateful_preprocessor import (
    FeaturePreprocessor,
    PreprocessConfig as MLPreprocessConfig,
)

try:
    from .qlib_processors import SafeRobustZScoreNorm, SafeFillna, SafeCSRankNorm
except Exception:  # optional dependency: qlib
    SafeRobustZScoreNorm = None
    SafeFillna = None
    SafeCSRankNorm = None

__all__ = [
    # Config
    "PreprocessConfig",
    "ScoreConfig",
    # Functions
    "fill_missing_by_group",
    "winsorize_features",
    "standardize_features",
    "build_score_frame",
    # Decorators
    "register_scoring_method",
    # Pipeline
    "FactorPreprocessPipeline",
    # Stateful ML preprocessor
    "FeaturePreprocessor",
    "MLPreprocessConfig",
    # Qlib wrappers (optional)
    "SafeRobustZScoreNorm",
    "SafeFillna",
    "SafeCSRankNorm",
]
