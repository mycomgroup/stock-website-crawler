# 任务 07：四状态路由器与二次进场集成

你正在整理通用择时中间层，不是在重新发明一套新的市场状态系统。

硬约束：
1. 只能基于已有四状态路由器与择时集成文档。
2. 不允许新增第五种状态，也不允许重新定义广度与情绪指标。
3. 必须把“连续2日确认”作为核心原则。
4. 输出必须能服务主仓和机会仓两类策略。

技术方案：
- 输入材料：
  - `docs/parallel_strategy_tasks_20260328/09_regime_router_v2_final_report_2026-03-31.md`
  - `docs/parallel_strategy_tasks_20260328/11_macro_regime_router_validation.md`
  - `docs/parallel_strategy_tasks_20260328/15_two_timing_strategies_comparison.md`
  - `strategies/task08_emotion_timing_integration/docs/择时集成文档_V1.0.md`
- 方法：
  1. 固化关闭/防守/正常/进攻四状态；
  2. 抽取上行、下行转换规则；
  3. 映射到主仓与机会仓的仓位建议；
  4. 形成统一“二次进场”模块说明。
- 输出结构：
  - 四状态定义
  - 转换规则
  - 连续2日确认原则
  - 主仓映射
  - 机会仓映射

任务提示词：
请只做四状态路由器与二次进场模块的整编，不要重新设计市场状态系统。你需要把已有文档整理成一个统一中间层：说明四种状态分别代表什么、如何在连续2日确认后切换、切换后主仓与机会仓分别该怎么处理仓位。