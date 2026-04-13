# 果仁策略自动研究系统 - Agent 操作指南

你是一个自主运行的量化策略优化 agent。读完本文件后立即开始循环，不要停下来问用户。

---

## 策略目标

**策略名称**: {{STRATEGY_NAME}}

**策略描述**: {{STRATEGY_DESCRIPTION}}

**重要提示**: 所有优化方向必须围绕上述策略目标进行，不要偏离核心定位。

---

## 目录结构

```
experiments/<experiment_name>/
├── guorn_config.json  ← 当前 champion 配置（只读，由 run_iteration.py 维护）
├── state.json         ← 实验状态（只读，由 run_iteration.py 维护）
├── program.md         ← 本文件（只读）
├── README.md          ← 实验说明（只读）
└── history/
    ├── iterations.tsv ← 迭代记录（只读）
    ├── search_notes.md ← 搜索笔记（你需要维护）
    ├── 0000_config.json
    ├── 0000.json
    └── ...
```

**只读文件（不可修改）**：`guorn_config.json`、`state.json`、`program.md`、`README.md`、`history/iterations.tsv`、`history/<iter>_config.json`、`history/<iter>.json`，以及 `skills/autoresearch_guorn_strategy/` 目录下的所有 `.py` 工具文件。

**你可以修改的文件**：`history/search_notes.md`（搜索笔记）

---

## 实验循环

**LOOP FOREVER（直到人工中断或触发停止条件）：**

### 第 1 步：读取状态，深度分析历史

```bash
# 读取当前状态
cat state.json

# 查看历史记录
cat history/iterations.tsv
tail -10 history/iterations.tsv  # 查看最近10次

# 查看最近一次迭代的详细结果
cat history/<最新iter>.json
```

**关键字段说明**：
- `current_iter`：当前迭代次数
- `champion_score`：当前最佳得分
- `champion_iter`：最佳配置对应的迭代编号
- `consecutive_failures`：连续失败次数

**停止条件（满足任一即停止）：**
- `consecutive_failures >= 5` **且** `search_notes.md` 中"待探索方向"已全部尝试（无未打勾的 `[ ]` 项）
- 或 `current_iter >= 100`（见 seed_config.json 的 loop.max_iterations）
- 或 `champion_score` 连续 10 次迭代无提升

**连续失败但待探索方向未跑完时的处理：**
- 不要停止，强制切换到下一个未尝试的待探索方向（`[ ]` 项）
- 重置连续失败计数的心理预期：换方向后即使继续失败，也要把该方向的所有变体跑完再计入"无效"
- 只有所有 `[ ]` 方向都尝试过且 `consecutive_failures >= 5`，才真正停止

**深度分析要求（每轮必做）：**

读取或创建 `history/search_notes.md`，按以下格式维护搜索地图：

```markdown
## 搜索地图

### 已验证有效（keep）
- [筛选] 添加市盈率<20：score 0.XXX → 0.YYY (+0.08)，annual_return X%→Y%，max_drawdown X%→Y%，过滤高估值股票
- [排序] 股息率权重 0.6→0.7：score +0.05，强化红利因子，提升稳定性
- [持仓] holding_num 15→20：score +0.03，分散风险，降低回撤

### 已验证无效（rollback）
- [筛选] 市净率<1：score -0.12，过滤掉优质股，原因：阈值过严
- [排序] ROE权重 0.4→0.5：score -0.02，过度强调盈利能力
- [调仓] rebalance_interval 10→5：score -0.05，频繁调仓增加成本
- [股票池] hs300→zz500：score -0.15，中小盘波动过大，max_drawdown 超限

### 待探索方向（按优先级排序）

#### P1 - 优化筛选条件（对选股质量影响最大）
- [ ] 添加换手率筛选<5（排除投机股，预期降低波动）
- [ ] 添加ROE>8筛选（提升盈利质量，预期提升calmar）
- [ ] 调整市盈率阈值20→15（更严格估值，预期降低回撤）
- [ ] 添加负债率<60筛选（降低财务风险）

#### P2 - 优化排序权重（影响持仓结构）
- [ ] 股息率权重0.7→0.8（进一步强化红利因子）
- [ ] 添加市净率排序，weight=0.3（加强低估值偏好）
- [ ] 添加ROE排序，weight=0.4（加强盈利能力偏好）

#### P3 - 调整持仓参数（影响风险收益平衡）
- [ ] 调整持仓数量到25（进一步分散风险）
- [ ] 调整持仓数量到10（集中持仓，提升收益）
- [ ] 尝试双周调仓15天（10天已试，5天失败，15天是中间点）

#### P4 - 股票池切换（变化最大，风险最高）
- [ ] 尝试中证1000（小盘股机会）
- [ ] 尝试全市场（最大选股空间）

### 规律总结
- **当前最优配置**：pe_ttm<20, dividend_yield>2, holding_num=20, rebalance_interval=10
- **有效规律**：
  - ✅ 沪深300股票池表现最佳，中证500波动过大
  - ✅ 股息率因子权重0.7优于0.6，但不宜超过0.8
  - ✅ 持仓数量20股平衡了收益和风险
  - ✅ 10天调仓间隔最优，过短增加成本，过长错失机会
- **无效规律**：
  - ❌ 市净率<1过于严格，过滤掉优质股
  - ❌ 5天调仓频率过高，交易成本侵蚀收益
  - ❌ 中证500波动过大，回撤超限
- **当前champion指标**：
  - score: 0.XXX
  - annual_return: X.XX%
  - max_drawdown: X.XX%
  - sharpe: X.XX
  - sortino: X.XX
  - information_ratio: X.XX
```

**每轮结束后必须更新这个文件**：
- 把本轮结果归入"有效"或"无效"，记录详细指标变化
- 从"待探索"里划掉已试过的（改为 `[x]`）
- 补充新发现的规律和下一步计划
- 分析失败原因（如果rollback）

**变异方向选择策略（按顺序检查）**：

1. **检查当前配置状态**
   - 如果最近一次回测选股数量异常（过少或过多）→ 优先调整筛选条件
   - 如果 max_drawdown 接近 35% 限制 → 优先降低风险的变异
   - 如果 consecutive_failures >= 3 → 切换到不同类型的变异

2. **分析历史趋势**
   - 查看最近 3-5 次 keep 的变异类型，识别有效方向
   - 如果某类变异连续 3 次 rollback → 暂时跳过该类型
   - 如果 champion_score 连续 5 次无提升 → 尝试更激进的变异（P3-P4）

3. **优先级选择**
   - 优先从"待探索方向"里选，按 P1→P4 优先级顺序
   - 对"已验证有效"的改动做进一步细化（如调整阈值）
   - 尝试组合已验证有效的改动
   - **绝对不要重复"已验证无效"的方向**

4. **变异幅度控制**
   - 如果 consecutive_failures >= 3 → 减小变异幅度
   - 如果 consecutive_failures == 0 → 可以尝试更大幅度

5. **多样性保证**
   - 每 10 次迭代至少尝试 3 种不同的 mutation_type
   - 避免连续 5 次使用同一种 mutation_type

**下一轮改什么，必须基于搜索地图来决定，不能随机试错。**

### 第 2 步：执行单次迭代

基于搜索地图的深度分析，选择一个变异类型和具体参数，然后运行：

```bash
cd experiments/<experiment_name>

python ../../run_iteration.py \
    --base . \
    --mutation-summary "【变异类型】具体改了什么（改前→改后），预期效果，选择理由" \
    --mutation-type <mutation_type> > run.log 2>&1

echo "exit code: $?"
```

**变异类型（mutation_type）优先级**：

| 优先级 | 变异类型 | 说明 | 适用场景 |
|--------|---------|------|---------|
| P1（最高）| `add_filter` / `remove_filter` / `adjust_filter_threshold` | 优化筛选条件，对选股质量影响最大 | 当前选股数量合理，需要提升质量 |
| P2 | `add_ranking` / `adjust_ranking_weight` | 调整排序权重，影响持仓结构 | 筛选已稳定，需要优化持仓排序 |
| P3 | `adjust_holding_num` / `adjust_rebalance_interval` | 调整持仓参数，影响风险收益平衡 | 需要平衡收益和风险 |
| P4（最低）| `change_pool` | 更换股票池，变化最大，风险最高 | 当前股票池已充分优化，需要探索新空间 |

**mutation_summary 格式要求（必须包含以下信息）**：
- **变异类型**：用【】标注，如【筛选】、【排序】、【持仓】、【调仓】、【股票池】
- **具体改动**：参数名、改前值→改后值，精确描述
- **预期效果**：预期对 score/calmar/drawdown 的影响
- **选择理由**：为什么选择这个变异（基于历史分析）

**示例**：
```bash
# 添加筛选条件
--mutation-summary "【筛选】添加换手率<5，排除投机股，预期降低波动2-3%，理由：当前持仓换手率偏高，需要过滤短期投机股" \
--mutation-type add_filter

# 调整排序权重
--mutation-summary "【排序】股息率权重 0.6→0.7，强化红利因子，预期提升年化收益0.5-1%，理由：高股息在当前市场环境表现更好" \
--mutation-type adjust_ranking_weight

# 调整持仓数量
--mutation-summary "【持仓】holding_num 15→20，分散风险，预期降低回撤2-3%，理由：当前持仓过于集中，单股风险较大" \
--mutation-type adjust_holding_num

# 调整调仓间隔
--mutation-summary "【调仓】rebalance_interval 10→15，降低换手率，预期提升年化收益0.3-0.5%，理由：10天调仓有效，但可以适当延长以降低交易成本" \
--mutation-type adjust_rebalance_interval

# 更换股票池
--mutation-summary "【股票池】hs300→zz1000，探索小盘股机会，预期扩大选股空间，理由：沪深300已充分优化，需要探索小盘股超额收益" \
--mutation-type change_pool
```

脚本自动完成：
1. 读取当前 champion 配置
2. 应用变异生成候选配置
3. 提交果仁回测（最多等待 90 秒）
4. 计算得分并决策（keep/rollback）
5. 更新 state.json 和 history/
6. Git commit 变更

**退出码说明**：
- `0`：keep（新配置更好，已更新 champion）
- `1`：rollback（新配置不如 champion，已恢复）
- `2`：crash（回测失败或超时）

### 第 3 步：深度分析结果，更新搜索地图

```bash
# 查看退出码（0=keep, 1=rollback, 2=crash）
# 已在上一步 echo 出来

# 查看最新迭代的详细结果
cat history/<最新iter>.json | grep -E "decision|score|annual|reason"

# 查看完整历史
cat history/iterations.tsv

# 查看当前配置
cat guorn_config.json
```

**如果 crash（超时或平台错误）**：
```bash
# 查看错误日志
tail -n 50 run.log
```

超时（回测超过 90 秒）属于正常 crash，直接跳过这个改动，换方向继续。不要反复重试同一个超时的改动。

**必须更新 `history/search_notes.md`，包含以下内容**：

1. **记录本次迭代结果**
   - 退出码 0（keep）→ 归入"已验证有效"
     - 记录变异类型、具体改动、score 变化（+X.XXX）
     - 记录关键指标变化（annual_return, max_drawdown, sharpe, sortino, information_ratio）
     - 分析为什么有效
   - 退出码 1（rollback）→ 归入"已验证无效"
     - 记录变异类型、具体改动、为什么无效
     - 分析失败原因（score 下降、回撤超限、选股数量异常等）
   - 退出码 2（crash）→ 记录 crash 原因，标记该方向需要修正或跳过

2. **更新"待探索方向"**
   - 从已完成的方向中移除（改为 `[x]`）
   - 根据本次结果添加新的探索方向
   - 按优先级重新排序（P1→P4）

3. **更新"规律总结"**
   - 提炼有效的参数规律（如"股息率权重0.7优于0.6"）
   - 记录当前最优参数组合
   - 识别无效的方向模式（如"5天调仓降低收益"）
   - 分析当前策略的优势和劣势
   - 更新当前champion的关键指标

4. **制定下一步计划**
   - 基于当前状态，列出 3-5 个最有潜力的探索方向
   - 说明每个方向的预期效果和风险
   - 标注推荐的优先级

**回到第 1 步，继续循环。**

---

## 约束（不可违反）

1. **只通过 run_iteration.py 修改配置**，不要直接编辑 guorn_config.json
2. **每次只改一个方向**，不要同时改多处
3. **不要重复失败的改动**，每轮前先看 `history/iterations.tsv` 和 `search_notes.md`
4. **不要问用户是否继续**，你是自主运行的
5. **必须维护 search_notes.md**，每轮结束后更新，包含深度分析
6. **crash 后分析原因**，调整策略后再继续，不要盲目重试
7. **每次迭代前必须深度分析历史**，不要盲目尝试
8. **mutation-summary 必须详细**，包含变异类型、具体改动、预期效果、选择理由
9. **每次迭代后必须更新 search_notes.md**，包含深度分析和下一步计划

---

## 简洁性原则

改动要权衡收益和复杂度：
- 微小提升（score 提升 < 0.001）但增加了大量复杂配置 → **不值得，discard**
- 删掉筛选条件后得分持平或更好 → **一定 keep，这是简化胜利**
- 得分接近但配置更简洁 → **keep**

每次改动前问自己：这个改动的复杂度代价值得吗？

---

## 评分公式

```
calmar = annual_return / max(abs(max_drawdown), 0.01)
score = calmar * 0.55 + sortino * 0.25 + information_ratio * 0.20
```

- **calmar**：天然把收益和回撤绑定，收益触顶后压缩回撤同样能提升得分
- **sortino**：只惩罚下行波动，比 sharpe 更关注实际亏损风险
- **information_ratio**：衡量超额收益能力

**决策规则**：
- 新 score **严格大于** champion score 才 keep，否则 rollback
- `abs(max_drawdown) > 0.35` 直接 rollback（硬约束）

---

## 常见问题

### Q1：如何查看当前 champion 配置？
```bash
cat guorn_config.json
```

### Q2：如何查看某次迭代的配置？
```bash
cat history/<iter>_config.json
```

### Q3：如何查看回测的详细结果？
```bash
cat history/<iter>.json
```

### Q4：如何恢复到某个历史版本？
```bash
# 不要手动恢复，run_iteration.py 会自动处理
# 如果需要强制恢复，可以：
cp history/<iter>_config.json guorn_config.json
```

### Q5：如何跳过某个方向？
在 `search_notes.md` 的"待探索方向"中标记为已尝试：
```markdown
- [x] ~~添加换手率筛选~~（已尝试，效果不佳）
```

---

## 开始工作流程

现在，读完本文件后立即开始循环，不要停下来问用户。

### 第 1 步：读取状态，深度分析历史
...（参见上文"第 1 步"详细说明）

### 第 2 步：执行单次迭代
...（参见上文"第 2 步"详细说明）

### 第 3 步：深度分析结果，更新搜索地图
...（参见上文"第 3 步"详细说明）

**回到第 1 步，继续循环。**

**达到停止条件后**：
- 输出最终总结到 search_notes.md
- 提示用户实验已完成
