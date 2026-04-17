"""
engine/constants.py
统一常量管理模块 - 向后兼容层。

注意: 常量定义已移动到 api/constants.py。
此文件重新导出以保持向后兼容性。
新代码请直接使用 from jk2bt.api.constants import ...
"""

from jk2bt.api.constants import (
    SECURITY_INDEXES,
    CONS_ONLY_INDICES,
    INDEX_FALLBACK_MAP,
    INDEX_CODE_ALIAS_MAP,
    INDEX_DESCRIPTION,
    DATE_COLUMN_CANDIDATES,
    SUPPORTED_INDEXES,
)

__all__ = [
    "SECURITY_INDEXES",
    "CONS_ONLY_INDICES",
    "INDEX_FALLBACK_MAP",
    "INDEX_CODE_ALIAS_MAP",
    "INDEX_DESCRIPTION",
    "DATE_COLUMN_CANDIDATES",
    "SUPPORTED_INDEXES",
]
