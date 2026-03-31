# 任务 07：情绪指标精细化阈值搜索

## 设计文档

### 任务定位

- 聚焦方向：`情绪指标精细化`
- 目标：搜索涨停数阈值的最优分段点，替代当前的粗粒度 30/50 阈值

### 当前已知问题

- 当前使用涨停数 30/50 作为阈值，但缺乏精细化验证
- 不清楚 25-60 区间内是否存在更优分段点
- 不清楚不同阈值对不同策略（防守线 vs 进攻线）的影响差异

### 参考材料

- `docs/opportunity_strategies_20260330/result_01_mainline_signal_convergence.md`（情绪开关部分）
- `docs/opportunity_strategies_20260330/dispatch_prompts_20260330_v2/06_v2_情绪开关阈值优化.md`

### 强制实际验证要求

- 必须使用 `/Users/fengzhi/Downloads/git/testlixingren/skills/joinquant_strategy`
- 必须搜索 25-60 区间的多个阈值点
- 必须对比不同阈值对防守线/进攻线的影响

### 结果归档要求

- 结果文档必须写入：`/Users/fengzhi/Downloads/git/testlixingren/docs/smallcap_state_router_20260330`
- 建议结果文件名：`result_07_sentiment_threshold_optimization.md`
- 跑完后必须同步更新：`/Users/fengzhi/Downloads/git/testlixingren/docs/smallcap_state_router_20260330/00_summary.md`

### 交付物

1. 阈值搜索结果表
2. 最优阈值推荐（防守线 vs 进攻线）
3. 是否需要差异化阈值的建议

## 子任务提示词

```text
你现在负责情绪指标阈值的精细化搜索。

请优先阅读：
- docs/opportunity_strategies_20260330/result_01_mainline_signal_convergence.md（情绪开关部分）

强制要求：
- 必须用 /Users/fengzhi/Downloads/git/testlixingren/skills/joinquant_strategy
- 结果文档必须写到 /Users/fengzhi/Downloads/git/testlixingren/docs/smallcap_state_router_20260330/result_07_sentiment_threshold_optimization.md
- 跑完后必须回填 /Users/fengzhi/Downloads/git/testlixingren/docs/smallcap_state_router_20260330/00_summary.md

请完成：

【搜索范围】
涨停数阈值：
- 冰点线：测试 20, 25, 30, 35
- 启动线：测试 40, 45, 50, 55, 60

【测试策略】
1. 小市值防守线（月度调仓，15-60亿市值）
2. 首板低开（短线事件驱动）

【验证方式】
在 2020-01-01 至 2025-03-30 样本期：
- 对每个阈值组合，测试：
  - "只在阈值以上交易" vs "无过滤"
  - 收益提升%
  - 回撤降低%
  - 信号损失率（因过滤而错过的机会比例）

【对比指标】
- 日均收益
- 最大回撤
- 夏普比率
- 信号数量（被保留的比例）

【关键问题】
1. 最优冰点线是多少？（20/25/30/35）
2. 最优启动线是多少？（40/45/50/55/60）
3. 防守线和进攻线是否需要不同的阈值？
4. 过高的阈值是否会过度损失机会？

输出要求：
- 必须有阈值搜索结果表（每种组合的效果）
- 必须给出最优阈值推荐
- 必须说明防守线/进攻线是否需要差异化阈值
```
