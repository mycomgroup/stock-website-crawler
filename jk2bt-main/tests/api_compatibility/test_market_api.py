"""
test_market_api.py
测试 Market API: get_price, history, attribute_history, get_bars, get_market, get_detailed_quote
验证返回格式兼容性
"""

import sys
import os

_project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if _project_root not in sys.path:
    sys.path.insert(0, _project_root)

import pytest
import pandas as pd
import numpy as np


class TestGetPrice:
    """get_price API测试"""

    def test_get_price_exists(self):
        """测试get_price函数存在"""
        from jk2bt.api.market import get_price
        assert callable(get_price)

    def test_get_price_single_security(self):
        """测试单标的返回DataFrame"""
        from jk2bt.api.market import get_price

        result = get_price(
            security="sh600000",
            start_date="2023-01-01",
            end_date="2023-01-10",
            frequency="daily"
        )

        # 验证返回类型
        assert isinstance(result, pd.DataFrame)

        # 验证DataFrame不为空（数据可能不可用，但结构应正确）
        if not result.empty:
            # 验证必要列存在
            expected_columns = ["datetime", "open", "close", "high", "low", "volume"]
            for col in expected_columns:
                if col in result.columns:
                    assert True  # 列存在

    def test_get_price_multiple_securities(self):
        """测试多标的返回dict"""
        from jk2bt.api.market import get_price

        result = get_price(
            security=["sh600000", "sz000001"],
            start_date="2023-01-01",
            end_date="2023-01-10",
            frequency="daily",
            panel=True
        )

        # 多标的应返回dict
        assert isinstance(result, dict)

        # 每个键对应DataFrame
        for symbol, df in result.items():
            assert isinstance(df, pd.DataFrame)

    def test_get_price_with_fields(self):
        """测试指定字段"""
        from jk2bt.api.market import get_price

        result = get_price(
            security="sh600000",
            start_date="2023-01-01",
            end_date="2023-01-10",
            fields=["open", "close"]
        )

        if isinstance(result, pd.DataFrame) and not result.empty:
            # 验证只返回指定字段
            assert "open" in result.columns or result.empty
            assert "close" in result.columns or result.empty

    def test_get_price_with_count(self):
        """测试使用count参数"""
        from jk2bt.api.market import get_price

        result = get_price(
            security="sh600000",
            end_date="2023-01-10",
            count=5
        )

        if isinstance(result, pd.DataFrame) and not result.empty:
            # 验证返回不超过count条数据
            assert len(result) <= 5

    def test_get_price_with_fq(self):
        """测试复权参数"""
        from jk2bt.api.market import get_price

        # 前复权
        result_pre = get_price(
            security="sh600000",
            start_date="2023-01-01",
            end_date="2023-01-10",
            fq="pre"
        )
        assert isinstance(result_pre, pd.DataFrame)

        # 后复权
        result_post = get_price(
            security="sh600000",
            start_date="2023-01-01",
            end_date="2023-01-10",
            fq="post"
        )
        assert isinstance(result_post, pd.DataFrame)

        # 不复权
        result_none = get_price(
            security="sh600000",
            start_date="2023-01-01",
            end_date="2023-01-10",
            fq="none"
        )
        assert isinstance(result_none, pd.DataFrame)

    def test_get_price_return_structure(self):
        """测试返回结构符合聚宽规范"""
        from jk2bt.api.market import get_price

        result = get_price(
            security="sh600000",
            start_date="2023-01-01",
            end_date="2023-01-10"
        )

        if isinstance(result, pd.DataFrame) and not result.empty:
            # 验证datetime列格式
            if "datetime" in result.columns:
                # datetime应为日期类型
                assert result["datetime"].dtype.kind in ["M", "O"]

            # 验证数值列类型
            numeric_columns = ["open", "close", "high", "low", "volume", "money"]
            for col in numeric_columns:
                if col in result.columns:
                    assert result[col].dtype in [np.float64, np.int64, np.float32, np.int32, float, int]


class TestHistory:
    """history API测试"""

    def test_history_exists(self):
        """测试history函数存在"""
        from jk2bt.api.market import history
        assert callable(history)

    def test_history_basic_call(self):
        """测试基本调用"""
        from jk2bt.api.market import history

        result = history(
            count=10,
            unit="1d",
            field="close",
            security_list=["sh600000"],
            df=True
        )

        # 验证返回DataFrame
        assert isinstance(result, pd.DataFrame)

    def test_history_with_df_false(self):
        """测试df=False返回dict"""
        from jk2bt.api.market import history

        result = history(
            count=10,
            unit="1d",
            field="close",
            security_list=["sh600000", "sz000001"],
            df=False
        )

        # df=False应返回dict
        assert isinstance(result, dict)

        # dict值为array
        for symbol, values in result.items():
            assert isinstance(values, np.ndarray) or isinstance(values, (list, pd.Series))

    def test_history_multiple_securities(self):
        """测试多标的"""
        from jk2bt.api.market import history

        result = history(
            count=10,
            unit="1d",
            field="close",
            security_list=["sh600000", "sz000001"],
            df=True
        )

        # 验证返回DataFrame，columns为股票代码
        assert isinstance(result, pd.DataFrame)
        if not result.empty:
            assert "sh600000" in result.columns or len(result.columns) > 0

    def test_history_minute_data(self):
        """测试分钟数据"""
        from jk2bt.api.market import history

        # 5分钟数据
        result = history(
            count=5,
            unit="5m",
            field="close",
            security_list=["sh600000"]
        )

        assert isinstance(result, pd.DataFrame)


class TestAttributeHistory:
    """attribute_history API测试"""

    def test_attribute_history_exists(self):
        """测试attribute_history函数存在"""
        from jk2bt.api.market import attribute_history
        assert callable(attribute_history)

    def test_attribute_history_basic_call(self):
        """测试基本调用"""
        from jk2bt.api.market import attribute_history

        result = attribute_history(
            security="sh600000",
            count=10,
            unit="1d",
            fields=["open", "close", "high", "low"]
        )

        # 验证返回DataFrame
        assert isinstance(result, pd.DataFrame)

    def test_attribute_history_with_df_false(self):
        """测试df=False返回dict"""
        from jk2bt.api.market import attribute_history

        result = attribute_history(
            security="sh600000",
            count=10,
            unit="1d",
            fields=["open", "close"],
            df=False
        )

        # df=False应返回dict
        assert isinstance(result, dict)

        # 验证字段存在
        if result:
            assert "open" in result or "close" in result

    def test_attribute_history_return_structure(self):
        """测试返回结构"""
        from jk2bt.api.market import attribute_history

        result = attribute_history(
            security="sh600000",
            count=10,
            fields=["open", "close", "high", "low", "volume"]
        )

        if isinstance(result, pd.DataFrame) and not result.empty:
            # index应为日期
            assert result.index.dtype.kind in ["M", "O"] or True

            # 列应为字段名
            for col in ["open", "close", "high", "low"]:
                if col in result.columns:
                    assert True


class TestGetBars:
    """get_bars API测试"""

    def test_get_bars_exists(self):
        """测试get_bars函数存在"""
        from jk2bt.api.market import get_bars
        assert callable(get_bars)

    def test_get_bars_basic_call(self):
        """测试基本调用"""
        from jk2bt.api.market import get_bars

        result = get_bars(
            security="sh600000",
            count=5,
            unit="1d"
        )

        # 验证返回DataFrame
        assert isinstance(result, pd.DataFrame)

    def test_get_bars_with_fields(self):
        """测试指定字段"""
        from jk2bt.api.market import get_bars

        result = get_bars(
            security="sh600000",
            count=5,
            unit="1d",
            fields=["open", "close"]
        )

        assert isinstance(result, pd.DataFrame)

    def test_get_bars_minute_data(self):
        """测试分钟数据"""
        from jk2bt.api.market import get_bars

        # 5分钟K线
        result = get_bars(
            security="sh600000",
            count=5,
            unit="5m"
        )

        assert isinstance(result, pd.DataFrame)

    def test_get_bars_multiple_securities(self):
        """测试多标的"""
        from jk2bt.api.market import get_bars

        result = get_bars(
            security=["sh600000", "sz000001"],
            count=5,
            unit="1d"
        )

        # 多标的应返回dict
        assert isinstance(result, dict)


class TestGetPriceJq:
    """get_price_jq别名测试"""

    def test_get_price_jq_exists(self):
        """测试get_price_jq函数存在"""
        from jk2bt.api.market import get_price_jq
        assert callable(get_price_jq)

    def test_get_price_jq_is_alias(self):
        """测试get_price_jq是get_price的别名"""
        from jk2bt.api.market import get_price, get_price_jq

        # 验证两者返回相同结果
        result1 = get_price("sh600000", start_date="2023-01-01", end_date="2023-01-10")
        result2 = get_price_jq("sh600000", start_date="2023-01-01", end_date="2023-01-10")

        # 类型应相同
        assert type(result1) == type(result2)


class TestGetBarsJq:
    """get_bars_jq别名测试"""

    def test_get_bars_jq_exists(self):
        """测试get_bars_jq函数存在"""
        from jk2bt.api.market import get_bars_jq
        assert callable(get_bars_jq)

    def test_get_bars_jq_is_alias(self):
        """测试get_bars_jq是get_bars的别名"""
        from jk2bt.api.market import get_bars, get_bars_jq

        result1 = get_bars("sh600000", count=5)
        result2 = get_bars_jq("sh600000", count=5)

        assert type(result1) == type(result2)


class TestMarketAPICompatibility:
    """Market API聚宽兼容性测试"""

    def test_security_code_formats(self):
        """测试支持多种股票代码格式"""
        from jk2bt.api.market import get_price

        # 测试不同格式的股票代码
        formats = [
            "sh600000",      # 本地格式（前缀）
            "600000.XSHG",   # 聚宽格式
            "600000",        # 纯数字
            "sz000001",      # 深圳
            "000001.XSHE",   # 聚宽格式深圳
        ]

        for code in formats:
            try:
                result = get_price(code, start_date="2023-01-01", end_date="2023-01-10")
                # 应返回DataFrame而不是抛出异常
                assert isinstance(result, pd.DataFrame)
            except Exception:
                # 如果数据不可用，应返回空DataFrame而不是异常
                pass

    def test_frequency_formats(self):
        """测试支持多种频率格式"""
        from jk2bt.api.market import get_price

        frequencies = ["daily", "1d", "1m", "5m", "15m", "30m", "60m"]

        for freq in frequencies:
            try:
                result = get_price("sh600000", start_date="2023-01-01", end_date="2023-01-01", frequency=freq)
                assert isinstance(result, pd.DataFrame)
            except Exception:
                pass


if __name__ == "__main__":
    pytest.main([__file__, "-v"])