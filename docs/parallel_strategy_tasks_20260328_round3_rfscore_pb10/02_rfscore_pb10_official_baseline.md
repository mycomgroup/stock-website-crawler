# 任务 02：RFScore PB10 正式基线封版

## 设计文档

### 任务定位

- 聚焦方向：`RFScore PB10` 主线
- 目标：把 `PB10` 版本做成唯一的正式基线，不再允许 PB20 / PB15 / 临时版混用

### 当前已知问题

- `PB10` 已有强证据，但当前仓库里还有多个版本并存
- 需要一个“正式基线回测文件 + 正式当前快照 + 正式策略文件”

### 参考材料

- `docs/parallel_strategy_tasks_20260328/11_rfscore7_pb10_upgrade_report.md`
- `strategies/rfscore7_pb10_final.py`
- `tmp/rfscore7_variant_eval.py`
- `tmp/rfscore7_refine_eval.py`

### 强制实际验证要求

- 必须使用 `/Users/fengzhi/Downloads/git/testlixingren/skills/joinquant_strategy` 跑正式回测
- 必须使用 `/Users/fengzhi/Downloads/git/testlixingren/skills/joinquant_nookbook` 输出当前候选与市场状态
- 必须给出一个“正式采用版本”的文件与结果路径

### 结果归档要求

- 结果文档必须写入：`/Users/fengzhi/Downloads/git/testlixingren/docs/parallel_strategy_tasks_20260328_round3_rfscore_pb10`
- 建议结果文件名：`result_02_rfscore_pb10_official_baseline.md`
- 跑完后必须同步更新：`/Users/fengzhi/Downloads/git/testlixingren/docs/parallel_strategy_tasks_20260328_round3_rfscore_pb10/00_round3_summary.md`

### 交付物

1. PB10 正式回测报告
2. 当前市场 PB10 正式候选池
3. 封版说明：正式文件、参数、适用场景

## 子任务提示词

```text
你现在负责把 RFScore PB10 封成正式基线。

请优先阅读：
- docs/parallel_strategy_tasks_20260328/11_rfscore7_pb10_upgrade_report.md
- strategies/rfscore7_pb10_final.py
- tmp/rfscore7_variant_eval.py
- tmp/rfscore7_refine_eval.py

强制要求：
- 必须用 /Users/fengzhi/Downloads/git/testlixingren/skills/joinquant_strategy 做正式回测
- 必须用 /Users/fengzhi/Downloads/git/testlixingren/skills/joinquant_nookbook 产出当前快照
- 结果文档必须写到 /Users/fengzhi/Downloads/git/testlixingren/docs/parallel_strategy_tasks_20260328_round3_rfscore_pb10/result_02_rfscore_pb10_official_baseline.md
- 跑完后必须回填 /Users/fengzhi/Downloads/git/testlixingren/docs/parallel_strategy_tasks_20260328_round3_rfscore_pb10/00_round3_summary.md

请完成：
1. 确认 PB10 是否仍是正式最优版本
2. 输出正式回测与当前候选
3. 写清“以后谁是官方版本”

输出要求：
- 结论必须唯一，不要给多个并列候选
- 必须有正式文件路径
- 必须说明当前是否适合直接上模拟盘/实盘跟踪
```
