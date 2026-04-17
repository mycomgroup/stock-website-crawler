# Task 04 Result

## 修改文件

- `jqdata_akshare_backtrader_utility/utils/standardize.py`
- `jqdata_akshare_backtrader_utility/market_data/minute.py`
- `jqdata_akshare_backtrader_utility/market_api.py`
- `tests/test_minute_data.py`

## 完成内容

### 1. 统一标准化层

在 `utils/standardize.py` 中添加了统一的标准化函数：

- `normalize_columns(df, column_map)` - 列名映射（中文 -> 英文）
- `normalize_datetime(df, errors)` - 时间戳格式统一处理
- `validate_required_columns(df, required_cols)` - 必要列验证
- `convert_numeric_columns(df, numeric_cols, dtype)` - 数值类型转换
- `COLUMN_MAP_COMMON` - 通用列名映射字典
- `COLUMN_MAP_DAILY` - 日线数据专用映射字典

更新了 `standardize_ohlcv()` 和 `standardize_minute_ohlcv()` 函数使用统一的基础函数。

### 2. 分钟数据后端改进

更新 `market_data/minute.py`：

- 使用 `ak.stock_zh_a_hist_min_em()` 替代已废弃的 `ak.stock_zh_a_minute()`
- 使用 `ak.fund_etf_hist_min_em()` 替代不支持分钟级别的 `ak.fund_etf_hist_em()`
- 统一使用 `utils/standardize.py` 的标准化函数
- `_prepare_for_storage()` 函数替代 `_normalize_minute_columns()`

### 3. market_api 分钟数据支持

更新 `market_api.py`：

- 导入并使用统一的标准化层
- `_fetch_price_data()` 函数支持分钟频率
- 正确识别股票/ETF 代码并调用对应 API
- 时间过滤时正确处理 datetime 类型转换

### 4. 测试用例覆盖

更新 `tests/test_minute_data.py`，共 49 个测试用例，覆盖：

| 测试类 | 测试数量 | 覆盖内容 |
|--------|----------|----------|
| TestStandardizeFunctions | 12 | 标准化函数单元测试 |
| TestMinuteDataStandardize | 8 | 分钟数据标准化 |
| TestDailyDataStandardize | 2 | 日线数据标准化 |
| TestPeriodValidation | 6 | 周期参数验证 |
| TestPrepareForStorage | 4 | 数据存储准备 |
| TestStockMinuteData | 2 | 股票分钟数据获取（网络测试，跳过） |
| TestETFMinuteData | 2 | ETF 分钟数据获取（网络测试，跳过） |
| TestDuckDBMinuteTables | 3 | DuckDB 表结构验证 |
| TestMinuteDataIntegration | 3 | 上层接口集成 |
| TestEdgeCases | 7 | 边界情况处理 |

### 5. 支持的周期

- 1m (1分钟)
- 5m (5分钟)
- 15m (15分钟)
- 30m (30分钟)
- 60m (60分钟)

### 6. 输出标准列

- `datetime` - 时间戳
- `open` - 开盘价
- `high` - 最高价
- `low` - 最低价
- `close` - 收盘价
- `volume` - 成交量
- `money` - 成交额
- `openinterest` - 持仓量 (默认 0.0)

## 验证命令

```bash
# pytest 测试
python3 -m pytest tests/test_minute_data.py -v

# smoke test（需要网络）
python3 -c "from tests.test_minute_data import run_smoke_test; run_smoke_test()"

# 直接测试
python3 -c "
import sys
sys.path.insert(0, 'jqdata_akshare_backtrader_utility')
from market_data.minute import get_stock_minute, get_etf_minute
from datetime import datetime

today = datetime.now().strftime('%Y-%m-%d')
start = '2026-03-25'

# 股票分钟数据
df = get_stock_minute('sh600000', start, today, period='5m')
print(f'Stock: {len(df)} 条')

# ETF 分钟数据
df = get_etf_minute('510300', start, today, period='5m')
print(f'ETF: {len(df)} 条')
"
```

## 验证结果

```
$ python3 -m pytest tests/test_minute_data.py -v
============================= test session starts ==============================
collected 49 items

tests/test_minute_data.py::TestStandardizeFunctions::test_normalize_columns_basic PASSED
tests/test_minute_data.py::TestStandardizeFunctions::test_normalize_columns_preserves_original PASSED
tests/test_minute_data.py::TestStandardizeFunctions::test_normalize_columns_custom_map PASSED
tests/test_minute_data.py::TestStandardizeFunctions::test_normalize_datetime_standard_format PASSED
tests/test_minute_data.py::TestStandardizeFunctions::test_normalize_datetime_with_time PASSED
tests/test_minute_data.py::TestStandardizeFunctions::test_normalize_datetime_sorted PASSED
tests/test_minute_data.py::TestStandardizeFunctions::test_normalize_datetime_invalid_dropped PASSED
tests/test_minute_data.py::TestStandardizeFunctions::test_normalize_datetime_no_datetime_column PASSED
tests/test_minute_data.py::TestStandardizeFunctions::test_convert_numeric_columns_basic PASSED
tests/test_minute_data.py::TestStandardizeFunctions::test_convert_numeric_columns_with_nan PASSED
tests/test_minute_data.py::TestStandardizeFunctions::test_validate_required_columns_pass PASSED
tests/test_minute_data.py::TestStandardizeFunctions::test_validate_required_columns_fail PASSED
tests/test_minute_data.py::TestMinuteDataStandardize::test_standard_columns PASSED
tests/test_minute_data.py::TestMinuteDataStandardize::test_standardize_with_missing_money PASSED
tests/test_minute_data.py::TestMinuteDataStandardize::test_standardize_with_missing_volume PASSED
tests/test_minute_data.py::TestMinuteDataStandardize::test_standardize_with_amount_alias PASSED
tests/test_minute_data.py::TestMinuteDataStandardize::test_standardize_with_chinese_columns PASSED
tests/test_minute_data.py::TestMinuteDataStandardize::test_standardize_sorted_by_datetime PASSED
tests/test_minute_data.py::TestMinuteDataStandardize::test_standardize_empty_dataframe PASSED
tests/test_minute_data.py::TestMinuteDataStandardize::test_standardize_missing_required_column PASSED
tests/test_minute_data.py::TestDailyDataStandardize::test_standardize_daily_columns PASSED
tests/test_minute_data.py::TestDailyDataStandardize::test_standardize_daily_with_chinese_columns PASSED
tests/test_minute_data.py::TestPeriodValidation::test_validate_period_standard PASSED
tests/test_minute_data.py::TestPeriodValidation::test_validate_period_uppercase PASSED
tests/test_minute_data.py::TestPeriodValidation::test_validate_period_alias_minute PASSED
tests/test_minute_data.py::TestPeriodValidation::test_validate_period_invalid PASSED
tests/test_minute_data.py::TestPeriodValidation::test_all_periods_in_valid_periods PASSED
tests/test_minute_data.py::TestPeriodValidation::test_period_map_mapping PASSED
tests/test_minute_data.py::TestPrepareForStorage::test_prepare_basic PASSED
tests/test_minute_data.py::TestPrepareForStorage::test_prepare_sorted PASSED
tests/test_minute_data.py::TestPrepareForStorage::test_prepare_missing_required_column PASSED
tests/test_minute_data.py::TestPrepareForStorage::test_prepare_empty_datetime PASSED
tests/test_minute_data.py::TestStockMinuteData::test_get_stock_minute_1m SKIPPED
tests/test_minute_data.py::TestStockMinuteData::test_get_stock_minute_all_periods SKIPPED
tests/test_minute_data.py::TestETFMinuteData::test_get_etf_minute_5m SKIPPED
tests/test_minute_data.py::TestETFMinuteData::test_get_etf_minute_all_periods SKIPPED
tests/test_minute_data.py::TestDuckDBMinuteTables::test_tables_exist PASSED
tests/test_minute_data.py::TestDuckDBMinuteTables::test_table_structure_stock_minute PASSED
tests/test_minute_data.py::TestDuckDBMinuteTables::test_table_structure_etf_minute PASSED
tests/test_minute_data.py::TestMinuteDataIntegration::test_get_price_minute_integration PASSED
tests/test_minute_data.py::TestMinuteDataIntegration::test_import_chain PASSED
tests/test_minute_data.py::TestMinuteDataIntegration::test_import_from_market_data_init PASSED
tests/test_minute_data.py::TestEdgeCases::test_single_row_dataframe PASSED
tests/test_minute_data.py::TestEdgeCases::test_large_dataframe PASSED
tests/test_minute_data.py::TestEdgeCases::test_float_precision PASSED
tests/test_minute_data.py::TestEdgeCases::test_negative_values PASSED
tests/test_minute_data.py::TestEdgeCases::test_zero_values PASSED
tests/test_minute_data.py::TestEdgeCases::test_duplicate_datetime PASSED
tests/test_minute_data.py::TestEdgeCases::test_missing_all_ohlcv PASSED

=================== 45 passed, 4 skipped, 1 warning in 3.39s ===================
```

## 已知边界

1. **数据源依赖**: 分钟数据依赖 akshare 的东方财富接口，接口稳定性依赖于东方财富网站
2. **日期范围限制**: akshare 分钟数据接口通常返回最近几个月的数据，无法获取历史很久的数据
3. **周末/节假日**: 非交易日无分钟数据
4. **网络依赖**: smoke test 需要网络访问，pytest 中跳过网络测试
5. **股票代码判断**: ETF 识别基于代码前缀 (51/15/50)，可能存在特殊情况
6. **未修改**: timer 和 finance 模块未改动，按任务要求保持不变