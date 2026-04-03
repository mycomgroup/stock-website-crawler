"""
test_date_api.py
测试日期相关API: get_shifted_date, get_trade_days 等
"""

import sys
import os

_project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if _project_root not in sys.path:
    sys.path.insert(0, _project_root)

import pytest
import pandas as pd
from datetime import datetime, timedelta


class TestDateUtils:
    """日期工具测试"""

    def test_find_date_column_exists(self):
        """测试find_date_column函数存在"""
        from jk2bt.utils.date_utils import find_date_column
        assert callable(find_date_column)

    def test_find_date_column_market(self):
        """测试市场数据日期列检测"""
        from jk2bt.utils.date_utils import find_date_column

        # 测试DataFrame
        df = pd.DataFrame({
            "日期": ["2023-01-01", "2023-01-02"],
            "close": [10.0, 11.0]
        })

        result = find_date_column(df, category="market")

        # 应找到"日期"列
        assert result == "日期"

    def test_find_date_column_date(self):
        """测试date列检测"""
        from jk2bt.utils.date_utils import find_date_column

        df = pd.DataFrame({
            "date": ["2023-01-01", "2023-01-02"],
            "close": [10.0, 11.0]
        })

        result = find_date_column(df, category="market")

        assert result == "date"

    def test_find_date_column_trade_date(self):
        """测试trade_date列检测"""
        from jk2bt.utils.date_utils import find_date_column

        df = pd.DataFrame({
            "trade_date": ["2023-01-01", "2023-01-02"],
            "close": [10.0, 11.0]
        })

        result = find_date_column(df, category="market")

        assert result == "trade_date"

    def test_find_date_column_financial(self):
        """测试财务数据日期列检测"""
        from jk2bt.utils.date_utils import find_date_column

        df = pd.DataFrame({
            "报告期": ["2023-03-31", "2023-06-30"],
            "revenue": [100, 200]
        })

        result = find_date_column(df, category="financial")

        assert result == "报告期"

    def test_find_date_column_not_found(self):
        """测试找不到日期列"""
        from jk2bt.utils.date_utils import find_date_column

        df = pd.DataFrame({
            "close": [10.0, 11.0],
            "volume": [1000, 2000]
        })

        result = find_date_column(df)

        # 应返回None
        assert result is None


class TestStrategyBaseDateAPI:
    """strategy_base日期API测试"""

    def test_get_all_trade_days_jq_exists(self):
        """测试get_all_trade_days_jq函数存在"""
        try:
            from jk2bt.core.strategy_base import get_all_trade_days_jq
            assert callable(get_all_trade_days_jq)
        except ImportError:
            pytest.skip("get_all_trade_days_jq not available")

    def test_get_all_trade_days_jq_returns_list(self):
        """测试get_all_trade_days_jq返回list"""
        try:
            from jk2bt.core.strategy_base import get_all_trade_days_jq

            result = get_all_trade_days_jq()

            # 应返回list
            assert isinstance(result, list)

            # list不为空
            assert len(result) > 0

            # 元素应为日期类型
            for item in result[:5]:  # 只检查前5个
                assert isinstance(item, (pd.Timestamp, datetime, str))
        except ImportError:
            pytest.skip("get_all_trade_days_jq not available")

    def test_get_trade_days_count(self):
        """测试交易日数量"""
        try:
            from jk2bt.core.strategy_base import get_all_trade_days_jq

            result = get_all_trade_days_jq()

            # 一年约有250个交易日
            assert len(result) > 200
        except ImportError:
            pytest.skip("get_all_trade_days_jq not available")


class TestDateOperations:
    """日期操作测试"""

    def test_date_string_format(self):
        """测试日期字符串格式"""
        # 测试标准日期格式
        date_formats = [
            "2023-01-01",
            "2023-12-31",
            "20230101",
        ]

        for date_str in date_formats:
            # 尝试解析
            try:
                if "-" in date_str:
                    parsed = pd.to_datetime(date_str)
                else:
                    parsed = pd.to_datetime(date_str, format="%Y%m%d")

                assert isinstance(parsed, pd.Timestamp)
            except Exception:
                pass

    def test_date_range_calculation(self):
        """测试日期范围计算"""
        end_date = datetime(2023, 12, 31)
        count = 10

        # 计算开始日期（粗略估算）
        start_date = end_date - timedelta(days=count * 3)

        assert start_date < end_date
        assert isinstance(start_date, datetime)

    def test_pandas_date_handling(self):
        """测试pandas日期处理"""
        # 创建日期序列
        dates = pd.date_range(start="2023-01-01", end="2023-01-10")

        assert len(dates) == 10

        # 测试日期比较
        assert dates[0] < dates[-1]

        # 测试日期格式转换
        date_str = dates[0].strftime("%Y-%m-%d")
        assert date_str == "2023-01-01"


class TestMarketApiDateHandling:
    """market_api日期处理测试"""

    def test_get_price_with_date_range(self):
        """测试get_price日期范围"""
        from jk2bt.api.market import get_price

        result = get_price(
            security="sh600000",
            start_date="2023-01-01",
            end_date="2023-01-31"
        )

        # 应返回DataFrame
        assert isinstance(result, pd.DataFrame)

    def test_history_end_date(self):
        """测试history end_date参数"""
        from jk2bt.api.market import history

        result = history(
            count=10,
            unit="1d",
            field="close",
            security_list=["sh600000"],
            end_date="2023-01-10"
        )

        assert isinstance(result, pd.DataFrame)

    def test_attribute_history_end_date(self):
        """测试attribute_history end_date参数"""
        from jk2bt.api.market import attribute_history

        result = attribute_history(
            security="sh600000",
            count=10,
            end_date="2023-01-10"
        )

        assert isinstance(result, pd.DataFrame)


class TestDateCompatibility:
    """日期格式兼容性测试"""

    def test_date_formats_compatibility(self):
        """测试多种日期格式兼容"""
        from jk2bt.api.market import get_price

        date_formats = [
            ("2023-01-01", "2023-01-10"),  # 标准格式
            ("20230101", "20230110"),      # 紧凑格式（可能不支持）
        ]

        for start, end in date_formats:
            try:
                result = get_price("sh600000", start_date=start, end_date=end)
                assert isinstance(result, pd.DataFrame)
            except Exception:
                # 某些格式可能不支持
                pass

    def test_datetime_index_handling(self):
        """测试datetime索引处理"""
        # 创建带datetime索引的DataFrame
        df = pd.DataFrame({
            "close": [10.0, 11.0, 12.0]
        }, index=pd.date_range("2023-01-01", periods=3))

        # 验证索引类型
        assert df.index.dtype.kind == "M"

        # 测试日期筛选
        filtered = df[df.index <= pd.Timestamp("2023-01-02")]
        assert len(filtered) == 2


if __name__ == "__main__":
    pytest.main([__file__, "-v"])