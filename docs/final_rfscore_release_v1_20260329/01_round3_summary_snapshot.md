# Round 3 Summary

## 用途

这个文件是第三轮 `RFScore PB10` 调研的统一汇总页。

从这一轮开始，所有子任务都必须遵守下面两条：

1. 结果文档必须写回本目录：`/Users/fengzhi/Downloads/git/testlixingren/docs/parallel_strategy_tasks_20260328_round3_rfscore_pb10`
2. 每个任务跑完后，必须同步更新本文件对应条目，至少补齐：
   - `状态`
   - `结果文件`
   - `一句话结论`
   - `是否进入正式版本`

## 结果命名约定

| 任务 | 建议结果文件 |
|------|--------------|
| 01 | `result_01_rfscore_data_parity_and_sanity.md` |
| 02 | `result_02_rfscore_pb10_official_baseline.md` |
| 03 | `result_03_rfscore_backup_pool_and_sparse_handling.md` |
| 04 | `result_04_rfscore_filter_enhancement_final.md` |
| 05 | `result_05_rfscore_market_state_sizing.md` |
| 06 | `result_06_rfscore_candidate_quality_monitor.md` |
| 07 | `result_07_rfscore_dividend_smallcap_full_backtest.md` |
| 08 | `result_08_rfscore_defensive_base_full_backtest.md` |
| 09 | `result_09_rfscore_capacity_and_execution.md` |
| 10 | `result_10_rfscore_sector_and_hidden_exposure.md` |

## 任务总表

### 01 数据口径与异常审计

- 状态：✅ 已完成
- 结果文件：`result_01_rfscore_data_parity_and_sanity.md`
- 一句话结论：发现 tmp/ 目录下脚本仍使用 PB20%（应改为 PB10%），候选股存在 PE 657 等异常值，需增加 PE<100 和 ROA>0.5% 的硬过滤
- 是否进入正式版本：是 - 口径对齐和异常过滤规则需纳入正式策略
- 主要修复：
  - ✅ 已修复 `tmp/rfscore7_current_candidates.py` 第 122 行：pb_group <= 2 → == 1
  - ✅ 已修复 `tmp/rfscore7_candidate_industry.py` 第 121 行：pb_group <= 2 → == 1

### 02 PB10 正式基线封版

- 状态：✅ 已完成
- 结果文件：`result_02_rfscore_pb10_official_baseline.md`
- 一句话结论：**PB10% 是唯一正式基线，年化收益 20.62%，夏普 0.974，全面优于 PB20 及其他版本**
- 是否进入正式版本：✅ **是，已确立为唯一正式版本**
- 正式文件：`/Users/fengzhi/Downloads/git/testlixingren/strategies/rfscore7_pb10_final.py`
- 当前建议：**市场弱势(宽度0.230)，建议等待好转后再上模拟盘**

### 03 候选稀疏与备用池机制

- 状态：✅ 已完成
- 结果文件：`result_03_rfscore_backup_pool_and_sparse_handling.md`
- 一句话结论：**PB10+PB20 备用池最不伤策略，15只持仓最稳（年化20.31%，夏普0.91），绝不用 Score≥6 补位**
- 是否进入正式版本：✅ **是，备用池规则已确认**
- 关键参数：
  - 目标持仓：15只 (g.base_hold_num = 15)
  - 减仓持仓：12只 (g.reduced_hold_num = 12)
  - 备用池：PB20% (RFScore=7)，绝不放宽到 Score≥6
  - 补位限制：PB20 占比 < 50%，避免质量稀释

### 04 过滤器终审

- 状态：**✅ 已完成**
- 结果文件：`result_04_rfscore_filter_enhancement_final.md`
- 一句话结论：**行业集中度约束必选，Turnover和CGO过滤可选保留，Combined双重过滤淘汰**
- 是否进入正式版本：
  - ✅ **Industry Cap**: 正式进入（必选）
  - ✅ **Turnover Filter**: 正式进入（可选，默认启用）
  - ✅ **CGO Filter**: 正式进入（可选，建议震荡市启用）
  - ❌ **Combined Filter**: 淘汰（过度复杂）

### 05 市场状态与仓位控制

- 状态：**✅ 已完成**
- 结果文件：`result_05_rfscore_market_state_sizing.md`
- 一句话结论：**RFScore应采用四档渐进式仓位规则(20/15/10/5只)，不设空仓线，底部收紧至PB5%**
- 是否进入正式版本：✅ **是，建议替换原有两档规则**
- 关键规则：
  - 正常(≥40%宽度): 20只，PB10%，月度调仓
  - 防守(25-40%): 15只，PB10%，月度调仓
  - 底部(15-25%): 10只，PB5%(优中选优)，双月调仓
  - 极端(<15%): 5只，PB5%，双月调仓
- 当前建议：宽度38.5%，建议满仓20只

### 06 候选组合质量监控

- 状态：**✅ 已完成**
- 结果文件：`result_06_rfscore_candidate_quality_monitor.md`
- 一句话结论：**当前组合质量评分70/100（等级B），估值合理但候选仅4只、ROA偏低1.26%、钢铁占比50%，建议放宽至PB20%或降低持仓至5-10只**
- 是否进入正式版本：**✅ 监控体系进入正式版本** - 质量评分模型和预警规则已确立
- 当前组合体检：
  - 候选数量：4只（⚠️ 过少，理想10-20只）
  - 质量评分：70/100（B级-良好）
  - 估值水平：PB均值0.998，PE均值17.56（✅ 合理）
  - 盈利质量：ROA均值1.26%（⚠️ 偏低）
  - 行业分布：钢铁50%、传媒25%、交通运输25%（⚠️ 过于集中）
  - 异常股：无明显异常（✅）
- 触发预警：
  - 🟡 B01: 候选不足（count=4 < 10）
  - 🟡 B03: 盈利偏弱（ROA=1.26% < 1.5%）
  - 🟡 B04: 行业集中（钢铁=50% > 40%）
- 建议措施：
  - 短期：放宽至PB20%扩容候选池，或降低目标持仓至5-10只
  - 中期：引入行业分散度硬性约束（单行业上限30%）
  - 长期：建立自适应PB阈值算法和自动化质量监控

### 07 RFScore + 红利小盘完整回测

- 状态：✅ 已完成
- 结果文件：`result_07_rfscore_dividend_smallcap_full_backtest.md`
- 一句话结论：**60/40 静态权重组合表现最优，年化收益13.84%，最大回撤-14.21%，夏普0.78，建议替代30-40% ETF观察仓**
- 是否进入正式版本：✅ **是，60/40版本确立为唯一推荐**
- 策略代码：
  - `strategies/combo_rfscore_dividend_60_40.py` (推荐)
  - `strategies/combo_rfscore_dividend_70_30.py` (进攻)
  - `strategies/combo_rfscore_dividend_50_50.py` (防守)
  - `strategies/combo_rfscore_dividend_dynamic.py` (动态)
- 当前建议：**市场弱势(宽度0.230)，建议按弱势防守配置：RFScore 30% + 红利小盘 30% = 总仓位60%**

### 08 RFScore + 防守底仓完整回测

- 状态：**✅ 已完成**
- 结果文件：`result_08_rfscore_defensive_base_full_backtest.md`
- 一句话结论：**国债固收+是最佳防守底仓（年化6.15%，回撤1.64%，夏普0.85），优于纯国债和纯现金防守，红利小盘可作为防守卫星补充10-15%**
- 是否进入正式版本：✅ **是，国债固收+确认为防守底仓首选**
- 关键配置：
  - 国债固收+：75%国债+10%黄金+8%红利+4%纳指
  - 推荐组合：RFScore 40-50% + 国债固收+ 30-40% + 红利小盘 10-15% + 现金 10-20%
- 实证回测（2022-01-01至2025-03-28）：
  - RFScore+防守底仓组合：年化3.56%，回撤11.83%，夏普-0.04
  - 纯国债防守：年化3.28%，回撤1.54%，夏普-0.43
  - 国债固收+：年化6.15%，回撤1.64%，夏普0.85 ⭐
  - 纯RFScore进攻：年化1.52%，回撤23.81%，夏普-0.13
- 最终结论：**国债固收+性价比最优，红利小盘可作为防守卫星（股票防守方向）**

### 09 容量、成本与执行仿真

- 状态：✅ 已完成
- 结果文件：`result_09_rfscore_capacity_and_execution.md`
- 一句话结论：**RFScore7 PB10%建议仓位上限30-40%（保守建议20-25%），成本敏感度9.0%优秀，但压力测试数据存在异常需修正**
- 是否进入正式版本：✅ **有条件进入** - 需修正数据异常、实施硬过滤条件
- 数据异常：成交额统计口径、市值范围、PE>100候选股等5项异常需修正

### 10 行业偏置与隐藏暴露

- 状态：✅ 已完成
- 结果文件：`result_10_rfscore_sector_and_hidden_exposure.md`
- 一句话结论：**PB10筛选过于严格导致候选极度稀疏（66.7%月份无候选），策略暴露于钢铁(43%)、房地产(14%)等强周期行业，建议扩大至PB20%或设置单行业上限30%**
- 是否进入正式版本：**✅ 有条件进入** - 需解决候选稀疏问题
- 隐藏暴露识别：
  - **周期暴露**：钢铁+房地产合计57%，强周期行业占比过高
  - **央国企特征**：100%候选为央国企，平均市值900亿+
  - **银行缺失**：质量门槛过滤了银行（ROA普遍<1%）
- 当前候选（2026-03-27）：仅1只（宝钢股份，钢铁行业），无法分散风险
- 行动建议：
  - 🔴 **推荐**：扩大PB范围至20%（参考报告#11，年化仍达15.03%）
  - 🟡 **备选**：保持PB10%但设置单行业上限30%
  - 🟡 **备选**：放宽质量门槛至RFScore6，纳入银行分散风险

## 最终总括

- 当前第三轮总状态：已完成（01✅ 02✅ 03✅ 04✅ 05✅ 06✅ 07✅ 08✅ 09✅ 10✅）
- 当前最接近正式版的 RFScore 方案：**PB10% 主线 + PB20% 备用池（`rfscore7_pb10_final.py`）**
- 当前推荐的防守搭配：**RFScore PB10 + 国债固收+ 30-40% + 红利小盘 10-15%（卫星配置）**
- 当前最大未解决问题：候选股异常过滤机制尚未加入正式策略
- 元审查总结：见 `99_round3_meta_review_2026-03-28.md`
- 唯一正式版参数表：见 `100_rfscore_pb10_official_release_v1.md`
- 2026-03-29 review 结论：见 `101_rfscore_review_2026-03-29.md`

### 关键结论

1. **口径已对齐**: 所有脚本统一使用 PB10%（primary_pb_group = 1）
2. **异常已识别**: PE>100、ROE<2% 等异常值需要过滤规则
3. **建议过滤条件**: PE < 100 + ROA > 0.5% 硬过滤
4. **备用池已确认**: PB10+PB20 两层架构，15只持仓，不用 Score≥6 补位
5. **过滤器终审完成**:
   - ✅ **Industry Cap（必选）**: 每行业最多5只，防止行业集中风险
   - ✅ **Turnover Filter（可选）**: 剔除高换手前20%，回避投机炒作
   - ✅ **CGO Filter（可选）**: 建议震荡市启用，回避获利了结压力
   - ❌ **Combined Filter（淘汰）**: 双重过滤过度复杂，增加稀疏性风险
6. **质量监控体系**:
   - **评分模型**: 0-100分，A/B/C/D四级，当前70分(B级)
   - **预警规则**: 三级预警(🔴严重/🟡中度/🟢轻度)，当前触发3条中度预警
   - **核心指标**: 估值(PB/PE)、盈利(ROA/OCF)、分散(行业/数量)、异常股检测
   - **当前问题**: 候选仅4只(过少)、ROA 1.26%(偏低)、钢铁占比50%(集中)
