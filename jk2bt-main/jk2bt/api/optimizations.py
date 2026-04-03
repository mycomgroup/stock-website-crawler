# src/api/optimizations.py（兼容层，保留 6 个月后删除）
# 已迁移到 src/api/cache.py，此文件仅保留向后兼容
import warnings
warnings.warn(
    "optimizations 已重命名为 cache，请更新导入：from jk2bt.api.cache import ...",
    DeprecationWarning,
    stacklevel=2,
)
from jk2bt.api.cache import *  # noqa: F401, F403
from jk2bt.api.cache import __all__  # noqa: F401
