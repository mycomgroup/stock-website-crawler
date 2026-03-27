# -*- coding: utf-8 -*-
"""
回测引擎模块
"""

import pandas as pd
import numpy as np
from datetime import datetime


class BacktestEngine:
    """回测引擎"""

    def __init__(self, config=None):
        """
        初始化回测引擎

        Args:
            config: 配置字典
        """
        from config import BACKTEST_CONFIG, STRATEGY_CONFIG

        self.backtest_config = config or BACKTEST_CONFIG
        self.strategy_config = STRATEGY_CONFIG

    def run_backtest(self, prices, signals, initial_capital=None, verbose=True):
        """
        运行回测

        Args:
            prices: 价格数据
            signals: 持仓信号
            initial_capital: 初始资金
            verbose: 是否打印详细信息

        Returns:
            dict: 回测结果
        """
        initial_capital = initial_capital or self.backtest_config["initial_capital"]
        commission_rate = self.strategy_config["commission_rate"]
        slippage_rate = self.strategy_config["slippage_rate"]
        hold_period = self.strategy_config["hold_period"]

        if verbose:
            print("=" * 50)
            print("开始回测")
            print("=" * 50)

        # 初始化
        capital = initial_capital
        position = 0
        holdings = {}
        daily_records = []

        # 按日回测
        dates = signals.index
        for i, date in enumerate(dates):
            daily_signals = signals.loc[date]
            held_etfs = daily_signals[daily_signals].index.tolist()

            # 计算当日收益
            if holdings:
                daily_return = 0
                for etf, shares in holdings.items():
                    if etf in prices.columns and date in prices.index:
                        if i > 0:
                            prev_date = dates[i - 1]
                            if prev_date in prices.index:
                                price_change = (
                                    prices.loc[date, etf] / prices.loc[prev_date, etf]
                                    - 1
                                )
                                daily_return += (
                                    price_change
                                    * (shares * prices.loc[date, etf])
                                    / capital
                                )

                capital *= 1 + daily_return

            # 调仓逻辑（每hold_period天调仓一次）
            if i % hold_period == 0 and held_etfs:
                # 卖出所有持仓
                for etf in list(holdings.keys()):
                    if etf in prices.columns and date in prices.index:
                        sell_value = holdings[etf] * prices.loc[date, etf]
                        sell_cost = sell_value * (commission_rate + slippage_rate)
                        capital += sell_value - sell_cost

                holdings = {}

                # 买入新持仓
                if held_etfs:
                    per_etf_capital = capital / len(held_etfs)
                    for etf in held_etfs:
                        if etf in prices.columns and date in prices.index:
                            buy_cost = per_etf_capital * (
                                commission_rate + slippage_rate
                            )
                            actual_capital = per_etf_capital - buy_cost
                            shares = actual_capital / prices.loc[date, etf]
                            holdings[etf] = shares

                    capital = 0  # 资金已全部投入

            # 记录每日数据
            position_value = 0
            for etf, shares in holdings.items():
                if etf in prices.columns and date in prices.index:
                    position_value += shares * prices.loc[date, etf]

            daily_records.append(
                {
                    "date": date,
                    "capital": capital,
                    "position_value": position_value,
                    "total_value": capital + position_value,
                    "holdings_count": len(holdings),
                    "holdings": list(holdings.keys()),
                }
            )

        # 转换为DataFrame
        results = pd.DataFrame(daily_records).set_index("date")

        # 计算绩效指标
        performance = self._calculate_performance(results, prices)

        if verbose:
            print("=" * 50)
            print("回测完成")
            print(f"总收益率: {performance['total_return']:.2%}")
            print(f"年化收益率: {performance['annual_return']:.2%}")
            print(f"最大回撤: {performance['max_drawdown']:.2%}")
            print(f"夏普比率: {performance['sharpe_ratio']:.4f}")
            print("=" * 50)

        return {"daily_records": results, "performance": performance}

    def _calculate_performance(self, results, prices):
        """
        计算绩效指标

        Args:
            results: 回测结果
            prices: 价格数据

        Returns:
            dict: 绩效指标
        """
        total_values = results["total_value"]

        # 总收益率
        total_return = total_values.iloc[-1] / total_values.iloc[0] - 1

        # 年化收益率
        days = len(total_values)
        annual_return = (1 + total_return) ** (252 / days) - 1

        # 日收益率
        daily_returns = total_values.pct_change().dropna()

        # 年化波动率
        annual_volatility = daily_returns.std() * np.sqrt(252)

        # 夏普比率
        risk_free_rate = 0.03  # 假设无风险利率3%
        sharpe_ratio = (
            (annual_return - risk_free_rate) / annual_volatility
            if annual_volatility > 0
            else 0
        )

        # 最大回撤
        cummax = total_values.cummax()
        drawdown = (total_values - cummax) / cummax
        max_drawdown = drawdown.min()

        # 胜率
        win_rate = (daily_returns > 0).mean()

        # 盈亏比
        avg_win = (
            daily_returns[daily_returns > 0].mean() if (daily_returns > 0).any() else 0
        )
        avg_loss = (
            abs(daily_returns[daily_returns < 0].mean())
            if (daily_returns < 0).any()
            else 0
        )
        profit_loss_ratio = avg_win / avg_loss if avg_loss > 0 else 0

        return {
            "total_return": total_return,
            "annual_return": annual_return,
            "annual_volatility": annual_volatility,
            "sharpe_ratio": sharpe_ratio,
            "max_drawdown": max_drawdown,
            "win_rate": win_rate,
            "profit_loss_ratio": profit_loss_ratio,
            "trading_days": days,
        }

    def plot_results(self, results, benchmark_prices=None, save_path=None):
        """
        绘制回测结果

        Args:
            results: 回测结果
            benchmark_prices: 基准价格数据
            save_path: 保存路径
        """
        import matplotlib.pyplot as plt

        daily_records = results["daily_records"]
        performance = results["performance"]

        fig, axes = plt.subplots(3, 1, figsize=(12, 10))

        # 1. 净值曲线
        ax1 = axes[0]
        total_values = daily_records["total_value"]
        normalized_values = total_values / total_values.iloc[0]
        ax1.plot(
            normalized_values.index,
            normalized_values.values,
            label="策略净值",
            linewidth=2,
        )

        if benchmark_prices is not None:
            benchmark = benchmark_prices / benchmark_prices.iloc[0]
            ax1.plot(
                benchmark.index,
                benchmark.values,
                label="基准净值",
                linewidth=1,
                alpha=0.7,
            )

        ax1.set_title("净值曲线", fontsize=14)
        ax1.legend()
        ax1.grid(True, alpha=0.3)

        # 2. 回撤曲线
        ax2 = axes[1]
        cummax = total_values.cummax()
        drawdown = (total_values - cummax) / cummax
        ax2.fill_between(drawdown.index, drawdown.values, 0, alpha=0.3, color="red")
        ax2.set_title("回撤曲线", fontsize=14)
        ax2.grid(True, alpha=0.3)

        # 3. 持仓数量
        ax3 = axes[2]
        ax3.bar(daily_records.index, daily_records["holdings_count"], alpha=0.7)
        ax3.set_title("持仓数量", fontsize=14)
        ax3.grid(True, alpha=0.3)

        plt.tight_layout()

        if save_path:
            plt.savefig(save_path, dpi=150, bbox_inches="tight")
            print(f"图表已保存到 {save_path}")

        plt.show()

    def generate_report(self, results, save_path=None):
        """
        生成回测报告

        Args:
            results: 回测结果
            save_path: 保存路径

        Returns:
            str: 回测报告文本
        """
        performance = results["performance"]

        report = f"""
ETF轮动策略回测报告
{"=" * 50}

一、绩效概览
-----------
总收益率: {performance["total_return"]:.2%}
年化收益率: {performance["annual_return"]:.2%}
年化波动率: {performance["annual_volatility"]:.2%}
夏普比率: {performance["sharpe_ratio"]:.4f}
最大回撤: {performance["max_drawdown"]:.2%}
胜率: {performance["win_rate"]:.2%}
盈亏比: {performance["profit_loss_ratio"]:.4f}
交易天数: {performance["trading_days"]}

二、策略参数
-----------
候选池数量: {self.strategy_config["hold_count"]}
持仓周期: {self.strategy_config["hold_period"]}天
单边佣金率: {self.strategy_config["commission_rate"]:.4%}
单边滑点率: {self.strategy_config["slippage_rate"]:.4%}

{"=" * 50}
"""

        if save_path:
            with open(save_path, "w", encoding="utf-8") as f:
                f.write(report)
            print(f"报告已保存到 {save_path}")

        return report
