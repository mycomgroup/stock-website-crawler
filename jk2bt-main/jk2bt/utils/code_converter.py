"""
utils/code_converter.py
DEPRECATED: 已合并到 utils/symbol.py

此模块仅为向后兼容，请直接使用:
    from jk2bt.utils.symbol import normalize_symbol, jq_code_to_ak, ak_code_to_jq
"""

import warnings

warnings.warn(
    "jk2bt.utils.code_converter is deprecated, use jk2bt.utils.symbol instead",
    DeprecationWarning,
    stacklevel=2,
)

from jk2bt.utils.symbol import (
    format_stock_symbol,
    jq_code_to_ak,
    ak_code_to_jq,
    normalize_symbol,
    get_symbol_prefix,
    is_valid_stock_code,
)


def normalize_to_jq_format(symbol: str) -> str:
    """兼容别名: 等同于 ak_code_to_jq"""
    return ak_code_to_jq(symbol)


def normalize_to_akshare_format(symbol: str) -> str:
    """兼容别名: 等同于 jq_code_to_ak"""
    return jq_code_to_ak(symbol)


def get_exchange_from_code(symbol: str) -> str:
    """兼容别名: 等同于 get_symbol_prefix (返回大写)"""
    prefix = get_symbol_prefix(symbol)
    return "XSHG" if prefix == "sh" else "XSHE"


__all__ = [
    "normalize_to_jq_format",
    "normalize_to_akshare_format",
    "get_exchange_from_code",
    "format_stock_symbol",
    "jq_code_to_ak",
    "ak_code_to_jq",
    "normalize_symbol",
    "get_symbol_prefix",
    "is_valid_stock_code",
]
