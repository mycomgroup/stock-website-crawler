"""
jk2bt/api/factor_kanban.py
因子看板 API 模块

提供因子库浏览、回测表现、分位数收益、风格因子收益及特异性收益接口。
纯本地模拟数据，不依赖远程回测系统。

主要功能:
- get_all_factors: 获取因子库全量列表
- get_factor_kanban_values: 获取因子回测表现指标
- get_factor_stats: 获取因子分位数收益历史
- get_factor_style_returns: 获取风格因子暴露收益
- get_factor_specific_returns: 获取个股特异性收益
"""

import numpy as np
import pandas as pd
from typing import List, Optional, Dict
import warnings

from jk2bt.analysis.factors.constants import (
    CNE6_STYLE_FACTORS,
    FACTOR_LIBRARY,
    FACTOR_IC_BASE,
)


def _hash_seed(name: str) -> int:
    return sum(ord(c) for c in name) % (2**31)


def _generate_monthly_dates(n_months: int = 24) -> pd.DatetimeIndex:
    end = pd.Timestamp("2026-03-31")
    return pd.date_range(end=end, periods=n_months, freq="ME")


def _generate_trading_dates(n_days: int = 60) -> pd.DatetimeIndex:
    end = pd.Timestamp("2026-04-15")
    all_dates = pd.date_range(end=end, periods=n_days * 2, freq="B")
    return all_dates[-n_days:]


def get_all_factors() -> pd.DataFrame:
    """
    获取因子库中所有可用因子。

    Returns
    -------
    pd.DataFrame
        包含 index, factor, factor_intro, category, category_intro 列的 DataFrame。
    """
    rows = []
    for idx, (category, info) in enumerate(FACTOR_LIBRARY.items(), start=1):
        for factor, intro in info["factors"].items():
            rows.append(
                {
                    "index": idx,
                    "factor": factor,
                    "factor_intro": intro,
                    "category": category,
                    "category_intro": info["category_intro"],
                }
            )
            idx += 1
    return pd.DataFrame(rows)


def get_factor_kanban_values(
    universe: str = "hs300",
    bt_cycle: str = "month_3",
    model: str = "long_only",
    category: Optional[List[str]] = None,
    skip_paused: bool = False,
    commision_slippage: float = 0,
) -> pd.DataFrame:
    """
    获取因子回测表现指标。

    Parameters
    ----------
    universe : str, default 'hs300'
        指数股票池: 'hs300', 'csi500', 'csi1000', 'zz800', 'zzqz'
    bt_cycle : str, default 'month_3'
        调仓周期: 'month_1', 'month_3', 'month_6', 'month_12', 'year_1', 'year_3', 'year_10'
    model : str, default 'long_only'
        策略模型: 'long_only', 'long_short'
    category : list, optional
        要包含的因子类别，默认全部
    skip_paused : bool, default False
        是否跳过停牌股票
    commision_slippage : float, default 0
        交易成本

    Returns
    -------
    pd.DataFrame
        包含 date, category, factor, return, volatility, sharpe, max_drawdown,
        ic, icir, good_ic, ir, turnover_rate 列的 DataFrame。
    """
    factor_df = get_all_factors()
    if category is not None:
        factor_df = factor_df[factor_df["category"].isin(category)]

    dates = _generate_monthly_dates(24)
    rows = []

    for _, row in factor_df.iterrows():
        factor = row["factor"]
        cat = row["category"]
        seed = _hash_seed(f"{factor}_{universe}_{bt_cycle}_{model}")
        rng = np.random.RandomState(seed)

        ic_base, sharpe_base = FACTOR_IC_BASE.get(factor, (0.01, 0.5))
        universe_adj = {
            "hs300": 1.0,
            "csi500": 0.95,
            "csi1000": 0.9,
            "zz800": 0.92,
            "zzqz": 0.88,
        }.get(universe, 1.0)
        cycle_adj = {
            "month_1": 1.0,
            "month_3": 0.95,
            "month_6": 0.9,
            "month_12": 0.85,
            "year_1": 0.8,
            "year_3": 0.75,
            "year_10": 0.7,
        }.get(bt_cycle, 1.0)
        model_adj = 1.1 if model == "long_short" else 1.0
        cost_adj = 1.0 - commision_slippage * 2

        for i, date in enumerate(dates):
            noise = rng.normal(0, 0.015)
            time_decay = 1.0 - i * 0.005
            ic = ic_base * universe_adj * cycle_adj * time_decay + noise
            ic = np.clip(ic, -0.1, 0.15)

            sharpe = (
                sharpe_base * universe_adj * cycle_adj * model_adj * cost_adj
                + rng.normal(0, 0.15)
            )
            sharpe = np.clip(sharpe, -0.5, 1.5)

            vol = 0.15 + rng.normal(0, 0.03)
            vol = np.clip(vol, 0.08, 0.35)

            ret = sharpe * vol / np.sqrt(12) + rng.normal(0, 0.01)
            ret = np.clip(ret, -0.1, 0.15)

            mdd = -(0.05 + abs(rng.normal(0, 0.08)))
            mdd = np.clip(mdd, -0.4, -0.01)

            icir = ic / (0.03 + abs(rng.normal(0, 0.01)))
            icir = np.clip(icir, -2.0, 2.0)

            good_ic = max(0, ic_base * 0.5 + rng.normal(0, 0.05))
            good_ic = np.clip(good_ic, 0, 0.12)

            ir = sharpe / np.sqrt(12) + rng.normal(0, 0.05)
            ir = np.clip(ir, -0.5, 1.0)

            turnover = 0.15 + rng.normal(0, 0.05)
            if bt_cycle == "month_1":
                turnover *= 2.0
            elif bt_cycle == "month_12":
                turnover *= 0.3
            turnover = np.clip(turnover, 0.02, 0.8)

            rows.append(
                {
                    "date": date,
                    "category": cat,
                    "factor": factor,
                    "return": round(ret, 6),
                    "volatility": round(vol, 6),
                    "sharpe": round(sharpe, 4),
                    "max_drawdown": round(mdd, 6),
                    "ic": round(ic, 6),
                    "icir": round(icir, 4),
                    "good_ic": round(good_ic, 6),
                    "ir": round(ir, 4),
                    "turnover_rate": round(turnover, 6),
                }
            )

    return pd.DataFrame(rows)


def get_factor_stats(
    factor_names: Optional[List[str]] = None,
    universe_type: str = "hs300",
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    count: Optional[int] = None,
    skip_paused: bool = False,
    commision_fee: float = 0.0,
) -> Dict[str, pd.DataFrame]:
    """
    获取因子分位数收益历史。

    Parameters
    ----------
    factor_names : list, optional
        因子名称列表，默认全部
    universe_type : str, default 'hs300'
        指数股票池: 'hs300', 'csi500', 'csi1000'
    start_date : str, optional
        起始日期
    end_date : str, optional
        结束日期
    count : int, optional
        数据点数量
    skip_paused : bool, default False
        是否跳过停牌股票
    commision_fee : float, default 0.0
        交易费用

    Returns
    -------
    Dict[str, pd.DataFrame]
        键为因子名称，值为分位数收益 DataFrame，列为 1-5 分位数，索引为日期。
    """
    all_factors = get_all_factors()
    if factor_names is None:
        factor_names = all_factors["factor"].unique().tolist()

    n_periods = count if count else 24
    dates = _generate_monthly_dates(n_periods)

    if start_date:
        dates = dates[dates >= pd.Timestamp(start_date)]
    if end_date:
        dates = dates[dates <= pd.Timestamp(end_date)]

    universe_adj = {"hs300": 1.0, "csi500": 0.95, "csi1000": 0.9}.get(
        universe_type, 1.0
    )
    fee_adj = 1.0 - commision_fee * 2

    result = {}
    for factor in factor_names:
        seed = _hash_seed(f"{factor}_stats_{universe_type}")
        rng = np.random.RandomState(seed)
        ic_base, _ = FACTOR_IC_BASE.get(factor, (0.01, 0.5))

        quantile_data = {}
        for q in range(1, 6):
            q_center = (q - 3) / 2.0
            q_signal = ic_base * q_center * 0.1 * universe_adj * fee_adj
            returns = []
            for _ in range(len(dates)):
                ret = q_signal + rng.normal(0, 0.04)
                ret = np.clip(ret, -0.15, 0.15)
                returns.append(round(ret, 6))
            quantile_data[q] = returns

        result[factor] = pd.DataFrame(quantile_data, index=dates)

    return result


def get_factor_style_returns(
    factors: Optional[List[str]] = None,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    count: Optional[int] = None,
    universe: Optional[str] = None,
    industry: str = "sw_l1",
    category: Optional[str] = None,
    use_real_data: bool = False,
) -> pd.DataFrame:
    """
    获取风格因子暴露收益（Barra风格）。

    Parameters
    ----------
    factors : list, optional
        因子名称列表，默认 CNE6 风格因子
    start_date : str, optional
        起始日期
    end_date : str, optional
        结束日期
    count : int, optional
        数据点数量
    universe : str, optional
        指数股票池
    industry : str, default 'sw_l1'
        行业分类标准
    category : str, optional
        因子类别，若提供则仅返回该类别下的因子
    use_real_data : bool, default False
        是否使用真实数据计算（Fama-MacBeth回归），默认使用模拟数据

    Returns
    -------
    pd.DataFrame
        索引为日期，列为因子名称，值为因子日收益率。
    """
    if use_real_data:
        return _get_real_factor_style_returns(
            factors=factors,
            start_date=start_date,
            end_date=end_date,
            universe=universe,
            industry=industry,
        )

    if factors is None:
        factors = CNE6_STYLE_FACTORS.copy()

    if category is not None:
        factors = [
            f
            for f in factors
            if f in FACTOR_LIBRARY.get(category, {}).get("factors", {})
        ]

    n_days = count if count else 60
    dates = _generate_trading_dates(n_days)

    if start_date:
        dates = dates[dates >= pd.Timestamp(start_date)]
    if end_date:
        dates = dates[dates <= pd.Timestamp(end_date)]

    n = len(dates)
    common_rng = np.random.RandomState(42)
    common_factor = common_rng.normal(0, 0.005, n)

    result = {}
    for factor in factors:
        seed = _hash_seed(f"{factor}_style_{industry}")
        rng = np.random.RandomState(seed)
        vol = rng.uniform(0.003, 0.01)
        specific = rng.normal(0, vol, n)
        corr = rng.uniform(0.1, 0.4)
        returns = corr * common_factor + np.sqrt(1 - corr**2) * specific
        returns = np.clip(returns, -0.02, 0.02)
        result[factor] = np.round(returns, 6)

    return pd.DataFrame(result, index=dates)


def _get_real_factor_style_returns(
    factors: Optional[List[str]] = None,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    universe: str = "hs300",
    industry: str = "sw_l1",
) -> pd.DataFrame:
    """
    使用真实数据计算风格因子收益率。

    调用 analysis.factors.risk.compute_style_factor_returns_real 进行计算。
    """
    from jk2bt.analysis.factors.risk import compute_style_factor_returns_real

    try:
        result = compute_style_factor_returns_real(
            factors=factors,
            start_date=start_date,
            end_date=end_date,
            universe=universe,
            industry=industry,
        )
        if result.empty:
            warnings.warn("真实因子收益计算失败，回退到模拟数据")
            return get_factor_style_returns(
                factors=factors,
                start_date=start_date,
                end_date=end_date,
                universe=universe,
                industry=industry,
                use_real_data=False,
            )
        return result
    except Exception as e:
        warnings.warn(f"真实因子收益计算异常: {e}，回退到模拟数据")
        return get_factor_style_returns(
            factors=factors,
            start_date=start_date,
            end_date=end_date,
            universe=universe,
            industry=industry,
            use_real_data=False,
        )


def get_factor_cov(
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    factors: Optional[List[str]] = None,
    columns: Optional[List[str]] = None,
    industry: str = "sw_l1",
    universe: Optional[str] = None,
    format: str = "matrix",
) -> pd.DataFrame:
    """
    获取风格因子协方差矩阵（聚宽标准接口）。

    参数
    ----
    start_date : str, optional
        起始日期
    end_date : str, optional
        结束日期
    factors : list, optional
        因子列表
    columns : list, optional
        返回列
    industry : str, default 'sw_l1'
        行业分类
    universe : str, optional
        股票池
    format : str, default 'matrix'
        返回格式: 'matrix' 返回方阵协方差矩阵, 'long' 返回长表格式
        长表格式: 每行 (date, factor, column1, column2, ...)

    返回
    ----
    pd.DataFrame
        风格因子协方差矩阵（format='matrix'）或长表格式（format='long'）
    """
    try:
        factor_returns = get_factor_style_returns(
            factors=factors,
            start_date=start_date,
            end_date=end_date,
            universe=universe,
            industry=industry,
            use_real_data=True,
        )
    except Exception:
        factor_returns = get_factor_style_returns(
            factors=factors,
            start_date=start_date,
            end_date=end_date,
            universe=universe,
            industry=industry,
            use_real_data=False,
        )

    if factor_returns.empty:
        return pd.DataFrame()

    cov_matrix = factor_returns.cov()

    if columns is not None:
        cov_matrix = cov_matrix[columns]
        cov_matrix = cov_matrix.loc[columns]

    if format == "long":
        return _cov_matrix_to_long(cov_matrix, industry=industry)

    return cov_matrix


def _cov_matrix_to_long(
    cov_matrix: pd.DataFrame,
    industry: str = "sw_l1",
) -> pd.DataFrame:
    """
    将协方差方阵转换为长表格式。

    每行: (date, factor, cov_with_factor1, cov_with_factor2, ...)
    列包括风格因子和行业因子。

    参数
    ----
    cov_matrix : pd.DataFrame
        协方差方阵，索引和列均为因子名称
    industry : str, default 'sw_l1'
        行业分类标准

    返回
    ----
    pd.DataFrame
        长表格式协方差数据
    """
    date = pd.Timestamp("2026-03-31")
    all_factors = list(cov_matrix.columns)

    industry_factors = FACTOR_LIBRARY.get("industry", {}).get("factors", {})
    for ind_name in industry_factors:
        if ind_name not in all_factors:
            all_factors.append(ind_name)

    rows = []
    for factor in all_factors:
        row = {"date": date, "factor": factor}
        for col_factor in all_factors:
            if factor in cov_matrix.index and col_factor in cov_matrix.columns:
                row[col_factor] = round(cov_matrix.loc[factor, col_factor], 8)
            else:
                row[col_factor] = 0.0
        rows.append(row)

    return pd.DataFrame(rows)


def get_factor_specific_returns(
    security: str,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    count: Optional[int] = None,
    category: Optional[str] = None,
    universe: Optional[str] = None,
    industry: str = "sw_l1",
) -> pd.DataFrame:
    """
    获取个股特异性收益（风格因子无法解释的部分）。

    Parameters
    ----------
    security : str or list
        股票代码或代码列表
    start_date : str, optional
        起始日期
    end_date : str, optional
        结束日期
    count : int, optional
        数据点数量
    category : str, optional
        因子类别，影响种子生成以保证可复现性
    universe : str, optional
        指数股票池，影响种子生成以保证可复现性
    industry : str, default 'sw_l1'
        行业分类标准，影响种子生成以保证可复现性

    Returns
    -------
    pd.DataFrame
        索引为日期，列为股票代码，值为特异性日收益率。
    """
    if isinstance(security, str):
        securities = [security]
    else:
        securities = list(security)

    n_days = count if count else 60
    dates = _generate_trading_dates(n_days)

    if start_date:
        dates = dates[dates >= pd.Timestamp(start_date)]
    if end_date:
        dates = dates[dates <= pd.Timestamp(end_date)]

    n = len(dates)
    result = {}
    for sec in securities:
        seed_parts = [f"{sec}_specific"]
        if category is not None:
            seed_parts.append(category)
        if universe is not None:
            seed_parts.append(universe)
        if industry is not None:
            seed_parts.append(industry)
        seed = _hash_seed("_".join(seed_parts))
        rng = np.random.RandomState(seed)
        vol = rng.uniform(0.005, 0.015)
        returns = rng.normal(0, vol, n)
        returns = np.clip(returns, -0.03, 0.03)
        result[sec] = np.round(returns, 6)

    return pd.DataFrame(result, index=dates)


__all__ = [
    "get_all_factors",
    "get_factor_kanban_values",
    "get_factor_stats",
    "get_factor_style_returns",
    "get_factor_specific_returns",
    "get_factor_cov",
]
