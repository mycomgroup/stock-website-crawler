# 任务 03：首板低开最新 OOS 验证

## 设计文档

### 任务定位

- 聚焦方向：`小市值进攻线 - 首板低开`
- 目标：验证首板低开策略在 2025-04 至今的表现，确认是否衰减

### 当前已知问题

- 已验证首板低开在 2024-07 至 2025-03 表现优异（年化 139.7%）
- 但样本外时间偏短（仅 9 个月），需要持续验证
- 不清楚 2025 年后是否出现策略衰减或市场环境变化

### 参考材料

- `docs/opportunity_strategies_20260330/result_01_mainline_signal_convergence.md`（首板低开部分）
- `docs/opportunity_strategies_20260330/dispatch_prompts_20260330_v2/` 相关任务

### 强制实际验证要求

- 必须使用 `/Users/fengzhi/Downloads/git/testlixingren/skills/joinquant_strategy` 或 `ricequant_strategy`
- 必须覆盖 2025-04-01 至今的全样本
- 必须对比 2024-07 至 2025-03 的历史表现

### 结果归档要求

- 结果文档必须写入：`/Users/fengzhi/Downloads/git/testlixingren/docs/smallcap_state_router_20260330`
- 建议结果文件名：`result_03_firstboard_low_open_oos_2025.md`
- 跑完后必须同步更新：`/Users/fengzhi/Downloads/git/testlixingren/docs/smallcap_state_router_20260330/00_summary.md`

### 交付物

1. 2025-04 至今的信号统计与收益表现
2. 与历史期（2024-07 至 2025-03）的对比分析
3. 衰减判定与下一步建议

## 子任务提示词

```text
你现在负责验证首板低开策略的最新 OOS 表现。

请优先阅读：
- docs/opportunity_strategies_20260330/result_01_mainline_signal_convergence.md（首板低开部分）

强制要求：
- 必须用 /Users/fengzhi/Downloads/git/testlixingren/skills/joinquant_strategy 或 ricequant_strategy
- 结果文档必须写到 /Users/fengzhi/Downloads/git/testlixingren/docs/smallcap_state_router_20260330/result_03_firstboard_low_open_oos_2025.md
- 跑完后必须回填 /Users/fengzhi/Downloads/git/testlixingren/docs/smallcap_state_router_20260330/00_summary.md

请完成：

【信号定义】
- 首板：当日首次涨停（非连板）
- 低开：次日开盘价相对昨收价涨幅在 -2% ~ +1.5%
- 流通市值：5-15亿
- 15日位置：≤30%

【退出方式】
测试三种：
1. 次日最高价卖出
2. 次日收盘价卖出
3. 10:30 时间止损

【验证范围】
1. 历史期：2024-07-01 至 2025-03-31
2. 最新期：2025-04-01 至今

【对比指标】
- 信号数量（日均/总计）
- 单笔平均收益
- 胜率
- 盈亏比
- 年化收益（按日均信号推算）

【关键问题】
1. 2025-04 至今的日均收益是否显著下降？
2. 信号数量是否明显减少？
3. 是否出现连续亏损期？

输出要求：
- 必须有两期对比表（历史期 vs 最新期）
- 必须给出衰减判定（无明显衰减 / 轻度衰减 / 严重衰减）
- 如果衰减，必须分析可能原因（市场环境变化 / 策略拥挤 / 其他）
```
