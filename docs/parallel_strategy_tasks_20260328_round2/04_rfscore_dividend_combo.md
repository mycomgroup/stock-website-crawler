# 任务 04：RFScore + 红利小盘双策略组合

## 设计文档

### 任务定位

- 类型：组合层主任务
- 优先级：最高
- 目标：验证第一轮提出的“进攻 RFScore + 防守 红利小盘”是否真是当前最优二元组合

### 第一轮已知结论

- RFScore 是当前最强进攻主线
- 红利小盘是当前最优防守股票分支
- 第一轮已经从逻辑上认为二者互补，但还缺组合层统一验证

### 本轮要回答的问题

1. 静态 `60/40`、`50/50`、`70/30` 哪个组合更好？
2. 底部试错状态下是否应该偏防守，趋势进攻时再偏 RFScore？
3. 这个双策略组合能否替代“RFScore + ETF 观察仓”作为股票层主方案？

### 参考材料

- `docs/parallel_strategy_tasks_20260328/01_rfscore7_pb_experiment_report.md`
- `docs/parallel_strategy_tasks_20260328/05_红利价值质量三分支验证报告.md`
- `docs/parallel_strategy_tasks_20260328/11_macro_regime_router_validation.md`

### 强制实际验证要求

- 必须使用 `/Users/fengzhi/Downloads/git/testlixingren/skills/joinquant_strategy` 做组合层回测
- 必须使用 `/Users/fengzhi/Downloads/git/testlixingren/skills/joinquant_nookbook` 获取当前双边候选与市场状态
- 不允许只做静态表述，不做组合回测

### 交付物

1. 一张组合权重对比表
2. 一份动态配比方案
3. 一个结论：当前最该推哪种组合结构

### 成功判据

- 能把“两个好策略”变成一个更好的可执行股票组合

## 子任务提示词

```text
你现在负责双策略组合验证：RFScore 作为进攻线，红利小盘作为防守线。

请优先阅读：
- docs/parallel_strategy_tasks_20260328/01_rfscore7_pb_experiment_report.md
- docs/parallel_strategy_tasks_20260328/05_红利价值质量三分支验证报告.md
- docs/parallel_strategy_tasks_20260328/11_macro_regime_router_validation.md

强制要求：
- 必须使用 /Users/fengzhi/Downloads/git/testlixingren/skills/joinquant_strategy 做组合回测
- 必须使用 /Users/fengzhi/Downloads/git/testlixingren/skills/joinquant_nookbook 获取当前候选与状态快照

请完成：
1. 对比 70/30、60/40、50/50 的静态组合
2. 测试基于市场状态的动态组合
3. 判断双策略组合是否优于单独持有 RFScore

输出要求：
- 结论必须告诉我当前该配多少
- 必须明确“是否替代 ETF 观察仓”
- 如果动态组合并没有明显更好，直接说保持静态
```
