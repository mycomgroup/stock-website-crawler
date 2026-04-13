# Strategy Autoresearch — 增强版

你是一个自主运行的量化策略优化 agent。读完本文件后立即开始循环，不要停下来问用户。

本文件是 `program.md` 的增强版，核心差异：**每轮改动前必须先查通用机制库，从已验证的机制中选方向，而不是随机试错。**

---

## 目录结构

```
strategy_autoresearch_STRATEGY_NAME/
├── strategy.py        ← 唯一策略文件，你直接在这里改（唯一可改文件）
├── seed_config.json   ← 只读
├── state.json         ← 只读，由 run_iteration.py 维护
├── program_enhance.md ← 只读，本文件
└── history/
    ├── iterations.tsv
    ├── search_notes.md ← 你维护的搜索地图
    └── *.json
```

**通用机制库位置**（只读参考，不可修改）：
```
../universal_mechanisms/
├── README.md          ← 机制全景图，先看这个
├── 01_emotion_switch.md
├── 08_rsrs_timing.md
├── 24_fscore_selection.md
... （共 39 个机制文档）
```

---

## 实验循环

**LOOP FOREVER（直到人工中断或触发停止条件）：**

### 第 1 步：读取状态 + 查机制库

```python
import json
state = json.load(open("state.json"))
```

查看历史：`cat history/iterations.tsv`

**停止条件：**
- `consecutive_failures >= 5` 且 `search_notes.md` 中"待探索方向"已全部尝试
- 或 `current_iter >= 100`

**每轮开始前必做：查通用机制库**

读取 `../universal_mechanisms/README.md` 的机制全景图，按策略类型找对应推荐：

```
完整量化策略的 6 个能力层：

因子/Alpha（选股）  择时（开关）  风控（保护）  组合（权重）  执行（交易）  诊断（迭代）
```

**按当前策略类型，优先从以下机制中选改动方向：**

| 策略类型 | 优先查的机制 |
|---------|------------|
| 小市值/微盘 | 01情绪开关、26扩散指数、11一致性、15拥挤度 |
| 基本面价值 | 24FScore/FFScore、28高股息、08RSRS、20FED估值 |
| ETF轮动 | 08RSRS、13行业轮动、25EPO、09北向资金 |
| 首板/二板 | 01情绪开关、02停手、14竞价信号、17移动止损 |
| 指数增强 | 31指数增强底座、03状态路由、24FFScore、34权重映射 |

**读取对应机制文档，提取可直接用于当前策略的代码片段。**

---

### 第 2 步：分析上一轮，决定下一步改什么

读取或创建 `history/search_notes.md`：

```markdown
## 搜索地图

### 已验证有效（keep）
- [机制-01情绪开关] 加入涨停家数<30停止开仓：score +0.12，回撤 -8%
- [参数] top_n 30→20：score +0.08

### 已验证无效（rollback）
- [机制-08RSRS] 加入RSRS择时：score -0.03，过滤掉太多好机会
- [参数] window 26, 35：均差于当前

### 待探索方向（按优先级排序）
- [ ] [机制-26扩散指数] 加入扩散指数双均线门控（参考 ../universal_mechanisms/26_diffusion_index_timing.md）
- [ ] [机制-11一致性] 加入一致性风控（参考 ../universal_mechanisms/11_consistency_control.md）
- [ ] [参数] 双月调仓（月度已试，季度失败）
- [ ] [机制-17移动止损] 加入移动止盈止损（参考 ../universal_mechanisms/17_trailing_stop.md）

### 规律总结
- 情绪开关对本策略有效，回撤改善显著
- RSRS 对本策略过于保守，不适合
- 当前最优：top_n=20, 情绪开关阈值=30
```

**下一轮改什么的决策规则：**
1. 优先从"待探索"里选，且优先选有机制文档支撑的方向
2. 对"有效"的改动做进一步细化
3. 尝试组合已验证有效的改动
4. **不要随机试参数**，每次改动都要能说出"为什么这个机制对这个策略有效"

---

### 第 3 步：修改 strategy.py，提交回测

参考对应机制文档里的代码示例，直接修改 `strategy.py`。

**改动前检查清单：**
- [ ] 这个改动对应哪个机制？（写在 mutation-summary 里）
- [ ] 机制文档里有没有"注意事项"或"不适用场景"？
- [ ] 改动是否只改一个方向？

```bash
AUTORESEARCH_DIR="/Users/fengzhi/Downloads/git/testlixingren/skills/autoresearch_ricequant"
python ${AUTORESEARCH_DIR}/run_iteration.py \
    --base . \
    --mutation-summary "【机制类型-机制名】具体改了什么（改前→改后），参考 ../universal_mechanisms/XX.md，预期效果" > run.log 2>&1
echo "exit: $?"
```

`--mutation-summary` 格式示例：
- `【择时-情绪开关】加入涨停家数<30停止开仓，参考 01_emotion_switch.md，预期降低熊市回撤`
- `【风控-移动止损】加入从最高点回撤10%止损，参考 17_trailing_stop.md，预期控制单次最大亏损`
- `【参数调整】top_n 20→15，集中持仓，预期提升 calmar`

---

### 第 4 步：查看结果，更新搜索地图

```bash
grep -E "decision|score|annual|reason" history/<iter_id>.json
cat history/iterations.tsv
```

更新 `search_notes.md`：
- keep → 归入"已验证有效"，记录机制名和 score 提升
- rollback → 归入"已验证无效"，记录为什么无效（参数问题？机制不适合本策略？）
- crash → 记录 crash 原因，跳过这个方向

**回到第 1 步，继续循环。**

---

## 约束（不可违反）

1. **只改 `strategy.py`**，其他文件只读
2. **每次只改一个方向**
3. **不要重复失败的改动**
4. **不要问用户是否继续**
5. 不能把策略拆成多文件，不能新增 import 依赖
6. **改动必须有机制依据**：每次改动都要能对应到 `../universal_mechanisms/` 里的某个机制，或者是对已验证有效参数的细化

---

## 机制选择优先级

```
P0（必先试）：
  01_emotion_switch.md    — 情绪开关，几乎所有策略都有效
  04_base_filters.md      — 基础过滤，防止回测失真

P1（强推）：
  08_rsrs_timing.md       — RSRS择时，ETF/趋势策略必试
  26_diffusion_index_timing.md — 扩散指数，微盘/小市值必试
  17_trailing_stop.md     — 移动止损，控制单次亏损

P2（按策略类型）：
  24_fscore_selection.md  — 基本面选股
  28_dividend_quality_filter.md — 高股息过滤
  11_consistency_control.md — 一致性风控（微盘）
  15_crowding_detection.md — 拥挤度检测
  02_pause_mechanism.md   — 停手机制

P3（高级增强）：
  25_epo_portfolio.md     — EPO组合优化
  27_es_risk_parity.md    — ES风险平价
  03_state_router.md      — 状态路由
```

---

## 简洁性原则

- score 提升 < 0.001 但增加大量代码 → discard
- 删掉代码后得分持平或更好 → keep（简化胜利）
- 机制代码超过 30 行且效果不明显 → 考虑简化实现

---

## 评分公式

```
calmar = annual_return / max(abs(max_drawdown), 0.01)
score = calmar * 0.55 + sortino * 0.25 + information_ratio * 0.20
```

新 score **严格大于** champion score 才 keep。
`abs(max_drawdown) > 0.35` 直接 rollback（硬约束）。
