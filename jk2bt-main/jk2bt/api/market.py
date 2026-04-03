"""
market.py
行情数据 API 权威模块（权威文件）

合并自 market_api.py 和 market_api_enhanced.py，并包含来自 enhancements.py 的
行情辅助函数（get_open_price、get_close_price、get_high_limit、get_low_limit）。

数据源说明:
- 市场行情数据优先使用 market_data 模块（支持多数据源备份）
- akshare 作为备用数据源（延迟导入）
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import warnings
import logging


def _get_akshare():
    """延迟导入 akshare，作为备用数据源"""
    try:
        import akshare as ak
        return ak
    except ImportError:
        warnings.warn("AkShare 未安装，行情 API 备用数据源不可用")
        return None

try:
    from utils.standardize import (
        normalize_columns,
        normalize_datetime,
        COLUMN_MAP_COMMON,
    )
except ImportError:
    COLUMN_MAP_COMMON = {
        "日期": "datetime", "时间": "datetime", "day": "datetime",
        "开盘": "open", "最高": "high", "最低": "low", "收盘": "close",
        "成交量": "volume", "成交额": "money", "amount": "money",
    }

    def normalize_columns(df, column_map=None):
        if column_map is None:
            column_map = COLUMN_MAP_COMMON
        df = df.copy()
        for old_col, new_col in column_map.items():
            if old_col in df.columns and new_col not in df.columns:
                df[new_col] = df[old_col]
        return df

    def normalize_datetime(df, errors="coerce"):
        df = df.copy()
        if "datetime" not in df.columns:
            return df
        df["datetime"] = pd.to_datetime(df["datetime"], errors=errors)
        df = df.dropna(subset=["datetime"])
        return df.sort_values("datetime").reset_index(drop=True)

try:
    from jk2bt.core.exceptions import (
        MarketDataError, NetworkError, DataSourceError, ValidationError,
    )
except ImportError:
    class MarketDataError(Exception): pass
    class NetworkError(Exception): pass
    class DataSourceError(Exception): pass
    class ValidationError(Exception): pass

logger = logging.getLogger(__name__)

from jk2bt.api._internal.symbol_utils import (
    normalize_symbol,
    get_symbol_prefix,
    is_gem_or_star,
    calculate_limit_price,
)

_normalize_symbol = normalize_symbol
_get_symbol_prefix = get_symbol_prefix
_is_gem_or_star = is_gem_or_star
_calculate_limit_price = calculate_limit_price


def _fq_to_adjust(fq):
    fq_map = {"pre": "qfq", "post": "hfq", "none": "", None: "qfq"}
    return fq_map.get(fq, "qfq")


def _fetch_price_data(symbol, start_date, end_date, frequency="daily", adjust="qfq"):
    """从缓存或 AkShare 获取行情数据"""
    ak_sym = _normalize_symbol(symbol)

    is_lof = ak_sym.startswith("16")
    is_etf = (
        ak_sym.startswith("51") or ak_sym.startswith("15") or ak_sym.startswith("50")
        or ak_sym.startswith("52") or ak_sym.startswith("56") or ak_sym.startswith("58")
    )
    is_index = (
        (ak_sym.startswith("000") and ak_sym in [
            "000001", "000002", "000003", "000004", "000005", "000006", "000007",
            "000008", "000009", "000010", "000011", "000012", "000013", "000014",
            "000015", "000016", "000017", "000018", "000300", "000688", "000851",
            "000852", "000903", "000905", "000906", "000978",
        ])
        or ak_sym.startswith("399")
    )

    try:
        if frequency in ["1d", "daily"]:
            if is_index:
                try:
                    from .market_data.index import get_index_daily
                except ImportError:
                    try:
                        from market_data.index import get_index_daily
                    except ImportError:
                        from jk2bt.market_data.index import get_index_daily
                try:
                    df = get_index_daily(
                        ak_sym,
                        start_date or "1990-01-01",
                        end_date or datetime.now().strftime("%Y-%m-%d"),
                    )
                    if df is not None and not df.empty:
                        return df
                except ConnectionError as e:
                    raise NetworkError("指数行情网络连接失败", context={"symbol": symbol}) from e
                except Exception as e:
                    raise MarketDataError("指数行情获取失败", context={"symbol": symbol}) from e

            if is_lof:
                try:
                    from .market_data.lof import get_lof_daily_with_fallback
                except ImportError:
                    from market_data.lof import get_lof_daily_with_fallback
                try:
                    df = get_lof_daily_with_fallback(
                        ak_sym,
                        start_date or "1990-01-01",
                        end_date or datetime.now().strftime("%Y-%m-%d"),
                    )
                    if df is not None and not df.empty:
                        return df
                except Exception:
                    return pd.DataFrame()

            # 优先使用 market_data.stock 模块获取股票日线数据
            ak_code = ("sh" if ak_sym.startswith("6") else "sz") + ak_sym
            try:
                try:
                    from jk2bt.market_data.stock import get_stock_daily
                except ImportError:
                    try:
                        from .market_data.stock import get_stock_daily
                    except ImportError:
                        from market_data.stock import get_stock_daily

                df = get_stock_daily(
                    ak_code,
                    start_date or "1990-01-01",
                    end_date or datetime.now().strftime("%Y-%m-%d"),
                    adjust=adjust,
                )
                if df is not None and not df.empty:
                    return df
            except Exception as stock_err:
                logger.warning(f"{symbol}: market_data.stock 获取失败: {stock_err}，尝试备用数据源")

            # 备用数据源: akshare（延迟导入）
            ak = _get_akshare()
            if ak is None:
                warnings.warn(f"{symbol}: AkShare 未安装，尝试从缓存加载日线数据")
                try:
                    from .db.duckdb_manager import DuckDBManager
                except ImportError:
                    from jk2bt.db.duckdb_manager import DuckDBManager
                db = DuckDBManager(read_only=True)
                df = db.get_stock_daily(
                    ak_code,
                    start_date or "1990-01-01",
                    end_date or datetime.now().strftime("%Y-%m-%d"),
                    adjust,
                )
                return df

            try:
                df = ak.stock_zh_a_hist(
                    symbol=ak_sym,
                    period="daily",
                    start_date=start_date.replace("-", "") if start_date else "19900101",
                    end_date=end_date.replace("-", "") if end_date else datetime.now().strftime("%Y%m%d"),
                    adjust=adjust,
                )
            except ConnectionError as e:
                raise NetworkError("股票行情网络连接失败", context={"symbol": symbol}) from e
            except ValueError:
                return pd.DataFrame()

            if df is None or df.empty:
                return pd.DataFrame()
            return df

        elif frequency in ["1m", "5m", "15m", "30m", "60m", "minute"]:
            try:
                try:
                    from jk2bt.market_data.minute import get_stock_minute, get_etf_minute
                except ImportError:
                    try:
                        from .market_data.minute import get_stock_minute, get_etf_minute
                    except ImportError:
                        from market_data.minute import get_stock_minute, get_etf_minute
            except ImportError as import_error:
                warnings.warn(f"{symbol}: 分钟数据模块导入失败")
                return pd.DataFrame()

            period_map = {"1m": "1m", "5m": "5m", "15m": "15m", "30m": "30m", "60m": "60m"}
            period = period_map.get(frequency, "1m")
            ak_code = ("sh" if ak_sym.startswith("6") else "sz") + ak_sym

            if not start_date:
                start_date = "1979-09-01 09:30:00"
            if not end_date:
                end_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            try:
                if is_lof:
                    try:
                        from .market_data.lof import get_lof_min
                    except ImportError:
                        from market_data.lof import get_lof_min
                    df = get_lof_min(ak_sym, start_date, end_date, period=period.replace("m", ""))
                elif is_etf:
                    df = get_etf_minute(ak_sym, start_date, end_date, period=period)
                else:
                    df = get_stock_minute(ak_code, start_date, end_date, period=period, adjust=adjust)

                if df.empty:
                    return pd.DataFrame()

                df = normalize_columns(df, COLUMN_MAP_COMMON)
                if "datetime" not in df.columns:
                    df["datetime"] = pd.to_datetime(
                        df.index if df.index.name == "datetime" else df.get("时间")
                    )
                df["datetime"] = pd.to_datetime(df["datetime"], errors="coerce")
                df = df.dropna(subset=["datetime"])

                if start_date and end_date:
                    start_dt = pd.to_datetime(start_date)
                    end_dt = pd.to_datetime(end_date)
                    df = df[(df["datetime"] >= start_dt) & (df["datetime"] <= end_dt)]

                return df

            except ConnectionError as e:
                raise NetworkError("分钟数据网络连接失败", context={"symbol": symbol}) from e
            except Exception as minute_error:
                warnings.warn(f"{symbol} ({frequency}) 分钟数据获取失败: {minute_error}")
                return pd.DataFrame()
        else:
            raise ValueError(f"不支持的 frequency: {frequency}")

    except ValueError:
        raise
    except (NetworkError, ValidationError, MarketDataError):
        raise
    except Exception as e:
        warnings.warn(f"{symbol} 行情获取失败: {e}")
        return pd.DataFrame()


def _standardize_columns(df):
    df = normalize_columns(df, COLUMN_MAP_COMMON)
    df = normalize_datetime(df)
    return df


def _add_derived_fields(df, symbol):
    if df.empty:
        return df
    c = _normalize_symbol(symbol)
    df["pre_close"] = df["close"].shift(1)
    df["paused"] = 0
    if "volume" in df.columns:
        df.loc[df["volume"] == 0, "paused"] = 1

    def _calc_high_limit(row):
        if row["paused"] == 1:
            return None
        prev = row["pre_close"]
        if pd.isna(prev) or prev <= 0:
            return None
        return _calculate_limit_price(prev, c, "up")

    def _calc_low_limit(row):
        if row["paused"] == 1:
            return None
        prev = row["pre_close"]
        if pd.isna(prev) or prev <= 0:
            return None
        return _calculate_limit_price(prev, c, "down")

    df["high_limit"] = df.apply(_calc_high_limit, axis=1)
    df["low_limit"] = df.apply(_calc_low_limit, axis=1)
    return df


def get_price(
    security,
    start_date=None,
    end_date=None,
    frequency="daily",
    fields=None,
    skip_paused=True,
    fq="pre",
    count=None,
    panel=True,
    fill_paused=True,
):
    """获取历史行情数据（聚宽风格）"""
    adjust = _fq_to_adjust(fq)

    if isinstance(security, str):
        security = [security]

    if count and not start_date:
        if end_date:
            end_dt = pd.to_datetime(end_date)
        else:
            end_dt = pd.Timestamp.now()
        start_dt = end_dt - pd.Timedelta(days=count * 3)
        start_date = start_dt.strftime("%Y-%m-%d")
        if not end_date:
            end_date = end_dt.strftime("%Y-%m-%d")

    result = {}

    for symbol in security:
        raw_df = _fetch_price_data(symbol, start_date, end_date, frequency, adjust)

        if raw_df.empty:
            result[symbol] = pd.DataFrame()
            continue

        df = _standardize_columns(raw_df)
        df = _add_derived_fields(df, symbol)

        if count:
            df = df.tail(count)

        default_fields = [
            "datetime", "open", "high", "low", "close", "volume", "money",
            "paused", "pre_close", "high_limit", "low_limit",
        ]
        if fields:
            keep_cols = ["datetime"] + [f for f in fields if f in df.columns]
        else:
            keep_cols = [f for f in default_fields if f in df.columns]

        df = df[[c for c in keep_cols if c in df.columns]].copy()

        if skip_paused and "paused" in df.columns:
            df = df[df["paused"] == 0].copy()

        if fill_paused and "paused" in df.columns:
            if not df[df["paused"] == 1].empty:
                for col in ["open", "high", "low", "close"]:
                    if col in df.columns:
                        df.loc[df["paused"] == 1, col] = df.loc[df["paused"] == 1, "pre_close"]
                if "volume" in df.columns:
                    df.loc[df["paused"] == 1, "volume"] = 0
                if "money" in df.columns:
                    df.loc[df["paused"] == 1, "money"] = 0

        df = df.reset_index(drop=True)
        result[symbol] = df

    if len(result) == 1:
        return result[security[0]]

    if panel:
        return result
    else:
        combined = []
        for sym, df in result.items():
            if not df.empty:
                df_copy = df.copy()
                df_copy["code"] = sym
                combined.append(df_copy)
        if not combined:
            return pd.DataFrame()
        return pd.concat(combined, ignore_index=True)


def get_price_jq(*args, **kwargs):
    """get_price 的别名，保持 JQ 风格命名兼容"""
    return get_price(*args, **kwargs)


def history(
    count,
    unit="1d",
    field="close",
    security_list=None,
    df=True,
    skip_paused=True,
    fq="pre",
    end_date=None,
):
    """获取多个标的单个字段的历史数据（聚宽风格）"""
    if security_list is None:
        if df:
            return pd.DataFrame()
        return {}

    if isinstance(security_list, str):
        security_list = [security_list]

    adjust = _fq_to_adjust(fq)
    frequency = "daily" if unit in ["1d", "daily"] else unit

    if end_date:
        end_dt = pd.to_datetime(end_date)
    else:
        try:
            from jk2bt.core.runner import _get_current_strategy
            strategy = _get_current_strategy()
            if strategy is not None and hasattr(strategy, "current_dt") and strategy.current_dt is not None:
                end_dt = strategy.current_dt
            else:
                end_dt = pd.Timestamp.now()
        except ImportError:
            end_dt = pd.Timestamp.now()

    if frequency == "daily":
        start_dt = end_dt - pd.Timedelta(days=count * 3)
        start_date = start_dt.strftime("%Y-%m-%d")
        end_date_str = end_dt.strftime("%Y-%m-%d")
    else:
        period_minutes = {"1m": 1, "5m": 5, "15m": 15, "30m": 30, "60m": 60}
        minutes = period_minutes.get(frequency, 5)
        start_dt = end_dt - pd.Timedelta(minutes=count * minutes * 5)
        start_date = start_dt.strftime("%Y-%m-%d %H:%M:%S")
        end_date_str = end_dt.strftime("%Y-%m-%d %H:%M:%S")

    frames = {}

    for symbol in security_list:
        raw_df = _fetch_price_data(symbol, start_date, end_date_str, frequency, adjust)

        if raw_df.empty:
            frames[symbol] = pd.Series(dtype=float)
            continue

        df_temp = _standardize_columns(raw_df)
        df_temp = _add_derived_fields(df_temp, symbol)

        if "datetime" in df_temp.columns:
            df_temp = df_temp.set_index("datetime")

        df_temp = df_temp[df_temp.index <= end_dt].tail(count)

        if skip_paused and "paused" in df_temp.columns:
            df_temp = df_temp[df_temp["paused"] == 0]

        if field in df_temp.columns:
            frames[symbol] = df_temp[field]
        else:
            frames[symbol] = pd.Series(dtype=float)

    if not df:
        return {sym: ser.values for sym, ser in frames.items()}

    return pd.DataFrame(frames)


def attribute_history(
    security,
    count,
    unit="1d",
    fields=None,
    skip_paused=True,
    df=True,
    fq="pre",
    end_date=None,
):
    """获取单个标的多字段历史数据（聚宽风格）"""
    if fields is None:
        fields = ["open", "close", "high", "low", "volume", "money"]

    adjust = _fq_to_adjust(fq)
    frequency = "daily" if unit in ["1d", "daily"] else unit

    if end_date:
        end_dt = pd.to_datetime(end_date)
    else:
        try:
            from jk2bt.core.runner import _get_current_strategy
            strategy = _get_current_strategy()
            if strategy is not None and hasattr(strategy, "current_dt") and strategy.current_dt is not None:
                end_dt = strategy.current_dt
            else:
                end_dt = pd.Timestamp.now()
        except ImportError:
            end_dt = pd.Timestamp.now()

    if frequency == "daily":
        start_dt = end_dt - pd.Timedelta(days=count * 3)
        start_date = start_dt.strftime("%Y-%m-%d")
        end_date_str = end_dt.strftime("%Y-%m-%d")
    else:
        period_minutes = {"1m": 1, "5m": 5, "15m": 15, "30m": 30, "60m": 60}
        minutes = period_minutes.get(frequency, 5)
        start_dt = end_dt - pd.Timedelta(minutes=count * minutes * 5)
        start_date = start_dt.strftime("%Y-%m-%d %H:%M:%S")
        end_date_str = end_dt.strftime("%Y-%m-%d %H:%M:%S")

    raw_df = _fetch_price_data(security, start_date, end_date_str, frequency, adjust)

    if raw_df.empty:
        if df:
            return pd.DataFrame()
        return {}

    df_temp = _standardize_columns(raw_df)
    df_temp = _add_derived_fields(df_temp, security)

    if "datetime" in df_temp.columns:
        df_temp = df_temp.set_index("datetime")

    df_temp = df_temp[df_temp.index <= end_dt].tail(count)

    if skip_paused and "paused" in df_temp.columns:
        df_temp = df_temp[df_temp["paused"] == 0]

    keep_cols = [f for f in fields if f in df_temp.columns]
    result = df_temp[keep_cols].copy()

    if not df:
        return {col: result[col].values for col in result.columns}

    return result


def get_bars(
    security,
    count,
    unit="1d",
    fields=None,
    include_now=False,
    end_dt=None,
    fq="pre",
    skip_paused=False,
):
    """获取历史 K 线数据（聚宽风格）"""
    adjust = _fq_to_adjust(fq)
    frequency = "daily" if unit in ["1d", "daily"] else unit

    if end_dt:
        end_dt = pd.to_datetime(end_dt)
    else:
        end_dt = pd.Timestamp.now()

    if frequency == "daily":
        start_dt = end_dt - pd.Timedelta(days=count * 3)
        start_date = start_dt.strftime("%Y-%m-%d")
        end_date_str = end_dt.strftime("%Y-%m-%d")
    else:
        period_minutes = {"1m": 1, "5m": 5, "15m": 15, "30m": 30, "60m": 60}
        minutes = period_minutes.get(frequency, 5)
        start_dt_calc = end_dt - pd.Timedelta(minutes=count * minutes * 5)
        start_date = start_dt_calc.strftime("%Y-%m-%d %H:%M:%S")
        end_date_str = end_dt.strftime("%Y-%m-%d %H:%M:%S")

    if isinstance(security, str):
        security = [security]

    if len(security) == 1:
        raw_df = _fetch_price_data(security[0], start_date, end_date_str, frequency, adjust)

        if raw_df.empty:
            return pd.DataFrame()

        df_temp = _standardize_columns(raw_df)
        df_temp = _add_derived_fields(df_temp, security[0])

        if "datetime" in df_temp.columns:
            df_temp = df_temp[df_temp["datetime"] <= end_dt]

        df_temp = df_temp.tail(count)

        if skip_paused and "paused" in df_temp.columns:
            df_temp = df_temp[df_temp["paused"] == 0]

        default_fields = ["datetime", "open", "high", "low", "close", "volume", "money"]
        if fields:
            keep_cols = ["datetime"] + [f for f in fields if f in df_temp.columns]
        else:
            keep_cols = [f for f in default_fields if f in df_temp.columns]

        return df_temp[[c for c in keep_cols if c in df_temp.columns]].reset_index(drop=True)

    else:
        result = {}
        for sym in security:
            result[sym] = get_bars(sym, count, unit, fields, include_now, end_dt, fq, skip_paused)
        return result


def get_bars_jq(*args, **kwargs):
    """get_bars 的别名，保持 JQ 风格命名兼容"""
    return get_bars(*args, **kwargs)


# ---------------------------------------------------------------------------
# 来自 market_api_enhanced.py 的函数
# ---------------------------------------------------------------------------

def _fetch_valuation_data(symbol, date=None):
    """获取估值数据（PE/PB/市值等）"""
    ak_sym = _normalize_symbol(symbol)

    try:
        ak = _get_akshare()
        if ak is None:
            warnings.warn(f"{symbol}: AkShare 未安装，无法获取估值数据")
            return pd.DataFrame()

        df = ak.stock_a_lg_indicator(symbol=ak_sym)

        if df is None or df.empty:
            return pd.DataFrame()

        col_map = {
            "日期": "datetime", "pe": "pe", "pe_ttm": "pe_ttm", "pb": "pb",
            "ps": "ps", "dv_ratio": "dividend_ratio", "total_mv": "market_cap",
            "circ_mv": "circulating_market_cap",
        }
        df = df.rename(columns=col_map)

        if "datetime" in df.columns:
            df["datetime"] = pd.to_datetime(df["datetime"], errors="coerce")
            df = df.dropna(subset=["datetime"])
            df = df.sort_values("datetime").reset_index(drop=True)
            if date:
                df = df[df["datetime"] <= pd.to_datetime(date)].tail(1)

        return df

    except Exception as e:
        warnings.warn(f"{symbol} 估值数据获取失败: {e}")
        return pd.DataFrame()


def _fetch_realtime_quote(symbol):
    """获取实时行情数据"""
    ak_sym = _normalize_symbol(symbol)

    try:
        ak = _get_akshare()
        if ak is None:
            return {}

        df = ak.stock_zh_a_spot_em()

        if df is None or df.empty:
            return {}

        row = df[df["代码"] == ak_sym]
        if row.empty:
            return {}

        row = row.iloc[0]

        return {
            "code": symbol,
            "display_name": row.get("名称", ""),
            "last_price": row.get("最新价", 0),
            "bid_price": row.get("买一价", 0),
            "ask_price": row.get("卖一价", 0),
            "bid_volume": row.get("买一量", 0),
            "ask_volume": row.get("卖一量", 0),
            "high_limit": row.get("涨停价", 0),
            "low_limit": row.get("跌停价", 0),
            "pre_close": row.get("昨收", 0),
            "open": row.get("今开", 0),
            "high": row.get("最高", 0),
            "low": row.get("最低", 0),
            "volume": row.get("成交量", 0),
            "money": row.get("成交额", 0),
            "change_pct": row.get("涨跌幅", 0),
            "change": row.get("涨跌额", 0),
            "turnover_rate": row.get("换手率", 0),
        }

    except Exception as e:
        warnings.warn(f"{symbol} 实时行情获取失败: {e}")
        return {}


def _fetch_tick_data(symbol, count=1000, date=None):
    """获取 tick 级数据"""
    ak_sym = _normalize_symbol(symbol)

    try:
        ak = _get_akshare()
        if ak is None:
            return pd.DataFrame()

        try:
            df = ak.stock_zh_a_tick_tx_js(symbol=ak_sym)
        except Exception:
            prefix = _get_symbol_prefix(symbol)
            today = date or datetime.now().strftime("%Y-%m-%d")
            try:
                df = ak.stock_zh_a_hist_min_em(
                    symbol=f"{prefix}{ak_sym}",
                    period="1",
                    start_date=f"{today} 09:30:00",
                    end_date=f"{today} 15:00:00",
                    adjust="qfq",
                )
            except Exception:
                return pd.DataFrame()

        if df is None or df.empty:
            return pd.DataFrame()

        col_map = {
            "时间": "time", "成交时间": "time", "datetime": "time",
            "价格": "price", "成交价": "price", "close": "price",
            "成交量": "volume", "成交数量": "volume", "vol": "volume",
            "成交额": "amount", "amount": "amount", "成交金额": "amount", "money": "amount",
        }
        df = df.rename(columns={k: v for k, v in col_map.items() if k in df.columns})

        if "time" not in df.columns:
            df["time"] = pd.date_range(start="09:30:00", periods=len(df), freq="1min")

        if "price" not in df.columns and "close" in df.columns:
            df["price"] = df["close"]

        if "amount" not in df.columns and "volume" in df.columns and "price" in df.columns:
            df["amount"] = df["volume"] * df["price"]

        df["time"] = pd.to_datetime(df["time"], errors="coerce")
        df = df.dropna(subset=["time"])
        df = df.sort_values("time").reset_index(drop=True)

        if count and len(df) > count:
            df = df.tail(count)

        return df

    except Exception as e:
        warnings.warn(f"{symbol} tick 数据获取失败: {e}")
        return pd.DataFrame()


def get_market(
    security,
    start_date=None,
    end_date=None,
    frequency="1d",
    fields=None,
    count=None,
    fq="pre",
):
    """获取综合行情数据（聚宽风格增强版）"""
    fq_map = {"pre": "qfq", "post": "hfq", "none": "", None: "qfq"}
    adjust = fq_map.get(fq, "qfq")

    default_fields = ["open", "high", "low", "close", "volume", "money"]
    valuation_fields = ["pe", "pe_ttm", "pb", "ps", "market_cap", "circulating_market_cap", "dividend_ratio"]

    if fields is None:
        fields = default_fields

    need_valuation = any(f in fields for f in valuation_fields)

    if isinstance(security, str):
        security = [security]

    if count and not start_date:
        if end_date:
            end_dt = pd.to_datetime(end_date)
        else:
            end_dt = pd.Timestamp.now()
        start_dt = end_dt - pd.Timedelta(days=count * 3)
        start_date = start_dt.strftime("%Y-%m-%d")
        if not end_date:
            end_date = end_dt.strftime("%Y-%m-%d")

    result = {}

    for symbol in security:
        raw_df = _fetch_price_data(symbol, start_date, end_date, frequency, adjust)

        if raw_df.empty:
            result[symbol] = pd.DataFrame()
            continue

        df = normalize_columns(raw_df, COLUMN_MAP_COMMON)
        df = normalize_datetime(df)

        df["pre_close"] = df["close"].shift(1)
        df["high_limit"] = df.apply(
            lambda row: _calculate_limit_price(row["pre_close"], symbol, "up")
            if pd.notna(row["pre_close"]) else None, axis=1
        )
        df["low_limit"] = df.apply(
            lambda row: _calculate_limit_price(row["pre_close"], symbol, "down")
            if pd.notna(row["pre_close"]) else None, axis=1
        )

        if need_valuation:
            val_df = _fetch_valuation_data(symbol, end_date)
            if not val_df.empty and "datetime" in val_df.columns:
                df = df.merge(
                    val_df[["datetime"] + [f for f in valuation_fields if f in val_df.columns]],
                    on="datetime",
                    how="left",
                )

        if count and len(df) > count:
            df = df.tail(count)

        keep_cols = ["datetime"] + [f for f in fields if f in df.columns]
        df = df[[c for c in keep_cols if c in df.columns]].copy()
        df = df.reset_index(drop=True)
        result[symbol] = df

    if len(result) == 1:
        return result[security[0]]

    return result


def get_detailed_quote(security, date=None):
    """获取详细行情信息（聚宽风格）"""
    if isinstance(security, str):
        security = [security]

    result = {}

    for symbol in security:
        if date is None:
            quote = _fetch_realtime_quote(symbol)

            if not quote:
                df = _fetch_price_data(symbol, None, datetime.now().strftime("%Y-%m-%d"))
                if not df.empty:
                    df = normalize_columns(df, COLUMN_MAP_COMMON)
                    df = normalize_datetime(df)
                    last_row = df.iloc[-1]
                    quote = {
                        "code": symbol,
                        "display_name": "",
                        "last_price": last_row.get("close", 0),
                        "bid_price": None, "ask_price": None,
                        "bid_volume": None, "ask_volume": None,
                        "high_limit": _calculate_limit_price(last_row.get("close", 0), symbol, "up"),
                        "low_limit": _calculate_limit_price(last_row.get("close", 0), symbol, "down"),
                        "pre_close": df.iloc[-2].get("close", 0) if len(df) > 1 else None,
                        "open": last_row.get("open", 0),
                        "high": last_row.get("high", 0),
                        "low": last_row.get("low", 0),
                        "volume": last_row.get("volume", 0),
                        "money": last_row.get("money", 0),
                        "change_pct": None, "change": None, "turnover_rate": None,
                    }
        else:
            df = _fetch_price_data(symbol, date, date)
            if df.empty:
                result[symbol] = {}
                continue
            df = normalize_columns(df, COLUMN_MAP_COMMON)
            df = normalize_datetime(df)
            if df.empty:
                result[symbol] = {}
                continue
            row = df.iloc[-1]
            prev_close = df.iloc[-2].get("close", 0) if len(df) > 1 else None
            quote = {
                "code": symbol,
                "display_name": "",
                "last_price": row.get("close", 0),
                "bid_price": None, "ask_price": None,
                "bid_volume": None, "ask_volume": None,
                "high_limit": _calculate_limit_price(prev_close, symbol, "up"),
                "low_limit": _calculate_limit_price(prev_close, symbol, "down"),
                "pre_close": prev_close,
                "open": row.get("open", 0),
                "high": row.get("high", 0),
                "low": row.get("low", 0),
                "volume": row.get("volume", 0),
                "money": row.get("money", 0),
                "change_pct": (row.get("close", 0) - prev_close) / prev_close * 100 if prev_close else None,
                "change": row.get("close", 0) - prev_close if prev_close else None,
                "turnover_rate": None,
            }

        result[symbol] = quote

    if len(result) == 1:
        return result[security[0]]

    return result


def get_ticks_enhanced(security, count=1000, fields=None, df=True, date=None):
    """获取增强的 tick 级数据（聚宽风格）"""
    if fields is None:
        fields = ["time", "price", "volume", "amount"]

    if isinstance(security, str):
        security = [security]

    result = {}

    for symbol in security:
        tick_df = _fetch_tick_data(symbol, count=count, date=date)

        if tick_df.empty:
            result[symbol] = pd.DataFrame() if df else []
            continue

        keep_cols = [f for f in fields if f in tick_df.columns]
        tick_df = tick_df[[c for c in keep_cols if c in tick_df.columns]].copy()

        if df:
            result[symbol] = tick_df.reset_index(drop=True)
        else:
            tick_list = []
            for _, row in tick_df.iterrows():
                item = {}
                for f in fields:
                    if f in row.index:
                        val = row[f]
                        item[f] = val.strftime("%Y-%m-%d %H:%M:%S") if isinstance(val, pd.Timestamp) else val
                tick_list.append(item)
            result[symbol] = tick_list

    if len(result) == 1:
        return result[security[0]]

    return result


# ---------------------------------------------------------------------------
# 来自 enhancements.py 的行情辅助函数
# ---------------------------------------------------------------------------

def get_open_price(security, date=None):
    """获取开盘价"""
    from jk2bt.core.strategy_base import get_current_data
    return get_current_data()[security].day_open


def get_close_price(security, date=None):
    """获取收盘价（最新价）"""
    from jk2bt.core.strategy_base import get_current_data
    return get_current_data()[security].last_price


def get_high_limit(security):
    """获取涨停价"""
    from jk2bt.core.strategy_base import get_current_data
    return get_current_data()[security].high_limit


def get_low_limit(security):
    """获取跌停价"""
    from jk2bt.core.strategy_base import get_current_data
    return get_current_data()[security].low_limit


__all__ = [
    # 来自 market_api.py
    "get_price",
    "get_price_jq",
    "history",
    "attribute_history",
    "get_bars",
    "get_bars_jq",
    # 来自 market_api_enhanced.py
    "get_market",
    "get_detailed_quote",
    "get_ticks_enhanced",
    # 来自 enhancements.py（行情辅助）
    "get_open_price",
    "get_close_price",
    "get_high_limit",
    "get_low_limit",
]
