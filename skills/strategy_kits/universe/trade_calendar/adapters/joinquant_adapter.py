"""
聚宽（JoinQuant）平台适配器

注入逻辑：
1. 交易日历：jqdata.get_trade_days(start, end) 拉取全量日历注入
2. 基础池：封装 get_all_securities / get_index_stocks
"""

from typing import List, Optional
import pandas as pd

from ..trade_calendar import set_trade_cal_source
from ..universe_selector import BaseUniverseAdapter, set_default_adapter


class JoinQuantAdapter(BaseUniverseAdapter):
    """聚宽平台适配器。"""

    def __init__(self, jq_module=None):
        """
        Args:
            jq_module: jqdata 模块。若回测环境已自动注入，可传 None 或 globals() 中的变量。
        """
        if jq_module is None:
            try:
                import jqdata

                jq_module = jqdata
            except ImportError:
                raise ImportError("未找到 jqdata 模块，请确保在聚宽回测环境中运行")
        self.jq = jq_module

    def get_all_securities(
        self, types: Optional[List[str]] = None, date: Optional[str] = None
    ) -> List[str]:
        types = types or ["stock"]
        df = self.jq.get_all_securities(types, date=date)
        return df.index.tolist()

    def get_index_stocks(self, index_code: str, date: Optional[str] = None) -> List[str]:
        return self.jq.get_index_stocks(index_code, date=date)

    def get_industry_stocks(
        self, industry_code: str, level: str = "sw_l1", date: Optional[str] = None
    ) -> List[str]:
        # 聚宽 get_industry_stocks 接收的是 industry_code
        return self.jq.get_industry_stocks(industry_code, date=date)


def init_cal_from_jq(
    start: str = "2010-01-01",
    end: Optional[str] = None,
    jq_module=None,
    set_as_default_adapter: bool = True,
):
    """
    从聚宽拉取交易日历并注入，同时注册默认适配器。

    Example:
        >>> from strategy_kits.universe.trade_calendar.adapters import init_cal_from_jq
        >>> init_cal_from_jq()
    """
    adapter = JoinQuantAdapter(jq_module=jq_module)
    if end is None:
        end = pd.Timestamp.today().strftime("%Y-%m-%d")
    trade_days = adapter.jq.get_trade_days(start, end)
    set_trade_cal_source(trade_days)
    if set_as_default_adapter:
        set_default_adapter(adapter)
    return adapter
