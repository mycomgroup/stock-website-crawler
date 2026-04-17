# 任务 10: 批量运行器与并发存储修复 - 完成报告

**执行时间**: 2026-03-30

---

## 1. 修改的文件

| 文件 | 操作 | 说明 |
|------|------|------|
| `jqdata_akshare_backtrader_utility/strategy_scanner.py` | 新建 | 策略可执行性扫描器 |
| `run_strategies_parallel.py` | 修改 | 统计口径修复、集成扫描器 |
| `jqdata_akshare_backtrader_utility/db/duckdb_manager.py` | 修改 | 并发优化、缓存层、重试机制 |

---

## 2. 完成的修复内容

### 2.1 策略扫描器 (strategy_scanner.py)

**功能**: 在运行策略前检查策略的可执行性

**识别能力**:

| 检查项 | 说明 |
|--------|------|
| `initialize` 函数 | 是否存在聚宽风格入口函数 |
| 未实现 API | 检测明显未实现的 API 依赖（如 `get_ticks`） |
| 策略文件区分 | 区分策略文件与研究文档/配套资料 |
| 语法错误 | 检测 Python 语法错误 |

**扫描结果分类** (`StrategyStatus` 枚举):

```
VALID            - 有效策略
NO_INITIALIZE    - 缺少 initialize 函数
MISSING_API      - 缺失必要 API
NOT_STRATEGY     - 非策略文件（研究文档）
SYNTAX_ERROR     - 语法错误
EMPTY_FILE       - 空文件
```

**扫描结果示例**:

```
总文件数: 449
可执行策略: 368

valid: 368 个
no_initialize: 6 个
missing_api: 19 个
not_strategy: 49 个
syntax_error: 7 个
```

### 2.2 统计口径修复 (run_strategies_parallel.py)

**问题**: 原代码中"异常仍可能被算作成功"

**修复**: 细化运行状态分类 (`RunStatus` 枚举):

```python
class RunStatus(Enum):
    SUCCESS_WITH_RETURN = "success_with_return"   # 成功有收益
    SUCCESS_ZERO_RETURN = "success_zero_return"   # 成功零收益
    SUCCESS_NO_TRADE = "success_no_trade"         # 成功无交易
    LOAD_FAILED = "load_failed"                   # 加载失败
    RUN_EXCEPTION = "run_exception"               # 运行异常
    TIMEOUT = "timeout"                           # 超时
    DATA_MISSING = "data_missing"                 # 数据缺失
    SKIPPED_NOT_STRATEGY = "skipped_not_strategy" # 跳过：非策略
    SKIPPED_SYNTAX_ERROR = "skipped_syntax_error" # 跳过：语法错误
    SKIPPED_NO_INITIALIZE = "skipped_no_initialize" # 跳过：无入口
    SKIPPED_MISSING_API = "skipped_missing_api"   # 跳过：缺失API
```

**成功定义**: 策略执行完成且无未处理异常

**报告输出**:

```
运行结果汇总（细分类别）
================================================================================
成功分类:
  成功有收益: X
  成功零收益: X
  成功无交易: X
  成功总计: X
--------------------------------------------------------------------------------
失败分类:
  加载失败: X
  运行异常: X
  超时: X
  数据缺失: X
  失败总计: X
--------------------------------------------------------------------------------
跳过分类:
  非策略文件: X
  语法错误: X
  无initialize: X
  缺失API: X
```

### 2.3 DuckDB 并发优化 (duckdb_manager.py)

**问题**: 多进程并发访问时的锁冲突

**解决方案**:

| 优化项 | 说明 |
|--------|------|
| 独立连接模式 | 每次操作创建独立连接，避免共享连接的锁冲突 |
| 本地内存缓存 | `LocalCache` 类，减少数据库访问频率 |
| 写入重试机制 | 遇锁冲突自动重试 3 次，间隔递增 |
| 只读模式优化 | 多进程并发读取安全 |

**新增工厂函数**:

```python
def get_shared_read_only_manager(db_path=None, use_cache=True):
    """获取只读管理器（推荐多进程并发读取）"""
    
def get_writer_manager(db_path=None, use_cache=False):
    """获取写入管理器（建议单进程写入）"""
    
def clear_global_cache():
    """清除全局缓存"""
```

**缓存层 (`LocalCache`)**:

```python
cache = LocalCache(max_size=1000)
cache.set('stock_daily', '600000', '2023-01-01', '2023-12-31', df)
cached = cache.get('stock_daily', '600000', '2023-01-01', '2023-12-31')
cache.invalidate(table='stock_daily', symbol='600000')
```

**写入重试**:

```python
_WRITE_RETRY_COUNT = 3
_WRITE_RETRY_DELAY = 0.5  # 秒

def _retry_write(self, func, *args, **kwargs):
    """写入操作重试机制"""
    for attempt in range(self._WRITE_RETRY_COUNT):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            if "lock" in str(e).lower() or "conflict" in str(e).lower():
                time.sleep(self._WRITE_RETRY_DELAY * (attempt + 1))
            else:
                raise
```

---

## 3. 测试验证

### 3.1 策略扫描器测试

```bash
cd /Users/yuping/Downloads/git/jk2bt-main
python3 run_strategies_parallel.py --scan-only
```

**输出**:

```
================================================================================
策略扫描结果摘要
================================================================================
总文件数: 449
可执行策略: 368
----------------------------------------
valid: 368
no_initialize: 6
missing_api: 19
not_strategy: 49
syntax_error: 7
```

### 3.2 DuckDB 缓存测试

```bash
cd /Users/yuping/Downloads/git/jk2bt-main/jqdata_akshare_backtrader_utility
python3 -c "
from db.duckdb_manager import DuckDBManager, LocalCache
import pandas as pd

# 测试缓存
cache = LocalCache()
df = pd.DataFrame({'a': [1, 2, 3]})
cache.set('test', '600000', '2023-01-01', '2023-12-31', df)
cached = cache.get('test', '600000', '2023-01-01', '2023-12-31')
print(f'缓存测试: {cached is not None}')

# 测试管理器
manager = DuckDBManager(db_path='/tmp/test.db', use_cache=True)
print(f'管理器: read_only={manager.read_only}, use_cache={manager.use_cache}')
"
```

**输出**:

```
缓存测试: True
管理器: read_only=False, use_cache=True
```

### 3.3 小批次运行测试

```bash
python3 run_strategies_parallel.py --limit 3 --no-confirm
```

---

## 4. 新增命令行参数

```bash
python3 run_strategies_parallel.py --help

--scan-only      # 仅扫描策略，不运行
--skip-scan      # 跳过扫描直接运行
--limit N        # 限制运行策略数量
--no-confirm     # 跳过确认
```

---

## 5. 已知边界 / 剩余风险

| 风险项 | 说明 | 影响 | 建议 |
|--------|------|------|------|
| 未实现 API | 19 个策略依赖 `get_ticks` 等未实现 API | 高 | 需后续补充实现 |
| 语法错误 | 7 个策略有 Python 语法错误 | 中 | 需手动修复 |
| 并发写入 | DuckDB 多进程写入仍有锁冲突风险 | 中 | 建议单进程写入 |
| 网络依赖 | 数据获取依赖 akshare，网络不可用时失败 | 低 | 可预下载数据 |

**缺失 API 列表** (19 个策略依赖):

```
get_ticks           - 逐笔成交数据
get_margin_stocks   - 融资融券标的
get_future_contracts - 期货合约
...
```

---

## 6. 最小验证方式

```bash
# 1. 扫描策略
python3 run_strategies_parallel.py --scan-only

# 2. 运行小批次（3个策略）
python3 run_strategies_parallel.py --limit 3 --no-confirm

# 3. 检查结果报告
ls logs/strategy_runs/
cat logs/strategy_runs/<run_id>/report.txt
```

---

## 7. 相关文件索引

| 文件 | 路径 |
|------|------|
| 策略扫描器 | `jqdata_akshare_backtrader_utility/strategy_scanner.py` |
| 并行运行器 | `run_strategies_parallel.py` |
| 数据库管理器 | `jqdata_akshare_backtrader_utility/db/duckdb_manager.py` |
| 策略目录 | `jkcode/jkcode/` |
| 日志目录 | `logs/strategy_runs/` |