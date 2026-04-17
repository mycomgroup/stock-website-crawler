"""兼容入口 - 从 stats 模块重新导出。"""

from .stats import (
    get_ols,
    get_zscore,
    get_rank,
    get_factor_filter_list,
    get_num,
    get_beta,
)

__all__ = [
    "get_ols",
    "get_zscore",
    "get_rank",
    "get_factor_filter_list",
    "get_num",
    "get_beta",
]
