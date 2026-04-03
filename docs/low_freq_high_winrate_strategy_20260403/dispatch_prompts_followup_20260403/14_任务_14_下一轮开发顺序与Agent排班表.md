# 任务 14：下一轮开发顺序与 Agent 排班表

你正在做“总收口与排班”任务，不是在重新展开研究。

硬约束：
1. 只能基于前 13 个任务的结果收口。
2. 必须输出 `Go / Watch / No-Go / 未完成` 总清单。
3. 必须给出下一轮开发顺序，而不是只给一堆方向。
4. 必须包含建议的 agent 波次和并行方式。

技术方案：
- 输入材料：
  - `docs/low_freq_high_winrate_strategy_20260403/results_followup_20260403/result_01_主仓底座现状对齐与冲突表.md`
  - `docs/low_freq_high_winrate_strategy_20260403/results_followup_20260403/result_02_状态输入统一与阈值冻结.md`
  - `docs/low_freq_high_winrate_strategy_20260403/results_followup_20260403/result_03_主仓动态映射候选表轻量比较.md`
  - `docs/low_freq_high_winrate_strategy_20260403/results_followup_20260403/result_04_主仓动态路由V1规格书.md`
  - `docs/low_freq_high_winrate_strategy_20260403/results_followup_20260403/result_05_RSRS改进版本候选筛选.md`
  - `docs/low_freq_high_winrate_strategy_20260403/results_followup_20260403/result_06_RSRS复合过滤增量验证.md`
  - `docs/low_freq_high_winrate_strategy_20260403/results_followup_20260403/result_07_RSRS模块挂接规则与接口定义.md`
  - `docs/low_freq_high_winrate_strategy_20260403/results_followup_20260403/result_08_ML逻辑回归基线复核与泄露检查.md`
  - `docs/low_freq_high_winrate_strategy_20260403/results_followup_20260403/result_09_ML十三因子候选筛选与缩表.md`
  - `docs/low_freq_high_winrate_strategy_20260403/results_followup_20260403/result_10_ML调仓频率与持仓数轻量比较.md`
  - `docs/low_freq_high_winrate_strategy_20260403/results_followup_20260403/result_11_FFScore对RFScore增量验证.md`
  - `docs/low_freq_high_winrate_strategy_20260403/results_followup_20260403/result_12_筹码_STR_行业量价预筛白名单.md`
  - `docs/low_freq_high_winrate_strategy_20260403/results_followup_20260403/result_13_低频ETF宏观原型映射与白名单.md`
- 方法：
  1. 逐项汇总每个方向的状态；
  2. 列出下一轮真正应进入开发的项目；
  3. 列出继续观察与停止推进的项目；
  4. 设计 agent 波次、并行关系、依赖关系。
- 验证标准：
  1. 必须给出唯一开发顺序；
  2. 必须给出 agent 排班建议；
  3. 必须有暂停推进清单。
- 输出文件：
  - 主结果：`docs/low_freq_high_winrate_strategy_20260403/results_followup_20260403/result_14_下一轮开发顺序与Agent排班表.md`
  - 简版回执：`docs/low_freq_high_winrate_strategy_20260403/dispatch_prompts_followup_20260403/results/14_下一轮开发顺序与Agent排班表_回执.md`
- 输出结构：
  - 状态
  - Go / Watch / No-Go / 未完成 总表
  - 下一轮开发顺序
  - Agent 排班表
  - 并行建议
  - 暂停推进清单

任务提示词：
请不要再扩展研究范围，而是把前 13 个任务的结果统一收口成“下一轮开发顺序与 Agent 排班表”。你需要明确告诉团队：哪些方向立即进入开发，哪些方向继续观察，哪些方向暂停推进；同时给出推荐的 agent 波次和并行方式，保证下一轮执行能直接开始。
