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
    y = X_std**2
    phi = (
        np.sum(
            np.sum(y[:, :, np.newaxis] * y[:, np.newaxis, :], axis=0) / n
            - sample_corr**2
        )
        / p
    )

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
            cov_ij = (
                (returns_centered[fi] * returns_centered[fj])
                .ewm(halflife=halflife)
                .mean()
                .iloc[-1]
            )
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

    result = pd.DataFrame(
        {
            "variance": variance,
            "std": std,
        }
    )

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


def compute_factor_covariance(
    factor_returns: pd.DataFrame,
    window: int = 252,
) -> pd.DataFrame:
    """
    计算因子协方差矩阵。

    Parameters
    ----------
    factor_returns : pd.DataFrame
        因子收益率时间序列
    window : int
        滚动窗口大小（交易日）

    Returns
    -------
    pd.DataFrame
        因子协方差矩阵
    """
    if factor_returns.empty or len(factor_returns) < 2:
        warnings.warn("数据不足，无法计算因子协方差矩阵")
        return pd.DataFrame()

    return factor_returns.tail(window).cov()


def compute_style_factor_returns_real(
    factors: Optional[List[str]] = None,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    universe: str = "hs300",
    industry: str = "sw_l1",
) -> pd.DataFrame:
    """
    使用真实数据计算风格因子收益率（Fama-MacBeth方法）。

    步骤:
    1. 获取股票池内所有股票的日收益率
    2. 计算每只股票在各风格因子上的暴露值
    3. 对每个交易日进行横截面回归: R_i = alpha + sum(beta_k * f_k) + epsilon_i
    4. 返回因子收益率时间序列

    Parameters
    ----------
    factors : list, optional
        因子名称列表，默认使用 CNE6 风格因子
        ['size', 'beta', 'momentum', 'volatility', 'liquidity',
         'growth', 'leverage', 'earnings_yield', 'book_to_price', 'profitability']
    start_date : str, optional
        起始日期，格式 'YYYY-MM-DD'
    end_date : str, optional
        结束日期，格式 'YYYY-MM-DD'
    universe : str, default 'hs300'
        股票池，支持 'hs300', 'csi500', 'csi1000', 'zz800', 'zzqz'
    industry : str, default 'sw_l1'
        行业分类标准，暂未使用

    Returns
    -------
    pd.DataFrame
        因子收益率时间序列，index 为日期，columns 为因子名称

    Raises
    ------
    ImportError
        当依赖模块不可用时
    ValueError
        当参数不合法时
    """
    from jk2bt.api.jq_compat import get_index_stocks, get_price, get_fundamentals
    from jk2bt.api.jq_compat import query, valuation
    from jk2bt.api.factor_kanban import CNE6_STYLE_FACTORS

    if factors is None:
        factors = CNE6_STYLE_FACTORS.copy()

    # 映射指数代码
    index_map = {
        "hs300": "000300.XSHG",
        "csi500": "000905.XSHG",
        "csi1000": "000852.XSHG",
        "zz800": "000906.XSHG",
        "zzqz": "000985.XSHG",
    }
    index_code = index_map.get(universe, "000300.XSHG")

    # 设置默认日期范围（最近一年）
    if end_date is None:
        end_date = pd.Timestamp.now().strftime("%Y-%m-%d")
    if start_date is None:
        start_dt = pd.Timestamp(end_date) - pd.Timedelta(days=365)
        start_date = start_dt.strftime("%Y-%m-%d")

    # 1. 获取股票池
    try:
        stocks = get_index_stocks(index_code)
    except Exception as e:
        warnings.warn(f"获取指数成分股失败: {e}")
        return pd.DataFrame()

    if not stocks:
        warnings.warn(f"指数 {universe} 成分股为空")
        return pd.DataFrame()

    # 限制股票数量以提高性能
    max_stocks = 100
    if len(stocks) > max_stocks:
        stocks = stocks[:max_stocks]

    # 2. 获取股票价格数据计算收益率
    try:
        price_data = get_price(
            stocks,
            start_date=start_date,
            end_date=end_date,
            frequency="daily",
            fields=["close"],
            skip_paused=True,
            fq="pre",
            panel=False,
        )
    except Exception as e:
        warnings.warn(f"获取价格数据失败: {e}")
        return pd.DataFrame()

    if price_data.empty:
        warnings.warn("价格数据为空")
        return pd.DataFrame()

    # 构建收益率矩阵
    returns_pivot = price_data.pivot_table(
        index="datetime", columns="code", values="close"
    )
    daily_returns = returns_pivot.pct_change().dropna()

    if daily_returns.empty:
        warnings.warn("收益率数据为空")
        return pd.DataFrame()

    # 3. 计算因子暴露
    factor_exposures = _calculate_factor_exposures(
        stocks, daily_returns.index[-1], factors
    )

    if factor_exposures.empty:
        warnings.warn("因子暴露计算失败")
        return pd.DataFrame()

    # 确保只有有因子暴露的股票参与回归
    common_stocks = list(set(daily_returns.columns) & set(factor_exposures.index))
    if len(common_stocks) < 10:
        warnings.warn("有效股票数量不足，无法进行横截面回归")
        return pd.DataFrame()

    returns_matrix = daily_returns[common_stocks]
    exposures_matrix = factor_exposures.loc[common_stocks]

    # 标准化因子暴露（横截面 z-score）
    exposures_matrix = (
        exposures_matrix - exposures_matrix.mean()
    ) / exposures_matrix.std()
    exposures_matrix = exposures_matrix.fillna(0)

    # 4. Fama-MacBeth 横截面回归
    factor_return_list = []

    for date_idx in range(len(returns_matrix)):
        date = returns_matrix.index[date_idx]
        stock_returns = returns_matrix.iloc[date_idx].values

        # 构建回归矩阵
        valid_mask = ~np.isnan(stock_returns)
        if valid_mask.sum() < 10:
            continue

        y = stock_returns[valid_mask]
        X = exposures_matrix.values[valid_mask]

        # 添加常数项
        X_with_const = np.column_stack([np.ones(len(y)), X])

        try:
            # OLS 回归: (X'X)^(-1) X'y
            XtX = X_with_const.T @ X_with_const
            Xty = X_with_const.T @ y
            coeffs = np.linalg.solve(XtX, Xty)

            # 提取因子收益率（跳过常数项）
            factor_returns_row = {"date": date}
            for i, factor_name in enumerate(factors):
                factor_returns_row[factor_name] = coeffs[i + 1]
            factor_return_list.append(factor_returns_row)

        except np.linalg.LinAlgError:
            continue

    if not factor_return_list:
        warnings.warn("横截面回归未产生有效结果")
        return pd.DataFrame()

    result_df = pd.DataFrame(factor_return_list)
    result_df.set_index("date", inplace=True)

    return result_df


def _calculate_factor_exposures(
    stocks: List[str],
    date: Union[str, pd.Timestamp],
    factors: List[str],
) -> pd.DataFrame:
    """
    计算股票在各风格因子上的暴露值。

    Parameters
    ----------
    stocks : List[str]
        股票代码列表
    date : str or pd.Timestamp
        计算日期
    factors : List[str]
        因子名称列表

    Returns
    -------
    pd.DataFrame
        因子暴露矩阵，index 为股票代码，columns 为因子名称
    """
    from jk2bt.api.jq_compat import get_fundamentals, query, valuation
    from jk2bt.api.jq_compat import get_price

    date_str = str(date)[:10] if isinstance(date, pd.Timestamp) else str(date)[:10]

    exposures = pd.DataFrame(index=stocks)

    # 获取估值数据
    try:
        valuation_df = get_fundamentals(
            query(valuation).filter(valuation.code.in_(stocks)),
            date=date_str,
        )
    except Exception:
        valuation_df = pd.DataFrame()

    if not valuation_df.empty and "code" in valuation_df.columns:
        valuation_df.set_index("code", inplace=True)

    # Size因子: ln(market_cap)
    if "size" in factors:
        if not valuation_df.empty and "market_cap" in valuation_df.columns:
            exposures["size"] = np.log(valuation_df["market_cap"])
        else:
            exposures["size"] = 0.0

    # Beta因子: 使用过去一年的日收益率对市场收益率回归
    if "beta" in factors:
        exposures["beta"] = _calculate_beta(stocks, date_str)

    # Momentum因子: 过去12个月收益率（剔除最近1个月）
    if "momentum" in factors:
        exposures["momentum"] = _calculate_momentum(stocks, date_str)

    # Volatility因子: 过去一年的日收益率标准差
    if "volatility" in factors:
        exposures["volatility"] = _calculate_volatility(stocks, date_str)

    # Liquidity因子: 过去一个月的平均换手率（用成交量/流通市值近似）
    if "liquidity" in factors:
        if not valuation_df.empty and "circulating_market_cap" in valuation_df.columns:
            exposures["liquidity"] = _calculate_liquidity(
                stocks, date_str, valuation_df["circulating_market_cap"]
            )
        else:
            exposures["liquidity"] = 0.0

    # Growth因子: 营业收入增长率
    if "growth" in factors:
        if (
            not valuation_df.empty
            and "inc_revenue_year_on_year" in valuation_df.columns
        ):
            exposures["growth"] = valuation_df["inc_revenue_year_on_year"]
        else:
            exposures["growth"] = 0.0

    # Leverage因子: 资产负债率
    if "leverage" in factors:
        if not valuation_df.empty and "debt_to_asset" in valuation_df.columns:
            exposures["leverage"] = valuation_df["debt_to_asset"]
        else:
            exposures["leverage"] = 0.0

    # Earnings Yield因子: 盈利收益率 (EP = 1/PE)
    if "earnings_yield" in factors:
        if not valuation_df.empty and "pe_ratio" in valuation_df.columns:
            pe = valuation_df["pe_ratio"].copy()
            pe = pe.replace(0, np.nan)
            exposures["earnings_yield"] = 1.0 / pe
            exposures["earnings_yield"] = exposures["earnings_yield"].fillna(0)
        else:
            exposures["earnings_yield"] = 0.0

    # Book to Price因子: 账面市值比 (1/PB)
    if "book_to_price" in factors or "book_to_market" in factors:
        col_name = "book_to_price" if "book_to_price" in factors else "book_to_market"
        if not valuation_df.empty and "pb_ratio" in valuation_df.columns:
            pb = valuation_df["pb_ratio"].copy()
            pb = pb.replace(0, np.nan)
            exposures[col_name] = 1.0 / pb
            exposures[col_name] = exposures[col_name].fillna(0)
        else:
            exposures[col_name] = 0.0

    # Profitability因子: ROE
    if "profitability" in factors:
        if not valuation_df.empty and "roe_ratio" in valuation_df.columns:
            exposures["profitability"] = valuation_df["roe_ratio"]
        else:
            exposures["profitability"] = 0.0

    # 填充缺失值
    exposures = exposures.fillna(0)

    # 处理无穷大值
    exposures = exposures.replace([np.inf, -np.inf], 0)

    return exposures


def _calculate_beta(
    stocks: List[str],
    date_str: str,
    window: int = 252,
) -> pd.Series:
    """
    计算股票 Beta 值。

    使用过去 window 个交易日的日收益率对市场收益率回归。
    """
    from jk2bt.api.jq_compat import get_index_stocks, get_price

    try:
        start_dt = pd.Timestamp(date_str) - pd.Timedelta(days=window * 2)
        start_str = start_dt.strftime("%Y-%m-%d")

        # 获取沪深300指数作为市场基准
        index_prices = get_price(
            "000300.XSHG",
            start_date=start_str,
            end_date=date_str,
            frequency="daily",
            fields=["close"],
            skip_paused=True,
        )

        if index_prices is None or index_prices.empty:
            return pd.Series(1.0, index=stocks)

        market_returns = index_prices["close"].pct_change().dropna()

        betas = {}
        for stock in stocks[:50]:  # 限制计算量
            try:
                stock_prices = get_price(
                    stock,
                    start_date=start_str,
                    end_date=date_str,
                    frequency="daily",
                    fields=["close"],
                    skip_paused=True,
                )

                if stock_prices is None or stock_prices.empty:
                    betas[stock] = 1.0
                    continue

                stock_returns = stock_prices["close"].pct_change().dropna()

                # 对齐数据
                common_idx = market_returns.index.intersection(stock_returns.index)
                if len(common_idx) < 60:
                    betas[stock] = 1.0
                    continue

                m_ret = market_returns.loc[common_idx].values
                s_ret = stock_returns.loc[common_idx].values

                # 计算 beta = Cov(R_s, R_m) / Var(R_m)
                cov = np.cov(s_ret, m_ret)[0, 1]
                var_m = np.var(m_ret)

                if var_m > 0:
                    betas[stock] = cov / var_m
                else:
                    betas[stock] = 1.0

            except Exception:
                betas[stock] = 1.0

        # 对于未计算的股票，使用平均值
        mean_beta = np.mean(list(betas.values())) if betas else 1.0
        for stock in stocks:
            if stock not in betas:
                betas[stock] = mean_beta

        return pd.Series(betas)

    except Exception:
        return pd.Series(1.0, index=stocks)


def _calculate_momentum(
    stocks: List[str],
    date_str: str,
    skip_months: int = 1,
    lookback_months: int = 12,
) -> pd.Series:
    """
    计算动量因子：过去12个月收益率（剔除最近1个月）。
    """
    from jk2bt.api.jq_compat import get_price

    try:
        end_dt = pd.Timestamp(date_str)
        start_dt = end_dt - pd.Timedelta(days=(lookback_months + skip_months) * 30)
        start_str = start_dt.strftime("%Y-%m-%d")

        momentums = {}
        for stock in stocks[:50]:
            try:
                prices = get_price(
                    stock,
                    start_date=start_str,
                    end_date=date_str,
                    frequency="daily",
                    fields=["close"],
                    skip_paused=True,
                )

                if prices is None or prices.empty or len(prices) < 60:
                    momentums[stock] = 0.0
                    continue

                close = prices["close"]
                # 计算 skip_months 前的价格和 lookback_months 前的价格
                skip_days = skip_months * 20
                lookback_days = lookback_months * 20

                if len(close) < lookback_days:
                    momentums[stock] = 0.0
                    continue

                price_start = close.iloc[-lookback_days]
                price_end = (
                    close.iloc[-skip_days] if len(close) > skip_days else close.iloc[-1]
                )

                momentums[stock] = (price_end / price_start) - 1.0

            except Exception:
                momentums[stock] = 0.0

        mean_momentum = np.mean(list(momentums.values())) if momentums else 0.0
        for stock in stocks:
            if stock not in momentums:
                momentums[stock] = mean_momentum

        return pd.Series(momentums)

    except Exception:
        return pd.Series(0.0, index=stocks)


def _calculate_volatility(
    stocks: List[str],
    date_str: str,
    window: int = 252,
) -> pd.Series:
    """
    计算波动率因子：过去一年的日收益率标准差。
    """
    from jk2bt.api.jq_compat import get_price

    try:
        start_dt = pd.Timestamp(date_str) - pd.Timedelta(days=window * 2)
        start_str = start_dt.strftime("%Y-%m-%d")

        vols = {}
        for stock in stocks[:50]:
            try:
                prices = get_price(
                    stock,
                    start_date=start_str,
                    end_date=date_str,
                    frequency="daily",
                    fields=["close"],
                    skip_paused=True,
                )

                if prices is None or prices.empty or len(prices) < 60:
                    vols[stock] = 0.0
                    continue

                returns = prices["close"].pct_change().dropna()
                vols[stock] = returns.std() * np.sqrt(252)

            except Exception:
                vols[stock] = 0.0

        mean_vol = np.mean(list(vols.values())) if vols else 0.0
        for stock in stocks:
            if stock not in vols:
                vols[stock] = mean_vol

        return pd.Series(vols)

    except Exception:
        return pd.Series(0.0, index=stocks)


def _calculate_liquidity(
    stocks: List[str],
    date_str: str,
    circulating_caps: pd.Series,
    window: int = 20,
) -> pd.Series:
    """
    计算流动性因子：过去一个月的日均换手率。
    使用成交量/流通股本近似。
    """
    from jk2bt.api.jq_compat import get_price

    try:
        start_dt = pd.Timestamp(date_str) - pd.Timedelta(days=window * 2)
        start_str = start_dt.strftime("%Y-%m-%d")

        liqs = {}
        for stock in stocks[:50]:
            try:
                prices = get_price(
                    stock,
                    start_date=start_str,
                    end_date=date_str,
                    frequency="daily",
                    fields=["volume"],
                    skip_paused=True,
                )

                if prices is None or prices.empty:
                    liqs[stock] = 0.0
                    continue

                # 使用成交量的对数作为流动性代理
                avg_volume = prices["volume"].mean()
                liqs[stock] = np.log1p(avg_volume)

            except Exception:
                liqs[stock] = 0.0

        mean_liq = np.mean(list(liqs.values())) if liqs else 0.0
        for stock in stocks:
            if stock not in liqs:
                liqs[stock] = mean_liq

        return pd.Series(liqs)

    except Exception:
        return pd.Series(0.0, index=stocks)


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
            columns=[f"PC{i + 1}" for i in range(eigenvectors.shape[1])],
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
