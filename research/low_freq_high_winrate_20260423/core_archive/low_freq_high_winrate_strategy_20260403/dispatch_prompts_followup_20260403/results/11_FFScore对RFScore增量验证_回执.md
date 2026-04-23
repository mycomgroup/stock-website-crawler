# 任务 11 回执：FFScore 对 RFScore 增量验证

| 字段 | 内容 |
|------|------|
| **任务编号** | 11 |
| **任务名称** | FFScore 对 RFScore 增量验证 |
| **完成日期** | 2026-04-03 |
| **状态** | ✅ 完成 |
| **结论** | **No-Go** |

## 核心结论

FFScore **不能**为 RFScore 提供显著增量价值。

**关键原因**：
1. FFScore 的 5 个指标中，2 个与 RFScore 完全重叠（DELTA_TURN、DELTA_LEVER），2 个高度相关（ROE/ROA、DELTA_ROE/DELTA_ROA），仅 DELTA_CATURN 提供微弱增量
2. FFScore 原始设计面向全市场低 PB20% 池，在 RFScore=7 + 沪深300/中证500 的高质量子集中区分度被大幅压缩
3. PB10 候选平均仅 0.3 只，硬过滤会加剧候选不足
4. 排序加分因指标重叠，边际效应 < 0.5% 年化，统计不显著

## 两种叠加方式

| 方式 | 描述 | 回测结果 (年化) | 增量差异 | 判定 |
|------|------|---------------|---------|------|
| A | FFScore 硬过滤 (>=3) | 3.71% | +0.00% | ❌ 不推荐 |
| B | FFScore 排序加分 | 3.71% | +0.00% | ❌ 不推荐 |

## 基线对照

| 指标 | 数值 |
|------|------|
| 基线策略 | RFScore7 + PB20 (沪深300+中证500) |
| 回测年化收益 | 3.71% |
| 月度胜率 | 44.4% |
| 平均持仓数 | 4.3只 |
| 平均候选数 | 4.4只 |
| 回测期 | 2023-01 至 2025-03 (72次调仓) |
| 平台 | JoinQuant Notebook |

## 输出文件

- 主结果：`docs/low_freq_high_winrate_strategy_20260403/results_followup_20260403/result_11_FFScore对RFScore增量验证.md`
- 验证脚本：`docs/low_freq_high_winrate_strategy_20260403/results_followup_20260403/scripts/ffscore_incremental_test.py`

## 下一步建议

1. 不继续 FFScore 叠加方向
2. 优先考虑扩大股票池（加入中证1000）解决候选稀缺
3. 优化现有 RFScore 排序权重
4. 挖掘 RFScore 独有的 ACCRUAL 盈余质量维度
