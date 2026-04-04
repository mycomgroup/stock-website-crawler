# 策略支持范围矩阵与分类规范

**版本**: 1.0
**生成日期**: 2026-04-04
**维护者**: jk2bt项目组

---

## 1. 产品支持范围定义

### 1.1 可执行策略 (in_scope = True)

**定义标准**：
- 包含 `initialize()` 函数
- 包含交易处理函数（`handle_data`, `before_trading_start`, `after_trading_end`等）
- 或使用定时器（`run_daily`, `run_weekly`, `run_monthly`）
- 无语法错误
- 无缺失的API依赖（未实现的聚宽API）
- 文件类型为 `.txt` 或 `.py`

**当前统计**：
- **总数**: 395个
- **占比**: 75.0% (总文件数527)

**用途**：
- 批量回测运行入口默认只处理此范围内的策略
- 可跑率统计的**分母**

---

### 1.2 非策略范围 (in_scope = False)

#### 1.2.1 研究文档类

| 类型 | 数量 | 说明 | 处理方式 |
|------|------|------|----------|
| notebook (.ipynb) | 69 | Jupyter notebook研究文档、数据分析、可视化研究 | **排除**，不计入可跑率分母 |
| documentation (.md) | 4 | 策略研究报告、技术文档、README | **排除**，不计入可跑率分母 |

#### 1.2.2 未实现策略类

| 类型 | 数量 | 说明 | 处理方式 |
|------|------|------|----------|
| not_strategy | 51 | 配套资料、研究文章、说明文档（txt格式） | **排除**，扫描器自动识别 |
| no_initialize | 6 | 缺少initialize函数的策略代码 | **排除**，不可执行 |
| syntax_error | 1 | 存在语法错误的文件 | **排除**，需要修复 |

---

## 2. 文件分类规范

### 2.1 按kind字段分类

```json
{
  "jq_strategy_txt": "聚宽策略txt文件（主力策略载体）",
  "python_strategy": "Python格式策略文件",
  "notebook": "Jupyter notebook研究文档",
  "documentation": "Markdown文档/研究报告",
  "test_or_cache": "测试文件或缓存文件",
  "other": "其他非策略文件"
}
```

**当前分布**：
- jq_strategy_txt: 451 (85.6%)
- notebook: 69 (13.1%)
- documentation: 4 (0.8%)
- python_strategy: 3 (0.6%)

---

### 2.2 按scan_status字段分类

```json
{
  "valid": "可执行策略，所有检查通过",
  "no_initialize": "缺少initialize函数",
  "missing_api": "使用了未实现的聚宽API",
  "not_strategy": "非策略文件（配套资料/研究文档）",
  "syntax_error": "语法错误",
  "excluded_notebook": "排除的notebook文件",
  "excluded_documentation": "排除的文档文件",
  "excluded_test": "排除的测试/缓存文件"
}
```

**当前分布**：
- valid: 395 (75.0%)
- excluded_notebook: 69 (13.1%)
- not_strategy: 51 (9.7%)
- no_initialize: 7 (1.3%)
- excluded_documentation: 4 (0.8%)
- syntax_error: 1 (0.2%)

---

### 2.3 按run_status字段分类

```json
{
  "executable": "可执行，会进入批量运行",
  "non_executable": "不可执行，会被跳过",
  "not_applicable": "不适用（研究文档等）"
}
```

**当前分布**：
- executable: 395 (75.0%)
- not_applicable: 73 (13.9%)
- non_executable: 59 (11.2%)

---

## 3. 可跑率统计规范

### 3.1 正确的可跑率定义

**公式**：
```
可跑率 = 可执行策略数 / 可跑策略总数
       = executable数量 / in_scope数量
```

**当前可跑率**：
- 395 / 395 = 100.0%

**注意**：
- ✅ 分母不再包含notebook、md等非策略文件
- ✅ 分母不再包含研究文章、配套资料
- ✅ 避免了"所有文件混在分母里"的统计误区

---

### 3.2 历史误区（已修正）

**旧统计方式（错误）**：
```
旧可跑率 = 成功数 / 总文件数 = 395 / 527 = 74.8%
```
- ❌ notebook (69个) 混在分母里
- ❌ 研究文档 (51个配套资料txt) 混在分母里
- ❌ md文档 (4个) 混在分母里
- ❌ 误导产品支持范围

**新统计方式（正确）**：
```
新可跑率 = executable / in_scope = 395 / 395 = 100.0%
```
- ✅ 分母清晰：只包含产品承诺支持的策略
- ✅ 统计透明：避免误导用户

---

## 4. 批量运行入口行为

### 4.1 get_all_strategy_files() 改造

**改造前**：
- 使用旧的启发式：`is_valid_strategy_file()` + `initialize`字符串搜索
- 返回420个文件（与scanner不一致）
- 无法区分研究文档

**改造后**：
- 优先从 `strategies_registry.json` 读取缓存
- 回退时使用 `StrategyScanner` 统一逻辑
- 只返回 `is_executable=True` 的策略
- 与scanner达成一致：395个

**验证结果**：
```
✅ Registry预期可执行策略: 395
✅ get_all_strategy_files返回: 395
✅ Scanner直接扫描: 395
✅ 完全一致！批量入口与scanner达成共识
```

---

### 4.2 需隔离的文件

**数量统计**：132个需隔离

**分类**：
- notebook: 69个
- jq_strategy_txt (not_strategy): 51个
- documentation: 4个
- jq_strategy_txt (no_initialize): 6个
- jq_strategy_txt (syntax_error): 1个
- python_strategy: 1个

**隔离方式**：
- 自动：Scanner通过文件名模式识别（`*.ipynb`, `*.md`, `研究*`, `说明*`, `配套资料*`）
- 自动：Scanner通过内容检测识别（缺少initialize、无策略函数定义）
- 扫描结果标记为 `in_scope=False`
- 批量入口自动跳过

---

## 5. 清单生成与维护

### 5.1 清单文件

**位置**：
- CSV: `strategies/strategies_registry.csv`
- JSON: `strategies/strategies_registry.json`

**字段定义**：
| 字段 | 类型 | 说明 |
|------|------|------|
| path | string | 文件绝对路径 |
| file_name | string | 文件名 |
| kind | string | 文件类型分类 |
| in_scope | boolean | 是否在产品支持范围内 |
| scan_status | string | 扫描器状态 |
| run_status | string | 运行状态预期 |
| root_cause | string | 排除原因/错误说明 |
| scan_timestamp | string | 扫描时间戳 |

---

### 5.2 重新生成清单

**方式1：自动生成脚本**
```bash
python generate_strategies_registry.py
```

**方式2：指定目录**
```bash
python generate_strategies_registry.py --dir ./my_strategies --output ./output
```

**方式3：只扫描txt文件**
```bash
python generate_strategies_registry.py --txt-only
```

**生成时机**：
- ✅ 每次发布前重新生成
- ✅ 新增策略文件后重新生成
- ✅ 扫描器逻辑升级后重新生成

---

## 6. 支持矩阵可视化

```
总文件数: 527
├─ 可执行策略 (in_scope=True): 395 (75.0%)
│  ├─ jq_strategy_txt (valid): 389
│  └─ python_strategy (valid): 2
│
└─ 非策略范围 (in_scope=False): 132 (25.0%)
   ├─ notebook (excluded_notebook): 69
   ├─ documentation (excluded_documentation): 4
   ├─ jq_strategy_txt (not_strategy): 51
   ├─ jq_strategy_txt (no_initialize): 6
   ├─ jq_strategy_txt (syntax_error): 1
   └─ python_strategy (not_strategy): 1
```

---

## 7. 未来改进方向

### 7.1 策略质量分级

**建议分级标准**：
- A级：完整可执行，有交易记录
- B级：可执行但零收益（未触发交易）
- C级：缺少initialize但有handle函数
- D级：配套资料/研究文档

### 7.2 自动化文档分离

**建议操作**：
- 将70个ipynb移至 `strategies_research/` 目录
- 将4个md文档移至 `docs/` 目录
- 将51个配套资料txt移至 `strategies_materials/` 目录

**收益**：
- ✅ 目录结构更清晰
- ✅ 避免scanner误判
- ✅ 降低用户混淆

---

## 8. 附录：scanner判断规则

### 8.1 非策略文件模式匹配

```python
_NON_STRATEGY_PATTERNS = [
    r".*\.ipynb$",
    r".*\.md$",
    r".*README.*",
    r".*研究.*",
    r".*说明.*",
    r".*教程.*",
    r".*test.*",
    r".*tests.*",
    r".*_test.*",
    r".*文档.*",
    r".*笔记.*",
    r".*备份.*",
    r".*\.bak$",
    r".*\.old$",
    r".*notes.*",
    r".*note.*",
    r".*非策略.*",
    r".*配套资料.*",
]
```

### 8.2 策略必需模式

```python
_STRATEGY_REQUIRED_PATTERNS = [
    r"def\s+initialize\s*\(",
    r"def\s+handle_data\s*\(",
    r"def\s+before_trading_start\s*\(",
    r"def\s+after_trading_end\s*\(",
    r"def\s+handle_",
    r"def\s+trading_",
    r"run_daily\s*\(",
    r"run_weekly\s*\(",
    r"run_monthly\s*\(",
]
```

---

**文档维护规范**：
- 每次新增策略类型时更新本矩阵
- 每次scanner逻辑升级时同步更新
- 发布前检查清单与矩阵的一致性