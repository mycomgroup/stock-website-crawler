"""
bond 模块 - 可转债专项JQData接口

提供聚宽风格的可转债数据查询接口：
1. bond.CONBOND_CONVERT_PRICE_ADJUST - 可转债转股价格调整
2. bond.CONBOND_DAILY_CONVERT - 可转债每日转股统计

使用示例：
>>> from jk2bt.api.bond import bond
>>> df = query(bond.CONBOND_CONVERT_PRICE_ADJUST).filter(bond.CONBOND_CONVERT_PRICE_ADJUST.code == '113009.XSHG')
>>> df = query(bond.CONBOND_DAILY_CONVERT).filter(bond.CONBOND_DAILY_CONVERT.date == '2024-01-01')
"""

import pandas as pd
import logging
from typing import Optional, Union

logger = logging.getLogger(__name__)


class CONBOND_CONVERT_PRICE_ADJUST:
    """
    可转债转股价格调整表 (CONBOND_CONVERT_PRICE_ADJUST)

    字段说明：
    - code: 可转债代码
    - name: 可转债名称
    - pub_date: 发布日期
    - adjust_date: 调整日期
    - new_convert_price: 新的转股价
    - adjust_reason: 调整原因
    """

    code = None
    name = None
    pub_date = None
    adjust_date = None
    new_convert_price = None
    adjust_reason = None


class CONBOND_DAILY_CONVERT:
    """
    可转债每日转股统计表 (CONBOND_DAILY_CONVERT)

    字段说明：
    - date: 日期
    - code: 可转债代码
    - name: 可转债名称
    - exchange_code: 交易所代码
    - issue_number: 发行量
    - convert_price: 转股价
    - daily_convert_number: 当日转股数量
    - acc_convert_number: 累计转股数量
    - acc_convert_ratio: 累计转股比例
    - convert_premium: 转股溢价
    - convert_premium_rate: 转股溢价率
    """

    date = None
    code = None
    name = None
    exchange_code = None
    issue_number = None
    convert_price = None
    daily_convert_number = None
    acc_convert_number = None
    acc_convert_ratio = None
    convert_premium = None
    convert_premium_rate = None


class BondQuery:
    """
    可转债查询模块 - 模拟聚宽 bond 模块

    提供 run_query 兼容接口，支持 query(bond.XXX).filter(...) 语法

    使用示例：
    >>> from jk2bt.api.bond import bond
    >>> df = bond.run_query(bond.CONBOND_CONVERT_PRICE_ADJUST.code == '113009.XSHG')
    >>> df = bond.run_query(bond.CONBOND_DAILY_CONVERT.date == '2024-01-01')
    """

    CONBOND_CONVERT_PRICE_ADJUST = CONBOND_CONVERT_PRICE_ADJUST
    CONBOND_DAILY_CONVERT = CONBOND_DAILY_CONVERT

    def run_query(
        self,
        query_obj,
        force_update: bool = False,
        use_duckdb: bool = True,
    ) -> pd.DataFrame:
        """
        执行可转债查询

        参数:
            query_obj: 查询对象（表对象或查询表达式）
            force_update: 强制更新
            use_duckdb: 是否使用DuckDB缓存

        返回:
            pd.DataFrame
        """
        table_name = None
        conditions = {}

        if hasattr(query_obj, "__name__"):
            table_name = query_obj.__name__
        elif hasattr(query_obj, "__class__"):
            table_name = query_obj.__class__.__name__

        if hasattr(query_obj, "left") and hasattr(query_obj, "right"):
            if hasattr(query_obj.left, "__name__"):
                table_name = query_obj.left.__name__
            elif hasattr(query_obj.left, "__class__"):
                table_name = query_obj.left.__class__.__name__
            if hasattr(query_obj, "right"):
                conditions["value"] = query_obj.right

        if hasattr(query_obj, "left") and hasattr(query_obj.left, "name"):
            conditions["field"] = query_obj.left.name

        if table_name == "CONBOND_CONVERT_PRICE_ADJUST":
            return self._query_convert_price_adjust(
                conditions, force_update, use_duckdb
            )
        elif table_name == "CONBOND_DAILY_CONVERT":
            return self._query_daily_convert(conditions, force_update, use_duckdb)
        else:
            logger.warning(f"[BondQuery] 不支持的表: {table_name}")
            return pd.DataFrame()

    def _query_convert_price_adjust(
        self,
        conditions: dict,
        force_update: bool = False,
        use_duckdb: bool = True,
    ) -> pd.DataFrame:
        """
        查询可转债转股价格调整数据

        TODO: akshare 目前没有直接提供可转债转股价格调整的接口
        如需实现，可考虑以下数据源：
        - 聚宽自有数据
        - 东方财富可转债详情页
        - 交易所公告数据
        """
        logger.debug(
            "[BondQuery] CONBOND_CONVERT_PRICE_ADJUST: "
            "akshare 暂无此接口，返回空DataFrame"
        )
        return pd.DataFrame(
            columns=[
                "code",
                "name",
                "pub_date",
                "adjust_date",
                "new_convert_price",
                "adjust_reason",
            ]
        )

    def _query_daily_convert(
        self,
        conditions: dict,
        force_update: bool = False,
        use_duckdb: bool = True,
    ) -> pd.DataFrame:
        """
        查询可转债每日转股统计数据

        TODO: akshare 目前没有直接提供可转债每日转股统计的接口
        如需实现，可考虑以下数据源：
        - 聚宽自有数据
        - 东方财富可转债转股详情页
        - 交易所每日转股数据
        """
        logger.debug(
            "[BondQuery] CONBOND_DAILY_CONVERT: akshare 暂无此接口，返回空DataFrame"
        )
        return pd.DataFrame(
            columns=[
                "date",
                "code",
                "name",
                "exchange_code",
                "issue_number",
                "convert_price",
                "daily_convert_number",
                "acc_convert_number",
                "acc_convert_ratio",
                "convert_premium",
                "convert_premium_rate",
            ]
        )


bond = BondQuery()


def query_convert_price_adjust(
    code: Optional[str] = None,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
) -> pd.DataFrame:
    """
    直接查询可转债转股价格调整数据

    参数:
        code: 可转债代码（可选）
        start_date: 开始日期（可选）
        end_date: 结束日期（可选）

    返回:
        pd.DataFrame
    """
    return bond.run_query(CONBOND_CONVERT_PRICE_ADJUST())


def query_daily_convert(
    date: Optional[str] = None,
    code: Optional[str] = None,
) -> pd.DataFrame:
    """
    直接查询可转债每日转股统计数据

    参数:
        date: 日期（可选）
        code: 可转债代码（可选）

    返回:
        pd.DataFrame
    """
    return bond.run_query(CONBOND_DAILY_CONVERT())


__all__ = [
    "CONBOND_CONVERT_PRICE_ADJUST",
    "CONBOND_DAILY_CONVERT",
    "BondQuery",
    "bond",
    "query_convert_price_adjust",
    "query_daily_convert",
]
