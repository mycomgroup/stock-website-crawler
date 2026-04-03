# 任务 08：RFScore PB10 主仓低频化整编

你正在整理 RFScore PB10 主仓方案，不是在重新开启一轮 PB 分组或 RFScore 参数研究。

硬约束：
1. 只能基于已有 RFScore PB10 研究与现有策略代码。
2. 不允许重新扩展 PB5/PB10/PB20 大范围比较题。
3. 必须把“候选稀疏、补位逻辑、市场状态持仓数”统一起来。
4. 输出必须指向一个可落地的月频主仓框架。

技术方案：
- 输入材料：
  - `docs/final_rfscore_release_v1_20260329/01_round3_summary_snapshot.md`
  - `docs/parallel_strategy_tasks_20260328_round3_rfscore_pb10/result_03_rfscore_backup_pool_and_sparse_handling.md`
  - `docs/parallel_strategy_tasks_20260328_round3_rfscore_pb10/result_05_rfscore_market_state_sizing.md`
  - `strategies/enhanced_v2/rfscore7_pb10_optimized.py`
- 方法：
  1. 提取 RFScore PB10 的核心选股规则；
  2. 整理候选不足时的补位与留现金逻辑；
  3. 整理市场状态对应的持仓数与仓位节奏；
  4. 输出一份主仓低频化方案卡。
- 输出结构：
  - 主池规则
  - 次池/补位规则
  - 留现金规则
  - 市场状态持仓数
  - 推荐落地版本

任务提示词：
请只整编 RFScore PB10 已有成果，不要重新做 PB 分组大实验。你的目标是把已有研究和现有代码统一成一个“月频主仓”方案：主池怎么选、候选不足怎么办、什么时候留现金、不同市场状态持多少只股票，最后给出一个最小可执行框架。