# JoinQuant（聚宽）回测指南

目录：`skills/joinquant_strategy/`

---

## 环境配置

```bash
cd skills/joinquant_strategy
npm install
```

`.env` 需要：
```
JOINQUANT_USERNAME=your_username
JOINQUANT_PASSWORD=your_password
```

Session 管理：需手动维护。Session 过期后重新登录：
```bash
node browser/capture-session.js --headed
```

---

## 提交回测

```bash
# 基本用法
node run-skill.js --id <algorithmId> --file ./my_strategy.py

# 完整参数
node run-skill.js \
  --id <algorithmId> \
  --file ./my_strategy.py \
  --start 2021-01-01 \
  --end 2024-12-31 \
  --capital 100000 \
  --freq day
```

参数说明：

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `--id` | 聚宽策略 ID（必填） | - |
| `--file` | 本地策略文件路径（必填） | - |
| `--start` | 回测开始日期 | 2021-01-01 |
| `--end` | 回测结束日期 | 2025-03-28 |
| `--capital` | 初始资金 | 100000 |
| `--freq` | 频率 day/minute | day |

---

## 查询回测结果

```bash
# 列出策略所有历史回测
node fetch-backtest-results.js --algorithm-id <id> --list

# 最近一次完整结果
node fetch-backtest-results.js --algorithm-id <id> --latest

# 指定 backtestId 查询
node fetch-backtest-results.js --algorithm-id <id> --backtest-id <btId>

# 保存结果到文件
node fetch-backtest-results.js --algorithm-id <id> --latest --save
```

注意：查询结果需要 CSRF token，必须同时提供 `--algorithm-id`。

---

## 策略代码格式

```python
def initialize(context):
    run_monthly(rebalance, 1)
    set_benchmark('000300.XSHG')
    set_slippage(PriceRelatedSlippage(0.002))

def rebalance(context, data):
    stocks = get_index_stocks('000300.XSHG')
    # 选股逻辑...
    order_target_percent(stock, 1.0 / len(selected))

def handle_data(context, data):
    pass
```

---

## 核心 API 对照（JoinQuant → RiceQuant）

| JoinQuant | RiceQuant | 说明 |
|-----------|-----------|------|
| `get_all_securities("stock", date)` | `all_instruments("CS")` | 全市场股票 |
| `get_index_stocks(code, date)` | `index_components(code)` | 指数成分股 |
| `get_price(stocks, ...)` | `history_bars(stock, n, freq, fields)` | 历史价格 |
| `get_trade_days(start, end)` | `get_trading_dates(start, end)` | 交易日 |
| `get_fundamentals(query(...))` | `get_factor(stocks, factor, start, end)` | 基本面数据 |
| `run_monthly(func, 1)` | `scheduler.run_monthly(func, 1)` | 月度调仓 |
| `order_target_percent(stock, pct)` | `order_target_percent(stock, pct)` | 目标仓位 |

---

## 文件结构

```
joinquant_strategy/
├── .env                              # 账号配置
├── run-skill.js                      # 提交回测入口
├── fetch-backtest-results.js         # 查询回测结果
├── list-strategies.js                # 列出所有策略
├── batch-backtest.js                 # 批量提交回测
├── check-backtest-status.js          # 检查回测状态
├── request/
│   ├── joinquant-strategy-client.js  # HTTP 客户端（含重试）
│   ├── strategy-runner.js            # 完整工作流
│   └── ensure-session.js             # Session 管理
├── browser/
│   └── capture-session.js            # 浏览器登录抓 session
└── output/                           # 回测结果输出
```

---

## 常见问题

**Q: 策略没有交易**
检查 `run_monthly` 是否正确触发。可以在 `handle_data` 里加日志确认。

**Q: API 报错 `get_fundamentals` 不存在**
聚宽的 `get_fundamentals` 需要 `from jqdata import *`，确认 import 正确。

**Q: Session 过期**
```bash
node browser/capture-session.js --headed
```

**Q: 批量提交时 429 错误**
自动重试会等待 60s/120s/300s，无需手动干预。如果频繁触发，减少并发数量。
