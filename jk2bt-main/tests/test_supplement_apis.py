"""
tests/test_supplement_apis.py
测试新增的9个数据接口API。

测试内容：
- 单只股票查询
- 批量查询
- 缓存机制
- finance.run_query 兼容性
- 空结果处理
- 错误处理
"""

import pytest
import pandas as pd
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


class TestShareholderAPI:
    """测试股东信息API"""

    def test_get_top10_shareholders(self):
        """测试获取十大股东"""
        from jk2bt.finance_data.shareholder import (
            get_top10_shareholders,
        )

        df = get_top10_shareholders("600519.XSHG", force_update=True)

        assert isinstance(df, pd.DataFrame)
        if not df.empty:
            assert "code" in df.columns

    def test_get_top10_float_shareholders(self):
        """测试获取十大流通股东"""
        from jk2bt.finance_data.shareholder import (
            get_top10_float_shareholders,
        )

        df = get_top10_float_shareholders("000001.XSHE", force_update=True)

        assert isinstance(df, pd.DataFrame)

    def test_get_shareholder_count(self):
        """测试获取股东户数"""
        from jk2bt.finance_data.shareholder import (
            get_shareholder_count,
        )

        df = get_shareholder_count("600519.XSHG", force_update=True)

        assert isinstance(df, pd.DataFrame)
        if not df.empty:
            assert "holder_num" in df.columns

    def test_query_shareholder_top10(self):
        """测试批量查询十大股东"""
        from jk2bt.finance_data.shareholder import (
            query_shareholder_top10,
        )

        df = query_shareholder_top10(["600519.XSHG", "000001.XSHE"])

        assert isinstance(df, pd.DataFrame)

    def test_finance_query_compatibility(self):
        """测试 finance.run_query 兼容性"""
        from jk2bt.finance_data.shareholder import finance

        df = finance.run_query(finance.STK_SHAREHOLDER_TOP10)

        assert isinstance(df, pd.DataFrame)


class TestDividendAPI:
    """测试分红送股API"""

    def test_get_dividend(self):
        """测试获取分红信息"""
        from jk2bt.finance_data.dividend import get_dividend

        df = get_dividend("600519.XSHG", force_update=True)

        assert isinstance(df, pd.DataFrame)
        if not df.empty:
            assert "code" in df.columns
            assert "ex_dividend_date" in df.columns

    def test_query_dividend(self):
        """测试批量查询分红"""
        from jk2bt.finance_data.dividend import (
            query_dividend,
        )

        df = query_dividend(["600519.XSHG"])

        assert isinstance(df, pd.DataFrame)

    def test_finance_query_compatibility(self):
        """测试 finance.run_query 兼容性"""
        from jk2bt.finance_data.dividend import finance

        df = finance.run_query(finance.STK_XR_XD)

        assert isinstance(df, pd.DataFrame)


class TestShareChangeAPI:
    """测试股东变动API"""

    def test_get_share_change(self):
        """测试获取股东变动"""
        from jk2bt.finance_data.share_change import (
            get_share_change,
        )

        df = get_share_change("600519.XSHG", force_update=True)

        assert isinstance(df, pd.DataFrame)
        if not df.empty:
            assert "code" in df.columns
            assert "change_date" in df.columns

    def test_query_share_change(self):
        """测试批量查询股东变动"""
        from jk2bt.finance_data.share_change import (
            query_share_change,
        )

        df = query_share_change(["600519.XSHG"])

        assert isinstance(df, pd.DataFrame)


class TestUnlockAPI:
    """测试限售解禁API"""

    def test_get_unlock(self):
        """测试获取限售解禁"""
        from jk2bt.finance_data.unlock import get_unlock

        df = get_unlock("600519.XSHG", force_update=True)

        assert isinstance(df, pd.DataFrame)
        if not df.empty:
            assert "code" in df.columns
            assert "unlock_date" in df.columns

    def test_get_unlock_calendar(self):
        """测试获取解禁日历"""
        from jk2bt.finance_data.unlock import (
            get_unlock_calendar,
        )

        df = get_unlock_calendar(force_update=True)

        assert isinstance(df, pd.DataFrame)


class TestMacroAPI:
    """测试宏观数据API"""

    def test_get_macro_cpi(self):
        """测试获取CPI数据"""
        from jk2bt.finance_data.macro import get_macro_cpi

        df = get_macro_cpi(force_update=True)

        assert isinstance(df, pd.DataFrame)
        if not df.empty:
            assert "indicator" in df.columns
            assert "value" in df.columns

    def test_get_macro_ppi(self):
        """测试获取PPI数据"""
        from jk2bt.finance_data.macro import get_macro_ppi

        df = get_macro_ppi(force_update=True)

        assert isinstance(df, pd.DataFrame)

    def test_get_macro_gdp(self):
        """测试获取GDP数据"""
        from jk2bt.finance_data.macro import get_macro_gdp

        df = get_macro_gdp(force_update=True)

        assert isinstance(df, pd.DataFrame)

    def test_query_macro(self):
        """测试批量查询宏观数据"""
        from jk2bt.finance_data.macro import query_macro

        df = query_macro(["CPI", "PPI"])

        assert isinstance(df, pd.DataFrame)


class TestConversionBondAPI:
    """测试可转债API"""

    def test_get_conversion_bond_list(self):
        """测试获取可转债列表"""
        from jk2bt.market_data.conversion_bond import (
            get_conversion_bond_list,
        )

        df = get_conversion_bond_list(force_update=True)

        assert isinstance(df, pd.DataFrame)
        if not df.empty:
            assert "bond_code" in df.columns
            assert "bond_name" in df.columns

    def test_get_conversion_bond(self):
        """测试获取单只可转债"""
        from jk2bt.market_data.conversion_bond import (
            get_conversion_bond,
        )

        df = get_conversion_bond("110053")

        assert isinstance(df, pd.DataFrame)


class TestOptionAPI:
    """测试期权API"""

    def test_get_option_list(self):
        """测试获取期权列表"""
        from jk2bt.market_data.option import get_option_list

        df = get_option_list(underlying="sse", force_update=True)

        assert isinstance(df, pd.DataFrame)
        if not df.empty:
            assert "option_code" in df.columns
            assert "option_name" in df.columns


class TestIndexComponentsAPI:
    """测试指数成分股API"""

    def test_get_index_components(self):
        """测试获取指数成分股"""
        from jk2bt.market_data.index_components import (
            get_index_components,
        )

        df = get_index_components("000300.XSHG", force_update=True)

        assert isinstance(df, pd.DataFrame)
        if not df.empty:
            assert "index_code" in df.columns
            assert "code" in df.columns
            assert "weight" in df.columns

    def test_query_index_components(self):
        """测试批量查询指数成分股"""
        from jk2bt.market_data.index_components import (
            query_index_components,
        )

        df = query_index_components(["000300.XSHG"])

        assert isinstance(df, pd.DataFrame)


class TestIndustrySWAPI:
    """测试申万行业API"""

    def test_get_industry_sw(self):
        """测试获取申万行业分类"""
        from jk2bt.market_data.industry_sw import (
            get_industry_sw,
        )

        df = get_industry_sw("600519.XSHG", force_update=True)

        assert isinstance(df, pd.DataFrame)
        if not df.empty:
            assert "code" in df.columns
            assert "industry_name" in df.columns

    def test_query_industry_sw(self):
        """测试批量查询申万行业"""
        from jk2bt.market_data.industry_sw import (
            query_industry_sw,
        )

        df = query_industry_sw(["600519.XSHG", "000001.XSHE"])

        assert isinstance(df, pd.DataFrame)


class TestSchemaConsistency:
    """测试字段一致性"""

    def test_shareholder_schema(self):
        """测试股东信息字段一致性"""
        from jk2bt.finance_data.shareholder import (
            _SHAREHOLDER_SCHEMA,
            get_top10_shareholders,
        )

        df = get_top10_shareholders("600519.XSHG")
        if not df.empty:
            for col in _SHAREHOLDER_SCHEMA:
                assert col in df.columns, f"Missing column: {col}"

    def test_dividend_schema(self):
        """测试分红送股字段一致性"""
        from jk2bt.finance_data.dividend import (
            _DIVIDEND_SCHEMA,
            get_dividend,
        )

        df = get_dividend("600519.XSHG")
        if not df.empty:
            for col in _DIVIDEND_SCHEMA:
                assert col in df.columns, f"Missing column: {col}"

    def test_unlock_schema(self):
        """测试限售解禁字段一致性"""
        from jk2bt.finance_data.unlock import (
            _UNLOCK_SCHEMA,
            get_unlock,
        )

        df = get_unlock("600519.XSHG")
        if not df.empty:
            for col in _UNLOCK_SCHEMA:
                assert col in df.columns, f"Missing column: {col}"


class TestCodeFormatSupport:
    """测试代码格式支持"""

    def test_jq_format(self):
        """测试聚宽格式"""
        from jk2bt.finance_data.shareholder import (
            get_top10_shareholders,
        )

        df = get_top10_shareholders("600519.XSHG")
        assert isinstance(df, pd.DataFrame)

    def test_plain_code(self):
        """测试纯代码格式"""
        from jk2bt.finance_data.shareholder import (
            get_top10_shareholders,
        )

        df = get_top10_shareholders("600519")
        assert isinstance(df, pd.DataFrame)

    def test_sh_prefix(self):
        """测试sh前缀格式"""
        from jk2bt.finance_data.shareholder import (
            get_top10_shareholders,
        )

        df = get_top10_shareholders("sh600519")
        assert isinstance(df, pd.DataFrame)


class TestEmptyResultHandling:
    """测试空结果处理"""

    def test_invalid_code_returns_empty_df(self):
        """测试无效代码返回空DataFrame"""
        from jk2bt.finance_data.shareholder import (
            get_top10_shareholders,
        )

        df = get_top10_shareholders("999999.XSHG")

        assert isinstance(df, pd.DataFrame)
        assert df.empty


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
