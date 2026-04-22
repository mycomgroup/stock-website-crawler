# G_event_driven 自动研究操作指南

你要做的事情很简单：**按照程序已经固定好的 A/B/C/D 流程推进，不自行发明阈值、规则或市场解释。**

---

## 策略目标

- **策略名称**: {{STRATEGY_NAME}}
- **策略描述**: {{STRATEGY_DESCRIPTION}}

目标不是找最高分，而是找：
- **短期仍有效**
- **不过拟合**
- **长周期不死**
- **参数有稳定带**
- **多窗口确认过**

---

## 以程序结果为准

下面这些内容已经固化在程序中，**不要再靠你自己判断**：

- `ACTIVE / WATCH / INACTIVE` 的判断
- 多窗口评分和权重
- keep / rollback 的 epsilon 规则
- 持仓数、交易数、回撤等硬约束
- G_event_driven 的粗调 / 细调步长
- 邻域稳健测试的通过标准

你只负责：
- 读取状态
- 执行一次迭代
- 看结果
- 把结果同步到 `search_notes.md`

---

## 固定流程

### 第 1 步：读取状态

先读：

```bash
cat trees/G_event_driven/experiments/<name>/state.json
cat trees/G_event_driven/experiments/<name>/iterations.tsv | tail -5
```

优先看这些字段：
- `direction_status`
- `direction_reason`
- `phase`
- `stable_param_ranges`
- `final_recommendation`
- `stop_reason`

如果满足以下任一条件，就停止继续自动探索：
- `direction_status == "INACTIVE"`
- `stop_reason` 非空
- `current_iter >= 100`

---

### 第 2 步：执行一次迭代

```bash
SKILL_DIR="skills/autoresearch_10jqka_backtest"
python ${SKILL_DIR}/run_iteration.py \
  --base trees/G_event_driven/experiments/<name> \
  --mutation-summary "G_event_driven 单轮验证"
```

说明：
- 不要自己定义阶段 A/B/C/D 的阈值
- 不要手动改 `formula_config.json`
- 不要并行跑多个迭代
- G_event_driven 默认只做有限粗搜索和有限细调

---

### 第 3 步：查看结果

再读：

如果你在**仓库根目录**执行：

```bash
cat skills/autoresearch_10jqka_backtest/trees/G_event_driven/experiments/<name>/state.json
cat skills/autoresearch_10jqka_backtest/trees/G_event_driven/experiments/<name>/iterations.tsv | tail -5
```

如果你在**实验目录**执行：

```bash
cat state.json
cat iterations.tsv | tail -5
```

你要关注的是：
- 当前 `direction_status` 是什么
- 这轮是 `keep` 还是 `rollback`
- `recent_6m / recent_12m / prior_12m / full_24m` 怎么样
- 有没有新的 `stable_param_ranges`
- `final_recommendation` 有没有变化

---

### 第 4 步：更新 `search_notes.md`

只同步**程序已经得出的结论**，不要自己重新解释阈值。

建议写法：

```markdown
## 当前状态
- 方向状态：ACTIVE / WATCH / INACTIVE
- 原因：直接抄 `state.json` 中的 `direction_reason`
- 阶段：直接抄 `phase`

## 当前 champion
- 最近6M：抄 `champion_windows.recent_6m.score`
- 最近12M：抄 `champion_windows.recent_12m.score`
- 前12M：抄 `champion_windows.prior_12m.score`
- 全24M：抄 `champion_windows.full_24m.score`

## 稳定参数带
- 直接抄 `stable_param_ranges`

## 最近结论
- keep / rollback 原因：直接抄最近一行 `iterations.tsv`
- 执行建议：直接抄 `final_recommendation`
```

---

## 不要做的事

- 不要自己定义什么叫 ACTIVE
- 不要自己发明新的评分规则
- 不要把 `program.md` 写成新的系统设计文档
- 不要跨 G1/G2/G3/G4/G5 随意跳方向
- 不要因为一次局部好看，就忽略邻域和多窗口验证

---

## 一句话原则

**程序负责判断，你负责按顺序执行和记录。**
