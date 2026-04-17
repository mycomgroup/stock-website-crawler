"""
securities_utils.py
证券代码工具函数、指数常量定义、格式化函数。

提供聚宽风格的证券代码转换和验证功能。
"""

import os
import re
import warnings
import pandas as pd
from datetime import datetime

from jk2bt.utils.symbol import (
    normalize_symbol,
    format_stock_symbol as format_stock_symbol_for_akshare,
    jq_code_to_ak,
    ak_code_to_jq,
)
from jk2bt.utils.result import RobustResult
from jk2bt.core.constants import (
    DATE_COLUMN_CANDIDATES,
    SECURITY_INDEXES,
    CONS_ONLY_INDICES,
    INDEX_FALLBACK_MAP,
    INDEX_DESCRIPTION,
    INDEX_CODE_ALIAS_MAP,
)

SUPPORTED_INDEXES = SECURITY_INDEXES

_DATE_COLUMN_CANDIDATES = DATE_COLUMN_CANDIDATES

# 项目根目录和缓存目录
_PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
_CACHE_BASE_DIR = os.path.join(_PROJECT_ROOT, "cache")


def _find_date_column(df: pd.DataFrame, category: str = "market") -> str:
    """动态检测 DataFrame 中的日期列名。

    Parameters
    ----------
    df : pd.DataFrame
    category : str, 'market' 或 'financial'

    Returns
    -------
    str : 日期列名，若找不到则返回 None
    """
    candidates = DATE_COLUMN_CANDIDATES.get(category, DATE_COLUMN_CANDIDATES["market"])
    for col in candidates:
        if col in df.columns:
            return col
    return None


def _resolve_cache_dir(cache_dir: str) -> str:
    """解析缓存目录路径，支持相对路径和绝对路径"""
    if os.path.isabs(cache_dir):
        return cache_dir
    return os.path.join(_CACHE_BASE_DIR, cache_dir)


# =====================================================================
# 股票代码工具函数（从 utils.symbol 导入）
# =====================================================================


def _stock_code_to_jq(code):
    """将股票代码转换为聚宽格式"""
    code = str(code).strip()
    if code.startswith("6"):
        return code + ".XSHG"
    else:
        return code + ".XSHE"


# =====================================================================
# 指数相关常量（从 constants.py 导入）
# =====================================================================


def _format_index_code(index_code):
    """格式化指数代码为6位数字，支持多种格式别名"""
    code = str(index_code).lower().strip()
    if code in INDEX_CODE_ALIAS_MAP:
        code = INDEX_CODE_ALIAS_MAP[code]
    code = code.replace(".xshg", "").replace(".xshe", "")
    code = code.replace("sh", "").replace("sz", "")
    code = code.zfill(6)
    if code.startswith("399") and len(code) == 6:
        return code
    return code


def _normalize_index_weights(df):
    """标准化指数权重DataFrame"""
    result = pd.DataFrame()

    col_mapping = {
        "成分券代码": ["成分券代码", "证券代码", "股票代码", "code"],
        "权重": ["权重", "weight", "W", "w"],
        "证券名称": ["证券名称", "股票名称", "name", "display_name"],
        "行业代码": ["行业代码", "industry_code", "CITICS行业代码"],
    }

    for target_col, source_cols in col_mapping.items():
        for src_col in source_cols:
            if src_col in df.columns:
                result[target_col] = df[src_col]
                break

    if "成分券代码" in result.columns:
        result["code"] = result["成分券代码"].apply(lambda x: _stock_code_to_jq(x))
        result = result.set_index("code")

    if "权重" in result.columns:
        result["weight"] = result["权重"].astype(float)
    elif "W" in result.columns:
        result["weight"] = result["W"].astype(float)

    return result
