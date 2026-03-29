# 任务 08：RFScore + 防守底仓完整组合回测

## 设计文档

### 任务定位

- 聚焦方向：`RFScore PB10` 主线
- 目标：把 RFScore 与“国债固收+ / 现金防守”组合跑成真实回测，不再停留在配置建议

### 当前已知问题

- 防守底仓报告里还写着“聚宽 session 可能过期，未能运行正式回测”
- 这意味着当前防守层的结论证据还不够硬

### 参考材料

- `docs/parallel_strategy_tasks_20260328/防守底仓策略验证报告_2026-03-28.md`
- `docs/parallel_strategy_tasks_20260328/10_压力测试结果_20260328.md`
- `strategies/rfscore7_pb10_final.py`
- `simplified_fixed_income_plus.py`

### 强制实际验证要求

- 必须使用 `/Users/fengzhi/Downloads/git/testlixingren/skills/joinquant_strategy` 做完整组合回测
- 必须使用 `/Users/fengzhi/Downloads/git/testlixingren/skills/joinquant_nookbook` 验证当前防守层状态

### 结果归档要求

- 结果文档必须写入：`/Users/fengzhi/Downloads/git/testlixingren/docs/parallel_strategy_tasks_20260328_round3_rfscore_pb10`
- 建议结果文件名：`result_08_rfscore_defensive_base_full_backtest.md`
- 跑完后必须同步更新：`/Users/fengzhi/Downloads/git/testlixingren/docs/parallel_strategy_tasks_20260328_round3_rfscore_pb10/00_round3_summary.md`

### 交付物

1. 一份真实的 RFScore + 防守底仓回测报告
2. 一张和 “RFScore + 红利小盘” 的正面对比表
3. 一个结论：股票防守更好，还是债券/现金防守更好

## 子任务提示词

```text
你现在负责 RFScore PB10 + 防守底仓组合的完整回测。

请优先阅读：
- docs/parallel_strategy_tasks_20260328/防守底仓策略验证报告_2026-03-28.md
- docs/parallel_strategy_tasks_20260328/10_压力测试结果_20260328.md
- strategies/rfscore7_pb10_final.py
- simplified_fixed_income_plus.py

强制要求：
- 必须用 /Users/fengzhi/Downloads/git/testlixingren/skills/joinquant_strategy 做真实组合回测
- 必须用 /Users/fengzhi/Downloads/git/testlixingren/skills/joinquant_nookbook 验证当前状态
- 结果文档必须写到 /Users/fengzhi/Downloads/git/testlixingren/docs/parallel_strategy_tasks_20260328_round3_rfscore_pb10/result_08_rfscore_defensive_base_full_backtest.md
- 跑完后必须回填 /Users/fengzhi/Downloads/git/testlixingren/docs/parallel_strategy_tasks_20260328_round3_rfscore_pb10/00_round3_summary.md

请完成：
1. 补齐正式回测
2. 比较国债固收+、纯国债、现金防守
3. 与红利小盘防守方案正面对比

输出要求：
- 必须回答哪个防守层更适合搭配 RFScore
- 不允许只有逻辑分析，没有实证
```
