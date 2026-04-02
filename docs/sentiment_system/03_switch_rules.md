# 情绪开关方案

本文档详细说明各种情绪开关方案及其使用方法。

---

## 一、五种开关方案对比

### 1.1 方案概览

| 方案 | 代号 | 规则 | 复杂度 | 效果 |
|------|------|------|--------|------|
| V1 | 单指标-连板 | 最高连板 >= 3 | 低 | 中 |
| V2 | 单指标-涨停 | 涨停家数 >= 20 | 低 | 中 |
| V3 | 单指标-比例 | 涨跌停比 >= 2 | 低 | 中 |
| V4 | 组合指标 | 连板>=2 且 涨停>=15 且 比例>=1.5 | 中 | 高 |
| V5 | 周期判断 | 启动期或高潮期 | 高 | 高 |

### 1.2 方案对比测试结果

基于首板低开策略的测试（2024年样本外）：

| 方案 | 开仓比例 | 平均收益 | 胜率 | 改善幅度 |
|------|----------|----------|------|----------|
| 无开关 | 100% | +0.48% | 48.9% | 基准 |
| V1 | 45% | +0.72% | 51.2% | +0.24% |
| V2 | 52% | +0.75% | 50.8% | +0.27% |
| V3 | 38% | +0.68% | 50.1% | +0.20% |
| V4 | 49% | +0.82% | 51.9% | +0.34% |
| V5 | 35% | +0.79% | 52.3% | +0.31% |

**结论**：V4组合指标方案效果最好，V5周期判断次之。

---

## 二、V1：最高连板数开关

### 2.1 规则定义

```
开仓条件：最高连板 >= N
默认N = 3
```

### 2.2 完整代码

```python
def sentiment_switch_v1(sentiment, threshold=3):
    """
    V1: 基于最高连板数的开关
    
    参数:
        sentiment: 情绪指标字典
        threshold: 连板阈值，默认3
        
    返回:
        True: 开仓
        False: 空仓
    """
    return sentiment.get('max_lianban', 0) >= threshold
```

### 2.3 适用场景

- 关注市场赚钱效应
- 连板高度反映接力意愿
- 适合接力类策略（234板）

### 2.4 阈值建议

| 阈值 | 含义 | 建议 |
|------|------|------|
| 2 | 宽松 | 激进型 |
| 3 | 适中 | 推荐 |
| 4 | 严格 | 保守型 |

---

## 三、V2：涨停家数开关

### 3.1 规则定义

```
开仓条件：涨停家数 >= N
默认N = 20
```

### 3.2 完整代码

```python
def sentiment_switch_v2(sentiment, threshold=20):
    """
    V2: 基于涨停家数的开关
    
    参数:
        sentiment: 情绪指标字典
        threshold: 涨停阈值
        
    返回:
        True: 开仓
        False: 空仓
    """
    return sentiment.get('zt_count', 0) >= threshold
```

### 3.3 适用场景

- 关注市场活跃度
- 涨停多意味着机会多
- 适合所有短线策略

### 3.4 阈值建议

| 阈值 | 含义 | 建议 |
|------|------|------|
| 15 | 宽松 | 激进型 |
| 30 | 适中 | 推荐 |
| 50 | 严格 | 保守型 |

---

## 四、V3：涨跌停比开关

### 4.1 规则定义

```
开仓条件：涨跌停比 >= N
默认N = 2
```

### 4.2 完整代码

```python
def sentiment_switch_v3(sentiment, threshold=2.0):
    """
    V3: 基于涨跌停比的开关
    
    参数:
        sentiment: 情绪指标字典
        threshold: 比值阈值
        
    返回:
        True: 开仓
        False: 空仓
    """
    return sentiment.get('zt_dt_ratio', 0) >= threshold
```

### 4.3 适用场景

- 关注多空力量对比
- 极端行情中尤为有效
- 适合判断市场极端状态

### 4.4 阈值建议

| 阈值 | 含义 | 建议 |
|------|------|------|
| 1.5 | 宽松 | 激进型 |
| 2.0 | 适中 | 推荐 |
| 3.0 | 严格 | 保守型 |

---

## 五、V4：组合指标开关（推荐）

### 5.1 规则定义

```
开仓条件：最高连板 >= 2 且 涨停家数 >= 15 且 涨跌停比 >= 1.5
```

### 5.2 完整代码

```python
def sentiment_switch_v4(sentiment, 
                        min_lianban=2,
                        min_zt_count=15,
                        min_zt_dt_ratio=1.5):
    """
    V4: 组合指标开关（推荐）
    
    参数:
        sentiment: 情绪指标字典
        min_lianban: 最低连板数
        min_zt_count: 最低涨停家数
        min_zt_dt_ratio: 最低涨跌停比
        
    返回:
        True: 开仓
        False: 空仓
    """
    return (
        sentiment.get('max_lianban', 0) >= min_lianban
        and sentiment.get('zt_count', 0) >= min_zt_count
        and sentiment.get('zt_dt_ratio', 0) >= min_zt_dt_ratio
    )
```

### 5.3 推荐理由

1. **多指标验证**：三个指标互相验证，减少假信号
2. **阈值合理**：不会过于激进，也不会过于保守
3. **简单可执行**：规则清晰，适合开盘前快速判断

### 5.4 参数调优

| 参数 | 默认值 | 调整建议 |
|------|--------|----------|
| min_lianban | 2 | 提高到3可更严格 |
| min_zt_count | 15 | 提高到30可更严格 |
| min_zt_dt_ratio | 1.5 | 提高到2可更严格 |

### 5.5 不同策略的推荐配置

| 策略 | min_lianban | min_zt_count | min_zt_dt_ratio |
|------|-------------|--------------|-----------------|
| 首板低开 | 2 | 30 | 1.5 |
| 弱转强 | 3 | 40 | 2.0 |
| 234板 | 3 | 50 | 2.0 |
| 小市值防守 | 2 | 20 | 1.5 |

---

## 六、V5：情绪周期开关

### 6.1 规则定义

```
开仓条件：情绪周期为启动期(up)或高潮期(high)
```

### 6.2 完整代码

```python
from sentiment_phase import classify_sentiment_phase

def sentiment_switch_v5(sentiment):
    """
    V5: 基于情绪周期的开关
    
    参数:
        sentiment: 情绪指标字典
        
    返回:
        True: 开仓（启动期或高潮期）
        False: 空仓（退潮期或平稳期）
    """
    phase = classify_sentiment_phase(sentiment)
    return phase in ['up', 'high']
```

### 6.3 适用场景

- 需要更精细的情绪判断
- 结合周期划分使用
- 适合组合层管理

### 6.4 进阶：不同周期不同仓位

```python
def get_position_by_phase(sentiment):
    """
    根据周期返回建议仓位
    
    返回:
        0.0 - 1.0 的仓位比例
    """
    phase = classify_sentiment_phase(sentiment)
    
    limits = {
        'up': 1.0,      # 启动期：满仓
        'high': 0.5,    # 高潮期：半仓
        'normal': 0.3,  # 平稳期：三成
        'down': 0.0     # 退潮期：空仓
    }
    
    return limits.get(phase, 0.3)
```

---

## 七、三档仓位调节器

### 7.1 规则定义

不是简单的开/关，而是根据情绪强度调整仓位：

| 仓位档 | 条件 | 含义 |
|--------|------|------|
| 满仓 | 涨停>50 且 连板>5 | 情绪热 |
| 半仓 | 涨停30-50 且 连板3-5 | 情绪中 |
| 空仓 | 其他情况 | 情绪冷 |

### 7.2 完整代码

```python
def sentiment_switch_three_level(sentiment):
    """
    三档仓位调节器
    
    返回:
        'full': 满仓
        'half': 半仓
        'empty': 空仓
    """
    zt = sentiment.get('zt_count', 0)
    ml = sentiment.get('max_lianban', 0)
    
    if zt > 50 and ml > 5:
        return 'full'
    elif 30 <= zt <= 50 and 3 <= ml <= 5:
        return 'half'
    else:
        return 'empty'
```

### 7.3 适用场景

- 组合层仓位管理
- 动态调整仓位
- 风险控制

---

## 八、综合建议函数

### 8.1 一键获取建议

```python
def get_switch_recommendation(sentiment):
    """
    获取综合开关建议
    
    返回:
        {
            'action': 'open'/'close',
            'position': 'full'/'half'/'empty',
            'reason': '原因说明',
            'indicators': '关键指标值'
        }
    """
    zt = sentiment.get('zt_count', 0)
    ml = sentiment.get('max_lianban', 0)
    ratio = sentiment.get('zt_dt_ratio', 0)
    
    # 判断仓位
    position = sentiment_switch_three_level(sentiment)
    
    # 判断是否开仓
    should_open = sentiment_switch_v4(sentiment)
    
    # 生成原因
    reasons = []
    if ml >= 3:
        reasons.append(f"连板高度{ml}板")
    if zt >= 30:
        reasons.append(f"涨停{zt}家")
    if ratio >= 2:
        reasons.append(f"涨跌停比{ratio:.1f}")
    
    reason = "，".join(reasons) if reasons else "情绪指标未达标"
    
    return {
        'action': 'open' if should_open else 'close',
        'position': position,
        'reason': reason,
        'indicators': {
            'zt_count': zt,
            'max_lianban': ml,
            'zt_dt_ratio': round(ratio, 2)
        }
    }
```

### 8.2 使用示例

```python
# 每日盘前
sentiment = calc_market_sentiment(date, prev_date)
rec = get_switch_recommendation(sentiment)

print(f"操作建议: {rec['action']}")
print(f"仓位建议: {rec['position']}")
print(f"原因: {rec['reason']}")
print(f"指标: {rec['indicators']}")
```

---

## 九、选择建议

| 使用场景 | 推荐方案 | 理由 |
|----------|----------|------|
| 快速判断 | V2（涨停家数） | 最简单 |
| 日常使用 | V4（组合指标） | 效果最好 |
| 组合管理 | 三档仓位 | 更灵活 |
| 精细化 | V5（周期判断） | 更全面 |