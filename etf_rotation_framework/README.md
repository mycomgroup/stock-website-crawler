# ETF轮动策略统一研究框架

基于聚宽有价值策略558个notebook的ETF轮动研究，搭建的标准化研究框架。

## 框架结构

```
etf_rotation_framework/
├── config.py                    # 统一配置文件
├── main.py                      # 主程序入口
├── modules/
│   ├── __init__.py             # 模块初始化
│   ├── pool_builder.py         # 候选池构建模块
│   ├── factor_calculator.py    # 因子计算模块
│   ├── timing_filter.py        # 择时过滤模块
│   ├── strategy.py             # 策略模块
│   └── backtest_engine.py      # 回测引擎模块
└── README.md                    # 本文件
```

## 核心模块

### 1. 候选池构建模块 (pool_builder.py)
- 基于notebook 66和86的逻辑
- 流动性过滤：成交额 > 1000万
- KMeans聚类去重：24个簇
- 相关性过滤：相关系数 > 0.85

### 2. 因子计算模块 (factor_calculator.py)
- 基于notebook 43的动量因子逻辑
- 斜率动量因子：线性回归斜率
- 收益率动量因子：N日累计收益率
- IC分析：信息系数计算

### 3. 择时过滤模块 (timing_filter.py)
- 基于notebook 52、59、60的逻辑
- 市场宽度：Close > MA20的股票占比
- RSRS择时：原始/钝化版本
- 综合择时：市场宽度 + RSRS

### 4. 策略模块 (strategy.py)
- 整合候选池、因子、择时
- 每日持仓信号生成
- 换手率计算

### 5. 回测引擎模块 (backtest_engine.py)
- 完整回测流程
- 绩效指标计算
- 可视化输出

## 配置文件

config.py 包含所有参数配置：
- POOL_CONFIG: 候选池构建参数
- FACTOR_CONFIG: 因子计算参数
- TIMING_CONFIG: 择时过滤参数
- STRATEGY_CONFIG: 策略执行参数
- BACKTEST_CONFIG: 回测参数
- DATA_CONFIG: 数据源配置

## 使用方法

### 在聚宽环境中运行

```python
from modules import ETFPoolBuilder, FactorCalculator, TimingFilter, BacktestEngine, RotationStrategy
from jqdata import *

# 1. 构建候选池
pool_builder = ETFPoolBuilder()
pool = pool_builder.build_pool(get_all_securities, get_price)

# 2. 获取价格数据
pool_codes = pool_builder.get_pool_codes()
prices = pd.DataFrame()
for code in pool_codes:
    prices[code] = get_price(code, fields='close', end_date='2024-12-31', count=1000)['close']

# 3. 计算因子
factor_calculator = FactorCalculator()
momentum = factor_calculator.calculate_momentum(prices)

# 4. 运行策略
strategy = RotationStrategy(pool_builder, factor_calculator, TimingFilter())
results = strategy.run(prices)

# 5. 回测
backtest_engine = BacktestEngine()
backtest_results = backtest_engine.run_backtest(prices, strategy.signals)
backtest_engine.plot_results(backtest_results)
```

## 后续工作

### P1: 候选池模块版本化
- 保存候选池版本表
- 记录每次构建的参数和结果

### P2: 建立统一因子对比实验
- 价格动量
- 价量因子
- 板块热度因子
- 中观行业打分因子

### P3: 择时层组合实验
- 不择时（基线）
- 仅市场宽度过滤
- 仅RSRS过滤
- 市场宽度 + RSRS联合过滤

### P4: 区分短周期轮动 vs 中周期配置
- 短周期：价格趋势 + 信号响应速度
- 中周期：景气 + 趋势 + 仓位控制

### P5: 补足实盘约束
- ETF最小成交额约束
- 单日最大换手限制
- 滑点和管理费
- 调仓日约束

## 参考notebook

- `66 手把手教你构建ETF策略候选池.ipynb`
- `86 手把手教你构建ETF策略候选池优化版.ipynb`
- `43 轮动ETF策略中的动量因子分析.ipynb`
- `52 市场宽度——简洁版.ipynb`
- `59 研究 【复现】RSRS择时改进.ipynb`
- `60 研究 【分享】对RSRS模型的一次修改.ipynb`

## 许可证

本框架仅供学习研究使用。