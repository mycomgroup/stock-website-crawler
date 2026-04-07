# Strategy Autoresearch

你是一个自主运行的量化策略优化 agent。读完本文件后立即开始循环，不要停下来问用户。

---

## 目录结构

```
strategy_autoresearch_STRATEGY_NAME/
├── strategy.py        ← 唯一策略文件，你直接在这里改（唯一可改文件）
├── seed_config.json   ← 只读，不可改
├── state.json         ← 只读，由 run_iteration.py 维护
├── program.md         ← 只读，本文件
└── history/
    ├── iterations.tsv ← 只读，由 run_iteration.py 维护
    ├── 0000_baseline.json
    └── 0001.json, ...
```

**只读文件（不可修改）**：`seed_config.json`、`state.json`、`program.md`、`history/`、以及 autoresearch 目录下的所有 `.py` 工具文件（`run_iteration.py`、`ricequant_executor.py`、`scorer.py`、`preflight_checker.py`）。

---

## 实验循环

**LOOP FOREVER（直到人工中断或触发停止条件）：**

### 第 1 步：读取状态，分析上一轮

```python
import json
state = json.load(open("state.json"))
# 关键字段：current_iter, champion_score, champion_metrics, consecutive_failures
```

查看历史：`cat history/iterations.tsv`

**停止条件（满足任一则停止）：**
- `consecutive_failures >= 5`
- `current_iter >= 100`（见 seed_config.json 的 loop.max_iterations）

分析思路：
- 看历史记录，找还没试过的改进方向
- 优先改对得分影响最大的指标（年化收益权重 0.45 > 回撤 0.30 > 夏普 0.20 > 胜率 0.05）
- 每次只改一个方向，小步迭代

### 第 2 步：直接修改 strategy.py，提交回测

直接编辑 `strategy.py`（就在实验目录里，原地改）。

改完后运行（**输出重定向到文件，不要让日志淹没 context**）：

```bash
AUTORESEARCH_DIR="/Users/fengzhi/Downloads/git/testlixingren/skills/autoresearch"
python ${AUTORESEARCH_DIR}/run_iteration.py \
    --base . \
    --mutation-summary "一句话描述本轮改了什么" > run.log 2>&1
echo "exit: $?"
```

脚本自动完成：预检查 → 提交回测 → 等待结果（最多 600s）→ 评分 → keep/rollback → 写 history/。

### 第 3 步：查看结果，继续下一轮

```bash
# 读取 exit code（0=keep, 1=rollback, 2=crash）
# 已在上一步 echo 出来

# 查看关键指标
grep -E "decision|score|annual|reason" history/<iter_id>.json

# 查看完整历史（含 commit hash）
cat history/iterations.tsv
```

- exit code 0 = keep（state.json 已更新 champion，strategy.py 已 git commit）
- exit code 1 = rollback（strategy.py 已自动恢复到 champion 版本）
- exit code 2 = crash（回测失败或超时）

**如果 crash（超时或平台错误）**：查看 `run.log` 末尾了解原因。超时（回测超过 600s）属于正常 crash，直接跳过这个改动，换方向继续。不要反复重试同一个超时的改动。

```bash
tail -n 30 run.log
```

**回到第 1 步，继续循环。**

---

## 约束（不可违反）

1. **只改 `strategy.py`**，其他文件只读
2. **每次只改一个方向**，不要同时改多处
3. **不要重复失败的改动**，每轮前先看 `history/iterations.tsv`
4. **不要问用户是否继续**，你是自主运行的
5. 不能把策略拆成多文件，不能新增 import 依赖

---

## 简洁性原则

改动要权衡收益和复杂度：
- 微小提升（score 提升 < 0.001）但增加了大量复杂代码 → **不值得，discard**
- 删掉代码后得分持平或更好 → **一定 keep，这是简化胜利**
- 得分接近但代码更简洁 → **keep**

每次改动前问自己：这个改动的复杂度代价值得吗？

---

## 评分公式

```
score = annual_return * 0.45 - abs(max_drawdown) * 0.30 + sharpe * 0.20 + win_rate * 0.05
```

新 score **严格大于** champion score 才 keep，否则 rollback。
`abs(max_drawdown) > 0.35` 直接 rollback（硬约束）。
