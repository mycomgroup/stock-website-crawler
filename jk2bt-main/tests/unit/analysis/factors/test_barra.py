"""
test_barra.py
Barra风格因子模块测试。

测试覆盖：
- compute_beta CAPM贝塔
- compute_momentum 动量因子
- compute_residual_volatility 残差波动率
- compute_liquidity_barra 流动性因子
- compute_earnings_yield 盈利能力因子
- compute_book_to_price 账面市值比
- compute_size 市值因子
"""

import warnings

warnings.filterwarnings("ignore")

import pytest
import pandas as pd
import numpy as np
from unittest.mock import patch, MagicMock


@pytest.fixture
def sample_price_data():
    """生成模拟价格数据。"""
    np.random.seed(42)
    dates = pd.date_range("2022-01-01", periods=300, freq="B")

    close = 100 * (1 + np.random.randn(300).cumsum() * 0.01)
    close = np.maximum(close, 1)

    high = close * (1 + np.abs(np.random.randn(300)) * 0.02)
    low = close * (1 - np.abs(np.random.randn(300)) * 0.02)
    open_price = close * (1 + np.random.randn(300) * 0.01)
    volume = np.random.randint(1000000, 10000000, 300)
    turnover = np.random.uniform(0.01, 0.05, 300)

    df = pd.DataFrame(
        {
            "日期": dates.strftime("%Y-%m-%d"),
            "开盘": open_price,
            "最高": high,
            "最低": low,
            "收盘": close,
            "成交量": volume,
            "换手率": turnover,
        }
    )
    return df


@pytest.fixture
def sample_index_data():
    """生成模拟指数数据。"""
    np.random.seed(43)
    dates = pd.date_range("2022-01-01", periods=300, freq="B")

    close = 3000 * (1 + np.random.randn(300).cumsum() * 0.008)
    close = np.maximum(close, 100)

    df = pd.DataFrame(
        {
            "date": dates,
            "close": close,
        }
    )
    return df


@pytest.fixture
def mock_adapter(sample_price_data, sample_index_data, monkeypatch):
    """Mock 数据源适配器。"""
    mock_instance = MagicMock()
    mock_instance.get_stock_hist.return_value = sample_price_data.copy()
    mock_instance.get_index_daily_raw.return_value = pd.DataFrame(
        {
            "日期": sample_index_data["date"].dt.strftime("%Y-%m-%d"),
            "收盘": sample_index_data["close"].values,
        }
    )

    monkeypatch.setattr(
        "jk2bt.analysis.factors.barra.get_adapter", lambda: mock_instance
    )

    return mock_instance


class TestBarraFactors:
    """测试Barra风格因子计算函数。"""

    def test_beta_empty(self, monkeypatch):
        """测试空数据返回nan。"""
        mock_instance = MagicMock()
        mock_instance.get_stock_hist.return_value = pd.DataFrame()

        monkeypatch.setattr(
            "jk2bt.analysis.factors.barra.get_adapter", lambda: mock_instance
        )

        from jk2bt.analysis.factors.barra import compute_beta

        result = compute_beta("sh600519")
        assert np.isnan(result)

    def test_beta_calculation(self, mock_adapter):
        """测试Beta计算。"""
        from jk2bt.analysis.factors.barra import compute_beta

        result = compute_beta("sh600519", window=60)
        assert isinstance(result, (pd.Series, float))

    def test_beta_with_count(self, mock_adapter):
        """测试带count参数。"""
        from jk2bt.analysis.factors.barra import compute_beta

        result = compute_beta("sh600519", count=10)
        assert isinstance(result, (pd.Series, float))

    def test_momentum_calculation(self, mock_adapter):
        """测试动量因子计算。"""
        from jk2bt.analysis.factors.barra import compute_momentum

        result = compute_momentum("sh600519", window=120)
        assert isinstance(result, (pd.Series, float))

    def test_residual_volatility_calculation(self, mock_adapter):
        """测试残差波动率计算。"""
        from jk2bt.analysis.factors.barra import compute_residual_volatility

        result = compute_residual_volatility("sh600519", window=60)
        assert isinstance(result, (pd.Series, float))

    def test_liquidity_barra_calculation(self, mock_adapter):
        """测试流动性因子计算。"""
        from jk2bt.analysis.factors.barra import compute_liquidity_barra

        result = compute_liquidity_barra("sh600519")
        assert isinstance(result, (pd.Series, float))

    def test_earnings_yield_empty_income(self, monkeypatch):
        """测试缺少利润数据时返回nan。"""
        mock_instance = MagicMock()
        mock_instance.get_stock_hist.return_value = pd.DataFrame(
            {
                "日期": ["2023-01-01"],
                "收盘": [100],
            }
        )

        monkeypatch.setattr(
            "jk2bt.analysis.factors.barra.get_adapter", lambda: mock_instance
        )
        monkeypatch.setattr(
            "jk2bt.analysis.factors.barra._get_income_statement",
            lambda symbol: pd.DataFrame(),
        )

        from jk2bt.analysis.factors.barra import compute_earnings_yield

        result = compute_earnings_yield("sh600519")
        assert np.isnan(result)

    def test_book_to_price_empty_balance(self, monkeypatch):
        """测试缺少资产负债表时返回nan。"""
        mock_instance = MagicMock()
        mock_instance.get_stock_hist.return_value = pd.DataFrame(
            {
                "日期": ["2023-01-01"],
                "收盘": [100],
            }
        )

        monkeypatch.setattr(
            "jk2bt.analysis.factors.barra.get_adapter", lambda: mock_instance
        )
        monkeypatch.setattr(
            "jk2bt.analysis.factors.barra._get_balance_sheet",
            lambda symbol: pd.DataFrame(),
        )

        from jk2bt.analysis.factors.barra import compute_book_to_price

        result = compute_book_to_price("sh600519")
        assert np.isnan(result)

    def test_size_calculation(self, monkeypatch):
        """测试Size因子计算。"""
        mock_instance = MagicMock()
        monkeypatch.setattr(
            "jk2bt.analysis.factors.barra.get_adapter", lambda: mock_instance
        )

        with patch("jk2bt.analysis.factors.barra.compute_market_cap") as mock_mc:
            mock_mc.return_value = 1e10
            from jk2bt.analysis.factors.barra import compute_size

            result = compute_size("sh600519")
            assert isinstance(result, (float, pd.Series))


class TestBarraFactorRegistration:
    """测试Barra因子注册。"""

    def test_factors_registered(self):
        """测试因子已注册。"""
        from jk2bt.analysis.factors import global_factor_registry

        assert global_factor_registry.is_registered("beta")
        assert global_factor_registry.is_registered("momentum")
        assert global_factor_registry.is_registered("residual_volatility")
        assert global_factor_registry.is_registered("liquidity_barra")
        assert global_factor_registry.is_registered("earnings_yield")
        assert global_factor_registry.is_registered("book_to_price")
        assert global_factor_registry.is_registered("size")

    def test_beta_dependencies(self):
        """测试Beta因子依赖。"""
        from jk2bt.analysis.factors import global_factor_registry

        info = global_factor_registry.get_info("beta")
        assert info is not None
        deps = info.get("dependencies", [])
        assert "daily_ohlcv" in deps
        assert "index_data" in deps

    def test_beta_window(self):
        """测试Beta因子窗口。"""
        from jk2bt.analysis.factors import global_factor_registry

        info = global_factor_registry.get_info("beta")
        assert info is not None
        assert info.get("window") == 252
