# 0330 总览总结与代码检查

## 1. 已有工作归档

今天的拆分任务产出已经落在以下位置：

- `docs/0330_result.md`
  - 任务 1：Runner 命名空间纠偏
- `docs/0330_result/task2_timer_rules_engine.md`
- `docs/0330_result/task3_jq_market_api_compatibility.md`
- `docs/0330_result/task4_minute_data_backend.md`
- `docs/0330_result/task5_runtime_io_api.md`
- `docs/0330_result/task6_call_auction_billboard.md`
- `docs/0330_result/任务7_资金流接口.md`
- `docs/0330_result/task8_finance_query_extension.md`
- `docs/0330_result/task9_asset_router_subportfolios.md`
- `docs/0330_result/task10_batch_runner_concurrency.md`

这说明目前已经完成了一轮按模块拆分的并行开发，但代码库还没有进入“核心接口稳定、可批量可靠运行”的状态。

## 2. 本次复查方式

本次没有只看文档，而是直接复查了代码与测试状态。

执行命令：

```bash
python3 -m pytest -q \
  tests/test_jq_runner.py \
  tests/test_api_compatibility.py \
  tests/test_finance_query.py \
  tests/test_context_simulation.py \
  tests/test_timer_mechanism.py
```

当前结果：

- `78 passed`
- `10 failed`
- `37 warnings`

结论：当前代码已经有明显进展，但还不能认为“核心兼容层已经稳定”。

## 3. 当前确认存在的问题

### P0. 包入口导出与真实实现不一致

文件：`jqdata_akshare_backtrader_utility/__init__.py:56-61,165-169`

问题：

- `run_jq_strategy`
- `load_jq_strategy`
- `JQStrategyWrapper`

这 3 个符号仍然出现在 `__all__` 中，但对应导入被注释掉了。

影响：

- 用户按包入口文档使用时，接口名会“看起来存在”，但实际并没有导出
- 包入口语义与真实能力不一致，容易误导后续开发和测试

补充验证：

```python
import jqdata_akshare_backtrader_utility as pkg
hasattr(pkg, "run_jq_strategy")      # False
hasattr(pkg, "load_jq_strategy")     # False
hasattr(pkg, "JQStrategyWrapper")    # False
```

### P0. `factors` 包正常导入路径有问题

文件：`jqdata_akshare_backtrader_utility/factors/__init__.py:17-25,40-46`

问题：

- 使用了 `from factors.base import ...`
- 使用了 `from factors.factor_zoo import ...`
- 使用了 `from factors import valuation ...`

这些都是非相对导入。

影响：

- 在“包内正常导入”路径下，`import jqdata_akshare_backtrader_utility.factors` 会直接失败
- 目前很多能力之所以还能跑，依赖的是测试或运行时对 `sys.path` 的特殊处理，不够稳

实际复查现象：

- 正常包导入时报错：`ModuleNotFoundError: No module named 'factors'`

### P0. 因子交易日回退链实际失效，导致多个因子测试空结果

文件：`jqdata_akshare_backtrader_utility/factors/base.py:283-316`

问题：

- 设计上 `get_trade_days()` 应该在拿不到 JQ 交易日时回退到工作日序列
- 实际复查时，`get_trade_days('2023-12-30', '2024-01-01')` 返回了 `[]`

影响：

- `get_factor_values_jq(... count=1 ...)` 直接拿不到窗口
- 现在失败的多标的因子测试，本质上是空 DataFrame，而不是字段映射小问题

对应失败：

- `tests/test_api_compatibility.py::TestGetFactorValuesJqSignature::test_multiple_securities_single_factor`
- `tests/test_api_compatibility.py::TestGetFactorValuesJqSignature::test_multiple_securities_multiple_factors`
- `tests/test_api_compatibility.py::TestGetFactorValuesJqReturnStructure::*`

### P1. 因子别名标准化大小写不统一

文件：`jqdata_akshare_backtrader_utility/factors/base.py:123-158`

问题：

- `normalize_factor_name()` 直接 `FACTOR_ALIAS_MAP.get(name, name)`
- 没有做大小写归一化

实际复查：

```python
normalize_factor_names(["PE_ratio", "pe_ratio", "Pe_ratio"])
# ['pe_ratio', 'pe_ratio', 'Pe_ratio']
```

影响：

- `Pe_ratio` 这类混合大小写别名不会被映射成 `pe_ratio`
- 兼容层对“聚宽风格别名”的容错不够

对应失败：

- `tests/test_api_compatibility.py::TestFactorAliasCompatibility::test_pe_ratio_aliases`

### P1. `get_history_fundamentals_jq` 签名不完整

文件：`jqdata_akshare_backtrader_utility/backtrader_base_strategy.py:1856-1878`

问题：

- 当前只接受 `security`
- 不接受测试所需的 `entity=...` 别名参数

影响：

- 这不是数据源问题，而是 JQ 兼容签名本身缺口

对应失败：

- `tests/test_api_compatibility.py::TestGetHistoryFundamentalsJqSignature::test_basic_params`
- `tests/test_api_compatibility.py::TestGetHistoryFundamentalsJqSignature::test_count_param`

### P1. `get_security_info_jq` 强依赖实时网络，且没有优雅降级

文件：`jqdata_akshare_backtrader_utility/backtrader_base_strategy.py:1931-1941`

问题：

- 每次直接调用 `ak.stock_info_a_code_name()`
- 无本地缓存兜底
- 无离线结构化返回
- 返回值仍是 `dict`，而不是更贴近聚宽语义的对象访问结构

影响：

- 在离线环境、网络波动环境、批量测试环境下都很脆弱
- 一旦源站不可达，整个接口直接抛连接错误

对应失败：

- `tests/test_api_compatibility.py::TestGetSecurityInfoJqSignature::test_single_security`
- `tests/test_api_compatibility.py::TestGetSecurityInfoJqSignature::test_return_structure`

### P1. 分红查询失败时丢失表结构

文件：`jqdata_akshare_backtrader_utility/backtrader_base_strategy.py:1273-1292`

相关标准化逻辑：

- `jqdata_akshare_backtrader_utility/backtrader_base_strategy.py:1294-1329`

问题：

- `_query_dividend()` 抓取失败后直接 `continue`
- 如果所有标的都失败，返回 `pd.DataFrame()`
- 空表没有最基本的 schema，例如 `code`

影响：

- 即使调用方可以接受“暂时无数据”，也拿不到稳定列结构
- 这会让很多上层逻辑把“网络失败”误判成“接口协议变化”

对应失败：

- `tests/test_finance_query.py::TestFinanceQuery::test_query_dividend_columns`

### P1. `runtime_io` 默认目录落到了仓库外层

文件：`jqdata_akshare_backtrader_utility/runtime_io.py:29-36`

问题：

- 默认目录使用 `Path(__file__).parent.parent.parent / "runtime_data"`
- 对当前仓库路径而言，这会落到 `/Users/yuping/Downloads/git/runtime_data`
- 而不是仓库根目录 `/Users/yuping/Downloads/git/jk2bt-main/runtime_data`

影响：

- 与“工作区安全目录”的设计目标不一致
- 后续如果多仓库共用、并发运行或清理数据，会更难管理

### P2. `ContextProxy.set_subportfolios` 使用非相对导入

文件：`jqdata_akshare_backtrader_utility/backtrader_base_strategy.py:2930-2940`

问题：

- 使用 `from subportfolios import ...`
- 没有使用包内相对导入

影响：

- 在普通包安装或外部引用时不稳定
- 和上面的 `factors` 导入问题是同一类边界不清问题

## 4. 对“代码乱不乱”的判断

是的，现在代码已经开始显得乱了，但还不是最适合做“大重构”的时点。

当前的乱，主要不是“命名不好看”或者“目录不优雅”，而是下面这 3 类问题叠加：

- 包入口、模块入口、测试入口不一致
- 一部分模块按包方式导入，一部分模块按脚本方式导入
- 数据接口、离线兜底、返回结构还没有完全定型

这类阶段如果直接做大范围重构，风险很高：

- API 还没稳定，重构完还会继续改接口
- 子模块边界还在变化，容易重构两次
- 现在失败点很多是“核心协议缺口”，不是简单“代码丑”

## 5. 下一步建议

建议：**先把核心功能补齐并稳定，再做小步重构；不要现在做全面重构。**

推荐顺序如下：

### 第一阶段：先修核心兼容闭环

优先修这 6 项：

1. 包入口和相对导入统一
   - 修 `__init__.py`
   - 修 `factors/__init__.py`
   - 修 `ContextProxy.set_subportfolios`

2. 修复因子交易日回退链
   - 保证离线时也能返回最小可用交易日序列

3. 修复因子别名归一化
   - `PE_ratio / Pe_ratio / pe_ratio` 都映射到 `pe_ratio`

4. 补全 `get_history_fundamentals_jq` 签名
   - 支持 `entity`
   - 保持与 `security` 兼容

5. 给 `get_security_info_jq` 增加缓存和离线兜底
   - 网络不可用时至少返回稳定结构

6. 给 finance 分红查询保底 schema
   - 就算抓不到数据，也要返回包含 `code` 等标准列的空表

阶段目标：

- 先把当前 `10 failed` 压到接近 0
- 至少让“基础兼容层测试”变成可信绿灯

### 第二阶段：再收敛核心模块边界

当第一阶段通过后，再做“小步重构”，重点是：

- 明确 `runner`
- 明确 `market_api`
- 明确 `factors`
- 明确 `finance`
- 明确 `runtime_io`
- 明确 `asset_router/subportfolios`

重构原则：

- 只做边界收敛，不做大重写
- 每次只动一层入口
- 每一步都带测试回归

### 第三阶段：再扩大策略覆盖面

这时再去追下面这些能力会更稳：

- 分钟级策略
- 竞价/龙虎榜/资金流
- 期货与子账户
- 文件资源与模型加载
- 批量跑批统计口径

## 6. 最终建议

一句话结论：

**先实现核心功能并把测试压绿，再做小步重构，不建议现在直接全面重构。**

原因很简单：

- 现在最痛的不是“代码风格乱”，而是“核心兼容协议还没收口”
- 核心协议没稳之前，大重构会把开发速度拖慢，还会放大回归风险

如果下一步要开工，最值得先做的是：

1. 导入与包入口统一
2. 因子交易日与别名修复
3. `get_security_info_jq` 与 finance 离线兜底
4. `get_history_fundamentals_jq(entity=...)` 兼容

把这 4 组修完，再谈结构化重构，会更划算。
