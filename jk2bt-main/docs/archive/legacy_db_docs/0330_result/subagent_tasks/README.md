# 子 Agent 任务包

本目录包含 10 个可并行分发的子任务文档。

使用约定：

- 每个任务一个独立文件，可直接复制给一个子 agent。
- 每个任务文档都包含：
  - 任务目标
  - 负责范围
  - 建议写入目录
  - 开发提示词
  - 验证要求
  - 成功总结模板
- 所有子 agent 都应遵守：
  - 不要回退其他人的改动
  - 不要做大范围重构
  - 只在自己负责的范围内修改
  - 完成后写清楚修改文件、验证结果、已知边界

任务列表：

- `task01_runner_namespace_prompt.md`
- `task02_timer_engine_prompt.md`
- `task03_market_api_prompt.md`
- `task04_minute_data_prompt.md`
- `task05_runtime_io_prompt.md`
- `task06_call_auction_billboard_prompt.md`
- `task07_money_flow_prompt.md`
- `task08_finance_query_prompt.md`
- `task09_asset_router_subportfolio_prompt.md`
- `task10_batch_runner_prompt.md`
