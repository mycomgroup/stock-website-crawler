# 任务 07：RFScore + 红利小盘完整组合回测

## 设计文档

### 任务定位

- 聚焦方向：`RFScore PB10` 主线
- 目标：把之前带推算成分的双策略组合，补成真实完整回测

### 当前已知问题

- 组合逻辑很有吸引力
- 但之前的组合报告里明确写了部分结果是推算值，不够硬

### 参考材料

- `docs/parallel_strategy_tasks_20260328/03_红利小盘防守线实盘化报告_2026-03-28.md`
- `docs/parallel_strategy_tasks_20260328/04_rfscore_dividend_combo_validation.md`
- `strategies/rfscore7_pb10_final.py`

### 强制实际验证要求

- 必须使用 `/Users/fengzhi/Downloads/git/testlixingren/skills/joinquant_strategy` 做真实组合回测
- 必须使用 `/Users/fengzhi/Downloads/git/testlixingren/skills/joinquant_nookbook` 输出当前双边候选

### 结果归档要求

- 结果文档必须写入：`/Users/fengzhi/Downloads/git/testlixingren/docs/parallel_strategy_tasks_20260328_round3_rfscore_pb10`
- 建议结果文件名：`result_07_rfscore_dividend_smallcap_full_backtest.md`
- 跑完后必须同步更新：`/Users/fengzhi/Downloads/git/testlixingren/docs/parallel_strategy_tasks_20260328_round3_rfscore_pb10/00_round3_summary.md`

### 交付物

1. 一份真实组合回测报告
2. 一张 `70/30`、`60/40`、`50/50`、动态权重对比表
3. 一个最终结论：这条组合是否值得替代 ETF 观察仓

## 子任务提示词

```text
你现在负责 RFScore PB10 + 红利小盘双策略组合的完整回测。

请优先阅读：
- docs/parallel_strategy_tasks_20260328/03_红利小盘防守线实盘化报告_2026-03-28.md
- docs/parallel_strategy_tasks_20260328/04_rfscore_dividend_combo_validation.md
- strategies/rfscore7_pb10_final.py

强制要求：
- 必须用 /Users/fengzhi/Downloads/git/testlixingren/skills/joinquant_strategy 做真实组合回测
- 必须用 /Users/fengzhi/Downloads/git/testlixingren/skills/joinquant_nookbook 输出当前候选
- 结果文档必须写到 /Users/fengzhi/Downloads/git/testlixingren/docs/parallel_strategy_tasks_20260328_round3_rfscore_pb10/result_07_rfscore_dividend_smallcap_full_backtest.md
- 跑完后必须回填 /Users/fengzhi/Downloads/git/testlixingren/docs/parallel_strategy_tasks_20260328_round3_rfscore_pb10/00_round3_summary.md

请完成：
1. 补齐真实回测
2. 比较静态与动态权重
3. 判断是否替代 ETF 观察仓

输出要求：
- 不允许再出现“推算值”
- 必须给唯一推荐版本
```
