"""
jk2bt/api/securities.py
证券元数据与代码标准化 API

提供 JQData 兼容的证券元数据查询接口和代码格式标准化工具。
"""

from jk2bt.api.jq_compat import (
    get_all_securities_jq as _get_all_securities_jq,
    get_security_info_jq as _get_security_info_jq,
)
from jk2bt.utils.symbol import ak_code_to_jq, format_stock_symbol


def normalize_code(code: str) -> str:
    """
    将股票代码转换为聚宽标准格式。

    参数
    ----
    code : str
        任意格式的代码，如 '600519', 'sh600519', '600519.sh' 等

    返回
    ----
    str
        聚宽格式代码，如 '600519.XSHG'

    示例
    ----
    >>> normalize_code('600519')
    '600519.XSHG'
    >>> normalize_code('sh600519')
    '600519.XSHG'
    """
    code = str(code).strip()
    return ak_code_to_jq(code)


def get_all_securities(types=None, date=None):
    """获取全市场证券列表。

    Args:
        types: 证券类型列表，默认 ``["stock"]``。可选值如 ``"stock"``、``"index"`` 等。
        date: 指定日期（暂未使用，保留以兼容 JQData 签名）。

    Returns:
        pandas.DataFrame: 以 JQ_Code 为索引的证券元数据 DataFrame。
    """
    return _get_all_securities_jq(types=types, date=date)


def get_security_info(code, date=None):
    """获取单只证券的基本信息。

    Args:
        code (str): 证券代码，支持 JQ_Code 格式（如 ``"000001.XSHE"``）或
            纯 6 位数字格式（如 ``"000001"``）。
        date: 指定日期（暂未使用，保留以兼容 JQData 签名）。

    Returns:
        SecurityInfo | None: 证券信息对象。若代码无效则返回 None。

    Raises:
        ValueError: 当 ``code`` 为空字符串或 None 时。
    """
    if not code:
        raise ValueError("code 参数不能为空")
    return _get_security_info_jq(code=code)


# JQData 向后兼容别名
get_all_securities_jq = get_all_securities
get_security_info_jq = get_security_info
