# -*- coding: utf-8 -*-
"""
择时过滤模块
基于notebook 52、59、60的逻辑
"""

import pandas as pd
import numpy as np
from scipy import stats


class TimingFilter:
    """择时过滤器"""

    def __init__(self, config=None):
        """
        初始化择时过滤器

        Args:
            config: 配置字典，如果为None则使用默认配置
        """
        from config import TIMING_CONFIG

        self.config = config or TIMING_CONFIG

    def calculate_market_breadth(self, all_stock_prices, window=None, threshold=None):
        """
        计算市场宽度指标

        Args:
            all_stock_prices: 全市场股票价格数据，index为日期，columns为股票代码
            window: MA计算窗口
            threshold: 宽度阈值

        Returns:
            pd.Series: 市场宽度指标（0-1之间）
        """
        window = window or self.config["breadth_window"]
        threshold = threshold or self.config["breadth_threshold"]

        # 计算每只股票的MA
        ma = all_stock_prices.rolling(window).mean()

        # 计算收盘价高于MA的股票比例
        breadth = (all_stock_prices > ma).mean(axis=1)

        return breadth

    def calculate_rsrs(self, high_prices, low_prices, window=None, method=None):
        """
        计算RSRS择时指标

        Args:
            high_prices: 最高价数据
            low_prices: 最低价数据
            window: 计算窗口
            method: 计算方法

        Returns:
            pd.DataFrame: RSRS指标值
        """
        window = window or self.config["rsrs_window"]
        method = method or self.config["rsrs_method"]

        if method == "original":
            return self._calculate_original_rsrs(high_prices, low_prices, window)
        elif method == "damped":
            return self._calculate_damped_rsrs(high_prices, low_prices, window)
        else:
            raise ValueError(f"不支持的RSRS计算方法: {method}")

    def _calculate_original_rsrs(self, high_prices, low_prices, window):
        """
        计算原始RSRS指标
        RSRS = z_score(beta) * R^2

        Args:
            high_prices: 最高价数据
            low_prices: 最低价数据
            window: 计算窗口

        Returns:
            pd.DataFrame: RSRS指标值
        """

        def rsrs_calc(high, low):
            if len(high) < window:
                return np.nan

            # 线性回归：high = beta * low + alpha
            slope, intercept, r_value, p_value, std_err = stats.linregress(low, high)

            # 计算z_score
            # 这里简化处理，实际应该用历史beta的均值和标准差
            z_score = slope

            # RSRS = z_score * R^2
            rsrs = z_score * (r_value**2)

            return rsrs

        rsrs_values = pd.DataFrame(index=high_prices.index, columns=high_prices.columns)

        for col in high_prices.columns:
            rsrs_values[col] = (
                high_prices[col]
                .rolling(window)
                .apply(
                    lambda x: rsrs_calc(x.values, low_prices[col].loc[x.index].values),
                    raw=False,
                )
            )

        return rsrs_values

    def _calculate_damped_rsrs(self, high_prices, low_prices, window):
        """
        计算钝化RSRS指标
        在震荡市中降低信号强度

        Args:
            high_prices: 最高价数据
            low_prices: 最低价数据
            window: 计算窗口

        Returns:
            pd.DataFrame: 钝化RSRS指标值
        """

        def damped_rsrs_calc(high, low):
            if len(high) < window:
                return np.nan

            # 线性回归
            slope, intercept, r_value, p_value, std_err = stats.linregress(low, high)

            # 计算收益率波动率的分位数
            returns = np.diff(high) / high[:-1]
            if len(returns) > 0:
                vol_quantile = (
                    np.percentile(np.abs(returns), 50) / np.max(np.abs(returns))
                    if np.max(np.abs(returns)) > 0
                    else 0.5
                )
            else:
                vol_quantile = 0.5

            # 钝化RSRS = z_score * R^(4 * vol_quantile)
            # 在高波动时，R的指数更大，信号被压低
            rsrs = slope * (r_value ** (4 * vol_quantile))

            return rsrs

        rsrs_values = pd.DataFrame(index=high_prices.index, columns=high_prices.columns)

        for col in high_prices.columns:
            rsrs_values[col] = (
                high_prices[col]
                .rolling(window)
                .apply(
                    lambda x: damped_rsrs_calc(
                        x.values, low_prices[col].loc[x.index].values
                    ),
                    raw=False,
                )
            )

        return rsrs_values

    def generate_timing_signal(self, breadth=None, rsrs=None, mode=None):
        """
        生成综合择时信号

        Args:
            breadth: 市场宽度指标
            rsrs: RSRS指标
            mode: 择时模式

        Returns:
            pd.Series: 择时信号（True表示可以进攻，False表示防守）
        """
        mode = mode or self.config["timing_mode"]
        threshold = self.config["breadth_threshold"]

        if mode == "none":
            # 不择时，始终返回True
            if breadth is not None:
                return pd.Series(True, index=breadth.index)
            elif rsrs is not None:
                return pd.Series(True, index=rsrs.index)
            else:
                raise ValueError("至少需要提供breadth或rsrs中的一个")

        elif mode == "breadth":
            # 仅使用市场宽度
            if breadth is None:
                raise ValueError("breadth模式需要提供市场宽度数据")
            return breadth > threshold

        elif mode == "rsrs":
            # 仅使用RSRS
            if rsrs is None:
                raise ValueError("rsrs模式需要提供RSRS数据")
            # RSRS > 0 表示趋势向上
            return rsrs.mean(axis=1) > 0

        elif mode == "combined":
            # 综合使用市场宽度和RSRS
            if breadth is None or rsrs is None:
                raise ValueError("combined模式需要同时提供breadth和rsrs数据")

            # 市场宽度 > 阈值 且 RSRS > 0
            breadth_signal = breadth > threshold
            rsrs_signal = rsrs.mean(axis=1) > 0

            return breadth_signal & rsrs_signal

        else:
            raise ValueError(f"不支持的择时模式: {mode}")

    def calculate_position_weight(self, timing_signal, mode="binary"):
        """
        根据择时信号计算仓位权重

        Args:
            timing_signal: 择时信号
            mode: 权重计算模式

        Returns:
            pd.Series: 仓位权重（0-1之间）
        """
        if mode == "binary":
            # 二值化：信号为True时满仓，False时空仓
            return timing_signal.astype(float)

        elif mode == "gradual":
            # 渐进式：根据信号强度调整仓位
            # 这里简化处理，实际可以根据RSRS值的大小来调整
            return timing_signal.astype(float) * 0.8 + 0.2  # 20%-100%仓位

        else:
            raise ValueError(f"不支持的权重计算模式: {mode}")
