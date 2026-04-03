# 数据缓存技术方案 v2.0

## 问题诊断

### 1. 失败原因分析

| 问题类型 | 表现 | 影响 | 优先级 |
|---------|------|------|--------|
| 并发锁冲突 | DuckDB写入锁被占用 | 部分数据写入失败 | P0 |
| 网络连接中断 | Connection aborted, RemoteDisconnected | 下载失败需重试 | P0 |
| 新股数据不足 | 301xxx/688xxx历史数据<500行 | 策略无法使用 | P2 |
| 重试机制简陋 | 固定3次重试，无退避 | 高峰期失败率高 | P1 |
| 错误未分类 | 所有错误统一处理 | 无法针对性恢复 | P1 |

### 2. 失败股票特征

```
按代码前缀分布:
  60xxx: 505只 (沪市主板，部分次新股)
  00xxx: 202只 (深市主板)
  30xxx: 194只 (创业板，多为新股)
  68xxx: 122只 (科创板，上市时间短)
```

## 改进方案

### 1. 并发控制优化

**问题**: DuckDB 在多进程写入时会报锁冲突

**解决方案**: 使用任务队列 + 单写入进程

```python
# 方案A: 使用 Redis 队列 (推荐生产环境)
import redis
from queue import Queue

class CacheQueue:
    """分布式缓存任务队列"""
    
    def __init__(self, redis_url="redis://localhost:6379"):
        self.redis = redis.from_url(redis_url)
        self.queue_key = "cache:tasks"
    
    def push(self, task: dict):
        """添加任务到队列"""
        self.redis.rpush(self.queue_key, json.dumps(task))
    
    def pop(self, timeout=10) -> Optional[dict]:
        """从队列获取任务"""
        result = self.redis.blpop(self.queue_key, timeout=timeout)
        if result:
            return json.loads(result[1])
        return None
```

```python
# 方案B: 使用文件队列 (轻量级，无需额外依赖)
import os
import json
import fcntl

class FileQueue:
    """基于文件的进程安全队列"""
    
    def __init__(self, queue_dir="data/queue"):
        self.queue_dir = queue_dir
        os.makedirs(queue_dir, exist_ok=True)
        self.pending_dir = os.path.join(queue_dir, "pending")
        self.processing_dir = os.path.join(queue_dir, "processing")
        os.makedirs(self.pending_dir, exist_ok=True)
        os.makedirs(self.processing_dir, exist_ok=True)
    
    def push(self, task: dict) -> str:
        """添加任务，返回任务ID"""
        task_id = f"{time.time_ns()}_{task.get('symbol', 'unknown')}"
        task_file = os.path.join(self.pending_dir, f"{task_id}.json")
        with open(task_file, 'w') as f:
            json.dump(task, f)
        return task_id
    
    def pop(self) -> Optional[tuple]:
        """获取任务 (进程安全)"""
        for filename in sorted(os.listdir(self.pending_dir)):
            pending_file = os.path.join(self.pending_dir, filename)
            processing_file = os.path.join(self.processing_dir, filename)
            
            try:
                # 原子性移动
                os.rename(pending_file, processing_file)
                with open(processing_file) as f:
                    task = json.load(f)
                return filename, task
            except FileExistsError:
                continue  # 已被其他进程处理
        return None
    
    def complete(self, task_id: str):
        """标记任务完成"""
        processing_file = os.path.join(self.processing_dir, task_id)
        if os.path.exists(processing_file):
            os.remove(processing_file)
```

### 2. 智能重试机制

**问题**: 固定3次重试，无指数退避，无错误分类

**解决方案**: 分级重试 + 指数退避 + 错误分类

```python
import time
import random
from enum import Enum
from dataclasses import dataclass
from typing import Optional, Callable, TypeVar

class ErrorType(Enum):
    """错误类型分类"""
    TRANSIENT = "transient"      # 暂时性错误，可重试 (网络超时、服务器繁忙)
    RATE_LIMIT = "rate_limit"    # 限流，需要等待
    NOT_FOUND = "not_found"      # 数据不存在，无需重试
    INVALID = "invalid"          # 参数错误，无需重试
    UNKNOWN = "unknown"          # 未知错误，尝试重试

@dataclass
class RetryConfig:
    """重试配置"""
    max_retries: int = 5
    base_delay: float = 1.0      # 基础延迟(秒)
    max_delay: float = 60.0      # 最大延迟(秒)
    exponential_base: float = 2.0  # 指数基数
    jitter: bool = True          # 是否添加随机抖动
    
    # 不同错误类型的重试策略
    error_strategies: dict = None
    
    def __post_init__(self):
        if self.error_strategies is None:
            self.error_strategies = {
                ErrorType.TRANSIENT: {"max_retries": 5, "base_delay": 2.0},
                ErrorType.RATE_LIMIT: {"max_retries": 10, "base_delay": 5.0},
                ErrorType.NOT_FOUND: {"max_retries": 0},
                ErrorType.INVALID: {"max_retries": 0},
                ErrorType.UNKNOWN: {"max_retries": 3, "base_delay": 1.0},
            }

def classify_error(error: Exception) -> ErrorType:
    """根据异常类型分类错误"""
    error_str = str(error).lower()
    
    # 暂时性错误
    if any(kw in error_str for kw in [
        "timeout", "connection", "reset", "refused", 
        "aborted", "disconnected", "503", "502", "429"
    ]):
        return ErrorType.TRANSIENT
    
    # 限流
    if "rate limit" in error_str or "too many" in error_str:
        return ErrorType.RATE_LIMIT
    
    # 数据不存在
    if any(kw in error_str for kw in [
        "not found", "empty", "no data", "不存在"
    ]):
        return ErrorType.NOT_FOUND
    
    # 参数错误
    if any(kw in error_str for kw in [
        "invalid", "参数", "format"
    ]):
        return ErrorType.INVALID
    
    return ErrorType.UNKNOWN

def calculate_delay(attempt: int, config: RetryConfig, error_type: ErrorType) -> float:
    """计算重试延迟 (指数退避 + 抖动)"""
    strategy = config.error_strategies.get(error_type, {})
    base = strategy.get("base_delay", config.base_delay)
    
    # 指数退避
    delay = base * (config.exponential_base ** attempt)
    delay = min(delay, config.max_delay)
    
    # 添加随机抖动 (避免惊群效应)
    if config.jitter:
        delay = delay * (0.5 + random.random())
    
    return delay

T = TypeVar('T')

def retry_with_backoff(
    func: Callable[..., T],
    config: RetryConfig = None,
    on_retry: Optional[Callable[[int, Exception, float], None]] = None,
) -> T:
    """带指数退避的重试装饰器"""
    if config is None:
        config = RetryConfig()
    
    last_error = None
    
    for attempt in range(config.max_retries):
        try:
            return func()
        except Exception as e:
            last_error = e
            error_type = classify_error(e)
            strategy = config.error_strategies.get(error_type, {})
            max_retries = strategy.get("max_retries", config.max_retries)
            
            if attempt >= max_retries:
                raise
            
            delay = calculate_delay(attempt, config, error_type)
            
            if on_retry:
                on_retry(attempt, e, delay)
            
            time.sleep(delay)
    
    raise last_error
```

### 3. 数据源健康检查

**问题**: 不知道数据源是否可用就开始请求

**解决方案**: 预检测 + 动态切换

```python
import time
from datetime import datetime, timedelta
from dataclasses import dataclass, field
from typing import Dict, List, Optional
import threading

@dataclass
class SourceHealth:
    """数据源健康状态"""
    name: str
    available: bool = True
    last_check: datetime = None
    last_success: datetime = None
    last_error: str = None
    error_count: int = 0
    success_count: int = 0
    avg_latency: float = 0.0
    latency_samples: List[float] = field(default_factory=list)
    
    def record_success(self, latency: float):
        self.last_success = datetime.now()
        self.success_count += 1
        self.available = True
        self.error_count = 0
        
        # 记录延迟样本
        self.latency_samples.append(latency)
        if len(self.latency_samples) > 10:
            self.latency_samples.pop(0)
        self.avg_latency = sum(self.latency_samples) / len(self.latency_samples)
    
    def record_error(self, error: str):
        self.last_error = error
        self.error_count += 1
        if self.error_count >= 5:
            self.available = False
    
    def should_use(self) -> bool:
        """是否应该使用此数据源"""
        if not self.available:
            # 检查是否应该恢复 (5分钟后)
            if self.last_success:
                elapsed = datetime.now() - self.last_success
                if elapsed > timedelta(minutes=5):
                    self.available = True
                    self.error_count = 0
        return self.available

class DataSourceHealthMonitor:
    """数据源健康监控"""
    
    _instance = None
    _lock = threading.Lock()
    
    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
                    cls._instance._sources: Dict[str, SourceHealth] = {}
        return cls._instance
    
    def get_health(self, source: str) -> SourceHealth:
        if source not in self._sources:
            self._sources[source] = SourceHealth(name=source)
        return self._sources[source]
    
    def get_best_source(self, sources: List[str]) -> Optional[str]:
        """获取最佳数据源 (基于延迟和可用性)"""
        available = [
            s for s in sources 
            if self.get_health(s).should_use()
        ]
        if not available:
            return None
        
        # 按平均延迟排序
        return min(available, key=lambda s: self.get_health(s).avg_latency)
    
    def check_source(self, source: str, check_func: Callable[[], bool]) -> bool:
        """检查数据源是否可用"""
        health = self.get_health(source)
        health.last_check = datetime.now()
        
        start = time.time()
        try:
            result = check_func()
            latency = time.time() - start
            if result:
                health.record_success(latency)
            else:
                health.record_error("Check failed")
            return result
        except Exception as e:
            health.record_error(str(e))
            return False

# 使用示例
def prefetch_with_health_check(symbol: str, start: str, end: str) -> pd.DataFrame:
    """带健康检查的数据获取"""
    monitor = DataSourceHealthMonitor()
    sources = ["sina", "east_money", "tushare", "baostock"]
    
    # 获取最佳数据源
    best_source = monitor.get_best_source(sources)
    if not best_source:
        # 所有数据源不可用，尝试恢复
        for source in sources:
            monitor.check_source(source, lambda: quick_check(source))
        best_source = monitor.get_best_source(sources)
    
    if best_source:
        health = monitor.get_health(best_source)
        fetcher = get_fetcher(best_source)
        
        start_time = time.time()
        try:
            df = fetcher(symbol, start, end)
            health.record_success(time.time() - start_time)
            return df
        except Exception as e:
            health.record_error(str(e))
            # 降级到下一个数据源
            remaining = [s for s in sources if s != best_source]
            return prefetch_with_health_check(symbol, start, end)
    
    return pd.DataFrame()
```

### 4. 增量更新策略

**问题**: 每次全量更新，浪费时间和资源

**解决方案**: 只更新缺失的日期

```python
from datetime import datetime, timedelta
from typing import Set

def get_missing_dates(
    symbol: str,
    start: str,
    end: str,
    db: DuckDBManager
) -> List[str]:
    """获取缺失的交易日期"""
    
    # 获取已有数据的日期
    existing_dates = set()
    try:
        df = db.get_stock_daily(symbol, start, end)
        if not df.empty and 'datetime' in df.columns:
            existing_dates = set(df['datetime'].dt.strftime('%Y-%m-%d'))
    except:
        pass
    
    # 获取所有交易日
    trade_days = get_trade_days(start, end)
    
    # 计算缺失日期
    missing = [d for d in trade_days if d not in existing_dates]
    return missing

def incremental_update(
    symbol: str,
    start: str,
    end: str,
    db: DuckDBManager,
    max_missing_ratio: float = 0.3,
) -> pd.DataFrame:
    """增量更新策略
    
    如果缺失比例超过阈值，执行全量更新
    否则只下载缺失日期
    """
    
    # 获取缺失日期
    missing = get_missing_dates(symbol, start, end, db)
    
    if not missing:
        logger.info(f"{symbol}: 数据完整，无需更新")
        return db.get_stock_daily(symbol, start, end)
    
    missing_ratio = len(missing) / len(get_trade_days(start, end))
    
    if missing_ratio > max_missing_ratio:
        # 缺失过多，执行全量更新
        logger.info(f"{symbol}: 缺失{missing_ratio:.1%}，执行全量更新")
        return full_update(symbol, start, end, db)
    else:
        # 增量更新
        logger.info(f"{symbol}: 缺失{len(missing)}天，执行增量更新")
        return partial_update(symbol, missing, db)

def partial_update(symbol: str, missing_dates: List[str], db: DuckDBManager) -> pd.DataFrame:
    """部分更新 (仅下载缺失日期)"""
    
    if not missing_dates:
        return pd.DataFrame()
    
    # 按月份分组下载
    from collections import defaultdict
    by_month = defaultdict(list)
    for d in missing_dates:
        month = d[:7]  # YYYY-MM
        by_month[month].append(d)
    
    all_data = []
    for month, dates in sorted(by_month.items()):
        start = dates[0]
        end = dates[-1]
        
        # 下载数据
        df = fetch_from_best_source(symbol, start, end)
        if df is not None and not df.empty:
            all_data.append(df)
            time.sleep(0.5)  # 避免请求过快
    
    if all_data:
        new_df = pd.concat(all_data, ignore_index=True)
        db.insert_stock_daily(symbol, new_df)
    
    return db.get_stock_daily(symbol, missing_dates[0], missing_dates[-1])
```

### 5. 离线优先策略

**问题**: 网络不可用时无法工作

**解决方案**: 优先使用本地缓存，网络作为补充

```python
def get_stock_daily_offline_first(
    symbol: str,
    start: str,
    end: str,
    adjust: str = "qfq",
    offline_mode: bool = False,
) -> pd.DataFrame:
    """离线优先的数据获取策略
    
    1. 首先检查本地缓存
    2. 如果缓存完整，直接返回
    3. 如果缓存不完整且非离线模式，尝试从网络补充
    4. 如果网络失败，返回部分缓存数据
    """
    
    db = DuckDBManager()
    
    # 1. 检查本地缓存
    cached_df = db.get_stock_daily(symbol, start, end, adjust)
    
    if not cached_df.empty:
        # 检查缓存是否完整
        expected_days = count_trade_days(start, end)
        actual_days = len(cached_df)
        
        if actual_days >= expected_days * 0.95:  # 允许5%容差
            logger.info(f"{symbol}: 缓存完整 ({actual_days}/{expected_days}天)")
            return standardize_ohlcv(cached_df)
        
        logger.info(f"{symbol}: 缓存不完整 ({actual_days}/{expected_days}天)")
    
    # 2. 离线模式，返回已有缓存
    if offline_mode:
        if not cached_df.empty:
            logger.warning(f"{symbol}: 离线模式，返回部分缓存")
            return standardize_ohlcv(cached_df)
        raise ValueError(f"{symbol}: 离线模式无缓存数据")
    
    # 3. 尝试从网络获取
    try:
        df = fetch_with_retry(symbol, start, end, adjust)
        if df is not None and not df.empty:
            # 合并缓存和新数据
            if not cached_df.empty:
                df = pd.concat([cached_df, df]).drop_duplicates(subset=['datetime'])
            db.insert_stock_daily(symbol, df, adjust)
            return standardize_ohlcv(df)
    except Exception as e:
        logger.warning(f"{symbol}: 网络获取失败: {e}")
        
        # 4. 网络失败，返回部分缓存
        if not cached_df.empty:
            logger.warning(f"{symbol}: 使用部分缓存数据")
            return standardize_ohlcv(cached_df)
        raise
```

### 6. 失败任务管理

**问题**: 失败任务没有记录，无法后续重试

**解决方案**: 记录失败任务，支持批量重试

```python
import json
import os
from datetime import datetime
from typing import Dict, List, Optional
from dataclasses import dataclass, asdict

@dataclass
class FailedTask:
    """失败任务记录"""
    symbol: str
    start: str
    end: str
    adjust: str
    error_type: str
    error_message: str
    attempt_count: int
    first_failed_at: str
    last_failed_at: str
    data_sources_tried: List[str]

class FailedTaskManager:
    """失败任务管理器"""
    
    def __init__(self, log_file: str = "data/failed_tasks.json"):
        self.log_file = log_file
        self.tasks: Dict[str, FailedTask] = {}
        self._load()
    
    def _load(self):
        """加载失败任务"""
        if os.path.exists(self.log_file):
            try:
                with open(self.log_file, 'r') as f:
                    data = json.load(f)
                    for k, v in data.items():
                        self.tasks[k] = FailedTask(**v)
            except:
                pass
    
    def _save(self):
        """保存失败任务"""
        os.makedirs(os.path.dirname(self.log_file), exist_ok=True)
        with open(self.log_file, 'w') as f:
            json.dump({k: asdict(v) for k, v in self.tasks.items()}, f, indent=2)
    
    def record_failure(
        self,
        symbol: str,
        start: str,
        end: str,
        adjust: str,
        error: Exception,
        sources_tried: List[str],
    ):
        """记录失败任务"""
        key = f"{symbol}_{start}_{end}_{adjust}"
        error_type = classify_error(error).value
        
        now = datetime.now().isoformat()
        
        if key in self.tasks:
            # 更新已有记录
            task = self.tasks[key]
            task.attempt_count += 1
            task.last_failed_at = now
            task.error_message = str(error)[:200]
            task.data_sources_tried = sources_tried
        else:
            # 新建记录
            self.tasks[key] = FailedTask(
                symbol=symbol,
                start=start,
                end=end,
                adjust=adjust,
                error_type=error_type,
                error_message=str(error)[:200],
                attempt_count=1,
                first_failed_at=now,
                last_failed_at=now,
                data_sources_tried=sources_tried,
            )
        
        self._save()
    
    def record_success(self, symbol: str, start: str, end: str, adjust: str):
        """记录成功 (移除失败记录)"""
        key = f"{symbol}_{start}_{end}_{adjust}"
        if key in self.tasks:
            del self.tasks[key]
            self._save()
    
    def get_retryable_tasks(self, max_attempts: int = 5) -> List[FailedTask]:
        """获取可重试的任务"""
        return [
            t for t in self.tasks.values()
            if t.attempt_count < max_attempts
            and t.error_type in ["transient", "rate_limit", "unknown"]
        ]
    
    def get_summary(self) -> Dict:
        """获取失败任务统计"""
        by_error_type = {}
        for task in self.tasks.values():
            by_error_type[task.error_type] = by_error_type.get(task.error_type, 0) + 1
        
        return {
            "total": len(self.tasks),
            "by_error_type": by_error_type,
            "retryable": len(self.get_retryable_tasks()),
        }

# 使用示例
failed_manager = FailedTaskManager()

def fetch_with_failure_tracking(
    symbol: str,
    start: str,
    end: str,
    adjust: str = "qfq",
):
    """带失败追踪的数据获取"""
    sources_tried = []
    
    for source in ["sina", "east_money", "baostock"]:
        sources_tried.append(source)
        try:
            df = fetch_from_source(source, symbol, start, end, adjust)
            if df is not None and not df.empty:
                failed_manager.record_success(symbol, start, end, adjust)
                return df
        except Exception as e:
            continue
    
    # 所有数据源失败
    last_error = Exception("All sources failed")
    failed_manager.record_failure(
        symbol, start, end, adjust,
        last_error, sources_tried
    )
    raise last_error
```

## 实施计划

### Phase 1: 基础优化 (已完成)
- [x] 多数据源备份
- [x] Sina 作为优先数据源
- [x] 本地缓存优先

### Phase 2: 并发优化
- [ ] 实现文件队列
- [ ] 单写入进程模式
- [ ] 批量写入优化

### Phase 3: 重试优化
- [ ] 指数退避重试
- [ ] 错误分类
- [ ] 数据源健康监控

### Phase 4: 增量更新
- [ ] 缺失日期检测
- [ ] 部分更新策略
- [ ] 失败任务管理

### Phase 5: 监控告警
- [ ] 缓存完整率监控
- [ ] 数据源可用性监控
- [ ] 自动恢复机制

## 配置建议

```yaml
# cache_config.yaml

# 并发控制
concurrency:
  max_workers: 5          # 最大并行数
  queue_size: 100         # 队列大小
  batch_size: 20          # 批量写入大小
  write_timeout: 30       # 写入超时(秒)

# 重试策略
retry:
  max_retries: 5
  base_delay: 1.0
  max_delay: 60.0
  exponential_base: 2.0
  jitter: true

  # 按错误类型配置
  strategies:
    transient:
      max_retries: 5
      base_delay: 2.0
    rate_limit:
      max_retries: 10
      base_delay: 5.0
    not_found:
      max_retries: 0
    invalid:
      max_retries: 0

# 数据源配置
data_sources:
  priority: ["sina", "east_money", "tushare", "baostock"]
  
  health_check:
    enabled: true
    interval: 300         # 检查间隔(秒)
    timeout: 10           # 检查超时(秒)
  
  rate_limit:
    sina:
      requests_per_second: 5
    east_money:
      requests_per_second: 3

# 增量更新
incremental:
  enabled: true
  max_missing_ratio: 0.3  # 超过30%缺失执行全量更新
  
# 失败任务
failed_tasks:
  log_file: "data/failed_tasks.json"
  max_attempts: 5
  auto_retry_interval: 3600  # 自动重试间隔(秒)
```