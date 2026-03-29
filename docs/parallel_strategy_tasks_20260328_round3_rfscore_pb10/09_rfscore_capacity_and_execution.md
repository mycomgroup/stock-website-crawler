# 任务 09：RFScore 容量、成本与执行仿真

## 设计文档

### 任务定位

- 聚焦方向：`RFScore PB10` 主线
- 目标：把这条主线从“能回测”推进到“能承受多大真实仓位”

### 当前已知问题

- 压力测试已经说 PB10 可以做大仓
- 但也出现了明显值得复核的数据异常，例如某些规模统计看起来不合理

### 参考材料

- `docs/parallel_strategy_tasks_20260328/10_压力测试结果_20260328.md`
- `tmp/rfscore7_current_candidates.py`
- `tmp/rfscore7_candidate_industry.py`
- `strategies/rfscore7_pb10_final.py`

### 强制实际验证要求

- 必须使用 `/Users/fengzhi/Downloads/git/testlixingren/skills/joinquant_nookbook` 获取真实成交额与候选股分布
- 必须使用 `/Users/fengzhi/Downloads/git/testlixingren/skills/joinquant_strategy` 做不同成本和仓位规模回测

### 结果归档要求

- 结果文档必须写入：`/Users/fengzhi/Downloads/git/testlixingren/docs/parallel_strategy_tasks_20260328_round3_rfscore_pb10`
- 建议结果文件名：`result_09_rfscore_capacity_and_execution.md`
- 跑完后必须同步更新：`/Users/fengzhi/Downloads/git/testlixingren/docs/parallel_strategy_tasks_20260328_round3_rfscore_pb10/00_round3_summary.md`

### 交付物

1. 一份容量与执行仿真报告
2. 一张建议仓位上限表
3. 一份需修正的数据异常清单

## 子任务提示词

```text
你现在负责 RFScore PB10 的容量、成本与执行仿真。

请优先阅读：
- docs/parallel_strategy_tasks_20260328/10_压力测试结果_20260328.md
- tmp/rfscore7_current_candidates.py
- tmp/rfscore7_candidate_industry.py
- strategies/rfscore7_pb10_final.py

强制要求：
- 必须用 /Users/fengzhi/Downloads/git/testlixingren/skills/joinquant_nookbook 获取当前成交额和候选分布
- 必须用 /Users/fengzhi/Downloads/git/testlixingren/skills/joinquant_strategy 做不同成本与不同仓位规模回测
- 结果文档必须写到 /Users/fengzhi/Downloads/git/testlixingren/docs/parallel_strategy_tasks_20260328_round3_rfscore_pb10/result_09_rfscore_capacity_and_execution.md
- 跑完后必须回填 /Users/fengzhi/Downloads/git/testlixingren/docs/parallel_strategy_tasks_20260328_round3_rfscore_pb10/00_round3_summary.md

请完成：
1. 复核压力测试结果
2. 给出 PB10 的建议仓位上限
3. 找出压力测试里可能的数据异常

输出要求：
- 必须告诉我这条线到底能上多大仓
- 数据异常不能忽略
```
