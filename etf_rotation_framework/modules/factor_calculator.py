# -*- coding: utf-8 -*-
"""
因子计算模块
基于notebook 43的动量因子逻辑
"""

import pandas as pd
import numpy as np
from scipy import stats


class FactorCalculator:
    """因子计算器"""

    def __init__(self, config=None):
        """
        初始化因子计算器

        Args:
            config: 配置字典，如果为None则使用默认配置
        """
        from config import FACTOR_CONFIG

        self.config = config or FACTOR_CONFIG

    def calculate_momentum(self, prices, window=None, method=None):
        """
        计算动量因子

        Args:
            prices: 价格数据DataFrame，index为日期，columns为ETF代码
            window: 动量计算窗口，如果为None则使用配置中的值
            method: 计算方法: 'slope' 或 'return'

        Returns:
            pd.DataFrame: 动量因子值
        """
        window = window or self.config["momentum_windows"][0]
        method = method or self.config["momentum_method"]

        if method == "slope":
            return self._calculate_slope_momentum(prices, window)
        elif method == "return":
            return self._calculate_return_momentum(prices, window)
        else:
            raise ValueError(f"不支持的动量计算方法: {method}")

    def _calculate_slope_momentum(self, prices, window):
        """
        计算斜率动量因子
        使用线性回归斜率作为动量指标

        Args:
            prices: 价格数据
            window: 计算窗口

        Returns:
            pd.DataFrame: 斜率动量因子
        """

        def slope(x):
            if len(x) < window:
                return np.nan
            # 归一化到起始价格
            x_normalized = x / x[0]
            # 线性回归
            slope_value, _, _, _, _ = stats.linregress(
                np.arange(len(x_normalized)), x_normalized
            )
            return slope_value * 100  # 放大100倍便于观察

        return prices.rolling(window).apply(slope, raw=True)

    def _calculate_return_momentum(self, prices, window):
        """
        计算收益率动量因子
        使用N日累计收益率作为动量指标

        Args:
            prices: 价格数据
            window: 计算窗口

        Returns:
            pd.DataFrame: 收益率动量因子
        """
        return prices.pct_change(window)

    def calculate_all_momentum_factors(self, prices, windows=None):
        """
        计算多个窗口的动量因子

        Args:
            prices: 价格数据
            windows: 动量计算窗口列表

        Returns:
            dict: 各窗口动量因子的字典
        """
        windows = windows or self.config["momentum_windows"]
        factors = {}

        for window in windows:
            factor_name = f"momentum_{window}d"
            factors[factor_name] = self.calculate_momentum(prices, window)

        return factors

    def calculate_forward_returns(self, prices, periods=None):
        """
        计算未来N日收益率（用于IC分析）

        Args:
            prices: 价格数据
            periods: 未来收益率周期列表

        Returns:
            dict: 各周期未来收益率的字典
        """
        periods = periods or self.config["ic_forward_periods"]
        returns = {}

        for period in periods:
            ret_name = f"return_{period}d"
            returns[ret_name] = prices.shift(-period) / prices - 1

        return returns

    def calculate_ic(self, factor, forward_return):
        """
        计算因子IC值（信息系数）

        Args:
            factor: 因子值DataFrame
            forward_return: 未来收益率DataFrame

        Returns:
            pd.Series: 每日IC值
        """
        # 对齐数据
        aligned_data = pd.concat(
            [factor, forward_return], axis=1, keys=["factor", "return"]
        )
        aligned_data = aligned_data.dropna()

        if len(aligned_data) == 0:
            return pd.Series(dtype=float)

        # 计算每日横截面IC
        ic_series = aligned_data.groupby(level=0).apply(
            lambda x: x["factor"].corr(x["return"]) if len(x) > 2 else np.nan
        )

        return ic_series

    def calculate_ic_analysis(self, prices, factor_window=20, forward_periods=None):
        """
        完整的IC分析

        Args:
            prices: 价格数据
            factor_window: 因子计算窗口
            forward_periods: 未来收益率周期

        Returns:
            dict: IC分析结果
        """
        forward_periods = forward_periods or self.config["ic_forward_periods"]

        # 计算因子
        factor = self.calculate_momentum(prices, factor_window)

        # 计算各周期未来收益率
        forward_returns = self.calculate_forward_returns(prices, forward_periods)

        # 计算各周期IC
        ic_results = {}
        for period in forward_periods:
            ret_name = f"return_{period}d"
            ic = self.calculate_ic(factor, forward_returns[ret_name])
            ic_results[f"IC_{period}d"] = {
                "mean": ic.mean(),
                "std": ic.std(),
                "icir": ic.mean() / ic.std() if ic.std() > 0 else 0,
                "positive_ratio": (ic > 0).mean(),
                "series": ic,
            }

        return ic_results

    def calculate_factor_half_life(self, factor, max_lag=20):
        """
        计算因子半衰期

        Args:
            factor: 因子值DataFrame（单列）
            max_lag: 最大滞后阶数

        Returns:
            float: 半衰期（天）
        """
        from statsmodels.tsa.stattools import acf

        factor_clean = factor.dropna()
        if len(factor_clean) < max_lag * 2:
            return np.nan

        # 计算自相关函数
        autocorr = acf(factor_clean, nlags=max_lag)

        # 找到自相关系数首次低于0.5的滞后阶数
        for lag in range(1, len(autocorr)):
            if autocorr[lag] < 0.5:
                return lag

        return max_lag
