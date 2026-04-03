"""
factors/custom_factors.py
自定义因子函数模块。

实现聚宽策略中常用的自定义因子函数：
- get_zscore           RSRS择时Z-Score因子
- get_zscore_slope     RSRS斜率因子
- get_single_factor_list 单因子查询函数
- get_score            综合评分因子

这些函数在聚宽策略中经常被调用，用于RSRS择时、多因子选股等场景。
"""

import warnings
from typing import Optional, Union, List, Dict
import pandas as pd
import numpy as np

from .base import (
    global_factor_registry,
    safe_divide,
)

from .technical import _get_daily_ohlcv


# =====================================================================
# RSRS择时因子（Z-Score）
# =====================================================================


def compute_zscore(
    symbol: str,
    window: int = 18,
    end_date: Optional[str] = None,
    count: Optional[int] = None,
    cache_dir: str = "stock_cache",
    force_update: bool = False,
    **kwargs,
) -> Union[float, pd.Series]:
    """
    计算 RSRS Z-Score（阻力支撑相对强度Z分数）因子。

    RSRS模型：
    1. 对过去N天的最高价和最低价进行线性回归：High = β * Low + α
    2. 记录斜率β序列
    3. 对斜率序列进行标准化：Z-Score = (β - μ) / σ

    用途：择时信号，Z-Score > 0 表示上行趋势，Z-Score < 0 表示下行趋势

    Parameters
    ----------
    symbol : str
        证券代码（也支持指数代码）
    window : int
        回归窗口，默认18天
    end_date : str, optional
        截止日期
    count : int, optional
        返回的历史数据数量
    """
    need_count = count + window * 2 + 10 if count else window * 2 + 20
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
    low = df["low"].astype(float)

    # 计算斜率序列
    betas = []

    for i in range(window, len(high)):
        low_window = low.iloc[i - window : i].values
        high_window = high.iloc[i - window : i].values

        # 线性回归
        try:
            # y = βx + α
            x = low_window
            y = high_window
            n = len(x)
            sum_x = np.sum(x)
            sum_y = np.sum(y)
            sum_xy = np.sum(x * y)
            sum_xx = np.sum(x * x)

            beta = (n * sum_xy - sum_x * sum_y) / (n * sum_xx - sum_x * sum_x)
            betas.append(beta)
        except Exception:
            betas.append(np.nan)

    # 创建斜率序列
    beta_series = pd.Series(betas, index=high.index[window:])

    # 计算Z-Score
    beta_mean = beta_series.rolling(window=window, min_periods=window // 2).mean()
    beta_std = beta_series.rolling(window=window, min_periods=window // 2).std()

    zscore = safe_divide(beta_series - beta_mean, beta_std)

    if count is not None and count > 0:
        zscore = zscore.tail(count)

    if len(zscore) == 1:
        return float(zscore.iloc[-1])

    return zscore


def compute_zscore_slope(
    symbol: str,
    window: int = 18,
    slope_window: int = 5,
    end_date: Optional[str] = None,
    count: Optional[int] = None,
    cache_dir: str = "stock_cache",
    force_update: bool = False,
    **kwargs,
) -> Union[float, pd.Series]:
    """
    计算 RSRS Slope（RSRS斜率）因子。

    直接返回RSRS模型中的斜率β值，用于判断支撑阻力强度。

    Parameters
    ----------
    symbol : str
        证券代码
    window : int
        回归窗口
    slope_window : int
        斜率平滑窗口
    """
    need_count = count + window + slope_window if count else window + slope_window + 10
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
    low = df["low"].astype(float)

    # 计算斜率序列
    betas = []

    for i in range(window, len(high)):
        low_window = low.iloc[i - window : i].values
        high_window = high.iloc[i - window : i].values

        try:
            x = low_window
            y = high_window
            n = len(x)
            sum_x = np.sum(x)
            sum_y = np.sum(y)
            sum_xy = np.sum(x * y)
            sum_xx = np.sum(x * x)

            beta = (n * sum_xy - sum_x * sum_y) / (n * sum_xx - sum_x * sum_x)
            betas.append(beta)
        except Exception:
            betas.append(np.nan)

    beta_series = pd.Series(betas, index=high.index[window:])

    # 平滑斜率
    smooth_beta = beta_series.rolling(window=slope_window, min_periods=1).mean()

    if count is not None and count > 0:
        smooth_beta = smooth_beta.tail(count)

    if len(smooth_beta) == 1:
        return float(smooth_beta.iloc[-1])

    return smooth_beta


# =====================================================================
# 综合评分因子
# =====================================================================


def compute_score(
    symbol: str,
    factors: Optional[List[str]] = None,
    weights: Optional[List[float]] = None,
    end_date: Optional[str] = None,
    count: Optional[int] = None,
    cache_dir: str = "stock_cache",
    force_update: bool = False,
    **kwargs,
) -> Union[float, pd.Series]:
    """
    计算综合评分因子。

    将多个因子按照权重加权求和，生成综合评分。

    Parameters
    ----------
    symbol : str
        证券代码
    factors : list of str
        因子名称列表，默认使用经典的估值+成长因子组合
    weights : list of float
        因子权重列表，默认等权
    """
    from .factor_zoo import get_factor_values_jq

    # 默认因子组合
    if factors is None:
        factors = ["pe_ratio", "pb_ratio", "roe", "inc_revenue_year_on_year"]
        weights = [0.25, 0.25, 0.25, 0.25]

    if weights is None:
        weights = [1.0 / len(factors)] * len(factors)

    if len(factors) != len(weights):
        warnings.warn("因子数量与权重数量不匹配，使用等权")
        weights = [1.0 / len(factors)] * len(factors)

    # 获取因子值
    factor_values = get_factor_values_jq(
        securities=symbol,
        factors=factors,
        end_date=end_date,
        count=count,
        cache_dir=cache_dir,
        force_update=force_update,
    )

    # 计算综合评分
    score = None
    valid_count = 0

    for factor_name, weight in zip(factors, weights):
        factor_df = factor_values.get(factor_name)
        if factor_df is None or factor_df.empty:
            continue

        factor_series = factor_df[symbol] if symbol in factor_df.columns else factor_df.iloc[:, 0]

        # 标准化因子值（Z-Score）
        mean_val = factor_series.mean()
        std_val = factor_series.std()
        if std_val and std_val > 0:
            normalized = (factor_series - mean_val) / std_val
        else:
            normalized = factor_series - mean_val

        # 对于估值因子，值越小越好，需要取负
        if factor_name in ["pe_ratio", "pb_ratio", "ps_ratio", "pcf_ratio"]:
            normalized = -normalized

        if score is None:
            score = normalized * weight
        else:
            score = score + normalized * weight

        valid_count += 1

    if score is None:
        return np.nan

    if count is not None and count > 0:
        score = score.tail(count)

    if len(score) == 1:
        return float(score.iloc[-1])

    return score


# =====================================================================
# 单因子查询函数（兼容聚宽API）
# =====================================================================


def get_single_factor_list(
    factor_name: str,
    securities: Optional[List[str]] = None,
    end_date: Optional[str] = None,
    count: Optional[int] = None,
    cache_dir: str = "stock_cache",
    force_update: bool = False,
    **kwargs,
) -> pd.DataFrame:
    """
    获取单个因子在多个证券上的值。

    聚宽风格API：返回DataFrame，index为日期，columns为证券代码。

    Parameters
    ----------
    factor_name : str
        因子名称
    securities : list of str
        证券代码列表
    end_date : str
        截止日期
    count : int
        历史数据数量

    Returns
    -------
    pd.DataFrame
        因子值矩阵
    """
    from .factor_zoo import get_factor_values_jq

    if securities is None:
        warnings.warn("未指定证券列表，返回空DataFrame")
        return pd.DataFrame()

    result = get_factor_values_jq(
        securities=securities,
        factors=[factor_name],
        end_date=end_date,
        count=count,
        cache_dir=cache_dir,
        force_update=force_update,
    )

    return result.get(factor_name, pd.DataFrame())


# =====================================================================
# 注册因子
# =====================================================================


def _register_factors():
    """向全局注册表注册自定义因子。"""
    registry = global_factor_registry

    registry.register("zscore", compute_zscore, window=36, dependencies=["daily_ohlcv"])
    registry.register("zscore_slope", compute_zscore_slope, window=23, dependencies=["daily_ohlcv"])
    registry.register("score", compute_score, window=1, dependencies=["multi_factor"])


# 模块加载时自动注册
_register_factors()


# =====================================================================
# 模块导出
# =====================================================================

__all__ = [
    "compute_zscore",
    "compute_zscore_slope",
    "compute_score",
    "get_single_factor_list",
]