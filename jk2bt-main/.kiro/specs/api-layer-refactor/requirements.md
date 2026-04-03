# 需求文档

## 简介

本文档描述 `api-layer-refactor` 重构项目的需求，基于设计文档推导而来。
本次重构以**不破坏现有功能、平滑迁移**为核心原则，对量化交易框架的
`src/api` 层、策略目录、脚本目录、测试结构和文档结构进行系统性整理。

---

## 术语表

- **API 层**：`src/api/` 目录，提供聚宽 API 兼容接口
- **兼容层**：旧文件保留为仅做 re-export 的包装文件，触发 `DeprecationWarning`
- **_internal 模块**：`src/api/_internal/`，存放不对外暴露的私有工具函数
- **Refactoring_System**：执行本次重构的系统/开发者
- **API_Module**：重构后的 `src/api/` 模块
- **Compat_Layer**：兼容层文件（旧文件名保留的 re-export 包装）
- **Tools_Dir**：重构后的 `tools/` 目录
- **Strategies_Dir**：重构后的 `strategies/` 目录
- **Tests_Dir**：重构后的 `tests/` 目录
- **Docs_Dir**：重构后的 `docs/` 目录

---

## 需求

### 需求 1：src/api 层私有工具提取

**用户故事：** 作为开发者，我希望消除 `market_api.py` 和 `market_api_enhanced.py` 中的重复私有函数，以便统一维护，避免两处不一致。

#### 验收标准

1. THE Refactoring_System SHALL 创建 `src/api/_internal/symbol_utils.py`，包含 `normalize_symbol`、`get_symbol_prefix`、`is_gem_or_star`、`calculate_limit_price` 函数
2. THE Refactoring_System SHALL 创建 `src/api/_internal/__init__.py`，使 `_internal` 成为合法 Python 包
3. WHEN `src/api/_internal/` 模块被创建后，THE API_Module SHALL 不在 `__init__.py` 的 `__all__` 中导出 `_internal` 下的任何符号
4. WHEN `_internal/symbol_utils.py` 创建完成后，THE Refactoring_System SHALL 从 `market_api.py` 和 `market_api_enhanced.py` 中移除重复的私有函数实现，改为从 `_internal/symbol_utils.py` 导入

---

### 需求 2：src/api 层文件合并与拆分

**用户故事：** 作为开发者，我希望 `src/api/` 下每个文件只包含单一职责领域的函数，以便快速定位代码，降低维护成本。

#### 验收标准

1. THE Refactoring_System SHALL 创建 `src/api/market.py`，合并 `market_api.py` 和 `market_api_enhanced.py` 的全部公开函数
2. THE Refactoring_System SHALL 创建 `src/api/order.py`，包含从 `enhancements.py` 拆出的订单相关函数（`order_shares`、`order_target_percent`、`LimitOrderStyle`、`MarketOrderStyle`、`rebalance_portfolio`、`get_portfolio_weights`、`calculate_position_value`）
3. THE Refactoring_System SHALL 创建 `src/api/filter.py`，合并 `filter_api.py` 和 `enhancements.py` 中的过滤函数（`filter_st`、`filter_paused`、`filter_limit_up`、`filter_limit_down`、`filter_new_stocks` 等）
4. THE Refactoring_System SHALL 创建 `src/api/finance.py`，包含从 `missing_apis.py` 迁移的财务类 API（`get_locked_shares`、`get_fund_info`、`get_fundamentals_continuously`）
5. THE Refactoring_System SHALL 创建 `src/api/cache.py`，包含从 `optimizations.py` 拆出的缓存与性能优化类（`CurrentDataCache`、`BatchDataLoader`、`DataPreloader`、`warm_up_cache`、`get_memory_usage`、`cleanup_memory`）
6. THE Refactoring_System SHALL 将 `date_api.py` 重命名为 `date.py`，`stats_api.py` 重命名为 `stats.py`，`factor_api.py` 重命名为 `factor.py`，`billboard_api.py` 重命名为 `billboard.py`
7. WHEN `missing_apis.py` 中的 `get_beta` 被迁移时，THE Refactoring_System SHALL 将其归入 `stats.py` 而非 `finance.py`
8. WHEN `enhancements.py` 中的 `get_open_price`、`get_close_price`、`get_high_limit`、`get_low_limit` 被迁移时，THE Refactoring_System SHALL 将其归入 `market.py`

---

### 需求 3：src/api/__init__.py 重写

**用户故事：** 作为开发者，我希望 `src/api/__init__.py` 按功能分组导出所有公开符号，以便清晰理解模块边界。

#### 验收标准

1. THE Refactoring_System SHALL 重写 `src/api/__init__.py`，按行情数据、订单与组合、过滤工具、财务数据、统计与因子、日期工具、技术指标、榜单数据、缓存与性能九个分组导出符号
2. WHEN `src/api/__init__.py` 重写完成后，THE API_Module SHALL 导出的符号集合 ⊇ 重构前 `src/api/__init__.py` 导出的符号集合（向后兼容）
3. THE API_Module SHALL 不在 `__init__.py` 中导出 `APIGapAnalyzer` 或任何来自 `gap_analyzer.py` 的符号

---

### 需求 4：旧文件兼容层保留

**用户故事：** 作为开发者，我希望旧文件名在重构后仍然可以导入，以便现有策略代码无需立即修改。

#### 验收标准

1. WHEN 新文件创建完成后，THE Refactoring_System SHALL 将旧文件（`market_api.py`、`market_api_enhanced.py`、`enhancements.py`、`missing_apis.py`、`optimizations.py`、`filter_api.py`）改写为兼容层，仅做 re-export
2. WHEN 兼容层文件被导入时，THE Compat_Layer SHALL 触发 `DeprecationWarning`，提示开发者迁移到新文件名
3. THE Compat_Layer SHALL 保留至少 6 个月后方可删除

---

### 需求 5：gap_analyzer.py 迁移

**用户故事：** 作为开发者，我希望将开发工具脚本从运行时 API 层移出，以便避免误导开发者将其当作运行时 API 使用。

#### 验收标准

1. THE Refactoring_System SHALL 将 `src/api/gap_analyzer.py` 复制到 `tools/gap_analyzer.py`
2. WHEN `gap_analyzer.py` 迁移完成后，THE Refactoring_System SHALL 从 `src/api/__init__.py` 中移除对 `APIGapAnalyzer` 的导出
3. IF `src/api/gap_analyzer.py` 被保留为兼容层，THEN THE Compat_Layer SHALL 触发 `DeprecationWarning`

---

### 需求 6：策略目录迁移

**用户故事：** 作为开发者，我希望将 `src/` 下的策略目录统一迁移到 `strategies/`，以便核心模块与策略代码清晰分离，提升 IDE 索引速度。

#### 验收标准

1. THE Refactoring_System SHALL 创建 `strategies/` 目录
2. THE Refactoring_System SHALL 将 `src/` 下所有以数字编号开头的策略目录（`src/02_xxx/` 至 `src/99_xxx/`）迁移到 `strategies/` 下对应目录
3. THE Refactoring_System SHALL 将 `src/strategy_converted/` 迁移到 `strategies/converted/`
4. THE Refactoring_System SHALL 删除 `src/market_api.py`（与 `src/api/market_api.py` 重复的旧版残留）
5. THE Refactoring_System SHALL 删除 `src/test_cache_fail/`（测试临时目录）
6. THE Refactoring_System SHALL 将 `src/test_simple_strategy/` 迁移到 `tests/fixtures/`
7. THE Refactoring_System SHALL 将 `src/dependency_checker.py` 迁移到 `tools/`
8. WHEN 策略目录迁移完成后，THE Refactoring_System SHALL 验证 `src/` 下不再包含数字编号开头的目录

---

### 需求 7：scripts/ 目录整理

**用户故事：** 作为开发者，我希望清理 `scripts/` 目录中的历史任务脚本，并将有价值的工具迁移到语义更清晰的目录，以便减少噪音，提升可维护性。

#### 验收标准

1. THE Refactoring_System SHALL 删除所有历史任务临时脚本（`scripts/task14_*.py`、`scripts/task26_*.py`、`scripts/task37_*.py`、`scripts/test_txt_normalization.py`、`scripts/tasks/task23_*.py`、`scripts/tasks/task31_*.py`）
2. THE Refactoring_System SHALL 创建 `tools/` 目录结构（`tools/data/`、`tools/offline_data/`、`tools/validation/`）
3. THE Refactoring_System SHALL 将 `scripts/data/` 迁移到 `tools/data/`
4. THE Refactoring_System SHALL 将 `scripts/offline_data/` 迁移到 `tools/offline_data/`，保持内部目录结构不变
5. THE Refactoring_System SHALL 将 `scripts/validation/` 下所有文件迁移到 `tools/validation/`
6. THE Refactoring_System SHALL 将 `scripts/scan_resource_dependencies.py` 迁移到 `tools/`
7. THE Refactoring_System SHALL 将 `scripts/examples/` 迁移到 `docs/examples/`
8. THE Refactoring_System SHALL 将 `scripts/run_tests.py`、`scripts/test_summary.sh`、`scripts/activate_env.sh` 迁移到项目根目录
9. WHEN 所有文件迁移完成后，THE Refactoring_System SHALL 删除空的 `scripts/` 目录
10. WHEN `tools/offline_data/` 迁移完成后，THE Refactoring_System SHALL 验证其内部相对路径引用（`config.yaml`、`utils/`）保持不变

---

### 需求 8：测试结构整理

**用户故事：** 作为开发者，我希望将 `tests/` 根目录下的测试文件按单元/集成/回归分层组织，以便清晰区分测试类型，减少重复测试文件。

#### 验收标准

1. THE Refactoring_System SHALL 创建 `tests/unit/api/`、`tests/unit/core/`、`tests/unit/utils/`、`tests/integration/`、`tests/regression/`、`tests/fixtures/` 子目录
2. THE Refactoring_System SHALL 将 `test_market_api.py`、`test_market_api_unit.py`、`test_market_api_enhanced.py` 合并为 `tests/unit/api/test_market.py`
3. THE Refactoring_System SHALL 将过滤相关测试合并为 `tests/unit/api/test_filter.py`
4. THE Refactoring_System SHALL 将 `test_duckdb_integration.py` 迁移到 `tests/integration/test_duckdb.py`
5. THE Refactoring_System SHALL 将 `test_api_compatibility.py` 迁移到 `tests/regression/test_api_compatibility.py`
6. WHEN 新测试文件创建完成后，THE Refactoring_System SHALL 确保新测试覆盖率不低于被合并的旧测试文件的覆盖率
7. WHEN 旧测试文件被迁移后，THE Refactoring_System SHALL 保留旧文件直到新测试覆盖率达到同等水平

---

### 需求 9：文档结构整理

**用户故事：** 作为开发者，我希望将 `docs/` 下的临时报告归档，以便正式文档不被临时文件淹没。

#### 验收标准

1. THE Refactoring_System SHALL 创建 `docs/archive/` 目录
2. THE Refactoring_System SHALL 将 `docs/0330_result/` 迁移到 `docs/archive/0330_result/`
3. THE Refactoring_System SHALL 将 `docs/strict_alignment_results/` 迁移到 `docs/archive/strict_alignment_results/`
4. THE Refactoring_System SHALL 将以下临时报告文件移入 `docs/archive/`：`all_tasks_completion_report.md`、`all_tasks_implementation_report.md`、`api_implementation_report.md`、`implementation_status.md`、`data_api_tasks.md`、`api_supplements.md`
5. WHEN 文档整理完成后，`docs/` 根目录 SHALL 只包含 `README.md`、`guides/`、`api/`、`design/`、`strategy_framework/`、`examples/`、`archive/` 这些条目

---

### 需求 10：向后兼容性验证

**用户故事：** 作为开发者，我希望每个重构阶段完成后都能验证现有导入仍然有效，以便确保重构不破坏现有功能。

#### 验收标准

1. WHEN 任意重构阶段完成后，THE Refactoring_System SHALL 执行 `python -c "from src.api import get_price, history, filter_st, order_shares; print('OK')"` 验证核心导入有效
2. WHEN 任意重构阶段完成后，THE Refactoring_System SHALL 执行 `python -c "import src.api"` 验证无循环导入
3. WHEN api 层重构完成后，THE Refactoring_System SHALL 运行 `tests/regression/test_api_compatibility.py` 确认所有回归测试通过
4. IF 任意验证步骤失败，THEN THE Refactoring_System SHALL 回滚该阶段的变更并分析原因
