# 问财公式回测自动研究系统架构文档

## 系统概览

本系统通过 AI Agent 驱动的迭代循环，自动优化问财公式回测的参数配置。

---

## 设计理念（借鉴 karpathy/autoresearch）

```
- formula_config.json 永远是最优配置
- 成功 → 覆盖 formula_config.json + git commit
- 失败 → formula_config.json 保持不变，不 commit
- iterations.tsv 记录所有结果（不 commit）
```

---

## 核心流程图

```
┌──────────────────────────────────────────────────────────┐
│                   完整迭代流程                            │
├──────────────────────────────────────────────────────────┤
│                                                           │
│  setup.py (初始化)                                        │
│  ├─ 创建实验目录                                          │
│  ├─ 写入 formula_config.json                              │
│  ├─ 写入 state.json                                       │
│  ├─ 创建 iterations.tsv                                   │
│  ├─ 创建 search_notes.md                                  │
│  ├─ 运行 baseline 回测                                    │
│  └─ 初始化 Git 仓库                                       │
│                                                           │
│  run_iteration.py (迭代循环)                              │
│  ├─ 1. 加载状态和配置                                     │
│  ├─ 2. 生成候选配置 (formula_mutator.py)                 │
│  ├─ 3. 覆盖 formula_config.json（待验证）                │
│  ├─ 4. 执行回测 (formula_executor.py)                    │
│  ├─ 5. 计算得分 (scorer.py)                              │
│  ├─ 6. 决策 keep/rollback                                │
│  ├─ 7. keep → git commit；rollback → git restore        │
│  └─ 8. 更新 state.json 和 iterations.tsv                │
│                                                           │
└──────────────────────────────────────────────────────────┘
```

---

## 模块说明

### 1. setup.py - 初始化模块

创建实验环境，运行 baseline 回测。

**输入**：
- `--name`: 实验名称
- `--seed`: 种子配置文件路径（可选）
- `--mock`: Mock 模式（可选）

**输出**：
- `experiments/<name>/` 目录
- `formula_config.json` - 初始配置
- `state.json` - 初始状态（current_iter=1）
- `iterations.tsv` - 包含 baseline 记录（iter=0000）

### 2. run_iteration.py - 迭代模块

执行单次迭代优化。

**输入**：
- `--base`: 实验目录路径
- `--mutation-summary`: 变异描述
- `--mutation-type`: 变异类型（可选）

**输出**：
- 更新的 `formula_config.json`（如果 keep）
- 更新的 `state.json`
- 追加的 `iterations.tsv`

**设计要点**：
- 先覆盖 formula_config.json，再执行回测
- keep → git commit 全部变更
- rollback → git checkout HEAD formula_config.json（不 commit）

### 3. formula_executor.py - 执行器模块

通过 subprocess 调用 10jqka_backtest skill 执行回测。

**主要函数**：
```python
def run_backtest(config: dict) -> dict:
    """
    提交回测并等待结果
    
    Returns:
        {
            "status": "ok",
            "backtest_id": str,
            "summary": {
                "annualReturn": float,
                "maxDrawdown": float,
                ...
            }
        }
    """
```

### 4. formula_mutator.py - 变异器模块

生成候选配置，支持 Formula 条件变异和回测参数变异。

**Formula 条件变异（核心）**：
- `adjust_formula_threshold` - 调整数值条件阈值
- `add_formula_condition` - 添加新筛选条件
- `remove_formula_condition` - 移除筛选条件
- `adjust_formula_sort` - 调整排序条件方向

**回测参数变异**：
- `adjust_days_for_sale` - 调整持仓天数
- `adjust_max_positions` - 调整最大持仓数
- `adjust_daily_buy_count` - 调整每日买入数
- `adjust_take_profit` - 调整止盈阈值
- `adjust_stop_loss` - 调整止损阈值
- `adjust_trailing_stop` - 调整追踪止损阈值

### 5. scorer.py - 评分模块

计算策略得分，决策 keep/rollback。

**评分公式**：
```python
calmar = annual_return / max(abs(max_drawdown), 0.01)
score = calmar * 0.55 + sortino * 0.25 + information_ratio * 0.20
```

**决策逻辑**：
```python
if abs(max_drawdown) > 0.35:
    return "rollback", "回撤过大"
elif new_score > champion_score:
    return "keep", "得分提升"
else:
    return "rollback", "得分未提升"
```

---

## 数据结构

### formula_config.json

```json
{
  "name": "策略名称",
  "formula": [
    "创业板",
    "非ST",
    "周成交量环比增长率大于8%",
    "近3天的涨幅大于0%小于20%",
    "上市时间大于300天",
    "未来5天涨跌幅从大到小",
    "龙脊线百分比由近到远"
  ],
  "daysForSaleStrategy": "2,3",
  "startDate": "2025-01-01",
  "endDate": "2026-04-10",
  "maxPositions": 2,
  "dailyBuyCount": 2,
  "takeProfit": 25,
  "stopLoss": 9,
  "trailingStopLoss": 5
}
```

### state.json

```json
{
  "current_iter": 1,
  "champion_score": 1.8932,
  "consecutive_failures": 0,
  "last_update": "2026-04-13T05:43:26"
}
```

### iterations.tsv

```
iter	backtest_id	status	annual_return	max_drawdown	sharpe	score	decision	mutation
0000	mock_xxx	success	0.0916	0.0363	1.03	1.8932	baseline	initial_seed_config
0001	mock_xxx	ok	0.0958	0.0571	1.15	1.4785	keep	[最大持仓] 2 → 5
```

---

## 文件系统布局

```
skills/autoresearch_10jqka_backtest/
├── formula_mutator.py        # 变异引擎
├── formula_executor.py       # 执行器
├── scorer.py                 # 评分模块
├── run_iteration.py          # 迭代脚本
├── setup.py                  # 初始化脚本
├── program.md                # Agent 操作指南
├── seed_config.json          # 种子配置
├── README.md                 # 使用说明
├── ARCHITECTURE.md           # 本文档
├── FAQ.md                    # 常见问题
├── pyproject.toml            # Python 项目配置
└── experiments/<name>/       # 实验目录
    ├── formula_config.json   # 当前配置
    ├── state.json            # 当前状态
    ├── iterations.tsv        # 迭代历史
    ├── search_notes.md       # 搜索笔记
    ├── program.md            # Agent 指南副本
    └── README.md             # 实验说明
```

---

## Git 版本管理

每次迭代都会自动 git commit（仅 keep 时）：

```bash
# 查看提交历史
cd experiments/<name>
git log --oneline

# 示例输出
abc123f keep: iter_0002 score=1.9684 annual=14.60% dd=-5.65%
def456g keep: iter_0001 score=1.4785 annual=9.58% dd=-5.71%
baseline: initial seed config
```

Rollback 时不 commit，用 `git checkout HEAD formula_config.json` 恢复。

---

## 总结

本系统采用模块化设计，各组件职责清晰：
- **setup.py**: 初始化实验环境
- **run_iteration.py**: 执行迭代循环
- **formula_executor.py**: 封装问财平台 API
- **formula_mutator.py**: 生成候选配置
- **scorer.py**: 评分和决策

通过 Git 版本管理和简洁的 iterations.tsv，系统可以追溯每次改动，便于分析和回滚。