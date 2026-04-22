# 问财公式回测自动研究系统

通过 AI Agent 驱动的迭代循环，自动寻找稳健的参数平台而非孤立峰值。

## 核心目标

**从找最高分 → 找最近活着稳健平台**

- 最近: 参数在最近 6~12 个月仍有信号
- 活着: 多窗口验证都表现稳定
- 稳健: 不是尖点，而是平台中心

## 功能特性

- **多窗口稳健评分**: 6M/12M/prior12M/24M 四窗口验证
- **敏感性测试**: 邻域检测避免脆弱尖点
- **方向状态**: ACTIVE/WATCH/INACTIVE 指导研究
- **参数平台选择**: 选区域中心而非峰值
- **Mock 模式**: 支持模拟回测开发调试
- **Git 版本管理**: 每次迭代自动 commit，可追溯历史

---

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

### 4. 理解输出

```json
{
  "direction_status": "ACTIVE",
  "robust_score": 1.6543,
  "parameter_band": {
    "takeProfit": [15, 20],
    "stopLoss": [9, 12],
    "maxPositions": [5, 8]
  },
  "suggestion": "可继续跟踪"
}
```

---

## 4阶段循环工作流

### 阶段A: 方向确认 — 最近是否还活着

检查种子方向在最近 6~12 个月是否有持续信号。

| 状态 | 含义 | 最近信号 |
|------|------|----------|
| `ACTIVE` | 持续有信号 | 最近 6~12 月稳定有交易信号 |
| `WATCH` | 有信号但不稳 | 信号时断时续，需观察 |
| `INACTIVE` | 近期无明显机会 | 超过 12 个月无明显信号 |

### 阶段B: 粗搜索 — 找参数平台

在参数空间中进行粗粒度搜索，寻找分数较高且稳定的区域。

### 阶段C: 邻域敏感性测试 — 检查参数是否脆弱

对候选参数的相邻配置做测试:
```
sensitivity = std(neighbor_scores) / mean(neighbor_scores)
```
- >0.3 认为参数脆弱，触发 sensitivity_penalty
- 尖点在实盘中容易失真，平台中心更稳定

### 阶段D: 多窗口确认 — 最终champion决策

在 4 个时间窗口上验证:
- `recent6m`: 最近 6 个月
- `recent12m`: 最近 12 个月
- `prior12m`: 之前 12 个月
- `full24m`: 完整 24 个月

---

## 评分公式 v4

```
robust_score = 0.35×recent6m + 0.35×recent12m + 0.15×prior12m + 0.15×full24m
              - sensitivity_penalty
              - complexity_penalty
              - concentration_penalty
              - trade_count_penalty
```

### 惩罚项

| 惩罚 | 触发条件 | 惩罚值 |
|------|----------|--------|
| `sensitivity_penalty` | sensitivity > 0.3 | 0.3 |
| `complexity_penalty` | 公式条件过多 | 0.1 |
| `concentration_penalty` | maxPositions 过小 | 0.1 |
| `trade_count_penalty` | trade_count < 20 | 0.5 |

### 交易次数惩罚

交易次数太少（<20）的回测结果不可信:
```
if trade_count < 20:
    trade_count_penalty = 0.5
else:
    trade_count_penalty = 0
```

---

## 目录结构

```
skills/autoresearch_10jqka_backtest/
├── formula_mutator.py        # 变异引擎（含条件候选库）
├── formula_executor.py       # 回测执行器
├── scorer.py                 # 评分和决策 (v4)
├── run_iteration.py          # 单次迭代执行 (v4)
├── setup.py                  # 初始化实验
├── program.md                # Agent 操作指南
├── seed_config.json          # 种子配置（默认模式）
├── seeds/                    # 种子库（批量种子配置）
│   ├── A1_低PE低PB低PS.json
│   ├── B1_稳定高ROE.json
│   └── ...
├── trees/                    # 策略树目录
│   ├── A_value/
│   ├── B_quality_growth/
│   └── ...
├── experiments/<name>/       # 实验目录
│   ├── formula_config.json   # 当前配置
│   ├── state.json            # 实验状态 (v4)
│   ├── iterations.tsv        # 迭代历史 (v4)
│   ├── search_notes.md       # 搜索笔记
│   ├── program.md            # Agent 指南副本
│   └── README.md             # 实验说明
├── README.md                 # 使用说明
├── ARCHITECTURE.md           # 架构文档
├── FAQ.md                    # 常见问题
└── pyproject.toml            # Python 项目配置
```

---

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

适合系统性研究某一策略主题：

```bash
# 使用树的专属种子和指南
python setup.py --name value_exp --tree A_value

# 实验目录位于树目录下
cd trees/A_value/experiments/value_exp
```

---

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

---

## 参数平台 vs 峰值选择

```
      尖点 (peak)              平台 (plateau)
           ▲                        ████
          █ █                      █  █
         █   █                    █    █
        █     █                  █      █
       █████████                █████████
       不稳定，易失真              稳定，抗噪声
```

系统选择**参数平台中心**而非单点峰值，因为:
1. 尖点在实盘中容易失真
2. 平台中心更稳定，抗噪声能力强
3. 多窗口验证一致性更高

---

## Mock 模式

开发调试时启用 Mock 模式：

```bash
export JQKA_MOCK_MODE=1
python setup.py --name test
```

---

## 环境要求

- Python 3.10+
- Node.js 18+（用于调用 10jqka_backtest skill）
- Git

## 相关 Skills

- `skills/10jqka_backtest`: 问财公式回测基础 skill
- `skills/autoresearch_guorn_strategy`: 果仁策略自动研究
- `skills/autoresearch_ricequant-wizard`: RiceQuant 向导式策略自动研究
