# 设计文档：API 层重构（api-layer-refactor）

## 概述

本文档描述对量化交易框架 `src/api` 层及整体项目结构的系统性重构方案。
当前代码库存在职责混乱、文件命名不规范、目录结构散乱等问题，本次重构以
**不破坏现有功能、平滑迁移** 为核心原则，重点整理 `src/api` 层的职责划分，
同时规划整体目录、文档和测试结构。

---

## 一、现状问题诊断

### 1.1 src/api 层问题

| 文件 | 问题 |
|------|------|
| `market_api.py` + `market_api_enhanced.py` | 两个文件都提供行情数据，职责重叠；`_normalize_symbol`、`_calculate_limit_price` 等私有函数在两个文件中完全重复 |
| `enhancements.py` | 命名模糊，实际包含两类完全不同的内容：订单函数（`order_shares`、`order_target_percent`）和过滤函数（`filter_st`、`filter_paused` 等） |
| `missing_apis.py` | "缺失补丁"命名，是临时性文件，包含 `get_locked_shares`、`get_fund_info`、`get_beta` 等正式 API |
| `optimizations.py` | 包含缓存、批量加载、内存管理三类不同职责，命名不能反映内容 |
| `gap_analyzer.py` | 这是一个开发工具/分析脚本，不属于运行时 API 层，放在 `src/api/` 下不合适 |
| `__init__.py` | 平铺导出所有符号，没有分组，难以理解模块边界 |

### 1.2 src/ 目录问题

`src/` 下混杂了 80+ 个策略目录（`src/02_xxx/`、`src/03_xxx/` 等）和核心模块，
导致核心代码难以定位，IDE 索引慢，`find` 命令噪音大。

### 1.3 测试问题

`tests/` 根目录下有 70+ 个测试文件，命名不一致（`test_market_api.py`、
`test_market_api_unit.py`、`test_market_api_enhanced.py` 三个文件测同一模块），
没有清晰的分层（单元/集成/回归）。

### 1.4 scripts/ 目录问题

`scripts/` 下混杂了三类性质完全不同的文件：

- **历史任务临时脚本**：`task14_*.py`、`task26_*.py`、`task37_*.py`（根目录）以及 `scripts/tasks/task23_*.py`、`task31_*.py`，是开发期遗留产物，命名带任务编号，已无维护价值
- **正式工具脚本**：`scripts/data/`（数据下载/预热）、`scripts/offline_data/`（离线数据管理，有完整 README）、`scripts/validation/`（策略验证），有实际用途，应归入 `tools/`
- **示例代码**：`scripts/examples/`，应归入文档体系
- **测试辅助**：`scripts/run_tests.py`、`scripts/test_summary.sh`，应靠近测试目录

### 1.5 文档问题

`docs/` 下混杂了正式文档和大量临时报告（`*_report.md`、`*_result.md`、
`docs/0330_result/` 目录下 120 个文件），正式文档被淹没。

---

## 二、目标架构

### 2.1 整体目录结构（重构后）


```
项目根目录/
├── src/
│   ├── api/                    # ← 重构重点：聚宽 API 兼容层
│   ├── core/                   # 核心运行时（不变）
│   ├── utils/                  # 工具函数（不变）
│   ├── finance_data/           # 财务数据（不变）
│   ├── market_data/            # 市场数据（不变）
│   ├── factors/                # 因子计算（不变）
│   ├── indicators/             # 指标（不变）
│   ├── db/                     # 数据库（不变）
│   ├── signals/                # 信号（不变）
│   ├── risk/                   # 风险（不变）
│   └── strategy/               # 策略框架（不变）
│
├── strategies/                 # ← 新增：策略代码统一存放（从 src/ 迁出）
│   ├── 02_7年40倍绩优低价超跌缩量小盘/
│   ├── 03_高评分ETF策略之核心资产轮动/
│   └── ...（所有 src/02_xxx ~ src/99_xxx 目录迁移至此）
│
├── tools/                      # ← 新增：开发工具脚本
│   ├── gap_analyzer.py         # 从 src/api/ 迁移
│   ├── data/                   # 从 scripts/data/ 迁移
│   │   ├── download_common_stocks.py
│   │   └── prewarm_data.py
│   ├── offline_data/           # 从 scripts/offline_data/ 迁移（保持内部结构）
│   │   ├── prewarm_all.py
│   │   ├── prewarm_daily.py
│   │   └── ...
│   └── validation/             # 从 scripts/validation/ 迁移
│       ├── validate_strategies.py
│       └── validate_resource_dependencies.py
│
├── tests/
│   ├── unit/                   # 单元测试（已有，整理）
│   ├── integration/            # 集成测试（已有，整理）
│   ├── regression/             # 回归测试（已有，整理）
│   └── conftest.py
│
├── docs/
│   ├── guides/                 # 使用指南（已有）
│   ├── design/                 # 设计文档（已有）
│   ├── api/                    # API 参考文档（已有，待填充）
│   ├── strategy_framework/     # 策略框架文档（已有）
│   └── archive/                # ← 新增：归档临时报告
│       └── 0330_result/        # 从 docs/ 根目录迁移
│
└── data/
    └── cache/                  # 缓存统一在此（已完成）
```

---

## 三、src/api 层重构方案

### 3.1 重构后文件结构

```
src/api/
├── __init__.py          # 重写：分组导出，清晰的公共接口
├── _internal/           # 私有工具（不对外暴露）
│   ├── __init__.py
│   └── symbol_utils.py  # _normalize_symbol, _calculate_limit_price 等共享私有函数
├── market.py            # 合并 market_api.py + market_api_enhanced.py
├── order.py             # 从 enhancements.py 拆出：订单相关函数
├── filter.py            # 合并 filter_api.py + enhancements.py 中的过滤函数
├── date.py              # 重命名自 date_api.py
├── stats.py             # 重命名自 stats_api.py
├── factor.py            # 重命名自 factor_api.py
├── billboard.py         # 重命名自 billboard_api.py
├── indicators.py        # 保持不变
├── finance.py           # 合并 missing_apis.py 中的财务类 API（get_locked_shares 等）
└── cache.py             # 从 optimizations.py 拆出：缓存与性能优化
```

### 3.2 文件职责映射（旧 → 新）


| 旧文件 | 旧内容 | 新文件 | 说明 |
|--------|--------|--------|------|
| `market_api.py` | `get_price`, `history`, `attribute_history`, `get_bars` | `market.py` | 合并 |
| `market_api_enhanced.py` | `get_market`, `get_detailed_quote`, `get_ticks_enhanced` | `market.py` | 合并，消除重复私有函数 |
| `enhancements.py` | `order_shares`, `order_target_percent` | `order.py` | 拆分 |
| `enhancements.py` | `filter_st`, `filter_paused`, `filter_limit_up/down`, `filter_new_stocks` | `filter.py` | 合并到 filter |
| `enhancements.py` | `get_open_price`, `get_close_price`, `get_high/low_limit` | `market.py` | 归入行情模块 |
| `enhancements.py` | `LimitOrderStyle`, `MarketOrderStyle` | `order.py` | 归入订单模块 |
| `enhancements.py` | `rebalance_portfolio`, `get_portfolio_weights`, `calculate_position_value` | `order.py` | 归入订单/组合模块 |
| `missing_apis.py` | `get_locked_shares`, `get_fund_info`, `get_fundamentals_continuously` | `finance.py` | 正式命名 |
| `missing_apis.py` | `get_beta` | `stats.py` | 归入统计模块 |
| `optimizations.py` | `CurrentDataCache`, `get_current_data_cached/batch` | `cache.py` | 拆分 |
| `optimizations.py` | `BatchDataLoader`, `DataPreloader`, `warm_up_cache` | `cache.py` | 拆分 |
| `optimizations.py` | `optimize_dataframe_memory`, `get_memory_usage`, `cleanup_memory` | `cache.py` | 拆分 |
| `gap_analyzer.py` | `APIGapAnalyzer`, `analyze_api_gaps` | `tools/gap_analyzer.py` | 迁出 api 层 |
| `filter_api.py` | `get_dividend_ratio_filter_list`, `filter_new_stock` 等 | `filter.py` | 合并 |
| `date_api.py` | 日期相关函数 | `date.py` | 重命名 |
| `stats_api.py` | 统计函数 | `stats.py` | 重命名 |
| `factor_api.py` | 因子函数 | `factor.py` | 重命名 |
| `billboard_api.py` | 榜单函数 | `billboard.py` | 重命名 |

### 3.3 私有工具模块：`_internal/symbol_utils.py`

当前 `market_api.py` 和 `market_api_enhanced.py` 中存在完全重复的私有函数，
统一提取到 `_internal/symbol_utils.py`：

```python
# src/api/_internal/symbol_utils.py

def normalize_symbol(symbol: str) -> str:
    """统一股票代码格式为 6 位数字"""
    ...

def get_symbol_prefix(symbol: str) -> str:
    """获取 sh/sz 前缀"""
    ...

def is_gem_or_star(code: str) -> bool:
    """判断创业板/科创板"""
    ...

def calculate_limit_price(prev_close: float, code: str, direction: str) -> float | None:
    """计算涨跌停价"""
    ...
```

### 3.4 重构后 `__init__.py` 结构

```python
# src/api/__init__.py
# 按功能分组导出，每组有清晰注释

# --- 行情数据 ---
from .market import get_price, history, attribute_history, get_bars
from .market import get_market, get_detailed_quote, get_ticks_enhanced
from .market import get_open_price, get_close_price, get_high_limit, get_low_limit

# --- 订单与组合 ---
from .order import order_shares, order_target_percent
from .order import LimitOrderStyle, MarketOrderStyle
from .order import rebalance_portfolio, get_portfolio_weights, calculate_position_value

# --- 过滤工具 ---
from .filter import filter_st, filter_paused, filter_limit_up, filter_limit_down
from .filter import filter_new_stocks, filter_new_stock, filter_st_stock, filter_paused_stock
from .filter import get_dividend_ratio_filter_list, get_margine_stocks, apply_common_filters

# --- 财务数据 ---
from .finance import get_locked_shares, get_fund_info, get_fundamentals_continuously

# --- 统计与因子 ---
from .stats import get_ols, get_zscore, get_rank, get_factor_filter_list, get_num, get_beta
from .factor import get_north_factor, get_comb_factor, get_factor_momentum

# --- 日期工具 ---
from .date import (get_shifted_date, get_previous_trade_date, get_next_trade_date,
                   transform_date, is_trade_date, get_trade_dates_between,
                   count_trade_dates_between, clear_trade_days_cache)

# --- 技术指标 ---
from .indicators import MA, EMA, MACD, KDJ, RSI, BOLL, ATR

# --- 榜单数据 ---
from .billboard import (get_billboard_list, get_institutional_holdings,
                        get_billboard_hot_stocks, get_broker_statistics)

# --- 缓存与性能 ---
from .cache import (CurrentDataCache, get_current_data_cached, get_current_data_batch,
                    BatchDataLoader, DataPreloader, warm_up_cache,
                    get_memory_usage, cleanup_memory)
```

---

## 四、策略目录迁移方案

### 4.1 问题

`src/` 下有 80+ 个策略目录（`src/02_xxx/` 到 `src/99_xxx/`），
与核心模块（`src/api/`、`src/core/` 等）混在一起。

### 4.2 方案

新建 `strategies/` 目录，将所有策略目录从 `src/` 迁移至 `strategies/`。

```
# 迁移前
src/02_7年40倍绩优低价超跌缩量小盘/
src/03_高评分ETF策略之核心资产轮动/
...

# 迁移后
strategies/02_7年40倍绩优低价超跌缩量小盘/
strategies/03_高评分ETF策略之核心资产轮动/
...
```

同时，`src/` 根目录下的散落文件也需要整理：

| 文件 | 处理方式 |
|------|----------|
| `src/market_api.py` | 删除（与 `src/api/market_api.py` 重复，是旧版残留） |
| `src/backtrader_base_strategy.py` | 评估是否并入 `src/core/` |
| `src/dependency_checker.py` | 迁移到 `tools/` |
| `src/subportfolios.py` | 评估是否并入 `src/core/` 或 `src/strategy/` |
| `src/strategy_converted/` | 迁移到 `strategies/converted/` |
| `src/test_cache_fail/` | 删除（测试临时目录） |
| `src/test_simple_strategy/` | 迁移到 `tests/fixtures/` |

---

## 五、scripts/ 目录整理方案

### 5.1 现状

`scripts/` 根目录下有 12 个散落文件，加上 4 个子目录，内容性质混杂。

### 5.2 处理方案

| 文件/目录 | 性质 | 处理方式 |
|-----------|------|----------|
| `scripts/task14_minute_minimal_test.py` | 历史任务临时脚本 | **删除** |
| `scripts/task14_minute_strategy_baseline.py` | 历史任务临时脚本 | **删除** |
| `scripts/task14_minute_strategy_real_test.py` | 历史任务临时脚本 | **删除** |
| `scripts/task26_minute_real_validation.py` | 历史任务临时脚本 | **删除** |
| `scripts/task37_txt_normalization_test.py` | 历史任务临时脚本 | **删除** |
| `scripts/test_txt_normalization.py` | 历史任务临时脚本 | **删除** |
| `scripts/tasks/task23_load_whitelist.py` | 历史任务临时脚本 | **删除** |
| `scripts/tasks/task23_real_whitelist.py` | 历史任务临时脚本 | **删除** |
| `scripts/tasks/task31_daily_true_run_pool.py` | 历史任务临时脚本 | **删除** |
| `scripts/tasks/task31_extend_pool.py` | 历史任务临时脚本 | **删除** |
| `scripts/data/` | 数据下载/预热工具 | **迁移到 `tools/data/`** |
| `scripts/offline_data/` | 离线数据管理（有 README） | **迁移到 `tools/offline_data/`** |
| `scripts/validation/` | 策略验证工具 | **迁移到 `tools/validation/`** |
| `scripts/examples/` | 功能演示示例 | **迁移到 `docs/examples/`** |
| `scripts/scan_resource_dependencies.py` | 依赖扫描工具 | **迁移到 `tools/`** |
| `scripts/validate_resource_dependencies.py` | 依赖验证工具 | **迁移到 `tools/validation/`** |
| `scripts/validate_syntax_recovery.py` | 语法验证工具 | **迁移到 `tools/validation/`** |
| `scripts/run_tests.py` | 测试辅助脚本 | **迁移到根目录** |
| `scripts/test_summary.sh` | 测试辅助脚本 | **迁移到根目录** |
| `scripts/activate_env.sh` | 环境激活脚本 | **迁移到根目录** |

整理完成后，`scripts/` 目录可以整体删除。

### 5.3 整理后 tools/ 结构

```
tools/
├── gap_analyzer.py              # 从 src/api/ 迁移
├── scan_resource_dependencies.py # 从 scripts/ 迁移
├── data/                        # 从 scripts/data/ 迁移
│   ├── download_common_stocks.py
│   └── prewarm_data.py
├── offline_data/                # 从 scripts/offline_data/ 迁移（保持内部结构）
│   ├── config.yaml
│   ├── prewarm_all.py
│   ├── prewarm_daily.py
│   ├── prewarm_monthly.py
│   ├── prewarm_quarterly.py
│   ├── prewarm_static.py
│   ├── prewarm_weekly.py
│   ├── README.md
│   └── utils/
└── validation/                  # 从 scripts/validation/ 迁移
    ├── validate_strategies.py
    ├── validate_resource_dependencies.py
    ├── validate_syntax_recovery.py
    ├── validate_with_package.py
    └── validate_with_package_fixed.py
```

`docs/examples/` 新增：

```
docs/examples/                   # 从 scripts/examples/ 迁移
├── demo_new_features.py
├── demo_runtime_io_usage.py
└── demo_task08_index_components.py
```

---

## 六、测试结构规划

### 6.1 现状

`tests/` 根目录下 70+ 个文件，同一模块有多个测试文件（如 `test_market_api.py`、
`test_market_api_unit.py`、`test_market_api_enhanced.py`），命名不一致。

### 6.2 目标结构

```
tests/
├── conftest.py                  # 全局 fixtures
├── unit/                        # 单元测试：测单个函数，不依赖外部数据
│   ├── api/
│   │   ├── test_market.py       # 合并 test_market_api*.py
│   │   ├── test_filter.py       # 合并 filter 相关测试
│   │   ├── test_date.py
│   │   ├── test_stats.py
│   │   ├── test_indicators.py
│   │   └── test_order.py
│   ├── core/
│   │   └── test_runner.py
│   └── utils/
│       └── test_symbol_utils.py
├── integration/                 # 集成测试：需要真实数据或数据库
│   ├── test_market_data.py
│   ├── test_finance_data.py
│   └── test_duckdb.py
├── regression/                  # 回归测试：防止已修复 bug 复现
│   └── test_api_compatibility.py
└── fixtures/                    # 测试数据和 mock
    ├── mock_data/
    └── sample_strategies/
```

### 6.3 测试文件合并计划

| 现有文件（合并来源） | 新文件 |
|---------------------|--------|
| `test_market_api.py`, `test_market_api_unit.py`, `test_market_api_enhanced.py` | `unit/api/test_market.py` |
| `test_filter_api.py`（如有）, filter 相关 | `unit/api/test_filter.py` |
| `test_data_utils.py`, `test_date_api.py`（如有） | `unit/api/test_date.py` |
| `test_indicators_api.py` | `unit/api/test_indicators.py` |
| `test_duckdb_integration.py` | `integration/test_duckdb.py` |
| `test_api_compatibility.py` | `regression/test_api_compatibility.py` |

---

## 七、文档结构规划

### 7.1 目标结构

```
docs/
├── README.md                    # 文档导航
├── guides/                      # 使用指南（已有）
│   ├── QUICK_START.md
│   ├── DEPENDENCIES.md
│   └── run_strategies_parallel_README.md
├── api/                         # API 参考（待填充）
│   ├── market.md                # 行情 API
│   ├── filter.md                # 过滤 API
│   ├── order.md                 # 订单 API
│   ├── date.md                  # 日期 API
│   └── finance.md               # 财务 API
├── design/                      # 设计文档（已有）
│   ├── strategy_run_analysis.md
│   └── api_layer_refactor.md    # 本文档
├── strategy_framework/          # 策略框架文档（已有）
└── archive/                     # 归档：临时报告、历史结果
    ├── 0330_result/             # 从 docs/ 根目录迁移
    └── strict_alignment_results/
```

### 7.2 需要清理的临时文件

以下文件从 `docs/` 根目录移入 `docs/archive/`：

- `all_tasks_completion_report.md`
- `all_tasks_implementation_report.md`
- `api_implementation_report.md`
- `implementation_status.md`
- `data_api_tasks.md`
- `api_supplements.md`

---

## 八、迁移策略（平滑过渡）

### 8.1 核心原则

**不破坏现有导入**。所有现有代码通过 `from src.api import xxx` 导入的符号，
重构后必须仍然可用。

### 8.2 分阶段执行

**阶段一：api 层内部重构（高优先级，低风险）**

1. 创建 `src/api/_internal/symbol_utils.py`，提取重复私有函数
2. 创建新文件（`market.py`、`order.py`、`filter.py`、`finance.py`、`cache.py`）
3. 将旧文件内容迁移到新文件
4. 旧文件保留，改为只做 re-export（兼容层）：
   ```python
   # src/api/market_api.py（兼容层，保留 6 个月后删除）
   # 已迁移到 src/api/market.py，此文件仅保留向后兼容
   from src.api.market import *  # noqa: F401, F403
   import warnings
   warnings.warn("market_api 已重命名为 market，请更新导入", DeprecationWarning, stacklevel=2)
   ```
5. 更新 `__init__.py`，从新文件导出

**阶段二：gap_analyzer 迁移（低风险）**

1. 将 `src/api/gap_analyzer.py` 复制到 `tools/gap_analyzer.py`
2. 更新 `src/api/__init__.py`，从 `tools/` 导入（或直接移除，因为这是开发工具）
3. 旧文件保留兼容层

**阶段三：策略目录迁移（需要验证）**

1. 新建 `strategies/` 目录
2. 逐批迁移策略目录（每次迁移后运行测试验证）
3. 更新 `pyproject.toml` 中的 `setuptools.packages.find` 配置，排除 `strategies/`
4. 检查是否有代码硬编码了 `src/02_xxx` 路径

**阶段四：测试整理（持续进行）**

1. 新建 `tests/unit/api/`、`tests/integration/` 等子目录
2. 逐步将根目录测试文件迁移到对应子目录
3. 合并重复测试文件
4. 旧测试文件保留直到新测试覆盖率达到同等水平

**阶段五：scripts/ 整理（与文档整理并行）**

1. 删除所有 `task*_*.py` 历史任务脚本
2. 将 `scripts/data/`、`scripts/offline_data/`、`scripts/validation/` 迁移到 `tools/`
3. 将 `scripts/examples/` 迁移到 `docs/examples/`
4. 将 `scripts/run_tests.py`、`scripts/test_summary.sh`、`scripts/activate_env.sh` 移到根目录
5. 删除空的 `scripts/` 目录

**阶段六：文档整理（低优先级）**

1. 新建 `docs/archive/`
2. 将临时报告文件移入 `docs/archive/`
3. 逐步填充 `docs/api/` 下的 API 参考文档

### 8.3 验证检查点

每个阶段完成后执行：

```bash
# 1. 确认所有现有导入仍然有效
python -c "from src.api import get_price, history, filter_st, order_shares; print('OK')"

# 2. 运行回归测试
pytest tests/regression/ -v

# 3. 运行 API 兼容性测试
pytest tests/test_api_compatibility.py -v

# 4. 检查无循环导入
python -c "import src.api"
```

---

## 九、关键设计决策

### 9.1 为什么合并 market_api.py 和 market_api_enhanced.py

两个文件中 `_normalize_symbol`、`_get_symbol_prefix`、`_is_gem_or_star`、
`_calculate_limit_price`、`_fetch_price_data` 等私有函数完全重复，
维护时需要同步修改两处，容易产生不一致。合并后消除重复，统一维护。

### 9.2 为什么 gap_analyzer.py 不属于 api 层

`gap_analyzer.py` 是一个**开发期分析工具**，用于扫描策略文件统计 API 使用情况，
生成报告。它不提供任何运行时 API，不应该被策略代码导入。
放在 `src/api/` 下会误导开发者认为它是运行时 API 的一部分。

### 9.3 为什么 missing_apis.py 要拆分而不是整体重命名

`missing_apis.py` 中的内容属于两个不同领域：
- `get_locked_shares`、`get_fund_info`、`get_fundamentals_continuously` → 财务数据，归入 `finance.py`
- `get_beta` → 统计计算，归入 `stats.py`

整体重命名为 `finance.py` 会让 `get_beta` 的归属产生歧义。

### 9.4 兼容层保留策略

旧文件名（`market_api.py`、`enhancements.py` 等）作为兼容层保留，
通过 `DeprecationWarning` 提示开发者迁移，6 个月后删除。
这样可以保证：
- 现有策略代码无需修改
- 开发者有足够时间迁移
- 不会因为重构导致生产环境故障

### 9.5 为什么 scripts/ 要整体废弃而不是保留

`scripts/` 目录本身没有清晰的语义边界——它混杂了工具、示例、测试辅助和历史垃圾。
废弃后按性质分流到 `tools/`、`docs/examples/` 和根目录，每个目标位置的语义都更清晰。

---

## 十、正确性属性

*属性是在系统所有有效执行中都应该成立的特征或行为——本质上是关于系统应该做什么的形式化陈述。属性是人类可读规范与机器可验证正确性保证之间的桥梁。*

### 属性 1：_internal 符号不对外暴露

对于 `src/api/_internal/` 下的**任意**符号，该符号都不应该出现在 `src/api/__init__.py` 的 `__all__` 列表中。

**验证：需求 1.3**

### 属性 2：向后兼容性（符号集合包含）

对于重构前 `src/api/__init__.py` 中可导入的**任意**符号名，重构后执行 `from src.api import <符号名>` 都应该成功，不抛出 `ImportError`。

**验证：需求 3.2、需求 10.1**

### 属性 3：兼容层触发 DeprecationWarning

对于**任意**兼容层文件（`market_api.py`、`market_api_enhanced.py`、`enhancements.py`、`missing_apis.py`、`optimizations.py`、`filter_api.py`），导入该文件时都应该触发 `DeprecationWarning`。

**验证：需求 4.2**

### 属性 4：策略目录完整迁移

对于 `src/` 下**任意**以数字编号开头的目录（匹配 `[0-9][0-9]_*` 模式），迁移完成后该目录应该在 `strategies/` 下存在，且在 `src/` 下不再存在。

**验证：需求 6.2**

### 属性 5：历史任务脚本完全删除

对于 `scripts/` 下**任意**匹配 `task[0-9]*_*.py` 模式的文件，删除操作完成后该文件不应该在文件系统中存在。

**验证：需求 7.1**

### 属性 6：tools/offline_data 内部路径完整性

对于 `tools/offline_data/` 内部**任意**使用相对路径引用的文件（如引用 `config.yaml`、`utils/`），迁移完成后这些相对路径引用应该仍然有效，不产生 `FileNotFoundError`。

**验证：需求 7.10**

### 属性 7：docs/ 根目录条目约束

迁移完成后，`docs/` 根目录的条目集合应该是 `{README.md, guides/, api/, design/, strategy_framework/, examples/, archive/}` 的子集，不包含任何临时报告文件（`*_report.md`、`*_result.md`、`*_tasks.md`、`*_supplements.md`）。

**验证：需求 9.5**
