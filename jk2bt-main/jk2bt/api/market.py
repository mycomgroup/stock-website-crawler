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
from datetime import datetime
import warnings
import logging

from jk2bt.data.sources import get_adapter

try:
    from jk2bt.utils.standardize import (
        normalize_columns,
        normalize_datetime,
        COLUMN_MAP_COMMON,
    )
except ImportError:
    from jk2bt.api.market_data.standardize import (
        normalize_columns,
        normalize_datetime,
        COLUMN_MAP_COMMON,
    )


from jk2bt.utils.exceptions import (
    MarketDataError,
    NetworkError,
    ValidationError,
)


logger = logging.getLogger(__name__)

from jk2bt.utils.symbol import (
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


_FUTURES_EXCHANGES = {".CCFX", ".XSGE", ".XDCE", ".XZCE", ".XINE", ".GFEX"}


def _is_futures_code(symbol):
    """判断是否为期货代码（如 IF2401.CCFX, RB2401.XSGE）"""
    sym = symbol.upper()
    for ex in _FUTURES_EXCHANGES:
        if sym.endswith(ex):
            return True
    return False


def _jq_futures_to_sina(symbol):
    """将聚宽风格期货代码转换为新浪期货符号。

    IF2401.CCFX -> IF2401
    AU9999.XSGE -> AU0  (连续合约使用主力合约)
    """
    sym = symbol.upper()
    for ex in _FUTURES_EXCHANGES:
        if sym.endswith(ex):
            code = sym[: -len(ex)]
            break
    else:
        code = sym

    # 9999 结尾表示连续合约，使用主力合约（0 结尾）
    if code.endswith("9999"):
        variety = code[:-4]
        return variety + "0"
    return code


def _fetch_futures_daily(symbol, start_date, end_date):
    """获取期货日线数据，返回与股票一致的 DataFrame 格式。"""
    try:
        df = get_adapter().get_futures_daily_with_fallback(
            symbol=symbol,
            start_date=start_date.replace("-", "") if start_date else None,
            end_date=end_date.replace("-", "") if end_date else None,
        )
        return df
    except Exception as e:
        warnings.warn(f"期货 {symbol} 获取失败: {e}")
        return pd.DataFrame()


def _fetch_price_data(symbol, start_date, end_date, frequency="daily", adjust="qfq"):
    """从缓存或 AkShare 获取行情数据"""
    # 期货代码分支：直接走期货数据获取逻辑
    if _is_futures_code(symbol):
        if frequency in ["1d", "daily"]:
            return _fetch_futures_daily(symbol, start_date, end_date)
        else:
            # TODO: 期货分钟线数据暂未实现，返回空 DataFrame
            warnings.warn(f"期货 {symbol} 的 {frequency} 分钟数据暂未支持")
            return pd.DataFrame()

    ak_sym = _normalize_symbol(symbol)

    is_lof = ak_sym.startswith("16")
    is_etf = (
        ak_sym.startswith("51")
        or ak_sym.startswith("15")
        or ak_sym.startswith("50")
        or ak_sym.startswith("52")
        or ak_sym.startswith("56")
        or ak_sym.startswith("58")
    )
    is_cov = ak_sym.startswith("11") or ak_sym.startswith(
        "12"
    )  # 可转债: 11xxxx.XSHG, 12xxxx.XSHE
    is_index = (
        ak_sym.startswith("000")
        and ak_sym
        in [
            "000001",
            "000002",
            "000003",
            "000004",
            "000005",
            "000006",
            "000007",
            "000008",
            "000009",
            "000010",
            "000011",
            "000012",
            "000013",
            "000014",
            "000015",
            "000016",
            "000017",
            "000018",
            "000300",
            "000688",
            "000851",
            "000852",
            "000903",
            "000905",
            "000906",
            "000978",
        ]
    ) or ak_sym.startswith("399")

    try:
        if frequency in ["1d", "daily"]:
            if is_cov:
                try:
                    import akshare as ak
                except ImportError:
                    raise ImportError("请安装 akshare: pip install akshare")

                try:
                    df = ak.bond_zh_cov_daily(symbol=ak_sym)
                    if df is not None and not df.empty:
                        if start_date:
                            df = df[df["date"] >= start_date]
                        if end_date:
                            df = df[df["date"] <= end_date]
                        df = df.rename(columns={"date": "datetime"})
                        if "close" in df.columns and "money" not in df.columns:
                            df["money"] = df.get("amount", None)
                        return df
                except Exception as cov_err:
                    logger.warning(
                        f"{symbol}: bond_zh_cov_daily 获取失败: {cov_err}，尝试 bond_zh_hs_daily"
                    )

                try:
                    ak_code_for_hs = (
                        "11" + ak_sym[2:]
                        if ak_sym.startswith("11")
                        else "12" + ak_sym[2:]
                    )
                    df = ak.bond_zh_hs_daily(symbol=ak_sym)
                    if df is not None and not df.empty:
                        if start_date:
                            df = df[df["date"] >= start_date]
                        if end_date:
                            df = df[df["date"] <= end_date]
                        df = df.rename(columns={"date": "datetime"})
                        if "close" in df.columns and "money" not in df.columns:
                            df["money"] = df.get("amount", None)
                        return df
                except Exception as hs_err:
                    logger.warning(f"{symbol}: bond_zh_hs_daily 获取失败: {hs_err}")

                return pd.DataFrame()

            if is_index:
                from jk2bt.data.market.index import get_index_daily

                try:
                    df = get_index_daily(
                        ak_sym,
                        start_date or "1990-01-01",
                        end_date or datetime.now().strftime("%Y-%m-%d"),
                    )
                    if df is not None and not df.empty:
                        return df
                except ConnectionError as e:
                    raise NetworkError(
                        "指数行情网络连接失败", context={"symbol": symbol}
                    ) from e
                except Exception as e:
                    raise MarketDataError(
                        "指数行情获取失败", context={"symbol": symbol}
                    ) from e

            if is_lof:
                from jk2bt.data.market.lof import get_lof_daily_with_fallback

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
                from jk2bt.data.market.stock import get_stock_daily

                df = get_stock_daily(
                    ak_code,
                    start_date or "1990-01-01",
                    end_date or datetime.now().strftime("%Y-%m-%d"),
                    adjust=adjust,
                )
                if df is not None and not df.empty:
                    return df
            except Exception as stock_err:
                logger.warning(
                    f"{symbol}: market_data.stock 获取失败: {stock_err}，尝试备用数据源"
                )

            # 备用数据源: akshare（通过 adapter）
            try:
                df = get_adapter().get_stock_hist(
                    symbol=ak_sym,
                    period="daily",
                    start_date=start_date.replace("-", "")
                    if start_date
                    else "19900101",
                    end_date=end_date.replace("-", "")
                    if end_date
                    else datetime.now().strftime("%Y%m%d"),
                    adjust=adjust,
                )
            except Exception:
                try:
                    from .db.parquet_adapter import ParquetAdapter
                except ImportError:
                    from jk2bt.data.storage.parquet_adapter import ParquetAdapter
                db = ParquetAdapter(read_only=True)
                df = db.get_stock_daily(
                    ak_code,
                    start_date or "1990-01-01",
                    end_date or datetime.now().strftime("%Y-%m-%d"),
                    adjust,
                )
                return df

            if df is None or df.empty:
                return pd.DataFrame()
            return df

        elif frequency in ["1m", "5m", "15m", "30m", "60m", "minute"]:
            if is_cov:
                # TODO: akshare 目前没有可转债分钟数据的直接接口
                # 可以考虑使用 bond_zh_cov_daily 的日线数据作为替代
                # 或者使用新浪/腾讯的实时行情接口获取分钟级快照
                warnings.warn(f"{symbol}: 可转债分钟数据暂不支持，返回空数据")
                return pd.DataFrame()

            try:
                from jk2bt.data.market.minute import (
                    get_stock_minute,
                    get_etf_minute,
                )
            except ImportError:
                warnings.warn(f"{symbol}: 分钟数据模块导入失败")
                return pd.DataFrame()

            period_map = {
                "1m": "1m",
                "5m": "5m",
                "15m": "15m",
                "30m": "30m",
                "60m": "60m",
            }
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
                    df = get_lof_min(
                        ak_sym, start_date, end_date, period=period.replace("m", "")
                    )
                elif is_etf:
                    df = get_etf_minute(ak_sym, start_date, end_date, period=period)
                else:
                    df = get_stock_minute(
                        ak_code, start_date, end_date, period=period, adjust=adjust
                    )

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
                raise NetworkError(
                    "分钟数据网络连接失败", context={"symbol": symbol}
                ) from e
            except Exception as minute_error:
                warnings.warn(
                    f"{symbol} ({frequency}) 分钟数据获取失败: {minute_error}"
                )
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
    df["pre_close"] = df["close"].shift(1)
    df["paused"] = 0
    if "volume" in df.columns:
        df.loc[df["volume"] == 0, "paused"] = 1

    # 期货不计算涨跌停价（期货涨跌停规则与股票不同）
    if _is_futures_code(symbol):
        df["high_limit"] = None
        df["low_limit"] = None
        return df

    c = _normalize_symbol(symbol)

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
            "datetime",
            "open",
            "high",
            "low",
            "close",
            "volume",
            "money",
            "paused",
            "pre_close",
            "high_limit",
            "low_limit",
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
                        df.loc[df["paused"] == 1, col] = df.loc[
                            df["paused"] == 1, "pre_close"
                        ]
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
        raw_df = _fetch_price_data(
            security[0], start_date, end_date_str, frequency, adjust
        )

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

        return df_temp[[c for c in keep_cols if c in df_temp.columns]].reset_index(
            drop=True
        )

    else:
        result = {}
        for sym in security:
            result[sym] = get_bars(
                sym, count, unit, fields, include_now, end_dt, fq, skip_paused
            )
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
        df = get_adapter().get_stock_valuation(symbol=ak_sym)

        if df is None or df.empty:
            return pd.DataFrame()

        col_map = {
            "日期": "datetime",
            "pe": "pe",
            "pe_ttm": "pe_ttm",
            "pb": "pb",
            "ps": "ps",
            "dv_ratio": "dividend_ratio",
            "total_mv": "market_cap",
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
        df = get_adapter().get_spot_em()

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


def _fetch_tick_data(
    symbol, count=1000, date=None, start_dt=None, end_dt=None, skip=False
):
    """获取 tick 级数据

    参数
    ----
    symbol : str
        股票代码
    count : int
        获取条数
    date : str
        查询日期（兼容旧接口）
    start_dt : str, optional
        起始日期时间
    end_dt : str, optional
        结束日期时间
    skip : bool
        是否跳过停牌数据

    返回
    ----
    DataFrame
    """
    ak_sym = _normalize_symbol(symbol)

    try:
        if start_dt and end_dt:
            df = get_adapter().get_stock_hist(
                symbol=ak_sym,
                period="1",
                start_date=start_dt,
                end_date=end_dt,
            )
        else:
            try:
                df = get_adapter().get_stock_hist(
                    symbol=ak_sym,
                    period="1",
                    start_date=f"{date or datetime.now().strftime('%Y-%m-%d')} 09:30:00",
                    end_date=f"{date or datetime.now().strftime('%Y-%m-%d')} 15:00:00",
                )
            except Exception:
                prefix = _get_symbol_prefix(symbol)
                today = date or datetime.now().strftime("%Y-%m-%d")
                try:
                    df = get_adapter().get_stock_hist(
                        symbol=f"{prefix}{ak_sym}",
                        period="1",
                        start_date=f"{today} 09:30:00",
                        end_date=f"{today} 15:00:00",
                    )
                except Exception:
                    return pd.DataFrame()

        if df is None or df.empty:
            return pd.DataFrame()

        col_map = {
            "时间": "time",
            "成交时间": "time",
            "datetime": "time",
            "价格": "price",
            "成交价": "price",
            "close": "price",
            "成交量": "volume",
            "成交数量": "volume",
            "vol": "volume",
            "成交额": "amount",
            "amount": "amount",
            "成交金额": "amount",
            "money": "amount",
        }
        df = df.rename(columns={k: v for k, v in col_map.items() if k in df.columns})

        if "time" not in df.columns:
            df["time"] = pd.date_range(start="09:30:00", periods=len(df), freq="1min")

        if "price" not in df.columns and "close" in df.columns:
            df["price"] = df["close"]

        if (
            "amount" not in df.columns
            and "volume" in df.columns
            and "price" in df.columns
        ):
            df["amount"] = df["volume"] * df["price"]

        df["time"] = pd.to_datetime(df["time"], errors="coerce")
        df = df.dropna(subset=["time"])

        if skip:
            df = df[df["volume"] > 0]

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
    valuation_fields = [
        "pe",
        "pe_ttm",
        "pb",
        "ps",
        "market_cap",
        "circulating_market_cap",
        "dividend_ratio",
    ]

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

        df["pre_close"] = df["close"].shift(1).ffill()
        df["high_limit"] = df.apply(
            lambda row: _calculate_limit_price(row["pre_close"], symbol, "up")
            if pd.notna(row["pre_close"])
            else None,
            axis=1,
        )
        df["low_limit"] = df.apply(
            lambda row: _calculate_limit_price(row["pre_close"], symbol, "down")
            if pd.notna(row["pre_close"])
            else None,
            axis=1,
        )

        if need_valuation:
            val_df = _fetch_valuation_data(symbol, end_date)
            if not val_df.empty and "datetime" in val_df.columns:
                df = df.merge(
                    val_df[
                        ["datetime"]
                        + [f for f in valuation_fields if f in val_df.columns]
                    ],
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
                df = _fetch_price_data(
                    symbol, None, datetime.now().strftime("%Y-%m-%d")
                )
                if not df.empty:
                    df = normalize_columns(df, COLUMN_MAP_COMMON)
                    df = normalize_datetime(df)
                    last_row = df.iloc[-1]
                    quote = {
                        "code": symbol,
                        "display_name": "",
                        "last_price": last_row.get("close", 0),
                        "bid_price": None,
                        "ask_price": None,
                        "bid_volume": None,
                        "ask_volume": None,
                        "high_limit": _calculate_limit_price(
                            last_row.get("close", 0), symbol, "up"
                        ),
                        "low_limit": _calculate_limit_price(
                            last_row.get("close", 0), symbol, "down"
                        ),
                        "pre_close": df.iloc[-2].get("close", 0)
                        if len(df) > 1
                        else None,
                        "open": last_row.get("open", 0),
                        "high": last_row.get("high", 0),
                        "low": last_row.get("low", 0),
                        "volume": last_row.get("volume", 0),
                        "money": last_row.get("money", 0),
                        "change_pct": None,
                        "change": None,
                        "turnover_rate": None,
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
                "bid_price": None,
                "ask_price": None,
                "bid_volume": None,
                "ask_volume": None,
                "high_limit": _calculate_limit_price(prev_close, symbol, "up"),
                "low_limit": _calculate_limit_price(prev_close, symbol, "down"),
                "pre_close": prev_close,
                "open": row.get("open", 0),
                "high": row.get("high", 0),
                "low": row.get("low", 0),
                "volume": row.get("volume", 0),
                "money": row.get("money", 0),
                "change_pct": (row.get("close", 0) - prev_close) / prev_close * 100
                if prev_close
                else None,
                "change": row.get("close", 0) - prev_close if prev_close else None,
                "turnover_rate": None,
            }

        result[symbol] = quote

    if len(result) == 1:
        return result[security[0]]

    return result


def _is_options_code(symbol):
    """判断是否为期权代码"""
    sym = symbol.upper()
    # 聚宽期权格式: 1000xxxx.XSHG, 1000xxxx.XSHE
    if sym.endswith(".XSHG") or sym.endswith(".XSHE"):
        code = sym.split(".")[0]
        if code.startswith("1000") or code.startswith("1001"):
            return True
    # 其他期权代码模式
    if any(kw in sym for kw in ["购", "沽", "CALL", "PUT", "C", "P"]):
        return True
    return False


def _is_index_code(symbol):
    """判断是否为指数代码"""
    sym_upper = symbol.upper()
    # 处理带交易所后缀的代码: 000xxx.XSHG, 880xxx.XSHG, 399xxx.XSHE
    if sym_upper.endswith(".XSHG") or sym_upper.endswith(".XSHE"):
        code = sym_upper.split(".")[0]
        if code.startswith("000") or code.startswith("880") or code.startswith("399"):
            return True

    ak_sym = _normalize_symbol(symbol)
    # 上证指数 000xxx, 深证指数 399xxx, 中证指数 880xxx
    if ak_sym.startswith("000") or ak_sym.startswith("399") or ak_sym.startswith("880"):
        return True
    # 常见指数代码
    known_indexes = [
        "000001",
        "000016",
        "000300",
        "000688",
        "000851",
        "000852",
        "000903",
        "000905",
        "000906",
        "000978",
        "399001",
        "399005",
        "399006",
        "399106",
        "399300",
    ]
    if ak_sym in known_indexes:
        return True
    return False


def _is_fund_code(symbol):
    """判断是否为基金代码（ETF/LOF/封闭式基金）"""
    ak_sym = _normalize_symbol(symbol)
    # ETF: 51xxxx, 52xxxx, 56xxxx, 58xxxx, 159xxx
    # LOF: 16xxxx
    # 封闭式基金: 18xxxx, 15xxxx
    if (
        ak_sym.startswith("51")
        or ak_sym.startswith("52")
        or ak_sym.startswith("56")
        or ak_sym.startswith("58")
        or ak_sym.startswith("159")
        or ak_sym.startswith("16")
        or ak_sym.startswith("18")
        or ak_sym.startswith("15")
    ):
        return True
    return False


def _fetch_futures_tick(symbol, count=1000, date=None):
    """获取期货 tick 数据（分钟级）"""
    try:
        import akshare as ak
    except ImportError:
        warnings.warn("请安装 akshare: pip install akshare")
        return pd.DataFrame()

    try:
        sina_symbol = _jq_futures_to_sina(symbol)
        df = ak.futures_zh_minute_sina(symbol=sina_symbol, period="1")
        if df is None or df.empty:
            warnings.warn(f"期货 {symbol} 分钟数据为空")
            return pd.DataFrame()

        col_map = {
            "date": "time",
            "datetime": "time",
            "open": "price",
            "close": "price",
            "volume": "volume",
            "hold": "amount",
        }
        df = df.rename(columns={k: v for k, v in col_map.items() if k in df.columns})

        if "time" not in df.columns and (
            "date" in df.columns or "datetime" in df.columns
        ):
            time_col = "datetime" if "datetime" in df.columns else "date"
            df["time"] = pd.to_datetime(df[time_col])

        if "price" not in df.columns:
            df["price"] = df.get("close", df.get("open", 0))

        if (
            "amount" not in df.columns
            and "volume" in df.columns
            and "price" in df.columns
        ):
            df["amount"] = df["volume"] * df["price"]

        df["time"] = pd.to_datetime(df["time"], errors="coerce")
        df = df.dropna(subset=["time"]).sort_values("time").reset_index(drop=True)

        if count and len(df) > count:
            df = df.tail(count)

        return df
    except Exception as e:
        warnings.warn(f"期货 {symbol} tick 数据获取失败: {e}")
        return pd.DataFrame()


def _fetch_options_tick(symbol, count=1000, date=None):
    """获取期权 tick 数据（实时行情快照）"""
    try:
        import akshare as ak
    except ImportError:
        warnings.warn("请安装 akshare: pip install akshare")
        return pd.DataFrame()

    try:
        # 上交所期权实时行情
        df = ak.option_sina_sse_spot()
        if df is None or df.empty:
            warnings.warn(f"期权 {symbol} 实时行情数据为空")
            return pd.DataFrame()

        ak_sym = _normalize_symbol(symbol)
        row = df[df["代码"] == ak_sym] if "代码" in df.columns else pd.DataFrame()
        if row.empty:
            warnings.warn(f"期权 {symbol} 未找到匹配数据")
            return pd.DataFrame()

        row = row.iloc[0]
        tick_data = {
            "time": [pd.Timestamp.now()],
            "price": [row.get("最新价", row.get("现价", 0))],
            "volume": [row.get("成交量", 0)],
            "amount": [row.get("成交额", 0)],
        }
        return pd.DataFrame(tick_data)
    except Exception as e:
        warnings.warn(f"期权 {symbol} tick 数据获取失败: {e}")
        return pd.DataFrame()


def _fetch_index_tick(symbol, count=1000, date=None):
    """获取指数 tick 数据（指数分钟级数据作为 tick 近似）"""
    try:
        import akshare as ak
    except ImportError:
        warnings.warn("请安装 akshare: pip install akshare")
        return pd.DataFrame()

    try:
        ak_sym = _normalize_symbol(symbol)
        # 构建 akshare 指数代码格式
        if ak_sym.startswith("000") or ak_sym.startswith("880"):
            full_code = f"sh{ak_sym}"
        elif ak_sym.startswith("399"):
            full_code = f"sz{ak_sym}"
        else:
            full_code = ak_sym

        # 使用指数分钟数据接口
        target_date = date or datetime.now().strftime("%Y-%m-%d")
        df = ak.stock_zh_index_hist_min_em(
            symbol=full_code,
            period="1",
            start_date=f"{target_date} 09:30:00",
            end_date=f"{target_date} 15:00:00",
        )
        if df is None or df.empty:
            return pd.DataFrame()

        col_map = {
            "时间": "time",
            "datetime": "time",
            "date": "time",
            "开盘": "price",
            "open": "price",
            "收盘": "price",
            "close": "price",
            "成交量": "volume",
            "volume": "volume",
            "成交额": "amount",
            "amount": "amount",
        }
        df = df.rename(columns={k: v for k, v in col_map.items() if k in df.columns})

        if "time" not in df.columns:
            time_col = None
            for col in df.columns:
                if (
                    "时间" in str(col)
                    or "time" in str(col).lower()
                    or "date" in str(col).lower()
                ):
                    time_col = col
                    break
            if time_col:
                df["time"] = pd.to_datetime(df[time_col])

        if "price" not in df.columns:
            df["price"] = df.get("close", df.get("open", 0))

        if (
            "amount" not in df.columns
            and "volume" in df.columns
            and "price" in df.columns
        ):
            df["amount"] = df["volume"] * df["price"]

        df["time"] = pd.to_datetime(df["time"], errors="coerce")
        df = df.dropna(subset=["time"]).sort_values("time").reset_index(drop=True)

        if count and len(df) > count:
            df = df.tail(count)

        return df
    except Exception as e:
        warnings.warn(f"指数 {symbol} tick/分钟数据获取失败: {e}")
        return pd.DataFrame()


def _fetch_fund_tick(symbol, count=1000, date=None):
    """获取基金 tick 数据（ETF/LOF 分钟级数据）"""
    try:
        import akshare as ak
    except ImportError:
        warnings.warn("请安装 akshare: pip install akshare")
        return pd.DataFrame()

    try:
        ak_sym = _normalize_symbol(symbol)
        prefix = "sh" if ak_sym.startswith(("51", "52", "56", "58")) else "sz"
        full_code = f"{prefix}{ak_sym}"

        target_date = date or datetime.now().strftime("%Y-%m-%d")

        # 尝试使用基金 ETF 分钟数据
        try:
            df = ak.fund_etf_hist_min_em(
                symbol=full_code,
                period="1",
                start_date=f"{target_date} 09:30:00",
                end_date=f"{target_date} 15:00:00",
            )
        except Exception:
            # 备用: 使用 sina 接口
            df = ak.fund_etf_hist_sina(symbol=full_code)

        if df is None or df.empty:
            return pd.DataFrame()

        col_map = {
            "时间": "time",
            "datetime": "time",
            "date": "time",
            "开盘": "price",
            "open": "price",
            "收盘": "price",
            "close": "price",
            "成交量": "volume",
            "volume": "volume",
            "成交额": "amount",
            "amount": "amount",
        }
        df = df.rename(columns={k: v for k, v in col_map.items() if k in df.columns})

        if "time" not in df.columns:
            time_col = None
            for col in df.columns:
                if (
                    "时间" in str(col)
                    or "time" in str(col).lower()
                    or "date" in str(col).lower()
                ):
                    time_col = col
                    break
            if time_col:
                df["time"] = pd.to_datetime(df[time_col])

        if "price" not in df.columns:
            df["price"] = df.get("close", df.get("open", 0))

        if (
            "amount" not in df.columns
            and "volume" in df.columns
            and "price" in df.columns
        ):
            df["amount"] = df["volume"] * df["price"]

        df["time"] = pd.to_datetime(df["time"], errors="coerce")
        df = df.dropna(subset=["time"]).sort_values("time").reset_index(drop=True)

        if count and len(df) > count:
            df = df.tail(count)

        return df
    except Exception as e:
        warnings.warn(f"基金 {symbol} tick 数据获取失败: {e}")
        return pd.DataFrame()


def get_ticks(
    security, start_dt=None, end_dt=None, count=1000, fields=None, df=True, skip=False
):
    """获取 tick 级数据（聚宽风格）"""
    if fields is None:
        fields = ["time", "price", "volume", "amount"]

    if isinstance(security, str):
        security = [security]

    result = {}

    for symbol in security:
        ak_sym = _normalize_symbol(symbol)
        is_cov = ak_sym.startswith("11") or ak_sym.startswith("12")

        if is_cov:
            # TODO: akshare 目前没有可转债 tick 数据的直接接口
            # bond_zh_cov_daily 只提供日线数据
            # 如需可转债 tick 数据，可考虑使用实时行情接口或第三方数据源
            warnings.warn(f"{symbol}: 可转债 tick 数据暂不支持，返回空结果")
            result[symbol] = pd.DataFrame() if df else []
            continue

        # 期货 tick 数据
        if _is_futures_code(symbol):
            tick_df = _fetch_futures_tick(symbol, count=count, date=start_dt or end_dt)
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
                            item[f] = (
                                val.strftime("%Y-%m-%d %H:%M:%S")
                                if isinstance(val, pd.Timestamp)
                                else val
                            )
                    tick_list.append(item)
                result[symbol] = tick_list
            continue

        # 期权 tick 数据
        if _is_options_code(symbol):
            tick_df = _fetch_options_tick(symbol, count=count, date=start_dt or end_dt)
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
                            item[f] = (
                                val.strftime("%Y-%m-%d %H:%M:%S")
                                if isinstance(val, pd.Timestamp)
                                else val
                            )
                    tick_list.append(item)
                result[symbol] = tick_list
            continue

        # 指数 tick 数据（指数无 tick 数据）
        if _is_index_code(symbol):
            tick_df = _fetch_index_tick(symbol, count=count, date=start_dt or end_dt)
            result[symbol] = pd.DataFrame() if df else []
            continue

        # 基金 tick 数据（ETF/LOF）
        if _is_fund_code(symbol):
            tick_df = _fetch_fund_tick(symbol, count=count, date=start_dt or end_dt)
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
                            item[f] = (
                                val.strftime("%Y-%m-%d %H:%M:%S")
                                if isinstance(val, pd.Timestamp)
                                else val
                            )
                    tick_list.append(item)
                result[symbol] = tick_list
            continue

        # 股票 tick 数据（原有逻辑）
        tick_df = _fetch_tick_data(
            symbol, count=count, start_dt=start_dt, end_dt=end_dt, skip=skip
        )

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
                        item[f] = (
                            val.strftime("%Y-%m-%d %H:%M:%S")
                            if isinstance(val, pd.Timestamp)
                            else val
                        )
                tick_list.append(item)
            result[symbol] = tick_list

    if len(result) == 1:
        return result[security[0]]

    return result


# ---------------------------------------------------------------------------
# 来自 enhancements.py 的行情辅助函数
# ---------------------------------------------------------------------------


def get_call_auction(security, date=None):
    """获取集合竞价数据（聚宽风格）

    Args:
        security: 证券代码或代码列表
        date: 指定日期（暂未使用）

    Returns:
        dict: 以证券代码为键，DataFrame 为值的字典

    Note:
        - ETF/LOF: 使用 akshare fund_etf_spot_em 获取
        - 股票: akshare 暂无股票集合竞价 tick 数据接口
        - 指数: 免费数据源通常不提供指数集合竞价 tick 数据
    """
    if isinstance(security, str):
        security = [security]

    result = {}

    for symbol in security:
        ak_sym = _normalize_symbol(symbol)
        is_cov = ak_sym.startswith("11") or ak_sym.startswith("12")

        if is_cov:
            # TODO: akshare 目前没有可转债集合竞价数据的直接接口
            # 可转债的集合竞价数据通常包含在 tick 数据中
            # 如需可转债集合竞价数据，可考虑使用实时行情接口或第三方数据源
            warnings.warn(f"{symbol}: 可转债集合竞价数据暂不支持，返回空结果")
            result[symbol] = pd.DataFrame()
            continue

        # ETF/LOF 集合竞价数据
        if _is_fund_code(symbol):
            try:
                import akshare as ak
            except ImportError:
                warnings.warn("请安装 akshare: pip install akshare")
                result[symbol] = pd.DataFrame()
                continue

            try:
                # ETF 实时行情包含集合竞价阶段数据
                prefix = "sh" if ak_sym.startswith(("51", "52", "56", "58")) else "sz"
                full_code = f"{prefix}{ak_sym}"

                # 使用 fund_etf_spot_em 获取 ETF 实时行情（含集合竞价）
                df = ak.fund_etf_spot_em()
                if df is not None and not df.empty:
                    code_col = "代码" if "代码" in df.columns else "symbol"
                    row = (
                        df[df[code_col] == ak_sym]
                        if code_col in df.columns
                        else pd.DataFrame()
                    )
                    if not row.empty:
                        row = row.iloc[0]
                        auction_data = {
                            "code": [symbol],
                            "time": [pd.Timestamp.now()],
                            "open": [row.get("今开", row.get("open", None))],
                            "high": [row.get("最高", row.get("high", None))],
                            "low": [row.get("最低", row.get("low", None))],
                            "close": [row.get("最新价", row.get("close", None))],
                            "volume": [row.get("成交量", row.get("volume", 0))],
                            "amount": [row.get("成交额", row.get("amount", 0))],
                            "pre_close": [row.get("昨收", row.get("pre_close", None))],
                        }
                        result[symbol] = pd.DataFrame(auction_data)
                        continue

                warnings.warn(f"{symbol}: ETF/LOF 集合竞价数据为空")
                result[symbol] = pd.DataFrame()
                continue
            except Exception as e:
                warnings.warn(f"{symbol}: ETF/LOF 集合竞价数据获取失败: {e}")
                result[symbol] = pd.DataFrame()
                continue

        # 判断是否为指数
        if _is_index_code(symbol):
            raise NotImplementedError(
                "指数集合竞价tick数据需要专业数据源。请替换为其他数据源（如Tushare/Wind）。"
            )

        # 股票集合竞价数据
        # akshare 目前没有专门的股票集合竞价 tick 数据接口
        # 集合竞价数据通常包含在 tick 数据的前几分钟（9:15-9:25）
        try:
            import akshare as ak

            # 尝试获取盘前数据
            premarket_df = ak.stock_zh_a_premarket_em()
            if premarket_df is not None and not premarket_df.empty:
                code_col = None
                for c in ["代码", "symbol", "code"]:
                    if c in premarket_df.columns:
                        code_col = c
                        break
                if code_col:
                    row = premarket_df[premarket_df[code_col] == ak_sym]
                    if not row.empty:
                        row = row.iloc[0]
                        auction_data = {
                            "code": [symbol],
                            "time": [pd.Timestamp.now()],
                            "bid_price": [row.get("买一价", None)],
                            "ask_price": [row.get("卖一价", None)],
                            "bid_volume": [row.get("买一量", None)],
                            "ask_volume": [row.get("卖一量", None)],
                        }
                        result[symbol] = pd.DataFrame(auction_data)
                        continue
        except Exception:
            pass

        raise NotImplementedError(
            "股票集合竞价tick数据需要专业数据源。当前akshare仅提供ETF/LOF集合竞价。请替换为其他数据源。"
        )

    if len(result) == 1:
        return result[security[0]]

    return result


def _get_current_field(security, field):
    """从 get_current_data 中读取指定字段"""
    from jk2bt.api.jq_compat import get_current_data

    return getattr(get_current_data()[security], field)


def get_open_price(security, date=None):
    """获取开盘价"""
    return _get_current_field(security, "day_open")


def get_close_price(security, date=None):
    """获取收盘价（最新价）"""
    return _get_current_field(security, "last_price")


def get_high_limit(security):
    """获取涨停价"""
    return _get_current_field(security, "high_limit")


def get_low_limit(security):
    """获取跌停价"""
    return _get_current_field(security, "low_limit")


def get_preopen_infos(
    security,
    fields=(
        "paused",
        "factor",
        "high_limit",
        "low_limit",
        "pre_close",
        "open",
        "change_pct",
    ),
):
    """
    获取股票当日盘前交易信息（停牌标志、后复权因子、涨停价、跌停价等）

    参数:
        security: 股票代码或代码列表
        fields: 要获取的字段，默认为 ("paused", "factor", "high_limit", "low_limit", "pre_close", "open", "change_pct")
            扩展支持: volume, money, turnover_rate

    返回:
        DataFrame: index 为股票代码，columns 为请求的字段
            - paused: 是否停牌 (0/1)
            - factor: 后复权因子
            - high_limit: 涨停价
            - low_limit: 跌停价
            - pre_close: 昨收价
            - open: 开盘价
            - change_pct: 涨跌幅(%)
            - volume: 成交量
            - money: 成交额
            - turnover_rate: 换手率(%)

    示例:
        >>> get_preopen_infos("600519")
                    paused  factor  high_limit  low_limit  pre_close  open  change_pct
        600519        0    1.234    1850.00    1510.00    1680.00  1690.00    0.60
    """
    try:
        import akshare as ak
    except ImportError:
        warnings.warn("请安装 akshare: pip install akshare")
        return pd.DataFrame(columns=list(fields))

    if isinstance(security, str):
        security = [security]

    result_df = pd.DataFrame(index=security, columns=list(fields))
    result_df.index.name = "code"

    try:
        df = ak.stock_zh_a_premarket_em()
        if df is None or df.empty:
            warnings.warn("stock_zh_a_premarket_em 返回空数据")
            return result_df

        code_col = None
        for col in ["代码", "code", "股票代码"]:
            if col in df.columns:
                code_col = col
                break

        if code_col is None:
            warnings.warn("stock_zh_a_premarket_em 返回数据中没有代码列")
            return result_df

        for sec in security:
            ak_code = sec.replace(".XSHG", "").replace(".XSHE", "").zfill(6)
            row = df[df[code_col] == ak_code]
            if not row.empty:
                row = row.iloc[0]
                if "paused" in fields:
                    result_df.loc[sec, "paused"] = 0
                if "factor" in fields:
                    result_df.loc[sec, "factor"] = 1.0
                if "high_limit" in fields:
                    for hl_col in ["涨停价", "high_limit", "涨停价格"]:
                        if hl_col in row.index:
                            result_df.loc[sec, "high_limit"] = row[hl_col]
                            break
                if "low_limit" in fields:
                    for ll_col in ["跌停价", "low_limit", "跌停价格"]:
                        if ll_col in row.index:
                            result_df.loc[sec, "low_limit"] = row[ll_col]
                            break
                if "pre_close" in fields:
                    for pc_col in ["昨收", "pre_close", "昨日收盘价"]:
                        if pc_col in row.index:
                            result_df.loc[sec, "pre_close"] = row[pc_col]
                            break
                if "open" in fields:
                    for op_col in ["今开", "open", "开盘价"]:
                        if op_col in row.index:
                            result_df.loc[sec, "open"] = row[op_col]
                            break
                if "change_pct" in fields:
                    for cp_col in ["涨跌幅", "change_pct"]:
                        if cp_col in row.index:
                            result_df.loc[sec, "change_pct"] = row[cp_col]
                            break
                if "volume" in fields:
                    for vol_col in ["成交量", "volume"]:
                        if vol_col in row.index:
                            result_df.loc[sec, "volume"] = row[vol_col]
                            break
                if "money" in fields:
                    for money_col in ["成交额", "money"]:
                        if money_col in row.index:
                            result_df.loc[sec, "money"] = row[money_col]
                            break
                if "turnover_rate" in fields:
                    for tr_col in ["换手率", "turnover_rate"]:
                        if tr_col in row.index:
                            result_df.loc[sec, "turnover_rate"] = row[tr_col]
                            break
    except Exception as e:
        warnings.warn(f"get_preopen_infos 获取失败: {e}")

    for col in fields:
        if col in result_df.columns:
            result_df[col] = pd.to_numeric(result_df[col], errors="coerce")

    return result_df


_SUPPORTED_STYLE_EXPOSURE_INDEXES = [
    "000300.XSHG",
    "000905.XSHG",
    "000906.XSHG",
    "000852.XSHG",
    "000985.XSHG",
]

_DEFAULT_STYLE_FACTORS = [
    "size",
    "book_to_market",
    "momentum",
    "volatility",
    "liquidity",
    "beta",
    "growth",
    "profitability",
    "leverage",
]


def get_index_style_exposure(
    index,
    factors=None,
    start_date=None,
    end_date=None,
    count=None,
):
    """
    获取重点宽基指数的风格暴露

    参数:
        index: 指数代码，支持 '000300.XSHG', '000905.XSHG', '000906.XSHG', '000852.XSHG', '000985.XSHG'
        factors: 风格因子列表，默认 ['size', 'book_to_market', 'momentum', 'volatility', 'liquidity',
                         'beta', 'growth', 'profitability', 'leverage']
        start_date: 开始日期
        end_date: 结束日期
        count: 数据条数

    返回:
        DataFrame: index=因子名称, columns=['exposure', 'change'] 或时间序列

    示例:
        >>> df = get_index_style_exposure('000300.XSHG')
        >>> df = get_index_style_exposure('000300.XSHG', factors=['size', 'book_to_market'])
    """
    if index not in _SUPPORTED_STYLE_EXPOSURE_INDEXES:
        warnings.warn(
            f"get_index_style_exposure: 不支持的指数 {index}，"
            f"支持的指数: {_SUPPORTED_STYLE_EXPOSURE_INDEXES}"
        )
        return pd.DataFrame(columns=["exposure", "change"])

    if factors is None:
        factors = _DEFAULT_STYLE_FACTORS

    if isinstance(factors, str):
        factors = [factors]

    try:
        from jk2bt.api.factor_kanban import get_factor_style_returns

        style_df = get_factor_style_returns(
            factors=factors,
            start_date=start_date,
            end_date=end_date,
            count=count,
            universe=index,
        )

        if style_df is not None and not style_df.empty:
            result = {}
            for factor in factors:
                if factor in style_df.columns:
                    series = style_df[factor]
                    exposure = float(series.mean()) if not series.empty else 0.0
                    if len(series) >= 2:
                        change = float(series.iloc[-1] - series.iloc[-2])
                    else:
                        change = 0.0
                    result[factor] = {
                        "exposure": round(exposure, 6),
                        "change": round(change, 6),
                    }
                else:
                    result[factor] = {"exposure": None, "change": None}

            df = pd.DataFrame(result).T
            df.index.name = "factor"
            return df
    except Exception as e:
        warnings.warn(f"get_index_style_exposure 计算失败，使用静态数据: {e}")

    index_abbr = {
        "000300.XSHG": "HS300",
        "000905.XSHG": "CSI500",
        "000906.XSHG": "CSI800",
        "000852.XSHG": "CSI1000",
        "000985.XSHG": "CSIALL",
    }.get(index, index)

    base_exposure = {
        "000300.XSHG": {
            "size": 0.85,
            "book_to_market": 0.45,
            "momentum": 0.52,
            "volatility": 0.38,
            "liquidity": 0.72,
            "beta": 1.0,
            "growth": 0.55,
            "profitability": 0.68,
            "leverage": 0.42,
        },
        "000905.XSHG": {
            "size": -0.65,
            "book_to_market": 0.58,
            "momentum": 0.48,
            "volatility": 0.55,
            "liquidity": 0.45,
            "beta": 0.92,
            "growth": 0.62,
            "profitability": 0.55,
            "leverage": 0.48,
        },
        "000906.XSHG": {
            "size": 0.15,
            "book_to_market": 0.52,
            "momentum": 0.50,
            "volatility": 0.45,
            "liquidity": 0.60,
            "beta": 0.96,
            "growth": 0.58,
            "profitability": 0.60,
            "leverage": 0.45,
        },
        "000852.XSHG": {
            "size": -0.85,
            "book_to_market": 0.62,
            "momentum": 0.45,
            "volatility": 0.58,
            "liquidity": 0.38,
            "beta": 0.88,
            "growth": 0.65,
            "profitability": 0.50,
            "leverage": 0.52,
        },
        "000985.XSHG": {
            "size": 0.0,
            "book_to_market": 0.50,
            "momentum": 0.50,
            "volatility": 0.50,
            "liquidity": 0.50,
            "beta": 1.0,
            "growth": 0.50,
            "profitability": 0.50,
            "leverage": 0.50,
        },
    }

    exposure_data = base_exposure.get(index, {})

    result = {}
    for factor in factors:
        if factor in exposure_data:
            result[factor] = {
                "exposure": exposure_data[factor],
                "change": 0.0,
            }
        else:
            warnings.warn(f"get_index_style_exposure: 未知因子 {factor}")
            result[factor] = {"exposure": None, "change": None}

    df = pd.DataFrame(result).T
    df.index.name = "factor"

    return df


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
    "get_ticks",
    # 集合竞价
    "get_call_auction",
    # 来自 enhancements.py（行情辅助）
    "get_open_price",
    "get_close_price",
    "get_high_limit",
    "get_low_limit",
    # 盘前交易信息
    "get_preopen_infos",
    # 风格暴露
    "get_index_style_exposure",
]
