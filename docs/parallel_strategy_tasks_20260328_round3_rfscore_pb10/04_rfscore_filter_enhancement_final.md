# 任务 04：RFScore 过滤器终审

## 设计文档

### 任务定位

- 聚焦方向：`RFScore PB10` 主线
- 目标：把已经试过的过滤器做终审，只留下真正值得接入正式版本的少数项

### 当前已知问题

- `tmp/final_rfscore_filters_test.py` 等脚本已经存在
- 但还没有形成清晰的“正式版到底接不接 turnover / CGO / 行业约束”的最终裁决

### 参考材料

- `tmp/final_rfscore_filters_test.py`
- `tmp/final_rfscore_filters_test_complete.py`
- `tmp/rfscore_filter_signals.py`
- `docs/parallel_strategy_tasks_20260328_round2/02_rfscore_filter_enhancement.md`

### 强制实际验证要求

- 必须使用 `/Users/fengzhi/Downloads/git/testlixingren/skills/joinquant_nookbook` 计算过滤信号
- 必须使用 `/Users/fengzhi/Downloads/git/testlixingren/skills/joinquant_strategy` 跑策略层回测

### 结果归档要求

- 结果文档必须写入：`/Users/fengzhi/Downloads/git/testlixingren/docs/parallel_strategy_tasks_20260328_round3_rfscore_pb10`
- 建议结果文件名：`result_04_rfscore_filter_enhancement_final.md`
- 跑完后必须同步更新：`/Users/fengzhi/Downloads/git/testlixingren/docs/parallel_strategy_tasks_20260328_round3_rfscore_pb10/00_round3_summary.md`

### 交付物

1. 一张过滤器终审表
2. 一份最终保留清单
3. 一份正式版拟接入规则

## 子任务提示词

```text
你现在负责 RFScore 过滤器终审。

请优先阅读：
- tmp/final_rfscore_filters_test.py
- tmp/final_rfscore_filters_test_complete.py
- tmp/rfscore_filter_signals.py

强制要求：
- 必须用 /Users/fengzhi/Downloads/git/testlixingren/skills/joinquant_nookbook 算信号
- 必须用 /Users/fengzhi/Downloads/git/testlixingren/skills/joinquant_strategy 跑策略层回测
- 结果文档必须写到 /Users/fengzhi/Downloads/git/testlixingren/docs/parallel_strategy_tasks_20260328_round3_rfscore_pb10/result_04_rfscore_filter_enhancement_final.md
- 跑完后必须回填 /Users/fengzhi/Downloads/git/testlixingren/docs/parallel_strategy_tasks_20260328_round3_rfscore_pb10/00_round3_summary.md

请完成：
1. 审核 turnover 过滤
2. 审核 CGO 过滤
3. 审核行业集中度约束
4. 给出“正式版保留项”

输出要求：
- 最终只保留少数几条规则
- 如果过滤器只是让回测好看但降低可执行性，要淘汰
```
