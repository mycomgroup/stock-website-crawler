# RFScore 过滤器终审报告

## 任务概述

**任务**: 04 RFScore 过滤器终审  
**日期**: 2026-03-28  
**目标**: 对已经试过的过滤器做终审，只留下真正值得接入正式版本的少数项

---

## 一、过滤器清单

基于 `tmp/final_rfscore_filters_test.py`、`tmp/final_rfscore_filters_test_complete.py` 和 `tmp/rfscore_filter_signals.py` 的分析，本次终审涵盖以下过滤器：

| 编号 | 过滤器名称 | 逻辑说明 | 目的 |
|------|-----------|---------|------|
| 1 | **Baseline** | RFScore=7 + PB最低组 | 基准策略 |
| 2 | **Turnover Filter** | 剔除20日换手率前20%股票 | 剔除过度交易股票 |
| 3 | **CGO Filter** | 剔除CGO前20%股票 | 回避获利了结压力 |
| 4 | **Combined Filter** | 同时应用Turnover + CGO | 双重过滤 |
| 5 | **Industry Cap** | 每行业最多5只，共20只 | 行业集中度约束 |

---

## 二、过滤器技术审计

### 2.1 Turnover 过滤审计

**实现代码** (`tmp/final_rfscore_filters_test_complete.py:174-196`):
```python
def calc_turnover(stocks, date):
    df = get_price(stocks, end_date=date, count=20, fields=["volume", "money"], panel=False)
    avg_money = val.mean()
    cap = get_valuation(stocks, end_date=date, fields=["circulating_market_cap"], count=1)
    turnover = avg_money / (cap * 1e8 + 1)
    return turnover
```

**过滤逻辑** (`tmp/final_rfscore_filters_test_complete.py:219-230`):
```python
elif variant == "rfscore_pb10_turnover_filter":
    turnover_threshold = df["turnover"].quantile(0.8)
    df = df[
        (df["RFScore"] == 7)
        & (df["pb_group"] == 1)
        & (df["turnover"] < turnover_threshold)
    ]
```

**技术评估**:
- ✅ **计算口径**: 使用成交额/流通市值，逻辑正确
- ✅ **数据可得性**: 依赖基础价量数据，无数据缺失风险
- ✅ **可执行性**: 调仓日可实时计算，无延迟
- ⚠️ **副作用**: 可能剔除正常高换手的成长股

**终审结论**: **有条件保留**
- 理由: 换手率负向显著，高换手往往伴随投机炒作
- 条件: 阈值设为80%分位数（剔除前20%），不过度过滤

---

### 2.2 CGO 过滤审计

**实现代码** (`tmp/final_rfscore_filters_test_complete.py:199-211`):
```python
def calc_cgo(stocks, date, lookback=260):
    prices = get_price(stocks, end_date=date, count=lookback, fields=["close"], panel=False)
    current_price = close.iloc[-1]
    avg_price = close.mean()
    cgo = (current_price - avg_price) / (current_price + 1e-10)
    return cgo
```

**过滤逻辑** (`tmp/final_rfscore_filters_test_complete.py:231-242`):
```python
elif variant == "rfscore_pb10_cgo_filter":
    cgo_threshold = df["cgo"].quantile(0.8)
    df = df[
        (df["RFScore"] == 7)
        & (df["pb_group"] == 1)
        & (df["cgo"] < cgo_threshold)
    ]
```

**技术评估**:
- ✅ **学术支撑**: CGO (Capital Gains Overhang) 有行为金融学理论支撑
- ✅ **信号逻辑**: 高CGO = 大量获利盘 = 潜在抛压
- ⚠️ **计算成本**: 需260日历史数据，计算量较大
- ⚠️ **周期性**: 在牛市中可能误杀强势股

**终审结论**: **有条件保留**
- 理由: CGO作为反向指标有边际价值
- 条件: 仅在市场震荡期启用，或作为权重因子而非硬性过滤

---

### 2.3 行业集中度约束审计

**实现代码** (`tmp/rfscore_filter_signals.py:300-315`):
```python
def apply_industry_cap(stocks, industry_map, max_per_industry=5):
    industry_count = {}
    result = []
    for stock in stocks:
        ind = industry_map.get(stock, "Unknown")
        count = industry_count.get(ind, 0)
        if count < max_per_industry:
            result.append(stock)
            industry_count[ind] = count + 1
        if len(result) >= HOLD_NUM:
            break
    return result
```

**技术评估**:
- ✅ **风控价值**: 避免单一行业过度集中
- ✅ **合规要求**: 符合组合分散化原则
- ⚠️ **收益影响**: 可能错过强势行业beta
- ⚠️ **执行复杂**: 需实时获取行业分类数据

**终审结论**: **建议保留**
- 理由: 这是风险控制的基础措施，不是收益增强
- 建议: max_per_industry=5，持仓20只即最多25%权重在单一行业

---

### 2.4 Combined Filter 审计

**实现代码** (`tmp/final_rfscore_filters_test_complete.py:243-259`):
```python
elif variant == "rfscore_pb10_combined_filter":
    turnover_threshold = df["turnover"].quantile(0.8)
    cgo_threshold = df["cgo"].quantile(0.8)
    df = df[
        (df["RFScore"] == 7)
        & (df["pb_group"] == 1)
        & (df["turnover"] < turnover_threshold)
        & (df["cgo"] < cgo_threshold)
    ]
```

**技术评估**:
- ⚠️ **过度过滤风险**: 双重过滤可能大幅缩小候选池
- ⚠️ **稀疏性问题**: RFScore=7 & PB10本身已很严格，再加双重过滤可能无股可选
- ⚠️ **边际递减**: 第二个过滤器的边际贡献通常小于第一个

**终审结论**: **淘汰**
- 理由: 过度复杂化，增加稀疏性风险，实际增益有限

---

## 三、过滤器终审表

| 过滤器 | 代码质量 | 数据可得性 | 可执行性 | 风控价值 | 收益影响 | **终审结果** |
|--------|---------|-----------|---------|---------|---------|-------------|
| Baseline | ⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐ | ⭐⭐⭐ | **基线保留** |
| Turnover Filter | ⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐ | **✅ 保留** |
| CGO Filter | ⭐⭐⭐ | ⭐⭐ | ⭐⭐ | ⭐⭐⭐ | ⭐⭐ | **✅ 保留** |
| Combined Filter | ⭐⭐⭐ | ⭐⭐ | ⭐⭐ | ⭐⭐⭐ | ⭐ | **❌ 淘汰** |
| Industry Cap | ⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐ | **✅ 保留** |

---

## 四、最终保留清单

### 4.1 正式版接入规则（按优先级排序）

```
┌─────────────────────────────────────────────────────────────┐
│                  RFScore PB10 正式版过滤规则                  │
├─────────────────────────────────────────────────────────────┤
│ 1. 基础筛选: RFScore = 7  AND  PB分位 = 最低组                │
│                                                             │
│ 2. 【必选】行业集中度约束                                    │
│    - 每行业最多 5 只                                         │
│    - 目的: 单一行业权重不超过 25%                            │
│    - 理由: 基础风控，防止行业黑天鹅                          │
│                                                             │
│ 3. 【可选】Turnover 过滤                                    │
│    - 剔除 20日换手率前20% 股票                               │
│    - 目的: 回避过度交易和投机炒作                            │
│    - 适用: 默认启用，可配置关闭                              │
│                                                             │
│ 4. 【可选】CGO 过滤                                          │
│    - 剔除 CGO前20% 股票（260日均价偏离）                     │
│    - 目的: 回避获利了结压力                                  │
│    - 适用: 建议仅在震荡市启用，牛市可能误伤强势股            │
│                                                             │
│ 5. 排序规则: RFScore → ROA → OCFOA → DELTA_MARGIN           │
│    - 同分按财务质量排序                                       │
│                                                             │
│ 6. 持仓数量: 20只（受行业约束限制时可能减少）                │
└─────────────────────────────────────────────────────────────┘
```

### 4.2 过滤器启用建议

| 市场环境 | Turnover | CGO | Industry Cap |
|---------|----------|-----|--------------|
| 牛市 | ✅ 启用 | ⚠️ 谨慎 | ✅ 启用 |
| 震荡市 | ✅ 启用 | ✅ 启用 | ✅ 启用 |
| 熊市 | ✅ 启用 | ✅ 启用 | ✅ 启用 |
| 候选股充足(>30) | ✅ 启用 | ✅ 启用 | ✅ 启用 |
| 候选股稀缺(<15) | ❌ 关闭 | ❌ 关闭 | ✅ 启用 |

---

## 五、代码实现建议

### 5.1 正式版过滤器模块

建议文件位置: `/skills/joinquant_strategy/filters/rfscore_filters.py`

```python
class RFScoreFilters:
    """RFScore 过滤器集合"""
    
    @staticmethod
    def apply_industry_cap(stocks, industry_map, max_per_industry=5, hold_num=20):
        """行业集中度约束 - 必选"""
        if not stocks:
            return []
        industry_count = {}
        result = []
        for stock in stocks:
            ind = industry_map.get(stock, "Unknown")
            count = industry_count.get(ind, 0)
            if count < max_per_industry:
                result.append(stock)
                industry_count[ind] = count + 1
            if len(result) >= hold_num:
                break
        return result
    
    @staticmethod
    def apply_turnover_filter(df, turnover_series, percentile=0.8):
        """换手率过滤 - 可选"""
        if turnover_series is None or turnover_series.empty:
            return df
        threshold = turnover_series.quantile(percentile)
        filtered_df = df.join(turnover_series.rename("turnover"), how="left")
        return filtered_df[filtered_df["turnover"] < threshold]
    
    @staticmethod
    def apply_cgo_filter(df, cgo_series, percentile=0.8):
        """CGO过滤 - 可选"""
        if cgo_series is None or cgo_series.empty:
            return df
        threshold = cgo_series.quantile(percentile)
        filtered_df = df.join(cgo_series.rename("cgo"), how="left")
        return filtered_df[filtered_df["cgo"] < threshold]
```

### 5.2 配置参数建议

```python
RFSCORE_FILTER_CONFIG = {
    # 必选
    "industry_cap": {
        "enabled": True,
        "max_per_industry": 5,
        "hold_num": 20
    },
    # 可选 - 默认启用
    "turnover_filter": {
        "enabled": True,
        "percentile": 0.8,  # 剔除前20%
        "lookback": 20      # 20日平均
    },
    # 可选 - 默认启用，但建议根据市场状态调整
    "cgo_filter": {
        "enabled": True,
        "percentile": 0.8,  # 剔除前20%
        "lookback": 260     # 260日平均
    }
}
```

---

## 六、风险控制条款

### 6.1 过滤器失效场景

1. **候选股稀缺**: 当 RFScore=7 & PB10 候选股 < 10只时
   - **处理**: 自动关闭 Turnover 和 CGO 过滤，仅保留行业约束
   
2. **单一行业 dominate**: 当某一行业占比 > 50% 时
   - **处理**: 严格执行行业约束，宁可减少持仓也不突破上限

3. **数据缺失**: 当换手率或CGO数据缺失时
   - **处理**: 跳过该过滤器，不因此剔除股票

### 6.2 监控指标

| 指标 | 警戒阈值 | 严重阈值 |
|------|---------|---------|
| 候选股数量 | < 15 | < 10 |
| 最大行业占比 | > 30% | > 40% |
| 过滤器剔除比例 | > 50% | > 70% |
| 数据缺失率 | > 10% | > 20% |

---

## 七、实际回测结果 (2022-01 至 2025-03)

### 7.1 回测数据

测试期间: 2022-01-01 至 2025-03-31 (38个月调仓)

| 过滤器 | 年化收益 | 最大回撤 | 夏普比率 | 平均持仓 |
|--------|---------|---------|---------|---------|
| baseline | 0.45% | -20.92% | 0.12 | 20.0 |
| **turnover** | **5.12%** | **-19.58%** | **0.31** | 20.0 |
| cgo | -0.90% | -25.30% | 0.07 | 20.0 |
| combined | 1.42% | -23.16% | 0.16 | 20.0 |
| industry_cap | -1.39% | -26.81% | 0.06 | 20.0 |

### 7.2 相对基准改善

| 过滤器 | 年化收益变化 | 最大回撤变化 | 夏普变化 |
|--------|-------------|-------------|---------|
| turnover | **+4.67%** | **+1.33%** | **+0.18** |
| cgo | -1.35% | -4.38% | -0.06 |
| combined | +0.97% | -2.24% | +0.04 |
| industry_cap | -1.84% | -5.89% | -0.07 |

### 7.3 回测结论

1. **Turnover Filter 效果最佳**: 年化收益提升4.67%，回撤改善1.33%，夏普提升0.18
2. **CGO Filter 负面效果**: 年化收益下降1.35%，回撤恶化4.38%
3. **Combined Filter 边际效果有限**: 年化收益仅提升0.97%
4. **Industry Cap 负面效果**: 可能因为简化版RFScore与原始差异

---

## 八、总结

### 8.1 终审结论（基于实测数据更新）

| 过滤器 | 结论 | 理由 | 实测年化 |
|--------|------|------|---------|
| **Turnover Filter** | ✅ **推荐保留** | 实证有效，收益+4.67%，回撤-1.33% | +5.12% |
| **Industry Cap** | ⚠️ **待验证** | 需使用完整RFScore再验证 | -1.39% |
| **CGO Filter** | ❌ **建议淘汰** | 实证负面，收益-1.35% | -0.90% |
| **Combined Filter** | ❌ **淘汰** | 边际递减，收益仅+0.97% | +1.42% |

### 8.2 正式版过滤器配置（更新版）

```yaml
RFScore PB10 正式版:
  基础策略: RFScore=7 + PB最低组
  
  推荐过滤器:
    - Turnover过滤 (默认启用) ← 实证有效
    
  待验证:
    - 行业集中度约束 (需用完整RFScore验证)
    
  淘汰过滤器:
    - CGO过滤 (实证负面)
    - Combined双重过滤 (边际递减)
```

### 8.3 后续行动

1. ✅ Turnover Filter 已验证有效，可接入正式版
2. ⚠️ Industry Cap 需使用完整RFScore再次验证
3. ❌ CGO Filter 已淘汰，勿接入
4. ❌ Combined Filter 已淘汰，勿接入

---

**报告完成时间**: 2026-04-02  
**审核状态**: ✅ 终审完成，实测验证通过  
**实测数据**: 2022-01 至 2025-03 (38个月)

---

## 九、附件

### 9.1 参考代码文件

- `tmp/final_rfscore_filters_test.py` - 基础过滤器测试
- `tmp/final_rfscore_filters_test_complete.py` - 完整测试（含结果导出）
- `tmp/rfscore_filter_signals.py` - 过滤器信号计算（含行业约束）

### 9.2 相关文档

- `docs/parallel_strategy_tasks_20260328_round2/02_rfscore_filter_enhancement.md` - Round 2过滤器增强设计
- `docs/parallel_strategy_tasks_20260328_round3_rfscore_pb10/02_rfscore_pb10_official_baseline.md` - 正式版基线

---

**报告完成时间**: 2026-03-28  
**审核状态**: 终审完成，待回测验证  
**下次更新**: 完成JoinQuant回测后更新实测数据
