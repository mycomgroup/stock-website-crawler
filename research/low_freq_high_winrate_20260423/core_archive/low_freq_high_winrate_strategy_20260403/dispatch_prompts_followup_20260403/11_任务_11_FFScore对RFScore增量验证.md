# 任务 11：FFScore 对 RFScore 增量验证

你正在做“FFScore 叠加到 RFScore”的增量验证，不是在重写 RFScore 主体。

硬约束：
1. 只能比较最多 2 种叠加方式：
   - 作为硬过滤；
   - 作为排序加分项。
2. 必须保持 RFScore 原有股票池与调仓频率不变。
3. 不允许改成全新的多因子模型。
4. 如果没有显著增量，也必须允许结论为 `No-Go`。

技术方案：
- 输入材料：
  - `docs/final_rfscore_release_v1_20260329/06_final_master_release_v1.md`
  - `docs/parallel_strategy_tasks_20260328_round3_rfscore_pb10/result_03_rfscore_backup_pool_and_sparse_handling.md`
  - `docs/parallel_strategy_tasks_20260328_round3_rfscore_pb10/result_05_rfscore_market_state_sizing.md`
  - `strategies/enhanced_v2/rfscore7_pb10_optimized.py`
  - `QuantsPlaybook/A-量化基本面/华泰FFScore/20170209-华泰证券-华泰价值选股之FFScore模型：比乔斯基选股模型A股实证研究.md`
  - `QuantsPlaybook/A-量化基本面/华泰FFScore/FFScore.ipynb`
  - `聚宽有价值策略558/19 复现FFScore财务模型.txt`
  - `聚宽有价值策略558/29 F_Score 选股，年化80%+.txt`
- 方法：
  1. 明确 RFScore 当前基线；
  2. 设计 FFScore 的两种最小叠加方式；
  3. 比较基线 vs 叠加后的候选覆盖、质量和表现；
  4. 若需验证脚本，写到 `docs/low_freq_high_winrate_strategy_20260403/results_followup_20260403/scripts/`。
- 验证标准：
  1. 必须有基线对照；
  2. 必须有两种叠加方式比较；
  3. 必须给出是否继续推进的明确结论。
- 输出文件：
  - 主结果：`docs/low_freq_high_winrate_strategy_20260403/results_followup_20260403/result_11_FFScore对RFScore增量验证.md`
  - 简版回执：`docs/low_freq_high_winrate_strategy_20260403/dispatch_prompts_followup_20260403/results/11_FFScore对RFScore增量验证_回执.md`
- 输出结构：
  - 状态
  - RFScore 基线
  - 两种叠加方式
  - 对比结果
  - 主结论
  - 下一步建议

任务提示词：
请只验证 FFScore 是否能为 RFScore 提供增量价值，不要把任务扩成新的综合多因子模型。你需要把 FFScore 作为硬过滤和排序加分项两种最小叠加方式，与 RFScore 原始基线做对照，回答它到底能不能提升候选质量、稳定性或风险收益比。如果没有明显增量，也请明确写成 `No-Go`。
