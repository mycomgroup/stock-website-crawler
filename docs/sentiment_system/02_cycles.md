# 情绪周期划分

本文档定义情绪周期的划分方法和判断规则。

---

## 一、四阶段模型

### 1.1 模型概述

将市场情绪划分为四个阶段：

```
启动期 → 发酵期 → 高潮期 → 退潮期 → 启动期 → ...
```

| 周期 | 英文代号 | 特征 | 仓位建议 |
|------|----------|------|----------|
| 启动期 | up | 情绪转暖，龙头确立 | 满仓 |
| 发酵期/平稳期 | normal | 赚钱效应扩散 | 三成仓 |
| 高潮期 | high | 情绪亢奋，涨停众多 | 半仓 |
| 退潮期 | down | 赚钱效应消失 | 空仓 |

---

## 二、各周期详细定义

### 2.1 启动期 (up)

**特征**

- 最高连板：3-4板
- 涨停家数：30-60家
- 晋级率：>= 30%
- 龙头开始确立
- 题材开始聚焦

**市场表现**

- 赚钱效应开始显现
- 前期亏损的短线资金开始回血
- 新题材开始发酵

**策略建议**

```
仓位：100%
策略：积极开仓，重点关注龙头和主流题材
止损：正常止损
```

**判断代码**

```python
def is_up_phase(sentiment):
    return (
        sentiment['max_lianban'] >= 3 
        and sentiment['zt_count'] >= 25 
        and sentiment['jinji_rate'] >= 0.3
    )
```

---

### 2.2 发酵期/平稳期 (normal)

**特征**

- 最高连板：2-3板
- 涨停家数：20-40家
- 晋级率：20-30%
- 无明显主线
- 题材分散

**市场表现**

- 震荡为主
- 个股分化严重
- 快进快出为主

**策略建议**

```
仓位：30%
策略：小仓位试探，快进快出
止损：严格止损
```

**判断代码**

```python
def is_normal_phase(sentiment):
    return (
        not is_up_phase(sentiment) 
        and not is_high_phase(sentiment) 
        and not is_down_phase(sentiment)
    )
```

---

### 2.3 高潮期 (high)

**特征**

- 最高连板：>= 5板
- 涨停家数：>= 40家
- 市场情绪亢奋
- 资金大量涌入

**市场表现**

- 涨停板众多
- 连板高度较高
- 但风险也在累积

**策略建议**

```
仓位：50%（注意风险）
策略：谨慎开仓，避免追高
止损：更严格止损
```

**注意**

高潮期虽然涨停多，但往往意味着分歧即将到来，风险较高。

**判断代码**

```python
def is_high_phase(sentiment):
    return (
        sentiment['max_lianban'] >= 5 
        and sentiment['zt_count'] >= 40
    )
```

---

### 2.4 退潮期 (down)

**特征**

- 最高连板：<= 2板
- 涨停家数：< 15家
- 晋级率：< 20%
- 龙头断板
- 亏钱效应明显

**市场表现**

- 接力资金被套
- 涨停稀少
- 高开低走频繁

**策略建议**

```
仓位：0%
策略：空仓观望
止损：立即止损
```

**判断代码**

```python
def is_down_phase(sentiment):
    return (
        sentiment['zt_count'] < 15 
        or (sentiment['max_lianban'] <= 2 and sentiment['zt_count'] < 20)
    )
```

---

## 三、周期判断规则

### 3.1 决策树

```
开始
  │
  ├─ 涨停 < 15 或 (连板 <= 2 且 涨停 < 20)?
  │   └─ 是 → 退潮期
  │   └─ 否 ↓
  │
  ├─ 连板 >= 5 且 涨停 >= 40?
  │   └─ 是 → 高潮期
  │   └─ 否 ↓
  │
  ├─ 连板 >= 3 且 涨停 >= 25 且 晋级率 >= 30%?
  │   └─ 是 → 启动期
  │   └─ 否 → 平稳期
```

### 3.2 阈值表

| 周期 | 涨停家数 | 最高连板 | 晋级率 | 其他条件 |
|------|----------|----------|--------|----------|
| 高潮期 | >= 40 | >= 5 | - | - |
| 启动期 | >= 25 | >= 3 | >= 30% | - |
| 平稳期 | - | - | - | 不满足其他条件 |
| 退潮期 | < 15 | - | - | 或 (连板<=2 且 涨停<20) |

### 3.3 完整判断代码

```python
def classify_sentiment_phase(sentiment):
    """
    划分情绪周期
    
    参数:
        sentiment: 情绪指标字典
        
    返回:
        'up': 启动期
        'high': 高潮期
        'normal': 平稳期
        'down': 退潮期
    """
    zt = sentiment.get('zt_count', 0)
    ml = sentiment.get('max_lianban', 0)
    jr = sentiment.get('jinji_rate', 0)
    
    # 高潮期
    if ml >= 5 and zt >= 40:
        return 'high'
    
    # 启动期
    elif ml >= 3 and zt >= 25 and jr >= 0.3:
        return 'up'
    
    # 退潮期
    elif zt < 15 or (ml <= 2 and zt < 20):
        return 'down'
    
    # 平稳期
    else:
        return 'normal'
```

---

## 四、周期转换分析

### 4.1 正向转换（情绪上升）

```
down → normal → up → high
```

| 转换 | 信号 | 操作 |
|------|------|------|
| down → normal | 涨停增加到20+ | 可以试探 |
| normal → up | 连板出现，晋级率上升 | 开始加仓 |
| up → high | 涨停大增，连板高度上升 | 注意风险 |

### 4.2 反向转换（情绪下降）

```
high → up → normal → down
```

| 转换 | 信号 | 操作 |
|------|------|------|
| high → up | 涨停减少，龙头断板 | 开始减仓 |
| up → normal | 连板高度下降 | 进一步减仓 |
| normal → down | 涨停稀少 | 立即空仓 |

### 4.3 转换检测代码

```python
def detect_phase_transition(prev_phase, curr_phase):
    """
    检测周期转换
    
    返回:
        'up': 情绪上升
        'down': 情绪下降
        'stable': 稳定
    """
    order = {'down': 0, 'normal': 1, 'up': 2, 'high': 3}
    
    prev_order = order.get(prev_phase, 1)
    curr_order = order.get(curr_phase, 1)
    
    if curr_order > prev_order:
        return 'up'
    elif curr_order < prev_order:
        return 'down'
    else:
        return 'stable'
```

---

## 五、仓位建议

### 5.1 各周期仓位上限

| 周期 | 仓位上限 | 理由 |
|------|----------|------|
| 启动期 | 100% | 赚钱效应最佳 |
| 平稳期 | 30% | 不确定性高 |
| 高潮期 | 50% | 风险累积 |
| 退潮期 | 0% | 亏钱效应 |

### 5.2 动态仓位计算

```python
def get_position_limit(phase):
    """获取仓位上限"""
    limits = {
        'up': 1.0,
        'normal': 0.3,
        'high': 0.5,
        'down': 0.0
    }
    return limits.get(phase, 0.3)
```

---

## 六、使用示例

```python
# 在策略中使用
from sentiment_phase import classify_sentiment_phase, get_position_limit

def before_trading(context):
    # 计算情绪
    sentiment = calc_market_sentiment(date, prev_date)
    
    # 判断周期
    phase = classify_sentiment_phase(sentiment)
    context.phase = phase
    
    # 设置仓位上限
    context.position_limit = get_position_limit(phase)
    
    log.info(f"情绪周期: {phase}, 仓位上限: {context.position_limit:.0%}")

def handle_bar(context, bar_dict):
    # 检查仓位限制
    current_position = context.portfolio.positions_value / context.portfolio.total_value
    
    if current_position >= context.position_limit:
        return  # 已达上限，不再开仓
    
    # 执行开仓逻辑
    pass
```

---

## 七、注意事项

### 7.1 高潮期的特殊性

高潮期虽然涨停多，但往往是风险累积的阶段：

- 连板高度过高，分歧随时到来
- 资金过于亢奋，容易高开低走
- 建议仓位不超过50%

### 7.2 周期判断的滞后性

情绪周期判断基于T-1日数据，存在一天滞后：

- 今日开盘前使用昨日收盘数据
- 如果今日情绪突变，需盘中观察

### 7.3 特殊情况处理

| 情况 | 处理方式 |
|------|----------|
| 涨停很少但连板很高 | 视为高潮期（风险更高） |
| 涨停很多但无连板 | 视为平稳期（主线未确立） |
| 指标矛盾时 | 以涨停家数为主 |