# 低频高胜率方向：当前进度 + 5个子任务执行计划

> 更新时间：2026-04-23
> 主题范围：仅保留低频高胜率方向

---

## 一、目前研究推进到哪一步（状态结论）

当前状态不是“从0开始”，而是已经完成了**研究收口前的证据汇总阶段**，具体处于：

- 已完成总纲与优先级排序（主仓动态路由、RSRS过滤、ML低频多因子、RFScore增强、低频ETF宏观映射）。
- 已完成 follow-up 结果归档（含主仓动态路由V1规格、RSRS增量验证、ML基线复核、FFScore增量验证、ETF宏观白名单映射等）。
- 已形成“哪些方向继续、哪些方向暂停”的明确结论。

一句话：

**这个方向已经从“方向探索期”进入“工程化验证与投产前收口期”。**

---

## 二、缺口在哪里（为什么还要做5个子任务）

现有材料强在“结论多”，弱在“可执行闭环”。

还缺的不是新的灵感，而是：

1. 统一主仓底座口径（避免不同文档/脚本口径漂移）。
2. RSRS作为过滤器的上线级接口定义（不是研究型结论）。
3. RFScore增强因子的明确白名单/黑名单（防止继续发散）。
4. 低频ETF/宏观原型的落地映射（哪些真进入主账户结构）。
5. 统一验收标准（每条线达到什么指标才允许进入下一阶段）。

---

## 三、接下来 5 个子任务（按顺序执行）

## 子任务1：主仓底座统一与冻结（P0）

**目标**：把当前主仓候选口径冻结成唯一版本，作为后续所有增量测试基线。

**输入**：
- `core_archive/low_freq_high_winrate_strategy_20260403/00_总纲_低频高胜率策略研究.md`
- `core_archive/low_freq_high_winrate_strategy_20260403/results_followup_20260403/result_01_主仓底座现状对齐与冲突表.md`
- `core_archive/low_freq_high_winrate_strategy_20260403/results_followup_20260403/result_02_状态输入统一与阈值冻结.md`

**产出**：
- 《主仓底座冻结卡 v1》（1页）
- 固定：资产池、调仓频率、状态输入、仓位上限、回退规则

**验收标准**：
- 任意后续子任务调用同一套基线参数；
- 不再出现“同名策略不同参数”的情况。

---

## 子任务2：主仓动态路由V1工程化验收（P0）

**目标**：把“主仓动态路由V1规格书”转成可直接实现与可直接验证的工程任务卡。

**输入**：
- `core_archive/low_freq_high_winrate_strategy_20260403/results_followup_20260403/result_04_主仓动态路由V1规格书.md`
- `core_archive/low_freq_high_winrate_strategy_20260403/results_followup_20260403/verify_dynamic_router_v1_logic_report.md`

**产出**：
- 《动态路由V1接口定义清单》
- 《动态路由V1验收测试清单》（状态切换、回退、异常处理）

**验收标准**：
- 状态切换与仓位映射有唯一规则；
- 可对照历史样本做“规则一致性回放”。

---

## 子任务3：RSRS过滤层收口（P1）

**目标**：确认 RSRS 在本主题内的定位仅为“过滤器/确认器”，并完成最小可上线版本。

**输入**：
- `core_archive/low_freq_high_winrate_strategy_20260403/results_followup_20260403/result_05_RSRS改进版本候选筛选.md`
- `core_archive/low_freq_high_winrate_strategy_20260403/results_followup_20260403/result_06_RSRS复合过滤增量验证.md`
- `core_archive/low_freq_high_winrate_strategy_20260403/results_followup_20260403/result_07_RSRS模块挂接规则与接口定义.md`

**产出**：
- 《RSRS过滤器最小生产版规则》
- 《RSRS与宽度/情绪冲突优先级表》

**验收标准**：
- 明确 No-Go 情况（何时不启用RSRS）；
- 明确只做过滤，不扩展成独立择时主策略。

---

## 子任务4：RFScore增强因子白名单化（P1）

**目标**：把“可继续验证”与“应暂停”的增强因子一次性写清，防止继续开新坑。

**输入**：
- `core_archive/low_freq_high_winrate_strategy_20260403/results_followup_20260403/result_11_FFScore对RFScore增量验证.md`
- `core_archive/low_freq_high_winrate_strategy_20260403/results_followup_20260403/result_12_筹码_STR_行业量价预筛白名单.md`
- `reference_strategies_from_jk2bt/` 下 FFScore/宏观/行业量价相关源策略

**产出**：
- 《RFScore增强白名单v1》：仅保留 1-2 个继续验证方向
- 《RFScore增强黑名单v1》：明确暂停项和暂停理由

**验收标准**：
- 每个候选都有“是否继续”的单句结论；
- 不保留“模糊观察中”状态超过两周。

---

## 子任务5：低频ETF/宏观慢变量并入主账户结构（P2）

**目标**：把低频ETF和宏观慢变量从“参考原型”变成“主账户结构中的明确角色”。

**输入**：
- `core_archive/low_freq_high_winrate_strategy_20260403/results_followup_20260403/result_10_静态60_40与聚宽低频原型映射总表.md`
- `core_archive/low_freq_high_winrate_strategy_20260403/results_followup_20260403/result_13_低频ETF宏观原型映射与白名单.md`
- `reference_strategies_from_jk2bt/18*.txt`
- `reference_strategies_from_jk2bt/21*.txt`
- `reference_strategies_from_jk2bt/48*.txt`

**产出**：
- 《主账户三层结构图 v1》（进攻层/防守层/现金缓冲层）
- 《低频ETF+宏观触发清单》

**验收标准**：
- 每个原型都归类为：主仓底座/过滤器/仓位器/仅参考；
- 不再出现“策略很好但不知道放在账户哪里”的情况。

---

## 四、执行节奏建议（10个工作日）

- Day 1-2：子任务1
- Day 3-4：子任务2
- Day 5-6：子任务3
- Day 7-8：子任务4
- Day 9-10：子任务5 + 总验收

---

## 五、总验收口径（统一）

每个子任务结束都用同一模板给出：

1. 结论：Go / No-Go / Watch
2. 与主仓关系：底座 / 过滤器 / 仓位器 / 观察线
3. 是否进入下一阶段：是/否
4. 阻塞项：仅允许列 1-3 条，可执行

