# 任务列表

## 阶段一：src/api 层内部重构

- [x] 1. 创建 _internal 私有工具模块
  - [x] 1.1 创建 `src/api/_internal/__init__.py`
  - [x] 1.2 创建 `src/api/_internal/symbol_utils.py`，提取 `normalize_symbol`、`get_symbol_prefix`、`is_gem_or_star`、`calculate_limit_price` 等共享私有函数
  - [x] 1.3 更新 `market_api.py` 和 `market_api_enhanced.py`，移除重复私有函数实现，改为从 `_internal/symbol_utils.py` 导入

- [x] 2. 创建新 API 文件
  - [x] 2.1 创建 `src/api/market.py`，合并 `market_api.py` 和 `market_api_enhanced.py` 的全部公开函数（含 `get_open_price`、`get_close_price`、`get_high_limit`、`get_low_limit`）
  - [x] 2.2 创建 `src/api/order.py`，包含从 `enhancements.py` 拆出的订单相关函数（`order_shares`、`order_target_percent`、`LimitOrderStyle`、`MarketOrderStyle`、`rebalance_portfolio`、`get_portfolio_weights`、`calculate_position_value`）
  - [x] 2.3 创建 `src/api/filter.py`，合并 `filter_api.py` 和 `enhancements.py` 中的过滤函数
  - [x] 2.4 创建 `src/api/finance.py`，包含从 `missing_apis.py` 迁移的财务类 API（`get_locked_shares`、`get_fund_info`、`get_fundamentals_continuously`）
  - [x] 2.5 创建 `src/api/cache.py`，包含从 `optimizations.py` 拆出的缓存与性能优化类
  - [x] 2.6 将 `stats_api.py` 中的 `get_beta` 合并到 `stats.py`，并重命名 `stats_api.py` → `stats.py`
  - [x] 2.7 重命名 `date_api.py` → `date.py`，`factor_api.py` → `factor.py`，`billboard_api.py` → `billboard.py`

- [x] 3. 重写 `src/api/__init__.py`
  - [x] 3.1 按九个功能分组（行情数据、订单与组合、过滤工具、财务数据、统计与因子、日期工具、技术指标、榜单数据、缓存与性能）重写 `__init__.py`
  - [x] 3.2 确认导出符号集合 ⊇ 重构前导出符号集合
  - [x] 3.3 确认 `APIGapAnalyzer` 不在导出列表中
  - [x] 3.4 确认 `_internal` 下的符号不在 `__all__` 中

- [x] 4. 将旧文件改写为兼容层
  - [x] 4.1 将 `market_api.py` 改写为兼容层（re-export + `DeprecationWarning`）
  - [x] 4.2 将 `market_api_enhanced.py` 改写为兼容层
  - [x] 4.3 将 `enhancements.py` 改写为兼容层
  - [x] 4.4 将 `missing_apis.py` 改写为兼容层
  - [x] 4.5 将 `optimizations.py` 改写为兼容层
  - [x] 4.6 将 `filter_api.py` 改写为兼容层

- [x] 5. 验证阶段一
  - [x] 5.1 执行 `python -c "from src.api import get_price, history, filter_st, order_shares; print('OK')"` 确认核心导入有效
  - [x] 5.2 执行 `python -c "import src.api"` 确认无循环导入
  - [x] 5.3 运行 `pytest tests/regression/test_api_compatibility.py -v` 确认回归测试通过

## 阶段二：gap_analyzer 迁移

- [x] 6. 迁移 gap_analyzer.py
  - [x] 6.1 将 `src/api/gap_analyzer.py` 复制到 `tools/gap_analyzer.py`
  - [x] 6.2 将 `src/api/gap_analyzer.py` 改写为兼容层（re-export + `DeprecationWarning`），或直接删除（因为这是开发工具，不是运行时 API）
  - [x] 6.3 确认 `src/api/__init__.py` 中不再导出 `APIGapAnalyzer`

## 阶段三：策略目录迁移

- [x] 7. 迁移策略目录
  - [x] 7.1 创建 `strategies/` 目录
  - [x] 7.2 将 `src/` 下所有以数字编号开头的策略目录（`02_xxx` 至 `99_xxx`）迁移到 `strategies/`
  - [x] 7.3 将 `src/strategy_converted/` 迁移到 `strategies/converted/`
  - [x] 7.4 将 `src/test_simple_strategy/` 迁移到 `tests/fixtures/`
  - [x] 7.5 将 `src/dependency_checker.py` 迁移到 `tools/`

- [x] 8. 清理 src/ 根目录散落文件
  - [x] 8.1 删除 `src/market_api.py`（旧版残留，与 `src/api/market_api.py` 重复）
  - [x] 8.2 删除 `src/test_cache_fail/`（测试临时目录）
  - [x] 8.3 评估 `src/backtrader_base_strategy.py` 和 `src/subportfolios.py`，决定并入 `src/core/` 或 `src/strategy/`

- [x] 9. 验证阶段三
  - [x] 9.1 确认 `src/` 下不再包含数字编号开头的目录
  - [x] 9.2 执行核心导入验证（同 5.1）

## 阶段四：测试结构整理

- [x] 10. 创建测试子目录结构
  - [x] 10.1 创建 `tests/unit/api/`、`tests/unit/core/`、`tests/unit/utils/` 目录
  - [x] 10.2 创建 `tests/integration/`、`tests/regression/`、`tests/fixtures/` 目录

- [x] 11. 合并和迁移测试文件
  - [x] 11.1 将 `test_market_api.py`、`test_market_api_unit.py`、`test_market_api_enhanced.py` 合并为 `tests/unit/api/test_market.py`
  - [x] 11.2 将过滤相关测试合并为 `tests/unit/api/test_filter.py`
  - [x] 11.3 将日期相关测试迁移到 `tests/unit/api/test_date.py`
  - [x] 11.4 将 `test_indicators_api.py` 迁移到 `tests/unit/api/test_indicators.py`
  - [x] 11.5 将 `test_duckdb_integration.py` 迁移到 `tests/integration/test_duckdb.py`
  - [x] 11.6 将 `test_api_compatibility.py` 迁移到 `tests/regression/test_api_compatibility.py`
  - [x] 11.7 创建 `tests/unit/utils/test_symbol_utils.py`，测试 `_internal/symbol_utils.py`

## 阶段五：scripts/ 目录整理

- [x] 12. 删除历史任务临时脚本
  - [x] 12.1 删除 `scripts/task14_minute_minimal_test.py`
  - [x] 12.2 删除 `scripts/task14_minute_strategy_baseline.py`
  - [x] 12.3 删除 `scripts/task14_minute_strategy_real_test.py`
  - [x] 12.4 删除 `scripts/task26_minute_real_validation.py`
  - [x] 12.5 删除 `scripts/task37_txt_normalization_test.py`
  - [x] 12.6 删除 `scripts/test_txt_normalization.py`
  - [x] 12.7 删除 `scripts/tasks/task23_load_whitelist.py`
  - [x] 12.8 删除 `scripts/tasks/task23_real_whitelist.py`
  - [x] 12.9 删除 `scripts/tasks/task31_daily_true_run_pool.py`
  - [x] 12.10 删除 `scripts/tasks/task31_extend_pool.py`

- [x] 13. 迁移工具脚本到 tools/
  - [x] 13.1 创建 `tools/data/`、`tools/offline_data/`、`tools/validation/` 目录
  - [x] 13.2 将 `scripts/data/` 下所有文件迁移到 `tools/data/`
  - [x] 13.3 将 `scripts/offline_data/` 迁移到 `tools/offline_data/`（保持内部结构不变）
  - [x] 13.4 将 `scripts/validation/` 下所有文件迁移到 `tools/validation/`
  - [x] 13.5 将 `scripts/scan_resource_dependencies.py` 迁移到 `tools/`
  - [x] 13.6 验证 `tools/offline_data/` 内部相对路径引用（`config.yaml`、`utils/`）仍然有效

- [x] 14. 迁移其他 scripts/ 文件
  - [x] 14.1 将 `scripts/examples/` 迁移到 `docs/examples/`
  - [x] 14.2 将 `scripts/run_tests.py`、`scripts/test_summary.sh`、`scripts/activate_env.sh` 迁移到项目根目录

- [x] 15. 清理 scripts/ 目录
  - [x] 15.1 删除空的 `scripts/` 目录

## 阶段六：文档结构整理

- [x] 16. 归档临时文档
  - [x] 16.1 创建 `docs/archive/` 目录
  - [x] 16.2 将 `docs/0330_result/` 迁移到 `docs/archive/0330_result/`
  - [x] 16.3 将 `docs/strict_alignment_results/` 迁移到 `docs/archive/strict_alignment_results/`
  - [x] 16.4 将 `docs/all_tasks_completion_report.md`、`docs/all_tasks_implementation_report.md`、`docs/api_implementation_report.md`、`docs/implementation_status.md`、`docs/data_api_tasks.md`、`docs/api_supplements.md` 移入 `docs/archive/`

- [x] 17. 验证文档结构
  - [x] 17.1 确认 `docs/` 根目录只包含 `README.md`、`guides/`、`api/`、`design/`、`strategy_framework/`、`examples/`、`archive/` 这些条目
