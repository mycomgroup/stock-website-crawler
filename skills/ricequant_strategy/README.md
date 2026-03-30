# RiceQuant Notebook 策略运行器

**核心优势：无每日 180 分钟时间限制**

在 RiceQuant Notebook 中运行策略代码，快速验证策略逻辑。

## 功能特性

### Notebook 运行（新增）
- 无时间限制（策略编辑器限制 180分钟/天）
- 快速验证策略逻辑
- 交互调试，逐步执行
- 自动抓取 Notebook session

### 策略编辑器回测（原有）
- 自动登录并保持会话
- 本地策略代码同步
- 运行回测并获取报告
- 支持自定义回测参数

## 快速开始

### Notebook 运行

```bash
# 1. 安装依赖
cd skills/ricequant_strategy
npm install

# 2. 配置账号和环境变量
# 创建 .env 文件：
# RICEQUANT_USERNAME=your_username
# RICEQUANT_PASSWORD=your_password
# RICEQUANT_NOTEBOOK_URL=https://www.ricequant.com/research

# 3. 运行策略（自动处理 session）
node run-strategy.js --strategy examples/simple_backtest.py

# 4. 查看结果
cat data/ricequant-notebook-result-*.json
```

### Session 自动管理

**系统会自动处理 session，无需手动干预：**

- ✅ 自动检查现有 session 是否有效
- ✅ Session 无效时自动后台登录（headless模式）
- ✅ 登录成功后自动保存 session
- ✅ 后续运行自动复用有效 session（7天有效期）

**首次运行时会自动登录，后续运行会自动复用 session。**

测试 session 状态：
```bash
npm run test-session
```

详细说明请查看：[SESSION_MANAGEMENT.md](SESSION_MANAGEMENT.md)

### 策略编辑器回测

```bash
# 列出策略
node list-strategies.js

# 运行回测
node run-skill.js --id <strategyId> --file ./my-strategy.py

# 获取回测报告
node fetch-report.js --id <backtestId> --full
```

## Notebook 示例

```bash
# 运行策略文件
node run-strategy.js --strategy examples/simple_backtest.py

# 直接执行代码
node run-strategy.js --cell-source "print('hello')"

# 增加超时时间
node run-strategy.js --strategy your_strategy.py --timeout-ms 300000

# 重新执行 notebook 中的 cell
node run-strategy.js --cell-index last

# 创建独立 notebook 并运行
node run-strategy.js --strategy your_strategy.py --create-new

# 创建独立 notebook，运行后自动清理
node run-strategy.js --strategy your_strategy.py --create-new --cleanup
```

## Notebook 管理策略

### 默认模式
- 使用现有 notebook
- 在现有 notebook 中追加 cell
- 不会自动清理

### 独立模式（`--create-new`）
- 创建新的独立 notebook
- 名称格式：`strategy_run_<timestamp>_<random>.ipynb`
- 适合测试和验证

### 临时模式（`--create-new --cleanup`）
- 创建新的独立 notebook
- 运行完成后自动删除
- 适合快速测试，不保留中间文件

## 示例策略

| 文件 | 说明 | 运行时间 |
|------|------|---------|
| `examples/simple_backtest.py` | API 连接测试 | ~30秒 |
| `examples/ma_strategy_notebook.py` | 双均线策略验证 | ~1分钟 |
| `examples/rfscore_simple_notebook.py` | RFScore 选股测试 | ~2分钟 |
| `examples/double-ma-strategy.py` | 策略编辑器格式 | 需转换 |

## 策略代码转换

### 策略编辑器格式
```python
def init(context):
    scheduler.run_monthly(rebalance, monthday=1)

def rebalance(context, bar_dict):
    stocks = get_all_securities("stock", context.now)
```

### Notebook 格式
```python
stocks = get_all_securities("stock", "2024-03-20")
print(f"股票数: {len(stocks)}")
```

## CLI 命令详解

### run-strategy.js - Notebook 策略运行

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `--strategy` | 策略文件路径 | - |
| `--cell-source` | 直接执行的代码 | - |
| `--notebook-url` | Notebook URL | 从 .env 读取 |
| `--timeout-ms` | 超时时间 | 60000 |
| `--cell-index` | 执行指定 cell | last |
| `--mode` | all: 执行所有 cells | - |
| `--create-new` | 创建新的独立 notebook | false |
| `--cleanup` | 运行后自动清理 notebook | false |
| `--notebook-base-name` | 新 notebook 基础名称 | strategy_run |

### test-functionality.js - 功能验证测试

```bash
# 运行自动化测试套件
node test-functionality.js
```

测试内容包括：
1. 基础连接测试
2. 创建独立 notebook 测试
3. 自动清理测试

### run-skill.js - 策略编辑器回测

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `--id` | RiceQuant 策略 ID | - |
| `--file` | 本地策略文件路径 | - |
| `--start` | 回测开始日期 | 2023-01-01 |
| `--end` | 回测结束日期 | 2023-12-31 |
| `--capital` | 初始资金 | 100000 |

## 文件结构

```
ricequant_strategy/
├── .env                    # 账户配置
├── package.json            # 依赖配置
├── run-strategy.js         # Notebook 运行脚本
├── run-skill.js            # 策略编辑器回测脚本
├── list-strategies.js      # CLI: 列出策略
├── fetch-report.js         # CLI: 获取报告
├── paths.js                # 路径配置
├── load-env.js             # 环境变量加载
│
├── request/
│   ├── ricequant-notebook-client.js           # Notebook API client
│   ├── test-ricequant-notebook.js             # Notebook test script
│   ├── ensure-ricequant-notebook-session.js   # Notebook session
│   ├── ricequant-client.js                    # HTTP client
│   └── strategy-runner.js                     # 回测工作流
│
├── browser/
│   ├── capture-ricequant-notebook-session.js  # Notebook session capture
│   ├── capture-session.js                     # API login
│   └── session-manager.js                     # Session persistence
│
├── data/
│   ├── session.json          # Cookie 存储
│   ├── notebook-contract.json # Notebook API contract
│   └── raw-capture.json      # Raw capture data
│
└── examples/
    ├── simple_backtest.py    # 简单测试
    ├── ma_strategy_notebook.py # MA策略
    ├── rfscore_simple_notebook.py # RFScore
    └── double-ma-strategy.py # 策略编辑器格式
```

## 输出文件

```bash
data/
├── ricequant-notebook-TIMESTAMP.ipynb           # Notebook 快照
└── ricequant-notebook-result-TIMESTAMP.json     # 执行结果详情
```

## 故障排查

### Notebook Session 过期

```bash
node browser/capture-ricequant-notebook-session.js --notebook-url "YOUR_URL" --headed
```

### Notebook 执行超时

```bash
node run-strategy.js --strategy your_strategy.py --timeout-ms 300000
```

### 策略编辑器登录失败

检查 `.env` 文件中的用户名密码是否正确。

### 策略编辑器 Cookie 过期

```bash
rm data/session.json
node run-skill.js --id <id> --file <file>
```

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

## RiceQuant API 端点

| 端点 | 方法 | 说明 |
|------|------|------|
| `/api/user/v1/workspaces` | GET | 获取工作空间列表 |
| `/api/strategy/v1/workspaces/{id}/strategies` | GET | 列出策略 |
| `/api/backtest/v1/workspaces/{id}/backtests` | POST | 运行回测 |
| `/api/backtest/v1/workspaces/{id}/backtests/{btId}/risk` | GET | 风险指标 |

## 程序化调用

### Notebook API

```javascript
import { runNotebookTest } from './request/test-ricequant-notebook.js';

const result = await runNotebookTest({
  notebookUrl: process.env.RICEQUANT_NOTEBOOK_URL,
  cellSource: 'print("hello")',
  timeoutMs: 60000
});

console.log(result.executions[0].textOutput);
```

### 策略编辑器 API

```javascript
import { RiceQuantClient } from './request/ricequant-client.js';

const client = new RiceQuantClient({ cookies });
const strategies = await client.listStrategies();
const report = await client.getFullReport(backtestId);
```

## 许可证

MIT