"""
factors/valuation.py
估值因子模块。

实现：
- market_cap                总市值
- circulating_market_cap    流通市值
- pe_ratio                  市盈率
- pb_ratio                  市净率
- ps_ratio                  市销率
- natural_log_of_market_cap 市值对数
- cube_of_size              规模立方（衍生）

数据来源策略：
1. 总市值/市净率：AkShare stock_zh_valuation_baidu（可用）
2. 流通市值：从日线数据换手率推算（换手率=成交量/流通股本）
3. 市盈率/市销率：暂不可用，返回NaN

稳定性保障：
- 多数据源备选
- 异常值检测和清理
- 缓存机制
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


def _normalize_symbol(symbol: str) -> str:
    """标准化股票代码为6位数字格式。"""
    ak_sym = symbol
    if symbol.startswith("sh") or symbol.startswith("sz"):
        ak_sym = symbol[2:]
    if symbol.endswith(".XSHG") or symbol.endswith(".XSHE"):
        ak_sym = symbol[:6]
    return ak_sym.zfill(6)


def _validate_valuation_data(df: pd.DataFrame, symbol: str) -> Dict:
    """
    验证估值数据质量。

    Parameters
    ----------
    df : pd.DataFrame
        估值数据
    symbol : str
        股票代码

    Returns
    -------
    dict
        包含 is_valid, issues, message 等字段
    """
    result = {
        "is_valid": True,
        "issues": [],
        "message": "",
        "data_count": len(df) if df is not None else 0,
        "missing_rate": {},
    }

    if df is None or df.empty:
        result["is_valid"] = False
        result["issues"].append("empty_data")
        result["message"] = f"{symbol}: 数据为空"
        return result

    required_cols = ["pe_ratio", "pb_ratio", "market_cap"]
    for col in required_cols:
        if col in df.columns:
            missing_rate = df[col].isna().sum() / len(df)
            result["missing_rate"][col] = missing_rate
            if missing_rate > 0.5:
                result["issues"].append(f"high_missing_{col}")
                result["is_valid"] = False
        else:
            result["issues"].append(f"missing_col_{col}")

    if "pe_ratio" in df.columns:
        pe = df["pe_ratio"].dropna()
        if len(pe) > 0:
            negative_pe_count = (pe < 0).sum()
            extreme_pe_count = (pe > 500).sum()
            if negative_pe_count > len(pe) * 0.3:
                result["issues"].append("excessive_negative_pe")
            if extreme_pe_count > len(pe) * 0.1:
                result["issues"].append("excessive_extreme_pe")

    if "pb_ratio" in df.columns:
        pb = df["pb_ratio"].dropna()
        if len(pb) > 0:
            invalid_pb_count = ((pb < -5) | (pb > 50)).sum()
            if invalid_pb_count > len(pb) * 0.1:
                result["issues"].append("invalid_pb_range")

    if "market_cap" in df.columns:
        mc = df["market_cap"].dropna()
        if len(mc) > 0:
            zero_mc_count = (mc <= 0).sum()
            if zero_mc_count > 0:
                result["issues"].append("zero_market_cap")

    if result["issues"]:
        result["message"] = f"{symbol}: 发现 {len(result['issues'])} 个数据质量问题"
        warnings.warn(result["message"])

    return result


def _clean_valuation_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    清理估值数据中的异常值。

    Parameters
    ----------
    df : pd.DataFrame
        原始估值数据

    Returns
    -------
    pd.DataFrame
        清理后的数据
    """
    if df is None or df.empty:
        return df

    df = df.copy()

    if "pe_ratio" in df.columns:
        df.loc[df["pe_ratio"] < -100, "pe_ratio"] = np.nan
        df.loc[df["pe_ratio"] > 1000, "pe_ratio"] = np.nan

    if "pb_ratio" in df.columns:
        df.loc[df["pb_ratio"] < -10, "pb_ratio"] = np.nan
        df.loc[df["pb_ratio"] > 100, "pb_ratio"] = np.nan

    if "market_cap" in df.columns:
        df.loc[df["market_cap"] <= 0, "market_cap"] = np.nan

    if "circulating_market_cap" in df.columns:
        df.loc[df["circulating_market_cap"] <= 0, "circulating_market_cap"] = np.nan

    return df


def _fetch_valuation_from_baidu(ak: object, ak_sym: str) -> pd.DataFrame:
    """
    从 stock_zh_valuation_baidu 接口获取估值数据。

    实际可用指标：总市值、市净率
    其他指标（流通市值、市盈率、市销率）接口不支持。
    """
    dfs = []

    # 已验证可用的指标
    available_indicators = {
        "总市值": "market_cap",
        "市净率": "pb_ratio",
    }

    for indicator, col_name in available_indicators.items():
        try:
            df_tmp = ak.stock_zh_valuation_baidu(symbol=ak_sym, indicator=indicator)
            if df_tmp is not None and not df_tmp.empty:
                df_tmp = df_tmp.rename(columns={"value": col_name})
                dfs.append(df_tmp)
        except Exception:
            continue

    if not dfs:
        return pd.DataFrame()

    from functools import reduce

    df = reduce(lambda x, y: pd.merge(x, y, on="date", how="outer"), dfs)
    return df if df is not None else pd.DataFrame()


def _estimate_circulating_market_cap_from_daily(
    symbol: str,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
) -> pd.DataFrame:
    """
    从日线数据推算流通市值。

    原理：
    - AkShare成交量单位是手（每手100股）
    - 换手率(%) = 成交量(手)*100 / 流通股本(股) * 100
    - 流通股本(股) = 成交量(手)*100 / 换手率(%) * 100
    - 流通市值(亿元) = 流通股本(股) * 收盘价 / 1e8

    数据源优先级：
    1. market_data.stock.get_stock_daily（DuckDB 缓存 + 多数据源备份）
    2. akshare.stock_zh_a_hist（直接获取）
    """
    # 标准化代码
    ak_sym = _normalize_symbol(symbol)

    # 优先尝试使用 market_data 模块
    try:
        from ..market_data.stock import get_stock_daily

        # 设置默认日期范围
        if start_date is None:
            start_date = "20100101"
        if end_date is None:
            end_date = pd.Timestamp.now().strftime("%Y-%m-%d")

        df = get_stock_daily(
            symbol=symbol,
            start=start_date,
            end=end_date,
            adjust="qfq",
        )

        if df is not None and not df.empty:
            # market_data 返回的数据格式是 datetime, open, high, low, close, volume
            df = df.copy()
            if "datetime" in df.columns:
                df["date"] = pd.to_datetime(df["datetime"]).dt.strftime("%Y-%m-%d")
            df["close"] = df["close"].astype(float)
            df["volume"] = df["volume"].astype(float)

            # market_data 可能没有换手率，需要额外获取或使用默认值
            if "turnover_rate" not in df.columns:
                # 尝试从 akshare 获取换手率
                try:
                    import akshare as ak
                    df_ak = ak.stock_zh_a_hist(symbol=ak_sym, period="daily", adjust="qfq")
                    if df_ak is not None and "换手率" in df_ak.columns:
                        # 合并换手率数据
                        df_ak = df_ak.rename(columns={"日期": "date"})
                        df_ak["date"] = pd.to_datetime(df_ak["date"]).dt.strftime("%Y-%m-%d")
                        df_ak["turnover_rate"] = df_ak["换手率"]  # 百分比形式
                        df = df.merge(df_ak[["date", "turnover_rate"]], on="date", how="left")
                except Exception:
                    df["turnover_rate"] = np.nan

            if "turnover_rate" in df.columns:
                # 成交量单位是手，换手率单位是%
                # 流通股本(股) = 成交量(手) * 100 / (换手率% / 100) = 成交量(手) * 10000 / 换手率%
                # 流通市值(亿) = 流通股本(股) * 收盘价 / 1e8 = 成交量(手) * 100 * 收盘价 / 换手率% / 1e8
                df["circulating_market_cap"] = (
                    safe_divide(df["volume"] * 100 * df["close"], df["turnover_rate"]) / 1e8
                )

                return df[["date", "circulating_market_cap"]]

    except ImportError:
        pass  # market_data 模块不可用，fallback 到 akshare
    except Exception as e:
        warnings.warn(f"market_data 模块获取数据失败 {symbol}: {e}，fallback 到 akshare")

    # Fallback: 使用 akshare 直接获取
    try:
        import akshare as ak
    except ImportError:
        raise ImportError("请安装 akshare: pip install akshare")

    try:
        df = ak.stock_zh_a_hist(symbol=ak_sym, period="daily", adjust="qfq")
        if df is None or df.empty:
            return pd.DataFrame()

        df = df.rename(
            columns={
                "日期": "date",
                "收盘": "close",
                "成交量": "volume",
                "换手率": "turnover_rate",
            }
        )

        # 成交量单位是手，换手率单位是%
        # 流通股本(股) = 成交量(手) * 100 / (换手率% / 100) = 成交量(手) * 10000 / 换手率%
        # 流通市值(亿) = 流通股本(股) * 收盘价 / 1e8 = 成交量(手) * 100 * 收盘价 / 换手率% / 1e8
        df["circulating_market_cap"] = (
            safe_divide(df["volume"] * 100 * df["close"], df["turnover_rate"]) / 1e8
        )

        return df[["date", "circulating_market_cap"]]
    except Exception as e:
        warnings.warn(f"推算流通市值失败 {ak_sym}: {e}")
        return pd.DataFrame()


def _get_valuation_raw(
    symbol: str, cache_dir: str = "stock_cache", force_update: bool = False
) -> pd.DataFrame:
    """
    获取估值原始数据。

    数据获取策略：
    1. 从 stock_zh_valuation_baidu 获取总市值、市净率
    2. 从日线数据推算流通市值

    Parameters
    ----------
    symbol : str
        证券代码，如 'sh600519'
    cache_dir : str
        缓存目录
    force_update : bool
        是否强制更新

    Returns
    -------
    pd.DataFrame
        估值数据表，包含 market_cap, pb_ratio, circulating_market_cap 等字段
    """
    import os

    try:
        import akshare as ak
    except ImportError:
        raise ImportError("请安装 akshare: pip install akshare")

    ak_sym = _normalize_symbol(symbol)
    cache_file = os.path.join(cache_dir, f"{symbol}_valuation.pkl")
    os.makedirs(cache_dir, exist_ok=True)

    need_dl = force_update or not os.path.exists(cache_file)
    if not need_dl:
        try:
            df = pd.read_pickle(cache_file)
            return df
        except Exception:
            need_dl = True

    if need_dl:
        # 1. 获取估值数据（总市值、市净率）- 使用 akshare
        try:
            import akshare as ak
            df_val = _fetch_valuation_from_baidu(ak, ak_sym)
        except Exception as e:
            warnings.warn(f"获取百度估值数据失败 {symbol}: {e}")
            df_val = pd.DataFrame()

        # 2. 推算流通市值 - 优先使用 market_data 模块
        df_circ = _estimate_circulating_market_cap_from_daily(symbol)

        # 3. 合并数据
        if df_val.empty and df_circ.empty:
            warnings.warn(f"获取估值数据失败 {symbol}: 所有数据源均不可用")
            return pd.DataFrame()

        if df_val.empty:
            df = df_circ
        elif df_circ.empty:
            df = df_val
        else:
            df = pd.merge(df_val, df_circ, on="date", how="outer")

        if not df.empty:
            # 数据质量检查
            validation = _validate_valuation_data(df, symbol)

            # 数据清理
            df = _clean_valuation_data(df)

            df.to_pickle(cache_file)
            return df

    return pd.DataFrame()


def _normalize_valuation_df(df: pd.DataFrame) -> pd.DataFrame:
    """
    标准化估值数据字段名。

    Parameters
    ----------
    df : pd.DataFrame
        原始数据

    Returns
    -------
    pd.DataFrame
        标准化后数据
    """
    if df is None or df.empty:
        return pd.DataFrame()

    df = df.copy()

    # 日期列标准化
    date_col = find_date_column(df, "market")
    if date_col:
        df["date"] = pd.to_datetime(df[date_col]).dt.strftime("%Y-%m-%d")
    else:
        df["date"] = pd.NaT

    # 字段映射
    col_map = {
        "market_cap": "market_cap",
        "circulating_market_cap": "circulating_market_cap",
        "pb_ratio": "pb_ratio",
        "pb": "pb_ratio",
    }

    for old, new in col_map.items():
        if old in df.columns and new not in df.columns:
            df[new] = df[old]

    # 保留核心列
    keep_cols = [
        "date",
        "pe_ratio",
        "pb_ratio",
        "ps_ratio",
        "market_cap",
        "circulating_market_cap",
    ]
    keep_cols = [c for c in keep_cols if c in df.columns]

    if "date" not in keep_cols:
        return pd.DataFrame()

    return df[keep_cols].sort_values("date").reset_index(drop=True)


# =====================================================================
# 因子计算函数
# =====================================================================


def compute_market_cap(
    symbol: str,
    end_date: Optional[str] = None,
    count: Optional[int] = None,
    cache_dir: str = "stock_cache",
    force_update: bool = False,
    **kwargs,
) -> Union[float, pd.Series]:
    """
    计算 market_cap（总市值）因子。

    Parameters
    ----------
    symbol : str
        证券代码
    end_date : str, optional
        截止日期
    count : int, optional
        窗口长度
    cache_dir : str
        缓存目录
    force_update : bool
        强制更新

    Returns
    -------
    float or pd.Series
        单值或日期序列
    """
    raw = _get_valuation_raw(symbol, cache_dir, force_update)
    df = _normalize_valuation_df(raw)

    if df.empty or "market_cap" not in df.columns:
        return np.nan

    if end_date:
        df = df[df["date"] <= end_date]

    if count is not None and count > 0:
        df = df.tail(count)

    if df.empty:
        return np.nan

    df = df.set_index("date")
    series = df["market_cap"].astype(float)

    if len(series) == 1:
        return float(series.iloc[0])
    return series


def compute_circulating_market_cap(
    symbol: str,
    end_date: Optional[str] = None,
    count: Optional[int] = None,
    cache_dir: str = "stock_cache",
    force_update: bool = False,
    **kwargs,
) -> Union[float, pd.Series]:
    """计算 circulating_market_cap（流通市值）因子。"""
    raw = _get_valuation_raw(symbol, cache_dir, force_update)
    df = _normalize_valuation_df(raw)

    if df.empty or "circulating_market_cap" not in df.columns:
        return np.nan

    if end_date:
        df = df[df["date"] <= end_date]
    if count is not None and count > 0:
        df = df.tail(count)

    if df.empty:
        return np.nan

    df = df.set_index("date")
    series = df["circulating_market_cap"].astype(float)

    if len(series) == 1:
        return float(series.iloc[0])
    return series


def compute_pe_ratio(
    symbol: str,
    end_date: Optional[str] = None,
    count: Optional[int] = None,
    cache_dir: str = "stock_cache",
    force_update: bool = False,
    **kwargs,
) -> Union[float, pd.Series]:
    """计算 pe_ratio（市盈率）因子。"""
    raw = _get_valuation_raw(symbol, cache_dir, force_update)
    df = _normalize_valuation_df(raw)

    if df.empty or "pe_ratio" not in df.columns:
        return np.nan

    if end_date:
        df = df[df["date"] <= end_date]
    if count is not None and count > 0:
        df = df.tail(count)

    if df.empty:
        return np.nan

    df = df.set_index("date")
    series = df["pe_ratio"].astype(float)

    if len(series) == 1:
        return float(series.iloc[0])
    return series


def compute_pb_ratio(
    symbol: str,
    end_date: Optional[str] = None,
    count: Optional[int] = None,
    cache_dir: str = "stock_cache",
    force_update: bool = False,
    **kwargs,
) -> Union[float, pd.Series]:
    """计算 pb_ratio（市净率）因子。"""
    raw = _get_valuation_raw(symbol, cache_dir, force_update)
    df = _normalize_valuation_df(raw)

    if df.empty or "pb_ratio" not in df.columns:
        return np.nan

    if end_date:
        df = df[df["date"] <= end_date]
    if count is not None and count > 0:
        df = df.tail(count)

    if df.empty:
        return np.nan

    df = df.set_index("date")
    series = df["pb_ratio"].astype(float)

    if len(series) == 1:
        return float(series.iloc[0])
    return series


def compute_ps_ratio(
    symbol: str,
    end_date: Optional[str] = None,
    count: Optional[int] = None,
    cache_dir: str = "stock_cache",
    force_update: bool = False,
    **kwargs,
) -> Union[float, pd.Series]:
    """计算 ps_ratio（市销率）因子。"""
    raw = _get_valuation_raw(symbol, cache_dir, force_update)
    df = _normalize_valuation_df(raw)

    if df.empty or "ps_ratio" not in df.columns:
        return np.nan

    if end_date:
        df = df[df["date"] <= end_date]
    if count is not None and count > 0:
        df = df.tail(count)

    if df.empty:
        return np.nan

    df = df.set_index("date")
    series = df["ps_ratio"].astype(float)

    if len(series) == 1:
        return float(series.iloc[0])
    return series


def compute_pcf_ratio(
    symbol: str,
    end_date: Optional[str] = None,
    count: Optional[int] = None,
    cache_dir: str = "stock_cache",
    force_update: bool = False,
    **kwargs,
) -> Union[float, pd.Series]:
    """
    计算 pcf_ratio（市现率）因子。

    公式：总市值 / 经营活动现金流量
    近似实现：使用 AkShare 的估值数据接口
    """
    import os
    try:
        import akshare as ak
    except ImportError:
        raise ImportError("请安装 akshare: pip install akshare")

    ak_sym = _normalize_symbol(symbol)
    cache_file = os.path.join(cache_dir, f"{symbol}_pcf.pkl")
    os.makedirs(cache_dir, exist_ok=True)

    need_dl = force_update or not os.path.exists(cache_file)
    df = pd.DataFrame()

    if not need_dl:
        try:
            df = pd.read_pickle(cache_file)
        except Exception:
            need_dl = True

    if need_dl:
        try:
            # 尝试从百度估值接口获取市现率
            df_tmp = ak.stock_zh_valuation_baidu(symbol=ak_sym, indicator="市现率")
            if df_tmp is not None and not df_tmp.empty:
                df = df_tmp.rename(columns={"value": "pcf_ratio"})
                if "date" in df.columns:
                    df["date"] = pd.to_datetime(df["date"]).dt.strftime("%Y-%m-%d")
                df.to_pickle(cache_file)
        except Exception as e:
            warnings.warn(f"获取市现率数据失败 {symbol}: {e}")
            return np.nan

    if df.empty or "pcf_ratio" not in df.columns:
        return np.nan

    if end_date:
        df = df[df["date"] <= end_date]
    if count is not None and count > 0:
        df = df.tail(count)

    if df.empty:
        return np.nan

    df = df.set_index("date")
    series = df["pcf_ratio"].astype(float)

    if len(series) == 1:
        return float(series.iloc[0])
    return series


def compute_turnover_ratio(
    symbol: str,
    end_date: Optional[str] = None,
    count: Optional[int] = None,
    cache_dir: str = "stock_cache",
    force_update: bool = False,
    **kwargs,
) -> Union[float, pd.Series]:
    """
    计算 turnover_ratio（换手率）因子。

    数据来源：日线行情中的换手率字段
    """
    # 复用 technical 模块的日线数据获取
    from .technical import _get_daily_ohlcv

    need_count = count + 1 if count else 10
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

    # 换手率转换为百分比形式（与聚宽一致）
    turnover = turnover * 100

    if count is not None and count > 0:
        turnover = turnover.tail(count)

    if len(turnover) == 1:
        return float(turnover.iloc[-1])
    return turnover


def compute_capitalization(
    symbol: str,
    end_date: Optional[str] = None,
    count: Optional[int] = None,
    cache_dir: str = "stock_cache",
    force_update: bool = False,
    **kwargs,
) -> Union[float, pd.Series]:
    """
    计算 capitalization（总股本）因子。

    单位：亿股
    近似实现：总市值 / 收盘价
    """
    from .technical import _get_daily_ohlcv

    mc = compute_market_cap(symbol, end_date, count, cache_dir, force_update)

    need_count = count + 1 if count else 10
    df = _get_daily_ohlcv(
        symbol,
        end_date=end_date,
        cache_dir=cache_dir,
        force_update=force_update,
        count=need_count,
    )

    if df.empty:
        return np.nan

    df = df.set_index("date")
    close = df["close"].astype(float)

    if isinstance(mc, pd.Series):
        mc.index = pd.to_datetime(mc.index)
        common_idx = mc.index.intersection(close.index)
        if len(common_idx) == 0:
            return np.nan
        mc = mc.loc[common_idx]
        close = close.loc[common_idx]
        cap = safe_divide(mc, close)
        cap.index = cap.index.strftime("%Y-%m-%d")
        if count is not None and count > 0:
            cap = cap.tail(count)
        if len(cap) == 1:
            return float(cap.iloc[-1])
        return cap
    elif isinstance(mc, (float, np.floating)) and not np.isnan(mc):
        latest_close = close.iloc[-1] if len(close) > 0 else np.nan
        return safe_divide(mc, latest_close)

    return np.nan


def compute_circulating_cap(
    symbol: str,
    end_date: Optional[str] = None,
    count: Optional[int] = None,
    cache_dir: str = "stock_cache",
    force_update: bool = False,
    **kwargs,
) -> Union[float, pd.Series]:
    """
    计算 circulating_cap（流通股本）因子。

    单位：亿股
    近似实现：流通市值 / 收盘价
    """
    from .technical import _get_daily_ohlcv

    cmc = compute_circulating_market_cap(symbol, end_date, count, cache_dir, force_update)

    need_count = count + 1 if count else 10
    df = _get_daily_ohlcv(
        symbol,
        end_date=end_date,
        cache_dir=cache_dir,
        force_update=force_update,
        count=need_count,
    )

    if df.empty:
        return np.nan

    df = df.set_index("date")
    close = df["close"].astype(float)

    if isinstance(cmc, pd.Series):
        cmc.index = pd.to_datetime(cmc.index)
        common_idx = cmc.index.intersection(close.index)
        if len(common_idx) == 0:
            return np.nan
        cmc = cmc.loc[common_idx]
        close = close.loc[common_idx]
        cap = safe_divide(cmc, close)
        cap.index = cap.index.strftime("%Y-%m-%d")
        if count is not None and count > 0:
            cap = cap.tail(count)
        if len(cap) == 1:
            return float(cap.iloc[-1])
        return cap
    elif isinstance(cmc, (float, np.floating)) and not np.isnan(cmc):
        latest_close = close.iloc[-1] if len(close) > 0 else np.nan
        return safe_divide(cmc, latest_close)

    return np.nan


def compute_natural_log_of_market_cap(
    symbol: str,
    end_date: Optional[str] = None,
    count: Optional[int] = None,
    cache_dir: str = "stock_cache",
    force_update: bool = False,
    **kwargs,
) -> Union[float, pd.Series]:
    """
    计算 natural_log_of_market_cap（市值对数）因子。

    公式：log(market_cap)
    """
    result = compute_market_cap(symbol, end_date, count, cache_dir, force_update)

    if isinstance(result, (int, float, np.floating)):
        return np.log(result) if result > 0 else np.nan
    elif isinstance(result, pd.Series):
        # 对有效值取 log
        result = result.copy()
        valid = result > 0
        result[valid] = np.log(result[valid])
        result[~valid] = np.nan
        return result
    return np.nan


def compute_cube_of_size(
    symbol: str,
    end_date: Optional[str] = None,
    count: Optional[int] = None,
    cache_dir: str = "stock_cache",
    force_update: bool = False,
    **kwargs,
) -> Union[float, pd.Series]:
    """
    计算 cube_of_size（规模立方）因子。

    公式：(natural_log_of_market_cap) ** 3
    """
    result = compute_natural_log_of_market_cap(
        symbol, end_date, count, cache_dir, force_update
    )

    if isinstance(result, (int, float, np.floating)):
        return result**3 if not np.isnan(result) else np.nan
    elif isinstance(result, pd.Series):
        return result**3
    return np.nan


# =====================================================================
# 注册因子
# =====================================================================


def _register_factors():
    """向全局注册表注册估值因子。"""
    registry = global_factor_registry

    registry.register(
        "market_cap", compute_market_cap, window=1, dependencies=["valuation"]
    )
    registry.register(
        "circulating_market_cap",
        compute_circulating_market_cap,
        window=1,
        dependencies=["valuation"],
    )
    registry.register(
        "pe_ratio", compute_pe_ratio, window=1, dependencies=["valuation"]
    )
    registry.register(
        "pb_ratio", compute_pb_ratio, window=1, dependencies=["valuation"]
    )
    registry.register(
        "ps_ratio", compute_ps_ratio, window=1, dependencies=["valuation"]
    )
    registry.register(
        "pcf_ratio", compute_pcf_ratio, window=1, dependencies=["valuation"]
    )
    registry.register(
        "turnover_ratio", compute_turnover_ratio, window=1, dependencies=["daily_ohlcv"]
    )
    registry.register(
        "capitalization", compute_capitalization, window=1, dependencies=["market_cap", "daily_ohlcv"]
    )
    registry.register(
        "circulating_cap", compute_circulating_cap, window=1, dependencies=["circulating_market_cap", "daily_ohlcv"]
    )
    registry.register(
        "natural_log_of_market_cap",
        compute_natural_log_of_market_cap,
        window=1,
        dependencies=["market_cap"],
    )
    registry.register(
        "cube_of_size",
        compute_cube_of_size,
        window=1,
        dependencies=["natural_log_of_market_cap"],
    )


# 模块加载时自动注册
_register_factors()


# =====================================================================
# 模块导出
# =====================================================================

__all__ = [
    "compute_market_cap",
    "compute_circulating_market_cap",
    "compute_pe_ratio",
    "compute_pb_ratio",
    "compute_ps_ratio",
    "compute_pcf_ratio",
    "compute_turnover_ratio",
    "compute_capitalization",
    "compute_circulating_cap",
    "compute_natural_log_of_market_cap",
    "compute_cube_of_size",
]
