# 任务列表: autoresearch-guorn-strategy

## 概述

本任务列表基于需求文档和设计文档，将 autoresearch-guorn-strategy 系统的实现分解为可执行的任务。

## 任务

### 1. 项目初始化与基础设施

#### 1.1 创建项目目录结构
- 创建 `skills/autoresearch_guorn_strategy/` 目录
- 创建子目录：`experiments/`、`tests/`
- 创建 `__init__.py` 文件

#### 1.2 创建 setup.py 初始化脚本
- 参考 `skills/autoresearch_ricequant-wizard/setup.py` 结构
- 实现 `init_experiment.py` 功能：
  - 解析命令行参数（--name, --seed-config）
  - 创建实验目录结构
  - 复制种子配置到实验目录
  - 初始化 state.json
  - 创建 history/ 目录和 iterations.tsv
  - 生成 program.md 和 README.md
  - 初始化 Git 仓库
- 添加 baseline 回测执行（可选，可跳过）

#### 1.3 创建种子配置文件
- 创建 `seed_config.json`，包含：
  - 示例策略配置（低估值高股息策略）
  - filters、rankings、pool、holding_num、rebalance_interval
  - backtest 参数（start, end, benchmark, trade_cost）
  - objective 权重和硬约束
  - loop 参数（max_iterations, max_consecutive_failures, max_wait_seconds）

#### 1.3.1 创建自然语言种子配置模板
- 创建 `SEED_TEMPLATE.md`，包含：
  - 模板使用说明
  - 结构化章节：策略基本信息、股票池设置、筛选条件、排序规则、回测参数、优化目标、循环参数
  - 至少 2 个完整示例（低估值高股息策略、高质量成长策略）
  - 常用指标参考表（估值、盈利、成长、红利、财务质量、市场指标）
  - JSON 生成步骤说明
  - 注意事项（指标名称规范、权重约束、阈值范围等）

#### 1.4 创建 program.md agent 指南
- 参考 `skills/autoresearch_ricequant/program.md` 结构
- 编写中文版 agent 操作指南：
  - 实验循环流程（读取状态 → 分析历史 → 选择变异 → 执行迭代）
  - 停止条件说明
  - search_notes.md 格式规范
  - 约束条件（只改配置文件，不改基础设施）
  - 评分公式说明

---

### 2. 评分模块（scorer.py）

#### 2.1 实现 ParsedMetrics 数据类
- 定义字段：status, backtest_id, total_return, annual_return, max_drawdown, sharpe, sortino, information_ratio, win_rate, avg_holding_days, sell_count

#### 2.2 实现 parse_backtest_result() 函数
- 从果仁回测结果 JSON 中提取指标
- 映射字段名：
  - `data.trade_summary.winsorize_annual` → annual_return
  - `data.trade_summary.win_ratio` → win_rate
  - `data.trade_summary.year_information_ratio` → information_ratio
  - `data.trade_summary.maxdrop_day` → max_drawdown
- 返回 ParsedMetrics 对象

#### 2.3 实现 calculate_score() 函数
- 计算 calmar 比率：`annual_return / max(abs(max_drawdown), 0.01)`
- 计算复合得分：`calmar × 0.55 + sortino × 0.25 + information_ratio × 0.20`
- 支持可配置权重（通过 weights 参数）

#### 2.4 实现 decide_keep_rollback() 函数
- 检查硬约束：`abs(max_drawdown) > max_drawdown_limit` → rollback
- 比较得分：`new_score > champion_score` → keep
- 否则 → rollback
- 返回 (decision, reason) 元组

---

### 3. 变异引擎（guorn_mutator.py）

#### 3.1 加载果仁因子库
- 实现 `load_factor_library()` 函数
- 从 `skills/guorn_strategy/GUORN_INDICATORS_CATALOG.md` 读取因子库
- 解析系统函数（~100+ 函数）和常用指标
- 返回结构化的因子字典

#### 3.2 定义变异类型常量
- 定义 8 种变异类型：
  - add_filter: 添加筛选条件
  - remove_filter: 移除筛选条件
  - adjust_filter_threshold: 调整筛选阈值
  - add_ranking: 添加排序规则
  - adjust_ranking_weight: 调整排序权重
  - adjust_holding_num: 调整持仓数量
  - adjust_rebalance_interval: 调整调仓间隔
  - change_pool: 更换股票池

#### 3.3 实现 mutate() 函数
- 接受 config 和可选的 mutation_type 参数
- 如果 mutation_type 为 None，随机选择变异类型
- 根据变异类型生成新配置
- 返回 (new_config, mutation_description) 元组

#### 3.4 实现各变异类型的具体逻辑
- `_mutate_add_filter()`: 从未使用的因子中选择，生成合理的阈值
- `_mutate_remove_filter()`: 随机移除一个 filter（如果为空则切换到 add_filter）
- `_mutate_adjust_filter_threshold()`: 应用 ±20%~±50% 的乘数
- `_mutate_add_ranking()`: 添加新的排序规则
- `_mutate_adjust_ranking_weight()`: 调整现有排序权重
- `_mutate_adjust_holding_num()`: 从预定义列表中选择新值
- `_mutate_adjust_rebalance_interval()`: 从预定义列表中选择新值
- `_mutate_change_pool()`: 从 [hs300, zz500, zz1000, all] 中选择

#### 3.5 实现 validate_config() 函数
- 验证 filters 格式（每个元素包含 factor, operator, value）
- 验证 rankings 格式（每个元素包含 factor, ascending, weight）
- 验证 pool 在可选列表中
- 验证 holding_num 在合理范围内
- 验证 rebalance_interval 在可选列表中

---

### 4. 执行器（guorn_executor.py）

#### 4.1 定义路径常量和异常类
- 定义 `GUORN_SKILL_DIR`、`SESSION_FILE` 路径常量
- 定义异常类：GuornExecutorError, BacktestTimeoutError, BacktestFailedError, SessionInvalidError

#### 4.2 实现 validate_session() 函数
- 读取 session.json 文件
- 验证文件存在且格式正确
- 返回 {valid, username, level, cookies}

#### 4.3 实现 normalize_config() 函数
- 将高级配置字段转换为果仁内部格式
- 使用参数缓存映射因子名称和股票池名称
- 验证配置合法性

#### 4.4 实现 run_backtest() 函数
- 验证 session 文件存在
- 调用 `skills/guorn_strategy/request/strategy-runner.js` 的 `runStrategyWorkflow()`
- 使用 subprocess 调用 Node.js 脚本
- 解析返回的 JSON 结果
- 映射字段名到标准格式
- 返回标准化的结果字典

#### 4.5 实现错误处理
- session 文件不存在 → 抛出 SessionInvalidError
- 回测超时（90秒） → 抛出 BacktestTimeoutError
- 回测失败 → 抛出 BacktestFailedError
- 浏览器启动失败 → 抛出 GuornExecutorError

---

### 5. 迭代执行器（run_iteration.py）

#### 5.1 实现命令行参数解析
- 使用 argparse 解析参数：
  - --base: 实验目录路径
  - --mutation-summary: 变异描述
  - --mutation-type: 可选的变异类型

#### 5.2 实现主流程
- 读取 state.json 和 guorn_config.json
- 调用 guorn_mutator.mutate() 生成候选配置
- 保存临时配置到 history/<iter_id>_config.json
- 调用 guorn_executor.run_backtest()
- 调用 scorer 计算得分和决策
- 根据决策更新文件（keep 或 rollback）
- 写入 history/<iter_id>.json 和追加 iterations.tsv
- Git commit 变更

#### 5.3 实现 keep 逻辑
- 覆盖 guorn_config.json
- 更新 state.json 的 champion 字段
- 重置 consecutive_failures 为 0
- Git commit

#### 5.4 实现 rollback 逻辑
- 从 history/<champion_iter>_config.json 恢复 guorn_config.json
- 增加 consecutive_failures
- 保持 current_iter
- Git commit

#### 5.5 实现退出码
- 0: keep
- 1: rollback
- 2: crash

---

### 6. 模拟模式（guorn_executor.py 扩展）

#### 6.1 实现模拟模式检测
- 检查环境变量 `GUORN_MOCK_MODE`
- 如果为 "1"，启用模拟模式

#### 6.2 实现模拟回测逻辑
- 基于配置复杂度生成模拟指标
- 模拟延迟：配置更新 0.5s，回测提交 1s，完成 2s
- 生成合理范围的指标：
  - annualReturn: [0.08, 0.25]
  - maxDrawdown: [0.05, 0.15]
  - sharpe: [1.0, 2.5]
- 记录 "[Mock]" 前缀

---

### 7. 测试

#### 7.1 单元测试（example-based）
- `test_init_experiment.py`: 验证初始化后的目录结构
- `test_state_json_fields.py`: 验证 state.json 初始字段
- `test_keep_updates_files.py`: 验证 keep 决策后文件更新
- `test_rollback_restores_config.py`: 验证 rollback 后配置恢复
- `test_tsv_format.py`: 验证 iterations.tsv 格式

#### 7.2 属性测试（property-based）
- `test_scorer_properties.py`: 测试属性 1、2、3
  - 属性 1: 评分公式正确性
  - 属性 2: keep 决策条件
  - 属性 3: rollback 决策条件（硬约束）
- `test_mutator_properties.py`: 测试属性 4、5、6
  - 属性 4: 变异后配置合法性
  - 属性 5: add_filter 不重复因子
  - 属性 6: adjust_filter_threshold 范围约束
- `test_history_properties.py`: 测试属性 7
  - 属性 7: 迭代记录 JSON 序列化往返

#### 7.3 集成测试
- `test_run_iteration_integration.py`: mock guorn_executor，验证完整迭代流程
- `test_mock_mode.py`: 验证模拟模式行为

---

### 8. 文档与示例

#### 8.1 创建 README.md
- 项目简介
- 安装说明
- 使用示例
- 目录结构说明

#### 8.2 创建示例配置
- 提供 2-3 个示例策略配置
- 低估值高股息策略
- 动量策略
- 质量因子策略
- 每个示例提供 JSON 格式和对应的 SEED_TEMPLATE.md 填写示例

#### 8.3 创建使用指南
- 初始化实验的步骤
- 运行迭代的步骤
- 查看结果的方法
- 常见问题解答

---

## 任务依赖关系

```
1. 项目初始化 (1.1-1.4)
   ↓
2. 评分模块 (2.1-2.4) ← 独立
   ↓
3. 变异引擎 (3.1-3.5) ← 独立
   ↓
4. 执行器 (4.1-4.5) ← 依赖 guorn_strategy skill
   ↓
5. 迭代执行器 (5.1-5.5) ← 依赖 2, 3, 4
   ↓
6. 模拟模式 (6.1-6.2) ← 扩展 4
   ↓
7. 测试 (7.1-7.3) ← 依赖所有模块
   ↓
8. 文档 (8.1-8.3) ← 最后完成
```

## 优先级

**P0 (必须完成)**:
- 1.1-1.4: 项目初始化（包括 1.3.1 自然语言模板）
- 2.1-2.4: 评分模块
- 3.1-3.5: 变异引擎
- 4.1-4.5: 执行器
- 5.1-5.5: 迭代执行器

**P1 (重要)**:
- 6.1-6.2: 模拟模式
- 7.1: 单元测试
- 8.1-8.2: 基础文档

**P2 (可选)**:
- 7.2-7.3: 属性测试和集成测试
- 8.3: 详细使用指南

## 预估工作量

- 项目初始化: 2-3 小时
- 评分模块: 2-3 小时
- 变异引擎: 4-6 小时
- 执行器: 3-4 小时
- 迭代执行器: 3-4 小时
- 模拟模式: 1-2 小时
- 测试: 4-6 小时
- 文档: 2-3 小时

**总计**: 21-31 小时
