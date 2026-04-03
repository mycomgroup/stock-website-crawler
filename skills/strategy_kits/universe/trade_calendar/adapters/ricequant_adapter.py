"""
米筐（RiceQuant）平台适配器

注入逻辑：
1. 交易日历：all_instruments(type="CS") 或 get_trading_dates 获取
2. 基础池：封装 get_all_securities / get_index_stocks（若存在）
"""

from typing import List, Optional
import pandas as pd

from ..trade_calendar import set_trade_cal_source
from ..universe_selector import BaseUniverseAdapter, set_default_adapter


class RiceQuantAdapter(BaseUniverseAdapter):
    """米筐平台适配器。"""

    def __init__(self, rq_module=None):
        if rq_module is None:
            try:
                import rqalpha

                rq_module = rqalpha
            except ImportError:
                try:
                    import rqalpha_plus

                    rq_module = rqalpha_plus
                except ImportError:
                    raise ImportError(
                        "未找到 rqalpha/rqalpha_plus 模块，请确保在米筐回测环境中运行"
                    )
        self.rq = rq_module

    def get_all_securities(
        self, types: Optional[List[str]] = None, date: Optional[str] = None
    ) -> List[str]:
        """
        米筐中 get_all_securities 等价于 get_all_securities(types=['stock'])
        返回 DataFrame，index 为 order_book_id
        """
        types = types or ["stock"]
        df = self.rq.get_all_securities(types)
        return df.index.tolist()

    def get_index_stocks(self, index_code: str, date: Optional[str] = None) -> List[str]:
        """
        米筐中获取指数成分股通常通过 index_components(index_code, date)
        或 all_instruments(type='IND')
        """
        try:
            # 不同版本 API 名称可能不同
            if hasattr(self.rq, "index_components"):
                return self.rq.index_components(index_code, date=date)
        except Exception:
            pass
        raise NotImplementedError(
            f"米筐环境下 get_index_stocks({index_code}) 需要额外适配"
        )

    def get_industry_stocks(
        self, industry_code: str, level: str = "sw_l1", date: Optional[str] = None
    ) -> List[str]:
        # 米筐行业数据获取方式因版本而异，此处留骨架
        raise NotImplementedError(
            "米筐 industry stocks 获取需要按具体环境补充实现"
        )


def init_cal_from_rq(
    start: str = "2010-01-01",
    end: Optional[str] = None,
    rq_module=None,
    set_as_default_adapter: bool = True,
):
    """
    从米筐拉取交易日历并注入，同时注册默认适配器。

    Example:
        >>> from strategy_kits.universe.trade_calendar.adapters import init_cal_from_rq
        >>> init_cal_from_rq()
    """
    adapter = RiceQuantAdapter(rq_module=rq_module)
    if end is None:
        end = pd.Timestamp.today().strftime("%Y-%m-%d")
    try:
        trade_days = adapter.rq.get_trading_dates(start, end)
    except AttributeError:
        # fallback：从所有股票上市日期推断（不精确，仅兜底）
        trade_days = pd.date_range(start, end, freq="B")
    set_trade_cal_source(trade_days)
    if set_as_default_adapter:
        set_default_adapter(adapter)
    return adapter
