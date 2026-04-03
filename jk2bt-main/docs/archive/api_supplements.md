# 聚宽API补充模块文档

## 概述

基于对jkcode目录下20个策略文件的API使用频率分析，我们补充了以下缺失或不完整的功能模块：

## 模块列表

### 1. api_enhancements.py - API增强模块

补充缺失的核心交易和过滤API：

#### 交易API
- `order_shares(security, amount)` - 按股数下单
- `order_target_percent(security, percent)` - 按比例调整仓位
- `rebalance_portfolio(target_weights)` - 按权重重新平衡组合

#### 过滤函数
- `filter_st(stock_list)` - 过滤ST股票
- `filter_paused(stock_list)` - 过滤停牌股票
- `filter_limit_up(stock_list)` - 过滤涨停股票
- `filter_limit_down(stock_list)` - 过滤跌停股票
- `filter_new_stocks(stock_list, days=180)` - 过滤次新股

#### 辅助函数
- `get_high_limit(security)` - 获取涨停价
- `get_low_limit(security)` - 获取跌停价
- `calculate_position_value(security)` - 计算持仓市值
- `get_position_ratio(security)` - 获取持仓比例
- `get_portfolio_weights()` - 获取组合权重

**使用示例：**
```python
from jqdata_akshare_backtrader_utility.api_enhancements import *

# 过滤ST和停牌股票
stocks = ['600519.XSHG', '000858.XSHE', '000333.XSHE']
clean_stocks = filter_st(stocks)
active_stocks = filter_paused(clean_stocks)

# 等权重新平衡
rebalance_equally(active_stocks, context)

# 获取当前组合权重
weights = get_portfolio_weights()
```

### 2. indicator_fields.py - 财务指标字段补充

补充完整的indicator表字段支持：

#### 支持的指标字段（部分）
- `roe` - 净资产收益率
- `roa` - 总资产收益率
- `gross_profit_margin` - 毛利率
- `net_profit_margin` - 净利率
- `operating_margin` - 营业利润率
- `inc_net_profit_year_on_year` - 净利润同比增长率
- `inc_revenue_year_on_year` - 营收同比增长率
- `current_ratio` - 流动比率
- `quick_ratio` - 速动比率
- `debt_asset_ratio` - 资产负债率
- `eps` - 每股收益

#### 主要函数
- `get_indicator_data(symbol, fields)` - 获取单个股票指标
- `get_indicator_batch(symbols, fields)` - 批量获取指标
- `get_indicator_ranking(symbols, field)` - 按指标排序
- `filter_by_indicator(symbols, field, min_value, max_value)` - 按指标筛选
- `get_financial_score(symbols, weights)` - 财务综合评分

**使用示例：**
```python
from jqdata_akshare_backtrader_utility.indicator_fields import *

# 获取ROE排名前10的股票
stocks = get_index_stocks('000300.XSHG')
top_roe = get_indicator_ranking(stocks, 'roe', top_n=10)

# 筛选ROE > 15%的股票
high_roe_stocks = filter_by_indicator(stocks, 'roe', min_value=0.15)

# 计算财务综合评分
weights = {
    'roe': 0.3,
    'inc_revenue_year_on_year': 0.3,
    'current_ratio': 0.2,
    'debt_asset_ratio': 0.2
}
scores = get_financial_score(stocks, weights)
```

### 3. api_optimizations.py - 性能优化模块

优化高频API的性能：

#### 缓存机制
- `CurrentDataCache` - get_current_data结果缓存器
- `get_current_data_cached(code)` - 带缓存的当前数据查询
- `cached_get_security_info(code)` - 带缓存的证券信息查询
- `cached_get_index_stocks(index_code)` - 带缓存的指数成分股查询

#### 批量加载
- `BatchDataLoader` - 批量数据加载器
- `get_current_data_batch(codes)` - 批量获取当前数据
- `preload_data_for_strategy(stock_pool, start_date, end_date)` - 预加载数据

#### 内存管理
- `optimize_dataframe_memory(df)` - 优化DataFrame内存
- `cleanup_memory()` - 清理内存
- `get_memory_usage()` - 获取内存使用情况

**使用示例：**
```python
from jqdata_akshare_backtrader_utility.api_optimizations import *

# 预加载策略所需数据
stock_pool = ['600519.XSHG', '000858.XSHE', '000333.XSHE']
data = preload_data_for_strategy(stock_pool, '2023-01-01', '2023-12-31')

# 批量获取当前数据
current_data = get_current_data_batch(stock_pool)

# 预热缓存
warm_up_cache(stock_pool)

# 清理内存
cleanup_memory()
```

### 4. strategy_helpers.py - 策略辅助函数

提供策略开发中常用的辅助函数：

#### 技术指标
- `calculate_ma(prices, window)` - 移动平均
- `calculate_ema(prices, span)` - 指数移动平均
- `calculate_boll(prices)` - 布林线
- `calculate_rsi(prices)` - RSI指标
- `calculate_macd(prices)` - MACD指标
- `calculate_kdj(highs, lows, closes)` - KDJ指标
- `calculate_atr(highs, lows, closes)` - ATR指标

#### 数据处理
- `normalize_data(data, method)` - 数据标准化
- `winsorize(data, lower, upper)` - 去极值

#### 绩效分析
- `calculate_sharpe(returns)` - 夏普比率
- `calculate_max_drawdown(values)` - 最大回撤
- `calculate_annualized_return(values)` - 年化收益
- `calculate_volatility(returns)` - 波动率

#### 组合管理
- `calculate_position_concentration(weights)` - 持仓集中度
- `calculate_diversification_index(weights)` - 分散度
- `rebalance_equally(stock_list, context)` - 等权平衡

**使用示例：**
```python
from jqdata_akshare_backtrader_utility.strategy_helpers import *

# 计算技术指标
ma5 = calculate_ma(df['close'], 5)
ma20 = calculate_ma(df['close'], 20)
boll = calculate_boll(df['close'])
rsi = calculate_rsi(df['close'])

# 计算绩效
sharpe = calculate_sharpe(daily_returns)
max_dd = calculate_max_drawdown(nav_series)
annual_return = calculate_annualized_return(nav_series)

# 等权重新平衡
rebalance_equally(stock_list, context)
```

## 使用建议

### 1. 在策略初始化时预加载数据

```python
def initialize(context):
    # 预加载数据
    from jqdata_akshare_backtrader_utility.api_optimizations import preload_data_for_strategy
    stock_pool = get_index_stocks('000300.XSHG')
    preload_data_for_strategy(stock_pool, '2020-01-01', '2023-12-31')
    
    # 初始化全局变量
    g.stock_pool = stock_pool
    g.stock_num = 10
```

### 2. 使用过滤函数构建股票池

```python
def get_stocks(context):
    from jqdata_akshare_backtrader_utility.api_enhancements import (
        filter_st, filter_paused, filter_new_stocks
    )
    from jqdata_akshare_backtrader_utility.indicator_fields import filter_by_indicator
    
    # 获取指数成分股
    stocks = get_index_stocks('000300.XSHG')
    
    # 过滤
    stocks = filter_st(stocks)
    stocks = filter_paused(stocks)
    stocks = filter_new_stocks(stocks, days=180)
    
    # 按指标筛选
    stocks = filter_by_indicator(stocks, 'roe', min_value=0.10)
    
    return stocks
```

### 3. 使用组合管理函数优化持仓

```python
def trade_stocks(context):
    from jqdata_akshare_backtrader_utility.api_enhancements import (
        order_target_percent, rebalance_portfolio, get_portfolio_weights
    )
    
    # 获取目标股票和权重
    target_stocks = g.target_stocks
    target_weight = 1.0 / len(target_stocks)
    target_weights = {stock: target_weight for stock in target_stocks}
    
    # 重新平衡组合
    rebalance_portfolio(target_weights, target_stocks)
    
    # 查看当前权重
    current_weights = get_portfolio_weights()
    log.info(f'当前权重: {current_weights}')
```

### 4. 使用性能优化功能

```python
def handle_data(context, data):
    from jqdata_akshare_backtrader_utility.api_optimizations import (
        get_current_data_cached, warm_up_cache
    )
    
    # 预热缓存（只需执行一次）
    if not hasattr(g, 'cache_warmed'):
        warm_up_cache(g.stock_pool)
        g.cache_warmed = True
    
    # 使用缓存获取数据
    for stock in g.stock_pool:
        cd = get_current_data_cached(stock)
        if not cd.paused and cd.last_price < cd.high_limit:
            # 执行交易逻辑
            pass
```

## API使用频率统计结果

基于对jkcode目录下20个策略文件的分析：

### 高频API（>50%使用率）
1. g.xxx (100%)
2. set_option (100%)
3. set_order_cost (100%)
4. context.portfolio (95%)
5. run_daily (85%)
6. log.info (85%)
7. set_slippage (80%)
8. get_current_data (75%)
9. context.current_dt (65%)
10. attribute_history (55%)

### 中频API（10-50%使用率）
1. get_price (50%)
2. order_target (45%)
3. get_security_info (45%)
4. history (40%)
5. get_fundamentals (35%)

### 补充优先级
1. ✅ 缺失的交易API（order_shares, order_target_percent）
2. ✅ 过滤函数（filter_st, filter_paused）
3. ✅ indicator字段补充
4. ✅ 性能优化（缓存、批量加载）
5. ✅ 策略辅助函数（技术指标、绩效分析）

## 更新日志

### v1.0.0 (2026-03-30)
- 创建api_enhancements.py，补充缺失的交易和过滤API
- 创建indicator_fields.py，补充indicator表字段支持
- 创建api_optimizations.py，优化API性能
- 创建strategy_helpers.py，提供策略辅助函数
- 完整文档和示例代码

## 注意事项

1. 所有补充模块都依赖现有的backtrader_base_strategy.py
2. 部分函数需要AkShare数据源支持
3. 建议在策略初始化时预加载数据以提高性能
4. 使用缓存机制时注意内存占用
5. indicator字段数据可能有1-2天延迟

### 5. finance_data/company_info.py - 上市公司基本信息与状态变动

**任务1已完成** - 提供上市公司基本信息和状态变动查询。

#### 主要函数
- `get_company_info(symbol)` - 获取单个公司基本信息
- `query_company_basic_info(symbols)` - 批量查询公司基本信息
- `get_security_status(symbol, date)` - 获取证券状态（停牌/复牌/退市）
- `query_status_change(symbols, start_date, end_date)` - 批量查询状态变动

#### finance表查询
- `finance.STK_COMPANY_BASIC_INFO` - 公司基本信息表
- `finance.STK_STATUS_CHANGE` - 公司状态变动表

#### 返回字段
- 公司基本信息：code, company_name, establish_date, list_date, main_business, industry, registered_address, company_status
- 状态变动：code, status_date, status_type, reason

**使用示例：**
```python
from jqdata_akshare_backtrader_utility.finance_data.company_info import (
    get_company_info, query_company_basic_info
)
from jqdata_akshare_backtrader_utility.backtrader_base_strategy import finance, query

# 单个公司查询
df = get_company_info('600519.XSHG')
print(df[['code', 'company_name', 'list_date']])

# 批量查询
symbols = ['600519.XSHG', '000001.XSHE', '000858.XSHE']
df_batch = query_company_basic_info(symbols)

# finance.run_query 兼容
df_finance = finance.run_query(
    query(
        finance.STK_COMPANY_BASIC_INFO.code,
        finance.STK_COMPANY_BASIC_INFO.company_name,
    ).filter(finance.STK_COMPANY_BASIC_INFO.code.in_(symbols))
)
```

#### 缓存策略
- **静态数据**：按季度缓存
- DuckDB优先（`data/company_info.db`）
- Pickle备用（`finance_cache/`）

#### 已知限制
1. 网络依赖：部分AkShare API不稳定
2. 数据完整性：当前字段较少，需补充更多数据源
3. 历史状态记录有限

---

## 更新日志

### v1.1.0 (2026-03-30)
- 完成任务1：上市公司基本信息与状态变动 API
- 新增 finance.STK_COMPANY_BASIC_INFO 表查询
- 新增 finance.STK_STATUS_CHANGE 表查询
- DuckDB缓存机制已建立

### v1.0.0 (2026-03-30)
- 创建api_enhancements.py，补充缺失的交易和过滤API
- 创建indicator_fields.py，补充indicator表字段支持
- 创建api_optimizations.py，优化API性能
- 创建strategy_helpers.py，提供策略辅助函数
- 完整文档和示例代码

### 6. finance_data/shareholder.py - 股东信息API

**任务2已完成** - 提供十大股东、十大流通股东、股东户数查询。

#### 主要函数
- `get_top10_shareholders(symbol, date)` - 获取十大股东
- `get_top10_float_shareholders(symbol, date)` - 获取十大流通股东
- `get_shareholder_count(symbol)` - 获取股东户数时间序列
- `query_shareholder_top10(symbols)` - 批量查询十大股东

#### finance表查询
- `finance.STK_SHAREHOLDER_TOP10` - 十大股东表
- `finance.STK_SHAREHOLDER_FLOAT_TOP10` - 十大流通股东表
- `finance.STK_SHAREHOLDER_NUM` - 股东户数表

#### 返回字段
- code, shareholder_name, shareholder_type, hold_amount, hold_ratio, change_type, report_date

**使用示例：**
```python
from jqdata_akshare_backtrader_utility.finance_data.shareholder import get_top10_shareholders

df = get_top10_shareholders('600519.XSHG')
```

---

### 7. finance_data/dividend.py - 分红送股API

**任务3已完成** - 提供分红送股信息查询。

#### 主要函数
- `get_dividend(symbol, start_date, end_date)` - 获取分红送股信息
- `query_dividend(symbols)` - 批量查询分红送股

#### finance表查询
- `finance.STK_XR_XD` - 分红送股表

#### 返回字段
- code, report_date, bonus_amount_rmb, transfer_ratio, bonus_ratio, ex_dividend_date, record_date

**使用示例：**
```python
from jqdata_akshare_backtrader_utility.finance_data.dividend import get_dividend

df = get_dividend('600519.XSHG')
```

---

### 8. finance_data/share_change.py - 股东变动API

**任务4已完成** - 提供股东持股变动查询。

#### 主要函数
- `get_share_change(symbol, start_date, end_date)` - 获取股东变动
- `query_share_change(symbols)` - 批量查询股东变动

#### finance表查询
- `finance.STK_SHAREHOLDER_CHANGE` - 股东变动表

#### 返回字段
- code, shareholder_name, change_date, change_type, change_amount, change_ratio, hold_amount_after, hold_ratio_after

---

### 9. finance_data/unlock.py - 限售解禁API

**任务5已完成** - 提供限售解禁信息查询。

#### 主要函数
- `get_unlock(symbol, start_date, end_date)` - 获取限售解禁
- `query_unlock(symbols)` - 批量查询限售解禁
- `get_unlock_calendar(date)` - 获取解禁日历

#### finance表查询
- `finance.STK_RESTRICTED_RELEASE` - 限售解禁表

#### 返回字段
- code, unlock_date, unlock_amount, unlock_ratio, unlock_type, holder_type

---

### 10. market_data/conversion_bond.py - 可转债API

**任务6已完成** - 提供可转债行情查询。

#### 主要函数
- `get_conversion_bond_list()` - 获取可转债列表
- `get_conversion_bond(bond_code)` - 获取单只可转债
- `query_conversion_bond(bond_codes)` - 批量查询可转债

#### finance表查询
- `finance.STK_CB_DAILY` - 可转债行情表

#### 返回字段
- bond_code, bond_name, stock_code, close, conversion_price, conversion_ratio, premium_rate

---

### 11. market_data/option.py - 期权API

**任务7已完成** - 提供期权行情查询。

#### 主要函数
- `get_option_list(underlying)` - 获取期权列表
- `get_option(option_code)` - 获取单只期权
- `query_option(option_codes)` - 批量查询期权

#### finance表查询
- `finance.STK_OPTION_DAILY` - 期权行情表

#### 返回字段
- option_code, option_name, underlying, strike, expiry_date, option_type, close, volume

---

### 12. market_data/index_components.py - 指数成分股API

**任务8已完成** - 提供指数成分股及权重查询。

#### 主要函数
- `get_index_components(index_code)` - 获取指数成分股
- `query_index_components(index_codes)` - 批量查询指数成分股

#### finance表查询
- `finance.STK_INDEX_WEIGHTS` - 指数成分股权重表

#### 返回字段
- index_code, code, weight, effective_date

**使用示例：**
```python
from jqdata_akshare_backtrader_utility.market_data.index_components import get_index_components

# 获取沪深300成分股
df = get_index_components('000300.XSHG')
print(df[['code', 'weight']].head(10))
```

---

### 13. market_data/industry_sw.py - 申万行业API

**任务9已完成** - 提供申万行业分类查询。

#### 主要函数
- `get_stock_industry(symbol)` - 获取股票所属行业
- `query_industry_sw(symbols)` - 批量查询申万行业
- `get_industry_stocks(industry_name)` - 获取行业所有股票

#### finance表查询
- `finance.STK_INDUSTRY_SW` - 申万行业分类表

#### 返回字段
- code, industry_name, industry_code, level

---

### 14. finance_data/macro.py - 宏观数据API

**任务10已完成** - 提供宏观经济数据查询。

#### 主要函数
- `get_macro_cpi()` - 获取CPI数据
- `get_macro_ppi()` - 获取PPI数据
- `get_macro_gdp()` - 获取GDP数据
- `query_macro(indicators)` - 批量查询宏观数据

#### finance表查询
- `finance.MACRO_CHINA_CPI` - CPI数据表
- `finance.MACRO_CHINA_PPI` - PPI数据表
- `finance.MACRO_CHINA_GDP` - GDP数据表

#### 返回字段
- indicator, value, date, unit

**使用示例：**
```python
from jqdata_akshare_backtrader_utility.finance_data.macro import get_macro_cpi, query_macro

# 获取CPI数据
df = get_macro_cpi()

# 批量获取多个指标
df = query_macro(['CPI', 'PPI', 'GDP'])
```

---

## 更新日志

### v1.2.0 (2026-03-30)
- 完成任务2-10：新增9个数据接口API
- 新增股东信息API（shareholder.py）
- 新增分红送股API（dividend.py）
- 新增股东变动API（share_change.py）
- 新增限售解禁API（unlock.py）
- 新增可转债API（conversion_bond.py）
- 新增期权API（option.py）
- 新增指数成分股API（index_components.py）
- 新增申万行业API（industry_sw.py）
- 新增宏观数据API（macro.py）
- 所有API支持DuckDB缓存
- 所有API提供finance.run_query兼容接口

### v1.1.0 (2026-03-30)
- 完成任务1：上市公司基本信息与状态变动 API
- 新增 finance.STK_COMPANY_BASIC_INFO 表查询
- 新增 finance.STK_STATUS_CHANGE 表查询
- DuckDB缓存机制已建立

### v1.0.0 (2026-03-30)
- 创建api_enhancements.py，补充缺失的交易和过滤API
- 创建indicator_fields.py，补充indicator表字段支持
- 创建api_optimizations.py，优化API性能
- 创建strategy_helpers.py，提供策略辅助函数
- 完整文档和示例代码

---

## 已知限制

1. **网络依赖**：部分AkShare API不稳定，可能需要重试
2. **数据延迟**：部分财务数据可能有1-3天延迟
3. **股东变动**：`stock_shareholder_change_ths` API仅支持部分股票
4. **期权数据**：中金所期权数据可能不完整
5. **宏观数据**：月度数据，更新频率较低

---

## 反馈与支持

如有问题或建议，请在项目Issue中反馈。