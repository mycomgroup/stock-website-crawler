# jk2bt - 聚宽策略本地运行框架

[![测试收集](https://img.shields.io/badge/pytest-4500_collected-brightgreen)](https://github.com)
[![Python 3.9+](https://img.shields.io/badge/Python-3.9+-blue)](https://www.python.org)
[![版本](https://img.shields.io/badge/version-1.0.0-blue)](https://github.com)

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
pip install -e .                # 基础安装
pip install -e ".[dev]"         # 开发依赖（pytest等）
pip install -e ".[full]"        # 机器学习依赖（可选）
pip install -e ".[ta]"          # 技术分析依赖（可选）
```

## 安装后验收（推荐）

```bash
# 1) 包导入与版本
python3 -c "import jk2bt; print(jk2bt.__version__)"

# 2) 核心链路 smoke
pytest -q tests/smoke/test_package_import.py tests/unit/engine/test_jq_runner.py

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
python3 -m jk2bt.cli run --strategy strategies/03*.txt --start 2020-01-01 --end 2023-12-31
# 或批量运行
python3 tests/scripts/run_daily_strategy_batch.py --strategies_dir strategies --limit 1
# 或并行运行
python3 tests/scripts/run_strategies_parallel.py --strategies_dir strategies --workers 4
```

### 方式3：继承基类

```python
from jk2bt.engine.strategy_base import JQ2BTBaseStrategy

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
3. **数据缓存** - 自动缓存到 `data/jk2bt.duckdb`，无需重复下载
4. **数据预热** - 首次运行策略前，建议预热数据以获得正常收益：
   ```bash
   # 预热样本数据（约300只股票）
   python3 tools/data/prewarm_data.py --sample --start 2020-01-01 --end 2023-12-31
   
   # 或安装离线数据包（见 docs/installation_validation.md 第2节）
   ```

**验收基准**：
- 验收策略集测试预期结果：4个通过(V4/V5/V6/V7)，3个失败(V1/V2/V3)
- 验收通过标准：`runtime_errors == 0` 且策略运行成功
- 收益率0.00%是正常状态（数据缓存不完整），不影响验收判断
- 要获得正常收益，需要先预热数据

---

## 项目结构

```
jk2bt-main/
├── jk2bt/                             # 主包
│   ├── engine/                        # 1. 回测框架
│   │   ├── runner.py                  #   回测主入口 run_jq_strategy
│   │   ├── strategy_base.py           #   策略基类 (继承 backtrader.Strategy)
│   │   ├── strategy_wrapper.py        #   策略包装器
│   │   ├── executor.py                #   执行器 (数据加载、股票池发现)
│   │   ├── global_state.py            #   全局状态 (ContextProxy, 组合代理)
│   │   ├── data_proxies.py            #   数据代理 (query builder)
│   │   ├── asset_router.py            #   资产类型路由
│   │   ├── securities_utils.py        #   证券代码转换
│   │   ├── timer_manager.py           #   定时器管理 (run_daily/run_weekly)
│   │   ├── validator.py               #   策略验证器
│   │   ├── constants.py               #   常量定义
│   │   ├── exceptions.py              #   异常体系
│   │   ├── io.py                      #   运行时IO (record, send_message, read/write_file)
│   │   ├── helpers.py                 #   辅助函数
│   │   ├── inventory.py               #   库存管理
│   │   ├── subportfolios.py           #   子组合管理
│   │   ├── globals/                   #   全局函数 (order/scheduler/industry/stubs)
│   │   └── namespace/                 #   聚宽命名空间模拟 (jqdata/jqlib/kuanke/jqfactor)
│   │
│   ├── api/                           # 3. 策略API层
│   │   ├── jq_compat.py               #   聚宽兼容API总入口
│   │   ├── market.py                  #   行情API (get_price, history)
│   │   ├── order.py                   #   交易API (order_shares, order_target_percent)
│   │   ├── filter.py                  #   过滤API (ST/停牌/涨跌停/新股)
│   │   ├── indicators.py              #   技术指标API (MA/EMA/MACD/KDJ/RSI/BOLL)
│   │   ├── factor.py                  #   因子API
│   │   ├── factor_analysis.py         #   因子分析API
│   │   ├── stats.py                   #   统计API
│   │   ├── valuation.py               #   估值API
│   │   ├── finance.py                 #   财务API
│   │   ├── futures.py                 #   期货API
│   │   ├── concept.py                 #   概念板块API
│   │   ├── billboard.py               #   龙虎榜API
│   │   ├── margin.py                  #   融资融券API
│   │   ├── bond.py                    #   债券API
│   │   ├── date.py                    #   日期API
│   │   ├── cache.py                   #   缓存API
│   │   ├── securities.py              #   证券信息API
│   │   ├── enhancements.py            #   增强API
│   │   ├── missing_apis.py            #   缺失API占位
│   │   ├── globals/                   #   全局函数
│   │   └── namespace/                 #   命名空间
│   │
│   ├── data/                          # 3. 数据层
│   │   ├── sources/                   #   数据源抽象
│   │   │   ├── base.py                #     DataSource 抽象基类
│   │   │   ├── akshare.py             #     AkShare 实现
│   │   │   ├── akshare_compat.py      #     AkShare 兼容层
│   │   │   ├── mock.py                #     Mock 数据源
│   │   │   ├── registry.py            #     数据源注册中心
│   │   │   ├── router.py              #     多源路由 + 故障转移
│   │   │   └── error_codes.py         #     错误码
│   │   ├── market/                    #   行情数据
│   │   │   ├── stock.py               #     股票日线
│   │   │   ├── etf.py                 #     ETF
│   │   │   ├── index.py               #     指数
│   │   │   ├── minute.py              #     分钟线
│   │   │   ├── futures.py             #     期货
│   │   │   ├── industry.py            #     行业分类
│   │   │   ├── industry_sw.py         #     申万行业
│   │   │   ├── index_components.py    #     指数成分股
│   │   │   ├── money_flow.py          #     资金流向
│   │   │   ├── north_money.py         #     北向资金
│   │   │   ├── call_auction.py        #     集合竞价
│   │   │   ├── concept.py             #     概念板块
│   │   │   ├── conversion_bond.py     #     可转债
│   │   │   ├── option.py              #     期权
│   │   │   ├── lof.py                 #     LOF基金
│   │   │   └── fund_of.py             #     FOF基金
│   │   ├── finance/                   #   财务数据
│   │   │   ├── company_info.py        #     公司信息
│   │   │   ├── shareholder.py         #     股东信息
│   │   │   ├── dividend.py            #     分红
│   │   │   ├── income.py              #     利润表
│   │   │   │   ├── cashflow.py        #     现金流
│   │   │   │   ├── share_change.py    #     股本变动
│   │   │   │   ├── unlock.py          #     解禁
│   │   │   │   ├── forecast.py        #     业绩预告
│   │   │   │   ├── margin.py          #     融资融券
│   │   │   │   ├── macro.py           #     宏观经济
│   │   │   │   └── tables.py          #     财务表统一接口
│   │   └── storage/                   #   数据存储 (DuckDB/Parquet)
│   │
│   ├── analysis/                      # 2. 信号 + 因子 + 风控
│   │   ├── factors/                   #   因子计算
│   │   │   ├── base.py                #     因子基类
│   │   │   ├── valuation.py           #     估值因子 (PE/PB/PS)
│   │   │   ├── technical.py           #     技术因子
│   │   │   ├── fundamentals.py        #     财务因子 (ROE/ROA)
│   │   │   ├── growth.py              #     成长因子
│   │   │   ├── quality.py             #     质量因子
│   │   │   ├── barra.py               #     Barra风格因子
│   │   │   ├── custom.py              #     自定义因子
│   │   │   ├── financial_metrics.py   #     财务指标
│   │   │   ├── qlib_alpha.py          #     Qlib Alpha101/191
│   │   │   ├── preprocess.py          #     预处理 (去极值/标准化/中性化)
│   │   │   ├── zoo.py                 #     因子注册中心
│   │   │   └── risk.py                #     风险因子
│   │   ├── signals/                   #   信号生成
│   │   │   ├── base.py                #     信号基类
│   │   │   ├── cross.py               #     交叉信号 (金叉/死叉)
│   │   │   ├── extreme.py             #     极值信号 (超买/超卖)
│   │   │   ├── breakthrough.py        #     突破信号
│   │   │   ├── divergence.py          #     背离信号
│   │   │   ├── rsrs.py                #     RSRS择时
│   │   │   └── sentiment.py           #     市场情绪
│   │   └── risk/                      #   风险管理
│   │       ├── volatility.py          #     波动率计算
│   │       ├── drawdown.py            #     回撤监控
│   │       └── position.py            #     仓位计算 (凯利/风险平价)
│   │
│   ├── cache/                         # 4. 缓存系统
│   │   ├── manager.py                 #   缓存管理器
│   │   ├── query.py                   #   查询引擎
│   │   ├── writer.py                  #   写入器
│   │   ├── config.py                  #   缓存配置
│   │   ├── partition.py               #   分区管理
│   │   ├── memory.py                  #   内存缓存
│   │   ├── aggregator.py              #   聚合器
│   │   ├── schema.py                  #   Schema验证
│   │   ├── registry.py                #   表注册
│   │   ├── validator.py               #   数据验证
│   │   └── cli.py                     #   CLI接口
│   │
│   ├── scanner/                       # 策略扫描器
│   │   ├── scanner.py                 #   策略扫描器
│   │   ├── txt_normalizer.py          #   TXT策略规范化
│   │   ├── runtime_resource.py        #   运行时资源包
│   │   └── timer_rules.py             #   定时规则
│   │
│   ├── validation/                    # 策略验证框架
│   │   ├── validator.py               #   验证器
│   │   ├── comparison_engine.py       #   比较引擎
│   │   ├── config.py                  #   验证配置
│   │   ├── data_collector.py          #   数据收集器
│   │   └── report_generator.py        #   报告生成
│   │
│   ├── logging/                       # 5. 日志系统
│   │   ├── manager.py                 #   日志管理器
│   │   ├── config.py                  #   日志配置
│   │   ├── formatters.py              #   格式化器
│   │   ├── handlers.py                #   处理器
│   │   ├── adapters.py                #   适配器
│   │   └── stats.py                   #   日志统计
│   │
│   ├── utils/                         # 5. 工具层
│   │   ├── config.py                  #   配置管理
│   │   ├── symbol.py                  #   代码标准化
│   │   ├── standardize.py             #   数据标准化
│   │   ├── code_converter.py          #   代码转换器
│   │   ├── date_utils.py              #   日期工具
│   │   ├── cache.py                   #   缓存工具
│   │   ├── result.py                  #   RobustResult
│   │   ├── dependency.py              #   依赖检查
│   │   ├── init_helper.py             #   懒加载单例
│   │   └── backup.py                  #   数据源备份
│   │
│   ├── asset_router.py                # 顶层资产路由
│   ├── cli.py                         # CLI入口
│   ├── dependency_checker.py          # 依赖检查器
│   └── runtime_io.py                  # 运行时IO
│
├── strategies/                        # 500+ 策略文件 (.txt/.ipynb/.py)
│   ├── json_config/                   # JSON配置示例
│   └── samples/                       # 示例策略结构
│
├── tests/                             # 169 测试文件
│   ├── unit/                          # 单元测试 (按源码镜像)
│   │   ├── engine/                    #   回测引擎 (runner, strategy_base, ...)
│   │   ├── api/                       #   策略API (market, date, filter, ...)
│   │   ├── data/                      #   数据层
│   │   │   ├── sources/               #     数据源 (akshare, router, ...)
│   │   │   ├── market/                #     行情数据 (stock, index, futures, ...)
│   │   │   ├── finance/               #     财务数据 (income, cashflow, ...)
│   │   │   └── storage/               #     存储 (duckdb, parquet, ...)
│   │   ├── analysis/                  #   分析层
│   │   │   ├── factors/               #     因子计算 (valuation, technical, ...)
│   │   │   ├── signals/               #     信号生成 (cross, breakthrough, ...)
│   │   │   └── risk/                  #     风险管理 (drawdown, volatility, ...)
│   │   ├── cache/                     #   缓存系统
│   │   ├── scanner/                   #   策略扫描器
│   │   ├── validation/                #   策略验证
│   │   ├── logging/                   #   日志系统
│   │   └── utils/                     #   工具函数
│   ├── integration/                   # 集成测试
│   ├── regression/                    # 回归测试 (35 tests)
│   ├── e2e/                          # 端到端测试
│   ├── smoke/                        # 冒烟测试
│   ├── scripts/                      # 运行脚本
│   └── fixtures/                     # 测试数据
│
├── tools/                             # 辅助工具
│   ├── data/                          # 数据工具 (prewarm/download)
│   ├── offline_data/                  # 离线数据包工具
│   ├── validation/                    # 策略验证工具
│   └── archive/                       # 归档脚本
│
├── docs/                              # 指南与设计文档
├── pyproject.toml                     # 打包与依赖配置
└── README.md                          # 本文件
```

## 模块依赖关系

```
engine/    →  api/ + analysis/ + data/ + cache/ + utils/ + logging/
api/       →  data/ + cache/ + utils/
analysis/  →  data/ + cache/ + utils/
data/      →  cache/ + utils/
cache/     →  utils/
utils/     →  (无依赖)
logging/   →  (无依赖)
```

## 五大业务模块

| 模块 | 对应目录 | 职责 |
|------|----------|------|
| 1. 回测框架 | `engine/` | 策略加载、命名空间模拟、回测主循环、订单执行、定时器 |
| 2. 回测分析 | `analysis/` | 因子计算、信号生成、风险管理、回测结果绩效分析 |
| 3. 策略API+数据 | `api/` + `data/` | 策略调用的API接口 + 底层数据获取(行情/财务) |
| 4. 缓存系统 | `cache/` | 独立缓存子系统 (Parquet/DuckDB) |
| 5. 工具+日志 | `utils/` + `logging/` | 配置、代码转换、日期、日志等通用工具 |

---

## 致谢

- [聚宽](https://www.joinquant.com/) - 优秀的量化平台
- [AkShare](https://github.com/akfamily/akshare) - 免费金融数据接口
- [Backtrader](https://www.backtrader.com/) - 强大的回测框架
