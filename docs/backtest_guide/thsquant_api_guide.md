# THSQuant (同花顺 SuperMind) 平台 API 指南

> 来源：https://quant.10jqka.com.cn/view/help/4
> 平台名称：SuperMind 量化交易平台
> 策略语言：Python（需 `from mindgo_api import *`）

---

## 一、策略框架函数

### 基本函数支持矩阵

| 函数 | 股票 | 股票日内 | 期货期权 | 股票期货 | 场外基金 |
|------|------|---------|---------|---------|---------|
| `init` | ✅ | ✅ | ✅ | ✅ | ✅ |
| `handle_bar` | ✅ | ✅ | ✅ | ✅ | ✅ |
| `handle_tick` | ✅ | ✅ | ❌ | ❌ | ❌ |
| `open_auction` | ✅ | ❌ | ❌ | ❌ | ❌ |
| `before_trading` | ✅ | ✅ | ✅ | ✅ | ✅ |
| `after_trading` | ✅ | ✅ | ✅ | ✅ | ✅ |
| `on_order` | ✅ | ❌ | ❌ | ❌ | ❌ |
| `on_trade` | ✅ | ❌ | ❌ | ❌ | ❌ |

### 核心框架函数

```python
from mindgo_api import *

def init(context):
    """初始化，全局只运行一次"""
    context.stock = '000001.SZ'
    set_benchmark('000300.SH')
    set_commission(PerShare(type='stock', cost=0.0002))
    set_slippage(PriceSlippage(0.002))

def before_trading(context):
    """开盘前半小时调用"""
    pass

def handle_bar(context, bar_dict):
    """每个交易频率调用"""
    order('000001.SZ', 100)

def after_trading(context):
    """收盘后半小时调用"""
    log.info(context.portfolio.pnl)

def on_order(context, odr):
    """委托状态更新回调（仅股票）"""
    log.info(odr)

def on_trade(context, trade):
    """成交回调（仅股票）"""
    log.info(trade)
```

---

## 二、定时运行函数

```python
# 每日定时
run_daily(func, time_rule='every_bar', hours=None, minutes=None)
# 示例：开盘后30分钟执行
run_daily(func=my_func, time_rule='after_open', hours=0, minutes=30)

# 每周定时
run_weekly(func, date_rule=1)  # date_rule: 1~5 或 -5~-1
# 示例：每周第一个交易日
run_weekly(func=my_func, date_rule=1)

# 每月定时
run_monthly(func, date_rule=5)  # date_rule: 1~23 或 -23~-1
# 示例：每月第5个交易日
run_monthly(func=my_func, date_rule=5)
```

---

## 三、初始化设置函数

```python
set_benchmark('000300.SH')          # 设置基准（默认沪深300）
set_slippage(PriceSlippage(0.002))  # 可变滑点2%
set_slippage(FixedSlippage(10))     # 固定滑点10元
set_commission(PerShare(type='stock', cost=0.0002, min_trade_cost=0.0))  # 万二手续费
set_volume_limit(daily=0.25, minute=0.5)  # 最大成交比例
set_trade_delay(delay_time=3)       # 延迟3个bar成交
set_execution('next_open')          # 撮合机制：close/next_open
set_log_level(level='warn')         # 日志级别
set_holding_stocks({'000001.SZ': 200})  # 初始持仓
enable_open_bar()                   # handle_bar在9:30执行
```

---

## 四、行情数据 API

### 策略内历史行情

```python
# 股票历史行情（策略内）
history(
    symbol_list,    # str 或 list
    fields,         # ['open','high','low','close','volume','turnover']
    bar_count,      # 历史长度
    fre_step,       # '1d' / '1m' / '5m' 等
    skip_paused=False,
    fq='pre',       # 'pre'前复权 / 'post'后复权 / None不复权
    df=True,
    is_panel=False
)

# 示例
values = history('000001.SZ', ['close'], 20, '1d', False, 'pre')

# 当前bar行情
bar = get_current(['000001.SZ'])  # 返回 dict，value 为 Bar 对象
```

### 研究环境历史行情

```python
# 通用行情（研究环境 + 策略内）
get_price(
    securities,     # str 或 list
    start_date,     # None 或 'YYYYMMDD'
    end_date,       # 'YYYYMMDD'
    fre_step,       # '1d' / '1m' / '5m' / '30m' 等
    fields,         # ['open','high','low','close','volume','turnover']
    skip_paused=False,
    fq='pre',
    bar_count=0,    # start_date=None 时必须为正整数
    is_panel=False
)

# 示例：获取最近3天收盘价
data = get_price('000001.SZ', None, '20240101', '1d', ['close'], bar_count=3)

# 蜡烛图（支持周/月/年）
get_candle_stick(securities, end_date, fre_step='month', fields=None, bar_count=5)

# 实时快照
get_last_tick(securities, fields)
get_tick(securities, start_date, end_date, fields)

# 集合竞价
get_call_auction(symbol, dt)

# 融资融券
get_mtss(security_list, start_date, end_date, fields, count=None)

# 资金流向
get_money_flow_step(security_list, start_date, end_date, fre_step='1d', fields, count=None)

# 压力支撑位
get_resistance_support(symbol_list, start_date, end_date, fre_step='1d', fields)

# 基金净值
get_extras(security_list, start_date, end_date, fields)  # unit_net_value / acc_net_value

# 涨跌区间统计
get_stats(date=None)  # 返回21个区间的个股数量
```

---

## 五、证券信息 API

```python
# 单只证券基本信息
get_security_info('000001.SZ')  # 返回 Instrument 对象

# 所有证券列表
get_all_securities(ty='stock', date='20240101')
# ty: 'stock'/'etf'/'futures'/'option'/'cbond'/'index'/'ota' 等

# 指数成分股
get_index_stocks('000300.SH', date='20240101')
get_index_weight('000300.SH', date='20240101')  # 带权重

# 行业成分股
get_industry_stocks('CI311000', date='20240101')  # 中信行业代码
get_symbol_industry('300033.SZ', date='20240101')  # 个股行业分类

# 概念成分股
get_concept_stocks('886031.TI', date='20240101')
get_concept_relate(date='20240101')  # 所有概念信息

# 交易日
get_trade_days(start_date='20240101', end_date='20241231')
get_all_trade_days()

# 期货
get_futures_info('RB', date='20240101')
get_futures_dominate('RB', date='20240101')  # 主力合约
get_future_code('RB', date='20240101')       # 所有可交易合约
get_option_code(date='20240101')             # 期权合约列表

# 行业分类
get_industry_relate(date='20240101', types='ci_industryid2')
get_index_list('TI', date='20240101')  # 按后缀查指数
```

---

## 六、财务数据 API

```python
# 财务数据（用 get_fundamentals）
data = get_fundamentals(
    query(
        valuation.symbol,
        valuation.market_cap,
        valuation.pe_ratio,
        valuation.pb_ratio
    ).filter(
        valuation.market_cap > 1e10
    ).order_by(
        valuation.market_cap.desc()
    ),
    date='20240101'
)

# 支持的财务表
# valuation    - 估值指标（pe_ratio, pb_ratio, market_cap, ps_ratio 等）
# balance      - 资产负债表
# cashflow     - 现金流量表
# income       - 利润表
# operating    - 运营能力表
# debtrepay    - 偿还能力表
# profit       - 盈利能力表
# growth       - 成长能力表
# profit_forecast - 业绩预告
# income_sq    - 利润表（单季度）
# profit_sq    - 盈利能力表（单季度）

# 非财务表（用 run_query）
data = run_query(query(concept_classification).limit(100))
```

---

## 七、交易函数

### 股票交易

```python
order('000001.SZ', 100)                    # 按数量（负数卖出）
order_value('000001.SZ', 100000)           # 按金额
order_percent('000001.SZ', 0.1)            # 按总资产比例
order_target('000001.SZ', 1000)            # 目标持仓数量
order_target_value('000001.SZ', 100000)    # 目标持仓金额
order_target_percent('000001.SZ', 0.1)     # 目标持仓比例

# 查询
get_orders(order_id=None, order_book_id=None)
get_open_orders()
get_tradelogs()
cancel_order(order)
cancel_order_all()
```

### 期货交易

```python
order_future(symbol, amount, offset_flag, order_type, limit_price=None)
# offset_flag: 'open'/'close'
# order_type: 'long'/'short'
order_close_today(symbol, amount, order_type)
```

### 期权交易

```python
order_option(order_book_id, amount, side, position_effect, price=None)
# side: 'buy'/'sell'
# position_effect: 'open'/'close'
```

---

## 八、账户信息对象

```python
# context.portfolio
context.portfolio.available_cash      # 可用现金
context.portfolio.market_value        # 持仓总市值
context.portfolio.portfolio_value     # 总资产
context.portfolio.pnl                 # 累计盈亏
context.portfolio.returns             # 收益率
context.portfolio.positions           # 持仓（dict，key=股票代码）

# 股票持仓
pos = context.portfolio.positions['000001.SZ']
pos.amount          # 持仓数量
pos.available_amount # 可用数量
pos.cost_basis      # 持仓成本
pos.market_value    # 持仓市值
pos.pnl             # 盈亏
pos.profit_rate     # 收益率
pos.position_days   # 持仓天数

# 策略运行信息
context.run_info.start_date
context.run_info.end_date
context.run_info.frequency
context.run_info.stock_starting_cash
context.run_info.benchmark
```

---

## 九、因子数据 API

```python
# 获取处理后的因子数据（去极值、标准化）
get_sfactor_data(
    start_date='20240101',
    end_date='20240131',
    stocks=['600519.SH', '300033.SZ'],
    factor_names=['macd', 'pe_ratio', 'pb_ratio']
)
# 返回 dict，key=因子名，value=DataFrame（index=股票，columns=日期）
```

---

## 十、问财接口

```python
# 研究环境（实时）
query_iwencai("市值>1000亿，日成交额>30亿，换手率大于4.5%")

# 回测环境（历史）
def init(context):
    get_iwencai('非ST，市值大于100亿')  # 结果存入 context.iwencai_securities

def handle_bar(context, bar_dict):
    stocks = context.iwencai_securities  # 前一日选股结果

# 研究环境历史问财
get_iwencai = get_open_api('public').get_iwencai
result = get_iwencai('净利润增长大于20%', '20230701', '20230801')
```

---

## 十一、辅助函数

```python
# 日志
log.info('信息')
log.warn('警告')
log.error('错误，会终止回测')

# 画图
record(MA5=ma5, MA10=ma10)

# 代码格式转换
normalize_symbol('300033')  # → '300033.SZ'

# 文件操作（研究环境）
write_file('log.txt', 'content')
read_file('log.txt')
list_file('')
copy_file('src.txt', 'dst.txt')
remove_file('file.txt')

# 消息推送
notify_push('策略报错', channel='wxpusher', uids='XXXXXX')
notify_push('策略报错', channel='webhook', url='XXXXXX',
            payload={"msgtype": "text", "text": {"content": "$content"}})

# 自选板块
custom_sector('板块1', 'insert', ['000001.SZ'])
custom_sector('板块1', 'query')

# 性能分析
enable_profile()  # 在策略框架函数之外调用
```

---

## 十二、与 JoinQuant 的 API 对比

| 功能 | JoinQuant | THSQuant (SuperMind) |
|------|-----------|---------------------|
| 历史行情 | `get_price()` | `get_price()` ✅ 相同 |
| 策略内行情 | `history()` | `history()` ✅ 相同 |
| 所有股票 | `get_all_securities('stock')` | `get_all_securities('stock')` ✅ 相同 |
| 指数成分股 | `get_index_stocks('000300.XSHG')` | `get_index_stocks('000300.SH')` ⚠️ 后缀不同 |
| 财务数据 | `get_fundamentals(query(...))` | `get_fundamentals(query(...))` ✅ 相同 |
| 交易日 | `get_trade_days()` | `get_trade_days()` ✅ 相同 |
| 下单 | `order()` / `order_target_percent()` | `order()` / `order_target_percent()` ✅ 相同 |
| 日志 | `log.info()` | `log.info()` ✅ 相同 |
| 问财 | `get_iwencai()` | `get_iwencai()` ✅ 相同 |
| 行业分类 | `get_industry_stocks()` | `get_industry_stocks()` ✅ 相同 |
| 融资融券 | `get_mtss()` | `get_mtss()` ✅ 相同 |
| 资金流向 | ❌ 无 | `get_money_flow_step()` ✅ THSQuant 独有 |
| 压力支撑位 | ❌ 无 | `get_resistance_support()` ✅ THSQuant 独有 |
| 实时快照 | `get_current_data()` | `get_last_tick()` ⚠️ 函数名不同 |
| 股票代码格式 | `000300.XSHG` | `000300.SH` ⚠️ 后缀不同 |
| 初始化 | `initialize(context)` | `init(context)` ⚠️ 函数名不同 |

### 代码迁移注意事项

```python
# JoinQuant → THSQuant 主要改动

# 1. 函数名
# JQ: def initialize(context):
# THS: def init(context):

# 2. 股票代码后缀
# JQ: '000300.XSHG', '000001.XSHE'
# THS: '000300.SH', '000001.SZ'

# 3. 实时行情
# JQ: current_data = get_current_data(); current_data['000001.XSHE'].close
# THS: bar = get_current(['000001.SZ']); bar['000001.SZ'].close

# 4. 必须导入
# THS: from mindgo_api import *  (JQ 不需要)
```

---

## 十三、策略模板

```python
from mindgo_api import *

def init(context):
    set_benchmark('000300.SH')
    set_commission(PerShare(type='stock', cost=0.0002, min_trade_cost=0.0))
    set_slippage(PriceSlippage(0.002))
    set_volume_limit(0.25, 0.5)
    
    # 月频调仓
    run_monthly(func=rebalance, date_rule=1)

def rebalance(context, bar_dict):
    # 选股
    stocks = get_index_stocks('000300.SH')
    
    # 获取财务数据
    data = get_fundamentals(
        query(valuation.symbol, valuation.pb_ratio)
        .filter(valuation.symbol.in_(stocks), valuation.pb_ratio < 2)
        .order_by(valuation.pb_ratio.asc())
        .limit(20),
        date=get_datetime().strftime('%Y%m%d')
    )
    
    selected = data['valuation_symbol'].tolist()
    
    # 调仓
    for stock in context.portfolio.positions:
        if stock not in selected:
            order_target_percent(stock, 0)
    
    weight = 1.0 / len(selected) if selected else 0
    for stock in selected:
        order_target_percent(stock, weight)

def handle_bar(context, bar_dict):
    pass
```
