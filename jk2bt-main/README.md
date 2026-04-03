# jk2bt - 聚宽策略本地运行框架

[![测试通过](https://img.shields.io/badge/测试-158_passed-brightgreen)](https://github.com)
[![Python 3.9+](https://img.shields.io/badge/Python-3.9+-blue)](https://www.python.org)

**让聚宽策略代码无需修改，直接在本地运行！**

---

## 快速开始

```python
from jq_strategy_runner import run_jq_strategy

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
pip install backtrader akshare pandas numpy duckdb
```

---

## 运行方式

### 方式1：Python调用（推荐）

```python
from jq_strategy_runner import run_jq_strategy

run_jq_strategy(
    strategy_file='../jkcode/jkcode/策略.txt',
    start_date='2020-01-01',
    end_date='2023-12-31',
    initial_capital=1000000,
    stock_pool=['600519.XSHG', '000858.XSHE', '000333.XSHE'],
)
```

### 方式2：命令行

```bash
cd jqdata_akshare_backtrader_utility

python3 jq_strategy_runner.py 策略.txt --start 2020-01-01 --end 2023-12-31 --capital 1000000
```

### 方式3：继承基类

```python
from src.core.strategy_base import JQ2BTBaseStrategy

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
jk2bt/
├── jqdata_akshare_backtrader_utility/
│   ├── backtrader_base_strategy.py    # 核心兼容层
│   ├── jq_strategy_runner.py          # 策略运行器
│   ├── factors/                       # 因子计算模块
│   ├── market_data/                   # 行情数据模块
│   ├── finance_data/                  # 财务数据模块
│   └── utils/                         # 工具函数
├── tests/                             # 测试文件（22个）
├── jkcode/jkcode/                     # 聚宽策略文件（449个）
├── data/market.db                     # 数据缓存
├── README.md                          # 本文件
└── QUICK_START.md                     # 快速开始
```

---

## 致谢

- [聚宽](https://www.joinquant.com/) - 优秀的量化平台
- [AkShare](https://github.com/akfamily/akshare) - 免费金融数据接口
- [Backtrader](https://www.backtrader.com/) - 强大的回测框架