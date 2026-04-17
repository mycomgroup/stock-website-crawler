"""兼容入口 - 从 factor 模块重新导出。"""

from .factor import get_north_factor, get_comb_factor, get_factor_momentum

__all__ = ["get_north_factor", "get_comb_factor", "get_factor_momentum"]
