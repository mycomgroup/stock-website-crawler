# 子 Agent 第三阶段任务包

本目录用于第三阶段并行开发，目标是继续向“尽量把 txt 策略都能跑起来”推进。

这轮任务的出发点不是补新花样，而是解决本次复查暴露出的真实问题：

- `factors` 兼容层出现导入回归，核心 API 兼容测试重新变红
- 日线白名单还没有形成“真实成功样本池”
- 分钟策略仍停留在理论分类，没有真实分钟回放闭环
- 多资产中的 LOF / OF / 期货仍主要停留在识别与梳理阶段
- 批量运行结果真值化和策略语义抽检还没有拿到当前代码下的真实证据

统一要求：

- 每个任务一个文档，一个子 agent 负责一个任务
- 不要回退其他人的改动
- 不要做大范围重构
- 完成后在 `docs/0330_result/` 下写结果文档
- 结果文档必须区分：
  - 已真实验证通过
  - 理论支持但未验证
  - 明确未支持

任务列表：

- `task21_factor_import_regression_prompt.md`
- `task22_execution_mode_unification_prompt.md`
- `task23_daily_whitelist_real_run_prompt.md`
- `task24_data_prewarm_cache_prompt.md`
- `task25_resource_dependency_seeding_prompt.md`
- `task26_minute_real_validation_prompt.md`
- `task27_minute_replay_engine_prompt.md`
- `task28_multi_asset_data_prompt.md`
- `task29_futures_trading_model_prompt.md`
- `task30_batch_truth_and_replay_prompt.md`
