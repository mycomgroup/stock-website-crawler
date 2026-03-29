# 任务 05：RFScore 主线的市场状态与仓位控制

## 设计文档

### 任务定位

- 聚焦方向：`RFScore PB10` 主线
- 目标：把这条线的仓位控制独立打穿，不再依赖模糊的“弱市少买一点”

### 当前已知问题

- 宽度阈值、持仓数和空仓线已经有初版
- 但还没形成一个经过系统回测的 RFScore 专属仓位控制规则

### 参考材料

- `strategies/rfscore7_pb10_final.py`
- `docs/parallel_strategy_tasks_20260328/11_macro_regime_router_validation.md`
- `docs/parallel_strategy_tasks_20260328/09_regime_router_v2_backtest_2026-03-28.md`

### 强制实际验证要求

- 必须使用 `/Users/fengzhi/Downloads/git/testlixingren/skills/joinquant_nookbook` 计算宽度、趋势和当前状态
- 必须使用 `/Users/fengzhi/Downloads/git/testlixingren/skills/joinquant_strategy` 比较不同仓位规则

### 结果归档要求

- 结果文档必须写入：`/Users/fengzhi/Downloads/git/testlixingren/docs/parallel_strategy_tasks_20260328_round3_rfscore_pb10`
- 建议结果文件名：`result_05_rfscore_market_state_sizing.md`
- 跑完后必须同步更新：`/Users/fengzhi/Downloads/git/testlixingren/docs/parallel_strategy_tasks_20260328_round3_rfscore_pb10/00_round3_summary.md`

### 交付物

1. 一张仓位控制对比表
2. 一套 RFScore 专属仓位规则
3. 一份当前市场仓位建议

## 子任务提示词

```text
你现在负责 RFScore PB10 的市场状态与仓位控制。

请优先阅读：
- strategies/rfscore7_pb10_final.py
- docs/parallel_strategy_tasks_20260328/11_macro_regime_router_validation.md
- docs/parallel_strategy_tasks_20260328/09_regime_router_v2_backtest_2026-03-28.md

强制要求：
- 必须用 /Users/fengzhi/Downloads/git/testlixingren/skills/joinquant_nookbook 计算宽度和趋势
- 必须用 /Users/fengzhi/Downloads/git/testlixingren/skills/joinquant_strategy 比较不同仓位控制
- 结果文档必须写到 /Users/fengzhi/Downloads/git/testlixingren/docs/parallel_strategy_tasks_20260328_round3_rfscore_pb10/result_05_rfscore_market_state_sizing.md
- 跑完后必须回填 /Users/fengzhi/Downloads/git/testlixingren/docs/parallel_strategy_tasks_20260328_round3_rfscore_pb10/00_round3_summary.md

请完成：
1. 测试不同宽度阈值
2. 测试不同减仓持股数
3. 测试是否需要空仓线

输出要求：
- 必须给 RFScore 专属仓位规则
- 不能只复用 ETF 的择时逻辑
```
