"""
jk2bt/api/factor_analysis.py
因子分析 API 模块

提供 JQData 兼容的单因子分析接口。
纯本地计算，不依赖远程数据。

主要功能:
- FactorAnalyzer: 因子分析器类
- analyze_factor: 单因子分析快捷函数
- AttributionAnalysis: 归因分析类
"""

import numpy as np
import pandas as pd
from typing import Union, List, Dict, Optional, Tuple
import warnings


class FactorAnalyzer:
    """
    因子分析器类。

    对因子数据进行全面分析，包括：
    - IC 分析（信息系数）
    - 分位数收益分析
    - 换手率分析
    - 累积收益分析

    使用方式:
        >>> fa = FactorAnalyzer(factor_data, price_data)
        >>> ic = fa.ic()
        >>> returns = fa.mean_return_by_quantile()
        >>> turnover = fa.quantile_turnover()

    Parameters
    ----------
    factor_data : pd.DataFrame
        因子数据，index 为日期，columns 为股票代码
    price_data : pd.DataFrame
        价格数据，index 为日期，columns 为股票代码
    quantiles : int, default 5
        分位数数量
    periods : tuple, default (1, 5, 10)
        收益计算周期
    """

    def __init__(
        self,
        factor_data: pd.DataFrame,
        price_data: pd.DataFrame,
        quantiles: int = 5,
        periods: Tuple[int, ...] = (1, 5, 10),
    ):
        self.factor_data = factor_data
        self.price_data = price_data
        self.quantiles = quantiles
        self.periods = periods

        # 预计算收益
        self._returns = {}
        for period in periods:
            self._returns[period] = price_data.pct_change(period).shift(-period)

        # 预计算分位数分组
        self._quantile_groups = self._compute_quantile_groups()

    def _compute_quantile_groups(self) -> Dict[int, pd.DataFrame]:
        """计算分位数分组"""
        groups = {}
        for q in range(1, self.quantiles + 1):
            groups[q] = pd.DataFrame(index=self.factor_data.index, columns=self.factor_data.columns)
            for date in self.factor_data.index:
                factor_vals = self.factor_data.loc[date].dropna()
                if len(factor_vals) == 0:
                    continue
                # 按分位数分组
                lower = factor_vals.quantile((q - 1) / self.quantiles)
                upper = factor_vals.quantile(q / self.quantiles)
                mask = (factor_vals >= lower) & (factor_vals <= upper)
                groups[q].loc[date, mask.index] = mask.astype(float)
        return groups

    def ic(
        self,
        method: str = "spearman",
        demean: bool = True,
    ) -> pd.Series:
        """
        计算信息系数 (IC) 序列。

        IC 是因子值与未来收益的相关系数。

        Parameters
        ----------
        method : str, default 'spearman'
            相关性计算方法: 'spearman' 或 'pearson'
        demean : bool, default True
            是否对收益进行去均值处理

        Returns
        -------
        pd.Series
            IC 序列，index 为日期
        """
        ic_series = {}
        default_period = self.periods[0] if self.periods else 1

        for date in self.factor_data.index:
            factor_vals = self.factor_data.loc[date].dropna()
            return_vals = self._returns.get(default_period)
            if return_vals is None:
                continue
            ret_vals = return_vals.loc[date].dropna() if date in return_vals.index else pd.Series()

            # 取交集
            common = factor_vals.index.intersection(ret_vals.index)
            if len(common) < 5:
                continue

            factor_common = factor_vals[common]
            ret_common = ret_vals[common]

            if demean:
                ret_common = ret_common - ret_common.mean()

            # 计算相关系数
            if method == "spearman":
                ic = factor_common.rank().corr(ret_common.rank())
            else:
                ic = factor_common.corr(ret_common)

            ic_series[date] = ic

        return pd.Series(ic_series)

    def ic_by_group(
        self,
        industry_data: pd.DataFrame,
        method: str = "spearman",
    ) -> pd.DataFrame:
        """
        按行业分组计算 IC。

        Parameters
        ----------
        industry_data : pd.DataFrame
            行业映射数据，index 为日期，columns 为股票代码，值为行业代码
        method : str, default 'spearman'
            相关性计算方法

        Returns
        -------
        pd.DataFrame
            分行业 IC，index 为日期，columns 为行业代码
        """
        default_period = self.periods[0] if self.periods else 1
        return_vals = self._returns.get(default_period)
        if return_vals is None:
            return pd.DataFrame()

        result = {}

        for date in self.factor_data.index:
            factor_vals = self.factor_data.loc[date].dropna()
            ret_vals = return_vals.loc[date].dropna() if date in return_vals.index else pd.Series()

            if date not in industry_data.index:
                continue

            industry_vals = industry_data.loc[date]

            # 按行业计算 IC
            date_ic = {}
            for industry in industry_vals.dropna().unique():
                stocks = industry_vals[industry_vals == industry].index
                common = stocks.intersection(factor_vals.index).intersection(ret_vals.index)
                if len(common) < 3:
                    continue

                factor_common = factor_vals[common]
                ret_common = ret_vals[common]

                if method == "spearman":
                    ic = factor_common.rank().corr(ret_common.rank())
                else:
                    ic = factor_common.corr(ret_common)

                date_ic[industry] = ic

            result[date] = date_ic

        return pd.DataFrame(result).T

    def mean_return_by_quantile(
        self,
        period: Optional[int] = None,
        by_date: bool = False,
    ) -> Union[pd.DataFrame, pd.Series]:
        """
        计算分位数平均收益。

        Parameters
        ----------
        period : int, optional
            收益周期，默认使用第一个周期
        by_date : bool, default False
            是否按日期返回详细结果

        Returns
        -------
        pd.DataFrame or pd.Series
            分位数平均收益
        """
        if period is None:
            period = self.periods[0] if self.periods else 1

        return_vals = self._returns.get(period)
        if return_vals is None:
            return pd.Series() if not by_date else pd.DataFrame()

        quantile_returns = {}

        for q in range(1, self.quantiles + 1):
            q_returns = []
            for date in self.factor_data.index:
                if date not in return_vals.index:
                    continue
                mask = self._quantile_groups[q].loc[date]
                if mask.isna().all():
                    continue
                factor_mask = self.factor_data.loc[date].notna()
                valid_mask = mask.fillna(0) * factor_mask.astype(float)
                ret_vals = return_vals.loc[date]

                # 计算等权平均收益
                valid_stocks = valid_mask[valid_mask > 0].index
                if len(valid_stocks) > 0:
                    mean_ret = ret_vals[valid_stocks].mean()
                    q_returns.append(mean_ret)

            if q_returns:
                quantile_returns[f"Q{q}"] = np.mean(q_returns)

        return pd.Series(quantile_returns)

    def quantile_turnover(
        self,
        period: int = 1,
    ) -> pd.DataFrame:
        """
        计算分位数换手率。

        换手率 = 分位数内股票变化比例

        Parameters
        ----------
        period : int, default 1
            计算周期

        Returns
        -------
        pd.DataFrame
            分位数换手率，index 为日期，columns 为分位数
        """
        turnover = {}

        dates = self.factor_data.index.tolist()

        for i in range(period, len(dates)):
            current_date = dates[i]
            prev_date = dates[i - period]

            current_factor = self.factor_data.loc[current_date].dropna()
            prev_factor = self.factor_data.loc[prev_date].dropna()

            common = current_factor.index.intersection(prev_factor.index)
            if len(common) < 5:
                continue

            date_turnover = {}

            for q in range(1, self.quantiles + 1):
                # 当前分位数股票
                lower = current_factor.quantile((q - 1) / self.quantiles)
                upper = current_factor.quantile(q / self.quantiles)
                current_stocks = set(current_factor[(current_factor >= lower) & (current_factor <= upper)].index)

                # 前一期分位数股票
                lower_prev = prev_factor.quantile((q - 1) / self.quantiles)
                upper_prev = prev_factor.quantile(q / self.quantiles)
                prev_stocks = set(prev_factor[(prev_factor >= lower_prev) & (prev_factor <= upper_prev)].index)

                # 计算换手率
                if len(current_stocks) > 0 and len(prev_stocks) > 0:
                    new_stocks = current_stocks - prev_stocks
                    turnover_rate = len(new_stocks) / len(current_stocks)
                    date_turnover[f"Q{q}"] = turnover_rate

            turnover[current_date] = date_turnover

        return pd.DataFrame(turnover).T

    def cumulative_returns(
        self,
        period: Optional[int] = None,
        quantile: Optional[int] = None,
    ) -> pd.DataFrame:
        """
        计算累积收益。

        Parameters
        ----------
        period : int, optional
            收益周期
        quantile : int, optional
            指定分位数，None 表示所有分位数

        Returns
        -------
        pd.DataFrame
            累积收益
        """
        if period is None:
            period = self.periods[0] if self.periods else 1

        return_vals = self._returns.get(period)
        if return_vals is None:
            return pd.DataFrame()

        # 获取分位数收益序列
        quantile_returns = {}

        for q in range(1, self.quantiles + 1):
            if quantile is not None and q != quantile:
                continue

            daily_returns = []
            dates = []

            for date in self.factor_data.index:
                if date not in return_vals.index:
                    continue
                mask = self._quantile_groups[q].loc[date]
                factor_mask = self.factor_data.loc[date].notna()
                valid_mask = mask.fillna(0) * factor_mask.astype(float)
                ret_vals = return_vals.loc[date]

                valid_stocks = valid_mask[valid_mask > 0].index
                if len(valid_stocks) > 0:
                    mean_ret = ret_vals[valid_stocks].mean()
                    daily_returns.append(mean_ret)
                    dates.append(date)

            if daily_returns:
                quantile_returns[f"Q{q}"] = pd.Series(daily_returns, index=dates)

        if not quantile_returns:
            return pd.DataFrame()

        df = pd.DataFrame(quantile_returns)

        # 计算累积收益
        return (1 + df).cumprod() - 1

    def calc_factor_alpha_beta(
        self,
        benchmark_returns: pd.Series,
        period: Optional[int] = None,
    ) -> Dict[str, float]:
        """
        计算因子 Alpha 和 Beta。

        Parameters
        ----------
        benchmark_returns : pd.Series
            基准收益序列
        period : int, optional
            收益周期

        Returns
        -------
        Dict[str, float]
            {'alpha': ..., 'beta': ...}
        """
        if period is None:
            period = self.periods[0] if self.periods else 1

        # 获取因子多空收益
        q1_returns = self._get_quantile_returns(1, period)
        q5_returns = self._get_quantile_returns(self.quantiles, period)

        if q1_returns is None or q5_returns is None:
            return {"alpha": 0.0, "beta": 0.0}

        long_short = q5_returns - q1_returns

        # 对齐日期
        common_dates = long_short.index.intersection(benchmark_returns.index)
        if len(common_dates) < 10:
            return {"alpha": 0.0, "beta": 0.0}

        y = long_short.loc[common_dates].values
        x = benchmark_returns.loc[common_dates].values

        # 线性回归
        x = x.reshape(-1, 1)
        x_with_intercept = np.column_stack([np.ones(len(x)), x])

        try:
            beta = np.linalg.lstsq(x_with_intercept, y, rcond=None)[0]
            return {"alpha": float(beta[0]), "beta": float(beta[1])}
        except Exception:
            return {"alpha": 0.0, "beta": 0.0}

    def _get_quantile_returns(self, quantile: int, period: int) -> Optional[pd.Series]:
        """获取指定分位数的收益序列"""
        return_vals = self._returns.get(period)
        if return_vals is None:
            return None

        daily_returns = []
        dates = []

        for date in self.factor_data.index:
            if date not in return_vals.index:
                continue
            mask = self._quantile_groups[quantile].loc[date]
            factor_mask = self.factor_data.loc[date].notna()
            valid_mask = mask.fillna(0) * factor_mask.astype(float)
            ret_vals = return_vals.loc[date]

            valid_stocks = valid_mask[valid_mask > 0].index
            if len(valid_stocks) > 0:
                mean_ret = ret_vals[valid_stocks].mean()
                daily_returns.append(mean_ret)
                dates.append(date)

        if daily_returns:
            return pd.Series(daily_returns, index=dates)
        return None

    def calc_autocorrelation(
        self,
        lag: int = 1,
    ) -> float:
        """
        计算因子自相关性。

        Parameters
        ----------
        lag : int, default 1
            滞后期数

        Returns
        -------
        float
            自相关系数
        """
        # 计算每个时间截面的因子排序
        factor_ranks = self.factor_data.rank(axis=1)

        # 计算自相关
        autocorr = []
        dates = factor_ranks.index.tolist()

        for i in range(lag, len(dates)):
            current = factor_ranks.loc[dates[i]].dropna()
            prev = factor_ranks.loc[dates[i - lag]].dropna()

            common = current.index.intersection(prev.index)
            if len(common) < 5:
                continue

            corr = current[common].corr(prev[common])
            autocorr.append(corr)

        return np.mean(autocorr) if autocorr else 0.0

    def summary(self) -> pd.DataFrame:
        """
        生成因子分析摘要报告。

        Returns
        -------
        pd.DataFrame
            分析摘要
        """
        ic = self.ic()
        ic_mean = ic.mean() if len(ic) > 0 else 0
        ic_std = ic.std() if len(ic) > 0 else 0
        icir = ic_mean / ic_std if ic_std != 0 else 0

        returns = self.mean_return_by_quantile()
        turnover = self.quantile_turnover().mean() if len(self.quantile_turnover()) > 0 else pd.Series()

        summary_data = {
            "IC均值": [ic_mean],
            "IC标准差": [ic_std],
            "ICIR": [icir],
            "IC > 0 占比": [(ic > 0).mean() if len(ic) > 0 else 0],
            "自相关系数": [self.calc_autocorrelation()],
        }

        # 添加分位数收益
        for q, ret in returns.items():
            summary_data[f"{q}平均收益"] = [ret]

        # 添加换手率
        for q, turn in turnover.items():
            summary_data[f"{q}换手率"] = [turn]

        return pd.DataFrame(summary_data, index=["统计值"]).T


def analyze_factor(
    factor_data: pd.DataFrame,
    price_data: pd.DataFrame,
    quantiles: int = 5,
    periods: Tuple[int, ...] = (1, 5, 10),
) -> Dict[str, Union[pd.Series, pd.DataFrame, float]]:
    """
    单因子分析快捷函数。

    对因子进行全面分析，返回分析结果字典。

    Parameters
    ----------
    factor_data : pd.DataFrame
        因子数据，index 为日期，columns 为股票代码
    price_data : pd.DataFrame
        价格数据，index 为日期，columns 为股票代码
    quantiles : int, default 5
        分位数数量
    periods : tuple, default (1, 5, 10)
        收益计算周期

    Returns
    -------
    Dict
        分析结果，包含:
        - 'ic': IC 序列
        - 'ic_mean': IC 均值
        - 'icir': ICIR
        - 'returns': 分位数平均收益
        - 'turnover': 分位数换手率
        - 'autocorr': 因子自相关系数
        - 'summary': 分析摘要

    Examples
    --------
    >>> factor_df = pd.DataFrame(...)  # 因子数据
    >>> price_df = pd.DataFrame(...)   # 价格数据
    >>> result = analyze_factor(factor_df, price_df)
    >>> print(result['ic_mean'])
    >>> print(result['returns'])
    """
    fa = FactorAnalyzer(factor_data, price_data, quantiles, periods)

    ic = fa.ic()

    result = {
        "ic": ic,
        "ic_mean": ic.mean() if len(ic) > 0 else 0,
        "ic_std": ic.std() if len(ic) > 0 else 0,
        "icir": (ic.mean() / ic.std()) if len(ic) > 0 and ic.std() != 0 else 0,
        "returns": fa.mean_return_by_quantile(),
        "turnover": fa.quantile_turnover(),
        "autocorr": fa.calc_autocorrelation(),
        "cumulative_returns": fa.cumulative_returns(),
        "summary": fa.summary(),
    }

    return result


class AttributionAnalysis:
    """
    归因分析类。

    对组合收益进行因子归因分析。

    Parameters
    ----------
    portfolio_returns : pd.Series
        组合收益序列，index 为日期
    factor_returns : pd.DataFrame
        因子收益序列，index 为日期，columns 为因子名称

    Examples
    --------
    >>> portfolio = pd.Series(...)  # 组合收益
    >>> factors = pd.DataFrame(...)  # 因子收益
    >>> aa = AttributionAnalysis(portfolio, factors)
    >>> attribution = aa.attribution()
    """

    def __init__(
        self,
        portfolio_returns: pd.Series,
        factor_returns: pd.DataFrame,
    ):
        self.portfolio_returns = portfolio_returns
        self.factor_returns = factor_returns

        # 对齐日期
        common_dates = portfolio_returns.index.intersection(factor_returns.index)
        self.portfolio_returns = portfolio_returns.loc[common_dates]
        self.factor_returns = factor_returns.loc[common_dates]

        # 计算因子暴露
        self._exposures = None
        self._residual = None

    def factor_exposure(self) -> pd.Series:
        """
        计算因子暴露。

        通过回归计算组合对各因子的暴露。

        Returns
        -------
        pd.Series
            因子暴露
        """
        if self._exposures is not None:
            return self._exposures

        y = self.portfolio_returns.values
        X = self.factor_returns.values

        # 添加截距
        X_with_intercept = np.column_stack([np.ones(len(X)), X])

        try:
            beta = np.linalg.lstsq(X_with_intercept, y, rcond=None)[0]
            self._exposures = pd.Series(
                beta[1:],
                index=self.factor_returns.columns,
                name="exposure"
            )
            self._residual = y - X_with_intercept @ beta
        except Exception:
            self._exposures = pd.Series(0, index=self.factor_returns.columns)
            self._residual = y

        return self._exposures

    def attribution(self) -> pd.DataFrame:
        """
        计算归因分析结果。

        Returns
        -------
        pd.DataFrame
            归因结果，包含因子贡献和残差
        """
        exposures = self.factor_exposure()

        # 计算各因子贡献
        contributions = {}
        for factor in self.factor_returns.columns:
            factor_ret = self.factor_returns[factor].mean()
            contributions[factor] = {
                "exposure": exposures.get(factor, 0),
                "factor_return": factor_ret,
                "contribution": exposures.get(factor, 0) * factor_ret,
            }

        # 计算残差贡献
        if self._residual is not None:
            residual_contribution = np.mean(self._residual)
        else:
            residual_contribution = 0

        contributions["residual"] = {
            "exposure": 1.0,
            "factor_return": residual_contribution,
            "contribution": residual_contribution,
        }

        return pd.DataFrame(contributions).T

    def rolling_attribution(
        self,
        window: int = 20,
    ) -> pd.DataFrame:
        """
        滚动归因分析。

        Parameters
        ----------
        window : int, default 20
            滚动窗口大小

        Returns
        -------
        pd.DataFrame
            滚动归因结果
        """
        results = []
        dates = []

        for i in range(window, len(self.portfolio_returns)):
            end_date = self.portfolio_returns.index[i]
            start_date = self.portfolio_returns.index[i - window]

            portfolio_window = self.portfolio_returns.loc[start_date:end_date]
            factors_window = self.factor_returns.loc[start_date:end_date]

            aa = AttributionAnalysis(portfolio_window, factors_window)
            attr = aa.attribution()

            results.append(attr["contribution"])
            dates.append(end_date)

        return pd.DataFrame(results, index=dates)

    def summary(self) -> Dict[str, float]:
        """
        生成归因分析摘要。

        Returns
        -------
        Dict[str, float]
            摘要统计
        """
        attr = self.attribution()
        exposures = self.factor_exposure()

        total_contribution = attr["contribution"].sum()
        factor_contribution = attr.loc[attr.index != "residual", "contribution"].sum()
        residual_contribution = attr.loc["residual", "contribution"]

        return {
            "total_return": self.portfolio_returns.mean(),
            "factor_contribution": factor_contribution,
            "residual_contribution": residual_contribution,
            "factor_contribution_pct": factor_contribution / total_contribution if total_contribution != 0 else 0,
            "r_squared": 1 - (residual_contribution ** 2) / (self.portfolio_returns.var() + 1e-10),
        }


__all__ = [
    "FactorAnalyzer",
    "analyze_factor",
    "AttributionAnalysis",
]