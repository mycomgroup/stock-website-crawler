# JoinQuant 与 RiceQuant API 差异对比

## 一、基础数据 API

### 1. 获取股票列表

**JoinQuant：**
```python
stocks = get_all_securities("stock", date).index.tolist()
```

**RiceQuant：**
```python
all_stocks = all_instruments("CS")
stocks = [s.order_book_id for s in all_stocks]
```

### 2. 获取指数成分股

**JoinQuant：**
```python
hs300 = get_index_stocks("000300.XSHG", date="2024-03-20")
```

**RiceQuant：**
```python
hs300 = index_components("000300.XSHG")
```

### 3. 获取历史数据

**JoinQuant：**
```python
df = get_price(stock, end_date=date, count=20, fields=["close", "volume"])
```

**RiceQuant：**
```python
bars = history_bars(stock, 20, "1d", ["close", "volume"])
# 返回 numpy 数组，需要转换为 DataFrame
```

### 4. 获取交易日

**JoinQuant：**
```python
dates = get_trade_days("2024-01-01", "2024-12-31")
```

**RiceQuant：**
```python
dates = get_trading_dates("2024-01-01", "2024-12-31")
```

## 二、财务数据 API

### 1. 获取估值数据

**JoinQuant：**
```python
q = query(
    valuation.code,
    valuation.pe_ratio,
    valuation.pb_ratio,
    valuation.market_cap
).filter(valuation.code.in_(stocks))

df = get_fundamentals(q, date="2024-03-20")
```

**RiceQuant：**
```python
from rqalpha.apis import *

q = query(
    fundamentals.eod_derivative_indicator.pe_ratio,
    fundamentals.eod_derivative_indicator.pb_ratio,
    fundamentals.eod_derivative_indicator.market_cap
).filter(
    fundamentals.eod_derivative_indicator.market_cap > 100
)

df = get_fundamentals(q, entry_date="2024-03-20")
```

### 2. 获取因子数据

**JoinQuant：**
```python
df = get_factor(stocks, "pe_ratio", start_date="2024-01-01", end_date="2024-03-20")
```

**RiceQuant：**
```python
df = get_factor(
    stocks,
    factor=["pe_ratio", "pb_ratio", "market_cap"],
    start_date="2024-01-01",
    end_date="2024-03-20"
)
```

## 三、实时数据差异

### 1. 获取实时价格

**JoinQuant：**
```python
current_data = get_current_data()
price = current_data[stock].last_price
high_limit = current_data[stock].high_limit
```

**RiceQuant（在 handle_bar 中）：**
```python
price = bar_dict[stock].close
# 涨停价需要计算
bars = history_bars(stock, 1, "1d", "limit_up")
high_limit = bars[-1]['limit_up'] if bars is not None else None

# 或手动计算（简化版）
bars = history_bars(stock, 1, "1d", "close")
pre_close = bars[-1]
high_limit = round(pre_close * 1.1, 2)
```

### 2. 定时任务

**JoinQuant：**
```python
run_daily(buy, '09:35')
run_monthly(rebalance, 1)
```

**RiceQuant：**
```python
scheduler.run_daily(buy, time_rule=market_open(minute=35))
scheduler.run_monthly(rebalance, monthday=1)
# 注意：RiceQuant 的 run_monthly 不支持 time 参数
```

## 四、因子库差异

### JoinQuant 支持的因子库

```python
from jqfactor import *

# 技术分析因子
jqfactor.technical_analysis.*

# 质量因子
jqfactor.quality.*

# 价值因子
jqfactor.value.*

# 动量因子
jqfactor.momentum.*

# 波动率因子
jqfactor.volatility.*

# 规模因子
jqfactor.size.*
```

### RiceQuant 支持的因子

```python
from rqalpha.apis import *

# 估值因子（通过 get_factor）
factor_names = [
    "market_cap",        # 总市值
    "pe_ratio",          # 市盈率
    "pb_ratio",          # 市净率
    "pcf_ratio",         # 市现率
    "capitalization",    # 总股本
    "market_cap_float",  # 流通市值
]

# 财务因子（通过 fundamentals）
fundamentals.eod_derivative_indicator:
    - market_cap              # 总市值
    - pe_ratio                # 市盈率
    - pb_ratio                # 市净率
    - turnover_rate           # 换手率

fundamentals.financial_indicator:
    - roa                     # 资产收益率
    - roe                     # 净资产收益率
    - net_profit_margin       # 净利率
    - gross_profit_margin     # 毛利率
    - debt_asset_ratio        # 资产负债率

fundamentals.cash_flow:
    - net_operate_cash_flow   # 经营现金流

fundamentals.balance_sheet:
    - total_assets            # 总资产
    - total_liability         # 总负债
    - total_equity            # 所有者权益
```

### RiceQuant 不支持的因子

以下因子在 RiceQuant 中**需要手动计算**：

```python
# 动量因子
def calc_momentum(stock, period=20):
    bars = history_bars(stock, period, "1d", "close")
    if bars is None or len(bars) < period:
        return None
    return (bars[-1] / bars[0] - 1) * 100

# 波动率因子
def calc_volatility(stock, period=20):
    bars = history_bars(stock, period, "1d", "close")
    if bars is None or len(bars) < period:
        return None
    returns = np.diff(bars) / bars[:-1]
    return np.std(returns) * np.sqrt(252)

# RSI
def calc_rsi(stock, period=14):
    bars = history_bars(stock, period + 1, "1d", "close")
    if bars is None or len(bars) < period + 1:
        return None
    deltas = np.diff(bars)
    gains = np.where(deltas > 0, deltas, 0)
    losses = np.where(deltas < 0, -deltas, 0)
    avg_gain = np.mean(gains)
    avg_loss = np.mean(losses)
    if avg_loss == 0:
        return 100
    rs = avg_gain / avg_loss
    return 100 - (100 / (1 + rs))

# MACD
def calc_macd(stock, fast=12, slow=26, signal=9):
    bars = history_bars(stock, slow + signal, "1d", "close")
    if bars is None or len(bars) < slow + signal:
        return None
    ema_fast = pd.Series(bars).ewm(span=fast).mean()
    ema_slow = pd.Series(bars).ewm(span=slow).mean()
    macd = ema_fast - ema_slow
    signal_line = macd.ewm(span=signal).mean()
    return macd[-1], signal_line[-1]
```

## 五、策略框架差异

### JoinQuant 策略框架

```python
from jqdata import *

def initialize(context):
    set_option("use_real_price", True)
    g.stocks = []
    run_daily(select_stocks, "9:00")

def select_stocks(context):
    date = context.current_dt
    stocks = get_all_securities("stock", date).index.tolist()
    g.stocks = stocks[:10]

def handle_data(context, data):
    for stock in g.stocks:
        order_target_value(stock, 10000)
```

### RiceQuant 策略框架

```python
from rqalpha.apis import *

def init(context):
    context.stocks = []
    scheduler.run_daily(select_stocks, time_rule=market_open())

def select_stocks(context, bar_dict):
    all_stocks = all_instruments("CS")
    context.stocks = [s.order_book_id for s in all_stocks][:10]

def handle_bar(context, bar_dict):
    for stock in context.stocks:
        order_target_value(stock, 10000)
```

## 六、API 对比总结表

| 功能 | JoinQuant | RiceQuant | 迁移难度 |
|------|-----------|-----------|---------|
| 历史K线 | `get_price()` | `history_bars()` | 低 |
| 所有股票 | `get_all_securities()` | `all_instruments()` | 低 |
| 指数成分股 | `get_index_stocks()` | `index_components()` | 低 |
| 实时数据 | `get_current_data()` | `bar_dict` | 中 |
| 财务数据 | `get_fundamentals()` | `get_fundamentals()` | 低 |
| 估值因子 | `get_valuation()` | `get_factor()` | 低 |
| 技术因子 | `jqfactor.*` | **手动计算** | 高 |
| 质量因子 | `jqfactor.quality.*` | **手动计算** | 高 |
| 动量因子 | `jqfactor.momentum.*` | **手动计算** | 高 |
| 波动率因子 | `jqfactor.volatility.*` | **手动计算** | 高 |
| 涨停价 | `get_current_data().high_limit` | **手动计算** | 中 |
| 定时任务 | `run_daily()` | `scheduler.run_daily()` | 低 |

## 七、迁移建议

### 容易迁移的策略

1. **均线策略** - 只需 `history_bars()`
2. **动量策略** - 手动计算动量
3. **市值选股** - `get_factor(["market_cap"])`
4. **指数增强** - `index_components()`
5. **财务选股** - `get_fundamentals()`

### 需要调整的策略

1. **多因子策略** - 部分因子需要手动计算
2. **技术指标策略** - 需要自己实现指标计算
3. **涨停板策略** - 涨停价需要计算

### 不适合迁移的策略

1. **依赖 jqfactor 特殊因子的策略**
2. **依赖复杂技术分析库的策略**
3. **需要 Tick 级别数据的策略**

## 八、Notebook 中的 API 使用

### JoinQuant Notebook

```python
from jqdata import *

date = "2024-03-20"
stocks = get_all_securities("stock", date).index.tolist()[:100]
print(f"股票数: {len(stocks)}")

# 获取财务数据
q = query(
    valuation.code,
    valuation.pe_ratio,
    valuation.pb_ratio
).filter(valuation.code.in_(stocks))

df = get_fundamentals(q, date=date)
print(df.head())
```

### RiceQuant Notebook

```python
from rqalpha.apis import *

date = "2024-03-20"
all_stocks = all_instruments("CS")
stocks = [s.order_book_id for s in all_stocks][:100]
print(f"股票数: {len(stocks)}")

# 获取财务数据
q = query(
    fundamentals.eod_derivative_indicator.pe_ratio,
    fundamentals.eod_derivative_indicator.pb_ratio
)

df = get_fundamentals(q, entry_date=date)
print(df.head())
```

## 九、总结

**RiceQuant 可以支持**：
- 基础数据获取（价格、成交量、指数成分）
- 基础估值因子（PE、PB、市值）
- 基础财务指标（ROA、ROE、现金流）
- 手动计算技术指标
- 手动计算涨跌停价

**不适合迁移的策略类型**：
- 依赖复杂因子库的策略
- 需要实时 Tick 数据的策略
- 依赖 JoinQuant 特殊因子的策略

**迁移建议**：
1. 选择逻辑简单、依赖基础数据的策略
2. 复杂因子改为手动计算
3. 先在 Notebook 中验证逻辑