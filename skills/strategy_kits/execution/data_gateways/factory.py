from typing import Literal

from .base import BaseDataGateway
from .jq_gateway import JQDataGateway
from .qlib_gateway import QlibDataGateway
from .tushare_gateway import TuShareDataGateway


def create_gateway(kind: Literal["jq", "tushare", "qlib"], **kwargs) -> BaseDataGateway:
    """工厂函数：按 kind 创建对应的数据网关适配器。"""
    if kind == "jq":
        return JQDataGateway(**kwargs)
    elif kind == "tushare":
        return TuShareDataGateway(**kwargs)
    elif kind == "qlib":
        return QlibDataGateway(**kwargs)
    else:
        raise ValueError(f"Unknown gateway kind: {kind}")
