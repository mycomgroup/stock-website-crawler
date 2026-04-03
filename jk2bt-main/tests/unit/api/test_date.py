"""
tests/unit/api/test_date.py
日期工具 API 单元测试

测试覆盖：
- transform_date：多种输入格式转换
- get_shifted_date：自然日偏移（'D' 类型，不依赖网络）
- is_trade_date / get_trade_dates_between / count_trade_dates_between：导入可调用性
- clear_trade_days_cache：缓存清除
- 模块导入与 __all__ 完整性
"""

import pytest
import datetime
import pandas as pd
import sys
import os

sys.path.insert(
    0,
    os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "src"),
)


class TestDateImports:
    """日期函数导入测试"""

    def test_transform_date_importable(self):
        from jk2bt.api.date import transform_date
        assert callable(transform_date)

    def test_get_shifted_date_importable(self):
        from jk2bt.api.date import get_shifted_date
        assert callable(get_shifted_date)

    def test_get_previous_trade_date_importable(self):
        from jk2bt.api.date import get_previous_trade_date
        assert callable(get_previous_trade_date)

    def test_get_next_trade_date_importable(self):
        from jk2bt.api.date import get_next_trade_date
        assert callable(get_next_trade_date)

    def test_is_trade_date_importable(self):
        from jk2bt.api.date import is_trade_date
        assert callable(is_trade_date)

    def test_get_trade_dates_between_importable(self):
        from jk2bt.api.date import get_trade_dates_between
        assert callable(get_trade_dates_between)

    def test_count_trade_dates_between_importable(self):
        from jk2bt.api.date import count_trade_dates_between
        assert callable(count_trade_dates_between)

    def test_clear_trade_days_cache_importable(self):
        from jk2bt.api.date import clear_trade_days_cache
        assert callable(clear_trade_days_cache)


class TestDateFromApiInit:
    """从 src.api 顶层导入日期函数"""

    def test_transform_date_from_api(self):
        from jk2bt.api import transform_date
        assert callable(transform_date)

    def test_get_shifted_date_from_api(self):
        from jk2bt.api import get_shifted_date
        assert callable(get_shifted_date)

    def test_is_trade_date_from_api(self):
        from jk2bt.api import is_trade_date
        assert callable(is_trade_date)


class TestTransformDate:
    """transform_date 格式转换测试（纯本地，不依赖网络）"""

    def test_string_dash_to_date(self):
        from jk2bt.api.date_api import transform_date
        result = transform_date("2023-01-05", "date")
        assert result == datetime.date(2023, 1, 5)

    def test_string_slash_to_date(self):
        from jk2bt.api.date_api import transform_date
        result = transform_date("2023/01/05", "date")
        assert result == datetime.date(2023, 1, 5)

    def test_string_compact_to_date(self):
        from jk2bt.api.date_api import transform_date
        result = transform_date("20230105", "date")
        assert result == datetime.date(2023, 1, 5)

    def test_date_object_to_str(self):
        from jk2bt.api.date_api import transform_date
        result = transform_date(datetime.date(2023, 1, 5), "str")
        assert result == "2023-01-05"

    def test_datetime_object_to_date(self):
        from jk2bt.api.date_api import transform_date
        result = transform_date(datetime.datetime(2023, 1, 5, 10, 30), "date")
        assert result == datetime.date(2023, 1, 5)

    def test_timestamp_to_date(self):
        from jk2bt.api.date_api import transform_date
        result = transform_date(pd.Timestamp("2023-01-05"), "date")
        assert result == datetime.date(2023, 1, 5)

    def test_to_datetime_output(self):
        from jk2bt.api.date_api import transform_date
        result = transform_date("2023-01-05", "datetime")
        assert isinstance(result, datetime.datetime)
        assert result.year == 2023 and result.month == 1 and result.day == 5

    def test_to_timestamp_output(self):
        from jk2bt.api.date_api import transform_date
        result = transform_date("2023-01-05", "timestamp")
        assert isinstance(result, pd.Timestamp)

    def test_invalid_string_raises(self):
        from jk2bt.api.date_api import transform_date
        with pytest.raises(ValueError):
            transform_date("not-a-date", "date")


class TestGetShiftedDateNaturalDay:
    """get_shifted_date 自然日偏移测试（不依赖网络）"""

    def test_forward_natural_days(self):
        from jk2bt.api.date_api import get_shifted_date
        result = get_shifted_date("2023-01-05", 5, "D")
        assert result == datetime.date(2023, 1, 10)

    def test_backward_natural_days(self):
        from jk2bt.api.date_api import get_shifted_date
        result = get_shifted_date("2023-01-10", -5, "D")
        assert result == datetime.date(2023, 1, 5)

    def test_zero_shift(self):
        from jk2bt.api.date_api import get_shifted_date
        result = get_shifted_date("2023-01-05", 0, "D")
        assert result == datetime.date(2023, 1, 5)

    def test_cross_month(self):
        from jk2bt.api.date_api import get_shifted_date
        result = get_shifted_date("2023-01-28", 5, "D")
        assert result == datetime.date(2023, 2, 2)


class TestClearCache:
    """缓存清除测试"""

    def test_clear_trade_days_cache_no_error(self):
        from jk2bt.api.date_api import clear_trade_days_cache
        # 调用不应抛出异常
        clear_trade_days_cache()


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
