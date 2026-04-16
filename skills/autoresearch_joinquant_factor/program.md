# 因子自动搜索 - Agent 操作指南

你是一个自主运行的因子搜索 agent。读完本文件后立即开始循环，不要停下来问用户。

---

## 目录结构

```
strategy_autoresearch_factor_<name>/
├── strategy.py        ← 唯一文件，包含因子组合+评估代码，每次迭代更新
├── search_notes.md    ← 状态 + 历史 + 搜索地图
├── iterations.tsv     ← 只读，由 run_iteration.py 维护
└── program.md         ← 本文件（只读）
```

**只读文件（不可修改）**：`iterations.tsv`、`program.md`

---

## 实验循环

**LOOP FOREVER（直到人工中断或触发停止条件）：**

### 第 1 步：读取状态，分析上一轮

```bash
cat search_notes.md
cat iterations.tsv
```

查看 git 历史：
```bash
git log --oneline -10
```

**停止条件（同时满足才停止）：**
- `consecutive_failures >= 5` **且** `iterations.tsv` 和 `search_notes.md` 中"待探索方向"已全部尝试
- 或 `current_iter >= 100`

**连续失败但待探索方向未跑完时的处理：**
- 不要停止，强制切换到下一个未尝试的待探索方向
- 只有所有 `[ ]` 方向都尝试过且 `consecutive_failures >= 5`，才真正停止

**分析要求（每轮必做）：**

读取 `search_notes.md`，关注：
1. 当前 champion_score 和 champion_factors
2. 已尝试组合表格，避免重复
3. 待探索方向，决定下一步

每轮结束后更新 `search_notes.md`：
- 把本轮结果归入"有效"或"无效"
- 从"待探索"里划掉已试过的
- 补充新发现的规律

**下一轮改什么，必须基于搜索地图来决定，不能随机试错。**

优先级：
1. 先把"待探索"里的方向系统性地跑完
2. 对"有效"的因子组合做进一步变异
3. 尝试组合已验证有效的因子

### 第 2 步：修改 strategy.py

直接编辑 `strategy.py`，只改 `FACTOR_COMBO` 这一行：

```python
FACTOR_COMBO = ['factor1', 'factor2', 'factor3']
```

改完后 git commit：
```bash
git add strategy.py
git commit -m "iter_XXXX: 新因子组合 [factor1, factor2] 预期效果"
```

### 第 3 步：执行回测

```bash
AUTORESEARCH_DIR="AUTORESEARCH_DIR_PLACEHOLDER"
python ${AUTORESEARCH_DIR}/run_iteration.py \
    --base . \
    --mutation-summary "【改动类型】具体改了什么，预期效果" > run.log 2>&1
echo "exit: $?"
```

`--mutation-summary` 格式要求：
- 写清楚**改动类型**（随机采样/频率优先/高分变异）
- 写清楚**具体改了什么**（因子名）
- 写清楚**预期效果**（为什么这样改）

脚本自动完成：执行 Notebook → 评分 → keep/rollback → 更新 search_notes.md。

### 第 4 步：查看结果，继续下一轮

```bash
# 读取 exit code（0=keep, 1=rollback）
# 已在上一步 echo 出来

# 查看最新状态
cat search_notes.md

# 查看完整迭代历史
cat iterations.tsv
```

- exit code 0 = keep（search_notes.md 已更新 champion）
- exit code 1 = rollback（strategy.py 已自动恢复到 champion 版本）

**回到第 1 步，继续循环。**

---

## 约束（不可违反）

1. **只改 `strategy.py` 中的 `FACTOR_COMBO`**，其他文件只读
2. **每次只改一个方向**，不要同时改多处
3. **不要重复失败的改动**，每轮前先看 `search_notes.md`
4. **不要问用户是否继续**，你是自主运行的
5. **不要修改 strategy.py 中的评估代码**，只改因子组合

---

## 评分公式

综合评分（0-1）由 8 项指标加权：

| 指标 | 权重 | 说明 |
|------|------|------|
| 分层多空收益 | 25% | Group_1 - Group_10 累计收益 |
| 顶层夏普比率 | 15% | 顶层收益风险调整后收益 |
| IC均值 | 15% | 因子值与收益率秩相关均值 |
| ICIR | 10% | IC均值/IC标准差 |
| IC胜率 | 5% | IC>0的周期占比 |
| 分层单调性 | 10% | 各组收益单调递减程度 |
| 收益波动率 | 10% | 顶层收益波动（越低越好） |
| 类别分散度 | 10% | 因子来自不同类别的程度 |

新 score **严格大于** champion score 才 keep，否则 rollback。

**硬约束**：
- 分散度 < 0.5 → 直接 rollback
- IC均值 < 0 → 直接 rollback

---

## 因子池

```
size, momentum, roe_ttm, beta, liquidity,
natural_log_of_market_cap, share_turnover_monthly,
book_to_price_ratio, earnings_yield, residual_volatility,
growth, leverage, non_linear_size, cube_of_size,
long_term_predicted_earnings_growth, predicted_earnings_to_price_ratio,
earnings_to_price_ratio, cash_earnings_to_price_ratio,
book_leverage, market_leverage, raw_beta, relative_strength,
sales_growth, earnings_growth, historical_sigma,
cumulative_range, daily_standard_deviation, debt_to_assets,
average_share_turnover_annual, average_share_turnover_quarterly
```

## 因子分类

| 类别 | 示例因子 |
|------|----------|
| basics | circulating_market_cap, market_cap, sales_to_price_ratio |
| emotion | TVMA6, TVSTD20, VOL10, VOL20, money_flow_20 |
| growth | net_profit_growth_rate, operating_revenue_growth_rate |
| momentum | ROC60, Price1M, Price3M, single_day_VPT_12 |
| quality | roe_ttm, roa_ttm, current_asset_turnover_rate, cfo_to_ev |
| style | size, natural_log_of_market_cap, beta, momentum, liquidity |
| technical | MAC120, EMAC120, boll_down |

**每次组合尽量从不同类别选因子，提高分散度。**
