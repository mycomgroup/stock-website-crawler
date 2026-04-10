# jk2bt → akshare-one-enhanced 数据层迁移需求

## 背景

将 jk2bt 项目的 110 个业务接口迁移到 akshare-one-enhanced，使 akshare-one-enhanced 成为统一的数据层。

## 源项目路径
- jk2bt: `/Users/fengzhi/Downloads/git/testlixingren/jk2bt-main/jk2bt/api/`
- akshare-one-enhanced: `/Users/fengzhi/Downloads/git/akshare-one-enhanced/src/akshare_one/`

## 目标结构

在 akshare-one-enhanced 中新增 `strategy/` 子包，存放从 jk2bt 迁移的策略工具层接口：

```
akshare_one/
├── strategy/
│   ├── __init__.py
│   ├── date.py          # 交易日工具（8个接口）
│   ├── indicators.py    # 技术指标（7个接口）
│   ├── filter.py        # 股票过滤（14个接口）
│   ├── stats.py         # 统计工具（6个接口）
│   ├── factor.py        # 因子工具（3个接口 + 3个类）
│   ├── order.py         # 订单/组合（10个接口）
│   └── cache.py         # 缓存/性能（13个接口）
├── modules/
│   ├── valuation/       # 扩展：加入 get_valuation + get_index_valuation
│   ├── margin/          # 扩展：加入 get_mtss / get_margincash_stocks / get_marginsec_stocks
│   ├── futures/         # 扩展：加入 get_dominant_future / get_settlement_price 等
│   └── concept/         # 扩展：加入 get_concepts / get_concept / get_all_concepts 别名
```

## 迁移原则

1. 保持 jk2bt 的公开接口签名不变（向后兼容）
2. 内部实现改为调用 akshare-one-enhanced 的现有模块
3. 对 akshare 的直接调用改为通过 akshare-one-enhanced 的 provider 层
4. 所有迁移接口在 `akshare_one/__init__.py` 中统一导出

## 需求列表

### R1: 交易日工具（strategy/date.py）
迁移 8 个接口，依赖 akshare 的交易日历数据：
- `get_shifted_date` - 日期偏移（支持交易日/自然日）
- `get_previous_trade_date` - 获取前N个交易日
- `get_next_trade_date` - 获取后N个交易日
- `transform_date` - 日期格式转换
- `is_trade_date` - 判断是否交易日
- `get_trade_dates_between` - 获取区间内所有交易日
- `count_trade_dates_between` - 计算区间交易日数量
- `clear_trade_days_cache` - 清除交易日缓存

### R2: 技术指标（strategy/indicators.py）
迁移 7 个 JQ 风格接口，内部调用 akshare-one-enhanced 的 `modules/indicators/`：
- `MA` - 简单移动平均
- `EMA` - 指数移动平均
- `MACD` - MACD 指标（依赖 history 接口）
- `KDJ` - KDJ 指标（依赖 history 接口）
- `RSI` - RSI 指标
- `BOLL` - 布林带（依赖 history 接口）
- `ATR` - 平均真实波幅（依赖 history 接口）

### R3: 股票过滤（strategy/filter.py）
迁移 14 个接口，改为调用 akshare-one-enhanced 的 modules：
- `filter_st` / `filter_st_stock` - 过滤ST股（调用 modules/st）
- `filter_paused` / `filter_paused_stock` - 过滤停牌（调用 modules/suspended）
- `filter_limit_up` / `filter_limit_down` - 过滤涨跌停（调用 modules/limitup）
- `filter_limitup_stock` / `filter_limitdown_stock` - 同上别名
- `filter_new_stock` / `filter_new_stocks` - 过滤新股（调用 modules/ipo）
- `filter_kcb_stock` / `filter_kcbj_stock` - 过滤科创板/北交所
- `apply_common_filters` - 组合过滤（ST+停牌+新股）
- `get_dividend_ratio_filter_list` - 股息率筛选
- `get_margine_stocks` - 两融标的列表

### R4: 统计工具（strategy/stats.py）
迁移 6 个接口，纯计算，无外部依赖：
- `get_ols` - OLS 线性回归
- `get_zscore` - Z-score 标准化
- `get_rank` - 截面排名
- `get_beta` - Beta 系数计算
- `get_num` - 数值统计
- `get_factor_filter_list` - 因子筛选列表

### R5: 因子工具（strategy/factor.py）
迁移 3 个接口 + 3 个类：
- `get_north_factor` - 北向资金因子
- `get_comb_factor` - 组合因子
- `get_factor_momentum` - 因子动量
- `FactorAnalyzer` - 因子分析器类
- `analyze_factor` - 因子分析函数
- `AttributionAnalysis` - 归因分析类

### R6: 估值模块扩展（modules/valuation/）
在现有 valuation 模块中新增：
- `get_valuation` - 批量个股估值（PE/PB/PS/市值）
- `get_index_valuation` / `get_index_valuation_jq` - 指数历史估值

### R7: 融资融券扩展（modules/margin/）
在现有 margin 模块中新增：
- `get_mtss` / `get_mtss_jq` - 融资融券明细
- `get_margincash_stocks` - 融资标的列表
- `get_marginsec_stocks` - 融券标的列表

### R8: 期货扩展（modules/futures/）
在现有 futures 模块中新增：
- `get_dominant_future` / `get_dominant_future_jq` - 主力合约
- `get_futures_info` / `get_futures_info_jq` - 期货合约信息
- `get_future_contracts` / `get_future_contracts_jq` - 合约列表
- `get_dominant_contracts` - 所有品种主力合约
- `get_settlement_price` - 结算价

### R9: 概念板块别名（modules/concept/）
在现有 concept 模块中新增别名：
- `get_concepts` / `get_concepts_jq` → `get_concept_list` 别名
- `get_concept` / `get_concept_jq` → `get_concept_constituents` 别名
- `get_all_concepts` → 返回所有概念列表

### R10: 行情适配层（strategy/market_compat.py）
迁移 JQ 风格行情接口，桥接到 modules/historical + modules/realtime：
- `get_price` / `get_price_jq` - 历史行情（JQ 签名）
- `history` / `attribute_history` - 历史数据（JQ 签名）
- `get_bars` / `get_bars_jq` - K线数据
- `get_market` - 市场行情
- `get_detailed_quote` - 详细行情
- `get_ticks_enhanced` - Tick 数据
- `get_open_price` / `get_close_price` / `get_high_limit` / `get_low_limit` - 单值快捷接口

### R11: 证券信息别名
- `get_all_securities` → `get_basic_info` 的批量版本
- `get_security_info` → `get_basic_info` 的单股版本

### R12: 龙虎榜别名（modules/lhb/）
- `get_billboard_list` → `get_dragon_tiger_list` 别名
- `get_billboard_hot_stocks` → 热门股票榜单
- `get_broker_statistics` → `get_dragon_tiger_broker_stats` 别名
- `get_institutional_holdings` → `get_institution_holdings` 别名

### R13: 资金流向别名（modules/fundflow/）
- `get_money_flow` → `get_stock_fund_flow` 别名
- `get_money_flow_rank` → `get_main_fund_flow_rank` 别名
- `get_sector_money_flow` → `get_sector_fund_flow` 别名

### R14: 金融行业指标（modules/financial/）
新增银行/证券/保险行业专项指标：
- `bank_indicator` / `bank_indicator_jq`
- `security_indicator` / `security_indicator_jq`
- `insurance_indicator` / `insurance_indicator_jq`

### R15: 订单/组合工具（strategy/order.py）
迁移回测框架接口（模拟实现）：
- `order_shares` / `order_target_percent`
- `rebalance_portfolio` / `get_portfolio_weights`
- `calculate_position_value` / `get_position_ratio`
- `will_sell_on_limit_up` / `will_buy_on_limit_down`
- `LimitOrderStyle` / `MarketOrderStyle`

### R16: 缓存/性能工具（strategy/cache.py）
迁移策略运行时缓存工具：
- `CurrentDataCache` / `BatchDataLoader` / `DataPreloader`
- `get_current_data_cached` / `get_current_data_batch`
- `cached_get_security_info` / `cached_get_index_stocks`
- `batch_get_fundamentals` / `warm_up_cache`
- `preload_data_for_strategy` / `optimize_dataframe_memory`
- `cleanup_memory` / `get_memory_usage`

### R17: 统一导出
更新 `akshare_one/__init__.py`，将所有迁移接口加入导出列表。
