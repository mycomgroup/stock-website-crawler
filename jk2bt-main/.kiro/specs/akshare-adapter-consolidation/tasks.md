# Tasks: AkShare Adapter Consolidation

目标：将 49 个文件中 97 处 `import akshare` 全部收口到 `jk2bt/data_access/akshare_adapter.py`。
完成后 `grep -r "import akshare" jk2bt/` 仅在 `akshare_adapter.py` 中出现。

---

- [x] Task 1: 基础设施 — 扩展 DataSource 接口 + AkShareAdapter

**文件**: `jk2bt/data_access/data_source.py`, `jk2bt/data_access/akshare_adapter.py`, `jk2bt/data_access/__init__.py`

在 `DataSource` 抽象基类中新增所有缺失的方法声明，在 `AkShareAdapter` 中实现，在 `__init__.py` 中暴露 `get_adapter()` / `set_adapter()` 单例工厂。

新增接口分组：

**ST/停牌**
- `get_st_stocks() -> DataFrame` — `ak.stock_zh_a_st_em()`
- `get_suspended_stocks() -> DataFrame` — `ak.stock_zh_a_stop_em()`

**估值**
- `get_index_valuation(index_code: str) -> DataFrame` — `ak.index_value_hist_fina()`
- `get_stock_valuation(symbol: str) -> DataFrame` — `ak.stock_a_lg_indicator()`
- `get_stock_pe_pb(symbol: str) -> DataFrame` — `ak.stock_a_pe_and_pb()`

**融资融券**
- `get_margin_detail(market: str, date: str) -> DataFrame` — `ak.stock_margin_detail_sse/szse()`
- `get_margin_underlying(market: str) -> DataFrame` — `ak.stock_margin_underlying_info_sse/szse()`

**宏观数据（原始，不含缓存）**
- `get_macro_raw(indicator: str) -> DataFrame` — 支持 pmi/cpi/ppi/gdp/m2/interest_rate/exchange_rate/rmb

**股东数据**
- `get_top10_holders(symbol: str) -> DataFrame`
- `get_top10_float_holders(symbol: str) -> DataFrame`
- `get_holder_count(symbol: str) -> DataFrame`
- `get_institutional_holders(symbol: str) -> DataFrame`

**财务报表**
- `get_financial_report(symbol: str, report_type: str) -> DataFrame` — 现金流量表/资产负债表/利润表
- `get_financial_benefit(symbol: str, indicator: str) -> DataFrame` — `ak.stock_financial_benefit_ths()`
- `get_cashflow(symbol: str) -> DataFrame`

**分红/股本变动/解禁**
- `get_dividend(symbol: str) -> DataFrame`
- `get_share_change(symbol: str) -> DataFrame`
- `get_unlock_schedule(symbol: str) -> DataFrame`

**行情扩展**
- `get_spot_em() -> DataFrame` — `ak.stock_zh_a_spot_em()` 全市场实时行情
- `get_index_daily(symbol: str) -> DataFrame` — `ak.stock_zh_index_daily()`
- `get_stock_hist(symbol: str, ...) -> DataFrame` — `ak.stock_zh_a_hist()`
- `get_trade_dates() -> DataFrame` — `ak.tool_trade_date_hist_sina()`
- `get_securities_code_name() -> DataFrame` — `ak.stock_info_a_code_name()`
- `get_bond_yield(symbol: str) -> DataFrame` — `ak.bond_china_yield()`

**行业/概念**
- `get_industry_list(source: str) -> DataFrame`
- `get_industry_components(industry_name: str, source: str) -> DataFrame`
- `get_concept_list() -> DataFrame`
- `get_concept_components(concept_name: str) -> DataFrame`
- `get_sw_industry(level: str) -> DataFrame` — 申万行业

**ETF/LOF/可转债/期货/期权**
- `get_etf_hist(symbol: str) -> DataFrame`
- `get_lof_hist(symbol: str) -> DataFrame`
- `get_conversion_bond_list() -> DataFrame`
- `get_conversion_bond_daily(symbol: str) -> DataFrame`
- `get_futures_daily(contract_code: str) -> DataFrame`
- `get_option_daily(option_code: str) -> DataFrame`

**龙虎榜/公司信息/预测**
- `get_billboard_list(date: str) -> DataFrame`
- `get_company_info(symbol: str) -> DataFrame`
- `get_forecast(symbol: str) -> DataFrame`

**验收标准**:
- `get_adapter() is get_adapter()` 返回 True（单例）
- `set_adapter(mock)` 后 `get_adapter()` 返回 mock
- 所有新增方法在 akshare 不可用时抛出 `DataSourceError`
- 所有 akshare 异常统一转换为 `DataSourceError`，不泄露原始异常类型

---

- [x] Task 2: 收口 core/ 层

**文件**: `jk2bt/core/api_wrappers.py`, `jk2bt/core/data_proxies.py`

替换点：
- `api_wrappers.py:938` — `ak.stock_financial_report_sina(现金流量表)` → `get_adapter().get_financial_report(symbol, "现金流量表")`
- `api_wrappers.py:969` — `ak.stock_financial_benefit_ths()` → `get_adapter().get_financial_benefit()`
- `api_wrappers.py:995` — `ak.stock_financial_report_sina(资产负债表)` → `get_adapter().get_financial_report(symbol, "资产负债表")`
- `api_wrappers.py:1714` — `ak.stock_info_a_code_name()` → `get_adapter().get_securities_code_name()`
- `api_wrappers.py:1876` — `ak.tool_trade_date_hist_sina()` → `get_adapter().get_trade_dates()`
- `api_wrappers.py:2002` — `ak.stock_zh_a_st_em()` → `get_adapter().get_st_stocks()`
- `data_proxies.py:668` — `ak.stock_zh_a_stop_em()` → `get_adapter().get_suspended_stocks()`
- `data_proxies.py:699` — `ak.stock_zh_a_st_em()` → `get_adapter().get_st_stocks()`

**验收标准**: `grep "import akshare" jk2bt/core/` 无输出

---

- [x] Task 3: 收口 api/ 层（薄逻辑模块）

**文件**: `jk2bt/api/filter.py`, `jk2bt/api/valuation.py`, `jk2bt/api/margin.py`, `jk2bt/api/billboard.py`, `jk2bt/api/finance.py`, `jk2bt/api/financial_indicator.py`, `jk2bt/api/market.py`, `jk2bt/api/money_flow_api.py`

替换点：
- `filter.py` — `ak.stock_zh_a_st_em()` / `ak.stock_zh_a_stop_em()` → `get_adapter().get_st_stocks()` / `get_suspended_stocks()`
- `valuation.py` — `ak.index_value_hist_fina()` / `ak.stock_a_lg_indicator()` → `get_adapter().get_index_valuation()` / `get_stock_valuation()`
- `margin.py` — `ak.stock_margin_detail_sse/szse()` / `ak.stock_margin_underlying_info_*()` → `get_adapter().get_margin_detail()` / `get_margin_underlying()`
- `billboard.py` — 龙虎榜相关 → `get_adapter().get_billboard_list()`
- `finance.py` — 财务相关 → `get_adapter().get_financial_report()`
- `financial_indicator.py` — 金融行业指标 → `get_adapter().get_financial_benefit()`
- `market.py` — 行情相关 → `get_adapter().get_stock_hist()` / `get_spot_em()`
- `money_flow_api.py` — 资金流向 → `get_adapter().get_money_flow()` / `get_sector_money_flow()`

**验收标准**: `grep "import akshare" jk2bt/api/` 无输出

---

- [x] Task 4: 收口 utils/ + db/ 层

**文件**: `jk2bt/utils/date_utils.py`, `jk2bt/utils/data_source_backup.py`, `jk2bt/db/meta_cache_api.py`

替换点：
- `date_utils.py:115` — `ak.tool_trade_date_hist_sina()` → `get_adapter().get_trade_dates()`
- `data_source_backup.py` — 所有 akshare 备用数据源调用 → `get_adapter()` 对应方法
- `meta_cache_api.py` — 元数据获取 → `get_adapter()` 对应方法

**验收标准**: `grep "import akshare" jk2bt/utils/ jk2bt/db/` 无输出

---

- [x] Task 5: 收口 signals/ + strategy/ 层

**文件**: `jk2bt/signals/fields.py`, `jk2bt/signals/market_sentiment.py`, `jk2bt/signals/rsrs.py`, `jk2bt/strategy/timer_rules.py`

替换点：
- `fields.py:169` — `ak.stock_financial_analysis_indicator()` → `get_adapter().get_financial_benefit()`
- `market_sentiment.py:41` — `ak.stock_zh_a_spot_em()` → `get_adapter().get_spot_em()`
- `market_sentiment.py:113` — `ak.stock_zh_index_daily()` → `get_adapter().get_index_daily()`
- `market_sentiment.py:224` — `ak.stock_a_pe_and_pb()` → `get_adapter().get_stock_pe_pb()`
- `market_sentiment.py:253` — `ak.bond_china_yield()` → `get_adapter().get_bond_yield()`
- `market_sentiment.py:334,397` — `ak.stock_zh_a_spot_em()` / `ak.stock_zh_a_hist()` → `get_adapter()` 对应方法
- `rsrs.py:160` — `ak.stock_zh_index_daily()` → `get_adapter().get_index_daily()`
- `timer_rules.py:52` — `ak.tool_trade_date_hist_sina()` → `get_adapter().get_trade_dates()`

**验收标准**: `grep "import akshare" jk2bt/signals/ jk2bt/strategy/` 无输出

---

- [x] Task 6: 收口 market_data/ 层

**文件**: `jk2bt/market_data/concept.py`, `jk2bt/market_data/industry.py`, `jk2bt/market_data/industry_sw.py`, `jk2bt/market_data/index_components.py`, `jk2bt/market_data/etf.py`, `jk2bt/market_data/lof.py`, `jk2bt/market_data/fund_of.py`, `jk2bt/market_data/futures.py`, `jk2bt/market_data/futures_data.py`, `jk2bt/market_data/conversion_bond.py`, `jk2bt/market_data/option.py`, `jk2bt/market_data/money_flow.py`, `jk2bt/market_data/north_money.py`, `jk2bt/market_data/minute.py`

策略：这些模块有自己的 DuckDB 缓存层，只替换 akshare 调用点，缓存/标准化逻辑保留原地。

- `concept.py` — `ak.stock_board_concept_*()` → `get_adapter().get_concept_list()` / `get_concept_components()`
- `industry.py` — `ak.stock_board_industry_*()` → `get_adapter().get_industry_list()` / `get_industry_components()`
- `industry_sw.py` — 申万行业相关 → `get_adapter().get_sw_industry()`
- `index_components.py` — 指数成分相关 → `get_adapter().get_index_components()`
- `etf.py` — `ak.fund_etf_hist_em()` 等 → `get_adapter().get_etf_hist()`
- `lof.py` — LOF 相关 → `get_adapter().get_lof_hist()`
- `fund_of.py` — 基金相关 → `get_adapter()` 对应方法
- `futures.py` / `futures_data.py` — 期货相关 → `get_adapter().get_futures_daily()`
- `conversion_bond.py` — 可转债相关 → `get_adapter().get_conversion_bond_*()`
- `option.py` — 期权相关 → `get_adapter().get_option_daily()`
- `money_flow.py` — 资金流向 → `get_adapter().get_money_flow()`
- `north_money.py` — 北向资金 → `get_adapter().get_north_money_flow()`
- `minute.py` — 分钟数据 → `get_adapter().get_minute_data()`

**验收标准**: `grep "import akshare" jk2bt/market_data/` 无输出

---

- [x] Task 7: 收口 finance_data/ 层（最复杂，厚逻辑模块）

**文件**: `jk2bt/finance_data/macro.py`, `jk2bt/finance_data/shareholder.py`, `jk2bt/finance_data/dividend.py`, `jk2bt/finance_data/share_change.py`, `jk2bt/finance_data/unlock.py`, `jk2bt/finance_data/cashflow.py`, `jk2bt/finance_data/finance_tables.py`, `jk2bt/finance_data/company_info.py`, `jk2bt/finance_data/forecast.py`, `jk2bt/finance_data/margin.py`

策略：这些模块有完整的 DuckDB 缓存管理，只替换 akshare 调用点，所有缓存/标准化/RobustResult 逻辑保留原地。

- `macro.py` — 7 个宏观指标调用 → `get_adapter().get_macro_raw(indicator)`
- `shareholder.py` — 股东数据 → `get_adapter().get_top10_holders()` 等
- `dividend.py` — 分红数据 → `get_adapter().get_dividend()`
- `share_change.py` — 股本变动 → `get_adapter().get_share_change()`
- `unlock.py` — 解禁数据 → `get_adapter().get_unlock_schedule()`
- `cashflow.py` — 现金流 → `get_adapter().get_cashflow()`
- `finance_tables.py` — 财务报表 → `get_adapter().get_financial_report()`
- `company_info.py` — 公司信息 → `get_adapter().get_company_info()`
- `forecast.py` — 业绩预告 → `get_adapter().get_forecast()`
- `margin.py` — 融资融券 → `get_adapter().get_margin_detail()`

**验收标准**: `grep "import akshare" jk2bt/finance_data/` 无输出

---

- [x] Task 8: 收口 factors/ 层

**文件**: `jk2bt/factors/technical.py`, `jk2bt/factors/valuation.py`, `jk2bt/factors/barra_factors.py`, `jk2bt/factors/fundamentals.py`, `jk2bt/factors/finance_tables.py`, `jk2bt/factors/data_sources.py`

策略：
- `technical._get_daily_ohlcv` 的 akshare fallback → `get_adapter().get_stock_hist()`
- `barra_factors._get_index_data` 的 akshare fallback → `get_adapter().get_index_daily()`
- `valuation._get_valuation_raw` → `get_adapter().get_stock_valuation()`
- `fundamentals._get_income_statement` / `_get_balance_sheet` → `get_adapter().get_financial_report()`
- `finance_tables.py` → `get_adapter().get_financial_report()`
- `data_sources.ValuationDataSource.fetch_from_eastmoney` → `get_adapter().get_stock_valuation()`
- `data_sources.TurnoverDataSource.fetch_from_akshare` → `get_adapter().get_stock_hist()`

**验收标准**: `grep "import akshare" jk2bt/factors/` 无输出

---

- [x] Task 9: 统一 normalize_symbol — 消除重复定义

**文件**: `jk2bt/utils/symbol.py` 及 15 个有重复定义的文件

当前有 15 处 `normalize_symbol` / `_normalize_code` / `format_stock_symbol` 的重复定义，逻辑各有微差。

- 在 `jk2bt/utils/symbol.py` 中确立唯一权威实现，覆盖所有格式：`sh600519` / `sz000001` / `600519.XSHG` / `000001.XSHE` / `600519` / `000001`
- 删除以下文件中的本地重复定义，改为 `from jk2bt.utils.symbol import normalize_symbol`：
  - `jk2bt/factors/valuation.py:43`
  - `jk2bt/factors/data_sources.py:260`
  - `jk2bt/api/billboard.py:31`
  - `jk2bt/api/financial_indicator.py:29`
  - `jk2bt/api/money_flow_api.py:75`
  - `jk2bt/api/market.py:272`
  - `jk2bt/market_data/money_flow.py:83`
  - `jk2bt/core/asset_router.py:155`
  - `jk2bt/core/securities_utils.py:66`
  - `jk2bt/api/_internal/symbol_utils.py:10`
  - `jk2bt/validation/data_collector.py:31`
  - 其余重复定义处

**验收标准**:
- `grep -rn "def.*normalize.*symbol\|def.*normalize.*code\|def.*format.*symbol" jk2bt/ --include="*.py"` 仅在 `utils/symbol.py` 中出现
- 所有格式的股票代码经 `normalize_symbol` 后输出一致

---

- [x] Task 10: 最终验收

**验收命令**:
```bash
# 唯一 akshare 入口
grep -r "import akshare" jk2bt/ --include="*.py" | grep -v "akshare_adapter.py"
# 期望：无输出

# 单例幂等性
python -c "from jk2bt.data_access import get_adapter; assert get_adapter() is get_adapter()"

# normalize_symbol 唯一定义
grep -rn "def.*normalize.*symbol\|def.*normalize.*code" jk2bt/ --include="*.py" | grep -v "utils/symbol.py"
# 期望：无输出（或仅剩 akshare_adapter 内部私有方法）
```

**回归测试**:
- 运行现有测试套件，确保无回归
- 对 `get_adapter()` 的每个新增方法做冒烟测试（有网络环境）
