# 任务 02：RFScore 辅助过滤增强

## 设计文档

### 任务定位

- 类型：主策略增强
- 优先级：高
- 目标：在不破坏 RFScore 母体的前提下，验证少数真正有价值的辅助过滤条件

### 第一轮已知结论

- 新因子没有跑出强主因子
- 但 `换手率负向显著`、`CGO/潮汐反转可做辅助过滤` 有一些边际信号
- 当前最合理的方向不是换主引擎，而是试少量“过滤器”

### 本轮要回答的问题

1. 高换手过滤能不能改善 RFScore 回撤或夏普？
2. `CGO 反向过滤` 是否有边际价值？
3. 行业过度集中约束、`RFScore>=6` 备用池是否能提升稳定性？

### 参考材料

- `docs/parallel_strategy_tasks_20260328/01_rfscore7_pb_experiment_report.md`
- `docs/parallel_strategy_tasks_20260328/09_factor_innovation_lab_validation_report.md`
- `docs/parallel_strategy_tasks_20260328/09_factor_innovation_lab_v2_validation_report.md`

### 强制实际验证要求

- 必须使用 `/Users/fengzhi/Downloads/git/testlixingren/skills/joinquant_nookbook` 计算过滤信号
- 必须使用 `/Users/fengzhi/Downloads/git/testlixingren/skills/joinquant_strategy` 在 RFScore 正式版本上逐个回测
- 不能只做 IC 检验，必须做策略层验证

### 交付物

1. 一张过滤器对比表：收益、回撤、夏普、候选股数变化
2. 一个最终结论：保留哪些过滤器，拒绝哪些过滤器
3. 一份最小增强版 RFScore 方案

### 成功判据

- 只留下 1 到 2 个真有用的增强项
- 不把主策略再次搞复杂

## 子任务提示词

```text
你现在负责 RFScore 的辅助过滤增强任务。

你的目标不是重做一个新策略，而是在 RFScore 正式版本上测试少量有证据的过滤器。

请优先阅读：
- docs/parallel_strategy_tasks_20260328/01_rfscore7_pb_experiment_report.md
- docs/parallel_strategy_tasks_20260328/09_factor_innovation_lab_validation_report.md
- docs/parallel_strategy_tasks_20260328/09_factor_innovation_lab_v2_validation_report.md

强制要求：
- 必须使用 /Users/fengzhi/Downloads/git/testlixingren/skills/joinquant_nookbook 计算换手率、CGO 等过滤信号
- 必须使用 /Users/fengzhi/Downloads/git/testlixingren/skills/joinquant_strategy 做策略层回测

请完成：
1. 测试高换手剔除
2. 测试 CGO 最高分位剔除
3. 测试行业集中度上限
4. 测试 RFScore>=6 的备用池补位

输出要求：
- 每个过滤器都要写清收益改善还是回撤改善
- 如果没有明显增益，直接淘汰
- 最终只允许保留少数几个真有用的增强项
```
