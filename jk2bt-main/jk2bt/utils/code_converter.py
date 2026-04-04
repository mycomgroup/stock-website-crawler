"""
utils/code_converter.py
股票代码格式统一转换工具。

支持三种格式：
1. akshare格式: sh600519, sz000858 (带sh/sz前缀)
2. 聚宽格式: 600519.XSHG, 000858.XSHE (带交易所后缀)
3. 纯数字: 600519, 000858

统一标准：内部存储和查询统一使用聚宽格式
"""

import logging

logger = logging.getLogger(__name__)


def normalize_to_jq_format(symbol: str) -> str:
    """
    将各种股票代码格式统一转换为聚宽格式（内部标准格式）。

    支持:
    - akshare格式: sh600519, sz000001
    - 聚宽格式: 600519.XSHG, 000001.XSHE
    - 纯数字: 600519, 000001

    返回:
    - 聚宽格式: 600519.XSHG, 000001.XSHE

    规则:
    - 6开头 -> 上交所(.XSHG)
    - 0/3开头 -> 深交所(.XSHE)
    """
    if symbol is None:
        return None

    symbol = str(symbol).strip()

    # 已经是聚宽格式，直接返回
    if symbol.endswith('.XSHG') or symbol.endswith('.XSHE'):
        # 确保代码部分是6位数字
        code = symbol.split('.')[0]
        return code.zfill(6) + '.' + symbol.split('.')[1]

    # akshare格式 sh/sz 前缀
    if symbol.lower().startswith('sh'):
        code = symbol[2:].zfill(6)
        return f"{code}.XSHG"
    if symbol.lower().startswith('sz'):
        code = symbol[2:].zfill(6)
        return f"{code}.XSHE"

    # 纯数字，按首位判断交易所
    code_num = symbol.zfill(6)

    # 根据代码首位判断交易所
    if code_num.startswith('6'):
        return f"{code_num}.XSHG"
    elif code_num.startswith('0') or code_num.startswith('3'):
        return f"{code_num}.XSHE"
    else:
        # 默认按深交所处理（如创业板30开头等）
        return f"{code_num}.XSHE"


def normalize_to_akshare_format(symbol: str) -> str:
    """
    将各种股票代码格式统一转换为akshare格式。

    支持:
    - akshare格式: sh600519, sz000001
    - 聚宽格式: 600519.XSHG, 000001.XSHE
    - 纯数字: 600519, 000001

    返回:
    - akshare格式: sh600519, sz000001
    """
    if symbol is None:
        return None

    symbol = str(symbol).strip()

    # 已经是akshare格式
    if symbol.lower().startswith('sh') or symbol.lower().startswith('sz'):
        code = symbol[2:].zfill(6)
        return symbol.lower()[:2] + code

    # 聚宽格式
    if symbol.endswith('.XSHG'):
        code = symbol.replace('.XSHG', '').zfill(6)
        return f"sh{code}"
    if symbol.endswith('.XSHE'):
        code = symbol.replace('.XSHE', '').zfill(6)
        return f"sz{code}"

    # 纯数字，按首位判断交易所
    code_num = symbol.zfill(6)
    if code_num.startswith('6'):
        return f"sh{code_num}"
    else:
        return f"sz{code_num}"


def get_exchange_from_code(symbol: str) -> str:
    """
    从股票代码判断交易所。

    返回:
    - 'XSHG': 上交所
    - 'XSHE': 深交所
    """
    jq_symbol = normalize_to_jq_format(symbol)
    if jq_symbol.endswith('.XSHG'):
        return 'XSHG'
    return 'XSHE'


def is_valid_stock_code(symbol: str) -> bool:
    """
    检查股票代码是否有效。

    有效格式:
    - akshare: sh600519, sz000858
    - 聚宽: 600519.XSHG, 000858.XSHE
    - 纯数字: 600519, 000858
    """
    if symbol is None:
        return False

    symbol = str(symbol).strip()

    # 检查长度合理性
    if len(symbol) < 6:
        return False

    # akshare格式检查
    if symbol.lower().startswith('sh') or symbol.lower().startswith('sz'):
        code = symbol[2:]
        if len(code) == 6 and code.isdigit():
            return True
        return False

    # 聚宽格式检查
    if '.XSHG' in symbol or '.XSHE' in symbol:
        parts = symbol.split('.')
        if len(parts) == 2 and len(parts[0]) == 6 and parts[0].isdigit():
            return True
        return False

    # 纯数字检查
    if symbol.isdigit() and len(symbol) <= 6:
        return True

    return False