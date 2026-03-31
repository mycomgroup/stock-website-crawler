# 任务 08：小市值事件策略容量与滑点测试

## 设计文档

### 任务定位

- 聚焦方向：`小市值事件策略真实化`
- 目标：评估首板低开/二板接力策略的真实容量与滑点敏感度

### 当前已知问题

- 已验证首板低开策略收益优异，但缺乏容量与滑点测试
- 不清楚策略能承载多大规模资金
- 不清楚滑点对收益的侵蚀程度

### 参考材料

- `docs/opportunity_strategies_20260330/result_01_mainline_signal_convergence.md`（首板低开部分）
- `docs/parallel_strategy_tasks_20260328_round3_rfscore_pb10/result_09_rfscore_capacity_and_execution.md`（RFScore 容量测试经验）

### 强制实际验证要求

- 必须使用 `/Users/fengzhi/Downloads/git/testlixingren/skills/joinquant_strategy`
- 必须测试不同规模下的收益变化
- 必须测试不同滑点假设下的收益变化

### 结果归档要求

- 结果文档必须写入：`/Users/fengzhi/Downloads/git/testlixingren/docs/smallcap_state_router_20260330`
- 建议结果文件名：`result_08_smallcap_event_capacity_slippage.md`
- 跑完后必须同步更新：`/Users/fengzhi/Downloads/git/testlixingren/docs/smallcap_state_router_20260330/00_summary.md`

### 交付物

1. 容量测试结果（不同规模下的收益变化）
2. 滑点敏感度测试结果
3. 推荐容量上限与滑点假设

## 子任务提示词

```text
你现在负责评估小市值事件策略的容量与滑点敏感度。

请优先阅读：
- docs/opportunity_strategies_20260330/result_01_mainline_signal_convergence.md（首板低开部分）
- docs/parallel_strategy_tasks_20260328_round3_rfscore_pb10/result_09_rfscore_capacity_and_execution.md（RFScore 容量测试经验）

强制要求：
- 必须用 /Users/fengzhi/Downloads/git/testlixingren/skills/joinquant_strategy
- 结果文档必须写到 /Users/fengzhi/Downloads/git/testlixingren/docs/smallcap_state_router_20260330/result_08_smallcap_event_capacity_slippage.md
- 跑完后必须回填 /Users/fengzhi/Downloads/git/testlixingren/docs/smallcap_state_router_20260330/00_summary.md

请完成：

【策略范围】
1. 首板低开（流通市值5-15亿）
2. 二板接力（流通市值<30亿）

【容量测试】
测试以下规模下的收益变化：
- 10万
- 50万
- 100万
- 300万
- 500万
- 1000万

假设：
- 单票成交额占比不超过当日成交额的5%
- 超过限制的信号视为无法成交，排除

【滑点测试】
测试以下滑点假设下的收益变化：
- 0bps（理想）
- 10bps
- 20bps
- 30bps
- 50bps
- 100bps

【对比指标】
- 年化收益（不同规模）
- 年化收益（不同滑点）
- 信号成交率（能成交的比例）
- 收益衰减曲线

【关键问题】
1. 策略容量上限是多少？
2. 在多少规模下收益衰减超过20%？
3. 滑点达到多少时策略失效？
4. 首板低开 vs 二板接力，谁的容量更小？

输出要求：
- 必须有容量测试结果表
- 必须有滑点敏感度测试结果表
- 必须给出推荐容量上限
- 必须给出合理的滑点假设建议
```
