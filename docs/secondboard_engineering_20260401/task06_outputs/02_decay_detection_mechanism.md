# 衰退检测机制设计

## 一、衰退定义

### 1.1 衰退概念界定

策略衰退是指策略在实际应用中的表现持续低于历史回测表现（样本内表现）的现象。衰退可能源于：
- **过拟合风险**：策略在样本内过度拟合，样本外表现自然衰减
- **市场环境变化**：市场结构、参与者行为、监管环境变化导致策略失效
- **策略拥挤**：同类策略参与者增加，降低策略有效性
- **流动性变化**：目标标的流动性变化影响策略执行

### 1.2 衰退分级定义

| 衰退级别 | 定义 | 表现下降幅度 | 持续时间要求 | 检测方法 |
|---------|------|------------|------------|---------|
| 无衰退 | 表现稳定 | <10% | 无要求 | 持续达标 |
| 轻度衰退 | 略有下降 | 10-20% | 持续2周以上 | 阈值+趋势 |
| 中度衰退 | 明显下降 | 20-40% | 持续1个月以上 | 阈值+统计检验 |
| 重度衰退 | 严重下降 | >40% | 持续1个月以上 | 阈值+统计检验 |
| 失效 | 策略失效 | 显著为负 | 持续1个月以上 | 统计检验（p<0.05） |

**说明**：
- 表现下降幅度计算：`(OOS表现 - IS表现) / IS表现`
- 持续时间要求：衰退状态需持续一定时间才能确认，避免短期波动误判
- 衰退级别可叠加：如表现下降30%且持续2周，判定为中度衰退观察期

## 二、衰退检测指标体系

### 2.1 核心检测指标

#### 2.1.1 收益指标衰退

| 指标 | IS表现基准 | 正常范围 | 观察范围 | 警告范围 | 失效阈值 |
|------|-----------|---------|---------|---------|---------|
| 年化收益 | 394% | >300% | 200-300% | <200% | <50% |
| 月度收益 | 30%+ | >20% | 10-20% | <10% | <0% |
| 超额收益（vs沪深300） | 350%+ | >250% | 150-250% | <150% | <0% |

#### 2.1.2 质量指标衰退

| 指标 | IS表现基准 | 正常范围 | 观察范围 | 警告范围 | 失效阈值 |
|------|-----------|---------|---------|---------|---------|
| 胜率 | 87.95% | >80% | 70-80% | <70% | <60% |
| 盈亏比 | 21.91 | >15 | 10-15 | <10 | <5 |
| 信号命中率 | 85%+ | >70% | 60-70% | <60% | <50% |

#### 2.1.3 风险指标恶化

| 指标 | IS表现基准 | 正常范围 | 观察范围 | 警告范围 | 失效阈值 |
|------|-----------|---------|---------|---------|---------|
| 最大回撤 | 0.60% | <10% | 10-15% | >15% | >25% |
| 波动率 | 2% | <3% | 3-5% | >5% | >10% |
| 回撤持续时间 | 2天 | <30天 | 30-60天 | >60天 | >120天 |

#### 2.1.4 风险调整收益衰退

| 指标 | IS表现基准 | 正常范围 | 观察范围 | 警告范围 | 失效阈值 |
|------|-----------|---------|---------|---------|---------|
| 夏普比率 | 20+ | >3.0 | 1.5-3.0 | <1.5 | <1.0 |
| 卡玛比率 | 30+ | >10 | 5-10 | <5 | <2 |

### 2.2 辅助检测指标

#### 2.2.1 信号质量变化

| 指标 | 正常范围 | 观察范围 | 警告范围 | 检测意义 |
|------|---------|---------|---------|---------|
| 月信号数量 | 10-30次 | 5-10次或30-40次 | <5次或>40次 | 信号生成异常 |
| 信号命中率 | >70% | 60-70% | <60% | 信号质量下降 |
| 信号平均收益 | >5% | 2-5% | <2% | 信号有效性下降 |

#### 2.2.2 交易质量变化

| 指标 | 正常范围 | 观察范围 | 警告范围 | 检测意义 |
|------|---------|---------|---------|---------|
| 月交易频率 | 10-30次 | 5-10次 | <5次 | 交易机会减少 |
| 平均持仓时长 | 1-3天 | 3-5天 | >5天 | 持仓效率下降 |
| 单笔平均收益 | >5% | 2-5% | <2% | 收益质量下降 |

#### 2.2.3 市场环境变化

| 指标 | 正常范围 | 观察范围 | 警告范围 | 检测意义 |
|------|---------|---------|---------|---------|
| 情绪指标 | 正常波动 | 略有变化 | 显著变化 | 策略适应性问题 |
| 涨跌停数量 | 正常水平 | 略有偏离 | 显著偏离 | 市场结构变化 |
| 连板数量分布 | 正常分布 | 略有变化 | 分布异常 | 板块接力环境变化 |

## 三、衰退检测方法

### 3.1 阈值法

**原理**：指标低于预设阈值即触发预警

**优点**：简单直观，反应迅速

**缺点**：可能误判短期波动

**实现逻辑**：
```python
def threshold_detection(current_value, is_baseline, thresholds):
    """
    阈值法衰退检测
    
    参数:
    - current_value: 当前指标值
    - is_baseline: IS表现基准值
    - thresholds: 各级别阈值字典
    
    返回:
    - alert_level: 预警级别
    - deviation: 偏离程度
    """
    # 计算衰减比例
    decay_ratio = (current_value - is_baseline) / is_baseline
    
    # 判断预警级别
    if decay_ratio > -0.1:  # 衰减<10%
        return "green", decay_ratio
    elif decay_ratio > -0.2:  # 衰减10-20%
        return "yellow", decay_ratio
    elif decay_ratio > -0.4:  # 衰退20-40%
        return "orange", decay_ratio
    else:  # 衰退>40%
        return "red", decay_ratio
```

### 3.2 趋势法

**原理**：指标持续恶化触发预警

**优点**：识别趋势性衰退，避免短期波动误判

**缺点**：反应较慢，需要一定观察期

**实现逻辑**：
```python
def trend_detection(indicator_series, window=20):
    """
    趋势法衰退检测
    
    参数:
    - indicator_series: 指标历史序列
    - window: 观察窗口长度
    
    返回:
    - trend_direction: 趋势方向（上升/下降/平稳）
    - deterioration_days: 连续恶化天数
    """
    # 提取最近window日数据
    recent_values = indicator_series[-window:]
    
    # 计算趋势方向
    slope = np.polyfit(range(window), recent_values, 1)[0]
    
    # 统计连续恶化天数
    deterioration_count = 0
    for i in range(window-1):
        if recent_values[i+1] < recent_values[i]:
            deterioration_count += 1
        else:
            deterioration_count = 0
    
    # 判断趋势状态
    if slope > 0 and deterioration_count < 5:
        return "rising", deterioration_count, "green"
    elif slope > -0.1 and deterioration_count < 10:
        return "stable", deterioration_count, "yellow"
    else:
        return "declining", deterioration_count, "orange"
```

### 3.3 统计法

**原理**：与历史表现差异显著触发预警

**优点**：科学严谨，显著性检验有统计依据

**缺点**：需要足够样本量，计算复杂

**实现逻辑**：
```python
def statistical_detection(current_series, historical_series, confidence=0.95):
    """
    统计法衰退检测
    
    参数:
    - current_series: 当前OOS表现序列
    - historical_series: IS表现序列
    - confidence: 显著性水平
    
    返回:
    - is_significant: 是否显著衰退
    - p_value: p值
    - effect_size: 效应量
    """
    # 计算均值和标准差
    current_mean = np.mean(current_series)
    current_std = np.std(current_series)
    historical_mean = np.mean(historical_series)
    historical_std = np.std(historical_series)
    
    # t检验
    n_current = len(current_series)
    n_historical = len(historical_series)
    
    pooled_std = np.sqrt(
        (current_std**2 + historical_std**2) / 2
    )
    
    t_stat = (current_mean - historical_mean) / (
        pooled_std * np.sqrt(1/n_current + 1/n_historical)
    )
    
    # 计算p值（双尾检验）
    p_value = 2 * (1 - t.cdf(abs(t_stat), df=n_current+n_historical-2))
    
    # Cohen's d效应量
    effect_size = (current_mean - historical_mean) / pooled_std
    
    # 判断显著性
    alpha = 1 - confidence
    is_significant = p_value < alpha
    
    # 根据效应量判断衰退程度
    if abs(effect_size) < 0.2:
        severity = "negligible"
    elif abs(effect_size) < 0.5:
        severity = "small"
    elif abs(effect_size) < 0.8:
        severity = "medium"
    else:
        severity = "large"
    
    return {
        'is_significant': is_significant,
        'p_value': p_value,
        'effect_size': effect_size,
        'severity': severity,
        'alert_level': "red" if is_significant and current_mean < historical_mean else "green"
    }
```

### 3.4 排名法（可选）

**原理**：在同类策略中排名下降触发预警

**优点**：横向对比，识别相对衰退

**缺点**：需要同类策略池，实施难度较大

**实现逻辑**：
```python
def ranking_detection(current_rank, historical_rank, threshold=5):
    """
    排名法衰退检测
    
    参数:
    - current_rank: 当前在同类策略中的排名
    - historical_rank: 历史平均排名
    - threshold: 排名下降阈值
    
    返回:
    - rank_change: 排名变化
    - alert_level: 预警级别
    """
    rank_change = current_rank - historical_rank
    
    if rank_change <= 0:
        return rank_change, "green"
    elif rank_change <= threshold:
        return rank_change, "yellow"
    elif rank_change <= 2*threshold:
        return rank_change, "orange"
    else:
        return rank_change, "red"
```

## 四、预警级别判定规则

### 4.1 四级预警体系

| 预警级别 | 级别名称 | 预警颜色 | 状态描述 | 核心特征 |
|---------|---------|---------|---------|---------|
| Level 0 | 正常 | 绿色 | 表现符合预期 | 所有指标正常范围 |
| Level 1 | 观察 | 黄色 | 表现略有下降，需观察 | 个别指标进入观察范围 |
| Level 2 | 警告 | 橙色 | 表现明显下降，需评估 | 多个指标进入警告范围 |
| Level 3 | 降级/暂停 | 红色 | 表现严重下降，需降级/暂停 | 关键指标严重衰退或失效 |

### 4.2 预警触发规则矩阵

| 预警级别 | 触发条件（单一指标） | 触发条件（多指标组合） | 持续时间要求 | 确认条件 |
|---------|-------------------|---------------------|------------|---------|
| 绿色 | 所有指标正常范围 | - | - | - |
| 黄色 | 任一指标进入观察范围 | 2个指标观察范围 | 持续≥2周 | 连续3次验证黄色 |
| 橙色 | 任一指标进入警告范围 | 2个指标警告范围 | 持续≥1个月 | 连续4次验证橙色 |
| 红色 | 任一指标失效 | 收益显著为负（p<0.05） | 持续≥1个月 | 统计检验确认 |

### 4.3 预警判定逻辑

```python
def determine_alert_level(metrics_status, duration_days):
    """
    综合判定预警级别
    
    参数:
    - metrics_status: 各指标状态字典
      {
        'annual_return': 'warning',
        'win_rate': 'normal',
        'max_drawdown': 'observation',
        ...
      }
    - duration_days: 异常持续天数
    
    返回:
    - alert_level: 最终预警级别
    - triggered_metrics: 触发预警的指标列表
    """
    # 统计各级别指标数量
    normal_count = sum(1 for s in metrics_status.values() if s == 'normal')
    observation_count = sum(1 for s in metrics_status.values() if s == 'observation')
    warning_count = sum(1 for s in metrics_status.values() if s == 'warning')
    failure_count = sum(1 for s in metrics_status.values() if s == 'failure')
    
    # 判定预警级别
    triggered_metrics = []
    
    if failure_count > 0:
        alert_level = "red"
        triggered_metrics = [k for k,v in metrics_status.items() if v == 'failure']
    
    elif warning_count >= 2 and duration_days >= 30:
        alert_level = "red"
        triggered_metrics = [k for k,v in metrics_status.items() if v in ['warning', 'failure']]
    
    elif warning_count > 0 and duration_days >= 30:
        alert_level = "orange"
        triggered_metrics = [k for k,v in metrics_status.items() if v == 'warning']
    
    elif observation_count >= 2 and duration_days >= 14:
        alert_level = "orange"
        triggered_metrics = [k for k,v in metrics_status.items() if v == 'observation']
    
    elif observation_count > 0 and duration_days >= 14:
        alert_level = "yellow"
        triggered_metrics = [k for k,v in metrics_status.items() if v == 'observation']
    
    else:
        alert_level = "green"
        triggered_metrics = []
    
    return alert_level, triggered_metrics
```

### 4.4 预警升降机制

**升级机制**：
- 连续3次验证触发黄色 → 升级为橙色（需评估）
- 连续4次验证触发橙色 → 升级为红色（需降级）
- 单次触发红色指标 → 立即升级为红色

**降级机制**：
- 连续5次验证绿色 → 从黄色降级为绿色
- 连续8次验证绿色 → 从橙色降级为黄色
- 需人工确认才能从红色降级

## 五、应对措施清单

### 5.1 分级应对措施

| 预警级别 | 应对措施 | 具体操作 | 持续时间 | 仓位调整 |
|---------|---------|---------|---------|---------|
| 绿色 | 正常执行 | 按原策略正常执行 | - | 维持原仓位（30-40%） |
| 黄色 | 加强监控 | 1. 增加验证频率至日频<br>2. 每日人工审核交易<br>3. 准备应对预案<br>4. 分析衰退原因 | 观察2周 | 维持原仓位，准备降仓 |
| 橙色 | 评估降仓 | 1. 立即降低仓位50%<br>2. 暂停新开仓（只卖出）<br>3. 深度分析衰退原因<br>4. 制定改进方案<br>5. 风控部门介入 | 评估1个月 | 降至15-20% |
| 红色 | 暂停策略 | 1. 立即暂停策略执行<br>2. 清空所有持仓<br>3. 全面复盘分析<br>4. 重新评估策略有效性<br>5. 决定是否重启或废弃 | 暂停≥1个月 | 清空仓位（0%） |

### 5.2 应对措施执行流程

#### 绿色（正常）

**触发条件**：所有指标正常范围

**执行流程**：
```
1. 按原策略参数正常执行
2. 维持原仓位水平（30-40%）
3. 按原验证频率（周频）监控
4. 定期生成月报、季报
```

**责任分工**：
- 策略执行：交易员
- 监控验证：风控专员
- 报告审核：策略主管

#### 黄色（观察）

**触发条件**：个别指标观察范围，持续≥2周

**执行流程**：
```
Day 1（触发日）：
1. 发出黄色预警通知
2. 增加验证频率至日频
3. 每日人工审核交易信号
4. 启动衰退原因分析

Week 1-2（观察期）：
1. 每日生成日报并人工审核
2. 深入分析衰退原因：
   - 市场环境变化？
   - 参数适应性？
   - 执行偏差？
   - 过拟合？
3. 准备应对预案（降仓方案）

Week 2结束：
1. 评估观察期表现
2. 如恢复正常 → 降级为绿色
3. 如持续恶化 → 升级为橙色
```

**责任分工**：
- 信号审核：交易员+策略主管
- 原因分析：策略开发团队
- 预案准备：风控部门
- 决策确认：策略委员会

#### 橙色（警告）

**触发条件**：多个指标警告范围，持续≥1个月

**执行流程**：
```
Day 1（触发日）：
1. 发出橙色警告通知
2. 立即降低仓位至50%（15-20%）
3. 暂停新开仓操作（只执行卖出）
4. 风控部门介入监督

Month 1（评估期）：
1. 维持降仓状态执行
2. 深度分析衰退根本原因：
   - 回测历史数据验证
   - 参数敏感性分析
   - 市场环境对比分析
   - 竞品策略对比分析
3. 制定改进方案：
   - 参数调整方案
   - 规则优化方案
   - 新策略替代方案

Month 1结束：
1. 评估改进方案可行性
2. 决策：
   - 方案可行 → 实施改进，逐步恢复仓位
   - 方案不可行 → 升级为红色，暂停策略
3. 如表现恢复 → 可降级为黄色
```

**责任分工**：
- 仓位调整：交易员（风控监督）
- 深度分析：策略开发团队+外部专家
- 改进方案：策略开发团队
- 决策审批：策略委员会

#### 红色（降级/暂停）

**触发条件**：关键指标失效或收益显著为负

**执行流程**：
```
Day 1（触发日）：
1. 发出红色紧急通知
2. 立即暂停策略执行
3. 开始清空所有持仓
4. 禁止任何新开仓操作

Week 1-4（复盘期）：
1. 全面复盘分析：
   - 策略历史表现回顾
   - 衰退全过程梳理
   - 根本原因深度剖析
   - 失效性质判定：
     * 过拟合失效？
     * 市场环境失效？
     * 执行问题失效？
2. 策略有效性重新评估：
   - 是否有改进价值？
   - 是否需要重新设计？
   - 是否应废弃策略？
3. 制定重启方案或替代方案：
   - 如有改进价值 → 制定重启方案
   - 如应废弃 → 制定替代策略方案

Month 1结束：
1. 策略委员会决策：
   - 重启策略（需严格验证）
   - 废弃策略（移至历史策略库）
   - 替代策略（启动新策略验证）
```

**责任分工**：
- 策略暂停：风控部门（强制执行）
- 全面复盘：策略开发团队+风控团队+外部专家
- 有效性评估：策略委员会
- 最终决策：投资决策委员会

### 5.3 异常情况快速响应流程

```python
def emergency_response(alert_level, triggered_metrics):
    """
    异常情况快速响应
    
    参数:
    - alert_level: 当前预警级别
    - triggered_metrics: 触发预警的指标
    
    返回:
    - response_actions: 响应措施列表
    - execution_priority: 执行优先级
    """
    response_actions = []
    
    # 根据预警级别制定响应措施
    if alert_level == "red":
        response_actions = [
            {"action": "pause_strategy", "priority": 1, "executor": "风控部"},
            {"action": "clear_positions", "priority": 2, "executor": "交易员"},
            {"action": "emergency_notification", "priority": 1, "executor": "风控部"},
            {"action": "full_review", "priority": 3, "executor": "策略团队"}
        ]
    
    elif alert_level == "orange":
        response_actions = [
            {"action": "reduce_position_50pct", "priority": 1, "executor": "交易员"},
            {"action": "stop_new_open", "priority": 2, "executor": "交易员"},
            {"action": "deep_analysis", "priority": 3, "executor": "策略团队"},
            {"action": "improvement_plan", "priority": 4, "executor": "策略团队"}
        ]
    
    elif alert_level == "yellow":
        response_actions = [
            {"action": "increase_monitor_frequency", "priority": 1, "executor": "风控专员"},
            {"action": "manual_review_signals", "priority": 2, "executor": "策略主管"},
            {"action": "analyze_decay_reason", "priority": 3, "executor": "策略团队"},
            {"action": "prepare_contingency_plan", "priority": 4, "executor": "风控部"}
        ]
    
    return response_actions
```

## 六、衰退检测实例模拟

### 6.1 模拟场景1：轻度衰退

**场景设定**：
- 时间：2026年1月
- 表现：年化收益从394%降至350%（衰减11.4%）
- 胜率：从87.95%降至82%（正常范围）
- 回撤：从0.6%升至3%（正常范围）

**检测过程**：
```
Week 1：
- 年化收益进入观察范围（350%，衰减11.4%）
- 其他指标正常
- 预警级别：黄色
- 应对：加强监控，每日审核

Week 2：
- 年化收益持续观察范围（340%，衰减13.9%）
- 胜率略有下降（80%，仍正常）
- 预警级别：黄色（持续）
- 应对：继续观察，分析原因

Week 3：
- 年化收益恢复至380%（衰减<10%）
- 预警级别：降级为绿色
- 结论：短期波动，已恢复
```

### 6.2 模拟场景2：中度衰退

**场景设定**：
- 时间：2026年2-3月
- 表现：年化收益从394%降至280%（衰减29.2%）
- 胜率：从87.95%降至75%（观察范围）
- 回撤：从0.6%升至8%（观察范围）

**检测过程**：
```
Week 1-2：
- 年化收益进入观察范围（300%，衰减23.9%）
- 胜率进入观察范围（78%）
- 回撤进入观察范围（5%）
- 预警级别：黄色

Month 1：
- 年化收益持续恶化（280%，衰减29.2%）
- 进入警告范围
- 胜率持续观察（75%）
- 回撤持续观察（8%）
- 预警级别：升级为橙色
- 应对：降仓50%，暂停新开仓

Month 2：
- 深度分析发现：市场风格切换，小票表现下降
- 制定改进方案：增加情绪开关过滤
- 实施改进方案
- 表现逐步恢复

Month 3：
- 年化收益恢复至320%（衰减18.8%）
- 预警级别：降级为黄色
- 逐步恢复仓位至正常
```

### 6.3 模拟场景3：重度衰退

**场景设定**：
- 时间：2026年4-6月
- 表现：年化收益从394%降至150%（衰减62%）
- 胜率：从87.95%降至65%（警告范围）
- 回撤：从0.6%升至15%（警告范围）
- 统计检验：收益显著为负（p=0.03）

**检测过程**：
```
Month 1-2：
- 年化收益持续恶化（280%，衰减29.2%）
- 进入警告范围
- 预警级别：橙色
- 应对：降仓50%

Month 3：
- 年化收益继续恶化（150%，衰减62%）
- 进入失效范围
- 统计检验：收益显著为负（p=0.03）
- 预警级别：升级为红色
- 应对：立即暂停策略，清空持仓

Month 3-4：
- 全面复盘分析
- 发现：策略逻辑失效，过拟合严重
- 结论：策略废弃，启动替代策略验证
```

## 七、衰退检测误报率控制

### 7.1 误报来源分析

| 误报类型 | 原因 | 特征 | 预防措施 |
|---------|------|------|---------|
| 短期波动误报 | 市场短期波动 | 单次触发，快速恢复 | 增加持续时间要求 |
| 单指标误报 | 单指标偶然异常 | 其他指标正常 | 多指标组合判定 |
| 基准偏移误报 | 基准数据异常 | 基准数据检查异常 | 基准数据质量检查 |
| 数据异常误报 | 数据质量问题 | 数据检查异常 | 数据质量前置检查 |

### 7.2 误报率控制措施

**措施1：持续时间要求**
- 黄色预警需持续≥2周
- 橙色预警需持续≥1个月
- 红色预警需持续≥1个月或统计检验确认

**措施2：多指标组合判定**
- 单指标观察 → 黄色观察
- 2个指标观察 → 黄色确认
- 2个指标警告 → 橙色确认
- 多指标失效 → 红色确认

**措施3：统计检验确认**
- 红色预警必须经过统计检验确认
- p值<0.05才能确认失效

**措施4：人工复核机制**
- 黄色预警由策略主管复核
- 橙色预警由策略委员会复核
- 红色预警由投资决策委员会复核

### 7.3 误报率评估目标

| 预警级别 | 目标误报率 | 测量方法 |
|---------|-----------|---------|
| 黄色 | <20% | 黄色预警中后续恢复正常的比例 |
| 橙色 | <10% | 橙色预警中后续恢复的比例 |
| 红色 | <5% | 红色预警中后续重启的比例 |

## 八、衰退检测报告模板

### 8.1 衰退检测日报模板

```markdown
## 二板接力策略衰退检测日报 - YYYY-MM-DD

### 1. 预警状态
- **当前预警级别**: [绿色/黄色/橙色/红色]
- **异常持续天数**: [X天]
- **触发指标**: [指标1, 指标2, ...]

### 2. 核心指标检测

| 指标 | 当前值 | IS基准 | 状态 | 偏离度 |
|------|--------|--------|------|--------|
| 年化收益 | [X%] | 394% | [正常/观察/警告/失效] | [X%] |
| 胜率 | [X%] | 87.95% | [状态] | [X%] |
| 最大回撤 | [X%] | 0.60% | [状态] | [X%] |
| 夏普比率 | [X] | 20+ | [状态] | [X%] |

### 3. 应对措施执行
- [措施1]: [执行状态]
- [措施2]: [执行状态]

### 4. 衰退原因分析（如有异常）
- [原因分析]

### 5. 下一步计划
- [具体计划]
```

### 8.2 衰退检测月报模板

```markdown
## 二板接力策略衰退检测月报 - YYYY-MM

### 1. 月度预警状态变化

| 日期 | 预警级别 | 主要触发指标 | 应对措施 | 状态变化 |
|------|---------|------------|---------|---------|
| MM-DD | [级别] | [指标] | [措施] | [升级/降级/维持] |

### 2. 月度衰退趋势分析
- **衰退开始时间**: [YYYY-MM-DD]
- **衰退持续时间**: [X天]
- **衰退程度**: [轻度/中度/重度]
- **主要衰退指标**: [指标列表]
- **衰退原因**: [原因分析]

### 3. 月度应对措施回顾
- **已执行措施**: [措施列表]
- **措施效果评估**: [效果描述]
- **改进方案**: [方案描述]

### 4. 下月预警目标
- **预警级别目标**: [级别]
- **重点监控指标**: [指标列表]
- **改进计划**: [计划]
```

## 九、总结

本衰退检测机制具有以下特点：

1. **分级科学**：四级衰退定义清晰，与应对措施对应
2. **指标全面**：核心指标+辅助指标，全方位检测
3. **方法多样**：阈值+趋势+统计+排名，多种方法互补
4. **预警明确**：四级预警体系，触发规则清晰
5. **应对具体**：分级应对措施，执行流程完整
6. **误报可控**：持续时间+多指标+统计检验，误报率可控

该机制能够及时发现策略衰退，保护投资本金，指导策略改进，确保策略长期有效性。