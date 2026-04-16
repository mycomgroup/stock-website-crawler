# AkShare 接口依赖调研报告

> 调研文件：`jk2bt/data_access/akshare_adapter.py`（共 1930 行，约 100+ 个接口）
> 调研时间：2026-04-16

---

## 概述

本报告对 `AkShareAdapter` 类中所有依赖 akshare 的接口进行了系统分类分析，按数据特征划分为 5 大类，并识别出多种特殊情况。

**核心结论**：文件中约 100+ 个 akshare 接口，**仅 3 个实现了缓存机制**（`get_daily_data`、`get_index_stocks`、`get_trading_days`）。回测场景下大量接口会被反复调用但每次都重新请求网络，建议按优先级逐步添加缓存策略。

---

## 分类总览

| 类别 | 数量 | 已有缓存 |
|------|------|---------|
| 1. 实时数据，无法也不需要缓存 | 12 | 0 |
| 2. 低频数据，不需要缓存 | ~64 | 0 |
| 3. 低频数据，需要缓存 | ~87 | 3 |
| 4. 数据太大，需要提前预存 | ~30 | 部分 |
| 5. 其他特殊情况 | 多类 | - |

---

## 1. 实时数据，无法也不需要缓存（12个）

这类接口返回实时/当日行情数据，盘中持续变化，缓存无意义。

| # | 方法名 | akshare 调用 | 原因 |
|---|--------|-------------|------|
| 1 | `get_spot_em()` | `stock_zh_a_spot_em()` | 全市场实时行情快照，每秒变化 |
| 2 | `get_lof_spot()` | `fund_lof_spot_em()` | LOF 基金实时行情 |
| 3 | `get_futures_spot()` | `futures_zh_spot()` | 期货实时行情 |
| 4 | `get_sw_index_daily_spot()` | `sw_index_daily_spot()` | 申万行业指数实时行情 |
| 5 | `get_option_current_day_sse()` | `option_current_day_sse()` | 上交所期权当日行情 |
| 6 | `get_option_current_day_szse()` | `option_current_day_szse()` | 深交所期权当日行情 |
| 7 | `get_option_cffex_hs300_spot()` | `option_cffex_hs300_spot_sina()` | 中金所沪深300期权实时 |
| 8 | `get_option_sse_greeks()` | `option_sse_greeks_sina()` | 期权希腊字母，基于实时价格动态计算 |
| 9 | `get_call_auction_raw()` | `stock_zh_a_hist_pre_min_em()` | 集合竞价原始数据，仅 09:15-09:25 有效 |
| 10 | `get_sector_money_flow()` | `stock_board_industry/concept_fund_flow_rank()` | 板块资金流向排名（默认"今日"） |
| 11 | `get_individual_fund_flow_rank()` | `stock_individual_fund_flow_rank()` | 个股资金流向排名（默认"今日"） |
| 12 | `get_hsgt_hold_stock()` | `stock_em_hsgt_hold_stock()` | 北向资金持股统计（默认"今日"） |

> **注意**：分钟级历史数据（`get_stock_minute_raw`、`get_etf_minute_raw`、`get_lof_hist_min`）虽有实时属性，但收盘后数据固定，**可缓存**。

---

## 2. 低频数据，不需要缓存（约64个）

这类接口数据更新频率低（季度/年度/不定期）、数据量小、查询标的分散导致缓存命中率低。

### 2.1 证券列表/代码映射（5个）

| 方法 | akshare 调用 | 原因 |
|------|-------------|------|
| `get_securities_list` | `stock_info_a_code_name()` / `fund_etf_category_sina()` / `index_stock_info()` | 仅在新股上市/退市时变化 |
| `get_securities_code_name` | `stock_info_a_code_name()` | A股代码-名称映射，变化极少 |
| `get_stock_info_sh_name_code` | `stock_info_sh_name_code()` | 上交所代码名称映射 |
| `get_stock_info_sz_name_code` | `stock_info_sz_name_code()` | 深交所代码名称映射 |
| `get_trade_dates` | `tool_trade_date_hist_sina()` | 交易日历每年仅新增，数据量小 |

### 2.2 公司/证券基本信息（4个）

| 方法 | akshare 调用 | 原因 |
|------|-------------|------|
| `get_security_info` | `stock_individual_info_em()` | 公司基本信息几乎不变 |
| `get_stock_individual_info` | `stock_individual_info_em()` | 同上 |
| `get_company_info` | `stock_individual_info_em()` | 同上 |
| `get_company_industry_em` | `stock_board_industry_name_em()` | 所属行业极少变化 |

### 2.3 行业/概念/指数列表（5个）

| 方法 | akshare 调用 | 原因 |
|------|-------------|------|
| `get_industry_list` | `stock_board_industry_name_em()` | 行业板块列表极少变化 |
| `get_concept_list` | `stock_board_concept_name_em()` | 概念板块列表变化不频繁 |
| `get_sw_industry` | `sw_index_first_info()` | 申万一级行业基本固定 |
| `get_sw_index_info` | `sw_index_info()` | 申万行业指数信息极少变化 |
| `get_index_stock_info` | `index_stock_info()` | 指数基本信息极少变化 |

### 2.4 指数/行业成分（10个）

| 方法 | akshare 调用 | 原因 |
|------|-------------|------|
| `get_index_stocks` | `index_stock_cons()` | 每季度调整，查询标的分散 |
| `get_index_components` | `index_stock_cons_weight_csindex()` | 每季度调整 |
| `get_index_stock_cons` | `index_stock_cons()` | 每季度调整 |
| `get_index_stock_cons_weight_csindex` | `index_stock_cons_weight_csindex()` | 每季度调整 |
| `get_index_component_sw` | `index_component_sw()` | 申万行业成分，定期调整 |
| `get_sw_index_cons` | `sw_index_cons()` | 申万行业成分，定期调整 |
| `get_industry_components` | `stock_board_industry_cons_em()` | 行业成分股，不定期调整 |
| `get_concept_components` | `stock_board_concept_cons_em()` | 概念成分股，不定期调整 |
| `get_industry_stocks` | `index_component_sw()` | 同上 |
| `get_industry_mapping` | `_get_all_industry_mapping()` | 股票-行业映射极少变化 |

### 2.5 财务报表/指标（5个）

| 方法 | akshare 调用 | 原因 |
|------|-------------|------|
| `get_finance_indicator` | `stock_financial_analysis_indicator()` | 季度更新，按股票查询命中率低 |
| `get_financial_analysis_indicator` | `stock_financial_analysis_indicator()` | 同上 |
| `get_financial_report` | `stock_financial_report_sina()` | 季度更新 |
| `get_financial_benefit` | `stock_financial_benefit_ths()` | 季度更新 |
| `get_cashflow` | `stock_financial_report_sina()` | 季度更新 |

### 2.6 股东/持股（8个）

| 方法 | akshare 调用 | 原因 |
|------|-------------|------|
| `get_top10_holders` | `stock_zh_a_gdhs()` | 季度更新 |
| `get_top10_holders_em` | `stock_gdfx_holding_detail_em()` | 季度更新 |
| `get_top10_float_holders` | `stock_zh_a_gdhs_detail_em()` | 季度更新 |
| `get_top10_float_holders_em` | `stock_gdfx_free_holding_detail_em()` | 季度更新 |
| `get_holder_count` | `stock_hold_num_cninfo()` | 季度更新 |
| `get_institutional_holders` | `stock_institute_hold()` | 季度更新 |
| `get_fund_hold_stock` | `stock_fund_hold_stock()` | 季度更新 |
| `get_fund_portfolio` | `fund_portfolio_em()` | 季度更新 |

### 2.7 分红/股本/解禁（14个）

| 方法 | akshare 调用 | 原因 |
|------|-------------|------|
| `get_dividend` | `stock_dividend_cninfo()` | 不定期更新 |
| `get_dividend_fhps` | `stock_fhps_em()` | 不定期更新 |
| `get_dividend_all` | `stock_dividend_cninfo()` | 不定期更新 |
| `get_share_change` | `stock_share_change_cninfo()` | 不定期更新 |
| `get_share_change_cninfo` | `stock_share_change_cninfo()` | 不定期更新 |
| `get_shareholder_change_ths` | `stock_shareholder_change_ths()` | 不定期更新 |
| `get_holding_change_em` | `stock_gdfx_holding_change_em()` | 不定期更新 |
| `get_pledge_ratio_em` | `stock_gpzy_pledge_ratio_em()` | 不定期更新 |
| `get_equity_mortgage_cninfo` | `stock_cg_equity_mortgage_cninfo()` | 不定期更新 |
| `get_unlock_schedule` | `stock_restricted_release_detail_em()` | 不定期更新 |
| `get_unlock_queue_sina` | `stock_restricted_release_queue_sina()` | 不定期更新 |
| `get_unlock_summary_em` | `stock_restricted_release_summary_em()` | 不定期更新 |
| `get_unlock_detail_em` | `stock_restricted_release_detail_em()` | 不定期更新 |
| `get_unlock_summary` | `stock_restricted_release_summary_em()` | 不定期更新 |

### 2.8 估值（2个）

| 方法 | akshare 调用 | 原因 |
|------|-------------|------|
| `get_index_valuation` | `index_value_hist_fina()` | 按指数查询，命中率低 |
| `get_stock_valuation_baidu` | `stock_zh_valuation_baidu()` | 按股票查询，命中率低 |

### 2.9 宏观数据（1个）

| 方法 | akshare 调用 | 原因 |
|------|-------------|------|
| `get_macro_raw` | `macro_china_pmi/cpi/ppi/gdp/m2_yearly/...` | 月度/季度更新，数据量小 |

### 2.10 其他低频列表（10个）

| 方法 | akshare 调用 | 原因 |
|------|-------------|------|
| `get_st_stocks` | `stock_zh_a_st_em()` | ST列表不定期变化 |
| `get_margin_underlying` | `stock_margin_underlying_info_sse/szse()` | 两融标的列表不定期调整 |
| `get_forecast` | `stock_profit_forecast()` | 业绩预告不定期更新 |
| `get_forecast_ths` | `stock_profit_forecast_ths()` | 同花顺业绩预告 |
| `get_conversion_bond_list` | `bond_zh_cov()` | 可转债列表仅在新债发行时变化 |
| `get_fund_name_list` | `fund_name_em()` | 基金名称列表极少变化 |
| `get_fund_open_info` | `fund_open_fund_info_em()` | 场外基金基本信息，静态数据 |
| `get_bond_cb_jsl` | `bond_cb_jsl()` | 集思录可转债列表，变化不频繁 |
| `get_futures_display_main` | `futures_display_main_sina()` | 期货合约列表，变化不频繁 |
| `get_bond_yield` | `bond_china_yield()` | 债券收益率月度更新 |

---

## 3. 低频数据，需要缓存（约87个，仅3个已实现缓存）

这类接口数据更新频率低但数据量大/调用成本高/回测复用率高，强烈建议添加缓存。

### 3.1 已实现缓存（3个）

| 方法 | akshare 调用 | 缓存原因 |
|------|-------------|---------|
| `get_daily_data` | `stock_zh_a_hist()` | **回测核心数据**，每只股票每天调用，历史数据跨越数年，同一股票在多次回测中反复查询 |
| `get_index_stocks` | `index_stock_cons()` | 回测中构建股票池时频繁调用，数据相对稳定 |
| `get_trading_days` | `tool_trade_date_hist_sina()` | 每次回测/日期计算都需要，全市场共享一份数据 |

### 3.2 P0 - 最高优先级（强烈建议添加缓存）

#### 日线行情类（14个）

| 方法 | akshare 调用 | 缓存原因 |
|------|-------------|---------|
| `get_etf_daily` | `_get_etf_daily()` | ETF 日线，回测中 ETF 策略频繁使用 |
| `get_index_daily` | `_get_index_daily()` | 指数日线，基准对比和因子计算基础数据 |
| `get_stock_hist` | `stock_zh_a_hist()` | 与 `get_daily_data` 功能重叠但独立入口，全市场扫描时批量调用 |
| `get_etf_hist` | `fund_etf_hist_em()` | ETF 历史行情，回测复用率高 |
| `get_lof_hist` | `fund_lof_hist_em()` | LOF 历史行情 |
| `get_conversion_bond_daily` | `bond_zh_cov_daily()` | 可转债日线，可转债策略回测反复使用 |
| `get_bond_zh_hs_daily` | `bond_zh_hs_daily()` | 可转债历史行情 |
| `get_futures_daily` | `futures_zh_daily_sina()` | 期货日线，CTA 策略回测核心数据 |
| `get_option_daily` | `option_finance_board()` | 期权日线，期权策略回测使用 |
| `get_option_sse_daily` | `option_sse_daily_sina()` | 上交所期权日线 |
| `get_index_daily_raw` | `stock_zh_index_daily()` | 指数日线原始数据，与 `get_index_daily` 功能重叠 |
| `get_index_zh_a_hist` | `index_zh_a_hist()` | 指数A股历史行情 |
| `get_futures_main_em` | `futures_main_em()` | 期货主力合约行情 |
| `get_futures_sina_main` | `futures_sina_main_sina()` | 新浪期货主力合约 |

#### 指数成分/权重类（5个）

| 方法 | akshare 调用 | 缓存原因 |
|------|-------------|---------|
| `get_index_components` | `index_stock_cons_weight_csindex()` | 指数增强/Smart Beta 策略核心数据，调用成本高（需从中证指数网站爬取） |
| `get_index_stock_cons` | `index_stock_cons()` | 同上 |
| `get_index_stock_cons_weight_csindex` | `index_stock_cons_weight_csindex()` | 同上 |
| `get_index_component_sw` | `index_component_sw()` | 行业轮动策略反复使用 |
| `get_sw_index_cons` | `sw_index_cons()` | 同上 |

#### 财务数据类（5个）

| 方法 | akshare 调用 | 缓存原因 |
|------|-------------|---------|
| `get_finance_indicator` | `stock_financial_analysis_indicator()` | 价值投资/多因子回测核心数据，全市场5000+股票逐个查询，调用成本极高 |
| `get_financial_report` | `stock_financial_report_sina()` | 单只股票数十个字段，全市场扫描成本极高 |
| `get_financial_benefit` | `stock_financial_benefit_ths()` | 同上 |
| `get_cashflow` | `stock_financial_report_sina()` | 同上 |
| `get_financial_analysis_indicator` | `stock_financial_analysis_indicator()` | 与 `get_finance_indicator` 功能重叠 |

### 3.3 P1 - 高优先级（建议添加缓存）

#### 资金流向类（6个）

| 方法 | akshare 调用 | 缓存原因 |
|------|-------------|---------|
| `get_money_flow` | `stock_individual_fund_flow()` | 资金流因子回测反复使用，历史数据跨度大 |
| `get_north_money_flow` | `stock_hsgt_north_net_flow_in_em()` | 全市场共享数据，每次查询获取全部历史 |
| `get_individual_fund_flow` | `stock_individual_fund_flow()` | 同上 |
| `get_hsgt_north_net_flow` | `stock_em_hsgt_north_net_flow_in()` | 北向资金净流入 |
| `get_hsgt_hold_stock` | `stock_em_hsgt_hold_stock()` | 北向资金持股统计 |
| `get_hsgt_individual_stock_flow` | `stock_em_hsgt_individual_stock_flow()` | 个股北向资金流入，单只股票反复查询 |

#### 行业/概念板块类（9个）

| 方法 | akshare 调用 | 缓存原因 |
|------|-------------|---------|
| `get_industry_stocks` | `index_component_sw()` | 行业轮动/行业中性策略核心数据 |
| `get_industry_mapping` | `_get_all_industry_mapping()` | 全市场5000+股票映射，每次因子计算都要查 |
| `get_industry_list` | `stock_board_industry_name_em()` | 初始化时查询一次即可 |
| `get_industry_components` | `stock_board_industry_cons_em()` | 行业成分股 |
| `get_concept_list` | `stock_board_concept_name_em()` | 概念板块列表 |
| `get_concept_components` | `stock_board_concept_cons_em()` | 概念板块成分股 |
| `get_sw_industry` | `sw_index_first_info()` | 申万行业数据 |
| `get_sw_index_info` | `sw_index_info()` | 申万行业指数信息 |
| `get_company_industry_em` | `stock_board_industry_name_em()` | 公司行业信息 |

#### 股东/持股类（8个）

| 方法 | akshare 调用 | 缓存原因 |
|------|-------------|---------|
| `get_top10_holders` | `stock_zh_a_gdhs()` | 公司治理/机构持股因子使用 |
| `get_top10_holders_em` | `stock_gdfx_holding_detail_em()` | 同上 |
| `get_top10_float_holders` | `stock_zh_a_gdhs_detail_em()` | 同上 |
| `get_top10_float_holders_em` | `stock_gdfx_free_holding_detail_em()` | 同上 |
| `get_holder_count` | `stock_hold_num_cninfo()` | 筹码集中度因子使用 |
| `get_institutional_holders` | `stock_institute_hold()` | 机构持股 |
| `get_fund_hold_stock` | `stock_fund_hold_stock()` | 基金持股 |
| `get_fund_portfolio` | `fund_portfolio_em()` | FOF 策略核心数据 |

#### 估值类（4个）

| 方法 | akshare 调用 | 缓存原因 |
|------|-------------|---------|
| `get_index_valuation` | `index_value_hist_fina()` | 估值因子回测反复使用 |
| `get_stock_valuation` | `stock_a_lg_indicator()` | 全市场扫描成本高 |
| `get_stock_pe_pb` | `stock_a_pe_and_pb()` | 价值因子核心数据 |
| `get_stock_valuation_baidu` | `stock_zh_valuation_baidu()` | 百度估值数据 |

### 3.4 P2 - 中优先级（建议添加缓存）

| 类别 | 数量 | 说明 |
|------|------|------|
| 分红/解禁/股本类 | 14 | 事件驱动策略使用，不定期更新但回测反复查询 |
| 证券元数据类 | 10 | 初始化/全市场扫描时调用，数据量大 |
| 宏观数据类 | 1 | 宏观因子回测反复使用 |
| 融资融券类 | 2 | 两融因子回测使用 |

### 3.5 P3 - 低优先级（可选缓存）

| 类别 | 数量 | 说明 |
|------|------|------|
| 龙虎榜/预告/停牌类 | 4 | 事件驱动策略使用 |
| 债券收益率类 | 1 | 无风险利率是因子计算基础数据 |
| 基金净值类 | 4 | 基金策略回测核心数据 |

---

## 4. 数据太大，需要提前拉好存起来（约30个）

这类接口返回全市场或大批量数据，适合定期批量拉取存入数据库，而非按需查询。

### 4.1 第一梯队 - 必须预存

| # | 方法 | 数据规模 | 预存策略 |
|---|------|---------|---------|
| 1 | `get_spot_em()` | ~5000股 x 30字段 ≈ 15万单元格 | **每日收盘后**批量拉取，存入 `market_spot_daily` 表 |
| 2 | `get_individual_fund_flow_rank()` | ~5000股 x 多周期 | **每日收盘后**批量拉取各周期（今日/3日/5日/10日） |
| 3 | `get_sector_money_flow()` | 行业~100 + 概念~300 x 多字段 | **每日收盘后**批量拉取，存入 `sector_fund_flow` 表 |
| 4 | `get_hsgt_hold_stock()` | 数百只北向持股 x 多字段 | **每日收盘后**批量拉取，存入 `hsgt_hold_daily` 表 |
| 5 | `get_billboard_list()` | 每日几十到上百条记录 | **每日收盘后**批量拉取，存入 `billboard_daily` 表 |

### 4.2 第二梯队 - 建议预存

| # | 方法 | 数据规模 | 预存策略 |
|---|------|---------|---------|
| 6 | `get_st_stocks` | ST股票列表，约几百只 | **每日更新**，存入 `st_status_daily` 表 |
| 7 | `get_suspended_stocks` | 停牌股票列表 | **每日更新**，存入 `suspended_daily` 表 |
| 8 | `get_unlock_summary` | 全市场解禁汇总 | **每周更新**，存入 `unlock_summary` 表 |
| 9 | `get_holding_change_em`(无参) | 全市场增减持，量大 | **每日/每周**批量拉取 |
| 10 | `get_dividend_fhps`(无参) | 全市场分红送股 | **财报季**批量拉取 |
| 11 | `get_margin_underlying` | 两融标的 ~2000只 | **定期更新**（标的调整不频繁） |
| 12 | `get_suspension_em` | 每日停牌数据 | **每日更新** |

### 4.3 基础元数据 - 应缓存

| # | 方法 | 数据规模 | 预存策略 |
|---|------|---------|---------|
| 13 | `get_trade_dates` | ~7000+ 条历史交易日 | **一次性拉取 + 增量更新** |
| 14 | `get_securities_code_name` | ~5000+ 只A股 | **每日更新**（新股/退市） |
| 15 | `get_fund_name_list` | 万只级别基金 | **每周更新** |
| 16 | `get_index_stock_info` | 数千个指数 | **一次性拉取 + 定期更新** |
| 17 | `get_industry_list` | ~100个行业板块 | 低频更新，缓存即可 |
| 18 | `get_concept_list` | ~300个概念板块 | 低频更新，缓存即可 |
| 19 | `get_sw_industry` | ~30个申万一级行业 | 极低频更新，缓存即可 |
| 20 | `get_conversion_bond_list` | 数百只可转债 | **每日更新**（新发/到期） |
| 21 | `get_bond_cb_jsl` | 数百只集思录可转债 | **每日更新** |
| 22 | `get_fund_open_daily` | 万只基金净值 | **每日收盘后**批量拉取 |
| 23 | `get_lof_spot` | LOF实时行情列表 | **每日收盘后**批量拉取 |
| 24 | `get_futures_spot` | 期货实时行情 | **每日收盘后**批量拉取 |
| 25 | `get_sw_index_daily_spot` | 申万行业指数实时行情 | **每日收盘后**批量拉取 |

### 4.4 宏观数据 - 低频全量

| # | 方法 | 数据规模 | 预存策略 |
|---|------|---------|---------|
| 26 | `get_macro_raw` | 各指标数百条历史数据 | **月度/季度发布后更新** |
| 27 | `get_bond_yield` | 债券收益率历史数据 | **月度更新** |

### 4.5 期权当日行情 - 量大但时效性强

| # | 方法 | 数据规模 | 预存策略 |
|---|------|---------|---------|
| 28 | `get_option_current_day_sse` | 上交所期权全量，数千合约 | **每日收盘后**批量拉取 |
| 29 | `get_option_current_day_szse` | 深交所期权全量 | **每日收盘后**批量拉取 |
| 30 | `get_option_cffex_hs300_spot` | 中金所期权行情 | **每日收盘后**批量拉取 |

### 4.6 建议的批量更新调度方案

```
每日 15:30 (收盘后30分钟):
  - get_spot_em
  - get_individual_fund_flow_rank (今日/3日/5日/10日)
  - get_sector_money_flow (行业+概念)
  - get_hsgt_hold_stock
  - get_billboard_list
  - get_st_stocks / get_suspended_stocks
  - get_fund_open_daily
  - get_sw_index_daily_spot

每周一次 (周末):
  - get_securities_code_name (检查新股/退市)
  - get_fund_name_list
  - get_unlock_summary
  - get_margin_underlying

每月/季度:
  - get_macro_raw (各指标按发布频率)
  - get_dividend_fhps (财报季)
```

---

## 5. 其他特殊情况

### 5.1 反爬/频率限制风险

| 方法 | akshare 调用 | 风险说明 | 建议 |
|------|-------------|---------|------|
| `get_spot_em()` | `stock_zh_a_spot_em()` | 全市场实时行情，高频调用极易触发反爬 | 调用间隔 >= 3秒；考虑本地缓存 + 定时刷新 |
| `get_individual_fund_flow_rank()` | `stock_individual_fund_flow_rank()` | 全市场资金流向排名，调用频繁易被封 | 仅盘中必要时调用，缓存当日结果 |
| `get_sector_money_flow()` | `stock_board_industry/concept_fund_flow_rank()` | 东方财富接口有严格频率限制 | 每日调用 1-2 次，结果缓存 |
| `get_securities_list()` | `stock_info_a_code_name()` | 全市场代码映射，频繁调用无意义 | 每日更新一次即可 |
| `get_billboard_list()` | `stock_lhb_detail_em()` | 龙虎榜数据，接口稳定性一般 | 按日期调用，结果应持久化 |
| `get_company_industry_em()` | `stock_board_industry_name_em()` | 按股票查行业，接口参数敏感 | 批量查询时加延时 |

### 5.2 数据源稳定性差

| 方法 | akshare 调用 | 风险说明 | 建议 |
|------|-------------|---------|------|
| `get_trading_days()` | `tool_trade_date_hist_sina()` | **强依赖新浪数据源**，接口偶尔不可用 | 增加本地静态交易日列表作为兜底 |
| `get_security_info()` | `stock_individual_info_em()` | 依赖东方财富，字段结构可能变化 | 异常时返回默认值（代码已处理），需监控字段变更 |
| `get_index_valuation()` | `index_value_hist_fina()` | **中证指数官网稳定性较差** | 建议预存历史估值数据，定期增量更新 |
| `get_futures_daily()` | `futures_zh_daily_sina()` | 依赖新浪期货，合约代码格式特殊 | 注意主力合约切换时的代码变化 |
| `get_option_daily()` | `option_finance_board()` | 期权数据源不稳定，品种代码复杂 | 建议增加重试逻辑（当前无重试） |
| `get_macro_raw()` 系列 | `macro_china_pmi/cpi/ppi/gdp/...` | 宏观数据依赖多个外部源，发布延迟常见 | 数据更新不规律，建议宽松 TTL + 异常容忍 |

### 5.3 特殊参数要求

| 方法 | akshare 调用 | 特殊要求 | 建议 |
|------|-------------|---------|------|
| `get_daily_data()` / `get_stock_hist()` | `stock_zh_a_hist()` | **日期格式要求 YYYYMMDD（无横杠）**，代码中已做 `.replace("-", "")` 转换 | 注意：如果传入的日期含时分秒会导致格式错误 |
| `get_margin_detail()` | `stock_margin_detail_sse(date)` / `stock_margin_detail_szse(date)` | **仅支持交易日**，非交易日调用会报错或返回空 | 调用前需校验日期是否为交易日 |
| `get_unlock_detail_em()` | `stock_restricted_release_detail_em(start_date, end_date)` | 日期跨度太大会超时 | 建议按月分段查询 |
| `get_call_auction_raw()` | `stock_zh_a_hist_pre_min_em(start_time, end_time)` | **需要时间字符串参数**（如 "09:15:00"），非日期 | 注意时间格式校验 |
| `get_fund_net_value_hist()` | `fund_open_fund_info_em(fund, indicator)` | **indicator 参数决定返回数据类型**（"单位净值走势" / "累计净值走势" 等） | 参数值需严格匹配，建议用枚举约束 |
| `get_hsgt_hold_stock()` | `stock_em_hsgt_hold_stock(symbol, indicator)` | symbol 和 indicator 组合决定数据维度 | 参数组合多，需文档说明 |
| `get_dividend_fhps()` | `stock_fhps_em(symbol/date)` | **symbol 和 date 二选一**，都不传则返回全量 | 全量调用数据量极大，应限制 |
| `get_holding_change_em()` | `stock_gdfx_holding_change_em(symbol/date)` | 同上，symbol 和 date 二选一 | 同上 |
| `get_share_change_cninfo()` | `stock_share_change_cninfo(symbol, start_date?, end_date?)` | 日期参数可选，但巨潮接口对日期范围敏感 | 建议始终传入日期范围 |

### 5.4 有 Fallback 逻辑的接口

以下接口优先使用 `market_data` 模块，失败后 fallback 到直接调用 akshare：

| 方法 | 优先使用 | Fallback |
|------|---------|---------|
| `get_daily_data()` | `market_data.stock.get_stock_daily` | `akshare.stock_zh_a_hist()` + 重试 |
| `get_index_stocks()` | `market_data.index.get_index_stocks` | `akshare.index_stock_cons()` |
| `get_index_components()` | `market_data.index_components.get_index_components` | `akshare.index_stock_cons_weight_csindex()` |
| `get_minute_data()` | `market_data.minute.get_stock_minute` | `akshare.stock_zh_a_minute()` |
| `get_money_flow()` | `market_data.money_flow.get_money_flow` | `akshare.stock_individual_fund_flow()` |
| `get_north_money_flow()` | `market_data.north_money.get_north_money_flow` | `akshare.stock_hsgt_north_net_flow_in_em()` |
| `get_industry_stocks()` | `market_data.industry_sw.get_industry_stocks_sw` | `akshare.index_component_sw()` |
| `get_etf_daily()` | `market_data.etf.get_etf_daily` | `get_daily_data(adjust="none")` |
| `get_index_daily()` | `market_data.index.get_index_daily` | `get_daily_data(adjust="none")` |
| `get_finance_indicator()` | `finance_data.finance.get_finance_indicator` | `akshare.stock_financial_analysis_indicator()` |

**架构弱点**：
- `get_industry_mapping()` 和 `get_call_auction()` **完全没有 akshare fallback**，如果 market_data 模块不可用则直接失败
- 建议在 `get_industry_mapping()` 中补充 akshare 的 `stock_board_industry_name_em()` 作为备选
- 建议在 `get_call_auction()` 中补充 `stock_zh_a_hist_pre_min_em()` 作为备选

### 5.5 分钟级高频历史数据（数据量巨大但有回测价值）

| 方法 | akshare 调用 | 特殊情况 | 建议 |
|------|-------------|---------|------|
| `get_minute_data()` | `stock_zh_a_minute()` | **不支持日期范围过滤**，全量拉取 | 强烈建议缓存 + 按需拉取 |
| `get_stock_minute_raw()` | `stock_zh_a_hist_min_em()` | 支持日期范围，但**每分钟级数据量极大**（每天 240 条） | 按周/月分段拉取；缓存策略需精细设计 |
| `get_etf_minute_raw()` | `fund_etf_hist_min_em()` | ETF 分钟数据，同上 | 同上 |
| `get_lof_hist_min()` | `fund_lof_hist_min_em()` | LOF 分钟数据，流动性差的数据可能缺失 | 注意数据完整性校验 |
| `get_call_auction_raw()` | `stock_zh_a_hist_pre_min_em()` | 集合竞价数据（9:15-9:25），**时间窗口极窄** | 仅回测有价值，缓存粒度需到日 |

### 5.6 跨市场/跨品种接口

#### 期货（5个）

| 方法 | akshare 调用 | 特殊情况 |
|------|-------------|---------|
| `get_futures_daily()` | `futures_zh_daily_sina()` | 合约代码格式特殊（如 "RB0" 主力连续） |
| `get_futures_spot()` | `futures_zh_spot()` | 实时数据，无法缓存 |
| `get_futures_main_em()` | `futures_main_em()` | 主力合约会切换，历史数据可能断裂 |
| `get_futures_sina_main()` | `futures_sina_main_sina()` | 与东方财富主力可能不一致 |
| `get_futures_display_main()` | `futures_display_main_sina()` | 合约数量多，包含过期合约 |

#### 期权（6个）

| 方法 | akshare 调用 | 特殊情况 |
|------|-------------|---------|
| `get_option_daily()` | `option_finance_board()` | 期权品种极多（数千个合约） |
| `get_option_current_day_sse()` | `option_current_day_sse()` | 上交所期权实时 |
| `get_option_current_day_szse()` | `option_current_day_szse()` | 深交所期权实时 |
| `get_option_cffex_hs300_spot()` | `option_cffex_hs300_spot_sina()` | 中金所期权，第三交易所 |
| `get_option_sse_greeks()` | `option_sse_greeks_sina()` | 期权希腊字母，计算值依赖模型参数 |
| `get_option_sse_daily()` | `option_sse_daily_sina()` | 上交所期权日线 |

#### 可转债（4个）

| 方法 | akshare 调用 | 特殊情况 |
|------|-------------|---------|
| `get_conversion_bond_list()` | `bond_zh_cov()` | 全量可转债，数量持续增长 |
| `get_conversion_bond_daily()` | `bond_zh_cov_daily()` | 单只可转债历史行情 |
| `get_bond_cb_jsl()` | `bond_cb_jsl()` | 依赖集思录网站，稳定性未知 |
| `get_bond_zh_hs_daily()` | `bond_zh_hs_daily()` | 另一数据源，可与 bond_zh_cov_daily 对比 |

#### 基金（6个）

| 方法 | akshare 调用 | 特殊情况 |
|------|-------------|---------|
| `get_etf_hist()` | `fund_etf_hist_em()` | 东方财富 ETF 数据，代码格式需验证 |
| `get_lof_hist()` | `fund_lof_hist_em()` | 东方财富 LOF 数据 |
| `get_fund_of_nav()` | `fund_etf_fund_info_em()` | 函数名与用途不完全匹配 |
| `get_fund_open_daily()` | `fund_open_fund_daily_em()` | 全市场开放式基金，数据量大 |
| `get_fund_open_info()` | `fund_open_fund_info_em()` | indicator 参数控制返回类型 |
| `get_fund_portfolio()` | `fund_portfolio_em()` | 季度更新，非实时 |

### 5.7 其他值得注意的特殊情况

| 方法 | akshare 调用 | 特殊情况 | 建议 |
|------|-------------|---------|------|
| `get_index_components()` | `index_stock_cons_weight_csindex()` | 内部有**嵌套 try-except**，先尝试获取权重，失败后 fallback 到等权重估算 | 等权重假设可能引入偏差，需在文档中说明 |
| `get_daily_data()` | `stock_zh_a_hist()` | 有**手动重试循环**（`max_retries` + `retry_delay`），是文件中唯一显式重试的接口 | 其他接口也应考虑增加重试 |
| 所有 `get_top10_holders*` / `get_holder_count` / `get_institutional_holders` | 多个股东相关接口 | **无任何缓存和重试**，且股东数据变化频率极低（季度） | 强烈建议增加缓存，TTL 可设为 90 天 |
| 所有 `get_financial_*` 系列 | 多个财务接口 | 财务数据**季度更新**，但当前无任何缓存策略 | 建议缓存 TTL >= 90 天 |
| `get_dividend_all()` | `stock_dividend_cninfo()` | **全市场分红数据**，无参数时返回全量，数据量巨大 | 默认调用应限制或提示 |
| `get_unlock_summary()` | `stock_restricted_release_summary_em()` | 全市场解禁汇总，数据量大 | 建议缓存 |
| `get_fund_name_list()` | `fund_name_em()` | 全市场基金列表，数量庞大 | 缓存 + 定期更新 |
| `get_stock_valuation_baidu()` | `stock_zh_valuation_baidu()` | 依赖百度数据源，与其他接口数据源不同 | 注意百度接口的稳定性 |
| `get_index_daily_raw()` | `stock_zh_index_daily()` | 返回**原始 DataFrame**，未做字段标准化 | 调用方需自行处理字段名 |
| `get_individual_fund_flow()` | `stock_individual_fund_flow()` | 需要 `market` 参数（"sh"/"sz"），但方法签名中 market 有默认值 | 默认值可能与实际代码不匹配，需校验 |

---

## 总结与建议

### 缓存优先级矩阵

```
P0（立即实施）
├── 日线行情类（14个）- 回测核心，复用率最高
├── 指数成分/权重类（5个）- 调用成本高
└── 财务数据类（5个）- 全市场扫描成本极高

P1（近期实施）
├── 资金流向类（6个）
├── 行业/概念板块类（9个）
├── 股东/持股类（8个）
└── 估值类（4个）

P2（中期实施）
├── 分红/解禁/股本类（14个）
├── 证券元数据类（10个）
├── 宏观数据类（1个）
└── 融资融券类（2个）

P3（可选实施）
├── 龙虎榜/预告/停牌类（4个）
├── 债券收益率类（1个）
└── 基金净值类（4个）
```

### 关键改进方向

1. **统一缓存策略**：当前仅 3/100+ 接口有缓存，建议建立统一的缓存管理层
2. **增加重试机制**：仅 `get_daily_data()` 有重试逻辑，其他接口均应增加
3. **补充 Fallback**：`get_industry_mapping()` 和 `get_call_auction()` 无 akshare fallback
4. **批量预存调度**：建立收盘后批量拉取机制，减少实时请求压力
5. **反爬防护**：对高频接口增加调用间隔控制和结果缓存
