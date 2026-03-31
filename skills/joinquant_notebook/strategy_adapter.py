#!/usr/bin/env python3
"""
策略适配器：将 JoinQuant 策略编辑器代码转换为 Notebook 可执行的格式

策略编辑器使用 initialize(context) 和 handle_data(context, data) 框架，
Notebook 中没有这个框架，需要手动模拟回测流程。

这个适配器提供：
1. 模拟的 context 对象
2. 手动的回测循环
3. 便捷的调试工具
"""

from jqdata import *
from datetime import datetime, timedelta
import pandas as pd


class MockContext:
    """模拟策略编辑器的 context 对象"""

    def __init__(self, current_dt, portfolio_cash=1000000):
        self.current_dt = current_dt
        self.portfolio = MockPortfolio(portfolio_cash)
        self.run_params = {
            "start_date": None,
            "end_date": None,
            "frequency": "daily",
            "benchmark": "000300.XSHG",
        }


class MockPortfolio:
    """模拟 portfolio 对象"""

    def __init__(self, cash=1000000):
        self.available_cash = cash
        self.positions = MockPositions()
        self.total_value = cash

    def update_cash(self, amount):
        self.available_cash += amount
        self.total_value = self.available_cash + self.positions.total_value()


class MockPositions:
    """模拟 positions 对象"""

    def __init__(self):
        self._positions = {}

    def __iter__(self):
        return iter(self._positions.keys())

    def __getitem__(self, stock):
        return self._positions.get(stock, MockPosition(stock, 0, 0))

    def add(self, stock, amount, price):
        if stock in self._positions:
            pos = self._positions[stock]
            pos.total_amount += amount
            pos.closeable_amount += amount
        else:
            self._positions[stock] = MockPosition(stock, amount, price)

    def remove(self, stock, amount):
        if stock in self._positions:
            pos = self._positions[stock]
            pos.total_amount -= amount
            pos.closeable_amount -= amount
            if pos.total_amount <= 0:
                del self._positions[stock]

    def total_value(self):
        return sum(pos.total_value for pos in self._positions.values())


class MockPosition:
    """模拟单个持仓"""

    def __init__(self, stock, amount, price):
        self.security = stock
        self.total_amount = amount
        self.closeable_amount = amount
        self.price = price
        self.total_value = amount * price


class NotebookBacktest:
    """Notebook 回测框架"""

    def __init__(self, strategy_module, start_date, end_date, initial_cash=1000000):
        """
        初始化回测

        Args:
            strategy_module: 包含 initialize 和 handle_data 的模块
            start_date: 回测开始日期
            end_date: 回测结束日期
            initial_cash: 初始资金
        """
        self.strategy = strategy_module
        self.start_date = start_date
        self.end_date = end_date
        self.initial_cash = initial_cash
        self.trade_days = []
        self.results = []

    def run(self):
        """执行回测"""
        # 获取交易日
        self.trade_days = get_trade_days(self.start_date, self.end_date)

        print(f"回测时间范围: {self.start_date} ~ {self.end_date}")
        print(f"交易日数量: {len(self.trade_days)}")

        # 创建初始 context
        context = MockContext(
            datetime.strptime(self.trade_days[0], "%Y-%m-%d"), self.initial_cash
        )

        # 调用 initialize
        if hasattr(self.strategy, "initialize"):
            print("执行 initialize...")
            self.strategy.initialize(context)

        # 每日循环
        for i, day in enumerate(self.trade_days):
            context.current_dt = datetime.strptime(day, "%Y-%m-%d")

            # 调用 handle_data 或其他每日函数
            if hasattr(self.strategy, "handle_data"):
                self.strategy.handle_data(context, None)

            # 记录每日状态
            self.results.append(
                {
                    "date": day,
                    "cash": context.portfolio.available_cash,
                    "positions": list(context.portfolio.positions._positions.keys()),
                    "total_value": context.portfolio.total_value,
                }
            )

            if i % 50 == 0:
                print(
                    f"进度: {i + 1}/{len(self.trade_days)}, 持仓数: {len(context.portfolio.positions._positions)}"
                )

        return self.results

    def summary(self):
        """输出回测摘要"""
        if not self.results:
            print("没有回测结果")
            return

        df = pd.DataFrame(self.results)

        # 计算收益
        start_value = df["total_value"].iloc[0]
        end_value = df["total_value"].iloc[-1]
        total_return = (end_value - start_value) / start_value * 100

        # 计算最大回撤
        peak = df["total_value"].expanding(min_periods=1).max()
        drawdown = (df["total_value"] - peak) / peak
        max_drawdown = drawdown.min() * 100

        print("\n回测摘要:")
        print(f"  总收益: {total_return:.2f}%")
        print(f"  最大回撤: {max_drawdown:.2f}%")
        print(f"  最终资金: {end_value:.0f}")
        print(f"  最终持仓: {df['positions'].iloc[-1]}")

        return df


def quick_test_single_day(strategy_module, test_date, initial_cash=1000000):
    """
    快速测试单日策略逻辑

    Args:
        strategy_module: 策略模块
        test_date: 测试日期
        initial_cash: 初始资金
    """
    context = MockContext(datetime.strptime(test_date, "%Y-%m-%d"), initial_cash)

    if hasattr(strategy_module, "initialize"):
        strategy_module.initialize(context)

    # 手动调用选股等函数（如果策略中有）
    # 例如：strategy_module.select_stocks(context)

    print(f"\n测试日期: {test_date}")
    print(f"  可用资金: {context.portfolio.available_cash}")
    print(f"  持仓: {list(context.portfolio.positions._positions.keys())}")

    return context


def example_usage():
    """使用示例"""
    print("""
# Notebook 策略适配器使用示例

## 1. 导入适配器和策略模块

```python
from strategy_adapter import NotebookBacktest, quick_test_single_day
import weak_to_strong_simple as strategy  # 你的策略文件
```

## 2. 运行完整回测

```python
bt = NotebookBacktest(strategy, '2024-01-01', '2024-12-31', 1000000)
bt.run()
bt.summary()
```

## 3. 快速测试单日

```python
context = quick_test_single_day(strategy, '2024-03-20')
# 手动调用策略中的选股函数
strategy.select_stocks(context)
print(context.portfolio.positions)
```

## 4. 不使用适配器，直接执行

如果策略中没有 initialize/handle_data，可以直接执行：

```python
# 直接运行策略逻辑
from jqdata import *
exec(open('weak_to_strong_simple.py').read())

# 手动调用函数
# 例如：select_stocks(MockContext(datetime.now()))
```
""")
