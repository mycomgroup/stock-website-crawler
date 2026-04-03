"""
src/core/exceptions.py
自定义异常类层次结构 - 提供更精确的错误处理和诊断能力。

异常层次:
    JK2BTError (基础异常)
    ├── DataSourceError (数据源相关)
    │   ├── NetworkError (网络连接)
    │   ├── IndexNotSupportedError (指数不支持)
    │   └── ValuationDataError (估值数据)
    ├── CacheError (缓存相关)
    ├── ValidationError (数据验证)
    ├── StrategyError (策略执行)
    └── APICompatibilityError (API兼容性)

使用方式:
    from jk2bt.core.exceptions import (
        JK2BTError,
        NetworkError,
        ValuationDataError,
        IndexNotSupportedError,
    )

    # 抛出异常时保留原始异常链
    try:
        df = ak.stock_a_lg_indicator(symbol=symbol)
    except ConnectionError as e:
        raise NetworkError(f"无法获取 {symbol} 的估值数据") from e

    # 捕获特定异常
    try:
        stocks = get_index_stocks('000300.XSHG')
    except IndexNotSupportedError as e:
        logger.warning(f"指数不支持: {e.index_code}, 建议使用: {e.supported_indices}")
"""

import logging

logger = logging.getLogger(__name__)


class JK2BTError(Exception):
    """
    JK2BT 基础异常类

    所有自定义异常都继承此类，提供统一的基础接口。

    属性:
        message: 错误消息
        context: 上下文信息字典（可选）

    示例:
        raise JK2BTError("操作失败", context={"symbol": "600519", "operation": "fetch"})
    """

    def __init__(self, message: str, context: dict = None):
        self.message = message
        self.context = context or {}
        super().__init__(self.message)

    def __str__(self):
        if self.context:
            context_str = ", ".join(f"{k}={v}" for k, v in self.context.items())
            return f"{self.message} [{context_str}]"
        return self.message


class DataSourceError(JK2BTError):
    """
    数据源错误

    当外部数据源（AkShare、网络API等）发生错误时抛出。

    示例:
        raise DataSourceError("AkShare API 调用失败", context={"api": "stock_zh_a_hist"})
    """
    pass


class NetworkError(DataSourceError):
    """
    网络连接错误

    当网络连接失败、超时或不可达时抛出。

    示例:
        try:
            response = requests.get(url, timeout=10)
        except requests.ConnectionError as e:
            raise NetworkError("网络连接失败") from e
        except requests.Timeout as e:
            raise NetworkError("请求超时") from e
    """
    pass


class CacheError(JK2BTError):
    """
    缓存错误

    当缓存读写操作失败时抛出。

    示例:
        try:
            df = pd.read_pickle(cache_file)
        except Exception as e:
            raise CacheError(f"缓存读取失败: {cache_file}") from e
    """
    pass


class ValidationError(JK2BTError):
    """
    数据验证错误

    当数据不符合预期格式或约束时抛出。

    示例:
        if df.empty:
            raise ValidationError("返回数据为空", context={"symbol": symbol})
        if 'close' not in df.columns:
            raise ValidationError("缺少必需列", context={"missing": "close", "columns": df.columns.tolist()})
    """
    pass


class StrategyError(JK2BTError):
    """
    策略执行错误

    当策略执行过程中发生错误时抛出。

    示例:
        raise StrategyError("订单执行失败", context={"order_id": order.id, "reason": "insufficient_balance"})
    """
    pass


class APICompatibilityError(JK2BTError):
    """
    API 兼容性错误

    当聚宽 API 与本地实现存在兼容性问题时抛出。

    示例:
        raise APICompatibilityError("接口签名不匹配", context={"api": "get_price", "expected": "panel参数"})
    """
    pass


class IndexNotSupportedError(DataSourceError):
    """
    指数不支持错误

    当请求的指数代码不在支持列表中时抛出。

    属性:
        index_code: 请求的指数代码
        supported_indices: 支持的指数列表

    示例:
        raise IndexNotSupportedError('999999', supported_indices=['000300', '000905'])
    """

    def __init__(self, index_code: str, supported_indices: list = None, context: dict = None):
        self.index_code = index_code
        self.supported_indices = supported_indices or []

        msg = f"指数 '{index_code}' 不在支持列表中"
        if supported_indices:
            display_indices = supported_indices[:5]
            msg += f"，支持的指数: {display_indices}..."

        super().__init__(msg, context=context)

    def __str__(self):
        base_msg = super().__str__()
        if self.supported_indices:
            return f"{base_msg} (完整列表请查询 SUPPORTED_INDEXES)"
        return base_msg


class ValuationDataError(DataSourceError):
    """
    估值数据不可用错误

    当无法获取估值数据（PE/PB/市值等）时抛出。

    示例:
        raise ValuationDataError(f"无法获取 {symbol} 的估值数据", context={"symbol": symbol, "source": "baidu"})
    """
    pass


class FinancialDataError(DataSourceError):
    """
    财务数据错误

    当财务数据获取失败时抛出。

    示例:
        raise FinancialDataError("利润表获取失败", context={"symbol": symbol, "report_type": "income"})
    """
    pass


class MarketDataError(DataSourceError):
    """
    市场数据错误

    当行情数据获取失败时抛出。

    示例:
        raise MarketDataError("分钟数据获取失败", context={"symbol": symbol, "frequency": "5m"})
    """
    pass


class DatabaseError(JK2BTError):
    """
    数据库错误

    当 DuckDB 或其他数据库操作失败时抛出。

    示例:
        raise DatabaseError("数据库连接失败", context={"db_path": db_path})
    """
    pass


class ConfigurationError(JK2BTError):
    """
    配置错误

    当配置参数无效或缺失时抛出。

    示例:
        raise ConfigurationError("缺少必需配置", context={"missing_key": "cache_dir"})
    """
    pass


# 异常处理辅助函数

def wrap_exception(
    original_exception: Exception,
    new_exception_class: type,
    message: str,
    context: dict = None,
    preserve_chain: bool = True
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
        context['original_error'] = str(original_exception)
        context['original_type'] = type(original_exception).__name__
        return new_exception_class(message, context=context)
    return new_exception_class(message, context=context)


def log_and_raise(
    exception_class: type,
    message: str,
    context: dict = None,
    log_level: str = "error",
    from_exception: Exception = None
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
    'JK2BTError',
    'DataSourceError',
    'NetworkError',
    'CacheError',
    'ValidationError',
    'StrategyError',
    'APICompatibilityError',
    'IndexNotSupportedError',
    'ValuationDataError',
    'FinancialDataError',
    'MarketDataError',
    'DatabaseError',
    'ConfigurationError',
    'wrap_exception',
    'log_and_raise',
    'safe_call',
]