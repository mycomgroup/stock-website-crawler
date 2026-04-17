"""
test_finance_tables.py
聚宽风格财务数据表查询接口测试。

测试覆盖：
- FinanceTable 基类
- STK_XR_XD 分红送转
- STK_ML_QUOTA 北向资金额度
- STK_HK_HOLD_INFO 港资持股
- BALANCE 资产负债表
- CASH_FLOW 现金流量表
- INCOME 利润表
"""

import warnings

warnings.filterwarnings("ignore")

import pytest
import pandas as pd
import numpy as np
from unittest.mock import patch, MagicMock


class TestFinanceTableBase:
    """测试财务表基类。"""

    def test_finance_table_init(self):
        """测试FinanceTable初始化。"""
        from jk2bt.analysis.factors.finance_tables import FinanceTable

        class TestTable(FinanceTable):
            def query(self, **kwargs):
                return pd.DataFrame()

        table = TestTable("TEST_TABLE")

        assert table.table_name == "TEST_TABLE"
        assert isinstance(table._cache, dict)

    def test_finance_table_not_implemented(self):
        """测试query方法未实现。"""
        from jk2bt.analysis.factors.finance_tables import FinanceTable

        table = FinanceTable("TEST")

        with pytest.raises(NotImplementedError):
            table.query()


class TestSTK_XR_XD:
    """测试分红送转数据表。"""

    def test_init(self):
        """测试初始化。"""
        from jk2bt.analysis.factors.finance_tables import STK_XR_XD

        table = STK_XR_XD()
        assert table.table_name == "STK_XR_XD"

    def test_query_no_code(self):
        """测试无code参数返回空。"""
        from jk2bt.analysis.factors.finance_tables import STK_XR_XD

        table = STK_XR_XD()
        result = table.query()

        assert result.empty

    def test_query_with_mock(self, monkeypatch):
        """测试带mock的查询。"""
        from jk2bt.analysis.factors.finance_tables import STK_XR_XD

        mock_data = pd.DataFrame(
            {
                "ex_dividend_date": ["2023-05-15"],
                "bonus_ratio_rmb": [2.0],
                "code": ["600519"],
            }
        )

        monkeypatch.setattr(
            "jk2bt.analysis.factors.finance_tables.get_dividend_info",
            lambda code: mock_data.copy(),
        )

        table = STK_XR_XD()
        result = table.query(code="sh600519")

        assert isinstance(result, pd.DataFrame)


class TestSTK_ML_QUOTA:
    """测试北向资金额度数据表。"""

    def test_init(self):
        """测试初始化。"""
        from jk2bt.analysis.factors.finance_tables import STK_ML_QUOTA

        table = STK_ML_QUOTA()
        assert table.table_name == "STK_ML_QUOTA"


class TestSTK_HK_HOLD_INFO:
    """测试港资持股数据表。"""

    def test_init(self):
        """测试初始化。"""
        from jk2bt.analysis.factors.finance_tables import STK_HK_HOLD_INFO

        table = STK_HK_HOLD_INFO()
        assert table.table_name == "STK_HK_HOLD_INFO"


class TestBALANCE:
    """测试资产负债表数据表。"""

    def test_init(self):
        """测试初始化。"""
        from jk2bt.analysis.factors.finance_tables import BALANCE

        table = BALANCE()
        assert table.table_name == "BALANCE"

    def test_query_no_code(self):
        """测试无code参数返回空。"""
        from jk2bt.analysis.factors.finance_tables import BALANCE

        table = BALANCE()
        result = table.query()

        assert result.empty


class TestCASH_FLOW:
    """测试现金流量表数据表。"""

    def test_init(self):
        """测试初始化。"""
        from jk2bt.analysis.factors.finance_tables import CASH_FLOW

        table = CASH_FLOW()
        assert table.table_name == "CASH_FLOW"

    def test_query_no_code(self):
        """测试无code参数返回空。"""
        from jk2bt.analysis.factors.finance_tables import CASH_FLOW

        table = CASH_FLOW()
        result = table.query()

        assert result.empty


class TestINCOME:
    """测试利润表数据表。"""

    def test_init(self):
        """测试初始化。"""
        from jk2bt.analysis.factors.finance_tables import INCOME

        table = INCOME()
        assert table.table_name == "INCOME"

    def test_query_no_code(self):
        """测试无code参数返回空。"""
        from jk2bt.analysis.factors.finance_tables import INCOME

        table = INCOME()
        result = table.query()

        assert result.empty


class TestFUND_PORTFOLIO_STOCK:
    """测试基金持仓股票数据表。"""

    def test_init(self):
        """测试初始化。"""
        from jk2bt.analysis.factors.finance_tables import FUND_PORTFOLIO_STOCK

        table = FUND_PORTFOLIO_STOCK()
        assert table.table_name == "FUND_PORTFOLIO_STOCK"

    def test_query_no_fund_code(self):
        """测试无fund_code参数返回空。"""
        from jk2bt.analysis.factors.finance_tables import FUND_PORTFOLIO_STOCK

        table = FUND_PORTFOLIO_STOCK()
        result = table.query()

        assert result.empty


class TestSTK_AH_PRICE_COMP:
    """测试AH股价格对比数据表。"""

    def test_init(self):
        """测试初始化。"""
        from jk2bt.analysis.factors.finance_tables import STK_AH_PRICE_COMP

        table = STK_AH_PRICE_COMP()
        assert table.table_name == "STK_AH_PRICE_COMP"


class TestFinanceTablesExport:
    """测试模块导出。"""

    def test_main_classes_exported(self):
        """测试主要类已导出。"""
        from jk2bt.analysis.factors.finance_tables import (
            FinanceTable,
            STK_XR_XD,
            STK_ML_QUOTA,
            STK_HK_HOLD_INFO,
            BALANCE,
            CASH_FLOW,
            INCOME,
        )

        assert FinanceTable is not None
        assert callable(STK_XR_XD)
        assert callable(STK_ML_QUOTA)
