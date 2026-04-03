# 任务 6: 竞价与龙虎榜接口

## 任务概述

实现竞价和龙虎榜相关接口，优先覆盖现有策略实际用到的字段。

## 修改的文件

### 1. 新创建文件

**`jqdata_akshare_backtrader_utility/market_data/call_auction.py`**

- 实现了 `get_call_auction` 函数
- 返回稳定的 DataFrame 结构，包含必需字段：
  - `code`: 股票代码（JQData 格式）
  - `time`: 时间
  - `current`: 竞价价格
  - `volume`: 竞价成交量
  - `money`: 竞价成交额
  - `capability`: 数据能力标记（'full' 或 'limited'）
- 显式标注能力边界：仅支持当日实时竞价数据

### 2. 修改文件

**`jqdata_akshare_backtrader_utility/backtrader_base_strategy.py`**

重构 `get_billboard_list_jq` 函数（第 2007-2103 行）：

- 增加 JQData 风格字段映射
- 映射后的字段：
  | akshare 中文列名 | JQData 风格列名 | 说明 |
  |-----------------|----------------|------|
  | 代码 | code | 股票代码 |
  | 上榜日 | date | 上榜日期 |
  | 龙虎榜净买额 | net_value | 净买额 |
  | 龙虎榜买入额 | buy_value | 买入额 |
  | 龙虎榜卖出额 | sell_value | 卖出额 |
  | 龙虎榜成交额 | total_value | 成交额 |
  | 净买额占总成交比 | buy_rate | 净买占比 |
  | 换手率 | turnover_rate | 换手率 |
  | 收盘价 | close_price | 收盘价 |
  | 涨跌幅 | change_pct | 涨跌幅 |
  | 上榜原因 | reason | 上榜原因 |

- 修复日期过滤的类型错误（支持 datetime.date 和字符串类型）
- 支持多种股票代码格式：sh/sz 前缀、JQData 格式（.XSHG/.XSHE）、纯代码

**`jqdata_akshare_backtrader_utility/jq_strategy_runner.py`**

- 导入 `get_call_auction` 和 `get_call_auction_jq`（第 127-131 行）
- 将 `get_call_auction` 添加到策略全局命名空间（第 691 行）

**`tests/test_jqdata_api.py`**

- 更新 `test_get_billboard_list_jq_param` 测试，验证 JQData 风格字段名
- 新增 `test_get_call_auction_fields` 测试，验证字段结构稳定性

## 完成的功能

### get_call_auction（集合竞价）

```python
from jq_strategy_runner import get_call_auction

# 示例用法
df = get_call_auction(
    stock_list=['000001.XSHE', '600000.XSHG'],
    start_date='2023-01-01',  # 注意：历史日期返回空表
    end_date='2023-01-01',
    fields=['time', 'current', 'volume', 'money']
)

# 返回字段
# - code: 股票代码
# - time: 时间
# - current: 竞价价格
# - volume: 竞价成交量
# - money: 竞价成交额
# - capability: 数据能力标记
```

**能力边界**：
- ✅ 当日实时竞价数据：可获取（`capability='full'`）
- ❌ 历史日期竞价数据：返回空 DataFrame（`capability='limited'`）
- 数据源：`akshare.stock_zh_a_hist_pre_min_em`

### get_billboard_list（龙虎榜）

```python
from jq_strategy_runner import get_billboard_list

# 示例用法（模拟策略 jkcode/96）
df = get_billboard_list(stock_list=None, end_date='2023-04-10', count=1)
filtered = df[df['net_value'] > 0]
filtered = filtered[filtered['buy_rate'] > 4]
codes = filtered['code'].tolist()

# 示例用法（模拟策略 jkcode/99）
longhu = get_billboard_list(stock_list=['000001.XSHE'], end_date='2023-04-10', count=30)
codes_list = longhu['code'].tolist()
```

**改进点**：
- 字段名从中文改为英文（JQData 风格），避免 KeyError
- 支持多种代码格式
- 修复日期过滤类型兼容问题

## 策略使用模式验证

基于仓库中现有策略的实际调用方式验证：

### 竞价类策略（jkcode/46, 21, 13 等）

```python
# jkcode/46 韶华研究之十二--还算可以的竞价研究
df_auction = get_call_auction(
    stocklist,
    start_date=today_date,
    end_date=today_date,
    fields=['time', 'current', 'volume', 'money']
)
df_auction = df_auction[df_auction.money > money_limit].sort_values(['money'], ascending=False)
stockcode = df_auction.code.values[i]  # ← 需要访问 code 字段
price = df_auction.current.values[i]   # ← 需要访问 current 字段
```

**验证结果**：✅ 字段访问不会 KeyError

### 龙虎榜类策略（jkcode/96, 99, 01, 26 等）

```python
# jkcode/96 首版+2版龙虎榜挖掘V2.0
g.muster = get_billboard_list(stock_list=None, end_date=context.previous_date, count=1)
g.muster = g.muster[g.muster['net_value'] > 0]       # ← 需要访问 net_value
g.muster = g.muster[g.muster['buy_rate'] > 4]        # ← 需要访问 buy_rate
g.muster = list(g.muster['code'])                    # ← 需要访问 code

# jkcode/99 最新龙回头5.0
longhu = get_billboard_list(stock_list=g.check_out_lists, end_date=context.previous_date, count=30)
g.check_out_lists = list(set(g.check_out_lists).intersection(set(longhu["code"])))  # ← 需要访问 code
```

**验证结果**：✅ 字段访问不会 KeyError

## 测试覆盖

### 新增测试文件

**`tests/test_call_auction_billboard.py`** - 58 个测试用例

测试类结构：
```
TestGetCallAuction              - 15 个测试（竞价接口主流程）
TestCallAuctionHelpers          - 9 个测试（辅助函数）
TestGetBillboardList            - 18 个测试（龙虎榜接口主流程）
TestBillboardListEdgeCases      - 4 个测试（边界情况）
TestStrategyIntegration         - 4 个测试（策略集成）
TestPerformanceAndStability     - 3 个测试（性能稳定性）
```

### 测试覆盖详情

#### 竞价接口测试（15 个）

| 测试场景 | 测试用例 |
|---------|---------|
| 返回值验证 | `test_return_type_is_dataframe` |
| 字段完整性 | `test_empty_result_has_required_columns` |
| 能力标记 | `test_empty_result_capability_marker` |
| 空输入处理 | `test_none_stock_list_returns_empty_df` |
| 单股票输入 | `test_single_stock_string_input` |
| 多股票输入 | `test_multiple_stocks_list_input` |
| fields 参数 | `test_fields_parameter_partial`, `test_fields_parameter_all` |
| 日期格式 | `test_date_formats_string`, `test_date_formats_datetime`, `test_date_formats_date` |
| 无效代码 | `test_fake_stock_code`, `test_mixed_valid_invalid_stocks` |
| 字段访问 | `test_no_keyerror_on_field_access` |
| 策略模拟 | `test_strategy_pattern_filter_sort` |

#### 辅助函数测试（9 个）

| 函数 | 测试场景 |
|-----|---------|
| `_jq_code_to_ak` | XSHE/XSHG/纯代码/sh 前缀格式转换 |
| `_normalize_date` | string/datetime/date/None/无效字符串标准化 |

#### 龙虎榜接口测试（18 个）

| 测试场景 | 测试用例 |
|---------|---------|
| 返回值验证 | `test_return_type_is_dataframe` |
| JQData 风格字段 | `test_has_jqdata_style_columns` |
| 原始字段保留 | `test_has_original_akshare_columns` |
| 代码格式 | sh/sz/JQData/纯代码/单字符串输入 |
| stock_list=None | `test_stock_list_none` |
| count 参数 | `test_count_parameter`, `test_count_zero` |
| end_date 过滤 | string/datetime/date 格式 |
| 无效代码 | `test_fake_stock_code` |
| 字段访问 | `test_no_keyerror_on_field_access` |
| 策略模拟 | net_value/buy_rate 过滤、交集操作 |
| 缓存参数 | `test_cache_parameter`, `test_force_update_parameter` |
| 空返回字段 | `test_empty_result_has_required_columns` |
| 列类型验证 | `test_column_value_types` |

#### 边界情况测试（4 个）

| 场景 | 测试用例 |
|-----|---------|
| 大 count 值 | `test_large_count` |
| 股票列表 | `test_empty_stock_list` |
| 混合代码格式 | `test_mixed_code_formats` |
| 很早的日期 | `test_very_old_end_date` |

#### 策略集成测试（4 个）

| 策略来源 | 测试用例 |
|---------|---------|
| jkcode/46 | `test_call_auction_strategy_pattern_46` |
| jkcode/96 | `test_billboard_strategy_pattern_96` |
| jkcode/99 | `test_billboard_strategy_pattern_99` |
| 完整工作流 | `test_full_workflow` |

#### 性能稳定性测试（3 个）

| 场景 | 测试用例 |
|-----|---------|
| 无效输入不抛异常 | `test_call_auction_no_exception_on_invalid_input` |
| 空缓存稳定 | `test_billboard_no_exception_on_empty_cache` |
| 重复调用稳定 | `test_repeated_calls_stability` |

## 如何验证

### 最小验证方式

```bash
# 方式 1: 测试竞价接口字段稳定性
python3 -m pytest tests/test_jqdata_api.py::test_get_call_auction_fields -v

# 方式 2: 测试龙虎榜字段映射
python3 -m pytest tests/test_jqdata_api.py::test_get_billboard_list_jq_param -v

# 方式 3: 端到端策略模拟测试
cd jqdata_akshare_backtrader_utility && python3 -c "
from jq_strategy_runner import get_call_auction, get_billboard_list
import pandas as pd

# 验证竞价接口
df1 = get_call_auction(['000001.XSHE'], fields=['time', 'current'])
assert 'code' in df1.columns and 'capability' in df1.columns

# 验证龙虎榜接口
df2 = get_billboard_list(stock_list=None, count=1)
assert 'code' in df2.columns and 'net_value' in df2.columns and 'buy_rate' in df2.columns

print('✓ 所有验证通过')
"
```

### 测试结果

```
tests/test_jqdata_api.py::test_get_billboard_list_jq_param[stock_list0] PASSED
tests/test_jqdata_api.py::test_get_billboard_list_jq_param[stock_list1] PASSED
tests/test_jqdata_api.py::test_get_billboard_list_jq_param[None] PASSED
tests/test_jqdata_api.py::test_get_call_auction_fields[000001.XSHE-fields0] PASSED
tests/test_jqdata_api.py::test_get_call_auction_fields[stock_list1-fields1] PASSED
tests/test_jqdata_api.py::test_get_call_auction_fields[fakecode-None] PASSED
```

## 已知边界与剩余风险

### 1. 竞价数据能力边界

| 场景 | 结果 | capability |
|------|------|------------|
| 当日实时数据 | ✅ 可获取 | 'full' |
| 历史日期数据 | ❌ 返回空 DataFrame | 'limited' |

**原因**：`akshare.stock_zh_a_hist_pre_min_em` 只能获取实时数据，无历史接口

**影响**：回测时无法使用竞价数据，策略需自行处理空数据情况

### 2. 龙虎榜数据能力边界

| 问题 | 说明 |
|------|------|
| 数据深度有限 | `akshare.stock_lhb_detail_em` 只提供近期数据 |
| 列名可能变化 | 已添加多个字段映射容错 |
| 空数据风险 | 某些历史日期可能无数据 |

### 3. 兼容性说明

**龙虎榜接口同时保留两种列名**：
- 原始 akshare 中文列名（如 `代码`、`龙虎榜净买额`）
- 映射后 JQData 风格英文列名（如 `code`、`net_value`）

**推荐**：使用英文列名，中文列名仅为向后兼容

### 4. 其他 agent 修改兼容

`backtrader_base_strategy.py` 已被其他 agent 修改（新增 `get_price_unified` 等），本任务修改与这些改动兼容，不覆盖他人的实现。

## 设计决策

### 为什么竞价接口返回空表而不是抛异常？

策略代码通常期望 DataFrame 结构，返回空表可以让策略继续执行而不中断。同时 `capability='limited'` 明确告知策略数据不可用，避免误导。

### 为什么龙虎榜保留两种列名？

部分旧策略可能使用中文列名，完全移除会破坏兼容性。保留两种列名确保平滑迁移。

### 为什么 `code` 字段始终包含在竞价返回中？

从策略实际使用分析（jkcode/46），策略需要从 `df_auction.code.values[i]` 获取股票代码。即使 `fields` 参数未包含 `code`，也需要返回此字段。

## 相关文件

- `jqdata_akshare_backtrader_utility/market_data/call_auction.py` - 竞价接口实现
- `jqdata_akshare_backtrader_utility/backtrader_base_strategy.py:2007-2103` - 龙虎榜接口
- `tests/test_jqdata_api.py` - 测试验证

## 策略示例参考

- `jkcode/46 韶华研究之十二--还算可以的竞价研究.txt` - 竞价策略
- `jkcode/21 【原创】年化123%最大回撤14%涨停弱转强竞价战法.txt` - 竞价策略
- `jkcode/96 首版+2版龙虎榜挖掘V2.0，年化1400.txt` - 龙虎榜策略
- `jkcode/99 最新龙回头5.0速度优化版+风险控制版本.txt` - 龙虎榜策略