# 任务 03：红利小盘防守线实盘化

## 设计文档

### 任务定位

- 类型：防守策略主线
- 优先级：高
- 目标：把第一轮里最值得保留的防守分支做成可直接跟踪的策略

### 第一轮已知结论

- 红利小盘是价值/红利线里唯一真正有意义的分支
- 它在 2022 年是唯一正收益分支
- 它与 RFScore 风格互补，适合做防守层

### 本轮要回答的问题

1. 红利小盘单跑是否足够稳定，值得进入正式观察名单？
2. 它的真实容量、流动性、换手成本是否还能接受？
3. 当前市场下它是否比 ETF 动量更值得拿防守仓位？

### 参考材料

- `docs/parallel_strategy_tasks_20260328/05_红利价值质量三分支验证报告.md`
- `docs/parallel_strategy_tasks_20260328/05_快速参考卡.md`

### 强制实际验证要求

- 必须使用 `/Users/fengzhi/Downloads/git/testlixingren/skills/joinquant_nookbook` 计算最新候选股和流动性检查
- 必须使用 `/Users/fengzhi/Downloads/git/testlixingren/skills/joinquant_strategy` 做正式回测
- 必须给出当前候选池和可执行性判断

### 交付物

1. 一份红利小盘正式回测报告
2. 一份当前候选股清单和成交额检查
3. 一份结论：是否进入首批正式防守策略名单

### 成功判据

- 红利小盘从“结论上不错”升级成“可实际跟踪”

## 子任务提示词

```text
你现在负责把红利小盘从研究结论推进到可跟踪的防守策略。

请优先阅读：
- docs/parallel_strategy_tasks_20260328/05_红利价值质量三分支验证报告.md
- docs/parallel_strategy_tasks_20260328/05_快速参考卡.md

强制要求：
- 必须使用 /Users/fengzhi/Downloads/git/testlixingren/skills/joinquant_nookbook 获取最新候选股并做流动性检查
- 必须使用 /Users/fengzhi/Downloads/git/testlixingren/skills/joinquant_strategy 做正式回测

请完成：
1. 统一回测红利小盘正式版本
2. 检查当前候选股的成交额、涨跌停风险、行业集中度
3. 判断它是否适合替代一部分 ETF 或现金防守仓位

输出要求：
- 必须写明当前是否 Go
- 必须给出当前候选名单与风险点
- 必须说明它和 RFScore 在资金配置上的关系
```
