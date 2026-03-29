# RFScore PB10 唯一正式版参数表 + 代码改造清单

## 目的

这份文档把第三轮研究结果收敛成一个**唯一正式版**，用于上线前封版。

从本文件开始，不再并列保留多套主规则。没有被写进这份文档的配置，默认都**不进入 V1 正式版**。

## 一、正式版定义

- 正式版名称：`RFScore7 PB10 Release V1`
- 正式版主文件：`/Users/fengzhi/Downloads/git/testlixingren/strategies/rfscore7_pb10_final.py`
- 生效原则：以本文件为唯一参数口径，代码必须向本文件对齐

## 二、唯一正式版参数表

### 2.1 基础执行参数

| 模块 | 参数 | 正式值 | 说明 |
|------|------|--------|------|
| 基准 | `benchmark` | `000300.XSHG` | 保持不变 |
| 股票池 | `universe` | `沪深300 ∪ 中证500` | 即 `000300` + `000905` |
| 板块过滤 | `exclude_prefix` | `688` | 排除科创板 |
| 新股过滤 | `ipo_days` | `180` | 上市不足 180 天不参与 |
| ST过滤 | `exclude_st` | `true` | 保持不变 |
| 停牌过滤 | `exclude_paused` | `true` | 保持不变 |
| 调仓频率 | `rebalance` | 每月第一个交易日 `09:35` | 保持不变 |
| 实时价格 | `use_real_price` | `true` | 保持不变 |
| 防未来函数 | `avoid_future_data` | `true` | 保持不变 |
| 交易成本 | `open_commission` | `0.0003` | 保持不变 |
| 交易成本 | `close_commission` | `0.0003` | 保持不变 |
| 印花税 | `close_tax` | `0.001` | 保持不变 |

### 2.2 因子与选股参数

| 模块 | 参数 | 正式值 | 说明 |
|------|------|--------|------|
| 因子 | `RFScore` | 7 因子打分 | 保持当前定义 |
| 主池门槛 | `primary_score` | `RFScore == 7` | 不降级 |
| 主池估值 | `primary_pb_group` | `1` | PB 最低 10% |
| 次级池门槛 | `secondary_score` | `RFScore == 7` | 不允许 `>=6` |
| 次级池估值 | `secondary_pb_group` | `2` | 仅 PB 10%-20% |
| 排序键1 | `sort_1` | `RFScore desc` | 保持不变 |
| 排序键2 | `sort_2` | `ROA desc` | 保持不变 |
| 排序键3 | `sort_3` | `OCFOA desc` | 保持不变 |
| 排序键4 | `sort_4` | `DELTA_MARGIN desc` | 保持不变 |
| 排序键5 | `sort_5` | `DELTA_TURN desc` | 保持不变 |
| 排序键6 | `sort_6` | `pb_ratio asc` | 保持不变 |

### 2.3 硬过滤参数

| 模块 | 参数 | 正式值 | 说明 |
|------|------|--------|------|
| 估值过滤 | `pb_ratio` | `> 0` | 去掉无效 PB |
| 估值过滤 | `pe_ratio` | `> 0 and < 100` | 去掉极端异常值 |
| 盈利过滤 | `ROA` | `> 0.5` | 吸收第三轮异常审计结论 |
| 缺失值过滤 | `required_fields` | `RFScore/ROA/OCFOA/pb_ratio/pe_ratio` 非空 | 保证排序和风控有效 |
| 回补规则 | `fallback` | `禁用` | 不再用泛化 fallback 补仓 |
| 降级规则 | `score_relax` | `禁用` | 不允许降到 `RFScore >= 6` |

### 2.4 行业风险约束

| 模块 | 参数 | 正式值 | 说明 |
|------|------|--------|------|
| 行业分类 | `industry_level` | 申万一级 | 用于行业约束和监控 |
| 行业上限 | `industry_cap_ratio` | `0.30` | 单行业最多占目标持仓 30% |
| 落地方式 | `industry_cap_count` | `floor(target_hold_num * 0.30)`，最少 1 只 | 15只=4只，12只=3只，10只=3只 |
| 候选不足处理 | `insufficient_after_cap` | 留现金 | 不为满仓破坏行业约束 |

### 2.5 市场状态与持仓参数

| 模块 | 参数 | 正式值 | 说明 |
|------|------|--------|------|
| 宽度定义 | `breadth` | `沪深300成分股中 close > MA20 的比例` | 统一唯一口径 |
| 趋势定义 | `trend_on` | `沪深300指数 close > MA20` | 统一唯一口径 |
| 正常持仓 | `hold_num_normal` | `15` | 主结论来自任务03 |
| 轻度减仓 | `hold_num_mid` | `12` | 主结论来自任务03 |
| 明显减仓 | `hold_num_weak` | `10` | 主结论来自任务03 |
| 空仓 | `hold_num_stop` | `0` | 极端市场允许空仓 |
| 阈值1 | `breadth_normal` | `0.35` | `>=0.35` 直接正常持仓 |
| 阈值2 | `breadth_reduce` | `0.25` | `0.25-0.35` 结合趋势判断 |
| 阈值3 | `breadth_stop` | `0.15` | `<0.15` 直接空仓 |

### 2.6 持仓决策函数

| 条件 | 正式动作 |
|------|----------|
| `breadth < 0.15` | 目标持仓 `0` |
| `0.15 <= breadth < 0.25` | 目标持仓 `10` |
| `0.25 <= breadth < 0.35 and trend_on == false` | 目标持仓 `12` |
| 其他情况 | 目标持仓 `15` |

### 2.7 组合层配置建议

这部分不是单策略内部逻辑，而是上线时的外部组合配置建议：

| 模块 | 参数 | 正式值 | 说明 |
|------|------|--------|------|
| 策略仓位目标 | `strategy_sleeve_target` | `25%` | 当前环境下保守上线值 |
| 策略仓位硬上限 | `strategy_sleeve_hard_cap` | `35%` | 在容量数据修正前不超过此值 |
| 未用资金 | `cash_policy` | 现金保留 | 候选不足时不强行迁移到别的风格 |

## 三、明确不进入 V1 的配置

下面这些内容不是“否定”，而是**延后到 V1.1 或后续版本**：

| 项目 | 处理 |
|------|------|
| Turnover Filter | 不进 V1 |
| CGO Filter | 不进 V1 |
| Combined Filter | 明确淘汰 |
| `PB5%` 极端收紧模式 | 不进 V1 |
| `RFScore >= 6` 补位 | 明确淘汰 |
| 泛化 fallback 补位 | 明确淘汰 |
| 自动容量联动仓位 | 不进 V1 |
| 与红利小盘/固收+做单文件混合 | 不进 V1 主策略文件 |

## 四、Review 后新增的正式升级点

这次对 backtest txt、notebook、监控脚本做完整体 review 后，没有发现足以替换主线的新 alpha 逻辑，但确认了一个必须升级的事项：

### 升级点 1：统一口径从“建议”升级为“上线阻断项”

当前仓库里的候选验证、质量监控、行业分析脚本，仍有一部分在使用：

- `PB20` 口径
- `pb_group <= 2` 的泛候选口径
- 未加入 `PE < 100` / `ROA > 0.5` 的硬过滤
- 未加入和正式策略一致的 `buyable` 过滤（涨跌停/实际可买性）

这会导致一个非常危险的问题：

- **研究看到的候选股**
- **监控看到的候选股**
- **正式策略真正会买的候选股**

三者可能不是同一批股票。

因此，V1 正式版新增一条规则：

> **所有用于“当前候选”“质量监控”“行业暴露”“上线核对”的工具脚本，都必须与正式策略使用同一套选股口径和可买性过滤。**

这条要求现在视为 **P0**，不再是可选优化。

## 五、代码改造清单

### 4.1 P0 阻断项

这些不改完，不建议上线。

#### 文件：`/Users/fengzhi/Downloads/git/testlixingren/strategies/rfscore7_pb10_final.py`

1. `initialize()` 参数改造
   - 把 [rfscore7_pb10_final.py](/Users/fengzhi/Downloads/git/testlixingren/strategies/rfscore7_pb10_final.py#L108) 到 [rfscore7_pb10_final.py](/Users/fengzhi/Downloads/git/testlixingren/strategies/rfscore7_pb10_final.py#L115) 的 `20/10/0.25/0.15` 双档参数，改成正式版四档参数：
   - `g.hold_num_normal = 15`
   - `g.hold_num_mid = 12`
   - `g.hold_num_weak = 10`
   - `g.hold_num_stop = 0`
   - `g.breadth_normal = 0.35`
   - `g.breadth_reduce = 0.25`
   - `g.breadth_stop = 0.15`
   - 新增：
   - `g.max_pe_ratio = 100`
   - `g.min_roa = 0.5`
   - `g.industry_cap_ratio = 0.30`

2. `calc_rfscore_table()` 增加硬过滤
   - 在 [rfscore7_pb10_final.py](/Users/fengzhi/Downloads/git/testlixingren/strategies/rfscore7_pb10_final.py#L165) 到 [rfscore7_pb10_final.py](/Users/fengzhi/Downloads/git/testlixingren/strategies/rfscore7_pb10_final.py#L190)：
   - 保留现有估值拼接逻辑
   - 追加硬过滤：
   - `pb_ratio > 0`
   - `pe_ratio > 0`
   - `pe_ratio < g.max_pe_ratio`
   - `ROA > g.min_roa`
   - 明确 dropna 字段为：`RFScore/ROA/OCFOA/pb_ratio/pe_ratio`

3. `choose_stocks()` 重写为“两层池 + 留现金”
   - 在 [rfscore7_pb10_final.py](/Users/fengzhi/Downloads/git/testlixingren/strategies/rfscore7_pb10_final.py#L193) 到 [rfscore7_pb10_final.py](/Users/fengzhi/Downloads/git/testlixingren/strategies/rfscore7_pb10_final.py#L229)：
   - 主池改为：`RFScore == 7 and pb_group == 1`
   - 次级池改为：`RFScore == 7 and pb_group == 2`
   - 删除：
   - `RFScore >= 6` 补位
   - fallback 全表补位
   - 候选不足时直接返回实际数量，剩余仓位留现金
   - 加入行业上限约束：按申万一级行业控制最大入选数量
   - 返回值增加元信息：
   - `primary_count`
   - `secondary_count`
   - `actual_count`
   - `industry_summary`

4. `rebalance()` 改成四档持仓决策
   - 在 [rfscore7_pb10_final.py](/Users/fengzhi/Downloads/git/testlixingren/strategies/rfscore7_pb10_final.py#L255) 到 [rfscore7_pb10_final.py](/Users/fengzhi/Downloads/git/testlixingren/strategies/rfscore7_pb10_final.py#L300)：
   - 用正式版规则替换当前 `20/10/0` 双档规则
   - `breadth < 0.15` 直接空仓，不再附加 `trend_on == false` 条件
   - `0.15-0.25` 使用 `10` 只
   - `0.25-0.35` 且趋势走弱使用 `12` 只
   - 其他情况使用 `15` 只
   - 当实际可买股票少于目标值时，只买实际数量，其余留现金

5. `record_market_state()` 增加上线监控字段
   - 在 [rfscore7_pb10_final.py](/Users/fengzhi/Downloads/git/testlixingren/strategies/rfscore7_pb10_final.py#L303) 到 [rfscore7_pb10_final.py](/Users/fengzhi/Downloads/git/testlixingren/strategies/rfscore7_pb10_final.py#L310)：
   - 新增记录：
   - `trend_on`
   - `target_hold_num`
   - `actual_hold_num`
   - `primary_count`
   - `secondary_count`
   - `cash_ratio`
   - `max_industry_ratio`

6. 抽出统一选股核心
   - 建议新增一个共享函数层，避免正式策略和 notebook 工具各写一套：
   - `build_candidate_frame()`
   - `select_release_v1_candidates()`
   - `filter_buyable()`
   - `get_target_hold_num()`
   - 目标不是“更复杂”，而是保证生产、验证、监控三端完全同构

#### 文件：`/Users/fengzhi/Downloads/git/testlixingren/docs/research_archive_20260329/skills_joinquant_nookbook/validate-rfscore-candidates.js`

- 从 P1 提升为 **P0**
- 该脚本不能再只打印“PB10/PB20 大盘点”，而要能输出：
- 正式版主池候选
- 正式版次级池候选
- 通过硬过滤后的候选
- 通过 `buyable` 过滤后的最终可买候选
- 行业上限裁剪后的最终候选

#### 文件：`/Users/fengzhi/Downloads/git/testlixingren/docs/research_archive_20260329/skills_joinquant_nookbook/rfscore_quality_monitor.py`

- 从 P1 提升为 **P0**
- 候选获取逻辑必须从：
- `RFScore >= 7 and pb_group <= 2`
- 升级为：
- 正式版 `PB10 主池 + PB20 次级池 + 硬过滤 + buyable 过滤 + 行业上限` 之后的结果
- 否则质量监控对象和真实持仓对象不是同一组

#### 文件：`/Users/fengzhi/Downloads/git/testlixingren/docs/research_archive_20260329/skills_joinquant_nookbook/rfscore_monitor_full.py`

- 新增为 **P0**
- 不能再使用 `RFScore >= 7 and pb_group <= 2` 作为“当前候选”的监控口径
- 必须改成正式版最终候选口径

#### 文件：`/Users/fengzhi/Downloads/git/testlixingren/docs/research_archive_20260329/skills_joinquant_nookbook/rfscore_sector_analysis.py`

- 新增为 **P0**
- 行业暴露分析应基于正式版最终候选，而不是“未经过硬过滤/可买性过滤”的宽口径 PB10 候选

### 5.2 P1 强烈建议项

#### 文件：`/Users/fengzhi/Downloads/git/testlixingren/docs/research_archive_20260329/skills_joinquant_nookbook/validate-rfscore-candidates.js`

- 为研究脚本增加 `mode`：
- `raw_pb10`
- `release_v1`
- `release_v1_buyable`
- 这样既保留研究视角，也不污染上线口径

#### 文件：`/Users/fengzhi/Downloads/git/testlixingren/docs/research_archive_20260329/skills_joinquant_nookbook/test_rfscore_backup_pool.py`

- 改成正式版校验脚本：
- 核心验证 `15 / 12 / 10 / 0`
- 验证次级池只允许 `pb_group == 2`
- 验证不再出现 `Score 6` 补位
- 验证候选不足时现金保留而非 fallback 补仓

#### 文件：`/Users/fengzhi/Downloads/git/testlixingren/docs/research_archive_20260329/skills_joinquant_nookbook/rfscore_quality_monitor.py`

- 监控规则对齐 V1：
- `count < 10` 警告
- `count < 3` 严重预警
- `avg_roa < 1.5` 警告
- `single_industry_ratio > 0.40` 警告

#### 文件：`/Users/fengzhi/Downloads/git/testlixingren/tmp/*.py`

- 所有临时 RFScore 研究脚本必须显式标注：
- `legacy_20_hold_experiment`
- 或 `release_v1_profile`
- 避免未来把 20 只持仓实验误读为正式版结论

### 5.3 P2 可延期项

- 把 `Turnover Filter` 和 `CGO Filter` 单独做成可插拔模块
- 重跑容量模型，把 `strategy_sleeve_hard_cap` 从 `35%` 再细化
- 输出单独的 `release dashboard`

## 六、上线前验收清单

### 5.1 必须全部通过

1. 当前正式策略不再出现 `RFScore 6` 股票
2. 当前正式策略不再使用 fallback 全表补仓
3. 当前正式策略候选不足时会保留现金
4. 当前正式策略可以跑出四档持仓：`15 / 12 / 10 / 0`
5. 候选快照工具与正式策略同日输出一致
6. 同日候选报告中，不再出现 `PE > 100` 或 `ROA <= 0.5`
7. 行业上限约束生效，单行业不超过目标持仓的 `30%`
8. 重新跑一版正式回测，回测文件明确标注 `Release V1`
9. `validate / quality_monitor / sector_analysis / monitor_full` 四类工具与正式策略同日候选集合一致
10. 工具输出已区分 `raw research candidates` 与 `release_v1 final candidates`

### 6.2 上线后首月监控

1. 每次调仓记录：
   - 市场宽度
   - 趋势状态
   - 目标持仓
   - 实际持仓
   - 主池数量
   - 次级池数量
   - 最大行业占比
2. 如果连续两次调仓候选数 `< 5`，进入人工复核
3. 如果单行业连续两次达到上限，进入人工复核

## 七、最小上线顺序

如果你要尽快上线，建议严格按这个顺序：

1. 先改 `strategies/rfscore7_pb10_final.py`
2. 抽出共享选股核心，供正式策略和 notebook 工具复用
3. 对齐 `validate-rfscore-candidates.js / rfscore_quality_monitor.py / rfscore_monitor_full.py / rfscore_sector_analysis.py`
4. 跑一次当前日期候选快照核对
5. 跑一次 `2022-01-01 ~ 2025-12-31` 正式回测
6. 生成 `Release V1` 候选报告和回测报告
7. 再上模拟盘/上线

## 八、一句话封版结论

**唯一正式版不是“PB10 原样继续跑”，而是“PB10 主池 + PB20 次级池 + RFScore7 不降级 + 15/12/10/0 四档持仓 + 硬过滤 + 行业上限 + 候选不足留现金”的收敛版本。**
