# Tasks: autoresearch-ricequant-wizard

## Task List

- [x] 1. 创建 scorer.py（独立评分模块）
  - [x] 1.1 定义 ParsedMetrics dataclass（status、backtest_id、total_return、annual_return、max_drawdown、sharpe、sortino、information_ratio、alpha、beta）
  - [x] 1.2 实现 parse_backtest_result(result_json) -> ParsedMetrics，映射 camelCase 字段到 snake_case
  - [x] 1.3 实现 calculate_score(metrics, weights=None) -> float，公式：calmar*0.55 + sortino*0.25 + ir*0.20
  - [x] 1.4 实现 decide_keep_rollback(new_score, champion_score, new_metrics, champion_metrics, hard_constraints) -> (str, str)
  - [x] 1.5 实现 validate_result(metrics) -> (bool, str)，检查 status 和 backtest_id

- [x] 2. 创建 wizard_executor.py（执行器）
  - [x] 2.1 定义路径常量：WIZARD_SKILL_DIR、SESSION_FILE
  - [x] 2.2 复用 ricequant_executor.py 的 session 读取和 HTTP 工具函数（_load_session、_cookie_header、_rq_get）
  - [x] 2.3 实现 update_strategy(strategy_id, config_path)：subprocess 调用 node run-skill.js --update
  - [x] 2.4 实现 run_backtest(strategy_id, bt_config)：subprocess 调用 node run-skill.js --run --wait，提取 backtestId（格式：回测已启动: <id>）
  - [x] 2.5 实现 _extract_backtest_id(output) -> Optional[str]：从 Node.js 输出提取 backtestId
  - [x] 2.6 实现 wait_for_completion(backtest_id, max_wait, poll_interval)：HTTP 轮询，支持 finished/error_exit/timeout
  - [x] 2.7 实现 fetch_results(strategy_id, backtest_id)：HTTP 获取结果，映射字段到 scorer.py 期望格式
  - [x] 2.8 定义异常类：WizardExecutorError、BacktestTimeoutError、BacktestFailedError

- [x] 3. 创建 wizard_mutator.py（变异器）
  - [x] 3.1 定义 FACTOR_CANDIDATES 字典（9个因子，含 type、operators、range、default_rhs）
  - [x] 3.2 定义 UNIVERSE_OPTIONS、HOLDING_NUM_OPTIONS、REBALANCE_OPTIONS 常量
  - [x] 3.3 实现 add_filter(config) -> (dict, str)：从候选库选未使用因子，生成合理阈值
  - [x] 3.4 实现 remove_filter(config) -> (dict, str)：随机删除一个 filter，filters 为空时 fallback
  - [x] 3.5 实现 adjust_filter_threshold(config) -> (dict, str)：在 ±20%~±50% 范围内调整阈值
  - [x] 3.6 实现 add_sorting(config) -> (dict, str)：增加排序因子
  - [x] 3.7 实现 adjust_sorting_weight(config) -> (dict, str)：调整权重，确保所有权重为正数
  - [x] 3.8 实现 adjust_holding_num(config) -> (dict, str)：在 HOLDING_NUM_OPTIONS 中选择不同值
  - [x] 3.9 实现 adjust_rebalance_interval(config) -> (dict, str)：在 REBALANCE_OPTIONS 中选择不同值
  - [x] 3.10 实现 change_universe(config) -> (dict, str)：切换股票池
  - [x] 3.11 实现 mutate(config, mutation_type=None) -> (dict, str)：统一入口，mutation_type 为 None 时随机选择，处理 fallback 逻辑

- [x] 4. 创建 run_iteration.py（单次迭代执行器）
  - [x] 4.1 实现 CLI 参数解析：--base、--mutation-summary、--mutation-type（可选）
  - [x] 4.2 实现 load_json / save_json / append_tsv 工具函数
  - [x] 4.3 实现 _recover_state(base, state)：检查 state.json 与 history/ 一致性，自动回退
  - [x] 4.4 实现主流程：读 state → 读 champion config → mutate → update_strategy → run_backtest → wait → fetch → score → decide
  - [x] 4.5 实现 keep 分支：覆盖 wizard_config.json，写 history/<iter_id>_config.json，更新 state.json
  - [x] 4.6 实现 rollback 分支：从 history/<champion_iter>_config.json 恢复 wizard_config.json，更新 state.json
  - [x] 4.7 实现 _write_result：写 history/<iter_id>.json（含 mutation_type 字段）
  - [x] 4.8 实现 _update_state：更新 current_iter、last_update、champion 信息、consecutive_failures
  - [x] 4.9 设置退出码：0=keep, 1=rollback, 2=crash

- [x] 5. 创建 setup.py（初始化脚本）
  - [x] 5.1 实现 CLI 参数解析：--name、--strategy-id
  - [x] 5.2 创建实验目录结构：experiments/<name>/、history/
  - [x] 5.3 从 seed_wizard_config.json 复制生成 wizard_config.json
  - [x] 5.4 生成初始 state.json（current_iter=0、champion_score=-inf、champion_iter=""、consecutive_failures=0）
  - [x] 5.5 写入 history/0000_config.json（初始配置快照）
  - [x] 5.6 写入 history/iterations.tsv（仅表头行）
  - [x] 5.7 验证 strategy_id 非空，否则打印错误并退出

- [x] 6. 创建 seed_wizard_config.json（种子配置）
  - [x] 6.1 按设计文档中的低估值高股息初始策略创建完整 JSON，包含 filters（pe_ratio<15、pb_ratio<1.5、dividend_yield>3）、sorting（dividend_yield 降序 0.6、pe_ratio 升序 0.4）、maxHoldingNum=15、rebalanceInterval=10
  - [x] 6.2 包含 backtest 字段（start_date=2021-01-01、end_date=2025-03-28、capital=100000、benchmark=000300.XSHG）
  - [x] 6.3 包含 objective 字段（weights: calmar=0.55、sortino=0.25、information_ratio=0.20；hard_constraints: max_drawdown_limit=0.35）
  - [x] 6.4 包含 loop 字段（max_iterations=100、max_consecutive_failures=5、max_wait_seconds=600）

- [x] 7. 创建 program.md（agent 操作指南）
  - [x] 7.1 描述完整优化循环流程：读取状态 → 分析历史 → 选择变异方向 → 执行迭代 → 更新搜索地图 → 循环
  - [x] 7.2 列出所有可变异参数类型及合理范围（参考 FACTOR_CANDIDATES 和各 OPTIONS 常量）
  - [x] 7.3 提供变异方向选择优先级指南（先优化 filters 组合，再调整 sorting 权重，最后调整 maxHoldingNum）
  - [x] 7.4 包含 search_notes.md 维护规范（已验证有效、已验证无效、待探索方向、规律总结）
  - [x] 7.5 明确标注只读文件（state.json、seed_wizard_config.json、program.md、所有 .py 工具文件）和可写文件（wizard_config.json、history/search_notes.md）
  - [x] 7.6 包含运行命令示例和停止条件（consecutive_failures>=5 且待探索方向已全部尝试，或 current_iter>=100）

- [x] 8. 编写属性测试
  - [x] 8.1 test_scorer_properties.py：Property 1（评分公式正确性）、Property 2（keep 决策条件）、Property 3（rollback 硬约束）、Property 4（rollback 失败状态）
  - [x] 8.2 test_mutator_properties.py：Property 5（变异后配置合法性）、Property 6（add_filter 不重复因子）、Property 7（adjust_filter_threshold 范围约束）、Property 8（adjust_sorting_weight 权重正数不变量）
  - [x] 8.3 test_executor_properties.py：Property 9（backtestId 解析正确性）
  - [x] 8.4 test_history_properties.py：Property 10（迭代记录 JSON 序列化往返）
  - [x] 8.5 确保每个属性测试使用 @settings(max_examples=100) 配置

- [x] 9. 编写单元测试
  - [x] 9.1 test_setup.py：验证初始化后的目录结构和文件内容
  - [x] 9.2 test_keep_rollback_files.py：验证 keep/rollback 后文件正确更新/恢复
  - [x] 9.3 test_recovery_on_restart.py：验证重启恢复逻辑（不一致状态自动修复）
  - [x] 9.4 test_tsv_format.py：验证 iterations.tsv 格式（表头 + 数据行）
