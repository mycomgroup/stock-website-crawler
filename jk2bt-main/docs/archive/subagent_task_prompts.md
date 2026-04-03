# 子 Agent 并行开发提示词

本文档给出 10 个可并行开发的子任务提示词。每个提示词都假设子 agent 在同一个仓库中工作，但**只拥有自己负责文件范围的写权限和责任**。

通用要求适用于所有子任务：

- 你不只是在做分析，请直接完成代码实现、补充测试，并给出最小验证方式。
- 你不在独占仓库，其他 agent 也可能同时修改代码。不要回退他人的改动，也不要假设工作树是干净的。
- 如果发现公共接口被别的 agent 改动了，优先兼容并在最终说明中注明，而不是强行覆盖。
- 除非任务明确要求，不要做大范围重构，不要顺手改 unrelated code。
- 优先保持现有代码风格和目录结构。
- 每个任务结束时请输出：
  - 修改了哪些文件
  - 完成了什么
  - 如何验证
  - 剩余风险或已知边界

---

## 任务 1: Runner 命名空间纠偏

你负责修复 `txt` 策略运行器中的全局命名空间绑定错误，并增强策略文件加载健壮性。

目标：

- 确保 `load_jq_strategy()` 暴露给策略代码的 API，优先绑定到真正的 JQ 风格兼容实现，而不是内部简化版或错误签名版本。
- 修复策略文本读取时的编码兼容问题，至少支持 `utf-8`、`gbk`、`gb2312`、`latin-1` 回退尝试。
- 不要改变策略作者的调用方式；优先保证现有 `txt` 策略“原样跑”的兼容性。

重点检查：

- `jqdata_akshare_backtrader_utility/jq_strategy_runner.py`
- 策略命名空间中 `get_price`、`get_current_data`、`get_all_trade_days`、`get_extras`、`get_billboard_list`
- `load_jq_strategy()` 对导入语句的预处理逻辑

实现要求：

- 如果仓库里已经有 JQ 风格实现，优先直接复用。
- 加载失败时，给出明确异常信息，不要静默返回 `None`。
- 不要引入破坏性行为，例如把所有导入都粗暴删除。

测试建议：

- 为 UTF-8 和 GBK 各构造一个最小策略样例。
- 验证带 `count/frequency/panel` 参数的 `get_price` 调用，不会因为绑定错函数而直接抛签名错误。

交付范围：

- 仅修改与你任务直接相关的 runner / loader / 对应测试。

---

## 任务 2: Timer 规则引擎

你负责替换当前过于简化的定时器逻辑，实现更接近聚宽语义的规则判断。

目标：

- 支持 `run_daily`、`run_weekly`、`run_monthly`
- 支持时间规则：
  - `before_open`
  - `open`
  - `after_close`
  - `HH:MM`
  - `open+30m`
- 支持月内第 N 个交易日、周几执行等基础语义
- 让定时器逻辑尽量纯函数化、可测试

重点检查：

- `jqdata_akshare_backtrader_utility/backtrader_base_strategy.py`
- 现有 `TimerManager`
- 相关测试 `tests/test_timer_mechanism.py`

实现要求：

- 现在的 `_check_time_rule()` 基本等于恒真，需要替换成真正判断。
- 不需要一口气实现聚宽全部时间系统，但要覆盖当前策略集中高频使用的规则。
- 若 Backtrader bar 粒度不足以精确模拟某些时间点，至少要显式降级，不要假装精确支持。

测试建议：

- 用合成交易日和合成 bar 时间做单元测试。
- 至少验证 daily/weekly/monthly 不会在同一交易日重复触发。

交付范围：

- 仅修改定时器相关实现与测试；不要顺手改订单逻辑。

---

## 任务 3: JQ 行情 API 兼容层

你负责统一实现 JQ 风格行情接口，使 `get_price`、`history`、`attribute_history`、`get_bars` 在签名和返回结构上尽量兼容聚宽常见调用。

目标：

- 统一这些函数的参数行为：
  - `count`
  - `start_date`
  - `end_date`
  - `frequency`
  - `fields`
  - `panel`
  - `df`
  - `fq`
  - `fill_paused`
  - `skip_paused`
- 统一返回结构，避免同类接口风格互相冲突

重点检查：

- `jqdata_akshare_backtrader_utility/backtrader_base_strategy.py`
- 如有需要，可以新增独立模块，但尽量不要造成重复实现
- 相关测试：
  - `tests/test_jqdata_api.py`
  - `tests/test_api_compatibility.py`

实现要求：

- 不要只修参数签名，要关注结果形状和字段。
- 至少覆盖高频字段：
  - `open`
  - `high`
  - `low`
  - `close`
  - `volume`
  - `money`
  - `paused`
  - `pre_close`
  - `high_limit`
  - `low_limit`
- 若底层数据源无法天然提供某字段，可以在兼容层推导，但要说明推导方式。

测试建议：

- 单标的、多标的、日线、分钟线都要覆盖最小样例。
- 验证 `panel=False` 时可被现有策略直接 `.pivot()` 或直接取列。

交付范围：

- 你只负责行情 API 兼容，不负责消息推送或 finance。

---

## 任务 4: 分钟级数据后端

你负责补充股票和 ETF 的分钟级数据后端，为日内策略提供数据基础。

目标：

- 支持至少：
  - `1m`
  - `5m`
  - `15m`
  - `30m`
  - `60m`
- 输出标准列：
  - `datetime`
  - `open`
  - `high`
  - `low`
  - `close`
  - `volume`
  - `money`
  - `openinterest`

重点检查：

- `jqdata_akshare_backtrader_utility/market_data/`
- 现有 stock / etf / index 数据模块
- 与行情 API 兼容层的接口衔接

实现要求：

- 优先做统一的标准化层，而不是在多个地方散着写。
- 要有本地缓存，避免反复下载。
- 要考虑数据源缺失、字段名不统一、时间戳格式混乱的问题。

测试建议：

- 至少构造一个股票、一个 ETF 的分钟数据读取 smoke test。
- 验证分钟数据被上层 `get_price` 或 `get_bars` 正常消费。

交付范围：

- 不负责 timer 和策略调度，只负责分钟数据拿得到、格式统一。

---

## 任务 5: 运行时 IO 与观测 API

你负责补上策略运行时常见的“非交易型 API”，让依赖这些接口的策略可以继续执行。

目标：

- 实现或最小可用支持：
  - `record`
  - `send_message`
  - `read_file`
  - `write_file`
- 让这些 API 在本地环境中有明确、可追踪的落点

建议语义：

- `record`: 输出到结构化日志或 CSV
- `send_message`: 记录到日志，不需要真的发消息
- `read_file`: 从工作区某个安全目录读取资源
- `write_file`: 写入工作区安全目录，支持追加模式

重点检查：

- `jqdata_akshare_backtrader_utility/jq_strategy_runner.py`
- 日志目录与现有 `logs/`
- 可能需要新增一个 runtime 辅助模块

实现要求：

- 重点是“本地可运行且行为清楚”，不是去模拟云端服务。
- `read_file/write_file` 不要允许随意越权访问工作区外路径。
- 对不支持的参数要明确报错，而不是静默忽略。

测试建议：

- 构造一个最小策略，运行后验证：
  - `record` 产生日志
  - `send_message` 被记录
  - `write_file` 写出文件
  - `read_file` 能读回

交付范围：

- 不负责机器学习模型正确性，只负责这些 IO API 能跑。

---

## 任务 6: 竞价与龙虎榜接口

你负责实现竞价和龙虎榜相关接口，优先覆盖现有策略实际用到的字段。

目标：

- 实现 `get_call_auction`
- 把当前空表 stub 的 `get_billboard_list` 替换成真实实现或明确降级实现

重点检查：

- `jqdata_akshare_backtrader_utility/jq_strategy_runner.py`
- `jqdata_akshare_backtrader_utility/backtrader_base_strategy.py`
- 可新增 `market_data/call_auction.py`、`market_data/billboard.py`

实现要求：

- 先根据仓库中现有策略调用方式，确定最低必需字段。
- 如果底层源拿不到完整数据，也要返回结构稳定的 DataFrame，并显式标注能力边界。
- 不要继续保留“静默空表”这种会误导策略的行为。

测试建议：

- 找 1 到 2 个现有竞价类策略片段做 smoke test。
- 验证访问常见字段时不会 `KeyError`。

交付范围：

- 仅负责竞价与龙虎榜，不负责资金流。

---

## 任务 7: 资金流接口

你负责补充 `get_money_flow` 能力，服务依赖主力资金流指标的策略。

目标：

- 实现 `get_money_flow`
- 支持常见参数组合：
  - 股票列表
  - 日期区间
  - `count`
  - `fields`

重点检查：

- `jqdata_akshare_backtrader_utility/market_data/`
- 已有北向资金模块是否有可复用字段标准化逻辑

实现要求：

- 返回结构要尽量贴近策略当前使用方式。
- 优先覆盖现有策略里出现频率最高的字段，如：
  - `sec_code`
  - `change_pct`
  - `net_pct_main`

测试建议：

- 从仓库里挑一段真实使用 `get_money_flow` 的策略代码做最小验证。
- 验证返回结果可直接筛选、排序、取列。

交付范围：

- 不负责竞价、龙虎榜和 order 逻辑。

---

## 任务 8: finance 扩展查询

你负责补齐 `finance.run_query` 在融资融券和业绩预告场景下的支持。

目标：

- 实现 `finance.STK_MX_RZ_RQ`
- 实现 `finance.STK_FIN_FORCAST`
- 如实现成本不高，可一并补 `get_mtss` 或相近包装函数

重点检查：

- `jqdata_akshare_backtrader_utility/backtrader_base_strategy.py`
- `jqdata_akshare_backtrader_utility/finance_data/`
- `tests/test_finance_query.py`

实现要求：

- 现在对应查询基本直接返回空表，需要替换成真实实现。
- 要保留现有 query/filter 风格，不要改调用方式。
- 如果只能部分支持字段，至少要让过滤和常见列查询通畅。

测试建议：

- 为分红、融资融券、业绩预告各写一个基本查询测试。
- 验证 `query(...).filter(... )` 组合还能工作。

交付范围：

- 不负责整体资产账户模型，只负责 finance 数据查询。

---

## 任务 9: 资产路由与子账户模型

你负责把资产类别识别和 `subportfolios` 最小模型搭起来，为 ETF、基金、期货类策略打基础。

目标：

- 识别并分类：
  - 股票
  - ETF / LOF
  - 场外基金 `.OF`
  - 股指期货 `.CCFX`
- 提供最小可用的：
  - `context.subportfolios`
  - `set_subportfolios`
  - `transfer_cash`

重点检查：

- `jqdata_akshare_backtrader_utility/backtrader_base_strategy.py`
- 现有 `ContextProxy` / `PortfolioProxy`
- 可以新增 `asset_router.py` 或 `subportfolios.py`

实现要求：

- 不要求一次实现真实完整的期货撮合系统，但至少不能再把 `subportfolios` 退化成同一个 portfolio 的浅包装。
- 要为后续 agent 留出扩展点。
- 若某些资产当前只能“识别但不支持交易”，要明确暴露状态。

测试建议：

- 构造最小子账户配置测试。
- 验证 `context.subportfolios[i]` 与主账户能区分现金视图。

交付范围：

- 不负责分钟数据，不负责 finance query。

---

## 任务 10: 批量运行器与并发存储修复

你负责提高批量跑策略的真实性和稳定性，修复统计口径和并发访问问题。

目标：

- 修复 `run_strategies_parallel.py` 中“异常仍可能被算作成功”的统计问题
- 解决或缓解 DuckDB 并发锁冲突
- 在运行前增加“策略可执行性扫描”

重点检查：

- `run_strategies_parallel.py`
- `jqdata_akshare_backtrader_utility/db/duckdb_manager.py`
- 可新增 `strategy_scanner.py`

实现要求：

- 成功必须意味着：策略执行完成且无未处理异常。
- 对“加载成功但运行异常”“零收益但运行正常”“数据缺失导致跳过”要分开统计。
- DuckDB 并发问题优先用工程方案缓解，例如：
  - 单进程下载、多进程读取
  - 独立连接
  - 本地缓存分层
  - 降低共享写冲突
- 扫描器至少要识别：
  - 是否存在 `initialize`
  - 是否依赖明显未实现 API
  - 是否是说明文档/配套资料而非可执行策略

测试建议：

- 运行一个小批次策略，确认成功率统计更可信。
- 至少验证一个“异常策略”不会再被记成 success。

交付范围：

- 只负责跑批框架、扫描和并发存储，不负责逐个补具体 API。

---

## 建议的并行顺序

如果资源有限，优先顺序建议如下：

1. 任务 1
2. 任务 3
3. 任务 2
4. 任务 4
5. 任务 10
6. 任务 5
7. 任务 8
8. 任务 6
9. 任务 7
10. 任务 9

前五项完成后，框架会从“能跑部分策略”明显提升到“能较稳定地跑一批日线与部分日内策略”。
