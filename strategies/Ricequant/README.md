# RiceQuant 策略迁移说明

## API 对照表

| JoinQuant | RiceQuant | 说明 |
|-----------|-----------|------|
| `from jqdata import *` | 无需导入 | RiceQuant 自动导入 |
| `from jqfactor import Factor, calc_factors` | `get_factor()` | RiceQuant 用 get_factor 获取因子 |
| `initialize(context)` | `init(context)` | 入口函数名不同 |
| `set_benchmark("000300.XSHG")` | `context.benchmark = "000300.XSHG"` | 在 init 中设置 |
| `set_order_cost(OrderCost(...), type="stock")` | `set_commission(PerTrade(...))` | 手续费设置方式不同 |
| `run_monthly(func, 1, time="9:35")` | `scheduler.run_monthly(func, tradingday=1)` | 定时任务 API |
| `run_daily(func, time="14:50")` | `scheduler.run_daily(func)` | 无 time 参数 |
| `get_index_stocks("000300.XSHG")` | `index_components("000300.XSHG")` | 指数成分股 |
| `get_all_securities(types=["stock"])` | `all_instruments(type="CS")` | 全部股票 |
| `get_extras("is_st", stocks)` | `instruments(stock).symbol` 检查 ST | ST 状态获取方式不同 |
| `get_price(stocks, count=20, fields="close")` | `history_bars(stock, 20, "1d", "close")` | 历史价格 |
| `get_valuation(stocks, fields=["pb_ratio"])` | `get_factor(stocks, "pb_ratio")` | 估值因子 |
| `get_current_data()` | `context.bar_dict` 或 `bar_dict` | 当前数据通过参数传入 |
| `current_data[stock].paused` | `bar_dict[stock].is_trading` | 停牌检查 |
| `current_data[stock].last_price` | `bar_dict[stock].close` | 最新价格 |
| `current_data[stock].high_limit` | `bar_dict[stock].limit_up` | 涨停价 |
| `order_target_value(stock, value)` | `order_target_value(stock, value)` | 相同 |
| `order_target(stock, amount)` | `order_target(stock, amount)` | 相同 |
| `record(breadth=value)` | `plot("breadth", value)` | 记录指标 |
| `log.set_level("order", "error")` | 无直接对应 | RiceQuant 日志级别不同 |
| `g.xxx` | `context.xxx` | 全局变量使用 context |

## 因子计算差异

### JoinQuant (jqfactor)
```python
from jqfactor import Factor, calc_factors

class RFScore(Factor):
    name = "RFScore"
    max_window = 1
    dependencies = ["roa", "net_operate_cash_flow", ...]

    def calc(self, data):
        # 自定义计算逻辑
        return self.fscore

calc_factors(stocks, [factor], start_date, end_date)
```

### RiceQuant (get_factor)
```python
# RiceQuant 没有自定义 Factor 类
# 使用 get_factor 获取基础因子, 手动计算组合因子

factor_names = ["roa", "net_operate_cash_flow", "total_assets"]
data = get_factor(stocks, factor_names, start_date, end_date)

# 手动计算 RFScore
df["RFScore"] = (data["roa"] > 0).astype(int) + ...
```

## RiceQuant get_factor() 完整因子列表

### 估值类因子

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

### 盈利能力因子

| 因子名 | 中文名 | 说明 |
|--------|--------|------|
| `roa` | 资产收益率 | 净利润/总资产 |
| `roe` | 净资产收益率 | 净利润/净资产 |
| `roic` | 投入资本回报率 | |
| `gross_profit_margin` | 毛利率 | |
| `net_profit_margin` | 净利率 | |
| `operating_profit_margin` | 营业利润率 | |
| `ebit` | 息税前利润 | |

### 成长能力因子

| 因子名 | 中文名 | 说明 |
|--------|--------|------|
| `or_yoy` | 营业收入同比增长 | |
| `op_yoy` | 营业利润同比增长 | |
| `net_profit_yoy` | 净利润同比增长 | |
| `dt_net_profit_yoy` | 归母净利润同比增长 | |
| `ebit_yoy` | EBIT同比增长 | |
| `ocf_yoy` | 经营现金流同比增长 | |

### 现金流因子

| 因子名 | 中文名 | 说明 |
|--------|--------|------|
| `net_operate_cash_flow` | 经营活动现金流净额 | |
| `net_invest_cash_flow` | 投资活动现金流净额 | |
| `net_financing_cash_flow` | 筹资活动现金流净额 | |
| `free_cash_flow` | 自由现金流 | |

### 偿债能力因子

| 因子名 | 中文名 | 说明 |
|--------|--------|------|
| `current_ratio` | 流动比率 | |
| `quick_ratio` | 速动比率 | |
| `debt_to_asset_ratio` | 资产负债率 | |
| `equity_ratio` | 产权比率 | |

### 每股指标因子

| 因子名 | 中文名 | 说明 |
|--------|--------|------|
| `eps` | 每股收益 | |
| `bps` | 每股净资产 | |
| `cfps` | 每股现金流 | |
| `ocfps` | 每股经营现金流 | |

### 资产负债因子

| 因子名 | 中文名 | 说明 |
|--------|--------|------|
| `total_assets` | 总资产 | |
| `total_liability` | 总负债 | |
| `total_non_current_liability` | 非流动负债 | |
| `total_current_liability` | 流动负债 | |
| `total_owner_equities` | 所有者权益 | |
| `book_value` | 账面价值 | |

### 营运能力因子

| 因子名 | 中文名 | 说明 |
|--------|--------|------|
| `turnover_ratio` | 换手率 | |
| `operating_revenue` | 营业收入 | |
| `operating_cost` | 营业成本 | |
| `total_profit` | 利润总额 | |
| `net_profit` | 净利润 | |

### 其他因子

| 因子名 | 中文名 | 说明 |
|--------|--------|------|
| `dividend_yield` | 股息率 | |
| `beta` | Beta系数 | |
| `alpha` | Alpha系数 | |

## JoinQuant 与 RiceQuant 因子名对照表

### valuation 模块对照

| JoinQuant | RiceQuant | 说明 |
|-----------|-----------|------|
| `valuation.pe_ratio` | `pe_ratio` | 市盈率 |
| `valuation.pb_ratio` | `pb_ratio` | 市净率 |
| `valuation.ps_ratio` | `ps_ratio` | 市销率 |
| `valuation.market_cap` | `market_cap` | 总市值 |
| `valuation.circulating_market_cap` | `circulating_market_cap` | 流通市值 |
| `valuation.turnover_ratio` | `turnover_ratio` | 换手率 |

### indicator 模块对照

| JoinQuant | RiceQuant | 说明 |
|-----------|-----------|------|
| `indicator.roa` | `roa` | 资产收益率 |
| `indicator.roe` | `roe` | 净资产收益率 |
| `indicator.gross_profit_margin` | `gross_profit_margin` | 毛利率 |
| `indicator.net_profit_margin` | `net_profit_margin` | 净利率 |
| `indicator.inc_revenue_year_on_year` | `or_yoy` | 营收同比增长 |
| `indicator.inc_net_profit_year_on_year` | `net_profit_yoy` | 净利润同比增长 |

### cash_flow 模块对照

| JoinQuant | RiceQuant | 说明 |
|-----------|-----------|------|
| `cash_flow.net_operate_cash_flow` | `net_operate_cash_flow` | 经营现金流 |
| `cash_flow.net_invest_cash_flow` | `net_invest_cash_flow` | 投资现金流 |
| `cash_flow.net_financing_cash_flow` | `net_financing_cash_flow` | 筹资现金流 |

### balance 模块对照

| JoinQuant | RiceQuant | 说明 |
|-----------|-----------|------|
| `balance.total_assets` | `total_assets` | 总资产 |
| `balance.total_liability` | `total_liability` | 总负债 |
| `balance.total_current_assets` | `total_current_assets` | 流动资产 |
| `balance.total_current_liability` | `total_current_liability` | 流动负债 |

## 因子获取代码对比

### JoinQuant 方式

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

### RiceQuant 方式

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

## 调用方式差异

### JoinQuant
```python
def rebalance(context):
    watch_date = context.previous_date
    current_data = get_current_data()
    price = current_data[stock].last_price
```

### RiceQuant
```python
def rebalance(context, bar_dict):
    watch_date = context.now.date()
    context.bar_dict = bar_dict  # 保存供其他函数使用
    price = bar_dict[stock].close
```

## 策略验证

迁移后的策略位于: `rfscore7_pb10_final_v2.py`

可通过以下方式验证:
```bash
cd skills/ricequant_strategy
node run-skill.js --id <strategyId> --file ../strategies/Ricequant/rfscore7_pb10_final_v2.py
```

## 注意事项

1. **定时任务**: RiceQuant 的 scheduler 不支持 `time` 参数, 只能在开盘后执行
2. **因子数据**: RiceQuant 的 get_factor 可能部分因子不存在, 需要 try-catch
3. **bar_dict**: 必须通过函数参数传入, 不能像 JoinQuant 那样主动获取
4. **ST检查**: RiceQuant 通过 instruments(stock).symbol 字段检查 ST 状态
5. **因子名称**: RiceQuant 因子名直接使用字符串，不需要模块前缀
6. **日期参数**: RiceQuant 使用 `start_date` + `end_date`，JoinQuant 使用 `statDate` 或 `end_date` + `count`
7. **异常处理**: 部分因子可能不存在，建议用 try-catch 包裹

## 详细迁移指南

完整的迁移指南请参考: [skills/backtest_guide/reference/jq_to_rq_migration.md](../../skills/backtest_guide/reference/jq_to_rq_migration.md)