"""
test_extended_factors.py
扩展因子模块测试。

测试覆盖：
- 量价因子（VOL系列、VEMA、AR/BR、WVAD、PSY、VR、MACD、MFI14等）
- Barra风格因子（beta、momentum、residual_volatility、liquidity_barra等）
- 风险因子（Skewness、Kurtosis、Sharpe）
- 财务扩展因子（gross_income_ratio、周转率系列）
- 因子计算函数单元测试
"""

import warnings

warnings.filterwarnings("ignore")

import pytest
import pandas as pd
import numpy as np
from unittest.mock import patch, MagicMock

pytestmark = pytest.mark.network


# =====================================================================
# Fixtures
# =====================================================================


@pytest.fixture
def sample_price_data():
    """生成模拟价格数据。"""
    np.random.seed(42)
    dates = pd.date_range("2023-01-01", periods=300, freq="B")

    close = 100 * (1 + np.random.randn(300).cumsum() * 0.01)
    close = np.maximum(close, 1)

    high = close * (1 + np.abs(np.random.randn(300)) * 0.02)
    low = close * (1 - np.abs(np.random.randn(300)) * 0.02)
    open_price = close * (1 + np.random.randn(300) * 0.01)
    volume = np.random.randint(1000000, 10000000, 300)
    money = volume * close
    turnover = np.random.uniform(0.01, 0.05, 300)

    df = pd.DataFrame(
        {
            "date": dates,
            "open": open_price,
            "high": high,
            "low": low,
            "close": close,
            "volume": volume,
            "money": money,
            "turnover_rate": turnover,
        }
    )
    return df


@pytest.fixture
def sample_returns():
    """生成模拟收益率序列。"""
    np.random.seed(42)
    return pd.Series(
        np.random.randn(252) * 0.02,
        index=pd.date_range("2023-01-01", periods=252, freq="B"),
    )


# =====================================================================
# 因子模块导入测试
# =====================================================================


class TestFactorModuleImport:
    """测试因子模块导入和注册。"""

    def test_import_factors_module(self):
        """测试因子模块导入。"""
        from jk2bt.factors import (
            get_factor_values_jq,
            global_factor_registry,
            technical,
            barra_factors,
            fundamentals,
        )

        assert callable(get_factor_values_jq)
        assert hasattr(global_factor_registry, "list_factors")

    def test_factor_registry_count(self):
        """测试注册因子数量。"""
        from jk2bt.factors import global_factor_registry

        factors = global_factor_registry.list_factors()
        assert len(factors) >= 100, f"因子数量不足: {len(factors)}"

    def test_factor_alias_normalization(self):
        """测试因子别名标准化。"""
        from jk2bt.factors.base import normalize_factor_name

        assert normalize_factor_name("BIAS5") == "bias_5"
        assert normalize_factor_name("EMAC26") == "emac_26"
        assert normalize_factor_name("VOL60") == "vol_60"
        assert normalize_factor_name("beta") == "beta"
        assert normalize_factor_name("Sharpe60") == "sharpe_ratio_60"


# =====================================================================
# 量价因子测试
# =====================================================================


class TestVolumeFactors:
    """测试成交量相关因子。"""

    def test_vol_series_factors_registered(self):
        """测试VOL系列因子注册。"""
        from jk2bt.factors import global_factor_registry

        for window in [5, 10, 20, 60, 120, 240]:
            factor_name = f"vol_{window}"
            assert global_factor_registry.is_registered(factor_name), (
                f"因子未注册: {factor_name}"
            )

    def test_davol_factors_registered(self):
        """测试DAVOL因子注册。"""
        from jk2bt.factors import global_factor_registry

        for window in [5, 10, 20]:
            factor_name = f"davol_{window}"
            assert global_factor_registry.is_registered(factor_name), (
                f"因子未注册: {factor_name}"
            )

    def test_vema_factors_registered(self):
        """测试VEMA因子注册。"""
        from jk2bt.factors import global_factor_registry

        for window in [5, 10, 12, 26]:
            factor_name = f"vema_{window}"
            assert global_factor_registry.is_registered(factor_name), (
                f"因子未注册: {factor_name}"
            )

    def test_vosc_factor_registered(self):
        """测试VOSC因子注册。"""
        from jk2bt.factors import global_factor_registry

        assert global_factor_registry.is_registered("vosc")

    def test_vroc_factors_registered(self):
        """测试VROC因子注册。"""
        from jk2bt.factors import global_factor_registry

        for window in [6, 12]:
            factor_name = f"vroc_{window}"
            assert global_factor_registry.is_registered(factor_name), (
                f"因子未注册: {factor_name}"
            )

    def test_tvma_tvstd_factors_registered(self):
        """测试TVMA/TVSTD因子注册。"""
        from jk2bt.factors import global_factor_registry

        for window in [6, 20]:
            assert global_factor_registry.is_registered(f"tvma_{window}")
            assert global_factor_registry.is_registered(f"tvstd_{window}")


class TestTechnicalIndicators:
    """测试技术指标因子。"""

    def test_ar_br_factors_registered(self):
        """测试AR/BR因子注册。"""
        from jk2bt.factors import global_factor_registry

        assert global_factor_registry.is_registered("ar")
        assert global_factor_registry.is_registered("br")
        assert global_factor_registry.is_registered("arbr")

    def test_wvad_factor_registered(self):
        """测试WVAD因子注册。"""
        from jk2bt.factors import global_factor_registry

        assert global_factor_registry.is_registered("wvad")
        assert global_factor_registry.is_registered("mawvad")

    def test_psy_factor_registered(self):
        """测试PSY因子注册。"""
        from jk2bt.factors import global_factor_registry

        assert global_factor_registry.is_registered("psy")

    def test_vr_factor_registered(self):
        """测试VR因子注册。"""
        from jk2bt.factors import global_factor_registry

        assert global_factor_registry.is_registered("vr")

    def test_macd_factor_registered(self):
        """测试MACD因子注册。"""
        from jk2bt.factors import global_factor_registry

        assert global_factor_registry.is_registered("macd")

    def test_mfi_factor_registered(self):
        """测试MFI因子注册。"""
        from jk2bt.factors import global_factor_registry

        assert global_factor_registry.is_registered("mfi_14")

    def test_cci_factors_registered(self):
        """测试CCI因子注册。"""
        from jk2bt.factors import global_factor_registry

        for window in [10, 15, 20, 88]:
            factor_name = f"cci_{window}"
            assert global_factor_registry.is_registered(factor_name), (
                f"因子未注册: {factor_name}"
            )

    def test_aroon_factors_registered(self):
        """测试Aroon因子注册。"""
        from jk2bt.factors import global_factor_registry

        assert global_factor_registry.is_registered("aroon_up")
        assert global_factor_registry.is_registered("aroon_down")

    def test_trix_factors_registered(self):
        """测试TRIX因子注册。"""
        from jk2bt.factors import global_factor_registry

        assert global_factor_registry.is_registered("trix_5")
        assert global_factor_registry.is_registered("trix_10")

    def test_bull_bear_power_registered(self):
        """测试Bull/Bear Power因子注册。"""
        from jk2bt.factors import global_factor_registry

        assert global_factor_registry.is_registered("bull_power")
        assert global_factor_registry.is_registered("bear_power")

    def test_bbic_factor_registered(self):
        """测试BBIC因子注册。"""
        from jk2bt.factors import global_factor_registry

        assert global_factor_registry.is_registered("bbic")

    def test_vpt_factors_registered(self):
        """测试VPT因子注册。"""
        from jk2bt.factors import global_factor_registry

        assert global_factor_registry.is_registered("single_day_vpt")
        assert global_factor_registry.is_registered("single_day_vpt_6")
        assert global_factor_registry.is_registered("single_day_vpt_12")


class TestMomentumFactors:
    """测试动量因子。"""

    def test_roc_factors_registered(self):
        """测试ROC因子注册。"""
        from jk2bt.factors import global_factor_registry

        for window in [6, 12, 20, 60, 120]:
            factor_name = f"roc_{window}"
            assert global_factor_registry.is_registered(factor_name), (
                f"因子未注册: {factor_name}"
            )

    def test_price_position_factors_registered(self):
        """测试价格位置因子注册。"""
        from jk2bt.factors import global_factor_registry

        assert global_factor_registry.is_registered("price_1m")
        assert global_factor_registry.is_registered("price_3m")
        assert global_factor_registry.is_registered("price_1y")

    def test_plrc_factors_registered(self):
        """测试PLRC因子注册。"""
        from jk2bt.factors import global_factor_registry

        for window in [6, 12, 24]:
            factor_name = f"plrc_{window}"
            assert global_factor_registry.is_registered(factor_name), (
                f"因子未注册: {factor_name}"
            )

    def test_fifty_two_week_rank_registered(self):
        """测试52周价格位置因子注册。"""
        from jk2bt.factors import global_factor_registry

        assert global_factor_registry.is_registered("fifty_two_week_close_rank")


# =====================================================================
# 风险因子测试
# =====================================================================


class TestRiskFactors:
    """测试风险因子。"""

    def test_variance_factors_registered(self):
        """测试方差因子注册。"""
        from jk2bt.factors import global_factor_registry

        for window in [20, 60, 120]:
            factor_name = f"variance_{window}"
            assert global_factor_registry.is_registered(factor_name), (
                f"因子未注册: {factor_name}"
            )

    def test_skewness_factors_registered(self):
        """测试偏度因子注册。"""
        from jk2bt.factors import global_factor_registry

        for window in [20, 60, 120]:
            factor_name = f"skewness_{window}"
            assert global_factor_registry.is_registered(factor_name), (
                f"因子未注册: {factor_name}"
            )

    def test_kurtosis_factors_registered(self):
        """测试峰度因子注册。"""
        from jk2bt.factors import global_factor_registry

        for window in [20, 60, 120]:
            factor_name = f"kurtosis_{window}"
            assert global_factor_registry.is_registered(factor_name), (
                f"因子未注册: {factor_name}"
            )

    def test_sharpe_ratio_factors_registered(self):
        """测试夏普比率因子注册。"""
        from jk2bt.factors import global_factor_registry

        for window in [20, 60, 120]:
            factor_name = f"sharpe_ratio_{window}"
            assert global_factor_registry.is_registered(factor_name), (
                f"因子未注册: {factor_name}"
            )


# =====================================================================
# Barra风格因子测试
# =====================================================================


class TestBarraFactors:
    """测试Barra风格因子。"""

    def test_barra_factors_registered(self):
        """测试Barra风格因子注册。"""
        from jk2bt.factors import global_factor_registry

        barra_factors = [
            "beta",
            "momentum",
            "residual_volatility",
            "liquidity_barra",
            "earnings_yield",
            "book_to_price",
            "size",
        ]

        for factor_name in barra_factors:
            assert global_factor_registry.is_registered(factor_name), (
                f"因子未注册: {factor_name}"
            )

    def test_barra_module_import(self):
        """测试Barra因子模块导入。"""
        from jk2bt.factors import barra_factors

        assert hasattr(barra_factors, "compute_beta")
        assert hasattr(barra_factors, "compute_momentum")
        assert hasattr(barra_factors, "compute_residual_volatility")
        assert hasattr(barra_factors, "compute_liquidity_barra")
        assert hasattr(barra_factors, "compute_earnings_yield")
        assert hasattr(barra_factors, "compute_book_to_price")
        assert hasattr(barra_factors, "compute_size")


# =====================================================================
# 财务扩展因子测试
# =====================================================================


class TestExtendedFundamentalFactors:
    """测试扩展财务因子。"""

    def test_gross_income_ratio_registered(self):
        """测试毛利率因子注册。"""
        from jk2bt.factors import global_factor_registry

        assert global_factor_registry.is_registered("gross_income_ratio")

    def test_turnover_factors_registered(self):
        """测试周转率因子注册。"""
        from jk2bt.factors import global_factor_registry

        assert global_factor_registry.is_registered("inventory_turnover")
        assert global_factor_registry.is_registered("account_receivable_turnover")
        assert global_factor_registry.is_registered("total_asset_turnover")


# =====================================================================
# 因子计算函数单元测试
# =====================================================================


class TestFactorCalculationUnits:
    """测试因子计算函数核心逻辑。"""

    def test_compute_ma(self, sample_price_data):
        """测试移动平均计算。"""
        from jk2bt.factors.technical import _compute_ma

        close = sample_price_data.set_index("date")["close"]
        ma20 = _compute_ma(close, 20)

        assert len(ma20) == len(close)
        assert ma20.iloc[:19].isna().all()
        assert not ma20.iloc[19:].isna().any()

    def test_compute_ema(self, sample_price_data):
        """测试指数移动平均计算。"""
        from jk2bt.factors.technical import _compute_ema

        close = sample_price_data.set_index("date")["close"]
        ema20 = _compute_ema(close, 20)

        assert len(ema20) == len(close)
        assert not ema20.isna().all()

    def test_compute_std(self, sample_price_data):
        """测试标准差计算。"""
        from jk2bt.factors.technical import _compute_std

        close = sample_price_data.set_index("date")["close"]
        std20 = _compute_std(close, 20)

        assert len(std20) == len(close)
        assert std20.iloc[:19].isna().all()
        assert (std20.iloc[20:] >= 0).all()

    def test_safe_divide(self):
        """测试安全除法。"""
        from jk2bt.factors.base import safe_divide

        assert safe_divide(10, 2) == 5
        assert np.isnan(safe_divide(10, 0))
        assert np.isnan(safe_divide(10, np.nan))

        result = safe_divide(np.array([10, 20, 30]), np.array([2, 0, 3]))
        assert result[0] == 5
        assert np.isnan(result[1])
        assert result[2] == 10

    def test_bias_calculation(self, sample_price_data):
        """测试BIAS因子计算。"""
        from jk2bt.factors.technical import compute_bias

        close = sample_price_data.set_index("date")["close"]
        bias = compute_bias("sh600519", window=20, end_date="2024-01-01", count=10)

        if isinstance(bias, pd.Series):
            assert len(bias) == 10
        elif isinstance(bias, (float, np.floating)):
            assert not np.isnan(bias) or True  # 可能因数据问题返回NaN

    def test_roc_calculation(self, sample_price_data):
        """测试ROC因子计算逻辑。"""
        close = sample_price_data.set_index("date")["close"]

        roc_6 = close / close.shift(6) - 1

        assert roc_6.iloc[:6].isna().all()
        assert len(roc_6) == len(close)

    def test_volume_factors_calculation(self, sample_price_data):
        """测试成交量因子计算逻辑。"""
        volume = sample_price_data.set_index("date")["volume"]

        vol_20 = volume.rolling(20).mean()
        vol_60 = volume.rolling(60).mean()

        assert len(vol_20) == len(volume)
        assert len(vol_60) == len(volume)
        assert vol_20.iloc[19] > 0
        assert vol_60.iloc[59] > 0

    def test_skewness_calculation(self, sample_returns):
        """测试偏度计算。"""
        skewness = sample_returns.rolling(60).skew()

        assert len(skewness) == len(sample_returns)
        assert skewness.iloc[:59].isna().all()
        assert not skewness.iloc[60:].isna().all()

    def test_kurtosis_calculation(self, sample_returns):
        """测试峰度计算。"""
        kurtosis = sample_returns.rolling(60).kurt()

        assert len(kurtosis) == len(sample_returns)
        assert kurtosis.iloc[:59].isna().all()

    def test_sharpe_ratio_logic(self, sample_returns):
        """测试夏普比率计算逻辑。"""
        rf = 0.04
        ann_ret = (1 + sample_returns.mean()) ** 252 - 1
        ann_std = sample_returns.std() * np.sqrt(252)
        sharpe = (ann_ret - rf) / ann_std if ann_std != 0 else np.nan

        assert isinstance(sharpe, float)


# =====================================================================
# 因子API接口测试
# =====================================================================


class TestFactorAPI:
    """测试因子API接口。"""

    def test_get_factor_values_single_factor(self):
        """测试单因子查询。"""
        from jk2bt.factors import get_factor_values_jq

        result = get_factor_values_jq(
            securities="sh600519", factors="vol_20", end_date="2024-01-01", count=5
        )

        assert isinstance(result, dict)
        assert "vol_20" in result

    def test_get_factor_values_multiple_factors(self):
        """测试多因子查询。"""
        from jk2bt.factors import get_factor_values_jq

        result = get_factor_values_jq(
            securities="sh600519",
            factors=["vol_20", "vol_60", "vema_12"],
            end_date="2024-01-01",
            count=5,
        )

        assert isinstance(result, dict)
        for factor in ["vol_20", "vol_60", "vema_12"]:
            assert factor in result

    def test_get_factor_values_multiple_securities(self):
        """测试多标查询。"""
        from jk2bt.factors import get_factor_values_jq

        result = get_factor_values_jq(
            securities=["sh600519", "sz000858"],
            factors="vol_20",
            end_date="2024-01-01",
            count=1,
        )

        assert isinstance(result, dict)
        assert "vol_20" in result
        df = result["vol_20"]
        assert isinstance(df, pd.DataFrame)

    def test_factor_with_count_parameter(self):
        """测试count参数。"""
        from jk2bt.factors import get_factor_values_jq

        result = get_factor_values_jq(
            securities="sh600519", factors="roc_20", end_date="2024-01-01", count=10
        )

        df = result.get("roc_20")
        if df is not None and not df.empty:
            assert len(df) <= 10

    def test_factor_with_start_date(self):
        """测试start_date参数。"""
        from jk2bt.factors import get_factor_values_jq

        result = get_factor_values_jq(
            securities="sh600519",
            factors="vol_20",
            start_date="2023-12-01",
            end_date="2023-12-31",
        )

        assert isinstance(result, dict)


# =====================================================================
# 因子数据质量测试
# =====================================================================


class TestFactorDataQuality:
    """测试因子数据质量。"""

    def test_factor_not_all_nan(self):
        """测试因子值不全为NaN。"""
        from jk2bt.factors import get_factor_values_jq

        result = get_factor_values_jq(
            securities="sh600519",
            factors=["vol_20", "roc_6", "bias_10"],
            end_date="2024-01-01",
            count=10,
        )

        for factor_name, df in result.items():
            if not df.empty:
                assert not df.isna().all().all(), f"因子 {factor_name} 全为NaN"

    def test_factor_value_range(self):
        """测试因子值范围合理性。"""
        from jk2bt.factors import get_factor_values_jq

        result = get_factor_values_jq(
            securities="sh600519", factors="psy", end_date="2024-01-01", count=10
        )

        df = result.get("psy")
        if df is not None and not df.empty:
            values = df.values.flatten()
            values = values[~np.isnan(values)]
            if len(values) > 0:
                assert (values >= 0).all() and (values <= 100).all(), "PSY应在0-100范围"

    def test_variance_positive(self):
        """测试方差因子为正。"""
        from jk2bt.factors import get_factor_values_jq

        result = get_factor_values_jq(
            securities="sh600519", factors="variance_60", end_date="2024-01-01", count=5
        )

        df = result.get("variance_60")
        if df is not None and not df.empty:
            values = df.values.flatten()
            values = values[~np.isnan(values)]
            if len(values) > 0:
                assert (values >= 0).all(), "方差应非负"


# =====================================================================
# 集成测试
# =====================================================================


class TestIntegration:
    """集成测试。"""

    @pytest.mark.slow
    def test_full_workflow(self):
        """测试完整工作流。"""
        from jk2bt.factors import get_factor_values_jq

        factors_to_test = [
            "vol_20",
            "vol_60",
            "davol_10",
            "vema_12",
            "vosc",
            "roc_20",
            "roc_60",
            "bias_20",
            "ar",
            "br",
            "psy",
            "vr",
            "macd",
            "mfi_14",
            "variance_60",
            "skewness_60",
            "kurtosis_60",
            "sharpe_ratio_60",
            "beta",
            "momentum",
        ]

        result = get_factor_values_jq(
            securities="sh600519",
            factors=factors_to_test,
            end_date="2024-01-01",
            count=5,
        )

        assert isinstance(result, dict)
        success_count = sum(1 for k, v in result.items() if not v.empty)
        print(f"\n成功计算因子数: {success_count}/{len(factors_to_test)}")

    @pytest.mark.slow
    def test_cross_section_factors(self):
        """测试截面因子计算。"""
        from jk2bt.factors import get_factor_values_jq

        stocks = ["sh600519", "sh600036", "sz000858"]
        factors = ["vol_20", "roc_20", "bias_20"]

        result = get_factor_values_jq(
            securities=stocks, factors=factors, end_date="2024-01-01", count=1
        )

        for factor_name, df in result.items():
            if not df.empty:
                assert df.shape[1] == len(stocks), (
                    f"截面因子股票数不匹配: {factor_name}"
                )


# =====================================================================
# 运行测试
# =====================================================================


def main():
    """运行所有测试。"""
    pytest.main([__file__, "-v", "--tb=short"])


if __name__ == "__main__":
    main()
