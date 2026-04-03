# API 快速开始指南

## 安装依赖

```bash
pip install akshare duckdb pandas
```

## 基本使用

### 1. 导入模块

```python
from jqdata_akshare_backtrader_utility.finance_data import (
    get_company_info,
    get_top_shareholders,
    get_dividend_info,
)
from jqdata_akshare_backtrader_utility.backtrader_base_strategy import finance, query
```

### 2. 查询公司信息

```python
# 直接调用
df = get_company_info("600519.XSHG")
print(df)

# 使用 finance.run_query
df = finance.run_query(
    query(finance.STK_COMPANY_BASIC_INFO).filter(
        finance.STK_COMPANY_BASIC_INFO.code.in_(["600519.XSHG"])
    )
)
print(df)
```

### 3. 查询股东信息

```python
# 获取十大股东
df = get_top_shareholders("600519.XSHG")

# 获取股东户数
df = get_shareholder_count("600519.XSHG")
```

### 4. 查询分红信息

```python
# 获取分红记录
df = get_dividend_info("600519.XSHG")

# 使用 finance 接口
df = finance.run_query(
    query(finance.STK_XR_XD).filter(
        finance.STK_XR_XD.code.in_(["600519.XSHG"])
    )
)
```

## 常用查询示例

### 批量查询多只股票

```python
stocks = ["600519.XSHG", "000001.XSHE", "000858.XSHE"]

# 批量查询公司信息
from jqdata_akshare_backtrader_utility.finance_data import query_company_basic_info
df = query_company_basic_info(stocks)
```

### 带日期范围的查询

```python
# 查询分红记录（带日期范围）
from datetime import datetime, timedelta

start_date = "2020-01-01"
end_date = "2024-12-31"

df = get_dividend_info("600519.XSHG", start_date=start_date, end_date=end_date)
```

### 使用过滤条件

```python
# 查询分红金额大于0的记录
df = finance.run_query(
    query(
        finance.STK_XR_XD.code,
        finance.STK_XR_XD.bonus_amount_rmb,
    ).filter(
        finance.STK_XR_XD.code.in_(["600519.XSHG"]),
        finance.STK_XR_XD.bonus_amount_rmb > 0,
    )
)
```

## 支持的代码格式

API 支持多种股票代码格式：

```python
# 聚宽格式（推荐）
"600519.XSHG"  # 上交所
"000001.XSHE"  # 深交所

# 其他格式
"sh600519"     # 带前缀
"600519"       # 纯数字
```

## 缓存管理

### 查看缓存

```python
import os
cache_dir = "finance_cache"
files = os.listdir(cache_dir)
print(f"缓存文件数: {len(files)}")
```

### 强制更新

```python
# 强制重新下载数据
df = get_company_info("600519.XSHG", force_update=True)
```

## 错误处理

```python
from jqdata_akshare_backtrader_utility.finance_data import get_company_info

try:
    df = get_company_info("600519.XSHG")
    if df.empty:
        print("未找到数据")
    else:
        print(df)
except Exception as e:
    print(f"查询失败: {e}")
```

## 性能优化建议

1. **使用缓存**：默认启用 DuckDB 和 pickle 双层缓存
2. **批量查询**：使用 `query_*` 批量查询函数
3. **避免频繁更新**：设置合理的缓存有效期

## 完整 API 列表

### 公司信息 (任务1)
- `get_company_info(symbol)` - 获取公司基本信息
- `get_security_status(symbol, date)` - 获取证券状态
- `query_company_basic_info(symbols)` - 批量查询

### 股东信息 (任务2)
- `get_top_shareholders(symbol)` - 获取十大股东
- `get_shareholder_count(symbol)` - 获取股东户数

### 分红送股 (任务3)
- `get_dividend_info(symbol)` - 获取分红信息

### 股东变动 (任务4)
- `get_share_change(symbol)` - 获取股东变动

### 限售解禁 (任务5)
- `get_unlock(symbol)` - 获取解禁信息

### 可转债 (任务6)
- `get_conversion_bond_list()` - 获取可转债列表

### 期权 (任务7)
- `get_option_list()` - 获取期权列表

### 指数成分股 (任务8)
- `get_index_components(index)` - 获取指数成分股

### 申万行业 (任务9)
- `get_stock_industry(symbol)` - 获取股票行业

### 宏观数据 (任务10)
- `get_macro_china_gdp()` - 获取GDP数据

---

**详细文档：** 请参考 `docs/api_implementation_report.md`
