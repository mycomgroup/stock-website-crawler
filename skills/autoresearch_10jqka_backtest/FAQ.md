# 问财公式回测自动研究系统常见问题

## Q1: 为什么要做多窗口确认？

单窗口评分容易被尖点欺骗。最近有机会不代表参数稳健。

v4 系统在 4 个时间窗口（6M/12M/prior12M/24M）上验证，只有多窗口都表现稳定的配置才会被选为 champion。这避免了"近期表现好但不可持续"的问题。

---

## Q2: 什么是邻域敏感性测试？

对候选参数的相邻配置做测试，检查是否是脆弱的尖点。

具体做法：
1. 对候选参数周围的邻域配置进行回测
2. 计算 `sensitivity = std(neighbor_scores) / mean(neighbor_scores)`
3. 如果 sensitivity > 0.3，认为参数脆弱，触发 sensitivity_penalty

```
尖点: 邻域分数差异大 → sensitivity 高 → 惩罚
平台: 邻域分数一致 → sensitivity 低 → 通过
```

---

## Q3: 方向状态 ACTIVE/WATCH/INACTIVE 是什么意思？

| 状态 | 含义 | 研究建议 |
|------|------|----------|
| `ACTIVE` | 最近 6~12 月持续有信号 | 可继续深挖 |
| `WATCH` | 有信号但不稳定 | 谨慎跟踪，观察是否转 ACTIVE |
| `INACTIVE` | 近期无明显机会 | 切换到其他 seed，或停止该方向 |

---

## Q4: 为什么要选参数平台而不是最高分点？

尖点在实盘中容易失真，平台中心更稳定。

```
峰值选择的问题:
- 找到的是历史最优，但不是未来最优
- 邻域配置表现差异大，实盘容易跳点
- 极端参数对数据噪声敏感

平台选择的优势:
- 邻域配置一致性高，抗噪声能力强
- 参数在实盘中有更大容错空间
- 多窗口验证一致性更好
```

---

## Q5: 如果某个 seed 被判为 INACTIVE 怎么办？

两个选择：

1. **切换到其他 seed**: 在 seeds/ 目录中选择其他方向继续研究
2. **停止该方向的深挖**: 标记为已尝试，换一个分支探索

```
状态转换示例:
seed_A: ACTIVE → WATCH (信号减弱) → INACTIVE (无信号)
seed_B: ACTIVE (接过主力)
```

---

## Q6: trade_count_penalty 是什么？

交易次数太少（<20）的回测结果不可信，因此惩罚。

```
trade_count >= 20: trade_count_penalty = 0
trade_count < 20:  trade_count_penalty = 0.5
```

原因：样本量太小的回测结果波动性大，不具备统计显著性。

---

## Q7: sensitivity_penalty 怎么计算？

```
sensitivity = std(neighbor_scores) / mean(neighbor_scores)

if sensitivity > 0.3:
    sensitivity_penalty = 0.3
else:
    sensitivity_penalty = 0
```

举例：
- 邻域分数 [0.8, 0.82, 0.81, 0.79]: mean=0.805, std=0.012, sensitivity=0.015 → 无惩罚
- 邻域分数 [1.0, 0.5, 0.3, 0.2]: mean=0.5, std=0.31, sensitivity=0.62 → 惩罚 0.3

---

## Q8: setup.py 的 baseline 评分和 scorer.py 不一致会有什么影响？

导致实验之间不可比。v4 已统一使用 scorer.py 计算 baseline。

setup.py 在初始化时会运行多窗口回测，scorer.py 负责计算 robust_score。两者的评分逻辑必须一致，否则：
- baseline 和后续迭代的评分基准不同
- 无法判断后续改进是否真正有效

---

## Q9: 如何初始化实验？

```bash
cd skills/autoresearch_10jqka_backtest
python setup.py --name my_experiment
```

Mock 模式：
```bash
python setup.py --name test --mock
```

---

## Q10: 如何查看当前状态？

```bash
cat state.json
cat iterations.tsv
```

v4 state.json 示例：
```json
{
  "direction_status": "ACTIVE",
  "robust_score": 1.6543,
  "parameter_band": {
    "takeProfit": [15, 20],
    "stopLoss": [9, 12],
    "maxPositions": [5, 8]
  }
}
```

---

## Q11: 如何启用 Mock 模式？

```bash
export JQKA_MOCK_MODE=1
python setup.py --name test
```

或使用 `--mock` 参数：
```bash
python setup.py --name test --mock
```

---

## Q12: Session 无效怎么办？

```bash
cd skills/10jqka_backtest
node browser/manual-login-capture.js
```

---

## Q13: 回测超时怎么办？

回测超时属于正常 crash，直接跳过这个改动，换方向继续。不要反复重试同一个超时的改动。

---

## Q14: 如何跳过某个变异方向？

在 `search_notes.md` 的"待探索方向"中标记为已尝试：
```markdown
- [x] ~~调整止损阈值~~（已尝试，效果不佳）
```

---

## Q15: 变异类型有哪些？

**Formula 条件变异（核心）**：

| 变异类型 | 说明 |
|---------|------|
| `adjust_formula_threshold` | 调整筛选条件数值阈值 |
| `add_formula_condition` | 添加新筛选条件 |
| `remove_formula_condition` | 移除筛选条件 |
| `adjust_formula_sort` | 调整排序条件方向 |

**回测参数变异**：

| 变异类型 | 说明 |
|---------|------|
| `adjust_days_for_sale` | 调整持仓天数策略 |
| `adjust_max_positions` | 调整最大持仓数 |
| `adjust_daily_buy_count` | 调整每日买入数 |
| `adjust_take_profit` | 调整止盈阈值 |
| `adjust_stop_loss` | 调整止损阈值 |
| `adjust_trailing_stop` | 调整追踪止损阈值 |

---

## Q16: Formula 条件变异具体支持哪些？

详见 `formula_mutator.py` 的条件候选库：

```bash
head -80 formula_mutator.py  # 数值条件库
grep "FORMULA_ADDABLE_CONDITIONS" -A 30 formula_mutator.py  # 可添加条件
```

**数值条件**：
- 周成交量环比增长率（1%~20%）
- 涨幅范围（0%~30%）
- 上市时间（100~1000天）
- 换手率（1%~20%）
- 市盈率（10~100）
- 市净率（1~10）
- 净资产收益率（5%~30%）
- 毛利率（10%~80%）

**可添加条件**：
- 换手率大于5%/8%/10%
- 流通市值小于50亿/100亿/200亿
- 市盈率小于30/50
- 市净率小于3/5
- 净资产收益率大于10%/15%
- 毛利率大于30%/50%
- 非科创板、非退市、破发股、破净股等

---

## Q17: 停止条件是什么？

- `consecutive_failures >= 5` 且 `search_notes.md` 中"待探索方向"已全部尝试
- 或 `current_iter >= 100`
- 或所有 seed 都处于 INACTIVE 状态

---

## Q18: 如何手动运行一次迭代？

```bash
cd experiments/<name>

python ../../run_iteration.py \
    --base . \
    --mutation-summary "【筛选阈值】周成交量增长率 8% → 10%" \
    --mutation-type adjust_formula_threshold
```

---

## Q19: 如何恢复到某个历史版本？

```bash
cd experiments/<name>
git log --oneline
git checkout <commit_hash> -- formula_config.json
```

---

## Q20: 目录结构是怎样的？

```
experiments/<name>/
├── formula_config.json   # 当前配置
├── state.json            # 实验状态 (v4)
├── iterations.tsv        # 迭代历史 (v4)
├── search_notes.md       # 搜索笔记
├── program.md            # Agent 指南副本
└── README.md             # 实验说明
```

注意：不再有 `history/` 子目录。
