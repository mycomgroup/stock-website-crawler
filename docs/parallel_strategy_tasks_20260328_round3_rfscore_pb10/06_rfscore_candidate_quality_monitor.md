# 任务 06：RFScore 候选组合质量监控

## 设计文档

### 任务定位

- 聚焦方向：`RFScore PB10` 主线
- 目标：建立一套专门盯当前候选池质量的监控体系

### 当前已知问题

- 候选股里出现过极端估值与低质量异常
- 如果没有质量监控，主策略可能在弱市里慢慢漂到不想要的风格

### 参考材料

- `tmp/rfscore7_current_candidates.py`
- `tmp/rfscore7_candidate_industry.py`
- `docs/parallel_strategy_tasks_20260328/11_rfscore7_pb10_upgrade_report.md`

### 强制实际验证要求

- 必须使用 `/Users/fengzhi/Downloads/git/testlixingren/skills/joinquant_nookbook` 抓取当前与历史候选快照
- 必须输出真实监控指标与异常名单

### 结果归档要求

- 结果文档必须写入：`/Users/fengzhi/Downloads/git/testlixingren/docs/parallel_strategy_tasks_20260328_round3_rfscore_pb10`
- 建议结果文件名：`result_06_rfscore_candidate_quality_monitor.md`
- 跑完后必须同步更新：`/Users/fengzhi/Downloads/git/testlixingren/docs/parallel_strategy_tasks_20260328_round3_rfscore_pb10/00_round3_summary.md`

### 交付物

1. 一套候选质量监控指标
2. 一份当前候选组合体检结果
3. 一份异常触发规则

## 子任务提示词

```text
你现在负责 RFScore 候选组合的质量监控。

请优先阅读：
- tmp/rfscore7_current_candidates.py
- tmp/rfscore7_candidate_industry.py
- docs/parallel_strategy_tasks_20260328/11_rfscore7_pb10_upgrade_report.md

强制要求：
- 必须用 /Users/fengzhi/Downloads/git/testlixingren/skills/joinquant_nookbook 抓当前候选与历史快照
- 结果文档必须写到 /Users/fengzhi/Downloads/git/testlixingren/docs/parallel_strategy_tasks_20260328_round3_rfscore_pb10/result_06_rfscore_candidate_quality_monitor.md
- 跑完后必须回填 /Users/fengzhi/Downloads/git/testlixingren/docs/parallel_strategy_tasks_20260328_round3_rfscore_pb10/00_round3_summary.md

请完成：
1. 设计组合质量监控指标
2. 对当前候选做体检
3. 给出异常触发规则

输出要求：
- 必须告诉我当前组合到底“像不像我们想要的 RFScore 组合”
- 要有行业、估值、盈利质量、异常股提示
```
