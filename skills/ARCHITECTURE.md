# Skills 架构文档

## 概述

`skills/` 目录是本项目的核心能力库，包含多个独立的 Skill 模块，覆盖量化策略研发的完整链路：**数据获取 → 策略回测 → 策略迭代 → 组合管理**。

每个 Skill 独立运行，有明确的职责边界，通过标准化接口协作。

---

## 整体架构

```
skills/
│
├── 数据层
│   ├── query_data/              # 多数据源查询（A股/美股/宏观）
│   ├── lixinger-screener/       # 理杏仁股票筛选器
│   └── url-pattern-analyzer/    # URL 模式分析（爬虫辅助）
│
├── 网页工具层
│   ├── web-api-generator/       # URL patterns → API 文档/配置
│   └── html-template-generator/ # 网页 → XPath 模板 → Markdown
│
├── 策略回测层（多平台）
│   ├── backtest_guide/          # 平台选择指南 + 通用文档
│   ├── joinquant_strategy/      # 聚宽策略运行器
│   ├── joinquant_nookbook/      # 聚宽 Notebook 研究
│   ├── ricequant_strategy/      # 米筐策略运行器（推荐日常使用）
│   ├── ricequant-wizard/        # 米筐辅助工具
│   ├── thsquant_strategy/       # 同花顺量化运行器
│   ├── bigquant_strategy/       # BigQuant AIStudio 运行器
│   └── guorn_strategy/          # 果仁网策略运行器
│
├── 策略研发层
│   ├── strategy_kits/           # 策略标准化接入与增强框架
│   └── autoresearch/            # 策略自动迭代优化系统
│
└── ARCHITECTURE.md              # 本文档
```

---

## 数据层

### query_data — 多数据源查询插件

**职责**：统一封装多个金融数据 API，支持 A 股、港股、美股、宏观数据查询。

**支持数据源**：

| 类型 | 数据源 |
|------|--------|
| A 股 | 理杏仁 (Lixinger)、AKShare |
| 美股 | Finnhub、FMP、Alpha Vantage、Tiingo、EODHD |
| 搜索 | Brave Search、Tavily、SerpAPI |
| 其他 | Eulerpool、Massive、AllTick、Financial Datasets |

**快速使用**：
```bash
cd skills/query_data
python3 test_datasource.py --source lixinger
python3 test_datasource.py --source finnhub --symbol AAPL
```

---

### lixinger-screener — 理杏仁股票筛选器

**职责**：通过理杏仁平台筛选 A 股/港股/美股，支持自然语言查询和结构化 JSON 条件。

**两种使用方式**：

```bash
cd skills/lixinger-screener

# 方式一：自然语言快速试错（浏览器版）
node run-skill.js --query "市盈率(TTM)小于20，股息率大于3%" --headless false

# 方式二：固化条件批量导出（request 版）
node request/fetch-lixinger-screener.js --input-file ./my-screen.json --output csv
```

**推荐工作流**：先用浏览器版试错，试出手感后固化成 `input.json`，再用 request 版批量导出。

---

### url-pattern-analyzer — URL 模式分析器

**职责**：从 `links.txt` 中识别 URL 模式，按路径结构聚类，生成正则表达式和 `url-patterns.json`。

**核心算法**：层次聚类 + 相似度评分（路径深度、路径段匹配、查询参数匹配）。

```bash
node skills/url-pattern-analyzer/main.js \
  --links-file stock-crawler/output/lixinger-crawler/links.txt \
  --output-file stock-crawler/output/lixinger-crawler/url-patterns.json
```

**输出格式**：
```json
{
  "patterns": [
    {
      "name": "api-doc",
      "pathTemplate": "/open/api/doc",
      "pattern": "^https://www\\.lixinger\\.com/open/api/doc\\?api-key=(.+)$",
      "urlCount": 163,
      "samples": ["..."]
    }
  ]
}
```

---

## 网页工具层

### web-api-generator — Web API 生成器

**职责**：将 `url-patterns.json` 转换为 API 文档和配置，提供命令行客户端进行网页抓取。

**工作流**：
```bash
cd skills/web-api-generator

# 1. 生成文档和配置
node main.js generate-docs

# 2. 分析数据选择器（可选）
node scripts/analyze-data-selectors.js --limit=5

# 3. 调用 API
node main.js call --api=constituents-list --param4=480301
```

---

### html-template-generator — HTML 模板生成器

**职责**：分析样本网页，自动生成 XPath 提取规则，将 HTML 渲染为结构化 Markdown。

**工作流（需人工确认）**：
```bash
cd skills/html-template-generator

# Phase 1: 生成单个模板并预览（必须人工确认）
node scripts/generate-and-test.js api-doc \
  --input ../../stock-crawler/output/lixinger-crawler/url-patterns.json \
  --output-dir ../../stock-crawler/output/lixinger-crawler/templates \
  --preview-dir ../../stock-crawler/output/lixinger-crawler/previews

# Phase 2: 确认无误后批量生成
node scripts/batch-generate-templates.js \
  --input ../../stock-crawler/output/lixinger-crawler/url-patterns.json \
  --output-dir ../../stock-crawler/output/lixinger-crawler/templates
```

---

## 策略回测层

### backtest_guide — 平台选择指南

**职责**：提供各量化平台的使用文档、平台选择建议、通用参数说明。

**平台选择速查**：

| 平台 | Skill 目录 | 适合场景 | 主要限制 |
|------|-----------|---------|---------|
| JoinQuant | `joinquant_strategy/` | 复杂因子、最终验证 | 需手动维护 session |
| RiceQuant | `ricequant_strategy/` | 日常开发、快速验证 | 策略编辑器 180min/天 |
| THSQuant | `thsquant_strategy/` | 同花顺生态 | 首次需手动登录 |
| BigQuant | `bigquant_strategy/` | AI/ML 策略 | Task-based，无策略 ID |
| GuornQuant | `guorn_strategy/` | 因子选股 | 结果不持久化 |

---

### joinquant_strategy — 聚宽策略运行器

**职责**：在聚宽平台提交策略、运行回测、查询结果。支持批量回测、归因分析。

```bash
cd skills/joinquant_strategy
node run-skill.js --id <algorithmId> --file ./my_strategy.py \
  --start 2021-01-01 --end 2024-12-31
node fetch-backtest-results.js --algorithm-id <id> --latest
```

**特点**：包含大量策略脚本（ETF 轮动、动量、价值、情绪切换等），适合复杂因子验证。

---

### joinquant_nookbook — 聚宽 Notebook 研究

**职责**：在聚宽 Notebook 环境中进行事件驱动研究和策略快速验证（Python 脚本直接运行）。

```bash
cd skills/joinquant_nookbook
python run_notebook.py
```

---

### ricequant_strategy — 米筐策略运行器（推荐）

**职责**：在米筐平台运行策略，支持策略编辑器回测和 Notebook 两种模式。

**核心优势**：Notebook 模式无每日 180 分钟时间限制，Session 自动管理。

```bash
cd skills/ricequant_strategy

# Notebook 模式（推荐，无时间限制）
node run-strategy.js --strategy examples/simple_backtest.py --create-new

# 策略编辑器模式
node run-skill.js --id <strategyId> --file ./my_strategy.py \
  --start 2021-01-01 --end 2024-12-31
```

**推荐流程**：Notebook → 快速验证逻辑 → 参数调优 → 策略编辑器精确回测。

---

### thsquant_strategy — 同花顺量化运行器

**职责**：在同花顺量化平台提交策略、运行回测。

```bash
cd skills/thsquant_strategy
node run-skill.js --id <algoId> --file ./my_strategy.py \
  --start 2023-01-01 --end 2024-12-31
```

---

### bigquant_strategy — BigQuant AIStudio 运行器

**职责**：在 BigQuant AIStudio 中运行策略代码和回测，支持 AI/ML 量化策略。

```bash
cd skills/bigquant_strategy
node run-skill.js --id <strategyId> --file examples/simple_backtest.py \
  --start 2022-01-01 --end 2025-03-28
```

**特点**：Task-based 架构，无策略 ID，按名称前缀查询历史结果。

---

### guorn_strategy — 果仁网策略运行器

**职责**：在果仁网平台运行因子选股策略，结果保存到本地。

```bash
cd skills/guorn_strategy
node run-skill.js
# 结果保存在 output/backtest-{timestamp}.json
```

**注意**：果仁网结果不持久化，每次回测后立即记录关键指标。

---

## 策略研发层

### strategy_kits — 策略标准化接入与增强框架

**职责**：把任意策略脚本接入标准化研发闭环，统一 contract、回测流程、报告产物。

**核心能力**：
1. 统一输入 contract：`pool_panel / score_panel / local_features`
2. 统一任务入口：`orchestration/task_runner.py`
3. 统一产物落盘：`summary.json`, `run_report.json`, `run_report.md`
4. 平台验证接入：配合 `backtest_guide` 做提交和结果拉取
5. 循环增强规范：每轮固定 5 步（本地回测 → 平台回测 → 差异归因 → 单点改动 → 版本结论）

**快速开始**：
```bash
# 环境自检
uv run pytest skills/strategy_kits/tests -q

# 执行本地回测
PYTHONPATH=skills python -m strategy_kits.orchestration.cli \
  --spec /abs/path/task_spec.json \
  --print-result-json
```

**目录结构**：
```
strategy_kits/
├── contracts/          # 输入/输出 contract 定义
├── core/               # 核心回测逻辑
├── execution/          # 执行引擎
├── orchestration/      # 任务调度（task_runner.py, cli）
├── portfolio/          # 组合管理
├── risk/               # 风险控制
├── signals/            # 信号生成
├── strategy_templates/ # 策略模板
├── universal_mechanisms/ # 通用机制（动量、股息、EPO 等）
├── docs/               # 架构设计、接入手册
└── tests/              # 单元测试
```

---

### autoresearch — 策略自动迭代优化系统

**职责**：输入一个成型的 RiceQuant 单文件策略，系统自动进行多轮迭代优化，全程留档可追溯。

**核心思想**：
- 每轮只允许修改策略脚本本身
- 以 RiceQuant 平台回测结果为目标函数
- 自动完成：提交回测 → 评分 → keep/rollback 决策 → 生成下一轮变异建议

**目标函数**（复合加权）：
```
score = annual_return × 0.45
      + max_drawdown × (-0.30)
      + sharpe × 0.20
      + win_rate × 0.05
```

**快速开始**：
```bash
cd skills/autoresearch

# 初始化实验环境
python initialize.py \
  --project-root /path/to/project \
  --strategy-name rfscore7_pb10_rq \
  --seed-strategy-path /path/to/strategy.py \
  --seed-config-path ./seed_config.json

# 运行自动迭代
python -c "
from orchestrator import AutoresearchOrchestrator
from pathlib import Path
o = AutoresearchOrchestrator(base_path=Path('skills/strategy_autoresearch_rfscore7_pb10_rq'))
o.run_loop(max_iterations=20)
"
```

**核心模块**：

| 模块 | 文件 | 作用 |
|------|------|------|
| 初始化 | `initialize.py` | 创建实验环境和目录结构 |
| 运行管理 | `run_manager.py` | 管理每轮迭代的目录和文件 |
| 平台执行器 | `ricequant_executor.py` | 封装 RiceQuant 回测提交和结果获取 |
| 预检查器 | `preflight_checker.py` | 提交前本地轻量检查（语法、编码等） |
| 评分器 | `scorer.py` | 解析回测结果，计算目标函数得分 |
| 台账 | `ledger.py` | 记录所有执行细节（TSV/JSONL/Markdown） |
| 变异生成器 | `mutator.py` | 生成策略修改建议 |

**推荐工作流**：
1. 先用 `strategy_kits` 或人工研究强化出单文件版本
2. 转成 RiceQuant 可运行脚本
3. 作为 `autoresearch` 的 seed
4. 让系统围绕这个脚本持续小步迭代

---

## Skill 间协作关系

```
query_data / lixinger-screener
        ↓ 数据获取
url-pattern-analyzer → web-api-generator → html-template-generator
        ↓ 爬虫辅助链路

strategy_kits（标准化接入）
        ↓ 生成 pool_panel / score_panel
backtest_guide（平台选择）
        ↓
joinquant_strategy / ricequant_strategy / thsquant_strategy / bigquant_strategy / guorn_strategy
        ↓ 回测结果
autoresearch（自动迭代优化）
```

---

## 通用约定

### Session 管理

- **RiceQuant / BigQuant**：自动管理，无需手动干预
- **JoinQuant**：需手动捕获 session：`node browser/capture-session.js --headed`
- **THSQuant**：首次需手动登录：`node browser/manual-login-capture.js`

### 重试策略（所有平台统一）

| 错误类型 | 第1次等待 | 第2次等待 | 第3次等待 |
|---------|---------|---------|---------|
| 429 / 503 并发限制 | 60s | 120s | 300s |
| 5xx 服务端错误 | 10s | 20s | 40s |
| 网络/超时 | 5s | 10s | 20s |

### 环境变量

每个 Skill 目录下有 `.env` 文件，参考 `.env.example` 配置账号凭证。

### 输出目录

各平台回测结果保存在各自 Skill 的 `data/` 或 `output/` 目录，带时间戳的 JSON 文件。

---

## 相关文档

- [backtest_guide/SKILL.md](backtest_guide/SKILL.md) — 平台选择与通用使用指南
- [strategy_kits/docs/](strategy_kits/docs/) — 策略接入手册、架构设计
- [autoresearch/README.md](autoresearch/README.md) — 自动迭代系统完整文档
- [lixinger-screener/SKILL.md](lixinger-screener/SKILL.md) — 股票筛选方法论
- [query_data/README.md](query_data/README.md) — 数据源配置说明
