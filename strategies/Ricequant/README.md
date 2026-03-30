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

## RiceQuant 支持的财务因子

| 因子名 | 说明 |
|--------|------|
| `roa` | 总资产收益率 |
| `roe` | 净资产收益率 |
| `net_operate_cash_flow` | 经营活动现金流量净额 |
| `total_assets` | 资产总计 |
| `total_liability` | 负债合计 |
| `total_non_current_liability` | 非流动负债合计 |
| `gross_profit_margin` | 销售毛利率 |
| `operating_revenue` | 营业收入 |
| `pb_ratio` | 市净率 |
| `pe_ratio` | 市盈率 |

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