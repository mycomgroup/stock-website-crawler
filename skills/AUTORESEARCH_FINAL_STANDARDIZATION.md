# Autoresearch 系统最终标准化报告

## 执行日期
2026-04-12

---

## 完成的所有标准化任务

### 第一阶段：核心文件命名统一 ✅

1. **重命名 autoresearch → autoresearch_ricequant**
   - 目录已重命名
   - 所有文档中的路径引用已更新

2. **统一初始化脚本命名**
   - 所有系统都使用 `setup.py`
   - 删除了 wizard 中的重复文件 `init_experiment.py`

3. **统一迭代脚本命名**
   - `run_iteration_wizard.py` → `run_iteration.py`
   - 所有系统都使用 `run_iteration.py`

4. **统一 Agent 指南命名**
   - `program_wizard.md` → `program.md`
   - 所有系统都使用 `program.md`

5. **修正路径引用错误**
   - 修正了 joinquant 中的 `AUTORESEARCH_DIR` 路径
   - 从 `skills/autoresearch_ricequant` 改为 `skills/autoresearch_joinquant`

6. **添加 Python 包结构**
   - 所有四个系统都添加了 `__init__.py`

### 第二阶段：进一步优化 ✅

7. **统一种子配置命名**
   - `seed_wizard_config.json` → `seed_config.json`
   - 所有系统现在都使用 `seed_config.json`

8. **简化 wizard README**
   - 将详细文档（12KB）拆分到 `WIZARD_GUIDE.md`
   - README 保持简洁（84 行，约 2KB）
   - 详细内容包括：配置结构、因子库、变异类型、技术架构

9. **添加分析工具**
   - 为 wizard 添加 `analyze.py`
   - 为 guorn 添加 `analyze.py`
   - 与 ricequant/joinquant 的 analyze.py 保持一致

10. **添加验证工具**
    - 为 wizard 添加 `validate.py`（验证 wizard_config.json）
    - 为 guorn 添加 `validate.py`（验证 guorn_config.json）
    - 支持严格模式（--strict）

---

## 最终文件结构对比

### autoresearch_ricequant（RiceQuant - Python 代码）

```
skills/autoresearch_ricequant/
├── __init__.py                ✅ 新增
├── setup.py                   ✅ 统一命名
├── run_iteration.py           ✅ 统一命名
├── ricequant_executor.py      ✅
├── scorer.py                  ✅
├── analyze.py                 ✅ 已有
├── preflight_checker.py       ✅ 已有
├── program.md                 ✅ 统一命名
├── program_enhance.md         ✅
└── seed_config.json           ✅ 统一命名
```

### autoresearch_ricequant-wizard（RiceQuant - JSON 配置）

```
skills/autoresearch_ricequant-wizard/
├── __init__.py                ✅ 新增
├── setup.py                   ✅ 统一命名
├── run_iteration.py           ✅ 重命名（原 run_iteration_wizard.py）
├── wizard_executor.py         ✅
├── wizard_mutator.py          ✅
├── scorer.py                  ✅
├── analyze.py                 ✅ 新增
├── validate.py                ✅ 新增
├── program.md                 ✅ 重命名（原 program_wizard.md）
├── seed_config.json           ✅ 重命名（原 seed_wizard_config.json）
├── README.md                  ✅ 简化（84 行）
└── WIZARD_GUIDE.md            ✅ 新增（详细文档）
```

### autoresearch_joinquant（JoinQuant - Python 代码）

```
skills/autoresearch_joinquant/
├── __init__.py                ✅ 新增
├── setup.py                   ✅ 统一命名
├── run_iteration.py           ✅ 统一命名
├── joinquant_executor.py      ✅
├── scorer.py                  ✅
├── analyze.py                 ✅ 已有
├── preflight_checker.py       ✅ 已有
├── program.md                 ✅ 统一命名（路径已修正）
├── program_enhance.md         ✅ 路径已修正
└── seed_config.json           ✅ 统一命名
```

### autoresearch_guorn_strategy（果仁网 - JSON 配置）

```
skills/autoresearch_guorn_strategy/
├── __init__.py                ✅ 已有
├── setup.py                   ✅ 统一命名
├── run_iteration.py           ✅ 统一命名
├── guorn_executor.py          ✅
├── guorn_mutator.py           ✅
├── scorer.py                  ✅
├── analyze.py                 ✅ 新增
├── validate.py                ✅ 新增
├── program.md                 ✅ 统一命名
└── seed_config.json           ✅ 统一命名
```

---

## 统一的命令行接口

所有四个系统现在使用相同的命令模式：

### 初始化实验

```bash
# ricequant (代码)
cd skills/autoresearch_ricequant
python setup.py --strategy-file /path/to/strategy.py

# wizard (配置)
cd skills/autoresearch_ricequant-wizard
python setup.py --name my_experiment

# joinquant (代码)
cd skills/autoresearch_joinquant
python setup.py --strategy-file /path/to/strategy.py

# guorn (配置)
cd skills/autoresearch_guorn_strategy
python setup.py --name my_experiment
```

### 运行迭代

```bash
# 所有系统统一使用
python run_iteration.py --base <experiment_dir> --mutation-summary "..." [options]
```

### 分析结果

```bash
# 所有系统统一使用
python analyze.py --base <experiment_dir>
```

### 验证配置（仅配置驱动系统）

```bash
# wizard
python validate.py --config experiments/<name>/wizard_config.json [--strict]

# guorn
python validate.py --config experiments/<name>/guorn_config.json [--strict]
```

---

## 工具脚本功能说明

### analyze.py

**功能**：分析实验结果，生成五个维度的报告

1. **总览**
   - keep/rollback/crash 统计
   - baseline vs champion 对比
   - 总提升（score, annual_return, max_drawdown）

2. **Keep 序列**
   - 改进路径
   - 每次 keep 的 mutation 和 score 提升

3. **Top 改进**
   - 按单次 score 提升排名
   - 识别最有效的改动

4. **失败模式分析**
   - rollback reason 分类
   - 反复失败的方向（高频词分析）
   - 最近 5 次失败

5. **指标趋势**
   - Score、Calmar、Sortino、IR 的 ASCII 折线图
   - 可视化迭代过程

6. **下一步建议**
   - 基于历史数据给出改进建议
   - 识别薄弱点
   - 避免重复失败的方向

**输出**：
- 终端打印报告
- 写入 `history/analysis_report.txt`（供 agent 读取）

### validate.py（仅 wizard/guorn）

**功能**：验证配置文件合法性

1. **JSON 格式正确性**
2. **必需字段完整性**
3. **因子名称有效性**（wizard）
4. **参数范围合理性**
5. **逻辑一致性**（严格模式）

**使用方法**：
```bash
python validate.py --config <config_file> [--strict]
```

**输出**：
- ✅ 配置验证通过
- ❌ 配置验证失败（列出所有错误）

---

## 文档结构统一

### README.md（所有系统）

简洁版说明（约 80-120 行）：
1. 系统概述（1-2 段）
2. 文件结构
3. 快速开始（3 步）
4. 评分公式
5. 相关资源

### 详细文档

- **ricequant/joinquant**：`program.md` + `program_enhance.md`
- **wizard**：`program.md` + `WIZARD_GUIDE.md`
- **guorn**：`program.md`

---

## 剩余的差异（设计差异，非问题）

### 1. 实验目录结构

- **ricequant/joinquant**: `strategy_autoresearch_*` 前缀，直接在根目录
- **wizard/guorn**: `experiments/` 子目录

**原因**：代码策略系统需要直接访问 `strategy.py`，而配置驱动系统使用子目录更清晰。

### 2. 配置文件命名

- **ricequant/joinquant**: `strategy.py` (Python 代码)
- **wizard**: `wizard_config.json` (JSON 配置)
- **guorn**: `guorn_config.json` (JSON 配置)

**原因**：不同平台的配置格式不同，保留平台特色命名有助于区分。

### 3. 工具文件差异

- **ricequant/joinquant**: 有 `preflight_checker.py`
- **wizard/guorn**: 无 `preflight_checker.py`（但有 `validate.py`）

**原因**：代码策略需要预检查 Python 语法，配置驱动系统使用 validate.py 验证 JSON。

---

## 验证清单

- [x] 所有系统都有 `setup.py`
- [x] 所有系统都有 `run_iteration.py`
- [x] 所有系统都有 `program.md`
- [x] 所有系统都有 `__init__.py`
- [x] 所有系统都有 `scorer.py`
- [x] 所有系统都有 `seed_config.json`
- [x] 所有系统都有 `analyze.py`
- [x] wizard/guorn 都有 `validate.py`
- [x] 路径引用正确（无交叉引用）
- [x] 文档中的命令示例正确
- [x] Spec 文件引用正确
- [x] README 简洁（80-120 行）
- [x] 详细文档已拆分

---

## 总结

✅ **所有标准化任务已完成**

四个 autoresearch 系统现在具有：
- ✅ 统一的文件命名规范
- ✅ 统一的命令行接口
- ✅ 统一的文档结构
- ✅ 统一的 Python 包结构
- ✅ 完整的工具脚本（analyze.py, validate.py）
- ✅ 简洁的 README + 详细的指南文档

剩余的差异是由于平台特性和设计选择导致的，不影响使用体验。

**系统已达到生产就绪状态。**

---

## 相关文档

- [AUTORESEARCH_COMPARISON.md](./AUTORESEARCH_COMPARISON.md) - 四个系统的详细对比
- [AUTORESEARCH_STANDARDIZATION_COMPLETE.md](./AUTORESEARCH_STANDARDIZATION_COMPLETE.md) - 标准化过程记录
- [autoresearch_ricequant/README.md](./autoresearch_ricequant/README.md)
- [autoresearch_ricequant-wizard/README.md](./autoresearch_ricequant-wizard/README.md)
- [autoresearch_ricequant-wizard/WIZARD_GUIDE.md](./autoresearch_ricequant-wizard/WIZARD_GUIDE.md)
- [autoresearch_joinquant/README.md](./autoresearch_joinquant/README.md)
- [autoresearch_guorn_strategy/README.md](./autoresearch_guorn_strategy/README.md)
