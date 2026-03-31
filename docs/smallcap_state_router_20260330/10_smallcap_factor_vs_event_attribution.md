# 任务 10：小市值因子 vs 事件策略归因分析

## 设计文档

### 任务定位

- 聚焦方向：`归因分析`
- 目标：拆解小市值策略收益来源，判断是"因子暴露"还是"事件驱动"

### 当前已知问题

- 不清楚首板低开、二板接力的收益有多少来自"小市值因子暴露"，有多少来自"事件信号"
- 不清楚如果剥离事件信号，纯小市值因子是否仍有 alpha
- 这是理解策略本质的关键问题

### 参考材料

- `docs/opportunity_strategies_20260330/result_01_mainline_signal_convergence.md`
- `docs/parallel_strategy_tasks_20260328_round3_rfscore_pb10/` 归因分析经验

### 强制实际验证要求

- 必须使用 `/Users/fengzhi/Downloads/git/testlixingren/skills/joinquant_strategy`
- 必须对比"纯小市值因子" vs "小市值+事件" vs "纯事件"三种策略
- 必须做收益归因分解

### 结果归档要求

- 结果文档必须写入：`/Users/fengzhi/Downloads/git/testlixingren/docs/smallcap_state_router_20260330`
- 建议结果文件名：`result_10_smallcap_factor_vs_event_attribution.md`
- 跑完后必须同步更新：`/Users/fengzhi/Downloads/git/testlixingren/docs/smallcap_state_router_20260330/00_summary.md`

### 交付物

1. 三种策略的收益对比表
2. 收益归因分解
3. 策略本质判定（因子驱动 vs 事件驱动 vs 混合）

## 子任务提示词

```text
你现在负责小市值因子 vs 事件策略的归因分析。

请优先阅读：
- docs/opportunity_strategies_20260330/result_01_mainline_signal_convergence.md

强制要求：
- 必须用 /Users/fengzhi/Downloads/git/testlixingren/skills/joinquant_strategy
- 结果文档必须写到 /Users/fengzhi/Downloads/git/testlixingren/docs/smallcap_state_router_20260330/result_10_smallcap_factor_vs_event_attribution.md
- 跑完后必须回填 /Users/fengzhi/Downloads/git/testlixingren/docs/smallcap_state_router_20260330/00_summary.md

请完成：

【三种策略定义】

策略A：纯小市值因子
- 选股：流通市值最小的前10%
- 无事件信号
- 月度等权调仓
- 持仓20只

策略B：小市值 + 事件（首板低开）
- 选股：流通市值5-15亿 + 首板 + 低开
- 次日退出
- 持仓1只（每日最多1个信号）

策略C：纯事件（全市场首板低开）
- 选股：全市场首板 + 低开（不限制市值）
- 次日退出
- 持仓1只

【验证范围】
- 样本期：2022-01-01 至 2025-03-30（首板低开策略的有效期）
- 年度切片：2022, 2023, 2024, 2025

【对比指标】
- 年化收益
- 最大回撤
- 夏普比率
- 年度收益

【归因分解】
假设策略B的收益 = 因子收益 + 事件收益 + 交互收益

估算：
- 因子收益 ≈ 策略A收益
- 事件收益 ≈ 策略C收益
- 交互收益 ≈ 策略B收益 - 策略A收益 - 策略C收益

【关键问题】
1. 首板低开策略的收益，有多少来自"小市值因子暴露"？
2. 如果剥离小市值条件（策略C），纯事件是否仍有 alpha？
3. 小市值 + 事件的组合是否存在协同效应（交互收益为正）？

输出要求：
- 必须有三种策略的对比表
- 必须有收益归因分解（因子/事件/交互）
- 必须给出策略本质判定：
  - 因子驱动：因子收益占比 > 60%
  - 事件驱动：事件收益占比 > 60%
  - 混合驱动：两者均显著，且交互收益为正
- 必须说明这对"下一步研究重点"的启示
```
