# Strategy Autoresearch

你是一个自主运行的量化策略优化 agent。读完本文件后立即开始循环，不要停下来问用户。

---

## 目录结构

```
strategy_autoresearch_rfscore7_pb10_enhanced_20260407/
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

**分析要求（每轮必做）：**

读取或创建 `history/search_notes.md`，按以下格式维护搜索地图：

```markdown
## 搜索地图

### 已验证有效（keep）
- [参数] base_hold_num 20→30：score +0.12，calmar 提升
- [过滤] 新增 PE<50：score +0.08，回撤降低

### 已验证无效（rollback）
- [参数] base_hold_num 30→40：score -0.05，分散过度
- [过滤] 新增 PB<1.5：score -0.03，股票池太小

### 待探索方向
- [ ] 调仓频率（当前月度，可试双月/季度）
- [ ] 止损阈值（当前无止损）
- [ ] 市场宽度过滤（熊市减仓）

### 规律总结
- 持仓数量在 20-25 之间效果最好，超过 30 开始分散过度
- PE 过滤有效，但阈值不能太严（<30 会导致股票池过小）
```

每轮结束后更新这个文件：
- 把本轮结果归入"有效"或"无效"
- 从"待探索"里划掉已试过的
- 补充新发现的规律

**下一轮改什么，必须基于搜索地图来决定，不能随机试错。**

优先级：
1. 先把"待探索"里的方向系统性地跑完
2. 对"有效"的改动做进一步细化（如 base_hold_num 已知 20-25 有效，可以试 22、23）
3. 尝试组合已验证有效的改动

### 第 2 步：直接修改 strategy.py，提交回测

直接编辑 `strategy.py`（就在实验目录里，原地改）。

改完后运行（**输出重定向到文件，不要让日志淹没 context**）：

```bash
AUTORESEARCH_DIR="/Users/fengzhi/Downloads/git/testlixingren/skills/autoresearch_ricequant"
python ${AUTORESEARCH_DIR}/run_iteration.py \
    --base . \
    --mutation-summary "【改动类型】具体改了什么参数/逻辑（改前→改后），预期效果" > run.log 2>&1
echo "exit: $?"
```

`--mutation-summary` 格式要求：
- 写清楚**改动类型**（参数调整/选股逻辑/过滤条件/仓位管理/止盈止损）
- 写清楚**具体改了什么**（变量名、改前值→改后值）
- 写清楚**预期效果**（为什么这样改）
- 示例：`"[参数] base_hold_num 20→30，预期提升分散度降低单股风险"`
- 示例：`"[过滤] 新增 PE<50 过滤，去除高估值股票，预期降低回撤"`
- 示例：`"[仓位] 等权改为按 RFScore 加权，高分股多配，预期提升收益"`
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
