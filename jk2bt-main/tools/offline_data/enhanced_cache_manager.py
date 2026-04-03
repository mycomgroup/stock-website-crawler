#!/usr/bin/env python3
"""
enhanced_cache_manager.py
增强版缓存管理器 - 解决并发锁冲突、网络中断、重试等问题

主要改进:
1. 文件队列实现进程安全
2. 智能重试 + 指数退避
3. 错误分类和处理
4. 失败任务追踪
5. 增量更新策略
"""

import os
import sys
import json
import time
import random
import logging
import threading
from datetime import datetime, timedelta
from typing import Optional, Dict, List, Callable, Any
from dataclasses import dataclass, asdict, field
from enum import Enum
from pathlib import Path
import traceback

# 项目路径
PROJECT_ROOT = Path(__file__).parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)
logger = logging.getLogger(__name__)


# ============================================================================
# 错误分类
# ============================================================================

class ErrorType(Enum):
    """错误类型"""
    TRANSIENT = "transient"       # 暂时性错误(网络、超时)
    RATE_LIMIT = "rate_limit"     # 限流
    NOT_FOUND = "not_found"       # 数据不存在
    INVALID = "invalid"           # 参数错误
    LOCK_CONFLICT = "lock"        # 数据库锁冲突
    UNKNOWN = "unknown"           # 未知错误


def classify_error(error: Exception) -> ErrorType:
    """根据异常分类错误类型"""
    error_str = str(error).lower()

    # 数据库锁冲突
    if "lock" in error_str or "conflict" in error_str:
        return ErrorType.LOCK_CONFLICT

    # 暂时性错误
    transient_keywords = [
        "timeout", "connection", "reset", "refused",
        "aborted", "disconnected", "503", "502",
        "remote", "eof", "broken pipe"
    ]
    if any(kw in error_str for kw in transient_keywords):
        return ErrorType.TRANSIENT

    # 限流
    if "rate limit" in error_str or "too many" in error_str or "429" in error_str:
        return ErrorType.RATE_LIMIT

    # 数据不存在
    not_found_keywords = ["not found", "empty", "no data", "不存在", "无数据"]
    if any(kw in error_str for kw in not_found_keywords):
        return ErrorType.NOT_FOUND

    # 参数错误
    if any(kw in error_str for kw in ["invalid", "参数", "format"]):
        return ErrorType.INVALID

    return ErrorType.UNKNOWN


# ============================================================================
# 重试配置
# ============================================================================

@dataclass
class RetryConfig:
    """重试配置"""
    max_retries: int = 5
    base_delay: float = 1.0
    max_delay: float = 60.0
    exponential_base: float = 2.0
    jitter: bool = True

    # 不同错误类型的最大重试次数
    error_max_retries: Dict[ErrorType, int] = field(default_factory=lambda: {
        ErrorType.TRANSIENT: 5,
        ErrorType.RATE_LIMIT: 10,
        ErrorType.LOCK_CONFLICT: 8,
        ErrorType.NOT_FOUND: 0,
        ErrorType.INVALID: 0,
        ErrorType.UNKNOWN: 3,
    })

    # 不同错误类型的基础延迟
    error_base_delay: Dict[ErrorType, float] = field(default_factory=lambda: {
        ErrorType.TRANSIENT: 2.0,
        ErrorType.RATE_LIMIT: 5.0,
        ErrorType.LOCK_CONFLICT: 0.5,
        ErrorType.NOT_FOUND: 0,
        ErrorType.INVALID: 0,
        ErrorType.UNKNOWN: 1.0,
    })


def calculate_delay(
    attempt: int,
    error_type: ErrorType,
    config: RetryConfig
) -> float:
    """计算重试延迟"""
    if error_type in [ErrorType.NOT_FOUND, ErrorType.INVALID]:
        return 0

    base = config.error_base_delay.get(error_type, config.base_delay)

    # 指数退避
    delay = base * (config.exponential_base ** attempt)
    delay = min(delay, config.max_delay)

    # 添加抖动
    if config.jitter:
        delay = delay * (0.5 + random.random() * 0.5)

    return delay


# ============================================================================
# 文件队列 (进程安全)
# ============================================================================

@dataclass
class CacheTask:
    """缓存任务"""
    task_id: str
    symbol: str
    start: str
    end: str
    adjust: str = "qfq"
    priority: int = 0
    created_at: str = ""

    def __post_init__(self):
        if not self.task_id:
            self.task_id = f"{self.symbol}_{int(time.time_ns())}"
        if not self.created_at:
            self.created_at = datetime.now().isoformat()


class FileQueue:
    """基于文件的进程安全任务队列"""

    def __init__(self, queue_dir: str = "data/queue"):
        self.queue_dir = Path(queue_dir)
        self.pending_dir = self.queue_dir / "pending"
        self.processing_dir = self.queue_dir / "processing"
        self.completed_dir = self.queue_dir / "completed"
        self.failed_dir = self.queue_dir / "failed"

        for d in [self.pending_dir, self.processing_dir,
                  self.completed_dir, self.failed_dir]:
            d.mkdir(parents=True, exist_ok=True)

        self._lock = threading.Lock()

    def push(self, task: CacheTask) -> str:
        """添加任务到队列"""
        task_file = self.pending_dir / f"{task.task_id}.json"
        with open(task_file, 'w') as f:
            json.dump(asdict(task), f)
        return task.task_id

    def push_batch(self, tasks: List[CacheTask]) -> int:
        """批量添加任务"""
        count = 0
        for task in tasks:
            self.push(task)
            count += 1
        return count

    def pop(self) -> Optional[CacheTask]:
        """获取下一个任务 (进程安全)"""
        with self._lock:
            # 按优先级和创建时间排序
            files = sorted(
                self.pending_dir.glob("*.json"),
                key=lambda f: f.stat().st_mtime
            )

            for task_file in files:
                try:
                    # 原子性移动到处理中
                    processing_file = self.processing_dir / task_file.name
                    task_file.rename(processing_file)

                    with open(processing_file) as f:
                        data = json.load(f)
                    return CacheTask(**data)
                except FileExistsError:
                    continue  # 已被其他进程处理
                except Exception as e:
                    logger.error(f"读取任务失败: {e}")
                    continue

            return None

    def complete(self, task: CacheTask):
        """标记任务完成"""
        src = self.processing_dir / f"{task.task_id}.json"
        dst = self.completed_dir / f"{task.task_id}.json"
        if src.exists():
            src.rename(dst)

    def fail(self, task: CacheTask, error: str):
        """标记任务失败"""
        src = self.processing_dir / f"{task.task_id}.json"
        dst = self.failed_dir / f"{task.task_id}.json"

        if src.exists():
            # 读取原始任务
            with open(src) as f:
                data = json.load(f)

            # 添加错误信息
            data["error"] = error
            data["failed_at"] = datetime.now().isoformat()

            # 写入失败目录
            with open(dst, 'w') as f:
                json.dump(data, f)

            src.unlink()

    def get_stats(self) -> Dict:
        """获取队列统计"""
        return {
            "pending": len(list(self.pending_dir.glob("*.json"))),
            "processing": len(list(self.processing_dir.glob("*.json"))),
            "completed": len(list(self.completed_dir.glob("*.json"))),
            "failed": len(list(self.failed_dir.glob("*.json"))),
        }

    def get_failed_tasks(self) -> List[Dict]:
        """获取失败任务列表"""
        failed = []
        for f in self.failed_dir.glob("*.json"):
            with open(f) as fp:
                failed.append(json.load(fp))
        return failed

    def retry_failed(self) -> int:
        """重试所有失败任务"""
        count = 0
        for f in self.failed_dir.glob("*.json"):
            with open(f) as fp:
                data = json.load(fp)

            # 移除错误信息
            data.pop("error", None)
            data.pop("failed_at", None)

            # 创建新任务
            task = CacheTask(**data)
            self.push(task)
            f.unlink()
            count += 1

        return count


# ============================================================================
# 数据源管理
# ============================================================================

@dataclass
class SourceStatus:
    """数据源状态"""
    name: str
    available: bool = True
    error_count: int = 0
    last_error: str = ""
    last_success: datetime = None
    avg_latency: float = 0.0
    latency_samples: List[float] = field(default_factory=list)


class DataSourceManager:
    """数据源管理器"""

    _instance = None
    _lock = threading.Lock()

    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
                    cls._instance._sources: Dict[str, SourceStatus] = {}
        return cls._instance

    def get_status(self, source: str) -> SourceStatus:
        if source not in self._sources:
            self._sources[source] = SourceStatus(name=source)
        return self._sources[source]

    def record_success(self, source: str, latency: float):
        status = self.get_status(source)
        status.available = True
        status.error_count = 0
        status.last_success = datetime.now()

        status.latency_samples.append(latency)
        if len(status.latency_samples) > 10:
            status.latency_samples.pop(0)
        status.avg_latency = sum(status.latency_samples) / len(status.latency_samples)

    def record_error(self, source: str, error: str):
        status = self.get_status(source)
        status.error_count += 1
        status.last_error = error

        # 连续5次错误则临时禁用
        if status.error_count >= 5:
            status.available = False
            logger.warning(f"数据源 {source} 临时禁用: {error}")

    def should_use(self, source: str) -> bool:
        status = self.get_status(source)

        if not status.available:
            # 检查是否应该恢复 (5分钟后)
            if status.last_success:
                elapsed = datetime.now() - status.last_success
                if elapsed > timedelta(minutes=5):
                    status.available = True
                    status.error_count = 0
                    logger.info(f"数据源 {source} 恢复")

        return status.available

    def get_best_source(self, sources: List[str]) -> Optional[str]:
        """获取最佳数据源"""
        available = [s for s in sources if self.should_use(s)]
        if not available:
            return None
        return min(available, key=lambda s: self.get_status(s).avg_latency or 999)


# ============================================================================
# 增强版缓存器
# ============================================================================

class EnhancedCacheManager:
    """增强版缓存管理器"""

    DEFAULT_SOURCES = ["sina", "east_money", "baostock"]

    def __init__(
        self,
        queue_dir: str = "data/queue",
        retry_config: RetryConfig = None,
    ):
        self.queue = FileQueue(queue_dir)
        self.source_manager = DataSourceManager()
        self.retry_config = retry_config or RetryConfig()

        # 导入数据获取函数
        from jk2bt.utils.data_source_backup import (
            fetch_stock_daily_sina,
            fetch_stock_daily_eastmoney,
            fetch_stock_daily_baostock,
        )
        from jk2bt.db.duckdb_manager import DuckDBManager

        self.fetchers = {
            "sina": fetch_stock_daily_sina,
            "east_money": fetch_stock_daily_eastmoney,
            "baostock": fetch_stock_daily_baostock,
        }
        self.db = DuckDBManager

    def fetch_with_retry(
        self,
        symbol: str,
        start: str,
        end: str,
        adjust: str = "qfq",
        sources: List[str] = None,
    ) -> Optional[Any]:
        """带智能重试的数据获取"""
        sources = sources or self.DEFAULT_SOURCES
        last_error = None

        for source in sources:
            if not self.source_manager.should_use(source):
                continue

            fetcher = self.fetchers.get(source)
            if not fetcher:
                continue

            # 获取该数据源的最大重试次数
            error_type = ErrorType.UNKNOWN

            for attempt in range(self.retry_config.max_retries):
                try:
                    start_time = time.time()
                    df = fetcher(symbol, start, end, adjust)

                    if df is not None and not df.empty:
                        latency = time.time() - start_time
                        self.source_manager.record_success(source, latency)
                        return df

                    # 空数据，尝试下一个源
                    break

                except Exception as e:
                    last_error = e
                    error_type = classify_error(e)

                    # 检查是否应该重试
                    max_retries = self.retry_config.error_max_retries.get(error_type, 0)
                    if attempt >= max_retries:
                        self.source_manager.record_error(source, str(e))
                        break

                    # 计算延迟并等待
                    delay = calculate_delay(attempt, error_type, self.retry_config)
                    if delay > 0:
                        logger.debug(f"[{source}] 重试 {attempt+1}/{max_retries}, 等待 {delay:.1f}s")
                        time.sleep(delay)

        raise last_error or Exception("所有数据源失败")

    def process_task(self, task: CacheTask) -> bool:
        """处理单个任务"""
        logger.info(f"处理: {task.symbol} ({task.start} ~ {task.end})")

        try:
            # 检查缓存是否已存在
            db = self.db()
            if db.has_data("stock_daily", task.symbol, task.start, task.end, task.adjust):
                existing = db.get_stock_daily(task.symbol, task.start, task.end, task.adjust)
                if len(existing) > 800:
                    logger.info(f"  已缓存: {len(existing)} 行，跳过")
                    self.queue.complete(task)
                    return True

            # 获取数据
            df = self.fetch_with_retry(
                task.symbol, task.start, task.end, task.adjust
            )

            if df is not None and not df.empty:
                # 写入数据库 (带重试)
                for attempt in range(3):
                    try:
                        db.insert_stock_daily(task.symbol, df, task.adjust)
                        break
                    except Exception as e:
                        if "lock" in str(e).lower():
                            time.sleep(random.uniform(0.5, 2))
                        else:
                            raise

                logger.info(f"  成功: {len(df)} 行")
                self.queue.complete(task)
                return True
            else:
                logger.warning(f"  失败: 无数据")
                self.queue.fail(task, "无数据")
                return False

        except Exception as e:
            error_type = classify_error(e)
            logger.error(f"  失败 [{error_type.value}]: {str(e)[:50]}")
            self.queue.fail(task, str(e)[:200])
            return False

    def run_worker(
        self,
        max_tasks: int = None,
        idle_timeout: int = 60,
    ):
        """运行工作进程"""
        logger.info("缓存工作进程启动")
        processed = 0
        idle_time = 0

        while True:
            task = self.queue.pop()

            if task is None:
                idle_time += 1
                if idle_time >= idle_timeout:
                    logger.info("无任务，退出")
                    break
                time.sleep(1)
                continue

            idle_time = 0
            self.process_task(task)
            processed += 1

            if max_tasks and processed >= max_tasks:
                logger.info(f"达到最大任务数 {max_tasks}，退出")
                break

            # 请求间隔
            time.sleep(random.uniform(0.3, 0.8))

        return processed

    def add_stocks_batch(
        self,
        symbols: List[str],
        start: str,
        end: str,
        adjust: str = "qfq",
        priority: int = 0,
    ):
        """批量添加股票缓存任务"""
        tasks = [
            CacheTask(
                task_id=f"{sym}_{int(time.time_ns())}",
                symbol=sym,
                start=start,
                end=end,
                adjust=adjust,
                priority=priority,
            )
            for sym in symbols
        ]

        count = self.queue.push_batch(tasks)
        logger.info(f"添加 {count} 个缓存任务")
        return count


# ============================================================================
# CLI 接口
# ============================================================================

def main():
    import argparse

    parser = argparse.ArgumentParser(description="增强版缓存管理器")
    parser.add_argument("--worker", action="store_true", help="启动工作进程")
    parser.add_argument("--add-hs300", action="store_true", help="添加HS300成分股任务")
    parser.add_argument("--add-zz500", action="store_true", help="添加ZZ500成分股任务")
    parser.add_argument("--add-stocks", nargs="+", help="添加指定股票任务")
    parser.add_argument("--start", default="2020-01-01", help="开始日期")
    parser.add_argument("--end", default="2023-12-31", help="结束日期")
    parser.add_argument("--max-tasks", type=int, default=None, help="最大处理任务数")
    parser.add_argument("--retry-failed", action="store_true", help="重试失败任务")
    parser.add_argument("--stats", action="store_true", help="显示队列统计")

    args = parser.parse_args()

    manager = EnhancedCacheManager()

    if args.stats:
        stats = manager.queue.get_stats()
        print(f"队列统计: {stats}")
        return

    if args.retry_failed:
        count = manager.queue.retry_failed()
        print(f"重试 {count} 个失败任务")
        return

    if args.add_hs300:
        from jk2bt.core.strategy_base import get_index_stocks
        stocks = get_index_stocks('000300.XSHG')
        # 转换代码格式
        symbols = []
        for s in stocks:
            if s.endswith('.XSHG'):
                symbols.append('sh' + s[:6])
            else:
                symbols.append('sz' + s[:6])
        manager.add_stocks_batch(symbols, args.start, args.end)

    if args.add_zz500:
        from jk2bt.core.strategy_base import get_index_stocks
        stocks = get_index_stocks('000905.XSHG')
        symbols = []
        for s in stocks:
            if s.endswith('.XSHG'):
                symbols.append('sh' + s[:6])
            else:
                symbols.append('sz' + s[:6])
        manager.add_stocks_batch(symbols, args.start, args.end)

    if args.add_stocks:
        manager.add_stocks_batch(args.add_stocks, args.start, args.end)

    if args.worker:
        manager.run_worker(max_tasks=args.max_tasks)


if __name__ == "__main__":
    main()