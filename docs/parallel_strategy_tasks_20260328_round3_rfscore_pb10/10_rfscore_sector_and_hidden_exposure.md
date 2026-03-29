# 任务 10：RFScore 的行业偏置与隐藏暴露

## 设计文档

### 任务定位

- 聚焦方向：`RFScore PB10` 主线
- 目标：搞清楚这条线本质上在押什么，而不是只看结果

### 当前已知问题

- 当前候选里已经能看出明显的低 PB 行业偏向
- 如果不理解隐藏暴露，就不知道它到底是“质量低估”还是“银行/周期/央国企贝塔”

### 参考材料

- `tmp/rfscore7_candidate_industry.py`
- `tmp/rfscore7_current_candidates.py`
- `docs/parallel_strategy_tasks_20260328/11_rfscore7_pb10_upgrade_report.md`
- `docs/parallel_strategy_tasks_20260328/09_regime_router_v2_backtest_2026-03-28.md`

### 强制实际验证要求

- 必须使用 `/Users/fengzhi/Downloads/git/testlixingren/skills/joinquant_nookbook` 抓取历史月度候选行业分布
- 必须给出当前候选与历史候选的行业、风格、估值暴露

### 结果归档要求

- 结果文档必须写入：`/Users/fengzhi/Downloads/git/testlixingren/docs/parallel_strategy_tasks_20260328_round3_rfscore_pb10`
- 建议结果文件名：`result_10_rfscore_sector_and_hidden_exposure.md`
- 跑完后必须同步更新：`/Users/fengzhi/Downloads/git/testlixingren/docs/parallel_strategy_tasks_20260328_round3_rfscore_pb10/00_round3_summary.md`

### 交付物

1. 一份历史行业分布图
2. 一份隐藏暴露分析
3. 一份结论：哪些暴露是策略本来就想要的，哪些是意外副产物

## 子任务提示词

```text
你现在负责 RFScore PB10 的行业偏置与隐藏暴露分析。

请优先阅读：
- tmp/rfscore7_candidate_industry.py
- tmp/rfscore7_current_candidates.py
- docs/parallel_strategy_tasks_20260328/11_rfscore7_pb10_upgrade_report.md
- docs/parallel_strategy_tasks_20260328/09_regime_router_v2_backtest_2026-03-28.md

强制要求：
- 必须用 /Users/fengzhi/Downloads/git/testlixingren/skills/joinquant_nookbook 抓历史月度候选与当前候选
- 结果文档必须写到 /Users/fengzhi/Downloads/git/testlixingren/docs/parallel_strategy_tasks_20260328_round3_rfscore_pb10/result_10_rfscore_sector_and_hidden_exposure.md
- 跑完后必须回填 /Users/fengzhi/Downloads/git/testlixingren/docs/parallel_strategy_tasks_20260328_round3_rfscore_pb10/00_round3_summary.md

请完成：
1. 分析行业分布
2. 分析是否存在银行/煤炭/周期等隐藏暴露
3. 判断这些暴露是策略想要的还是意外副产物

输出要求：
- 结论必须帮助我们决定要不要加行业约束
- 不要只给饼图，要给行动结论
```
