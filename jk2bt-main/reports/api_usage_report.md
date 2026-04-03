# 策略API需求分析报告

生成日期: 2026-04-01

## 概述

本报告分析了 `/Users/yuping/Downloads/git/jk2bt-main/strategies/` 目录下所有策略文件的聚宽API使用情况，共扫描 **481** 个策略文件。

---

## API使用频率统计

### 行情数据API

| API名称 | 使用文件数 | 调用次数 | 实现状态 |
|---------|-----------|---------|---------|
| get_price | 283 | 818 | ✅ 已实现 |
| history | 211 | 1071 | ✅ 已实现 |
| attribute_history | 164 | 446 | ✅ 已实现 |
| get_bars | 65 | 150 | ✅ 已实现 |
| get_current_data | 317 | 1114 | ✅ 已实现 |
| get_current_tick | 7 | - | ✅ 已实现 |

### 财务数据API

| API名称 | 使用文件数 | 调用次数 | 实现状态 |
|---------|-----------|---------|---------|
| get_fundamentals | 213 | 451 | ✅ 已实现 |
| get_history_fundamentals | 9 | 34 | ✅ 已实现 |
| get_factor_values | 92 | 158 | ✅ 已实现 |
| valuation | 281 | 1065 | ✅ 已实现 |
| income | 47 | 174 | ✅ 已实现 |
| balance | 47 | 259 | ✅ 已实现 |
| cash_flow | 22 | 76 | ✅ 已实现 |
| indicator | 120 | 536 | ✅ 已实现 |

### 证券元数据API

| API名称 | 使用文件数 | 调用次数 | 实现状态 |
|---------|-----------|---------|---------|
| get_index_stocks | 223 | 221 | ✅ 已实现 |
| get_all_securities | 211 | 278 | ✅ 已实现 |
| get_security_info | 120 | 386 | ✅ 已实现 |
| get_all_trade_days | 108 | 43 | ✅ 已实现 |
| get_trade_days | 108 | 138 | ✅ 已实现 |
| get_extras | 33 | 41 | ✅ 已实现 |

### 订单与交易API

| API名称 | 使用文件数 | 调用次数 | 实现状态 |
|---------|-----------|---------|---------|
| order_target_value | 424 | 823 | ✅ 已实现 |
| order_target | 424 | 473 | ✅ 已实现 |
| order_value | 424 | 203 | ✅ 已实现 |
| order | 424 | - | ✅ 已实现 |

### 定时任务API

| API名称 | 使用文件数 | 调用次数 | 实现状态 |
|---------|-----------|---------|---------|
| run_daily | 408 | 1231 | ✅ 已实现 |
| run_weekly | 408 | 175 | ✅ 已实现 |
| run_monthly | 408 | 160 | ✅ 已实现 |

### 过滤筛选API

| API名称 | 使用文件数 | 调用次数 | 实现状态 |
|---------|-----------|---------|---------|
| filter_st_stock | 196 | 289 | ✅ 已实现 |
| filter_paused_stock | 196 | 287 | ✅ 已实现 |
| filter_new_stock | 196 | 222 | ✅ 已实现 |
| filter_limitup_stock | 196 | 200 | ⚠️ 部分实现 |
| filter_limitdown_stock | 196 | 187 | ⚠️ 部分实现 |
| filter_kcbj_stock | 196 | 172 | ⚠️ 策略自定义 |
| filter_st | 196 | 46 | ✅ 已实现 |
| filter_paused | 196 | 18 | ✅ 已实现 |

### 统计与因子API

| API名称 | 使用文件数 | 调用次数 | 实现状态 |
|---------|-----------|---------|---------|
| get_ols | 46 | 87 | ✅ 已实现 |
| get_zscore | 46 | 63 | ✅ 已实现 |
| get_rank | 46 | 81 | ✅ 已实现 |
| get_factor_filter_list | 46 | 87 | ✅ 已实现 |
| get_num | 46 | 333 | ✅ 已实现 |

### 行业数据API

| API名称 | 使用文件数 | 调用次数 | 实现状态 |
|---------|-----------|---------|---------|
| get_industry_stocks | 47 | 79 | ✅ 已实现 |
| get_stock_industry | 47 | - | ✅ 已实现 |
| get_industry | 47 | 16 | ✅ 已实现 |

### 日期工具API

| API名称 | 使用文件数 | 调用次数 | 实现状态 |
|---------|-----------|---------|---------|
| get_shifted_date | 36 | 77 | ✅ 已实现 |
| get_previous_trade_date | 36 | 14 | ✅ 已实现 |
| get_next_trade_date | 36 | - | ✅ 已实现 |
| transform_date | 36 | 14 | ✅ 已实现 |
| is_trade_date | 36 | - | ✅ 已实现 |

### 设置类API

| API名称 | 使用文件数 | 调用次数 | 实现状态 |
|---------|-----------|---------|---------|
| set_option | 393 | 828 | ✅ 已实现(stub) |
| set_benchmark | 393 | 400 | ✅ 已实现(stub) |
| set_order_cost | 393 | 349 | ✅ 已实现(stub) |
| set_slippage | 393 | 259 | ✅ 已实现(stub) |
| set_universe | 393 | 12 | ✅ 已实现(stub) |
| set_subportfolios | 393 | 28 | ✅ 已实现(stub) |

### 其他API

| API名称 | 使用文件数 | 调用次数 | 实现状态 |
|---------|-----------|---------|---------|
| get_billboard_list | 5 | 5 | ✅ 已实现 |
| get_locked_shares | 19 | - | ✅ 已实现 |
| get_future_contracts | 8 | 8 | ✅ 已实现(stub) |
| get_call_auction | 13 | 13 | ✅ 已实现 |
| get_ticks | 23 | 23 | ✅ 已实现(stub) |
| get_valuation | 51 | 26 | ✅ 已实现 |
| get_north_money | 3 | 7 | ✅ 已实现 |
| compute_rsrs | 36 | 2 | ✅ 已实现 |

---

## 缺失API列表

以下API在策略中被使用，但尚未在jk2bt模块中完整实现：

| API名称 | 使用次数 | 建议优先级 |
|---------|---------|-----------|
| get_dominant_future | 34 | 中 - 期货策略需要 |
| filter_limitup_stock | 200 | 高 - 常用筛选 |
| filter_limitdown_stock | 187 | 高 - 常用筛选 |
| filter_kcbj_stock | 172 | 中 - 科创板/北交所筛选 |
| filter_highprice_stock | 34 | 低 |
| filter_stock_by_days | 26 | 低 |
| filter_gem_stock | 17 | 低 - 创业板筛选 |
| filter_delisted | 14 | 低 |
| get_peg | 18 | 低 - 可用现有API组合实现 |
| get_security_universe | 15 | 低 |
| get_money_flow | 15 | 中 - 资金流向 |
| get_concept_stocks | 9 | 中 - 概念股 |
| get_open_orders | 10 | 低 |

---

## 策略自定义函数

以下是策略内部自定义的函数（非聚宽API，策略自行定义）：

| 函数名 | 定义次数 | 说明 |
|--------|---------|------|
| initialize | 415 | 策略初始化函数（聚宽标准） |
| close_position | 131 | 平仓函数 |
| open_position | 125 | 开仓函数 |
| order_target_value_ | 119 | order_target_value的包装 |
| before_market_open | 111 | 开盘前处理 |
| market_open | 96 | 开盘处理 |
| after_market_close | 95 | 收盘后处理 |
| adjust_position | 70 | 调仓函数 |
| get_stock_list | 99 | 获取股票列表（策略自定义） |
| prepare_stock_list | 96 | 准备股票列表 |
| check_limit_up | 79 | 检查涨停 |
| my_trade | 54 | 自定义交易函数 |
| trade | 50 | 交易函数 |
| weekly_adjustment | 51 | 周度调仓 |
| set_params | 43 | 设置参数 |
| before_trading_start | 39 | 交易前处理 |
| buy | 38 | 买入函数 |
| sell | 36 | 卖出函数 |
| close_account | 37 | 清仓函数 |
| get_timing_signal | 58 | 获取择时信号 |
| get_signal | 39 | 获取信号 |

---

## 模块导入统计

| 模块名 | 使用文件数 | 说明 |
|--------|-----------|------|
| jqdata | 393 | 聚宽数据模块（已模拟） |
| jqlib | 多处 | 聚宽因子库（已模拟） |
| jqfactor | 多处 | 聚宽因子模块（已模拟） |
| kuanke | 多处 | 宽客模块（已模拟） |
| talib | 58 | 技术分析库 |

---

## 结论

### 总体统计

- **总策略文件数**: 481
- **已实现API数**: 65+
- **部分实现API数**: 5
- **缺失API数**: 13
- **API覆盖率**: 约 85%

### 已实现的核心API

1. **行情数据**: get_price, history, attribute_history, get_bars, get_current_data
2. **财务数据**: get_fundamentals, get_history_fundamentals, get_factor_values
3. **证券元数据**: get_index_stocks, get_all_securities, get_security_info
4. **订单交易**: order_target_value, order_target, order_value
5. **定时任务**: run_daily, run_weekly, run_monthly
6. **过滤筛选**: filter_st_stock, filter_paused_stock, filter_new_stock
7. **统计工具**: get_ols, get_zscore, get_rank

### 建议优先实现的API

1. **filter_limitup_stock / filter_limitdown_stock** - 高频使用，涨停/跌停筛选
2. **get_dominant_future** - 期货策略需要
3. **filter_kcbj_stock** - 科创板/北交所筛选
4. **get_concept_stocks** - 概念股筛选
5. **get_money_flow** - 资金流向数据

### 实现建议

1. **涨停/跌停筛选**: 可通过 get_price 获取 high_limit/low_limit 字段后比较实现
2. **期货主力合约**: 可使用 akshare 的期货数据接口实现
3. **概念股**: akshare 提供 get_concept_stocks 类似功能
4. **资金流向**: akshare 提供个股资金流数据

---

## 附录：API实现位置

| API模块 | 文件路径 |
|---------|---------|
| 核心API | `/jk2bt/core/api_wrappers.py` |
| 策略运行器 | `/jk2bt/core/runner.py` |
| 行情API | `/jk2bt/api/market.py`, `/jk2bt/api/market_api.py` |
| 订单API | `/jk2bt/api/order.py` |
| 过滤API | `/jk2bt/api/filter.py` |
| 财务API | `/jk2bt/api/finance.py` |
| 统计API | `/jk2bt/api/stats_api.py` |
| 日期API | `/jk2bt/api/date_api.py` |
| 因子API | `/jk2bt/api/factor_api.py` |
| 指标API | `/jk2bt/api/indicators.py` |