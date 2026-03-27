# ETF轮动策略统一研究框架 - 项目总结

## 项目概述

基于聚宽有价值策略558个notebook的ETF轮动研究，搭建的标准化研究框架。

## 已完成工作

### P0: 搭建统一ETF轮动研究骨架 ✓

**完成时间**: 2026-03-27

**核心成果**:
- 创建了完整的项目结构
- 实现了6个核心模块：
  - `pool_builder.py` - 候选池构建模块
  - `factor_calculator.py` - 因子计算模块
  - `timing_filter.py` - 择时过滤模块
  - `strategy.py` - 策略模块
  - `backtest_engine.py` - 回测引擎模块
  - `config.py` - 统一配置文件

**技术实现**:
- 基于notebook 66和86的候选池构建逻辑
- 基于notebook 43的动量因子计算
- 基于notebook 52、59、60的择时过滤逻辑
- 完整的回测引擎和绩效评估

### P1: 候选池模块版本化 ✓

**完成时间**: 2026-03-27

**核心成果**:
- 创建了`pool_version_manager.py`版本管理模块
- 实现了候选池版本的保存、加载、对比功能
- 支持版本元数据管理

**功能特性**:
- 版本创建和保存
- 版本加载和查询
- 版本对比分析
- 版本导出和删除
- 版本报告生成

### P2: 建立统一因子对比实验 ✓

**完成时间**: 2026-03-27

**核心成果**:
- 创建了`factor_comparison.py`因子对比模块
- 实现了因子IC分析和对比功能
- 支持多种因子类型的对比

**功能特性**:
- 因子IC计算
- 因子对比分析
- 因子半衰期计算
- 可视化对比图表
- 对比报告生成

## 项目结构

```
etf_rotation_framework/
├── config.py                    # 统一配置文件
├── main.py                      # 主程序入口
├── README.md                    # 项目说明
├── modules/
│   ├── __init__.py             # 模块初始化
│   ├── pool_builder.py         # 候选池构建模块
│   ├── factor_calculator.py    # 因子计算模块
│   ├── timing_filter.py        # 择时过滤模块
│   ├── strategy.py             # 策略模块
│   ├── backtest_engine.py      # 回测引擎模块
│   ├── pool_version_manager.py # 候选池版本管理模块
│   └── factor_comparison.py    # 因子对比实验模块
├── examples/
│   └── usage_example.ipynb     # 使用示例
└── pool_versions/              # 候选池版本存储目录
```

## 核心模块说明

### 1. 候选池构建模块 (pool_builder.py)
- **基于**: notebook 66和86
- **功能**: 
  - 流动性过滤（成交额 > 1000万）
  - KMeans聚类去重（24个簇）
  - 相关性过滤（相关系数 > 0.85）
- **配置参数**: 
  - `start_date_threshold`: ETF成立时间阈值
  - `min_avg_volume`: 最低成交额
  - `n_clusters`: 聚类簇数
  - `corr_threshold`: 相关系数阈值

### 2. 因子计算模块 (factor_calculator.py)
- **基于**: notebook 43
- **功能**:
  - 斜率动量因子（线性回归斜率）
  - 收益率动量因子（N日累计收益率）
  - IC分析（信息系数）
  - 因子半衰期计算

### 3. 择时过滤模块 (timing_filter.py)
- **基于**: notebook 52、59、60
- **功能**:
  - 市场宽度计算
  - RSRS择时（原始/钝化版本）
  - 综合择时信号生成

### 4. 策略模块 (strategy.py)
- **功能**:
  - 整合候选池、因子、择时
  - 每日持仓信号生成
  - 换手率计算

### 5. 回测引擎模块 (backtest_engine.py)
- **功能**:
  - 完整回测流程
  - 绩效指标计算
  - 可视化输出
  - 回测报告生成

### 6. 候选池版本管理模块 (pool_version_manager.py)
- **功能**:
  - 版本创建和保存
  - 版本加载和查询
  - 版本对比分析
  - 版本导出和删除

### 7. 因子对比实验模块 (factor_comparison.py)
- **功能**:
  - 因子IC计算
  - 因子对比分析
  - 因子半衰期计算
  - 可视化对比图表

## 配置文件说明

config.py 包含所有参数配置：

```python
# 候选池构建参数
POOL_CONFIG = {
    'start_date_threshold': '2021-01-01',
    'min_avg_volume': 1e7,
    'n_clusters': 24,
    'corr_threshold': 0.85,
    ...
}

# 因子计算参数
FACTOR_CONFIG = {
    'momentum_windows': [3, 5, 10, 20, 30, 60],
    'ic_forward_periods': [1, 5, 10, 20, 30, 60, 90],
    ...
}

# 择时过滤参数
TIMING_CONFIG = {
    'breadth_window': 20,
    'rsrs_window': 60,
    'timing_mode': 'combined',
    ...
}

# 策略执行参数
STRATEGY_CONFIG = {
    'hold_count': 5,
    'hold_period': 10,
    'commission_rate': 0.0003,
    ...
}
```

## 使用示例

### 在聚宽环境中运行

```python
from modules import ETFPoolBuilder, FactorCalculator, TimingFilter, BacktestEngine, RotationStrategy
from jqdata import *

# 1. 构建候选池
pool_builder = ETFPoolBuilder()
pool = pool_builder.build_pool(get_all_securities, get_price)

# 2. 计算因子
factor_calculator = FactorCalculator()
momentum = factor_calculator.calculate_momentum(prices)

# 3. 运行策略
strategy = RotationStrategy(pool_builder, factor_calculator, TimingFilter())
results = strategy.run(prices, all_stock_prices=all_stock_prices)

# 4. 回测
backtest_engine = BacktestEngine()
backtest_results = backtest_engine.run_backtest(prices, strategy.signals)
backtest_engine.plot_results(backtest_results)
```

## 后续工作计划

### P3: 择时层组合实验
- [ ] 测试不同择时模式的效果
  - 不择时（基线）
  - 仅市场宽度过滤
  - 仅RSRS过滤
  - 市场宽度 + RSRS联合过滤
- [ ] 分析不同择时组合对回撤的改善
- [ ] 评估不同择时组合的换手冲击

### P4: 区分短周期轮动 vs 中周期配置
- [ ] 短周期线：价格趋势 + 信号响应速度
  - 基于notebook 43、64、59/60
- [ ] 中周期线：景气 + 趋势 + 仓位控制
  - 基于notebook 29、52、候选池

### P5: 补足实盘约束
- [ ] ETF最小成交额约束
- [ ] 单日最大换手限制
- [ ] 滑点和管理费
- [ ] 调仓日约束
- [ ] 停牌/申赎异常数据检查

## 参考notebook

- `66 手把手教你构建ETF策略候选池.ipynb`
- `86 手把手教你构建ETF策略候选池优化版.ipynb`
- `43 轮动ETF策略中的动量因子分析.ipynb`
- `52 市场宽度——简洁版.ipynb`
- `59 研究 【复现】RSRS择时改进.ipynb`
- `60 研究 【分享】对RSRS模型的一次修改.ipynb`

## 项目价值

1. **标准化流程**: 将分散的notebook研究整合为统一框架
2. **可复用性**: 模块化设计，便于扩展和复用
3. **版本管理**: 候选池版本化，便于追踪和对比
4. **因子对比**: 统一的因子有效性评估体系
5. **完整回测**: 从候选池到回测的完整流程

## 总结

已完成ETF轮动策略统一研究框架的核心部分（P0、P1、P2），为后续的择时实验、周期区分和实盘约束奠定了基础。框架采用模块化设计，便于扩展和维护，可以支持多种策略配置和实验需求。

下一步工作重点：
1. 完成P3择时层组合实验
2. 区分短周期和中周期策略
3. 补充实盘约束条件
4. 进行滚动样本验证