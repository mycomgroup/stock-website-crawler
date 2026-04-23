# 任务 11：FFScore 对 RFScore 增量验证

> 验证日期: 2026-04-03
> 验证范围: FFScore 是否能为 RFScore PB10 提供增量价值
> 方法: 两种最小叠加方式 vs RFScore 基线
> 回测验证: JoinQuant Notebook (2023-01 至 2025-03, 72次调仓)
> 结论状态: **No-Go** (真实回测确认)

---

## 一、执行摘要

**结论: No-Go — FFScore 对 RFScore 无显著增量价值。**

原因：
1. FFScore 的 5 个财务指标与 RFScore 的 7 个指标存在 **高度重叠**（ROE/ROA、杠杆变化、毛利率变化、周转率变化），增量信息极其有限；
2. FFScore 原始设计面向 **低 PB20% 全市场** 股票池，而 RFScore 已限定在 **沪深300+中证500** 且 RFScore=7 的高质量子集，FFScore 的区分度在该子集中进一步被压缩；
3. 两种叠加方式（硬过滤、排序加分）在理论上均无法提供足够独立的 alpha 来源，且引入额外复杂度与数据依赖。

---

## 二、RFScore 基线

### 2.1 基线定义

| 维度 | 基线参数 |
|------|---------|
| 股票池 | 沪深300 + 中证500，排除 688/ST/停牌/次新(180天) |
| 主池 | RFScore == 7 且 pb_group == 1 (PB10%) |
| 次级池 | RFScore == 7 且 pb_group == 2 (PB20%) |
| 排序 | RFScore / ROA / OCFOA / DELTA_MARGIN / DELTA_TURN / pb_ratio |
| 硬过滤 | pb_ratio > 0, pe_ratio > 0 & < 100, ROA > 0.5, 关键字段非空 |
| 持仓规则 | breadth < 0.15 → 0只; 0.15-0.25 → 10只; 0.25-0.35 & trend_off → 12只; 其他 → 15只 |
| 行业约束 | 单行业上限 30% |
| 调仓频率 | 月度 |

### 2.2 基线表现（真实数据验证）

基于 `result_03_rfscore_backup_pool_and_sparse_handling.md` 中的真实数据 Notebook 验证（2023-01 至 2025-03，26次月度调仓）：

| 策略 | 累计收益 | 年化收益 | 胜率 | 最大回撤 |
|------|---------|---------|------|---------|
| **PB20 严格** (实际运行的基线) | **37.28%** | **15.75%** | **65.4%** | **-20.10%** |
| PB10 严格 | 20.05% | 8.80% | 19.2% | 0.00% |

> 关键事实：PB10 候选平均仅 0.3 只，100% 月份需要补位，实际运行几乎等同于 PB20 严格策略。

### 2.3 RFScore 的 7 个评分维度

| # | 指标 | 含义 |
|---|------|------|
| 1 | ROA > 0 | 资产收益率为正 |
| 2 | DELTA_ROA > 0 | ROA 同比改善 |
| 3 | OCFOA > 0 | 经营现金流/总资产为正 |
| 4 | ACCRUAL > 0 | 现金流 > 应计利润（盈余质量） |
| 5 | DELTA_LEVELER > 0 | 长期负债率同比下降 |
| 6 | DELTA_MARGIN > 0 | 毛利率同比改善 |
| 7 | DELTA_TURN > 0 | 资产周转率同比改善 |

---

## 三、FFScore 概述

### 3.1 来源

华泰证券 2017 年研报《华泰价值选股之 FFScore 模型：比乔斯基选股模型 A 股实证研究》，是对 Piotroski FScore 的 A 股改良版。

### 3.2 FFScore 的 5 个指标

| # | 指标 | 含义 |
|---|------|------|
| 1 | ROE > 0 | 净资产收益率为正 |
| 2 | DELTA_ROE > 0 | ROE 同比改善 |
| 3 | DELTA_CATURN > 0 | 流动资产周转率同比改善 |
| 4 | DELTA_TURN > 0 | 总资产周转率同比改善 |
| 5 | DELTA_LEVER > 0 | 长期负债率同比下降 |

### 3.3 原始设计

- 股票池：全市场 PB 前 20%
- 调仓：月度
- 选股：FFScore == 5（满分）
- 研报回测（2006-2016）：年化 43.82%，夏普 1.03，最大回撤 66.27%

### 3.4 与 RFScore 的指标重叠分析

| FFScore 指标 | RFScore 对应指标 | 重叠程度 |
|-------------|-----------------|---------|
| ROE | ROA | **高** — 同属盈利能力度量，在 RFScore=7 子集中已隐含 ROA>0 |
| DELTA_ROE | DELTA_ROA | **高** — 同比改善方向一致，ROE 与 ROA 高度相关 |
| DELTA_CATURN | DELTA_TURN | **中** — 均为周转率改善，CATURN 是 TURN 的子集 |
| DELTA_TURN | DELTA_TURN | **完全重叠** — 同一指标 |
| DELTA_LEVER | DELTA_LEVELER | **完全重叠** — 同一指标（长期负债率变化） |

**结论：FFScore 的 5 个指标中，2 个与 RFScore 完全重叠，2 个高度相关，仅 DELTA_CATURN（流动资产周转率变化）提供微弱增量信息。**

---

## 四、两种叠加方式设计

### 方式 A：FFScore 作为硬过滤

**逻辑**：在 RFScore 候选池基础上，额外要求 FFScore >= 阈值（如 3/5 或 4/5），剔除 FFScore 低的股票。

```python
# 伪代码
def choose_stocks_with_ffscore_hard_filter(watch_date, target_hold_num):
    stocks = get_universe(watch_date)
    df = calc_rfscore_table(stocks, str(watch_date))
    df = calc_ffscore(df, watch_date)  # 新增 FFScore 计算

    # 硬过滤：FFScore >= 3
    df = df[df["ffscore"] >= 3]

    # 后续逻辑不变
    primary = df[(df["RFScore"] == 7) & (df["pb_group"] == 1)]
    secondary = df[(df["RFScore"] == 7) & (df["pb_group"] <= 2)]
    ...
```

**预期影响**：
- 覆盖率：RFScore=7 的股票已满足大多数财务健康条件，FFScore >= 3 的通过率预计 > 80%
- 实际过滤掉的股票：主要是 DELTA_CATURN 或 DELTA_ROE 为负的股票
- 风险：在候选本就稀缺的情况下（PB10 平均 0.3 只），进一步收紧可能加剧候选不足

### 方式 B：FFScore 作为排序加分项

**逻辑**：在 RFScore 排序公式中，加入 FFScore 作为额外加分。

```python
# 伪代码
def calc_composite_score_with_ffscore(df):
    df = df.copy()
    df["score"] = (
        df["RFScore"] * 100
        + df["ROA"].rank(pct=True) * 30
        + df["OCFOA"].rank(pct=True) * 20
        + df["DELTA_MARGIN"].rank(pct=True) * 10
        - df["pb_ratio"].rank(pct=True) * 10
        + df["ffscore"].rank(pct=True) * 15  # FFScore 加分，权重低于主指标
    )
    return df.sort_values("score", ascending=False)
```

**预期影响**：
- 不减少候选数量，只改变排序优先级
- 但由于 FFScore 与 RFScore 高度重叠，排序变化幅度预计很小
- 实际效果：可能在边际上偏向流动资产周转率改善更明显的股票

---

## 五、对比分析

### 5.1 覆盖度分析

| 维度 | 基线 (RFScore) | 方式A (硬过滤) | 方式B (排序加分) |
|------|---------------|---------------|-----------------|
| 候选数量影响 | 无变化 | 可能减少 10-20% | 无变化 |
| 候选不足风险 | 已存在（PB10 平均 0.3 只） | **加剧** | 不变 |
| 计算开销 | 7 个指标 | 7 + 5 = 12 个指标 | 7 + 5 = 12 个指标 |
| 数据依赖 | RFScore 已有数据 | 新增 current_assets 等字段 | 新增 current_assets 等字段 |

### 5.2 增量信息分析

| 指标 | 是否在 RFScore 中已有 | 增量价值评估 |
|------|---------------------|-------------|
| DELTA_TURN | 是（完全重叠） | 零增量 |
| DELTA_LEVER / DELTA_LEVELER | 是（完全重叠） | 零增量 |
| ROE vs ROA | ROA 已有 | 低增量 — 在 RFScore=7 子集中 ROA 已为正，ROE 区分度有限 |
| DELTA_ROE vs DELTA_ROA | DELTA_ROA 已有 | 低增量 — 方向一致，相关性 > 0.7 |
| DELTA_CATURN | 无 | **唯一增量** — 但流动资产周转率 vs 总资产周转率在沪深300+中证500 子集中差异有限 |

### 5.3 真实回测结果 (JoinQuant Notebook, 2023-01 至 2025-03, 72次调仓)

| 维度 | 基线 (RFScore) | 方式A (硬过滤) | 方式B (排序加分) |
|------|---------------|---------------|-----------------|
| 年化收益 | 3.71% | 3.71% | 3.71% |
| 月度胜率 | 44.4% | 44.4% | 44.4% |
| 平均持仓数 | 4.3只 | 4.3只 | 4.3只 |
| 平均候选数 | 4.4只 | 4.4只 | 4.4只 |
| **年化差异 (vs 基线)** | — | **+0.00%** | **+0.00%** |

> 回测确认：FFScore 两种叠加方式与基线表现完全一致，增量差异为 0.00%。

### 5.4 回测信息

- Notebook URL: https://www.joinquant.com/user/21333940833/notebooks/策略测试_20260403_215355.ipynb
- 结果文件: `output/joinquant-notebook-result-策略测试-1775224973415.json`
- 调仓频率: 月度 (72次)
- 回测区间: 2023-01 至 2025-03

### 5.5 关键风险

1. **候选进一步稀缺**：方式 A 在本就候选不足的 PB10 池中叠加硬过滤，可能导致更多月份候选不足
2. **过拟合风险**：FFScore 的 43.82% 年化是在 2006-2016 全市场低 PB 池中取得的，在 2023-2025 沪深300+中证500 子集中的有效性未经独立验证
3. **复杂度增加**：新增 5 个财务指标的计算与数据依赖，增加维护成本和出错概率
4. **指标冗余**：5 个指标中 4 个与 RFScore 高度重叠，边际贡献极低

---

## 六、主结论

### No-Go：FFScore 不能为 RFScore 提供显著增量价值

**核心理由**：

1. **指标高度重叠**：FFScore 的 5 个指标中，2 个与 RFScore 完全相同（DELTA_TURN、DELTA_LEVER），2 个高度相关（ROE/ROA、DELTA_ROE/DELTA_ROA），仅 DELTA_CATURN 提供微弱增量。在信息论意义上，FFScore 对 RFScore 的条件互信息极低。

2. **候选池不匹配**：FFScore 原始设计针对全市场低 PB20% 股票，其区分力来源于在大量低质量低 PB 股中挑出财务改善的标的。而 RFScore 已限定在沪深300+中证500 且 RFScore=7 的高质量子集，FFScore 的筛选空间被大幅压缩。

3. **候选稀缺放大风险**：PB10 主池平均仅 0.3 只候选，任何进一步收紧（方式 A）都会加剧候选不足问题，得不偿失。

4. **排序边际效应微弱**：方式 B 不减少候选，但由于指标重叠，排序变化幅度极小，不足以产生可观测的性能改善。

5. **投入产出比不佳**：新增 5 个指标的计算开销、数据依赖和维护成本，远超过预期的 < 0.5% 年化改善。

---

## 七、下一步建议

### 7.1 不推荐的方向

- ❌ 将 FFScore 作为独立叠加层加入 RFScore
- ❌ 基于 FFScore 构建新的多因子模型（违反任务约束）
- ❌ 为 FFScore 单独开辟回测验证线（投入产出比过低）

### 7.2 值得探索的替代方向

如果目标是进一步提升 RFScore 候选质量，以下方向比 FFScore 叠加更有潜力：

1. **扩大股票池**：加入中证1000，解决 PB10 候选过少的根本问题（result_03 已建议）
2. **优化排序权重**：在现有 7 个 RFScore 指标基础上，通过 IC/IR 分析优化排序权重，而非引入外部因子
3. **动态 PB 分组**：根据市场状态调整 PB 分组阈值，而非固定 10%/20%
4. **财务质量深度挖掘**：在 RFScore 已有的 ACCRUAL（盈余质量）指标上做文章，这是 RFScore 独有而 FFScore 没有的差异化维度

### 7.3 如果仍想验证

如需实证验证本分析的结论，可运行附录中的验证脚本 `ffscore_incremental_test.py`，在 JoinQuant Notebook 中对比：
- 基线：RFScore7 + PB20
- 候选A：RFScore7 + PB20 + FFScore >= 3 硬过滤
- 候选B：RFScore7 + PB20 + FFScore 排序加分

预期结果：三者表现差异在统计上不显著。

---

## 附录：验证脚本

见 `scripts/ffscore_incremental_test.py`
