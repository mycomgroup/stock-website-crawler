# 需求文档

## 简介

本功能旨在补全量化交易框架对 JQData（聚宽）API 的兼容性。当前框架底层已有大量实现，但许多函数未通过 `src/api/__init__.py` 对外暴露；另有部分 JQData 核心 API 在底层也尚未实现。

目标分两层：
1. **暴露层**：将底层已有实现（`src/core/api_wrappers.py`、`src/core/runner.py`、`src/market_data/` 等）通过 `src/api/__init__.py` 统一对外导出。
2. **实现层**：对底层缺失的重要 JQData API，在 `src/api/` 下新建或扩展模块实现。

不在范围内的 API（回测引擎专用）：`run_daily`、`run_weekly`、`run_monthly`、`set_benchmark`、`set_slippage`、`set_order_cost`、`set_universe`、`set_option` 等。

## 词汇表

- **API_Layer**：`src/api/` 目录下的公开接口层，通过 `__init__.py` 统一导出
- **Core_Layer**：`src/core/api_wrappers.py` 和 `src/core/runner.py` 中的底层实现
- **Market_Data_Layer**：`src/market_data/` 目录下的行情数据模块
- **JQ_Code**：聚宽标准证券代码格式，如 `000001.XSHE`、`600519.XSHG`
- **SecurityInfo**：证券基本信息对象，包含 `display_name`、`name`、`start_date`、`end_date`、`type` 等属性
- **Caller**：调用 `src/api` 接口的策略代码或用户代码

## 需求

### 需求 1：暴露证券元数据 API

**用户故事：** 作为量化策略开发者，我希望通过 `src/api` 直接调用证券元数据接口，以便查询全市场证券列表和单支证券信息。

#### 验收标准

1. THE API_Layer 应导出 `get_all_securities(types, date)` 函数，其底层调用 `get_all_securities_jq`
2. THE API_Layer 应导出 `get_security_info(code, date)` 函数，其底层调用 `get_security_info_jq`
3. WHEN `get_all_securities` 被调用时，THE API_Layer 应返回包含 `display_name`、`name`、`start_date`、`end_date`、`type` 字段的 DataFrame
4. WHEN `get_security_info` 被调用时，THE API_Layer 应返回 SecurityInfo 对象，支持属性访问（如 `.display_name`、`.start_date`）
5. THE API_Layer 应同时导出 `get_all_securities_jq` 和 `get_security_info_jq` 作为底层别名，保持向后兼容
6. IF `code` 参数为无效证券代码，THEN THE API_Layer 应返回 None 或抛出明确的异常，而非静默失败


### 需求 2：暴露代码标准化 API

**用户故事：** 作为量化策略开发者，我希望通过 `src/api` 调用代码标准化接口，以便将各种格式的证券代码统一转换为聚宽标准格式。

#### 验收标准

1. THE API_Layer 应导出 `normalize_code(code)` 函数，将任意格式代码转换为 JQ_Code 格式
2. WHEN 输入 `000001` 时，THE API_Layer 应返回 `000001.XSHE`
3. WHEN 输入 `600519` 时，THE API_Layer 应返回 `600519.XSHG`
4. WHEN 输入已是 JQ_Code 格式的代码时，THE API_Layer 应原样返回该代码
5. THE API_Layer 应同时导出 `normalize_security_code` 作为 `normalize_code` 的别名

### 需求 3：暴露交易日历 API

**用户故事：** 作为量化策略开发者，我希望通过 `src/api` 调用交易日历接口，以便查询指定范围内的交易日。

#### 验收标准

1. THE API_Layer 应导出 `get_all_trade_days()` 函数，返回包含所有交易日的 numpy.ndarray
2. THE API_Layer 应导出 `get_trade_days(start_date, end_date, count)` 函数，返回指定范围内的交易日数组
3. WHEN `get_trade_days` 同时传入 `start_date` 和 `count` 时，THE API_Layer 应返回从 `start_date` 起的 `count` 个交易日
4. WHEN `get_trade_days` 同时传入 `end_date` 和 `count` 时，THE API_Layer 应返回 `end_date` 前的 `count` 个交易日（含 `end_date`）
5. IF `start_date` 和 `count` 同时与 `end_date` 一起传入，THEN THE API_Layer 应抛出 ValueError 提示参数冲突
6. THE API_Layer 应同时导出 `get_all_trade_days_jq` 作为底层别名

### 需求 4：暴露指数数据 API

**用户故事：** 作为量化策略开发者，我希望通过 `src/api` 调用指数相关接口，以便获取指数成分股和权重数据。

#### 验收标准

1. THE API_Layer 应导出 `get_index_stocks(index_code, date)` 函数，返回指数成分股代码列表
2. THE API_Layer 应导出 `get_index_weights(index_code, date)` 函数，返回包含 `weight`、`display_name` 字段的 DataFrame
3. WHEN `get_index_stocks` 被调用时，THE API_Layer 应返回 JQ_Code 格式的股票代码列表
4. WHEN `date` 参数为 None 时，THE API_Layer 应返回最新日期的数据
5. IF 指数代码不受支持，THEN THE API_Layer 应返回空列表并记录警告日志，而非抛出异常


### 需求 5：暴露财务数据 API

**用户故事：** 作为量化策略开发者，我希望通过 `src/api` 调用财务数据接口，以便查询股票基本面和估值数据。

#### 验收标准

1. THE API_Layer 应导出 `get_fundamentals(query_obj, date, statDate)` 函数，支持通过 query 对象查询财务数据
2. THE API_Layer 应导出 `get_valuation(security_list, end_date, fields, count)` 函数，返回市值、市盈率等估值数据
3. THE API_Layer 应导出 `get_history_fundamentals(security_list, fields, watch_date, count, interval, report_type)` 函数，返回多期历史财务数据
4. WHEN `get_fundamentals` 被调用时，THE API_Layer 应支持 `valuation`、`income`、`cash_flow`、`balance`、`indicator` 等数据表对象
5. THE API_Layer 应导出 `query` 函数，支持链式调用构建查询条件（如 `query(valuation).filter(...).limit(...)`）
6. IF `security_list` 为空列表，THEN THE API_Layer 应返回空 DataFrame 而非抛出异常

### 需求 6：暴露行业概念 API

**用户故事：** 作为量化策略开发者，我希望通过 `src/api` 调用行业概念接口，以便查询股票所属行业、行业成分股和概念板块数据。

#### 验收标准

1. THE API_Layer 应导出 `get_industry(security, date, df)` 函数，返回股票所属行业信息
2. THE API_Layer 应导出 `get_industries(name, date)` 函数，返回行业列表 DataFrame
3. THE API_Layer 应导出 `get_industry_stocks(industry_code, date)` 函数，返回行业成分股代码列表
4. THE API_Layer 应导出 `get_concepts()` 函数，返回概念板块列表 DataFrame
5. THE API_Layer 应导出 `get_concept_stocks(concept_code, date)` 函数，返回概念成分股代码列表
6. WHEN `get_industries` 的 `name` 参数为 `sw_l1` 时，THE API_Layer 应返回申万一级行业列表
7. WHEN `get_industries` 的 `name` 参数为 `zjw` 时，THE API_Layer 应返回证监会行业列表
8. WHEN `get_industry` 的 `df` 参数为 True 时，THE API_Layer 应返回 DataFrame 格式而非 dict 格式

### 需求 7：暴露集合竞价 API

**用户故事：** 作为量化策略开发者，我希望通过 `src/api` 调用集合竞价接口，以便获取股票开盘前的集合竞价数据。

#### 验收标准

1. THE API_Layer 应导出 `get_call_auction(security, start_date, end_date, fields)` 函数
2. WHEN `get_call_auction` 被调用时，THE API_Layer 应返回包含 `time`、`current`、`volume`、`money`、五档买卖价量字段的 DataFrame
3. WHEN `fields` 参数为 None 时，THE API_Layer 应返回全部字段
4. IF 指定日期范围内无集合竞价数据，THEN THE API_Layer 应返回空 DataFrame


### 需求 8：暴露额外信息 API（get_extras）

**用户故事：** 作为量化策略开发者，我希望通过 `src/api` 调用 get_extras 接口，以便查询股票 ST 状态、停牌状态等额外信息。

#### 验收标准

1. THE API_Layer 应导出 `get_extras(field, security_list, start_date, end_date, df, count)` 函数
2. WHEN `field` 为 `is_st` 时，THE API_Layer 应返回各股票在指定日期是否为 ST 的布尔值
3. WHEN `field` 为 `is_paused` 时，THE API_Layer 应返回各股票在指定日期是否停牌的布尔值
4. WHEN `df` 参数为 True 时，THE API_Layer 应返回 DataFrame 格式；WHEN `df` 为 False 时，应返回 dict 格式
5. THE API_Layer 应同时导出 `get_extras_jq` 作为底层别名

### 需求 9：实现融资融券 API

**用户故事：** 作为量化策略开发者，我希望通过 `src/api` 调用融资融券接口，以便查询股票的融资融券余额和标的列表。

#### 验收标准

1. THE API_Layer 应导出 `get_mtss(security_list, start_date, end_date, fields, count)` 函数，返回融资融券明细数据
2. WHEN `get_mtss` 被调用时，THE API_Layer 应返回包含 `date`、`sec_code`、`fin_value`、`fin_buy_value`、`fin_refund_value`、`sec_value`、`sec_sell_value`、`sec_refund_value`、`fin_sec_value` 字段的 DataFrame
3. THE API_Layer 应导出 `get_margincash_stocks(date)` 函数，返回融资标的股票代码列表
4. THE API_Layer 应导出 `get_marginsec_stocks(date)` 函数，返回融券标的股票代码列表
5. IF `start_date` 和 `count` 同时传入，THEN THE API_Layer 应抛出 ValueError 提示参数互斥
6. WHEN `fields` 参数为 None 时，THE API_Layer 应返回全部字段

### 需求 10：实现资金流向 API

**用户故事：** 作为量化策略开发者，我希望通过 `src/api` 调用资金流向接口，以便分析大单、中单、小单的资金流入流出情况。

#### 验收标准

1. THE API_Layer 应导出 `get_money_flow(security_list, start_date, end_date, fields, count)` 函数，返回日级别资金流向数据
2. WHEN `get_money_flow` 被调用时，THE API_Layer 应返回包含超大单、大单、中单、小单流入流出字段的 DataFrame
3. THE API_Layer 应支持的字段包括：`inflow_xl`、`inflow_l`、`inflow_m`、`inflow_s`、`outflow_xl`、`outflow_l`、`outflow_m`、`outflow_s`、`netflow_xl`、`netflow_l`、`netflow_m`、`netflow_s`
4. WHEN `fields` 参数为 None 时，THE API_Layer 应仅返回流入和流出字段，不包含净流入字段
5. IF 指定股票在某日停牌，THEN THE API_Layer 应对该日返回空行或 NaN，而非抛出异常


### 需求 11：实现沪深港通持股数据 API

**用户故事：** 作为量化策略开发者，我希望通过 `src/api` 查询北向资金持股数据，以便分析外资持仓变化。

#### 验收标准

1. THE API_Layer 应导出 `get_hk_hold_info(link_id, date, count)` 函数，返回沪深港通持股数据
2. WHEN `link_id` 为 310001 时，THE API_Layer 应返回沪股通持股数据
3. WHEN `link_id` 为 310002 时，THE API_Layer 应返回深股通持股数据
4. WHEN `get_hk_hold_info` 被调用时，THE API_Layer 应返回包含 `day`、`link_id`、`link_name`、`code`、`name`、`share_number`、`share_ratio` 字段的 DataFrame
5. IF 指定日期无数据，THEN THE API_Layer 应返回空 DataFrame

### 需求 12：实现 run_query 财务数据库查询接口

**用户故事：** 作为量化策略开发者，我希望通过 `src/api` 使用 `finance.run_query` 查询财务数据库，以便获取沪深市场成交概况、沪深港通持股等结构化数据。

#### 验收标准

1. THE API_Layer 应导出 `finance` 模块对象，支持 `finance.run_query(query_obj)` 调用方式
2. WHEN `finance.run_query` 被调用时，THE API_Layer 应返回 DataFrame，每行对应数据库中的一条记录
3. THE API_Layer 应支持 `finance.STK_EXCHANGE_TRADE_INFO` 表，包含沪深市场每日成交概况数据
4. THE API_Layer 应支持 `finance.STK_HK_HOLD_INFO` 表，包含沪深港通持股数据
5. THE API_Layer 应支持 `query(table).filter(...).limit(n)` 链式查询语法
6. IF 查询结果超过 5000 行，THEN THE API_Layer 应截断并记录警告，或支持 `run_offset_query` 分批获取

### 需求 13：暴露 Tick 数据 API

**用户故事：** 作为量化策略开发者，我希望通过 `src/api` 调用 Tick 数据接口，以便获取股票的逐笔成交数据。

#### 验收标准

1. THE API_Layer 应导出 `get_ticks(security, date, count, fields, skip, df)` 函数
2. WHEN `get_ticks` 被调用时，THE API_Layer 应返回包含时间、价格、成交量、买卖方向等字段的 DataFrame
3. WHEN `df` 参数为 True 时，THE API_Layer 应返回 DataFrame 格式
4. IF 指定日期无 Tick 数据，THEN THE API_Layer 应返回空 DataFrame


### 需求 14：统一 API 导出与向后兼容

**用户故事：** 作为量化策略开发者，我希望所有新增 API 都通过 `src/api/__init__.py` 统一导出，以便用一个导入路径访问全部接口。

#### 验收标准

1. THE API_Layer 应在 `__init__.py` 的 `__all__` 列表中包含所有新增导出符号
2. THE API_Layer 应按功能分组组织导出（证券元数据、交易日历、指数数据、财务数据、行业概念、行情数据、融资融券、资金流向、港通数据）
3. WHEN 执行 `from src.api import get_all_securities, get_security_info, normalize_code` 时，THE API_Layer 应无报错地完成导入
4. WHEN 执行 `from src.api import get_fundamentals, get_valuation, get_history_fundamentals` 时，THE API_Layer 应无报错地完成导入
5. WHEN 执行 `from src.api import get_industry, get_industries, get_industry_stocks, get_concepts, get_concept_stocks` 时，THE API_Layer 应无报错地完成导入
6. THE API_Layer 应保持现有已导出符号不变，不得删除或重命名任何已在 `__all__` 中的符号
7. FOR ALL 新增导出函数，THE API_Layer 应提供与 JQData 官方文档一致的函数签名（参数名和默认值）

### 需求 15：新增 API 的错误处理规范

**用户故事：** 作为量化策略开发者，我希望所有新增 API 在遇到错误时有一致且可预期的行为，以便策略代码能够稳健地处理异常情况。

#### 验收标准

1. WHEN 网络或数据源不可用时，THE API_Layer 应返回空 DataFrame 或空列表，并通过日志记录错误原因，而非向上抛出未捕获异常
2. WHEN 参数类型不符合预期时，THE API_Layer 应抛出 ValueError 并附带明确的错误描述
3. WHEN 日期参数格式无效时，THE API_Layer 应抛出 ValueError，错误信息中包含期望的日期格式说明
4. IF 底层数据源返回空结果，THEN THE API_Layer 应返回具有正确列名的空 DataFrame，而非 None
5. THE API_Layer 应对所有新增函数提供 docstring，包含参数说明、返回值说明和使用示例


### 需求 16：暴露回测引擎定时调度 API

**用户故事：** 作为量化策略开发者，我希望通过 `jk2bt/api` 调用定时调度接口，以便在策略中注册每日、每周、每月的定时执行函数。

#### 验收标准

1. THE API_Layer 应导出 `run_daily(func, time, reference_security)` 函数，其底层调用 `jk2bt.core.runner.run_daily`
2. THE API_Layer 应导出 `run_weekly(func, weekday, time, reference_security)` 函数，其底层调用 `jk2bt.core.runner.run_weekly`
3. THE API_Layer 应导出 `run_monthly(func, day, time, reference_security, force, monthday)` 函数，其底层调用 `jk2bt.core.runner.run_monthly`
4. THE API_Layer 应导出 `unschedule_all()` 函数，其底层调用 `jk2bt.core.runner.unschedule_all`
5. WHEN `run_daily` 被调用时，THE API_Layer 应将 `func` 注册为每个交易日在指定 `time` 时刻执行的任务
6. WHEN `run_monthly` 的 `monthday` 参数被传入时，THE API_Layer 应将其作为 `day` 参数的别名处理，保持与聚宽 API 的兼容性
7. WHEN `unschedule_all` 被调用时，THE API_Layer 应清空当前策略的所有已注册定时任务


### 需求 17：暴露策略设置 API

**用户故事：** 作为量化策略开发者，我希望通过 `jk2bt/api` 调用策略配置接口，以便在 `initialize` 阶段设置基准、滑点、交易成本、股票池等策略参数。

#### 验收标准

1. THE API_Layer 应导出 `set_option(option_name, value)` 函数，其底层调用 `jk2bt.core.runner.set_option`
2. THE API_Layer 应导出 `set_benchmark(symbol)` 函数，其底层调用 `jk2bt.core.runner.set_benchmark`
3. THE API_Layer 应导出 `set_slippage(slippage_obj, type)` 函数，其底层调用 `jk2bt.core.runner.set_slippage`，`type` 参数默认值为 `"stock"`
4. THE API_Layer 应导出 `set_order_cost(cost_obj, type)` 函数，其底层调用 `jk2bt.core.runner.set_order_cost`，`type` 参数默认值为 `"stock"`
5. THE API_Layer 应导出 `set_universe(security_list)` 函数，其底层调用 `jk2bt.core.runner.set_universe`
6. THE API_Layer 应导出 `set_subportfolios(configs)` 函数，其底层调用 `jk2bt.core.runner.set_subportfolios`
7. WHEN `set_slippage` 被调用时，THE API_Layer 应接受 `FixedSlippage`、`PriceRelatedSlippage` 或 `StepRelatedSlippage` 类型的 `slippage_obj` 参数
8. WHEN `set_order_cost` 被调用时，THE API_Layer 应接受 `OrderCost` 或 `PerTrade` 类型的 `cost_obj` 参数


### 需求 18：暴露完整下单 API 及相关对象

**用户故事：** 作为量化策略开发者，我希望通过 `jk2bt/api` 调用完整的下单接口和相关配置对象，以便在策略中执行按数量、按市值、按目标数量等多种下单方式。

#### 验收标准

1. THE API_Layer 应导出 `order(security, amount, style, side)` 函数，其底层调用 `jk2bt.core.runner.order`
2. THE API_Layer 应导出 `order_target(security, amount, style, side)` 函数，其底层调用 `jk2bt.core.runner.order_target`
3. THE API_Layer 应导出 `order_value(security, value)` 函数，其底层调用 `jk2bt.core.runner.order_value`
4. THE API_Layer 应导出 `order_target_value(security, value, style, pindex)` 函数，其底层调用 `jk2bt.core.runner.order_target_value`
5. THE API_Layer 应导出 `FixedSlippage` 类，接受 `value` 参数，表示固定滑点金额
6. THE API_Layer 应导出 `PriceRelatedSlippage` 类，接受 `value` 参数，表示价格比例滑点
7. THE API_Layer 应导出 `StepRelatedSlippage` 类，接受 `value` 参数，表示阶梯滑点
8. THE API_Layer 应导出 `OrderCost` 类，接受 `open_tax`、`close_tax`、`open_commission`、`close_commission`、`close_today_commission`、`min_commission` 参数
9. THE API_Layer 应导出 `PerTrade` 类，接受 `buy_cost`、`sell_cost`、`min_cost` 参数，表示每笔交易成本
10. THE API_Layer 应导出 `SubPortfolioConfig` 类，接受 `cash`、`starting_cash`、`type` 参数，支持 `cash` 和 `starting_cash` 作为互为别名的参数
11. THE API_Layer 应导出 `OrderStatus` 类，包含 `held`、`canceled`、`rejected` 状态常量
12. WHEN `order` 或 `order_target` 的 `style` 参数为 `LimitOrderStyle` 实例时，THE API_Layer 应将限价信息传递给底层下单函数


### 需求 19：暴露运行时状态 API 及全局对象

**用户故事：** 作为量化策略开发者，我希望通过 `jk2bt/api` 访问运行时状态接口和全局对象，以便在策略执行过程中获取当前行情、交易记录，以及使用全局变量存储和日志记录功能。

#### 验收标准

1. THE API_Layer 应导出 `get_current_data()` 函数，返回当前时刻各证券的行情快照数据
2. THE API_Layer 应导出 `get_trades()` 函数，其底层调用 `jk2bt.core.runner.get_trades`，返回当前策略的交易记录字典
3. THE API_Layer 应导出 `disable_cache()` 函数，其底层调用 `jk2bt.core.runner.disable_cache`，用于禁用数据缓存
4. THE API_Layer 应导出 `g` 全局变量代理对象（`_GlobalVariableProxy` 实例），支持在策略中通过 `g.my_var = value` 方式存储跨函数共享的变量
5. THE API_Layer 应导出 `log` 日志代理对象（`_GlobalLogProxy` 实例），支持 `log.info(msg)`、`log.warn(msg)`、`log.error(msg)`、`log.set_level(level)` 调用方式
6. THE API_Layer 应导出 `record(*args, **kwargs)` 函数，其底层调用 `jk2bt.core.io.record`，用于将数据记录到回测图表
7. THE API_Layer 应导出 `send_message(title, content, channel)` 函数，其底层调用 `jk2bt.core.io.send_message`，用于发送策略消息通知
8. WHEN `g` 对象的属性被赋值时，THE API_Layer 应将该属性持久化到当前策略实例的全局变量存储中
9. WHEN `log.set_level` 被调用时，THE API_Layer 应更新当前策略实例的日志级别


### 需求 20：暴露止损止盈工具 API

**用户故事：** 作为量化策略开发者，我希望通过 `jk2bt/api` 调用止损止盈工具函数，以便在策略中对个股或整体组合设置止损和止盈条件。

#### 验收标准

1. THE API_Layer 应导出 `security_stoploss(context, stoploss_pct, open_sell_securities)` 函数，其底层调用 `jk2bt.core.runner.security_stoploss`
2. THE API_Layer 应导出 `portfolio_stoploss(context, stoploss_pct, open_sell_securities)` 函数，其底层调用 `jk2bt.core.runner.portfolio_stoploss`
3. THE API_Layer 应导出 `security_stopprofit(context, stopprofit_pct, open_sell_securities)` 函数，其底层调用 `jk2bt.core.runner.security_stopprofit`
4. THE API_Layer 应导出 `portfolio_stopprofit(context, stopprofit_pct, open_sell_securities)` 函数，其底层调用 `jk2bt.core.runner.portfolio_stopprofit`
5. WHEN `security_stoploss` 被调用时，THE API_Layer 应对 `context.portfolio.positions` 中每只持仓股票检查其亏损是否超过 `stoploss_pct`，并对触发条件的股票执行卖出操作
6. WHEN `portfolio_stoploss` 被调用时，THE API_Layer 应检查整体组合的亏损幅度是否超过 `stoploss_pct`，若超过则对所有持仓执行清仓操作
7. WHEN `security_stopprofit` 被调用时，THE API_Layer 应对每只持仓股票检查其盈利是否超过 `stopprofit_pct`，并对触发条件的股票执行卖出操作
8. WHEN `portfolio_stopprofit` 被调用时，THE API_Layer 应检查整体组合的盈利幅度是否超过 `stopprofit_pct`，若超过则对所有持仓执行清仓操作
9. IF `open_sell_securities` 参数不为空，THEN THE API_Layer 应在止损止盈触发时，仅对不在 `open_sell_securities` 列表中的持仓执行卖出操作
