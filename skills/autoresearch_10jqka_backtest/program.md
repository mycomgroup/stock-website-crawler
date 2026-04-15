# 问财公式回测自动研究系统 — Agent 操作指南

你是一个自主运行的公式回测参数优化 agent。读完本文件后立即开始循环，不要停下来问用户。

---

## 策略目标

**策略名称**: {{STRATEGY_NAME}}

**策略描述**: {{STRATEGY_DESCRIPTION}}

**重要提示**: 所有优化方向必须围绕上述策略目标进行，不要偏离核心定位。

---

## 目录结构

```
skills/autoresearch_10jqka_backtest/
├── formula_mutator.py      ← 只读，变异器（含条件候选库）
├── formula_executor.py     ← 只读，执行器
├── scorer.py               ← 只读，评分模块
├── run_iteration.py        ← 只读，单次迭代 CLI 入口
├── setup.py                ← 只读，初始化脚本
├── seed_config.json        ← 只读，种子配置
├── program.md              ← 只读，本文件
└── experiments/
    └── <experiment_name>/
        ├── formula_config.json   ← 当前 champion 配置（只读，由脚本维护）
        ├── state.json            ← 只读，由脚本维护
        ├── iterations.tsv        ← 只读，由脚本维护
        └── search_notes.md       ← 你维护的搜索地图
```

**只读文件（不可修改）**：`formula_config.json`、`state.json`、`seed_config.json`、`program.md`、`iterations.tsv`，以及 `formula_*.py`、`run_iteration.py`、`setup.py`、`scorer.py` 等工具文件。

**你可以修改的文件**：`search_notes.md`（搜索笔记）

---

## 实验循环

**LOOP FOREVER（直到人工中断或触发停止条件）：**

### 第 1 步：读取状态

```bash
cat state.json
cat iterations.tsv
```

**停止条件（满足任一即停止）：**
- `consecutive_failures >= 5` 且 `search_notes.md` 中"待探索方向"已全部尝试
- 或 `current_iter >= 100`

如未触发停止条件，继续下一步。

---

### 第 2 步：读取变异能力定义

在规划探索方向前，先读取 `formula_mutator.py` 了解可用的条件和参数范围：

```bash
SKILL_DIR="skills/autoresearch_10jqka_backtest"

# 读取数值条件候选库
head -80 ${SKILL_DIR}/formula_mutator.py

# 读取可添加条件库
grep "FORMULA_ADDABLE_CONDITIONS" -A 30 ${SKILL_DIR}/formula_mutator.py
```

关键信息：
- `FORMULA_NUMERIC_CONDITIONS`：数值条件库，每个条件含 `range`、`template`
- `FORMULA_ADDABLE_CONDITIONS`：可添加条件列表（换手率、市值、市盈率等）
- `MUTATION_TYPES`：变异类型列表

**理解条件特性**：
- 成交量条件（周成交量环比增长率）：越高表示越活跃，阈值调整影响选股活跃度
- 涨幅条件（涨幅范围）：影响选股范围，过窄选股少，过宽选股质量下降
- 上市时间条件：越长越稳定，新股波动大
- 市值条件（流通市值）：越小成长空间大，越大稳定性好
- 估值条件（市盈率、市净率）：越低越便宜
- 盈利条件（净资产收益率、毛利率）：越高越好

---

### 第 3 步：分析历史，选择变异方向

读取或创建 `search_notes.md`，维护搜索地图：

```markdown
## 搜索地图

### 已验证有效（keep）
- [变异类型] 具体改动描述：score 从 X.XXX → Y.YYY，+Z.ZZZ

### 已验证无效（rollback）
- [变异类型] 具体改动描述：rollback，原因

### 待探索方向
- [ ] [阈值] 周成交量增长率 8% → 10%
- [ ] [阈值] 涨幅范围 0%~20% → 5%~25%
- [ ] [添加] 添加换手率大于5%
- [ ] [添加] 添加流通市值小于100亿
- [ ] [移除] 移除热点概念条件
- [ ] [排序] 调整涨跌幅排序方向

### 未尝试条件（基于 formula_mutator.py）
列出当前配置未使用的条件，便于规划探索：
- 换手率（range=[1, 20]，适合大于/小于）
- 流通市值（range=[10, 500]亿，适合小于）
- 市盈率（range=[10, 100]，适合小于）
- 市净率（range=[1, 10]，适合小于）
- 净资产收益率（range=[5, 30]%，适合大于）
- 毛利率（range=[10, 80]%，适合大于）

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
SKILL_DIR="skills/autoresearch_10jqka_backtest"
python ${SKILL_DIR}/run_iteration.py \
    --base ${SKILL_DIR}/experiments/<name> \
    --mutation-summary "【变异类型】具体改了什么（改前→改后），预期效果" \
    [--mutation-type <type>]
echo "exit: $?"
```

`--mutation-summary` 格式要求：
- 写清楚**变异类型**（如 adjust_formula_threshold、add_formula_condition 等）
- 写清楚**具体改了什么**（参数名、改前值→改后值）
- 写清楚**预期效果**（为什么这样改）

`--mutation-type` 可选，不指定时系统随机选择变异类型。参考 `formula_mutator.py` 中的 MUTATION_TYPES。

**退出码含义：**
- `0` = keep（新配置更优，已保存为 champion）
- `1` = rollback（新配置不如 champion，已恢复）
- `2` = crash（执行出错，consecutive_failures +1）

---

### 第 5 步：查看结果，更新搜索地图

```bash
cat iterations.tsv | tail -5
```

更新 `search_notes.md`：
- 退出码 0（keep）→ 归入"已验证有效"，记录变异类型和 score 提升量
- 退出码 1（rollback）→ 归入"已验证无效"，记录为什么无效
- 退出码 2（crash）→ 记录 crash 原因，跳过这个方向

**回到第 1 步，继续循环。**

---

## 评分公式（v3 - 防过拟合优化版）

```
calmar = annual_return / max(abs(max_drawdown), 0.01)
complexity_penalty = min((formula条件数 + 调优参数数) / 10, 1.0)

# 选股数量惩罚（双边软约束）
if maxPositions < 5:
    position_penalty = (5 - maxPositions) ** 2 * 0.1
elif maxPositions > 15:
    position_penalty = (maxPositions - 15) ** 2 * 0.01
else:
    position_penalty = 0

# 过拟合惩罚（v3新增）
overfit_penalty = 持股少时胜率不足的惩罚

score = sortino * 0.40 + calmar * 0.25 + information_ratio * 0.15 
      + win_rate * 0.10 - complexity_penalty * 0.10 - position_penalty - overfit_penalty
```

**权重解读：**
- **sortino (40%)**：只惩罚下行风险，对趋势策略最友好
- **calmar (25%)**：收益/回撤比，衡量风险收益效率
- **information_ratio (15%)**：超额收益稳定性
- **win_rate (10%)**：胜率，防止低胜率高风险策略
- **complexity_penalty (10%)**：复杂度惩罚，防止过拟合

**过拟合惩罚规则（v3新增）：**
持股少于5支时，胜率必须足够高，否则判定为过拟合：
- 持股1支：需要胜率≥60%
- 持股2支：需要胜率≥55%
- 持股3支：需要胜率≥50%
- 持股4支：需要胜率≥45%
- 持股≥5支：无限制

示例：持股2支、胜率30% → 惩罚 = (55%-30%) × 3 × 3 = 2.25分

**选股数量建议**：5-15支最佳，避免过拟合。

**硬约束**：
- `abs(max_drawdown) > 0.35` 直接 rollback
- 新 score **严格大于** champion score 才 keep

---

## 约束（不可违反）

1. **先读变异能力定义**，每次规划探索前先读取 formula_mutator.py 的条件候选库
2. **只通过 run_iteration.py 修改配置**，不要直接编辑 formula_config.json
3. **按顺序执行**，每次只运行一个回测，等待结果后再执行下一次（不要并行）
4. **不要重复失败的改动**，每轮前先看 `iterations.tsv` 和 `search_notes.md`
5. **不要问用户是否继续**，你是自主运行的
6. **必须维护 search_notes.md**，每轮结束后更新，包括更新"未尝试条件"列表
7. **crash 后分析原因**，调整策略后再继续，不要盲目重试

---

## 简洁性原则

评分公式已内置复杂度惩罚，但额外注意：

- 删掉筛选条件后得分持平或更好 → **一定 keep，这是简化胜利**
- 微小提升（score 提升 < 0.02）但增加了 3+ 条件 → **需谨慎，复杂度惩罚会抵消收益**
- 得分接近（差异 < 0.01）但配置更简洁 → **优先 keep 简洁版**

每次改动前问自己：这个改动的复杂度代价值得吗？

---

## 停止条件

满足以下任一条件时停止循环：

1. `consecutive_failures >= 5` **且** `search_notes.md` 中"待探索方向"已全部尝试（无未打勾的 `[ ]` 项）
2. `current_iter >= 100`

停止后，输出最终 champion 配置的路径和 score：
```bash
cat state.json | python -c "import json,sys; s=json.load(sys.stdin); print(f'champion_score={s[\"champion_score\"]:.4f}')"
```