# 任务 05：小市值防守线 v1 设计

## 设计文档

### 任务定位

- 聚焦方向：`小市值防守线设计`
- 目标：做出一条能单独活下来的中频小市值策略，作为防守/底仓

### 当前已知问题

- 已有 RFScore PB10 作为大盘价值防守线，但缺乏"小市值防守线"
- 纯小市值策略回撤大、波动高，不适合直接做底仓
- 需要找到"小市值 + 质量/红利/低估值"的最优组合

### 参考材料

- `docs/parallel_strategy_tasks_20260328_round3_rfscore_pb10/` RFScore 防守线经验
- `docs/opportunity_strategies_20260330/dispatch_prompts_20260330_v2/` 相关任务

### 强制实际验证要求

- 必须使用 `/Users/fengzhi/Downloads/git/testlixingren/skills/joinquant_strategy`
- 必须覆盖 2018-01-01 至 2025-03-30 全样本
- 必须做 IS/OOS 分段验证

### 结果归档要求

- 结果文档必须写入：`/Users/fengzhi/Downloads/git/testlixingren/docs/smallcap_state_router_20260330`
- 建议结果文件名：`result_05_smallcap_defense_v1_design.md`
- 跑完后必须同步更新：`/Users/fengzhi/Downloads/git/testlixingren/docs/smallcap_state_router_20260330/00_summary.md`

### 交付物

1. 三种增强方案的对比回测（小市值+质量、小市值+红利、小市值+低估值）
2. 最优方案推荐
3. 是否达到"防守线标准"的判定

## 子任务提示词

```text
你现在负责设计小市值防守线 v1。

请优先阅读：
- docs/parallel_strategy_tasks_20260328_round3_rfscore_pb10/ （RFScore 防守线经验）

强制要求：
- 必须用 /Users/fengzhi/Downloads/git/testlixingren/skills/joinquant_strategy
- 结果文档必须写到 /Users/fengzhi/Downloads/git/testlixingren/docs/smallcap_state_router_20260330/result_05_smallcap_defense_v1_design.md
- 跑完后必须回填 /Users/fengzhi/Downloads/git/testlixingren/docs/smallcap_state_router_20260330/00_summary.md

请完成：

【基础池】
流通市值：15-60亿（从任务01的最优区间中取偏中区间，确保可交易性）

【三种增强方案】
1. 小市值 + 质量
   - 市值分位：最小30%
   - ROE > 8%
   - 经营现金流/净利润 > 0.8
   - 资产负债率 < 60%

2. 小市值 + 红利
   - 市值分位：最小30%
   - 股息率 > 2%
   - 分红稳定性：近3年连续分红

3. 小市值 + 低估值
   - 市值分位：最小30%
   - PB < 1.5
   - PE < 20

【回测参数】
- 样本期：2018-01-01 至 2025-03-30
- IS/OOS：前60%为IS，后40%为OOS
- 调仓频率：月度
- 持仓数量：15只
- 基准：中证1000

【对比指标】
- IS年化收益、OOS年化收益
- IS最大回撤、OOS最大回撤
- IS夏普、OOS夏普
- 换手率
- 平均成交额

【防守线标准】
- OOS年化超额 > 8%
- OOS最大回撤 <= 25%
- 至少60%的年度切片为正

输出要求：
- 必须有三种方案的对比表
- 必须给出最优方案推荐
- 必须明确判定是否达到"防守线标准"
- 如果三种方案均不达标，必须给出改进方向
```
