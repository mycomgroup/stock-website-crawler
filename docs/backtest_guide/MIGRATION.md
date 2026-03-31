# JoinQuant 策略迁移到 RiceQuant 指南

## 一、迁移策略列表

根据 RiceQuant API 能力评估，推荐迁移以下策略：

| 优先级 | 策略名称 | 迁移难度 | 预计时间 | 所需API |
|--------|---------|---------|---------|---------|
| 1 | 小市值策略 | 低 | 1小时 | `get_factor(["market_cap"])` |
| 2 | 股息率策略 | 低 | 1小时 | `get_fundamentals()` |
| 3 | ETF动量轮动 | 低 | 1.5小时 | `history_bars()`, `index_components()` |
| 4 | 龙头底分型 | 中 | 2小时 | `history_bars()`, `bar_dict` |
| 5 | 首板低开 | 中 | 2.5小时 | `history_bars()`, 涨停价计算 |

## 二、迁移步骤

### 步骤 1：评估策略依赖

检查策略是否使用以下 JoinQuant 特殊因子：

```python
# 检查是否使用这些因子库
from jqfactor import *
jqfactor.technical_analysis.*   # 需手动计算
jqfactor.quality.*              # 需手动计算
jqfactor.momentum.*             # 需手动计算
jqfactor.volatility.*           # 需手动计算
jqfactor.size.*                 # 可用 fundamentals 替代
```

### 步骤 2：替换基础 API

| JoinQuant API | RiceQuant API |
|---------------|--------------|
| `get_all_securities("stock", date)` | `all_instruments("CS")` |
| `get_index_stocks(code, date)` | `index_components(code)` |
| `get_price(stock, end_date, count)` | `history_bars(stock, count, "1d")` |
| `get_trade_days(start, end)` | `get_trading_dates(start, end)` |
| `valuation.code` | `fundamentals.eod_derivative_indicator.*` |

### 步骤 3：替换财务数据查询

**JoinQuant：**
```python
q = query(
    valuation.code,
    valuation.pb_ratio,
    valuation.pe_ratio,
    indicator.roa
).filter(valuation.code.in_(stocks))

df = get_fundamentals(q, date=date)
```

**RiceQuant：**
```python
from rqalpha.apis import *

q = query(
    fundamentals.eod_derivative_indicator.pb_ratio,
    fundamentals.eod_derivative_indicator.pe_ratio,
    fundamentals.financial_indicator.roa
)

df = get_fundamentals(q, entry_date=date)
```

### 步骤 4：替换定时任务

**JoinQuant：**
```python
def initialize(context):
    run_daily(select_stocks, "9:35")
    run_monthly(rebalance, 1)
```

**RiceQuant：**
```python
def init(context):
    scheduler.run_daily(select_stocks, time_rule=market_open(minute=35))
    scheduler.run_monthly(rebalance, monthday=1)
```

### 步骤 5：计算缺失的因子

```python
def calc_momentum(stock, period=20):
    bars = history_bars(stock, period, "1d", "close")
    if bars is None or len(bars) < period:
        return None
    return (bars[-1] / bars[0] - 1) * 100

def calc_volatility(stock, period=20):
    bars = history_bars(stock, period, "1d", "close")
    if bars is None or len(bars) < period:
        return None
    returns = np.diff(bars) / bars[:-1]
    return np.std(returns) * np.sqrt(252)

def calc_high_limit(stock):
    bars = history_bars(stock, 1, "1d", "close")
    if bars is None:
        return None
    return round(bars[-1] * 1.1, 2)
```

### 步骤 6：测试迁移结果

```bash
cd skills/ricequant_strategy

# 创建迁移后的策略
node run-strategy.js --strategy migrated_strategy.py --create-new

# 查看输出
cat data/ricequant-notebook-result-*.json
```

## 三、迁移示例

### 示例 1：小市值策略

**JoinQuant 原版：**
```python
def select_stocks(context):
    date = context.current_dt
    q = query(
        valuation.code,
        valuation.market_cap
    ).filter(
        valuation.market_cap < 5000000000
    ).order_by(
        valuation.market_cap.asc()
    ).limit(30)
    
    df = get_fundamentals(q, date=date)
    return df['code'].tolist()
```

**RiceQuant 迁移版：**
```python
def select_stocks(context, bar_dict):
    q = query(
        fundamentals.eod_derivative_indicator.market_cap
    ).filter(
        fundamentals.eod_derivative_indicator.market_cap < 5000000000
    ).order_by(
        fundamentals.eod_derivative_indicator.market_cap.asc()
    ).limit(30)
    
    df = get_fundamentals(q, entry_date=context.now)
    return df.index.tolist()
```

### 示例 2：首板低开策略

**关键差异：涨停价获取**

**JoinQuant：**
```python
current_data = get_current_data()
high_limit = current_data[stock].high_limit
```

**RiceQuant：**
```python
def get_high_limit(stock):
    bars = history_bars(stock, 1, "1d", ["close", "limit_up"])
    if bars is not None and len(bars) > 0:
        return bars[-1]['limit_up']
    # 手动计算
    bars = history_bars(stock, 1, "1d", "close")
    if bars is not None:
        return round(bars[-1] * 1.1, 2)
    return None
```

## 四、迁移注意事项

### 1. 数据获取差异

```python
# JoinQuant
stocks = get_all_securities("stock", date).index

# RiceQuant
all_stocks = all_instruments("CS")
stocks = [s.order_book_id for s in all_stocks]
```

### 2. 实时数据差异

```python
# JoinQuant
current_data = get_current_data()
price = current_data[stock].last_price

# RiceQuant（在 handle_bar 中）
price = bar_dict[stock].close
```

### 3. 涨停价差异

```python
# JoinQuant
high_limit = get_current_data()[stock].high_limit

# RiceQuant
bars = history_bars(stock, 1, "1d", "limit_up")
high_limit = bars[-1]['limit_up'] if bars is not None else None
```

### 4. 定时任务差异

```python
# JoinQuant
run_daily(buy, '09:35')

# RiceQuant
scheduler.run_daily(buy, time_rule=market_open(minute=35))
```

## 五、不适合迁移的策略

以下策略类型不建议迁移到 RiceQuant：

| 策略类型 | 原因 |
|---------|------|
| 依赖 jqfactor 特殊因子 | 需要大量手动计算 |
| 依赖复杂技术分析库 | 计算复杂度高 |
| 需要 Tick 级别数据 | RiceQuant 回测不支持 |
| 使用 JoinQuant 特色数据 | RiceQuant 可能无对应数据 |

## 六、迁移测试计划

```bash
# 1. 小市值策略测试
node run-strategy.js --strategy migrated/01_small_cap_strategy.py --create-new

# 2. 股息率策略测试
node run-strategy.js --strategy migrated/02_dividend_strategy.py --create-new

# 3. ETF动量轮动测试
node run-strategy.js --strategy migrated/03_etf_momentum.py --create-new

# 4. 龙头底分型测试
node run-strategy.js --strategy migrated/04_leader_fractal.py --create-new --timeout-ms 300000

# 5. 首板低开测试
node run-strategy.js --strategy migrated/05_first_board_low_open.py --create-new --timeout-ms 300000
```

## 七、总结

**迁移建议**：
1. 优先迁移逻辑简单、依赖基础数据的策略
2. 复杂因子改为手动计算
3. 先在 Notebook 中验证逻辑
4. 对比两个平台的回测结果

**迁移优先级**：
- 低难度策略优先迁移（小市值、股息率）
- 中难度策略评估收益后决定（龙头底分型、首板低开）
- 高难度策略不建议迁移（依赖特殊因子）