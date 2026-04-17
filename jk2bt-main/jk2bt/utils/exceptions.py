"""
utils/exceptions.py
共享异常类 - 供所有模块使用的基础异常定义。

这些异常类被多个模块共享使用（api, analysis, data, engine），
因此放在 utils 层，避免循环依赖。

异常层次:
    JK2BTError (基础异常)
    ├── DataSourceError (数据源相关)
    │   ├── NetworkError (网络连接)
    │   ├── IndexNotSupportedError (指数不支持)
    │   └── ValuationDataError (估值数据)
    │   └── FinancialDataError (财务数据)
    │   └── MarketDataError (市场数据)
    ├── CacheError (缓存相关)
    ├── ValidationError (数据验证)
    ├── DatabaseError (数据库相关)
    ├── ConfigurationError (配置相关)

使用方式:
    from jk2bt.utils.exceptions import (
        JK2BTError,
        DataSourceError,
        CacheError,
        ValidationError,
        DatabaseError,
    )

    # 抛出异常时保留原始异常链
    try:
        df = ak.stock_a_lg_indicator(symbol=symbol)
    except ConnectionError as e:
        raise DataSourceError(f"无法获取 {symbol} 的估值数据") from e
"""


class JK2BTError(Exception):
    """
    JK2BT 基础异常类

    所有自定义异常都继承此类，提供统一的基础接口。

    属性:
        message: 错误消息
        context: 上下文信息字典（可选）
    """

    def __init__(
        self, message: str, context: dict = None, source: str = None, **kwargs
    ):
        self.message = message
        self.context = context or {}
        if source:
            self.context["source"] = source
        for k, v in kwargs.items():
            if k not in ("message", "context"):
                self.context[k] = v
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
    """

    pass


class NetworkError(DataSourceError):
    """
    网络连接错误

    当网络连接失败、超时或不可达时抛出。
    """

    pass


class CacheError(JK2BTError):
    """
    缓存错误

    当缓存读写操作失败时抛出。
    """

    pass


class ValidationError(JK2BTError):
    """
    数据验证错误

    当数据不符合预期格式或约束时抛出。
    """

    pass


class DatabaseError(JK2BTError):
    """
    数据库错误

    当 DuckDB 或其他数据库操作失败时抛出。
    """

    pass


class ConfigurationError(JK2BTError):
    """
    配置错误

    当配置参数无效或缺失时抛出。
    """

    pass


class IndexNotSupportedError(DataSourceError):
    """
    指数不支持错误

    当请求的指数代码不在支持列表中时抛出。

    属性:
        index_code: 请求的指数代码
        supported_indices: 支持的指数列表
    """

    def __init__(
        self, index_code: str, supported_indices: list = None, context: dict = None
    ):
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
    """

    pass


class FinancialDataError(DataSourceError):
    """
    财务数据错误

    当财务数据获取失败时抛出。
    """

    pass


class MarketDataError(DataSourceError):
    """
    市场数据错误

    当行情数据获取失败时抛出。
    """

    pass


__all__ = [
    "JK2BTError",
    "DataSourceError",
    "NetworkError",
    "CacheError",
    "ValidationError",
    "DatabaseError",
    "ConfigurationError",
    "IndexNotSupportedError",
    "ValuationDataError",
    "FinancialDataError",
    "MarketDataError",
]
