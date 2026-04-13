# Autoresearch RiceQuant Wizard 架构文档

## 系统概览

本系统通过 AI Agent 驱动的迭代循环，自动优化 RiceQuant 向导式策略的 JSON 配置参数。

---

## 核心流程图

```
┌──────────────────────────────────────────────────────────┐
│                   完整迭代流程                            │
├──────────────────────────────────────────────────────────┤
│                                                           │
│  setup.py (初始化)                                        │
│  ├─ 创建实验目录                                          │
│  ├─ 初始化 Git 仓库                                       │
│  ├─ 运行 baseline 回测                                    │
│  └─ 保存初始状态                                          │
│                                                           │
│  run_iteration.py (迭代循环)                              │
│  ├─ 1. 加载状态和配置                                     │
│  ├─ 2. 生成候选配置 (wizard_mutator.py)                  │
│  ├─ 3. 执行回测 (wizard_executor.py)                     │
│  ├─ 4. 计算得分 (scorer.py)                              │
│  ├─ 5. 决策 keep/rollback                                │
│  ├─ 6. Git commit/rollback                               │
│  └─ 7. 更新状态和历史                                     │
│                                                           │
└──────────────────────────────────────────────────────────┘
```

---

## 模块说明

### 1. setup.py - 初始化模块

创建实验环境，运行 baseline 回测。

**输入**：
- `--name`: 实验名称
- `--seed-config`: 种子配置路径（可选）

**输出**：
- `experiments/<name>/` 目录
- `wizard_config.json` - 初始配置
- `state.json` - 初始状态
- `iterations.tsv` - baseline 记录

### 2. run_iteration.py - 迭代模块

执行单次迭代优化。

**输入**：
- `--base`: 实验目录路径
- `--mutation-summary`: 变异描述
- `--mutation-type`: 变异类型（可选）

**输出**：
- 更新的 `wizard_config.json`（如果 keep）
- 更新的 `state.json`
- 追加的 `iterations.tsv`

### 3. wizard_executor.py - 执行器模块

封装 RiceQuant API，执行回测。

**主要函数**：
```python
def run_backtest(config: dict) -> dict:
    """
    提交回测并等待结果
    
    Returns:
        {
            "backtest_id": str,
            "metrics": {
                "annual_return": float,
                "max_drawdown": float,
                "sharpe": float,
                "sortino": float,
                "information_ratio": float
            }
        }
    """
```

### 4. wizard_mutator.py - 变异器模块

生成候选配置。

**8 种变异类型**：
1. `add_filter` - 添加筛选条件
2. `remove_filter` - 移除筛选条件
3. `adjust_filter_threshold` - 调整筛选阈值
4. `add_ranking` - 添加排序规则
5. `adjust_ranking_weight` - 调整排序权重
6. `adjust_holding_num` - 调整持仓数量
7. `adjust_rebalance_interval` - 调整调仓间隔
8. `change_pool` - 更换股票池

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

### wizard_config.json

```json
{
  "name": "策略名称",
  "pool": "stock_pool_name",
  "filters": [
    {"factor": "pe", "operator": "<", "value": 20},
    {"factor": "roe", "operator": ">", "value": 10}
  ],
  "ranking": [
    {"factor": "pb", "direction": "asc", "weight": 0.5},
    {"factor": "roe", "direction": "desc", "weight": 0.5}
  ],
  "holding_num": 30,
  "rebalance_interval": "month",
  "backtest": {
    "start_date": "2020-01-01",
    "end_date": "2023-12-31",
    "capital": 1000000,
    "benchmark": "000300.XSHG"
  }
}
```

### state.json

```json
{
  "current_iter": 5,
  "champion_score": 1.2345,
  "consecutive_failures": 0,
  "last_update": "2026-04-12T11:15:00Z"
}
```

---

## 文件系统布局

```
skills/autoresearch_ricequant-wizard/
├── setup.py                    # 初始化脚本
├── run_iteration.py            # 迭代脚本
├── wizard_executor.py          # RiceQuant API 封装
├── wizard_mutator.py           # 配置变异逻辑
├── scorer.py                   # 评分和决策
├── analyze.py                  # 结果分析工具
├── validate.py                 # 配置验证工具
├── program.md                  # Agent 操作指南
├── seed_config.json            # 种子配置
├── README.md                   # 使用说明
├── FAQ.md                      # 常见问题
├── ARCHITECTURE.md             # 本文档
└── experiments/<name>/         # 实验目录
    ├── wizard_config.json      # 当前最优配置
    ├── state.json              # 迭代状态
    ├── iterations.tsv          # 所有迭代记录
    ├── search_notes.md         # 搜索笔记
    ├── program.md              # Agent 指南副本
    └── .git/                   # Git 历史（只 commit 成功版本）
```

---

## Git 版本管理

每次迭代都会自动 git commit，方便追溯历史：

```bash
# 查看提交历史
cd experiments/<name>
git log --oneline

# 示例输出
abc123f keep: iter_0003 score=1.2345 annual=15.00% dd=-12.00%
def456g rollback: iter_0002 score=1.1000 < champion=1.1234
789hij0 keep: iter_0001 score=1.1234 annual=14.50% dd=-11.00%
baseline: initial seed config
```

---

## 扩展性

### 自定义变异策略

编辑 `wizard_mutator.py`，添加新的变异函数：

```python
def mutate_custom(config: dict) -> tuple[dict, str]:
    """自定义变异逻辑"""
    new_config = config.copy()
    # 你的变异逻辑...
    return new_config, "custom: 描述"
```

### 自定义评分权重

编辑 `scorer.py`：

```python
DEFAULT_WEIGHTS = {
    "calmar": 0.4,       # 调整权重
    "sortino": 0.3,
    "information": 0.2,
    "win_rate": 0.1,     # 添加新指标
}
```

---

## 性能优化

### 并行运行

```bash
# 在不同实验目录并行运行
python run_iteration.py --base experiments/exp1 ... &
python run_iteration.py --base experiments/exp2 ... &
wait
```

### Mock 模式

开发测试时使用模拟数据：

```bash
export RICEQUANT_MOCK_MODE=1
python setup.py --name test
```

---

## 监控和调试

### 查看进度

```bash
# 查看迭代历史
cat experiments/<name>/iterations.tsv

# 详细分析
python analyze.py --base experiments/<name>

# 查看当前状态
cat experiments/<name>/state.json
```

### 验证配置

```bash
python validate.py --config experiments/<name>/wizard_config.json
python validate.py --config experiments/<name>/wizard_config.json --strict
```

---

## 总结

本系统采用模块化设计，各组件职责清晰：
- **setup.py**: 初始化实验环境
- **run_iteration.py**: 执行迭代循环
- **wizard_executor.py**: 封装平台 API
- **wizard_mutator.py**: 生成候选配置
- **scorer.py**: 评分和决策

通过 Git 版本管理和完善的历史记录，系统可以追溯每次改动，便于分析和回滚。
