"""
tests/test_finance_missing.py
补充缺失的 finance_data 模块测试

测试模块：
- income.py - 利润表
- cashflow.py - 现金流量表
- margin.py - 融资融券
- forecast.py - 业绩预告
"""

import pytest
import pandas as pd
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))


class TestIncomeAPI:
    """测试利润表 API"""

    def test_import_income_module(self):
        """测试导入 income 模块"""
        from jk2bt.finance_data import get_income

        assert callable(get_income)

    def test_get_income_basic(self):
        """测试获取利润表基本功能"""
        from jk2bt.finance_data import get_income

        # 使用缓存数据
        df = get_income("600519", indicator="按报告期", force_update=False)

        assert isinstance(df, pd.DataFrame)

    def test_get_income_cache(self):
        """测试利润表缓存机制"""
        from jk2bt.finance_data import get_income

        df1 = get_income("600036", indicator="按报告期", force_update=False)
        df2 = get_income("600036", indicator="按报告期", force_update=False)

        assert isinstance(df1, pd.DataFrame)
        assert isinstance(df2, pd.DataFrame)


class TestCashflowAPI:
    """测试现金流量表 API"""

    def test_import_cashflow_module(self):
        """测试导入 cashflow 模块"""
        from jk2bt.finance_data import get_cashflow

        assert callable(get_cashflow)

    def test_get_cashflow_basic(self):
        """测试获取现金流量表基本功能"""
        from jk2bt.finance_data import get_cashflow

        df = get_cashflow("600519", force_update=False)

        assert isinstance(df, pd.DataFrame)


class TestMarginAPI:
    """测试融资融券 API"""

    def test_import_margin_module(self):
        """测试导入 margin 模块"""
        from jk2bt.finance_data import (
            get_margin_data,
            get_margin_history,
        )

        assert callable(get_margin_data)
        assert callable(get_margin_history)

    def test_get_margin_data_basic(self):
        """测试获取融资融券数据基本功能"""
        from jk2bt.finance_data import get_margin_data

        df = get_margin_data("600519")

        assert isinstance(df, pd.DataFrame)

    def test_get_margin_history_basic(self):
        """测试获取融资融券历史数据"""
        from jk2bt.finance_data import get_margin_history

        df = get_margin_history("600519")

        assert isinstance(df, pd.DataFrame)


class TestForecastAPI:
    """测试业绩预告 API"""

    def test_import_forecast_module(self):
        """测试导入 forecast 模块"""
        from jk2bt.finance_data import get_forecast_data

        assert callable(get_forecast_data)

    def test_get_forecast_data_basic(self):
        """测试获取业绩预告数据"""
        from jk2bt.finance_data import get_forecast_data

        df = get_forecast_data("600519")

        assert isinstance(df, pd.DataFrame)


class TestFinanceIntegration:
    """财务数据集成测试"""

    def test_finance_run_query_dividend(self):
        """测试 finance.run_query 查询分红"""
        from jk2bt.core.strategy_base import (
            finance,
            query,
        )

        q = query(finance.STK_XR_XD).filter(finance.STK_XR_XD.code.in_(["600519.XSHG"]))
        df = finance.run_query(q)

        assert isinstance(df, pd.DataFrame)

    def test_finance_run_query_margin(self):
        """测试 finance.run_query 查询融资融券"""
        from jk2bt.core.strategy_base import (
            finance,
            query,
        )

        q = query(finance.STK_MX_RZ_RQ).filter(
            finance.STK_MX_RZ_RQ.code.in_(["600519.XSHG"])
        )
        df = finance.run_query(q)

        assert isinstance(df, pd.DataFrame)

    def test_finance_run_query_forecast(self):
        """测试 finance.run_query 查询业绩预告"""
        from jk2bt.core.strategy_base import (
            finance,
            query,
        )

        q = query(finance.STK_FIN_FORCAST).filter(
            finance.STK_FIN_FORCAST.code.in_(["600519.XSHG"])
        )
        df = finance.run_query(q)

        assert isinstance(df, pd.DataFrame)


def test_quick_validation():
    """快速验证测试"""
    print("\n=== 快速验证测试 ===")

    from jk2bt.finance_data import (
        get_income,
        get_cashflow,
        get_margin_data,
        get_forecast_data,
    )

    print("\n1. 测试利润表")
    df_income = get_income("600519", force_update=False)
    print(f"   利润表数据: {len(df_income)} 条")

    print("\n2. 测试现金流量表")
    df_cashflow = get_cashflow("600519", force_update=False)
    print(f"   现金流量表数据: {len(df_cashflow)} 条")

    print("\n3. 测试融资融券")
    df_margin = get_margin_data("600519")
    print(f"   融资融券数据: {len(df_margin)} 条")

    print("\n4. 测试业绩预告")
    df_forecast = get_forecast_data("600519")
    print(f"   业绩预告数据: {len(df_forecast)} 条")

    print("\n=== 验证完成 ===\n")


if __name__ == "__main__":
    test_quick_validation()
    pytest.main([__file__, "-v", "-s"])
