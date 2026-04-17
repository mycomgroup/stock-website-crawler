"""
engine/exceptions.py
引擎层异常类 - 包含共享异常和引擎特有异常。

架构说明:
    共享异常类（JK2BTError, DataSourceError, CacheError 等）定义在 utils/exceptions.py
    这里导入并重新导出，保持向后兼容性。

    引擎特有异常:
    - StrategyError: 策略执行错误
    - APICompatibilityError: API兼容性错误

使用方式:
    # 推荐：从 utils 导入共享异常
    from jk2bt.utils.exceptions import DataSourceError, CacheError

    # 兼容：从 engine 导入（会自动包含所有异常）
    from jk2bt.engine.exceptions import DataSourceError, StrategyError
"""

import logging

from jk2bt.utils.exceptions import (
    JK2BTError,
    DataSourceError,
    NetworkError,
    CacheError,
    ValidationError,
    DatabaseError,
    ConfigurationError,
    IndexNotSupportedError,
    ValuationDataError,
    FinancialDataError,
    MarketDataError,
)

logger = logging.getLogger(__name__)


class StrategyError(JK2BTError):
    """
    策略执行错误（引擎特有）

    当策略执行过程中发生错误时抛出。
    """

    pass


class APICompatibilityError(JK2BTError):
    """
    API 兼容性错误（引擎特有）

    当聚宽 API 与本地实现存在兼容性问题时抛出。
    """

    pass


# 异常处理辅助函数


def wrap_exception(
    original_exception: Exception,
    new_exception_class: type,
    message: str,
    context: dict = None,
    preserve_chain: bool = True,
) -> JK2BTError:
    """
    将原始异常包装为自定义异常。

    参数:
        original_exception: 原始异常
        new_exception_class: 新异常类
        message: 新异常消息
        context: 上下文信息
        preserve_chain: 是否保留异常链 (使用 raise ... from e)

    返回:
        新的异常实例

    示例:
        try:
            df = ak.stock_zh_a_hist(symbol=symbol)
        except Exception as e:
            new_exc = wrap_exception(e, MarketDataError, f"行情获取失败: {symbol}")
            raise new_exc from e if preserve_chain else new_exc
    """
    if preserve_chain:
        # 创建新异常并保留原始异常信息
        context = context or {}
        context["original_error"] = str(original_exception)
        context["original_type"] = type(original_exception).__name__
        return new_exception_class(message, context=context)
    return new_exception_class(message, context=context)


def log_and_raise(
    exception_class: type,
    message: str,
    context: dict = None,
    log_level: str = "error",
    from_exception: Exception = None,
):
    """
    记录日志并抛出异常。

    参数:
        exception_class: 异常类
        message: 错误消息
        context: 上下文信息
        log_level: 日志级别 ('error', 'warning', 'debug')
        from_exception: 原始异常（用于异常链）

    示例:
        try:
            result = api_call()
        except ConnectionError as e:
            log_and_raise(NetworkError, "API连接失败", {"api": "get_price"}, from_exception=e)
    """
    exc = exception_class(message, context=context)

    # 记录日志
    log_func = getattr(logger, log_level, logger.error)
    log_func(f"{exception_class.__name__}: {exc}")

    # 抛出异常（保留异常链）
    if from_exception:
        raise exc from from_exception
    raise exc


def safe_call(func, *args, default=None, exceptions_to_catch=None, **kwargs):
    """
    安全调用函数，捕获指定异常并返回默认值。

    参数:
        func: 要调用的函数
        args: 函数参数
        default: 发生异常时的默认返回值
        exceptions_to_catch: 要捕获的异常类型列表（默认捕获 JK2BTError）
        kwargs: 函数关键字参数

    返回:
        函数返回值或默认值

    示例:
        df = safe_call(ak.stock_zh_a_hist, symbol='600519', default=pd.DataFrame(),
                       exceptions_to_catch=[NetworkError, ValuationDataError])
    """
    if exceptions_to_catch is None:
        exceptions_to_catch = (JK2BTError,)

    try:
        return func(*args, **kwargs)
    except exceptions_to_catch as e:
        logger.warning(f"安全调用失败: {e}")
        return default
    except Exception as e:
        # 未预期的异常，记录并返回默认值
        logger.error(f"安全调用发生未预期异常: {type(e).__name__}: {e}")
        return default


# 导出所有异常类
__all__ = [
    "JK2BTError",
    "DataSourceError",
    "NetworkError",
    "CacheError",
    "ValidationError",
    "StrategyError",
    "APICompatibilityError",
    "IndexNotSupportedError",
    "ValuationDataError",
    "FinancialDataError",
    "MarketDataError",
    "DatabaseError",
    "ConfigurationError",
    "wrap_exception",
    "log_and_raise",
    "safe_call",
]
