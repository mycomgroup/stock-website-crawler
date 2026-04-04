# RiceQuant（米筐）回测指南

目录：`skills/ricequant_strategy/`

---

## 环境配置

```bash
cd skills/ricequant_strategy
npm install
```

`.env` 需要：
```
RICEQUANT_USERNAME=your_username
RICEQUANT_PASSWORD=your_password
```

Session 自动管理，无需手动干预。

---

## 两种运行模式

### 模式 1：策略编辑器回测（精确回测）

适合：策略逻辑完整，需要完整风险指标（夏普、最大回撤等）。

```bash
# 先查看已有策略列表，获取 strategyId
node list-strategies.js

# 提交回测
node run-skill.js --id <strategyId> --file ./my_strategy.py \
  --start 2021-01-01 --end 2024-12-31

# 等待完成后自动输出摘要，完整报告保存在 output/
```

完整参数：

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `--id` | RiceQuant 策略 ID（必填） | - |
| `--file` | 本地策略文件路径（必填） | - |
| `--start` | 回测开始日期 | 2021-01-01 |
| `--end` | 回测结束日期 | 2025-03-28 |
| `--capital` | 初始资金 | 100000 |
| `--freq` | day / minute | day |
| `--benchmark` | 基准指数 | 000300.XSHG |
| `--no-wait` | 提交后不等待结果 | false |
| `--wait-if-full` | 并发满时等待 | false |
| `--max-running` | 最大并发数 | 3 |

### 模式 2：Notebook 运行（快速验证）

适合：验证选股逻辑、调试数据 API，无时间限制。

```bash
node run-strategy.js --strategy ./my_strategy.py --create-new
# 结果在 data/ricequant-notebook-result-*.json
```

---

## 查询回测结果

```bash
# 列出策略所有历史回测
node fetch-backtest-results.js --strategy-id <id> --list

# 最近一次完整结果
node fetch-backtest-results.js --strategy-id <id> --latest

# 指定 backtestId 查询
node fetch-backtest-results.js --backtest-id <id>

# 保存结果到文件
node fetch-backtest-results.js --strategy-id <id> --latest --save
```

---

## 策略代码格式（策略编辑器）

```python
def init(context):
    context.month_count = 0
    context.last_month = -1

def handle_bar(context, bar_dict):
    # 手动判断月份调仓（scheduler.run_monthly 可能不触发）
    current_month = context.now.month
    if current_month != context.last_month:
        context.last_month = current_month
        rebalance(context, bar_dict)

def rebalance(context, bar_dict):
    stocks = index_components('000300.XSHG')
    # 选股逻辑...
    order_target_percent(stock, 1.0 / len(selected))
```

关键注意事项：
- 不能在 `init()` 中下单
- `scheduler.run_monthly` 可能不触发，建议用 `handle_bar` 手动判断月份
- 全局变量用 `context.xxx` 存储
- 实时数据通过 `bar_dict[stock]` 获取

---

## 核心 API

```python
# 全市场股票
stocks = all_instruments("CS")

# 指数成分股
stocks = index_components('000300.XSHG', date=context.now)

# 历史价格
bars = history_bars(stock, 20, '1d', ['close', 'volume'])

# 因子数据
pe = get_factor(stocks, 'pe_ratio', start_date, end_date)

# 涨停价
limit_up = history_bars(stock, 1, '1d', 'limit_up')[0]

# 交易日
dates = get_trading_dates('2023-01-01', '2024-12-31')
```

---

## 文件结构

```
ricequant_strategy/
├── .env                              # 账号配置
├── run-skill.js                      # 策略编辑器回测入口
├── run-strategy.js                   # Notebook 运行入口
├── fetch-backtest-results.js         # 查询回测结果
├── fetch-report.js                   # 获取指定回测报告
├── list-strategies.js                # 列出所有策略
├── request/
│   ├── ricequant-client.js           # HTTP 客户端（含重试）
│   ├── strategy-runner.js            # 完整工作流
│   └── ricequant-notebook-client.js  # Notebook 客户端
├── browser/
│   └── session-manager.js            # Session 自动管理
└── output/                           # 回测结果输出
```

---

## 常见问题

**Q: 策略没有交易**
`scheduler.run_monthly` 在某些情况下不触发。改用 `handle_bar` 手动判断月份：
```python
if context.now.month != context.last_month:
    context.last_month = context.now.month
    rebalance(context, bar_dict)
```

**Q: 并发限制（最多 3 个回测同时运行）**
加 `--wait-if-full` 参数，自动等待队列空出：
```bash
node run-skill.js --id <id> --file <file> --wait-if-full --max-running 3
```

**Q: 获取因子报错**
确认因子名称正确，参考 [reference/ricequant_factor_list.md](reference/ricequant_factor_list.md)。

**Q: Session 失效**
RiceQuant session 自动管理，失效时会自动重新登录。如果持续失败，检查 `.env` 账号密码。
