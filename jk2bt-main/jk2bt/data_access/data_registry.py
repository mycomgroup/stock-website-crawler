"""
src/data_access/data_registry.py
数据源注册中心 - 管理全局数据源实例。

提供单例模式的数据源管理，支持:
- 默认数据源注册
- 动态数据源切换
- 数据源健康检查
- 测试环境 Mock 数据源注入
"""

import logging
import threading
from typing import Optional, Dict, Any, Type
import pandas as pd

from .data_source import DataSource, DataSourceError

logger = logging.getLogger(__name__)


class DataRegistry:
    """
    数据源注册中心 (单例模式)。

    管理全局数据源实例，支持:
    - 注册默认数据源
    - 动态切换数据源
    - 获取当前数据源
    - 数据源健康检查

    使用方式:
        # 获取默认数据源
        source = DataRegistry.get_source()
        df = source.get_daily_data('sh600000', '2020-01-01', '2020-12-31')

        # 注册自定义数据源
        DataRegistry.register(my_custom_source)

        # 使用 Mock 数据源测试
        from jk2bt.data_access import MockDataSource
        DataRegistry.register(MockDataSource())

        # 恢复默认数据源
        DataRegistry.reset()

    线程安全:
        所有操作都使用锁保护，确保多线程环境下的安全性。
    """

    _instance = None
    _lock = threading.Lock()
    _source: Optional[DataSource] = None
    _default_source_class: Type[DataSource] = None
    _initialized: bool = False

    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
        return cls._instance

    @classmethod
    def get_source(cls) -> DataSource:
        """
        获取当前注册的数据源。

        如果未注册，自动创建默认 AkShareAdapter。

        Returns:
            DataSource: 当前数据源实例

        Raises:
            DataSourceError: 数据源不可用
        """
        with cls._lock:
            if cls._source is None:
                cls._init_default_source()
            return cls._source

    @classmethod
    def _init_default_source(cls):
        """初始化默认数据源"""
        try:
            # 延迟导入避免循环依赖
            from .akshare_adapter import AkShareAdapter
            cls._source = AkShareAdapter()
            cls._default_source_class = AkShareAdapter
            cls._initialized = True
            logger.info("初始化默认数据源: AkShareAdapter")
        except Exception as e:
            logger.error(f"初始化默认数据源失败: {e}")
            # 尝试使用 Mock 数据源作为备用
            try:
                from .mock_data_source import MockDataSource
                cls._source = MockDataSource()
                cls._initialized = True
                logger.warning("使用 MockDataSource 作为备用数据源")
            except Exception:
                raise DataSourceError("无法初始化任何数据源")

    @classmethod
    def register(cls, source: DataSource):
        """
        注册数据源。

        替换当前数据源为新实例。

        Args:
            source: DataSource 实例

        注意:
            - 注册新数据源会清除缓存
            - 线程安全
        """
        with cls._lock:
            if not isinstance(source, DataSource):
                raise ValueError(f"source 必须是 DataSource 实例，收到: {type(source)}")

            cls._source = source
            cls._initialized = True
            logger.info(f"注册数据源: {source.name}")

            # 清除缓存
            try:
                from .cache_manager import clear_cache
                clear_cache()
            except Exception:
                pass

    @classmethod
    def register_class(cls, source_class: Type[DataSource], **kwargs):
        """
        注册数据源类。

        使用提供的类创建实例并注册。

        Args:
            source_class: DataSource 子类
            **kwargs: 传递给构造函数的参数
        """
        with cls._lock:
            instance = source_class(**kwargs)
            cls.register(instance)

    @classmethod
    def reset(cls):
        """
        重置为默认数据源。

        清除当前注册的数据源，下次调用 get_source() 时重新初始化。
        """
        with cls._lock:
            cls._source = None
            cls._initialized = False
            logger.info("重置数据源注册中心")

            # 清除缓存
            try:
                from .cache_manager import reset_cache
                reset_cache()
            except Exception:
                pass

    @classmethod
    def get_source_info(cls) -> Dict[str, Any]:
        """
        获取当前数据源信息。

        Returns:
            Dict: 数据源信息
        """
        with cls._lock:
            if cls._source is None:
                return {
                    "status": "not_initialized",
                    "name": None,
                    "type": None,
                }

            info = cls._source.get_source_info()
            info["status"] = "initialized"
            return info

    @classmethod
    def health_check(cls) -> Dict[str, Any]:
        """
        数据源健康检查。

        Returns:
            Dict: 健康状态
        """
        with cls._lock:
            if cls._source is None:
                return {
                    "status": "error",
                    "message": "数据源未初始化",
                }

            return cls._source.health_check()

    @classmethod
    def is_initialized(cls) -> bool:
        """检查是否已初始化"""
        with cls._lock:
            return cls._initialized

    @classmethod
    def get_source_name(cls) -> str:
        """获取当前数据源名称"""
        with cls._lock:
            if cls._source is None:
                return "not_initialized"
            return cls._source.name


# 便捷函数
def get_data_source() -> DataSource:
    """
    获取数据源实例。

    这是推荐的获取数据源的方式。

    Returns:
        DataSource: 当前数据源

    使用示例:
        from jk2bt.data_access import get_data_source

        source = get_data_source()
        df = source.get_daily_data('sh600000', '2020-01-01', '2020-12-31')
        stocks = source.get_index_stocks('000300.XSHG')
        days = source.get_trading_days()
    """
    return DataRegistry.get_source()


def set_data_source(source: DataSource):
    """
    设置数据源实例。

    Args:
        source: DataSource 实例

    使用示例:
        from jk2bt.data_access import set_data_source, MockDataSource

        # 测试环境使用 Mock 数据源
        mock = MockDataSource()
        set_data_source(mock)
    """
    DataRegistry.register(source)


def reset_data_source():
    """
    重置数据源为默认值。
    """
    DataRegistry.reset()


def get_source_health() -> Dict[str, Any]:
    """
    获取数据源健康状态。
    """
    return DataRegistry.health_check()


__all__ = [
    "DataRegistry",
    "get_data_source",
    "set_data_source",
    "reset_data_source",
    "get_source_health",
]