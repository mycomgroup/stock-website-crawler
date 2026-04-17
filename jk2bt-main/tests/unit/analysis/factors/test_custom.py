"""
test_custom.py
自定义因子模块测试。

测试覆盖：
- compute_zscore RSRS择时Z-Score因子
- compute_zscore_slope RSRS斜率因子
- compute_score 综合评分因子
- get_single_factor_list 单因子查询函数
"""

import warnings

warnings.filterwarnings("ignore")

import pytest
import pandas as pd
import numpy as np
from unittest.mock import patch, MagicMock


@pytest.fixture
def sample_ohlcv_data():
    """生成模拟OHLCV数据。"""
    np.random.seed(42)
    dates = pd.date_range("2022-01-01", periods=100, freq="B")

    close = 100 * (1 + np.random.randn(100).cumsum() * 0.01)
    close = np.maximum(close, 1)

    high = close * (1 + np.abs(np.random.randn(100)) * 0.02)
    low = close * (1 - np.abs(np.random.randn(100)) * 0.02)

    df = pd.DataFrame(
        {
            "日期": dates.strftime("%Y-%m-%d"),
            "最高": high,
            "最低": low,
            "收盘": close,
        }
    )
    return df


@pytest.fixture
def mock_adapter(sample_ohlcv_data, monkeypatch):
    """Mock 数据源适配器。"""
    mock_instance = MagicMock()
    mock_instance.get_stock_hist.return_value = sample_ohlcv_data.copy()

    monkeypatch.setattr(
        "jk2bt.analysis.factors.custom.get_adapter", lambda: mock_instance
    )

    return mock_instance


class TestCustomFactors:
    """测试自定义因子计算函数。"""

    def test_zscore_empty(self, monkeypatch):
        """测试空数据返回nan。"""
        mock_instance = MagicMock()
        mock_instance.get_stock_hist.return_value = pd.DataFrame()

        monkeypatch.setattr(
            "jk2bt.analysis.factors.custom.get_adapter", lambda: mock_instance
        )

        from jk2bt.analysis.factors.custom import compute_zscore

        result = compute_zscore("sh600519")
        assert np.isnan(result)

    def test_zscore_calculation(self, mock_adapter):
        """测试Z-Score计算。"""
        from jk2bt.analysis.factors.custom import compute_zscore

        result = compute_zscore("sh600519", window=18)
        assert isinstance(result, (pd.Series, float))

    def test_zscore_with_count(self, mock_adapter):
        """测试带count参数。"""
        from jk2bt.analysis.factors.custom import compute_zscore

        result = compute_zscore("sh600519", count=10)
        assert isinstance(result, (pd.Series, float))

    def test_zscore_single_value(self, mock_adapter):
        """测试单值返回。"""
        from jk2bt.analysis.factors.custom import compute_zscore

        result = compute_zscore("sh600519", count=1)
        assert isinstance(result, float)

    def test_zscore_slope_calculation(self, mock_adapter):
        """测试RSRS斜率计算。"""
        from jk2bt.analysis.factors.custom import compute_zscore_slope

        result = compute_zscore_slope("sh600519", window=18)
        assert isinstance(result, (pd.Series, float))

    def test_zscore_slope_with_smooth(self, mock_adapter):
        """测试带平滑窗口的斜率计算。"""
        from jk2bt.analysis.factors.custom import compute_zscore_slope

        result = compute_zscore_slope("sh600519", window=18, slope_window=5)
        assert isinstance(result, (pd.Series, float))

    def test_score_no_factors(self, monkeypatch):
        """测试综合评分无因子数据时返回nan。"""
        mock_instance = MagicMock()
        monkeypatch.setattr(
            "jk2bt.analysis.factors.custom.get_adapter", lambda: mock_instance
        )

        monkeypatch.setattr(
            "jk2bt.analysis.factors.zoo.get_factor_values_jq", lambda **kwargs: {}
        )

        from jk2bt.analysis.factors.custom import compute_score

        result = compute_score("sh600519")
        assert np.isnan(result)


class TestCustomFactorRegistration:
    """测试自定义因子注册。"""

    def test_factors_registered(self):
        """测试因子已注册。"""
        from jk2bt.analysis.factors import global_factor_registry

        assert global_factor_registry.is_registered("zscore")
        assert global_factor_registry.is_registered("zscore_slope")
        assert global_factor_registry.is_registered("score")

    def test_zscore_dependencies(self):
        """测试Z-Score因子依赖。"""
        from jk2bt.analysis.factors import global_factor_registry

        info = global_factor_registry.get_info("zscore")
        assert info is not None
        assert "daily_ohlcv" in info.get("dependencies", [])


class TestGetSingleFactorList:
    """测试单因子查询函数。"""

    def test_empty_securities(self, monkeypatch):
        """测试空证券列表。"""
        monkeypatch.setattr(
            "jk2bt.analysis.factors.custom.get_factor_values_jq", lambda **kwargs: {}
        )

        from jk2bt.analysis.factors.custom import get_single_factor_list

        result = get_single_factor_list("pe_ratio", securities=None)
        assert result.empty

    def test_normal_call(self, monkeypatch):
        """测试正常调用。"""
        mock_df = pd.DataFrame(
            {"sh600519": [10.0, 11.0]}, index=["2023-01-01", "2023-01-02"]
        )

        monkeypatch.setattr(
            "jk2bt.analysis.factors.custom.get_factor_values_jq",
            lambda **kwargs: {"pe_ratio": mock_df},
        )

        from jk2bt.analysis.factors.custom import get_single_factor_list

        result = get_single_factor_list("pe_ratio", securities=["sh600519"])
        assert isinstance(result, pd.DataFrame)
