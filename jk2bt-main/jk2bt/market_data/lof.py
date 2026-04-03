"""
market_data/lof.py
LOF（上市开放式基金）数据获取模块。

LOF 既可以在场内交易（像 ETF），也可以在场外申购赎回。
提供两种数据源：
1. 场内交易行情（fund_lof_hist_em）- 网络不稳定
2. 场外净值数据（fund_etf_fund_info_em）- 稳定可用

建议：
- 场内行情不稳定时，使用场外净值数据作为备用
- 净值数据每日更新一次，适合长期跟踪
"""

import logging
import pandas as pd
from typing import Optional

logger = logging.getLogger(__name__)


def get_lof_daily(
    symbol: str,
    start: str,
    end: str,
    period: str = "daily",
    adjust: str = "",
    force_update: bool = False,
    retry_count: int = 3,
) -> pd.DataFrame:
    """
    获取 LOF 日线行情数据。

    参数
    ----
    symbol : str
        LOF 代码，如 '161725'（招商中证白酒指数LOF）
    start : str
        资始日期 'YYYY-MM-DD'
    end : str
        结束日期 'YYYY-MM-DD'
    period : str
        周期：daily/weekly/monthly
    adjust : str
        复权类型：qfq/hfq/''（空字符串不复权）
    force_update : bool
        强制从 akshare 重新下载（忽略缓存）
    retry_count : int
        网络请求重试次数

    返回
    ----
    pd.DataFrame
        标准化后的 OHLCV 数据，包含：
        datetime, open, high, low, close, volume, amount, openinterest

    异常
    ----
    ValueError
        数据获取失败或返回空数据
    """
    try:
        import akshare as ak
    except ImportError:
        raise ImportError("请安装 akshare: pip install akshare")

    from ..utils.standardize import standardize_ohlcv

    start_date = start.replace("-", "")
    end_date = end.replace("-", "")

    raw_df = None
    last_error = None

    for attempt in range(retry_count):
        try:
            logger.info(
                f"{symbol}: 尝试从 akshare 获取 LOF 数据 (第 {attempt + 1}/{retry_count} 次)"
            )
            raw_df = ak.fund_lof_hist_em(
                symbol=symbol,
                period=period,
                start_date=start_date,
                end_date=end_date,
                adjust=adjust,
            )

            if raw_df is not None and not raw_df.empty:
                break

        except Exception as e:
            last_error = e
            logger.warning(f"{symbol}: 第 {attempt + 1} 次尝试失败 - {str(e)[:100]}")
            if attempt < retry_count - 1:
                import time

                time.sleep(0.5 * (attempt + 1))

    if raw_df is None or raw_df.empty:
        error_msg = f"{symbol}: LOF 数据获取失败"
        if last_error:
            error_msg += f" - {str(last_error)[:100]}"
        logger.error(error_msg)
        raise ValueError(error_msg)

    logger.info(f"{symbol}: 成功获取 LOF 数据，共 {len(raw_df)} 条记录")

    df = raw_df.copy()

    columns_map = {
        "日期": "datetime",
        "开盘": "open",
        "最高": "high",
        "最低": "low",
        "收盘": "close",
        "成交量": "volume",
        "成交额": "amount",
    }

    for old_col, new_col in columns_map.items():
        if old_col in df.columns:
            df[new_col] = df[old_col]

    df["datetime"] = pd.to_datetime(df["datetime"])

    select_cols = ["datetime", "open", "high", "low", "close", "volume"]
    if "amount" in df.columns:
        select_cols.append("amount")

    df = df[select_cols].copy()

    df = df[
        (df["datetime"] >= pd.to_datetime(start))
        & (df["datetime"] <= pd.to_datetime(end))
    ]

    return standardize_ohlcv(df)


def get_lof_spot() -> pd.DataFrame:
    """
    获取所有 LOF 的实时行情列表。

    返回
    ----
    pd.DataFrame
        LOF 实时行情数据，包含：代码、名称、最新价、涨跌幅等
    """
    try:
        import akshare as ak
    except ImportError:
        raise ImportError("请安装 akshare: pip install akshare")

    try:
        df = ak.fund_lof_spot_em()
        logger.info(f"获取 LOF 实时行情，共 {len(df)} 条")
        return df
    except Exception as e:
        logger.error(f"LOF 实时行情获取失败: {e}")
        raise


def get_lof_min(
    symbol: str,
    start: str = "1979-09-01 09:32:00",
    end: str = "2222-01-01 09:32:00",
    period: str = "5",
    adjust: str = "",
    retry_count: int = 3,
) -> pd.DataFrame:
    """
    获取 LOF 分钟级别行情数据。

    参数
    ----
    symbol : str
        LOF 代码
    start : str
        资始时间
    end : str
        结束时间
    period : str
        分钟周期：1/5/15/30/60
    adjust : str
        复权类型
    retry_count : int
        重试次数

    返回
    ----
    pd.DataFrame
        分钟级别 OHLCV 数据
    """
    try:
        import akshare as ak
    except ImportError:
        raise ImportError("请安装 akshare: pip install akshare")

    from ..utils.standardize import standardize_minute_ohlcv

    raw_df = None
    last_error = None

    for attempt in range(retry_count):
        try:
            raw_df = ak.fund_lof_hist_min_em(
                symbol=symbol,
                start_date=start,
                end_date=end,
                period=period,
                adjust=adjust,
            )
            if raw_df is not None and not raw_df.empty:
                break
        except Exception as e:
            last_error = e
            if attempt < retry_count - 1:
                import time

                time.sleep(0.5)

    if raw_df is None or raw_df.empty:
        error_msg = f"{symbol}: LOF 分钟数据获取失败"
        if last_error:
            error_msg += f" - {str(last_error)[:100]}"
        raise ValueError(error_msg)

    df = raw_df.copy()

    columns_map = {
        "时间": "datetime",
        "开盘": "open",
        "最高": "high",
        "最低": "low",
        "收盘": "close",
        "成交量": "volume",
        "成交额": "money",
    }

    for old_col, new_col in columns_map.items():
        if old_col in df.columns:
            df[new_col] = df[old_col]

    return standardize_minute_ohlcv(df)


def get_lof_nav(
    symbol: str,
    start: Optional[str] = None,
    end: Optional[str] = None,
) -> pd.DataFrame:
    """
    获取 LOF 场外净值数据（稳定接口）。

    这是 LOF 的场外净值数据，每日更新一次，接口稳定。
    当场内行情接口不可用时，可作为备用数据源。

    参数
    ----
    symbol : str
        LOF 代码，如 '161725'
    start : str, optional
        资始日期 'YYYY-MM-DD'
    end : str, optional
        结束日期 'YYYY-MM-DD'

    返回
    ----
    pd.DataFrame
        净值数据，字段：
        datetime, unit_nav, acc_nav, daily_growth_rate, purchase_status, redeem_status
    """
    try:
        import akshare as ak
    except ImportError:
        raise ImportError("请安装 akshare: pip install akshare")

    try:
        logger.info(f"{symbol}: 获取 LOF 净值数据")
        raw_df = ak.fund_etf_fund_info_em(fund=symbol)

        if raw_df is None or raw_df.empty:
            raise ValueError(f"{symbol}: LOF 净值数据为空")

        logger.info(f"{symbol}: 成功获取净值数据，共 {len(raw_df)} 条")

        df = raw_df.copy()

        columns_map = {
            "净值日期": "datetime",
            "单位净值": "unit_nav",
            "累计净值": "acc_nav",
            "日增长率": "daily_growth_rate",
            "申购状态": "purchase_status",
            "赎回状态": "redeem_status",
        }

        for old_col, new_col in columns_map.items():
            if old_col in df.columns:
                df[new_col] = df[old_col]

        if "datetime" in df.columns:
            df["datetime"] = pd.to_datetime(df["datetime"], errors="coerce")
            df = df.dropna(subset=["datetime"])
            df = df.sort_values("datetime").reset_index(drop=True)

        numeric_cols = ["unit_nav", "acc_nav", "daily_growth_rate"]
        for col in numeric_cols:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors="coerce")

        if start is not None:
            df = df[df["datetime"] >= pd.to_datetime(start)]
        if end is not None:
            df = df[df["datetime"] <= pd.to_datetime(end)]

        result_cols = [
            "datetime",
            "unit_nav",
            "acc_nav",
            "daily_growth_rate",
            "purchase_status",
            "redeem_status",
        ]
        df = df[[col for col in result_cols if col in df.columns]]

        logger.info(f"{symbol}: 返回 {len(df)} 条净值记录")
        return df.reset_index(drop=True)

    except Exception as e:
        logger.error(f"{symbol}: LOF 净值获取失败 - {str(e)[:100]}")
        raise ValueError(f"{symbol}: LOF 净值获取失败 - {str(e)[:100]}")


def get_lof_daily_with_fallback(
    symbol: str,
    start: str,
    end: str,
    prefer_nav: bool = False,
) -> pd.DataFrame:
    """
    获取 LOF 数据，优先使用场内行情，失败时自动切换到场外净值。

    参数
    ----
    symbol : str
        LOF 代码
    start : str
        资始日期
    end : str
        结束日期
    prefer_nav : bool
        是否优先使用净值数据（默认 False，优先使用行情）

    返回
    ----
    pd.DataFrame
        行情或净值数据
    """
    if prefer_nav:
        try:
            logger.info(f"{symbol}: 优先使用净值数据")
            return get_lof_nav(symbol, start, end)
        except Exception as e:
            logger.warning(f"{symbol}: 净值数据获取失败，尝试行情: {str(e)[:50]}")

    try:
        logger.info(f"{symbol}: 尝试获取场内行情")
        return get_lof_daily(symbol, start, end, retry_count=2)
    except Exception as e:
        logger.warning(f"{symbol}: 场内行情失败，切换到净值数据: {str(e)[:50]}")
        return get_lof_nav(symbol, start, end)
