# 问财公式回测自动研究系统架构文档 (v4)

## 系统概览

本系统通过 AI Agent 驱动的迭代循环，自动寻找**稳健的参数平台**而非孤立的最高分点。核心目标从"找最高分"转变为"找最近活着稳健的平台"。

---

## 设计理念（v4 核心变化）

### 旧架构 (v3)
```
setup.py → baseline → state.json (champion_score)
run_iteration.py: mutate → backtest → score → keep/rollback (single window)
scorer.py: single window scoring
analyze.py: "战报风格" - champion分数/改进路径
```

### 新架构 (v4)
```
setup.py → baseline → state.json (champion_score + robust_score + seed_metadata)
run_iteration.py: 3-stage pipeline
  Stage 1: Quick screen (recent 12M)
  Stage 2: Sensitivity probe (neighbor configs)
  Stage 3: Multi-window confirm (6M, 12M, prior12M, 24M)
scorer.py: multi-window robust scoring + sensitivity penalty + trade_count penalty
analyze.py: "研究风格" - 5 new sections
```

---

## 系统目标

**从找最高分 → 找最近活着稳健平台**

- **最近**: 参数组合在最近 6~12 个月仍有信号
- **活着**: 多窗口验证都表现稳定
- **稳健**: 不是尖点，而是参数平台中心

---

## 4-阶段循环工作流

```
┌──────────────────────────────────────────────────────────┐
│              完整迭代流程 (v4)                            │
├──────────────────────────────────────────────────────────┤
│                                                           │
│  setup.py (初始化)                                        │
│  ├─ 创建实验目录                                          │
│  ├─ 写入 formula_config.json                              │
│  ├─ 写入 state.json (champion_score + robust_score)       │
│  ├─ 创建 iterations.tsv                                   │
│  ├─ 创建 search_notes.md                                  │
│  ├─ 运行 baseline 回测 (多窗口)                           │
│  └─ 初始化 Git 仓库                                       │
│                                                           │
│  run_iteration.py (3-stage pipeline)                      │
│  ├─ Stage 1: Quick screen (recent 12M)                    │
│  │   └─ 快速淘汰无效配置                                  │
│  ├─ Stage 2: Sensitivity probe (neighbor configs)         │
│  │   └─ 检查是否是脆弱尖点                                │
│  └─ Stage 3: Multi-window confirm (6M/12M/prior12M/24M)  │
│      └─ 最终 champion 决策                               │
│                                                           │
└──────────────────────────────────────────────────────────┘
```

### 阶段A: 方向确认 — 最近是否还活着
- 检查种子方向在最近 6~12 个月是否有持续信号
- 状态: ACTIVE / WATCH / INACTIVE

### 阶段B: 粗搜索 — 找参数平台
- 在参数空间中进行粗粒度搜索
- 寻找分数较高且稳定的区域（而非单点峰值）

### 阶段C: 邻域敏感性测试 — 检查参数是否脆弱
- 对候选参数的相邻配置做测试
- 计算 `sensitivity_penalty = std(neighbor_scores) / mean(neighbor_scores)`
- >0.3 认为参数脆弱，惩罚robust_score

### 阶段D: 多窗口确认 — 最终champion决策
- 在 4 个时间窗口上验证: 6M, 12M, prior12M, 24M
- 综合得分 = 多窗口加权平均 - 各项惩罚

---

## 评分公式 v4

### 多窗口稳健评分

```
robust_score = 0.35×recent6m + 0.35×recent12m + 0.15×prior12m + 0.15×full24m
              - sensitivity_penalty
              - complexity_penalty
              - concentration_penalty
```

### 各项惩罚说明

| 惩罚项 | 计算方式 | 阈值 |
|--------|----------|------|
| `sensitivity_penalty` | std(neighbor_scores) / mean(neighbor_scores) | >0.3 触发 |
| `complexity_penalty` | 公式复杂度（条件数量过多） | 固定惩罚 |
| `concentration_penalty` | 持仓过于集中（maxPositions 过小） | 固定惩罚 |
| `trade_count_penalty` | 交易次数<20时触发 | trade_count<20 |

### trade_count_penalty

交易次数太少（<20）的回测结果不可信，因此惩罚:
```
if trade_count < 20:
    trade_count_penalty = 0.5
else:
    trade_count_penalty = 0
```

### 方向状态

| 状态 | 含义 | 最近信号 |
|------|------|----------|
| `ACTIVE` | 持续有信号 | 最近 6~12 月稳定有交易信号 |
| `WATCH` | 有信号但不稳 | 信号时断时续，需观察 |
| `INACTIVE` | 近期无明显机会 | 超过 12 个月无明显信号 |

---

## 缓存系统

### 多窗口回测缓存

同一配置在不同时间窗口的组合会被缓存:
```
cache_key = (config_hash, start_date, end_date)
```

- Stage 1 完成的回测结果会被 Stage 3 复用
- 邻域测试的结果也会被缓存

---

## 参数平台选择

### 不是峰值选择，而是平台选择

```
      尖点 (peak)              平台 (plateau)
           ▲                        ████
          █ █                      █  █
         █   █                    █    █
        █     █                  █      █
       █████████                █████████
       不稳定，易失真              稳定，抗噪声
```

- 尖点: 单点最高分，但邻域分数差异大，实盘容易失真
- 平台: 分数略低但邻域一致性好，实盘更稳定

---

## 模块说明

### 1. setup.py - 初始化模块

创建实验环境，运行 baseline 多窗口回测。

**输入**：
- `--name`: 实验名称
- `--seed`: 种子配置文件路径（可选）
- `--mock`: Mock 模式（可选）

**输出**：
- `experiments/<name>/` 目录
- `formula_config.json` - 初始配置
- `state.json` - 初始状态（champion_score + robust_score）
- `iterations.tsv` - 包含 baseline 记录（iter=0000）

### 2. run_iteration.py - 迭代模块 (v4)

执行 3-stage 迭代优化。

**输入**：
- `--base`: 实验目录路径
- `--mutation-summary`: 变异描述
- `--mutation-type`: 变异类型（可选）

**输出**：
- 更新的 `formula_config.json`（如果 keep）
- 更新的 `state.json`
- 追加的 `iterations.tsv`

### 3. formula_executor.py - 执行器模块

通过 subprocess 调用 10jqka_backtest skill 执行回测。

### 4. formula_mutator.py - 变异器模块

生成候选配置，支持 Formula 条件变异和回测参数变异。

### 5. scorer.py - 评分模块 (v4)

计算多窗口稳健评分，决策 keep/rollback。

---

## 数据结构

### state.json (v4)

```json
{
  "current_iter": 1,
  "champion_score": 1.8932,
  "robust_score": 1.6543,
  "seed_metadata": {
    "seed_id": "A1_低PE低PB低PS",
    "direction_status": "ACTIVE",
    "parameter_band": {
      "takeProfit": [15, 20],
      "stopLoss": [9, 12],
      "maxPositions": [5, 8]
    }
  },
  "consecutive_failures": 0,
  "last_update": "2026-04-13T05:43:26"
}
```

### iterations.tsv (v4)

```
iter	backtest_id	status	robust_score	sensitivity	trade_count	window_scores	decision	mutation
0000	mock_xxx	success	1.6543	0.12	45	[0.92,0.88,0.78,0.68]	baseline	initial_seed_config
0001	mock_xxx	ok	1.7234	0.15	52	[0.95,0.91,0.82,0.72]	keep	[最大持仓] 2 → 5
```

---

## Git 版本管理

每次迭代都会自动 git commit（仅 keep 时）：

```bash
cd experiments/<name>
git log --oneline

# 示例输出
abc123f keep: iter_0002 robust=1.7234 direction=ACTIVE
def456g keep: iter_0001 robust=1.6543 direction=ACTIVE
baseline: initial seed config
```

---

## 文件系统布局

```
skills/autoresearch_10jqka_backtest/
├── formula_mutator.py        # 变异引擎
├── formula_executor.py       # 执行器
├── scorer.py                 # 评分模块 (v4)
├── run_iteration.py          # 迭代脚本 (v4)
├── setup.py                  # 初始化脚本
├── program.md                # Agent 操作指南
├── seed_config.json          # 种子配置
├── README.md                 # 使用说明
├── ARCHITECTURE.md           # 本文档
├── FAQ.md                    # 常见问题
├── pyproject.toml            # Python 项目配置
└── experiments/<name>/       # 实验目录
    ├── formula_config.json   # 当前配置
    ├── state.json            # 当前状态 (v4)
    ├── iterations.tsv        # 迭代历史 (v4)
    ├── search_notes.md       # 搜索笔记
    ├── program.md            # Agent 指南副本
    └── README.md             # 实验说明
```

---

## 总结

v4 架构的核心变化:

1. **多窗口稳健评分**: 避免单窗口尖点欺骗
2. **敏感性测试**: 排除脆弱的尖点参数
3. **参数平台选择**: 选区域中心而非峰值
4. **方向状态**: ACTIVE/WATCH/INACTIVE 指导研究方向
5. **trade_count 惩罚**: 避免小样本误导

系统的核心目标是找到**最近活着稳健的参数平台**，而不是孤立的最高分点。
