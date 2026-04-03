"""Qlib 数据网关适配器。"""

import hashlib
from typing import List, Optional, Union

import pandas as pd

from .base import BaseDataGateway
from .cache import FileCache
from .retry import retry_on_failure
from .symbol import canonicalize, to_jq, to_qlib

# Qlib 为可选依赖
try:
    import qlib
    from qlib.constant import REG_CN
    from qlib.data import D
except Exception:  # pragma: no cover
    qlib = None
    REG_CN = "cn"
    D = None


class QlibDataGateway(BaseDataGateway):
    """基于 Qlib 的数据网关适配器。"""

    _qlib_initialized: bool = False

    def __init__(
        self,
        database_uri: Optional[str] = None,
        region: str = REG_CN,
        cache_dir: str = ".gateway_cache_qlib",
        ttl_seconds: int = 86400,
        retry: int = 3,
        retry_sleep: float = 1.0,
    ):
        self.database_uri = database_uri
        self.region = region
        self.cache = FileCache(cache_dir, ttl_seconds)
        self.retry = retry
        self.retry_sleep = retry_sleep
        self._init_qlib_once()

    def _init_qlib_once(self) -> None:
        if qlib is None:
            raise ImportError("qlib is required for QlibDataGateway")
        if not QlibDataGateway._qlib_initialized:
            kwargs = {"region": self.region}
            if self.database_uri:
                kwargs["database_uri"] = self.database_uri
            qlib.init(**kwargs)
            QlibDataGateway._qlib_initialized = True

    def _cache_key(self, method: str, **kwargs) -> str:
        payload = f"{method}:{sorted(kwargs.items())}"
        return hashlib.md5(payload.encode()).hexdigest()

    def _maybe_cached(self, method: str, force_update: bool, fetch_fn, **kwargs):
        key = self._cache_key(method, **kwargs)
        if not force_update:
            val = self.cache.get(key)
            if val is not None:
                return val
        val = fetch_fn()
        self.cache.set(key, val)
        return val

    @staticmethod
    def _to_qlib_instruments(codes: List[str]) -> List[str]:
        return [to_qlib(c) for c in codes]

    @retry_on_failure(max_retry=3, sleep=1.0)
    def get_price(
        self,
        symbols: Union[str, List[str]],
        start_date: str,
        end_date: str,
        frequency: str = "daily",
        fields: Optional[List[str]] = None,
        adjust: str = "qfq",
        count: Optional[int] = None,
        force_update: bool = False,
    ) -> Union[pd.DataFrame, dict[str, pd.DataFrame]]:
        if D is None:
            raise ImportError("qlib is required for QlibDataGateway")
        if isinstance(symbols, str):
            symbols = [symbols]
        symbols = [canonicalize(s) for s in symbols]
        qlib_fields = fields or ["open", "high", "low", "close", "volume"]
        exprs = [f"${f}" for f in qlib_fields]
        instruments = self._to_qlib_instruments(symbols)
        df = self._maybe_cached(
            "get_price",
            force_update,
            lambda: D.features(instruments, exprs, start_time=start_date, end_time=end_date),
            symbols=tuple(symbols),
            start_date=start_date,
            end_date=end_date,
            fields=tuple(qlib_fields),
        )
        if df is None or df.empty:
            return {s: pd.DataFrame() for s in symbols} if len(symbols) > 1 else pd.DataFrame()
        # 字段重命名 $open -> open
        rename_map = {f"${f}": f for f in qlib_fields}
        df = df.rename(columns=rename_map)
        df = df.reset_index()
        # 拆分为 dict[symbol] -> DataFrame
        result = {}
        for sym in symbols:
            qlib_sym = to_qlib(sym)
            sub = df[df["instrument"] == qlib_sym].copy()
            sub = sub.rename(columns={"datetime": "datetime"})
            sub = sub[["datetime"] + [f for f in qlib_fields if f in sub.columns]]
            result[sym] = sub.reset_index(drop=True)
        return result if len(result) > 1 else result[symbols[0]]

    @retry_on_failure(max_retry=3, sleep=1.0)
    def get_bars(
        self,
        security: str,
        count: int,
        unit: str = "1d",
        fields: Optional[List[str]] = None,
        end_dt: Optional[str] = None,
    ) -> pd.DataFrame:
        # Qlib D.features 不直接支持按 count 拉取，这里以 end_dt 为结束日期往前截断
        # 为简化，start 取一个足够早的日期
        start_date = "2000-01-01"
        df = self.get_price(
            security,
            start_date=start_date,
            end_date=end_dt or "2099-12-31",
            frequency=unit,
            fields=fields,
        )
        if isinstance(df, dict):
            df = df.get(canonicalize(security), pd.DataFrame())
        if df.empty:
            return df
        return df.tail(count).reset_index(drop=True)

    @retry_on_failure(max_retry=3, sleep=1.0)
    def get_all_securities(
        self, types: Optional[List[str]] = None, date: Optional[str] = None, force_update: bool = False
    ) -> pd.DataFrame:
        # Qlib 没有全市场 stock_basic 表，这里返回空 DataFrame 并给出提示
        return pd.DataFrame(
            columns=["code", "name", "jq_code"]
        )

    @retry_on_failure(max_retry=3, sleep=1.0)
    def get_security_info(self, code: str) -> Optional[dict]:
        # Qlib 无直接对应接口
        return None

    @retry_on_failure(max_retry=3, sleep=1.0)
    def get_fundamentals(
        self,
        query_obj: dict,
        date: Optional[str] = None,
        stat_date: Optional[str] = None,
    ) -> pd.DataFrame:
        raise NotImplementedError("QlibDataGateway 不支持原始财报三张表查询，请使用 Qlib 特征表达式或切换到 JQ/TuShare 网关")

    @retry_on_failure(max_retry=3, sleep=1.0)
    def get_history_fundamentals(
        self,
        security: Union[str, List[str]],
        fields: List[str],
        watch_date: Optional[str] = None,
        stat_date: Optional[str] = None,
        count: int = 1,
        interval: str = "1q",
    ) -> pd.DataFrame:
        raise NotImplementedError("QlibDataGateway 不支持原始财报三张表查询")

    @retry_on_failure(max_retry=3, sleep=1.0)
    def get_index_members(self, index_code: str, date: Optional[str] = None) -> List[str]:
        if D is None:
            raise ImportError("qlib is required for QlibDataGateway")
        market_map = {"000300": "csi300", "000500": "csi500", "000852": "csi1000"}
        market = market_map.get(index_code, index_code)
        inst = D.instruments(market=market)
        # Qlib 的 instruments 是过滤对象，list_instruments 拿到实际列表
        codes = D.list_instruments(inst)
        # codes 形式为 ['SH600000', 'SZ000001', ...]
        return [to_jq(c) for c in codes]

    @retry_on_failure(max_retry=3, sleep=1.0)
    def get_trade_days(
        self, start_date: Optional[str] = None, end_date: Optional[str] = None
    ) -> List[pd.Timestamp]:
        if D is None:
            raise ImportError("qlib is required for QlibDataGateway")
        days = D.calendar(start_time=start_date or "2000-01-01", end_time=end_date or "2099-12-31", freq="day")
        return [pd.Timestamp(d) for d in days]

    @retry_on_failure(max_retry=3, sleep=1.0)
    def get_extras(
        self,
        field: str,
        securities: Union[str, List[str]],
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
    ) -> pd.DataFrame:
        # Qlib 通常不直接提供 ST/停牌 表，返回空结构
        return pd.DataFrame()
