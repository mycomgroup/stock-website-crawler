# JoinQuant Data API 严格对照

基于原始文档目录：
- https://github.com/mycomgroup/stock-website-crawler/tree/main/skills/joinquant_nookbook/joinquant_doc/doc

本清单按“文档表名/接口名”对照当前代码的真实实现状态，重点区分：
- 模块内已实现
- 已接入全局统一入口 `jqdata_akshare_backtrader_utility.finance`
- 已做文档命名兼容

## 总览

| 任务 | 文档主题 | 模块实现 | 全局入口 | 命名兼容 | 结论 |
|---|---|---|---|---|---|
| 1 | 上市公司基本信息/状态变动/上市信息 | 是 | 是 | 基本一致 | 已完成 |
| 2 | 前10大股东/流通股东/股东户数 | 是 | 是 | 一致 | 已完成 |
| 3 | 公司行为/分红送股 | 是 | 是 | 已补 `STK_DIVIDEND_RIGHT` | 基本完成 |
| 4 | 质押/冻结/增减持/股本变动 | 是 | 是 | 一致 | 基本完成 |
| 5 | 限售解禁/预计解禁/实际解禁 | 是 | 是 | 已补 `STK_UNLOCK_DATE` | 基本完成 |
| 6 | 可转债 | 是 | 是 | 一致 | 基本完成 |
| 7 | 期权 | 是 | 是 | 一致 | 基本完成 |
| 8 | 指数成分股及权重 | 是 | 是 | 一致 | 基本完成 |
| 9 | 申万行业 | 是 | 是 | 已补 `STK_SW_INDUSTRY` | 基本完成 |
| 10 | 宏观数据 | 是 | 是 | 已补 `MAC_ECONOMIC_DATA` | 基本完成 |

## 逐项结果

### 任务 1

- 文档：`10016`、`10023`、`10025`
- 当前实现：
  - `get_company_info`
  - `get_security_status`
  - `finance.STK_COMPANY_BASIC_INFO`
  - `finance.STK_STATUS_CHANGE`
- 代码位置：
  - `jqdata_akshare_backtrader_utility/finance_data/company_info.py`
  - `jqdata_akshare_backtrader_utility/backtrader_base_strategy.py`

### 任务 2

- 文档：`10011`、`10012`、`10015`
- 当前实现：
  - `get_top10_shareholders`
  - `get_top10_float_shareholders`
  - `get_shareholder_count`
  - `finance.STK_SHAREHOLDER_TOP10`
  - `finance.STK_SHAREHOLDER_FLOAT_TOP10`
  - `finance.STK_SHAREHOLDER_NUM`
- 本次补齐：
  - Schema 字段对齐：`shareholder_code`, `change_amount`, `holder_num_change`, `holder_num_change_ratio`
  - 日期字段命名统一：`report_date`, `ann_date`
  - 空结果 Schema 保障

### 任务 3

- 文档：`10010`、`10022`
- 当前实现：
  - `get_dividend_info`
  - `get_adjust_factor`
  - `get_rights_issue`
  - `get_next_dividend`
  - `finance.STK_XR_XD`
- 本次补齐：
  - 全局 `finance.STK_DIVIDEND_RIGHT` 文档别名

### 任务 4

- 文档：`10013`、`10014`、`10017`、`10018`
- 当前实现：
  - `get_pledge_info`
  - `get_major_holder_trade`
  - `get_share_change`
  - `get_shareholder_changes`
  - `finance.STK_SHARE_PLEDGE`
  - `finance.STK_SHARE_FREEZE`
  - `finance.STK_TOPHOLDER_CHANGE`
  - `finance.STK_CAPITAL_CHANGE`
- 本次补齐：
  - 接入全局 `finance.run_query`

### 任务 5

- 文档：`10019`、`10020`、`10021`
- 当前实现：
  - `get_unlock_schedule`
  - `get_unlock_pressure`
  - `get_unlock_calendar`
  - `get_upcoming_unlocks`
  - `get_unlock_history`
  - `analyze_unlock_impact`
  - `finance.STK_LOCK_UNLOCK`
  - `finance.STK_LOCK_SHARE`
- 本次补齐：
  - 全局 `finance.STK_UNLOCK_DATE` 文档别名

### 任务 6

- 文档：`10293`
- 当前实现：
  - `get_conversion_bond_list`
  - `get_conversion_bond_quote`
  - `get_conversion_info`
  - `get_conversion_value`
  - `query_conversion_bond_basic`
  - `query_conversion_bond_price`
  - `finance.STK_CONVERSION_BOND_BASIC`
  - `finance.STK_CONVERSION_BOND_PRICE`
- 本次补齐：
  - 接入全局 `finance.run_query`

### 任务 7

- 文档：`10030`、`10251`、`10252`
- 当前实现：
  - `get_option_list`
  - `get_option_quote`
  - `get_option_greeks`
  - `get_option_chain`
  - `finance.STK_OPTION_BASIC`
  - `finance.STK_OPTION_DAILY`
- 本次补齐：
  - 接入全局 `finance.run_query`

### 任务 8

- 文档：`10291`
- 当前实现：
  - `get_index_components`
  - `get_index_weights`
  - `get_index_component_history`
  - `finance.STK_INDEX_COMPONENTS`
  - `finance.STK_INDEX_WEIGHTS`
- 本次补齐：
  - 接入全局 `finance.run_query`

### 任务 9

- 文档：`10282`
- 当前实现：
  - `get_stock_industry`
  - `get_industry_stocks` (支持 `level` 参数)
  - `get_industry_category`
  - `finance.STK_INDUSTRY_SW`
- 本次补齐：
  - 文档别名 `finance.STK_SW_INDUSTRY` ✅
  - 补充 `finance.STK_SW_INDUSTRY_STOCK` 到统一入口 ✅
  - 行业成分股返回结构稳定化 ✅
  - 测试覆盖别名兼容性 ✅

### 任务 10

- 文档：`10289`
- 当前实现：
  - `get_macro_data`
  - `get_macro_series`
  - `get_macro_indicators`
  - `finance.MACRO_ECONOMIC_DATA`
- 本次补齐：
  - 文档别名 `finance.MAC_ECONOMIC_DATA`

## 仍需继续核实的点

- 原始 JoinQuant 文档正文里的字段级细节，还需要逐篇拉取后做字段级核对。
- `query(...).filter(...)` 的过滤表达式在统一入口里历史上实现并不完整，本次优先修复的是表接入与别名兼容。
- 某些模块已支持的历史查询能力，仍建议用现有测试进一步验证。
