# 量化回测平台 Skill 集合

## 功能描述

向多个量化回测平台（JoinQuant / RiceQuant / THSQuant / BigQuant / GuornQuant）提交策略代码、运行回测、查询历史结果。每个平台是独立的 skill，共享相同的接口规范。

---

## 平台选择

```
策略用了 jqfactor 特殊因子？
  是 → JoinQuant
  否 → 因子简单（PE/PB/ROE/市值等）？
        是 → RiceQuant（推荐，session 自动管理）
        否 → 参考下表
```

| 平台 | Skill 目录 | 适合场景 | 主要限制 |
|------|-----------|---------|---------|
| JoinQuant | `skills/joinquant_strategy/` | 复杂因子、最终验证 | 需手动维护 session |
| RiceQuant | `skills/ricequant_strategy/` | 日常开发、快速验证 | 策略编辑器 180min/天 |
| THSQuant | `skills/thsquant_strategy/` | 同花顺生态 | 首次需手动登录 |
| BigQuant | `skills/bigquant_strategy/` | AI/ML 策略 | Task-based，无策略 ID |
| GuornQuant | `skills/guorn_strategy/` | 因子选股 | 回测不持久化，需浏览器 |

---

## 核心能力

1. **提交回测**：将本地策略文件同步到平台并触发回测
2. **等待结果**：轮询回测状态，完成后输出摘要指标
3. **查询历史**：忘记 ID 时，按策略 ID / 名称前缀找回历史回测
4. **自动重试**：429/503 并发限制自动等待（60s/120s/300s），网络错误自动重试
5. **结果持久化**：回测报告保存到各平台的 `output/` 目录

---

## 使用方式

### JoinQuant

```bash
cd skills/joinquant_strategy
node run-skill.js --id <algorithmId> --file ./my_strategy.py \
  --start 2021-01-01 --end 2024-12-31

# 查询历史回测
node fetch-backtest-results.js --algorithm-id <id> --latest
```

### RiceQuant

```bash
cd skills/ricequant_strategy
node run-skill.js --id <strategyId> --file ./my_strategy.py \
  --start 2021-01-01 --end 2024-12-31

# 并发满时自动等待
node run-skill.js --id <id> --file <file> --wait-if-full

# 查询历史回测
node fetch-backtest-results.js --strategy-id <id> --latest
```

### THSQuant

```bash
cd skills/thsquant_strategy

# 首次使用：手动登录
node browser/manual-login-capture.js

node run-skill.js --id <algoId> --file ./my_strategy.py \
  --start 2023-01-01 --end 2024-12-31

# 查询历史回测
node fetch-backtest-results.js --algo-id <id> --latest
```

### BigQuant

```bash
cd skills/bigquant_strategy
node run-skill.js --strategy ./my_strategy.py \
  --name rfscore7_pb10 \
  --start-date 2023-01-01 --end-date 2024-12-31

# 按名称前缀查询历史
node fetch-backtest-results.js --name-prefix rfscore7_pb10 --latest
```

### GuornQuant

```bash
cd skills/guorn_strategy
node run-skill.js
# 结果保存在 output/backtest-{timestamp}.json
```

---

## 输入参数

各平台 `run-skill.js` 的通用参数：

| 参数 | JoinQuant | RiceQuant | THSQuant | BigQuant |
|------|-----------|-----------|----------|----------|
| 策略 ID | `--id` | `--id` | `--id` | 无（Task-based） |
| 策略文件 | `--file` | `--file` | `--file` | `--strategy` |
| 开始日期 | `--start` | `--start` | `--start` | `--start-date` |
| 结束日期 | `--end` | `--end` | `--end` | `--end-date` |
| 初始资金 | `--capital` | `--capital` | `--capital` | `--capital` |
| 频率 | `--freq` | `--freq` | `--freq` | `--frequency` |
| 业务名称 | — | — | `--name` | `--name` |

---

## 输出

- 回测摘要（终端打印）：总收益、年化收益、最大回撤、夏普比率
- 完整报告（JSON 文件）：保存在各平台 `output/` 目录
- 日志文件：`output/` 目录下带时间戳的 JSON

---

## 查询历史回测

提交时没记录 ID，用以下命令找回：

```bash
# RiceQuant
node fetch-backtest-results.js --strategy-id <id> --list    # 列出所有
node fetch-backtest-results.js --strategy-id <id> --latest  # 最近一条
node fetch-backtest-results.js --backtest-id <id>           # 指定 ID

# JoinQuant（需同时提供 algorithm-id 获取 CSRF token）
node fetch-backtest-results.js --algorithm-id <id> --latest

# THSQuant
node fetch-backtest-results.js --algo-id <id> --latest

# BigQuant（按 Task 名称前缀过滤）
node fetch-backtest-results.js --name-prefix <策略名> --latest

# 所有平台均支持 --save 保存结果到文件
node fetch-backtest-results.js --strategy-id <id> --latest --save
```

---

## 重试策略

所有平台 HTTP 客户端统一实现：

| 错误类型 | 第1次等待 | 第2次等待 | 第3次等待 |
|---------|---------|---------|---------|
| 429 / 503 并发限制 | 60s | 120s | 300s |
| 5xx 服务端错误 | 10s | 20s | 40s |
| 网络/超时 | 5s | 10s | 20s |
| 4xx 客户端错误 | 不重试 | — | — |

请求超时默认 30 秒，超时后触发网络错误重试。

---

## 常见问题

**Q: 提交失败 / 429 / 503**
平台并发限制，自动重试，等待即可。RiceQuant 可加 `--wait-if-full` 主动等待队列空出。

**Q: 没记录 backtestId**
用 `fetch-backtest-results.js --latest` 查最近一条，详见上方"查询历史回测"。

**Q: Session 过期**
- JoinQuant：`node browser/capture-session.js --headed`
- THSQuant：`node browser/manual-login-capture.js`
- RiceQuant / BigQuant：自动处理，无需手动操作

**Q: 策略没有交易（RiceQuant）**
`scheduler.run_monthly` 可能不触发，改用 `handle_bar` 手动判断月份：
```python
if context.now.month != context.last_month:
    context.last_month = context.now.month
    rebalance(context, bar_dict)
```

**Q: BigQuant 找不到历史结果**
BigQuant 没有策略 ID，用 Task 名称前缀查：
```bash
node fetch-backtest-results.js --name-prefix 你的策略名 --list
```

**Q: 果仁网回测结果丢失**
果仁网结果不持久化，只有本地 `output/backtest-*.json`。每次回测后立即记录关键指标。

---

## 详细文档

- [JoinQuant 详细指南](joinquant.md)
- [RiceQuant 详细指南](ricequant.md)
- [THSQuant 详细指南](thsquant.md)
- [BigQuant 详细指南](bigquant.md)
- [GuornQuant 详细指南](guorn.md)
- [重试与超时策略](reference/retry_policy.md)
- [回测结果查询](reference/fetch_results.md)
