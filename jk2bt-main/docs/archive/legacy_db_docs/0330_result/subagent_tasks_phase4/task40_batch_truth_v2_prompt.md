# Task 40: 跑批真值 v2

## 任务目标

把批量跑批结果从“统计能看”推进到“结论可信”，形成统一的成功/失败/假跑通/数据缺失归因体系。

## 建议写入目录

- `run_strategies_parallel.py`
- `jqdata_akshare_backtrader_utility/strategy_validator.py`
- `docs/0330_result/`
- `logs/strategy_runs/`

## 负责范围

- 跑批结果结构
- 语义判定标准
- 误判修复
- 结果汇总

## 给子 agent 的提示词

你负责跑批真值 v2。

目标是让大规模 txt 跑批的结果真正能拿来做排期和决策，而不是只看表层状态。

请统一以下判定：
- load_failed
- syntax_error
- missing_dependency
- missing_api
- entered_backtest_loop
- success_no_trade
- success_with_nav
- success_with_transactions
- pseudo_success
- pseudo_failure

要求：
- 修复验证脚本自身导致的误判
- 每个策略结果都保留证据字段
- 输出可聚合 JSON 和可读 Markdown

## 任务验证

- 用当前代码重新跑一轮固定样本集
- 对至少 10 个样本做人工抽检
- 输出 `docs/0330_result/task40_batch_truth_v2_result.md`

## 任务成功总结

- 跑批结果可信度提升
- 后续缺口分析和开发排期有了可靠依据
