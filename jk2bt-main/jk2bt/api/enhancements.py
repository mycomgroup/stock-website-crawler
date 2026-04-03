# src/api/enhancements.py（兼容层，保留 6 个月后删除）
# 订单函数已迁移到 src/api/order.py
# 过滤函数已迁移到 src/api/filter.py
# 此文件仅保留向后兼容
import warnings
warnings.warn(
    "enhancements 已拆分为 order 和 filter，请更新导入："
    " from jk2bt.api.order import ... 或 from jk2bt.api.filter import ...",
    DeprecationWarning,
    stacklevel=2,
)
from jk2bt.api.order import *  # noqa: F401, F403
from jk2bt.api.filter import *  # noqa: F401, F403

from jk2bt.api.order import __all__ as _order_all
from jk2bt.api.filter import __all__ as _filter_all

__all__ = list(_order_all) + [s for s in _filter_all if s not in _order_all]
