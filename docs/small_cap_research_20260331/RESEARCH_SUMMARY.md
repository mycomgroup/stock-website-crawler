# 小市值策略技术研究报告

**日期**: 2026-03-31  
**状态**: 研究完成，建议实施

---

## 一、核心发现（来自研究文档）

### 1.1 情绪开关（最重要）

| 指标 | 无开关 | 有开关（涨停>=30） | 改善 |
|------|--------|-------------------|------|
| 年化收益 | 8.5% | 10.8% | +27% |
| 最大回撤 | 35.2% | 21.3% | **-40%** |
| 卡玛比率 | 0.24 | 0.51 | **+113%** |

**规则**：
```python
# 涨停家数 >= 30 → 开仓
# 涨停家数 < 30  → 空仓/持有ETF
```

---

### 1.2 停手机制

| 机制 | 回撤改善 | 卡玛提升 | 收益变化 |
|------|---------|---------|---------|
| 连亏3停3天 | -28.4% | +68.6% | +20.7% |

**规则**：
```python
# 连亏3笔 → 停手3天
# 停手期间忽略所有信号
```

---

### 1.3 二板策略思路（胜率87.95%）

| 选股条件 | 说明 |
|----------|------|
| 昨日二板 | 第二个涨停板 |
| 非一字板 | 排除一字涨停 |
| 换手率 < 30% | 避免过度换手 |
| 缩量 | 昨日量 <= 前日×1.875 |
| 非涨停开盘 | 保证可成交 |
| 市值最小优先 | 小市值弹性大 |

**结果**：
- 胜率：87.95%
- 年化收益：407%
- 最大回撤：0.60%

---

## 二、策略改进建议

### 2.1 必须加入

| 改进项 | 优先级 | 难度 | 预期效果 |
|--------|--------|------|----------|
| **情绪开关** | P0 | ⭐ | 回撤-40% |
| **停手机制** | P0 | ⭐⭐ | 卡玛+68% |
| **不追涨停** | P1 | ⭐ | 成交保证 |

### 2.2 建议加入

| 改进项 | 优先级 | 难度 | 预期效果 |
|--------|--------|------|----------|
| 缩量筛选 | P1 | ⭐⭐ | 过滤假突破 |
| 换手率限制 | P1 | ⭐ | 流动性保障 |

---

## 三、完整策略代码框架

### 3.1 情绪开关模块

```python
def get_emotion_score():
    """计算涨停家数"""
    stocks = get_all_securities('stock').index
    zt_count = 0
    current = get_current_data()
    
    for s in stocks:
        if current[s].last_price >= current[s].high_limit * 0.995:
            zt_count += 1
    
    return zt_count

# 使用
if get_emotion_score() < 30:
    return  # 不开仓
```

### 3.2 停手机制模块

```python
class PauseManager:
    def __init__(self):
        self.loss_count = 0
        self.pause_days = 0
    
    def record_trade(self, pnl):
        if pnl < 0:
            self.loss_count += 1
        else:
            self.loss_count = 0
        
        if self.loss_count >= 3:
            self.pause_days = 3
    
    def can_trade(self):
        return self.pause_days == 0
    
    def daily_update(self):
        if self.pause_days > 0:
            self.pause_days -= 1
```

### 3.3 不追涨停

```python
def filter_limit_up(stocks):
    """过滤涨停股"""
    current = get_current_data()
    return [s for s in stocks 
            if current[s].last_price < current[s].high_limit * 0.98]
```

### 3.4 缩量筛选

```python
def filter_shrink(stocks):
    """筛选缩量股票"""
    results = []
    for s in stocks:
        vol = history(2, '1d', 'volume', [s])
        if vol is not None and len(vol) >= 2:
            if vol[s].iloc[-1] <= vol[s].iloc[-2] * 1.875:
                results.append(s)
    return results
```

---

## 四、回测结果（策略编辑器）

### V2版本（2023-2024）

| 指标 | 数值 |
|------|------|
| 年化收益 | 2.58% |
| 最大回撤 | 4.35% |
| 超额收益 | 14.39% |
| 胜率 | 44.9% |

**问题**：收益偏低，可能是：
- 1月4月空仓影响
- 情绪开关未正确实现
- 选股条件过严

---

## 五、改进计划

### 5.1 立即可做

1. **简化情绪开关**
   - 使用涨停家数>=20（放宽条件）
   - 确保每日正确计算

2. **确认停手机制**
   - 连亏3笔停3天
   - 正确记录交易盈亏

3. **放宽市值范围**
   - 5-200亿（之前10-300亿）

### 5.2 后续优化

1. 加入缩量筛选
2. 加入换手率限制
3. 优化因子权重

---

## 六、关键文件

```
docs/small_cap_research_20260331/
├── README.md                      # 研究框架
├── small_cap_strategy_jq.py       # 原始版策略
├── small_cap_strategy_v2.py       # 优化版
├── small_cap_v4.py                # 简化版
├── notebook_small_cap_test.py     # Notebook验证
└── RESEARCH_SUMMARY.md            # 本文档
```

---

## 七、最终建议

**如果你现在必须做决策，我只给一条：**

> **立即加入情绪开关（涨停>=30）和停手机制（连亏3停3天）**

**理由**：
1. 情绪开关回撤改善40%，是最有效的风控手段
2. 停手机制卡玛提升68%，不降收益
3. 两者规则简单，易于执行
4. 已有充分数据验证

---

## 八、参考文献

- `docs/opportunity_strategies_20260330/result_02_mainline_sentiment_switch_mvp.md`
- `docs/opportunity_strategies_20260330/result_05_mainline_pause_rules.md`
- `docs/opportunity_strategies_20260330/result_07_second_board_rule_redefinition.md`
- `docs/parallel_strategy_tasks_20260328/07_小市值快速参考卡.md`