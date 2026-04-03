# jk2bt - 聚宽策略本地运行框架

[![测试收集](https://img.shields.io/badge/pytest-4298_collected-brightgreen)](https://github.com)
[![Python 3.9+](https://img.shields.io/badge/Python-3.9+-blue)](https://www.python.org)

**让聚宽策略代码无需修改，直接在本地运行！**

---

## 快速开始

```python
from jk2bt import run_jq_strategy

# 直接运行聚宽策略文件
run_jq_strategy(
    strategy_file='策略.txt',
    start_date='2020-01-01',
    end_date='2023-12-31',
    stock_pool=['600519.XSHG', '000858.XSHE'],
)
```

---

## 安装

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -U pip
pip install -e .
```

## 安装后验收（推荐）

```bash
# 1) 包导入与版本
python3 -c "import jk2bt; print(jk2bt.__version__)"

# 2) 核心链路 smoke
pytest -q tests/test_package_import.py tests/integration/test_jq_runner.py

# 3) 扫描全部测试用例是否可收集
pytest --collect-only -q
```

---

## 运行方式

### 方式1：Python调用（推荐）

```python
from jk2bt import run_jq_strategy

run_jq_strategy(
    strategy_file='strategies/03 一个简单而持续稳定的懒人超额收益策略.txt',
    start_date='2020-01-01',
    end_date='2023-12-31',
    initial_capital=1000000,
    stock_pool=['600519.XSHG', '000858.XSHE', '000333.XSHE'],
)
```

### 方式2：命令行

```bash
python3 run_daily_strategy_batch.py --strategies_dir strategies --limit 1
```

### 方式3：继承基类

```python
from jk2bt.core.strategy_base import JQ2BTBaseStrategy

class MyStrategy(JQ2BTBaseStrategy):
    def __init__(self):
        super().__init__()
        self.g.stocks = ['600519.XSHG', '000858.XSHE']
        self.run_monthly(self.rebalance, 1, 'open')
    
    def rebalance(self, context):
        for stock in context.portfolio.positions:
            if stock not in self.g.stocks:
                self.order_target(stock, 0)
        
        position = context.portfolio.total_value / len(self.g.stocks)
        for stock in self.g.stocks:
            self.order_value(stock, position)
```

---

## 支持的聚宽API

| API | 说明 |
|-----|------|
| `g` | 全局变量 |
| `log.info()` | 日志输出 |
| `context.portfolio` | 持仓和资产 |
| `run_monthly/daily/weekly` | 定时器 |
| `order_target/value` | 下单函数 |
| `get_current_data()` | 实时数据 |
| `get_fundamentals()` | 估值查询 |
| `get_index_weights()` | 指数权重 |
| `get_index_stocks()` | 指数成分股 |
| `finance.run_query()` | 分红数据 |

---

## 策略示例

### 简单轮动策略

```python
def initialize(context):
    g.stocks = ['600519.XSHG', '000858.XSHE']
    run_monthly(rebalance, 1, 'open')

def rebalance(context):
    current = get_current_data()
    
    for stock in context.portfolio.positions:
        if stock not in g.stocks:
            order_target(stock, 0)
    
    position = context.portfolio.total_value / len(g.stocks)
    for stock in g.stocks:
        order_value(stock, position)
```

### 多因子选股

```python
def initialize(context):
    run_monthly(select_stocks, 1, 'open')

def select_stocks(context):
    stocks = get_index_stocks('000300.XSHG')
    
    df = get_fundamentals(
        query(valuation).filter(
            valuation.code.in_(stocks),
            valuation.pb_ratio > 0,
            valuation.pe_ratio > 0,
        )
    )
    
    g.stocks = list(df['code'].head(10))
```

---

## 注意事项

1. **必须指定股票池** - 策略中用到的所有股票都要包含在 `stock_pool` 参数中
2. **股票代码格式** - 支持 `600519.XSHG`、`sh600519`、`600519` 三种格式
3. **数据缓存** - 自动缓存到 `data/market.db`，无需重复下载

---

## 项目结构

```
jk2bt-main/
├── jk2bt/                             # 主包（core/api/market_data/factors/...）
├── strategies/                        # 策略样本
├── tests/                             # 自动化测试
├── docs/                              # 指南与设计文档
├── run_daily_strategy_batch.py        # 批量策略运行入口
├── run_strategies_parallel.py         # 并行运行入口
└── pyproject.toml                     # 打包与依赖配置
```

---

## 致谢

- [聚宽](https://www.joinquant.com/) - 优秀的量化平台
- [AkShare](https://github.com/akfamily/akshare) - 免费金融数据接口
- [Backtrader](https://www.backtrader.com/) - 强大的回测框架
