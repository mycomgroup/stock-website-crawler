# 实现计划：jqdata-api-completion

## 概述

将底层已有实现通过新建 API 模块对外暴露，并补全缺失的 JQData 兼容接口。
所有新模块位于 `jk2bt/api/`，最终统一在 `jk2bt/api/__init__.py` 导出。

## 任务

- [-] 1. 新建 `jk2bt/api/securities.py`（证券元数据与代码标准化）
  - [-] 1.1 实现 `get_all_securities`、`get_security_info` 及其 `_jq` 别名
    - 包装 `jk2bt.core.api_wrappers.get_all_securities_jq` 和 `get_security_info_jq`
    - 无效代码返回 None 或抛出明确异常，不静默失败
    - _需求：1.1, 1.2, 1.3, 1.4, 1.5, 1.6_
  - [ ] 1.2 为 `get_all_securities` 编写单元测试
    - 验证返回 DataFrame 包含 `display_name`、`name`、`start_date`、`end_date`、`type` 列
    - _需求：1.3_
  - [ ] 1.3 实现 `normalize_code` 及 `normalize_security_code` 别名
    - 基于 `jk2bt.core.securities_utils` 中的 `ak_code_to_jq` / `_stock_code_to_jq` 逻辑
    - 纯 6 位数字 → 按首位判断交易所后缀；已是 JQ_Code 则原样返回
    - _需求：2.1, 2.2, 2.3, 2.4, 2.5_
  - [ ] 1.4 为 `normalize_code` 编写属性测试
    - **属性 1：幂等性** — `normalize_code(normalize_code(x)) == normalize_code(x)`
    - **验证：需求 2.4**

- [ ] 2. 新建 `jk2bt/api/calendar.py`（交易日历）
  - [ ] 2.1 实现 `get_all_trade_days` 和 `get_trade_days`
    - `get_all_trade_days` 包装 `jk2bt.utils.date_utils.get_all_trade_days`
    - `get_trade_days` 包装 `jk2bt.utils.date_utils.get_trade_days`，参数冲突时抛出 `ValueError`
    - 导出 `get_all_trade_days_jq` 作为底层别名
    - _需求：3.1, 3.2, 3.3, 3.4, 3.5, 3.6_
  - [ ] 2.2 为 `get_trade_days` 编写单元测试
    - 测试 `start_date+count`、`end_date+count`、参数冲突三种场景
    - _需求：3.3, 3.4, 3.5_

- [ ] 3. 新建 `jk2bt/api/index.py`（指数数据）
  - [ ] 3.1 实现 `get_index_stocks` 和 `get_index_weights`
    - 包装 `jk2bt.core.api_wrappers.get_index_stocks` 和 `get_index_weights`
    - 不支持的指数代码返回空列表并记录 warning，不抛异常
    - _需求：4.1, 4.2, 4.3, 4.4, 4.5_
  - [ ] 3.2 为 `get_index_stocks` 编写单元测试
    - 验证返回 JQ_Code 格式列表；不支持指数返回空列表
    - _需求：4.3, 4.5_

- [ ] 4. 新建 `jk2bt/api/fundamentals.py`（财务与估值数据）
  - [ ] 4.1 实现 `get_fundamentals`、`get_valuation`、`get_history_fundamentals`
    - 包装 `jk2bt.core.api_wrappers` 中对应函数
    - `security_list` 为空时返回空 DataFrame，不抛异常
    - _需求：5.1, 5.2, 5.3, 5.6_
  - [ ] 4.2 实现 `query` 函数及财务表对象（`valuation`、`income`、`cash_flow`、`balance`、`indicator`）
    - 包装 `jk2bt.core.api_wrappers.query`，支持链式调用
    - _需求：5.4, 5.5_
  - [ ] 4.3 为 `get_fundamentals` 编写单元测试
    - 验证空列表返回空 DataFrame；验证链式 query 语法可用
    - _需求：5.5, 5.6_

- [ ] 5. 新建 `jk2bt/api/industry.py`（行业与概念）
  - [ ] 5.1 实现 `get_industry`、`get_industries`、`get_industry_stocks`
    - 包装 `jk2bt.market_data.industry` 中对应函数
    - `df=True` 时返回 DataFrame，否则返回 dict
    - _需求：6.1, 6.2, 6.3, 6.6, 6.7, 6.8_
  - [ ] 5.2 实现 `get_concepts` 和 `get_concept_stocks`
    - `get_concept_stocks` 包装 `jk2bt.core.runner.get_concept_stocks`
    - `get_concepts` 返回概念板块列表 DataFrame（stub 实现，返回空 DataFrame 并记录日志）
    - _需求：6.4, 6.5_
  - [ ] 5.3 为 `get_industry` 编写单元测试
    - 验证 `df=True` 返回 DataFrame，`df=False` 返回 dict
    - _需求：6.8_

- [ ] 6. 新建 `jk2bt/api/extras.py`（集合竞价、get_extras、Tick 数据）
  - [ ] 6.1 实现 `get_call_auction`
    - 包装 `jk2bt.market_data.call_auction.get_call_auction`
    - 无数据时返回空 DataFrame，`fields=None` 返回全部字段
    - _需求：7.1, 7.2, 7.3, 7.4_
  - [ ] 6.2 实现 `get_extras` 及 `get_extras_jq` 别名
    - 包装 `jk2bt.core.api_wrappers.get_extras_jq`
    - `df=True` 返回 DataFrame，`df=False` 返回 dict
    - _需求：8.1, 8.2, 8.3, 8.4, 8.5_
  - [ ] 6.3 实现 `get_ticks`
    - 包装 `jk2bt.core.runner.get_ticks`
    - 无数据时返回空 DataFrame
    - _需求：13.1, 13.2, 13.3, 13.4_
  - [ ] 6.4 为 `get_extras` 编写单元测试
    - 验证 `is_st`、`is_paused` 字段；验证 `df` 参数格式切换
    - _需求：8.2, 8.3, 8.4_

- [ ] 7. 新建 `jk2bt/api/margin.py`（融资融券）
  - [ ] 7.1 实现 `get_mtss`、`get_margincash_stocks`、`get_marginsec_stocks`
    - `get_mtss` 基于 akshare 数据源实现，`start_date` 与 `count` 互斥时抛出 `ValueError`
    - `fields=None` 返回全部字段；`get_margincash_stocks`/`get_marginsec_stocks` 返回 JQ_Code 列表
    - _需求：9.1, 9.2, 9.3, 9.4, 9.5, 9.6_
  - [ ] 7.2 为 `get_mtss` 编写单元测试
    - 验证返回 DataFrame 包含必要字段；验证参数互斥抛出 ValueError
    - _需求：9.2, 9.5_

- [ ] 8. 新建 `jk2bt/api/money_flow.py`（资金流向）
  - [ ] 8.1 实现 `get_money_flow`
    - 包装 `jk2bt.market_data.money_flow.get_money_flow`
    - `fields=None` 时仅返回流入/流出字段，不含净流入；停牌日返回 NaN 行
    - _需求：10.1, 10.2, 10.3, 10.4, 10.5_
  - [ ] 8.2 为 `get_money_flow` 编写单元测试
    - 验证 `fields=None` 不含 `netflow_*` 字段；验证停牌日不抛异常
    - _需求：10.4, 10.5_

- [ ] 9. 新建 `jk2bt/api/hk_connect.py`（沪深港通）
  - [ ] 9.1 实现 `get_hk_hold_info`
    - 基于 akshare 北向资金持股数据实现
    - `link_id=310001` 返回沪股通，`link_id=310002` 返回深股通
    - 无数据时返回空 DataFrame，包含正确列名
    - _需求：11.1, 11.2, 11.3, 11.4, 11.5_
  - [ ] 9.2 为 `get_hk_hold_info` 编写单元测试
    - 验证返回 DataFrame 包含 `day`、`link_id`、`code`、`share_ratio` 等字段
    - _需求：11.4_

- [ ] 10. 新建 `jk2bt/api/engine.py`（回测引擎调度与设置）
  - [ ] 10.1 实现定时调度 API：`run_daily`、`run_weekly`、`run_monthly`、`unschedule_all`
    - 直接包装 `jk2bt.core.runner` 中对应函数
    - `run_monthly` 的 `monthday` 参数作为 `day` 的别名
    - _需求：16.1, 16.2, 16.3, 16.4, 16.5, 16.6, 16.7_
  - [ ] 10.2 实现策略设置 API：`set_option`、`set_benchmark`、`set_slippage`、`set_order_cost`、`set_universe`、`set_subportfolios`
    - 直接包装 `jk2bt.core.runner` 中对应函数
    - _需求：17.1, 17.2, 17.3, 17.4, 17.5, 17.6, 17.7, 17.8_
  - [ ] 10.3 实现下单 API：`order`、`order_target`、`order_value`、`order_target_value`
    - 直接包装 `jk2bt.core.runner` 中对应函数
    - _需求：18.1, 18.2, 18.3, 18.4_
  - [ ] 10.4 导出下单相关类和对象：`FixedSlippage`、`PriceRelatedSlippage`、`StepRelatedSlippage`、`OrderCost`、`PerTrade`、`SubPortfolioConfig`、`OrderStatus`
    - 从 `jk2bt.core.runner` 重新导出
    - _需求：18.5, 18.6, 18.7, 18.8, 18.9, 18.10, 18.11, 18.12_
  - [ ] 10.5 实现止损止盈 API：`security_stoploss`、`portfolio_stoploss`、`security_stopprofit`、`portfolio_stopprofit`
    - 直接包装 `jk2bt.core.runner` 中对应函数
    - _需求：20.1, 20.2, 20.3, 20.4, 20.5, 20.6, 20.7, 20.8, 20.9_

- [ ] 11. 新建 `jk2bt/api/runtime.py`（运行时状态与全局对象）
  - [ ] 11.1 实现 `get_current_data`、`get_trades`、`disable_cache`
    - 包装 `jk2bt.core.runner` 和 `jk2bt.core.api_wrappers` 中对应函数
    - _需求：19.1, 19.2, 19.3_
  - [ ] 11.2 导出 `g`（`_GlobalVariableProxy` 实例）和 `log`（`_GlobalLogProxy` 实例）
    - 从 `jk2bt.core.runner` 重新导出模块级实例
    - _需求：19.4, 19.5, 19.8, 19.9_
  - [ ] 11.3 实现 `record` 和 `send_message`
    - 包装 `jk2bt.core.io.record` 和 `jk2bt.core.io.send_message`
    - _需求：19.6, 19.7_
  - [ ] 11.4 实现 `finance` 模块对象，支持 `finance.run_query` 和相关表常量
    - 包装 `jk2bt.core.runner.finance` 类，暴露 `STK_EXCHANGE_TRADE_INFO`、`STK_HK_HOLD_INFO` 表
    - 查询超 5000 行时截断并记录警告
    - _需求：12.1, 12.2, 12.3, 12.4, 12.5, 12.6_
  - [ ] 11.5 为 `finance.run_query` 编写单元测试
    - 验证链式查询语法；验证超限截断行为
    - _需求：12.5, 12.6_

- [ ] 12. 检查点 — 确保所有新模块可正常导入，运行现有测试套件
  - 确保所有测试通过，如有问题请向用户反馈。

- [ ] 13. 更新 `jk2bt/api/__init__.py`（统一导出）
  - [ ] 13.1 从各新模块导入所有新增符号，按功能分组添加到文件头部导入区
    - 新增分组：证券元数据、交易日历、指数数据、财务数据、行业概念、集合竞价/Tick、融资融券、资金流向、港通数据、回测引擎、运行时状态
    - _需求：14.1, 14.2_
  - [ ] 13.2 将所有新增符号追加到 `__all__` 列表，保持现有符号不变
    - 验证 `from jk2bt.api import get_all_securities, normalize_code, get_fundamentals, get_industry` 等导入无报错
    - _需求：14.1, 14.3, 14.4, 14.5, 14.6, 14.7_

- [ ] 14. 编写集成测试（需求 15）
  - [ ] 14.1 在 `tests/unit/api/` 下新建各模块对应测试文件
    - 覆盖错误处理规范：网络不可用返回空 DataFrame/列表；参数类型错误抛出 ValueError；日期格式无效抛出 ValueError
    - 验证底层返回空结果时返回带正确列名的空 DataFrame，而非 None
    - _需求：15.1, 15.2, 15.3, 15.4_
  - [ ] 14.2 为错误处理编写属性测试
    - **属性 2：空输入稳定性** — 任意空列表输入不抛异常，返回空 DataFrame
    - **验证：需求 15.4**

- [ ] 15. 新建 `jk2bt/api/preprocess.py`（切换到 lib/jqfactor_analyzer 版本）
  - [ ] 15.1 调研 `lib/jqfactor_analyzer` 是否可直接 import（检查 setup.py 和依赖）
    - 确认 `lib/jqfactor_analyzer` 已安装或可通过 sys.path 引用
  - [ ] 15.2 新建 `jk2bt/api/preprocess.py`，从 lib 版本重新导出
    - 从 `lib.jqfactor_analyzer.jqfactor_analyzer.preprocess` 导入 `winsorize`、`winsorize_med`、`standardlize`、`neutralize`
    - 若 lib 不可用则 fallback 到 `jk2bt.core.api_wrappers` 中的实现
  - [ ] 15.3 更新 `jk2bt/api/__init__.py`，将 `winsorize`/`standardlize`/`neutralize` 的导入源切换到 `jk2bt.api.preprocess`
    - 移除原来从 `jk2bt.core.api_wrappers` 或 `jk2bt.factors.preprocess` 的重复导入（如有）
  - [ ] 15.4 验证切换后行为一致性
    - 对相同输入，新旧实现结果应一致（属性 P9）

- [ ] 16. 新建 `jk2bt/api/factor_analysis.py`（单因子分析新增能力）
  - [ ] 16.1 新建 `jk2bt/api/factor_analysis.py`，从 lib 版本导出
    - 从 `lib.jqfactor_analyzer.jqfactor_analyzer` 导入 `FactorAnalyzer`、`analyze_factor`、`AttributionAnalysis`
    - 若 lib 不可用则提供明确的 ImportError 提示
  - [ ] 16.2 更新 `jk2bt/api/__init__.py`，新增单因子分析分组导出
    - 导出 `FactorAnalyzer`、`analyze_factor`、`AttributionAnalysis`

- [ ] 17. 最终检查点 — 确保所有测试通过
  - 确保所有测试通过，如有问题请向用户反馈。

## 备注

- 标有 `*` 的子任务为可选测试任务，可跳过以加快 MVP 进度
- 每个任务均引用具体需求条款，便于追溯
- 属性测试验证普遍正确性，单元测试验证具体示例和边界条件
- 新模块均需提供 docstring，包含参数说明、返回值说明和使用示例（需求 15.5）
- `lib/jqdatasdk` 的函数签名作为 API 层的参考标准，但实现逻辑使用本地数据源
- `lib/jqfactor_analyzer` 的 `winsorize`/`standardlize`/`neutralize` 实现比本项目自有实现更完整，应切换过去
