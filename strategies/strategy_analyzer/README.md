# Strategy Regime Analyzer

通用策略分行情验证框架，支持任意策略在不同市场状态下的表现分析。

## 功能特性

- **任意策略接入**: 只需提供选股函数即可接入
- **多维度分析**: 年度、市场状态、择时效果、前N期影响
- **多基准对比**: 同时对比多个基准指数
- **风险指标**: 夏普比率、最大回撤、Calmar比率
- **并行执行**: 多策略同时回测加速
- **Markdown输出**: 自动生成结构化报告

## 目录结构

```
strategy_analyzer/
├── README.md                    # 说明文档
├── config.py                    # 配置定义
├── analyzer.py                  # 核心分析框架
├── backtest_engine.py           # 回测引擎
├── market_classifier.py         # 市场状态分类器
├── analysis_modules.py          # 分析模块
├── risk_metrics.py              # 风险指标计算
├── report_generator.py          # 报告生成器
├── utils.py                     # 工具函数
├── examples/                    # 示例
│   ├── example_small_cap.py     # 小市值示例
│   └── example_etf_momentum.py  # ETF动量示例
└── tests/                       # 测试
    └── test_analyzer.py
```

## 快速开始

```python
from strategy_analyzer import StrategyRegimeAnalyzer, AnalyzerConfig

# 定义策略
def select_guojiu(date, n=10):
    # 选股逻辑
    return stock_list

# 配置
config = AnalyzerConfig(
    start="2020-01-01",
    end="2026-03-28",
    freq="quarterly",
    cost=0.003,
    benchmarks=["399101.XSHE", "000300.XSHG"],
)

# 运行
analyzer = StrategyRegimeAnalyzer(config)
analyzer.register("国九条筛选型", select_guojiu, hold_n=10)
analyzer.register("微盘再平衡型", select_micro_cap, hold_n=10)

analyzer.run()
analyzer.report(output_path="report.md")
```

## 分析维度

1. **年度收益**: 各年度累计收益
2. **市场状态**: 牛市/温和上涨/温和下跌/熊市表现
3. **择时效果**: 不择时 vs 择时策略对比
4. **前N期影响**: 前期涨跌对后续收益的影响
5. **近期表现**: 最近N个周期表现
6. **风险指标**: 夏普、回撤、Calmar等
