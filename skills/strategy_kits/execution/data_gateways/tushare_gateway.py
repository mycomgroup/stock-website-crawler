"""TuShare 数据网关适配器。"""

import hashlib
from typing import List, Optional, Union

import pandas as pd

from .base import BaseDataGateway
from .cache import FileCache
from .retry import retry_on_failure
from .symbol import canonicalize, to_jq, to_ts

# TuShare 为可选依赖
try:
    import tushare as ts
except Exception:  # pragma: no cover
    ts = None


class _TuShareClient:
    """最小复用 QuantsPlaybook 中的无限重试思想，内部保持轻量封装。"""

    def __init__(self, token: str, max_retry: int = 10):
        if ts is None:
            raise ImportError("tushare is required for TuShareDataGateway")
        ts.set_token(token)
        self.pro = ts.pro_api()
        self.max_retry = max_retry

    def __getattr__(self, name):
        import time

        def wrapper(*args, **kwargs):
            for i in range(self.max_retry):
                try:
                    if name == "pro_bar":
                        m = getattr(ts, name, None)
                    else:
                        m = getattr(self.pro, name, None)
                    if m is None:
                        raise AttributeError(f"TuShare method {name} does not exist")
                    return m(*args, **kwargs)
                except Exception as e:
                    if i == self.max_retry - 1:
                        raise e
                    time.sleep(1)

        return wrapper


class TuShareDataGateway(BaseDataGateway):
    """基于 TuShare 的数据网关适配器。"""

    def __init__(
        self,
        token: str,
        cache_dir: str = ".gateway_cache_ts",
        ttl_seconds: int = 86400,
        retry: int = 3,
        retry_sleep: float = 1.0,
    ):
        self.client = _TuShareClient(token)
        self.cache = FileCache(cache_dir, ttl_seconds)
        self.retry = retry
        self.retry_sleep = retry_sleep

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
        if isinstance(symbols, str):
            symbols = [symbols]
        symbols = [canonicalize(s) for s in symbols]
        adj_flag = "qfq" if adjust == "qfq" else ("hfq" if adjust == "hfq" else "")
        result: dict[str, pd.DataFrame] = {}
        for symbol in symbols:
            ts_code = to_ts(symbol)
            df = self._maybe_cached(
                "get_price",
                force_update,
                lambda: self._fetch_price_native(ts_code, start_date, end_date, frequency, adj_flag),
                symbol=symbol,
                start_date=start_date,
                end_date=end_date,
                frequency=frequency,
                adjust=adj_flag,
            )
            if df.empty:
                result[symbol] = df
                continue
            df = df.rename(
                columns={
                    "trade_date": "datetime",
                    "open": "open",
                    "high": "high",
                    "low": "low",
                    "close": "close",
                    "vol": "volume",
                    "amount": "money",
                }
            )
            if "datetime" in df.columns:
                df["datetime"] = pd.to_datetime(df["datetime"])
            if fields:
                keep = ["datetime"] + [f for f in fields if f in df.columns]
                df = df[keep]
            result[symbol] = df.reset_index(drop=True)
        return result if len(result) > 1 else result[symbols[0]]

    def _fetch_price_native(self, ts_code: str, start_date: str, end_date: str, frequency: str, adjust: str) -> pd.DataFrame:
        freq = "D" if frequency in ("1d", "daily") else frequency
        df = self.client.pro_bar(
            ts_code=ts_code,
            start_date=start_date.replace("-", ""),
            end_date=end_date.replace("-", ""),
            freq=freq,
            adj=adjust,
        )
        if df is None:
            return pd.DataFrame()
        return df.copy()

    @retry_on_failure(max_retry=3, sleep=1.0)
    def get_bars(
        self,
        security: str,
        count: int,
        unit: str = "1d",
        fields: Optional[List[str]] = None,
        end_dt: Optional[str] = None,
    ) -> pd.DataFrame:
        ts_code = to_ts(canonicalize(security))
        freq = "D" if unit in ("1d", "daily") else unit
        end_date = end_dt.replace("-", "") if end_dt else None
        df = self.client.pro_bar(ts_code=ts_code, freq=freq, adj="qfq")
        if df is None or df.empty:
            return pd.DataFrame()
        df["trade_date"] = pd.to_datetime(df["trade_date"])
        if end_dt:
            df = df[df["trade_date"] <= pd.to_datetime(end_dt)]
        df = df.tail(count)
        df = df.rename(
            columns={
                "trade_date": "datetime",
                "open": "open",
                "high": "high",
                "low": "low",
                "close": "close",
                "vol": "volume",
                "amount": "money",
            }
        )
        if fields:
            keep = ["datetime"] + [f for f in fields if f in df.columns]
            df = df[keep]
        return df.reset_index(drop=True)

    @retry_on_failure(max_retry=3, sleep=1.0)
    def get_all_securities(
        self, types: Optional[List[str]] = None, date: Optional[str] = None, force_update: bool = False
    ) -> pd.DataFrame:
        df = self._maybe_cached(
            "get_all_securities", force_update, lambda: self.client.stock_basic(exchange="", list_status="L")
        )
        df["jq_code"] = df["ts_code"].apply(
            lambda x: f"{x.split('.')[0]}.XSHG" if x.endswith(".SH") else f"{x.split('.')[0]}.XSHE"
        )
        return df.copy()

    @retry_on_failure(max_retry=3, sleep=1.0)
    def get_security_info(self, code: str) -> Optional[dict]:
        ts_code = to_ts(canonicalize(code))
        df = self.client.stock_basic(ts_code=ts_code)
        if df is None or df.empty:
            return None
        return df.iloc[0].to_dict()

    @retry_on_failure(max_retry=3, sleep=1.0)
    def get_fundamentals(
        self,
        query_obj: dict,
        date: Optional[str] = None,
        stat_date: Optional[str] = None,
        force_update: bool = False,
    ) -> pd.DataFrame:
        if not isinstance(query_obj, dict):
            raise NotImplementedError("仅支持 dict 类型 query_obj")
        table = query_obj.get("table")
        symbol = query_obj.get("symbol")
        ts_code = to_ts(canonicalize(symbol))
        end = stat_date.replace("-", "") if stat_date else date.replace("-", "") if date else None
        if table == "balance":
            df = self._maybe_cached(
                "balance", force_update, lambda: self.client.balancesheet(ts_code=ts_code, end_date=end), ts_code=ts_code, end_date=end
            )
        elif table == "income":
            df = self._maybe_cached(
                "income", force_update, lambda: self.client.income(ts_code=ts_code, end_date=end), ts_code=ts_code, end_date=end
            )
        elif table == "cash_flow":
            df = self._maybe_cached(
                "cashflow", force_update, lambda: self.client.cashflow(ts_code=ts_code, end_date=end), ts_code=ts_code, end_date=end
            )
        else:
            raise NotImplementedError(f"暂不支持的 table: {table}")
        return df.copy() if df is not None else pd.DataFrame()

    @retry_on_failure(max_retry=3, sleep=1.0)
    def get_history_fundamentals(
        self,
        security: Union[str, List[str]],
        fields: List[str],
        watch_date: Optional[str] = None,
        stat_date: Optional[str] = None,
        count: int = 1,
        interval: str = "1q",
        force_update: bool = False,
    ) -> pd.DataFrame:
        # TuShare 侧与 JQ 侧逻辑类似：按前缀分发到三张表，再按 end_date/count 截取
        if isinstance(security, str):
            security = [security]
        dfs = []
        # 简单实现：对每个 symbol 调用 get_fundamentals，再 concat 并取头部 count 条
        for code in security:
            # 为简化骨架，这里直接透传第一个 table 前缀
            # 真实使用时可继续细化
            # 暂不支持多表合并（作为最小骨架，提示使用者自行扩展或直接使用 get_fundamentals）
            raise NotImplementedError("TuShareDataGateway.get_history_fundamentals 在最小骨架中未完整实现，建议直接调用 get_fundamentals")
        return pd.concat(dfs, ignore_index=True) if dfs else pd.DataFrame()

    @retry_on_failure(max_retry=3, sleep=1.0)
    def get_index_members(self, index_code: str, date: Optional[str] = None) -> List[str]:
        trade_date = date.replace("-", "") if date else None
        df = self.client.index_weight(index_code=index_code, trade_date=trade_date)
        if df is None or df.empty:
            return []
        codes = df["con_code"].astype(str).tolist()
        return [to_jq(c) for c in codes]

    @retry_on_failure(max_retry=3, sleep=1.0)
    def get_trade_days(
        self, start_date: Optional[str] = None, end_date: Optional[str] = None
    ) -> List[pd.Timestamp]:
        df = self.client.trade_cal(exchange="SSE")
        df = df[df["is_open"] == 1]
        days = pd.to_datetime(df["cal_date"]).tolist()
        if start_date:
            days = [d for d in days if d >= pd.to_datetime(start_date)]
        if end_date:
            days = [d for d in days if d <= pd.to_datetime(end_date)]
        return days

    @retry_on_failure(max_retry=3, sleep=1.0)
    def get_extras(
        self,
        field: str,
        securities: Union[str, List[str]],
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
    ) -> pd.DataFrame:
        if isinstance(securities, str):
            securities = [securities]
        ts_codes = [to_ts(canonicalize(s)) for s in securities]
        if field == "is_st":
            # TuShare 中 namechange 表可查询 ST 历史
            dfs = []
            for tc in ts_codes:
                df = self.client.namechange(ts_code=tc)
                if df is not None and not df.empty:
                    dfs.append(df)
            return pd.concat(dfs, ignore_index=True) if dfs else pd.DataFrame()
        elif field == "is_paused":
            dfs = []
            for tc in ts_codes:
                df = self.client.suspend_d(ts_code=tc)
                if df is not None and not df.empty:
                    dfs.append(df)
            return pd.concat(dfs, ignore_index=True) if dfs else pd.DataFrame()
        else:
            raise NotImplementedError(f"暂不支持的 extras 字段: {field}")
