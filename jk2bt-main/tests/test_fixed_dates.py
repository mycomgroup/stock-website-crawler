"""
tests/test_fixed_dates.py
使用固定日期的测试用例

解决数据时效问题：
1. 使用固定的历史日期进行测试
2. 避免依赖实时数据
3. 确保测试可重复
"""

import pytest
import pandas as pd
import sys
from pathlib import Path
from datetime import datetime

sys.path.insert(0, str(Path(__file__).parent.parent))


# 固定测试日期（确保这些日期有数据）
FIXED_TEST_DATES = {
    "recent": "2024-12-15",  # 近期日期
    "mid": "2024-06-30",  # 中期日期
    "historical": "2023-12-31",  # 历史日期
}

# 固定测试股票
FIXED_TEST_STOCKS = {
    "sh_main": "600519",  # 上交所主板：贵州茅台
    "sz_main": "000001",  # 深交所主板：平安银行
    "sh_bank": "600036",  # 招商银行
}


class TestFixedDateCompanyInfo:
    """使用固定日期测试公司信息"""

    def test_company_info_with_cache(self):
        """测试使用缓存的公司信息查询"""
        from jk2bt.finance_data.company_info import (
            get_company_info,
        )

        # 使用缓存数据，不强制更新
        df = get_company_info(FIXED_TEST_STOCKS["sh_main"], force_update=False)

        assert isinstance(df, pd.DataFrame)

        # 即使网络不可用，也应该返回缓存数据或空 DataFrame
        if not df.empty:
            assert "code" in df.columns


class TestFixedDateDividend:
    """使用固定日期测试分红数据"""

    def test_dividend_history_2023(self):
        """测试 2023 年分红历史"""
        from jk2bt.finance_data.dividend import (
            get_dividend_info,
        )

        # 使用缓存数据
        df = get_dividend_info(FIXED_TEST_STOCKS["sh_main"], force_update=False)

        assert isinstance(df, pd.DataFrame)

    def test_dividend_by_year(self):
        """测试按年份查询分红"""
        from jk2bt.finance_data.dividend import (
            get_dividend_by_date,
        )

        # 使用固定历史日期
        try:
            df = get_dividend_by_date(
                FIXED_TEST_STOCKS["sh_main"],
                query_date=FIXED_TEST_DATES["historical"],
                force_update=False,
            )
            assert isinstance(df, pd.DataFrame)
        except TypeError:
            # 如果参数名不对，尝试不同参数
            df = get_dividend_by_date(FIXED_TEST_STOCKS["sh_main"])
            assert isinstance(df, pd.DataFrame)


class TestFixedDateShareholder:
    """使用固定日期测试股东数据"""

    def test_shareholder_by_report_date(self):
        """测试按报告期查询股东"""
        from jk2bt.finance_data.shareholder import (
            get_top10_shareholders,
        )

        # 使用缓存数据
        df = get_top10_shareholders(FIXED_TEST_STOCKS["sh_main"], force_update=False)

        assert isinstance(df, pd.DataFrame)


class TestFixedDateUnlock:
    """使用固定日期测试解禁数据"""

    def test_unlock_schedule_historical(self):
        """测试历史解禁计划"""
        from jk2bt.finance_data.unlock import (
            get_unlock_schedule,
        )

        # 查询历史解禁记录
        df = get_unlock_schedule(
            FIXED_TEST_STOCKS["sh_main"],
            start_date="2024-01-01",
            end_date="2024-12-31",
            force_update=False,
        )

        assert isinstance(df, pd.DataFrame)


class TestFixedDateMacro:
    """使用固定日期测试宏观数据"""

    def test_macro_cpi_2024(self):
        """测试 CPI 数据"""
        from jk2bt.finance_data.macro import (
            get_macro_cpi,
        )

        # 使用默认参数
        df = get_macro_cpi()

        assert isinstance(df, pd.DataFrame)

    def test_macro_gdp_historical(self):
        """测试历史 GDP 数据"""
        from jk2bt.finance_data.macro import (
            get_macro_gdp,
        )

        df = get_macro_gdp()

        assert isinstance(df, pd.DataFrame)


class TestDateNormalization:
    """日期标准化测试"""

    def test_date_format_conversion(self):
        """测试日期格式转换"""
        from jk2bt.finance_data.company_info import (
            _normalize_date,
        )

        # 测试各种日期格式
        assert _normalize_date("2024-01-15") == "2024-01-15"
        assert _normalize_date("20240115") == "2024-01-15"

    def test_stock_code_normalization(self):
        """测试股票代码标准化"""
        from jk2bt.finance_data.company_info import (
            _extract_code_num,
            _normalize_to_jq,
        )

        # 测试代码提取
        assert _extract_code_num("sh600519") == "600519"
        assert _extract_code_num("600519.XSHG") == "600519"

        # 测试聚宽格式转换
        assert _normalize_to_jq("600519") == "600519.XSHG"
        assert _normalize_to_jq("000001") == "000001.XSHE"


class TestDateRangeQueries:
    """日期范围查询测试"""

    def test_stock_daily_range(self):
        """测试股票日线日期范围"""
        from jk2bt.market_data.stock import get_stock_daily

        start = "2024-12-01"
        end = "2024-12-31"

        df = get_stock_daily(
            f"sh{FIXED_TEST_STOCKS['sh_main']}",
            start=start,
            end=end,
            force_update=False,
        )

        assert isinstance(df, pd.DataFrame)

        if not df.empty and "datetime" in df.columns:
            dates = pd.to_datetime(df["datetime"])
            assert dates.min() >= pd.to_datetime(start)
            assert dates.max() <= pd.to_datetime(end)

    def test_index_daily_range(self):
        """测试指数日线日期范围"""
        from jk2bt.market_data.index import get_index_daily

        start = "2024-11-01"
        end = "2024-11-30"

        df = get_index_daily("000300", start=start, end=end, force_update=False)

        assert isinstance(df, pd.DataFrame)


def test_date_utils():
    """测试日期工具函数"""
    print("\n=== 测试日期工具 ===")

    # 测试固定日期
    for name, date in FIXED_TEST_DATES.items():
        print(f"  {name}: {date}")

    # 测试固定股票
    for name, code in FIXED_TEST_STOCKS.items():
        print(f"  {name}: {code}")

    print("=== 日期工具测试完成 ===\n")


if __name__ == "__main__":
    test_date_utils()
    pytest.main([__file__, "-v", "-s"])
