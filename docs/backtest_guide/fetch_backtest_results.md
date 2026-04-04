# 回测结果查询指南

> 问题背景：提交回测时如果没有记录 backtestId / taskId，事后仍可通过策略 ID 或名称查询历史回测结果。

---

## 各平台查询入口

每个平台均提供统一的 `fetch-backtest-results.js` 脚本，支持以下模式：

| 模式 | 参数 | 说明 |
|------|------|------|
| 列出所有回测 | `--list` | 按时间倒序列出历史记录 |
| 最近一次结果 | `--latest` | 自动找最新一条并拉完整数据 |
| 指定 ID 查询 | `--backtest-id` / `--task-id` | 直接用已知 ID 查 |
| 保存到文件 | `--save` | 任意模式均可附加，结果写入 output/ |

---

## RiceQuant（米筐）

路径：`skills/ricequant_strategy/`

```bash
# 列出策略所有回测
node fetch-backtest-results.js --strategy-id <id> --list

# 最近一次完整结果
node fetch-backtest-results.js --strategy-id <id> --latest

# 指定 backtestId 查
node fetch-backtest-results.js --backtest-id <id>

# 保存结果
node fetch-backtest-results.js --strategy-id <id> --latest --save
```

底层 API（`ricequant-client.js`）：

| 方法 | 说明 |
|------|------|
| `listStrategyBacktests(strategyId)` | 按策略 ID 列出所有回测，时间倒序 |
| `getLatestBacktestResult(strategyId)` | 自动取最新一条并拉完整结果 |
| `getBacktestResultById(backtestId)` | 直接用 backtestId 查 |
| `getBacktestList(strategyId)` | 原始列表（不排序） |

---

## JoinQuant（聚宽）

路径：`skills/joinquant_strategy/`

```bash
# 列出策略所有回测
node fetch-backtest-results.js --algorithm-id <id> --list

# 最近一次完整结果
node fetch-backtest-results.js --algorithm-id <id> --latest

# 指定 backtestId 查（需同时提供 algorithm-id 获取 CSRF token）
node fetch-backtest-results.js --algorithm-id <id> --backtest-id <btId>

# 保存结果
node fetch-backtest-results.js --algorithm-id <id> --latest --save
```

注意事项：
- 聚宽的 `getBacktests()` 通过解析 HTML 页面获取回测列表，依赖页面结构，如遇空结果请检查 session 是否有效
- 查询回测结果需要 CSRF token，必须先调用 `getStrategyContext(algorithmId)` 获取
- 旧的 `check-backtest-results.js` 和 `check-latest-backtest.js` 是硬编码 ID 的临时脚本，建议改用 `fetch-backtest-results.js`

底层 API（`joinquant-strategy-client.js`）：

| 方法 | 说明 |
|------|------|
| `getBacktests(algorithmId)` | 列出策略所有回测（HTML 解析） |
| `getBacktestResult(backtestId, context)` | 查回测结果（需 context.token） |
| `getFullReport(backtestId, context)` | 聚合所有数据（含归因分析） |

---

## THSQuant（同花顺 SuperMind）

路径：`skills/thsquant_strategy/`

```bash
# 列出策略所有回测（最多 50 条）
node fetch-backtest-results.js --algo-id <id> --list

# 最近一次完整结果
node fetch-backtest-results.js --algo-id <id> --latest

# 指定 backtestId 查
node fetch-backtest-results.js --backtest-id <id>

# 保存结果
node fetch-backtest-results.js --algo-id <id> --latest --save
```

底层 API（`thsquant-client.js`）：

| 方法 | 说明 |
|------|------|
| `listBacktests(algoId, page, num)` | 列出策略历史回测（分页） |
| `getLatestBacktest(algoId)` | 获取最近一次回测信息 |
| `getFullReport(backtestId)` | 并行拉取完整报告（detail/performance/tradeLog/backtestLog/dailyGains） |
| `getBacktestPerformance(backtestId)` | 单独获取绩效指标 |

---

## BigQuant

路径：`skills/bigquant_strategy/`

BigQuant 是 **Task-based 模型**，没有"策略 ID"概念。每次提交创建新 Task，Task 名称包含策略文件名 + 时间戳（如 `rfscore7_pb10_v3_20260404_1430`）。查询时通过名称前缀过滤。

```bash
# 列出所有 Task（最近 100 条）
node fetch-backtest-results.js --list

# 按策略名称前缀过滤
node fetch-backtest-results.js --name-prefix rfscore7_pb10 --list

# 最近一条（可配合前缀）
node fetch-backtest-results.js --latest
node fetch-backtest-results.js --name-prefix rfscore7_pb10 --latest

# 指定 taskId 查
node fetch-backtest-results.js --task-id <id>

# 保存结果
node fetch-backtest-results.js --name-prefix rfscore7 --latest --save
```

底层 API（`bigquant-client.js`）：

| 方法 | 说明 |
|------|------|
| `listTasks({ size })` | 列出所有 Task（按 creator 过滤） |
| `getTask(taskId)` | 获取 Task 详情 |
| `getNotebookOutputs(taskId)` | 获取 notebook cell 输出 |
| `getLogs(runId, count)` | 获取执行日志 |

注意事项：
- Task 名称格式：`{策略文件名}_{YYYYMMDD}_{HHMM}`，可通过 `--name-prefix` 按文件名前缀过滤
- BigQuant 的回测结果在 notebook 输出中（print 语句），不是结构化 API 返回
- 如果策略代码没有 print 输出关键指标，则无法自动解析，需要手动查看 `textOutput`

---

## GuornQuant（果仁网）

路径：`skills/guorn_strategy/`

果仁网的回测通过浏览器 JS（`scrat.utility.ajaxDispatch`）执行，**结果直接返回给前端，不持久化到服务端**。

- 没有 backtestId 概念
- 历史查询接口 `/stock/backtest/history` 存在但可靠性未验证
- 每次回测结果保存在本地 `output/backtest-{timestamp}.json`

建议：每次运行后立即检查 `output/` 目录下的结果文件，文件名包含时间戳可以追溯。

---

## 问题总结

| 平台 | 有历史查询 | 查询方式 | 入口脚本 |
|------|-----------|---------|---------|
| RiceQuant | ✅ | 按 strategyId 查 API | `fetch-backtest-results.js` |
| JoinQuant | ✅ | 按 algorithmId 解析 HTML | `fetch-backtest-results.js` |
| THSQuant | ✅ | 按 algoId 查 API | `fetch-backtest-results.js` |
| BigQuant | ⚠️ | 按 task name 前缀过滤 | `fetch-backtest-results.js` |
| GuornQuant | ❌ | 无服务端持久化 | 查本地 `output/*.json` |
