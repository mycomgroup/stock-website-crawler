# RFScore7 收益归因验证代码集

## 验证目标
以 `/Users/fengzhi/Downloads/git/testlixingren/strategies/misc_research/dividend_value_quality_v1/v1_rfscore7_offensive.py` 为基准版本
验证核心收益来源：RFScore7质量因子 vs PB低估值 vs 动态风控

---

## 版本对比表

| 版本 | 文件路径 | 核心差异 | 验证目的 |
|------|---------|---------|---------|
| **基准版A** | `v1_rfscore7_offensive.py` | RFScore7 + PB低20% + ROA排序 + 满仓持有 | 原始策略收益 |
| **归因版B** | `attribution_b_pure_pb.py` | **仅PB最低10%** + 无RFScore + 有风控 | 验证PB单独贡献 |
| **归因版C** | `attribution_c_pure_rfscore.py` | **仅RFScore=7** + 无PB过滤 + 有风控 | 验证RFScore单独贡献 |
| **归因版D** | `attribution_d_no_risk_control.py` | RFScore7 + PB10% + **无风控** | 验证风控贡献 |
| **归因版E** | `attribution_e_pb20_loose.py` | RFScore7 + **PB20%** + 有风控 | 验证PB严格度影响 |

---

## 各版本详细说明

### 版本A：基准版（原始策略）
**文件**: `v1_rfscore7_offensive.py`

**核心逻辑**:
```python
# 1. 中证800股票池
stocks = 沪深300 + 中证500

# 2. PB低20%筛选（约160只）
df = query(PB最低20%)

# 3. 按ROA排序（质量排序）
df.sort_values("roa", ascending=False)

# 4. 取前20只，满仓持有
return df[:20]
```

**特点**:
- 无动态风控（始终满仓）
- PB低20%（较宽松）
- ROA排序（简单质量因子）
- 无行业分散
- 佣金更低（0.012% vs 0.03%）

---

### 版本B：纯PB低估值（剥离RFScore）
**文件**: `skills/joinquant_strategy/attribution_b_pure_pb.py`

**核心改动**:
```python
# 移除RFScore7因子计算
# 仅保留PB最低10%选股

# 原逻辑：
# primary = df[(df["RFScore"] == 7) & (df["pb_group"] <= 1)]

# 改为：
primary = df[df["pb_group"] == 1]  # 仅PB最低10%
```

**特点**:
- 保留动态风控（市场宽度<25%减仓）
- 保留行业分散（单行业≤30%）
- 保留PE<100过滤
- **无RFScore质量筛选**

**预期结果**:
- 如果收益大幅下降 → RFScore是核心贡献
- 如果收益变化不大 → PB是核心贡献

---

### 版本C：纯RFScore质量（剥离PB）
**文件**: `skills/joinquant_strategy/attribution_c_pure_rfscore.py`（需创建）

**核心逻辑**:
```python
# 仅保留RFScore=7，不限制PB分组
primary = df[df["RFScore"] == 7]  # 仅质量最高
# 不限制pb_group
```

**特点**:
- 保留动态风控
- 保留行业分散
- **无PB低估值过滤**
- 可能选到高PB股票

**预期结果**:
- 如果收益大幅下降 → PB低估值是核心贡献
- 如果收益变化不大 → RFScore是核心贡献

---

### 版本D：无风控（剥离动态仓位）
**文件**: `skills/joinquant_strategy/attribution_d_no_risk_control.py`（需创建）

**核心改动**:
```python
# 移除所有市场宽度判断
# 始终满仓持有20只

def rebalance(context):
    # 原逻辑：
    # if breadth < 0.15: 空仓
    # elif breadth < 0.25: 减仓至10只
    # else: 20只
    
    # 改为：
    target_hold_num = 20  # 始终20只
    target_stocks, _ = choose_stocks(watch_date, 20)
```

**特点**:
- 保留RFScore7 + PB10%
- **无动态风控**
- 始终满仓

**预期结果**:
- 对比2022年熊市表现
- 如果回撤大幅增加 → 风控有效
- 如果收益变化不大 → 风控参数过拟合

---

### 版本E：PB20%宽松版（验证PB严格度）
**文件**: `skills/joinquant_strategy/attribution_e_pb20_loose.py`（需创建）

**核心改动**:
```python
# 将PB10%放宽到PB20%
g.primary_pb_group = 2  # PB20%
g.reduced_pb_group = 3  # PB30%
```

**特点**:
- 保留RFScore7
- 保留动态风控
- **PB分组更宽松**
- 候选股更多

**预期结果**:
- 如果收益下降 → PB10%严格筛选有效
- 如果收益上升或不变 → PB10%过拟合

---

## 回测对比维度

| 对比组 | 版本 | 验证问题 |
|--------|------|---------|
| **A vs B** | 完整版 vs 纯PB | RFScore7贡献多少？ |
| **A vs C** | 完整版 vs 纯RFScore | PB低估值贡献多少？ |
| **A vs D** | 完整版 vs 无风控 | 动态风控贡献多少？ |
| **A vs E** | PB10% vs PB20% | PB严格度是否过拟合？ |
| **B vs C** | 纯PB vs 纯RFScore | 哪个因子单独更强？ |

---

## 关键评估指标

| 指标 | 说明 |
|------|------|
| **年化收益** | 核心收益指标 |
| **最大回撤** | 风控效果指标 |
| **夏普比率** | 风险调整后收益 |
| **2022年收益** | 熊市表现（风控关键期） |
| **2024-2025年收益** | 牛市表现（选股关键期） |
| **月胜率** | 稳定性指标 |
| **候选股平均数量** | 策略容量指标 |

---

## 执行建议

### 第一步：跑基准版A
- 确认原始策略回测结果
- 记录各年度收益

### 第二步：跑剥离测试（B、C、D）
- 分别移除RFScore、PB、风控
- 看哪个移除后收益下降最多

### 第三步：跑参数敏感性（E）
- 测试PB10% vs PB20% vs PB30%
- 看收益是否单调变化

### 第四步：综合分析
- 制作归因表格
- 确定核心收益来源

---

## 预期结论（假设）

| 情景 | 核心收益来源 | 建议 |
|------|------------|------|
| A>B且A>C | RFScore+PB共同作用 | 保留双因子 |
| A>>B且A≈C | RFScore是核心 | 强化质量因子 |
| A≈B且A>>C | PB是核心 | 简化策略，只留PB |
| A≈D | 风控无效 | 移除复杂风控 |
| A>E | PB10%有效 | 保持严格PB筛选 |

---

## 代码文件清单

| 文件 | 状态 | 说明 |
|------|------|------|
| `v1_rfscore7_offensive.py` | ✅ 已有 | 基准版A |
| `attribution_b_pure_pb.py` | ✅ 已有 | 纯PB版B |
| `attribution_c_pure_rfscore.py` | ❌ 待创建 | 纯RFScore版C |
| `attribution_d_no_risk_control.py` | ❌ 待创建 | 无风控版D |
| `attribution_e_pb20_loose.py` | ❌ 待创建 | PB宽松版E |

---

**下一步**: 需要我创建版本C、D、E的代码吗？
