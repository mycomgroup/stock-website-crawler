# 任务 01：RFScore 数据口径与候选股异常审计

## 设计文档

### 任务定位

- 聚焦方向：`RFScore PB10` 主线
- 目标：把 notebook、临时脚本、正式策略里的口径彻底对齐，先消灭“数据和定义不一致”

### 当前已知问题

- `PB10` 已经胜出，但不同报告里仍混着 `PB20`
- 当前候选股里出现了 `PE 657`、超低 `ROE` 之类的异常值
- `tmp/` 里已经有多份 RFScore 测试脚本，说明这条线的定义和过滤还在漂

### 参考材料

- `docs/parallel_strategy_tasks_20260328/11_rfscore7_pb10_upgrade_report.md`
- `strategies/rfscore7_pb10_final.py`
- `tmp/test_rfscore_pb10.py`
- `tmp/rfscore7_current_candidates.py`
- `tmp/rfscore7_candidate_industry.py`

### 强制实际验证要求

- 必须使用 `/Users/fengzhi/Downloads/git/testlixingren/skills/joinquant_nookbook`
- 必须使用 `/Users/fengzhi/Downloads/git/testlixingren/skills/joinquant_strategy`
- 必须输出一份“口径对齐清单”和一份“异常候选股清单”

### 结果归档要求

- 结果文档必须写入：`/Users/fengzhi/Downloads/git/testlixingren/docs/parallel_strategy_tasks_20260328_round3_rfscore_pb10`
- 建议结果文件名：`result_01_rfscore_data_parity_and_sanity.md`
- 跑完后必须同步更新：`/Users/fengzhi/Downloads/git/testlixingren/docs/parallel_strategy_tasks_20260328_round3_rfscore_pb10/00_round3_summary.md`

### 交付物

1. 一份 RFScore 正式定义文档
2. 一份候选股异常审计表
3. 一份“该保留/该剔除”的候选股规则

## 子任务提示词

```text
你现在负责 RFScore PB10 主线的第一道关：数据口径与异常值审计。

请优先阅读：
- docs/parallel_strategy_tasks_20260328/11_rfscore7_pb10_upgrade_report.md
- strategies/rfscore7_pb10_final.py
- tmp/test_rfscore_pb10.py
- tmp/rfscore7_current_candidates.py
- tmp/rfscore7_candidate_industry.py

强制要求：
- 必须用 /Users/fengzhi/Downloads/git/testlixingren/skills/joinquant_nookbook 跑当前候选股快照
- 必须用 /Users/fengzhi/Downloads/git/testlixingren/skills/joinquant_strategy 复核正式策略结果
- 结果文档必须写到 /Users/fengzhi/Downloads/git/testlixingren/docs/parallel_strategy_tasks_20260328_round3_rfscore_pb10/result_01_rfscore_data_parity_and_sanity.md
- 跑完后必须回填 /Users/fengzhi/Downloads/git/testlixingren/docs/parallel_strategy_tasks_20260328_round3_rfscore_pb10/00_round3_summary.md

请完成：
1. 对齐 RFScore 的正式定义
2. 检查候选股里是否存在明显异常值
3. 给出异常处理规则

输出要求：
- 先列出当前最大的不一致点
- 必须给出“正式口径”
- 异常值不能只指出，必须给处理建议
```
