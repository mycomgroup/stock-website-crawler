# Task 31: 日线真实跑通样本池

## 任务目标

把“日线白名单”从“可加载”升级为“真实完整跑通样本池”。至少沉淀 20 个可复现的真实成功日线策略样本，并给出失败归因。

## 建议写入目录

- `docs/0330_result/`
- `logs/strategy_runs/`
- `tests/`

## 负责范围

- 日线股票 / ETF / 指数增强类 `.txt` 策略
- 不负责分钟策略
- 不负责期货与 OF 交易实现

## 给子 agent 的提示词

你负责建立“日线真实跑通样本池”。

目标不是只验证 `load_jq_strategy()`，而是要验证真实回测闭环：
- 策略成功加载
- 进入回测循环
- 产生净值序列
- 有交易或有明确的无交易原因
- 最终结果可复现

请优先处理：
- `docs/0330_result/task23_daily_whitelist_real_run_result.md`
- `docs/0330_result/task19_strategy_replay_validation_result.md`
- `jqdata_akshare_backtrader_utility/jq_strategy_runner.py`
- `jqdata_akshare_backtrader_utility/strategy_validator.py`
- 批量选择一批低依赖、日线、股票/ETF 为主的 txt 策略

交付内容：
- 真实成功样本池 JSON
- 失败样本池 JSON
- 一份结果文档，明确区分：
  - load_success
  - entered_backtest_loop
  - has_nav_series
  - has_transactions
  - final_value
  - pnl_pct
  - failure_reason

注意：
- 不要把“加载成功”当成“跑通成功”
- 要排除验证脚本误判
- 尽量使用固定日期区间和固定缓存数据，确保复现

## 任务验证

- 运行一个专用脚本，对至少 30 个日线候选策略进行批量验证
- 至少产出 20 个“真实跑通”样本，或明确说明为什么达不到
- 结果文件写入 `docs/0330_result/task31_daily_true_run_pool_result.md`

## 任务成功总结

- 成功建立真实日线样本池
- 将“可加载”与“真跑通”严格分开
- 为后续大规模跑批提供可靠基线

