# -*- coding: utf-8 -*-
"""
ETF轮动策略主程序
统一研究骨架的入口
"""

import sys
import os
from datetime import datetime

# 添加模块路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from modules import (
    ETFPoolBuilder,
    FactorCalculator,
    TimingFilter,
    BacktestEngine,
    RotationStrategy,
)


def main():
    """主函数"""
    print("=" * 60)
    print("ETF轮动策略统一研究框架")
    print("=" * 60)
    print(f"运行时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()

    # 注意：此框架需要在聚宽环境中运行
    # 如果在本地运行，需要提供数据接口函数

    print("请在聚宽环境中运行此框架，或提供以下数据接口函数：")
    print("1. get_all_securities - 获取所有证券列表")
    print("2. get_price - 获取价格数据")
    print()
    print("框架结构：")
    print("- config.py - 配置文件")
    print("- modules/pool_builder.py - 候选池构建模块")
    print("- modules/factor_calculator.py - 因子计算模块")
    print("- modules/timing_filter.py - 择时过滤模块")
    print("- modules/strategy.py - 策略模块")
    print("- modules/backtest_engine.py - 回测引擎模块")
    print()
    print("使用示例：")
    print("""
from modules import ETFPoolBuilder, FactorCalculator, TimingFilter, BacktestEngine, RotationStrategy
from jqdata import *

# 1. 构建候选池
pool_builder = ETFPoolBuilder()
pool = pool_builder.build_pool(get_all_securities, get_price)

# 2. 计算因子
factor_calculator = FactorCalculator()
momentum = factor_calculator.calculate_momentum(prices)

# 3. 择时过滤
timing_filter = TimingFilter()
timing_signal = timing_filter.generate_timing_signal(breadth=breadth)

# 4. 运行策略
strategy = RotationStrategy(pool_builder, factor_calculator, timing_filter)
results = strategy.run(prices, all_stock_prices=all_stock_prices)

# 5. 回测
backtest_engine = BacktestEngine()
backtest_results = backtest_engine.run_backtest(prices, strategy.signals)
backtest_engine.plot_results(backtest_results)
""")


if __name__ == "__main__":
    main()
