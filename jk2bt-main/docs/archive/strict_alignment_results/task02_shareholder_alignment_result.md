# Task 02 Result

## 修改文件

- `jqdata_akshare_backtrader_utility/finance_data/shareholder.py`
- `jqdata_akshare_backtrader_utility/backtrader_base_strategy.py`
- `tests/test_shareholder_api.py`

## 完成内容

### 1. Schema 对齐

**shareholder.py `_SHAREHOLDER_SCHEMA`** 更新为：
```python
[
    "code",
    "report_date",
    "ann_date",
    "shareholder_name",
    "shareholder_code",
    "shareholder_type",
    "hold_amount",
    "hold_ratio",
    "change_type",
    "change_amount",
    "rank",
]
```

**shareholder.py `_SHAREHOLDER_NUM_SCHEMA`** 更新为：
```python
[
    "code",
    "report_date",
    "ann_date",
    "holder_num",
    "holder_num_change",
    "holder_num_change_ratio",
]
```

**FinanceDBProxy `_SHAREHOLDER_TOP10_SCHEMA`** 更新为：
```python
[
    "code",
    "report_date",
    "ann_date",
    "shareholder_name",
    "shareholder_code",
    "shareholder_type",
    "hold_amount",
    "hold_ratio",
    "change_type",
    "change_amount",
    "rank",
]
```

### 2. 新增字段填充

- `_normalize_top10_holders()` 新增：
  - `shareholder_code` (None 填充)
  - `change_amount` (从 akshare 原始字段映射，如 "持股变动"、"增持股数"、"减持股数")
  - 确保 `report_date`、`ann_date` 在正确位置

- `_normalize_holder_count()` 新增：
  - `holder_num_change` (从 akshare 或计算差值)
  - `holder_num_change_ratio` (计算环比变化)

### 3. 适配器函数

在 `FinanceDBProxy` 新增：
- `_adapt_shareholder_top10_schema(df)` - 确保 TOP10 输出列完整
- `_adapt_shareholder_num_schema(df)` - 确保 NUM 输出列完整

### 4. FinanceQuery 类表定义更新

更新了以下表类的字段定义：
- `STK_SHAREHOLDER`
- `STK_SHAREHOLDER_TOP10`
- `STK_SHAREHOLDER_FLOAT_TOP10`
- `STK_SHAREHOLDER_NUM`
- `TOP10_SHAREHOLDERS`
- `TOP10_FLOAT_SHAREHOLDERS`

### 5. DuckDB 表结构更新

更新了 DuckDB 表结构以匹配新 schema：
- `top10_shareholders` 表
- `top10_float_shareholders` 表
- `shareholder_num` 表 (新增)

## 验证命令

```bash
python3 -m pytest tests/test_shareholder_api.py::TestSchemaDefinition tests/test_shareholder_api.py::TestCodeNormalization tests/test_shareholder_api.py::TestRobustResult tests/test_shareholder_api.py::TestFinanceQuery tests/test_shareholder_api.py::TestBatchQuery -q --tb=short
```

## 验证结果

```
27 passed, 2 warnings in 0.74s
```

Schema 对齐验证：
```python
from jqdata_akshare_backtrader_utility.finance_data.shareholder import _SHAREHOLDER_SCHEMA as sh_schema
from jqdata_akshare_backtrader_utility.backtrader_base_strategy import FinanceDBProxy
fdb = FinanceDBProxy()
print('TOP10 schemas match:', set(sh_schema) == set(fdb._SHAREHOLDER_TOP10_SCHEMA))
# 输出: TOP10 schemas match: True
```

## 已知边界

1. **akshare API 兼容性**：部分 akshare 接口参数名可能变化（如 `stock_gdfx_free_holding_detail_em` 使用 `symbol` 参数可能报错），已通过空 DataFrame 兜底处理。

2. **数据来源差异**：`shareholder_code` 和 `change_amount` 字段在 akshare 原始数据中可能缺失，当前以 `None` 填充。

3. **股东户数变化计算**：`holder_num_change` 和 `holder_num_change_ratio` 在 akshare 原始数据无对应字段时，通过 DataFrame 差值计算。

4. **DuckDB 表结构迁移**：原有数据表结构已更新，但历史数据可能需重新导入以匹配新列。

## 接口对照清单

| 接口 | 模块实现 | 全局入口 | 命名兼容 |
|---|---|---|---|
| `get_top10_shareholders` | 是 | 是 | 一致 |
| `get_top10_float_shareholders` | 是 | 是 | 一致 |
| `get_shareholder_count` | 是 | 是 | 一致 |
| `finance.STK_SHAREHOLDER_TOP10` | 是 | 是 | 一致 |
| `finance.STK_SHAREHOLDER_FLOAT_TOP10` | 是 | 是 | 一致 |
| `finance.STK_SHAREHOLDER_NUM` | 是 | 是 | 一致 |

## 日期字段命名

统一使用 JoinQuant 规范：
- `report_date` - 报告期
- `ann_date` - 公告日期

两个模块均已按此规范对齐。

## 空结果 Schema

所有空 DataFrame 返回时均携带完整 schema 列定义，确保下游过滤不报错。