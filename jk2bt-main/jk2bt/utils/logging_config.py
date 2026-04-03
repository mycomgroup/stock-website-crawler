"""
logging_config.py
统一日志配置模块

支持:
- 日志级别配置（通过环境变量 JK2BT_LOG_LEVEL）
- 日志文件输出
- 聚宽风格日志适配器

使用方法:
    from jk2bt.utils.logging_config import setup_logging, get_logger

    # 初始化日志
    setup_logging(level="INFO", log_file="logs/jk2bt.log")

    # 获取logger
    logger = get_logger(__name__)
    logger.info("消息")
"""

import logging
import sys
import os
from pathlib import Path


def setup_logging(
    level: str = "INFO",
    log_file: str = None,
    format_string: str = None,
    force: bool = False
):
    """
    配置全局日志

    参数:
        level: 日志级别, 'DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'
        log_file: 日志文件路径, None则只输出到控制台
        format_string: 自定义格式字符串
        force: 是否强制重新配置（清除已有handlers）

    示例:
        setup_logging(level="DEBUG", log_file="logs/app.log")
        setup_logging(level=os.environ.get("JK2BT_LOG_LEVEL", "INFO"))
    """
    if format_string is None:
        format_string = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

    # 获取日志级别
    log_level = getattr(logging, level.upper(), logging.INFO)

    # 获取根logger
    root_logger = logging.getLogger()

    # 如果强制重新配置，清除已有handlers
    if force:
        root_logger.handlers.clear()

    # 配置根logger
    root_logger.setLevel(log_level)

    # 避免重复添加handlers
    if not root_logger.handlers:
        # 控制台handler
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(log_level)
        console_handler.setFormatter(logging.Formatter(format_string))
        root_logger.addHandler(console_handler)

        # 文件handler（如果指定）
        if log_file:
            log_path = Path(log_file)
            log_path.parent.mkdir(parents=True, exist_ok=True)
            file_handler = logging.FileHandler(log_file, encoding='utf-8')
            file_handler.setLevel(log_level)
            file_handler.setFormatter(logging.Formatter(format_string))
            root_logger.addHandler(file_handler)

    # 设置常用第三方库的日志级别（避免过多输出）
    logging.getLogger("matplotlib").setLevel(logging.WARNING)
    logging.getLogger("PIL").setLevel(logging.WARNING)
    logging.getLogger("urllib3").setLevel(logging.WARNING)
    logging.getLogger("requests").setLevel(logging.WARNING)

    return root_logger


def get_logger(name: str = None) -> logging.Logger:
    """
    获取logger实例

    参数:
        name: logger名称，通常使用 __name__

    返回:
        logging.Logger 实例

    示例:
        logger = get_logger(__name__)
        logger.info("这是一条信息")
    """
    if name is None:
        name = "jk2bt"
    return logging.getLogger(name)


class LogAdapter:
    """
    聚宽风格日志适配器

    兼容聚宽的 log.info(), log.warn(), log.error() 调用方式。
    支持多参数拼接（类似print的行为）。

    示例:
        log = LogAdapter("jk2bt")
        log.info("策略初始化完成", "股票数:", 100)
        log.warn("风险警告:", "回撤超过10%")
    """

    def __init__(self, logger_name: str = "jk2bt"):
        self._logger = logging.getLogger(logger_name)

    def info(self, *args, **kwargs):
        """输出INFO级别日志"""
        self._logger.info(self._format(args, kwargs))

    def warn(self, *args, **kwargs):
        """输出WARNING级别日志"""
        self._logger.warning(self._format(args, kwargs))

    def warning(self, *args, **kwargs):
        """输出WARNING级别日志（warn的别名）"""
        self._logger.warning(self._format(args, kwargs))

    def error(self, *args, **kwargs):
        """输出ERROR级别日志"""
        self._logger.error(self._format(args, kwargs))

    def debug(self, *args, **kwargs):
        """输出DEBUG级别日志"""
        self._logger.debug(self._format(args, kwargs))

    def critical(self, *args, **kwargs):
        """输出CRITICAL级别日志"""
        self._logger.critical(self._format(args, kwargs))

    def set_level(self, level: str):
        """
        设置日志级别

        参数:
            level: 'DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'
        """
        self._logger.setLevel(getattr(logging, level.upper(), logging.INFO))

    def _format(self, args, kwargs):
        """
        格式化日志消息

        将多个参数拼接成字符串，类似print的行为
        """
        msg = " ".join(str(a) for a in args)
        if kwargs:
            msg += " " + str(kwargs)
        return msg


class JQLogAdapter(LogAdapter):
    """
    聚宽风格日志适配器（别名）

    完全兼容聚宽平台的 log 对象行为。
    """
    pass


def create_jq_log_adapter(logger_name: str = "jk2bt") -> JQLogAdapter:
    """
    创建聚宽风格日志适配器

    参数:
        logger_name: logger名称

    返回:
        JQLogAdapter 实例
    """
    return JQLogAdapter(logger_name)


# 提供一个全局默认logger实例
_default_logger = None


def get_default_logger():
    """
    获取默认logger实例

    如果尚未初始化，会自动使用环境变量 JK2BT_LOG_LEVEL 配置
    """
    global _default_logger
    if _default_logger is None:
        level = os.environ.get("JK2BT_LOG_LEVEL", "INFO")
        setup_logging(level=level)
        _default_logger = get_logger("jk2bt")
    return _default_logger


# 模块加载时自动初始化（如果环境变量设置了）
if os.environ.get("JK2BT_LOG_LEVEL"):
    setup_logging(level=os.environ.get("JK2BT_LOG_LEVEL", "INFO"))


__all__ = [
    "setup_logging",
    "get_logger",
    "LogAdapter",
    "JQLogAdapter",
    "create_jq_log_adapter",
    "get_default_logger",
]