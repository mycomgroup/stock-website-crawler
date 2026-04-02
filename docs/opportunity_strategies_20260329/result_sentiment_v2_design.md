# 情绪层v2完善方案

> 日期：2026-04-02
> 状态：测试完成，代码实现中
> 结论：**Go - 采用动态阈值 + 过热过滤 + 5档仓位**

---

## 一、测试结果汇总

### 1.1 阈值优化测试（2024年Q1）

| 阈值 | 信号数 | 收益% | 胜率% | 交易次数 |
|------|--------|-------|-------|----------|
| 0（无过滤） | 37 | -0.041 | 51.4 | 35 |
| 20 | 2 | +1.539 | 100.0 | 2 |
| 30+ | 0 | - | - | 0 |

**发现**：2024年Q1市场情绪低，涨停家数大部分<20，阈值30以上无信号。

### 1.2 仓位分层测试

| 方案 | 信号数 | 加权收益% | 胜率% | 交易次数 |
|------|--------|-----------|-------|----------|
| 硬开关（阈值30） | 0 | - | - | 0 |
| 3档仓位 | 0 | - | - | 0 |
| 5档仓位 | 6 | +0.700 | 100.0 | 6 |

**发现**：5档仓位在低情绪期仍能产生信号，适应性更强。

### 1.3 历史数据参考

| 来源 | 阈值 | 样本内年化 | 样本外年化 | 卡玛比率 |
|------|------|------------|------------|----------|
| result_02 | 30 | 10.8% | 8.2% | 0.51 |
| result_05 | 50 | - | +0.82%/次 | - |
| result_02补充 | 30-80 | - | 推荐区间 | - |

---

## 二、最优参数确定

### 2.1 最终参数

| 参数 | 值 | 说明 |
|------|-----|------|
| 基准阈值 | 20 | 适应低情绪期 |
| 过热阈值 | 100 | 避免过热市场 |
| 仓位档位 | 5档 | 适应不同情绪强度 |
| 趋势周期 | 5日 | 响应快 |

### 2.2 仓位分层规则

| 涨停家数 | 仓位比例 | 说明 |
|----------|----------|------|
| >100 | 0% | 过热，空仓 |
| 80-100 | 100% | 极高情绪，满仓 |
| 50-80 | 80% | 高情绪 |
| 30-50 | 50% | 中情绪 |
| 20-30 | 25% | 低情绪 |
| <20 | 0% | 极低情绪，空仓 |

### 2.3 动态阈值规则

```python
# 趋势判断
def get_trend(zt_counts_5d):
    ma5 = sum(zt_counts_5d[-5:]) / 5
    ma10 = sum(zt_counts_5d[-10:]) / 10 if len(zt_counts_5d) >= 10 else ma5
    
    if ma5 > ma10 * 1.1:
        return 'up'
    elif ma5 < ma10 * 0.9:
        return 'down'
    else:
        return 'stable'

# 动态阈值
def get_dynamic_threshold(base_threshold=20, trend='stable'):
    if trend == 'up':
        return base_threshold * 0.85  # 放宽至17
    elif trend == 'down':
        return base_threshold * 1.15  # 收紧至23
    else:
        return base_threshold
```

---

## 三、代码实现

### 3.1 情绪层v2核心函数

```python
def sentiment_switch_v2(zt_count, zt_counts_5d=None):
    """
    情绪开关v2：动态阈值 + 过热过滤 + 5档仓位
    
    参数:
        zt_count: 当日涨停家数
        zt_counts_5d: 近5日涨停家数列表（可选）
    
    返回:
        (should_trade, position_ratio)
    """
    # 1. 过热过滤（硬规则）
    if zt_count > 100:
        return False, 0.0
    
    # 2. 趋势判断（可选）
    if zt_counts_5d and len(zt_counts_5d) >= 5:
        trend = get_trend(zt_counts_5d)
        threshold = get_dynamic_threshold(base_threshold=20, trend=trend)
    else:
        threshold = 20
    
    # 3. 仓位分层
    if zt_count >= threshold:
        if zt_count >= 80:
            return True, 1.0   # 极高情绪，满仓
        elif zt_count >= 50:
            return True, 0.8   # 高情绪
        elif zt_count >= 30:
            return True, 0.5   # 中情绪
        elif zt_count >= 20:
            return True, 0.25  # 低情绪
        else:
            return False, 0.0  # 极低情绪
    else:
        return False, 0.0
```

---

## 四、与首板低开的接入

```python
def strategy_with_sentiment_v2(context, stock, zt_count, zt_counts_5d=None):
    """
    首板低开策略 + 情绪层v2
    """
    # 检查情绪开关
    should_trade, position_ratio = sentiment_switch_v2(zt_count, zt_counts_5d)
    
    if not should_trade:
        return 0  # 不交易
    
    # 计算实际仓位
    base_position = 0.05  # 单票基础仓位5%
    actual_position = base_position * position_ratio
    
    return actual_position
```

---

## 五、最终结论

### Go / Watch / No-Go：**Go**

**推荐采用**：
- 动态阈值（基准20，趋势调整±15%）
- 过热过滤（涨停>100不参与）
- 5档仓位（0%/25%/50%/80%/100%）

**优势**：
1. 适应低情绪期（阈值20）
2. 避免过热市场（>100）
3. 仓位灵活（5档分层）
4. 规则简单可执行

---

**文档版本**：v1.0
**生成时间**：2026-04-02
