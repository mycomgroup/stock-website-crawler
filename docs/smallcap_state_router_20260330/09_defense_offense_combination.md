# 任务 09：防守线与进攻线组合测试

## 设计文档

### 任务定位

- 聚焦方向：`双引擎组合`
- 目标：验证防守线 + 进攻线的组合效果，替代简单等权组合

### 当前已知问题

- 已验证"多策略等权组合"会稀释 alpha，但不确定"防守+进攻"的组合方式是否有效
- 不清楚如何通过状态路由来动态调整两者权重
- 需要验证组合后的整体风险收益特征

### 参考材料

- `docs/parallel_strategy_tasks_20260328_round3_rfscore_pb10/result_07_rfscore_dividend_smallcap_full_backtest.md`（RFScore+红利小盘组合经验）
- `docs/opportunity_strategies_20260330/result_01_mainline_signal_convergence.md`

### 强制实际验证要求

- 必须使用 `/Users/fengzhi/Downloads/git/testlixingren/skills/joinquant_strategy`
- 必须测试静态权重 + 动态路由两种组合方式
- 必须对比组合效果 vs 单策略

### 结果归档要求

- 结果文档必须写入：`/Users/fengzhi/Downloads/git/testlixingren/docs/smallcap_state_router_20260330`
- 建议结果文件名：`result_09_defense_offense_combination.md`
- 跑完后必须同步更新：`/Users/fengzhi/Downloads/git/testlixingren/docs/smallcap_state_router_20260330/00_summary.md`

### 交付物

1. 静态权重组合测试结果
2. 动态路由组合测试结果
3. 组合方案推荐

## 子任务提示词

```text
你现在负责验证防守线 + 进攻线的组合效果。

请优先阅读：
- docs/parallel_strategy_tasks_20260328_round3_rfscore_pb10/result_07_rfscore_dividend_smallcap_full_backtest.md（组合经验）

强制要求：
- 必须用 /Users/fengzhi/Downloads/git/testlixingren/skills/joinquant_strategy
- 结果文档必须写到 /Users/fengzhi/Downloads/git/testlixingren/docs/smallcap_state_router_20260330/result_09_defense_offense_combination.md
- 跑完后必须回填 /Users/fengzhi/Downloads/git/testlixingren/docs/smallcap_state_router_20260330/00_summary.md

请完成：

【策略定义】
1. 防守线：小市值防守线 v1（从任务05获取最优方案）
2. 进攻线：首板低开（从任务03获取）

【组合方式】

方式A：静态权重
- 防守线 70% + 进攻线 30%
- 防守线 60% + 进攻线 40%
- 防守线 50% + 进攻线 50%
- 防守线 40% + 进攻线 60%

方式B：动态路由
- 极弱状态：空仓
- 弱状态：仅防守线，仓位30%
- 中状态：防守线70% + 进攻线30%，仓位50%
- 强状态：防守线50% + 进攻线50%，仓位70%
- 高潮状态：防守线30% + 进攻线70%，仓位90%

【验证范围】
- 样本期：2020-01-01 至 2025-03-30
- IS/OOS：前60%为IS，后40%为OOS

【对比指标】
- IS年化收益、OOS年化收益
- IS最大回撤、OOS最大回撤
- IS夏普、OOS夏普
- 年度胜率
- 与单策略对比

【关键问题】
1. 静态权重组合是否会稀释 alpha？
2. 动态路由组合是否优于静态权重？
3. 组合后的回撤是否显著降低？
4. 最优组合方式是什么？

输出要求：
- 必须有静态权重组合测试结果表
- 必须有动态路由组合测试结果表
- 必须对比组合效果 vs 单策略
- 必须给出组合方案推荐（静态权重 vs 动态路由，具体参数）
```
