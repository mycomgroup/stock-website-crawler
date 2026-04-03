"""
jk2bt/api/securities.py
证券元数据与代码标准化 API

提供 JQData 兼容的证券元数据查询接口和代码格式标准化工具。
"""

import logging
from typing import Optional, Union

logger = logging.getLogger(__name__)


def get_all_securities(types=None, date=None):
    """获取全市场证券列表。

    包装 ``jk2bt.core.api_wrappers.get_all_securities_jq``，返回 JQData 风格的
    证券元数据 DataFrame。

    Args:
        types: 证券类型列表，默认 ``["stock"]``。可选值如 ``"stock"``、``"index"`` 等。
        date: 指定日期（暂未使用，保留以兼容 JQData 签名）。

    Returns:
        pandas.DataFrame: 以 JQ_Code 为索引，包含以下列：
            - ``display_name``：证券中文名称
            - ``name``：证券简称
            - ``start_date``：上市日期
            - ``end_date``：退市日期（在市则为 NaT/None）
            - ``type``：证券类型

    Examples:
        >>> df = get_all_securities()
        >>> df.columns.tolist()  # 包含 display_name, name, start_date, end_date, type
        >>> df = get_all_securities(types=["stock"], date="2023-01-01")
    """
    from jk2bt.core.api_wrappers import get_all_securities_jq as _get_all_securities_jq

    return _get_all_securities_jq(types=types, date=date)


def get_security_info(code, date=None):
    """获取单只证券的基本信息。

    包装 ``jk2bt.core.api_wrappers.get_security_info_jq``，返回 SecurityInfo 对象。
    若传入无效代码，将返回 None 或抛出明确异常，不会静默失败。

    Args:
        code (str): 证券代码，支持 JQ_Code 格式（如 ``"000001.XSHE"``）或
            纯 6 位数字格式（如 ``"000001"``）。
        date: 指定日期（暂未使用，保留以兼容 JQData 签名）。

    Returns:
        SecurityInfo | None: 证券信息对象，支持属性访问：
            - ``.display_name``：证券中文名称
            - ``.name``：证券简称
            - ``.start_date``：上市日期
            - ``.end_date``：退市日期
            - ``.type``：证券类型
            若代码无效则返回 None。

    Raises:
        ValueError: 当 ``code`` 为空字符串或 None 时。

    Examples:
        >>> info = get_security_info("000001.XSHE")
        >>> info.display_name
        '平安银行'
        >>> info = get_security_info("600519.XSHG")
        >>> info.start_date
    """
    if not code:
        raise ValueError("code 参数不能为空")

    from jk2bt.core.api_wrappers import get_security_info_jq as _get_security_info_jq

    return _get_security_info_jq(code=code)


# JQData 向后兼容别名
get_all_securities_jq = get_all_securities
get_security_info_jq = get_security_info
