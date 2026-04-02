# RiceQuant 回测框架修复记录

## 问题排查时间线

### 1. 初始问题：`get_factor()` 参数错误

**错误信息**:
```
get_factor() got an unexpected keyword argument 'start_date'
```

**原因**: RiceQuant 的 `get_factor()` 不接受 `start_date`/`end_date` 关键字参数

**解决**: 省略日期参数，返回当前日期数据
```python
# 错误
get_factor(stocks, factors, start_date=date, end_date=date)

# 正确
get_factor(stocks, factors)
```

---

### 2. 因子名称错误

**错误信息**:
```
get_factor(['roa']): None
```

**原因**: RiceQuant 使用完整因子名称

**解决**: 使用正确的因子名称
```python
# 错误
get_factor(stocks, ["roa", "roe"])

# 正确
get_factor(stocks, ["return_on_asset", "return_on_equity"])
```

**可用因子**:
- `return_on_asset` (ROA)
- `return_on_equity` (ROE)
- `pb_ratio` (市净率)
- `pe_ratio` (市盈率)
- `market_cap` (市值)

---

### 3. `bar_dict` 无个股数据

**错误现象**: `bar_dict[stock]` 返回 `NOT FOUND`

**原因**: RiceQuant 不预加载个股数据到 `bar_dict`

**解决**: 使用 `history_bars()` 获取数据
```python
# 错误
if stock in bar_dict:
    close = bar_dict[stock].close

# 正确
hist = history_bars(stock, 1, "1d", "close")
if hist is not None and len(hist) > 0:
    close = hist[-1]
```

---

### 4. `portfolio.available_cash` 不存在

**错误信息**:
```
'Portfolio' object has no attribute 'available_cash'
```

**解决**: 使用 `portfolio.cash`
```python
# 错误
cash = context.portfolio.available_cash

# 正确
cash = context.portfolio.cash
```

---

### 5. 策略运行超时

**问题**: 18 个月回测运行超过 10 分钟

**原因**: 循环中单独调用 `instruments()` 和 `history_bars()`

**解决**: 预加载数据，批量处理
```python
# 错误：循环中单独调用
for stock in stocks:
    inst = instruments(stock)
    hist = history_bars(stock, 1, "1d", "close")

# 正确：预加载
all_inst = all_instruments(type="CS")
inst_dict = {row["order_book_id"]: row for _, row in all_inst.iterrows()}

for stock in stocks:
    if stock in inst_dict:
        symbol = inst_dict[stock].get("symbol", "")
```

**优化效果**: 回测时间从 >10分钟 降至 ~1分钟

---

## RiceQuant API 端点

### 回测相关

```
POST /api/strategy/v1/workspaces/{id}/strategies     # 创建策略
POST /api/backtest/v1/workspaces/{id}/backtests      # 运行回测
GET  /api/backtest/v1/workspaces/{id}/backtests/{btId}  # 获取状态
GET  /api/backtest/v1/workspaces/{id}/backtests/{btId}/risk  # 风险指标
GET  /api/backtest/v1/workspaces/{id}/backtests/{btId}/portfolios  # 收益数据
GET  /api/backtest/v1/workspaces/{id}/backtests/{btId}/trades  # 交易记录
GET  /api/backtest/v1/workspaces/{id}/backtests/{btId}/logs  # 日志
DELETE /api/strategy/v1/workspaces/{id}/strategies/{sid}  # 删除策略
```

### 获取收益率

收益率数据在 `/portfolios` 端点，不在 `/risk` 端点：

```javascript
const portfolios = await client.request(
  `/api/backtest/v1/workspaces/${workspaceId}/backtests/${backtestId}/portfolios`
);

// 最后一条记录包含总收益
const lastPortfolio = portfolios.portfolios[portfolios.portfolios.length - 1];
const totalReturn = lastPortfolio.total_returns;
const annualReturn = lastPortfolio.annualized_returns;
```

---

## 策略代码模板

### 基础结构

```python
def init(context):
    context.benchmark = "000300.XSHG"
    context.hold_num = 20
    scheduler.run_monthly(rebalance, monthday=1)


def rebalance(context, bar_dict):
    context.bar_dict = bar_dict
    
    # 获取股票池
    stocks = get_universe(context)
    
    # 获取因子
    factor_data = get_factor(stocks, ["return_on_asset", "return_on_equity", "pb_ratio"])
    
    # 选股
    selected = choose_stocks(stocks, factor_data)
    
    # 交易
    for stock in selected:
        hist = history_bars(stock, 1, "1d", "close")
        if hist is not None and len(hist) > 0:
            order_target_value(stock, target_value)


def get_universe(context):
    hs300 = index_components("000300.XSHG")
    zz500 = index_components("000905.XSHG")
    stocks = list(set(hs300) | set(zz500))
    return [s for s in stocks if not s.startswith("688")]


def after_trading(context):
    pass
```

---

## 测试验证

### API 测试策略

创建简单策略验证 API 是否工作：

```python
def init(context):
    scheduler.run_monthly(test_api, monthday=1)


def test_api(context, bar_dict):
    stocks = index_components("000300.XSHG")[:5]
    
    # 测试 get_factor
    data = get_factor(stocks, ["return_on_asset", "pb_ratio"])
    logger.info(f"get_factor: {data}")
    
    # 测试 history_bars
    hist = history_bars(stocks[0], 5, "1d", "close")
    logger.info(f"history_bars: {hist}")
```

---

## 常见错误速查表

| 错误信息 | 原因 | 解决方案 |
|----------|------|----------|
| `got an unexpected keyword argument 'start_date'` | `get_factor()` 不接受日期参数 | 省略日期参数 |
| `name 'roa' is not defined` | 因子名称错误 | 使用 `return_on_asset` |
| `bar_dict[stock]: NOT FOUND` | bar_dict 无个股数据 | 使用 `history_bars()` |
| `'Portfolio' object has no attribute 'available_cash'` | 属性名错误 | 使用 `portfolio.cash` |
| `order_book_ids: at least one valid instrument expected` | 股票列表为空 | 检查股票池获取逻辑 |
| 回测超时 | 循环调用 API | 预加载数据批量处理 |

---

**文档更新时间**: 2026-04-01