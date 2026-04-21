# 问财公式回测自动研究系统

通过 AI Agent 驱动的迭代循环，自动优化问财公式回测的参数配置。

## 功能特性

- **自动参数优化**：迭代调整持仓天数、止盈止损、持仓数量等参数
- **标准化输出**：问财回测结果自动解析为统一 JSON 格式
- **Mock 模式**：支持模拟回测，方便开发调试
- **Git 版本管理**：每次迭代自动 commit，可追溯历史
- **搜索笔记**：维护搜索地图，智能选择变异方向

## 快速开始

### 1. 初始化实验

```bash
cd skills/autoresearch_10jqka_backtest
python setup.py --name my_experiment
```

### 2. 开始迭代

```bash
cd experiments/my_experiment
# 阅读 program.md，让 agent 开始迭代循环
```

### 3. 查看结果

```bash
cat state.json
cat iterations.tsv
cat search_notes.md
```

## 目录结构

```
skills/autoresearch_10jqka_backtest/
├── formula_mutator.py        # 变异引擎（含条件候选库）
├── formula_executor.py       # 回测执行器
├── scorer.py                 # 评分和决策
├── run_iteration.py          # 单次迭代执行
├── setup.py                  # 初始化实验
├── program.md                # Agent 操作指南（默认模式）
├── seed_config.json          # 种子配置（默认模式）
├── seeds/                    # 种子库（批量种子配置）
│   ├── A1_低PE低PB低PS.json
│   ├── B1_稳定高ROE.json
│   └── ...                   # 共 60+ 个种子文件
├── trees/                    # 策略树目录（按研究主题组织）
│   ├── A_value/              # 价值树
│   │   ├── seed.json         # 树种子配置
│   │   ├── program.md        # 树专属 Agent 指南
│   │   └── experiments/<name>/
│   ├── B_quality_growth/     # 质量成长树
│   ├── ...                   # 共 9 棵策略树（A-I）
│   └── I_portfolio_risk/     # 组合与风控树
├── experiments/<name>/       # 实验目录（默认模式）
│   ├── formula_config.json   # 当前配置
│   ├── state.json            # 实验状态
│   ├── iterations.tsv        # 迭代历史
│   ├── search_notes.md       # 搜索笔记
│   ├── program.md            # Agent 指南副本
│   └── README.md             # 实验说明
├── README.md                 # 使用说明
├── ARCHITECTURE.md           # 架构文档
├── FAQ.md                    # 常见问题
└── pyproject.toml            # Python 项目配置
```

## 两种使用模式

### 默认模式（通用研究）

适合快速实验或自定义策略研究：

```bash
# 使用默认种子配置
python setup.py --name my_experiment

# 使用 seeds/ 目录中的种子
python setup.py --name my_experiment --seed seeds/A1_低PE低PB低PS.json

# 实验目录位于 skill 根目录下
cd experiments/my_experiment
```

### Tree 模式（策略树研究）

适合系统性研究某一策略主题（如价值、成长、小盘等）：

```bash
# 使用树的专属种子和指南
python setup.py --name value_exp --tree A_value

# 实验目录位于树目录下
cd trees/A_value/experiments/value_exp
```

**Tree 模式优势**：
- 每棵树有专属的 `seed.json`（基础配置）和 `program.md`（Agent 指南）
- 指南包含该树的核心分支（如 A 树有 A1-A4 四个分支）和特定条件库
- Agent 根据树的核心理念进行针对性优化

## seeds/ 与 trees/ 的关系

| 目录 | 用途 | 适用场景 |
|-----|------|---------|
| `seeds/` | 批量种子库（60+ 文件） | 默认模式下选择特定策略作为起点 |
| `trees/<tree>/seed.json` | 树种子（9 个） | Tree 模式下使用树的基础配置 |

**seeds/ 目录**：
- 包含所有分支的具体种子文件（如 `A1_低PE低PB低PS.json`、`B1_稳定高ROE.json`）
- 文件命名格式：`<分支号>_<策略名>.json`（如 `A1_xxx.json`、`C2_xxx.json`）
- 用于默认模式下快速选择特定策略

**trees/<tree>/seed.json**：
- 每棵树一个基础种子文件
- 包含该树的通用筛选条件（更宽泛，便于探索）
- 用于 Tree 模式下系统性研究该树的所有分支

## 变异类型

### Formula 条件变异（核心）

| 变异类型 | 说明 |
|---------|------|
| `adjust_formula_threshold` | 调整筛选条件数值阈值 |
| `add_formula_condition` | 添加新筛选条件 |
| `remove_formula_condition` | 移除筛选条件 |
| `adjust_formula_sort` | 调整排序条件方向 |

### 回测参数变异

| 变异类型 | 说明 |
|---------|------|
| `adjust_days_for_sale` | 调整持仓天数策略 |
| `adjust_max_positions` | 调整最大持仓数 |
| `adjust_daily_buy_count` | 调整每日买入数 |
| `adjust_take_profit` | 调整止盈阈值 |
| `adjust_stop_loss` | 调整止损阈值 |
| `adjust_trailing_stop` | 调整追踪止损阈值 |

### 支持的数值条件阈值调整

- 周成交量环比增长率（1%~20%）
- 涨幅范围（0%~30%）
- 上市时间（100~1000天）
- 换手率（1%~20%）
- 市盈率（10~100）
- 市净率（1~10）
- 净资产收益率（5%~30%）
- 毛利率（10%~80%）

### 可添加条件库

- 换手率大于5%/8%/10%
- 流通市值小于50亿/100亿/200亿
- 市盈率小于30/50
- 市净率小于3/5
- 净资产收益率大于10%/15%
- 毛利率大于30%/50%
- 非科创板、非退市、破发股、破净股等

## 评分公式

```
calmar = annual_return / max(abs(max_drawdown), 0.01)
score = calmar * 0.55 + sortino * 0.25 + information_ratio * 0.20
```

## Mock 模式

开发调试时启用 Mock 模式：

```bash
export JQKA_MOCK_MODE=1
python setup.py --name test
```

## 环境要求

- Python 3.10+
- Node.js 18+（用于调用 10jqka_backtest skill）
- Git

## 相关 Skills

- `skills/10jqka_backtest`: 问财公式回测基础 skill
- `skills/autoresearch_guorn_strategy`: 果仁策略自动研究
- `skills/autoresearch_ricequant-wizard`: RiceQuant 向导式策略自动研究