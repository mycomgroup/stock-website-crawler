# 策略编辑器回测系统使用指南

> 更新时间：2026-03-31
> 验证状态：已通过实测验证

## 一、概述

策略编辑器回测是量化平台的标准回测方式，与 Notebook 回测各有优劣。

### Notebook vs 策略编辑器对比

| 特性 | Notebook 回测 | 策略编辑器回测 |
|------|--------------|---------------|
| **时间限制** | 无限制 | 180分钟/天 |
| **回测精度** | 手动实现循环 | 自动精确回测 |
| **数据 API** | 完整 | 完整 |
| **因子 API** | 完整 | 完整 |
| **实时数据** | 不支持 | 支持（bar_dict） |
| **逐步调试** | 支持 | 不支持 |
| **交易记录** | 需手动记录 | 自动生成 |
| **风险指标** | 需手动计算 | 自动计算 |
| **适用场景** | 快速验证逻辑 | 精确回测、实盘前验证 |

### 推荐流程

```
1. Notebook 回测 → 快速验证策略逻辑（无时间限制）
2. Notebook 回测 → 参数调优和敏感度分析
3. 策略编辑器回测 → 精确回测，验证交易细节
4. 策略编辑器回测 → 最终回测，准备实盘
```

## 二、平台选择

### RiceQuant 策略编辑器

**Skill 目录：** `skills/ricequant_strategy`

**特点：**
- Session 自动管理（无需手动抓取）
- 支持 `get_factor()` 获取财务因子
- 回测结果自动计算风险指标
- 支持 headless 模式（无浏览器界面）

**适用场景：**
- 因子简单的策略（PE/PB/ROA/ROE/市值等）
- 需要精确回测的 JoinQuant 迁移策略
- 需要自动计算风险指标

**运行命令：**
```bash
cd skills/ricequant_strategy

# 运行回测
node run-skill.js --id <策略ID> --file <策略文件> --start 2024-01-01 --end 2024-12-31

# 示例
node run-skill.js --id 2415370 --file ../../strategies/Ricequant/rfscore7_pb10_final_v2.py --start 2024-01-01 --end 2024-06-30
```

### JoinQuant 策略编辑器

**Skill 目录：** `skills/joinquant_strategy`（待完善）

**特点：**
- 需要手动管理 Session
- 支持 jqfactor 特殊因子
- 回测框架成熟

**适用场景：**
- 依赖 jqfactor 特殊因子的策略
- 需要 JoinQuant 特色数据
- 已有 JoinQuant 策略，无需迁移

## 三、RiceQuant 策略编辑器详细指南

### 3.1 初始化配置

**配置 .env 文件：**
```bash
# skills/ricequant_strategy/.env
RICEQUANT_USERNAME=你的账号
RICEQUANT_PASSWORD=你的密码
```

**Session 管理：**
- Session 自动管理，无需手动抓取
- Session 有效期 7 天
- 过期时自动 headless 登录
- Session 文件：`data/session.json`

### 3.2 策略格式要求

**RiceQuant 策略编辑器格式：**
```python
def init(context):
    context.benchmark = "000300.XSHG"
    context.hold_num = 10
    scheduler.run_monthly(rebalance, monthday=1)

def handle_bar(context, bar_dict):
    # 每日执行
    pass

def rebalance(context, bar_dict):
    # 调仓逻辑
    stocks = get_universe(context, bar_dict)
    
    # 买入
    for stock in stocks:
        order_target_value(stock, 10000)
```

**注意：**
- ❌ 不能在 `init()` 中下单
- ❌ 不能使用 `scheduler.run_monthly` 在首月触发（建议用 `handle_bar` 手动判断）
- ✅ 使用 `context.xxx` 存储全局变量
- ✅ 使用 `bar_dict[stock]` 获取实时数据

### 3.3 运行回测

**基本命令：**
```bash
node run-skill.js --id <策略ID> --file <策略文件> [选项]
```

**参数说明：**
| 参数 | 说明 | 默认值 |
|------|------|--------|
| `--id` | 策略ID（必需） | - |
| `--file` | 策略文件路径（必需） | - |
| `--start` | 开始日期 | 2021-01-01 |
| `--end` | 结束日期 | 2025-03-28 |
| `--capital` | 初始资金 | 100000 |
| `--freq` | 频率（day/minute） | day |
| `--benchmark` | 基准指数 | 000300.XSHG |

**示例：**
```bash
# 基本回测
node run-skill.js --id 2415370 --file my_strategy.py --start 2024-01-01 --end 2024-12-31

# 指定参数
node run-skill.js --id 2415370 --file my_strategy.py \
  --start 2024-01-01 --end 2024-06-30 \
  --capital 500000 --benchmark 000905.XSHG
```

### 3.4 查看回测结果

**结果文件：**
```bash
# 查看最新回测结果
cat data/ricequant-backtest-*.json

# 查看所有回测
ls -lht data/ricequant-backtest-*.json
```

**结果包含：**
- 回测状态（status）
- 风险指标（risk）
  - 最大回撤（max_drawdown）
  - 夏普比率（sharpe）
  - Alpha、Beta
  - 年化波动率（annual_volatility）

### 3.5 API 差异

**JoinQuant → RiceQuant 对照表：**

| JoinQuant | RiceQuant | 说明 |
|-----------|-----------|------|
| `initialize(context)` | `init(context)` | 初始化函数 |
| `handle_data(context, data)` | `handle_bar(context, bar_dict)` | 主循环函数 |
| `g.xxx` | `context.xxx` | 全局变量 |
| `get_current_data()` | `bar_dict` | 实时数据 |
| `current_data[stock].last_price` | `bar_dict[stock].close` | 最新价 |
| `current_data[stock].high_limit` | `bar_dict[stock].limit_up` | 涨停价 |
| `get_price()` | `history_bars()` | 历史数据 |
| `get_all_securities("stock")` | `all_instruments("CS")` | 所有股票 |
| `get_index_stocks()` | `index_components()` | 指数成分股 |
| `order(stock, amount)` | `order_shares(stock, amount)` | 下单 |
| `order_target(stock, 0)` | `order_target_value(stock, 0)` | 清仓 |

**详细迁移指南：**
- `joinquant_to_ricequant_migration_guide.md` - 完整迁移指南
- `ricequant_factor_list.md` - 因子列表速查
- `strategies/Ricequant/README.md` - API 对照表

## 四、常见问题

### Q1: Session 过期怎么办？

**RiceQuant：** 自动处理，无需手动干预。

系统会自动检测 session 是否过期，过期时自动 headless 登录。

### Q2: 策略没有交易记录？

**可能原因：**
1. `scheduler.run_monthly` 未触发（建议用 `handle_bar` 手动判断月份）
2. 选股条件太严格，没有符合的股票
3. 所有股票都涨停/跌停/停牌

**解决方案：**
```python
def init(context):
    context.last_rebalance_month = -1  # 关键：用 -1 而非 None

def handle_bar(context, bar_dict):
    today = context.now
    
    # 每月第一个交易日调仓
    if context.last_rebalance_month != today.month:
        context.last_rebalance_month = today.month
        rebalance(context, bar_dict)
```

### Q3: 如何获取财务因子？

**使用 `get_factor()`：**
```python
# 获取单个因子
pe_data = get_factor(stocks, "pe_ratio", start_date=date, end_date=date)

# 获取多个因子
factors = ["pe_ratio", "pb_ratio", "roa", "roe"]
data = get_factor(stocks, factors, start_date=date, end_date=date)
```

**支持的因子：**
- 估值类：`pe_ratio`, `pb_ratio`, `ps_ratio`, `market_cap`
- 盈利类：`roa`, `roe`, `gross_profit_margin`, `net_profit_margin`
- 成长类：`or_yoy`, `net_profit_yoy`
- 现金流：`net_operate_cash_flow`, `free_cash_flow`
- 完整列表：`ricequant_factor_list.md`

### Q4: 如何计算涨停价？

**方法1：从历史数据获取**
```python
bars = history_bars(stock, 1, "1d", "limit_up")
high_limit = bars[-1]['limit_up'] if bars is not None else None
```

**方法2：手动计算**
```python
def get_limit_price(stock):
    bars = history_bars(stock, 1, "1d", "close")
    if bars is None:
        return None, None
    
    pre_close = bars[-1]
    inst = instruments(stock)
    
    # 判断涨跌停幅度
    if "ST" in inst.symbol:
        limit_pct = 0.05
    elif stock.startswith("688") or stock.startswith("30"):
        limit_pct = 0.20
    else:
        limit_pct = 0.10
    
    high_limit = round(pre_close * (1 + limit_pct), 2)
    low_limit = round(pre_close * (1 - limit_pct), 2)
    
    return high_limit, low_limit
```

### Q5: 代码保存后显示 base64？

**原因：** 早期版本的 bug，已修复。

**解决方案：** 确保使用最新版本的 `ricequant-client.js`，代码会直接保存为原始 Python，不再 base64 编码。

## 五、最佳实践

### 5.1 Session 管理

- RiceQuant Session 自动管理
- 有效期 7 天
- 过期时自动 headless 登录（无界面）
- Session 文件：`data/session.json`

### 5.2 策略代码结构

```python
def init(context):
    # 初始化全局变量
    context.xxx = value
    context.last_rebalance_month = -1  # 用 -1 而非 None

def handle_bar(context, bar_dict):
    # 每日检查是否需要调仓
    today = context.now
    
    if context.last_rebalance_month != today.month:
        context.last_rebalance_month = today.month
        rebalance(context, bar_dict)

def rebalance(context, bar_dict):
    # 调仓逻辑
    logger.info(f"Rebalance on {today.date()}")
    
    # 选股
    stocks = select_stocks(context, bar_dict)
    
    # 清仓
    for stock in list(context.portfolio.positions.keys()):
        if stock not in stocks:
            order_target_value(stock, 0)
    
    # 买入
    if stocks:
        value_each = context.portfolio.total_value / len(stocks)
        for stock in stocks:
            order_target_value(stock, value_each)
```

### 5.3 错误处理

```python
def rebalance(context, bar_dict):
    try:
        stocks = get_universe(context, bar_dict)
        if not stocks:
            logger.warning("No stocks selected")
            return
        
        # 交易逻辑
        for stock in stocks:
            if stock not in bar_dict:
                logger.warning(f"{stock} not in bar_dict")
                continue
            
            bar = bar_dict[stock]
            if not bar.is_trading:
                logger.warning(f"{stock} not trading")
                continue
            
            order_target_value(stock, value)
            logger.info(f"Bought {stock}")
            
    except Exception as e:
        logger.error(f"Rebalance error: {e}")
        import traceback
        traceback.print_exc()
```

## 六、相关文档

### 本目录文档

- `README.md` - Notebook 回测系统指南
- `PROMPT.md` - Agent 运行提示词
- `API_DIFF.md` - API 差异对比
- `MIGRATION.md` - 迁移指南

### 迁移指南

- `joinquant_to_ricequant_migration_guide.md` - JoinQuant → RiceQuant 完整迁移指南
- `ricequant_factor_list.md` - RiceQuant 因子列表速查
- `strategies/Ricequant/README.md` - API 对照表

### Skill 目录文档

**RiceQuant：**
- `skills/ricequant_strategy/README.md` - 详细使用指南
- `skills/ricequant_strategy/QUICK_REFERENCE.md` - 快速参考
- `skills/ricequant_strategy/SESSION_MANAGEMENT.md` - Session 管理

**JoinQuant：**
- `skills/joinquant_notebook/README.md` - Notebook 使用指南

## 七、总结

### 使用建议

| 场景 | 推荐方式 |
|------|---------|
| **快速验证策略逻辑** | Notebook 回测 |
| **参数调优** | Notebook 回测 |
| **精确回测** | 策略编辑器回测 |
| **实盘前验证** | 策略编辑器回测 |
| **JoinQuant 迁移策略** | RiceQuant 策略编辑器 |

### 核心改进

- RiceQuant Session 自动管理
- 代码保存使用原始 Python（非 base64）
- 回测结果自动计算风险指标
- 支持 headless 模式（无浏览器界面）

---

*最后更新: 2026-03-31*
*验证状态: 已通过实测验证*