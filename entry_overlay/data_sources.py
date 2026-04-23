from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

import pandas as pd


class MarketDataAdapter:
    """统一行情数据接口，兼容 JoinQuant / Akshare / 本地DataFrame."""

    def get_bars(
        self,
        code: str,
        start: Optional[pd.Timestamp],
        end: pd.Timestamp,
        freq: str = "1m",
        count: Optional[int] = None,
    ) -> pd.DataFrame:
        raise NotImplementedError


@dataclass
class PandasAdapter(MarketDataAdapter):
    data: pd.DataFrame
    code_col: str = "code"
    time_col: str = "time"

    def get_bars(self, code, start, end, freq="1m", count=None):
        df = self.data[self.data[self.code_col] == code].copy()
        ts = pd.to_datetime(df[self.time_col])
        mask = ts <= pd.Timestamp(end)
        if start is not None:
            mask &= ts >= pd.Timestamp(start)
        out = df.loc[mask].copy()
        out.index = pd.to_datetime(out[self.time_col])
        out = out[["open", "high", "low", "close", "volume"]].sort_index()
        if count:
            out = out.tail(count)
        return out


class JQDataAdapter(MarketDataAdapter):
    """JoinQuant 适配器，运行环境中可直接复用 get_price。"""

    def get_bars(self, code, start, end, freq="1m", count=None):
        try:
            from jqdata import get_price  # type: ignore
        except Exception as exc:
            raise RuntimeError("JQDataAdapter 需要在 JoinQuant 环境运行") from exc

        if count is not None:
            df = get_price(
                code,
                end_date=end,
                count=count,
                frequency=freq,
                fields=["open", "high", "low", "close", "volume"],
            )
        else:
            df = get_price(
                code,
                start_date=start,
                end_date=end,
                frequency=freq,
                fields=["open", "high", "low", "close", "volume"],
            )
        return df[["open", "high", "low", "close", "volume"]]


class AkshareAdapter(MarketDataAdapter):
    """Akshare 适配器。

    注意：不同市场API字段略有差异，这里统一映射到 OHLCV。
    """

    def __init__(self, market: str = "cn"):
        self.market = market

    def get_bars(self, code, start, end, freq="1m", count=None):
        try:
            import akshare as ak  # type: ignore
        except Exception as exc:
            raise RuntimeError("AkshareAdapter 需要安装 akshare") from exc

        if self.market != "cn":
            raise NotImplementedError("当前示例仅实现A股分钟行情")

        period = "1" if freq in ("1m", "1min") else "5"
        start_s = pd.Timestamp(start or end - pd.Timedelta(days=7)).strftime("%Y-%m-%d %H:%M:%S")
        end_s = pd.Timestamp(end).strftime("%Y-%m-%d %H:%M:%S")

        raw = ak.stock_zh_a_hist_min_em(symbol=code.split(".")[0], period=period, start_date=start_s, end_date=end_s, adjust="qfq")
        col_map = {
            "时间": "time",
            "开盘": "open",
            "收盘": "close",
            "最高": "high",
            "最低": "low",
            "成交量": "volume",
        }
        raw = raw.rename(columns=col_map)
        raw["time"] = pd.to_datetime(raw["time"])
        raw = raw.set_index("time").sort_index()
        out = raw[["open", "high", "low", "close", "volume"]]
        if count:
            out = out.tail(count)
        return out
