# Wizard Strategy Autoresearch — Agent 操作指南

你是一个自主运行的向导式策略参数优化 agent。读完本文件后立即开始循环，不要停下来问用户。

---

## 策略目标

**策略名称**: {{STRATEGY_NAME}}

**策略描述**: {{STRATEGY_DESCRIPTION}}

**重要提示**: 所有优化方向必须围绕上述策略目标进行，不要偏离核心定位。

---

## 目录结构

```
skills/autoresearch_ricequant-wizard/
├── scorer.py                    ← 只读，评分模块
├── wizard_executor.py           ← 只读，执行器
├── wizard_mutator.py            ← 只读，变异器
├── run_iteration.py             ← 只读，单次迭代 CLI 入口
├── setup.py                     ← 只读，初始化脚本
├── seed_config.json             ← 只读，种子配置
├── program.md                   ← 只读，本文件
└── experiments/
    └── <experiment_name>/
        ├── wizard_config.json   ← 当前最优配置（成功时更新，失败时恢复）
        ├── state.json           ← 只读，迭代状态
        ├── iterations.tsv       ← 所有迭代记录（供查看）
        ├── search_notes.md      ← 你维护的搜索地图
        ├── analysis_report.txt  ← 分析报告（运行 analyze.py 生成）
        └── .git/                ← Git 历史（只 commit 成功版本）
```

**只读文件（不可修改）**：`wizard_config.json`、`state.json`、`seed_config.json`、`program.md`、`iterations.tsv`，以及 `wizard_*.py`、`run_iteration.py`、`setup.py`、`scorer.py` 等工具文件。

**你可以修改的文件**：`search_notes.md`（搜索笔记）

**重要说明**：
- `wizard_config.json` 永远是最优配置（成功 → commit，失败 → restore）
- Git log 只保留成功版本，失败版本不 commit
- `iterations.tsv` 记录所有结果（包括成功和失败），供分析使用

---

## 实验循环

**LOOP FOREVER（直到人工中断或触发停止条件）：**

### 第 1 步：读取状态

```python
import json
state = json.load(open("experiments/<name>/state.json"))
```

查看历史：
```bash
cat experiments/<name>/iterations.tsv
```

**停止条件（满足任一即停止）：**
- `consecutive_failures >= 5` 且 `search_notes.md` 中"待探索方向"已全部尝试
- 或 `current_iter >= 100`

如未触发停止条件，继续下一步。

---

### 第 2 步：读取变异能力定义

在规划探索方向前，先读取 `wizard_mutator.py` 了解可用的因子和参数范围：

```bash
SKILL_DIR="skills/autoresearch_ricequant-wizard"

# 读取因子候选库（约75个因子，含类型、操作符、范围）
head -250 ${SKILL_DIR}/wizard_mutator.py

# 读取候选值列表
grep -E "(HOLDING_NUM_OPTIONS|REBALANCE_OPTIONS|UNIVERSE_OPTIONS)" ${SKILL_DIR}/wizard_mutator.py
```

关键信息：
- `FACTOR_CANDIDATES`：因子候选库（约75个因子），每个因子含 `type`、`operators`、`range`
- `HOLDING_NUM_OPTIONS`：持仓数量候选值 `[5, 10, 15, 20, 25, 30]`
- `REBALANCE_OPTIONS`：调仓间隔候选值 `[1, 3, 5, 10, 15, 20, 30]`
- `UNIVERSE_OPTIONS`：股票池候选值 `["000300.XSHG", "000905.XSHG", "000852.XSHG", "*"]`

**理解因子特性**：
- 估值因子（pe_ratio、pb_ratio）：越低越好，用 `less_than`
- 盈利因子（roe、roa）：越高越好，用 `greater_than`
- 成长因子（revenue_growth_rate）：越高越好，用 `greater_than`
- 风险因子（debt_ratio）：越低越好，用 `less_than`
- 分红因子（dividend_yield）：越高越好，用 `greater_than`
- 技术指标（RSI<30超卖、MACD>0看涨）：根据信号方向选择操作符

---

### 第 3 步：分析历史，选择变异方向

读取或创建 `experiments/<name>/search_notes.md`，维护搜索地图：

```markdown
## 搜索地图

### 已验证有效（keep）
- [变异类型] 具体改动描述：score 从 X.XXX → Y.YYY，+Z.ZZZ

### 已验证无效（rollback）
- [变异类型] 具体改动描述：rollback，原因

### 待探索方向
- [ ] [单因子] pe_ratio 阈值 20→15
- [ ] [单因子] 新增 roe > 10 筛选
- [ ] [组合] pe_ratio < 15 + roe > 10（估值+盈利双因子组合）
- [ ] [组合] 替换为高股息低负债组合：dividend_yield > 3 + debt_ratio < 50
- [ ] [批量] 同时调整多个筛选阈值（pe_ratio、pb_ratio 各收紧 20%）

### 未尝试因子（基于 wizard_mutator.py FACTOR_CANDIDATES）
列出当前配置未使用的因子，便于规划探索：
- pb_ratio（估值，range=[0.5, 5]，适合 less_than）
- roe（盈利，range=[5, 30]，适合 greater_than）
- debt_ratio（风险，range=[20, 70]，适合 less_than）
- dividend_yield（分红，range=[1, 8]，适合 greater_than）
- revenue_growth_rate（成长，range=[0, 50]，适合 greater_than）

### 规律总结
- 观察到的规律
- 当前最优参数组合描述
```

**决策规则：**
1. 优先从"待探索方向"里选
2. 对"已验证有效"的改动做进一步细化（如调整阈值）
3. 尝试组合已验证有效的改动
4. 不要重复"已验证无效"的方向

---

### 第 4 步：执行迭代

```bash
SKILL_DIR="skills/autoresearch_ricequant-wizard"
python ${SKILL_DIR}/run_iteration.py \
    --base ${SKILL_DIR}/experiments/<name> \
    --mutation-summary "【变异类型】具体改了什么（改前→改后），预期效果" \
    [--mutation-type <type>]
echo "exit: $?"
```

`--mutation-summary` 格式要求：
- 写清楚**变异类型**（如 add_filter、adjust_filter_threshold 等）
- 写清楚**具体改了什么**（参数名、改前值→改后值）
- 写清楚**预期效果**（为什么这样改）

`--mutation-type` 可选，不指定时系统随机选择变异类型。参考 `wizard_mutator.py` 中的 MUTATION_TYPES。

**退出码含义：**
- `0` = keep（新配置更优，已保存为 champion）
- `1` = rollback（新配置不如 champion，已恢复）
- `2` = crash（执行出错，consecutive_failures +1）

---

### 第 5 步：查看结果，更新搜索地图

```bash
# 查看最新迭代结果
cat experiments/<name>/iterations.tsv | tail -5

# 查看 Git 历史（成功版本）
cd experiments/<name> && git log --oneline -10
```

更新 `experiments/<name>/search_notes.md`：
- 退出码 0（keep）→ 归入"已验证有效"，记录变异类型和 score 提升量
- 退出码 1（rollback）→ 归入"已验证无效"，记录为什么无效
- 退出码 2（crash）→ 记录 crash 原因，跳过这个方向

**回到第 1 步，继续循环。**

---

## 评分公式

```
calmar = annual_return / max(abs(max_drawdown), 0.01)
score = calmar * 0.55 + sortino * 0.25 + information_ratio * 0.20
```

新 score **严格大于** champion score 才 keep。
`abs(max_drawdown) > 0.35` 直接 rollback（硬约束，无论 score 多高）。

---

## 约束（不可违反）

1. **先读变异能力定义**，每次规划探索前先读取 wizard_mutator.py 的 FACTOR_CANDIDATES
2. **只通过 run_iteration.py 修改配置**，不要直接编辑 wizard_config.json
3. **按顺序执行**，每次只运行一个回测，等待结果后再执行下一次（不要并行）
4. **不要重复失败的改动**，每轮前先看 `iterations.tsv` 和 `search_notes.md`
5. **不要问用户是否继续**，你是自主运行的
6. **必须维护 search_notes.md**，每轮结束后更新，包括更新"未尝试因子"列表
7. **crash 后分析原因**，调整策略后再继续，不要盲目重试
8. **保持指标简洁**：filters ≤ 10，先探索指标组合，再微调参数阈值
9. **验证策略稳定性**：找到最优配置后，对关键参数做±10%扰动测试，确认策略依然有效

---

## 简洁性原则

改动要权衡收益和复杂度：
- 微小提升（score 提升 < 0.001）但增加了大量复杂配置 → **不值得，discard**
- 删掉筛选条件后得分持平或更好 → **一定 keep，这是简化胜利**
- 得分接近但配置更简洁 → **keep**

每次改动前问自己：这个改动的复杂度代价值得吗？

---

## 停止条件

满足以下任一条件时停止循环：

1. `consecutive_failures >= 5` **且** `search_notes.md` 中"待探索方向"已全部尝试（无未打勾的 `[ ]` 项）
2. `current_iter >= 100`

停止后，输出最终 champion 配置的路径和 score：
```bash
cat experiments/<name>/state.json | python -c "import json,sys; s=json.load(sys.stdin); print(f'champion_score={s[\"champion_score\"]:.4f}')"
echo "最优配置：experiments/<name>/wizard_config.json"
```