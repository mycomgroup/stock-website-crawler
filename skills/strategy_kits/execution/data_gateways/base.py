from abc import ABC, abstractmethod
from typing import List, Optional, Union

import pandas as pd


class BaseDataGateway(ABC):
    """数据网关统一接口。策略代码只应依赖此抽象类。"""

    @abstractmethod
    def get_price(
        self,
        symbols: Union[str, List[str]],
        start_date: str,
        end_date: str,
        frequency: str = "daily",
        fields: Optional[List[str]] = None,
        adjust: str = "qfq",
        count: Optional[int] = None,
    ) -> Union[pd.DataFrame, dict[str, pd.DataFrame]]:
        """获取行情数据。多标时返回 dict[symbol] -> DataFrame。"""
        ...

    @abstractmethod
    def get_fundamentals(
        self,
        query_obj: dict,
        date: Optional[str] = None,
        stat_date: Optional[str] = None,
    ) -> pd.DataFrame:
        """单期财务数据查询。"""
        ...

    @abstractmethod
    def get_history_fundamentals(
        self,
        security: Union[str, List[str]],
        fields: List[str],
        watch_date: Optional[str] = None,
        stat_date: Optional[str] = None,
        count: int = 1,
        interval: str = "1q",
    ) -> pd.DataFrame:
        """多标的多期财报数据。fields 支持 'balance.xxx' / 'income.xxx' / 'cash_flow.xxx' 前缀。"""
        ...

    @abstractmethod
    def get_all_securities(
        self, types: Optional[List[str]] = None, date: Optional[str] = None
    ) -> pd.DataFrame:
        """全市场基础信息。"""
        ...

    @abstractmethod
    def get_security_info(self, code: str) -> Optional[dict]:
        """单只标的基础信息。"""
        ...

    @abstractmethod
    def get_index_members(
        self, index_code: str, date: Optional[str] = None
    ) -> List[str]:
        """指数成分股列表，返回统一 code 格式（如 JQ 风格 000001.XSHE）。"""
        ...

    @abstractmethod
    def get_trade_days(
        self, start_date: Optional[str] = None, end_date: Optional[str] = None
    ) -> List[pd.Timestamp]:
        """交易日序列。"""
        ...

    @abstractmethod
    def get_extras(
        self,
        field: str,
        securities: Union[str, List[str]],
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
    ) -> pd.DataFrame:
        """ST、停牌等附加信息。"""
        ...

    @abstractmethod
    def get_bars(
        self,
        security: str,
        count: int,
        unit: str = "1d",
        fields: Optional[List[str]] = None,
        end_dt: Optional[str] = None,
    ) -> pd.DataFrame:
        """按 count 获取历史 K 线。"""
        ...
