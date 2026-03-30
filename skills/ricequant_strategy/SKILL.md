---
name: ricequant-notebook-strategy
description: 在 RiceQuant Notebook 中运行策略代码，无时间限制，可快速验证策略
---

# RiceQuant Notebook 策略运行器

**核心优势：无每日 180 分钟时间限制**

## 快速开始

```bash
# 1. 首次使用：抓取 session
node browser/capture-ricequant-notebook-session.js --notebook-url "YOUR_NOTEBOOK_URL" --headed

# 2. 运行策略
node run-strategy.js --strategy examples/simple_backtest.py

# 3. 查看结果
cat data/ricequant-notebook-result-*.json
```

## 三种使用方式

### 1. 运行策略文件

```bash
node run-strategy.js --strategy examples/simple_backtest.py
node run-strategy.js --strategy /path/to/your/strategy.py
```

### 2. 创建独立 Notebook 并运行（推荐）

```bash
# 创建新的独立 notebook 并运行
node run-strategy.js --strategy examples/simple_backtest.py --create-new

# 创建新的独立 notebook，运行后自动清理
node run-strategy.js --strategy examples/simple_backtest.py --create-new --cleanup
```

### 3. 直接执行代码

```bash
node run-strategy.js --cell-source "print('hello from ricequant')"
```

### 4. 重新执行 Notebook Cell

```bash
node run-strategy.js --cell-index last   # 执行最后一个 cell
node run-strategy.js --mode all          # 执行所有 cells
```

## 示例策略

| 文件 | 说明 | 运行时间 |
|------|------|---------|
| `examples/simple_backtest.py` | API 连接测试 | ~30秒 |
| `examples/ma_strategy_notebook.py` | 双均线策略验证 | ~1分钟 |
| `examples/rfscore_simple_notebook.py` | RFScore 选股测试 | ~2分钟 |
| `examples/double-ma-strategy.py` | 策略编辑器格式 | 需转换 |

## 参数说明

```bash
node run-strategy.js [参数]

必需参数（二选一）：
  --strategy <path>             策略文件路径
  --cell-source <code>          直接执行的代码

可选参数：
  --notebook-url <url>          Notebook URL（默认从 .env 读取）
  --timeout-ms <ms>             超时时间（默认 60000ms）
  --cell-index <index>          执行指定 cell（0, last）
  --mode <mode>                 all: 执行所有 cells
  --create-new                  创建新的独立 notebook
  --cleanup                     运行后自动清理 notebook（需配合 --create-new）
  --notebook-base-name <name>   新 notebook 基础名称（默认 strategy_run）
```

### Notebook 管理策略

1. **默认模式**（无参数）
   - 使用现有 notebook
   - 在现有 notebook 中追加 cell
   - 不会自动清理

2. **独立模式**（`--create-new`）
   - 创建新的独立 notebook
   - 名称格式：`strategy_run_<timestamp>_<random>.ipynb`
   - 适合测试和验证

3. **临时模式**（`--create-new --cleanup`）
   - 创建新的独立 notebook
   - 运行完成后自动删除
   - 适合快速测试，不保留中间文件

## 策略代码适配

### 策略编辑器 → Notebook

```python
# 策略编辑器格式
def init(context):
    scheduler.run_monthly(rebalance, monthday=1)

def rebalance(context, bar_dict):
    stocks = get_all_securities("stock", context.now)
```

```python
# Notebook 格式
stocks = get_all_securities("stock", "2024-03-20")
print(f"股票数: {len(stocks)}")
```

## 输出文件

```bash
data/
├── ricequant-notebook-TIMESTAMP.ipynb           # Notebook 快照
└── ricequant-notebook-result-TIMESTAMP.json     # 执行结果详情
```

## 常见问题

### Session 过期

```bash
node browser/capture-ricequant-notebook-session.js --notebook-url "YOUR_URL" --headed
```

### 执行超时

```bash
node run-strategy.js --strategy your_strategy.py --timeout-ms 300000  # 5分钟
```

## 功能验证测试

```bash
# 运行自动化测试套件
node test-functionality.js
```

测试内容包括：
1. 基础连接测试
2. 创建独立 notebook 测试
3. 自动清理测试

## 策略编辑器回测（原有功能）

### 运行回测

```bash
# Run a backtest with a strategy file
node run-skill.js --strategy path/to/strategy.py --config '{"start_date":"2022-01-01","end_date":"2022-12-31"}'

# List existing strategies
node list-strategies.js

# Fetch backtest report
node fetch-report.js --id <backtestId> [--full]
```

## Configuration

Create `.env` file with:
```
RICEQUANT_USERNAME=your_username
RICEQUANT_PASSWORD=your_password
RICEQUANT_NOTEBOOK_URL=your_notebook_url
```

## API Endpoints

RiceQuant uses these endpoints:
- `GET /api/user/v1/workspaces` - Get workspace list
- `GET /api/strategy/v1/workspaces/{id}/strategies` - List strategies
- `POST /api/strategy/v1/workspaces/{id}/strategies` - Create strategy
- `POST /api/backtest/v1/workspaces/{id}/backtests` - Run backtest
- `GET /api/backtest/v1/workspaces/{id}/backtests/{btId}` - Get backtest status
- `GET /api/backtest/v1/workspaces/{id}/backtests/{btId}/risk` - Risk metrics

## 文件结构

```
ricequant_strategy/
├── .env                    # Account credentials
├── browser/
│   ├── capture-ricequant-notebook-session.js  # Notebook session capture
│   ├── capture-session.js                     # API login
│   └── session-manager.js                     # Session persistence
├── request/
│   ├── ricequant-notebook-client.js           # Notebook API client
│   ├── test-ricequant-notebook.js             # Notebook test script
│   ├── ensure-ricequant-notebook-session.js   # Session management
│   ├── ricequant-client.js                    # Core HTTP client
│   └── strategy-runner.js                     # Strategy workflow
├── examples/
│   ├── simple_backtest.py                     # Simple backtest test
│   ├── ma_strategy_notebook.py                # MA strategy notebook
│   ├── rfscore_simple_notebook.py             # RFScore notebook
│   └── double-ma-strategy.py                  # Strategy editor format
├── run-strategy.js           # CLI: Run notebook strategy
├── run-skill.js              # CLI: Run backtest
├── list-strategies.js        # CLI: List strategies
├── fetch-report.js           # CLI: Get backtest report
└── data/
    ├── session.json          # Saved session cookies
    ├── notebook-contract.json # Notebook API contract
    └── raw-capture.json      # Raw capture data
```

## Notes

- RiceQuant session requires browser login (uses Playwright)
- Session cookies stored in `data/session.json`
- RQAlpha API differs from JoinQuant:
  - `scheduler.run_monthly()` doesn't support `time` parameter
  - Use `context.portfolio.positions[stock].market_value` for position value
  - Use `/risk` endpoint for statistics (not `/stats`)

## 对比：Notebook vs 策略编辑器

| 特性 | 策略编辑器 | Notebook |
|------|-----------|----------|
| 时间限制 | **180分钟/天** | **无限制** ✓ |
| 数据 API | ✓ | ✓ |
| 因子 API | ✓ | ✓ |
| 回测框架 | 完整 | 需手动实现 |
| 交互调试 | ✗ | ✓ |
| 逐步执行 | ✗ | ✓ |
| 适用场景 | 精确回测 | 快速验证 |

**推荐流程**：
1. Notebook → 快速验证逻辑
2. Notebook → 参数调优
3. 策略编辑器 → 最终精确回测