# JoinQuant Data Source

JoinQuant 数据源，通过 Notebook 执行获取各类金融数据。

## 目录结构

```
data_source/
├── joinquant_data_executor.py  # 执行器（Notebook 端运行）
├── joinquant_data_cli.js       # CLI 脚本
├── test_joinquant_data.py       # 测试脚本
└── README.md                    # 本文件
```

## 快速开始

### 1. 抓取 Session

```bash
# 首次使用需要抓取 session
node browser/capture-joinquant-session.js --notebook-url "YOUR_NOTEBOOK_URL" --headed
```

### 2. 通过 CLI 调用

```bash
# 列出所有可用方法
node data_source/joinquant_data_cli.js --list

# 调用方法
node data_source/joinquant_data_cli.js --function get_stock_daily --params '{"symbol":"000001.XSHE","count":5}'

# 获取股票列表
node data_source/joinquant_data_cli.js --function get_all_securities --params '{"types":["stock"],"date":"2024-01-02"}'

# 获取因子数据
node data_source/joinquant_data_cli.js --function get_factor_kanban_values --params '{"universe":"hs300","bt_cycle":"month_3"}'

# 获取交易日
node data_source/joinquant_data_cli.js --function get_trade_days --params '{"start_date":"2024-01-01","end_date":"2024-01-10"}'
```

### 3. 通过 Python 测试

```bash
# 运行完整测试
node run-strategy.js --strategy data_source/test_joinquant_data.py --timeout-ms 180000

# 或直接运行快速测试
node run-strategy.js --strategy data/test_quick.py --timeout-ms 120000
```

## 方法列表

### 行情数据

| 方法 | 说明 | 参数 |
|------|------|------|
| `get_stock_daily` | 获取股票日线行情 | symbol, start_date?, end_date?, count?, adjust? |
| `get_stock_daily_batch` | 批量获取股票日线 | symbols, start_date?, end_date?, count?, adjust? |
| `get_stock_minute` | 获取分时行情 | symbol, date, freq? |
| `get_call_auction` | 获取集合竞价数据 | symbol, date |

### 估值数据

| 方法 | 说明 | 参数 |
|------|------|------|
| `get_valuation` | 获取股票估值 | symbol, start_date?, end_date? |
| `get_index_valuation` | 获取指数估值 | index_symbol, start_date?, end_date? |

### 财务数据

| 方法 | 说明 | 参数 |
|------|------|------|
| `get_financial` | 获取财务报表 | symbol, table?, period? |
| `get_finance_indicators` | 获取财务指标 | symbol, start_date?, end_date? |
| `get_dividend` | 获取分红数据 | symbol |

### 指数与行业

| 方法 | 说明 | 参数 |
|------|------|------|
| `get_index_daily` | 获取指数日线 | symbol, start_date?, end_date?, count? |
| `get_index_components` | 获取指数成分股 | index_symbol, date |
| `get_industry_list` | 获取行业列表 | level? |
| `get_industry_classification` | 获取行业分类 | symbols, level? |

### 宏观与情绪

| 方法 | 说明 | 参数 |
|------|------|------|
| `get_market_spot` | 全市场行情快照 | date |
| `get_money_flow` | 资金流向 | symbol, start_date?, end_date? |
| `get_analyst_forecast` | 分析师预测 | symbol, start_date?, end_date? |
| `get_shareholder_data` | 股东数据 | symbol, start_date?, end_date? |

### 辅助数据

| 方法 | 说明 | 参数 |
|------|------|------|
| `get_trading_calendar` | 交易日历 | start_date?, end_date? |
| `get_stock_info` | 股票基本信息 | symbol |

### 交易事件

| 方法 | 说明 | 参数 |
|------|------|------|
| `get_dragon_tiger_list` | 龙虎榜 | date |
| `get_limit_up_pool` | 涨停股池 | date |
| `get_restricted_release` | 限售解禁 | start_date?, end_date? |

### 板块与概念

| 方法 | 说明 | 参数 |
|------|------|------|
| `get_concept_list` | 概念板块列表 | - |
| `get_concept_constituents` | 概念板块成分股 | concept_code |
| `get_stock_industry` | 个股行业信息 | symbol |
| `get_st_stocks` | ST股票列表 | - |

### 基金与可转债

| 方法 | 说明 | 参数 |
|------|------|------|
| `get_etf_list` | ETF列表 | - |
| `get_etf_hist` | ETF历史行情 | symbol, start_date?, end_date? |
| `get_convert_bond_list` | 可转债列表 | - |
| `get_convert_bond_hist` | 可转债历史行情 | symbol, start_date?, end_date? |

### 因子数据

| 方法 | 说明 | 参数 |
|------|------|------|
| `get_all_factors` | 因子列表 | - |
| `get_factor_kanban_values` | 因子看板 | universe?, bt_cycle?, model?, category?, skip_paused?, commision_slippage? |

### 其他

| 方法 | 说明 | 参数 |
|------|------|------|
| `get_all_securities` | 股票列表 | types?, date? |
| `get_trade_days` | 交易日列表 | start_date?, end_date?, count? |

## 返回格式

- **DataFrame**: 直接返回 pandas DataFrame，CLI 会打印 shape 和内容
- **List/Dict**: JSON 序列化后返回
- **其他**: 直接打印

## 注意事项

1. 首次使用需要先抓取 session: `node browser/capture-joinquant-session.js --headed`
2. Session 有效期约 1 天，过期后需要重新抓取
3. 某些 API 需要聚宽机构账号权限
4. 返回结果不做 trim，由客户端统一处理