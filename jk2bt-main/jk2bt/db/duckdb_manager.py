"""
db/duckdb_manager.py
DuckDB 数据库管理器，用于存储和查询股票、ETF、指数的日线行情数据。

并发优化 (P2-7 DuckDB并发治理):
1. 单例模式：每个进程只创建一个管理器实例，避免重复初始化
2. 进程级初始化锁：使用文件锁确保表结构初始化只执行一次
3. 延迟初始化：表结构初始化延迟到首次操作，减少启动冲突
4. 读写分离工厂：明确区分只读和写入场景
5. 静默降级：锁冲突时静默重试，不产生噪音日志
6. 本地缓存分层：对高频查询添加进程内内存缓存
7. 写入重试机制：处理并发写入的锁冲突，指数退避
"""

import os
import logging
import time
import threading
import hashlib
from typing import Optional, List, Tuple, Dict, Any
from contextlib import contextmanager
from functools import lru_cache
import pandas as pd
from collections import defaultdict

try:
    import duckdb
except ImportError:
    raise ImportError("请安装 duckdb: pip install duckdb")

# 导入统一的代码转换工具
from jk2bt.utils.code_converter import normalize_to_jq_format

logger = logging.getLogger(__name__)

# 进程级单例管理器缓存
_PROCESS_SINGLETONS: Dict[str, "DuckDBManager"] = {}
_SINGLETON_LOCK = threading.Lock()

# 进程级初始化完成标记（避免重复初始化）
_DB_INITIALIZED_FLAGS: Dict[str, bool] = {}


class LocalCache:
    """本地内存缓存层，减少数据库访问"""

    def __init__(self, max_size: int = 1000):
        self._cache: Dict[str, pd.DataFrame] = {}
        self._timestamps: Dict[str, float] = {}
        self._lock = threading.Lock()
        self._max_size = max_size

    def _make_key(self, table: str, symbol: str, start: str, end: str, **kwargs) -> str:
        params = "&".join(f"{k}={v}" for k, v in kwargs.items())
        return f"{table}:{symbol}:{start}:{end}:{params}"

    def get(
        self, table: str, symbol: str, start: str, end: str, **kwargs
    ) -> Optional[pd.DataFrame]:
        key = self._make_key(table, symbol, start, end, **kwargs)
        with self._lock:
            if key in self._cache:
                return self._cache[key].copy()
        return None

    def set(
        self, table: str, symbol: str, start: str, end: str, df: pd.DataFrame, **kwargs
    ):
        key = self._make_key(table, symbol, start, end, **kwargs)
        with self._lock:
            if len(self._cache) >= self._max_size:
                oldest_key = min(self._timestamps, key=self._timestamps.get)
                self._cache.pop(oldest_key, None)
                self._timestamps.pop(oldest_key, None)
            self._cache[key] = df.copy()
            self._timestamps[key] = time.time()

    def invalidate(self, table: str = None, symbol: str = None):
        with self._lock:
            if table is None and symbol is None:
                self._cache.clear()
                self._timestamps.clear()
            else:
                keys_to_remove = []
                for key in self._cache:
                    if table and table not in key:
                        continue
                    if symbol and symbol not in key:
                        continue
                    keys_to_remove.append(key)
                for key in keys_to_remove:
                    self._cache.pop(key, None)
                    self._timestamps.pop(key, None)

    def clear(self):
        with self._lock:
            self._cache.clear()
            self._timestamps.clear()


_global_cache = LocalCache()


class DuckDBManager:
    """DuckDB 数据库管理器（支持多进程并发只读访问，优化写入冲突）

    并发治理改进 (P2-7):
    - 使用工厂函数获取实例，避免直接构造
    - 延迟初始化表结构，减少启动时锁冲突
    - 静默重试模式，减少噪音日志
    """

    _WRITE_RETRY_COUNT = 5  # 增加重试次数
    _WRITE_RETRY_DELAY_BASE = 0.3  # 基础延迟，指数退避
    _MAX_CONNECTION_RETRY = 5
    _SILENT_RETRY = True  # 静默重试模式，不产生噪音日志

    def __init__(
        self, db_path: str = None, read_only: bool = False, use_cache: bool = True,
        _delay_init: bool = False  # 内部参数：延迟初始化
    ):
        """
        初始化数据库连接

        参数:
            db_path: 数据库路径
            read_only: 是否只读模式（并发安全，默认False）
            use_cache: 是否使用本地缓存（默认True）
            _delay_init: 延迟初始化表结构（内部使用）

        注意:
            推荐使用工厂函数获取实例:
            - get_shared_read_only_manager() 用于多进程读取
            - get_writer_manager() 用于单进程写入
        """
        if db_path is None:
            # 从统一配置获取默认数据库路径
            try:
                from jk2bt.utils.config import get_config
                config = get_config()
                db_path = config.cache.duckdb_path
            except Exception:
                # fallback 到原有逻辑（向后兼容）
                base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
                project_root = os.path.dirname(base_dir)
                db_path = os.path.join(project_root, "data", "market.db")

        self.db_path = db_path
        self.read_only = read_only
        self.use_cache = use_cache
        self._tables_initialized = False
        self._connection_pool: Dict[int, Any] = {}
        self._pool_lock = threading.Lock()
        self._init_lock = threading.Lock()  # 初始化锁

        # 确保目录存在
        db_dir = os.path.dirname(db_path)
        if db_dir and not os.path.exists(db_dir):
            try:
                os.makedirs(db_dir, exist_ok=True)
            except Exception:
                pass  # 多进程创建目录时可能冲突，忽略

        # 延迟初始化：减少启动时锁冲突
        if not _delay_init and not read_only:
            self._init_database_safe()
        elif read_only:
            # 只读模式不需要初始化，只记录
            logger.debug(f"DuckDB 只读模式: {db_path}")

    def _create_connection(self, read_only: bool = None) -> Any:
        """创建新的独立连接（静默重试模式）"""
        if read_only is None:
            read_only = self.read_only

        for attempt in range(self._MAX_CONNECTION_RETRY):
            try:
                conn = duckdb.connect(self.db_path, read_only=read_only)
                return conn
            except Exception as e:
                error_lower = str(e).lower()

                # DuckDB 在同一进程内可能拒绝"同库不同配置"的连接（如先写后只读）。
                # 此时降级为读写连接，保证并发读线程可继续工作。
                if read_only and "different configuration" in error_lower:
                    # 静默降级，不产生噪音
                    try:
                        return duckdb.connect(self.db_path, read_only=False)
                    except Exception:
                        pass  # 继续重试

                if "lock" in error_lower or "conflict" in error_lower or "busy" in error_lower:
                    # 静默重试，指数退避
                    delay = self._WRITE_RETRY_DELAY_BASE * (1.5 ** attempt)
                    time.sleep(delay)
                else:
                    raise

        raise RuntimeError(f"无法创建数据库连接: {self.db_path}")

    @contextmanager
    def _get_connection(self, read_only=None):
        """获取独立数据库连接（上下文管理器）

        参数:
            read_only: 是否以只读模式打开，默认使用实例的read_only设置
        """
        if read_only is None:
            read_only = self.read_only

        conn = None
        try:
            conn = self._create_connection(read_only=read_only)
            yield conn
        except Exception as e:
            # 只在最终失败时记录错误，减少噪音
            if not self._SILENT_RETRY:
                logger.error(f"数据库连接错误: {e}")
            raise
        finally:
            if conn:
                try:
                    conn.close()
                except Exception:
                    pass

    def _retry_write(self, func, *args, **kwargs):
        """写入操作重试机制（静默模式，指数退避）"""
        last_error = None
        for attempt in range(self._WRITE_RETRY_COUNT):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                last_error = e
                error_str = str(e).lower()
                if (
                    "lock" in error_str
                    or "conflict" in error_str
                    or "timeout" in error_str
                    or "busy" in error_str
                ):
                    # 静默重试，指数退避
                    delay = self._WRITE_RETRY_DELAY_BASE * (1.5 ** attempt)
                    time.sleep(delay)
                else:
                    raise

        # 只在最终失败时记录一次警告
        logger.warning(f"写入重试 {self._WRITE_RETRY_COUNT} 次后仍失败: {last_error}")
        raise last_error

    def _init_database_safe(self):
        """安全的数据库初始化（带文件锁，避免多进程冲突）"""
        with self._init_lock:
            if self._tables_initialized:
                return

            # 检查进程级全局标记
            global _DB_INITIALIZED_FLAGS
            if _DB_INITIALIZED_FLAGS.get(self.db_path, False):
                self._tables_initialized = True
                return

            # 使用文件锁确保只有一个进程执行初始化
            lock_file = self._get_init_lock_file()
            lock_fd = None
            try:
                # 尝试创建并锁定文件
                lock_fd = open(lock_file, 'w')
                # 非阻塞尝试获取锁
                import fcntl
                try:
                    fcntl.flock(lock_fd.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
                    # 成功获取锁，执行初始化
                    self._init_database()
                    _DB_INITIALIZED_FLAGS[self.db_path] = True
                except (IOError, OSError):
                    # 其他进程持有锁，等待并跳过初始化
                    time.sleep(0.5)
                    self._tables_initialized = True
                    _DB_INITIALIZED_FLAGS[self.db_path] = True
                    logger.debug(f"数据库初始化由其他进程完成: {self.db_path}")
            except Exception as e:
                # 文件锁不可用时，使用静默重试策略
                logger.debug(f"文件锁不可用，静默初始化: {e}")
                self._init_database()
            finally:
                if lock_fd:
                    try:
                        import fcntl
                        fcntl.flock(lock_fd.fileno(), fcntl.LOCK_UN)
                        lock_fd.close()
                    except Exception:
                        pass

    def _get_init_lock_file(self) -> str:
        """获取初始化锁文件路径"""
        # 使用数据库路径的hash作为锁文件名
        db_hash = hashlib.md5(self.db_path.encode()).hexdigest()[:8]
        lock_dir = os.path.dirname(self.db_path) or "/tmp"
        return os.path.join(lock_dir, f".duckdb_init_{db_hash}.lock")

    def _init_database(self):
        """初始化数据库表结构（仅在写模式下执行）"""
        if self._tables_initialized:
            return

        try:
            with self._get_connection(read_only=False) as conn:
                conn.execute("""
                    CREATE TABLE IF NOT EXISTS stock_daily (
                        symbol VARCHAR NOT NULL,
                        datetime DATE NOT NULL,
                        open DOUBLE,
                        high DOUBLE,
                        low DOUBLE,
                        close DOUBLE,
                        volume BIGINT,
                        amount DOUBLE,
                        adjust VARCHAR DEFAULT 'qfq',
                        PRIMARY KEY (symbol, datetime, adjust)
                    )
                """)

                conn.execute("""
                    CREATE TABLE IF NOT EXISTS etf_daily (
                        symbol VARCHAR NOT NULL,
                        datetime DATE NOT NULL,
                        open DOUBLE,
                        high DOUBLE,
                        low DOUBLE,
                        close DOUBLE,
                        volume BIGINT,
                        amount DOUBLE,
                        PRIMARY KEY (symbol, datetime)
                    )
                """)

                conn.execute("""
                    CREATE TABLE IF NOT EXISTS lof_daily (
                        symbol VARCHAR NOT NULL,
                        datetime DATE NOT NULL,
                        open DOUBLE,
                        high DOUBLE,
                        low DOUBLE,
                        close DOUBLE,
                        volume BIGINT,
                        amount DOUBLE,
                        PRIMARY KEY (symbol, datetime)
                    )
                """)

                conn.execute("""
                    CREATE TABLE IF NOT EXISTS index_daily (
                        symbol VARCHAR NOT NULL,
                        datetime DATE NOT NULL,
                        open DOUBLE,
                        high DOUBLE,
                        low DOUBLE,
                        close DOUBLE,
                        volume BIGINT,
                        amount DOUBLE,
                        PRIMARY KEY (symbol, datetime)
                    )
                """)

                conn.execute("""
                    CREATE TABLE IF NOT EXISTS stock_minute (
                        symbol VARCHAR NOT NULL,
                        datetime TIMESTAMP NOT NULL,
                        period VARCHAR NOT NULL,
                        open DOUBLE,
                        high DOUBLE,
                        low DOUBLE,
                        close DOUBLE,
                        volume BIGINT,
                        money DOUBLE,
                        adjust VARCHAR DEFAULT 'qfq',
                        PRIMARY KEY (symbol, datetime, period, adjust)
                    )
                """)

                conn.execute("""
                    CREATE TABLE IF NOT EXISTS etf_minute (
                        symbol VARCHAR NOT NULL,
                        datetime TIMESTAMP NOT NULL,
                        period VARCHAR NOT NULL,
                        open DOUBLE,
                        high DOUBLE,
                        low DOUBLE,
                        close DOUBLE,
                        volume BIGINT,
                        money DOUBLE,
                        PRIMARY KEY (symbol, datetime, period)
                    )
                """)

                conn.execute(
                    "CREATE INDEX IF NOT EXISTS idx_stock_symbol ON stock_daily(symbol)"
                )
                conn.execute(
                    "CREATE INDEX IF NOT EXISTS idx_stock_date ON stock_daily(datetime)"
                )
                conn.execute(
                    "CREATE INDEX IF NOT EXISTS idx_etf_symbol ON etf_daily(symbol)"
                )
                conn.execute(
                    "CREATE INDEX IF NOT EXISTS idx_etf_date ON etf_daily(datetime)"
                )
                conn.execute(
                    "CREATE INDEX IF NOT EXISTS idx_lof_symbol ON lof_daily(symbol)"
                )
                conn.execute(
                    "CREATE INDEX IF NOT EXISTS idx_lof_date ON lof_daily(datetime)"
                )
                conn.execute(
                    "CREATE INDEX IF NOT EXISTS idx_index_symbol ON index_daily(symbol)"
                )
                conn.execute(
                    "CREATE INDEX IF NOT EXISTS idx_index_date ON index_daily(datetime)"
                )
                conn.execute(
                    "CREATE INDEX IF NOT EXISTS idx_stock_minute_symbol ON stock_minute(symbol)"
                )
                conn.execute(
                    "CREATE INDEX IF NOT EXISTS idx_stock_minute_datetime ON stock_minute(datetime)"
                )
                conn.execute(
                    "CREATE INDEX IF NOT EXISTS idx_stock_minute_period ON stock_minute(period)"
                )
                conn.execute(
                    "CREATE INDEX IF NOT EXISTS idx_etf_minute_symbol ON etf_minute(symbol)"
                )
                conn.execute(
                    "CREATE INDEX IF NOT EXISTS idx_etf_minute_datetime ON etf_minute(datetime)"
                )
                conn.execute(
                    "CREATE INDEX IF NOT EXISTS idx_etf_minute_period ON etf_minute(period)"
                )

                self._tables_initialized = True
                # 静默完成，减少噪音
                logger.debug("数据库表结构初始化完成")
        except Exception as e:
            # 静默处理，假设其他进程已初始化
            error_lower = str(e).lower()
            if "lock" in error_lower or "conflict" in error_lower:
                logger.debug("数据库初始化跳过（其他进程正在操作）")
            else:
                logger.debug(f"初始化表结构跳过: {e}")
            self._tables_initialized = True

    def insert_stock_daily(self, symbol: str, df: pd.DataFrame, adjust: str = "qfq"):
        """
        插入股票日线数据，自动去重。

        参数
        ----
        symbol : str
            股票代码，支持多种格式：'sh600000'、'sz000001'、'600000.XSHG'、'000001.XSHE'、'600000'
            内部统一转换为聚宽格式存储
        df : pd.DataFrame
            日线数据，必须包含 datetime/open/high/low/close/volume 列
        adjust : str
            复权类型：qfq/hfq/none
        """
        if df is None or df.empty:
            logger.warning(f"{symbol}: 无数据需要插入")
            return

        # 统一转换为聚宽格式存储
        jq_symbol = normalize_to_jq_format(symbol)

        df = df.copy()
        df["symbol"] = jq_symbol  # 使用统一格式存储
        df["adjust"] = adjust

        if "datetime" not in df.columns:
            raise ValueError(f"{symbol}: DataFrame 必须包含 'datetime' 列")

        if "amount" not in df.columns:
            df["amount"] = 0

        cols = [
            "symbol",
            "datetime",
            "open",
            "high",
            "low",
            "close",
            "volume",
            "amount",
            "adjust",
        ]
        df = df[[col for col in cols if col in df.columns]]

        def _do_insert():
            with self._get_connection() as conn:
                count_before = conn.execute(
                    "SELECT COUNT(*) FROM stock_daily WHERE symbol=? AND adjust=?",
                    [jq_symbol, adjust],
                ).fetchone()[0]

                conn.execute("""
                    INSERT OR REPLACE INTO stock_daily
                    (symbol, datetime, open, high, low, close, volume, amount, adjust)
                    SELECT symbol, datetime, open, high, low, close, volume, amount, adjust
                    FROM df
                """)

                count_after = conn.execute(
                    "SELECT COUNT(*) FROM stock_daily WHERE symbol=? AND adjust=?",
                    [jq_symbol, adjust],
                ).fetchone()[0]

                logger.info(
                    f"{jq_symbol} ({adjust}): 插入/更新 {len(df)} 条数据，总记录数 {count_after}"
                )

                if self.use_cache:
                    _global_cache.invalidate(table="stock_daily", symbol=jq_symbol)

        self._retry_write(_do_insert)

    def insert_etf_daily(self, symbol: str, df: pd.DataFrame):
        """插入 ETF 日线数据。

        参数:
            symbol: ETF代码，支持多种格式，内部统一转换为聚宽格式存储
            df: 日线数据
        """
        if df is None or df.empty:
            logger.warning(f"{symbol}: 无数据需要插入")
            return

        # 统一转换为聚宽格式存储
        jq_symbol = normalize_to_jq_format(symbol)

        df = df.copy()
        df["symbol"] = jq_symbol  # 使用统一格式存储

        if "datetime" not in df.columns:
            raise ValueError(f"{symbol}: DataFrame 必须包含 'datetime' 列")

        if "amount" not in df.columns:
            df["amount"] = 0

        cols = [
            "symbol",
            "datetime",
            "open",
            "high",
            "low",
            "close",
            "volume",
            "amount",
        ]
        df = df[[col for col in cols if col in df.columns]]

        def _do_insert():
            with self._get_connection() as conn:
                count_before = conn.execute(
                    "SELECT COUNT(*) FROM etf_daily WHERE symbol=?", [jq_symbol]
                ).fetchone()[0]

                conn.execute("""
                    INSERT OR REPLACE INTO etf_daily
                    (symbol, datetime, open, high, low, close, volume, amount)
                    SELECT symbol, datetime, open, high, low, close, volume, amount
                    FROM df
                """)

                count_after = conn.execute(
                    "SELECT COUNT(*) FROM etf_daily WHERE symbol=?", [jq_symbol]
                ).fetchone()[0]

                logger.info(
                    f"{jq_symbol}: 插入/更新 {len(df)} 条数据，总记录数 {count_after}"
                )

                if self.use_cache:
                    _global_cache.invalidate(table="etf_daily", symbol=jq_symbol)

        self._retry_write(_do_insert)

    def insert_lof_daily(self, symbol: str, df: pd.DataFrame):
        """插入 LOF 日线数据。

        参数:
            symbol: LOF代码，支持多种格式，内部统一转换为聚宽格式存储
            df: 日线数据
        """
        if df is None or df.empty:
            logger.warning(f"{symbol}: 无数据需要插入")
            return

        # 统一转换为聚宽格式存储
        jq_symbol = normalize_to_jq_format(symbol)

        df = df.copy()
        df["symbol"] = jq_symbol  # 使用统一格式存储

        if "datetime" not in df.columns:
            raise ValueError(f"{symbol}: DataFrame 必须包含 'datetime' 列")

        if "amount" not in df.columns:
            df["amount"] = 0

        cols = [
            "symbol",
            "datetime",
            "open",
            "high",
            "low",
            "close",
            "volume",
            "amount",
        ]
        df = df[[col for col in cols if col in df.columns]]

        def _do_insert():
            with self._get_connection() as conn:
                count_before = conn.execute(
                    "SELECT COUNT(*) FROM lof_daily WHERE symbol=?", [jq_symbol]
                ).fetchone()[0]

                conn.execute("""
                    INSERT OR REPLACE INTO lof_daily
                    (symbol, datetime, open, high, low, close, volume, amount)
                    SELECT symbol, datetime, open, high, low, close, volume, amount
                    FROM df
                """)

                count_after = conn.execute(
                    "SELECT COUNT(*) FROM lof_daily WHERE symbol=?", [jq_symbol]
                ).fetchone()[0]

                logger.info(
                    f"{jq_symbol}: 插入/更新 {len(df)} 条数据，总记录数 {count_after}"
                )

                if self.use_cache:
                    _global_cache.invalidate(table="lof_daily", symbol=jq_symbol)

        self._retry_write(_do_insert)

    def insert_index_daily(self, symbol: str, df: pd.DataFrame):
        """插入指数日线数据。

        参数:
            symbol: 指数代码，支持多种格式，内部统一转换为聚宽格式存储
            df: 日线数据
        """
        if df is None or df.empty:
            logger.warning(f"{symbol}: 无数据需要插入")
            return

        # 统一转换为聚宽格式存储
        jq_symbol = normalize_to_jq_format(symbol)

        df = df.copy()
        df["symbol"] = jq_symbol  # 使用统一格式存储

        if "datetime" not in df.columns:
            raise ValueError(f"{symbol}: DataFrame 必须包含 'datetime' 列")

        if "amount" not in df.columns:
            df["amount"] = 0

        cols = [
            "symbol",
            "datetime",
            "open",
            "high",
            "low",
            "close",
            "volume",
            "amount",
        ]
        df = df[[col for col in cols if col in df.columns]]

        def _do_insert():
            with self._get_connection() as conn:
                count_before = conn.execute(
                    "SELECT COUNT(*) FROM index_daily WHERE symbol=?", [jq_symbol]
                ).fetchone()[0]

                conn.execute("""
                    INSERT OR REPLACE INTO index_daily
                    (symbol, datetime, open, high, low, close, volume, amount)
                    SELECT symbol, datetime, open, high, low, close, volume, amount
                    FROM df
                """)

                count_after = conn.execute(
                    "SELECT COUNT(*) FROM index_daily WHERE symbol=?", [jq_symbol]
                ).fetchone()[0]

                logger.info(
                    f"{jq_symbol}: 插入/更新 {len(df)} 条数据，总记录数 {count_after}"
                )

                if self.use_cache:
                    _global_cache.invalidate(table="index_daily", symbol=jq_symbol)

        self._retry_write(_do_insert)

    def get_stock_daily(
        self,
        symbol: str,
        start: str,
        end: str,
        adjust: str = "qfq",
        use_cache: bool = None,
    ) -> pd.DataFrame:
        """
        查询股票日线数据（支持缓存）。

        参数
        ----
        symbol : str
            股票代码，支持多种格式：'sh600000'、'sz000001'、'600000.XSHG'、'000001.XSHE'、'600000'
            内部统一转换为聚宽格式查询
        start : str
            起始日期 'YYYY-MM-DD'
        end : str
            结束日期 'YYYY-MM-DD'
        adjust : str
            复权类型：qfq/hfq/none
        use_cache : bool
            是否使用缓存，默认使用实例设置

        返回
        ----
        pd.DataFrame
            包含 datetime/open/high/low/close/volume/amount 列
        """
        if use_cache is None:
            use_cache = self.use_cache

        # 统一转换为聚宽格式查询
        jq_symbol = normalize_to_jq_format(symbol)

        if use_cache:
            cached = _global_cache.get("stock_daily", jq_symbol, start, end, adjust=adjust)
            if cached is not None:
                logger.debug(f"{jq_symbol} ({adjust}): 使用缓存数据")
                return cached

        with self._get_connection(read_only=True) as conn:
            df = conn.execute(
                """
                SELECT datetime, open, high, low, close, volume, amount
                FROM stock_daily
                WHERE symbol = ? AND adjust = ?
                  AND datetime >= ? AND datetime <= ?
                ORDER BY datetime
            """,
                [jq_symbol, adjust, start, end],
            ).fetchdf()

            if not df.empty:
                logger.info(
                    f"{jq_symbol} ({adjust}): 查询到 {len(df)} 条数据 ({start} ~ {end})"
                )
                if use_cache:
                    _global_cache.set("stock_daily", jq_symbol, start, end, df, adjust=adjust)
            else:
                logger.warning(f"{jq_symbol} ({adjust}): 数据库中无数据")

            return df

    # 旧的格式转换方法已移除，使用统一的 jk2bt.utils.code_converter.normalize_to_jq_format

    def get_etf_daily(
        self, symbol: str, start: str, end: str, use_cache: bool = None
    ) -> pd.DataFrame:
        """查询 ETF 日线数据（支持缓存）。

        参数:
            symbol: ETF代码，支持多种格式，内部统一转换为聚宽格式查询
        """
        if use_cache is None:
            use_cache = self.use_cache

        # 统一转换为聚宽格式查询
        jq_symbol = normalize_to_jq_format(symbol)

        if use_cache:
            cached = _global_cache.get("etf_daily", jq_symbol, start, end)
            if cached is not None:
                return cached

        with self._get_connection(read_only=True) as conn:
            df = conn.execute(
                """
                SELECT datetime, open, high, low, close, volume, amount
                FROM etf_daily
                WHERE symbol = ? AND datetime >= ? AND datetime <= ?
                ORDER BY datetime
            """,
                [jq_symbol, start, end],
            ).fetchdf()

            if df.empty:
                logger.warning(f"{jq_symbol}: 数据库中无数据")
            else:
                logger.info(f"{jq_symbol}: 查询到 {len(df)} 条数据 ({start} ~ {end})")

            if use_cache and not df.empty:
                _global_cache.set("etf_daily", jq_symbol, start, end, df)

            return df

    def get_lof_daily(
        self, symbol: str, start: str, end: str, use_cache: bool = None
    ) -> pd.DataFrame:
        """查询 LOF 日线数据（支持缓存）。

        参数:
            symbol: LOF代码，支持多种格式，内部统一转换为聚宽格式查询
        """
        if use_cache is None:
            use_cache = self.use_cache

        # 统一转换为聚宽格式查询
        jq_symbol = normalize_to_jq_format(symbol)

        if use_cache:
            cached = _global_cache.get("lof_daily", jq_symbol, start, end)
            if cached is not None:
                return cached

        with self._get_connection(read_only=True) as conn:
            df = conn.execute(
                """
                SELECT datetime, open, high, low, close, volume, amount
                FROM lof_daily
                WHERE symbol = ? AND datetime >= ? AND datetime <= ?
                ORDER BY datetime
            """,
                [jq_symbol, start, end],
            ).fetchdf()

            if df.empty:
                logger.warning(f"{jq_symbol}: 数据库中无数据")
            else:
                logger.info(f"{jq_symbol}: 查询到 {len(df)} 条数据 ({start} ~ {end})")

            if use_cache and not df.empty:
                _global_cache.set("lof_daily", jq_symbol, start, end, df)

            return df

    def get_index_daily(
        self, symbol: str, start: str, end: str, use_cache: bool = None
    ) -> pd.DataFrame:
        """查询指数日线数据（支持缓存）。

        参数:
            symbol: 指数代码，支持多种格式，内部统一转换为聚宽格式查询
        """
        if use_cache is None:
            use_cache = self.use_cache

        # 统一转换为聚宽格式查询
        jq_symbol = normalize_to_jq_format(symbol)

        if use_cache:
            cached = _global_cache.get("index_daily", jq_symbol, start, end)
            if cached is not None:
                return cached

        with self._get_connection(read_only=True) as conn:
            df = conn.execute(
                """
                SELECT datetime, open, high, low, close, volume, amount
                FROM index_daily
                WHERE symbol = ? AND datetime >= ? AND datetime <= ?
                ORDER BY datetime
            """,
                [jq_symbol, start, end],
            ).fetchdf()

            if df.empty:
                logger.warning(f"{jq_symbol}: 数据库中无数据")
            else:
                logger.info(f"{jq_symbol}: 查询到 {len(df)} 条数据 ({start} ~ {end})")

            if use_cache and not df.empty:
                _global_cache.set("index_daily", jq_symbol, start, end, df)

            return df

    def insert_stock_minute(
        self, symbol: str, period: str, df: pd.DataFrame, adjust: str = "qfq"
    ):
        """
        插入股票分钟数据，自动去重。

        参数
        ----
        symbol : str
            股票代码，支持多种格式，内部统一转换为聚宽格式存储
        period : str
            周期：1/5/15/30/60
        df : pd.DataFrame
            分钟数据，必须包含 datetime/open/high/low/close/volume/money 列
        adjust : str
            复权类型：qfq/hfq/none
        """
        if df is None or df.empty:
            logger.warning(f"{symbol} ({period}): 无数据需要插入")
            return

        # 统一转换为聚宽格式存储
        jq_symbol = normalize_to_jq_format(symbol)

        df = df.copy()
        df["symbol"] = jq_symbol  # 使用统一格式存储
        df["period"] = period
        df["adjust"] = adjust

        if "datetime" not in df.columns:
            raise ValueError(f"{symbol}: DataFrame 必须包含 'datetime' 列")

        if "money" not in df.columns:
            df["money"] = df.get("amount", 0)

        cols = [
            "symbol",
            "datetime",
            "period",
            "open",
            "high",
            "low",
            "close",
            "volume",
            "money",
            "adjust",
        ]
        df = df[[col for col in cols if col in df.columns]]

        def _do_insert():
            with self._get_connection() as conn:
                conn.execute("""
                    INSERT OR REPLACE INTO stock_minute
                    (symbol, datetime, period, open, high, low, close, volume, money, adjust)
                    SELECT symbol, datetime, period, open, high, low, close, volume, money, adjust
                    FROM df
                """)

                logger.info(
                    f"{jq_symbol} ({period} {adjust}): 插入/更新 {len(df)} 条分钟数据"
                )

                if self.use_cache:
                    _global_cache.invalidate(table="stock_minute", symbol=jq_symbol)

        self._retry_write(_do_insert)

    def insert_etf_minute(self, symbol: str, period: str, df: pd.DataFrame):
        """插入 ETF 分钟数据。

        参数:
            symbol: ETF代码，支持多种格式，内部统一转换为聚宽格式存储
            period: 周期
            df: 分钟数据
        """
        if df is None or df.empty:
            logger.warning(f"{symbol} ({period}): 无数据需要插入")
            return

        # 统一转换为聚宽格式存储
        jq_symbol = normalize_to_jq_format(symbol)

        df = df.copy()
        df["symbol"] = jq_symbol  # 使用统一格式存储
        df["period"] = period

        if "datetime" not in df.columns:
            raise ValueError(f"{symbol}: DataFrame 必须包含 'datetime' 列")

        if "money" not in df.columns:
            df["money"] = df.get("amount", 0)

        cols = [
            "symbol",
            "datetime",
            "period",
            "open",
            "high",
            "low",
            "close",
            "volume",
            "money",
        ]
        df = df[[col for col in cols if col in df.columns]]

        def _do_insert():
            with self._get_connection() as conn:
                conn.execute("""
                    INSERT OR REPLACE INTO etf_minute
                    (symbol, datetime, period, open, high, low, close, volume, money)
                    SELECT symbol, datetime, period, open, high, low, close, volume, money
                    FROM df
                """)

                logger.info(f"{jq_symbol} ({period}): 插入/更新 {len(df)} 条分钟数据")

                if self.use_cache:
                    _global_cache.invalidate(table="etf_minute", symbol=jq_symbol)

        self._retry_write(_do_insert)

    def get_stock_minute(
        self,
        symbol: str,
        period: str,
        start: str,
        end: str,
        adjust: str = "qfq",
        use_cache: bool = None,
    ) -> pd.DataFrame:
        """
        查询股票分钟数据（支持缓存）。

        参数
        ----
        symbol : str
            股票代码，支持多种格式，内部统一转换为聚宽格式查询
        period : str
            周期：1/5/15/30/60
        start : str
            起始时间 'YYYY-MM-DD HH:MM:SS' 或 'YYYY-MM-DD'
        end : str
            结束时间 'YYYY-MM-DD HH:MM:SS' 或 'YYYY-MM-DD'
        adjust : str
            复权类型：qfq/hfq/none
        use_cache : bool
            是否使用缓存

        返回
        ----
        pd.DataFrame
            包含 datetime/open/high/low/close/volume/money 列
        """
        if use_cache is None:
            use_cache = self.use_cache

        # 统一转换为聚宽格式查询
        jq_symbol = normalize_to_jq_format(symbol)

        if use_cache:
            cached = _global_cache.get(
                "stock_minute", jq_symbol, start, end, period=period, adjust=adjust
            )
            if cached is not None:
                return cached

        start_dt = pd.to_datetime(start)
        end_dt = pd.to_datetime(end)

        with self._get_connection(read_only=True) as conn:
            df = conn.execute(
                """
                SELECT datetime, open, high, low, close, volume, money
                FROM stock_minute
                WHERE symbol = ? AND period = ? AND adjust = ?
                  AND datetime >= ? AND datetime <= ?
                ORDER BY datetime
            """,
                [jq_symbol, period, adjust, start_dt, end_dt],
            ).fetchdf()

            if df.empty:
                logger.warning(f"{jq_symbol} ({period} {adjust}): 数据库中无分钟数据")
            else:
                logger.info(
                    f"{jq_symbol} ({period} {adjust}): 查询到 {len(df)} 条分钟数据"
                )

            if use_cache and not df.empty:
                _global_cache.set(
                    "stock_minute", jq_symbol, start, end, df, period=period, adjust=adjust
                )

            return df

    def get_etf_minute(
        self, symbol: str, period: str, start: str, end: str, use_cache: bool = None
    ) -> pd.DataFrame:
        """查询 ETF 分钟数据（支持缓存）。

        参数:
            symbol: ETF代码，支持多种格式，内部统一转换为聚宽格式查询
        """
        if use_cache is None:
            use_cache = self.use_cache

        # 统一转换为聚宽格式查询
        jq_symbol = normalize_to_jq_format(symbol)

        if use_cache:
            cached = _global_cache.get("etf_minute", jq_symbol, start, end, period=period)
            if cached is not None:
                return cached

        start_dt = pd.to_datetime(start)
        end_dt = pd.to_datetime(end)

        with self._get_connection(read_only=True) as conn:
            df = conn.execute(
                """
                SELECT datetime, open, high, low, close, volume, money
                FROM etf_minute
                WHERE symbol = ? AND period = ?
                  AND datetime >= ? AND datetime <= ?
                ORDER BY datetime
            """,
                [jq_symbol, period, start_dt, end_dt],
            ).fetchdf()

            if df.empty:
                logger.warning(f"{jq_symbol} ({period}): 数据库中无分钟数据")
            else:
                logger.info(f"{jq_symbol} ({period}): 查询到 {len(df)} 条分钟数据")

            if use_cache and not df.empty:
                _global_cache.set("etf_minute", jq_symbol, start, end, df, period=period)

            return df

    def has_data(
        self,
        table: str,
        symbol: str,
        start: str,
        end: str,
        adjust: str = None,
        period: str = None,
    ) -> bool:
        """
        检查数据库中是否有足够的时间范围数据。

        参数
        ----
        table : str
            表名：stock_daily/etf_daily/index_daily/stock_minute/etf_minute
        symbol : str
            代码，支持多种格式，内部统一转换为聚宽格式查询
        start : str
            起始日期/时间 'YYYY-MM-DD' 或 'YYYY-MM-DD HH:MM:SS'
        end : str
            结束日期/时间 'YYYY-MM-DD' 或 'YYYY-MM-DD HH:MM:SS'
        adjust : str
            复权类型（仅 stock_daily/stock_minute 需要）
        period : str
            周期（仅分钟表需要）：1/5/15/30/60

        返回
        ----
        bool
            True 表示数据覆盖完整
        """
        # 统一转换为聚宽格式查询
        jq_symbol = normalize_to_jq_format(symbol)

        with self._get_connection(read_only=True) as conn:
            if table == "stock_daily":
                if adjust is None:
                    adjust = "qfq"
                result = conn.execute(
                    """
                    SELECT MIN(datetime) as min_date, MAX(datetime) as max_date
                    FROM stock_daily
                    WHERE symbol = ? AND adjust = ?
                """,
                    [jq_symbol, adjust],
                ).fetchone()
            elif table == "stock_minute":
                if adjust is None:
                    adjust = "qfq"
                if period is None:
                    period = "1"
                result = conn.execute(
                    """
                    SELECT MIN(datetime) as min_date, MAX(datetime) as max_date
                    FROM stock_minute
                    WHERE symbol = ? AND period = ? AND adjust = ?
                """,
                    [jq_symbol, period, adjust],
                ).fetchone()
            elif table == "etf_minute":
                if period is None:
                    period = "1"
                result = conn.execute(
                    """
                    SELECT MIN(datetime) as min_date, MAX(datetime) as max_date
                    FROM etf_minute
                    WHERE symbol = ? AND period = ?
                """,
                    [jq_symbol, period],
                ).fetchone()
            else:
                result = conn.execute(
                    """
                    SELECT MIN(datetime) as min_date, MAX(datetime) as max_date
                    FROM {table}
                    WHERE symbol = ?
                """.format(table=table),
                    [jq_symbol],
                ).fetchone()

            if result[0] is None:
                return False

            min_date = pd.to_datetime(result[0])
            max_date = pd.to_datetime(result[1])
            start_dt = pd.to_datetime(start)
            end_dt = pd.to_datetime(end)

            return min_date <= start_dt and max_date >= end_dt

    def count_records(self, table: str, symbol: str = None, adjust: str = None) -> int:
        """
        统计记录数量。

        参数
        ----
        table : str
            表名
        symbol : str
            代码（可选，不指定则统计全部），支持多种格式，内部统一转换为聚宽格式查询
        adjust : str
            复权类型（仅 stock_daily 需要）

        返回
        ----
        int
            记录数量
        """
        # 统一转换为聚宽格式查询
        jq_symbol = normalize_to_jq_format(symbol) if symbol else None

        with self._get_connection(read_only=True) as conn:
            if table == "stock_daily":
                if jq_symbol and adjust:
                    count = conn.execute(
                        "SELECT COUNT(*) FROM stock_daily WHERE symbol=? AND adjust=?",
                        [jq_symbol, adjust],
                    ).fetchone()[0]
                elif jq_symbol:
                    count = conn.execute(
                        "SELECT COUNT(*) FROM stock_daily WHERE symbol=?", [jq_symbol]
                    ).fetchone()[0]
                else:
                    count = conn.execute("SELECT COUNT(*) FROM stock_daily").fetchone()[
                        0
                    ]
            else:
                if jq_symbol:
                    count = conn.execute(
                        f"SELECT COUNT(*) FROM {table} WHERE symbol=?", [jq_symbol]
                    ).fetchone()[0]
                else:
                    count = conn.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0]

            return count

    def get_symbols(self, table: str) -> List[str]:
        """获取表中所有唯一的代码"""
        with self._get_connection(read_only=True) as conn:
            result = conn.execute(
                f"SELECT DISTINCT symbol FROM {table} ORDER BY symbol"
            ).fetchall()
            return [row[0] for row in result]

    def clear_table(self, table: str, symbol: str = None, adjust: str = None):
        """
        清空表数据（危险操作！）

        参数
        ----
        table : str
            表名
        symbol : str
            代码（可选，不指定则清空全部），支持多种格式，内部统一转换为聚宽格式
        adjust : str
            复权类型（仅 stock_daily 需要）
        """
        # 统一转换为聚宽格式
        jq_symbol = normalize_to_jq_format(symbol) if symbol else None

        with self._get_connection() as conn:
            if table == "stock_daily":
                if jq_symbol and adjust:
                    conn.execute(
                        "DELETE FROM stock_daily WHERE symbol=? AND adjust=?",
                        [jq_symbol, adjust],
                    )
                    logger.warning(
                        f"已删除 {table} 中 symbol={jq_symbol}, adjust={adjust} 的数据"
                    )
                elif jq_symbol:
                    conn.execute("DELETE FROM stock_daily WHERE symbol=?", [jq_symbol])
                    logger.warning(f"已删除 {table} 中 symbol={jq_symbol} 的数据")
                else:
                    conn.execute("DELETE FROM stock_daily")
                    logger.warning(f"已清空表 {table}")
            else:
                if jq_symbol:
                    conn.execute(f"DELETE FROM {table} WHERE symbol=?", [jq_symbol])
                    logger.warning(f"已删除 {table} 中 symbol={jq_symbol} 的数据")
                else:
                    conn.execute(f"DELETE FROM {table}")
                    logger.warning(f"已清空表 {table}")

    def close(self):
        """关闭数据库连接（不再需要，保留接口兼容）"""
        if self.use_cache:
            _global_cache.clear()

    def clear_cache(self):
        """清除本地缓存"""
        if self.use_cache:
            _global_cache.clear()
            logger.info("本地缓存已清除")

    def __del__(self):
        """析构函数"""
        pass


def clear_global_cache():
    """清除全局缓存（用于多进程场景）"""
    _global_cache.clear()


def get_shared_read_only_manager(
    db_path: str = None, use_cache: bool = True
) -> DuckDBManager:
    """
    获取共享的只读管理器实例（推荐用于多进程并发读取）

    改进：
    - 进程级单例，避免重复创建
    - 延迟初始化，减少启动时锁冲突

    参数:
        db_path: 数据库路径
        use_cache: 是否启用缓存

    返回:
        DuckDBManager: 只读模式的管理器实例
    """
    if db_path is None:
        try:
            from jk2bt.utils.config import get_config
            db_path = get_config().cache.duckdb_path
        except Exception:
            base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            project_root = os.path.dirname(base_dir)
            db_path = os.path.join(project_root, "data", "market.db")

    # 使用进程级单例
    cache_key = f"ro:{db_path}:{use_cache}"
    global _PROCESS_SINGLETONS, _SINGLETON_LOCK
    with _SINGLETON_LOCK:
        if cache_key not in _PROCESS_SINGLETONS:
            _PROCESS_SINGLETONS[cache_key] = DuckDBManager(
                db_path=db_path, read_only=True, use_cache=use_cache
            )
        return _PROCESS_SINGLETONS[cache_key]


def get_writer_manager(db_path: str = None, use_cache: bool = False) -> DuckDBManager:
    """
    获取写入管理器实例（建议单进程写入）

    改进：
    - 进程级单例，避免重复创建
    - 延迟初始化表结构，减少锁冲突
    - 静默重试模式，减少噪音日志

    参数:
        db_path: 数据库路径
        use_cache: 是否启用缓存（写入场景建议关闭）

    返回:
        DuckDBManager: 可写模式的管理器实例
    """
    if db_path is None:
        try:
            from jk2bt.utils.config import get_config
            db_path = get_config().cache.duckdb_path
        except Exception:
            base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            project_root = os.path.dirname(base_dir)
            db_path = os.path.join(project_root, "data", "market.db")

    # 使用进程级单例
    cache_key = f"rw:{db_path}:{use_cache}"
    global _PROCESS_SINGLETONS, _SINGLETON_LOCK
    with _SINGLETON_LOCK:
        if cache_key not in _PROCESS_SINGLETONS:
            _PROCESS_SINGLETONS[cache_key] = DuckDBManager(
                db_path=db_path, read_only=False, use_cache=use_cache,
                _delay_init=True  # 延迟初始化，减少启动冲突
            )
        return _PROCESS_SINGLETONS[cache_key]


def get_manager(db_path: str = None, read_only: bool = False, use_cache: bool = True) -> DuckDBManager:
    """
    获取管理器实例的统一入口（推荐使用）

    自动选择合适的工厂函数：
    - read_only=True -> get_shared_read_only_manager()
    - read_only=False -> get_writer_manager()

    参数:
        db_path: 数据库路径
        read_only: 是否只读模式
        use_cache: 是否启用缓存

    返回:
        DuckDBManager: 管理器实例
    """
    if read_only:
        return get_shared_read_only_manager(db_path=db_path, use_cache=use_cache)
    else:
        return get_writer_manager(db_path=db_path, use_cache=use_cache)
