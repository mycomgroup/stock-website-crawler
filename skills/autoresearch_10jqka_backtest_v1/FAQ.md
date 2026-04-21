# 问财公式回测自动研究系统常见问题

## Q1：如何初始化实验？

```bash
cd skills/autoresearch_10jqka_backtest
python setup.py --name my_experiment
```

Mock 模式：
```bash
python setup.py --name test --mock
```

## Q2：如何开始迭代？

```bash
cd experiments/my_experiment
# 阅读 program.md，让 agent 开始迭代循环
```

## Q3：如何查看当前状态？

```bash
cat state.json
cat iterations.tsv
```

## Q4：如何查看当前配置？

```bash
cat formula_config.json
```

## Q5：如何查看回测历史？

```bash
cat iterations.tsv | tail -10
```

## Q6：如何恢复到某个历史版本？

```bash
cd experiments/<name>
git log --oneline
git checkout <commit_hash> -- formula_config.json
```

## Q7：如何启用 Mock 模式？

```bash
export JQKA_MOCK_MODE=1
python setup.py --name test
```

或使用 `--mock` 参数：
```bash
python setup.py --name test --mock
```

## Q8：Session 无效怎么办？

```bash
cd skills/10jqka_backtest
node browser/manual-login-capture.js
```

## Q9：回测超时怎么办？

回测超时属于正常 crash，直接跳过这个改动，换方向继续。不要反复重试同一个超时的改动。

## Q10：如何跳过某个变异方向？

在 `search_notes.md` 的"待探索方向"中标记为已尝试：
```markdown
- [x] ~~调整止损阈值~~（已尝试，效果不佳）
```

## Q11：变异类型有哪些？

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

## Q12：Formula 条件变异具体支持哪些？

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

## Q13：评分公式是什么？

```
calmar = annual_return / max(abs(max_drawdown), 0.01)
score = calmar * 0.55 + sortino * 0.25 + information_ratio * 0.20
```

新 score **严格大于** champion score 才 keep。
`abs(max_drawdown) > 0.35` 直接 rollback（硬约束）。

## Q14：停止条件是什么？

- `consecutive_failures >= 5` 且 `search_notes.md` 中"待探索方向"已全部尝试
- 或 `current_iter >= 100`

## Q15：如何手动运行一次迭代？

```bash
cd experiments/<name>

python ../../run_iteration.py \
    --base . \
    --mutation-summary "【筛选阈值】周成交量增长率 8% → 10%" \
    --mutation-type adjust_formula_threshold
```

## Q16：目录结构是怎样的？

```
experiments/<name>/
├── formula_config.json   # 当前配置
├── state.json            # 实验状态
├── iterations.tsv        # 迭代历史
├── search_notes.md       # 搜索笔记
├── program.md            # Agent 指南副本
└── README.md             # 实验说明
```

注意：不再有 `history/` 子目录。