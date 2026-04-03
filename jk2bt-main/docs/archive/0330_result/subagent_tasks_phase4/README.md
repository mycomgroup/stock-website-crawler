# Phase 4 子任务说明

这一轮任务目标不是继续补零散单测，而是把项目从“主干兼容测试通过”推进到“尽量让 `txt` 策略真实可跑、可归因、可验证”。

当前我复查到的事实：

- 主干回归测试通过：`108 passed`
- 基础运行/导入/子账户测试通过：`91 passed`
- 兼容导入链已经恢复：`factors`、`backtrader_base_strategy`、`subportfolios`、`db.duckdb_manager` 可导入
- 但离“尽量把 txt 策略都跑起来”还有明显缺口：
  - 日线白名单更多是“可加载”，不是“真实完整跑通”
  - 分钟缓存回放基本有了，但上层 `get_price/history/attribute_history/get_bars` 仍有空数据问题
  - 多资产里 LOF / OF / 期货仍未真正落地
  - 跑批真值文档里仍暴露“数据缺失、误判、验证脚本与真实策略状态混杂”的问题

本目录下的 10 个任务，都是可以并行推进的子任务。每个文件都包含：

- 任务目标
- 建议写入目录
- 负责范围
- 可直接发给子 agent 的提示词
- 任务验证
- 任务成功总结

推荐优先级：

1. `task31_daily_true_run_pool_prompt.md`
2. `task32_minute_upper_api_closure_prompt.md`
3. `task33_offline_data_pack_prompt.md`
4. `task34_index_fundamentals_robustness_prompt.md`
5. `task40_batch_truth_v2_prompt.md`

