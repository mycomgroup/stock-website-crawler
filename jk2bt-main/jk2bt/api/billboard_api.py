"""兼容入口 - 从 billboard 模块重新导出。"""

from .billboard import (
    get_billboard_list,
    get_billboard_hot_stocks,
    get_institutional_holdings,
    get_broker_statistics,
)

__all__ = [
    "get_billboard_list",
    "get_billboard_hot_stocks",
    "get_institutional_holdings",
    "get_broker_statistics",
]
