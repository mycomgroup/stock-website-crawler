"""
平台适配器层

包含：
- joinquant_adapter: 聚宽平台适配器（封装 jqdata API）
- ricequant_adapter: 米筐平台适配器（封装 ricequant API）
- local_adapter:     本地数据适配器（Tushare/自建数据库）
"""

from .joinquant_adapter import JoinQuantAdapter, init_cal_from_jq
from .ricequant_adapter import RiceQuantAdapter, init_cal_from_rq
from .local_adapter import LocalGatewayAdapter, init_cal_from_local_gateway

__all__ = [
    "JoinQuantAdapter",
    "RiceQuantAdapter",
    "LocalGatewayAdapter",
    "init_cal_from_jq",
    "init_cal_from_rq",
    "init_cal_from_local_gateway",
]
