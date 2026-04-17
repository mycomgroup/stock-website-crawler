"""
utils/result.py
统一的结果包装类，用于封装 API 调用的成功/失败状态和数据。

避免在多个模块中重复定义相同的类。
"""

from typing import Any, Optional


class RobustResult:
    """封装 API 调用结果的统一容器。

    属性:
        success: 调用是否成功
        data: 成功时返回的数据
        error: 失败时的错误信息
        error_code: 错误码（可选）
        source: 数据来源标识（可选）
    """

    def __init__(
        self,
        success: bool,
        data: Any = None,
        error: Optional[str] = None,
        error_code: Optional[str] = None,
        source: Optional[str] = None,
        reason: Optional[str] = None,
    ):
        self.success = success
        self.data = data
        self.error = error or reason
        self.reason = self.error
        self.error_code = error_code
        self.source = source

    def __bool__(self) -> bool:
        return self.success

    def __repr__(self) -> str:
        if self.success:
            return f"RobustResult(success=True, data={type(self.data).__name__})"
        return f"RobustResult(success=False, error={self.error!r})"

    def get_data(self, default=None):
        """安全获取数据，失败时返回默认值。"""
        return self.data if self.success else default

    @classmethod
    def ok(cls, data=None, source=None):
        """创建成功结果。"""
        return cls(success=True, data=data, source=source)

    @classmethod
    def fail(cls, error, error_code=None, source=None):
        """创建失败结果。"""
        return cls(success=False, error=error, error_code=error_code, source=source)


__all__ = ["RobustResult"]
