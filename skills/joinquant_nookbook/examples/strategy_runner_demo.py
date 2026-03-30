#!/usr/bin/env python3
"""
策略运行器演示 - 展示如何复用 joinquant_strategy 的代码

这个文件展示了三种方式：
1. 直接复用策略代码（不需要修改）
2. 使用适配器运行回测
3. 手动模拟回测流程
"""

from jqdata import *
import pandas as pd
from datetime import datetime

print("=" * 70)
print("JoinQuant Notebook 策略运行器演示")
print("=" * 70)

# ============================================================================
# 方式 1: 直接复用策略代码（快速验证选股逻辑）
# ============================================================================
print("\n【方式 1】直接复用策略代码 - 快速验证")
print("-" * 50)

# 直接从 joinquant_strategy 复用代码片段
test_date = "2024-03-20"
print(f"测试日期: {test_date}")

# 复用选股逻辑（来自 weak_to_strong_simple.py）
all_stocks = get_all_securities("stock", test_date).index
all_stocks = [s for s in all_stocks if s[0] not in ["3", "4", "8"] and s[:2] != "68"]

# 检查涨停股
limit_up_stocks = []
for stock in all_stocks[:200]:
    try:
        df = get_price(
            stock,
            end_date=test_date,
            count=2,
            fields=["close", "high_limit"],
            panel=False,
            skip_paused=True,
        )
        if df.empty or len(df) < 2:
            continue

        if df["close"].iloc[-1] == df["high_limit"].iloc[-1]:
            limit_up_stocks.append(stock)
    except:
        continue

print(f"涨停股数量: {len(limit_up_stocks)}")
print(f"涨停股列表: {limit_up_stocks[:10]}")

# ============================================================================
# 方式 2: 执行完整策略文件（参数调优）
# ============================================================================
print("\n【方式 2】参数调优 - 不需要回测框架")
print("-" * 50)

# 测试不同的参数组合
test_params = [
    {"name": "宽松版", "market_cap_min": 20, "money_min": 3e8},
    {"name": "标准版", "market_cap_min": 50, "money_min": 5e8},
    {"name": "严格版", "market_cap_min": 100, "money_min": 10e8},
]

results = []
for params in test_params:
    qualified = []
    for stock in limit_up_stocks:
        try:
            # 市值筛选
            valuation = get_valuation(
                stock, end_date=test_date, count=1, fields=["market_cap"]
            )
            if (
                valuation.empty
                or valuation["market_cap"].iloc[-1] < params["market_cap_min"]
            ):
                continue

            # 成交额筛选
            price_data = get_price(
                stock, end_date=test_date, count=1, fields=["money"], panel=False
            )
            if price_data.empty or price_data["money"].iloc[-1] < params["money_min"]:
                continue

            qualified.append(stock)
        except:
            continue

    results.append(
        {"name": params["name"], "count": len(qualified), "stocks": qualified[:5]}
    )

print("\n参数调优结果:")
for r in results:
    print(f"  {r['name']}: {r['count']} 只股票")
    print(f"    示例: {r['stocks']}")

# ============================================================================
# 方式 3: 手动模拟回测（如果策略需要）
# ============================================================================
print("\n【方式 3】手动模拟回测 - 单日测试")
print("-" * 50)


# 如果你的策略需要 initialize/handle_data，可以这样模拟
class MockContext:
    def __init__(self, current_dt):
        self.current_dt = current_dt
        self.portfolio = MockPortfolio()


class MockPortfolio:
    def __init__(self):
        self.available_cash = 1000000
        self.positions = {}


# 创建模拟 context
context = MockContext(datetime.strptime(test_date, "%Y-%m-%d"))

# 模拟策略执行（直接调用选股函数）
# 如果策略有 select_stocks 函数，可以这样调用：
# select_stocks(context)

print(f"模拟 context 创建完成")
print(f"  日期: {context.current_dt}")
print(f"  资金: {context.portfolio.available_cash}")

# ============================================================================
# 总结
# ============================================================================
print("\n" + "=" * 70)
print("使用总结")
print("=" * 70)
print("""
1. 直接复用策略代码：适合快速验证选股逻辑，无需修改代码
   使用: node run-strategy.js --strategy weak_to_strong_simple.py

2. 参数调优：适合测试不同参数组合的效果
   使用: node run-strategy.js --strategy examples/grid_search.py

3. 手动模拟回测：适合需要 initialize/handle_data 的策略
   使用: 导入 strategy_adapter.py 并创建 NotebookBacktest

优势：
- 无每日 180 分钟限制
- 可以逐步调试
- 可以查看中间结果
- 与策略编辑器使用相同的 API
""")
