"""
test_exceptions.py
exceptions.py 单元测试

测试场景覆盖:
1. JK2BTError 基础异常
2. DataSourceError 数据源错误
3. NetworkError 网络错误
4. CacheError 缓存错误
5. ValidationError 验证错误
6. StrategyError 策略错误
7. APICompatibilityError API兼容性错误
8. IndexNotSupportedError 指数不支持错误
9. ValuationDataError 估值数据错误
10. FinancialDataError 财务数据错误
11. MarketDataError 市场数据错误
12. DatabaseError 数据库错误
13. ConfigurationError 配置错误
14. wrap_exception 异常包装函数
15. log_and_raise 日志记录并抛出函数
16. safe_call 安全调用函数
"""

import pytest
from jk2bt.engine.exceptions import (
    JK2BTError,
    DataSourceError,
    NetworkError,
    CacheError,
    ValidationError,
    StrategyError,
    APICompatibilityError,
    IndexNotSupportedError,
    ValuationDataError,
    FinancialDataError,
    MarketDataError,
    DatabaseError,
    ConfigurationError,
    wrap_exception,
    log_and_raise,
    safe_call,
)


class TestJK2BTError:
    """测试 JK2BTError 基础异常"""

    def test_basic_exception(self):
        """测试基本异常创建"""
        err = JK2BTError("test message")
        assert str(err) == "test message"
        assert err.message == "test message"

    def test_exception_with_context(self):
        """测试带上下文的异常"""
        err = JK2BTError("test", context={"key": "value"})
        assert err.context["key"] == "value"

    def test_exception_str_with_context(self):
        """测试带上下文的字符串表示"""
        err = JK2BTError("test", context={"a": 1, "b": 2})
        s = str(err)
        assert "test" in s
        assert "a=1" in s
        assert "b=2" in s

    def test_exception_inheritance(self):
        """测试异常继承"""
        err = JK2BTError("test")
        assert isinstance(err, Exception)


class TestDataSourceError:
    """测试 DataSourceError 数据源错误"""

    def test_inheritance(self):
        """测试继承关系"""
        err = DataSourceError("data error")
        assert isinstance(err, JK2BTError)
        assert isinstance(err, Exception)


class TestNetworkError:
    """测试 NetworkError 网络错误"""

    def test_inheritance(self):
        """测试继承关系"""
        err = NetworkError("network error")
        assert isinstance(err, DataSourceError)
        assert isinstance(err, JK2BTError)


class TestCacheError:
    """测试 CacheError 缓存错误"""

    def test_inheritance(self):
        """测试继承关系"""
        err = CacheError("cache error")
        assert isinstance(err, JK2BTError)


class TestValidationError:
    """测试 ValidationError 验证错误"""

    def test_inheritance(self):
        """测试继承关系"""
        err = ValidationError("validation error")
        assert isinstance(err, JK2BTError)

    def test_with_context(self):
        """测试带上下文"""
        err = ValidationError("invalid", context={"field": "close"})
        assert err.context["field"] == "close"


class TestStrategyError:
    """测试 StrategyError 策略错误"""

    def test_inheritance(self):
        """测试继承关系"""
        err = StrategyError("strategy error")
        assert isinstance(err, JK2BTError)


class TestAPICompatibilityError:
    """测试 APICompatibilityError API兼容性错误"""

    def test_inheritance(self):
        """测试继承关系"""
        err = APICompatibilityError("api error")
        assert isinstance(err, JK2BTError)


class TestIndexNotSupportedError:
    """测试 IndexNotSupportedError 指数不支持错误"""

    def test_basic_creation(self):
        """测试基本创建"""
        err = IndexNotSupportedError("999999")
        assert err.index_code == "999999"
        assert "999999" in str(err)

    def test_with_supported_indices(self):
        """测试带支持指数列表"""
        supported = ["000300", "000905", "000852"]
        err = IndexNotSupportedError("999999", supported_indices=supported)
        assert err.supported_indices == supported

    def test_str_shows_supported_indices(self):
        """测试字符串显示支持指数"""
        err = IndexNotSupportedError("999999", supported_indices=["000300"])
        s = str(err)
        assert "000300" in s


class TestValuationDataError:
    """测试 ValuationDataError 估值数据错误"""

    def test_inheritance(self):
        """测试继承关系"""
        err = ValuationDataError("valuation error")
        assert isinstance(err, DataSourceError)


class TestFinancialDataError:
    """测试 FinancialDataError 财务数据错误"""

    def test_inheritance(self):
        """测试继承关系"""
        err = FinancialDataError("financial error")
        assert isinstance(err, DataSourceError)


class TestMarketDataError:
    """测试 MarketDataError 市场数据错误"""

    def test_inheritance(self):
        """测试继承关系"""
        err = MarketDataError("market error")
        assert isinstance(err, DataSourceError)


class TestDatabaseError:
    """测试 DatabaseError 数据库错误"""

    def test_inheritance(self):
        """测试继承关系"""
        err = DatabaseError("db error")
        assert isinstance(err, JK2BTError)


class TestConfigurationError:
    """测试 ConfigurationError 配置错误"""

    def test_inheritance(self):
        """测试继承关系"""
        err = ConfigurationError("config error")
        assert isinstance(err, JK2BTError)


class TestWrapException:
    """测试 wrap_exception 异常包装函数"""

    def test_wrap_exception_without_chain(self):
        """测试不保留异常链"""
        original = ValueError("original")
        new_exc = wrap_exception(
            original, ValidationError, "wrapped", preserve_chain=False
        )
        assert isinstance(new_exc, ValidationError)
        assert str(new_exc) == "wrapped"

    def test_wrap_exception_with_chain(self):
        """测试保留异常链"""
        original = ValueError("original")
        new_exc = wrap_exception(
            original, ValidationError, "wrapped", preserve_chain=True
        )
        assert isinstance(new_exc, ValidationError)
        assert new_exc.context["original_type"] == "ValueError"

    def test_wrap_exception_preserves_context(self):
        """测试保留上下文"""
        original = ValueError("original")
        new_exc = wrap_exception(
            original, ValidationError, "wrapped", context={"extra": "data"}
        )
        assert new_exc.context["extra"] == "data"


class TestLogAndRaise:
    """测试 log_and_raise 函数"""

    def test_basic_log_and_raise(self):
        """测试基本日志和抛出"""
        with pytest.raises(NetworkError):
            log_and_raise(NetworkError, "test error", log_level="error")

    def test_log_and_raise_with_context(self):
        """测试带上下文的日志和抛出"""
        with pytest.raises(NetworkError):
            log_and_raise(NetworkError, "test", context={"key": "value"})

    def test_log_and_raise_from_exception(self):
        """测试从已有异常抛出"""
        original = ConnectionError("connection failed")
        with pytest.raises(NetworkError):
            log_and_raise(NetworkError, "network error", from_exception=original)


class TestSafeCall:
    """测试 safe_call 安全调用函数"""

    def test_safe_call_success(self):
        """测试成功调用"""

        def func(x):
            return x * 2

        result = safe_call(func, 5)
        assert result == 10

    def test_safe_call_with_default(self):
        """测试返回默认值"""

        def func():
            raise JK2BTError("error")

        result = safe_call(func, default=42)
        assert result == 42

    def test_safe_call_catches_specific_exception(self):
        """测试捕获特定异常"""

        def func():
            raise NetworkError("network error")

        result = safe_call(func, default=None, exceptions_to_catch=(NetworkError,))
        assert result is None

    def test_safe_call_with_args_kwargs(self):
        """测试传递参数"""

        def func(a, b, key=1):
            return a + b + key

        result = safe_call(func, 1, 2, key=3)
        assert result == 6

    def test_safe_call_default_catches_jk2bt_error(self):
        """测试默认捕获JK2BTError"""

        def func():
            raise JK2BTError("error")

        result = safe_call(func, default="fallback")
        assert result == "fallback"

    def test_safe_call_unknown_exception(self):
        """测试未知异常"""

        def func():
            raise RuntimeError("unknown")

        result = safe_call(func, default="fallback")
        assert result == "fallback"
