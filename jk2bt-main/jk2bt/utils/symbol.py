"""
utils/symbol.py
股票代码格式转换工具（统一实现）。

支持的格式:
- 聚宽格式: '600519.XSHG', '000001.XSHE'
- AkShare格式: 'sh600519', 'sz000001'
- 纯数字: '600519', '000001'

主要函数:
- format_stock_symbol: 统一转为6位纯数字
- jq_code_to_ak: 聚宽格式 -> AkShare格式
- ak_code_to_jq: AkShare格式 -> 聚宽格式
- normalize_symbol: 标准化代码格式
"""

import re


def format_stock_symbol(symbol):
    """
    将各种格式的股票代码统一转为 6 位纯数字字符串。

    支持: sh600000, sz000001, 600000.XSHG, 000001.XSHE, 600000, 000001

    参数:
        symbol: 股票代码（各种格式）

    返回:
        str: 6位纯数字股票代码

    示例:
        format_stock_symbol('sh600000') -> '600000'
        format_stock_symbol('600519.XSHG') -> '600519'
        format_stock_symbol('000001') -> '000001'
    """
    if symbol is None:
        return None

    symbol = str(symbol)

    # 移除 sh/sz 前缀
    if symbol.startswith('sh') or symbol.startswith('sz'):
        symbol = symbol[2:]

    # 移除 .XSHG/.XSHE 后缀
    if symbol.endswith('.XSHG') or symbol.endswith('.XSHE'):
        symbol = symbol[:6]

    return symbol.zfill(6)


def jq_code_to_ak(code):
    """
    聚宽代码格式 -> 带前缀的 AkShare 格式。

    参数:
        code: 聚宽格式代码，如 '600519.XSHG'

    返回:
        str: AkShare格式代码，如 'sh600519'

    示例:
        jq_code_to_ak('600519.XSHG') -> 'sh600519'
        jq_code_to_ak('000001.XSHE') -> 'sz000001'
        jq_code_to_ak('sh600519') -> 'sh600519' (不变)
    """
    if code is None:
        return None

    code = str(code)

    if code.endswith('.XSHG'):
        return 'sh' + code[:6]
    elif code.endswith('.XSHE'):
        return 'sz' + code[:6]
    elif code.startswith('sh') or code.startswith('sz'):
        return code
    else:
        # 纯数字，按首位判断交易所
        c = code.zfill(6)
        if c.startswith('6'):
            return 'sh' + c
        else:
            return 'sz' + c


def ak_code_to_jq(code):
    """
    AkShare 格式 -> 聚宽格式。

    参数:
        code: AkShare格式代码，如 'sh600519'

    返回:
        str: 聚宽格式代码，如 '600519.XSHG'

    示例:
        ak_code_to_jq('sh600519') -> '600519.XSHG'
        ak_code_to_jq('sz000001') -> '000001.XSHE'
    """
    if code is None:
        return None

    code = str(code)

    if code.startswith('sh'):
        return code[2:] + '.XSHG'
    elif code.startswith('sz'):
        return code[2:] + '.XSHE'
    elif code.endswith('.XSHG') or code.endswith('.XSHE'):
        return code
    else:
        # 纯数字，按首位判断
        c = code.zfill(6)
        if c.startswith('6'):
            return c + '.XSHG'
        else:
            return c + '.XSHE'


def normalize_symbol(symbol):
    """
    统一股票代码格式为 6 位数字（兼容各种输入格式）。

    这是 format_stock_symbol 的别名，用于向后兼容。

    参数:
        symbol: 股票代码（各种格式）

    返回:
        str: 6位纯数字股票代码
    """
    return format_stock_symbol(symbol)


def get_symbol_prefix(symbol):
    """
    获取股票代码前缀（交易所标识）。

    参数:
        symbol: 股票代码

    返回:
        str: 'sh' 或 'sz'

    示例:
        get_symbol_prefix('600519.XSHG') -> 'sh'
        get_symbol_prefix('000001.XSHE') -> 'sz'
    """
    code = normalize_symbol(symbol)
    if code.startswith('6'):
        return 'sh'
    return 'sz'


def is_valid_stock_code(symbol):
    """
    验证是否为有效的股票代码格式。

    参数:
        symbol: 股票代码

    返回:
        bool: 是否有效
    """
    if symbol is None:
        return False

    symbol = str(symbol)

    # 匹配各种有效格式
    patterns = [
        r'^[shsz]?[0-9]{6}$',  # sh600000, sz000001, 600000
        r'^[0-9]{6}\.[XSHGXSHE]{4}$',  # 600000.XSHG, 000001.XSHE
    ]

    for pattern in patterns:
        if re.match(pattern, symbol):
            return True

    return False


# 兼容别名
format_stock_symbol_for_akshare = format_stock_symbol


__all__ = [
    'format_stock_symbol',
    'format_stock_symbol_for_akshare',  # 兼容别名
    'jq_code_to_ak',
    'ak_code_to_jq',
    'normalize_symbol',
    'get_symbol_prefix',
    'is_valid_stock_code',
]