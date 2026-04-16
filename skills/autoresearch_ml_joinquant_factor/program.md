# ML 多策略弱因子自动研究 - Agent 操作指南

你是一个自主运行的因子搜索 agent。读完本文件后立即开始循环，不要停下来问用户。

---

## 目录结构

```
strategy_autoresearch_ml_<name>/
├── strategy.py            ← 当前最优因子组合（自动同步）
├── strategy_pool.json     ← Top-K 策略池（多策略并存）
├── search_notes.md        ← 状态 + 历史 + 搜索地图
├── iteration_history.jsonl ← 每轮迭代明细（只读）
├── iterations.tsv         ← 迭代摘要（只读）
└── program.md             ← 本文件（只读）
```

**只读文件（不可修改）**：`iteration_history.jsonl`、`iterations.tsv`、`program.md`

---

## 实验循环

**LOOP FOREVER（直到人工中断或触发停止条件）：**

### 第 1 步：读取状态

```bash
cat search_notes.md
cat strategy_pool.json
```

查看迭代历史：
```bash
cat iterations.tsv | tail -20
```

### 第 2 步：分析上一轮

读取 `search_notes.md` 和 `strategy_pool.json`，关注：
1. **Top-K 池**：当前最优的 K 组策略及其分数
2. **搜索地图**：已探索方向、待探索方向
3. **失败模式**：哪些组合模式反复失败

**停止条件（同时满足才停止）：**
- `consecutive_failures >= 5` **且** 待探索方向已全部尝试
- 或 `current_iter >= 100`

**连续失败但待探索方向未跑完时的处理：**
- 不要停止，强制切换到下一个未尝试的待探索方向
- 只有所有 `[ ]` 方向都尝试过且 `consecutive_failures >= 5`，才真正停止

### 第 3 步：生成候选组合

策略优先级：
1. **待探索方向**：从搜索地图中选取未尝试的方向
2. **变异**：对 Top-K 中的高分组合做小范围变异
3. **频率优先**：选择历史上出现频率高的有效因子
4. **随机采样**：确保探索多样性

生成参数：
- `--batch-size`：每轮候选数（建议 8-16）
- `--top-k`：保留策略数（建议 5-10）

### 第 4 步：执行迭代命令

```bash
AUTORESEARCH_DIR="/path/to/skills/autoresearch_ml_joinquant_factor"
python ${AUTORESEARCH_DIR}/run_iteration.py \
    --base . \
    --batch-size 8 \
    --top-k 5 \
    --mutation-summary "【改动类型】具体改了什么，预期效果" > run.log 2>&1
echo "exit: $?"
```

`--mutation-summary` 格式要求：
- 写清楚**改动类型**（待探索/变异/频率优先/随机采样）
- 写清楚**具体改了什么**（因子名、组合逻辑）
- 写清楚**预期效果**（为什么这样改）

脚本自动完成：
- 生成候选组合
- 执行回测评估
- 更新 Top-K 池
- 同步最优组合到 `strategy.py`
- 更新 `search_notes.md`

### 第 5 步：查看结果

```bash
# 读取 exit code（0=有改进，1=无改进）
# 已在上一步 echo 出来

# 查看最新状态
cat search_notes.md

# 查看 Top-K 策略池
cat strategy_pool.json

# 查看迭代历史
cat iterations.tsv | tail -10
```

- exit code 0 = 有候选进入 Top-K（策略池已更新）
- exit code 1 = 本轮无改进（策略池不变）

**回到第 1 步，继续循环。**

---

## 约束（不可违反）

1. **只生成因子组合**，通过 `run_iteration.py` 自动执行，不手动修改 `strategy.py`
2. **每次只改一个方向**，不要同时尝试多个新方向
3. **不要重复失败的组合**，每轮前先看 `search_notes.md` 和 `strategy_pool.json`
4. **不要问用户是否继续**，你是自主运行的
5. **因子组合必须满足**：
   - 因子数量：3-8 个
   - 分散度 >= 0.5（至少一半因子来自不同类别）
   - 不与已失败组合重复

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

**硬约束**：
- 分散度 < 0.5 → 直接淘汰
- IC均值 < 0 → 直接淘汰
- 因子数 < 3 或 > 8 → 直接淘汰

---

## 因子池

```
administration_expense_ttm, asset_impairment_loss_ttm, cash_flow_to_price_ratio,
circulating_market_cap, EBIT, EBITDA, financial_assets, financial_expense_ttm,
financial_liability, goods_sale_and_service_render_cash_ttm, gross_profit_ttm,
interest_carry_current_liability, interest_free_current_liability, market_cap,
net_debt, net_finance_cash_flow_ttm, net_interest_expense, net_invest_cash_flow_ttm,
net_operate_cash_flow_ttm, net_profit_ttm, net_working_capital,
non_operating_net_profit_ttm, non_recurring_gain_loss, np_parent_company_owners_ttm,
OperateNetIncome, operating_assets, operating_cost_ttm, operating_liability,
operating_profit_ttm, operating_revenue_ttm, retained_earnings, sales_to_price_ratio,
sale_expense_ttm, total_operating_cost_ttm, total_operating_revenue_ttm,
total_profit_ttm, value_change_profit_ttm, AR, ARBR, ATR14, ATR6, BR, DAVOL10,
DAVOL20, DAVOL5, MAWVAD, money_flow_20, PSY, turnover_volatility, TVMA20, TVMA6,
TVSTD20, TVSTD6, VDEA, VDIFF, VEMA10, VEMA12, VEMA26, VEMA5, VMACD, VOL10, VOL120,
VOL20, VOL240, VOL5, VOL60, VOSC, VR, VROC12, VROC6, VSTD10, VSTD20, WVAD,
financing_cash_growth_rate, net_asset_growth_rate, net_operate_cashflow_growth_rate,
net_profit_growth_rate, np_parent_company_owners_growth_rate,
operating_revenue_growth_rate, PEG, total_asset_growth_rate, total_profit_growth_rate,
arron_down_25, arron_up_25, BBIC, bear_power, BIAS10, BIAS20, BIAS5, BIAS60,
bull_power, CCI10, CCI15, CCI20, CCI88, CR20, fifty_two_week_close_rank, MASS,
PLRC12, PLRC24, PLRC6, Price1M, Price1Y, Price3M, Rank1M, ROC12, ROC120, ROC20,
ROC6, ROC60, single_day_VPT, single_day_VPT_12, single_day_VPT_6, TRIX10, TRIX5,
Volume1M, capital_reserve_fund_per_share, cashflow_per_share_ttm,
cash_and_equivalents_per_share, eps_ttm, net_asset_per_share,
net_operate_cash_flow_per_share, operating_profit_per_share,
operating_profit_per_share_ttm, operating_revenue_per_share,
operating_revenue_per_share_ttm, retained_earnings_per_share, retained_profit_per_share,
surplus_reserve_fund_per_share, total_operating_revenue_per_share,
total_operating_revenue_per_share_ttm, ACCA, accounts_payable_turnover_days,
accounts_payable_turnover_rate, account_receivable_turnover_days,
account_receivable_turnover_rate, adjusted_profit_to_total_profit, admin_expense_rate,
asset_turnover_ttm, cash_rate_of_sales, cash_to_current_liability, cfo_to_ev,
current_asset_turnover_rate, current_ratio, debt_to_asset_ratio, debt_to_equity_ratio,
debt_to_tangible_equity_ratio, DEGM, DEGM_8y, DSRI, equity_to_asset_ratio,
equity_to_fixed_asset_ratio, equity_turnover_rate, financial_expense_rate,
fixed_assets_turnover_rate, fixed_asset_ratio, GMI,
goods_service_cash_to_operating_revenue_ttm, gross_income_ratio, intangible_asset_ratio,
inventory_turnover_days, inventory_turnover_rate, invest_income_associates_to_total_profit,
long_debt_to_asset_ratio, long_debt_to_working_capital_ratio, long_term_debt_to_asset_ratio,
LVGI, margin_stability, maximum_margin, MLEV, net_non_operating_income_to_total_profit,
net_operate_cash_flow_to_asset, net_operate_cash_flow_to_net_debt,
net_operate_cash_flow_to_operate_income, net_operate_cash_flow_to_total_current_liability,
net_operate_cash_flow_to_total_liability, net_operating_cash_flow_coverage, net_profit_ratio,
net_profit_to_total_operate_revenue_ttm, non_current_asset_ratio, OperatingCycle,
operating_cost_to_operating_revenue_ratio, operating_profit_growth_rate,
operating_profit_ratio, operating_profit_to_operating_revenue, operating_profit_to_total_profit,
operating_tax_to_operating_revenue_ratio_ttm, profit_margin_ttm, quick_ratio, rnoa_ttm,
ROAEBITTTM, roa_ttm, roa_ttm_8y, roe_ttm, roe_ttm_8y, roic_ttm,
sale_expense_to_operating_revenue, SGAI, SGI, super_quick_ratio, total_asset_turnover_rate,
total_profit_to_cost_ratio, Kurtosis120, Kurtosis20, Kurtosis60, sharpe_ratio_120,
sharpe_ratio_20, sharpe_ratio_60, Skewness120, Skewness20, Skewness60, Variance120,
Variance20, Variance60, average_share_turnover_annual, average_share_turnover_quarterly,
beta, book_leverage, book_to_price_ratio, cash_earnings_to_price_ratio, cube_of_size,
cumulative_range, daily_standard_deviation, debt_to_assets, earnings_growth,
earnings_to_price_ratio, earnings_yield, growth, historical_sigma, leverage, liquidity,
long_term_predicted_earnings_growth, market_leverage, momentum, natural_log_of_market_cap,
non_linear_size, predicted_earnings_to_price_ratio, raw_beta, relative_strength,
residual_volatility, sales_growth, share_turnover_monthly, short_term_predicted_earnings_growth,
size, boll_down, boll_up, EMA5, EMAC10, EMAC12, EMAC120, EMAC20, EMAC26, MAC10, MAC120,
MAC20, MAC5, MAC60, MACDC, MFI14, price_no_fq
```

## 因子分类表

| 类别 | 示例因子 |
|------|----------|
| basics | circulating_market_cap, market_cap, sales_to_price_ratio, EBIT, EBITDA, net_profit_ttm |
| emotion | TVMA6, TVSTD20, VOL10, VOL20, money_flow_20, AR, BR, ARBR, VMACD, VOSC |
| growth | net_profit_growth_rate, operating_revenue_growth_rate, PEG, total_asset_growth_rate |
| momentum | ROC60, Price1M, Price3M, single_day_VPT_12, CCI20, BIAS20, fifty_two_week_close_rank |
| pershare | eps_ttm, net_asset_per_share, cashflow_per_share_ttm, operating_profit_per_share |
| quality | roe_ttm, roa_ttm, current_asset_turnover_rate, cfo_to_ev, debt_to_asset_ratio |
| risk | Kurtosis120, Skewness60, sharpe_ratio_120, Variance20, sharpe_ratio_60 |
| style | size, natural_log_of_market_cap, beta, momentum, liquidity, book_to_price_ratio |
| technical | MAC120, EMAC120, boll_down, boll_up, MFI14, EMA5 |

**每次组合尽量从不同类别选因子，提高分散度。**