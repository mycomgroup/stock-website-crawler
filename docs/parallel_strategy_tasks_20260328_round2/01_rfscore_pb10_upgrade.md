# 任务 01：RFScore 主线从 PB20 升级到 PB10

## 设计文档

### 任务定位

- 类型：主策略升级
- 优先级：最高
- 目标：把第一轮里最强的单条结论正式落地成新主线

### 第一轮已知结论

- 第一轮验证显示 `PB10%` 明显优于 `PB20%`
- `PB10%` 在全区间、近期区间、2022 熊市区间都胜出
- 当前最大问题不是“要不要继续研究 RFScore”，而是“尽快把主策略口径统一到 PB10”

### 本轮要回答的问题

1. `PB10` 是否应该直接取代 `PB20` 成为正式版本？
2. `PB10 / PB15 / PB25` 在更长区间与当前市场下，哪个最适合作为正式实盘参数？
3. 是否需要同步修改当前策略代码、文件名、当前候选股口径？

### 参考材料

- `docs/parallel_strategy_tasks_20260328/01_rfscore7_pb_experiment_report.md`
- `RFScore7终极版策略总结.md`
- `strategies/rfscore7_pb20_final.py`
- `strategies/rfscore7_base_800.py`

### 强制实际验证要求

- 必须使用 `/Users/fengzhi/Downloads/git/testlixingren/skills/joinquant_nookbook` 做参数与候选股验证
- 必须使用 `/Users/fengzhi/Downloads/git/testlixingren/skills/joinquant_strategy` 做正式回测
- 必须输出真实结果文件路径
- 没有实际运行结果，不允许写“升级完成”

### 交付物

1. 一份 `PB10/PB15/PB25` 统一口径对比表
2. 一份当前市场候选股快照
3. 一个最终结论：正式版本到底是 `PB10` 还是别的
4. 如果 `PB10` 胜出，给出代码改动点和新文件命名建议

### 成功判据

- 主线参数从“猜测”变成“统一口径”
- 后续所有组合任务都能直接引用同一个 RFScore 正式版本

## 子任务提示词

```text
你现在负责 RFScore 主线升级任务。

背景：
- 第一轮验证已经显示 PB10% 显著优于 PB20%
- 但当前执行方案、文档和代码口径仍然混用了 PB20

请优先阅读：
- docs/parallel_strategy_tasks_20260328/01_rfscore7_pb_experiment_report.md
- RFScore7终极版策略总结.md
- strategies/rfscore7_pb20_final.py
- strategies/rfscore7_base_800.py

强制要求：
- 必须使用 /Users/fengzhi/Downloads/git/testlixingren/skills/joinquant_nookbook 做实际参数验证
- 必须使用 /Users/fengzhi/Downloads/git/testlixingren/skills/joinquant_strategy 做正式回测
- 必须给出结果文件路径和关键指标

请完成：
1. 统一比较 PB10 / PB15 / PB25
2. 检查当前市场候选股是否因为 PB 阈值变化而明显改善
3. 判断正式版本应采用哪个阈值
4. 给出代码迁移方案，明确哪几行该改

输出要求：
- 先给正式版本结论
- 明确写 Go / No-Go
- 不要停留在“建议”，要回答“现在就该用哪个版本”
```
