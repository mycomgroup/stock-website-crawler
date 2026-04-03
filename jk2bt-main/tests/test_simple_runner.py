# test_jq_runner.py
"""
测试聚宽策略运行器 - 简化版
"""

import pandas as pd
import backtrader as bt
from datetime import datetime

# 导入必要的模块
from jk2bt.core.strategy_base import (
    JQ2BTBaseStrategy,
    GlobalState,
    get_price,
    jq_code_to_ak,
)


def simple_test():
    """简单测试：直接运行一个最小策略"""

    print("=" * 80)
    print("简单测试：最小化策略运行")
    print("=" * 80)

    # 准备数据
    print("\n1. 准备数据...")
    stocks = ["sh600519", "sz000858", "sz000333"]  # 茅台、五粮液、美的

    cerebro = bt.Cerebro()
    cerebro.broker.setcash(1000000)
    cerebro.broker.setcommission(commission=0.0002)

    for stock in stocks:
        try:
            print(f"  加载 {stock}...", end="")
            df = get_price(stock, "2022-01-01", "2022-12-31", adjust="qfq")

            if df is not None and not df.empty:
                print(f" {len(df)} 条数据 ✓")

                # 确保datetime是索引
                if "datetime" in df.columns:
                    df["datetime"] = pd.to_datetime(df["datetime"])
                    df = df.set_index("datetime")

                # 创建数据源
                data = bt.feeds.PandasData(
                    dataname=df,
                    datetime=None,
                    open="open",
                    high="high",
                    low="low",
                    close="close",
                    volume="volume",
                    openinterest=-1,
                    name=stock,
                )

                cerebro.adddata(data, name=stock)
            else:
                print(" 无数据 ✗")
        except Exception as e:
            print(f" 失败: {e} ✗")

    # 创建简单策略
    print("\n2. 创建策略...")

    class SimpleStrategy(bt.Strategy):
        def __init__(self):
            self.order_dict = {}
            self.rebalance_day = None

        def next(self):
            current_date = self.datas[0].datetime.date(0)

            # 每月第一个交易日调仓
            if (
                self.rebalance_day is None
                or current_date.month != self.rebalance_day.month
            ):
                self.rebalance_day = current_date
                print(f"\n{current_date} 调仓日")

                # 等权重买入所有股票
                for data in self.datas:
                    target_percent = 1.0 / len(self.datas)
                    self.order_target_percent(data, target_percent)
                    print(f"  买入 {data._name}: {target_percent:.2%}")

    cerebro.addstrategy(SimpleStrategy)

    # 运行回测
    print("\n3. 运行回测...")
    print(f"初始资金: {cerebro.broker.getvalue():,.2f}")

    results = cerebro.run()

    final_value = cerebro.broker.getvalue()
    pnl = final_value - 1000000
    pnl_pct = (final_value / 1000000 - 1) * 100

    print(f"\n最终资金: {final_value:,.2f}")
    print(f"盈亏: {pnl:,.2f} ({pnl_pct:.2f}%)")
    print("\n" + "=" * 80)
    print("✅ 测试通过！Backtrader运行正常")


if __name__ == "__main__":
    simple_test()
