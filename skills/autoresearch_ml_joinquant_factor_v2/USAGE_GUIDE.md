# OSS 因子文件下载 + 价格拼接使用指南

## 问题：DuckDB 被锁定

如果遇到以下错误：
```
IO Error: Could not set lock on file "market.duckdb": Conflicting lock is held in PID 94724
```

**解决方法：**

### 方法 1: 关闭占用 DuckDB 的进程

```bash
# 1. 查看占用进程
ps aux | grep duckdb

# 2. 找到进程 ID (PID)，例如 94724

# 3. 关闭进程
kill 94724

# 或者强制关闭
kill -9 94724
```

### 方法 2: 等待其他进程完成

如果其他进程正在更新数据库，等待它完成后再运行下载脚本。

### 方法 3: 使用导出的价格数据（推荐）

我已经创建了一个工具，可以先从 DuckDB 导出价格数据到 CSV 文件，然后使用 CSV 文件进行价格拼接，避免 DuckDB 锁定问题。

## 使用步骤

### 步骤 1: 导出价格数据（只需执行一次）

等 DuckDB 可用时，运行：

```bash
python3 export_price_data.py
```

这会将价格数据导出到 `./data/price_cache/` 目录，按年份组织。

### 步骤 2: 下载因子并拼接价格

```bash
python3 download_with_price_from_csv.py
```

或在 Python 中：

```python
from download_with_price_from_csv import download_and_merge_factors

# 下载指定日期范围
download_and_merge_factors(
    start_date="2024-01-01",
    end_date="2024-01-31"
)

# 下载整年
from download_with_price_from_csv import download_year_with_price
download_year_with_price(2024)
```

## 文件说明

- `download_oss.py` - 基础 OSS 下载工具
- `download_with_price_final.py` - 从 DuckDB 实时读取价格（需要 DuckDB 可用）
- `export_price_data.py` - 导出价格数据到 CSV（待创建）
- `download_with_price_from_csv.py` - 从 CSV 文件读取价格（待创建）

## 输出文件结构

```
data/factors_with_price/
├── 2024/
│   ├── factors_20240101_all.csv  # 包含 close_price 列
│   ├── factors_20240102_all.csv
│   └── ...
└── 2025/
    └── ...
```

每个文件最后会多一列 `close_price`，包含当天的股票收盘价。

## 常见问题

### Q: 价格匹配率低怎么办？

A: 检查股票代码格式是否一致。因子文件中的代码格式（如 `002001.XSHE`）需要与 DuckDB 中的格式匹配。

### Q: 如何修改价格列名？

A: 使用 `price_column_name` 参数：

```python
download_and_merge_factors(
    start_date="2024-01-01",
    end_date="2024-01-31",
    price_column_name="收盘价"  # 自定义列名
)
```

### Q: 如何指定股票代码列？

A: 使用 `stock_code_column` 参数：

```python
download_and_merge_factors(
    start_date="2024-01-01",
    end_date="2024-01-31",
    stock_code_column="股票代码"  # 默认使用第一列
)
```

## 性能优化

1. **批量下载**: 下载整年比多次下载单日更高效
2. **价格缓存**: 价格数据会自动缓存，避免重复查询
3. **并行处理**: 可以修改代码支持多线程下载（高级用法）

## 联系支持

如有问题，请检查日志输出或联系开发团队。
