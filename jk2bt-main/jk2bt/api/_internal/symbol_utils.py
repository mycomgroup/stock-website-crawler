"""
共享私有工具函数：股票代码处理与价格计算

此模块供 src/api 内部使用，不对外暴露。
"""

from __future__ import annotations


def normalize_symbol(symbol: str) -> str:
    """
    统一股票代码格式为 6 位数字

    支持: sh600000, sz000001, 600000.XSHG, 000001.XSHE, 600000
    """
    if symbol.startswith("sh") or symbol.startswith("sz"):
        return symbol[2:].zfill(6)
    if symbol.endswith(".XSHG") or symbol.endswith(".XSHE"):
        return symbol[:6].zfill(6)
    return symbol.zfill(6)


def get_symbol_prefix(symbol: str) -> str:
    """
    获取股票代码前缀

    返回: 'sh' 或 'sz'
    """
    code = normalize_symbol(symbol)
    if code.startswith("6"):
        return "sh"
    return "sz"


def is_gem_or_star(code: str) -> bool:
    """
    判断是否为创业板或科创板

    创业板: 300xxx
    科创板: 688xxx
    """
    c = normalize_symbol(code)
    return c.startswith("300") or c.startswith("688")


def calculate_limit_price(prev_close: float, code: str, direction: str = "up") -> float | None:
    """
    计算涨跌停价

    参数:
        prev_close: 前收盘价
        code: 股票代码
        direction: 'up'=涨停, 'down'=跌停

    返回:
        涨跌停价，若 prev_close 无效则返回 None
    """
    if prev_close is None or prev_close <= 0:
        return None

    c = normalize_symbol(code)

    # 默认涨跌幅限制 10%
    limit_ratio = 0.10
    if is_gem_or_star(c):
        # 创业板/科创板 20%
        limit_ratio = 0.20
    elif _is_st(c):
        # ST 股票 5%
        limit_ratio = 0.05

    if direction == "up":
        return round(prev_close * (1 + limit_ratio), 2)
    else:
        return round(prev_close * (1 - limit_ratio), 2)


def _is_st(code: str) -> bool:
    """
    判断是否为 ST 股票（简化版，仅按代码判断）

    完整判断需要查询 ST 列表
    """
    # 简化实现：代码本身无法判断 ST，需外部数据
    return False
