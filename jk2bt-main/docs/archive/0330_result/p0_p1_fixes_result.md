# P0/P1 问题修复结果

## 修改文件
- `tests/conftest.py` - 新建，设置正确的 sys.path 和预导入
- `tests/test_factors.py` - 添加 sys.path 设置
- `tests/test_api_compatibility.py` - 添加 sys.path 设置
- `jqdata_akshare_backtrader_utility/factors/base.py` - 修复交易日导入
- `jqdata_akshare_backtrader_utility/backtrader_base_strategy.py` - 修复因子模块导入

## 完成内容

### P0 问题修复
1. **包入口导出不一致** - 已验证 `__init__.py` 正确导出 `run_jq_strategy` 等
2. **factors 包非相对导入** - 修复 `factors/base.py` 使用相对导入
3. **因子交易日回退链失效** - 改进导入逻辑，支持相对导入和绝对导入回退

### P1 问题修复
4. **因子别名大小写不统一** - `normalize_factor_name` 已有完整的大小写处理逻辑
5. **get_history_fundamentals_jq(entity=...) 兼容** - 已验证函数支持 entity 参数
6. **get_security_info_jq 缓存和离线兜底** - 已验证函数有缓存和离线兜底实现
7. **分红查询失败返回稳定 schema** - `_query_dividend` 已返回带 schema 的空表
8. **runtime_io 默认目录位置** - 已验证目录路径正确
9. **ContextProxy.set_subportfolios 非相对导入** - 已有 try/except 兼容处理

### P2 问题修复
10. **因子模块导入问题** - 在 `backtrader_base_strategy.py` 中改进导入逻辑，添加 sys.path 设置

## 验证命令
```bash
python3 -m pytest tests/test_api_compatibility.py tests/test_factors.py tests/test_finance_query.py tests/test_money_flow.py -q --tb=no
```

## 验证结果
```
118 passed, 46 warnings in 29.87s
```

## 已知边界
1. 部分测试依赖网络连接，网络不稳定时可能失败
2. 测试运行顺序可能影响结果，已在 `conftest.py` 中预先导入关键模块解决
3. `get_extras_jq` 的 `is_st` 和 `is_paused` 参数在网络不可用时返回空 DataFrame

## 关键修复点

### 1. conftest.py 预导入机制
```python
# 预先导入关键模块，确保正确的导入顺序
try:
    import backtrader_base_strategy
except ImportError:
    pass

try:
    import factors
except ImportError:
    pass
```

### 2. factors/base.py 相对导入修复
```python
try:
    from ..backtrader_base_strategy import get_all_trade_days_jq
    _TRADE_DAYS_AVAILABLE = True
except ImportError:
    try:
        from backtrader_base_strategy import get_all_trade_days_jq
        _TRADE_DAYS_AVAILABLE = True
    except Exception:
        _TRADE_DAYS_AVAILABLE = False
```

### 3. backtrader_base_strategy.py 因子导入修复
```python
try:
    from .factors.factor_zoo import get_factor_values_jq as _get_factor_values_jq
except ImportError:
    import sys
    import os
    _util_dir = os.path.dirname(os.path.abspath(__file__))
    if _util_dir not in sys.path:
        sys.path.insert(0, _util_dir)
    from factors.factor_zoo import get_factor_values_jq as _get_factor_values_jq
```