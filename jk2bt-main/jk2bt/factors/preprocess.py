"""
factors/preprocess.py
聚宽风格的因子预处理函数：winsorize_med, standardlize, neutralize

这些函数用于因子数据的去极值、标准化和中性化处理。

注意：优先使用官方 jqfactor_analyzer 版本，此模块作为 fallback 实现。
"""

import numpy as np
import pandas as pd
from typing import Union, List, Optional
import warnings


def winsorize_med(
    factor_data: Union[pd.DataFrame, pd.Series],
    scale: float = 3.0,
    inclusive: bool = True,
    inf2nan: bool = True,
    axis: int = 0,
) -> Union[pd.DataFrame, pd.Series]:
    """
    聚宽风格的去极值函数（中位数绝对偏差法，MAD法）。

    注意：优先使用官方 jqfactor_analyzer 版本。
    官方版本 scale 默认值为 1，此版本默认值为 3。

    对因子数据进行去极值处理，使用中位数绝对偏差方法。
    超过 median ± scale * MAD 的值会被调整为边界值。

    Parameters
    ----------
    factor_data : pd.DataFrame or pd.Series
        因子数据。DataFrame 时每列代表一个因子（或证券），按 axis 方向处理。
    scale : float, default 3.0
        MAD 的倍数，默认 3 倍。超过此范围的值视为极值。
        聚宽常用值：3、5、10
    inclusive : bool, default True
        是否将极值调整为边界值（True: Winsorize，替换为边界值）
        False: 直接删除极值（暂不支持，转为 NaN）
    inf2nan : bool, default True
        是否将无穷值转换为 NaN
    axis : int, default 0
        处理方向：
        - 0: 按列处理（每列独立去极值，适用于因子值为列）
        - 1: 按行处理（每行独立去极值）

    Returns
    -------
    pd.DataFrame or pd.Series
        处理后的因子数据，保持原形状。

    Examples
    --------
    >>> df = pd.DataFrame({'factor': [1, 2, 3, 100, 4, 5, -50]})
    >>> winsorize_med(df, scale=3)
    """
    # 尝试使用官方SDK
    try:
        from jqfactor_analyzer import winsorize_med as _jq_winsorize_med
        return _jq_winsorize_med(factor_data, scale=scale, inclusive=inclusive, inf2nan=inf2nan, axis=axis)
    except ImportError:
        pass

    # 本地 fallback 实现
    if isinstance(factor_data, pd.Series):
        return _winsorize_med_series(factor_data, scale, inclusive, inf2nan)

    df = factor_data.copy()

    if inf2nan:
        df = df.replace([np.inf, -np.inf], np.nan)

    if axis == 0:
        for col in df.columns:
            df[col] = _winsorize_med_series(df[col], scale, inclusive, inf2nan=False)
    else:
        for idx in df.index:
            df.loc[idx] = _winsorize_med_series(
                df.loc[idx], scale, inclusive, inf2nan=False
            )

    return df


def _winsorize_med_series(
    series: pd.Series,
    scale: float,
    inclusive: bool,
    inf2nan: bool,
) -> pd.Series:
    """对单个 Series 进行 MAD 去极值"""
    s = series.copy()

    if inf2nan:
        s = s.replace([np.inf, -np.inf], np.nan)

    valid = s.dropna()
    if len(valid) == 0:
        return s

    med = valid.median()
    mad = (valid - med).abs().median()

    if mad == 0:
        mad = valid.std() / 1.4826
        if mad == 0:
            return s

    upper = med + scale * mad * 1.4826
    lower = med - scale * mad * 1.4826

    if inclusive:
        s = s.clip(lower=lower, upper=upper)
    else:
        s[(s < lower) | (s > upper)] = np.nan

    return s


def standardlize(
    factor_data: Union[pd.DataFrame, pd.Series],
    inf2nan: bool = True,
    axis: int = 0,
) -> Union[pd.DataFrame, pd.Series]:
    """
    聚宽风格的标准化函数（Z-Score 标准化）。

    注意：优先使用官方 jqfactor_analyzer 版本。

    对因子数据进行标准化处理，使其均值为 0，标准差为 1。

    Parameters
    ----------
    factor_data : pd.DataFrame or pd.Series
        因子数据。
    inf2nan : bool, default True
        是否将无穷值转换为 NaN
    axis : int, default 0
        标准化方向：
        - 0: 按列标准化（每列独立标准化，适用于因子值为列）
        - 1: 按行标准化（每行独立标准化）

    Returns
    -------
    pd.DataFrame or pd.Series
        标准化后的因子数据。

    Examples
    --------
    >>> df = pd.DataFrame({'factor': [1, 2, 3, 4, 5]})
    >>> standardlize(df)
    """
    # 尝试使用官方SDK
    try:
        from jqfactor_analyzer import standardlize as _jq_standardlize
        return _jq_standardlize(factor_data, inf2nan=inf2nan, axis=axis)
    except ImportError:
        pass

    # 本地 fallback 实现
    if isinstance(factor_data, pd.Series):
        return _standardlize_series(factor_data, inf2nan)

    df = factor_data.copy()

    if inf2nan:
        df = df.replace([np.inf, -np.inf], np.nan)

    if axis == 0:
        mean = df.mean(axis=0)
        std = df.std(axis=0)
        std = std.replace(0, np.nan)
        df = (df - mean) / std
    else:
        mean = df.mean(axis=1)
        std = df.std(axis=1)
        std = std.replace(0, np.nan)
        df = df.sub(mean, axis=0).div(std, axis=0)

    return df


def _standardlize_series(series: pd.Series, inf2nan: bool) -> pd.Series:
    """对单个 Series 进行 Z-Score 标准化"""
    s = series.copy()

    if inf2nan:
        s = s.replace([np.inf, -np.inf], np.nan)

    mean = s.mean()
    std = s.std()

    if std == 0 or np.isnan(std):
        return s

    return (s - mean) / std


def neutralize(
    factor_data: Union[pd.DataFrame, pd.Series],
    how: Optional[List[str]] = None,
    date: Optional[str] = None,
    axis: int = 0,
    market_cap: Optional[pd.Series] = None,
    industry_data: Optional[pd.DataFrame] = None,
) -> Union[pd.DataFrame, pd.Series]:
    """
    聚宽风格的因子中性化函数。

    注意：优先使用官方 jqfactor_analyzer 版本。
    官方版本支持自动获取市值和行业数据，需要 JQData 账号。

    对因子进行市值中性化和/或行业中性化处理。

    Parameters
    ----------
    factor_data : pd.DataFrame or pd.Series
        因子数据。列名应为证券代码（当 axis=0 时）。
    how : list of str, optional
        中性化方式，支持：
        - 'market_cap': 市值中性化
        - 'sw_l1', 'sw_l2', 'sw_l3': 申万行业中性化（需提供行业数据）
        - ['sw_l1', 'market_cap']: 同时进行行业和市值中性化
        默认为 ['market_cap']
    date : str, optional
        日期，格式 'YYYY-MM-DD'（用于获取市值/行业数据）
    axis : int, default 0
        中性化方向：
        - 0: 按列处理（每列代表一个证券的因子值）
        - 1: 按行处理
    market_cap : pd.Series, optional
        市值数据，index 为证券代码，value 为市值
        如果不提供，官方SDK会自动获取（需要JQData账号）
    industry_data : pd.DataFrame, optional
        行业哑变量矩阵，index 为证券代码，columns 为行业代码
        如果不提供，官方SDK会自动获取（需要JQData账号）

    Returns
    -------
    pd.DataFrame or pd.Series
        中性化后的因子数据。

    Notes
    -----
    本地版本与聚宽版本的差异：
    - 聚宽版本会自动获取市值和行业数据
    - 本地版本需要手动传入 market_cap 和 industry_data
    - 对于行业中性化，使用行业哑变量回归取残差的方法

    Examples
    --------
    >>> factors = pd.DataFrame({'stock1': [0.5], 'stock2': [0.3]})
    >>> market_cap = pd.Series({'stock1': 1e10, 'stock2': 5e9})
    >>> neutralize(factors, how=['market_cap'], market_cap=market_cap)
    """
    # 尝试使用官方SDK（当提供 date 参数时，官方SDK可自动获取数据）
    if date is not None and market_cap is None and industry_data is None:
        try:
            from jqfactor_analyzer import neutralize as _jq_neutralize
            return _jq_neutralize(factor_data, how=how, date=date, axis=axis)
        except ImportError:
            pass
        except Exception:
            pass  # 官方版本可能因数据获取失败，fallback到本地实现

    # 本地 fallback 实现
    if how is None:
        how = ["market_cap"]

    if isinstance(factor_data, pd.Series):
        factor_data = factor_data.to_frame().T

    df = factor_data.copy()
    securities = df.columns.tolist() if axis == 0 else df.index.tolist()

    need_market_cap = "market_cap" in how
    need_industry = any(h in how for h in ["sw_l1", "sw_l2", "sw_l3", "industry"])

    X = None
    feature_names = []

    if need_market_cap:
        if market_cap is None:
            warnings.warn("市值中性化需要提供 market_cap 参数，跳过市值中性化")
        else:
            mc = np.log(market_cap.reindex(securities).fillna(market_cap.mean()))
            X = (
                mc.values.reshape(-1, 1)
                if X is None
                else np.column_stack([X, mc.values])
            )
            feature_names.append("market_cap")

    if need_industry:
        if industry_data is None:
            warnings.warn("行业中性化需要提供 industry_data 参数，跳过行业中性化")
        else:
            industry_dummies = industry_data.reindex(securities).fillna(0)
            X = (
                industry_dummies.values
                if X is None
                else np.column_stack([X, industry_dummies.values])
            )
            feature_names.extend(industry_dummies.columns.tolist())

    if X is None:
        return df

    X = np.column_stack([np.ones(X.shape[0]), X])

    result = df.copy()
    if axis == 0:
        for col in df.columns:
            y = df[col].values
            valid_mask = ~(np.isnan(y) | np.any(np.isnan(X), axis=1))
            if valid_mask.sum() > X.shape[1]:
                X_valid = X[valid_mask]
                y_valid = y[valid_mask]
                try:
                    beta = np.linalg.lstsq(X_valid, y_valid, rcond=None)[0]
                    residual = y_valid - X_valid @ beta
                    result.loc[valid_mask, col] = residual
                except np.linalg.LinAlgError:
                    pass
    else:
        for idx in df.index:
            y = df.loc[idx].values
            valid_mask = ~(np.isnan(y) | np.any(np.isnan(X), axis=1))
            if valid_mask.sum() > X.shape[1]:
                X_valid = X[valid_mask]
                y_valid = y[valid_mask]
                try:
                    beta = np.linalg.lstsq(X_valid, y_valid, rcond=None)[0]
                    residual = y_valid - X_valid @ beta
                    result.loc[idx, valid_mask] = residual
                except np.linalg.LinAlgError:
                    pass

    return result


__all__ = [
    "winsorize_med",
    "standardlize",
    "neutralize",
]
