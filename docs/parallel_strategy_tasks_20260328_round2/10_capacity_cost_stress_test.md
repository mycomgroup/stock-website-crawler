# 任务 10：容量 / 成本 / 执行压力测试

## 设计文档

### 任务定位

- 类型：实盘落地关卡
- 优先级：最高
- 目标：把第二轮筛出来的优胜策略过一遍“真能不能做”的最后门槛

### 第一轮已知结论

- 目前最值得继续推进的方向已经比较清晰
- 但不同策略的流动性、换手、冲击成本、候选股稀疏程度差异很大
- 如果不做压力测试，很容易把“回测好看”误判成“可执行”

### 本轮要回答的问题

1. `RFScore 主线 / 红利小盘 / ETF 基线 / 防守底仓` 在更严成本下是否还能成立？
2. 哪些策略对滑点和成交额最敏感？
3. 哪些策略可以放较大仓位，哪些只能小仓观察？

### 参考材料

- `docs/parallel_strategy_tasks_20260328/01_rfscore7_pb_experiment_report.md`
- `docs/parallel_strategy_tasks_20260328/05_红利价值质量三分支验证报告.md`
- `docs/parallel_strategy_tasks_20260328/02_etf_baseline_report.md`
- `docs/parallel_strategy_tasks_20260328/首批实跑组合验证报告_2026-03-28.md`

### 强制实际验证要求

- 必须使用 `/Users/fengzhi/Downloads/git/testlixingren/skills/joinquant_strategy` 做不同成本、不同仓位规模的压力测试
- 必须使用 `/Users/fengzhi/Downloads/git/testlixingren/skills/joinquant_nookbook` 获取当前成交额、候选股数、换手快照
- 必须输出“建议最大仓位等级”

### 交付物

1. 一张压力测试表：标准成本、2倍成本、3倍成本
2. 一张仓位等级表：可大仓、中仓、小仓、观察
3. 一个最终建议：哪些策略可以真正放到实盘主名单

### 成功判据

- 最终执行方案不再只看收益，而是看可执行性

## 子任务提示词

```text
你现在负责对第二轮优胜策略做实盘落地前的压力测试。

请优先阅读：
- docs/parallel_strategy_tasks_20260328/01_rfscore7_pb_experiment_report.md
- docs/parallel_strategy_tasks_20260328/05_红利价值质量三分支验证报告.md
- docs/parallel_strategy_tasks_20260328/02_etf_baseline_report.md
- docs/parallel_strategy_tasks_20260328/首批实跑组合验证报告_2026-03-28.md

强制要求：
- 必须使用 /Users/fengzhi/Downloads/git/testlixingren/skills/joinquant_strategy 做成本压力测试
- 必须使用 /Users/fengzhi/Downloads/git/testlixingren/skills/joinquant_nookbook 获取成交额与换手快照

请完成：
1. 对 RFScore、红利小盘、ETF 基线、防守底仓做成本敏感性测试
2. 检查候选池稀疏和流动性问题
3. 给出每条策略的建议最大仓位等级

输出要求：
- 不能只给收益曲线
- 必须明确哪些策略只能小仓，哪些可做核心仓
- 如果某条策略对成本过敏，直接降级
```
