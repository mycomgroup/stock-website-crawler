# -*- coding: utf-8 -*-
"""
ETF轮动策略模块
整合候选池、因子、择时，形成完整策略
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta


class RotationStrategy:
    """ETF轮动策略"""

    def __init__(self, pool_builder, factor_calculator, timing_filter, config=None):
        """
        初始化策略

        Args:
            pool_builder: 候选池构建器
            factor_calculator: 因子计算器
            timing_filter: 择时过滤器
            config: 配置字典
        """
        from config import STRATEGY_CONFIG

        self.config = config or STRATEGY_CONFIG
        self.pool_builder = pool_builder
        self.factor_calculator = factor_calculator
        self.timing_filter = timing_filter

        self.pool_codes = None
        self.signals = None
        self.positions = None

    def run(
        self,
        prices,
        high_prices=None,
        low_prices=None,
        all_stock_prices=None,
        verbose=True,
    ):
        """
        运行策略

        Args:
            prices: ETF收盘价数据
            high_prices: ETF最高价数据（用于RSRS）
            low_prices: ETF最低价数据（用于RSRS）
            all_stock_prices: 全市场股票价格（用于市场宽度）
            verbose: 是否打印详细信息

        Returns:
            dict: 策略运行结果
        """
        if verbose:
            print("=" * 50)
            print("开始运行ETF轮动策略")
            print("=" * 50)

        # 1. 获取候选池代码
        self.pool_codes = self.pool_builder.get_pool_codes()
        pool_prices = prices[self.pool_codes]

        if verbose:
            print(f"候选池: {len(self.pool_codes)} 只ETF")

        # 2. 计算动量因子
        momentum = self.factor_calculator.calculate_momentum(
            pool_prices, window=self.config["hold_period"]
        )

        if verbose:
            print("动量因子计算完成")

        # 3. 计算择时信号（如果提供相关数据）
        timing_signal = None
        if all_stock_prices is not None:
            breadth = self.timing_filter.calculate_market_breadth(all_stock_prices)
            timing_signal = self.timing_filter.generate_timing_signal(
                breadth=breadth, mode="breadth"
            )
            if verbose:
                print("市场宽度择时信号计算完成")

        # 4. 生成每日持仓信号
        self.signals = self._generate_daily_signals(momentum, timing_signal)

        if verbose:
            print("每日持仓信号生成完成")
            print("=" * 50)
            print("策略运行完成")
            print("=" * 50)

        return {
            "pool_codes": self.pool_codes,
            "momentum": momentum,
            "timing_signal": timing_signal,
            "signals": self.signals,
        }

    def _generate_daily_signals(self, momentum, timing_signal=None):
        """
        生成每日持仓信号

        Args:
            momentum: 动量因子
            timing_signal: 择时信号

        Returns:
            pd.DataFrame: 每日持仓信号
        """
        hold_count = self.config["hold_count"]

        signals = pd.DataFrame(
            index=momentum.index, columns=momentum.columns, data=False
        )

        for date in momentum.index:
            daily_momentum = momentum.loc[date].dropna()
            daily_momentum = daily_momentum[
                daily_momentum.notna() & ~np.isinf(daily_momentum)
            ]

            if len(daily_momentum) < hold_count:
                continue

            top_n = daily_momentum.nlargest(hold_count).index
            signals.loc[date, top_n] = True

            # 应用择时过滤
            if timing_signal is not None and date in timing_signal.index:
                if not timing_signal.loc[date]:
                    signals.loc[date, :] = False

        return signals

    def get_daily_positions(self):
        """
        获取每日持仓

        Returns:
            pd.DataFrame: 每日持仓ETF代码
        """
        if self.signals is None:
            raise ValueError("请先运行策略")

        positions = []
        for date in self.signals.index:
            daily_positions = self.signals.loc[date]
            held_etfs = daily_positions[daily_positions].index.tolist()
            positions.append(
                {"date": date, "holdings": held_etfs, "count": len(held_etfs)}
            )

        return pd.DataFrame(positions)

    def calculate_turnover(self):
        """
        计算换手率

        Returns:
            pd.Series: 每日换手率
        """
        if self.signals is None:
            raise ValueError("请先运行策略")

        turnover = []
        prev_holdings = set()

        for date in self.signals.index:
            daily_holdings = set(self.signals.loc[date][self.signals.loc[date]].index)

            if prev_holdings:
                # 计算换手率 = 新增 + 减少的ETF数量 / 总持仓数
                added = len(daily_holdings - prev_holdings)
                removed = len(prev_holdings - daily_holdings)
                total = len(prev_holdings) + len(daily_holdings)

                if total > 0:
                    rate = (added + removed) / total
                else:
                    rate = 0
            else:
                rate = 1.0 if daily_holdings else 0.0

            turnover.append({"date": date, "turnover_rate": rate})
            prev_holdings = daily_holdings

        return pd.DataFrame(turnover).set_index("date")["turnover_rate"]

    def save_signals(self, filepath):
        """保存信号到文件"""
        if self.signals is None:
            raise ValueError("请先运行策略")
        self.signals.to_csv(filepath)
        print(f"信号已保存到 {filepath}")

    def load_signals(self, filepath):
        """从文件加载信号"""
        self.signals = pd.read_csv(filepath, index_col=0, parse_dates=True)
        print(f"已从 {filepath} 加载信号")
