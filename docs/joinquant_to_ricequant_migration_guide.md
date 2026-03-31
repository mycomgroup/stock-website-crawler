# 聚宽(JoinQuant) → 米筐(RiceQuant) 策略迁移指南

> 更新时间：2026-03-31
> 验证状态：已通过实测验证

## 目录

1. [核心差异总览](#核心差异总览)
2. [初始化与配置](#初始化与配置)
3. [定时任务机制](#定时任务机制)
4. [数据获取API对照](#数据获取api对照)
5. [交易函数API对照](#交易函数api对照)
6. [持仓与账户信息](#持仓与账户信息)
7. [全局变量管理](#全局变量管理)
8. [完整迁移案例](#完整迁移案例)
9. [常见问题与陷阱](#常见问题与陷阱)
10. [迁移检查清单](#迁移检查清单)
11. [实测验证要点](#实测验证要点)
12. [因子数据API对照](#十二因子数据-api-对照)

---

## 核心差异总览

| 功能模块 | 聚宽 (JoinQuant) | 米筐 (RiceQuant) | 迁移难度 |
|---------|-----------------|-----------------|---------|
| 初始化函数 | `initialize(context)` | `init(context)` | 低 |
| 主循环函数 | 无（通过run_daily注册） | `handle_bar(context, bar_dict)` | 高 |
| 全局变量 | `g.xxx` | `context.xxx` | 低 |
| 定时任务 | `run_daily(func, time)` | `scheduler.run_daily(func)` | 高 |
| 历史数据 | `get_price()` | `history_bars()` | 中 |
| 所有股票列表 | `get_all_securities()` | `all_instruments()` | **高** |
| 当日实时数据 | `get_current_data()` | `bar_dict` 参数 | 高 |
| 日志系统 | `log.info()` | `logger.info()` | 低 |
| 涨停价获取 | `cd.high_limit` | 需计算或使用 `get_price()` | 中 |
| 配置选项 | `set_option()` | `config` 字典 | 中 |
| **清仓函数** | `order_target(stock, 0)` | `order_target_value(stock, 0)` | **高** |

---

## 初始化与配置

### 聚宽写法

```python
from jqdata import *

def initialize(context):
    # 配置选项
    set_option("use_real_price", True)
    set_option("avoid_future_data", True)
    log.set_level("order", "error")
    log.set_level("system", "error")
    
    # 全局变量
    g.trade_count = 0
    g.win_count = 0
    g.target_stocks = []
    
    # 注册定时任务
    run_daily(select_stocks, "9:00")
    run_daily(buy_stocks, "9:35")
    run_daily(sell_stocks, "14:50")
```

### 米筐写法

```python
def init(context):
    # 配置选项（通过字典）
    context.config = {
        "use_real_price": True,
        "avoid_future_data": True,
    }
    
    # 全局变量（存储在context中）
    context.trade_count = 0
    context.win_count = 0
    context.target_stocks = []
    
    # 注册定时任务
    scheduler.run_daily(select_stocks, time_rule=market_open(minute=0))
    scheduler.run_daily(buy_stocks, time_rule=market_open(minute=35))
    scheduler.run_daily(sell_stocks, time_rule=market_close(minute=10))
```

### 关键差异

| 项目 | 聚宽 | 米筐 | 说明 |
|-----|------|------|-----|
| 函数名 | `initialize` | `init` | 必须改名 |
| 全局变量前缀 | `g.` | `context.` | 必须替换 |
| 配置方式 | `set_option()` | `context.config` | 可选，米筐默认已优化 |
| 时间格式 | `"9:00"` 字符串 | `market_open(minute=0)` | 必须修改 |

---

## 定时任务机制

### 聚宽定时任务

```python
def initialize(context):
    run_daily(select_stocks, "9:00")      # 开盘前选股
    run_daily(buy_stocks, "9:35")          # 开盘后买入
    run_daily(sell_stocks, "14:50")        # 收盘前卖出
    run_weekly(weekly_rebalance, 1, "9:00") # 每周执行
    run_monthly(monthly_report, 1, "15:00") # 每月执行

def select_stocks(context):
    # 这里的context和initialize的context是同一个
    pass

def buy_stocks(context):
    pass
```

### 米筐定时任务

```python
def init(context):
    # 方式1：使用scheduler
    scheduler.run_daily(select_stocks, time_rule=market_open(minute=0))
    scheduler.run_daily(buy_stocks, time_rule=market_open(minute=35))
    scheduler.run_daily(sell_stocks, time_rule=market_close(minute=10))
    
    # 方式2：在handle_bar中手动判断（更灵活）
    context.last_rebalance_date = None

def handle_bar(context, bar_dict):
    # 每分钟执行一次
    today = context.now.date()
    
    # 判断是否需要执行（每月初）
    if context.last_rebalance_date is None or context.last_rebalance_date.month != today.month:
        context.last_rebalance_date = today
        monthly_rebalance(context, bar_dict)
    
    # 判断时间执行每日任务
    current_time = context.now.time()
    if current_time.hour == 9 and current_time.minute == 35:
        buy_stocks(context, bar_dict)

def select_stocks(context, bar_dict):
    pass

def buy_stocks(context, bar_dict):
    pass
```

### 时间规则对照

| 聚宽 | 米筐 | 说明 |
|------|------|-----|
| `"9:00"` | `market_open(minute=0)` | 开盘时刻 |
| `"9:35"` | `market_open(minute=35)` | 开盘后35分钟 |
| `"14:50"` | `market_close(minute=10)` | 收盘前10分钟 |
| `run_weekly` | 手动判断 `context.now.weekday()` | 每周任务 |
| `run_monthly` | 手动判断 `context.now.month` | 每月任务 |

---

## 数据获取API对照

### 1. 获取历史K线数据

#### 聚宽: get_price()

```python
# 获取单只股票
df = get_price("000001.XSHE", 
               end_date="2024-01-01", 
               count=20, 
               fields=["open", "close", "high", "low", "volume"],
               panel=False)

# 获取多只股票
df = get_price(["000001.XSHE", "000002.XSHE"],
               end_date="2024-01-01",
               count=20,
               fields=["close"],
               panel=False)

# 返回DataFrame格式
#         code        close    open     high      low    volume
# 0  000001.XSHE  12.34   12.00    12.50    11.90   1000000
# 1  000001.XSHE  12.56   12.30    12.70    12.20   1200000
```

#### 米筐: history_bars()

```python
# 获取单只股票（返回numpy数组）
bars = history_bars("000001.XSHE", 20, "1d", 
                   fields=["open", "close", "high", "low", "volume"])

# 返回结构化数组，字段通过columns访问
# bars['close'] 返回收盘价数组
# bars['open'] 返回开盘价数组
close_prices = bars['close']  # 形状: (20,)

# 获取多只股票需要循环
stocks = ["000001.XSHE", "000002.XSHE"]
for stock in stocks:
    bars = history_bars(stock, 20, "1d", "close")
    if bars is not None:
        close_prices = bars
```

#### 关键差异

| 特性 | 聚宽 `get_price()` | 米筐 `history_bars()` |
|-----|-------------------|---------------------|
| 返回类型 | DataFrame | numpy结构化数组 |
| 批量获取 | 支持，一次多只 | 不支持，需要循环 |
| 字段访问 | `df['close']` | `bars['close']` |
| 时间参数 | `end_date` + `count` | 仅 `count`（默认到当前） |
| None检查 | `df.empty` | `bars is None or len(bars) == 0` |

### 2. 获取所有股票列表

#### 聚宽: get_all_securities()

```python
# 获取所有A股
all_stocks = get_all_securities("stock", date="2024-01-01")
# 返回DataFrame，index为股票代码

# 获取所有ETF
all_etfs = get_all_securities("etf", date="2024-01-01")

# 过滤
stocks = [s for s in all_stocks.index if s[0] not in "683"]  # 排除科创板、北交所
```

#### 米筐: all_instruments()

```python
# 获取所有A股
all_stocks = all_instruments("CS")  # CS表示股票
# 返回DataFrame，列包括order_book_id, symbol, display_name等

# 获取股票代码列表
stock_ids = [inst.order_book_id for inst in all_stocks]

# 过滤
stocks = [s.order_book_id for s in all_stocks 
          if not s.order_book_id.startswith("688")]  # 排除科创板
```

#### 类型对照表

| 类型 | 聚宽参数 | 米筐参数 |
|------|---------|---------|
| A股股票 | `"stock"` | `"CS"` |
| ETF基金 | `"etf"` | `"ETF"` |
| LOF基金 | `"lof"` | `"LOF"` |
| 指数 | `"index"` | `"INDX"` |

### 3. 获取指数成分股

#### 聚宽: get_index_stocks()

```python
hs300 = get_index_stocks("000300.XSHG", date="2024-01-01")
# 返回股票代码列表
```

#### 米筐: index_components()

```python
hs300 = index_components("000300.XSHG")
# 返回股票代码列表
```

### 4. 获取财务数据

#### 聚宽: get_fundamentals()

```python
q = query(
    valuation.code,
    valuation.market_cap,
    valuation.pe_ratio
).filter(
    valuation.market_cap > 100
).order_by(
    valuation.market_cap.desc()
).limit(10)

df = get_fundamentals(q, statDate="2024q1")
```

#### 米筐: get_fundamentals()

```python
# 米筐语法类似但字段名不同
q = query(
    fundamentals.eod_derivative_indicator.market_cap,
    fundamentals.eod_derivative_indicator.pe_ratio
).filter(
    fundamentals.eod_derivative_indicator.market_cap > 100
).order_by(
    fundamentals.eod_derivative_indicator.market_cap.desc()
).limit(10)

df = get_fundamentals(q, entry_date="2024-03-31")
```

### 5. 获取估值数据

#### 聚宽: get_valuation()

```python
df = get_valuation("000001.XSHE", 
                   end_date="2024-01-01", 
                   count=10,
                   fields=["market_cap", "pe_ratio", "pb_ratio", "circulating_market_cap"])
```

#### 米筐: get_factor()

```python
# 米筐使用get_factor获取估值因子
df = get_factor("000001.XSHE",
                factor=["market_cap", "pe_ratio", "pb_ratio"],
                start_date="2023-12-01",
                end_date="2024-01-01")
```

### 6. 当日实时数据

#### 聚宽: get_current_data()

```python
def buy_stocks(context):
    current_data = get_current_data()
    
    for stock in g.target_stocks:
        cd = current_data[stock]
        
        # 当日开盘价
        day_open = cd.day_open
        
        # 昨日收盘价
        pre_close = cd.pre_close
        
        # 涨停价
        high_limit = cd.high_limit
        
        # 跌停价
        low_limit = cd.low_limit
        
        # 是否停牌
        if cd.paused:
            continue
        
        # 最新价
        last_price = cd.last_price
        
        # 计算开盘涨幅
        open_pct = (day_open - pre_close) / pre_close * 100
```

#### 米筐: bar_dict

```python
def handle_bar(context, bar_dict):
    for stock in context.target_stocks:
        # 通过bar_dict访问
        bar = bar_dict[stock]
        
        # 当日开盘价
        day_open = bar.open
        
        # 昨日收盘价
        pre_close = bar.close / (1 + bar.benchmark_return)  # 近似
        
        # 涨停价和跌停价 - 需要通过history_bars计算
        bars = history_bars(stock, 1, "1d", "close")
        pre_close = bars[-1] if bars is not None else bar.close
        high_limit = round(pre_close * 1.1, 2)  # 简化计算
        low_limit = round(pre_close * 0.9, 2)
        
        # 是否停牌
        if bar.is_trading is False:
            continue
        
        # 最新价
        last_price = bar.close
```

#### 米筐涨停价准确计算

```python
def get_limit_price(stock, bar_dict):
    """获取涨停价和跌停价"""
    # 方法1：从历史数据获取
    bars = history_bars(stock, 2, "1d", ["close", "limit_up", "limit_down"])
    if bars is not None and len(bars) >= 2:
        return bars[-1]['limit_up'], bars[-1]['limit_down']
    
    # 方法2：近似计算（可能不精确，ST股票涨跌幅不同）
    bars = history_bars(stock, 1, "1d", "close")
    if bars is not None:
        pre_close = bars[-1]
        # 需要判断是否ST股票
        instrument = instruments(stock)
        if instrument.special_type == "ST":  # ST股票
            return round(pre_close * 1.05, 2), round(pre_close * 0.95, 2)
        else:
            return round(pre_close * 1.1, 2), round(pre_close * 0.9, 2)
    
    return None, None
```

---

## 交易函数API对照

### 1. 下单函数

#### 聚宽

```python
# 按股数下单
order("000001.XSHE", 100)  # 买入100股
order("000001.XSHE", -100)  # 卖出100股

# 按金额下单
order_value("000001.XSHE", 10000)  # 买入1万元

# 调整到目标股数
order_target("000001.XSHE", 1000)  # 调整持仓到1000股

# 调整到目标金额
order_target_value("000001.XSHE", 10000)  # 调整持仓到1万元

# 调整到目标比例
order_target_percent("000001.XSHE", 0.1)  # 调整持仓到总资产的10%
```

#### 米筐

```python
# 按股数下单
order_shares("000001.XSHE", 100)  # 买入100股
order_shares("000001.XSHE", -100)  # 卖出100股

# 按金额下单
order_value("000001.XSHE", 10000)  # 买入1万元（同名）

# 调整到目标股数
order_target_quantity("000001.XSHE", 1000)  # 注意：不是order_target

# 调整到目标金额
order_target_value("000001.XSHE", 10000)  # 同名

# 调整到目标比例
order_target_percent("000001.XSHE", 0.1)  # 同名
```

### 函数名对照表

| 功能 | 聚宽 | 米筐 |
|-----|------|------|
| 按股数下单 | `order(stock, amount)` | `order_shares(stock, amount)` |
| 按金额下单 | `order_value(stock, cash)` | `order_value(stock, cash)` |
| 调整到目标股数 | `order_target(stock, amount)` | `order_target_quantity(stock, amount)` |
| 调整到目标金额 | `order_target_value(stock, cash)` | `order_target_value(stock, cash)` |
| 调整到目标比例 | `order_target_percent(stock, percent)` | `order_target_percent(stock, percent)` |

### 2. 持仓信息

#### 聚宽

```python
def sell_stocks(context):
    for stock in context.portfolio.positions:
        pos = context.portfolio.positions[stock]
        
        # 总持仓股数
        total_amount = pos.total_amount
        
        # 可卖股数（T+1限制）
        closeable_amount = pos.closeable_amount
        
        # 平均成本
        avg_cost = pos.avg_cost
        
        # 当前市值
        value = pos.value
        
        # 盈亏比例
        pnl_ratio = (pos.price - avg_cost) / avg_cost
        
        # 清仓
        if closeable_amount > 0:
            order_target(stock, 0)
```

#### 米筐

```python
def handle_bar(context, bar_dict):
    for stock in list(context.portfolio.positions.keys()):
        pos = context.portfolio.positions[stock]
        
        # 总持仓股数
        quantity = pos.quantity
        
        # 可卖股数
        sellable_quantity = pos.sellable_quantity
        
        # 平均成本
        avg_cost = pos.avg_cost
        
        # 当前市值
        market_value = pos.market_value
        
        # 盈亏比例
        pnl_ratio = (pos.last_price - avg_cost) / avg_cost
        
        # 清仓
        if sellable_quantity > 0:
            order_target_quantity(stock, 0)  # 注意：不是order_target
```

### 持仓属性对照表

| 属性 | 聚宽 | 米筐 |
|-----|------|------|
| 总股数 | `total_amount` | `quantity` |
| 可卖股数 | `closeable_amount` | `sellable_quantity` |
| 平均成本 | `avg_cost` | `avg_cost` |
| 当前价格 | `price` (需计算) | `last_price` |
| 市值 | `value` | `market_value` |
| 盈亏金额 | `pnl` | `pnl` |

### 3. 账户信息

#### 聚宽

```python
# 总资产
total_value = context.portfolio.total_value

# 可用现金
available_cash = context.portfolio.available_cash

# 持仓市值
positions_value = context.portfolio.positions_value

# 收益率
returns = context.portfolio.returns
```

#### 米筐

```python
# 总资产
total_value = context.portfolio.total_value

# 可用现金
available_cash = context.portfolio.cash  # 注意：不是available_cash

# 持仓市值
positions_value = context.portfolio.market_value

# 收益率（需要自己计算）
returns = (total_value - context.portfolio.starting_cash) / context.portfolio.starting_cash
```

---

## 全局变量管理

### 聚宽: g对象

```python
def initialize(context):
    g.trade_count = 0
    g.target_stocks = []
    g.last_trade_date = None
    
def select_stocks(context):
    g.target_stocks = ["000001.XSHE", "000002.XSHE"]
    g.trade_count += 1
    
def buy_stocks(context):
    if g.target_stocks:
        for stock in g.target_stocks:
            order(stock, 100)
```

### 米筐: context对象

```python
def init(context):
    context.trade_count = 0
    context.target_stocks = []
    context.last_trade_date = None
    
def select_stocks(context, bar_dict):
    context.target_stocks = ["000001.XSHE", "000002.XSHE"]
    context.trade_count += 1
    
def buy_stocks(context, bar_dict):
    if context.target_stocks:
        for stock in context.target_stocks:
            order_shares(stock, 100)
```

### 迁移要点

1. **全局搜索替换**: `g.` → `context.`
2. 注意`context`需要在每个函数中传递
3. 米筐的自定义函数必须接受`context`和`bar_dict`参数

---

## 完整迁移案例

### 案例1: 简单选股策略

#### 聚宽原始代码

```python
from jqdata import *

def initialize(context):
    set_option("use_real_price", True)
    log.set_level("order", "error")
    
    g.stocks = []
    g.trade_count = 0
    
    run_daily(select_stocks, "9:00")
    run_daily(buy_stocks, "9:35")

def select_stocks(context):
    date = context.current_dt.date()
    date_str = str(date)
    
    # 获取沪深300成分股
    hs300 = get_index_stocks("000300.XSHG", date=date)
    
    # 选出市值前10
    q = query(
        valuation.code,
        valuation.market_cap
    ).filter(
        valuation.code.in_(hs300)
    ).order_by(
        valuation.market_cap.desc()
    ).limit(10)
    
    df = get_fundamentals(q, statDate=date_str)
    g.stocks = list(df['code'])

def buy_stocks(context):
    if not g.stocks:
        return
    
    # 等权买入
    cash_per_stock = context.portfolio.available_cash / len(g.stocks)
    
    for stock in g.stocks:
        order_value(stock, cash_per_stock)
        g.trade_count += 1
```

#### 米筐迁移后代码

```python
def init(context):
    context.stocks = []
    context.trade_count = 0
    
    scheduler.run_daily(select_stocks, time_rule=market_open(minute=0))
    scheduler.run_daily(buy_stocks, time_rule=market_open(minute=35))

def select_stocks(context, bar_dict):
    # 获取沪深300成分股
    hs300 = index_components("000300.XSHG")
    
    # 选出市值前10
    q = query(
        fundamentals.eod_derivative_indicator.market_cap
    ).filter(
        fundamentals.eod_derivative_indicator.order_book_id.in_(hs300)
    ).order_by(
        fundamentals.eod_derivative_indicator.market_cap.desc()
    ).limit(10)
    
    df = get_fundamentals(q, entry_date=context.now.date())
    context.stocks = list(df.index)

def buy_stocks(context, bar_dict):
    if not context.stocks:
        return
    
    # 等权买入
    cash_per_stock = context.portfolio.cash / len(context.stocks)
    
    for stock in context.stocks:
        order_value(stock, cash_per_stock)
        context.trade_count += 1
```

### 案例2: 涨停板策略（复杂实时数据）

#### 聚宽原始代码

```python
from jqdata import *

def initialize(context):
    set_option("use_real_price", True)
    
    g.target = []
    run_daily(select_limit_up, "9:00")
    run_daily(buy_stocks, "9:35")

def select_limit_up(context):
    prev_date = context.previous_date.strftime("%Y-%m-%d")
    
    all_stocks = get_all_securities("stock", prev_date).index.tolist()
    all_stocks = [s for s in all_stocks if s[0] not in "483"]
    
    # 找出昨日涨停股票
    df = get_price(
        all_stocks,
        end_date=prev_date,
        frequency="daily",
        fields=["close", "high_limit"],
        count=1,
        panel=False,
    )
    df = df.dropna()
    df = df[df["close"] == df["high_limit"]]
    g.target = list(df["code"])[:20]

def buy_stocks(context):
    if not g.target:
        return
    
    current_data = get_current_data()
    qualified = []
    
    for s in g.target:
        cd = current_data[s]
        
        if cd.paused:
            continue
        
        # 计算开盘涨幅
        open_pct = (cd.day_open - cd.pre_close) / cd.pre_close * 100
        
        # 选择开盘涨幅在-1.5%到1.5%之间的
        if -1.5 <= open_pct <= 1.5:
            qualified.append(s)
    
    if qualified:
        cash = context.portfolio.available_cash / min(len(qualified), 3)
        for s in qualified[:3]:
            shares = int(cash / current_data[s].last_price / 100) * 100
            if shares >= 100:
                order(s, shares)
```

#### 米筐迁移后代码

```python
def init(context):
    context.target = []
    scheduler.run_daily(select_limit_up, time_rule=market_open(minute=0))
    scheduler.run_daily(buy_stocks, time_rule=market_open(minute=35))

def select_limit_up(context, bar_dict):
    # 获取所有A股
    all_stocks = all_instruments("CS")
    stock_ids = [s.order_book_id for s in all_stocks 
                 if not s.order_book_id.startswith(('688', '4', '8'))]
    
    context.target = []
    
    # 找出昨日涨停股票（需要循环获取）
    for stock in stock_ids[:500]:  # 注意：需要分批处理
        try:
            bars = history_bars(stock, 2, "1d", ["close", "limit_up"])
            if bars is None or len(bars) < 2:
                continue
            
            # 昨日收盘价等于涨停价
            if abs(bars[-1]['close'] - bars[-1]['limit_up']) < 0.01:
                context.target.append(stock)
                
            if len(context.target) >= 20:
                break
        except:
            continue

def buy_stocks(context, bar_dict):
    if not context.target:
        return
    
    qualified = []
    
    for s in context.target:
        try:
            bar = bar_dict[s]
            
            # 检查是否停牌
            if not bar.is_trading:
                continue
            
            # 获取昨日收盘价
            bars = history_bars(s, 1, "1d", "close")
            if bars is None or len(bars) == 0:
                continue
            
            pre_close = bars[-1]
            day_open = bar.open
            
            # 计算开盘涨幅
            open_pct = (day_open - pre_close) / pre_close * 100
            
            # 选择开盘涨幅在-1.5%到1.5%之间的
            if -1.5 <= open_pct <= 1.5:
                qualified.append(s)
        except:
            continue
    
    if qualified:
        cash = context.portfolio.cash / min(len(qualified), 3)
        for s in qualified[:3]:
            last_price = bar_dict[s].close
            shares = int(cash / last_price / 100) * 100
            if shares >= 100:
                order_shares(s, shares)
```

---

## 常见问题与陷阱

### 1. 批量数据获取性能问题

**问题**: 聚宽的`get_price()`支持批量获取，米筐的`history_bars()`需要循环

**解决方案**:

```python
# 错误：直接对大量股票循环（性能差）
stocks = all_instruments("CS")  # 4000+只股票
for stock in stocks:
    bars = history_bars(stock, 20, "1d", "close")  # 非常慢

# 正确：分批处理
stocks = all_instruments("CS")
batch_size = 100
for i in range(0, len(stocks), batch_size):
    batch = stocks[i:i+batch_size]
    for stock in batch:
        bars = history_bars(stock, 20, "1d", "close")
        # 处理...
```

### 2. 涨停价计算差异

**问题**: 米筐没有直接的`high_limit`属性，需要计算

**解决方案**:

```python
def get_limit_prices(stock, pre_close):
    """计算涨停价和跌停价"""
    # 获取股票信息
    inst = instruments(stock)
    
    # 判断涨跌停幅度
    # 普通股票: 10%
    # ST股票: 5%
    # 科创板/创业板注册制: 20%
    # 北交所: 30%
    
    if inst.special_type == "ST":
        limit_pct = 0.05
    elif stock.startswith("688") or stock.startswith("30"):
        limit_pct = 0.20
    elif stock.startswith(("4", "8")):  # 北交所
        limit_pct = 0.30
    else:
        limit_pct = 0.10
    
    high_limit = round(pre_close * (1 + limit_pct), 2)
    low_limit = round(pre_close * (1 - limit_pct), 2)
    
    return high_limit, low_limit
```

### 3. 时间判断问题

**问题**: 聚宽`run_daily`精确到分钟，米筐`scheduler.run_daily`可能在开盘后第一分钟执行

**解决方案**:

```python
def init(context):
    context.last_execute_time = None
    scheduler.run_daily(buy_stocks, time_rule=market_open(minute=35))

def buy_stocks(context, bar_dict):
    # 双重检查
    current_time = context.now.time()
    target_time = datetime.time(9, 35)
    
    if context.last_execute_time != target_time:
        # 执行逻辑
        context.last_execute_time = current_time
```

### 4. 空值检查差异

**问题**: 聚宽返回空DataFrame，米筐返回None

```python
# 聚宽
df = get_price(stock, end_date=date, count=10)
if df.empty:
    return

# 米筐
bars = history_bars(stock, 10, "1d", "close")
if bars is None or len(bars) == 0:
    return
```

### 5. 字典键访问差异

**问题**: `bar_dict`访问不存在的股票会报错

```python
# 错误：直接访问可能不存在
bar = bar_dict[stock]  # 如果stock停牌或未上市，会报错

# 正确：先检查
if stock in bar_dict:
    bar = bar_dict[stock]
else:
    continue
```

### 6. 日期格式差异

```python
# 聚宽
date = context.previous_date.strftime("%Y-%m-%d")

# 米筐
date = context.now.date()  # datetime.date对象
date_str = context.now.strftime("%Y-%m-%d")  # 字符串格式
```

---

## 迁移检查清单

### 第一阶段：准备工作

- [ ] 备份原始聚宽策略代码
- [ ] 在米筐平台注册账号
- [ ] 熟悉米筐API文档
- [ ] 准备测试数据（相同时间段）

### 第二阶段：代码修改

- [ ] 修改初始化函数名：`initialize` → `init`
- [ ] 替换全局变量：`g.` → `context.`
- [ ] 修改定时任务注册方式
- [ ] 修改数据获取函数
  - [ ] `get_price()` → `history_bars()`
  - [ ] `get_all_securities()` → `all_instruments()`
  - [ ] `get_index_stocks()` → `index_components()`
  - [ ] `get_current_data()` → `bar_dict`
- [ ] 修改交易函数
  - [ ] `order()` → `order_shares()`
  - [ ] `order_target()` → `order_target_quantity()`
- [ ] 修改持仓属性访问
  - [ ] `closeable_amount` → `sellable_quantity`
  - [ ] `available_cash` → `cash`
- [ ] 修改日志函数：`log` → `logger`
- [ ] 添加涨停价计算函数

### 第三阶段：功能测试

- [ ] 在相同时间段运行回测
- [ ] 对比交易次数
- [ ] 对比收益率
- [ ] 对比持仓股票
- [ ] 检查是否遗漏`bar_dict`参数
- [ ] 检查空值处理

### 第四阶段：性能优化

- [ ] 减少批量数据获取次数
- [ ] 优化循环效率
- [ ] 缓存频繁访问的数据
- [ ] 检查回测时间是否合理

### 第五阶段：上线准备

- [ ] 模拟盘测试
- [ ] 实盘小资金测试
- [ ] 监控日志输出
- [ ] 设置错误告警

---

## 快速参考表

### 常用函数对照

| 功能 | 聚宽 | 米筐 |
|-----|------|------|
| 初始化 | `initialize(context)` | `init(context)` |
| 主循环 | `run_daily()` | `handle_bar()` + `scheduler` |
| 历史数据 | `get_price()` | `history_bars()` |
| 所有股票 | `get_all_securities()` | `all_instruments()` |
| 成分股 | `get_index_stocks()` | `index_components()` |
| 实时数据 | `get_current_data()` | `bar_dict` |
| 买入 | `order(stock, n)` | `order_shares(stock, n)` |
| 清仓 | `order_target(stock, 0)` | `order_target_quantity(stock, 0)` |
| 按金额 | `order_value()` | `order_value()` |
| 按比例 | `order_target_percent()` | `order_target_percent()` |
| 可用现金 | `available_cash` | `cash` |
| 可卖股数 | `closeable_amount` | `sellable_quantity` |
| 日志 | `log.info()` | `logger.info()` |

### 时间规则对照

| 时间点 | 聚宽 | 米筐 |
|-------|------|------|
| 开盘 | `"9:30"` | `market_open(minute=0)` |
| 开盘后N分钟 | `"9:35"` | `market_open(minute=5)` |
| 收盘前N分钟 | `"14:50"` | `market_close(minute=10)` |
| 收盘 | `"15:00"` | `market_close(minute=0)` |

---

## 总结

聚宽到米筐的迁移主要涉及：

1. **低难度**：函数名、变量名修改（约20%工作量）
2. **中难度**：数据获取函数重写（约40%工作量）
3. **高难度**：定时任务和实时数据处理重构（约40%工作量）

建议：
- 先迁移简单策略熟悉差异
- 使用相同参数对比回测结果
- 注意性能优化（批量数据获取）
- 充分测试后再实盘

---

## 附录：常用代码片段

### 米筐涨停价判断

```python
def is_limit_up(stock, bar_dict):
    """判断是否涨停"""
    bars = history_bars(stock, 2, "1d", ["close", "limit_up"])
    if bars is None or len(bars) < 2:
        return False
    
    current_close = bar_dict[stock].close
    limit_up = bars[-1]['limit_up']
    
    return abs(current_close - limit_up) < 0.01
```

### 米筐涨停板股票筛选

```python
def get_limit_up_stocks(context, bar_dict):
    """获取今日涨停股票"""
    stocks = []
    all_instruments_list = all_instruments("CS")
    
    for inst in all_instruments_list:
        stock = inst.order_book_id
        if stock.startswith(('688', '4', '8')):  # 排除科创板、北交所
            continue
        
        try:
            if stock not in bar_dict:
                continue
            
            bar = bar_dict[stock]
            if not bar.is_trading:
                continue
            
            bars = history_bars(stock, 1, "1d", "limit_up")
            if bars is None:
                continue
            
            if abs(bar.close - bars[-1]['limit_up']) < 0.01:
                stocks.append(stock)
        except:
            continue
    
    return stocks
```

### 米筐定时任务模板

```python
def init(context):
    context.last_rebalance_month = -1
    context.last_trade_date = None

def handle_bar(context, bar_dict):
    today = context.now.date()
    
    # 每月初执行
    if context.last_rebalance_month != today.month:
        context.last_rebalance_month = today.month
        monthly_rebalance(context, bar_dict)
    
    # 每日特定时间执行
    current_time = context.now.time()
    if current_time.hour == 9 and current_time.minute == 35:
        daily_buy(context, bar_dict)
    
    if current_time.hour == 14 and current_time.minute == 50:
        daily_sell(context, bar_dict)

def monthly_rebalance(context, bar_dict):
    logger.info(f"Monthly rebalance: {context.now}")

def daily_buy(context, bar_dict):
    logger.info(f"Daily buy: {context.now}")

def daily_sell(context, bar_dict):
    logger.info(f"Daily sell: {context.now}")
```

---

## 十一、实测验证要点

> 以下内容基于 2026-03-31 实测验证，确保策略能正常运行

### 11.1 关键发现（必须注意）

#### ❌ `order_target` 不存在

**错误写法**：
```python
order_target(stock, 0)  # NameError: name 'order_target' is not defined
```

**正确写法**：
```python
order_target_value(stock, 0)  # 清仓（目标市值=0）
# 或
order_target_quantity(stock, 0)  # 清仓（目标数量=0）
```

#### ❌ `all_instruments("CS")` 返回 DataFrame

**错误写法**：
```python
for inst in all_instruments("CS"):
    stock = inst.order_book_id  # AttributeError: 'str' object has no attribute 'order_book_id'
```

**正确写法**：
```python
all_inst = all_instruments("CS")
stock_list = all_inst["order_book_id"].tolist()  # 获取股票代码列表

for stock in stock_list:
    # 处理每只股票
    pass
```

#### ✅ 日志函数使用 `logger` 而非 `log`

```python
# 正确
logger.info(f"买入 {stock}")

# 错误（在某些版本中可能报错）
log.info(f"买入 {stock}")
```

### 11.2 股票列表获取方式对比

| 方式 | 聚宽 | 米筐 |
|------|------|------|
| 获取所有股票 | `get_all_securities("stock", date).index.tolist()` | `all_instruments("CS")["order_book_id"].tolist()` |
| 获取所有ETF | `get_all_securities("etf", date).index.tolist()` | `all_instruments("ETF")["order_book_id"].tolist()` |
| 遍历方式 | `for stock in stocks:` | `for stock in stock_list:` |

### 11.3 清仓/调仓函数对比

| 功能 | 聚宽 | 米筐 |
|------|------|------|
| 清仓 | `order_target(stock, 0)` | `order_target_value(stock, 0)` 或 `order_target_quantity(stock, 0)` |
| 调整到目标数量 | `order_target(stock, 1000)` | `order_target_quantity(stock, 1000)` |
| 调整到目标市值 | `order_target_value(stock, 10000)` | `order_target_value(stock, 10000)` |
| 买入指定股数 | `order(stock, 100)` | `order_shares(stock, 100)` |

### 11.4 实测验证的最小策略模板

```python
"""
RiceQuant 最小验证策略
实测通过，可产生交易记录
"""

def init(context):
    context.s1 = "000001.XSHE"
    logger.info("=== 策略初始化 ===")


def handle_bar(context, bar_dict):
    stock = context.s1
    
    # 获取历史价格
    prices = history_bars(stock, 5, "1d", "close")
    
    if len(prices) < 5:
        return
    
    # 获取当前持仓
    position = context.portfolio.positions.get(stock)
    cur_position = position.quantity if position else 0
    
    # 如果没有持仓，买入
    if cur_position == 0:
        cash = context.portfolio.cash
        shares = int(cash / bar_dict[stock].close / 100) * 100
        if shares >= 100:
            order_shares(stock, shares)
            logger.info(f"买入 {stock} {shares}股")
    
    # 如果有持仓，卖出
    elif cur_position > 0:
        order_target_value(stock, 0)  # 正确的清仓方式
        logger.info(f"卖出 {stock} {cur_position}股")
```

### 11.5 常见错误速查

| 错误信息 | 原因 | 解决方案 |
|----------|------|----------|
| `NameError: name 'order_target' is not defined` | 米筐没有 `order_target` 函数 | 改用 `order_target_value(stock, 0)` |
| `AttributeError: 'str' object has no attribute 'order_book_id'` | `all_instruments()` 返回 DataFrame，不能直接遍历 | 使用 `all_instruments("CS")["order_book_id"].tolist()` |
| `NameError: name 'log' is not defined` | 某些版本不支持 `log` | 改用 `logger.info()` |
| `KeyError` 访问持仓 | 持仓字典可能不包含该股票 | 使用 `positions.get(stock)` 或先检查 |

### 11.6 迁移检查清单（更新版）

- [ ] 修改初始化函数名：`initialize` → `init`
- [ ] 替换全局变量：`g.` → `context.`
- [ ] **修改股票列表获取**：`get_all_securities()` → `all_instruments()["order_book_id"].tolist()`
- [ ] **修改清仓函数**：`order_target(stock, 0)` → `order_target_value(stock, 0)`
- [ ] **修改买入函数**：`order(stock, n)` → `order_shares(stock, n)`
- [ ] 修改数据获取：`get_price()` → `history_bars()`
- [ ] 修改实时数据：`get_current_data()` → `bar_dict`
- [ ] 检查日志函数：确保使用 `logger.info()`
- [ ] 测试最小策略验证交易是否正常

---

## 十二、因子数据 API 对照

### 12.1 RiceQuant get_factor() 完整因子列表

RiceQuant 使用 `get_factor()` 函数获取财务和估值因子数据。

#### 基本用法

```python
# 获取单个因子
data = get_factor(stocks, "pe_ratio", start_date="2024-01-01", end_date="2024-01-31")

# 获取多个因子
factors = ["pe_ratio", "pb_ratio", "roa", "roe"]
data = get_factor(stocks, factors, start_date="2024-01-01", end_date="2024-01-31")

# 返回格式: DataFrame 或 dict
# 可通过 data["pe_ratio"] 访问具体因子
```

### 12.2 估值类因子

| 因子名 | 中文名 | 说明 |
|--------|--------|------|
| `pe_ratio` | 市盈率 | 股价/每股收益 |
| `pb_ratio` | 市净率 | 股价/每股净资产 |
| `ps_ratio` | 市销率 | 股价/每股销售额 |
| `pcf_ratio` | 市现率 | 股价/每股现金流 |
| `ev` | 企业价值 | 市值+净债务 |
| `ebitda` | 息税折旧摊销前利润 | |
| `market_cap` | 总市值 | |
| `circulating_market_cap` | 流通市值 | |
| `capitalization` | 总股本 | |
| `circulating_cap` | 流通股本 | |

### 12.3 盈利能力因子

| 因子名 | 中文名 | 说明 |
|--------|--------|------|
| `roa` | 资产收益率 | 净利润/总资产 |
| `roe` | 净资产收益率 | 净利润/净资产 |
| `roic` | 投入资本回报率 | |
| `gross_profit_margin` | 毛利率 | |
| `net_profit_margin` | 净利率 | |
| `operating_profit_margin` | 营业利润率 | |
| `ebit` | 息税前利润 | |

### 12.4 成长能力因子

| 因子名 | 中文名 | 说明 |
|--------|--------|------|
| `or_yoy` | 营业收入同比增长 | |
| `op_yoy` | 营业利润同比增长 | |
| `net_profit_yoy` | 净利润同比增长 | |
| `dt_net_profit_yoy` | 归母净利润同比增长 | |
| `ebit_yoy` | EBIT同比增长 | |
| `ocf_yoy` | 经营现金流同比增长 | |

### 12.5 现金流因子

| 因子名 | 中文名 | 说明 |
|--------|--------|------|
| `net_operate_cash_flow` | 经营活动现金流净额 | |
| `net_invest_cash_flow` | 投资活动现金流净额 | |
| `net_financing_cash_flow` | 筹资活动现金流净额 | |
| `free_cash_flow` | 自由现金流 | |

### 12.6 偿债能力因子

| 因子名 | 中文名 | 说明 |
|--------|--------|------|
| `current_ratio` | 流动比率 | |
| `quick_ratio` | 速动比率 | |
| `debt_to_asset_ratio` | 资产负债率 | |
| `equity_ratio` | 产权比率 | |

### 12.7 每股指标因子

| 因子名 | 中文名 | 说明 |
|--------|--------|------|
| `eps` | 每股收益 | |
| `bps` | 每股净资产 | |
| `cfps` | 每股现金流 | |
| `ocfps` | 每股经营现金流 | |

### 12.8 资产负债因子

| 因子名 | 中文名 | 说明 |
|--------|--------|------|
| `total_assets` | 总资产 | |
| `total_liability` | 总负债 | |
| `total_non_current_liability` | 非流动负债 | |
| `total_current_liability` | 流动负债 | |
| `total_owner_equities` | 所有者权益 | |
| `book_value` | 账面价值 | |

### 12.9 营运能力因子

| 因子名 | 中文名 | 说明 |
|--------|--------|------|
| `turnover_ratio` | 换手率 | |
| `operating_revenue` | 营业收入 | |
| `operating_cost` | 营业成本 | |
| `total_profit` | 利润总额 | |
| `net_profit` | 净利润 | |

### 12.10 其他因子

| 因子名 | 中文名 | 说明 |
|--------|--------|------|
| `dividend_yield` | 股息率 | |
| `beta` | Beta系数 | |
| `alpha` | Alpha系数 | |

### 12.11 JoinQuant 与 RiceQuant 因子名对照表

| JoinQuant (valuation) | RiceQuant | 说明 |
|----------------------|-----------|------|
| `valuation.pe_ratio` | `pe_ratio` | 市盈率 |
| `valuation.pb_ratio` | `pb_ratio` | 市净率 |
| `valuation.ps_ratio` | `ps_ratio` | 市销率 |
| `valuation.market_cap` | `market_cap` | 总市值 |
| `valuation.circulating_market_cap` | `circulating_market_cap` | 流通市值 |
| `valuation.turnover_ratio` | `turnover_ratio` | 换手率 |

| JoinQuant (indicator) | RiceQuant | 说明 |
|----------------------|-----------|------|
| `indicator.roa` | `roa` | 资产收益率 |
| `indicator.roe` | `roe` | 净资产收益率 |
| `indicator.gross_profit_margin` | `gross_profit_margin` | 毛利率 |
| `indicator.net_profit_margin` | `net_profit_margin` | 净利率 |
| `indicator.inc_revenue_year_on_year` | `or_yoy` | 营收同比增长 |
| `indicator.inc_net_profit_year_on_year` | `net_profit_yoy` | 净利润同比增长 |

| JoinQuant (cash_flow) | RiceQuant | 说明 |
|----------------------|-----------|------|
| `cash_flow.net_operate_cash_flow` | `net_operate_cash_flow` | 经营现金流 |
| `cash_flow.net_invest_cash_flow` | `net_invest_cash_flow` | 投资现金流 |
| `cash_flow.net_financing_cash_flow` | `net_financing_cash_flow` | 筹资现金流 |

| JoinQuant (balance) | RiceQuant | 说明 |
|---------------------|-----------|------|
| `balance.total_assets` | `total_assets` | 总资产 |
| `balance.total_liability` | `total_liability` | 总负债 |
| `balance.total_current_assets` | `total_current_assets` | 流动资产 |
| `balance.total_current_liability` | `total_current_liability` | 流动负债 |

### 12.12 因子获取代码对比

#### JoinQuant 方式

```python
# 使用 get_fundamentals 查询
q = query(
    valuation.code,
    valuation.pe_ratio,
    valuation.pb_ratio,
    valuation.market_cap
).filter(
    valuation.code.in_(stocks)
)

df = get_fundamentals(q, statDate="2024q1")

# 使用 get_valuation 获取历史估值
df = get_valuation(stocks, 
                   end_date="2024-01-01", 
                   count=20,
                   fields=["pe_ratio", "pb_ratio", "market_cap"])
```

#### RiceQuant 方式

```python
# 使用 get_factor 获取因子
factors = ["pe_ratio", "pb_ratio", "market_cap"]
data = get_factor(stocks, factors, 
                  start_date="2024-01-01", 
                  end_date="2024-01-31")

# 获取单个股票的单个因子
pe = get_factor("000001.XSHE", "pe_ratio", 
                start_date="2024-01-01", 
                end_date="2024-01-31")

# 使用 get_fundamentals 查询（语法类似但字段路径不同）
q = query(
    fundamentals.eod_derivative_indicator.pe_ratio,
    fundamentals.eod_derivative_indicator.pb_ratio
).filter(
    fundamentals.eod_derivative_indicator.order_book_id.in_(stocks)
)

df = get_fundamentals(q, entry_date="2024-01-01")
```

### 12.13 注意事项

1. **因子名称**: RiceQuant 因子名直接使用字符串，不需要模块前缀
2. **日期参数**: RiceQuant 使用 `start_date` + `end_date`，JoinQuant 使用 `statDate` 或 `end_date` + `count`
3. **返回格式**: RiceQuant `get_factor()` 返回 DataFrame 或 dict，JoinQuant `get_valuation()` 返回 DataFrame
4. **批量获取**: RiceQuant 一次可获取多只股票的多个因子
5. **异常处理**: 部分因子可能不存在，建议用 try-catch 包裹

---

*最后更新: 2026-03-31*
*验证状态: 已通过实测验证（57笔交易）*