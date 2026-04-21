# 策略优化技术方案 - 避免过拟合

## 📋 目标

在当前Phase 2基础上优化策略参数和组合构建，同时**严格防止过拟合**

---

## 🎯 核心原则

### 1. 样本外验证 (Out-of-Sample, OOS)
- **永远不用测试集调参**
- 使用Walk-Forward验证
- 保留独立的holdout集

### 2. 交叉验证
- Time Series Cross-Validation
- 避免未来信息泄露
- 多个时间段验证稳定性

### 3. 参数空间约束
- 限制参数搜索范围
- 避免过度优化
- 使用经济学直觉约束

---

## 📊 当前策略参数

### 从Phase 2配置中提取的关键参数

```python
# 因子处理
new_stock_cooldown_days: 60        # 新股冷静期
mad_multiplier: 5.0                # 异常值处理倍数
missing_rate_threshold: 0.3        # 缺失率阈值

# 因子合成
max_single_family_weight: 0.4      # 单因子族最大权重
weight_smoothing_halflife: 4       # 权重平滑半衰期
alpha_reg_grid: [0.001, 0.01, 0.1, 1.0, 10.0]  # 正则化参数
l1_ratio_grid: [0.0, 0.1, 0.5]     # L1/L2比例

# 组合构建
n_stocks: 50                       # 持仓股票数
max_single_weight: 0.03            # 单股最大权重
max_turnover: 0.3                  # 最大换手率

# 回测设置
min_train_periods: 260             # 最小训练周期
test_block: 52                     # 测试块大小
step: 4                            # 滚动步长
embargo: 1                         # 禁运期
holdout_periods: 52                # 留出期数
```

---

## 🔬 优化方案设计

### 阶段1: 参数敏感性分析 (1-2天)

**目标**: 了解哪些参数对结果影响最大

#### 1.1 单参数扫描

对每个参数进行独立扫描，其他参数保持默认值：

```python
# 参数扫描范围
param_ranges = {
    # 组合构建参数（最重要）
    'n_stocks': [30, 40, 50, 60, 80, 100],
    'max_single_weight': [0.02, 0.025, 0.03, 0.04, 0.05],
    'max_turnover': [0.2, 0.25, 0.3, 0.35, 0.4],
    
    # 因子合成参数
    'max_single_family_weight': [0.3, 0.35, 0.4, 0.45, 0.5],
    'weight_smoothing_halflife': [2, 3, 4, 5, 6],
    
    # 因子处理参数
    'mad_multiplier': [3.0, 4.0, 5.0, 6.0, 7.0],
    'new_stock_cooldown_days': [30, 45, 60, 90, 120],
}
```

**验证方法**:
- 使用2015-2024训练
- 在2025验证集上测试
- 2026作为最终holdout（不碰）

**输出**:
- 每个参数的敏感性曲线
- 识别高敏感参数（需要谨慎）
- 识别低敏感参数（可以固定）

#### 1.2 实现代码

```python
# sensitivity_analysis.py
"""
参数敏感性分析 - 单参数扫描
"""

import pandas as pd
import numpy as np
from pathlib import Path
import json
from v2.pipeline import Pipeline, PipelineConfig

def run_sensitivity_analysis():
    """运行单参数敏感性分析"""
    
    # 基准配置
    base_config = PipelineConfig(
        csv_path="train_merged_all_with_2026.csv",
        holdout_periods=104,  # 2025-2026作为holdout
        n_stocks=50,
        max_single_weight=0.03,
        max_turnover=0.3,
        # ... 其他默认参数
    )
    
    # 参数扫描
    param_ranges = {
        'n_stocks': [30, 40, 50, 60, 80, 100],
        'max_single_weight': [0.02, 0.025, 0.03, 0.04, 0.05],
        'max_turnover': [0.2, 0.25, 0.3, 0.35, 0.4],
    }
    
    results = []
    
    for param_name, param_values in param_ranges.items():
        for param_value in param_values:
            # 创建新配置
            config = base_config.copy()
            setattr(config, param_name, param_value)
            
            # 运行pipeline
            pipeline = Pipeline(config)
            result = pipeline.run()
            
            # 在2025验证集上评估
            val_metrics = evaluate_on_validation(result, year=2025)
            
            results.append({
                'param_name': param_name,
                'param_value': param_value,
                'ic_mean': val_metrics['ic_mean'],
                'ic_ir': val_metrics['ic_ir'],
                'annual_return': val_metrics['annual_return'],
                'sharpe': val_metrics['sharpe'],
            })
    
    # 保存结果
    df_results = pd.DataFrame(results)
    df_results.to_csv('output/optimization/sensitivity_analysis.csv')
    
    # 生成可视化报告
    generate_sensitivity_plots(df_results)
```

---

### 阶段2: Walk-Forward优化 (2-3天)

**目标**: 在多个时间窗口上验证参数稳定性

#### 2.1 Walk-Forward设计

```
训练集1: 2015-2020 → 验证集1: 2021
训练集2: 2015-2021 → 验证集2: 2022
训练集3: 2015-2022 → 验证集3: 2023
训练集4: 2015-2023 → 验证集4: 2024
训练集5: 2015-2024 → 验证集5: 2025
最终测试: 2015-2025 → Holdout: 2026
```

**关键点**:
- 每个验证集只用一次
- 参数在所有验证集上平均表现最好
- 避免针对单个时期过度优化

#### 2.2 实现代码

```python
# walk_forward_optimization.py
"""
Walk-Forward参数优化
"""

def walk_forward_optimize():
    """Walk-Forward优化"""
    
    # 定义时间窗口
    windows = [
        {'train_end': 2020, 'val_year': 2021},
        {'train_end': 2021, 'val_year': 2022},
        {'train_end': 2022, 'val_year': 2023},
        {'train_end': 2023, 'val_year': 2024},
        {'train_end': 2024, 'val_year': 2025},
    ]
    
    # 候选参数组合（基于敏感性分析结果）
    param_combinations = [
        {'n_stocks': 40, 'max_turnover': 0.25},
        {'n_stocks': 50, 'max_turnover': 0.3},
        {'n_stocks': 60, 'max_turnover': 0.35},
        # ... 更多组合
    ]
    
    results = []
    
    for params in param_combinations:
        window_results = []
        
        for window in windows:
            # 训练模型
            config = create_config(
                train_end=window['train_end'],
                **params
            )
            pipeline = Pipeline(config)
            result = pipeline.run()
            
            # 在验证集评估
            val_metrics = evaluate_on_year(result, window['val_year'])
            window_results.append(val_metrics)
        
        # 计算平均表现
        avg_metrics = average_metrics(window_results)
        std_metrics = std_metrics(window_results)
        
        results.append({
            'params': params,
            'avg_ic': avg_metrics['ic_mean'],
            'std_ic': std_metrics['ic_mean'],
            'avg_sharpe': avg_metrics['sharpe'],
            'std_sharpe': std_metrics['sharpe'],
            'consistency': calculate_consistency(window_results),
        })
    
    # 选择最稳定的参数组合
    best_params = select_best_params(results)
    
    return best_params
```

---

### 阶段3: 组合构建优化 (2-3天)

**目标**: 优化从因子得分到最终持仓的转换过程

#### 3.1 优化方向

##### A. 持仓数量优化

```python
# 测试不同持仓数
n_stocks_range = [30, 40, 50, 60, 80, 100]

# 评估指标
# - IC不应该随持仓数变化太大（说明因子稳定）
# - 夏普比率可能在某个点最优（分散vs集中）
# - 换手率随持仓数增加而降低
```

##### B. 权重方案优化

当前是等权（1/N），可以测试：

```python
weight_schemes = [
    'equal_weight',           # 等权（当前）
    'ic_weighted',            # 按IC加权
    'volatility_weighted',    # 按波动率倒数加权
    'risk_parity',            # 风险平价
    'min_variance',           # 最小方差
]
```

##### C. 换手率控制优化

```python
# 测试不同换手率约束
turnover_constraints = [0.2, 0.25, 0.3, 0.35, 0.4]

# 评估
# - 换手率vs收益的权衡
# - 考虑交易成本（单边0.2%）
# - 净收益 = 毛收益 - 换手率 * 交易成本
```

#### 3.2 实现代码

```python
# portfolio_optimization.py
"""
组合构建优化
"""

def optimize_portfolio_construction():
    """优化组合构建方法"""
    
    # 加载Phase 2的因子得分
    predictions = load_predictions('output/phase2/oof_predictions_phase2.csv')
    
    # 测试不同组合构建方法
    methods = [
        {'name': 'equal_50', 'n_stocks': 50, 'weight': 'equal'},
        {'name': 'equal_60', 'n_stocks': 60, 'weight': 'equal'},
        {'name': 'ic_weighted_50', 'n_stocks': 50, 'weight': 'ic'},
        {'name': 'risk_parity_50', 'n_stocks': 50, 'weight': 'risk_parity'},
    ]
    
    results = []
    
    for method in methods:
        # 构建组合
        portfolio = build_portfolio(
            predictions,
            n_stocks=method['n_stocks'],
            weight_scheme=method['weight'],
        )
        
        # 回测
        backtest_results = backtest_portfolio(
            portfolio,
            transaction_cost=0.002,  # 单边0.2%
        )
        
        results.append({
            'method': method['name'],
            'gross_return': backtest_results['gross_return'],
            'net_return': backtest_results['net_return'],
            'turnover': backtest_results['turnover'],
            'sharpe': backtest_results['sharpe'],
            'max_drawdown': backtest_results['max_drawdown'],
        })
    
    return pd.DataFrame(results)
```

---

### 阶段4: 过拟合检测 (1-2天)

**目标**: 验证优化后的参数没有过拟合

#### 4.1 检测方法

##### A. 样本外测试

```python
# 最终在2026 holdout上测试
# 如果2026表现显著差于2025，说明过拟合

def overfitting_test():
    """过拟合检测"""
    
    # 优化后的参数
    optimized_params = load_optimized_params()
    
    # 在2025验证集的表现
    val_2025 = evaluate_on_year(optimized_params, 2025)
    
    # 在2026 holdout的表现
    holdout_2026 = evaluate_on_year(optimized_params, 2026)
    
    # 计算衰减
    decay = {
        'ic_decay': (val_2025['ic'] - holdout_2026['ic']) / val_2025['ic'],
        'sharpe_decay': (val_2025['sharpe'] - holdout_2026['sharpe']) / val_2025['sharpe'],
    }
    
    # 判断标准
    # IC衰减 < 20%: 正常
    # IC衰减 20-40%: 轻微过拟合
    # IC衰减 > 40%: 严重过拟合
    
    return decay
```

##### B. 参数稳定性测试

```python
def parameter_stability_test():
    """参数稳定性测试"""
    
    # 在不同时期训练，看参数是否一致
    periods = [
        (2015, 2020),
        (2015, 2021),
        (2015, 2022),
        (2015, 2023),
        (2015, 2024),
    ]
    
    optimal_params = []
    
    for start, end in periods:
        params = optimize_on_period(start, end)
        optimal_params.append(params)
    
    # 计算参数变异系数
    param_cv = calculate_coefficient_of_variation(optimal_params)
    
    # CV < 0.2: 参数稳定
    # CV > 0.5: 参数不稳定，可能过拟合
    
    return param_cv
```

##### C. 随机性测试

```python
def randomness_test():
    """随机性测试 - Bootstrap"""
    
    n_bootstrap = 100
    results = []
    
    for i in range(n_bootstrap):
        # 随机抽样（有放回）
        sampled_data = bootstrap_sample(data)
        
        # 优化参数
        params = optimize(sampled_data)
        
        # 评估
        metrics = evaluate(params)
        results.append(metrics)
    
    # 计算置信区间
    ci_95 = np.percentile(results, [2.5, 97.5])
    
    # 如果置信区间很宽，说明结果不稳定
    
    return ci_95
```

#### 4.2 过拟合判断标准

| 指标 | 正常 | 轻微过拟合 | 严重过拟合 |
|------|------|-----------|-----------|
| **样本外衰减** | < 20% | 20-40% | > 40% |
| **参数CV** | < 0.2 | 0.2-0.5 | > 0.5 |
| **时期一致性** | > 80% | 60-80% | < 60% |
| **Bootstrap CI宽度** | < 30% | 30-50% | > 50% |

---

## 🎯 完整实施流程

### Week 1: 准备和敏感性分析

**Day 1-2**: 
- [ ] 设计数据分割方案
- [ ] 实现敏感性分析框架
- [ ] 运行单参数扫描

**Day 3-4**:
- [ ] 分析敏感性结果
- [ ] 识别关键参数
- [ ] 确定参数搜索空间

### Week 2: Walk-Forward优化

**Day 5-7**:
- [ ] 实现Walk-Forward框架
- [ ] 运行多窗口优化
- [ ] 选择稳定参数组合

**Day 8-9**:
- [ ] 组合构建方法测试
- [ ] 权重方案对比
- [ ] 换手率优化

### Week 3: 验证和测试

**Day 10-11**:
- [ ] 过拟合检测
- [ ] 稳定性测试
- [ ] Bootstrap验证

**Day 12-13**:
- [ ] 在2026 holdout最终测试
- [ ] 生成完整报告
- [ ] 参数确定

**Day 14**:
- [ ] 代码整理
- [ ] 文档编写
- [ ] 结果展示

---

## 📊 评估指标体系

### 主要指标

```python
primary_metrics = {
    'ic_mean': 'IC均值',
    'ic_ir': 'IC信息比率',
    'annual_return': '年化收益',
    'sharpe_ratio': '夏普比率',
    'max_drawdown': '最大回撤',
}
```

### 稳定性指标

```python
stability_metrics = {
    'ic_consistency': 'IC一致性（IC>0的比例）',
    'period_correlation': '不同时期表现相关性',
    'parameter_cv': '参数变异系数',
    'oos_decay': '样本外衰减率',
}
```

### 综合评分

```python
def calculate_score(metrics):
    """综合评分 - 平衡收益和稳定性"""
    
    score = (
        0.3 * normalize(metrics['ic_ir']) +
        0.2 * normalize(metrics['sharpe_ratio']) +
        0.2 * normalize(metrics['annual_return']) +
        0.15 * normalize(metrics['ic_consistency']) +
        0.15 * (1 - normalize(metrics['oos_decay']))
    )
    
    return score
```

---

## 🚨 风险控制

### 1. 参数约束

```python
# 硬约束 - 基于经济学直觉
constraints = {
    'n_stocks': (20, 150),           # 太少分散不够，太多稀释alpha
    'max_single_weight': (0.01, 0.1), # 单股权重合理范围
    'max_turnover': (0.1, 0.5),       # 换手率合理范围
    'max_single_family_weight': (0.2, 0.6),  # 因子族权重
}
```

### 2. 优化次数限制

```python
# 限制参数搜索次数，避免过度优化
max_iterations = 50  # 最多50次参数组合测试
```

### 3. 正则化

```python
# 在优化目标中加入正则化项
def objective_with_regularization(params):
    """带正则化的目标函数"""
    
    # 主要目标
    performance = evaluate_performance(params)
    
    # 正则化项 - 惩罚复杂度
    complexity_penalty = calculate_complexity(params)
    
    # 稳定性奖励
    stability_bonus = calculate_stability(params)
    
    return performance - 0.1 * complexity_penalty + 0.1 * stability_bonus
```

---

## 📝 输出文档

### 1. 敏感性分析报告
- `output/optimization/sensitivity_analysis.csv`
- `output/optimization/sensitivity_plots/`

### 2. Walk-Forward结果
- `output/optimization/walk_forward_results.csv`
- `output/optimization/optimal_params.json`

### 3. 过拟合检测报告
- `output/optimization/overfitting_test.txt`
- `output/optimization/stability_metrics.json`

### 4. 最终报告
- `output/optimization/OPTIMIZATION_FINAL_REPORT.md`

---

## 🎓 理论支持

### 为什么这个方案能避免过拟合？

1. **时间序列交叉验证**: 
   - 严格的时间顺序
   - 多个独立验证集
   - 避免look-ahead bias

2. **样本外测试**:
   - 2026作为真正的holdout
   - 从未用于任何优化决策

3. **参数稳定性**:
   - 在多个时期验证
   - 选择稳定的参数
   - 避免针对特定时期优化

4. **正则化约束**:
   - 限制参数空间
   - 经济学直觉约束
   - 复杂度惩罚

5. **统计检验**:
   - Bootstrap置信区间
   - 参数变异系数
   - 衰减率检测

---

## 💡 实施建议

### 优先级

**高优先级** (必做):
1. ✅ 敏感性分析 - 了解参数影响
2. ✅ Walk-Forward优化 - 验证稳定性
3. ✅ 2026 holdout测试 - 最终验证

**中优先级** (推荐):
4. 组合构建优化 - 可能有显著提升
5. 过拟合检测 - 确保结果可靠

**低优先级** (可选):
6. Bootstrap测试 - 额外验证
7. 参数可视化 - 更好理解

### 时间分配

- **快速版本** (1周): 只做敏感性分析 + 简单Walk-Forward
- **标准版本** (2周): 完整流程，不含Bootstrap
- **完整版本** (3周): 所有测试和验证

---

## 🔧 代码框架

我会为你创建以下文件：

1. `sensitivity_analysis.py` - 敏感性分析
2. `walk_forward_optimization.py` - Walk-Forward优化
3. `portfolio_optimization.py` - 组合构建优化
4. `overfitting_detection.py` - 过拟合检测
5. `optimization_utils.py` - 工具函数
6. `run_full_optimization.py` - 主控脚本

---

## ✅ 成功标准

优化成功的标志：

1. **性能提升**: 
   - 2025验证集IC IR提升 > 5%
   - 2026 holdout IC IR提升 > 3%

2. **稳定性保持**:
   - 样本外衰减 < 20%
   - 参数CV < 0.3
   - 时期一致性 > 70%

3. **实用性**:
   - 换手率可控 (< 40%)
   - 参数简单易理解
   - 可解释性强

---

**准备好开始了吗？我可以先帮你实现敏感性分析框架！**
