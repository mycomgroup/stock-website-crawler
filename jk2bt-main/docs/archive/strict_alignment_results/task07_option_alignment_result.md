# Task 07 Result: 期权数据对齐

## 修改文件

- `jqdata_akshare_backtrader_utility/market_data/option.py`
- `tests/test_bond_option_api.py`

## 完成内容

### 1. 字段命名对齐

- 新增 `underlying_code` 字段作为 JoinQuant 标准字段
- 保留 `underlying` 字段作为兼容别名
- 新增 `underlying_name` 字段（标的名称）
- 新增 `contract_unit`、`exercise_type`、`listing_date` 字段

### 2. Schema 定义

新增并导出标准 schema 常量：

```python
OPTION_SCHEMA = [
    "option_code", "option_name", "underlying_code", "underlying",
    "underlying_name", "strike", "expiry_date", "option_type",
    "contract_unit", "exercise_type", "listing_date",
    "close", "volume", "date"
]

OPTION_BASIC_SCHEMA = [
    "option_code", "option_name", "underlying_code", "underlying_name",
    "strike", "expiry_date", "option_type", "contract_unit",
    "exercise_type", "listing_date"
]

OPTION_DAILY_SCHEMA = [
    "option_code", "date", "open", "high", "low", "close",
    "volume", "amount", "pre_close", "implied_vol"
]

GREEKS_SCHEMA = [
    "option_code", "option_name", "delta", "gamma", "theta", "vega",
    "implied_vol", "strike", "last_price", "theoretical_value", "date"
]
```

### 3. 全局 finance 查询对齐

- `finance.STK_OPTION_BASIC` - 期权基础信息表
- `finance.STK_OPTION_DAILY` - 期权日行情表
- 空结果返回稳定 schema

### 4. 函数更新

| 函数 | 更新内容 |
|------|----------|
| `_parse_sse_option_row` | 添加 `underlying_code`, `underlying_name` 字段 |
| `_parse_szse_option_row` | 添加 `underlying_code`, `underlying_name` 字段 |
| `_parse_cffex_option_row` | 添加 `underlying_code`, `underlying_name` 字段 |
| `FinanceQuery.run_query` | 更新 schema 处理逻辑 |
| `run_query_simple` | 支持 `underlying_code` 过滤 |
| `get_option_chain` | 支持 `underlying_code` 字段过滤 |

## 验证命令

```bash
python3 -m pytest -q tests/test_option_api.py
python3 -m pytest -q tests/test_bond_option_api.py
```

## 验证结果

```
tests/test_option_api.py: 52 passed, 9 skipped
tests/test_bond_option_api.py: 4 passed
```

## 已知边界

1. 期权数据依赖 AkShare 接口，部分字段可能为空
2. 中金所期权（CFFEX）的到期日字段可能无法解析
3. `listing_date` 字段当前数据源未提供，默认为 None
4. 缓存使用 pickle 格式，DuckDB 缓存可选

## API 参考

### get_option_list

```python
result = get_option_list(underlying="sse")  # sse/szse/cffex/all
if result.success:
    df = result.data  # DataFrame with OPTION_SCHEMA columns
```

### finance.STK_OPTION_BASIC

```python
from jqdata_akshare_backtrader_utility.backtrader_base_strategy import finance, query
df = finance.run_query(finance.STK_OPTION_BASIC)
```

### finance.STK_OPTION_DAILY

```python
df = finance.run_query(finance.STK_OPTION_DAILY)
```

### run_query_simple

```python
from jqdata_akshare_backtrader_utility.market_data.option import run_query_simple
df = run_query_simple("STK_OPTION_BASIC", underlying_code="510050")
df = run_query_simple("STK_OPTION_DAILY", option_code="10002224")
```