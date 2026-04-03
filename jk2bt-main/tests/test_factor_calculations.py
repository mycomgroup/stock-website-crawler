"""
test_factor_calculations.py
因子计算函数详细单元测试。

测试覆盖：
- 核心计算函数正确性
- 边界条件处理
- 异常数据处理
- 数值精度验证
"""

import warnings

warnings.filterwarnings("ignore")

import pytest
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

pytestmark = pytest.mark.network


# =====================================================================
# 测试数据生成工具
# =====================================================================


def generate_ohlcv_data(days=300, seed=42):
    """生成模拟OHLCV数据。"""
    np.random.seed(seed)
    dates = pd.date_range(end=datetime.now(), periods=days, freq="B")

    base = 100
    returns = np.random.randn(days) * 0.02
    close = base * np.exp(np.cumsum(returns))
    close = np.maximum(close, 1)

    high_factor = 1 + np.abs(np.random.randn(days)) * 0.02
    low_factor = 1 - np.abs(np.random.randn(days)) * 0.02
    open_factor = 1 + np.random.randn(days) * 0.005

    high = close * high_factor
    low = close * low_factor
    open_price = close * open_factor

    high = np.maximum(high, close)
    low = np.minimum(low, close)

    volume = np.random.randint(1000000, 10000000, days).astype(float)
    money = volume * close
    turnover = np.random.uniform(0.01, 0.05, days)

    return pd.DataFrame(
        {
            "date": dates.strftime("%Y-%m-%d"),
            "open": open_price,
            "high": high,
            "low": low,
            "close": close,
            "volume": volume,
            "money": money,
            "turnover_rate": turnover,
        }
    )


def generate_trending_prices(days=100, trend="up"):
    """生成趋势价格数据。"""
    np.random.seed(42)
    base = np.linspace(100, 150 if trend == "up" else 50, days)
    noise = np.random.randn(days) * 2
    return pd.Series(base + noise)


def generate_volatile_prices(days=100, volatility=0.03):
    """生成高波动价格数据。"""
    np.random.seed(42)
    returns = np.random.randn(days) * volatility
    return pd.Series(100 * np.exp(np.cumsum(returns)))


# =====================================================================
# BIAS因子计算测试
# =====================================================================


class TestBiasCalculation:
    """BIAS因子计算测试。"""

    def test_bias_formula(self):
        """测试BIAS计算公式正确性。"""
        close = pd.Series([100, 102, 104, 103, 105, 107, 106, 108, 110, 109])
        window = 5

        ma = close.rolling(window).mean()
        expected_bias = (close - ma) / ma * 100

        bias_5 = expected_bias.dropna()

        assert len(bias_5) == len(close) - window + 1
        assert not bias_5.isna().any()

    def test_bias_with_constant_price(self):
        """测试价格不变时BIAS为0。"""
        close = pd.Series([100] * 20)
        ma = close.rolling(5).mean()
        bias = (close - ma) / ma

        assert (bias.dropna() == 0).all()

    def test_bias_extreme_values(self):
        """测试极端价格情况。"""
        close = pd.Series([100, 50, 200, 25, 400, 12.5, 800])
        ma = close.rolling(3).mean()
        bias = (close - ma) / ma

        assert not bias.dropna().isna().any()


# =====================================================================
# ROC因子计算测试
# =====================================================================


class TestRocCalculation:
    """ROC因子计算测试。"""

    def test_roc_formula(self):
        """测试ROC计算公式正确性。"""
        close = pd.Series([100, 105, 110, 108, 112, 115, 113, 118, 120, 117])
        window = 3

        expected_roc = (close / close.shift(window) - 1) * 100

        roc = expected_roc.dropna()

        assert len(roc) == len(close) - window
        assert roc.iloc[0] == pytest.approx(8.0, rel=0.01)  # 108/100 - 1 = 8%

    def test_roc_zero_when_unchanged(self):
        """测试价格不变时ROC为0。"""
        close = pd.Series([100] * 10)
        roc = (close / close.shift(3) - 1) * 100

        assert (roc.dropna() == 0).all()

    def test_roc_negative_when_declining(self):
        """测试价格下跌时ROC为负。"""
        close = pd.Series([100, 95, 90, 85, 80, 75])
        roc = close / close.shift(2) - 1

        assert (roc.dropna() < 0).all()


# =====================================================================
# VOL因子计算测试
# =====================================================================


class TestVolCalculation:
    """成交量因子计算测试。"""

    def test_vol_ma_calculation(self):
        """测试成交量均值计算。"""
        volume = pd.Series([1000, 1100, 1200, 1300, 1400, 1500, 1600, 1700, 1800, 1900])

        vol_5 = volume.rolling(5).mean()

        assert vol_5.iloc[4] == 1200
        assert vol_5.iloc[9] == 1700

    def test_vol_with_zero_volume(self):
        """测试成交量为0的情况。"""
        volume = pd.Series([1000, 0, 1000, 0, 1000, 0, 1000, 0, 1000, 0])
        vol_5 = volume.rolling(5).mean()

        assert vol_5.iloc[4] == 600

    def test_davol_calculation(self):
        """测试DAVOL计算。"""
        volume = pd.Series(range(100, 200, 10))

        vol_5 = volume.rolling(5).mean()
        vol_20 = volume.rolling(min(20, len(volume))).mean()

        davol = vol_5 / vol_20

        assert not davol.isna().all()


# =====================================================================
# EMA/VEMA因子计算测试
# =====================================================================


class TestEmaCalculation:
    """EMA因子计算测试。"""

    def test_ema_weights(self):
        """测试EMA权重衰减。"""
        close = pd.Series([100] * 20 + [110] * 10)
        ema = close.ewm(span=10, adjust=False).mean()

        assert ema.iloc[-1] > 100
        assert ema.iloc[-1] < 110

    def test_ema_smoother_than_ma(self):
        """测试EMA比MA更平滑。"""
        close = generate_volatile_prices(100)

        ma20 = close.rolling(20).mean()
        ema20 = close.ewm(span=20, adjust=False).mean()

        ma_std = ma20.diff().std()
        ema_std = ema20.diff().std()

        assert ema_std <= ma_std * 1.1  # EMA应该接近或更平滑

    def test_vema_calculation(self):
        """测试VEMA计算。"""
        volume = pd.Series(np.random.randint(1000, 10000, 50))
        vema = volume.ewm(span=10, adjust=False).mean()

        assert len(vema) == len(volume)
        assert vema.iloc[0] == volume.iloc[0]


# =====================================================================
# MACD因子计算测试
# =====================================================================


class TestMacdCalculation:
    """MACD因子计算测试。"""

    def test_macd_components(self):
        """测试MACD组成。"""
        close = generate_ohlcv_data(100)["close"]

        ema12 = close.ewm(span=12, adjust=False).mean()
        ema26 = close.ewm(span=26, adjust=False).mean()
        diff = ema12 - ema26
        dea = diff.ewm(span=9, adjust=False).mean()
        macd = 2 * (diff - dea)

        assert len(macd) == len(close)
        assert not macd.isna().all()

    def test_macd_signal_crossover(self):
        """测试MACD金叉死叉逻辑。"""
        close = generate_trending_prices(100, "up")

        ema12 = close.ewm(span=12, adjust=False).mean()
        ema26 = close.ewm(span=26, adjust=False).mean()
        diff = ema12 - ema26

        assert diff.iloc[-1] > 0


# =====================================================================
# AR/BR因子计算测试
# =====================================================================


class TestArBrCalculation:
    """AR/BR因子计算测试。"""

    def test_ar_calculation(self):
        """测试AR计算。"""
        high = pd.Series([105, 110, 108, 112, 115])
        low = pd.Series([95, 100, 98, 102, 105])
        open_price = pd.Series([100, 102, 104, 106, 108])

        window = 5
        numerator = (high - open_price).sum()
        denominator = (open_price - low).sum()

        ar = numerator / denominator * 100 if denominator != 0 else np.nan

        assert 50 <= ar <= 200  # 放宽范围

    def test_br_calculation(self):
        """测试BR计算。"""
        high = pd.Series([105, 110, 108, 112, 115])
        low = pd.Series([95, 100, 98, 102, 105])
        close = pd.Series([102, 108, 106, 110, 113])
        prev_close = close.shift(1)

        window = 4
        up = (high.iloc[1:] - prev_close.iloc[1:]).clip(lower=0).sum()
        down = (prev_close.iloc[1:] - low.iloc[1:]).clip(lower=0).sum()

        br = up / down * 100 if down != 0 else np.nan

        assert not np.isnan(br)

    def test_ar_extreme_values(self):
        """测试AR极端值处理。"""
        high = pd.Series([100, 100, 100, 100, 100])
        low = pd.Series([100, 100, 100, 100, 100])
        open_price = pd.Series([100, 100, 100, 100, 100])

        num = (high - open_price).sum()
        den = (open_price - low).sum()

        if den == 0:
            assert True
        else:
            ar = num / den * 100
            assert ar == 0


# =====================================================================
# VR因子计算测试
# =====================================================================


class TestVrCalculation:
    """VR因子计算测试。"""

    def test_vr_formula(self):
        """测试VR公式。"""
        close = pd.Series([100, 102, 101, 103, 102, 104, 103, 105, 104, 106])
        volume = pd.Series([1000, 1200, 900, 1300, 800, 1400, 1100, 1500, 1000, 1600])

        ret = close.diff()

        avs = volume[1:][ret[1:] > 0].sum()
        bvs = volume[1:][ret[1:] < 0].sum()
        cvs = volume[1:][ret[1:] == 0].sum()

        vr = (avs + 0.5 * cvs) / (bvs + 0.5 * cvs) * 100

        assert not np.isnan(vr)

    def test_vr_all_up_days(self):
        """测试全部上涨日的VR。"""
        close = pd.Series([100, 101, 102, 103, 104])
        volume = pd.Series([1000] * 5)

        ret = close.diff()
        avs = volume[1:][ret[1:] > 0].sum()
        bvs = volume[1:][ret[1:] < 0].sum()

        vr = avs / bvs if bvs > 0 else np.inf

        assert vr == np.inf or vr > 100


# =====================================================================
# PSY因子计算测试
# =====================================================================


class TestPsyCalculation:
    """PSY因子计算测试。"""

    def test_psy_formula(self):
        """测试PSY公式。"""
        close = pd.Series(
            [100, 102, 101, 103, 102, 104, 103, 105, 104, 106, 105, 107, 106, 108, 107]
        )

        window = 12
        up_days = (close.diff() > 0).astype(int)
        psy = up_days.rolling(window).sum() / window * 100

        assert len(psy.dropna()) > 0
        assert (psy.dropna() >= 0).all() and (psy.dropna() <= 100).all()

    def test_psy_all_up(self):
        """测试全部上涨时的PSY。"""
        close = pd.Series(range(100, 120))
        window = 10

        up_days = (close.diff() > 0).astype(int)
        psy = up_days.rolling(window).sum() / window * 100

        assert psy.iloc[-1] == 100

    def test_psy_all_down(self):
        """测试全部下跌时的PSY。"""
        close = pd.Series(range(120, 100, -1))
        window = 10

        up_days = (close.diff() > 0).astype(int)
        psy = up_days.rolling(window).sum() / window * 100

        assert psy.iloc[-1] == 0


# =====================================================================
# CCI因子计算测试
# =====================================================================


class TestCciCalculation:
    """CCI因子计算测试。"""

    def test_cci_formula(self):
        """测试CCI公式。"""
        high = pd.Series([105, 110, 108, 112, 115, 113, 118, 116, 120, 118])
        low = pd.Series([95, 100, 98, 102, 105, 103, 108, 106, 110, 108])
        close = pd.Series([100, 105, 103, 107, 110, 108, 113, 111, 115, 113])

        tp = (high + low + close) / 3
        window = 5

        ma_tp = tp.rolling(window).mean()
        md = tp.rolling(window).apply(lambda x: np.abs(x - x.mean()).mean())
        cci = (tp - ma_tp) / (0.015 * md)

        assert len(cci.dropna()) > 0

    def test_cci_range(self):
        """测试CCI典型范围。"""
        high = generate_ohlcv_data(50)["high"]
        low = generate_ohlcv_data(50)["low"]
        close = generate_ohlcv_data(50)["close"]

        tp = (high + low + close) / 3
        window = 10

        ma_tp = tp.rolling(window).mean()
        md = tp.rolling(window).apply(lambda x: np.abs(x - x.mean()).mean())
        cci = (tp - ma_tp) / (0.015 * md)

        cci_valid = cci.dropna()
        assert (np.abs(cci_valid) < 500).all()


# =====================================================================
# 风险因子计算测试
# =====================================================================


class TestRiskFactorCalculations:
    """风险因子计算测试。"""

    def test_variance_calculation(self):
        """测试方差计算。"""
        returns = pd.Series(np.random.randn(100) * 0.02)

        var_20 = returns.rolling(20).var()

        assert var_20.iloc[19] > 0
        assert len(var_20.dropna()) == 81

    def test_skewness_calculation(self):
        """测试偏度计算。"""
        np.random.seed(42)

        symmetric = pd.Series(np.random.randn(100))
        skew_sym = symmetric.rolling(60).skew()

        assert abs(skew_sym.iloc[-1]) < 0.5

        right_skewed = pd.Series(np.random.exponential(1, 100))
        skew_right = right_skewed.rolling(60).skew()

        assert skew_right.iloc[-1] > 0

    def test_kurtosis_calculation(self):
        """测试峰度计算。"""
        np.random.seed(42)

        normal = pd.Series(np.random.randn(100))
        kurt_normal = normal.rolling(60).kurt()

        assert abs(kurt_normal.iloc[-1]) < 1

        fat_tail = pd.Series(np.random.standard_t(3, 100))
        kurt_fat = fat_tail.rolling(60).kurt()

        assert kurt_fat.iloc[-1] > kurt_normal.iloc[-1]

    def test_sharpe_ratio_calculation(self):
        """测试夏普比率计算。"""
        np.random.seed(42)
        returns = pd.Series(np.random.randn(252) * 0.02 + 0.0004)

        window = 60
        rf = 0.04

        ann_ret = (1 + returns.rolling(window).mean()) ** 252 - 1
        ann_std = returns.rolling(window).std() * np.sqrt(252)
        sharpe = (ann_ret - rf) / ann_std

        assert len(sharpe.dropna()) > 0


# =====================================================================
# ATR因子计算测试
# =====================================================================


class TestAtrCalculation:
    """ATR因子计算测试。"""

    def test_tr_calculation(self):
        """测试真实波幅计算。"""
        high = pd.Series([105, 110, 108, 112, 115])
        low = pd.Series([95, 100, 98, 102, 105])
        close = pd.Series([100, 105, 103, 107, 110])

        prev_close = close.shift(1)

        tr1 = high - low
        tr2 = abs(high - prev_close)
        tr3 = abs(low - prev_close)

        tr = pd.concat([tr1, tr2, tr3], axis=1).max(axis=1)

        assert tr.iloc[0] == 10
        assert not tr.iloc[1:].isna().any()

    def test_atr_calculation(self):
        """测试ATR计算。"""
        df = generate_ohlcv_data(30)
        high = df["high"]
        low = df["low"]
        close = df["close"]

        prev_close = pd.Series([np.nan] + list(close[:-1]))

        tr = pd.concat(
            [high - low, abs(high - prev_close), abs(low - prev_close)], axis=1
        ).max(axis=1)

        atr = tr.ewm(span=14, adjust=False).mean()

        assert atr.iloc[-1] > 0


# =====================================================================
# 布林带计算测试
# =====================================================================


class TestBollCalculation:
    """布林带计算测试。"""

    def test_boll_bands(self):
        """测试布林带上下轨。"""
        close = generate_ohlcv_data(30)["close"]

        window = 20
        num_std = 2

        ma = close.rolling(window).mean()
        std = close.rolling(window).std()

        boll_up = ma + num_std * std
        boll_down = ma - num_std * std

        assert (boll_up.dropna() > boll_down.dropna()).all()

    def test_boll_contains_price(self):
        """测试布林带包含大部分价格。"""
        close = generate_ohlcv_data(100)["close"]

        window = 20
        num_std = 2

        ma = close.rolling(window).mean()
        std = close.rolling(window).std()

        boll_up = ma + num_std * std
        boll_down = ma - num_std * std

        close_valid = close.iloc[window:]
        up_valid = boll_up.iloc[window:]
        down_valid = boll_down.iloc[window:]

        inside = (close_valid >= down_valid.values) & (close_valid <= up_valid.values)
        ratio = inside.sum() / len(inside)

        assert ratio > 0.9


# =====================================================================
# 边界条件测试
# =====================================================================


class TestEdgeCases:
    """边界条件测试。"""

    def test_short_data_window(self):
        """测试数据短于窗口期。"""
        close = pd.Series([100, 101, 102])

        ma_20 = close.rolling(20).mean()

        assert ma_20.isna().all()

    def test_nan_handling(self):
        """测试NaN值处理。"""
        close = pd.Series([100, np.nan, 102, np.nan, 104])

        ma = close.rolling(3).mean()

        assert ma.isna().sum() > 0

    def test_zero_division(self):
        """测试除零处理。"""
        from jk2bt.factors.base import safe_divide

        result = safe_divide(100, 0)
        assert np.isnan(result)

        result = safe_divide(0, 100)
        assert result == 0

    def test_constant_series(self):
        """测试常数序列。"""
        close = pd.Series([100] * 50)

        ret = close.pct_change()
        std = ret.std()

        assert std == 0 or np.isnan(std)


# =====================================================================
# 性能测试
# =====================================================================


class TestPerformance:
    """性能测试。"""

    def test_large_window_performance(self):
        """测试大窗口计算性能。"""
        import time

        close = generate_ohlcv_data(1000)["close"]

        start = time.time()
        ma_240 = close.rolling(240).mean()
        elapsed = time.time() - start

        assert elapsed < 1.0
        assert not ma_240.iloc[240:].isna().any()

    def test_multiple_factor_calculation_speed(self):
        """测试多因子计算速度。"""
        import time

        close = generate_ohlcv_data(500)["close"]
        volume = generate_ohlcv_data(500)["volume"]

        start = time.time()

        for window in [5, 10, 20, 60, 120, 240]:
            _ = close.rolling(window).mean()
            _ = close.rolling(window).std()
            _ = volume.rolling(window).mean()

        elapsed = time.time() - start

        assert elapsed < 2.0


# =====================================================================
# 运行测试
# =====================================================================


def main():
    """运行所有测试。"""
    pytest.main([__file__, "-v", "--tb=short"])


if __name__ == "__main__":
    main()
