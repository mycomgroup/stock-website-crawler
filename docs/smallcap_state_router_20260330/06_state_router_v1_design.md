# 任务 06：状态路由器 v1 设计

## 设计文档

### 任务定位

- 聚焦方向：`状态路由器设计`
- 目标：将市场广度 + 情绪指标组合成统一的状态路由器，用于控制小市值策略的开关与仓位

### 当前已知问题

- 已有市场广度开关（沪深300站上20日线占比）和情绪开关（涨停数）
- 但缺乏两者的组合使用规则
- 不清楚如何映射到具体仓位/策略启停

### 参考材料

- `docs/opportunity_strategies_20260330/result_01_mainline_signal_convergence.md`（情绪开关部分）
- `docs/opportunity_strategies_20260330/dispatch_prompts_20260330_v2/08_v2_停手机制实测验证.md`

### 强制实际验证要求

- 必须使用 `/Users/fengzhi/Downloads/git/testlixingren/skills/joinquant_strategy`
- 必须在历史数据上验证状态路由器的效果
- 必须对比"有路由器" vs "无路由器"的差异

### 结果归档要求

- 结果文档必须写入：`/Users/fengzhi/Downloads/git/testlixingren/docs/smallcap_state_router_20260330`
- 建议结果文件名：`result_06_state_router_v1_design.md`
- 跑完后必须同步更新：`/Users/fengzhi/Downloads/git/testlixingren/docs/smallcap_state_router_20260330/00_summary.md`

### 交付物

1. 状态路由器规则表（状态 -> 仓位/策略）
2. 历史回测效果对比
3. 路由器提升效果量化评估

## 子任务提示词

```text
你现在负责设计状态路由器 v1。

请优先阅读：
- docs/opportunity_strategies_20260330/result_01_mainline_signal_convergence.md（情绪开关部分）
- docs/opportunity_strategies_20260330/dispatch_prompts_20260330_v2/08_v2_停手机制实测验证.md

强制要求：
- 必须用 /Users/fengzhi/Downloads/git/testlixingren/skills/joinquant_strategy
- 结果文档必须写到 /Users/fengzhi/Downloads/git/testlixingren/docs/smallcap_state_router_20260330/result_06_state_router_v1_design.md
- 跑完后必须回填 /Users/fengzhi/Downloads/git/testlixingren/docs/smallcap_state_router_20260330/00_summary.md

请完成：

【状态定义】
基于两个维度：
1. 市场广度（沪深300站上20日线占比）
   - 极弱（<15%）、弱（15%-25%）、中（25%-35%）、强（≥35%）
2. 情绪（涨停数）
   - 冰点（<30）、启动（30-50）、发酵（50-80）、高潮（>80）

组合成 4x4 = 16 种状态，但简化为以下 5 种：

| 状态 | 广度 | 情绪 | 操作 |
|------|------|------|------|
| 关闭 | 极弱 | 任意 | 空仓 |
| 防守 | 弱 | 冰点/启动 | 仅防守线，仓位30% |
| 轻仓 | 弱/中 | 启动/发酵 | 防守线+轻量进攻，仓位50% |
| 正常 | 中/强 | 发酵 | 防守线+进攻线，仓位70% |
| 进攻 | 强 | 高潮 | 满仓进攻线 |

【验证方式】
在 2018-01-01 至 2025-03-30 样本期：
1. 测试"有路由器"的收益/回撤
2. 测试"无路由器"（始终满仓）的收益/回撤
3. 对比差异

【对比指标】
- 年化收益
- 最大回撤
- 夏普比率
- 年度胜率（正收益年度占比）
- 换手率

【关键问题】
1. 路由器能否显著降低回撤？
2. 路由器是否会牺牲过多收益？
3. 是否存在"过度择时"导致错过机会的问题？

输出要求：
- 必须有状态路由器规则表
- 必须有"有路由器 vs 无路由器"对比表
- 必须给出路由器提升效果的量化评估
```
