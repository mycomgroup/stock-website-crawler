# 函数重复定义重构报告

## 执行日期
2026-04-01

## 问题分析

项目中存在多处函数重复定义，导致维护困难和潜在的不一致问题。

### 发现的重复函数

| 函数名 | 原定义位置 | 问题 |
|--------|-----------|------|
| `get_price` | strategy_base.py, market_api.py, runner.py | 3处定义，实现不同 |
| `get_index_stocks` | strategy_base.py, index_components.py | 2处定义，实现略有不同 |
| `format_stock_symbol` | strategy_base.py, symbol.py, market_api.py | 3处定义，功能相同 |
| `get_trading_days/get_all_trade_days` | strategy_base.py, runner.py, date_utils.py | 多处定义 |

## 重构方案

### 设计原则
1. **核心实现放在最底层的模块**
2. **API层重新导出作为兼容层**
3. **其他模块从核心模块导入**

### 重构后导入关系图

```
src/utils/symbol.py              [主实现]
    format_stock_symbol()
    jq_code_to_ak()
    ak_code_to_jq()
    normalize_symbol()
         │
         ▼
src/api/market_api.py            [导入使用]
    from utils.symbol import normalize_symbol, get_symbol_prefix
         │
         ▼
src/core/strategy_base.py        [重新导出兼容层]
    from utils.symbol import format_stock_symbol, jq_code_to_ak, ak_code_to_jq
         │
         ▼
src/core/runner.py               [导入使用]
    from strategy_base import format_stock_symbol_for_akshare, jq_code_to_ak


src/utils/date_utils.py          [主实现]
    get_all_trade_days()
    get_trade_days()
    is_trade_date()
    get_previous_trade_date()
    get_next_trade_date()
         │
         ▼
src/core/strategy_base.py        [重新导出兼容层]
    from utils.date_utils import get_all_trade_days, get_trade_days
         │
         ▼
src/core/runner.py               [导入使用]
    from strategy_base import get_trade_days, get_all_trade_days


src/api/market_api.py            [主实现]
    get_price()
    history()
    attribute_history()
    get_bars()
         │
         ▼
src/core/strategy_base.py        [兼容层包装]
    get_price_jq() -> 调用 market_api.get_price()
    get_price_unified() -> 调用 market_api.get_price()
    get_price_simple() -> 简化版（内部使用）
         │
         ▼
src/core/runner.py               [包装器]
    get_price_wrapper() -> 包装 get_price_jq()


src/market_data/index_components.py  [主实现]
    get_index_stocks()
    get_index_components()
         │
         ▼
src/core/strategy_base.py        [保留本地实现]
    get_index_stocks() -> 使用 get_index_weights()
    （注：保留此实现因为有 robust 参数和预运行模式功能）
```

## 执行的修改

### 1. src/utils/symbol.py (增强)
- 添加完整的文档和类型注解
- 添加 `jq_code_to_ak()`, `ak_code_to_jq()` 函数
- 添加 `normalize_symbol()`, `get_symbol_prefix()` 函数
- 添加兼容别名 `format_stock_symbol_for_akshare`

### 2. src/utils/date_utils.py (增强)
- 添加 `get_all_trade_days()` 函数（主实现）
- 添加 `get_trade_days()` 函数
- 添加 `is_trade_date()`, `get_previous_trade_date()`, `get_next_trade_date()`
- 添加 `count_trade_days_between()`
- 支持 DuckDB 缓存和 pickle fallback

### 3. src/core/strategy_base.py (修改)
- 从 `utils/symbol.py` 导入股票代码转换函数
- 从 `utils/date_utils.py` 导入交易日函数
- 删除重复的函数定义
- 保留 `get_index_stocks()` 本地实现（因为有特殊功能）
- 重命名 `get_price()` 为 `get_price_simple()`（内部使用）

### 4. src/api/market_api.py (修改)
- 从 `utils/symbol.py` 导入代码转换函数
- 删除内部 `_normalize_symbol()` 和 `_get_symbol_prefix()` 定义

### 5. src/core/runner.py (修改)
- 从 `strategy_base` 导入 `get_trade_days`
- 删除本地 `get_trade_days()` 函数定义

## 验证结果

所有导入测试通过:
- `utils/symbol.py` 函数正常工作
- `utils/date_utils.py` 函数正常工作
- `strategy_base.py` 导入成功
- `runner.py` 导入成功

## 后续建议

1. **统一 get_index_stocks**: 考虑将 `strategy_base.py` 和 `index_components.py` 中的 `get_index_stocks` 合并，保留 robust 和预运行模式功能

2. **添加单元测试**: 为统一模块添加单元测试，确保函数行为一致

3. **更新文档**: 更新 API 文档，明确各函数的主实现位置

4. **渐进式清理**: 后续可以进一步清理其他重复函数，如:
   - `get_all_securities`
   - `get_security_info`
   - `get_fundamentals`