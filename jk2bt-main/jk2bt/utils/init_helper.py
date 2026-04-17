"""
utils/init_helper.py
通用延迟初始化辅助工具。

提供单例模式 + 延迟初始化的通用实现，避免各模块重复编写相同的模板代码。
"""

import threading
from typing import Any, Callable, Optional


class LazyInitSingleton:
    """
    延迟初始化单例基类。

    子类只需实现 _do_init() 方法，无需再写 __new__ / _ensure_initialized 模板。

    使用示例:
        class MyManager(LazyInitSingleton):
            def _do_init(self, db_path=None):
                self._manager = SomeAdapter(db_path)

        mgr = MyManager()
        mgr.ensure_initialized(db_path="/data")
    """

    _instance: Optional[Any] = None
    _lock = threading.Lock()
    _initialized = False

    def __new__(cls, *args, **kwargs):
        with cls._lock:
            if cls._instance is None:
                cls._instance = super().__new__(cls)
                cls._instance._initialized = False
            return cls._instance

    def ensure_initialized(self, *args, **kwargs):
        """确保已初始化（线程安全）"""
        if self._initialized:
            return
        with self._lock:
            if self._initialized:
                return
            self._do_init(*args, **kwargs)
            self._initialized = True

    def _do_init(self, *args, **kwargs):
        """子类必须实现的实际初始化逻辑"""
        raise NotImplementedError

    @classmethod
    def reset(cls):
        """重置单例（主要用于测试）"""
        with cls._lock:
            cls._instance = None
            cls._initialized = False


def make_lazy_init_getter(
    manager_cls,
    availability_flag: bool,
    default_db_path: Optional[str] = None,
):
    """
    生成 _get_db_manager() 风格的获取函数。

    参数
    ----
    manager_cls      : LazyInitSingleton 子类
    availability_flag: 功能是否可用的布尔标志（如 _PARQUET_AVAILABLE）
    default_db_path  : 默认数据库路径

    返回
    ----
    一个无参函数，调用时返回已初始化的单例，或不可用时返回 None
    """

    def getter(db_path: Optional[str] = None):
        if not availability_flag:
            return None
        manager = manager_cls()
        manager.ensure_initialized(db_path or default_db_path)
        return manager

    return getter
