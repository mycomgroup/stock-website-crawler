# 迁移任务列表

## Task 1: 创建 strategy 包骨架
- [ ] 在 `/Users/fengzhi/Downloads/git/akshare-one-enhanced/src/akshare_one/strategy/` 创建目录
- [ ] 创建 `strategy/__init__.py`，预留所有导出占位

## Task 2: 迁移交易日工具 (strategy/date.py)
源文件: `jk2bt/api/date.py`

- [ ] 创建 `strategy/date.py`
- [ ] 将 `get_all_trade_days_jq` 依赖替换为 akshare 的 `tool_trade_date_hist_sina()` 接口
  ```python
  import akshare as ak
  def _load_trade_days():
      df = ak.tool_trade_date_hist_sina()
      return sorted([pd.to_datetime(d).date() for d in df['trade_date']])
  ```
- [ ] 迁移以下函数（逻辑不变，只替换数据源）:
  - `transform_date`
  - `get_shifted_date`
  - `get_previous_trade_date`
  - `get_next_trade_date`
  - `is_trade_date`
  - `get_trade_dates_between`
  - `count_trade_dates_between`
  - `clear_trade_days_cache`
- [ ] 验证: `from akshare_one.strategy.date import is_trade_date; assert is_trade_date('2024-01-02') == True`

## Task 3: 迁移技术指标 (strategy/indicators.py)
源文件: `jk2bt/api/indicators.py`

- [ ] 创建 `strategy/indicators.py`
- [ ] 迁移 `MA`、`EMA`（纯 pandas 计算，无外部依赖，直接复制）
- [ ] 迁移 `RSI`（纯 pandas 计算部分直接复制；股票代码输入部分改为调用 `history()`）
- [ ] 迁移 `MACD`、`KDJ`、`BOLL`、`ATR`（内部 `history()` 调用改为调用 `strategy/market_compat.py` 的 `history`）
  - 注意：Task 10 完成后才能完整测试，Task 3 先实现骨架，history 调用用 lazy import
- [ ] 验证: `from akshare_one.strategy.indicators import MA; import pandas as pd; result = MA(pd.Series([1,2,3,4,5]), 3); assert len(result) == 5`

## Task 4: 迁移统计工具 (strategy/stats.py)
源文件: `jk2bt/api/stats.py`

- [ ] 创建 `strategy/stats.py`
- [ ] 读取 jk2bt/api/stats.py 完整内容
- [ ] 迁移以下函数（纯计算，无外部依赖）:
  - `get_ols` - OLS 线性回归
  - `get_zscore` - Z-score 标准化
  - `get_rank` - 截面排名
  - `get_beta` - Beta 系数
  - `get_num` - 数值统计
  - `get_factor_filter_list` - 因子筛选
- [ ] 验证: `from akshare_one.strategy.stats import get_zscore; import pandas as pd; result = get_zscore(pd.Series([1,2,3,4,5])); assert abs(result.mean()) < 1e-10`

## Task 5: 迁移因子工具 (strategy/factor.py)
源文件: `jk2bt/api/factor.py` + `jk2bt/api/factor_analysis.py`

- [ ] 创建 `strategy/factor.py`
- [ ] 读取 jk2bt/api/factor.py 和 jk2bt/api/factor_analysis.py 完整内容
- [ ] 迁移 `get_north_factor`、`get_comb_factor`、`get_factor_momentum`
  - 内部 date 依赖改为 `from akshare_one.strategy.date import ...`
- [ ] 迁移 `FactorAnalyzer` 类、`analyze_factor` 函数、`AttributionAnalysis` 类
- [ ] 验证: `from akshare_one.strategy.factor import FactorAnalyzer; fa = FactorAnalyzer(); assert fa is not None`

## Task 6: 迁移过滤工具 (strategy/filter.py)
源文件: `jk2bt/api/filter.py` + `jk2bt/api/limit_api.py`

- [ ] 创建 `strategy/filter.py`
- [ ] 读取 jk2bt/api/filter.py 和 jk2bt/api/limit_api.py 完整内容
- [ ] 实现 `filter_st` / `filter_st_stock`，改为调用:
  ```python
  from akshare_one.modules.st.eastmoney import EastMoneyST
  provider = EastMoneyST()
  st_df = provider.get_st_stocks()
  st_codes = set(st_df['symbol'].values)
  ```
- [ ] 实现 `filter_paused` / `filter_paused_stock`，调用 `modules/suspended/eastmoney.py`
- [ ] 实现 `filter_limit_up` / `filter_limit_down` / `filter_limitup_stock` / `filter_limitdown_stock`，调用 `modules/limitup/eastmoney.py`
- [ ] 实现 `filter_new_stock` / `filter_new_stocks`，调用 `modules/ipo/eastmoney.py`
- [ ] 实现 `filter_kcb_stock`（科创板：代码以 688 开头）
- [ ] 实现 `filter_kcbj_stock`（北交所：代码以 8 开头）
- [ ] 实现 `apply_common_filters`（组合调用 ST + 停牌 + 新股过滤）
- [ ] 实现 `get_dividend_ratio_filter_list`（调用 akshare 股息率数据）
- [ ] 实现 `get_margine_stocks`（调用 `modules/margin/eastmoney.py`）
- [ ] 从 limit_api.py 迁移: `get_continue_count_df`、`get_hl_count_df`、`get_hl_stock`、`get_recent_limit_up_stock`、`get_recent_limit_down_stock`
- [ ] 验证: `from akshare_one.strategy.filter import filter_kcb_stock; result = filter_kcb_stock(['688001.XSHG', '000001.XSHE']); assert '000001.XSHE' in result and '688001.XSHG' not in result`

## Task 7: 扩展估值模块 (modules/valuation/)
源文件: `jk2bt/api/valuation.py`

- [ ] 读取 jk2bt/api/valuation.py 完整内容
- [ ] 在 `modules/valuation/base.py` 中新增方法签名:
  - `get_valuation(security_list, date, fields)` - 批量个股估值
  - `get_index_valuation(index_code, start_date, end_date, fields, count)` - 指数历史估值
- [ ] 创建 `modules/valuation/jq_compat.py`，实现上述方法
  - `get_valuation` 内部循环调用 `get_stock_valuation`
  - `get_index_valuation` 调用 akshare 的 `index_value_hist_fina`
- [ ] 在 `modules/valuation/__init__.py` 中导出新方法
- [ ] 添加 `get_index_valuation_jq` 别名
- [ ] 验证: `from akshare_one.modules.valuation.jq_compat import get_index_valuation`

## Task 8: 扩展融资融券模块 (modules/margin/)
源文件: `jk2bt/api/margin.py`

- [ ] 读取 jk2bt/api/margin.py 完整内容
- [ ] 创建 `modules/margin/jq_compat.py`，实现:
  - `get_mtss(security_list, start_date, end_date, fields)` - 融资融券明细
    内部调用 `get_margin_data` 并转换格式
  - `get_margincash_stocks(date)` - 融资标的列表
  - `get_marginsec_stocks(date)` - 融券标的列表
- [ ] 添加 `get_mtss_jq` 别名
- [ ] 在 `modules/margin/__init__.py` 中导出
- [ ] 验证: `from akshare_one.modules.margin.jq_compat import get_mtss`

## Task 9: 扩展期货模块 (modules/futures/)
源文件: `jk2bt/api/futures.py`

- [ ] 读取 jk2bt/api/futures.py 完整内容
- [ ] 创建 `modules/futures/jq_compat.py`，实现:
  - `get_dominant_future(underlying_symbol, date)` - 主力合约代码
  - `get_futures_info(underlying_symbol)` - 合约基本信息
  - `get_future_contracts(underlying_symbol, date)` - 合约列表
  - `get_dominant_contracts(date)` - 所有品种主力合约
  - `get_settlement_price(contract, date)` - 结算价
- [ ] 添加 `_jq` 后缀别名
- [ ] 在 `modules/futures/__init__.py` 中导出
- [ ] 验证: `from akshare_one.modules.futures.jq_compat import get_dominant_future`

## Task 10: 行情适配层 (strategy/market_compat.py)
源文件: `jk2bt/api/market.py`

- [ ] 读取 jk2bt/api/market.py 完整内容
- [ ] 创建 `strategy/market_compat.py`
- [ ] 实现符号标准化工具函数（从 jk2bt/_internal/symbol_utils.py 迁移）:
  - `normalize_symbol('000300.XSHG')` → `'000300'`
  - `_freq_map('daily')` → `'day'`
  - `_fq_map('pre')` → `'qfq'`
- [ ] 实现 `get_price(security, start_date, end_date, frequency, fields, skip_paused, fq, count)`:
  ```python
  from akshare_one.modules.historical import HistoricalDataFactory
  provider = HistoricalDataFactory.create(
      source="eastmoney",
      symbol=normalize_symbol(security),
      interval=_freq_map(frequency),
      start_date=start_date, end_date=end_date,
      adjust=_fq_map(fq),
  )
  return provider.get_hist_data()
  ```
- [ ] 实现 `history(count, unit, field, security_list, end_dt, include_now)` - JQ 风格历史数据
- [ ] 实现 `attribute_history(security, count, unit, fields, skip_paused, df)` - 单股历史
- [ ] 实现 `get_bars(security_list, count, unit, fields, include_now, end_dt, fq_ref)` - K线
- [ ] 实现 `get_market(security, date)` - 市场行情
- [ ] 实现 `get_detailed_quote(security, date)` - 详细行情（调用 modules/realtime）
- [ ] 实现 `get_open_price` / `get_close_price` / `get_high_limit` / `get_low_limit` 快捷接口
- [ ] 实现 `get_ticks_enhanced` - Tick 数据
- [ ] 添加 `get_price_jq` / `get_bars_jq` 别名
- [ ] 验证: `from akshare_one.strategy.market_compat import normalize_symbol; assert normalize_symbol('000300.XSHG') == '000300'`

## Task 11: 概念板块别名 (modules/concept/)
源文件: `jk2bt/api/concept.py`

- [ ] 读取 jk2bt/api/concept.py 完整内容
- [ ] 创建 `modules/concept/jq_compat.py`，实现:
  - `get_concepts(date)` → 调用 `get_concept_list()`
  - `get_concept(concept_code, date)` → 调用 `get_concept_constituents()`
  - `get_all_concepts(date)` → 调用 `get_concept_list()` 返回全量
  - `get_concept_stocks_jq(concept_code, date)` → 调用 `get_concept_constituents()`
  - `get_concepts_jq` / `get_concept_jq` 别名
- [ ] 在 `modules/concept/__init__.py` 中导出
- [ ] 验证: `from akshare_one.modules.concept.jq_compat import get_all_concepts`

## Task 12: 龙虎榜别名 (modules/lhb/)
源文件: `jk2bt/api/billboard.py`

- [ ] 读取 jk2bt/api/billboard.py 完整内容
- [ ] 创建 `modules/lhb/jq_compat.py`，实现:
  - `get_billboard_list(start_date, end_date)` → `get_dragon_tiger_list` 别名
  - `get_billboard_hot_stocks(date, top_n)` → 热门股票榜单
  - `get_broker_statistics(start_date, end_date)` → `get_dragon_tiger_broker_stats` 别名
  - `get_institutional_holdings(stock, start_date, end_date)` → `get_institution_holdings` 别名
- [ ] 在 `modules/lhb/__init__.py` 中导出
- [ ] 验证: `from akshare_one.modules.lhb.jq_compat import get_billboard_list`

## Task 13: 资金流向别名 (modules/fundflow/)
源文件: `jk2bt/api/money_flow_api.py`

- [ ] 读取 jk2bt/api/money_flow_api.py 完整内容
- [ ] 创建 `modules/fundflow/jq_compat.py`，实现:
  - `get_money_flow(security, start_date, end_date, count)` → `get_stock_fund_flow` 适配
  - `get_money_flow_rank(top_n, direction)` → `get_main_fund_flow_rank` 适配
  - `get_sector_money_flow(sector, date)` → `get_sector_fund_flow` 适配
- [ ] 在 `modules/fundflow/__init__.py` 中导出
- [ ] 验证: `from akshare_one.modules.fundflow.jq_compat import get_money_flow`

## Task 14: 金融行业指标 (modules/financial/)
源文件: `jk2bt/api/financial_indicator.py`

- [ ] 读取 jk2bt/api/financial_indicator.py 完整内容
- [ ] 创建 `modules/financial/industry.py`，实现:
  - `bank_indicator(stock_list, date, fields)` - 银行业专项指标
  - `security_indicator(stock_list, date, fields)` - 证券业专项指标
  - `insurance_indicator(stock_list, date, fields)` - 保险业专项指标
- [ ] 添加 `_jq` 后缀别名
- [ ] 在 `modules/financial/__init__.py` 中导出
- [ ] 验证: `from akshare_one.modules.financial.industry import bank_indicator`

## Task 15: 证券信息别名 (strategy/securities_compat.py)
源文件: `jk2bt/api/securities.py`

- [ ] 读取 jk2bt/api/securities.py 完整内容
- [ ] 创建 `strategy/securities_compat.py`，实现:
  - `get_all_securities(types, date)` → 调用 `modules/info` 的批量接口
  - `get_security_info(code, date)` → 调用 `modules/info/eastmoney.py` 的 `get_basic_info`
- [ ] 验证: `from akshare_one.strategy.securities_compat import get_security_info`

## Task 16: 订单/组合工具 (strategy/order.py)
源文件: `jk2bt/api/order.py`

- [ ] 读取 jk2bt/api/order.py 完整内容
- [ ] 创建 `strategy/order.py`，直接迁移（这些是回测框架接口，不依赖数据源）:
  - `LimitOrderStyle` / `MarketOrderStyle` 类
  - `order_shares` / `order_target_percent`
  - `rebalance_portfolio` / `get_portfolio_weights`
  - `calculate_position_value` / `get_position_ratio`
  - `will_sell_on_limit_up` / `will_buy_on_limit_down`
- [ ] 验证: `from akshare_one.strategy.order import LimitOrderStyle, MarketOrderStyle`

## Task 17: 缓存/性能工具 (strategy/cache.py)
源文件: `jk2bt/api/cache.py`

- [ ] 读取 jk2bt/api/cache.py 完整内容
- [ ] 创建 `strategy/cache.py`，迁移以下内容:
  - `CurrentDataCache` 类 → 内部调用 `modules/realtime` 替换 `get_current_data`
  - `BatchDataLoader` 类 → 内部调用 `modules/historical`
  - `DataPreloader` 类
  - `get_current_data_cached` / `get_current_data_batch`
  - `cached_get_security_info` → 调用 `modules/info`
  - `cached_get_index_stocks` → 调用 `modules/index`
  - `batch_get_fundamentals` → 调用 `modules/financial`
  - `warm_up_cache` / `preload_data_for_strategy`
  - `optimize_dataframe_memory` / `cleanup_memory` / `get_memory_usage`
- [ ] 验证: `from akshare_one.strategy.cache import CurrentDataCache; c = CurrentDataCache(); assert c is not None`

## Task 18: 更新 strategy/__init__.py
- [ ] 在 `strategy/__init__.py` 中导出所有迁移接口:
  ```python
  from .date import *
  from .indicators import *
  from .filter import *
  from .stats import *
  from .factor import *
  from .market_compat import *
  from .order import *
  from .cache import *
  from .securities_compat import *
  ```

## Task 19: 更新顶层 akshare_one/__init__.py
- [ ] 读取现有 `akshare_one/__init__.py` 内容
- [ ] 追加导出所有迁移接口（不删除现有导出）:
  ```python
  # JQ 兼容层 - 从 jk2bt 迁移
  from .strategy import (
      # 日期工具
      get_shifted_date, get_previous_trade_date, get_next_trade_date,
      transform_date, is_trade_date, get_trade_dates_between,
      count_trade_dates_between, clear_trade_days_cache,
      # 技术指标
      MA, EMA, MACD, KDJ, RSI, BOLL, ATR,
      # 过滤工具
      filter_st, filter_st_stock, filter_paused, filter_paused_stock,
      filter_limit_up, filter_limit_down, filter_new_stock, filter_new_stocks,
      filter_kcb_stock, filter_kcbj_stock, apply_common_filters,
      get_dividend_ratio_filter_list, get_margine_stocks,
      # 统计工具
      get_ols, get_zscore, get_rank, get_beta, get_num, get_factor_filter_list,
      # 因子工具
      get_north_factor, get_comb_factor, get_factor_momentum,
      FactorAnalyzer, analyze_factor, AttributionAnalysis,
      # 行情适配
      get_price, get_price_jq, history, attribute_history,
      get_bars, get_bars_jq, get_market, get_detailed_quote,
      get_open_price, get_close_price, get_high_limit, get_low_limit,
      get_ticks_enhanced,
      # 订单/组合
      order_shares, order_target_percent, rebalance_portfolio,
      get_portfolio_weights, calculate_position_value, get_position_ratio,
      will_sell_on_limit_up, will_buy_on_limit_down,
      LimitOrderStyle, MarketOrderStyle,
      # 缓存/性能
      CurrentDataCache, BatchDataLoader, DataPreloader,
      get_current_data_cached, get_current_data_batch,
      cached_get_security_info, cached_get_index_stocks,
      batch_get_fundamentals, warm_up_cache, preload_data_for_strategy,
      optimize_dataframe_memory, cleanup_memory, get_memory_usage,
      # 证券信息
      get_all_securities, get_security_info,
  )
  from .modules.valuation.jq_compat import get_valuation, get_index_valuation, get_index_valuation_jq
  from .modules.margin.jq_compat import get_mtss, get_mtss_jq, get_margincash_stocks, get_marginsec_stocks
  from .modules.futures.jq_compat import (
      get_dominant_future, get_dominant_future_jq, get_futures_info, get_futures_info_jq,
      get_future_contracts, get_future_contracts_jq, get_dominant_contracts, get_settlement_price,
  )
  from .modules.concept.jq_compat import get_concepts, get_concepts_jq, get_concept, get_concept_jq, get_all_concepts, get_concept_stocks_jq
  from .modules.lhb.jq_compat import get_billboard_list, get_billboard_hot_stocks, get_broker_statistics, get_institutional_holdings
  from .modules.fundflow.jq_compat import get_money_flow, get_money_flow_rank, get_sector_money_flow
  from .modules.financial.industry import bank_indicator, bank_indicator_jq, security_indicator, security_indicator_jq, insurance_indicator, insurance_indicator_jq
  ```
- [ ] 验证所有导出无 ImportError

## Task 20: 集成验证
- [ ] 运行验证脚本，确认所有 110 个接口可以从 `akshare_one` 顶层 import:
  ```python
  python3 -c "
  from akshare_one import (
      is_trade_date, get_trade_dates_between, MA, EMA, RSI,
      filter_st, filter_paused, apply_common_filters,
      get_ols, get_zscore, get_rank,
      get_price, history, get_bars,
      get_valuation, get_index_valuation,
      get_mtss, get_dominant_future,
      get_concepts, get_billboard_list,
      get_money_flow, bank_indicator,
      order_shares, CurrentDataCache,
  )
  print('所有接口导入成功')
  "
  ```
- [ ] 检查无循环导入
- [ ] 检查无 NameError / ImportError
