# Requirements Document

## Introduction

autoresearch-ricequant-wizard 是一个针对 RiceQuant 向导式策略（Wizard Strategy）的自动迭代参数优化系统，作为独立 skill 放置于 `skills/autoresearch_ricequant-wizard/` 目录下，与现有的 `skills/autoresearch_ricequant/`（Python 代码策略优化）完全独立，不共享任何文件。

本系统的优化对象是 `wizard_config.json`——一个描述向导式策略参数空间的 JSON 配置文件，包含股票池（universe）、筛选条件（filters）、排序规则（sorting）、持仓数量（maxHoldingNum）、调仓周期（rebalanceInterval）等参数。

系统通过调用 `skills/ricequant-wizard/run-skill.js` 的 Node.js 接口（`--update` + `--run`）来更新策略并触发回测，内置独立的评分模块（scorer.py），使用与 autoresearch 相同的评分公式（calmar×0.55 + sortino×0.25 + information_ratio×0.20），并通过 keep/rollback 机制维护最优配置（champion）。

---

## Glossary

- **Skill_Root**: 本 skill 的根目录，位于 `skills/autoresearch_ricequant-wizard/`，包含所有工具文件和实验目录
- **Wizard_Config**: 向导式策略的 JSON 配置文件（`wizard_config.json`），包含 universe、filters、sorting、maxHoldingNum、rebalanceInterval 等参数
- **Wizard_Executor**: Python 模块（`skills/autoresearch_ricequant-wizard/wizard_executor.py`），通过调用 Node.js 脚本与 RiceQuant 平台交互，负责更新策略配置并触发回测
- **Mutator**: Python 模块（`skills/autoresearch_ricequant-wizard/wizard_mutator.py`），负责对 Wizard_Config 进行参数变异，生成候选配置
- **Run_Iteration**: Python 脚本（`skills/autoresearch_ricequant-wizard/run_iteration.py`），单次迭代执行器，协调预检查→更新配置→提交回测→等待→评分→keep/rollback→写历史的完整流程
- **Scorer**: 本 skill 内置的评分模块（`skills/autoresearch_ricequant-wizard/scorer.py`），独立实现，不依赖 autoresearch 目录，计算 calmar、sortino、information_ratio 的加权复合得分
- **Experiment_Dir**: 实验目录，位于 `skills/autoresearch_ricequant-wizard/experiments/<experiment_name>/`，每个实验独立存放配置和历史
- **State**: 实验目录下的 `state.json`，维护当前迭代编号、champion 分数、champion 配置等状态
- **Champion**: 当前得分最高的 Wizard_Config 版本，作为下一轮变异的基础
- **Seed_Config**: 初始向导式策略配置（`seed_wizard_config.json`），位于 Skill_Root，作为优化起点模板
- **History**: 实验目录下的 `history/` 子目录，存储每次迭代的 JSON 记录和 TSV 汇总
- **Mutation**: 对 Wizard_Config 的一次参数变异操作，如增删 filter、调整阈值、改变 sorting 权重等
- **Factor**: RiceQuant 平台支持的量化因子，如 pe_ratio、pb_ratio、roe、dividend_yield 等
- **Program_Wizard**: agent 操作指南文档（`skills/autoresearch_ricequant-wizard/program.md`），指导 agent 如何运行优化循环

---

## Requirements

### Requirement 1: 种子配置与实验目录初始化

**User Story:** As a 量化研究员, I want 通过一个种子配置文件快速初始化优化实验, so that 我可以从一个已知的向导式策略出发开始自动迭代优化。

#### Acceptance Criteria

1. THE System SHALL 提供 `seed_wizard_config.json` 作为初始配置模板，位于 `skills/autoresearch_ricequant-wizard/`，包含 universe、filters、sorting、maxHoldingNum、rebalanceInterval、backtest、objective 等完整字段
2. WHEN 用户创建新实验时，THE System SHALL 在 `skills/autoresearch_ricequant-wizard/experiments/<experiment_name>/` 下生成 `wizard_config.json`（从 seed 复制）、`state.json`（初始状态）、`history/` 目录
3. THE `state.json` SHALL 包含字段：`current_iter`（初始为 0）、`strategy_id`（RiceQuant 策略 ID）、`champion_score`（初始为 -inf）、`champion_iter`（初始为空字符串）、`champion_config`（初始为 null）、`consecutive_failures`（初始为 0）
4. THE `seed_wizard_config.json` SHALL 包含 `backtest` 字段（start_date、end_date、capital、benchmark）和 `objective` 字段（weights、hard_constraints）
5. IF `state.json` 中 `strategy_id` 为空，THEN THE System SHALL 打印错误提示并退出，要求用户先在 RiceQuant 平台创建向导式策略并填入 strategy_id

### Requirement 2: 向导式策略执行器（Wizard_Executor）

**User Story:** As a 优化系统, I want 通过 Python 调用 Node.js 接口来更新策略配置并触发回测, so that 不需要直接操作 HTTP API，复用 ricequant-wizard 已有的认证和请求逻辑。

#### Acceptance Criteria

1. THE Wizard_Executor SHALL 提供 `update_and_run(strategy_id, config_path, backtest_config)` 函数，通过 `subprocess` 调用 `node run-skill.js --update --id <id> --config <file>` 更新策略配置
2. WHEN 策略配置更新成功后，THE Wizard_Executor SHALL 调用 `node run-skill.js --run --id <id> --start <date> --end <date> --capital <n>` 触发回测，并从输出中提取 `backtestId`
3. THE Wizard_Executor SHALL 提供 `wait_for_completion(backtest_id, max_wait_seconds, poll_interval)` 函数，通过 HTTP API 轮询回测状态直到完成或超时
4. THE Wizard_Executor SHALL 提供 `fetch_results(backtest_id)` 函数，获取回测完整结果并映射为 scorer.py 期望的字段格式（annualReturn、maxDrawdown、sharpe、sortino、informationRatio）
5. IF Node.js 脚本调用失败（非零退出码），THEN THE Wizard_Executor SHALL 抛出 `WizardExecutorError` 异常，包含详细错误信息
6. IF 回测等待超时，THEN THE Wizard_Executor SHALL 抛出 `BacktestTimeoutError` 异常
7. IF 回测以错误状态结束（error_exit），THEN THE Wizard_Executor SHALL 抛出 `BacktestFailedError` 异常
8. THE Wizard_Executor SHALL 使用 `skills/ricequant-wizard/` 目录下的 Node.js 脚本绝对路径调用，不依赖当前工作目录；session 文件从 `skills/ricequant_strategy/data/session.json` 读取（与 ricequant-wizard 共享认证）

### Requirement 3: 参数变异器（Mutator）

**User Story:** As a 优化系统, I want 对向导式策略的 JSON 配置进行智能参数变异, so that 每轮迭代都能探索新的参数组合，而不是随机试错。

#### Acceptance Criteria

1. THE Mutator SHALL 提供 `mutate(config, mutation_type)` 函数，接受当前 champion 配置和变异类型，返回新的候选配置
2. THE Mutator SHALL 支持以下变异类型：`add_filter`（增加一个筛选条件）、`remove_filter`（删除一个筛选条件）、`adjust_filter_threshold`（调整筛选阈值）、`add_sorting`（增加排序因子）、`adjust_sorting_weight`（调整排序权重）、`adjust_holding_num`（调整持仓数量）、`adjust_rebalance_interval`（调整调仓周期）、`change_universe`（切换股票池）
3. WHEN 执行 `add_filter` 变异时，THE Mutator SHALL 从预定义的因子候选列表中随机选择一个尚未使用的因子，并生成合理的阈值范围
4. WHEN 执行 `adjust_filter_threshold` 变异时，THE Mutator SHALL 在当前阈值的 ±20%~±50% 范围内随机调整，保持方向不变
5. WHEN 执行 `adjust_holding_num` 变异时，THE Mutator SHALL 在 [5, 30] 范围内调整，步长为 5
6. WHEN 执行 `adjust_rebalance_interval` 变异时，THE Mutator SHALL 在 [1, 30] 范围内调整，候选值为 [1, 3, 5, 10, 15, 20, 30]
7. THE Mutator SHALL 确保变异后的配置通过 ricequant-wizard 的 `validateWizardConfig` 逻辑（filters 格式正确、sorting 权重合理）
8. IF 变异操作无法执行（如 `remove_filter` 但当前 filters 为空），THEN THE Mutator SHALL 自动切换到其他可用的变异类型

### Requirement 4: 单次迭代执行器（Run_Iteration）

**User Story:** As a 优化 agent, I want 通过一个命令完成单次迭代的全部流程, so that 我只需要决定变异方向，其余工作由脚本自动完成。

#### Acceptance Criteria

1. THE Run_Iteration SHALL 接受命令行参数 `--base <实验目录>` 和 `--mutation-summary <改动摘要>`，以及可选的 `--mutation-type <类型>`
2. WHEN 执行时，THE Run_Iteration SHALL 按顺序执行：读取 state.json → 生成变异配置 → 保存为临时文件 → 调用 Wizard_Executor 更新并运行回测 → 等待结果 → 评分 → keep/rollback → 写 history
3. WHEN 决策为 keep 时，THE Run_Iteration SHALL 将变异后的配置保存为 `wizard_config.json`（覆盖），并更新 state.json 中的 champion 信息
4. WHEN 决策为 rollback 时，THE Run_Iteration SHALL 将 champion 配置恢复到 `wizard_config.json`（从 `history/<champion_iter>_config.json` 读取），不需要 git 操作
5. THE Run_Iteration SHALL 在 `history/` 目录下写入 `<iter_id>.json`（完整记录）和 `<iter_id>_config.json`（本轮使用的配置快照）
6. THE Run_Iteration SHALL 向 `history/iterations.tsv` 追加一行，包含：iter、backtest_id、status、annual_return、max_drawdown、sharpe、score、decision、mutation
7. THE Run_Iteration SHALL 以退出码 0（keep）、1（rollback）、2（crash）结束，供 agent 判断结果
8. IF `consecutive_failures >= 5`，THEN THE Run_Iteration SHALL 打印警告但继续执行（由 agent 决定是否停止）

### Requirement 5: 评分与决策（复用 Scorer）

**User Story:** As a 优化系统, I want 使用与现有 autoresearch 相同的评分公式评估向导式策略, so that 两套系统的优化目标保持一致，结果可以横向比较。

#### Acceptance Criteria

1. THE System SHALL 直接在 `skills/autoresearch_ricequant-wizard/scorer.py` 中实现独立的评分模块，不依赖 `skills/autoresearch_ricequant/scorer.py`，评分逻辑与 autoresearch 保持一致
2. THE System SHALL 使用评分公式：`score = calmar * 0.55 + sortino * 0.25 + information_ratio * 0.20`，其中 `calmar = annual_return / max(abs(max_drawdown), 0.01)`
3. WHEN 新配置的 score 严格大于 champion score 时，THE System SHALL 决策为 keep
4. WHEN 新配置的 max_drawdown 绝对值超过 `hard_constraints.max_drawdown_limit`（默认 0.35）时，THE System SHALL 决策为 rollback，无论 score 高低
5. WHEN 回测状态不是成功状态（非 finished/normal_exit）时，THE System SHALL 决策为 rollback
6. THE System SHALL 在首次迭代（无 champion）时，只要回测成功且通过硬约束，THE System SHALL 决策为 keep

### Requirement 6: 历史记录与状态管理

**User Story:** As a 量化研究员, I want 查看完整的优化历史记录, so that 我可以了解哪些参数变异有效，哪些无效，并指导后续优化方向。

#### Acceptance Criteria

1. THE System SHALL 在 `history/iterations.tsv` 中维护 TSV 格式的历史记录，包含表头行和每次迭代的数据行
2. THE System SHALL 为每次迭代在 `history/<iter_id>.json` 中保存完整记录，包含：iter、backtest_id、status、start_time、end_time、annual_return、max_drawdown、sharpe、sortino、information_ratio、score、decision、reason、mutation、mutation_type
3. THE System SHALL 为每次迭代在 `history/<iter_id>_config.json` 中保存本轮使用的完整 wizard_config 快照
4. THE `state.json` SHALL 在每次迭代后更新：`current_iter` +1、`last_update` 时间戳、champion 相关字段（仅在 keep 时更新）、`consecutive_failures`（keep 时清零，rollback/crash 时 +1）
5. WHEN 系统重启时，THE Run_Iteration SHALL 检查 state.json 与 history/ 的一致性，如发现不一致（current_iter 对应的 history 文件不存在），THE System SHALL 自动回退 current_iter 并恢复 champion 配置

### Requirement 7: Agent 操作指南（Program_Wizard）

**User Story:** As a 优化 agent, I want 一份清晰的操作指南, so that 我知道如何运行优化循环、选择变异方向、记录搜索地图。

#### Acceptance Criteria

1. THE System SHALL 提供 `program.md` 文件，位于 `skills/autoresearch_ricequant-wizard/`，描述完整的优化循环流程：读取状态 → 分析历史 → 选择变异方向 → 执行迭代 → 更新搜索地图 → 循环
2. THE `program.md` SHALL 包含向导式策略参数空间的说明，列出所有可变异的参数类型及其合理范围
3. THE `program.md` SHALL 包含变异方向选择的优先级指南，基于向导式策略的特点（如：先优化 filters 组合，再调整 sorting 权重，最后调整 maxHoldingNum）
4. THE `program.md` SHALL 包含 `search_notes.md` 的维护规范，格式与 `skills/autoresearch_ricequant/program_enhance.md` 保持一致（已验证有效、已验证无效、待探索方向、规律总结）
5. THE `program.md` SHALL 包含停止条件：`consecutive_failures >= 5` 且待探索方向已全部尝试，或 `current_iter >= 100`
6. THE `program.md` SHALL 明确标注哪些文件只读（state.json、seed_wizard_config.json、program.md、所有 .py 工具文件）、哪些文件可写（实验目录下的 wizard_config.json、history/search_notes.md）
7. THE `program.md` SHALL 包含运行命令示例：`python run_iteration.py --base experiments/<name> --mutation-summary "..."`

### Requirement 8: 因子候选库与变异策略

**User Story:** As a 优化系统, I want 基于 RiceQuant 平台支持的因子列表进行有依据的参数变异, so that 每次变异都在合理的参数空间内探索，避免无效配置。

#### Acceptance Criteria

1. THE System SHALL 维护一个因子候选库（内嵌在 `wizard_mutator.py` 中），包含基本面因子（pe_ratio、pb_ratio、roe、dividend_yield 等）的合理阈值范围
2. THE Mutator SHALL 为每个因子定义默认的阈值范围，如 pe_ratio 的合理筛选范围为 [5, 50]，roe 的合理范围为 [5%, 30%]
3. THE System SHALL 支持 `single_period` 和 `three_periods` 两种模板的参数变异，`three_periods` 模板还需支持对 buy.filters 和 sell.filters 的独立变异
4. WHEN 变异 sorting 权重时，THE Mutator SHALL 确保所有 sorting 规则的权重之和保持合理（各权重均为正数，无需强制归一化）
5. THE System SHALL 在 `seed_wizard_config.json` 中提供一个基于低估值高股息逻辑的初始配置，作为优化起点（参考 `skills/ricequant-wizard/SKILL.md` 中的第一套经典策略模板）
