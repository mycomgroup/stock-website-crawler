# 任务 03：RFScore 候选稀疏与备用池机制

## 设计文档

### 任务定位

- 聚焦方向：`RFScore PB10` 主线
- 目标：解决 PB10 太严格时候选不足、质量下降或被迫乱补仓的问题

### 当前已知问题

- PB10 候选更优，但在弱市场里可能不够多
- 当前策略里已有 `RFScore>=6 + PB20 次级池` 备用逻辑，但还没被真正打穿

### 参考材料

- `strategies/rfscore7_pb10_final.py`
- `tmp/rfscore7_variant_eval.py`
- `tmp/rfscore7_refine_eval.py`
- `docs/parallel_strategy_tasks_20260328/11_rfscore7_pb10_upgrade_report.md`

### 强制实际验证要求

- 必须使用 `/Users/fengzhi/Downloads/git/testlixingren/skills/joinquant_nookbook` 验证当前候选数量分布
- 必须使用 `/Users/fengzhi/Downloads/git/testlixingren/skills/joinquant_strategy` 比较不同备用池逻辑

### 结果归档要求

- 结果文档必须写入：`/Users/fengzhi/Downloads/git/testlixingren/docs/parallel_strategy_tasks_20260328_round3_rfscore_pb10`
- 建议结果文件名：`result_03_rfscore_backup_pool_and_sparse_handling.md`
- 跑完后必须同步更新：`/Users/fengzhi/Downloads/git/testlixingren/docs/parallel_strategy_tasks_20260328_round3_rfscore_pb10/00_round3_summary.md`

### 交付物

1. 一张候选稀疏场景对比表
2. 一套正式备用池规则
3. 一个结论：`20只 / 15只 / 10只` 哪个更稳

## 子任务提示词

```text
你现在负责 RFScore PB10 的备用池与稀疏处理。

请优先阅读：
- strategies/rfscore7_pb10_final.py
- tmp/rfscore7_variant_eval.py
- tmp/rfscore7_refine_eval.py
- docs/parallel_strategy_tasks_20260328/11_rfscore7_pb10_upgrade_report.md

强制要求：
- 必须用 /Users/fengzhi/Downloads/git/testlixingren/skills/joinquant_nookbook 查看不同月份的候选数量
- 必须用 /Users/fengzhi/Downloads/git/testlixingren/skills/joinquant_strategy 比较不同补位逻辑
- 结果文档必须写到 /Users/fengzhi/Downloads/git/testlixingren/docs/parallel_strategy_tasks_20260328_round3_rfscore_pb10/result_03_rfscore_backup_pool_and_sparse_handling.md
- 跑完后必须回填 /Users/fengzhi/Downloads/git/testlixingren/docs/parallel_strategy_tasks_20260328_round3_rfscore_pb10/00_round3_summary.md

请完成：
1. 比较 PB10 单独持仓
2. 比较 RFScore>=6 的备用池
3. 比较 PB10 + PB20 次级补位
4. 比较持仓数 10 / 15 / 20

输出要求：
- 必须回答“候选不足时怎么补最不伤策略”
- 不能只看收益，还要看质量下降程度
```
