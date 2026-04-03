# 任务 1: Runner 命名空间纠偏 - 完成报告

**执行时间**: 2026-03-30

---

## 1. 修改的文件

| 文件 | 操作 | 说明 |
|------|------|------|
| `jqdata_akshare_backtrader_utility/jq_strategy_runner.py` | 修改 | 主要修复目标 |
| `tests/test_namespace_correction.py` | 新增 | 测试用例 |
| `tests/test_jq_runner.py` | 修改 | 修复导入路径 |

---

## 2. 完成的修复内容

### 2.1 命名空间绑定纠偏

**问题**: `load_jq_strategy()` 暴露给策略代码的 API 绑定到了内部简化版函数，而非完整版 JQ 风格实现。

**修复**: 将以下函数重新绑定到完整版实现：

| 函数名 | 原绑定 | 现绑定 |
|--------|--------|--------|
| `get_price` | 简化版 (无 count/panel 参数) | `get_price_jq` (完整版) |
| `get_all_trade_days` | runner 内部简化实现 | `get_all_trade_days_jq` |
| `get_extras` | runner 内部简化实现 | `get_extras_jq` |
| `get_billboard_list` | runner 内部空实现 | `get_billboard_list_jq` |
| `get_bars` | runner 内部简化实现 | `get_bars_jq` |

**代码变更** (jq_strategy_runner.py 导入部分):

```python
try:
    from .backtrader_base_strategy import (
        # ... 其他导入 ...
        get_price_jq,
        get_all_trade_days_jq,
        get_extras_jq,
        get_billboard_list_jq,
        get_bars_jq,
    )
    # 绑定到完整版实现
    get_price = get_price_jq
    get_all_trade_days = get_all_trade_days_jq
    get_extras = get_extras_jq
    get_billboard_list = get_billboard_list_jq
    get_bars = get_bars_jq
except ImportError:
    # ... 同样的回退逻辑 ...
```

### 2.2 编码兼容性增强

**问题**: `load_jq_strategy()` 仅支持 UTF-8 编码，无法读取 GBK/GB2312 编码的中文策略文件。

**修复**: 实现多编码自动回退机制：

```python
_ENCODINGS = ["utf-8", "gbk", "gb2312", "latin-1"]

for encoding in _ENCODINGS:
    try:
        with open(strategy_file, "r", encoding=encoding) as f:
            code = f.read()
        used_encoding = encoding
        break
    except UnicodeDecodeError:
        continue
```

### 2.3 错误处理改进

**问题**: 加载失败时静默返回 `None`，难以定位问题。

**修复**: 抛出明确的异常：

| 错误类型 | 触发条件 |
|----------|----------|
| `FileNotFoundError` | 策略文件不存在 |
| `UnicodeDecodeError` | 所有编码尝试都失败 |
| `SyntaxError` | 策略代码语法错误 |
| `RuntimeError` | 策略执行时异常 |

### 2.4 导入预处理优化

**问题**: 导入语句处理逻辑分散，难以维护；多行 import 语句未被正确处理。

**修复**: 使用正则表达式模式匹配，并支持多行 import 语句处理：

```python
_JQ_MODULE_PATTERNS = [
    r"^from\s+jqdata\s+import",
    r"^import\s+jqdata",
    r"^from\s+jqlib\b",
    r"^import\s+jqlib\b",
    r"^from\s+kuanke\s+import",
    r"^import\s+kuanke",
    r"^from\s+jqfactor\s+import",
    r"^import\s+jqfactor",
]

# 支持多行括号 import
in_jqdata_import = False
paren_depth = 0

for line in lines:
    if in_jqdata_import:
        paren_depth += line.count("(") - line.count(")")
        if paren_depth <= 0:
            in_jqdata_import = False
        continue
    # ...
```

---

## 3. 测试验证

### 3.1 测试文件

新增 `tests/test_namespace_correction.py`，包含以下测试类：

- `TestEncodingFallback`: 编码回退测试 (9 用例)
  - UTF-8/GBK/GB2312/Latin-1 编码
  - 文件不存在异常
  - 语法错误报告
  - 运行时错误报告
  - 空策略文件

- `TestNamespaceBinding`: 命名空间绑定测试 (10 用例)
  - 函数签名验证 (get_price/get_all_trade_days/get_extras/get_billboard_list/get_bars)
  - 策略命名空间绑定验证

- `TestImportPreprocessing`: 导入预处理测试 (10 用例)
  - jqdata/jqlib/kuanke/jqfactor 导入移除
  - 多行 import 处理
  - 正常导入保留

- `TestGlobalNamespaceCompleteness`: 全局命名空间完整性测试 (12 用例)
  - Python 内置函数
  - numpy/pandas/datetime
  - JQ API 完整性

- `TestComplexStrategy`: 复杂策略场景测试 (5 用例)
  - 多函数策略
  - 类策略
  - 嵌套函数、lambda、注释

- `TestEdgeCases`: 边界情况测试 (5 用例)
  - 二进制文件
  - Tab 缩进
  - 大文件
  - 特殊字符
  - 装饰器

### 3.2 验证命令

```bash
cd /Users/yuping/Downloads/git/jk2bt-main
python3 -m pytest tests/test_namespace_correction.py -v
```

### 3.3 测试结果

```
======================== 51 passed, 1 warning in 3.59s ========================
```

**测试覆盖度统计**:

| 测试类 | 用例数 | 状态 |
|--------|--------|------|
| `TestEncodingFallback` | 9 | ✅ 全部通过 |
| `TestNamespaceBinding` | 10 | ✅ 全部通过 |
| `TestImportPreprocessing` | 10 | ✅ 全部通过 |
| `TestGlobalNamespaceCompleteness` | 12 | ✅ 全部通过 |
| `TestComplexStrategy` | 5 | ✅ 全部通过 |
| `TestEdgeCases` | 5 | ✅ 全部通过 |
| **总计** | **51** | **100% 通过** |

---

## 4. 兼容性说明

### 4.1 保持的兼容性

- 策略代码调用方式不变
- 所有 JQ 风格 API 签名不变
- 原有 `txt` 策略可原样运行

### 4.2 API 签名确认

`get_price_jq` 完整参数签名：

```
get_price_jq(
    symbols,           # 必需
    start_date=None,
    end_date=None,
    frequency='daily',
    fields=None,
    adjust='qfq',
    count=None,        # ✅ 支持
    panel=False,       # ✅ 支持
    fill_paused=True,
    skip_paused=True,
    cache_dir='stock_cache',
    force_update=False
)
```

---

## 5. 剩余风险 / 已知边界

| 风险项 | 说明 | 影响 |
|--------|------|------|
| 网络依赖 | `get_price_jq` 依赖 akshare 获取数据，网络不可用时可能失败 | 中 |
| 编码检测性能 | 编码检测是顺序尝试，大文件可能有轻微性能影响 | 低 |
| 非标准编码 | 不在支持列表中的编码会失败 | 低 |

---

## 6. 最小验证方式

创建一个简单策略文件测试：

```python
# test_minimal.py
def initialize(context):
    log.info('初始化')
    run_monthly(rebalance, 1, 'open')

def rebalance(context):
    # 验证 get_price 支持 count 参数
    df = get_price('600519.XSHG', end_date='2023-12-31', count=10)
    log.info(f'获取到 {len(df)} 条数据')
```

运行验证：

```bash
cd /Users/yuping/Downloads/git/jk2bt-main/jqdata_akshare_backtrader_utility
python3 -c "
from jq_strategy_runner import load_jq_strategy
import tempfile
import os

# 创建 GBK 编码策略
strategy = '''
def initialize(context):
    log.info('GBK 编码测试')
'''
with tempfile.NamedTemporaryFile(mode='w', encoding='gbk', suffix='.txt', delete=False) as f:
    f.write(strategy)
    f.flush()
    funcs = load_jq_strategy(f.name)
    print(f'加载成功: {list(funcs.keys())}')
    os.unlink(f.name)
"
```

---

## 7. 相关文件索引

| 文件 | 路径 |
|------|------|
| 策略运行器 | `jqdata_akshare_backtrader_utility/jq_strategy_runner.py` |
| 基础策略类 | `jqdata_akshare_backtrader_utility/backtrader_base_strategy.py` |
| 测试文件 | `tests/test_namespace_correction.py` |
| 原有测试 | `tests/test_jq_runner.py` |
| API 测试 | `tests/test_jqdata_api.py` |