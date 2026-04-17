"""
test_error_codes.py
测试错误码模块
"""

import pytest

from jk2bt.data.sources.error_codes import (
    ErrorCode,
    DataAccessException,
    DataSourceError,
    SourceUnavailableError,
    NoDataError,
    TimeoutError,
    RateLimitError,
)


class TestErrorCode:
    """测试 ErrorCode 枚举"""

    def test_error_codes_exist(self):
        """验证所有错误码存在"""
        assert ErrorCode.SOURCE_UNAVAILABLE is not None
        assert ErrorCode.SOURCE_TIMEOUT is not None
        assert ErrorCode.NO_DATA is not None
        assert ErrorCode.INVALID_DATA is not None
        assert ErrorCode.CACHE_MISS is not None
        assert ErrorCode.INVALID_SYMBOL is not None
        assert ErrorCode.INVALID_DATE_RANGE is not None
        assert ErrorCode.INTERNAL_ERROR is not None

    def test_error_code_values(self):
        """验证错误码值"""
        assert ErrorCode.SOURCE_UNAVAILABLE.value == "SOURCE_UNAVAILABLE"
        assert ErrorCode.NO_DATA.value == "NO_DATA"
        assert ErrorCode.CACHE_MISS.value == "CACHE_MISS"


class TestDataAccessException:
    """测试 DataAccessException 基类"""

    def test_basic_exception(self):
        """测试基本异常创建"""
        exc = DataAccessException("test message")
        assert str(exc) == "test message"
        assert exc.error_code is None
        assert exc.source is None
        assert exc.symbol is None

    def test_exception_with_error_code(self):
        """测试带错误码的异常"""
        exc = DataAccessException("test", error_code=ErrorCode.NO_DATA)
        assert exc.error_code == ErrorCode.NO_DATA

    def test_exception_with_source(self):
        """测试带数据源信息的异常"""
        exc = DataAccessException("test", source="akshare")
        assert exc.source == "akshare"

    def test_exception_with_symbol(self):
        """测试带股票代码的异常"""
        exc = DataAccessException("test", symbol="600519")
        assert exc.symbol == "600519"

    def test_exception_with_all_params(self):
        """测试带所有参数的异常"""
        exc = DataAccessException(
            "test message",
            error_code=ErrorCode.SOURCE_UNAVAILABLE,
            source="akshare",
            symbol="600519",
        )
        assert exc.error_code == ErrorCode.SOURCE_UNAVAILABLE
        assert exc.source == "akshare"
        assert exc.symbol == "600519"

    def test_to_dict(self):
        """测试转换为字典"""
        exc = DataAccessException(
            "test", error_code=ErrorCode.NO_DATA, source="test_source", symbol="600519"
        )
        d = exc.to_dict()
        assert d["error_code"] == "NO_DATA"
        assert d["message"] == "test"
        assert d["source"] == "test_source"
        assert d["symbol"] == "600519"

    def test_to_dict_no_error_code(self):
        """测试无错误码时转换为字典"""
        exc = DataAccessException("test")
        d = exc.to_dict()
        assert d["error_code"] is None


class TestDataSourceError:
    """测试 DataSourceError 异常"""

    def test_creation(self):
        """测试创建"""
        exc = DataSourceError("data source error")
        assert str(exc) == "data source error"

    def test_creation_with_params(self):
        """测试带参数创建"""
        exc = DataSourceError(
            "error message",
            error_code=ErrorCode.SOURCE_UNAVAILABLE,
            source="akshare",
            symbol="600519",
        )
        assert exc.error_code == ErrorCode.SOURCE_UNAVAILABLE
        assert exc.source == "akshare"
        assert exc.symbol == "600519"


class TestSourceUnavailableError:
    """测试 SourceUnavailableError 异常"""

    def test_creation(self):
        """测试创建"""
        exc = SourceUnavailableError("source unavailable")
        assert str(exc) == "source unavailable"
        assert exc.error_code == ErrorCode.SOURCE_UNAVAILABLE

    def test_default_error_code(self):
        """测试默认错误码"""
        exc = SourceUnavailableError("test")
        assert exc.error_code == ErrorCode.SOURCE_UNAVAILABLE


class TestNoDataError:
    """测试 NoDataError 异常"""

    def test_creation(self):
        """测试创建"""
        exc = NoDataError("no data found")
        assert str(exc) == "no data found"
        assert exc.error_code == ErrorCode.NO_DATA


class TestTimeoutError:
    """测试 TimeoutError 异常"""

    def test_creation(self):
        """测试创建"""
        exc = TimeoutError("request timeout")
        assert str(exc) == "request timeout"
        assert exc.error_code == ErrorCode.SOURCE_TIMEOUT


class TestRateLimitError:
    """测试 RateLimitError 异常"""

    def test_creation(self):
        """测试创建"""
        exc = RateLimitError("rate limit exceeded")
        assert str(exc) == "rate limit exceeded"
        assert exc.error_code == ErrorCode.SOURCE_RATE_LIMITED


class TestExceptionInheritance:
    """测试异常继承关系"""

    def test_data_source_error_inherits(self):
        """验证 DataSourceError 继承自 DataAccessException"""
        exc = DataSourceError("test")
        assert isinstance(exc, DataAccessException)
        assert isinstance(exc, Exception)

    def test_all_specific_errors_inherit(self):
        """验证所有具体错误类继承自 DataSourceError"""
        specific_errors = [
            SourceUnavailableError,
            NoDataError,
            TimeoutError,
            RateLimitError,
        ]
        for error_class in specific_errors:
            exc = error_class("test")
            assert isinstance(exc, DataSourceError)
            assert isinstance(exc, DataAccessException)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
