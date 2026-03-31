# 任务 04：二板接力跨周期验证

## 设计文档

### 任务定位

- 聚焦方向：`小市值进攻线 - 二板接力`
- 目标：验证二板接力策略是否存在"策略生命周期"问题，确认是否跨周期稳定

### 当前已知问题

- 弱转强策略在 2022 年有效、2023 年失效，说明短线策略可能有生命周期
- 不清楚二板接力是否存在类似问题
- 需要验证 2021-2023 全样本表现，确认是否能跨周期存活

### 参考材料

- `docs/opportunity_strategies_20260330/dispatch_prompts_20260330_v2/07_v2_主线二板组合测试.md`
- `聚宽有价值策略558/` 目录下的二板策略

### 强制实际验证要求

- 必须使用 `/Users/fengzhi/Downloads/git/testlixingren/skills/joinquant_strategy`
- 必须覆盖 2021-01-01 至 2025-03-30 全样本
- 必须做年度切片分析（2021, 2022, 2023, 2024, 2025）

### 结果归档要求

- 结果文档必须写入：`/Users/fengzhi/Downloads/git/testlixingren/docs/smallcap_state_router_20260330`
- 建议结果文件名：`result_04_secondboard_cross_cycle_validation.md`
- 跑完后必须同步更新：`/Users/fengzhi/Downloads/git/testlixingren/docs/smallcap_state_router_20260330/00_summary.md`

### 交付物

1. 2021-2025 年度收益对比表
2. 策略稳定性判定（跨周期有效 / 单周期有效 / 已失效）
3. 是否纳入进攻线的建议

## 子任务提示词

```text
你现在负责验证二板接力策略的跨周期稳定性。

请优先阅读：
- docs/opportunity_strategies_20260330/dispatch_prompts_20260330_v2/07_v2_主线二板组合测试.md
- 聚宽有价值策略558/ 目录下的二板策略

强制要求：
- 必须用 /Users/fengzhi/Downloads/git/testlixingren/skills/joinquant_strategy
- 结果文档必须写到 /Users/fengzhi/Downloads/git/testlixingren/docs/smallcap_state_router_20260330/result_04_secondboard_cross_cycle_validation.md
- 跑完后必须回填 /Users/fengzhi/Downloads/git/testlixingren/docs/smallcap_state_router_20260330/00_summary.md

请完成：

【信号定义】
- 二板：首板次日继续涨停
- 主线关联：属于当前市场主线板块（可选，单独说明）
- 流通市值：<30亿（可分层测试）

【退出方式】
测试两种：
1. 次日最高价卖出
2. 次日收盘价卖出

【验证范围】
- 全样本：2021-01-01 至 2025-03-30
- 年度切片：2021, 2022, 2023, 2024, 2025

【对比指标】
- 每年信号数量
- 每年平均收益
- 每年胜率
- 每年最大回撤
- 每年夏普比率

【关键问题】
1. 是否存在某一年显著失效？
2. 收益是否逐年下降（衰减趋势）？
3. 信号数量是否逐年减少（拥挤信号）？

输出要求：
- 必须有年度对比表（2021-2025）
- 必须给出策略稳定性判定：
  - ✅ 跨周期稳定：所有年度均为正收益
  - ⚠️ 部分失效：1-2个年度为负，但整体仍为正
  - ❌ 已失效：多个年度为负，或整体已负
- 必须给出是否纳入进攻线的建议
```
