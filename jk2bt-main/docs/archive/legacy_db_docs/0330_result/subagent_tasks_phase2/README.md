# 子 Agent 第二阶段任务包

本目录用于第二阶段并行开发，目标不是继续补零散 API，而是把项目从“主干测试通过”推进到“尽量让 txt 策略批量可运行、可归因、可验证”。

这 10 个任务的定位：

- 第一阶段已经把核心兼容主干打通
- 第二阶段重点是批量策略落地能力
- 目标是让更多 `txt` 策略真正被识别、运行、归因、复现，而不是只过接口单测

统一要求：

- 每个任务一个文档，一个子 agent 负责一个任务
- 不要回退其他人的改动
- 不要做大范围重构
- 只在自己负责的范围内修改
- 完成后在 `docs/0330_result/` 下写结果文档

任务列表：

- `task11_strategy_inventory_prompt.md`
- `task12_missing_api_matrix_prompt.md`
- `task13_daily_equity_baseline_prompt.md`
- `task14_minute_intraday_baseline_prompt.md`
- `task15_multi_asset_coverage_prompt.md`
- `task16_runtime_resource_pack_prompt.md`
- `task17_dependency_ml_stack_prompt.md`
- `task18_batch_runner_truth_prompt.md`
- `task19_strategy_replay_validation_prompt.md`
- `task20_package_entrypoint_prompt.md`
