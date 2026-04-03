# 快速开始指南

## 1. 安装依赖

```bash
pip install backtrader akshare pandas numpy duckdb
```

## 2. 验证环境

```bash
cd jqdata_akshare_backtrader_utility
python3 -c "from src.core.strategy_base import *; print('OK')"
```

## 3. 运行策略

```python
from jq_strategy_runner import run_jq_strategy

run_jq_strategy(
    strategy_file='../jkcode/jkcode/策略.txt',
    start_date='2020-01-01',
    end_date='2023-12-31',
    stock_pool=['600519.XSHG', '000858.XSHE'],
)
```

---

## 核心功能

### Context对象

```python
positions = context.portfolio.positions       # 持仓
total_value = context.portfolio.total_value   # 总资产
cash = context.portfolio.available_cash       # 可用现金
```

### 全局变量

```python
g.stocks = []         # 设置
stocks = g.stocks     # 获取
```

### 下单

```python
order_target('600519.XSHG', 100)    # 调整到100股
order_value('600519.XSHG', 50000)   # 按市值买入5万
```

### 定时器

```python
run_monthly(func, 1, 'open')   # 每月首日开盘
run_daily(func, 'open')        # 每日开盘
```

### 数据获取

```python
current = get_current_data()
price = current['600519.XSHG'].last_price

weights = get_index_weights('000300.XSHG')
stocks = get_index_stocks('000300.XSHG')
```

---

## 策略模板

```python
from src.core.strategy_base import JQ2BTBaseStrategy

class MyStrategy(JQ2BTBaseStrategy):
    def __init__(self):
        super().__init__()
        self.g.stocks = []
        self.run_monthly(self.rebalance, 1, 'open')
    
    def rebalance(self, context):
        for stock in context.portfolio.positions:
            if stock not in self.g.stocks:
                self.order_target(stock, 0)
        
        position = context.portfolio.total_value / len(self.g.stocks)
        for stock in self.g.stocks:
            self.order_value(stock, position)
```

---

## 常见问题

**Q: 提示找不到数据？**
检查股票代码格式和日期范围。

**Q: 策略执行出错？**
查看错误信息，确认API是否支持。

**Q: 如何调试？**
添加 `log.info()` 输出调试信息。