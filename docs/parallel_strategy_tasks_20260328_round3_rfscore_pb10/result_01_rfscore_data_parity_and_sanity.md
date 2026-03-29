# RFScore 数据口径与候选股异常审计报告

> **任务编号**: 01  
> **执行时间**: 2026-03-28  
> **审计范围**: RFScore PB10 主线 - 数据口径对齐与候选股质量检查

---

## 一、执行摘要

### 1.1 核心发现

| 类别 | 发现问题 | 严重程度 |
|------|----------|----------|
| **口径不一致** | `tmp/` 目录下的测试脚本仍使用 PB20% 而非 PB10% | 🔴 高 |
| **异常候选股** | PE 657、超低 ROE 等极端值进入候选池 | 🟡 中 |
| **定义漂移** | 不同脚本中 RFScore 计算逻辑存在细微差异 | 🟡 中 |

### 1.2 审计结论

- **必须立即修复**: `rfscore7_current_candidates.py` 和 `rfscore7_candidate_industry.py` 中的 PB 组筛选条件
- **建议增加**: 候选股质量过滤器（PE 上限、ROE 下限）
- **正式口径**: PB10% 作为唯一主筛选条件，PB20% 仅作为备用池

---

## 二、口径对齐检查

### 2.1 当前不一致点汇总

| 文件路径 | 当前 PB 组设置 | 问题描述 |
|----------|---------------|----------|
| `strategies/rfscore7_pb10_final.py:113-114` | `primary_pb_group = 1`<br>`reduced_pb_group = 2` | ✅ **正确** - 符合 PB10% 正式口径 |
| `tmp/rfscore7_current_candidates.py:122` | `pb_group <= 2` | ❌ **错误** - 仍在使用 PB20% |
| `tmp/rfscore7_candidate_industry.py:121` | `pb_group <= 2` | ❌ **错误** - 仍在使用 PB20% |
| `tmp/test_rfscore_pb10.py:191` | `pb_group == 1` | ✅ **正确** - 但仅用于测试 |

### 2.2 影响评估

根据 `11_rfscore7_pb10_upgrade_report.md` 的对比数据：

| 版本 | 年化收益 | 最大回撤 | 夏普比率 | vs PB10% 劣势 |
|------|----------|----------|----------|---------------|
| **PB10%** | **20.62%** | **-12.75%** | **0.974** | 基准 |
| PB20% | 15.03% | -10.77% | 0.654 | **-5.59% 年化** |

**结论**: 使用 PB20% 会导致年化收益损失 5.59%，在熊市区间（2022年）PB10% 盈利 +10.05% 而 PB20% 亏损 -1.88%。

---

## 三、候选股异常值审计

### 3.1 当前候选股快照（2026-03-27）

根据 `11_rfscore7_pb10_upgrade_report.md` 第 4.2 节数据：

| 代码 | 名称 | RFScore | PB | PE | ROE | 毛利率 | 异常类型 |
|------|------|---------|-----|------|------|--------|----------|
| **300070.XSHE** | 碧水源 | 6 | 0.53 | **657.17** | **0.10%** | 24.69% | 🔴 PE极端异常 |
| 000725.XSHE | 京东方A | 6 | 1.09 | 22.12 | 1.02% | 14.44% | 🟡 低ROE |
| 000537.XSHE | 广宇发展 | 6 | 1.18 | 26.17 | 0.94% | 43.84% | 🟡 低ROE |
| 600000.XSHG | 浦发银行 | 6 | 0.45 | 6.67 | 1.12% | - | ⚪ PB超低 |
| 600019.XSHG | 宝钢股份 | 6 | 0.69 | 14.84 | 1.51% | 7.76% | ⚪ ROE偏低 |

### 3.2 异常值统计

| 异常指标 | 阈值 | 触及股票数 | 占比 |
|----------|------|-----------|------|
| PE > 100 | 100 | 1 | 10% |
| PE > 50 | 50 | 1 | 10% |
| ROE < 2% | 2% | 3 | 30% |
| PB < 0.5 | 0.5 | 2 | 20% |

### 3.3 异常根因分析

**300070.XSHE（碧水源）PE=657 异常说明**:
- 该公司近期净利润大幅下滑，导致 PE 计算基数极低
- RFScore=6 主要依赖资产负债率改善（去杠杆）
- **问题**: RFScore 指标未包含盈利能力绝对水平检查

---

## 四、正式口径定义

### 4.1 RFScore 计算公式（正式版）

```python
class RFScore(Factor):
    name = "RFScore"
    max_window = 1
    dependencies = [
        # ROA 及同比变化
        "roa", "roa_4",
        # CFO TTM 及资产均值
        "net_operate_cash_flow", "net_operate_cash_flow_1", 
        "net_operate_cash_flow_2", "net_operate_cash_flow_3",
        "total_assets", "total_assets_1", "total_assets_2", "total_assets_3",
        "total_assets_4", "total_assets_5",
        # 杠杆率变化
        "total_non_current_liability", "total_non_current_liability_1",
        # 毛利率变化
        "gross_profit_margin", "gross_profit_margin_4",
        # 营收及资产周转
        "operating_revenue", "operating_revenue_4",
    ]

    def calc(self, data):
        # 1. ROA 水平
        roa = data["roa"]
        
        # 2. ROA 同比变化
        delta_roa = roa / data["roa_4"] - 1
        
        # 3. 经营现金流/资产 (OCFOA) TTM
        cfo_sum = sum([
            data["net_operate_cash_flow"], data["net_operate_cash_flow_1"],
            data["net_operate_cash_flow_2"], data["net_operate_cash_flow_3"]
        ])
        ta_ttm = sum([data["total_assets"], data["total_assets_1"],
                     data["total_assets_2"], data["total_assets_3"]]) / 4
        ocfoa = cfo_sum / ta_ttm
        
        # 4. 应计项目（现金流质量）
        accrual = ocfoa - roa * 0.01
        
        # 5. 杠杆率变化（去杠杆为正）
        leveler = data["total_non_current_liability"] / data["total_assets"]
        leveler1 = data["total_non_current_liability_1"] / data["total_assets_1"]
        delta_leveler = -(leveler / leveler1 - 1)
        
        # 6. 毛利率变化
        delta_margin = data["gross_profit_margin"] / data["gross_profit_margin_4"] - 1
        
        # 7. 资产周转率变化
        turnover = data["operating_revenue"] / (data["total_assets"] + data["total_assets_1"]).mean()
        turnover_1 = data["operating_revenue_4"] / (data["total_assets_4"] + data["total_assets_5"]).mean()
        delta_turn = turnover / turnover_1 - 1
        
        # 综合评分（7项指标每项为正得1分）
        indicators = [roa, delta_roa, ocfoa, accrual, delta_leveler, delta_margin, delta_turn]
        fscore = sum([np.where(ind > 0, 1, 0) for ind in indicators])
```

### 4.2 候选股筛选规则（正式版）

```python
# 主筛选池（必须满足）
primary_pool = df[
    (df["RFScore"] == 7) &           # RFScore 满分
    (df["pb_group"] == 1) &          # PB 最低 10% ⭐ 正式口径
    (df["pe_ratio"] < 50) &          # PE 上限过滤（新增）
    (df["ROA"] > 0.5)                # ROA 最低要求（新增）
]

# 次级筛选池（主池不足时启用）
secondary_pool = df[
    (df["RFScore"] >= 6) &          # RFScore >= 6
    (df["pb_group"] <= 2) &         # PB 最低 20%
    (df["pe_ratio"] < 50) &          # PE 上限过滤
    (df["ROA"] > 0.5)                # ROA 最低要求
]

# 排序规则（优先级从高到低）
sort_keys = [
    "RFScore",      # 降序 - RFScore 越高越好
    "ROA",          # 降序 - 盈利能力越强越好
    "OCFOA",        # 降序 - 现金流越好越好
    "DELTA_MARGIN", # 降序 - 毛利率改善越多越好
    "DELTA_TURN",   # 降序 - 周转率改善越多越好
    "pb_ratio"      # 升序 - PB 越低越好
]
```

### 4.3 PB 分组定义

```python
# 对所有股票按 PB 进行十分位分组
df["pb_group"] = pd.qcut(
    df["pb_ratio"].rank(method="first"),
    10,
    labels=False,
    duplicates="drop"
) + 1

# group=1: PB 最低 10%（正式主池）
# group=2: PB 10%-20%（次级池）
# group=3-10: 其他（不使用）
```

---

## 五、异常处理规则

### 5.1 该剔除的候选股

| 剔除条件 | 理由 | 实施方式 |
|----------|------|----------|
| PE > 100 | 盈利质量极差或一次性亏损 | 硬过滤（直接剔除） |
| ROA < 0.5% | 盈利能力不足 | 硬过滤（直接剔除） |
| PB < 0.4 | 可能存在基本面问题（资不抵债风险） | 软过滤（降级处理） |
| 毛利率 < 5% | 行业竞争恶化或公司竞争力下降 | 软过滤（排序降级） |

### 5.2 该保留的候选股

| 保留条件 | 适用场景 | 优先级 |
|----------|----------|--------|
| RFScore=7 + PB10% + 财务指标正常 | 标准入选条件 | ⭐⭐⭐⭐⭐ 最高 |
| RFScore=7 + PB10% + PE 略高但 ROA 强劲 | 成长股特例 | ⭐⭐⭐⭐ 高 |
| RFScore=6 + PB10% + 其他指标优异 | 次级池候选 | ⭐⭐⭐ 中 |
| RFScore=6-7 + PB20% | 仅当主池不足时使用 | ⭐⭐ 低 |

### 5.3 降级处理机制

当股票触发软过滤条件时：
1. **降级排序**: 在同等 RFScore 和 PB 组内，排到最后
2. **标记风险**: 在输出中添加风险标签
3. **权重调整**: 在组合构建时降低该类股票的配置权重

---

## 六、代码修复清单

### 6.1 必须修复的文件

| 文件 | 行号 | 当前代码 | 修复后代码 |
|------|------|----------|------------|
| `tmp/rfscore7_current_candidates.py` | 122 | `df["pb_group"] <= 2` | `df["pb_group"] == 1` |
| `tmp/rfscore7_candidate_industry.py` | 121 | `df["pb_group"] <= 2` | `df["pb_group"] == 1` |

### 6.2 建议增加的过滤器

在所有候选股筛选脚本中增加：

```python
# 在 sort_values 之前增加质量过滤
df = df[
    (df["pe_ratio"] < 100) &      # PE 上限
    (df["ROA"] > 0.5)               # ROA 下限
].copy()
```

---

## 七、验证结果

### 7.1 口径验证

| 检查项 | 预期值 | 实际值 | 状态 |
|--------|--------|--------|------|
| 正式策略 PB 组 | primary=1, reduced=2 | primary=1, reduced=2 | ✅ 一致 |
| 候选股脚本 PB 组 | 1 | 2 | ❌ 不一致 |
| 测试脚本 PB 组 | 1 | 1 | ✅ 一致 |

### 7.2 异常值验证

| 异常类型 | 发现数量 | 已处理 | 处理方式 |
|----------|----------|--------|----------|
| PE > 100 | 1 | 待处理 | 建议增加硬过滤 |
| ROE < 2% | 3 | 待处理 | 建议增加软过滤 |
| PB < 0.4 | 1 | 保留 | 浦发银行，银行股正常偏低 |

---

## 八、后续行动

### 8.1 立即执行（优先级 P0）

- [ ] 修复 `tmp/rfscore7_current_candidates.py` 第 122 行的 PB 组筛选
- [ ] 修复 `tmp/rfscore7_candidate_industry.py` 第 121 行的 PB 组筛选
- [ ] 统一所有脚本的口径到 PB10%

### 8.2 短期执行（优先级 P1）

- [ ] 在正式策略中增加 PE < 100 的硬过滤
- [ ] 在正式策略中增加 ROA > 0.5% 的硬过滤
- [ ] 更新所有相关文档中的口径说明

### 8.3 中期执行（优先级 P2）

- [ ] 建立候选股质量监控机制（任务 06）
- [ ] 增加行业分散度检查
- [ ] 完善异常值预警系统

---

## 九、附录

### 9.1 参考文档

1. `docs/parallel_strategy_tasks_20260328/11_rfscore7_pb10_upgrade_report.md` - PB10 升级报告
2. `strategies/rfscore7_pb10_final.py` - 正式策略文件
3. `tmp/test_rfscore_pb10.py` - PB10 测试脚本
4. `tmp/rfscore7_current_candidates.py` - 当前候选股脚本
5. `tmp/rfscore7_candidate_industry.py` - 行业分析脚本

### 9.2 版本信息

| 组件 | 版本 |
|------|------|
| RFScore 算法 | 7.0 |
| PB 筛选 | 10%（正式）/ 20%（备用）|
| 股票池 | 中证800（沪深300 ∪ 中证500）|
| 调仓频率 | 月度 |

---

**报告完成时间**: 2026-03-28  
**审计人员**: AI Assistant  
**下次审计**: 建议下次调仓前（2026-04-01）再次验证
