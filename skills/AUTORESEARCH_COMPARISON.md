# Autoresearch 系统对比分析

## 四个系统概览

| 系统 | 平台 | 优化对象 | 初始化脚本 | 迭代脚本 | 执行器 | 变异器 |
|------|------|---------|-----------|---------|--------|--------|
| **autoresearch_ricequant** | RiceQuant | Python 代码 | `setup.py` | `run_iteration.py` | `ricequant_executor.py` | ❌ (agent 自由发挥) |
| **autoresearch_ricequant-wizard** | RiceQuant | JSON 配置 | `setup.py` | `run_iteration_wizard.py` | `wizard_executor.py` | `wizard_mutator.py` |
| **autoresearch_joinquant** | JoinQuant | Python 代码 | `setup.py` | `run_iteration.py` | `joinquant_executor.py` | ❌ (agent 自由发挥) |
| **autoresearch_guorn_strategy** | 果仁网 | JSON 配置 | `setup.py` | `run_iteration.py` | `guorn_executor.py` | `guorn_mutator.py` |

---

## 发现的不一致问题

### 1. 初始化脚本命名不一致

| 系统 | 当前命名 | 应该统一为 |
|------|---------|-----------|
| autoresearch_ricequant | ✅ `setup.py` | `setup.py` |
| autoresearch_ricequant-wizard | ❌ `init_experiment.py` + `setup.py` | `setup.py` |
| autoresearch_joinquant | ✅ `setup.py` | `setup.py` |
| autoresearch_guorn_strategy | ✅ `setup.py` | `setup.py` |

**问题**：`autoresearch_ricequant-wizard` 同时有 `init_experiment.py` 和 `setup.py`，功能重复。

**建议**：删除 `init_experiment.py`，统一使用 `setup.py`。

---

### 2. 迭代脚本命名不一致

| 系统 | 当前命名 | 应该统一为 |
|------|---------|-----------|
| autoresearch_ricequant | ✅ `run_iteration.py` | `run_iteration.py` |
| autoresearch_ricequant-wizard | ❌ `run_iteration_wizard.py` | `run_iteration.py` |
| autoresearch_joinquant | ✅ `run_iteration.py` | `run_iteration.py` |
| autoresearch_guorn_strategy | ✅ `run_iteration.py` | `run_iteration.py` |

**问题**：`autoresearch_ricequant-wizard` 使用 `run_iteration_wizard.py`，与其他三个不一致。

**建议**：重命名为 `run_iteration.py`，保持一致性。

---

### 3. Agent 指南文档命名不一致

| 系统 | 当前命名 | 应该统一为 |
|------|---------|-----------|
| autoresearch_ricequant | ✅ `program.md` + `program_enhance.md` | `program.md` |
| autoresearch_ricequant-wizard | ❌ `program_wizard.md` | `program.md` |
| autoresearch_joinquant | ✅ `program.md` + `program_enhance.md` | `program.md` |
| autoresearch_guorn_strategy | ✅ `program.md` | `program.md` |

**问题**：`autoresearch_ricequant-wizard` 使用 `program_wizard.md`，与其他三个不一致。

**建议**：重命名为 `program.md`，保持一致性。

---

### 4. 配置文件命名不一致

| 系统 | 配置文件名 | 种子配置文件名 |
|------|-----------|--------------|
| autoresearch_ricequant | `strategy.py` | `seed_config.json` |
| autoresearch_ricequant-wizard | `wizard_config.json` | `seed_wizard_config.json` |
| autoresearch_joinquant | `strategy.py` | `seed_config.json` |
| autoresearch_guorn_strategy | `guorn_config.json` | `seed_config.json` |

**问题**：
- wizard 使用 `wizard_config.json` 和 `seed_wizard_config.json`
- guorn 使用 `guorn_config.json` 和 `seed_config.json`

**建议**：统一为 `config.json` 和 `seed_config.json`（或保持平台特色命名，但需在文档中明确说明）。

---

### 5. 实验目录命名规则不一致

| 系统 | 实验目录前缀 |
|------|------------|
| autoresearch_ricequant | `strategy_autoresearch_<name>` |
| autoresearch_ricequant-wizard | `experiments/<name>` |
| autoresearch_joinquant | `strategy_autoresearch_jq_<name>` |
| autoresearch_guorn_strategy | `experiments/<name>` |

**问题**：
- ricequant 和 joinquant 使用 `strategy_autoresearch_*` 前缀
- wizard 和 guorn 使用 `experiments/` 子目录

**建议**：统一使用 `experiments/<name>` 结构，更清晰。

---

### 6. README 文档结构不一致

| 系统 | 快速开始路径 | 文件结构说明 | 评分公式 |
|------|------------|------------|---------|
| autoresearch_ricequant | ✅ 有 | ✅ 有 | ✅ 有 |
| autoresearch_ricequant-wizard | ✅ 有 | ✅ 有 | ✅ 有 |
| autoresearch_joinquant | ✅ 有 | ✅ 有 | ✅ 有 |
| autoresearch_guorn_strategy | ✅ 有 | ✅ 有 | ✅ 有 |

**问题**：wizard 的 README 过于详细（12KB），其他三个较简洁（2-3KB）。

**建议**：将 wizard 的详细文档拆分到单独的文档中（如 `WIZARD_GUIDE.md`），README 保持简洁。

---

### 7. 缺少的文件

| 系统 | `analyze.py` | `preflight_checker.py` | `__init__.py` |
|------|-------------|----------------------|--------------|
| autoresearch_ricequant | ✅ 有 | ✅ 有 | ❌ 无 |
| autoresearch_ricequant-wizard | ❌ 无 | ❌ 无 | ❌ 无 |
| autoresearch_joinquant | ✅ 有 | ✅ 有 | ❌ 无 |
| autoresearch_guorn_strategy | ❌ 无 | ❌ 无 | ✅ 有 |

**问题**：
- wizard 缺少 `analyze.py` 和 `preflight_checker.py`
- guorn 缺少 `analyze.py` 和 `preflight_checker.py`
- ricequant 和 joinquant 缺少 `__init__.py`

**建议**：
- 如果 `analyze.py` 和 `preflight_checker.py` 是通用工具，应该在所有系统中提供
- 添加 `__init__.py` 使目录成为 Python 包

---

### 8. 文档中的路径引用不一致

**问题**：在 program.md 中，有些使用绝对路径，有些使用相对路径。

**示例**：
```bash
# autoresearch_ricequant/program.md
AUTORESEARCH_DIR="/Users/fengzhi/Downloads/git/testlixingren/skills/autoresearch_ricequant"

# autoresearch_joinquant/program.md
AUTORESEARCH_DIR="/Users/fengzhi/Downloads/git/testlixingren/skills/autoresearch_ricequant"  # ❌ 错误！
```

**建议**：统一使用相对路径或环境变量，避免硬编码绝对路径。

---

## 建议的统一规范

### 1. 文件命名规范

```
skills/autoresearch_<platform>/
├── setup.py                    # 初始化脚本（统一命名）
├── run_iteration.py            # 迭代脚本（统一命名）
├── <platform>_executor.py      # 平台执行器
├── <platform>_mutator.py       # 变异器（仅配置驱动系统）
├── scorer.py                   # 评分模块（统一）
├── program.md                  # Agent 指南（统一命名）
├── program_enhance.md          # 增强版指南（可选）
├── README.md                   # 简洁版说明
├── seed_config.json            # 种子配置
└── experiments/                # 实验目录（统一结构）
    └── <name>/
        ├── config.json         # 当前配置
        ├── state.json          # 状态文件
        ├── program.md          # Agent 指南副本
        └── history/
            ├── iterations.tsv
            ├── search_notes.md
            └── <iter>.json
```

### 2. 命令行接口统一

```bash
# 初始化
python setup.py --name <experiment_name> [options]

# 迭代
python run_iteration.py --base experiments/<name> --mutation-summary "..." [options]

# 分析
python analyze.py --base experiments/<name>
```

### 3. 配置文件统一

所有系统的 `seed_config.json` 应包含：
- `name`: 策略名称
- `platform`: 平台标识（ricequant/joinquant/guorn）
- `backtest`: 回测参数（start_date, end_date, capital, benchmark）
- `objective`: 优化目标（weights, hard_constraints）
- `loop`: 循环控制（max_iterations, max_consecutive_failures）

### 4. 文档结构统一

每个系统的 README.md 应包含：
1. 系统概述（1-2 段）
2. 文件结构
3. 快速开始（3 步）
4. 评分公式
5. 常见问题（可选）

详细文档放在单独文件中（如 `GUIDE.md`、`API.md`）。

---

## 优先级修复清单

### 高优先级（影响使用体验）

1. ✅ **已完成**：重命名 `autoresearch` → `autoresearch_ricequant`
2. ✅ **已完成**：重命名 `init_experiment.py` → `setup.py`（guorn）
3. ⚠️ **待修复**：重命名 `init_experiment.py` → `setup.py`（wizard）
4. ⚠️ **待修复**：重命名 `run_iteration_wizard.py` → `run_iteration.py`（wizard）
5. ⚠️ **待修复**：重命名 `program_wizard.md` → `program.md`（wizard）
6. ⚠️ **待修复**：修正 program.md 中的路径引用（joinquant）

### 中优先级（改善一致性）

7. 统一实验目录结构为 `experiments/<name>`
8. 统一配置文件命名为 `config.json`
9. 添加缺失的 `__init__.py` 文件
10. 简化 wizard 的 README.md

### 低优先级（可选优化）

11. 为 wizard 和 guorn 添加 `analyze.py`
12. 为 wizard 和 guorn 添加 `preflight_checker.py`
13. 统一所有系统的命令行参数格式
14. 创建共享的 `autoresearch_common` 模块

---

## 总结

四个系统的核心逻辑一致（setup → iterate → score → keep/rollback），但在命名、结构、文档方面存在不一致。建议优先修复高优先级问题，确保用户体验一致。
