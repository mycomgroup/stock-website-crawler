"""
test_result.py
RobustResult 统一结果包装类测试
"""

import pytest
from jk2bt.utils.result import RobustResult


class TestRobustResultCreation:
    """测试 RobustResult 创建"""

    def test_create_success_result(self):
        """测试创建成功结果"""
        result = RobustResult(success=True, data={"key": "value"})
        assert result.success is True
        assert result.data == {"key": "value"}
        assert result.error is None

    def test_create_failure_result(self):
        """测试创建失败结果"""
        result = RobustResult(
            success=False, error="Something went wrong", error_code="E001"
        )
        assert result.success is False
        assert result.error == "Something went wrong"
        assert result.error_code == "E001"

    def test_create_with_source(self):
        """测试带数据源标识"""
        result = RobustResult(success=True, data=[1, 2, 3], source="akshare")
        assert result.source == "akshare"


class TestRobustResultBool:
    """测试布尔转换"""

    def test_bool_true_for_success(self):
        """测试成功结果布尔值为 True"""
        result = RobustResult(success=True, data=[1, 2, 3])
        assert bool(result) is True

    def test_bool_false_for_failure(self):
        """测试失败结果布尔值为 False"""
        result = RobustResult(success=False, error="error")
        assert bool(result) is False


class TestRobustResultRepr:
    """测试字符串表示"""

    def test_repr_success(self):
        """测试成功结果的 __repr__"""
        result = RobustResult(success=True, data=[1, 2, 3])
        repr_str = repr(result)
        assert "success=True" in repr_str
        assert "list" in repr_str

    def test_repr_failure(self):
        """测试失败结果的 __repr__"""
        result = RobustResult(success=False, error="test error")
        repr_str = repr(result)
        assert "success=False" in repr_str
        assert "test error" in repr_str


class TestRobustResultGetData:
    """测试安全数据获取"""

    def test_get_data_success(self):
        """测试成功时获取数据"""
        result = RobustResult(success=True, data={"key": "value"})
        assert result.get_data() == {"key": "value"}

    def test_get_data_failure_returns_default(self):
        """测试失败时返回默认值"""
        result = RobustResult(success=False, error="error")
        assert result.get_data() is None
        assert result.get_data(default="fallback") == "fallback"


class TestRobustResultFactory:
    """测试工厂方法"""

    def test_ok_factory(self):
        """测试 ok 工厂方法"""
        result = RobustResult.ok(data=[1, 2, 3])
        assert result.success is True
        assert result.data == [1, 2, 3]

    def test_ok_factory_with_source(self):
        """测试 ok 带数据源"""
        result = RobustResult.ok(data=[1, 2, 3], source="sina")
        assert result.source == "sina"

    def test_fail_factory(self):
        """测试 fail 工厂方法"""
        result = RobustResult.fail(error="Failed to fetch", error_code="E100")
        assert result.success is False
        assert result.error == "Failed to fetch"
        assert result.error_code == "E100"

    def test_fail_factory_with_source(self):
        """测试 fail 带数据源"""
        result = RobustResult.fail(error="error", source="tushare")
        assert result.source == "tushare"


class TestRobustResultChaining:
    """测试结果链式处理"""

    def test_or_else_pattern(self):
        """测试 or else 模式"""
        success_result = RobustResult.ok(data=[1, 2, 3])
        fail_result = RobustResult.fail(error="error")

        default_data = success_result.get_data() or [4, 5, 6]
        assert default_data == [1, 2, 3]

        default_data = fail_result.get_data() or [4, 5, 6]
        assert default_data == [4, 5, 6]
