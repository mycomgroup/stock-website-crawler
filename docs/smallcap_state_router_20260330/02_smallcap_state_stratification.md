# 任务 02：小市值状态分层基线研究

## 设计文档

### 任务定位

- 聚焦方向：`小市值状态依赖性研究`
- 目标：验证小市值策略是否存在明显的"市场状态依赖"，确定哪些状态下有效/失效

### 当前已知问题

- 已有证据显示情绪指标（涨停数）对短线策略有效，但不确定是否对"小市值因子本身"有效
- 不清楚在强/弱市场、情绪冰点/高潮时，小市值表现差异有多大
- 缺乏对小市值"何时停手"的硬规则验证

### 参考材料

- `docs/opportunity_strategies_20260330/result_01_mainline_signal_convergence.md`（情绪开关部分）
- `docs/opportunity_strategies_20260330/dispatch_prompts_20260330_v2/08_v2_停手机制实测验证.md`

### 强制实际验证要求

- 必须使用 `/Users/fengzhi/Downloads/git/testlixingren/skills/joinquant_strategy`
- 必须同时测试：市场广度分层 + 情绪分层
- 必须对比"有状态过滤" vs "无状态过滤"的差异

### 结果归档要求

- 结果文档必须写入：`/Users/fengzhi/Downloads/git/testlixingren/docs/smallcap_state_router_20260330`
- 建议结果文件名：`result_02_smallcap_state_stratification.md`
- 跑完后必须同步更新：`/Users/fengzhi/Downloads/git/testlixingren/docs/smallcap_state_router_20260330/00_summary.md`

### 交付物

1. 市场广度分层下的收益对比表
2. 情绪分层下的收益对比表
3. "状态过滤提升效果"量化评估
4. 推荐的状态开关规则

## 子任务提示词

```text
你现在负责小市值状态依赖性研究。

请优先阅读：
- docs/opportunity_strategies_20260330/result_01_mainline_signal_convergence.md（情绪开关部分）
- docs/opportunity_strategies_20260330/dispatch_prompts_20260330_v2/08_v2_停手机制实测验证.md

强制要求：
- 必须用 /Users/fengzhi/Downloads/git/testlixingren/skills/joinquant_strategy
- 结果文档必须写到 /Users/fengzhi/Downloads/git/testlixingren/docs/smallcap_state_router_20260330/result_02_smallcap_state_stratification.md
- 跑完后必须回填 /Users/fengzhi/Downloads/git/testlixingren/docs/smallcap_state_router_20260330/00_summary.md

请完成：

【市场广度分层】
基于沪深300站上20日均线占比，分为四档：
- 极弱（<15%）
- 弱（15%-25%）
- 中（25%-35%）
- 强（≥35%）

在每一档下，测试：
- 5-30亿流通市值组的收益/回撤
- 对比"有广度过滤" vs "无广度过滤"的差异

【情绪分层】
基于当日涨停数，分为四档：
- 冰点（<30）
- 启动（30-50）
- 发酵（50-80）
- 高潮（>80）

在每一档下，测试：
- 5-30亿流通市值组的收益/回撤
- 对比"有情绪过滤" vs "无情绪过滤"的差异

【关键问题】
1. 小市值在"极弱市场"是否系统性失效？
2. 情绪冰点时是否必须完全停手？
3. 状态过滤能否显著降低回撤？

输出要求：
- 必须有两张分层对比表（广度/情绪）
- 必须给出"状态过滤提升效果"的量化指标（收益提升%、回撤降低%）
- 必须给出初步的状态开关规则建议
```
