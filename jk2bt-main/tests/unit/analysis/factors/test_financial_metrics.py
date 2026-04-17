"""
test_financial_metrics.py
财务指标因子模块测试。

测试覆盖：
- compute_eps 每股收益
- compute_net_assets 每股净资产
- compute_roe_percentage ROE百分比
- compute_roa_percentage ROA百分比
- compute_net_profit_margin_pct 净利润率
- compute_gross_profit_margin_pct 毛利率
- compute_inc_net_profit_year_on_year 净利润同比增长率
- compute_inc_revenue_year_on_year 营收同比增长率
- compute_inc_total_revenue_year_on_year 营业总收入同比增长率
- compute_inc_operation_profit_year_on_year 营业利润同比增长率
- compute_inc_return ROE增长
- compute_ocf_to_operating_profit 经营现金流/营业利润
- compute_ocf_to_revenue 经营现金流/营业收入
- compute_adjusted_profit 调整后利润
"""

import warnings

warnings.filterwarnings("ignore")

import pytest
import pandas as pd
import numpy as np
from unittest.mock import patch, MagicMock


@pytest.fixture
def sample_income_data():
    """生成模拟利润表数据。"""
    dates = pd.date_range("2022-01-01", periods=8, freq="QE")

    df = pd.DataFrame(
        {
            "date": dates,
            "net_profit": [100, 110, 115, 120, 130, 140, 150, 160],
            "operating_revenue": [500, 550, 580, 600, 650, 700, 750, 800],
            "total_revenue": [500, 550, 580, 600, 650, 700, 750, 800],
            "operating_cost": [300, 330, 350, 360, 390, 420, 450, 480],
            "operating_profit": [150, 165, 175, 180, 200, 220, 240, 260],
            "eps": [1.0, 1.1, 1.15, 1.2, 1.3, 1.4, 1.5, 1.6],
        }
    )
    return df


@pytest.fixture
def sample_balance_data():
    """生成模拟资产负债表数据。"""
    dates = pd.date_range("2022-01-01", periods=8, freq="QE")

    df = pd.DataFrame(
        {
            "date": dates,
            "total_assets": [1000, 1050, 1100, 1150, 1200, 1250, 1300, 1350],
            "total_equity": [600, 630, 660, 690, 720, 750, 780, 810],
            "net_assets_per_share": [6.0, 6.3, 6.6, 6.9, 7.2, 7.5, 7.8, 8.1],
        }
    )
    return df


@pytest.fixture
def mock_income_statement(monkeypatch, sample_income_data):
    """Mock _get_income_statement 函数。"""

    def mock_get_income_statement(symbol):
        return sample_income_data.copy()

    monkeypatch.setattr(
        "jk2bt.analysis.factors.financial_metrics._get_income_statement",
        mock_get_income_statement,
    )


@pytest.fixture
def mock_balance_sheet(monkeypatch, sample_balance_data):
    """Mock _get_balance_sheet 函数。"""

    def mock_get_balance_sheet(symbol):
        return sample_balance_data.copy()

    monkeypatch.setattr(
        "jk2bt.analysis.factors.financial_metrics._get_balance_sheet",
        mock_get_balance_sheet,
    )


class TestFinancialMetricsImports:
    """测试财务指标模块导入。"""

    def test_module_import(self):
        """测试模块导入。"""
        from jk2bt.analysis.factors import financial_metrics

        assert financial_metrics is not None

    def test_all_compute_functions_exist(self):
        """测试所有compute函数存在。"""
        from jk2bt.analysis.factors import financial_metrics

        funcs = [
            "compute_eps",
            "compute_net_assets",
            "compute_roe_percentage",
            "compute_roa_percentage",
            "compute_net_profit_margin_pct",
            "compute_gross_profit_margin_pct",
            "compute_inc_net_profit_year_on_year",
            "compute_inc_revenue_year_on_year",
            "compute_inc_total_revenue_year_on_year",
            "compute_inc_operation_profit_year_on_year",
            "compute_inc_return",
            "compute_ocf_to_operating_profit",
            "compute_ocf_to_revenue",
            "compute_adjusted_profit",
        ]

        for func_name in funcs:
            assert hasattr(financial_metrics, func_name)


class TestEps:
    """测试每股收益因子。"""

    def test_eps_empty_data(self, monkeypatch):
        """测试空数据返回nan。"""
        monkeypatch.setattr(
            "jk2bt.analysis.factors.financial_metrics._get_income_statement",
            lambda symbol: pd.DataFrame(),
        )

        from jk2bt.analysis.factors.financial_metrics import compute_eps

        result = compute_eps("sh600519")
        assert np.isnan(result)

    def test_eps_series(self, mock_income_statement):
        """测试EPS返回序列。"""
        from jk2bt.analysis.factors.financial_metrics import compute_eps

        result = compute_eps("sh600519")
        assert isinstance(result, pd.Series)

    def test_eps_single(self, mock_income_statement):
        """测试EPS返回单值。"""
        from jk2bt.analysis.factors.financial_metrics import compute_eps

        result = compute_eps("sh600519", count=1)
        assert isinstance(result, float)

    def test_eps_no_column(self, monkeypatch):
        """测试缺少EPS列返回nan。"""

        def mock_get_income_empty(symbol):
            return pd.DataFrame(
                {
                    "date": pd.date_range("2022-01-01", periods=4, freq="QE"),
                    "net_profit": [100, 110, 120, 130],
                }
            )

        monkeypatch.setattr(
            "jk2bt.analysis.factors.financial_metrics._get_income_statement",
            mock_get_income_empty,
        )

        from jk2bt.analysis.factors.financial_metrics import compute_eps

        result = compute_eps("sh600519")
        assert np.isnan(result)


class TestNetAssets:
    """测试每股净资产因子。"""

    def test_net_assets_series(self, mock_balance_sheet):
        """测试每股净资产返回序列。"""
        from jk2bt.analysis.factors.financial_metrics import compute_net_assets

        result = compute_net_assets("sh600519")
        assert isinstance(result, pd.Series)


class TestRoePercentage:
    """测试ROE百分比因子。"""

    def test_roe_percentage_series(self, mock_income_statement, mock_balance_sheet):
        """测试ROE返回序列。"""
        from jk2bt.analysis.factors.financial_metrics import compute_roe_percentage

        result = compute_roe_percentage("sh600519")
        assert isinstance(result, pd.Series)

    def test_roe_percentage_positive(self, mock_income_statement, mock_balance_sheet):
        """测试ROE为正。"""
        from jk2bt.analysis.factors.financial_metrics import compute_roe_percentage

        result = compute_roe_percentage("sh600519")
        assert (result > 0).all() or result.isna().any()

    def test_roe_empty_data(self, monkeypatch):
        """测试空数据返回nan。"""
        monkeypatch.setattr(
            "jk2bt.analysis.factors.financial_metrics._get_income_statement",
            lambda symbol: pd.DataFrame(),
        )
        monkeypatch.setattr(
            "jk2bt.analysis.factors.financial_metrics._get_balance_sheet",
            lambda symbol: pd.DataFrame(),
        )

        from jk2bt.analysis.factors.financial_metrics import compute_roe_percentage

        result = compute_roe_percentage("sh600519")
        assert np.isnan(result)


class TestRoaPercentage:
    """测试ROA百分比因子。"""

    def test_roa_percentage_series(self, mock_income_statement, mock_balance_sheet):
        """测试ROA返回序列。"""
        from jk2bt.analysis.factors.financial_metrics import compute_roa_percentage

        result = compute_roa_percentage("sh600519")
        assert isinstance(result, pd.Series)


class TestNetProfitMarginPct:
    """测试净利润率因子。"""

    def test_margin_series(self, mock_income_statement):
        """测试净利润率返回序列。"""
        from jk2bt.analysis.factors.financial_metrics import (
            compute_net_profit_margin_pct,
        )

        result = compute_net_profit_margin_pct("sh600519")
        assert isinstance(result, pd.Series)


class TestGrossProfitMarginPct:
    """测试毛利率因子。"""

    def test_gross_margin_series(self, mock_income_statement):
        """测试毛利率返回序列。"""
        from jk2bt.analysis.factors.financial_metrics import (
            compute_gross_profit_margin_pct,
        )

        result = compute_gross_profit_margin_pct("sh600519")
        assert isinstance(result, pd.Series)


class TestGrowthFactors:
    """测试成长能力因子。"""

    def test_inc_net_profit_yoy(self, mock_income_statement):
        """测试净利润同比增长率。"""
        from jk2bt.analysis.factors.financial_metrics import (
            compute_inc_net_profit_year_on_year,
        )

        result = compute_inc_net_profit_year_on_year("sh600519")
        assert isinstance(result, pd.Series)

    def test_inc_revenue_yoy(self, mock_income_statement):
        """测试营收同比增长率。"""
        from jk2bt.analysis.factors.financial_metrics import (
            compute_inc_revenue_year_on_year,
        )

        result = compute_inc_revenue_year_on_year("sh600519")
        assert isinstance(result, pd.Series)

    def test_inc_total_revenue_yoy(self, mock_income_statement):
        """测试营业总收入同比增长率。"""
        from jk2bt.analysis.factors.financial_metrics import (
            compute_inc_total_revenue_year_on_year,
        )

        result = compute_inc_total_revenue_year_on_year("sh600519")
        assert isinstance(result, pd.Series)

    def test_inc_operation_profit_yoy(self, mock_income_statement):
        """测试营业利润同比增长率。"""
        from jk2bt.analysis.factors.financial_metrics import (
            compute_inc_operation_profit_year_on_year,
        )

        result = compute_inc_operation_profit_year_on_year("sh600519")
        assert isinstance(result, pd.Series)


class TestIncReturn:
    """测试ROE增长因子。"""

    def test_inc_return_series(self, mock_income_statement, mock_balance_sheet):
        """测试ROE增长返回序列。"""
        from jk2bt.analysis.factors.financial_metrics import compute_inc_return

        result = compute_inc_return("sh600519")
        assert isinstance(result, pd.Series)


class TestCashFlowRatios:
    """测试现金流比率因子。"""

    def test_ocf_to_operating_profit(self, mock_income_statement):
        """测试经营现金流/营业利润。"""
        from jk2bt.analysis.factors.financial_metrics import (
            compute_ocf_to_operating_profit,
        )

        result = compute_ocf_to_operating_profit("sh600519")
        assert isinstance(result, (pd.Series, float))

    def test_ocf_to_revenue(self, mock_income_statement):
        """测试经营现金流/营业收入。"""
        from jk2bt.analysis.factors.financial_metrics import compute_ocf_to_revenue

        result = compute_ocf_to_revenue("sh600519")
        assert isinstance(result, (pd.Series, float))


class TestAdjustedProfit:
    """测试调整后利润因子。"""

    def test_adjusted_profit_series(self, mock_income_statement):
        """测试调整后利润返回序列。"""
        from jk2bt.analysis.factors.financial_metrics import compute_adjusted_profit

        result = compute_adjusted_profit("sh600519")
        assert isinstance(result, pd.Series)


class TestFinancialMetricsRegistration:
    """测试财务指标因子注册。"""

    def test_factors_registered(self):
        """测试因子已注册。"""
        from jk2bt.analysis.factors import global_factor_registry

        factors = [
            "eps",
            "net_assets",
            "roe_percentage",
            "roa_percentage",
            "net_profit_margin_pct",
            "gross_profit_margin_pct",
            "inc_net_profit_year_on_year",
            "inc_revenue_year_on_year",
            "inc_total_revenue_year_on_year",
            "inc_operation_profit_year_on_year",
            "inc_return",
            "ocf_to_operating_profit",
            "ocf_to_revenue",
            "adjusted_profit",
        ]

        for factor in factors:
            assert global_factor_registry.is_registered(factor), (
                f"{factor} not registered"
            )

    def test_factor_dependencies(self):
        """测试因子依赖。"""
        from jk2bt.analysis.factors import global_factor_registry

        info = global_factor_registry.get_info("roe_percentage")
        assert info is not None
        deps = info.get("dependencies", [])
        assert "income" in deps
        assert "balance" in deps


class TestFinancialMetricsWithParams:
    """测试带参数的财务指标函数。"""

    def test_with_end_date(self, mock_income_statement, mock_balance_sheet):
        """测试带截止日期。"""
        from jk2bt.analysis.factors.financial_metrics import compute_roe_percentage

        result = compute_roe_percentage("sh600519", end_date="2023-06-30")
        assert isinstance(result, pd.Series)

    def test_with_count(self, mock_income_statement, mock_balance_sheet):
        """测试带count参数。"""
        from jk2bt.analysis.factors.financial_metrics import compute_roe_percentage

        result = compute_roe_percentage("sh600519", count=4)
        assert isinstance(result, (pd.Series, float))
