"""Error codes and exception hierarchy for data access layer.

Provides structured error handling with error codes for better
error classification and reporting.
"""

from enum import Enum
from typing import Optional


class ErrorCode(Enum):
    """Standardized error codes for data access operations."""

    # Source-related errors
    SOURCE_UNAVAILABLE = "SOURCE_UNAVAILABLE"
    SOURCE_TIMEOUT = "SOURCE_TIMEOUT"
    SOURCE_RATE_LIMITED = "SOURCE_RATE_LIMITED"
    SOURCE_AUTH_FAILED = "SOURCE_AUTH_FAILED"

    # Data-related errors
    NO_DATA = "NO_DATA"
    INVALID_DATA = "INVALID_DATA"
    DATA_FORMAT_ERROR = "DATA_FORMAT_ERROR"
    MISSING_COLUMNS = "MISSING_COLUMNS"

    # Cache-related errors
    CACHE_MISS = "CACHE_MISS"
    CACHE_CORRUPTED = "CACHE_CORRUPTED"

    # Validation errors
    INVALID_SYMBOL = "INVALID_SYMBOL"
    INVALID_DATE_RANGE = "INVALID_DATE_RANGE"
    INVALID_PARAMETER = "INVALID_PARAMETER"

    # System errors
    INTERNAL_ERROR = "INTERNAL_ERROR"
    NOT_IMPLEMENTED = "NOT_IMPLEMENTED"


class DataAccessException(Exception):
    """Base exception for all data access errors."""

    def __init__(
        self,
        message: str,
        error_code: Optional[ErrorCode] = None,
        source: Optional[str] = None,
        symbol: Optional[str] = None,
    ):
        super().__init__(message)
        self.error_code = error_code
        self.source = source
        self.symbol = symbol

    def to_dict(self) -> dict:
        """Convert exception to dictionary for logging/serialization."""
        return {
            "error_code": self.error_code.value if self.error_code else None,
            "message": str(self),
            "source": self.source,
            "symbol": self.symbol,
        }


class DataSourceError(DataAccessException):
    """Generic data source error (backward compatible alias)."""

    def __init__(
        self,
        message: str,
        error_code: Optional[ErrorCode] = None,
        source: Optional[str] = None,
        symbol: Optional[str] = None,
    ):
        super().__init__(message, error_code, source, symbol)


class SourceUnavailableError(DataSourceError):
    """Raised when a data source is unavailable or unreachable."""

    def __init__(
        self,
        message: str,
        error_code: ErrorCode = ErrorCode.SOURCE_UNAVAILABLE,
        source: Optional[str] = None,
        symbol: Optional[str] = None,
    ):
        super().__init__(message, error_code, source, symbol)


class NoDataError(DataSourceError):
    """Raised when no data is available for the requested query."""

    def __init__(
        self,
        message: str,
        error_code: ErrorCode = ErrorCode.NO_DATA,
        source: Optional[str] = None,
        symbol: Optional[str] = None,
    ):
        super().__init__(message, error_code, source, symbol)


class TimeoutError(DataSourceError):
    """Raised when a data source request times out."""

    def __init__(
        self,
        message: str,
        error_code: ErrorCode = ErrorCode.SOURCE_TIMEOUT,
        source: Optional[str] = None,
        symbol: Optional[str] = None,
    ):
        super().__init__(message, error_code, source, symbol)


class RateLimitError(DataSourceError):
    """Raised when a data source rate limit is exceeded."""

    def __init__(
        self,
        message: str,
        error_code: ErrorCode = ErrorCode.SOURCE_RATE_LIMITED,
        source: Optional[str] = None,
        symbol: Optional[str] = None,
    ):
        super().__init__(message, error_code, source, symbol)


__all__ = [
    "ErrorCode",
    "DataAccessException",
    "DataSourceError",
    "SourceUnavailableError",
    "NoDataError",
    "TimeoutError",
    "RateLimitError",
]
