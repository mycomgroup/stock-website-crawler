"""
test_growth.py
成长因子模块测试。

测试覆盖：
- compute_np_parent_company_owners_growth_rate 归母净利润增长率
- compute_operating_revenue_growth_rate 营业收入增长率
- compute_earnings_growth 利润增速
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
    dates = pd.date_range("2022-01-01", periods=12, freq="QE")
    np.random.seed(42)

    net_profit = np.array([100, 110, 115, 120, 130, 140, 150, 160, 170, 180, 190, 200])
    operating_revenue = np.array(
        [500, 550, 580, 600, 650, 700, 750, 800, 850, 900, 950, 1000]
    )

    df = pd.DataFrame(
        {
            "date": dates,
            "net_profit_parent": net_profit,
            "operating_revenue": operating_revenue,
            "total_revenue": operating_revenue,
        }
    )
    return df


@pytest.fixture
def mock_income_statement(monkeypatch, sample_income_data):
    """Mock _get_income_statement 函数。"""

    def mock_get_income_statement(symbol):
        return sample_income_data.copy()

    monkeypatch.setattr(
        "jk2bt.analysis.factors.growth._get_income_statement", mock_get_income_statement
    )


class TestGrowthFactors:
    """测试成长因子计算函数。"""

    def test_np_parent_company_owners_growth_rate_empty(self, monkeypatch):
        """测试空数据返回nan。"""
        monkeypatch.setattr(
            "jk2bt.analysis.factors.growth._get_income_statement",
            lambda symbol: pd.DataFrame(),
        )
        from jk2bt.analysis.factors.growth import (
            compute_np_parent_company_owners_growth_rate,
        )

        result = compute_np_parent_company_owners_growth_rate("sh600519")
        assert np.isnan(result)

    def test_np_parent_company_owners_growth_rate_series(self, mock_income_statement):
        """测试归母净利润增长率返回序列。"""
        from jk2bt.analysis.factors.growth import (
            compute_np_parent_company_owners_growth_rate,
        )

        result = compute_np_parent_company_owners_growth_rate("sh600519")
        assert isinstance(result, pd.Series)
        assert len(result) > 0

    def test_np_parent_company_owners_growth_rate_single(self, mock_income_statement):
        """测试归母净利润增长率返回单值。"""
        from jk2bt.analysis.factors.growth import (
            compute_np_parent_company_owners_growth_rate,
        )

        result = compute_np_parent_company_owners_growth_rate("sh600519", count=1)
        assert isinstance(result, float)

    def test_operating_revenue_growth_rate(self, mock_income_statement):
        """测试营业收入增长率。"""
        from jk2bt.analysis.factors.growth import compute_operating_revenue_growth_rate

        result = compute_operating_revenue_growth_rate("sh600519")
        assert isinstance(result, pd.Series)
        assert len(result) > 0

    def test_earnings_growth(self, mock_income_statement):
        """测试利润增速（与归母净利润增长率一致）。"""
        from jk2bt.analysis.factors.growth import (
            compute_earnings_growth,
            compute_np_parent_company_owners_growth_rate,
        )

        earnings = compute_earnings_growth("sh600519")
        np_growth = compute_np_parent_company_owners_growth_rate("sh600519")

        assert isinstance(earnings, pd.Series)
        assert len(earnings) == len(np_growth)

    def test_growth_with_end_date(self, mock_income_statement):
        """测试带截止日期过滤。"""
        from jk2bt.analysis.factors.growth import (
            compute_np_parent_company_owners_growth_rate,
        )

        result = compute_np_parent_company_owners_growth_rate(
            "sh600519", end_date="2023-06-30"
        )
        assert isinstance(result, pd.Series)

    def test_growth_with_count(self, mock_income_statement):
        """测试带count参数。"""
        from jk2bt.analysis.factors.growth import (
            compute_np_parent_company_owners_growth_rate,
        )

        result = compute_np_parent_company_owners_growth_rate("sh600519", count=4)
        assert isinstance(result, (pd.Series, float))

    def test_growth_no_column(self, monkeypatch):
        """测试缺少必需列时返回nan。"""

        def mock_get_income_empty(symbol):
            return pd.DataFrame(
                {
                    "date": pd.date_range("2022-01-01", periods=4, freq="QE"),
                    "total_revenue": [100, 110, 120, 130],
                }
            )

        monkeypatch.setattr(
            "jk2bt.analysis.factors.growth._get_income_statement", mock_get_income_empty
        )

        from jk2bt.analysis.factors.growth import (
            compute_np_parent_company_owners_growth_rate,
        )

        result = compute_np_parent_company_owners_growth_rate("sh600519")
        assert np.isnan(result)


class TestGrowthFactorRegistration:
    """测试成长因子注册。"""

    def test_factor_registered(self):
        """测试因子已注册。"""
        from jk2bt.analysis.factors import global_factor_registry

        assert global_factor_registry.is_registered(
            "np_parent_company_owners_growth_rate"
        )
        assert global_factor_registry.is_registered("operating_revenue_growth_rate")
        assert global_factor_registry.is_registered("earnings_growth")

    def test_factor_dependencies(self):
        """测试因子依赖。"""
        from jk2bt.analysis.factors import global_factor_registry

        info = global_factor_registry.get_info("np_parent_company_owners_growth_rate")
        assert info is not None
        assert "income" in info.get("dependencies", [])

    def test_factor_window(self):
        """测试因子窗口。"""
        from jk2bt.analysis.factors import global_factor_registry

        info = global_factor_registry.get_info("np_parent_company_owners_growth_rate")
        assert info is not None
        assert info.get("window") == 5
