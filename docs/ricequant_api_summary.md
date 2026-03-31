# RiceQuant API 能力总结

## 核心API对比

| 功能 | JoinQuant | RiceQuant | 支持情况 |
|------|-----------|-----------|---------|
| 历史K线 | `get_price()` | `history_bars()` | ✅ 支持 |
| 所有股票 | `get_all_securities()` | `all_instruments()` | ✅ 支持 |
| 指数成分 | `get_index_stocks()` | `index_components()` | ✅ 支持 |
| 实时数据 | `get_current_data()` | `bar_dict` | ✅ 支持 |
| 财务数据 | `get_fundamentals()` | `get_fundamentals()` | ✅ 支持 |
| 估值因子 | `get_valuation()` | `get_factor()` | ⚠️ 部分支持 |
| 因子库 | `jqfactor.*` | `fundamentals.*` | ⚠️ 有限支持 |

## RiceQuant 支持的因子

### 1. 估值因子 (get_factor)
```python
# 可用的估值因子
factor_names = [
    "market_cap",        # 总市值
    "pe_ratio",          # 市盈率
    "pb_ratio",          # 市净率
    "pcf_ratio",         # 市现率
    "capitalization",    # 总股本
    "market_cap_float",  # 流通市值
]

# 使用方式
df = get_factor(
    stocks,
    factor=["market_cap", "pe_ratio", "pb_ratio"],
    start_date="2024-01-01",
    end_date="2024-01-31"
)
```

### 2. 财务因子 (get_fundamentals)
```python
from rqalpha.apis import *

# 使用 fundamentals 对象
q = query(
    fundamentals.eod_derivative_indicator.market_cap,
    fundamentals.eod_derivative_indicator.pe_ratio,
    fundamentals.eod_derivative_indicator.pb_ratio,
    fundamentals.financial_indicator.roa,
    fundamentals.financial_indicator.roe,
).filter(
    fundamentals.eod_derivative_indicator.market_cap > 100
)

df = get_fundamentals(q, entry_date="2024-01-01")
```

### 3. 常用财务指标
```python
# RiceQuant fundamentals 支持的主要指标
fundamentals.eod_derivative_indicator:
    - market_cap              # 总市值
    - pe_ratio                # 市盈率
    - pb_ratio                # 市净率
    - turnover_rate           # 换手率
    - volume                  # 成交量
    
fundamentals.financial_indicator:
    - roa                     # 资产收益率
    - roe                     # 净资产收益率
    - net_profit_margin       # 净利率
    - gross_profit_margin     # 毛利率
    - debt_asset_ratio        # 资产负债率
    
fundamentals.cash_flow:
    - net_operate_cash_flow   # 经营现金流
    - net_invest_cash_flow    # 投资现金流
    
fundamentals.balance_sheet:
    - total_assets            # 总资产
    - total_liability         # 总负债
    - total_equity            # 所有者权益
```

## 不支持的 JoinQuant 功能

### 1. 特殊因子库
- ❌ `jqfactor.technical_analysis.*` - 技术分析因子
- ❌ `jqfactor.quality.*` - 质量因子
- ❌ `jqfactor.value.*` - 价值因子
- ❌ `jqfactor.momentum.*` - 动量因子
- ❌ `jqfactor.volatility.*` - 波动率因子
- ❌ `jqfactor.size.*` - 规模因子

**替代方案**：需要手动计算

```python
# 动量因子 - 需要手动计算
def calc_momentum(stock, period=20):
    bars = history_bars(stock, period, "1d", "close")
    if bars is None or len(bars) < period:
        return None
    return (bars[-1] / bars[0] - 1) * 100

# 波动率因子 - 需要手动计算
def calc_volatility(stock, period=20):
    bars = history_bars(stock, period, "1d", "close")
    if bars is None or len(bars) < period:
        return None
    returns = np.diff(bars) / bars[:-1]
    return np.std(returns) * np.sqrt(252)

# RSI - 需要手动计算
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
```

### 2. 其他限制
- ❌ `get_ticks()` - Tick数据（回测中不可用）
- ⚠️ `get_price()` 批量获取 - RiceQuant需要循环
- ⚠️ 涨停价获取 - 需要手动计算

## 策略迁移建议

### ✅ 容易迁移的策略
1. **均线策略** - 只需 `history_bars()`
2. **动量策略** - 手动计算动量
3. **市值选股** - `get_factor(["market_cap"])`
4. **指数增强** - `index_components()`
5. **财务选股** - `get_fundamentals()`

### ⚠️ 需要调整的策略
1. **多因子策略** - 部分因子需要手动计算
2. **技术指标策略** - 需要自己实现指标计算
3. **涨停板策略** - 涨停价需要计算

### ❌ 不适合迁移的策略
1. **依赖 jqfactor 特殊因子的策略**
2. **依赖复杂技术分析库的策略**
3. **需要Tick级别数据的策略**

## Notebook 回测方式

### RiceQuant Notebook API
```python
# 在 Notebook 中测试
import pandas as pd
import numpy as np

# 获取交易日
dates = get_trading_dates('2024-01-01', '2024-12-31')

# 获取股票列表
all_stocks = all_instruments("CS")
stock_ids = [s.order_book_id for s in all_stocks]

# 获取历史数据
bars = history_bars("000001.XSHE", 20, "1d", ["close", "volume"])

# 获取指数成分
hs300 = index_components("000300.XSHG")

# 获取财务数据
from rqalpha.apis import *
q = query(fundamentals.eod_derivative_indicator.market_cap)
df = get_fundamentals(q, entry_date="2024-01-01")
```

## 总结

**RiceQuant 可以支持**：
- ✅ 基础数据获取（价格、成交量、指数成分）
- ✅ 基础估值因子（PE、PB、市值）
- ✅ 基础财务指标（ROA、ROE、现金流）
- ⚠️ 手动计算技术指标
- ⚠️ 手动计算涨跌停价

**不适合的策略类型**：
- ❌ 依赖复杂因子库的策略
- ❌ 需要实时Tick数据的策略

**迁移建议**：
1. 选择逻辑简单、依赖基础数据的策略
2. 复杂因子改为手动计算
3. 先在Notebook中验证逻辑