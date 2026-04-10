# 迁移设计文档

## 架构决策

### 1. 新增 `strategy/` 子包
不污染现有 `modules/` 的 Provider 架构，策略工具层单独放在 `strategy/` 下。
这些接口是"计算工具"而非"数据提供者"，不需要 Factory/Provider 模式。

### 2. 依赖方向
```
strategy/*.py  →  modules/*/  →  akshare (底层)
```
strategy 层调用 modules 层的公开接口，不直接调用 akshare。

### 3. 交易日数据源
jk2bt 的 `date.py` 依赖 `jk2bt.core.strategy_base.get_all_trade_days_jq`。
迁移后改为调用 akshare 的 `tool_trade_date_hist_sina()` 接口，
并在 `strategy/date.py` 内部维护缓存。

### 4. 技术指标的 history 依赖
MACD/KDJ/BOLL/ATR 内部调用 `history()` 获取历史数据。
迁移后 `history()` 改为调用 `modules/historical/` 的 `HistoricalDataFactory`。

### 5. 过滤工具的数据依赖
| 过滤函数 | 数据来源 |
|---------|---------|
| filter_st | modules/st/eastmoney.py → get_st_stocks() |
| filter_paused | modules/suspended/eastmoney.py → get_suspended_stocks() |
| filter_limit_up/down | modules/limitup/eastmoney.py → get_limit_up_pool() |
| filter_new_stock | modules/ipo/eastmoney.py → get_new_stocks() |

### 6. 命名冲突处理
- `get_valuation`：jk2bt 是批量个股，akshare-one 是单股 `get_stock_valuation`
  → 新增 `get_valuation` 作为批量版本，不覆盖现有接口
- `get_concept_stocks`：两边都有，签名不同
  → jk2bt 版本加 `_jq` 后缀：`get_concept_stocks_jq`

## 文件映射

| jk2bt 源文件 | 目标文件 | 迁移方式 |
|-------------|---------|---------|
| api/date.py | strategy/date.py | 直接迁移，替换 trade_days 数据源 |
| api/indicators.py | strategy/indicators.py | 直接迁移，替换 history 调用 |
| api/filter.py | strategy/filter.py | 重写，调用 modules/* |
| api/stats.py | strategy/stats.py | 直接迁移，无外部依赖 |
| api/factor.py | strategy/factor.py | 直接迁移，替换 date 依赖 |
| api/factor_analysis.py | strategy/factor.py | 合并到 factor.py |
| api/market.py | strategy/market_compat.py | 重写，调用 modules/historical |
| api/valuation.py | modules/valuation/jq_compat.py | 新增 provider |
| api/margin.py | modules/margin/jq_compat.py | 新增方法 |
| api/futures.py | modules/futures/jq_compat.py | 新增方法 |
| api/concept.py | modules/concept/jq_compat.py | 新增别名 |
| api/billboard.py | modules/lhb/jq_compat.py | 新增别名 |
| api/money_flow_api.py | modules/fundflow/jq_compat.py | 新增别名 |
| api/financial_indicator.py | modules/financial/industry.py | 新增文件 |
| api/order.py | strategy/order.py | 直接迁移 |
| api/cache.py | strategy/cache.py | 重写，调用 modules/* |
| api/securities.py | strategy/securities_compat.py | 别名层 |
| api/limit_api.py | strategy/filter.py | 合并到 filter.py |
| api/stats_api.py | strategy/stats.py | 合并到 stats.py |
