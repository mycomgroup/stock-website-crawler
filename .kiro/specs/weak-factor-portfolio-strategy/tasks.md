# Tasks: 弱因子组合量化策略 v2

## Phase 1：生产主线（L0-L4 + L7 简化版）

### 1. 数据治理层（L0）

- [x] 1.1 实现 `pit_panel.py`：加载 `train_merged_all.csv`，重命名 `Unnamed: 0` 为 `stock_id`，解析日期，按 `[date, stock_id]` 排序
- [x] 1.2 实现可交易掩码 `compute_tradable_mask()`：过滤 ST/*ST、停牌、涨跌停一字板、新股冷启动（< 60交易日）、退市整理
- [x] 1.3 实现财务因子时滞校验（若有披露日字段则按实际披露日生效，否则记录缺失）
- [x] 1.4 实现存活偏差检查 `check_survivorship_bias()`：验证退市股票是否被正确处理，退市前最后收益是否纳入，提供对比报告（对应需求14、技术方案18.7节）
- [x] 1.5 编写 PBT 测试 P1：随机打乱未来标签后验证 OOF IC 接近 0（|IC| < 0.005）

### 2. 因子预处理层（L1）

- [x] 2.1 实现 `winsorize_cross_section()`：按日截面执行 `median ± 5 * MAD` robust winsor（禁止全局 clip）
- [x] 2.2 实现 `impute_factors()`：财务类因子用行业内中位数填补，微观结构类用前推，缺失率 > 30% 的因子降权
- [x] 2.3 实现双轨标准化：rank 表示（`rank(x)/(N+1) - 0.5`）和 robust zscore（`(x - median) / (MAD + eps)`）
- [ ] 2.4 实现风格中性化 `neutralize_factors()`（对应需求16、技术方案6.5节）：
  - 对每个因子单独回归，右侧使用**同一组联合风险暴露**（禁止逐步回归，避免路径依赖）
  - 暴露集合：行业哑变量（K-1+截距，全框架统一）+ `ln(float_mcap)` + `beta` + `residual_vol` + `liquidity`
  - WLS 权重：`sqrt(float_mcap)` clip 后
  - 样本极少行业（< 10 个样本）：使用行业合并或 ridge 回归，避免矩阵近奇异
  - rolling beta / residual_vol 的估计窗口必须严格因果（只使用 `date < t` 的数据）
- [x] 2.5 编写 PBT 测试 P2-P4：标准化幂等性、去极值有界性、中性化残差正交性（|corr| < 0.05）

### 3. 因子家族划分（L2）

- [x] 3.1 实现 `family_map.py`：冻结 9 个经济家族与 CSV 列的完整映射（**注意正确数量：basics=37，quality=71**，合计 260）
- [x] 3.2 实现有效维度计算 `compute_effective_dimension()`：`n_eff = (Σλ_j)² / Σλ_j²`
- [x] 3.3 实现组内冗余检测：识别截面相关性长期 > 0.8 的因子对，标记为冗余候选
- [x] 3.4 实现因子准入/淘汰三段式流程：shadow_pool → 观察期（快衰减6~12月/中速12~18月/慢速18~24月）→ 正式纳入/淘汰（连续4~6个窗口增量贡献为负则淘汰）
- [x] 3.5 编写 PBT 测试 P5：家族完备性（`union(families) == set(all_factors)`，无重叠，无遗漏）

### 4. OOF Walk-Forward 框架

- [x] 4.1 实现 `WalkForwardSplitter`：outer loop（最小训练期 260 周，test block 52 周，步长 4 周，embargo 1 周）
- [x] 4.2 实现 `InnerLoopTuner`：在 outer-train 内部做超参数选择（validation block 13 周），慢因子用 expanding window，快衰减因子用 rolling window
- [x] 4.3 实现超参数稳定化：指数平滑（`θ_t = f(θ_t*, θ_{t-1}, ...)`），禁止使用未来窗口信息
- [x] 4.4 实现 OOF 预测构造器：确保每个 `(date, stock)` 样本恰好有一个 OOF 预测，含 purge/embargo（`embargo >= max(label_horizon, execution_delay, feature_publication_lag)`）
- [x] 4.5 实现 final holdout 分区：最后 52~104 周冻结，研究阶段不可访问，记录访问次数
- [x] 4.6 编写 PBT 测试 P6：OOF 无泄漏验证（预测值仅依赖 `date < t - embargo` 的数据）

### 5. 组内合成（L3）

- [x] 5.1 实现 `equal_rank_score()`：家族内 rank 等权平均（稳健基线）
- [x] 5.2 实现 `ridge_family_score()`：rolling ridge 预测下期残差收益（OOF）
- [x] 5.3 实现 `pc1_score_with_sign_anchor()`：PC1 分数，含符号锚定（与上期相关性为负时自动翻号，首窗口以等权基线为方向锚）和失稳处理（第一/第二特征值比值 < 1.5 或跨期相关性 < 0.7 时降权，回退到 equal-rank + ridge）
- [x] 5.4 实现 `stack_family_scores_oof()`：非负 ridge 叠加三类子分数，权重由 OOF 决定（禁止使用样本内拟合值）

### 6. 组间收缩合成——主模型（L4）

- [x] 6.1 实现 `CrossFamilyModel`：rolling ridge / elastic net，输入必须是 OOF 家族分数矩阵（禁止样本内拟合值）
- [x] 6.2 实现超参数网格搜索：`alpha_reg ∈ [0.001, 0.01, 0.1, 1.0, 10.0]`，`l1_ratio ∈ [0.0, 0.1, 0.5]`（0.0=纯ridge）
- [x] 6.3 实现权重约束：单家族上限 0.4，指数平滑（半衰期 4 个再平衡周期），轻度允许负权，不建议让权重频繁翻正翻负
- [x] 6.4 实现 `predict_alpha_linear()`：`alpha_linear[t,i] = Σ_g β_{t,g} · s_g[t,i]`

### 7. 简化组合优化器（L7 Phase 1）

- [x] 7.1 实现 `TopNEqualWeightOptimizer`：过滤不可交易 → 按 alpha 排序取 top-N → 等权分配 → 应用单票上限（3%）
- [x] 7.2 实现换手约束：相邻再平衡日换手率 ≤ 30%
- [x] 7.3 实现不可交易冻结：停牌/涨跌停股票权重保持不变（`w_i = w_prev_i`）
- [x] 7.4 编写 PBT 测试 P7-P8：权重合法性（`Σw=1, 0≤w_i≤0.03, 不可交易冻结`）、换手有界性

### 8. 完整 Pipeline 集成

- [x] 8.1 实现 `WeakFactorPipelineV2`：串联 L0→L1→L2→L3→L4→L7，确保严格串行因果链（组内模型→组间线性模型→残差overlay，不能随意并行）
- [x] 8.2 实现结果落盘：OOF 预测、inner loop 结果、outer loop 结果分别保存
- [x] 8.3 实现参数快照：每次运行保存参数配置、数据版本和随机种子，确保完全可复现
- [x] 8.4 在 `train_merged_all.csv` 上运行完整 Phase 1 pipeline，验证 OOF rank IC > 0.03

### 9. Phase 1 评估与验收

- [x] 9.1 实现因子层评估：rank IC、ICIR、单调分组收益
- [x] 9.2 实现合成层评估：OOF rank IC、decile spread、家族权重稳定性
- [x] 9.3 实现组合层评估：税费后 Sharpe/IR、最大回撤、月度胜率、换手率
- [x] 9.4 实现稳健性测试：删掉最强10%因子后的 OOF IC 衰减测试（P9：`IC(top_90%) / IC(all) > 0.80`）
- [x] 9.5 实现延迟执行测试：延迟1天后的 Sharpe 衰减测试（P10：`Sharpe(delay=1) / Sharpe(delay=0) > 0.85`）
- [x] 9.6 验证6项上线闸门全部通过（税费后成立、延迟执行成立、容量不过度衰减、风险暴露可控、参数扰动不脆弱、final holdout 不弱于 research OOS）

---

## Phase 2：研究增强（L5 + L6 + L7 完整版 + Freshness + Data Snooping）

- [x] 10.1 实现 `ResidualGBDTOverlay`（L5）：GBDT 拟合线性主模型残差，eta 通过 inner loop 从 `[0, 0.05, 0.10, 0.20, 0.30]` 选择，eta=0 必须永远保留为合法选项
- [x] 10.2 实现 L5 准入条件检查：OOF 成本后 IR 提升 > 5%，bootstrap 置信区间支持增益为正（block-bootstrap p < 0.1），换手增幅 < 20%
- [x] 10.3 实现 `SoftRegimeOverlay`（L6）：单一全局调节系数，先压缩 regime 指标为 1~2 个状态变量，再用低自由度映射（`adj_t = clip(a + b·z, 0.9, 1.1)`），参数在 inner loop 中选择
- [x] 10.4 实现 `QPOptimizer`（L7 完整版）：cvxpy + OSQP 二次规划，目标函数含风险惩罚（`λ_risk·w'Σw`）+ L1/L2 换手成本 + HHI 集中度惩罚，约束含行业偏离 ≤ 5%、风格偏离、流动性参与率
- [x] 10.5 实现 `FreshnessDecayModule`：计算 `c_{g,t} = exp(-age_{g,t} / tau_g)`，作为 stack 输入特征或置信度权重（禁止直接乘到因子值），通过 inner loop 比较有无 freshness 处理（对应需求13、技术方案5.5节）
- [x] 10.6 实现 block-bootstrap 统计检验模块：对 OOF IC 做显著性检验
- [x] 10.7 实现 data snooping 防控：multiple testing 调整（BH 校正），在模型家族选择和最终候选模型比较两个节点执行（对应需求15、技术方案17.5节）
- [x] 10.8 实现容量评估模块：资金规模放大10x后的 alpha 衰减测试
- [x] 10.9 实现 `HorizonCalibrationModule`：native horizon → decision horizon 校准（isotonic regression / 分桶校准 / 线性校准），在 fit_pipeline 中作为第3步（对应需求17、技术方案5.4节和21节伪代码）

---

## Phase 3：结构升级（研究线）

- [x] 11.1 实现 IPCA / latent factor 模型（研究增强线）
- [x] 11.2 实现多 horizon sleeve 管理：按因子衰减速度分类（快/中/慢），native horizon → decision horizon 校准（依赖 10.9）
- [x] 11.3 实现 alpha-risk 联合估计
- [x] 11.4 实现多目标优化器
- [x] 11.5 实现 Bayesian shrinkage 作为 L4 可选增强（非默认，替代 elastic net）
- [x] 11.6 实现 PCA/whitened 空间下的 covariance-aware shrinkage（L4 可选增强，非默认）

---

## 技术债务清理（v1 → v2 迁移）

- [x] 12.1 废弃 `combine_signals_fixed()` 固定 40/30/30 融合
- [x] 12.2 废弃 `get_active_factors()` IC top-k 激活机制（替换为收缩法自然降权）
- [x] 12.3 废弃 `strategy_risk_parity()` 作为主方案（因子波动率倒数加权理论弱）
- [x] 12.4 废弃 `apply_stop_loss()` 因子层止损（止损属于组合层应急开关）
- [x] 12.5 废弃 `market_phases` 手工划分牛熊硬切换（替换为 soft regime overlay）
- [x] 12.6 废弃 `strategy_ml_weighted()` ML 作为主模型（降级为 residual overlay）
- [x] 12.7 改造 `standardize_factors()` 为 L1 预处理子步骤（增加 robust winsor 和联合中性化）
- [x] 12.8 改造 `strategy_equal_weighted()` 为 L3 组内合成的 `s_eq_g` 基线分数
- [x] 12.9 修正因子家族数量映射：basics=37（非36），quality=71（非67）
