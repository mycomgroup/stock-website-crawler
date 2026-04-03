"""
factors/technical.py
技术因子模块。

实现：
- bias_5 / bias_10 / bias_60   乖离率
- emac_10 / emac_20 / emac_26 / emac_60  指数平均线
- roc_6 / roc_120               动量
- mac_60 / mac_120              简单移动平均
- vol_20 / vol_240              成交量均值
- vstd_20                       成交量标准差
- vroc_6                        成交量动量
- cci_10                        顺势指标
- money_flow_20                 资金流
- average_share_turnover_annual 年均换手率
- share_turnover_monthly        月均换手率

数据来源：AkShare stock_zh_a_hist 接口（日线行情，含换手率）
"""

import warnings
from typing import Optional, Union, Dict
import pandas as pd
import numpy as np

from .base import (
    global_factor_registry,
    safe_divide,
    load_factor_cache,
    save_factor_cache,
)

try:
    from ..utils.date_utils import find_date_column
except ImportError:
    from utils.date_utils import find_date_column

try:
    from .data_sources import (
        TurnoverDataSource,
        validate_turnover_data,
        retry_on_failure,
    )

    _TURNOVER_SOURCE_AVAILABLE = True
except ImportError:
    _TURNOVER_SOURCE_AVAILABLE = False
    warnings.warn("无法导入 data_sources 模块，换手率将使用简化计算")


# =====================================================================
# 数据获取函数
# =====================================================================


def _get_daily_ohlcv(
    symbol: str,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    cache_dir: str = "stock_cache",
    force_update: bool = False,
    count: Optional[int] = None,
) -> pd.DataFrame:
    """
    获取日线 OHLCV 数据。

    数据源优先级：
    1. market_data.stock.get_stock_daily（DuckDB 缓存 + 多数据源备份）
    2. akshare.stock_zh_a_hist（直接获取）

    Parameters
    ----------
    symbol : str
        证券代码，如 'sh600519'
    start_date : str, optional
        起始日期
    end_date : str, optional
        截止日期
    cache_dir : str
        缓存目录（仅用于 akshare fallback）
    force_update : bool
        强制更新
    count : int, optional
        需要的交易日数量（用于估算起始日期）

    Returns
    -------
    pd.DataFrame
        包含 date, open, high, low, close, volume, money 列
    """
    import os

    # 标准化代码格式
    ak_sym = symbol
    if symbol.startswith("sh") or symbol.startswith("sz"):
        ak_sym = symbol[2:]
    if symbol.endswith(".XSHG") or symbol.endswith(".XSHE"):
        ak_sym = symbol[:6]
    ak_sym = ak_sym.zfill(6)

    # 估算起始日期（如果只提供了 count）
    if count is not None and count > 0 and start_date is None and end_date is not None:
        # 简单估算：每个交易日大约对应 1.5 个自然日
        start_date = pd.Timestamp(end_date) - pd.Timedelta(days=int(count * 1.5))
        start_date = start_date.strftime("%Y-%m-%d")

    # 优先尝试使用 market_data 模块
    try:
        from ..market_data.stock import get_stock_daily

        if start_date and end_date:
            df = get_stock_daily(
                symbol=symbol,
                start=start_date,
                end=end_date,
                force_update=force_update,
                adjust="qfq",
                offline_mode=False,
            )

            # market_data 返回的数据已经是标准化的格式
            if df is not None and not df.empty:
                # 转换 datetime 列为 date 字符串格式（保持与原有代码兼容）
                df = df.copy()
                if "datetime" in df.columns:
                    df["date"] = pd.to_datetime(df["datetime"]).dt.strftime("%Y-%m-%d")
                elif "date" not in df.columns:
                    df["date"] = pd.NaT

                # 确保有 turnover_rate 列（market_data 可能不包含）
                if "turnover_rate" not in df.columns:
                    # 换手率需要额外获取，暂用 NaN
                    df["turnover_rate"] = np.nan

                # 标准化列名
                col_map = {
                    "amount": "money",
                }
                for old, new in col_map.items():
                    if old in df.columns and new not in df.columns:
                        df[new] = df[old]

                keep_cols = [
                    "date",
                    "open",
                    "high",
                    "low",
                    "close",
                    "volume",
                    "money",
                    "turnover_rate",
                ]
                keep_cols = [c for c in keep_cols if c in df.columns]

                df = df[keep_cols].sort_values("date").reset_index(drop=True)

                if count is not None and count > 0:
                    df = df.tail(count)

                return df
    except ImportError:
        pass  # market_data 模块不可用，fallback 到 akshare
    except Exception as e:
        warnings.warn(f"market_data 模块获取数据失败 {symbol}: {e}，fallback 到 akshare")

    # Fallback: 使用 akshare 直接获取
    try:
        import akshare as ak
    except ImportError:
        raise ImportError("请安装 akshare: pip install akshare")

    cache_file = os.path.join(cache_dir, f"{symbol}_daily.pkl")
    os.makedirs(cache_dir, exist_ok=True)

    need_dl = force_update or not os.path.exists(cache_file)

    if not need_dl:
        try:
            df = pd.read_pickle(cache_file)
        except Exception:
            need_dl = True

    if need_dl:
        try:
            df = ak.stock_zh_a_hist(symbol=ak_sym, period="daily", adjust="qfq")
            if df is not None and not df.empty:
                df.to_pickle(cache_file)
            else:
                return pd.DataFrame()
        except Exception as e:
            warnings.warn(f"获取日线数据失败 {symbol}: {e}")
            return pd.DataFrame()

    if df is None or df.empty:
        return pd.DataFrame()

    # 标准化字段
    df = df.copy()
    date_col = find_date_column(df, "market")
    if date_col:
        df["date"] = pd.to_datetime(df[date_col]).dt.strftime("%Y-%m-%d")
    else:
        return pd.DataFrame()

    col_map = {
        "开盘": "open",
        "最高": "high",
        "最低": "low",
        "收盘": "close",
        "成交量": "volume",
        "成交额": "money",
        "换手率": "turnover_rate_raw",
    }
    for old, new in col_map.items():
        if old in df.columns:
            df[new] = df[old]

    # 换手率数据处理：AkShare返回的换手率是百分比（如 2.5 表示 2.5%）
    if "turnover_rate_raw" in df.columns:
        df["turnover_rate"] = df["turnover_rate_raw"] / 100

    keep_cols = [
        "date",
        "open",
        "high",
        "low",
        "close",
        "volume",
        "money",
        "turnover_rate",
    ]
    keep_cols = [c for c in keep_cols if c in df.columns]

    df = df[keep_cols].sort_values("date").reset_index(drop=True)

    # 日期过滤
    if end_date:
        df = df[df["date"] <= end_date]
    if start_date:
        df = df[df["date"] >= start_date]
    if count is not None and count > 0:
        df = df.tail(count)

    return df


# =====================================================================
# 技术因子计算函数
# =====================================================================


def _compute_ma(series: pd.Series, window: int) -> pd.Series:
    """简单移动平均。"""
    return series.rolling(window=window, min_periods=window).mean()


def _compute_ema(series: pd.Series, window: int) -> pd.Series:
    """指数移动平均。"""
    return series.ewm(span=window, adjust=False).mean()


def _compute_std(series: pd.Series, window: int) -> pd.Series:
    """滚动标准差。"""
    return series.rolling(window=window, min_periods=window).std()


# -----------------------------------------------------------------
# BIAS（乖离率）
# -----------------------------------------------------------------


def compute_bias(
    symbol: str,
    window: int,
    end_date: Optional[str] = None,
    count: Optional[int] = None,
    cache_dir: str = "stock_cache",
    force_update: bool = False,
    **kwargs,
) -> Union[float, pd.Series]:
    """
    计算 BIAS（乖离率）因子。

    公式：(close - MA(close, window)) / MA(close, window)
    """
    need_count = count + window if count else window + 10
    df = _get_daily_ohlcv(
        symbol,
        end_date=end_date,
        cache_dir=cache_dir,
        force_update=force_update,
        count=need_count,
    )

    if df.empty or "close" not in df.columns:
        return np.nan

    df = df.set_index("date")
    close = df["close"].astype(float)

    ma = _compute_ma(close, window)
    bias = safe_divide(close - ma, ma)

    if count is not None and count > 0:
        bias = bias.tail(count)

    if len(bias) == 1:
        return float(bias.iloc[-1])
    return bias


def compute_bias_5(
    symbol,
    end_date=None,
    count=None,
    cache_dir="stock_cache",
    force_update=False,
    **kwargs,
):
    return compute_bias(
        symbol,
        window=5,
        end_date=end_date,
        count=count,
        cache_dir=cache_dir,
        force_update=force_update,
    )


def compute_bias_10(
    symbol,
    end_date=None,
    count=None,
    cache_dir="stock_cache",
    force_update=False,
    **kwargs,
):
    return compute_bias(
        symbol,
        window=10,
        end_date=end_date,
        count=count,
        cache_dir=cache_dir,
        force_update=force_update,
    )


def compute_bias_20(
    symbol,
    end_date=None,
    count=None,
    cache_dir="stock_cache",
    force_update=False,
    **kwargs,
):
    return compute_bias(
        symbol,
        window=20,
        end_date=end_date,
        count=count,
        cache_dir=cache_dir,
        force_update=force_update,
    )


def compute_bias_60(
    symbol,
    end_date=None,
    count=None,
    cache_dir="stock_cache",
    force_update=False,
    **kwargs,
):
    return compute_bias(
        symbol,
        window=60,
        end_date=end_date,
        count=count,
        cache_dir=cache_dir,
        force_update=force_update,
    )


# -----------------------------------------------------------------
# EMAC（指数平均线）
# -----------------------------------------------------------------


def compute_emac(
    symbol: str,
    window: int,
    end_date: Optional[str] = None,
    count: Optional[int] = None,
    cache_dir: str = "stock_cache",
    force_update: bool = False,
    **kwargs,
) -> Union[float, pd.Series]:
    """
    计算 EMAC（指数平均线）因子。

    公式：EMA(close, window)
    """
    need_count = count + window if count else window + 10
    df = _get_daily_ohlcv(
        symbol,
        end_date=end_date,
        cache_dir=cache_dir,
        force_update=force_update,
        count=need_count,
    )

    if df.empty or "close" not in df.columns:
        return np.nan

    df = df.set_index("date")
    close = df["close"].astype(float)

    ema = _compute_ema(close, window)

    if count is not None and count > 0:
        ema = ema.tail(count)

    if len(ema) == 1:
        return float(ema.iloc[-1])
    return ema


def compute_emac_10(
    symbol,
    end_date=None,
    count=None,
    cache_dir="stock_cache",
    force_update=False,
    **kwargs,
):
    return compute_emac(
        symbol,
        window=10,
        end_date=end_date,
        count=count,
        cache_dir=cache_dir,
        force_update=force_update,
    )


def compute_emac_20(
    symbol,
    end_date=None,
    count=None,
    cache_dir="stock_cache",
    force_update=False,
    **kwargs,
):
    return compute_emac(
        symbol,
        window=20,
        end_date=end_date,
        count=count,
        cache_dir=cache_dir,
        force_update=force_update,
    )


def compute_emac_26(
    symbol,
    end_date=None,
    count=None,
    cache_dir="stock_cache",
    force_update=False,
    **kwargs,
):
    return compute_emac(
        symbol,
        window=26,
        end_date=end_date,
        count=count,
        cache_dir=cache_dir,
        force_update=force_update,
    )


def compute_emac_60(
    symbol,
    end_date=None,
    count=None,
    cache_dir="stock_cache",
    force_update=False,
    **kwargs,
):
    return compute_emac(
        symbol,
        window=60,
        end_date=end_date,
        count=count,
        cache_dir=cache_dir,
        force_update=force_update,
    )


# -----------------------------------------------------------------
# ROC（动量）
# -----------------------------------------------------------------


def compute_roc(
    symbol: str,
    window: int,
    end_date: Optional[str] = None,
    count: Optional[int] = None,
    cache_dir: str = "stock_cache",
    force_update: bool = False,
    **kwargs,
) -> Union[float, pd.Series]:
    """
    计算 ROC（动量）因子。

    公式：(close / close.shift(window) - 1) * 100
    """
    need_count = count + window + 1 if count else window + 11
    df = _get_daily_ohlcv(
        symbol,
        end_date=end_date,
        cache_dir=cache_dir,
        force_update=force_update,
        count=need_count,
    )

    if df.empty or "close" not in df.columns:
        return np.nan

    df = df.set_index("date")
    close = df["close"].astype(float)

    roc = (safe_divide(close, close.shift(window)) - 1) * 100

    if count is not None and count > 0:
        roc = roc.tail(count)

    if len(roc) == 1:
        return float(roc.iloc[-1])
    return roc


def compute_roc_6(
    symbol,
    end_date=None,
    count=None,
    cache_dir="stock_cache",
    force_update=False,
    **kwargs,
):
    return compute_roc(
        symbol,
        window=6,
        end_date=end_date,
        count=count,
        cache_dir=cache_dir,
        force_update=force_update,
    )


def compute_roc_12(
    symbol,
    end_date=None,
    count=None,
    cache_dir="stock_cache",
    force_update=False,
    **kwargs,
):
    return compute_roc(
        symbol,
        window=12,
        end_date=end_date,
        count=count,
        cache_dir=cache_dir,
        force_update=force_update,
    )


def compute_roc_20(
    symbol,
    end_date=None,
    count=None,
    cache_dir="stock_cache",
    force_update=False,
    **kwargs,
):
    return compute_roc(
        symbol,
        window=20,
        end_date=end_date,
        count=count,
        cache_dir=cache_dir,
        force_update=force_update,
    )


def compute_roc_60(
    symbol,
    end_date=None,
    count=None,
    cache_dir="stock_cache",
    force_update=False,
    **kwargs,
):
    return compute_roc(
        symbol,
        window=60,
        end_date=end_date,
        count=count,
        cache_dir=cache_dir,
        force_update=force_update,
    )


def compute_roc_120(
    symbol,
    end_date=None,
    count=None,
    cache_dir="stock_cache",
    force_update=False,
    **kwargs,
):
    return compute_roc(
        symbol,
        window=120,
        end_date=end_date,
        count=count,
        cache_dir=cache_dir,
        force_update=force_update,
    )


# -----------------------------------------------------------------
# Price_NM（价格相对位置）
# -----------------------------------------------------------------


def compute_price_nm(
    symbol: str,
    window: int,
    end_date: Optional[str] = None,
    count: Optional[int] = None,
    cache_dir: str = "stock_cache",
    force_update: bool = False,
    **kwargs,
) -> Union[float, pd.Series]:
    """
    计算 PriceNM（价格相对位置）因子。

    公式：close / MA(close, window) - 1
    """
    need_count = count + window if count else window + 10
    df = _get_daily_ohlcv(
        symbol,
        end_date=end_date,
        cache_dir=cache_dir,
        force_update=force_update,
        count=need_count,
    )

    if df.empty or "close" not in df.columns:
        return np.nan

    df = df.set_index("date")
    close = df["close"].astype(float)

    ma = _compute_ma(close, window)
    price_nm = safe_divide(close, ma) - 1

    if count is not None and count > 0:
        price_nm = price_nm.tail(count)

    if len(price_nm) == 1:
        return float(price_nm.iloc[-1])
    return price_nm


def compute_price_1m(
    symbol,
    end_date=None,
    count=None,
    cache_dir="stock_cache",
    force_update=False,
    **kwargs,
):
    return compute_price_nm(
        symbol,
        window=21,
        end_date=end_date,
        count=count,
        cache_dir=cache_dir,
        force_update=force_update,
    )


def compute_price_3m(
    symbol,
    end_date=None,
    count=None,
    cache_dir="stock_cache",
    force_update=False,
    **kwargs,
):
    return compute_price_nm(
        symbol,
        window=61,
        end_date=end_date,
        count=count,
        cache_dir=cache_dir,
        force_update=force_update,
    )


def compute_price_1y(
    symbol,
    end_date=None,
    count=None,
    cache_dir="stock_cache",
    force_update=False,
    **kwargs,
):
    return compute_price_nm(
        symbol,
        window=250,
        end_date=end_date,
        count=count,
        cache_dir=cache_dir,
        force_update=force_update,
    )


# -----------------------------------------------------------------
# PLRC（价格线性回归系数）
# -----------------------------------------------------------------


def compute_plrc(
    symbol: str,
    window: int,
    end_date: Optional[str] = None,
    count: Optional[int] = None,
    cache_dir: str = "stock_cache",
    force_update: bool = False,
    **kwargs,
) -> Union[float, pd.Series]:
    """
    计算 PLRC（价格线性回归系数）因子。

    公式：对 close 进行 window 日的线性回归，返回斜率（归一化后）
    """
    need_count = count + window if count else window + 10
    df = _get_daily_ohlcv(
        symbol,
        end_date=end_date,
        cache_dir=cache_dir,
        force_update=force_update,
        count=need_count,
    )

    if df.empty or "close" not in df.columns:
        return np.nan

    df = df.set_index("date")
    close = df["close"].astype(float)

    def _slope(x):
        if len(x) < window:
            return np.nan
        norm_x = x / x.mean()
        y = np.arange(len(x))
        try:
            return np.polyfit(y, norm_x.values, 1)[0]
        except:
            return np.nan

    plrc = close.rolling(window=window, min_periods=window).apply(_slope)

    if count is not None and count > 0:
        plrc = plrc.tail(count)

    if len(plrc) == 1:
        return float(plrc.iloc[-1])
    return plrc


def compute_plrc_6(
    symbol,
    end_date=None,
    count=None,
    cache_dir="stock_cache",
    force_update=False,
    **kwargs,
):
    return compute_plrc(
        symbol,
        window=6,
        end_date=end_date,
        count=count,
        cache_dir=cache_dir,
        force_update=force_update,
    )


def compute_plrc_12(
    symbol,
    end_date=None,
    count=None,
    cache_dir="stock_cache",
    force_update=False,
    **kwargs,
):
    return compute_plrc(
        symbol,
        window=12,
        end_date=end_date,
        count=count,
        cache_dir=cache_dir,
        force_update=force_update,
    )


def compute_plrc_24(
    symbol,
    end_date=None,
    count=None,
    cache_dir="stock_cache",
    force_update=False,
    **kwargs,
):
    return compute_plrc(
        symbol,
        window=24,
        end_date=end_date,
        count=count,
        cache_dir=cache_dir,
        force_update=force_update,
    )


# -----------------------------------------------------------------
# Aroon（阿隆指标）
# -----------------------------------------------------------------


def compute_aroon(
    symbol: str,
    window: int = 25,
    end_date: Optional[str] = None,
    count: Optional[int] = None,
    cache_dir: str = "stock_cache",
    force_update: bool = False,
    **kwargs,
) -> Dict[str, Union[float, pd.Series]]:
    """
    计算 Aroon（阿隆指标）因子。

    返回：{'aroon_up': ..., 'aroon_down': ...}
    """
    need_count = count + window if count else window + 10
    df = _get_daily_ohlcv(
        symbol,
        end_date=end_date,
        cache_dir=cache_dir,
        force_update=force_update,
        count=need_count,
    )

    if df.empty or "high" not in df.columns:
        return {"aroon_up": np.nan, "aroon_down": np.nan}

    df = df.set_index("date")
    high = df["high"].astype(float)
    low = df["low"].astype(float)

    def _aroon_calc(h_vals, l_vals):
        days_since_high = window - 1 - np.argmax(h_vals)
        days_since_low = window - 1 - np.argmin(l_vals)
        aroon_up = (window - days_since_high) / window * 100
        aroon_down = (window - days_since_low) / window * 100
        return aroon_up, aroon_down

    aroon_up = pd.Series(index=high.index, dtype=float)
    aroon_down = pd.Series(index=high.index, dtype=float)

    for i in range(window - 1, len(high)):
        h_chunk = high.iloc[i - window + 1 : i + 1].values
        l_chunk = low.iloc[i - window + 1 : i + 1].values
        up, down = _aroon_calc(h_chunk, l_chunk)
        aroon_up.iloc[i] = up
        aroon_down.iloc[i] = down

    if count is not None and count > 0:
        aroon_up = aroon_up.tail(count)
        aroon_down = aroon_down.tail(count)

    return {
        "aroon_up": aroon_up.iloc[-1] if len(aroon_up) == 1 else aroon_up,
        "aroon_down": aroon_down.iloc[-1] if len(aroon_down) == 1 else aroon_down,
    }


def compute_aroon_up(
    symbol,
    end_date=None,
    count=None,
    cache_dir="stock_cache",
    force_update=False,
    **kwargs,
):
    result = compute_aroon(
        symbol,
        window=25,
        end_date=end_date,
        count=count,
        cache_dir=cache_dir,
        force_update=force_update,
    )
    return result["aroon_up"]


def compute_aroon_down(
    symbol,
    end_date=None,
    count=None,
    cache_dir="stock_cache",
    force_update=False,
    **kwargs,
):
    result = compute_aroon(
        symbol,
        window=25,
        end_date=end_date,
        count=count,
        cache_dir=cache_dir,
        force_update=force_update,
    )
    return result["aroon_down"]


# -----------------------------------------------------------------
# 52周价格位置
# -----------------------------------------------------------------


def compute_fifty_two_week_close_rank(
    symbol: str,
    end_date: Optional[str] = None,
    count: Optional[int] = None,
    cache_dir: str = "stock_cache",
    force_update: bool = False,
    **kwargs,
) -> Union[float, pd.Series]:
    """
    计算 52周价格位置因子。

    公式：当前收盘价在过去250天价格中的排名位置（有多少天价格高于当前）
    """
    need_count = count + 250 if count else 260
    df = _get_daily_ohlcv(
        symbol,
        end_date=end_date,
        cache_dir=cache_dir,
        force_update=force_update,
        count=need_count,
    )

    if df.empty or "close" not in df.columns or len(df) < 250:
        return np.nan

    df = df.set_index("date")
    close = df["close"].astype(float)

    rank = close.rolling(250).apply(
        lambda x: np.sum(x[:-1] > x[-1]) if len(x) == 250 else np.nan
    )

    if count is not None and count > 0:
        rank = rank.tail(count)

    if len(rank) == 1:
        return float(rank.iloc[-1])
    return rank


# -----------------------------------------------------------------
# Bull / Bear Power
# -----------------------------------------------------------------


def compute_bull_power(
    symbol: str,
    window: int = 13,
    end_date: Optional[str] = None,
    count: Optional[int] = None,
    cache_dir: str = "stock_cache",
    force_update: bool = False,
    **kwargs,
) -> Union[float, pd.Series]:
    """
    计算 Bull Power（多头力量）因子。

    公式：(high - EMA(close, window)) / close
    """
    need_count = count + window if count else window + 10
    df = _get_daily_ohlcv(
        symbol,
        end_date=end_date,
        cache_dir=cache_dir,
        force_update=force_update,
        count=need_count,
    )

    if df.empty or "high" not in df.columns:
        return np.nan

    df = df.set_index("date")
    high = df["high"].astype(float)
    close = df["close"].astype(float)

    ema = _compute_ema(close, window)
    bull = safe_divide(high - ema, close)

    if count is not None and count > 0:
        bull = bull.tail(count)

    if len(bull) == 1:
        return float(bull.iloc[-1])
    return bull


def compute_bear_power(
    symbol: str,
    window: int = 13,
    end_date: Optional[str] = None,
    count: Optional[int] = None,
    cache_dir: str = "stock_cache",
    force_update: bool = False,
    **kwargs,
) -> Union[float, pd.Series]:
    """
    计算 Bear Power（空头力量）因子。

    公式：(low - EMA(close, window)) / close
    """
    need_count = count + window if count else window + 10
    df = _get_daily_ohlcv(
        symbol,
        end_date=end_date,
        cache_dir=cache_dir,
        force_update=force_update,
        count=need_count,
    )

    if df.empty or "low" not in df.columns:
        return np.nan

    df = df.set_index("date")
    low = df["low"].astype(float)
    close = df["close"].astype(float)

    ema = _compute_ema(close, window)
    bear = safe_divide(low - ema, close)

    if count is not None and count > 0:
        bear = bear.tail(count)

    if len(bear) == 1:
        return float(bear.iloc[-1])
    return bear


# -----------------------------------------------------------------
# BBIC（BBI动量）
# -----------------------------------------------------------------


def compute_bbic(
    symbol: str,
    end_date: Optional[str] = None,
    count: Optional[int] = None,
    cache_dir: str = "stock_cache",
    force_update: bool = False,
    **kwargs,
) -> Union[float, pd.Series]:
    """
    计算 BBIC（BBI动量）因子。

    公式：(MA3 + MA6 + MA12 + MA24) / 4 / close
    """
    need_count = count + 24 if count else 34
    df = _get_daily_ohlcv(
        symbol,
        end_date=end_date,
        cache_dir=cache_dir,
        force_update=force_update,
        count=need_count,
    )

    if df.empty or "close" not in df.columns:
        return np.nan

    df = df.set_index("date")
    close = df["close"].astype(float)

    ma3 = _compute_ma(close, 3)
    ma6 = _compute_ma(close, 6)
    ma12 = _compute_ma(close, 12)
    ma24 = _compute_ma(close, 24)

    bbi = (ma3 + ma6 + ma12 + ma24) / 4
    bbic = safe_divide(bbi, close)

    if count is not None and count > 0:
        bbic = bbic.tail(count)

    if len(bbic) == 1:
        return float(bbic.iloc[-1])
    return bbic


# -----------------------------------------------------------------
# Volume1M（成交量动量）
# -----------------------------------------------------------------


def compute_volume_1m(
    symbol: str,
    end_date: Optional[str] = None,
    count: Optional[int] = None,
    cache_dir: str = "stock_cache",
    force_update: bool = False,
    **kwargs,
) -> Union[float, pd.Series]:
    """
    计算 Volume1M 因子。

    公式：(当日成交量 / 20日均成交量) * 20日平均收益率
    """
    need_count = count + 20 if count else 30
    df = _get_daily_ohlcv(
        symbol,
        end_date=end_date,
        cache_dir=cache_dir,
        force_update=force_update,
        count=need_count,
    )

    if df.empty or "volume" not in df.columns:
        return np.nan

    df = df.set_index("date")
    close = df["close"].astype(float)
    volume = df["volume"].astype(float)

    vol_ratio = safe_divide(volume, _compute_ma(volume, 20))
    ret_mean = close.pct_change().rolling(20).mean()

    volume_1m = vol_ratio * ret_mean

    if count is not None and count > 0:
        volume_1m = volume_1m.tail(count)

    if len(volume_1m) == 1:
        return float(volume_1m.iloc[-1])
    return volume_1m


# -----------------------------------------------------------------
# VPT（成交量价格趋势）
# -----------------------------------------------------------------


def compute_vpt(
    symbol: str,
    window: int = 6,
    end_date: Optional[str] = None,
    count: Optional[int] = None,
    cache_dir: str = "stock_cache",
    force_update: bool = False,
    **kwargs,
) -> Union[float, pd.Series]:
    """
    计算 VPT（成交量价格趋势）因子。

    公式：Σ(收益率 * 成交量)
    """
    need_count = count + window if count else window + 10
    df = _get_daily_ohlcv(
        symbol,
        end_date=end_date,
        cache_dir=cache_dir,
        force_update=force_update,
        count=need_count,
    )

    if df.empty or "volume" not in df.columns:
        return np.nan

    df = df.set_index("date")
    close = df["close"].astype(float)
    volume = df["volume"].astype(float)

    vpt_daily = close.pct_change() * volume
    vpt = vpt_daily.rolling(window).sum()

    if count is not None and count > 0:
        vpt = vpt.tail(count)

    if len(vpt) == 1:
        return float(vpt.iloc[-1])
    return vpt


def compute_single_day_vpt(
    symbol,
    end_date=None,
    count=None,
    cache_dir="stock_cache",
    force_update=False,
    **kwargs,
):
    return compute_vpt(
        symbol,
        window=1,
        end_date=end_date,
        count=count,
        cache_dir=cache_dir,
        force_update=force_update,
    )


def compute_single_day_vpt_6(
    symbol,
    end_date=None,
    count=None,
    cache_dir="stock_cache",
    force_update=False,
    **kwargs,
):
    return compute_vpt(
        symbol,
        window=6,
        end_date=end_date,
        count=count,
        cache_dir=cache_dir,
        force_update=force_update,
    )


def compute_single_day_vpt_12(
    symbol,
    end_date=None,
    count=None,
    cache_dir="stock_cache",
    force_update=False,
    **kwargs,
):
    return compute_vpt(
        symbol,
        window=12,
        end_date=end_date,
        count=count,
        cache_dir=cache_dir,
        force_update=force_update,
    )


# -----------------------------------------------------------------
# TRIX（三重指数平滑）
# -----------------------------------------------------------------


def compute_trix(
    symbol: str,
    window: int = 5,
    end_date: Optional[str] = None,
    count: Optional[int] = None,
    cache_dir: str = "stock_cache",
    force_update: bool = False,
    **kwargs,
) -> Union[float, pd.Series]:
    """
    计算 TRIX（三重指数平滑）因子。

    公式：(TR3 - TR3.shift(1)) / TR3.shift(1) * 100
    其中 TR3 = EMA(EMA(EMA(close, window), window), window)
    """
    need_count = count + window * 3 if count else window * 3 + 10
    df = _get_daily_ohlcv(
        symbol,
        end_date=end_date,
        cache_dir=cache_dir,
        force_update=force_update,
        count=need_count,
    )

    if df.empty or "close" not in df.columns:
        return np.nan

    df = df.set_index("date")
    close = df["close"].astype(float)

    ema1 = _compute_ema(close, window)
    ema2 = _compute_ema(ema1, window)
    ema3 = _compute_ema(ema2, window)

    trix = safe_divide(ema3 - ema3.shift(1), ema3.shift(1)) * 100

    if count is not None and count > 0:
        trix = trix.tail(count)

    if len(trix) == 1:
        return float(trix.iloc[-1])
    return trix


def compute_trix_5(
    symbol,
    end_date=None,
    count=None,
    cache_dir="stock_cache",
    force_update=False,
    **kwargs,
):
    return compute_trix(
        symbol,
        window=5,
        end_date=end_date,
        count=count,
        cache_dir=cache_dir,
        force_update=force_update,
    )


def compute_trix_10(
    symbol,
    end_date=None,
    count=None,
    cache_dir="stock_cache",
    force_update=False,
    **kwargs,
):
    return compute_trix(
        symbol,
        window=10,
        end_date=end_date,
        count=count,
        cache_dir=cache_dir,
        force_update=force_update,
    )


# -----------------------------------------------------------------
# MAC（简单移动平均）
# -----------------------------------------------------------------


def compute_mac(
    symbol: str,
    window: int,
    end_date: Optional[str] = None,
    count: Optional[int] = None,
    cache_dir: str = "stock_cache",
    force_update: bool = False,
    **kwargs,
) -> Union[float, pd.Series]:
    """
    计算 MAC（简单移动平均）因子。

    公式：MA(close, window)
    """
    need_count = count + window if count else window + 10
    df = _get_daily_ohlcv(
        symbol,
        end_date=end_date,
        cache_dir=cache_dir,
        force_update=force_update,
        count=need_count,
    )

    if df.empty or "close" not in df.columns:
        return np.nan

    df = df.set_index("date")
    close = df["close"].astype(float)

    ma = _compute_ma(close, window)

    if count is not None and count > 0:
        ma = ma.tail(count)

    if len(ma) == 1:
        return float(ma.iloc[-1])
    return ma


def compute_mac_60(
    symbol,
    end_date=None,
    count=None,
    cache_dir="stock_cache",
    force_update=False,
    **kwargs,
):
    return compute_mac(
        symbol,
        window=60,
        end_date=end_date,
        count=count,
        cache_dir=cache_dir,
        force_update=force_update,
    )


def compute_mac_120(
    symbol,
    end_date=None,
    count=None,
    cache_dir="stock_cache",
    force_update=False,
    **kwargs,
):
    return compute_mac(
        symbol,
        window=120,
        end_date=end_date,
        count=count,
        cache_dir=cache_dir,
        force_update=force_update,
    )


# -----------------------------------------------------------------
# VOL（成交量均值）
# -----------------------------------------------------------------


def compute_vol(
    symbol: str,
    window: int,
    end_date: Optional[str] = None,
    count: Optional[int] = None,
    cache_dir: str = "stock_cache",
    force_update: bool = False,
    **kwargs,
) -> Union[float, pd.Series]:
    """
    计算 VOL（成交量均值）因子。

    公式：MA(volume, window)
    """
    need_count = count + window if count else window + 10
    df = _get_daily_ohlcv(
        symbol,
        end_date=end_date,
        cache_dir=cache_dir,
        force_update=force_update,
        count=need_count,
    )

    if df.empty or "volume" not in df.columns:
        return np.nan

    df = df.set_index("date")
    volume = df["volume"].astype(float)

    vol = _compute_ma(volume, window)

    if count is not None and count > 0:
        vol = vol.tail(count)

    if len(vol) == 1:
        return float(vol.iloc[-1])
    return vol


def compute_vol_5(
    symbol,
    end_date=None,
    count=None,
    cache_dir="stock_cache",
    force_update=False,
    **kwargs,
):
    return compute_vol(
        symbol,
        window=5,
        end_date=end_date,
        count=count,
        cache_dir=cache_dir,
        force_update=force_update,
    )


def compute_vol_10(
    symbol,
    end_date=None,
    count=None,
    cache_dir="stock_cache",
    force_update=False,
    **kwargs,
):
    return compute_vol(
        symbol,
        window=10,
        end_date=end_date,
        count=count,
        cache_dir=cache_dir,
        force_update=force_update,
    )


def compute_vol_20(
    symbol,
    end_date=None,
    count=None,
    cache_dir="stock_cache",
    force_update=False,
    **kwargs,
):
    return compute_vol(
        symbol,
        window=20,
        end_date=end_date,
        count=count,
        cache_dir=cache_dir,
        force_update=force_update,
    )


def compute_vol_60(
    symbol,
    end_date=None,
    count=None,
    cache_dir="stock_cache",
    force_update=False,
    **kwargs,
):
    return compute_vol(
        symbol,
        window=60,
        end_date=end_date,
        count=count,
        cache_dir=cache_dir,
        force_update=force_update,
    )


def compute_vol_120(
    symbol,
    end_date=None,
    count=None,
    cache_dir="stock_cache",
    force_update=False,
    **kwargs,
):
    return compute_vol(
        symbol,
        window=120,
        end_date=end_date,
        count=count,
        cache_dir=cache_dir,
        force_update=force_update,
    )


def compute_vol_240(
    symbol,
    end_date=None,
    count=None,
    cache_dir="stock_cache",
    force_update=False,
    **kwargs,
):
    return compute_vol(
        symbol,
        window=240,
        end_date=end_date,
        count=count,
        cache_dir=cache_dir,
        force_update=force_update,
    )


# -----------------------------------------------------------------
# DAVOL（成交量偏离度）
# -----------------------------------------------------------------


def compute_davol(
    symbol: str,
    window: int,
    ref_window: int = 120,
    end_date: Optional[str] = None,
    count: Optional[int] = None,
    cache_dir: str = "stock_cache",
    force_update: bool = False,
    **kwargs,
) -> Union[float, pd.Series]:
    """
    计算 DAVOL（成交量偏离度）因子。

    公式：VOL_window / VOL_ref_window
    """
    need_count = (
        count + max(window, ref_window) if count else max(window, ref_window) + 10
    )
    df = _get_daily_ohlcv(
        symbol,
        end_date=end_date,
        cache_dir=cache_dir,
        force_update=force_update,
        count=need_count,
    )

    if df.empty or "volume" not in df.columns:
        return np.nan

    df = df.set_index("date")
    volume = df["volume"].astype(float)

    vol_short = _compute_ma(volume, window)
    vol_ref = _compute_ma(volume, ref_window)

    davol = safe_divide(vol_short, vol_ref)

    if count is not None and count > 0:
        davol = davol.tail(count)

    if len(davol) == 1:
        return float(davol.iloc[-1])
    return davol


def compute_davol_5(
    symbol,
    end_date=None,
    count=None,
    cache_dir="stock_cache",
    force_update=False,
    **kwargs,
):
    return compute_davol(
        symbol,
        window=5,
        ref_window=120,
        end_date=end_date,
        count=count,
        cache_dir=cache_dir,
        force_update=force_update,
    )


def compute_davol_10(
    symbol,
    end_date=None,
    count=None,
    cache_dir="stock_cache",
    force_update=False,
    **kwargs,
):
    return compute_davol(
        symbol,
        window=10,
        ref_window=120,
        end_date=end_date,
        count=count,
        cache_dir=cache_dir,
        force_update=force_update,
    )


def compute_davol_20(
    symbol,
    end_date=None,
    count=None,
    cache_dir="stock_cache",
    force_update=False,
    **kwargs,
):
    return compute_davol(
        symbol,
        window=20,
        ref_window=120,
        end_date=end_date,
        count=count,
        cache_dir=cache_dir,
        force_update=force_update,
    )


# -----------------------------------------------------------------
# VSTD（成交量标准差）
# -----------------------------------------------------------------


def compute_vstd(
    symbol: str,
    window: int,
    end_date: Optional[str] = None,
    count: Optional[int] = None,
    cache_dir: str = "stock_cache",
    force_update: bool = False,
    **kwargs,
) -> Union[float, pd.Series]:
    """计算 VSTD（成交量标准差）因子。"""
    need_count = count + window if count else window + 10
    df = _get_daily_ohlcv(
        symbol,
        end_date=end_date,
        cache_dir=cache_dir,
        force_update=force_update,
        count=need_count,
    )

    if df.empty or "volume" not in df.columns:
        return np.nan

    df = df.set_index("date")
    volume = df["volume"].astype(float)

    vstd = _compute_std(volume, window)

    if count is not None and count > 0:
        vstd = vstd.tail(count)

    if len(vstd) == 1:
        return float(vstd.iloc[-1])
    return vstd


def compute_vstd_10(
    symbol,
    end_date=None,
    count=None,
    cache_dir="stock_cache",
    force_update=False,
    **kwargs,
):
    return compute_vstd(
        symbol,
        window=10,
        end_date=end_date,
        count=count,
        cache_dir=cache_dir,
        force_update=force_update,
    )


def compute_vstd_20(
    symbol,
    end_date=None,
    count=None,
    cache_dir="stock_cache",
    force_update=False,
    **kwargs,
):
    return compute_vstd(
        symbol,
        window=20,
        end_date=end_date,
        count=count,
        cache_dir=cache_dir,
        force_update=force_update,
    )


# -----------------------------------------------------------------
# VROC（成交量动量）
# -----------------------------------------------------------------


def compute_vroc(
    symbol: str,
    window: int,
    end_date: Optional[str] = None,
    count: Optional[int] = None,
    cache_dir: str = "stock_cache",
    force_update: bool = False,
    **kwargs,
) -> Union[float, pd.Series]:
    """计算 VROC（成交量动量）因子。公式：(volume - volume.shift(window)) / volume.shift(window) * 100"""
    need_count = count + window + 1 if count else window + 11
    df = _get_daily_ohlcv(
        symbol,
        end_date=end_date,
        cache_dir=cache_dir,
        force_update=force_update,
        count=need_count,
    )

    if df.empty or "volume" not in df.columns:
        return np.nan

    df = df.set_index("date")
    volume = df["volume"].astype(float)

    vroc = safe_divide(volume - volume.shift(window), volume.shift(window)) * 100

    if count is not None and count > 0:
        vroc = vroc.tail(count)

    if len(vroc) == 1:
        return float(vroc.iloc[-1])
    return vroc


def compute_vroc_6(
    symbol,
    end_date=None,
    count=None,
    cache_dir="stock_cache",
    force_update=False,
    **kwargs,
):
    return compute_vroc(
        symbol,
        window=6,
        end_date=end_date,
        count=count,
        cache_dir=cache_dir,
        force_update=force_update,
    )


def compute_vroc_12(
    symbol,
    end_date=None,
    count=None,
    cache_dir="stock_cache",
    force_update=False,
    **kwargs,
):
    return compute_vroc(
        symbol,
        window=12,
        end_date=end_date,
        count=count,
        cache_dir=cache_dir,
        force_update=force_update,
    )


# -----------------------------------------------------------------
# VEMA（成交量指数移动平均）
# -----------------------------------------------------------------


def compute_vema(
    symbol: str,
    window: int,
    end_date: Optional[str] = None,
    count: Optional[int] = None,
    cache_dir: str = "stock_cache",
    force_update: bool = False,
    **kwargs,
) -> Union[float, pd.Series]:
    """计算 VEMA（成交量EMA）因子。"""
    need_count = count + window if count else window + 10
    df = _get_daily_ohlcv(
        symbol,
        end_date=end_date,
        cache_dir=cache_dir,
        force_update=force_update,
        count=need_count,
    )

    if df.empty or "volume" not in df.columns:
        return np.nan

    df = df.set_index("date")
    volume = df["volume"].astype(float)

    vema = _compute_ema(volume, window)

    if count is not None and count > 0:
        vema = vema.tail(count)

    if len(vema) == 1:
        return float(vema.iloc[-1])
    return vema


def compute_vema_5(
    symbol,
    end_date=None,
    count=None,
    cache_dir="stock_cache",
    force_update=False,
    **kwargs,
):
    return compute_vema(
        symbol,
        window=5,
        end_date=end_date,
        count=count,
        cache_dir=cache_dir,
        force_update=force_update,
    )


def compute_vema_10(
    symbol,
    end_date=None,
    count=None,
    cache_dir="stock_cache",
    force_update=False,
    **kwargs,
):
    return compute_vema(
        symbol,
        window=10,
        end_date=end_date,
        count=count,
        cache_dir=cache_dir,
        force_update=force_update,
    )


def compute_vema_12(
    symbol,
    end_date=None,
    count=None,
    cache_dir="stock_cache",
    force_update=False,
    **kwargs,
):
    return compute_vema(
        symbol,
        window=12,
        end_date=end_date,
        count=count,
        cache_dir=cache_dir,
        force_update=force_update,
    )


def compute_vema_26(
    symbol,
    end_date=None,
    count=None,
    cache_dir="stock_cache",
    force_update=False,
    **kwargs,
):
    return compute_vema(
        symbol,
        window=26,
        end_date=end_date,
        count=count,
        cache_dir=cache_dir,
        force_update=force_update,
    )


# -----------------------------------------------------------------
# VOSC（成交量震荡指标）
# -----------------------------------------------------------------


def compute_vosc(
    symbol: str,
    end_date: Optional[str] = None,
    count: Optional[int] = None,
    cache_dir: str = "stock_cache",
    force_update: bool = False,
    **kwargs,
) -> Union[float, pd.Series]:
    """
    计算 VOSC（成交量震荡指标）因子。

    公式：(VEMA12 - VEMA26) / VEMA12 * 100
    """
    need_count = count + 26 if count else 36
    df = _get_daily_ohlcv(
        symbol,
        end_date=end_date,
        cache_dir=cache_dir,
        force_update=force_update,
        count=need_count,
    )

    if df.empty or "volume" not in df.columns:
        return np.nan

    df = df.set_index("date")
    volume = df["volume"].astype(float)

    vema12 = _compute_ema(volume, 12)
    vema26 = _compute_ema(volume, 26)

    vosc = safe_divide(vema12 - vema26, vema12) * 100

    if count is not None and count > 0:
        vosc = vosc.tail(count)

    if len(vosc) == 1:
        return float(vosc.iloc[-1])
    return vosc


# -----------------------------------------------------------------
# TVMA / TVSTD（成交额均值/标准差）
# -----------------------------------------------------------------


def compute_tvma(
    symbol: str,
    window: int,
    end_date: Optional[str] = None,
    count: Optional[int] = None,
    cache_dir: str = "stock_cache",
    force_update: bool = False,
    **kwargs,
) -> Union[float, pd.Series]:
    """计算 TVMA（成交额均值）因子。"""
    need_count = count + window if count else window + 10
    df = _get_daily_ohlcv(
        symbol,
        end_date=end_date,
        cache_dir=cache_dir,
        force_update=force_update,
        count=need_count,
    )

    if df.empty or "money" not in df.columns:
        return np.nan

    df = df.set_index("date")
    money = df["money"].astype(float)

    tvma = _compute_ma(money, window)

    if count is not None and count > 0:
        tvma = tvma.tail(count)

    if len(tvma) == 1:
        return float(tvma.iloc[-1])
    return tvma


def compute_tvma_6(
    symbol,
    end_date=None,
    count=None,
    cache_dir="stock_cache",
    force_update=False,
    **kwargs,
):
    return compute_tvma(
        symbol,
        window=6,
        end_date=end_date,
        count=count,
        cache_dir=cache_dir,
        force_update=force_update,
    )


def compute_tvma_20(
    symbol,
    end_date=None,
    count=None,
    cache_dir="stock_cache",
    force_update=False,
    **kwargs,
):
    return compute_tvma(
        symbol,
        window=20,
        end_date=end_date,
        count=count,
        cache_dir=cache_dir,
        force_update=force_update,
    )


def compute_tvstd(
    symbol: str,
    window: int,
    end_date: Optional[str] = None,
    count: Optional[int] = None,
    cache_dir: str = "stock_cache",
    force_update: bool = False,
    **kwargs,
) -> Union[float, pd.Series]:
    """计算 TVSTD（成交额标准差）因子。"""
    need_count = count + window if count else window + 10
    df = _get_daily_ohlcv(
        symbol,
        end_date=end_date,
        cache_dir=cache_dir,
        force_update=force_update,
        count=need_count,
    )

    if df.empty or "money" not in df.columns:
        return np.nan

    df = df.set_index("date")
    money = df["money"].astype(float)

    tvstd = _compute_std(money, window)

    if count is not None and count > 0:
        tvstd = tvstd.tail(count)

    if len(tvstd) == 1:
        return float(tvstd.iloc[-1])
    return tvstd


def compute_tvstd_6(
    symbol,
    end_date=None,
    count=None,
    cache_dir="stock_cache",
    force_update=False,
    **kwargs,
):
    return compute_tvstd(
        symbol,
        window=6,
        end_date=end_date,
        count=count,
        cache_dir=cache_dir,
        force_update=force_update,
    )


def compute_tvstd_20(
    symbol,
    end_date=None,
    count=None,
    cache_dir="stock_cache",
    force_update=False,
    **kwargs,
):
    return compute_tvstd(
        symbol,
        window=20,
        end_date=end_date,
        count=count,
        cache_dir=cache_dir,
        force_update=force_update,
    )


# -----------------------------------------------------------------
# CCI（顺势指标）
# -----------------------------------------------------------------


def compute_cci(
    symbol: str,
    window: int,
    end_date: Optional[str] = None,
    count: Optional[int] = None,
    cache_dir: str = "stock_cache",
    force_update: bool = False,
    **kwargs,
) -> Union[float, pd.Series]:
    """
    计算 CCI（顺势指标）因子。

    公式：CCI = (TP - MA(TP, window)) / (0.015 * MD)
    其中 TP = (high + low + close) / 3，MD = mean deviation
    """
    need_count = count + window if count else window + 10
    df = _get_daily_ohlcv(
        symbol,
        end_date=end_date,
        cache_dir=cache_dir,
        force_update=force_update,
        count=need_count,
    )

    if df.empty or "close" not in df.columns:
        return np.nan

    df = df.set_index("date")
    high = df["high"].astype(float)
    low = df["low"].astype(float)
    close = df["close"].astype(float)

    tp = (high + low + close) / 3
    ma_tp = _compute_ma(tp, window)
    md = tp.rolling(window=window, min_periods=window).apply(
        lambda x: np.abs(x - x.mean()).mean()
    )
    cci = safe_divide(tp - ma_tp, 0.015 * md)

    if count is not None and count > 0:
        cci = cci.tail(count)

    if len(cci) == 1:
        return float(cci.iloc[-1])
    return cci


def compute_cci_10(
    symbol,
    end_date=None,
    count=None,
    cache_dir="stock_cache",
    force_update=False,
    **kwargs,
):
    return compute_cci(
        symbol,
        window=10,
        end_date=end_date,
        count=count,
        cache_dir=cache_dir,
        force_update=force_update,
    )


def compute_cci_15(
    symbol,
    end_date=None,
    count=None,
    cache_dir="stock_cache",
    force_update=False,
    **kwargs,
):
    return compute_cci(
        symbol,
        window=15,
        end_date=end_date,
        count=count,
        cache_dir=cache_dir,
        force_update=force_update,
    )


def compute_cci_20(
    symbol,
    end_date=None,
    count=None,
    cache_dir="stock_cache",
    force_update=False,
    **kwargs,
):
    return compute_cci(
        symbol,
        window=20,
        end_date=end_date,
        count=count,
        cache_dir=cache_dir,
        force_update=force_update,
    )


def compute_cci_88(
    symbol,
    end_date=None,
    count=None,
    cache_dir="stock_cache",
    force_update=False,
    **kwargs,
):
    return compute_cci(
        symbol,
        window=88,
        end_date=end_date,
        count=count,
        cache_dir=cache_dir,
        force_update=force_update,
    )


# -----------------------------------------------------------------
# AR / BR（人气/意愿指标）
# -----------------------------------------------------------------


def compute_ar(
    symbol: str,
    window: int = 26,
    end_date: Optional[str] = None,
    count: Optional[int] = None,
    cache_dir: str = "stock_cache",
    force_update: bool = False,
    **kwargs,
) -> Union[float, pd.Series]:
    """
    计算 AR（人气指标）因子。

    公式：AR = Σ(high - open) / Σ(open - low) * 100
    """
    need_count = count + window if count else window + 10
    df = _get_daily_ohlcv(
        symbol,
        end_date=end_date,
        cache_dir=cache_dir,
        force_update=force_update,
        count=need_count,
    )

    if df.empty or "open" not in df.columns:
        return np.nan

    df = df.set_index("date")
    high = df["high"].astype(float)
    low = df["low"].astype(float)
    open_price = df["open"].astype(float)

    ar = (
        safe_divide(
            (high - open_price).rolling(window).sum(),
            (open_price - low).rolling(window).sum(),
        )
        * 100
    )

    if count is not None and count > 0:
        ar = ar.tail(count)

    if len(ar) == 1:
        return float(ar.iloc[-1])
    return ar


def compute_br(
    symbol: str,
    window: int = 26,
    end_date: Optional[str] = None,
    count: Optional[int] = None,
    cache_dir: str = "stock_cache",
    force_update: bool = False,
    **kwargs,
) -> Union[float, pd.Series]:
    """
    计算 BR（意愿指标）因子。

    公式：BR = Σ(max(high - prev_close, 0)) / Σ(max(prev_close - low, 0)) * 100
    """
    need_count = count + window + 1 if count else window + 11
    df = _get_daily_ohlcv(
        symbol,
        end_date=end_date,
        cache_dir=cache_dir,
        force_update=force_update,
        count=need_count,
    )

    if df.empty or "close" not in df.columns:
        return np.nan

    df = df.set_index("date")
    high = df["high"].astype(float)
    low = df["low"].astype(float)
    close = df["close"].astype(float)
    prev_close = close.shift(1)

    up = (high - prev_close).clip(lower=0)
    down = (prev_close - low).clip(lower=0)

    br = safe_divide(up.rolling(window).sum(), down.rolling(window).sum()) * 100

    if count is not None and count > 0:
        br = br.tail(count)

    if len(br) == 1:
        return float(br.iloc[-1])
    return br


def compute_arbr(
    symbol: str,
    window: int = 26,
    end_date: Optional[str] = None,
    count: Optional[int] = None,
    cache_dir: str = "stock_cache",
    force_update: bool = False,
    **kwargs,
) -> Union[float, pd.Series]:
    """计算 ARBR（AR-BR差值）因子。"""
    ar = compute_ar(symbol, window, end_date, count, cache_dir, force_update)
    br = compute_br(symbol, window, end_date, count, cache_dir, force_update)

    if isinstance(ar, pd.Series) and isinstance(br, pd.Series):
        return ar - br
    elif isinstance(ar, (float, np.floating)) and isinstance(br, (float, np.floating)):
        return ar - br
    return np.nan


# -----------------------------------------------------------------
# WVAD（威廉变异离散量）
# -----------------------------------------------------------------


def compute_wvad(
    symbol: str,
    window: int = 6,
    end_date: Optional[str] = None,
    count: Optional[int] = None,
    cache_dir: str = "stock_cache",
    force_update: bool = False,
    **kwargs,
) -> Union[float, pd.Series]:
    """
    计算 WVAD（威廉变异离散量）因子。

    公式：Σ((close - open) / (high - low) * volume)，若 high==low 则跳过
    """
    need_count = count + window if count else window + 10
    df = _get_daily_ohlcv(
        symbol,
        end_date=end_date,
        cache_dir=cache_dir,
        force_update=force_update,
        count=need_count,
    )

    if df.empty or "open" not in df.columns:
        return np.nan

    df = df.set_index("date")
    high = df["high"].astype(float)
    low = df["low"].astype(float)
    close = df["close"].astype(float)
    open_price = df["open"].astype(float)
    volume = df["volume"].astype(float)

    hl_range = high - low
    hl_range = hl_range.replace(0, np.nan)

    wvad_daily = safe_divide(close - open_price, hl_range) * volume
    wvad = wvad_daily.rolling(window).sum()

    if count is not None and count > 0:
        wvad = wvad.tail(count)

    if len(wvad) == 1:
        return float(wvad.iloc[-1])
    return wvad


def compute_mawvad(
    symbol,
    end_date=None,
    count=None,
    cache_dir="stock_cache",
    force_update=False,
    **kwargs,
):
    return compute_wvad(
        symbol,
        window=6,
        end_date=end_date,
        count=count,
        cache_dir=cache_dir,
        force_update=force_update,
    )


# -----------------------------------------------------------------
# PSY（心理线）
# -----------------------------------------------------------------


def compute_psy(
    symbol: str,
    window: int = 12,
    end_date: Optional[str] = None,
    count: Optional[int] = None,
    cache_dir: str = "stock_cache",
    force_update: bool = False,
    **kwargs,
) -> Union[float, pd.Series]:
    """
    计算 PSY（心理线）因子。

    公式：(上涨天数 / window) * 100
    """
    need_count = count + window if count else window + 10
    df = _get_daily_ohlcv(
        symbol,
        end_date=end_date,
        cache_dir=cache_dir,
        force_update=force_update,
        count=need_count,
    )

    if df.empty or "close" not in df.columns:
        return np.nan

    df = df.set_index("date")
    close = df["close"].astype(float)

    up_days = (close.diff() > 0).astype(int)
    psy = up_days.rolling(window).sum() / window * 100

    if count is not None and count > 0:
        psy = psy.tail(count)

    if len(psy) == 1:
        return float(psy.iloc[-1])
    return psy


# -----------------------------------------------------------------
# VR（成交量比率）
# -----------------------------------------------------------------


def compute_vr(
    symbol: str,
    window: int = 26,
    end_date: Optional[str] = None,
    count: Optional[int] = None,
    cache_dir: str = "stock_cache",
    force_update: bool = False,
    **kwargs,
) -> Union[float, pd.Series]:
    """
    计算 VR（成交量比率）因子。

    公式：(上涨成交量 + 0.5*平盘成交量) / (下跌成交量 + 0.5*平盘成交量) * 100
    """
    need_count = count + window + 1 if count else window + 11
    df = _get_daily_ohlcv(
        symbol,
        end_date=end_date,
        cache_dir=cache_dir,
        force_update=force_update,
        count=need_count,
    )

    if df.empty or "volume" not in df.columns:
        return np.nan

    df = df.set_index("date")
    close = df["close"].astype(float)
    volume = df["volume"].astype(float)

    ret = close.diff()
    avs = volume.where(ret > 0, 0).rolling(window).sum()
    bvs = volume.where(ret < 0, 0).rolling(window).sum()
    cvs = volume.where(ret == 0, 0).rolling(window).sum()

    vr = safe_divide(avs + 0.5 * cvs, bvs + 0.5 * cvs) * 100

    if count is not None and count > 0:
        vr = vr.tail(count)

    if len(vr) == 1:
        return float(vr.iloc[-1])
    return vr


# -----------------------------------------------------------------
# MACD（指数平滑异同移动平均线）
# -----------------------------------------------------------------


def compute_macd(
    symbol: str,
    end_date: Optional[str] = None,
    count: Optional[int] = None,
    cache_dir: str = "stock_cache",
    force_update: bool = False,
    **kwargs,
) -> Union[float, pd.Series]:
    """
    计算 MACD 因子。

    公式：MACD = 2 * (EMA12 - EMA26的EMA9) / close
    返回 MACD柱值除以收盘价
    """
    need_count = count + 35 if count else 45
    df = _get_daily_ohlcv(
        symbol,
        end_date=end_date,
        cache_dir=cache_dir,
        force_update=force_update,
        count=need_count,
    )

    if df.empty or "close" not in df.columns:
        return np.nan

    df = df.set_index("date")
    close = df["close"].astype(float)

    ema12 = _compute_ema(close, 12)
    ema26 = _compute_ema(close, 26)
    diff = ema12 - ema26
    dea = _compute_ema(diff, 9)
    macd = 2 * (diff - dea)

    macd_ratio = safe_divide(macd, close)

    if count is not None and count > 0:
        macd_ratio = macd_ratio.tail(count)

    if len(macd_ratio) == 1:
        return float(macd_ratio.iloc[-1])
    return macd_ratio


# -----------------------------------------------------------------
# MFI（资金流量指标）
# -----------------------------------------------------------------


def compute_mfi(
    symbol: str,
    window: int = 14,
    end_date: Optional[str] = None,
    count: Optional[int] = None,
    cache_dir: str = "stock_cache",
    force_update: bool = False,
    **kwargs,
) -> Union[float, pd.Series]:
    """
    计算 MFI（资金流量指标）因子。

    公式：MFI = 100 - 100 / (1 + MR)
    其中 MR = 正资金流量 / 负资金流量
    """
    need_count = count + window + 1 if count else window + 15
    df = _get_daily_ohlcv(
        symbol,
        end_date=end_date,
        cache_dir=cache_dir,
        force_update=force_update,
        count=need_count,
    )

    if df.empty or "volume" not in df.columns:
        return np.nan

    df = df.set_index("date")
    high = df["high"].astype(float)
    low = df["low"].astype(float)
    close = df["close"].astype(float)
    volume = df["volume"].astype(float)

    typical = (high + low + close) / 3
    mf = typical * volume

    pos_mf = mf.where(typical > typical.shift(1), 0).rolling(window).sum()
    neg_mf = mf.where(typical < typical.shift(1), 0).rolling(window).sum()

    mr = safe_divide(pos_mf, neg_mf)
    mfi = 100 - safe_divide(100, 1 + mr)

    if count is not None and count > 0:
        mfi = mfi.tail(count)

    if len(mfi) == 1:
        return float(mfi.iloc[-1])
    return mfi


def compute_mfi_14(
    symbol,
    end_date=None,
    count=None,
    cache_dir="stock_cache",
    force_update=False,
    **kwargs,
):
    return compute_mfi(
        symbol,
        window=14,
        end_date=end_date,
        count=count,
        cache_dir=cache_dir,
        force_update=force_update,
    )


# -----------------------------------------------------------------
# money_flow（资金流）
# -----------------------------------------------------------------


def compute_money_flow_20(
    symbol: str,
    end_date: Optional[str] = None,
    count: Optional[int] = None,
    cache_dir: str = "stock_cache",
    force_update: bool = False,
    **kwargs,
) -> Union[float, pd.Series]:
    """
    计算 money_flow_20（20 日资金流）因子。

    近似公式：MA(money, 20)，其中 money 为成交额
    """
    need_count = count + 20 if count else 30
    df = _get_daily_ohlcv(
        symbol,
        end_date=end_date,
        cache_dir=cache_dir,
        force_update=force_update,
        count=need_count,
    )

    if df.empty or "money" not in df.columns:
        return np.nan

    df = df.set_index("date")
    money = df["money"].astype(float)

    mf = _compute_ma(money, 20)

    if count is not None and count > 0:
        mf = mf.tail(count)

    if len(mf) == 1:
        return float(mf.iloc[-1])
    return mf


# -----------------------------------------------------------------
# 换手率类因子
# -----------------------------------------------------------------


def compute_average_share_turnover_annual(
    symbol: str,
    end_date: Optional[str] = None,
    count: Optional[int] = None,
    cache_dir: str = "stock_cache",
    force_update: bool = False,
    **kwargs,
) -> Union[float, pd.Series]:
    """
    计算 average_share_turnover_annual（年均换手率）因子。

    直接使用日线数据中的换手率字段，取240日均值。
    换手率单位已标准化为比例（如0.02表示2%）。
    """
    need_count = count + 240 if count else 250
    df = _get_daily_ohlcv(
        symbol,
        end_date=end_date,
        cache_dir=cache_dir,
        force_update=force_update,
        count=need_count,
    )

    if df.empty or "turnover_rate" not in df.columns:
        return np.nan

    df = df.set_index("date")
    turnover = df["turnover_rate"].astype(float)

    # 计算240日换手率均值
    avg_turnover = turnover.rolling(window=240, min_periods=20).mean()

    if count is not None and count > 0:
        avg_turnover = avg_turnover.tail(count)

    if len(avg_turnover) == 1:
        return float(avg_turnover.iloc[-1])
    return avg_turnover


def compute_share_turnover_monthly(
    symbol: str,
    end_date: Optional[str] = None,
    count: Optional[int] = None,
    cache_dir: str = "stock_cache",
    force_update: bool = False,
    **kwargs,
) -> Union[float, pd.Series]:
    """
    计算 share_turnover_monthly（月均换手率）因子。

    直接使用日线数据中的换手率字段，取20日均值。
    """
    need_count = count + 20 if count else 30
    df = _get_daily_ohlcv(
        symbol,
        end_date=end_date,
        cache_dir=cache_dir,
        force_update=force_update,
        count=need_count,
    )

    if df.empty or "turnover_rate" not in df.columns:
        return np.nan

    df = df.set_index("date")
    turnover = df["turnover_rate"].astype(float)

    # 计算20日换手率均值
    avg_turnover = turnover.rolling(window=20, min_periods=5).mean()

    if count is not None and count > 0:
        avg_turnover = avg_turnover.tail(count)

    if len(avg_turnover) == 1:
        return float(avg_turnover.iloc[-1])
    return avg_turnover


# -----------------------------------------------------------------
# BOLL（布林带）
# -----------------------------------------------------------------


def compute_boll(
    symbol: str,
    window: int = 20,
    num_std: float = 2.0,
    end_date: Optional[str] = None,
    count: Optional[int] = None,
    cache_dir: str = "stock_cache",
    force_update: bool = False,
    **kwargs,
) -> Union[float, pd.Series, tuple]:
    """
    计算布林带因子。

    公式：
    - boll_up = MA(close, window) + num_std * STD(close, window)
    - boll_down = MA(close, window) - num_std * STD(close, window)

    返回：(boll_up, boll_down) 如果 is_output_boll=True，否则返回 boll_up
    """
    need_count = count + window if count else window + 10
    df = _get_daily_ohlcv(
        symbol,
        end_date=end_date,
        cache_dir=cache_dir,
        force_update=force_update,
        count=need_count,
    )

    if df.empty or "close" not in df.columns:
        return np.nan

    df = df.set_index("date")
    close = df["close"].astype(float)

    ma = _compute_ma(close, window)
    std = _compute_std(close, window)

    boll_up = ma + num_std * std
    boll_down = ma - num_std * std

    if count is not None and count > 0:
        boll_up = boll_up.tail(count)
        boll_down = boll_down.tail(count)

    if len(boll_up) == 1:
        return (float(boll_up.iloc[-1]), float(boll_down.iloc[-1]))
    return (boll_up, boll_down)


def compute_boll_up(
    symbol: str,
    end_date: Optional[str] = None,
    count: Optional[int] = None,
    cache_dir: str = "stock_cache",
    force_update: bool = False,
    **kwargs,
) -> Union[float, pd.Series]:
    """计算 boll_up（布林带上轨）因子。"""
    result = compute_boll(
        symbol,
        window=20,
        num_std=2.0,
        end_date=end_date,
        count=count,
        cache_dir=cache_dir,
        force_update=force_update,
    )
    if isinstance(result, tuple):
        return result[0]
    return result


def compute_boll_down(
    symbol: str,
    end_date: Optional[str] = None,
    count: Optional[int] = None,
    cache_dir: str = "stock_cache",
    force_update: bool = False,
    **kwargs,
) -> Union[float, pd.Series]:
    """计算 boll_down（布林带下轨）因子。"""
    result = compute_boll(
        symbol,
        window=20,
        num_std=2.0,
        end_date=end_date,
        count=count,
        cache_dir=cache_dir,
        force_update=force_update,
    )
    if isinstance(result, tuple):
        return result[1]
    return result


# -----------------------------------------------------------------
# ATR（真实波动幅度）
# -----------------------------------------------------------------


def compute_atr(
    symbol: str,
    window: int,
    end_date: Optional[str] = None,
    count: Optional[int] = None,
    cache_dir: str = "stock_cache",
    force_update: bool = False,
    **kwargs,
) -> Union[float, pd.Series]:
    """
    计算 ATR（平均真实波动幅度）因子。

    公式：ATR = EMA(TR, window)
    其中 TR = max(H-L, abs(H-C_prev), abs(L-C_prev))
    """
    need_count = count + window + 1 if count else window + 11
    df = _get_daily_ohlcv(
        symbol,
        end_date=end_date,
        cache_dir=cache_dir,
        force_update=force_update,
        count=need_count,
    )

    if df.empty or "close" not in df.columns:
        return np.nan

    df = df.set_index("date")
    high = df["high"].astype(float)
    low = df["low"].astype(float)
    close = df["close"].astype(float)

    # 计算 TR
    tr1 = high - low
    tr2 = np.abs(high - close.shift(1))
    tr3 = np.abs(low - close.shift(1))
    tr = pd.concat([tr1, tr2, tr3], axis=1).max(axis=1)

    # 计算 ATR
    atr = tr.ewm(span=window, adjust=False).mean()

    if count is not None and count > 0:
        atr = atr.tail(count)

    if len(atr) == 1:
        return float(atr.iloc[-1])
    return atr


def compute_atr_6(
    symbol: str,
    end_date: Optional[str] = None,
    count: Optional[int] = None,
    cache_dir: str = "stock_cache",
    force_update: bool = False,
    **kwargs,
) -> Union[float, pd.Series]:
    """计算 ATR6（6日平均真实波动幅度）因子。"""
    return compute_atr(
        symbol,
        window=6,
        end_date=end_date,
        count=count,
        cache_dir=cache_dir,
        force_update=force_update,
    )


def compute_atr_14(
    symbol: str,
    end_date: Optional[str] = None,
    count: Optional[int] = None,
    cache_dir: str = "stock_cache",
    force_update: bool = False,
    **kwargs,
) -> Union[float, pd.Series]:
    """计算 ATR14（14日平均真实波动幅度）因子。"""
    return compute_atr(
        symbol,
        window=14,
        end_date=end_date,
        count=count,
        cache_dir=cache_dir,
        force_update=force_update,
    )


# -----------------------------------------------------------------
# Variance（收益率方差）
# -----------------------------------------------------------------


def compute_variance(
    symbol: str,
    window: int,
    end_date: Optional[str] = None,
    count: Optional[int] = None,
    cache_dir: str = "stock_cache",
    force_update: bool = False,
    **kwargs,
) -> Union[float, pd.Series]:
    """
    计算收益率方差因子。

    公式：VAR(ret, window)，其中 ret = close / close.shift(1) - 1
    """
    need_count = count + window + 1 if count else window + 11
    df = _get_daily_ohlcv(
        symbol,
        end_date=end_date,
        cache_dir=cache_dir,
        force_update=force_update,
        count=need_count,
    )

    if df.empty or "close" not in df.columns:
        return np.nan

    df = df.set_index("date")
    close = df["close"].astype(float)

    ret = close.pct_change()
    variance = ret.rolling(window=window, min_periods=window).var() * 252

    if count is not None and count > 0:
        variance = variance.tail(count)

    if len(variance) == 1:
        return float(variance.iloc[-1])
    return variance


def compute_variance_20(
    symbol,
    end_date=None,
    count=None,
    cache_dir="stock_cache",
    force_update=False,
    **kwargs,
):
    return compute_variance(
        symbol,
        window=20,
        end_date=end_date,
        count=count,
        cache_dir=cache_dir,
        force_update=force_update,
    )


def compute_variance_60(
    symbol,
    end_date=None,
    count=None,
    cache_dir="stock_cache",
    force_update=False,
    **kwargs,
):
    return compute_variance(
        symbol,
        window=60,
        end_date=end_date,
        count=count,
        cache_dir=cache_dir,
        force_update=force_update,
    )


def compute_variance_120(
    symbol,
    end_date=None,
    count=None,
    cache_dir="stock_cache",
    force_update=False,
    **kwargs,
):
    return compute_variance(
        symbol,
        window=120,
        end_date=end_date,
        count=count,
        cache_dir=cache_dir,
        force_update=force_update,
    )


# -----------------------------------------------------------------
# Skewness（偏度）
# -----------------------------------------------------------------


def compute_skewness(
    symbol: str,
    window: int,
    end_date: Optional[str] = None,
    count: Optional[int] = None,
    cache_dir: str = "stock_cache",
    force_update: bool = False,
    **kwargs,
) -> Union[float, pd.Series]:
    """
    计算收益率偏度因子。

    公式：Skewness(ret, window)
    """
    need_count = count + window + 1 if count else window + 11
    df = _get_daily_ohlcv(
        symbol,
        end_date=end_date,
        cache_dir=cache_dir,
        force_update=force_update,
        count=need_count,
    )

    if df.empty or "close" not in df.columns:
        return np.nan

    df = df.set_index("date")
    close = df["close"].astype(float)

    ret = close.pct_change()
    skewness = ret.rolling(window=window, min_periods=window).skew()

    if count is not None and count > 0:
        skewness = skewness.tail(count)

    if len(skewness) == 1:
        return float(skewness.iloc[-1])
    return skewness


def compute_skewness_20(
    symbol,
    end_date=None,
    count=None,
    cache_dir="stock_cache",
    force_update=False,
    **kwargs,
):
    return compute_skewness(
        symbol,
        window=20,
        end_date=end_date,
        count=count,
        cache_dir=cache_dir,
        force_update=force_update,
    )


def compute_skewness_60(
    symbol,
    end_date=None,
    count=None,
    cache_dir="stock_cache",
    force_update=False,
    **kwargs,
):
    return compute_skewness(
        symbol,
        window=60,
        end_date=end_date,
        count=count,
        cache_dir=cache_dir,
        force_update=force_update,
    )


def compute_skewness_120(
    symbol,
    end_date=None,
    count=None,
    cache_dir="stock_cache",
    force_update=False,
    **kwargs,
):
    return compute_skewness(
        symbol,
        window=120,
        end_date=end_date,
        count=count,
        cache_dir=cache_dir,
        force_update=force_update,
    )


# -----------------------------------------------------------------
# Kurtosis（峰度）
# -----------------------------------------------------------------


def compute_kurtosis(
    symbol: str,
    window: int,
    end_date: Optional[str] = None,
    count: Optional[int] = None,
    cache_dir: str = "stock_cache",
    force_update: bool = False,
    **kwargs,
) -> Union[float, pd.Series]:
    """
    计算收益率峰度因子。

    公式：Kurtosis(ret, window)
    """
    need_count = count + window + 1 if count else window + 11
    df = _get_daily_ohlcv(
        symbol,
        end_date=end_date,
        cache_dir=cache_dir,
        force_update=force_update,
        count=need_count,
    )

    if df.empty or "close" not in df.columns:
        return np.nan

    df = df.set_index("date")
    close = df["close"].astype(float)

    ret = close.pct_change()
    kurtosis = ret.rolling(window=window, min_periods=window).kurt()

    if count is not None and count > 0:
        kurtosis = kurtosis.tail(count)

    if len(kurtosis) == 1:
        return float(kurtosis.iloc[-1])
    return kurtosis


def compute_kurtosis_20(
    symbol,
    end_date=None,
    count=None,
    cache_dir="stock_cache",
    force_update=False,
    **kwargs,
):
    return compute_kurtosis(
        symbol,
        window=20,
        end_date=end_date,
        count=count,
        cache_dir=cache_dir,
        force_update=force_update,
    )


def compute_kurtosis_60(
    symbol,
    end_date=None,
    count=None,
    cache_dir="stock_cache",
    force_update=False,
    **kwargs,
):
    return compute_kurtosis(
        symbol,
        window=60,
        end_date=end_date,
        count=count,
        cache_dir=cache_dir,
        force_update=force_update,
    )


def compute_kurtosis_120(
    symbol,
    end_date=None,
    count=None,
    cache_dir="stock_cache",
    force_update=False,
    **kwargs,
):
    return compute_kurtosis(
        symbol,
        window=120,
        end_date=end_date,
        count=count,
        cache_dir=cache_dir,
        force_update=force_update,
    )


# -----------------------------------------------------------------
# Sharpe Ratio（夏普比率）
# -----------------------------------------------------------------


def compute_sharpe_ratio(
    symbol: str,
    window: int,
    rf: float = 0.04,
    end_date: Optional[str] = None,
    count: Optional[int] = None,
    cache_dir: str = "stock_cache",
    force_update: bool = False,
    **kwargs,
) -> Union[float, pd.Series]:
    """
    计算夏普比率因子。

    公式：(年化收益率 - 无风险利率) / 年化波动率
    """
    need_count = count + window + 1 if count else window + 11
    df = _get_daily_ohlcv(
        symbol,
        end_date=end_date,
        cache_dir=cache_dir,
        force_update=force_update,
        count=need_count,
    )

    if df.empty or "close" not in df.columns:
        return np.nan

    df = df.set_index("date")
    close = df["close"].astype(float)

    ret = close.pct_change()
    ann_ret = (1 + ret.rolling(window).mean()) ** 252 - 1
    ann_std = ret.rolling(window).std() * np.sqrt(252)

    sharpe = safe_divide(ann_ret - rf, ann_std)

    if count is not None and count > 0:
        sharpe = sharpe.tail(count)

    if len(sharpe) == 1:
        return float(sharpe.iloc[-1])
    return sharpe


def compute_sharpe_ratio_20(
    symbol,
    end_date=None,
    count=None,
    cache_dir="stock_cache",
    force_update=False,
    **kwargs,
):
    return compute_sharpe_ratio(
        symbol,
        window=20,
        end_date=end_date,
        count=count,
        cache_dir=cache_dir,
        force_update=force_update,
    )


def compute_sharpe_ratio_60(
    symbol,
    end_date=None,
    count=None,
    cache_dir="stock_cache",
    force_update=False,
    **kwargs,
):
    return compute_sharpe_ratio(
        symbol,
        window=60,
        end_date=end_date,
        count=count,
        cache_dir=cache_dir,
        force_update=force_update,
    )


def compute_sharpe_ratio_120(
    symbol,
    end_date=None,
    count=None,
    cache_dir="stock_cache",
    force_update=False,
    **kwargs,
):
    return compute_sharpe_ratio(
        symbol,
        window=120,
        end_date=end_date,
        count=count,
        cache_dir=cache_dir,
        force_update=force_update,
    )


# -----------------------------------------------------------------
# PLRC（价格线性回归系数）
# -----------------------------------------------------------------


def compute_plrc(
    symbol: str,
    window: int,
    end_date: Optional[str] = None,
    count: Optional[int] = None,
    cache_dir: str = "stock_cache",
    force_update: bool = False,
    **kwargs,
) -> Union[float, pd.Series]:
    """
    计算 PLRC（价格线性回归系数）因子。

    公式：对 close 进行 window 日的线性回归，返回斜率
    """
    need_count = count + window if count else window + 10
    df = _get_daily_ohlcv(
        symbol,
        end_date=end_date,
        cache_dir=cache_dir,
        force_update=force_update,
        count=need_count,
    )

    if df.empty or "close" not in df.columns:
        return np.nan

    df = df.set_index("date")
    close = df["close"].astype(float)

    def _linear_regression_slope(x):
        if len(x) < window:
            return np.nan
        y = np.arange(len(x))
        try:
            slope = np.polyfit(y, x, 1)[0]
            return slope
        except Exception:
            return np.nan

    plrc = close.rolling(window=window, min_periods=window).apply(
        _linear_regression_slope
    )

    if count is not None and count > 0:
        plrc = plrc.tail(count)

    if len(plrc) == 1:
        return float(plrc.iloc[-1])
    return plrc


def compute_plrc_6(
    symbol: str,
    end_date: Optional[str] = None,
    count: Optional[int] = None,
    cache_dir: str = "stock_cache",
    force_update: bool = False,
    **kwargs,
) -> Union[float, pd.Series]:
    """计算 PLRC6（6日价格线性回归系数）因子。"""
    return compute_plrc(
        symbol,
        window=6,
        end_date=end_date,
        count=count,
        cache_dir=cache_dir,
        force_update=force_update,
    )


# -----------------------------------------------------------------
# CR（能量指标）
# -----------------------------------------------------------------


def compute_cr(
    symbol: str,
    window: int,
    end_date: Optional[str] = None,
    count: Optional[int] = None,
    cache_dir: str = "stock_cache",
    force_update: bool = False,
    **kwargs,
) -> Union[float, pd.Series]:
    """
    计算 CR（能量指标）因子。

    公式：
    - 中间价 M = (H + L) / 2
    - P1 = max(H - M.shift(1), 0) 的 window 日和
    - P2 = max(M.shift(1) - L, 0) 的 window 日和
    - CR = P1 / P2 * 100
    """
    need_count = count + window + 1 if count else window + 11
    df = _get_daily_ohlcv(
        symbol,
        end_date=end_date,
        cache_dir=cache_dir,
        force_update=force_update,
        count=need_count,
    )

    if df.empty or "close" not in df.columns:
        return np.nan

    df = df.set_index("date")
    high = df["high"].astype(float)
    low = df["low"].astype(float)

    m = (high + low) / 2
    m_prev = m.shift(1)

    p1 = (high - m_prev).clip(lower=0)
    p2 = (m_prev - low).clip(lower=0)

    p1_sum = p1.rolling(window=window, min_periods=window).sum()
    p2_sum = p2.rolling(window=window, min_periods=window).sum()

    cr = safe_divide(p1_sum, p2_sum) * 100

    if count is not None and count > 0:
        cr = cr.tail(count)

    if len(cr) == 1:
        return float(cr.iloc[-1])
    return cr


def compute_cr_20(
    symbol: str,
    end_date: Optional[str] = None,
    count: Optional[int] = None,
    cache_dir: str = "stock_cache",
    force_update: bool = False,
    **kwargs,
) -> Union[float, pd.Series]:
    """计算 CR20（20日能量指标）因子。"""
    return compute_cr(
        symbol,
        window=20,
        end_date=end_date,
        count=count,
        cache_dir=cache_dir,
        force_update=force_update,
    )


# -----------------------------------------------------------------
# RSI（相对强弱指标）
# -----------------------------------------------------------------


def compute_rsi(
    symbol: str,
    window: int = 14,
    end_date: Optional[str] = None,
    count: Optional[int] = None,
    cache_dir: str = "stock_cache",
    force_update: bool = False,
    **kwargs,
) -> Union[float, pd.Series]:
    """
    计算 RSI（相对强弱指标）因子。

    公式：RSI = 100 - 100 / (1 + RS)
    其中 RS = 平均上涨幅度 / 平均下跌幅度
    """
    need_count = count + window + 1 if count else window + 11
    df = _get_daily_ohlcv(
        symbol,
        end_date=end_date,
        cache_dir=cache_dir,
        force_update=force_update,
        count=need_count,
    )

    if df.empty or "close" not in df.columns:
        return np.nan

    df = df.set_index("date")
    close = df["close"].astype(float)

    # 计算价格变动
    delta = close.diff()

    # 分离上涨和下跌
    gain = delta.where(delta > 0, 0)
    loss = (-delta).where(delta < 0, 0)

    # 计算平均上涨和下跌（使用EMA）
    avg_gain = gain.ewm(span=window, adjust=False).mean()
    avg_loss = loss.ewm(span=window, adjust=False).mean()

    # 计算RS和RSI
    rs = safe_divide(avg_gain, avg_loss)
    rsi = 100 - safe_divide(100, 1 + rs)

    if count is not None and count > 0:
        rsi = rsi.tail(count)

    if len(rsi) == 1:
        return float(rsi.iloc[-1])
    return rsi


def compute_rsi_6(
    symbol: str,
    end_date: Optional[str] = None,
    count: Optional[int] = None,
    cache_dir: str = "stock_cache",
    force_update: bool = False,
    **kwargs,
) -> Union[float, pd.Series]:
    """计算 RSI6（6日相对强弱指标）因子。"""
    return compute_rsi(
        symbol,
        window=6,
        end_date=end_date,
        count=count,
        cache_dir=cache_dir,
        force_update=force_update,
    )


def compute_rsi_12(
    symbol: str,
    end_date: Optional[str] = None,
    count: Optional[int] = None,
    cache_dir: str = "stock_cache",
    force_update: bool = False,
    **kwargs,
) -> Union[float, pd.Series]:
    """计算 RSI12（12日相对强弱指标）因子。"""
    return compute_rsi(
        symbol,
        window=12,
        end_date=end_date,
        count=count,
        cache_dir=cache_dir,
        force_update=force_update,
    )


def compute_rsi_14(
    symbol: str,
    end_date: Optional[str] = None,
    count: Optional[int] = None,
    cache_dir: str = "stock_cache",
    force_update: bool = False,
    **kwargs,
) -> Union[float, pd.Series]:
    """计算 RSI14（14日相对强弱指标）因子。"""
    return compute_rsi(
        symbol,
        window=14,
        end_date=end_date,
        count=count,
        cache_dir=cache_dir,
        force_update=force_update,
    )


def compute_rsi_24(
    symbol: str,
    end_date: Optional[str] = None,
    count: Optional[int] = None,
    cache_dir: str = "stock_cache",
    force_update: bool = False,
    **kwargs,
) -> Union[float, pd.Series]:
    """计算 RSI24（24日相对强弱指标）因子。"""
    return compute_rsi(
        symbol,
        window=24,
        end_date=end_date,
        count=count,
        cache_dir=cache_dir,
        force_update=force_update,
    )


# -----------------------------------------------------------------
# KDJ（随机指标）
# -----------------------------------------------------------------


def compute_kdj(
    symbol: str,
    n: int = 9,
    m1: int = 3,
    m2: int = 3,
    end_date: Optional[str] = None,
    count: Optional[int] = None,
    cache_dir: str = "stock_cache",
    force_update: bool = False,
    **kwargs,
) -> Dict[str, Union[float, pd.Series]]:
    """
    计算 KDJ（随机指标）因子。

    公式：
    - RSV = (Close - Min(Low, n)) / (Max(High, n) - Min(Low, n)) * 100
    - K = SMA(RSV, m1)
    - D = SMA(K, m2)
    - J = 3 * K - 2 * D

    返回：{'K': ..., 'D': ..., 'J': ...}
    """
    need_count = count + n + m1 + m2 if count else n + m1 + m2 + 10
    df = _get_daily_ohlcv(
        symbol,
        end_date=end_date,
        cache_dir=cache_dir,
        force_update=force_update,
        count=need_count,
    )

    if df.empty or "close" not in df.columns:
        return {"K": np.nan, "D": np.nan, "J": np.nan}

    df = df.set_index("date")
    high = df["high"].astype(float)
    low = df["low"].astype(float)
    close = df["close"].astype(float)

    # 计算RSV
    low_n = low.rolling(window=n, min_periods=n).min()
    high_n = high.rolling(window=n, min_periods=n).max()

    rsv = safe_divide(close - low_n, high_n - low_n) * 100

    # 计算K值（使用EMA近似SMA）
    k = rsv.ewm(span=m1, adjust=False).mean()

    # 计算D值
    d = k.ewm(span=m2, adjust=False).mean()

    # 计算J值
    j = 3 * k - 2 * d

    if count is not None and count > 0:
        k = k.tail(count)
        d = d.tail(count)
        j = j.tail(count)

    if len(k) == 1:
        return {
            "K": float(k.iloc[-1]),
            "D": float(d.iloc[-1]),
            "J": float(j.iloc[-1]),
        }

    return {"K": k, "D": d, "J": j}


def compute_kdj_k(
    symbol: str,
    end_date: Optional[str] = None,
    count: Optional[int] = None,
    cache_dir: str = "stock_cache",
    force_update: bool = False,
    **kwargs,
) -> Union[float, pd.Series]:
    """计算 KDJ_K（KDJ指标中的K值）因子。"""
    result = compute_kdj(
        symbol,
        n=9,
        m1=3,
        m2=3,
        end_date=end_date,
        count=count,
        cache_dir=cache_dir,
        force_update=force_update,
    )
    return result["K"]


def compute_kdj_d(
    symbol: str,
    end_date: Optional[str] = None,
    count: Optional[int] = None,
    cache_dir: str = "stock_cache",
    force_update: bool = False,
    **kwargs,
) -> Union[float, pd.Series]:
    """计算 KDJ_D（KDJ指标中的D值）因子。"""
    result = compute_kdj(
        symbol,
        n=9,
        m1=3,
        m2=3,
        end_date=end_date,
        count=count,
        cache_dir=cache_dir,
        force_update=force_update,
    )
    return result["D"]


def compute_kdj_j(
    symbol: str,
    end_date: Optional[str] = None,
    count: Optional[int] = None,
    cache_dir: str = "stock_cache",
    force_update: bool = False,
    **kwargs,
) -> Union[float, pd.Series]:
    """计算 KDJ_J（KDJ指标中的J值）因子。"""
    result = compute_kdj(
        symbol,
        n=9,
        m1=3,
        m2=3,
        end_date=end_date,
        count=count,
        cache_dir=cache_dir,
        force_update=force_update,
    )
    return result["J"]


# -----------------------------------------------------------------
# BOLL_WIDTH（布林带宽度）
# -----------------------------------------------------------------


def compute_boll_width(
    symbol: str,
    window: int = 20,
    num_std: float = 2.0,
    end_date: Optional[str] = None,
    count: Optional[int] = None,
    cache_dir: str = "stock_cache",
    force_update: bool = False,
    **kwargs,
) -> Union[float, pd.Series]:
    """
    计算 BOLL_WIDTH（布林带宽度）因子。

    公式：(boll_up - boll_down) / boll_mid
    反映波动率收窄/扩张程度

    Parameters
    ----------
    symbol : str
        股票代码
    window : int
        计算窗口
    num_std : float
        标准差倍数

    Returns
    -------
    float or pd.Series
        布林带宽度
    """
    need_count = count + window if count else window + 10
    df = _get_daily_ohlcv(
        symbol,
        end_date=end_date,
        cache_dir=cache_dir,
        force_update=force_update,
        count=need_count,
    )

    if df.empty or "close" not in df.columns:
        return np.nan

    df = df.set_index("date")
    close = df["close"].astype(float)

    ma = _compute_ma(close, window)
    std = _compute_std(close, window)

    boll_up = ma + num_std * std
    boll_down = ma - num_std * std

    boll_width = safe_divide(boll_up - boll_down, ma)

    if count is not None and count > 0:
        boll_width = boll_width.tail(count)

    if len(boll_width) == 1:
        return float(boll_width.iloc[-1])
    return boll_width


# -----------------------------------------------------------------
# VOL_RATIO（量比）
# -----------------------------------------------------------------


def compute_vol_ratio(
    symbol: str,
    window: int = 5,
    end_date: Optional[str] = None,
    count: Optional[int] = None,
    cache_dir: str = "stock_cache",
    force_update: bool = False,
    **kwargs,
) -> Union[float, pd.Series]:
    """
    计算 VOL_RATIO（量比）因子。

    公式：当日成交量 / N日平均成交量
    反映当前成交量的相对大小

    Parameters
    ----------
    symbol : str
        股票代码
    window : int
        均量计算窗口（默认5日）

    Returns
    -------
    float or pd.Series
        量比
    """
    need_count = count + window + 1 if count else window + 11
    df = _get_daily_ohlcv(
        symbol,
        end_date=end_date,
        cache_dir=cache_dir,
        force_update=force_update,
        count=need_count,
    )

    if df.empty or "volume" not in df.columns:
        return np.nan

    df = df.set_index("date")
    volume = df["volume"].astype(float)

    # N日平均成交量（不包含当日）
    avg_vol = volume.shift(1).rolling(window=window, min_periods=window).mean()

    vol_ratio = safe_divide(volume, avg_vol)

    if count is not None and count > 0:
        vol_ratio = vol_ratio.tail(count)

    if len(vol_ratio) == 1:
        return float(vol_ratio.iloc[-1])
    return vol_ratio


# -----------------------------------------------------------------
# VWAP（成交量加权均价）
# -----------------------------------------------------------------


def compute_vwap(
    symbol: str,
    window: int = 20,
    end_date: Optional[str] = None,
    count: Optional[int] = None,
    cache_dir: str = "stock_cache",
    force_update: bool = False,
    **kwargs,
) -> Union[float, pd.Series]:
    """
    计算 VWAP（成交量加权均价）因子。

    公式：Σ(close * volume) / Σ(volume)
    反映平均成交价格

    Parameters
    ----------
    symbol : str
        股票代码
    window : int
        计算窗口

    Returns
    -------
    float or pd.Series
        VWAP
    """
    need_count = count + window if count else window + 10
    df = _get_daily_ohlcv(
        symbol,
        end_date=end_date,
        cache_dir=cache_dir,
        force_update=force_update,
        count=need_count,
    )

    if df.empty or "volume" not in df.columns:
        return np.nan

    df = df.set_index("date")
    close = df["close"].astype(float)
    volume = df["volume"].astype(float)

    # 计算VWAP
    tp_volume = close * volume
    vwap = safe_divide(
        tp_volume.rolling(window=window, min_periods=window).sum(),
        volume.rolling(window=window, min_periods=window).sum()
    )

    if count is not None and count > 0:
        vwap = vwap.tail(count)

    if len(vwap) == 1:
        return float(vwap.iloc[-1])
    return vwap


# -----------------------------------------------------------------
# OBV（能量潮指标）
# -----------------------------------------------------------------


def compute_obv(
    symbol: str,
    end_date: Optional[str] = None,
    count: Optional[int] = None,
    cache_dir: str = "stock_cache",
    force_update: bool = False,
    **kwargs,
) -> Union[float, pd.Series]:
    """
    计算 OBV（能量潮指标）因子。

    公式：OBV = 前一日OBV + 今日成交量（上涨加，下跌减）
    反映资金流向

    Parameters
    ----------
    symbol : str
        股票代码

    Returns
    -------
    float or pd.Series
        OBV累计值
    """
    need_count = count + 20 if count else 30
    df = _get_daily_ohlcv(
        symbol,
        end_date=end_date,
        cache_dir=cache_dir,
        force_update=force_update,
        count=need_count,
    )

    if df.empty or "volume" not in df.columns:
        return np.nan

    df = df.set_index("date")
    close = df["close"].astype(float)
    volume = df["volume"].astype(float)

    # 计算OBV
    obv = pd.Series(0.0, index=close.index)
    obv.iloc[0] = volume.iloc[0]

    for i in range(1, len(close)):
        if close.iloc[i] > close.iloc[i - 1]:
            obv.iloc[i] = obv.iloc[i - 1] + volume.iloc[i]
        elif close.iloc[i] < close.iloc[i - 1]:
            obv.iloc[i] = obv.iloc[i - 1] - volume.iloc[i]
        else:
            obv.iloc[i] = obv.iloc[i - 1]

    if count is not None and count > 0:
        obv = obv.tail(count)

    if len(obv) == 1:
        return float(obv.iloc[-1])
    return obv


# -----------------------------------------------------------------
# AMOUNT_RATIO（换手率比）
# -----------------------------------------------------------------


def compute_amount_ratio(
    symbol: str,
    window: int = 5,
    end_date: Optional[str] = None,
    count: Optional[int] = None,
    cache_dir: str = "stock_cache",
    force_update: bool = False,
    **kwargs,
) -> Union[float, pd.Series]:
    """
    计算 AMOUNT_RATIO（换手率比）因子。

    公式：当日换手率 / N日平均换手率
    反映当前换手活跃程度

    Parameters
    ----------
    symbol : str
        股票代码
    window : int
        均值计算窗口

    Returns
    -------
    float or pd.Series
        换手率比
    """
    need_count = count + window + 1 if count else window + 11
    df = _get_daily_ohlcv(
        symbol,
        end_date=end_date,
        cache_dir=cache_dir,
        force_update=force_update,
        count=need_count,
    )

    if df.empty or "turnover_rate" not in df.columns:
        return np.nan

    df = df.set_index("date")
    turnover = df["turnover_rate"].astype(float)

    # N日平均换手率
    avg_turnover = turnover.shift(1).rolling(window=window, min_periods=window).mean()

    amount_ratio = safe_divide(turnover, avg_turnover)

    if count is not None and count > 0:
        amount_ratio = amount_ratio.tail(count)

    if len(amount_ratio) == 1:
        return float(amount_ratio.iloc[-1])
    return amount_ratio


# =====================================================================
# 注册因子
# =====================================================================


def _register_factors():
    """向全局注册表注册技术因子。"""
    registry = global_factor_registry

    # BIAS
    registry.register("bias_5", compute_bias_5, window=5, dependencies=["daily_ohlcv"])
    registry.register(
        "bias_10", compute_bias_10, window=10, dependencies=["daily_ohlcv"]
    )
    registry.register(
        "bias_20", compute_bias_20, window=20, dependencies=["daily_ohlcv"]
    )
    registry.register(
        "bias_60", compute_bias_60, window=60, dependencies=["daily_ohlcv"]
    )

    # EMAC
    registry.register(
        "emac_10", compute_emac_10, window=10, dependencies=["daily_ohlcv"]
    )
    registry.register(
        "emac_20", compute_emac_20, window=20, dependencies=["daily_ohlcv"]
    )
    registry.register(
        "emac_26", compute_emac_26, window=26, dependencies=["daily_ohlcv"]
    )
    registry.register(
        "emac_60", compute_emac_60, window=60, dependencies=["daily_ohlcv"]
    )

    # ROC
    registry.register("roc_6", compute_roc_6, window=6, dependencies=["daily_ohlcv"])
    registry.register("roc_12", compute_roc_12, window=12, dependencies=["daily_ohlcv"])
    registry.register("roc_20", compute_roc_20, window=20, dependencies=["daily_ohlcv"])
    registry.register("roc_60", compute_roc_60, window=60, dependencies=["daily_ohlcv"])
    registry.register(
        "roc_120", compute_roc_120, window=120, dependencies=["daily_ohlcv"]
    )

    # MAC
    registry.register("mac_60", compute_mac_60, window=60, dependencies=["daily_ohlcv"])
    registry.register(
        "mac_120", compute_mac_120, window=120, dependencies=["daily_ohlcv"]
    )

    # VOL
    registry.register("vol_5", compute_vol_5, window=5, dependencies=["daily_ohlcv"])
    registry.register("vol_10", compute_vol_10, window=10, dependencies=["daily_ohlcv"])
    registry.register("vol_20", compute_vol_20, window=20, dependencies=["daily_ohlcv"])
    registry.register("vol_60", compute_vol_60, window=60, dependencies=["daily_ohlcv"])
    registry.register(
        "vol_120", compute_vol_120, window=120, dependencies=["daily_ohlcv"]
    )
    registry.register(
        "vol_240", compute_vol_240, window=240, dependencies=["daily_ohlcv"]
    )

    # DAVOL
    registry.register(
        "davol_5", compute_davol_5, window=5, dependencies=["daily_ohlcv"]
    )
    registry.register(
        "davol_10", compute_davol_10, window=10, dependencies=["daily_ohlcv"]
    )
    registry.register(
        "davol_20", compute_davol_20, window=20, dependencies=["daily_ohlcv"]
    )

    # VSTD
    registry.register(
        "vstd_10", compute_vstd_10, window=10, dependencies=["daily_ohlcv"]
    )
    registry.register(
        "vstd_20", compute_vstd_20, window=20, dependencies=["daily_ohlcv"]
    )

    # VROC
    registry.register("vroc_6", compute_vroc_6, window=6, dependencies=["daily_ohlcv"])
    registry.register(
        "vroc_12", compute_vroc_12, window=12, dependencies=["daily_ohlcv"]
    )

    # VEMA
    registry.register("vema_5", compute_vema_5, window=5, dependencies=["daily_ohlcv"])
    registry.register(
        "vema_10", compute_vema_10, window=10, dependencies=["daily_ohlcv"]
    )
    registry.register(
        "vema_12", compute_vema_12, window=12, dependencies=["daily_ohlcv"]
    )
    registry.register(
        "vema_26", compute_vema_26, window=26, dependencies=["daily_ohlcv"]
    )

    # VOSC
    registry.register("vosc", compute_vosc, window=26, dependencies=["daily_ohlcv"])

    # TVMA / TVSTD
    registry.register("tvma_6", compute_tvma_6, window=6, dependencies=["daily_ohlcv"])
    registry.register(
        "tvma_20", compute_tvma_20, window=20, dependencies=["daily_ohlcv"]
    )
    registry.register(
        "tvstd_6", compute_tvstd_6, window=6, dependencies=["daily_ohlcv"]
    )
    registry.register(
        "tvstd_20", compute_tvstd_20, window=20, dependencies=["daily_ohlcv"]
    )

    # CCI
    registry.register("cci_10", compute_cci_10, window=10, dependencies=["daily_ohlcv"])
    registry.register("cci_15", compute_cci_15, window=15, dependencies=["daily_ohlcv"])
    registry.register("cci_20", compute_cci_20, window=20, dependencies=["daily_ohlcv"])
    registry.register("cci_88", compute_cci_88, window=88, dependencies=["daily_ohlcv"])

    # AR / BR
    registry.register("ar", compute_ar, window=26, dependencies=["daily_ohlcv"])
    registry.register("br", compute_br, window=26, dependencies=["daily_ohlcv"])
    registry.register("arbr", compute_arbr, window=26, dependencies=["daily_ohlcv"])

    # WVAD
    registry.register("wvad", compute_wvad, window=6, dependencies=["daily_ohlcv"])
    registry.register("mawvad", compute_mawvad, window=6, dependencies=["daily_ohlcv"])

    # PSY
    registry.register("psy", compute_psy, window=12, dependencies=["daily_ohlcv"])

    # VR
    registry.register("vr", compute_vr, window=26, dependencies=["daily_ohlcv"])

    # MACD
    registry.register("macd", compute_macd, window=35, dependencies=["daily_ohlcv"])

    # MFI
    registry.register("mfi_14", compute_mfi_14, window=14, dependencies=["daily_ohlcv"])

    # money_flow
    registry.register(
        "money_flow_20", compute_money_flow_20, window=20, dependencies=["daily_ohlcv"]
    )

    # Price_NM
    registry.register(
        "price_1m", compute_price_1m, window=21, dependencies=["daily_ohlcv"]
    )
    registry.register(
        "price_3m", compute_price_3m, window=61, dependencies=["daily_ohlcv"]
    )
    registry.register(
        "price_1y", compute_price_1y, window=250, dependencies=["daily_ohlcv"]
    )

    # PLRC
    registry.register("plrc_6", compute_plrc_6, window=6, dependencies=["daily_ohlcv"])
    registry.register(
        "plrc_12", compute_plrc_12, window=12, dependencies=["daily_ohlcv"]
    )
    registry.register(
        "plrc_24", compute_plrc_24, window=24, dependencies=["daily_ohlcv"]
    )

    # Aroon
    registry.register(
        "aroon_up", compute_aroon_up, window=25, dependencies=["daily_ohlcv"]
    )
    registry.register(
        "aroon_down", compute_aroon_down, window=25, dependencies=["daily_ohlcv"]
    )

    # 52周价格位置
    registry.register(
        "fifty_two_week_close_rank",
        compute_fifty_two_week_close_rank,
        window=250,
        dependencies=["daily_ohlcv"],
    )

    # Bull/Bear Power
    registry.register(
        "bull_power", compute_bull_power, window=13, dependencies=["daily_ohlcv"]
    )
    registry.register(
        "bear_power", compute_bear_power, window=13, dependencies=["daily_ohlcv"]
    )

    # BBIC
    registry.register("bbic", compute_bbic, window=24, dependencies=["daily_ohlcv"])

    # Volume1M
    registry.register(
        "volume_1m", compute_volume_1m, window=20, dependencies=["daily_ohlcv"]
    )

    # VPT
    registry.register(
        "single_day_vpt", compute_single_day_vpt, window=1, dependencies=["daily_ohlcv"]
    )
    registry.register(
        "single_day_vpt_6",
        compute_single_day_vpt_6,
        window=6,
        dependencies=["daily_ohlcv"],
    )
    registry.register(
        "single_day_vpt_12",
        compute_single_day_vpt_12,
        window=12,
        dependencies=["daily_ohlcv"],
    )

    # TRIX
    registry.register("trix_5", compute_trix_5, window=15, dependencies=["daily_ohlcv"])
    registry.register(
        "trix_10", compute_trix_10, window=30, dependencies=["daily_ohlcv"]
    )

    # 换手率
    registry.register(
        "average_share_turnover_annual",
        compute_average_share_turnover_annual,
        window=240,
        dependencies=["daily_ohlcv"],
    )
    registry.register(
        "share_turnover_monthly",
        compute_share_turnover_monthly,
        window=20,
        dependencies=["daily_ohlcv"],
    )

    # 布林带
    registry.register(
        "boll_up", compute_boll_up, window=20, dependencies=["daily_ohlcv"]
    )
    registry.register(
        "boll_down", compute_boll_down, window=20, dependencies=["daily_ohlcv"]
    )

    # ATR
    registry.register("atr_6", compute_atr_6, window=6, dependencies=["daily_ohlcv"])
    registry.register("atr_14", compute_atr_14, window=14, dependencies=["daily_ohlcv"])

    # Variance
    registry.register(
        "variance_20", compute_variance_20, window=20, dependencies=["daily_ohlcv"]
    )
    registry.register(
        "variance_60", compute_variance_60, window=60, dependencies=["daily_ohlcv"]
    )
    registry.register(
        "variance_120", compute_variance_120, window=120, dependencies=["daily_ohlcv"]
    )

    # Skewness
    registry.register(
        "skewness_20", compute_skewness_20, window=20, dependencies=["daily_ohlcv"]
    )
    registry.register(
        "skewness_60", compute_skewness_60, window=60, dependencies=["daily_ohlcv"]
    )
    registry.register(
        "skewness_120", compute_skewness_120, window=120, dependencies=["daily_ohlcv"]
    )

    # Kurtosis
    registry.register(
        "kurtosis_20", compute_kurtosis_20, window=20, dependencies=["daily_ohlcv"]
    )
    registry.register(
        "kurtosis_60", compute_kurtosis_60, window=60, dependencies=["daily_ohlcv"]
    )
    registry.register(
        "kurtosis_120", compute_kurtosis_120, window=120, dependencies=["daily_ohlcv"]
    )

    # Sharpe Ratio
    registry.register(
        "sharpe_ratio_20",
        compute_sharpe_ratio_20,
        window=20,
        dependencies=["daily_ohlcv"],
    )
    registry.register(
        "sharpe_ratio_60",
        compute_sharpe_ratio_60,
        window=60,
        dependencies=["daily_ohlcv"],
    )
    registry.register(
        "sharpe_ratio_120",
        compute_sharpe_ratio_120,
        window=120,
        dependencies=["daily_ohlcv"],
    )

    # CR
    registry.register("cr_20", compute_cr_20, window=20, dependencies=["daily_ohlcv"])

    # RSI
    registry.register("rsi_6", compute_rsi_6, window=6, dependencies=["daily_ohlcv"])
    registry.register("rsi_12", compute_rsi_12, window=12, dependencies=["daily_ohlcv"])
    registry.register("rsi_14", compute_rsi_14, window=14, dependencies=["daily_ohlcv"])
    registry.register("rsi_24", compute_rsi_24, window=24, dependencies=["daily_ohlcv"])

    # KDJ
    registry.register("kdj_k", compute_kdj_k, window=9, dependencies=["daily_ohlcv"])
    registry.register("kdj_d", compute_kdj_d, window=9, dependencies=["daily_ohlcv"])
    registry.register("kdj_j", compute_kdj_j, window=9, dependencies=["daily_ohlcv"])

    # BOLL_WIDTH
    registry.register("boll_width", compute_boll_width, window=20, dependencies=["daily_ohlcv"])

    # VOL_RATIO
    registry.register("vol_ratio", compute_vol_ratio, window=5, dependencies=["daily_ohlcv"])

    # VWAP
    registry.register("vwap", compute_vwap, window=20, dependencies=["daily_ohlcv"])

    # OBV
    registry.register("obv", compute_obv, window=20, dependencies=["daily_ohlcv"])

    # AMOUNT_RATIO
    registry.register("amount_ratio", compute_amount_ratio, window=5, dependencies=["daily_ohlcv"])


# 模块加载时自动注册
_register_factors()


# =====================================================================
# 模块导出
# =====================================================================

__all__ = [
    "compute_bias_5",
    "compute_bias_10",
    "compute_bias_20",
    "compute_bias_60",
    "compute_emac_10",
    "compute_emac_20",
    "compute_emac_26",
    "compute_emac_60",
    "compute_roc_6",
    "compute_roc_12",
    "compute_roc_20",
    "compute_roc_60",
    "compute_roc_120",
    "compute_mac_60",
    "compute_mac_120",
    "compute_vol_5",
    "compute_vol_10",
    "compute_vol_20",
    "compute_vol_60",
    "compute_vol_120",
    "compute_vol_240",
    "compute_davol_5",
    "compute_davol_10",
    "compute_davol_20",
    "compute_vstd_10",
    "compute_vstd_20",
    "compute_vroc_6",
    "compute_vroc_12",
    "compute_vema_5",
    "compute_vema_10",
    "compute_vema_12",
    "compute_vema_26",
    "compute_vosc",
    "compute_tvma_6",
    "compute_tvma_20",
    "compute_tvstd_6",
    "compute_tvstd_20",
    "compute_cci_10",
    "compute_cci_15",
    "compute_cci_20",
    "compute_cci_88",
    "compute_ar",
    "compute_br",
    "compute_arbr",
    "compute_wvad",
    "compute_mawvad",
    "compute_psy",
    "compute_vr",
    "compute_macd",
    "compute_mfi_14",
    "compute_money_flow_20",
    "compute_price_1m",
    "compute_price_3m",
    "compute_price_1y",
    "compute_plrc_6",
    "compute_plrc_12",
    "compute_plrc_24",
    "compute_aroon_up",
    "compute_aroon_down",
    "compute_fifty_two_week_close_rank",
    "compute_bull_power",
    "compute_bear_power",
    "compute_bbic",
    "compute_volume_1m",
    "compute_single_day_vpt",
    "compute_single_day_vpt_6",
    "compute_single_day_vpt_12",
    "compute_trix_5",
    "compute_trix_10",
    "compute_average_share_turnover_annual",
    "compute_share_turnover_monthly",
    "compute_boll_up",
    "compute_boll_down",
    "compute_atr_6",
    "compute_atr_14",
    "compute_variance_20",
    "compute_variance_60",
    "compute_variance_120",
    "compute_skewness_20",
    "compute_skewness_60",
    "compute_skewness_120",
    "compute_kurtosis_20",
    "compute_kurtosis_60",
    "compute_kurtosis_120",
    "compute_sharpe_ratio_20",
    "compute_sharpe_ratio_60",
    "compute_sharpe_ratio_120",
    "compute_cr_20",
    "compute_rsi_6",
    "compute_rsi_12",
    "compute_rsi_14",
    "compute_rsi_24",
    "compute_kdj_k",
    "compute_kdj_d",
    "compute_kdj_j",
    # 新增因子
    "compute_boll_width",
    "compute_vol_ratio",
    "compute_vwap",
    "compute_obv",
    "compute_amount_ratio",
]
