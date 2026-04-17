# 任务 4: 分钟级数据后端 - 实现报告

## 修改的文件

| 文件 | 改动 |
|------|------|
| `jqdata_akshare_backtrader_utility/db/duckdb_manager.py` | 添加 `stock_minute` 和 `etf_minute` 表、插入/查询方法 |
| `jqdata_akshare_backtrader_utility/market_data/minute.py` | **新建** - 统一分钟数据获取模块 |
| `jqdata_akshare_backtrader_utility/utils/standardize.py` | 添加 `standardize_minute_ohlcv()` 函数 |
| `jqdata_akshare_backtrader_utility/market_data/__init__.py` | 导出 `get_stock_minute`, `get_etf_minute`（兼容其他agent添加的 `get_money_flow`） |
| `tests/test_minute_data.py` | **新建** - 单元测试 |

## 完成内容

### 1. 支持周期
- `1m` - 1分钟
- `5m` - 5分钟
- `15m` - 15分钟
- `30m` - 30分钟
- `60m` - 60分钟

### 2. 标准输出列
```
datetime, open, high, low, close, volume, money, openinterest
```

### 3. 本地缓存机制
- 使用 DuckDB 存储，避免重复下载
- 表结构：
  - `stock_minute`: (symbol, datetime, period, open, high, low, close, volume, money, adjust)
  - `etf_minute`: (symbol, datetime, period, open, high, low, close, volume, money)

### 4. 统一标准化层
- `market_data/minute.py` 集中处理：
  - 字段名映射（时间/日期 -> datetime, 成交额/amount -> money）
  - 时间戳格式统一（pd.to_datetime）
  - 缺失字段补充（money, openinterest）
  - 周期参数验证

### 5. 兼容其他 agent 改动
`__init__.py` 保留了其他 agent 添加的 `get_money_flow` 导出

## 验证方式

### 单元测试
```bash
cd /Users/yuping/Downloads/git/jk2bt-main
.venv/bin/python -m pytest tests/test_minute_data.py -v
```

### 手动 Smoke Test（需要网络）
```bash
cd /Users/yuping/Downloads/git/jk2bt-main/jqdata_akshare_backtrader_utility

# 股票分钟数据
python -c "
from market_data.minute import get_stock_minute
df = get_stock_minute('sh600000', '2026-03-25', '2026-03-28', '5m')
print(f'记录数: {len(df)}')
print(f'列: {list(df.columns)}')
print(df.head())
"

# ETF 分钟数据
python -c "
from market_data.minute import get_etf_minute
df = get_etf_minute('510300', '2026-03-25', '2026-03-28', '5m')
print(f'记录数: {len(df)}')
print(f'列: {list(df.columns)}')
print(df.head())
"
```

## API 使用示例

```python
from market_data import get_stock_minute, get_etf_minute

# 获取股票 5 分钟数据
df_stock = get_stock_minute(
    symbol="sh600000",
    start="2026-03-25",
    end="2026-03-28",
    period="5m",      # 1m/5m/15m/30m/60m
    adjust="qfq",     # 复权类型（可选）
    force_update=False  # 强制重新下载
)

# 获取 ETF 15 分钟数据
df_etf = get_etf_minute(
    symbol="510300",
    start="2026-03-25",
    end="2026-03-28",
    period="15m"
)

# 输出格式
# datetime | open | high | low | close | volume | money | openinterest
```

## 剩余风险/已知边界

### 1. akshare 分钟数据限制
- akshare 的分钟数据通常只提供最近一段时间的数据
- 无法获取历史太久的数据（具体限制取决于 akshare 版本）

### 2. 复权处理
- 分钟数据通常不复权
- 当前实现保留 `adjust` 参数接口，但实际效果取决于 akshare 返回

### 3. 上层接口衔接
- `backtrader_base_strategy.py` 中的 `get_price_jq`/`get_bars_jq` 已有分钟数据逻辑
- 可以考虑后续统一调用新模块（本次任务范围外，避免大范围重构）

### 4. ETF 分钟数据 API
- akshare 的 `fund_etf_hist_em` 的分钟周期参数可能与股票不同
- 需要实际网络测试验证各周期是否都支持

### 5. 数据源异常处理
- 当前实现：akshare 返回空数据时抛出 `ValueError`
- 缺失字段时自动补充默认值（money=0, openinterest=0）

## 设计决策

### 为什么新建 minute.py 而不是修改现有文件？
1. 日线和分钟数据有本质差异（DATE vs TIMESTAMP）
2. 分钟数据需要 period 参数
3. 避免影响现有日线数据的稳定性

### 为什么 money 和 amount 都保留？
- akshare 股票分钟数据返回"成交额"
- akshare ETF 数据可能返回"amount"
- 标准化层统一映射到"money"，同时保持兼容

### 数据库表为什么分离 stock_minute 和 etf_minute？
- 股票需要 adjust 字段（复权类型）
- ETF 不需要复权
- 分表查询更高效，避免冗余字段

## 测试结果

```
tests/test_minute_data.py::TestMinuteDataColumns::test_standard_columns PASSED
tests/test_minute_data.py::TestMinuteDataColumns::test_standardize_with_missing_money PASSED
tests/test_minute_data.py::TestMinuteDataColumns::test_standardize_with_amount_alias PASSED
tests/test_minute_data.py::TestStockMinuteData::test_get_stock_minute_1m SKIPPED (需要网络)
tests/test_minute_data.py::TestStockMinuteData::test_period_validation PASSED
tests/test_minute_data.py::TestETFMinuteData::test_get_etf_minute_5m SKIPPED (需要网络)
tests/test_minute_data.py::TestDuckDBMinuteTables::test_tables_exist PASSED
tests/test_minute_data.py::TestMinuteDataIntegration::test_get_price_minute_integration PASSED
tests/test_minute_data.py::TestMinuteDataIntegration::test_import_chain PASSED

=================== 7 passed, 2 skipped, 1 warning in 0.61s ====================
```

---
*完成时间: 2026-03-30*