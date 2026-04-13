# Wizard Strategy Autoresearch — Agent 操作指南

你是一个自主运行的向导式策略参数优化 agent。读完本文件后立即开始循环，不要停下来问用户。

本系统优化的对象是 `wizard_config.json`（JSON 参数配置），而非 Python 代码。每轮迭代通过 `run_iteration.py` 自动完成：变异配置 → 提交回测 → 评分 → keep/rollback。

---

## 目录结构

```
skills/autoresearch_ricequant-wizard/
├── scorer.py                    ← 只读，评分模块
├── wizard_executor.py           ← 只读，执行器
├── wizard_mutator.py            ← 只读，变异器
├── run_iteration.py      ← 只读，单次迭代 CLI 入口
├── setup.py           ← 只读，初始化脚本
├── seed_wizard_config.json      ← 只读，种子配置
├── program.md            ← 只读，本文件
└── experiments/
    └── <experiment_name>/
        ├── wizard_config.json   ← 可写，当前 champion 配置
        ├── state.json           ← 只读，由脚本维护
        └── history/
            ├── iterations.tsv   ← 只读，由脚本维护
            ├── search_notes.md  ← 可写，你维护的搜索地图
            ├── 0000_config.json
            ├── 0000.json
            └── ...
```

**文件权限一览：**

| 文件 | 权限 | 说明 |
|------|------|------|
| `state.json` | 只读 | 由 run_iteration.py 自动维护 |
| `seed_wizard_config.json` | 只读 | 种子配置，不可修改 |
| `program.md` | 只读 | 本操作指南 |
| `scorer.py` / `wizard_executor.py` / `wizard_mutator.py` / `run_iteration.py` / `setup.py` | 只读 | 工具文件，不可修改 |
| `experiments/<name>/wizard_config.json` | 可写 | 由 keep/rollback 机制自动更新 |
| `experiments/<name>/history/search_notes.md` | 可写 | 你负责维护的搜索地图 |

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
cat experiments/<name>/history/iterations.tsv
```

**停止条件（满足任一即停止）：**
- `consecutive_failures >= 5` 且 `search_notes.md` 中"待探索方向"已全部尝试
- 或 `current_iter >= 100`

如未触发停止条件，继续下一步。

---

### 第 2 步：分析历史，选择变异方向

读取或创建 `experiments/<name>/history/search_notes.md`，格式如下：

```markdown
## 搜索地图

### 已验证有效（keep）
- [add_filter] pe_ratio < 15：score +0.18，回撤 -5%
- [adjust_sorting_weight] dividend_yield 权重 0.6→0.8：score +0.06

### 已验证无效（rollback）
- [change_universe] 000300→000905：score -0.12，收益下降明显
- [adjust_rebalance_interval] 10→1：score -0.08，换手率过高

### 待探索方向（按优先级排序）
- [ ] [add_filter] 加入 roe > 10 过滤低质量公司
- [ ] [add_filter] 加入 debt_ratio < 50 过滤高杠杆
- [ ] [adjust_filter_threshold] pe_ratio 阈值从 15 调低到 10
- [ ] [adjust_sorting_weight] pb_ratio 排序权重调整
- [ ] [adjust_holding_num] maxHoldingNum 15→10，集中持仓

### 规律总结
- 基本面过滤对本策略有效，pe+dividend 组合表现最佳
- 频繁调仓（rebalanceInterval<5）会显著降低 calmar
- 当前最优：pe_ratio<15, dividend_yield>3, maxHoldingNum=15, rebalanceInterval=10
```

**变异方向选择优先级（按顺序尝试）：**

| 优先级 | 变异类型 | 说明 |
|--------|---------|------|
| P1（最高）| `add_filter` / `remove_filter` / `adjust_filter_threshold` | 优化 filters 组合，对选股质量影响最大 |
| P2 | `add_sorting` / `adjust_sorting_weight` | 调整排序权重，影响持仓结构 |
| P3 | `adjust_holding_num` | 调整持仓数量，影响集中度 |
| P4 | `adjust_rebalance_interval` | 调整调仓周期，影响换手率 |
| P5（最低）| `change_universe` | 切换股票池，变化最大，风险最高 |

**决策规则：**
1. 优先从"待探索方向"里选，按优先级顺序
2. 对"已验证有效"的改动做进一步细化（如调整阈值）
3. 尝试组合已验证有效的改动
4. 不要重复"已验证无效"的方向

---

### 第 3 步：执行迭代

```bash
SKILL_DIR="skills/autoresearch_ricequant-wizard"
python ${SKILL_DIR}/run_iteration.py \
    --base ${SKILL_DIR}/experiments/<name> \
    --mutation-summary "【变异类型】具体改了什么（改前→改后），预期效果" \
    [--mutation-type <type>]
echo "exit: $?"
```

`--mutation-summary` 格式示例：
- `【add_filter】新增 roe > 10 过滤低质量公司，预期提升 calmar`
- `【adjust_filter_threshold】pe_ratio 阈值 15→10，更严格的估值过滤，预期降低回撤`
- `【adjust_sorting_weight】dividend_yield 权重 0.6→0.8，加强高股息排序，预期提升年化`
- `【adjust_holding_num】maxHoldingNum 15→10，集中持仓，预期提升 calmar`
- `【change_universe】000300→000905，切换到中证500，预期扩大选股空间`

`--mutation-type` 可选值（对应 wizard_mutator.py 中的 MUTATION_TYPES）：
- `add_filter`
- `remove_filter`
- `adjust_filter_threshold`
- `add_sorting`
- `adjust_sorting_weight`
- `adjust_holding_num`
- `adjust_rebalance_interval`
- `change_universe`

不指定 `--mutation-type` 时，系统随机选择变异类型。

**退出码含义：**
- `0` = keep（新配置更优，已保存为 champion）
- `1` = rollback（新配置不如 champion，已恢复）
- `2` = crash（执行出错，consecutive_failures +1）

---

### 第 4 步：查看结果，更新搜索地图

```bash
# 查看最新迭代结果
cat experiments/<name>/history/iterations.tsv | tail -5

# 查看详细记录（替换 <iter_id> 为实际编号，如 0001）
cat experiments/<name>/history/<iter_id>.json
```

更新 `experiments/<name>/history/search_notes.md`：
- 退出码 0（keep）→ 归入"已验证有效"，记录变异类型和 score 提升量
- 退出码 1（rollback）→ 归入"已验证无效"，记录为什么无效
- 退出码 2（crash）→ 记录 crash 原因，跳过这个方向

**回到第 1 步，继续循环。**

---

## 可变异参数空间

### 1. filters（筛选条件）

每个 filter 的结构：
```json
{
  "operator": "less_than",
  "factor": {"type": "fundamental", "name": "pe_ratio"},
  "rhs": 15
}
```

**因子候选库（来自 wizard_mutator.py FACTOR_CANDIDATES）：**

| 因子名 | 类型 | 合理范围 | 默认阈值 | 支持的 operator | 说明 |
|--------|------|---------|---------|----------------|------|
| `pe_ratio` | fundamental | [5, 80] | 20 | `less_than`, `in_range` | 市盈率，越低越便宜 |
| `pb_ratio` | fundamental | [0.5, 5] | 2 | `less_than` | 市净率，越低越便宜 |
| `roe` | fundamental | [5, 30] | 10 | `greater_than` | 净资产收益率，越高越好 |
| `dividend_yield` | fundamental | [1, 8] | 2 | `greater_than` | 股息率，越高越好 |
| `debt_ratio` | fundamental | [20, 70] | 50 | `less_than` | 资产负债率，越低越稳健 |
| `revenue_growth_rate` | fundamental | [0, 30] | 5 | `greater_than` | 营收增长率，越高越好 |
| `net_profit_growth_rate` | fundamental | [0, 30] | 5 | `greater_than` | 净利润增长率，越高越好 |
| `market_cap` | fundamental | [5e8, 1e11] | 1e9 | `greater_than`, `less_than` | 市值，单位元 |
| `turnover_rate` | pricing | [0.5, 10] | 2 | `greater_than`, `less_than` | 换手率，单位% |

**变异示例：**
- `add_filter`：新增 `roe > 10`，过滤低质量公司
- `remove_filter`：删除 `debt_ratio < 50`，放宽杠杆限制
- `adjust_filter_threshold`：`pe_ratio < 15` → `pe_ratio < 12`（阈值调整 ±20%~±50%）

### 2. sorting（排序规则）

每个 sorting 规则的结构：
```json
{
  "factor": {"type": "fundamental", "name": "dividend_yield"},
  "ascending": false,
  "weight": 0.6
}
```

- `ascending: false` = 降序（高值优先，适合 dividend_yield、roe）
- `ascending: true` = 升序（低值优先，适合 pe_ratio、pb_ratio）
- `weight`：权重，正数，无需归一化

**变异示例：**
- `add_sorting`：新增 `roe` 降序排序，weight=0.3
- `adjust_sorting_weight`：`dividend_yield` 权重 0.6 → 0.8（调整 ±20%~±50%）

### 3. maxHoldingNum（最大持仓数量）

**候选值（HOLDING_NUM_OPTIONS）：** `[5, 10, 15, 20, 25, 30]`

- 值越小，持仓越集中，波动越大
- 值越大，持仓越分散，接近指数

**变异示例：**
- `adjust_holding_num`：`15 → 10`（集中持仓，提升 calmar）

### 4. rebalanceInterval（调仓间隔，单位：交易日）

**候选值（REBALANCE_OPTIONS）：** `[1, 3, 5, 10, 15, 20, 30]`

- 值越小，调仓越频繁，换手率越高，摩擦成本越大
- 值越大，调仓越少，持仓更稳定

**变异示例：**
- `adjust_rebalance_interval`：`10 → 20`（降低换手率）

### 5. universe（股票池）

**候选值（UNIVERSE_OPTIONS）：** `["000300.XSHG", "000905.XSHG", "000852.XSHG", "*"]`

| 值 | 说明 |
|----|------|
| `000300.XSHG` | 沪深300，大盘蓝筹 |
| `000905.XSHG` | 中证500，中盘成长 |
| `000852.XSHG` | 中证1000，小盘 |
| `*` | 全市场 |

**变异示例：**
- `change_universe`：`000300.XSHG → 000905.XSHG`（切换到中证500）

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

1. **只改 `experiments/<name>/wizard_config.json`**，其他文件只读（由脚本自动管理）
2. **每次只改一个方向**（一次变异只对应一种 mutation_type）
3. **不要重复失败的改动**（参考 search_notes.md 中"已验证无效"）
4. **不要问用户是否继续**，直接循环
5. **不要修改任何 .py 工具文件**
6. **crash 后继续循环**，不要因为单次 crash 停止

---

## search_notes.md 维护规范

文件路径：`experiments/<name>/history/search_notes.md`

**格式模板：**

```markdown
## 搜索地图

### 已验证有效（keep）
- [mutation_type] 具体改动描述：score 从 X.XXX → Y.YYY，+Z.ZZZ

### 已验证无效（rollback）
- [mutation_type] 具体改动描述：rollback，原因（score 下降 / 回撤超限）

### 待探索方向（按优先级排序）
- [ ] [mutation_type] 具体方向描述
- [ ] [mutation_type] 具体方向描述

### 规律总结
- 观察到的规律，如"pe_ratio 阈值越低，calmar 越高"
- 当前最优参数组合描述
```

**维护规则：**
- 每次迭代后必须更新 search_notes.md
- keep → 从"待探索"移到"已验证有效"，记录 score 变化
- rollback → 从"待探索"移到"已验证无效"，记录原因
- 定期更新"规律总结"，提炼有效的参数规律
- "待探索方向"按 P1→P5 优先级排序

---

## 停止条件

满足以下任一条件时停止循环：

1. `consecutive_failures >= 5` **且** `search_notes.md` 中"待探索方向"已全部尝试
2. `current_iter >= 100`

停止后，输出最终 champion 配置的路径和 score：
```bash
cat experiments/<name>/state.json | python -c "import json,sys; s=json.load(sys.stdin); print(f'champion_score={s[\"champion_score\"]:.4f}, champion_iter={s[\"champion_iter\"]}')"
```

