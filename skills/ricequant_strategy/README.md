# RiceQuant 策略回测工具

RiceQuant 量化交易平台自动化策略回测工具。支持本地策略代码同步、运行回测、获取完整报告。

## 功能特性

- 自动登录并保持会话（Cookie 持久化，避免重复登录）
- 本地策略代码同步到 RiceQuant 平台
- 运行回测并自动轮询等待完成
- 获取完整回测报告（风险指标、持仓、日志）
- 支持自定义回测参数

## 快速开始

### 1. 安装依赖

```bash
cd skills/ricequant_strategy
npm install
```

### 2. 配置账号

创建 `.env` 文件：

```env
RICEQUANT_USERNAME=your_username
RICEQUANT_PASSWORD=your_password
```

### 3. 列出策略

```bash
node list-strategies.js
# 或
npm run list
```

输出示例：
```
Available Strategies:
------------------------------------------------------------
ID           | Name
------------------------------------------------------------
abc123       | 我的策略
def456       | 双均线策略
------------------------------------------------------------
Total: 2 strategies
```

### 4. 运行回测

```bash
node run-skill.js --id <strategyId> --file ./my-strategy.py
```

完整参数示例：
```bash
node run-skill.js \
  --id abc123 \
  --file ./strategy.py \
  --start 2022-01-01 \
  --end 2024-12-31 \
  --capital 1000000 \
  --freq day \
  --benchmark 000300.XSHG
```

### 5. 获取回测报告

```bash
# 基础报告（终端显示）
node fetch-report.js --id <backtestId>

# 完整报告（保存到文件）
node fetch-report.js --id <backtestId> --full
```

## CLI 命令详解

### run-skill.js - 运行回测

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `--id` | RiceQuant 策略 ID（必填） | - |
| `--file` | 本地策略文件路径（必填） | - |
| `--start` | 回测开始日期 | 2023-01-01 |
| `--end` | 回测结束日期 | 2023-12-31 |
| `--capital` | 初始资金 | 100000 |
| `--freq` | 回测频率 (day/minute) | day |
| `--benchmark` | 基准指数 | 000300.XSHG |

### list-strategies.js - 列出策略

```bash
node list-strategies.js
```

### fetch-report.js - 获取报告

```bash
node fetch-report.js --id <backtestId> [--full]
```

| 参数 | 说明 |
|------|------|
| `--id` | 回测 ID（必填） |
| `--full` | 保存完整报告到 data 目录 |

报告内容：
- 基本信息（状态、标题、创建时间）
- 风险指标（Sharpe、Sortino、MaxDrawdown、Alpha、Beta、信息比率）
- 持仓汇总（交易日数、市值、估算收益率）

## 文件结构

```
ricequant_strategy/
├── .env                    # 账户配置
├── package.json            # 依赖配置
├── run-skill.js            # CLI: 运行回测
├── list-strategies.js      # CLI: 列出策略
├── fetch-report.js         # CLI: 获取报告
├── run-backtest.js         # 脚本: 创建并运行回测
├── paths.js                # 路径配置
├── load-env.js             # 环境变量加载
│
├── request/
│   ├── ricequant-client.js # 核心 HTTP 客户端
│   ├── strategy-runner.js  # 回测工作流
│   └── ensure-session.js   # 会话入口
│
├── browser/
│   ├── session-manager.js  # 会话管理（Cookie 检查）
│   └── capture-session.js  # 登录捕获（API + 浏览器）
│
├── data/
│   └── session.json        # Cookie 存储（自动生成）
│
└── examples/
    └── double-ma-strategy.py
```

## 会话管理（Cookie 机制）

**关键特性：登录一次后，Cookie 会自动保存并复用**

工作流程：

1. **首次运行**
   - 检测 `data/session.json` 不存在或已过期
   - 自动登录（优先 API 登录，备用浏览器登录）
   - 保存 Cookie 到 `data/session.json`

2. **后续运行**
   - 检测到有效 Cookie（包含 session、rqjwt 等）
   - 直接复用，**无需重新登录**
   - 不会打开浏览器

3. **过期处理**
   - Cookie 有效期：24 小时
   - 过期后自动重新登录

Cookie 文件示例（`data/session.json`）：
```json
{
  "cookies": [
    { "name": "sid", "value": "..." },
    { "name": "rqjwt", "value": "..." }
  ],
  "timestamp": 1774763944473
}
```

登录方式（按优先级）：
1. **API 直接登录** - 快速，无浏览器依赖
2. **浏览器自动化登录** - 备用方案（Playwright）

## RiceQuant API 端点

| 端点 | 方法 | 说明 |
|------|------|------|
| `/api/user/v1/workspaces` | GET | 获取工作空间列表 |
| `/api/strategy/v1/workspaces/{id}/strategies` | GET | 列出策略 |
| `/api/strategy/v1/workspaces/{id}/strategies` | POST | 创建策略 |
| `/api/strategy/v1/workspaces/{id}/strategies/{sid}` | PUT | 保存策略代码 |
| `/api/backtest/v1/workspaces/{id}/backtests` | POST | 运行回测 |
| `/api/backtest/v1/workspaces/{id}/backtests/{btId}` | GET | 获取回测状态 |
| `/api/backtest/v1/workspaces/{id}/backtests/{btId}/risk` | GET | 风险指标 |
| `/api/backtest/v1/workspaces/{id}/backtests/{btId}/positions` | GET | 持仓数据 |
| `/api/backtest/v1/workspaces/{id}/backtests/{btId}/logs` | GET | 回测日志 |

## 程序化调用

```javascript
import { RiceQuantClient } from './request/ricequant-client.js';
import { ensureRiceQuantSession } from './browser/session-manager.js';

// 1. 获取会话（自动复用 Cookie）
const cookies = await ensureRiceQuantSession({
  username: process.env.RICEQUANT_USERNAME,
  password: process.env.RICEQUANT_PASSWORD
});

// 2. 创建客户端
const client = new RiceQuantClient({ cookies });

// 3. 列出策略
const strategies = await client.listStrategies();

// 4. 获取策略上下文
const context = await client.getStrategyContext(strategyId);

// 5. 保存策略代码
await client.saveStrategy(strategyId, '策略名称', code, context);

// 6. 运行回测
const result = await client.runBacktest(strategyId, code, {
  startTime: '2022-01-01',
  endTime: '2024-12-31',
  baseCapital: '1000000',
  frequency: 'day',
  benchmark: '000300.XSHG'
}, context);

// 7. 获取完整报告
const report = await client.getFullReport(backtestId);
console.log('Sharpe:', report.risk?.sharpe);
console.log('MaxDrawdown:', report.risk?.max_drawdown);
```

## 策略代码注意事项

RiceQuant 使用 RQAlpha 框架，部分 API 与 JoinQuant 不同：

```python
# 定时任务 - 不支持 time 参数
scheduler.run_monthly(my_func)  # 正确
scheduler.run_monthly(my_func, time='open')  # 错误

# 持仓市值
position = context.portfolio.positions[stock]
value = position.market_value  # 使用 market_value，不是 value

# 常用基准指数
# 000300.XSHG - 沪深300
# 000905.XSHG - 中证500
# 000001.XSHG - 上证指数
```

## 故障排查

### 登录失败

```
Error: Login failed: 401
```

检查 `.env` 文件中的用户名密码是否正确。

### Cookie 过期

```
Error: Session expired
```

删除 `data/session.json` 后重新运行：
```bash
rm data/session.json
node run-skill.js --id <id> --file <file>
```

### 回测超时

```
Error: Backtest timeout after 60 attempts
```

回测时间较长，可在 `run-backtest.js:124` 调整 `maxAttempts`（默认 120 次，每次等待 5 秒）。

### 获取策略 ID

策略 ID 可从 RiceQuant 网页版 URL 获取：
```
https://www.ricequant.com/quant/editor/{strategyId}
```

## 许可证

MIT