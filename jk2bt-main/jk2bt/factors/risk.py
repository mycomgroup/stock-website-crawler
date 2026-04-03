"""
jk2bt/factors/risk.py
风险因子计算模块

提供因子风险相关的计算功能。
纯本地计算，不依赖远程数据。

主要功能:
- get_factor_cov: 计算因子协方差矩阵
- get_factor_variance: 计算因子方差
- get_factor_correlation: 计算因子相关性
- factor_risk_analysis: 因子风险分析
"""

import numpy as np
import pandas as pd
from typing import Optional, List, Union, Tuple, Dict
import warnings


def get_factor_cov(
    factor_returns: pd.DataFrame,
    method: str = "sample",
    shrinkage: Optional[float] = None,
    halflife: Optional[int] = None,
) -> pd.DataFrame:
    """
    计算因子协方差矩阵。

    参数
    ----
    factor_returns : pd.DataFrame
        因子收益数据，index 为日期，columns 为因子名称
    method : str, default 'sample'
        协方差估计方法:
        - 'sample': 样本协方差
        - 'shrinkage': 压缩估计
        - 'ewma': 指数加权移动平均
    shrinkage : float, optional
        压缩系数 (0-1)，仅 method='shrinkage' 时使用
    halflife : int, optional
        半衰期，仅 method='ewma' 时使用

    返回
    ----
    pd.DataFrame
        因子协方差矩阵

    示例
    ----
    >>> factor_returns = pd.DataFrame(...)  # 因子收益数据
    >>> cov = get_factor_cov(factor_returns)
    >>> print(cov.shape)
    (10, 10)
    """
    # 去除缺失值
    factor_returns = factor_returns.dropna()

    if len(factor_returns) < 2:
        warnings.warn("数据不足，无法计算协方差矩阵")
        return pd.DataFrame()

    if method == "sample":
        cov = factor_returns.cov()
    elif method == "shrinkage":
        cov = _shrinkage_cov(factor_returns, shrinkage)
    elif method == "ewma":
        cov = _ewma_cov(factor_returns, halflife)
    else:
        cov = factor_returns.cov()

    return cov


def _shrinkage_cov(
    returns: pd.DataFrame,
    shrinkage: Optional[float] = None,
) -> pd.DataFrame:
    """
    压缩协方差估计。

    使用 Ledoit-Wolf 方法或指定压缩系数
    """
    n = len(returns)
    p = returns.shape[1]

    # 样本协方差
    sample_cov = returns.cov()

    # 目标矩阵 (对角矩阵)
    target = np.diag(np.diag(sample_cov.values))

    # 计算最优压缩系数
    if shrinkage is None:
        # 使用 Ledoit-Wolf 公式
        shrinkage = _ledoit_wolf_shrinkage(returns.values, sample_cov.values)

    # 压缩协方差
    shrunk_cov = shrinkage * target + (1 - shrinkage) * sample_cov.values

    return pd.DataFrame(shrunk_cov, index=sample_cov.index, columns=sample_cov.columns)


def _ledoit_wolf_shrinkage(
    X: np.ndarray,
    sample_cov: np.ndarray,
) -> float:
    """
    计算 Ledoit-Wolf 最优压缩系数。

    参考: Ledoit & Wolf (2004) "A Well-Conditioned Estimator for Large-Dimensional Covariance Matrices"
    """
    n, p = X.shape

    # 标准化
    X_centered = X - X.mean(axis=0)
    X_std = X_centered / X_centered.std(axis=0, ddof=1)

    # 计算样本相关矩阵
    sample_corr = np.corrcoef(X_std.T)

    # 目标: 单位矩阵
    target = np.eye(p)

    # 计算压缩系数
    delta = np.sum((sample_corr - target) ** 2) / p

    # 计算 Frobenius 范数的期望
    y = X_std ** 2
    phi = np.sum(
        np.sum(y[:, :, np.newaxis] * y[:, np.newaxis, :], axis=0) / n - sample_corr ** 2
    ) / p

    # 压缩系数
    shrinkage = max(0, min(1, phi / delta)) if delta > 0 else 0

    return shrinkage


def _ewma_cov(
    returns: pd.DataFrame,
    halflife: Optional[int] = None,
) -> pd.DataFrame:
    """
    指数加权移动平均协方差估计。
    """
    if halflife is None:
        halflife = 20  # 默认半衰期

    # 计算衰减因子
    alpha = 1 - np.exp(-np.log(2) / halflife)

    # 使用 ewm 计算协方差
    # 对每个因子对计算 EWMA 相关性
    factors = returns.columns
    n = len(factors)
    cov_matrix = np.zeros((n, n))

    returns_centered = returns - returns.ewm(halflife=halflife).mean()

    for i, fi in enumerate(factors):
        for j, fj in enumerate(factors):
            # 计算协方差
            cov_ij = (returns_centered[fi] * returns_centered[fj]).ewm(halflife=halflife).mean().iloc[-1]
            cov_matrix[i, j] = cov_ij

    return pd.DataFrame(cov_matrix, index=factors, columns=factors)


def get_factor_variance(
    factor_returns: pd.DataFrame,
    annualize: bool = True,
    periods_per_year: int = 252,
) -> pd.Series:
    """
    计算因子方差。

    参数
    ----
    factor_returns : pd.DataFrame
        因子收益数据
    annualize : bool, default True
        是否年化
    periods_per_year : int, default 252
        年化周期数

    返回
    ----
    pd.Series
        因子方差
    """
    variance = factor_returns.var()

    if annualize:
        variance = variance * periods_per_year

    return variance


def get_factor_correlation(
    factor_returns: pd.DataFrame,
    method: str = "pearson",
) -> pd.DataFrame:
    """
    计算因子相关性矩阵。

    参数
    ----
    factor_returns : pd.DataFrame
        因子收益数据
    method : str, default 'pearson'
        相关性计算方法: 'pearson' 或 'spearman'

    返回
    ----
    pd.DataFrame
        因子相关性矩阵
    """
    return factor_returns.corr(method=method)


def factor_risk_analysis(
    factor_returns: pd.DataFrame,
    portfolio_weights: Optional[np.ndarray] = None,
) -> pd.DataFrame:
    """
    因子风险分析。

    参数
    ----
    factor_returns : pd.DataFrame
        因子收益数据
    portfolio_weights : np.ndarray, optional
        组合因子暴露权重

    返回
    ----
    pd.DataFrame
        风险分析结果:
        - variance: 因子方差
        - std: 因子标准差
        - contribution: 风险贡献 (如有组合权重)
    """
    # 计算方差
    variance = get_factor_variance(factor_returns, annualize=False)
    std = np.sqrt(variance)

    result = pd.DataFrame({
        "variance": variance,
        "std": std,
    })

    # 计算风险贡献
    if portfolio_weights is not None:
        cov = get_factor_cov(factor_returns)
        portfolio_var = portfolio_weights @ cov.values @ portfolio_weights

        # 边际风险贡献
        mcr = cov.values @ portfolio_weights / np.sqrt(portfolio_var)
        # 风险贡献
        cr = portfolio_weights * mcr / np.sqrt(portfolio_var) * 100

        result["marginal_contribution"] = mcr
        result["risk_contribution_pct"] = cr

    return result


def portfolio_factor_risk(
    factor_exposure: np.ndarray,
    factor_cov: pd.DataFrame,
    idiosyncratic_var: Optional[float] = None,
) -> Dict[str, float]:
    """
    计算组合因子风险。

    参数
    ----
    factor_exposure : np.ndarray
        组合因子暴露
    factor_cov : pd.DataFrame
        因子协方差矩阵
    idiosyncratic_var : float, optional
        特质风险方差

    返回
    ----
    Dict[str, float]
        风险分解:
        - total_risk: 总风险
        - factor_risk: 因子风险
        - idiosyncratic_risk: 特质风险
    """
    # 因子风险
    factor_variance = factor_exposure @ factor_cov.values @ factor_exposure
    factor_risk = np.sqrt(factor_variance)

    # 特质风险
    if idiosyncratic_var is not None:
        idiosyncratic_risk = np.sqrt(idiosyncratic_var)
        total_variance = factor_variance + idiosyncratic_var
    else:
        idiosyncratic_risk = 0
        total_variance = factor_variance

    total_risk = np.sqrt(total_variance)

    return {
        "total_risk": total_risk,
        "factor_risk": factor_risk,
        "idiosyncratic_risk": idiosyncratic_risk,
        "factor_risk_pct": factor_risk / total_risk * 100 if total_risk > 0 else 0,
    }


def rolling_factor_cov(
    factor_returns: pd.DataFrame,
    window: int = 60,
    method: str = "sample",
) -> pd.DataFrame:
    """
    滚动计算因子协方差矩阵。

    参数
    ----
    factor_returns : pd.DataFrame
        因子收益数据
    window : int, default 60
        滚动窗口大小
    method : str, default 'sample'
        协方差估计方法

    返回
    ----
    pd.DataFrame
        滚动协方差矩阵 (只保留最后一个时间点的结果)
    """
    if len(factor_returns) < window:
        warnings.warn(f"数据不足 {len(factor_returns)} < {window}")
        return get_factor_cov(factor_returns, method)

    return factor_returns.tail(window).cov()


def eigenvalue_decomposition(
    cov_matrix: pd.DataFrame,
    top_n: Optional[int] = None,
) -> Dict[str, Union[np.ndarray, pd.DataFrame]]:
    """
    特征值分解。

    对协方差矩阵进行特征值分解，用于主成分分析。

    参数
    ----
    cov_matrix : pd.DataFrame
        协方差矩阵
    top_n : int, optional
        保留前N个主成分

    返回
    ----
    Dict
        - eigenvalues: 特征值
        - eigenvectors: 特征向量
        - explained_variance_ratio: 解释方差比例
    """
    # 确保矩阵是对称的
    cov_values = (cov_matrix.values + cov_matrix.values.T) / 2

    # 特征值分解
    eigenvalues, eigenvectors = np.linalg.eigh(cov_values)

    # 按特征值降序排列
    idx = np.argsort(eigenvalues)[::-1]
    eigenvalues = eigenvalues[idx]
    eigenvectors = eigenvectors[:, idx]

    # 解释方差比例
    explained_variance_ratio = eigenvalues / eigenvalues.sum()

    # 截断
    if top_n is not None:
        eigenvalues = eigenvalues[:top_n]
        eigenvectors = eigenvectors[:, :top_n]
        explained_variance_ratio = explained_variance_ratio[:top_n]

    return {
        "eigenvalues": eigenvalues,
        "eigenvectors": pd.DataFrame(
            eigenvectors,
            index=cov_matrix.index,
            columns=[f"PC{i+1}" for i in range(eigenvectors.shape[1])],
        ),
        "explained_variance_ratio": explained_variance_ratio,
    }


__all__ = [
    "get_factor_cov",
    "get_factor_variance",
    "get_factor_correlation",
    "factor_risk_analysis",
    "portfolio_factor_risk",
    "rolling_factor_cov",
    "eigenvalue_decomposition",
]