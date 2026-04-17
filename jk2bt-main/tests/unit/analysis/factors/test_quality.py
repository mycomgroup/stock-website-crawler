"""
test_quality.py
质量/杠杆因子模块测试。

测试覆盖：
- compute_debt_to_assets 资产负债率
- compute_equity_to_asset_ratio 权益资产比
- compute_leverage 杠杆率
- compute_super_quick_ratio 超速动比率
- compute_current_ratio 流动比率
- compute_liquidity 流动性指标
- compute_long_term_debt_to_asset_ratio 长期负债资产比
- compute_financial_liability 金融负债
"""

import warnings

warnings.filterwarnings("ignore")

import pytest
import pandas as pd
import numpy as np
from unittest.mock import patch, MagicMock


@pytest.fixture
def sample_balance_data():
    """生成模拟资产负债表数据。"""
    dates = pd.date_range("2022-01-01", periods=8, freq="QE")

    df = pd.DataFrame(
        {
            "date": dates,
            "total_assets": [1000, 1050, 1100, 1150, 1200, 1250, 1300, 1350],
            "total_liabilities": [400, 420, 440, 460, 480, 500, 520, 540],
            "total_equity": [600, 630, 660, 690, 720, 750, 780, 810],
            "current_assets": [300, 320, 340, 360, 380, 400, 420, 440],
            "current_liabilities": [200, 210, 220, 230, 240, 250, 260, 270],
            "inventory": [50, 55, 60, 65, 70, 75, 80, 85],
        }
    )
    return df


@pytest.fixture
def mock_balance_sheet(monkeypatch, sample_balance_data):
    """Mock _get_balance_sheet 函数。"""

    def mock_get_balance_sheet(symbol):
        return sample_balance_data.copy()

    monkeypatch.setattr(
        "jk2bt.analysis.factors.quality._get_balance_sheet", mock_get_balance_sheet
    )


class TestQualityFactors:
    """测试质量因子计算函数。"""

    def test_debt_to_assets_empty(self, monkeypatch):
        """测试空数据返回nan。"""
        monkeypatch.setattr(
            "jk2bt.analysis.factors.quality._get_balance_sheet",
            lambda symbol: pd.DataFrame(),
        )
        from jk2bt.analysis.factors.quality import compute_debt_to_assets

        result = compute_debt_to_assets("sh600519")
        assert np.isnan(result)

    def test_debt_to_assets(self, mock_balance_sheet):
        """测试资产负债率计算。"""
        from jk2bt.analysis.factors.quality import compute_debt_to_assets

        result = compute_debt_to_assets("sh600519")
        assert isinstance(result, pd.Series)
        assert len(result) > 0
        assert (result <= 1).all()
        assert (result >= 0).all()

    def test_equity_to_asset_ratio(self, mock_balance_sheet):
        """测试权益资产比。"""
        from jk2bt.analysis.factors.quality import compute_equity_to_asset_ratio

        result = compute_equity_to_asset_ratio("sh600519")
        assert isinstance(result, pd.Series)
        assert len(result) > 0
        assert (result <= 1).all()
        assert (result >= 0).all()

    def test_leverage(self, mock_balance_sheet):
        """测试杠杆率。"""
        from jk2bt.analysis.factors.quality import compute_leverage

        result = compute_leverage("sh600519")
        assert isinstance(result, pd.Series)
        assert len(result) > 0
        assert (result >= 1).all()

    def test_super_quick_ratio(self, mock_balance_sheet):
        """测试超速动比率。"""
        from jk2bt.analysis.factors.quality import compute_super_quick_ratio

        result = compute_super_quick_ratio("sh600519")
        assert isinstance(result, pd.Series)
        assert len(result) > 0

    def test_current_ratio(self, mock_balance_sheet):
        """测试流动比率。"""
        from jk2bt.analysis.factors.quality import compute_current_ratio

        result = compute_current_ratio("sh600519")
        assert isinstance(result, pd.Series)
        assert len(result) > 0
        assert (result > 0).all()

    def test_liquidity(self, mock_balance_sheet):
        """测试流动性因子（与current_ratio一致）。"""
        from jk2bt.analysis.factors.quality import (
            compute_liquidity,
            compute_current_ratio,
        )

        liquidity = compute_liquidity("sh600519")
        current = compute_current_ratio("sh600519")

        assert isinstance(liquidity, pd.Series)
        pd.testing.assert_series_equal(liquidity, current)

    def test_long_term_debt_to_asset_ratio(self, mock_balance_sheet):
        """测试长期负债资产比。"""
        from jk2bt.analysis.factors.quality import compute_long_term_debt_to_asset_ratio

        result = compute_long_term_debt_to_asset_ratio("sh600519")
        assert isinstance(result, (pd.Series, float))

    def test_financial_liability(self, mock_balance_sheet):
        """测试金融负债。"""
        from jk2bt.analysis.factors.quality import compute_financial_liability

        result = compute_financial_liability("sh600519")
        assert isinstance(result, (pd.Series, float))

    def test_with_end_date(self, mock_balance_sheet):
        """测试带截止日期。"""
        from jk2bt.analysis.factors.quality import compute_debt_to_assets

        result = compute_debt_to_assets("sh600519", end_date="2023-06-30")
        assert isinstance(result, pd.Series)

    def test_with_count(self, mock_balance_sheet):
        """测试带count参数。"""
        from jk2bt.analysis.factors.quality import compute_debt_to_assets

        result = compute_debt_to_assets("sh600519", count=4)
        assert isinstance(result, (pd.Series, float))

    def test_single_value_return(self, mock_balance_sheet):
        """测试单值返回。"""
        from jk2bt.analysis.factors.quality import compute_debt_to_assets

        result = compute_debt_to_assets("sh600519", count=1)
        assert isinstance(result, float)

    def test_missing_columns(self, monkeypatch):
        """测试缺少必需列。"""

        def mock_get_income_empty(symbol):
            return pd.DataFrame(
                {
                    "date": pd.date_range("2022-01-01", periods=4, freq="QE"),
                    "total_assets": [100, 110, 120, 130],
                }
            )

        monkeypatch.setattr(
            "jk2bt.analysis.factors.quality._get_balance_sheet", mock_get_income_empty
        )

        from jk2bt.analysis.factors.quality import compute_debt_to_assets

        result = compute_debt_to_assets("sh600519")
        assert np.isnan(result)


class TestQualityFactorRegistration:
    """测试质量因子注册。"""

    def test_factors_registered(self):
        """测试因子已注册。"""
        from jk2bt.analysis.factors import global_factor_registry

        assert global_factor_registry.is_registered("debt_to_assets")
        assert global_factor_registry.is_registered("equity_to_asset_ratio")
        assert global_factor_registry.is_registered("leverage")
        assert global_factor_registry.is_registered("super_quick_ratio")
        assert global_factor_registry.is_registered("current_ratio")
        assert global_factor_registry.is_registered("liquidity")
        assert global_factor_registry.is_registered("long_term_debt_to_asset_ratio")
        assert global_factor_registry.is_registered("financial_liability")

    def test_factor_dependencies(self):
        """测试因子依赖。"""
        from jk2bt.analysis.factors import global_factor_registry

        info = global_factor_registry.get_info("debt_to_assets")
        assert info is not None
        assert "balance" in info.get("dependencies", [])
