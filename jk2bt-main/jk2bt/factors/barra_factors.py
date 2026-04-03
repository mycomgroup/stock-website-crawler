"""
factors/barra_factors.py
Barra风格因子模块。

实现：
- beta                      CAPM贝塔
- momentum                  动量因子（Barra风格）
- residual_volatility       残差波动率
- liquidity                 流动性因子（Barra风格）
- earnings_yield            盈利能力因子
- book_to_price             账面市值比

数据来源：AkShare 日线行情 + 市场指数数据
"""

import warnings
from typing import Optional, Union
import pandas as pd
import numpy as np

from .base import (
    global_factor_registry,
    safe_divide,
)

from .technical import _get_daily_ohlcv


# =====================================================================
# 辅助函数
# =====================================================================


def _get_index_data(
    index_code: str = "000300",
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    cache_dir: str = "stock_cache",
    force_update: bool = False,
    count: Optional[int] = None,
) -> pd.DataFrame:
    """
    获取指数数据作为市场基准。

    数据源优先级：
    1. market_data.index.get_index_daily（DuckDB 缓存）
    2. akshare.index_zh_a_hist（直接获取）
    """
    # 优先尝试使用 market_data 模块
    try:
        from ..market_data.index import get_index_daily

        # 设置默认日期范围
        if start_date is None:
            start_date = "20100101"
        if end_date is None:
            end_date = pd.Timestamp.now().strftime("%Y-%m-%d")

        df = get_index_daily(
            symbol=index_code,
            start=start_date,
            end=end_date,
            force_update=force_update,
        )

        if df is not None and not df.empty:
            # market_data 返回的数据格式是 datetime, open, high, low, close, volume
            df = df.copy()
            if "datetime" in df.columns:
                df["date"] = pd.to_datetime(df["datetime"])
            df = df.set_index("date").sort_index()

            if end_date:
                df = df[df.index <= pd.to_datetime(end_date)]
            if count:
                df = df.tail(count)

            return df[["close"]]
    except ImportError:
        pass  # market_data 模块不可用，fallback 到 akshare
    except Exception as e:
        warnings.warn(f"market_data 模块获取指数数据失败 {index_code}: {e}，fallback 到 akshare")

    # Fallback: 使用 akshare 直接获取
    try:
        import akshare as ak
    except ImportError:
        raise ImportError("请安装 akshare: pip install akshare")

    try:
        df = ak.index_zh_a_hist(
            symbol=index_code,
            period="daily",
            start_date=start_date.replace("-", "") if start_date else "20100101",
            end_date=end_date.replace("-", "") if end_date else "20991231",
        )
        if df is None or df.empty:
            return pd.DataFrame()

        df = df.rename(columns={"日期": "date", "收盘": "close"})
        df["date"] = pd.to_datetime(df["date"])
        df = df.set_index("date").sort_index()

        if end_date:
            df = df[df.index <= pd.to_datetime(end_date)]
        if count:
            df = df.tail(count)

        return df[["close"]]
    except Exception as e:
        warnings.warn(f"获取指数数据失败 {index_code}: {e}")
        return pd.DataFrame()


# =====================================================================
# Beta因子
# =====================================================================


def compute_beta(
    symbol: str,
    window: int = 252,
    halflife: int = 63,
    index_code: str = "000300",
    end_date: Optional[str] = None,
    count: Optional[int] = None,
    cache_dir: str = "stock_cache",
    force_update: bool = False,
    **kwargs,
) -> Union[float, pd.Series]:
    """
    计算 Beta（CAPM贝塔）因子。

    公式：指数加权协方差 / 指数加权方差
    半衰期默认63日
    """
    need_count = count + window if count else window + 10

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
    stock_ret = np.log(close / close.shift(1)).dropna()

    idx_df = _get_index_data(index_code, end_date=end_date, count=need_count)
    if idx_df.empty:
        return np.nan

    market_ret = np.log(idx_df["close"] / idx_df["close"].shift(1)).dropna()

    common_idx = stock_ret.index.intersection(market_ret.index)
    if len(common_idx) < 21:
        return np.nan

    stock_ret = stock_ret.loc[common_idx]
    market_ret = market_ret.loc[common_idx]

    def _calc_beta(sr, mr, n):
        if n > len(sr):
            n = len(sr)
        sr_vals = sr.iloc[-n:].values
        mr_vals = mr.iloc[-n:].values

        weights = np.array([0.5 ** (i / halflife) for i in range(n - 1, -1, -1)])
        weights = weights / weights.sum()

        s_mean = np.dot(weights, sr_vals)
        m_mean = np.dot(weights, mr_vals)

        cov = np.dot(weights, (sr_vals - s_mean) * (mr_vals - m_mean))
        var = np.dot(weights, (mr_vals - m_mean) ** 2)

        return cov / var if var != 0 else np.nan

    beta = pd.Series(index=stock_ret.index[window - 1 :], dtype=float)
    for i in range(window - 1, len(stock_ret)):
        beta.iloc[i - window + 1] = _calc_beta(
            stock_ret.iloc[: i + 1], market_ret.iloc[: i + 1], window
        )

    if count is not None and count > 0:
        beta = beta.tail(count)

    if len(beta) == 1:
        return float(beta.iloc[-1])
    return beta


# =====================================================================
# 动量因子（Barra风格）
# =====================================================================


def compute_momentum(
    symbol: str,
    window: int = 504,
    lag: int = 21,
    halflife: int = 126,
    end_date: Optional[str] = None,
    count: Optional[int] = None,
    cache_dir: str = "stock_cache",
    force_update: bool = False,
    **kwargs,
) -> Union[float, pd.Series]:
    """
    计算 Momentum（动量因子）。

    Barra风格：滞后21日的过去504日对数收益率指数加权和
    """
    need_count = count + window + lag if count else window + lag + 10

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

    log_ret = np.log(close / close.shift(1)).dropna()

    if len(log_ret) < lag + 20:
        return np.nan

    def _calc_mom(lr, n, lag_days):
        if n + lag_days > len(lr):
            n = len(lr) - lag_days
        lr_window = (
            lr.iloc[-(n + lag_days) : -lag_days] if lag_days > 0 else lr.iloc[-n:]
        )

        weights = np.array(
            [0.5 ** (i / halflife) for i in range(len(lr_window) - 1, -1, -1)]
        )
        weights = weights / weights.sum()

        return np.dot(weights, lr_window.values)

    momentum = pd.Series(index=log_ret.index[window + lag - 1 :], dtype=float)
    for i in range(window + lag - 1, len(log_ret)):
        momentum.iloc[i - window - lag + 1] = _calc_mom(
            log_ret.iloc[: i + 1], window, lag
        )

    if count is not None and count > 0:
        momentum = momentum.tail(count)

    if len(momentum) == 1:
        return float(momentum.iloc[-1])
    return momentum


# =====================================================================
# 残差波动率因子
# =====================================================================


def compute_residual_volatility(
    symbol: str,
    window: int = 252,
    halflife_std: int = 42,
    index_code: str = "000300",
    end_date: Optional[str] = None,
    count: Optional[int] = None,
    cache_dir: str = "stock_cache",
    force_update: bool = False,
    **kwargs,
) -> Union[float, pd.Series]:
    """
    计算 Residual Volatility（残差波动率）因子。

    公式：0.74*daily_std + 0.16*cumulative_range + 0.10*historical_sigma
    """
    need_count = count + window if count else window + 10

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
    high = df["high"].astype(float)
    low = df["low"].astype(float)

    stock_ret = close.pct_change().dropna()

    idx_df = _get_index_data(index_code, end_date=end_date, count=need_count)
    if idx_df.empty:
        return np.nan
    market_ret = idx_df["close"].pct_change().dropna()

    common_idx = stock_ret.index.intersection(market_ret.index)
    if len(common_idx) < 21:
        return np.nan

    stock_ret = stock_ret.loc[common_idx]
    market_ret = market_ret.loc[common_idx]

    def _daily_std(sr, mr, n):
        sr_vals = sr.iloc[-n:].values
        mr_vals = mr.iloc[-n:].values
        excess = sr_vals - mr_vals

        weights = np.array([0.5 ** (i / halflife_std) for i in range(n - 1, -1, -1)])
        weights = weights / weights.sum()

        mean = np.dot(weights, excess)
        return np.sqrt(np.dot(weights, (excess - mean) ** 2))

    def _cum_range(c, months=12, days_per_month=21):
        total_days = months * days_per_month
        if len(c) < total_days:
            return np.nan
        c_window = c.iloc[-total_days:]

        monthly_rets = []
        for i in range(months):
            chunk = c_window.iloc[i * days_per_month : (i + 1) * days_per_month]
            if len(chunk) > 1:
                monthly_rets.append(chunk.iloc[-1] / chunk.iloc[0] - 1)

        return (
            max(monthly_rets) - min(monthly_rets) if len(monthly_rets) >= 6 else np.nan
        )

    def _hist_sigma(sr, mr, n):
        sr_vals = sr.iloc[-n:].values
        mr_vals = mr.iloc[-n:].values

        X = np.column_stack([np.ones(n), mr_vals])
        y = sr_vals

        try:
            beta_hat = np.linalg.lstsq(X, y, rcond=None)[0]
            residuals = y - X @ beta_hat
            return np.std(residuals)
        except:
            return np.nan

    res_vol = pd.Series(index=stock_ret.index[window - 1 :], dtype=float)
    for i in range(window - 1, len(stock_ret)):
        ds = _daily_std(stock_ret.iloc[: i + 1], market_ret.iloc[: i + 1], window)
        cr = _cum_range(close.iloc[: i + 1])
        hs = _hist_sigma(stock_ret.iloc[: i + 1], market_ret.iloc[: i + 1], window)

        components = [(0.74, ds), (0.16, cr), (0.10, hs)]
        valid = [(w, v) for w, v in components if not np.isnan(v)]

        if valid:
            total_w = sum(w for w, _ in valid)
            res_vol.iloc[i - window + 1] = sum(w * v for w, v in valid) / total_w
        else:
            res_vol.iloc[i - window + 1] = np.nan

    if count is not None and count > 0:
        res_vol = res_vol.tail(count)

    if len(res_vol) == 1:
        return float(res_vol.iloc[-1])
    return res_vol


# =====================================================================
# 流动性因子（Barra风格）
# =====================================================================


def compute_liquidity_barra(
    symbol: str,
    end_date: Optional[str] = None,
    count: Optional[int] = None,
    cache_dir: str = "stock_cache",
    force_update: bool = False,
    **kwargs,
) -> Union[float, pd.Series]:
    """
    计算 Liquidity（流动性因子）。

    公式：0.35*月换手率对数 + 0.35*季换手率对数 + 0.30*年换手率对数
    """
    need_count = count + 252 if count else 260

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

    def _calc_liq(t):
        if len(t) < 21:
            return np.nan

        monthly = t.iloc[-21:].sum()
        monthly_log = np.log(monthly) if monthly > 0 else np.nan

        quarterly_mean = t.iloc[-63:].mean() if len(t) >= 63 else np.nan
        quarterly_log = (
            np.log(quarterly_mean)
            if (quarterly_mean and quarterly_mean > 0)
            else np.nan
        )

        annual_mean = t.iloc[-252:].mean() if len(t) >= 252 else np.nan
        annual_log = (
            np.log(annual_mean) if (annual_mean and annual_mean > 0) else np.nan
        )

        components = [(0.35, monthly_log), (0.35, quarterly_log), (0.30, annual_log)]
        valid = [(w, v) for w, v in components if not np.isnan(v)]

        if valid:
            total_w = sum(w for w, _ in valid)
            return sum(w * v for w, v in valid) / total_w
        return np.nan

    liq = pd.Series(index=turnover.index[251:], dtype=float)
    for i in range(251, len(turnover)):
        liq.iloc[i - 251] = _calc_liq(turnover.iloc[: i + 1])

    if count is not None and count > 0:
        liq = liq.tail(count)

    if len(liq) == 1:
        return float(liq.iloc[-1])
    return liq


# =====================================================================
# 盈利能力因子
# =====================================================================


def compute_earnings_yield(
    symbol: str,
    end_date: Optional[str] = None,
    count: Optional[int] = None,
    cache_dir: str = "stock_cache",
    force_update: bool = False,
    **kwargs,
) -> Union[float, pd.Series]:
    """
    计算 Earnings Yield（盈利能力因子）。

    公式：0.11*EP + 0.21*CFO/MV（简化版本，实际需要分析师预测）
    """
    from .valuation import compute_market_cap
    from .fundamentals import _get_income_statement, _normalize_income

    mc = compute_market_cap(
        symbol,
        end_date=end_date,
        count=count,
        cache_dir=cache_dir,
        force_update=force_update,
    )

    income_raw = _get_income_statement(symbol, cache_dir, force_update)
    income = _normalize_income(income_raw)

    if income.empty:
        return np.nan

    income = income.set_index("date")
    net_profit = income.get("net_profit")

    if net_profit is None or (isinstance(mc, (float, np.floating)) and np.isnan(mc)):
        return np.nan

    if isinstance(mc, pd.Series):
        mc.index = pd.to_datetime(mc.index)
        common_idx = net_profit.index.intersection(mc.index)
        if len(common_idx) == 0:
            return np.nan
        net_profit = net_profit.loc[common_idx]
        mc = mc.loc[common_idx]

        ep = safe_divide(net_profit, mc)
        ep.index = ep.index.strftime("%Y-%m-%d")
        return ep * 0.32  # 0.11 + 0.21 = 0.32 简化
    else:
        latest_np = net_profit.iloc[-1] if len(net_profit) > 0 else np.nan
        return safe_divide(latest_np, mc) * 0.32 if not np.isnan(mc) else np.nan


# =====================================================================
# 账面市值比
# =====================================================================


def compute_book_to_price(
    symbol: str,
    end_date: Optional[str] = None,
    count: Optional[int] = None,
    cache_dir: str = "stock_cache",
    force_update: bool = False,
    **kwargs,
) -> Union[float, pd.Series]:
    """
    计算 Book to Price（账面市值比）因子。

    公式：净资产 / 总市值
    """
    from .valuation import compute_market_cap
    from .fundamentals import _get_balance_sheet, _normalize_balance

    mc = compute_market_cap(
        symbol,
        end_date=end_date,
        count=count,
        cache_dir=cache_dir,
        force_update=force_update,
    )

    balance_raw = _get_balance_sheet(symbol, cache_dir, force_update)
    balance = _normalize_balance(balance_raw)

    if balance.empty:
        return np.nan

    balance = balance.set_index("date")
    equity = balance.get("total_equity")

    if equity is None or (isinstance(mc, (float, np.floating)) and np.isnan(mc)):
        return np.nan

    if isinstance(mc, pd.Series):
        mc.index = pd.to_datetime(mc.index)
        common_idx = equity.index.intersection(mc.index)
        if len(common_idx) == 0:
            return np.nan
        equity = equity.loc[common_idx]
        mc = mc.loc[common_idx]

        bp = safe_divide(equity, mc)
        bp.index = bp.index.strftime("%Y-%m-%d")
        return bp
    else:
        latest_eq = equity.iloc[-1] if len(equity) > 0 else np.nan
        return safe_divide(latest_eq, mc) if not np.isnan(mc) else np.nan


# =====================================================================
# Size因子（市值对数）
# =====================================================================


def compute_size(
    symbol: str,
    end_date: Optional[str] = None,
    count: Optional[int] = None,
    cache_dir: str = "stock_cache",
    force_update: bool = False,
    **kwargs,
) -> Union[float, pd.Series]:
    """
    计算 Size（市值因子）。

    公式：ln(总市值)
    """
    from .valuation import compute_market_cap

    mc = compute_market_cap(
        symbol,
        end_date=end_date,
        count=count,
        cache_dir=cache_dir,
        force_update=force_update,
    )

    if isinstance(mc, pd.Series):
        return np.log(mc.where(mc > 0, np.nan))
    elif isinstance(mc, (float, np.floating)):
        return np.log(mc) if mc > 0 else np.nan
    return np.nan


# =====================================================================
# 注册因子
# =====================================================================


def _register_factors():
    """向全局注册表注册Barra风格因子。"""
    registry = global_factor_registry

    registry.register(
        "beta", compute_beta, window=252, dependencies=["daily_ohlcv", "index_data"]
    )
    registry.register(
        "momentum", compute_momentum, window=504, dependencies=["daily_ohlcv"]
    )
    registry.register(
        "residual_volatility",
        compute_residual_volatility,
        window=252,
        dependencies=["daily_ohlcv", "index_data"],
    )
    registry.register(
        "liquidity_barra",
        compute_liquidity_barra,
        window=252,
        dependencies=["daily_ohlcv"],
    )
    registry.register(
        "earnings_yield",
        compute_earnings_yield,
        window=1,
        dependencies=["market_cap", "income"],
    )
    registry.register(
        "book_to_price",
        compute_book_to_price,
        window=1,
        dependencies=["market_cap", "balance"],
    )
    registry.register("size", compute_size, window=1, dependencies=["market_cap"])


_register_factors()


__all__ = [
    "compute_beta",
    "compute_momentum",
    "compute_residual_volatility",
    "compute_liquidity_barra",
    "compute_earnings_yield",
    "compute_book_to_price",
    "compute_size",
]
