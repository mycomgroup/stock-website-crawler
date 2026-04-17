# .db 依赖清理与迁移计划

## 背景

项目已全面将数据存储从 DuckDB/SQLite 迁移至 Parquet 缓存体系。本计划梳理当前代码库中残留的 `.db` 相关引用，明确迁移路径，确保多 Agent 并行运行时不再依赖任何 `.db` 文件。

## 现状梳理

### 1. 核心代码 `jk2bt/` ✅ 已解耦

- **无** `sqlite3` 或 `duckdb` 的直接 import 与连接代码。
- 残留 `.db` 字符串仅作为**历史兼容映射**存在：
  - `jk2bt/db/cache_config.py:335-349`：`DOMAIN_DB_MAPPING` 中仍使用 `data/market.db` 等旧路径作为字典 key。
  - `jk2bt/db/parquet_adapter.py:50-51`：运行时会自动将 `.db` 路径重写为 `_parquet` 目录。
  - 部分模块 docstring/注释中的 legacy 说明（如 `jk2bt/finance_data/` 下）。

### 2. 测试代码 `tests/` ⚠️ 仍有直接连接

| 文件 | 行号 | 问题描述 |
|------|------|----------|
| `tests/regression/test_offline_mode.py` | 27 | `duckdb.connect("data/market.db", read_only=True)` |
| `tests/regression/test_strategy_with_cache.py` | 62 | `db_path = "data/market.db"` |
| `tests/regression/test_task13_daily_baseline.py` | 187 | `os.path.join(..., "data", "market.db")` |
| `tests/regression/test_task32_minute_api.py` | 214 | `os.path.join(..., "data", "market.db")` |
| `tests/regression/test_task10_batch_runner.py` | 432 | `tempfile.mktemp(suffix=".db")` |
| `tests/regression/test_task24_prewarm_cache.py` | 42 | `os.path.join(tmpdir, "test_cache.db")` |
| `tests/unit/test_cache_status.py` | 47, 63 | `tmp_path / "custom_cache.db"`、`tmp_path / "test_cache.db"` |

### 3. 策略目录 `strategies/` ⚠️ 真实依赖

- `docs/archive/legacy_strategies/29 【策略.行业轮动】趋势-拥挤-景气度模型看行业轮动.ipynb`
  - `import sqlite3`
  - 连接外部 `.db` 文件：`../../basic_auto_get_factors/factors_base_Price_and_TAindex.db`、`factors_base_valuation.db`

### 4. 工具/配置/文档 ⚠️ 残留引用

| 文件 | 行号 | 问题描述 |
|------|------|----------|
| `tools/archive/migrate_duckdb_to_parquet.py` | 29-78 | 定义了 12 个 legacy DuckDB 文件迁移映射（如 `data/market.db`） |
| `config/default.json` | 6 | `"duckdb_path": "data/jk2bt.duckdb"` |
| `tools/data/download_common_stocks.py` | 281 | CLI 提示字符串：`sqlite3 data/market.db "SELECT COUNT(*) FROM stock_daily"` |
| `docs/` 多文件 | 各处 | 历史归档文档中仍有 `.db` 相关说明 |

## 迁移计划

### P0 - 清理真实运行时依赖（阻塞多 Agent）

1. **测试用例去 `.db` 化**
   - 将 `tests/regression/test_offline_mode.py:27` 的 `duckdb.connect` 替换为 `ParquetAdapter` 或 `get_cache_manager` 调用。
   - 将 `test_strategy_with_cache.py`、`test_task13_daily_baseline.py`、`test_task32_minute_api.py` 中的硬编码 `data/market.db` 改为指向 parquet 缓存目录。
   - 将 `test_task10_batch_runner.py`、`test_task24_prewarm_cache.py`、`test_cache_status.py` 中的 `.db` 临时文件后缀改为 `.parquet` 或 `_parquet` 目录。

2. **策略 notebook 迁移**
    - 评估 `docs/archive/legacy_strategies/29 【策略.行业轮动】趋势-拥挤-景气度模型看行业轮动.ipynb` 是否仍在维护：
     - 若仍在使用：将其 `sqlite3` 数据源切换为 parquet 或 akshare 实时接口。
     - 若已弃用：移至 `docs/archive/` 或标记为 deprecated。

### P1 - 清理配置与历史映射

3. **核心配置更新**
   - `config/default.json`：移除或注释掉 `duckdb_path` 字段，改为 `parquet_cache_root`。
   - `jk2bt/db/cache_config.py`：`DOMAIN_DB_MAPPING` 中的 key 从 `data/xxx.db` 重命名为 `xxx` 或 `xxx_parquet`，同步更新所有引用方。
   - `jk2bt/db/parquet_adapter.py`：当 `DOMAIN_DB_MAPPING` 不再返回 `.db` 路径后，可移除 `.db → _parquet` 的运行时转换逻辑。

4. **工具脚本更新**
    - `tools/archive/migrate_duckdb_to_parquet.py`：已迁移至 `tools/archive/`。
   - `tools/data/download_common_stocks.py:281`：将 CLI 提示中的 `sqlite3 data/market.db` 改为读取 parquet 缓存的校验命令（如 `python -c "from jk2bt.db.cache_status import get_cache_manager; ..."`）。

### P2 - 文档归档清理

5. **文档更新**
   - 新建 `docs/guides/parquet_migration_done.md` 说明迁移完成后的使用方式。
   - 将 `docs/archive/` 中涉及 `.db` 的历史文档统一移动至 `docs/archive/legacy_db_docs/` 子目录，避免搜索时产生误导。
   - 更新 `docs/README.md` 和 `docs/installation_validation.md`，删除 `.db` 相关的安装校验步骤。

## 验收标准

- [ ] `grep -r "\.db" --include="*.py" jk2bt/ tests/ strategies/` 仅命中 `.db` 包名（如 `jk2bt.db`）或明确归档路径。
- [ ] `grep -r "sqlite3" --include="*.py" jk2bt/ tests/ strategies/` 返回空。
- [ ] `grep -r "duckdb.connect" --include="*.py" tests/` 返回空。
- [ ] CI 中所有测试用例在**无** `data/*.db` 文件的环境下全部通过。
- [ ] `config/default.json` 中不再包含 `duckdb_path` 配置项。

## 相关文件索引

### 核心代码
- `jk2bt/db/cache_config.py`
- `jk2bt/db/parquet_adapter.py`
- `jk2bt/db/cache_status.py`

### 测试代码
- `tests/regression/test_offline_mode.py`
- `tests/regression/test_strategy_with_cache.py`
- `tests/regression/test_task13_daily_baseline.py`
- `tests/regression/test_task32_minute_api.py`
- `tests/regression/test_task10_batch_runner.py`
- `tests/regression/test_task24_prewarm_cache.py`
- `tests/unit/test_cache_status.py`

### 策略/工具/配置
- `docs/archive/legacy_strategies/29 【策略.行业轮动】趋势-拥挤-景气度模型看行业轮动.ipynb`
- `tools/archive/migrate_duckdb_to_parquet.py`
- `tools/data/download_common_stocks.py`
- `config/default.json`
