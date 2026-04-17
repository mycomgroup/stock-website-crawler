"""
test_data_sources.py
多数据源管理模块测试。

测试覆盖：
- DataSource 枚举
- DataQualityError 异常
- validate_valuation_data 估值数据验证
- validate_turnover_data 换手率数据验证
- retry_on_failure 重试装饰器
"""

import warnings

warnings.filterwarnings("ignore")

import pytest
import pandas as pd
import numpy as np
from unittest.mock import patch, MagicMock


class TestDataSourceEnum:
    """测试数据源枚举。"""

    def test_datasource_values(self):
        """测试枚举值。"""
        from jk2bt.analysis.factors.data_sources import DataSource

        assert DataSource.BAIDU.value == "baidu"
        assert DataSource.EASTMONEY.value == "eastmoney"
        assert DataSource.THS.value == "ths"
        assert DataSource.AKSHARE_DEFAULT.value == "akshare"

    def test_datasource_is_enum(self):
        """测试是Enum类型。"""
        from jk2bt.analysis.factors.data_sources import DataSource

        assert hasattr(DataSource, "__members__")


class TestDataQualityError:
    """测试数据质量异常。"""

    def test_raise_error(self):
        """测试抛出异常。"""
        from jk2bt.analysis.factors.data_sources import DataQualityError

        with pytest.raises(DataQualityError):
            raise DataQualityError("数据质量错误")

    def test_exception_message(self):
        """测试异常消息。"""
        from jk2bt.analysis.factors.data_sources import DataQualityError

        msg = "测试错误消息"
        try:
            raise DataQualityError(msg)
        except DataQualityError as e:
            assert str(e) == msg


class TestValidateValuationData:
    """测试估值数据验证。"""

    def test_valid_data(self):
        """测试有效数据。"""
        from jk2bt.analysis.factors.data_sources import validate_valuation_data

        df = pd.DataFrame(
            {
                "date": ["2023-01-01", "2023-01-02"],
                "market_cap": [1e10, 1.1e10],
                "pe_ratio": [10.0, 11.0],
                "pb_ratio": [1.5, 1.6],
            }
        )

        result = validate_valuation_data(df, "sh600519")

        assert isinstance(result, dict)
        assert result["is_valid"] == True

    def test_empty_data(self):
        """测试空数据。"""
        from jk2bt.analysis.factors.data_sources import validate_valuation_data

        result = validate_valuation_data(pd.DataFrame(), "sh600519")

        assert result["is_valid"] == False
        assert "empty_data" in result["issues"]

    def test_none_data(self):
        """测试None数据。"""
        from jk2bt.analysis.factors.data_sources import validate_valuation_data

        result = validate_valuation_data(None, "sh600519")

        assert result["is_valid"] == False

    def test_missing_required_columns(self):
        """测试缺少必需列。"""
        from jk2bt.analysis.factors.data_sources import validate_valuation_data

        df = pd.DataFrame(
            {
                "date": ["2023-01-01"],
                "market_cap": [1e10],
            }
        )

        result = validate_valuation_data(df, "sh600519")

        assert result["is_valid"] == False
        assert any("missing_col" in issue for issue in result["issues"])

    def test_negative_pe(self):
        """测试负PE。"""
        from jk2bt.analysis.factors.data_sources import validate_valuation_data

        df = pd.DataFrame(
            {
                "date": ["2023-01-01", "2023-01-02"],
                "market_cap": [1e10, 1e10],
                "pe_ratio": [-5.0, 10.0],
                "pb_ratio": [1.5, 1.6],
            }
        )

        result = validate_valuation_data(df, "sh600519")

        assert "negative_pe" in result["issues"]

    def test_extreme_pe(self):
        """测试极端PE。"""
        from jk2bt.analysis.factors.data_sources import validate_valuation_data

        df = pd.DataFrame(
            {
                "date": ["2023-01-01", "2023-01-02"],
                "market_cap": [1e10, 1e10],
                "pe_ratio": [5000.0, 10.0],
                "pb_ratio": [1.5, 1.6],
            }
        )

        result = validate_valuation_data(df, "sh600519")

        assert "extreme_pe" in result["issues"]

    def test_invalid_market_cap(self):
        """测试无效市值。"""
        from jk2bt.analysis.factors.data_sources import validate_valuation_data

        df = pd.DataFrame(
            {
                "date": ["2023-01-01", "2023-01-02"],
                "market_cap": [-1e10, 1e10],
                "pe_ratio": [10.0, 11.0],
                "pb_ratio": [1.5, 1.6],
            }
        )

        result = validate_valuation_data(df, "sh600519")

        assert "invalid_market_cap" in result["issues"]

    def test_high_missing_rate(self):
        """测试高缺失率。"""
        from jk2bt.analysis.factors.data_sources import validate_valuation_data

        df = pd.DataFrame(
            {
                "date": ["2023-01-01"] * 10,
                "market_cap": [np.nan] * 8 + [1e10, 1e10],
                "pe_ratio": [10.0] * 10,
                "pb_ratio": [1.5] * 10,
            }
        )

        result = validate_valuation_data(df, "sh600519")

        assert "high_missing_market_cap" in result["issues"]

    def test_strict_mode(self):
        """测试严格模式。"""
        from jk2bt.analysis.factors.data_sources import (
            validate_valuation_data,
            DataQualityError,
        )

        df = pd.DataFrame()

        with pytest.raises(DataQualityError):
            validate_valuation_data(df, "sh600519", strict=True)

    def test_data_count(self):
        """测试数据计数。"""
        from jk2bt.analysis.factors.data_sources import validate_valuation_data

        df = pd.DataFrame(
            {
                "date": ["2023-01-01", "2023-01-02", "2023-01-03"],
                "market_cap": [1e10, 1.1e10, 1.2e10],
                "pe_ratio": [10.0, 11.0, 12.0],
                "pb_ratio": [1.5, 1.6, 1.7],
            }
        )

        result = validate_valuation_data(df, "sh600519")

        assert result["data_count"] == 3


class TestValidateTurnoverData:
    """测试换手率数据验证。"""

    def test_valid_turnover(self):
        """测试有效换手率数据。"""
        from jk2bt.analysis.factors.data_sources import validate_turnover_data

        df = pd.DataFrame(
            {
                "date": ["2023-01-01", "2023-01-02"],
                "turnover_rate": [0.02, 0.03],
            }
        )

        result = validate_turnover_data(df, "sh600519")

        assert isinstance(result, dict)
        assert result["is_valid"] == True

    def test_empty_turnover(self):
        """测试空换手率数据。"""
        from jk2bt.analysis.factors.data_sources import validate_turnover_data

        result = validate_turnover_data(pd.DataFrame(), "sh600519")

        assert result["is_valid"] == False

    def test_negative_turnover(self):
        """测试负换手率。"""
        from jk2bt.analysis.factors.data_sources import validate_turnover_data

        df = pd.DataFrame(
            {
                "date": ["2023-01-01", "2023-01-02"],
                "turnover_rate": [-0.01, 0.03],
            }
        )

        result = validate_turnover_data(df, "sh600519")

        assert "negative_turnover" in result["issues"]

    def test_turnover_over_100(self):
        """测试换手率超过100%。"""
        from jk2bt.analysis.factors.data_sources import validate_turnover_data

        df = pd.DataFrame(
            {
                "date": ["2023-01-01", "2023-01-02"],
                "turnover_rate": [1.5, 0.03],
            }
        )

        result = validate_turnover_data(df, "sh600519")

        assert "turnover_over_100" in result["issues"]


class TestRetryOnFailure:
    """测试重试装饰器。"""

    def test_retry_success(self):
        """测试重试成功。"""
        from jk2bt.analysis.factors.data_sources import retry_on_failure

        call_count = 0

        @retry_on_failure(max_retries=3)
        def succeed_after(count):
            nonlocal call_count
            call_count += 1
            return "success"

        result = succeed_after(1)

        assert result == "success"
        assert call_count == 1

    def test_retry_eventually_success(self):
        """测试最终成功。"""
        from jk2bt.analysis.factors.data_sources import retry_on_failure

        call_count = 0

        @retry_on_failure(max_retries=3, retry_delay=0.01)
        def fail_twice():
            nonlocal call_count
            call_count += 1
            if call_count < 3:
                raise ValueError("temporary error")
            return "success"

        result = fail_twice()

        assert result == "success"
        assert call_count == 3

    def test_retry_all_fail(self):
        """测试全部失败。"""
        from jk2bt.analysis.factors.data_sources import (
            retry_on_failure,
            DataSourceError,
        )

        @retry_on_failure(max_retries=3, retry_delay=0.01)
        def always_fail():
            raise ValueError("always fail")

        with pytest.raises(DataSourceError):
            always_fail()


class TestDataSourcesExport:
    """测试模块导出。"""

    def test_all_exports(self):
        """测试所有导出。"""
        from jk2bt.analysis.factors.data_sources import (
            DataSource,
            DataQualityError,
            validate_valuation_data,
            validate_turnover_data,
            retry_on_failure,
        )

        assert DataSource is not None
        assert callable(validate_valuation_data)
        assert callable(validate_turnover_data)
        assert callable(retry_on_failure)
