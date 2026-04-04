# 回测结果查询

提交回测时如果没有记录 ID，可以通过以下方式找回。

---

## 各平台查询命令

### RiceQuant
```bash
cd skills/ricequant_strategy

node fetch-backtest-results.js --strategy-id <id> --list     # 列出所有
node fetch-backtest-results.js --strategy-id <id> --latest   # 最近一条
node fetch-backtest-results.js --backtest-id <id>            # 指定 ID
node fetch-backtest-results.js --strategy-id <id> --latest --save  # 保存文件
```

### JoinQuant
```bash
cd skills/joinquant_strategy

node fetch-backtest-results.js --algorithm-id <id> --list
node fetch-backtest-results.js --algorithm-id <id> --latest
node fetch-backtest-results.js --algorithm-id <id> --backtest-id <btId>
```

注意：JoinQuant 查询结果需要 CSRF token，必须同时提供 `--algorithm-id`。

### THSQuant
```bash
cd skills/thsquant_strategy

node fetch-backtest-results.js --algo-id <id> --list
node fetch-backtest-results.js --algo-id <id> --latest
node fetch-backtest-results.js --backtest-id <id>
```

### BigQuant
```bash
cd skills/bigquant_strategy

node fetch-backtest-results.js --list                              # 所有 Task
node fetch-backtest-results.js --name-prefix rfscore7 --list      # 按名称过滤
node fetch-backtest-results.js --name-prefix rfscore7 --latest    # 最近一条
node fetch-backtest-results.js --task-id <id>                     # 指定 Task
```

### GuornQuant
果仁网结果不持久化，只能查本地文件：
```bash
ls skills/guorn_strategy/output/backtest-*.json | sort -r
```

---

## 各平台能力对比

| 平台 | 有历史查询 | 查询方式 |
|------|-----------|---------|
| RiceQuant | ✅ | 按 strategyId 查 API |
| JoinQuant | ✅ | 按 algorithmId 解析 HTML |
| THSQuant | ✅ | 按 algoId 查 API |
| BigQuant | ⚠️ | 按 task name 前缀过滤 |
| GuornQuant | ❌ | 无服务端持久化，查本地文件 |

---

## 底层 API 方法

各平台 client 新增的查询方法：

**RiceQuant** (`ricequant-client.js`)：
- `listStrategyBacktests(strategyId)` — 按策略列出所有回测，时间倒序
- `getLatestBacktestResult(strategyId)` — 自动取最新一条并拉完整结果
- `getBacktestResultById(backtestId)` — 直接用 ID 查

**JoinQuant** (`joinquant-strategy-client.js`)：
- `getBacktests(algorithmId)` — 列出策略历史回测（HTML 解析）
- `getBacktestResult(backtestId, context)` — 查回测结果（需 context.token）

**THSQuant** (`thsquant-client.js`)：
- `listBacktests(algoId, page, num)` — 列出历史回测（分页）
- `getLatestBacktest(algoId)` — 获取最近一次回测信息
- `getFullReport(backtestId)` — 并行拉取完整报告

**BigQuant** (`bigquant-client.js`)：
- `listTasks({ size })` — 列出所有 Task
- `getTask(taskId)` — 获取 Task 详情
- `getNotebookOutputs(taskId)` — 获取 notebook 输出
