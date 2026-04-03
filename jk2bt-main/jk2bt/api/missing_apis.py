# src/api/missing_apis.py（兼容层，保留 6 个月后删除）
# 财务类 API 已迁移到 src/api/finance.py
# get_beta 已迁移到 src/api/stats.py
# 此文件仅保留向后兼容
import warnings
warnings.warn(
    "missing_apis 已拆分为 finance 和 stats，请更新导入："
    " from jk2bt.api.finance import ... 或 from jk2bt.api.stats import ...",
    DeprecationWarning,
    stacklevel=2,
)
from jk2bt.api.finance import *  # noqa: F401, F403
from jk2bt.api.stats import get_beta  # noqa: F401

from jk2bt.api.finance import __all__ as _finance_all

__all__ = list(_finance_all) + ["get_beta"]
