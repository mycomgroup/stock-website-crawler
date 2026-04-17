# 代码重复与冗余改造计划

> 生成日期: 2026-04-17
> 项目: jk2bt (聚宽策略本地运行框架)
> 备注: 已排除缓存相关代码 (CacheManager 相关由其他模块统一管理)

---

## 一、问题总览

| 优先级 | 重复类型 | 影响范围 | 预计优化行数 |
|--------|----------|----------|-------------|
| P0 | 异常类重复定义 | 5 处 | ~50 行 |
| P0 | 日期解析函数 `_parse_date()` | 7+ 处 | ~100 行 |
| P0 | 日期范围过滤 `_filter_by_date_range()` | 4+ 处 | ~60 行 |
| P0 | `__init__.py` 重复导入 | 1 处 | ~20 行 |
| P1 | 股票代码转换函数 | 5+ 处 | ~150 行 |
| P1 | 百分比解析 `_parse_ratio()` | 4+ 处 | ~60 行 |
| P1 | 数据源配置常量 | 3 处 | ~30 行 |
| P2 | `normalize_datetime` 函数重复 | 2 处 | ~40 行 |
| P2 | `get_all_trade_days` 函数重复 | 4+ 处 | ~80 行 |
| P2 | 指数常量 `SUPPORTED_INDEXES` | 2 处 | ~50 行 |
| P2 | `_DATE_COLUMN_CANDIDATES` 常量 | 2 处 | ~30 行 |
| P3 | 空 DataFrame 返回模式 | 273 处 | 可抽象工具函数 |
| P3 | `df.copy()` 调用 | 116 处 | 需评估必要性 |

**总计影响文件**: 30+
**预计减少重复代码**: 1500+ 行

---

## 二、详细改造方案

### 2.1 P0 优先级 - 立即处理

#### 2.1.1 异常类统一定义

**问题**: `DataSourceError`、`MarketDataError` 等异常类在多个位置重复定义。

**当前状态**:
| 文件 | 异常类 |
|------|--------|
| `jk2bt/core/exceptions.py` | ✅ 官方定义 |
| `jk2bt/api/market.py:68-77` | ❌ 重复定义 |
| `jk2bt/data_access/data_source.py:15-22` | ❌ 重复定义 |
| `jk2bt/factors/data_sources.py:46-52` | ❌ 重复定义 |

**改造方案**:
```python
# 删除以下文件的重复定义，统一从 core/exceptions.py 导入
# jk2bt/api/market.py:68-77
# jk2bt/data_access/data_source.py:15-22
# jk2bt/factors/data_sources.py:46-52

# 改为:
from jk2bt.core.exceptions import (
    DataSourceError,
    MarketDataError,
    NetworkError,
    ValidationError
)
```

---

#### 2.1.2 日期解析函数统一

**问题**: `_parse_date()` 函数在多个模块重复定义。

**当前状态**:
| 文件 | 行号 |
|------|------|
| `jk2bt/finance_data/share_change.py` | ~200 |
| `jk2bt/finance_data/shareholder.py` | ~845 |
| `jk2bt/finance_data/unlock.py` | ~196 |
| `jk2bt/finance_data/dividend.py` | ~218 |
| `jk2bt/finance_data/company_info.py` | - |
| `jk2bt/market_data/index_components.py` | ~279 |

**改造方案**:
```python
# 新建 jk2bt/utils/date_utils.py 或扩展现有文件

def parse_date(date_str) -> Optional[str]:
    """统一日期解析函数"""
    if not date_str or pd.isna(date_str):
        return None
    date_str = str(date_str).strip()
    for fmt in ["%Y-%m-%d", "%Y%m%d", "%Y/%m/%d"]:
        try:
            dt = datetime.strptime(date_str, fmt)
            return dt.strftime("%Y-%m-%d")
        except ValueError:
            continue
    return None

# 各模块删除本地定义，改为:
from jk2bt.utils.date_utils import parse_date as _parse_date
```

---

#### 2.1.3 日期范围过滤函数统一

**问题**: `_filter_by_date_range()` 在多个文件重复实现。

**当前状态**:
| 文件 | 行号 |
|------|------|
| `jk2bt/finance_data/dividend.py` | ~396 |
| `jk2bt/finance_data/unlock.py` | ~352 |
| `jk2bt/finance_data/share_change.py` | ~327 |
| `jk2bt/market_data/index_components.py` | ~549 (命名 `_filter_history_by_date`) |

**改造方案**:
```python
# 在 jk2bt/utils/date_utils.py 添加

def filter_by_date_range(
    df: pd.DataFrame,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    date_col: str = "datetime"
) -> pd.DataFrame:
    """统一日期范围过滤"""
    if start_date is None and end_date is None:
        return df
    if start_date:
        df = df[df[date_col] >= pd.to_datetime(start_date)]
    if end_date:
        df = df[df[date_col] <= pd.to_datetime(end_date)]
    return df
```

---

#### 2.1.4 `__init__.py` 重复导入修复

**问题**: `jk2bt/data_access/__init__.py` 第47-87行存在完全重复的导入。

**改造方案**:
```python
# 删除 jk2bt/data_access/__init__.py 中第72-87行的重复导入
# 保留第47-62行的导入即可
```

---

### 2.2 P1 优先级 - 短期处理

#### 2.2.1 股票代码转换函数统一

**问题**: 相同功能函数多处定义，部分模块未使用通用实现。

**当前状态**:
| 文件 | 函数 |
|------|------|
| `jk2bt/utils/symbol.py` | ✅ `format_stock_symbol()`, `jq_code_to_ak()`, `ak_code_to_jq()` |
| `jk2bt/core/securities_utils.py` | ❌ `jq_code_to_ak()`, `ak_code_to_jq()` 重复定义 |
| `jk2bt/api/_internal/symbol_utils.py` | ❌ `get_symbol_prefix` 重复定义 |
| `jk2bt/data_access/multi_source_adapter.py` | ❌ `_normalize_symbol` 局部实现 |
| `jk2bt/data_access/akshare_adapter.py` | ❌ `_normalize_symbol` 局部实现 |

**改造方案**:
1. 删除 `securities_utils.py` 中的 `jq_code_to_ak`, `ak_code_to_jq` 定义
2. 删除 `symbol_utils.py` 文件，所有导入改为 `from jk2bt.utils.symbol import ...`
3. `multi_source_adapter.py` 和 `akshare_adapter.py` 中的 `_normalize_symbol` 改为调用 `utils/symbol.py`

---

#### 2.2.2 百分比解析函数统一

**问题**: `_parse_ratio()` 函数在多个 finance_data 模块重复定义。

**当前状态**:
| 文件 |
|------|
| `jk2bt/finance_data/share_change.py` |
| `jk2bt/finance_data/dividend.py` |
| `jk2bt/finance_data/shareholder.py` |
| `jk2bt/finance_data/company_info.py` |

**改造方案**:
```python
# 在 jk2bt/utils/date_utils.py 或新建 jk2bt/utils/parsers.py 添加

def parse_ratio(value) -> Optional[float]:
    """统一百分比解析"""
    if value is None or value == "" or value == "-":
        return None
    try:
        if isinstance(value, str):
            value = value.replace("%", "").strip()
            return float(value) / 100 if float(value) > 1 else float(value)
        return float(value)
    except (ValueError, TypeError):
        return None
```

---

#### 2.2.3 数据源配置常量统一

**问题**: 数据源配置在多处定义。

**当前状态**:
| 文件 | 常量 |
|------|------|
| `jk2bt/data_access/multi_source_adapter.py:22-23` | `_DEFAULT_STOCK_DAILY_SOURCES`, `_DEFAULT_ETF_DAILY_SOURCES` |
| `jk2bt/data_access/akshare_adapter.py:64` | `DEFAULT_DATA_SOURCES` |
| `jk2bt/utils/data_source_backup.py:50-53` | ✅ 完整定义 |

**改造方案**:
```python
# 删除 multi_source_adapter.py 和 akshare_adapter.py 中的定义
# 统一从 data_source_backup.py 导入

from jk2bt.utils.data_source_backup import (
    DEFAULT_STOCK_DAILY_SOURCES,
    DEFAULT_ETF_DAILY_SOURCES,
    DEFAULT_INDEX_SOURCES,
    DEFAULT_MINUTE_SOURCES
)
```

---

### 2.3 P2 优先级 - 后续优化

#### 2.3.1 `normalize_datetime` 函数去重

**问题**: `normalize_datetime` 在以下位置重复定义:
- `jk2bt/utils/standardize.py` (官方实现)
- `jk2bt/api/market.py:41-56` (fallback实现)

**改造方案**:
```python
# 删除 jk2bt/api/market.py:41-56 的定义
# 改为从 standardize.py 导入

from jk2bt.utils.standardize import normalize_datetime
```

---

#### 2.3.2 `get_all_trade_days` 函数统一

**问题**: 函数在多处定义或调用。

**当前状态**:
| 文件 | 说明 |
|------|------|
| `jk2bt/utils/date_utils.py` | ✅ 官方实现 |
| `jk2bt/api/jq_compat.py:1963` | 导入别名 |
| `jk2bt/core/strategy_base.py:640-644` | 导入别名 |
| `jk2bt/db/meta_cache_api.py:36` | 局部实现 |

**改造方案**:
```python
# 统一使用 jk2bt/utils/date_utils.py 中的实现
# 删除其他文件的重复定义和别名
```

---

#### 2.3.3 指数常量统一

**问题**: `SUPPORTED_INDEXES` 在多处定义。

**当前状态**:
| 文件 |
|------|
| `jk2bt/core/securities_utils.py:121-143` |
| `jk2bt/finance_data/index_fundamentals_robust.py:31-51` |

**改造方案**:
```python
# 创建 jk2bt/core/constants.py 统一管理

# SECURITY_INDEXES = {
#     "000300": "沪深300",
#     "000016": "上证50",
#     "000905": "中证500",
#     "000852": "中证1000",
#     ...
# }

# 其他文件删除本地定义，改为导入
```

---

#### 2.3.4 `_DATE_COLUMN_CANDIDATES` 常量统一

**问题**: 常量在以下位置重复定义:
- `jk2bt/core/securities_utils.py:25-36`
- `jk2bt/utils/date_utils.py:37-48`

**改造方案**:
```python
# 在 jk2bt/core/constants.py 统一管理
# 其他文件删除本地定义，统一导入
```

---

### 2.4 P3 优先级 - 可选优化

#### 2.4.1 空 DataFrame 返回模式

**问题**: 273 处返回空 DataFrame 的代码。

**当前模式**:
```python
return pd.DataFrame(columns=_SCHEMA)
```

**改造方案**:
```python
# 创建工具函数
def empty_df(schema: List[str]) -> pd.DataFrame:
    return pd.DataFrame(columns=schema)

# 或使用 functools.partial
empty_df_by_schema = partial(pd.DataFrame, columns=[])
```

---

#### 2.4.2 `df.copy()` 调用评估

**问题**: 116 处 `df.copy()` 调用，部分可能不必要。

**改造方案**:
1. 对只读操作，移除不必要的 `copy()`
2. 使用 context manager 封装需要复制的场景
3. 标记可疑位置进行人工评估

---

#### 2.4.3 数据验证逻辑简化

**问题**: 200+ 处 `if df is None or df.empty:` 检查。

**改造方案**:
```python
# 创建装饰器
def validate_dataframe(empty_handler=None):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # 统一验证逻辑
            ...
        return wrapper
    return decorator
```

---

## 三、改造执行顺序

### Phase 1: P0 优先级 (立即执行)
1. ✅ 删除 `data_access/__init__.py` 重复导入
2. ✅ 统一异常类定义
3. ✅ 创建 `utils/date_utils.py` 统一日期函数
4. ✅ 统一 `_filter_by_date_range` 函数

### Phase 2: P1 优先级 (短期执行)
5. ✅ 统一股票代码转换函数
6. ✅ 统一百分比解析函数
7. ✅ 统一数据源配置常量

### Phase 3: P2 优先级 (后续执行)
8. ✅ `normalize_datetime` 去重
9. ✅ `get_all_trade_days` 统一
10. ✅ 创建 `core/constants.py` 统一常量管理
11. ✅ 删除 `api/_internal/symbol_utils.py`

### Phase 4: P3 优先级 (可选)
12. ⬜ 空 DataFrame 工具函数
13. ⬜ `df.copy()` 评估
14. ⬜ 数据验证装饰器

---

## 四、注意事项

1. **向后兼容**: 改造过程中保持 API 兼容性
2. **测试覆盖**: 每次改造后运行测试确保功能正常
3. **渐进式**: 建议分阶段执行，避免一次性大规模改动
4. **文档更新**: 改造完成后更新相关文档

---

## 五、预期收益

- **代码量减少**: ~1500+ 行重复代码
- **维护成本降低**: 消除多处同步更新的风险
- **代码一致性**: 统一的数据处理和错误处理方式
- **可读性提升**: 减少理解代码的认知负担
