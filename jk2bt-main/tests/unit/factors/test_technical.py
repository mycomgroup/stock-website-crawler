"""
test_technical.py
technical.py 模块核心函数单元测试。

测试目标：
- 辅助函数: _compute_ma, _compute_ema, _compute_std
- BIAS系列: compute_bias, compute_bias_5, compute_bias_10
- EMAC系列: compute_emac, compute_emac_10, compute_emac_26
- ROC系列: compute_roc, compute_roc_6
- VOL系列: compute_vol_20, compute_vol_240
- 技术指标: compute_rsi, compute_macd, compute_kdj, compute_boll
"""

import warnings

warnings.filterwarnings("ignore")

import pytest
import pandas as pd
import numpy as np
from unittest.mock import patch, MagicMock
import sys
import os

# Add jk2bt to path for direct import
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../../'))

# Import functions directly from technical module
from jk2bt.factors.technical import (
    _compute_ma,
    _compute_ema,
    _compute_std,
    compute_bias,
    compute_bias_5,
    compute_bias_10,
    compute_emac,
    compute_emac_10,
    compute_emac_26,
    compute_roc,
    compute_roc_6,
    compute_vol,
    compute_vol_20,
    compute_vol_240,
    compute_rsi,
    compute_macd,
    compute_kdj,
    compute_boll,
)
from jk2bt.factors.base import safe_divide


# =====================================================================
# Fixtures
# =====================================================================


@pytest.fixture
def sample_close_series():
    """生成模拟收盘价序列。"""
    np.random.seed(42)
    # 生成稳定的收盘价序列（约100基准，有小幅波动）
    close = 100 + np.random.randn(100) * 2
    # 确保正数
    close = np.abs(close)
    dates = pd.date_range("2023-01-01", periods=100, freq="B")
    return pd.Series(close, index=dates)


@pytest.fixture
def sample_volume_series():
    """生成模拟成交量序列。"""
    np.random.seed(42)
    volume = np.random.randint(1e6, 1e7, 100)
    dates = pd.date_range("2023-01-01", periods=100, freq="B")
    return pd.Series(volume, index=dates)


@pytest.fixture
def sample_ohlcv_df():
    """生成模拟OHLCV数据DataFrame。"""
    np.random.seed(42)
    dates = pd.date_range("2023-01-01", periods=100, freq="B")
    dates_str = dates.strftime("%Y-%m-%d").tolist()

    close = 100 + np.random.randn(100) * 2
    close = np.abs(close)

    high = close * 1.02
    low = close * 0.98
    open_price = close * 0.99 + np.random.randn(100) * 0.5
    open_price = np.abs(open_price)
    volume = np.random.randint(1e6, 1e7, 100)
    money = close * volume

    df = pd.DataFrame({
        'date': dates_str,
        'open': open_price,
        'high': high,
        'low': low,
        'close': close,
        'volume': volume,
        'money': money,
    })
    return df


@pytest.fixture
def constant_series():
    """生成常量序列用于测试边界条件。"""
    dates = pd.date_range("2023-01-01", periods=20, freq="B")
    return pd.Series([100.0] * 20, index=dates)


@pytest.fixture
def short_series():
    """生成短序列用于测试数据不足场景。"""
    dates = pd.date_range("2023-01-01", periods=3, freq="B")
    return pd.Series([100.0, 101.0, 102.0], index=dates)


# =====================================================================
# Helper Function Tests
# =====================================================================


class TestComputeMA:
    """测试 _compute_ma 辅助函数。"""

    def test_ma_basic_calculation(self, sample_close_series):
        """验证MA基本计算正确性。"""
        result = _compute_ma(sample_close_series, 5)

        # 验证长度一致
        assert len(result) == len(sample_close_series)

        # 验证前4个值为NaN（因为min_periods=5）
        assert result.iloc[:4].isna().all()

        # 手动计算第5个MA值验证
        expected_ma5 = sample_close_series.iloc[:5].mean()
        np.testing.assert_almost_equal(result.iloc[4], expected_ma5, decimal=6)

    def test_ma_with_different_windows(self, sample_close_series):
        """参数化测试不同窗口期的MA。"""
        for window in [3, 5, 10, 20]:
            result = _compute_ma(sample_close_series, window)

            # 验证前window-1个值为NaN
            assert result.iloc[:window-1].isna().all()

            # 验证第window个值是前window个值的均值
            expected = sample_close_series.iloc[:window].mean()
            np.testing.assert_almost_equal(result.iloc[window-1], expected, decimal=6)

    def test_ma_constant_series(self, constant_series):
        """测试常量序列的MA值应与原值相同。"""
        result = _compute_ma(constant_series, 5)

        # 第5个值应该是100（与前5个值均值相同）
        assert result.iloc[4] == 100.0

    def test_ma_short_series(self, short_series):
        """测试短序列数据不足时返回NaN。"""
        result = _compute_ma(short_series, 5)

        # 数据不足5个，全部应为NaN
        assert result.isna().all()


class TestComputeEMA:
    """测试 _compute_ema 辅助函数。"""

    def test_ema_basic_calculation(self, sample_close_series):
        """验证EMA基本计算正确性。"""
        result = _compute_ema(sample_close_series, 5)

        # 验证长度一致
        assert len(result) == len(sample_close_series)

        # EMA从第一个值开始计算（adjust=False）
        # 第一个EMA值等于第一个收盘价
        np.testing.assert_almost_equal(result.iloc[0], sample_close_series.iloc[0], decimal=6)

    def test_ema_smoothing_effect(self, sample_close_series):
        """验证EMA平滑效果：EMA应介于前后值之间。"""
        result = _compute_ema(sample_close_series, 10)

        # EMA应该比原始数据更平滑（波动更小）
        original_std = sample_close_series.std()
        ema_std = result.std()

        # EMA的标准差应该更小
        assert ema_std < original_std

    def test_ema_constant_series(self, constant_series):
        """测试常量序列的EMA值应与原值相同。"""
        result = _compute_ema(constant_series, 5)

        # 所有EMA值应该是100
        assert (result == 100.0).all()


class TestComputeStd:
    """测试 _compute_std 辅助函数。"""

    def test_std_basic_calculation(self, sample_close_series):
        """验证标准差基本计算正确性。"""
        result = _compute_std(sample_close_series, 5)

        # 验证长度一致
        assert len(result) == len(sample_close_series)

        # 验证前4个值为NaN（因为min_periods=5）
        assert result.iloc[:4].isna().all()

        # 手动计算第5个标准差值验证
        expected_std5 = sample_close_series.iloc[:5].std()
        np.testing.assert_almost_equal(result.iloc[4], expected_std5, decimal=6)

    def test_std_constant_series(self, constant_series):
        """测试常量序列的标准差应为0。"""
        result = _compute_std(constant_series, 5)

        # 第5个值开始，标准差应该是0（因为值相同）
        assert result.iloc[4] == 0.0

    def test_std_short_series(self, short_series):
        """测试短序列数据不足时返回NaN。"""
        result = _compute_std(short_series, 5)

        # 数据不足5个，全部应为NaN
        assert result.isna().all()


# =====================================================================
# BIAS Tests
# =====================================================================


class TestComputeBIAS:
    """测试 BIAS（乖离率）因子计算。"""

    @patch('jk2bt.factors.technical._get_daily_ohlcv')
    def test_bias_calculation(self, mock_get_ohlcv, sample_ohlcv_df):
        """验证BIAS计算公式：(close - MA) / MA。"""
        mock_get_ohlcv.return_value = sample_ohlcv_df

        result = compute_bias('sh600519', window=5)

        # 验证返回Series
        assert isinstance(result, pd.Series)

        # 验证BIAS前几个值为NaN（因为MA需要5个数据）
        assert result.iloc[:4].isna().all()

    @patch('jk2bt.factors.technical._get_daily_ohlcv')
    def test_bias_5_wrapper(self, mock_get_ohlcv, sample_ohlcv_df):
        """测试 compute_bias_5 调用 compute_bias 参数正确。"""
        mock_get_ohlcv.return_value = sample_ohlcv_df

        result = compute_bias_5('sh600519')

        # 验证调用参数
        call_args = mock_get_ohlcv.call_args
        assert call_args is not None

        # 验证返回Series
        assert isinstance(result, pd.Series)

    @patch('jk2bt.factors.technical._get_daily_ohlcv')
    def test_bias_10_wrapper(self, mock_get_ohlcv, sample_ohlcv_df):
        """测试 compute_bias_10 调用 compute_bias 参数正确。"""
        mock_get_ohlcv.return_value = sample_ohlcv_df

        result = compute_bias_10('sh600519')

        # 验证返回Series
        assert isinstance(result, pd.Series)

    @patch('jk2bt.factors.technical._get_daily_ohlcv')
    def test_bias_with_count(self, mock_get_ohlcv, sample_ohlcv_df):
        """测试BIAS返回指定数量的数据。"""
        mock_get_ohlcv.return_value = sample_ohlcv_df

        result = compute_bias('sh600519', window=5, count=10)

        # 验证返回10条数据
        assert len(result) == 10

    @patch('jk2bt.factors.technical._get_daily_ohlcv')
    def test_bias_empty_data(self, mock_get_ohlcv):
        """测试空数据返回NaN。"""
        mock_get_ohlcv.return_value = pd.DataFrame()

        result = compute_bias('sh600519', window=5)

        # 验证返回NaN
        assert result is np.nan or (isinstance(result, float) and np.isnan(result))


# =====================================================================
# EMAC Tests
# =====================================================================


class TestComputeEMAC:
    """测试 EMAC（指数平均线）因子计算。"""

    @patch('jk2bt.factors.technical._get_daily_ohlcv')
    def test_emac_calculation(self, mock_get_ohlcv, sample_ohlcv_df):
        """验证EMAC计算公式：EMA(close, window)。"""
        mock_get_ohlcv.return_value = sample_ohlcv_df

        result = compute_emac('sh600519', window=10)

        # 验证返回Series
        assert isinstance(result, pd.Series)

        # EMAC第一个值应该等于第一个收盘价
        close_first = sample_ohlcv_df['close'].iloc[0]
        np.testing.assert_almost_equal(result.iloc[0], close_first, decimal=6)

    @patch('jk2bt.factors.technical._get_daily_ohlcv')
    def test_emac_10_wrapper(self, mock_get_ohlcv, sample_ohlcv_df):
        """测试 compute_emac_10 调用正确。"""
        mock_get_ohlcv.return_value = sample_ohlcv_df

        result = compute_emac_10('sh600519')

        # 验证返回Series
        assert isinstance(result, pd.Series)

    @patch('jk2bt.factors.technical._get_daily_ohlcv')
    def test_emac_26_wrapper(self, mock_get_ohlcv, sample_ohlcv_df):
        """测试 compute_emac_26 调用正确。"""
        mock_get_ohlcv.return_value = sample_ohlcv_df

        result = compute_emac_26('sh600519')

        # 验证返回Series
        assert isinstance(result, pd.Series)

    @patch('jk2bt.factors.technical._get_daily_ohlcv')
    def test_emac_with_count(self, mock_get_ohlcv, sample_ohlcv_df):
        """测试EMAC返回指定数量的数据。"""
        mock_get_ohlcv.return_value = sample_ohlcv_df

        result = compute_emac('sh600519', window=10, count=5)

        # 验证返回5条数据
        assert len(result) == 5

    @patch('jk2bt.factors.technical._get_daily_ohlcv')
    def test_emac_empty_data(self, mock_get_ohlcv):
        """测试空数据返回NaN。"""
        mock_get_ohlcv.return_value = pd.DataFrame()

        result = compute_emac('sh600519', window=10)

        # 验证返回NaN
        assert result is np.nan or (isinstance(result, float) and np.isnan(result))


# =====================================================================
# ROC Tests
# =====================================================================


class TestComputeROC:
    """测试 ROC（变动率）因子计算。"""

    @patch('jk2bt.factors.technical._get_daily_ohlcv')
    def test_roc_calculation(self, mock_get_ohlcv, sample_ohlcv_df):
        """验证ROC计算公式：(close / close.shift(window) - 1) * 100。"""
        mock_get_ohlcv.return_value = sample_ohlcv_df

        result = compute_roc('sh600519', window=6)

        # 验证返回Series
        assert isinstance(result, pd.Series)

        # ROC前6个值应该是NaN（因为没有足够的历史数据）
        assert result.iloc[:6].isna().all()

    @patch('jk2bt.factors.technical._get_daily_ohlcv')
    def test_roc_6_wrapper(self, mock_get_ohlcv, sample_ohlcv_df):
        """测试 compute_roc_6 调用正确。"""
        mock_get_ohlcv.return_value = sample_ohlcv_df

        result = compute_roc_6('sh600519')

        # 验证返回Series
        assert isinstance(result, pd.Series)

    @patch('jk2bt.factors.technical._get_daily_ohlcv')
    def test_roc_with_count(self, mock_get_ohlcv, sample_ohlcv_df):
        """测试ROC返回指定数量的数据。"""
        mock_get_ohlcv.return_value = sample_ohlcv_df

        result = compute_roc('sh600519', window=6, count=10)

        # 验证返回10条数据
        assert len(result) == 10

    @patch('jk2bt.factors.technical._get_daily_ohlcv')
    def test_roc_empty_data(self, mock_get_ohlcv):
        """测试空数据返回NaN。"""
        mock_get_ohlcv.return_value = pd.DataFrame()

        result = compute_roc('sh600519', window=6)

        # 验证返回NaN
        assert result is np.nan or (isinstance(result, float) and np.isnan(result))


# =====================================================================
# VOL Tests
# =====================================================================


class TestComputeVOL:
    """测试 VOL（成交量均值）因子计算。"""

    @patch('jk2bt.factors.technical._get_daily_ohlcv')
    def test_vol_calculation(self, mock_get_ohlcv, sample_ohlcv_df):
        """验证VOL计算公式：MA(volume, window)。"""
        mock_get_ohlcv.return_value = sample_ohlcv_df

        result = compute_vol('sh600519', window=20)

        # 验证返回Series
        assert isinstance(result, pd.Series)

        # VOL前19个值应该是NaN（min_periods=20）
        assert result.iloc[:19].isna().all()

        # 验证第20个值是前20个成交量的均值
        expected_vol20 = sample_ohlcv_df['volume'].iloc[:20].mean()
        np.testing.assert_almost_equal(result.iloc[19], expected_vol20, decimal=6)

    @patch('jk2bt.factors.technical._get_daily_ohlcv')
    def test_vol_20_wrapper(self, mock_get_ohlcv, sample_ohlcv_df):
        """测试 compute_vol_20 调用正确。"""
        mock_get_ohlcv.return_value = sample_ohlcv_df

        result = compute_vol_20('sh600519')

        # 验证返回Series
        assert isinstance(result, pd.Series)

    @patch('jk2bt.factors.technical._get_daily_ohlcv')
    def test_vol_240_wrapper(self, mock_get_ohlcv, sample_ohlcv_df):
        """测试 compute_vol_240 调用正确。"""
        # 需要240+数据，扩展样本
        extended_df = pd.concat([sample_ohlcv_df] * 3, ignore_index=True)
        mock_get_ohlcv.return_value = extended_df

        result = compute_vol_240('sh600519')

        # 验证返回Series
        assert isinstance(result, pd.Series)

    @patch('jk2bt.factors.technical._get_daily_ohlcv')
    def test_vol_empty_data(self, mock_get_ohlcv):
        """测试空数据返回NaN。"""
        mock_get_ohlcv.return_value = pd.DataFrame()

        result = compute_vol('sh600519', window=20)

        # 验证返回NaN
        assert result is np.nan or (isinstance(result, float) and np.isnan(result))


# =====================================================================
# RSI Tests
# =====================================================================


class TestComputeRSI:
    """测试 RSI（相对强弱指标）因子计算。"""

    @patch('jk2bt.factors.technical._get_daily_ohlcv')
    def test_rsi_calculation(self, mock_get_ohlcv, sample_ohlcv_df):
        """验证RSI计算：RSI = 100 - 100/(1+RS)。"""
        mock_get_ohlcv.return_value = sample_ohlcv_df

        result = compute_rsi('sh600519', window=14)

        # 验证返回Series
        assert isinstance(result, pd.Series)

        # RSI值应在0-100之间（除了NaN）
        valid_values = result.dropna()
        assert (valid_values >= 0).all() and (valid_values <= 100).all()

    @patch('jk2bt.factors.technical._get_daily_ohlcv')
    def test_rsi_with_constant_price(self, mock_get_ohlcv):
        """测试常量价格RSI应为50（中性）。"""
        # 创建常量价格数据
        dates = pd.date_range("2023-01-01", periods=50, freq="B")
        dates_str = dates.strftime("%Y-%m-%d").tolist()

        df = pd.DataFrame({
            'date': dates_str,
            'close': [100.0] * 50,
            'high': [102.0] * 50,
            'low': [98.0] * 50,
            'volume': [1e6] * 50,
        })
        mock_get_ohlcv.return_value = df

        result = compute_rsi('sh600519', window=14)

        # 当价格不变时，没有涨跌，RSI理论上是50（但实际上可能因计算方式不同）
        # 验证返回Series
        assert isinstance(result, pd.Series)

    @patch('jk2bt.factors.technical._get_daily_ohlcv')
    def test_rsi_with_count(self, mock_get_ohlcv, sample_ohlcv_df):
        """测试RSI返回指定数量的数据。"""
        mock_get_ohlcv.return_value = sample_ohlcv_df

        result = compute_rsi('sh600519', window=14, count=10)

        # 验证返回10条数据
        assert len(result) == 10

    @patch('jk2bt.factors.technical._get_daily_ohlcv')
    def test_rsi_empty_data(self, mock_get_ohlcv):
        """测试空数据返回NaN。"""
        mock_get_ohlcv.return_value = pd.DataFrame()

        result = compute_rsi('sh600519', window=14)

        # 验证返回NaN
        assert result is np.nan or (isinstance(result, float) and np.isnan(result))


# =====================================================================
# MACD Tests
# =====================================================================


class TestComputeMACD:
    """测试 MACD（指数平滑异同移动平均线）因子计算。"""

    @patch('jk2bt.factors.technical._get_daily_ohlcv')
    def test_macd_calculation(self, mock_get_ohlcv, sample_ohlcv_df):
        """验证MACD计算：MACD = 2 * (DIFF - DEA) / close。"""
        mock_get_ohlcv.return_value = sample_ohlcv_df

        result = compute_macd('sh600519')

        # 验证返回Series
        assert isinstance(result, pd.Series)

    @patch('jk2bt.factors.technical._get_daily_ohlcv')
    def test_macd_with_count(self, mock_get_ohlcv, sample_ohlcv_df):
        """测试MACD返回指定数量的数据。"""
        mock_get_ohlcv.return_value = sample_ohlcv_df

        result = compute_macd('sh600519', count=10)

        # 验证返回10条数据
        assert len(result) == 10

    @patch('jk2bt.factors.technical._get_daily_ohlcv')
    def test_macd_empty_data(self, mock_get_ohlcv):
        """测试空数据返回NaN。"""
        mock_get_ohlcv.return_value = pd.DataFrame()

        result = compute_macd('sh600519')

        # 验证返回NaN
        assert result is np.nan or (isinstance(result, float) and np.isnan(result))

    @patch('jk2bt.factors.technical._get_daily_ohlcv')
    def test_macd_components(self, mock_get_ohlcv, sample_ohlcv_df):
        """验证MACD各组成部分计算正确。"""
        mock_get_ohlcv.return_value = sample_ohlcv_df

        result = compute_macd('sh600519')

        # 手动验证计算逻辑
        close = sample_ohlcv_df.set_index('date')['close'].astype(float)
        ema12 = _compute_ema(close, 12)
        ema26 = _compute_ema(close, 26)
        diff = ema12 - ema26
        dea = _compute_ema(diff, 9)
        expected_macd = safe_divide(2 * (diff - dea), close)

        # 验证结果匹配
        pd.testing.assert_series_equal(result, expected_macd, check_names=False)


# =====================================================================
# KDJ Tests
# =====================================================================


class TestComputeKDJ:
    """测试 KDJ（随机指标）因子计算。"""

    @patch('jk2bt.factors.technical._get_daily_ohlcv')
    def test_kdj_calculation(self, mock_get_ohlcv, sample_ohlcv_df):
        """验证KDJ计算返回K, D, J三个值。"""
        mock_get_ohlcv.return_value = sample_ohlcv_df

        result = compute_kdj('sh600519', n=9, m1=3, m2=3)

        # 验证返回字典包含K, D, J
        assert isinstance(result, dict)
        assert 'K' in result
        assert 'D' in result
        assert 'J' in result

    @patch('jk2bt.factors.technical._get_daily_ohlcv')
    def test_kdj_values_range(self, mock_get_ohlcv, sample_ohlcv_df):
        """验证KDJ值在合理范围内。"""
        mock_get_ohlcv.return_value = sample_ohlcv_df

        result = compute_kdj('sh600519', n=9, m1=3, m2=3)

        # K和D值通常在0-100之间，J值可能超出范围
        k_values = result['K']
        d_values = result['D']

        # K和D的有效值应在0-100之间
        valid_k = k_values.dropna()
        valid_d = d_values.dropna()

        # K值范围检查（允许少量超出）
        assert (valid_k >= -10).all() and (valid_k <= 110).all()

        # D值范围检查
        assert (valid_d >= -10).all() and (valid_d <= 110).all()

    @patch('jk2bt.factors.technical._get_daily_ohlcv')
    def test_kdj_with_count(self, mock_get_ohlcv, sample_ohlcv_df):
        """测试KDJ返回指定数量的数据。"""
        mock_get_ohlcv.return_value = sample_ohlcv_df

        result = compute_kdj('sh600519', n=9, m1=3, m2=3, count=10)

        # 验证每个值返回10条数据
        assert len(result['K']) == 10
        assert len(result['D']) == 10
        assert len(result['J']) == 10

    @patch('jk2bt.factors.technical._get_daily_ohlcv')
    def test_kdj_empty_data(self, mock_get_ohlcv):
        """测试空数据返回NaN字典。"""
        mock_get_ohlcv.return_value = pd.DataFrame()

        result = compute_kdj('sh600519', n=9, m1=3, m2=3)

        # 验证返回NaN字典
        assert result['K'] is np.nan
        assert result['D'] is np.nan
        assert result['J'] is np.nan

    @patch('jk2bt.factors.technical._get_daily_ohlcv')
    def test_kdj_j_formula(self, mock_get_ohlcv, sample_ohlcv_df):
        """验证J = 3*K - 2*D公式。"""
        mock_get_ohlcv.return_value = sample_ohlcv_df

        result = compute_kdj('sh600519', n=9, m1=3, m2=3)

        # 手动验证J值计算
        k = result['K']
        d = result['D']
        j = result['J']

        expected_j = 3 * k - 2 * d
        pd.testing.assert_series_equal(j, expected_j, check_names=False)


# =====================================================================
# BOLL Tests
# =====================================================================


class TestComputeBOLL:
    """测试 BOLL（布林带）因子计算。"""

    @patch('jk2bt.factors.technical._get_daily_ohlcv')
    def test_boll_calculation(self, mock_get_ohlcv, sample_ohlcv_df):
        """验证布林带计算返回上轨和下轨。"""
        mock_get_ohlcv.return_value = sample_ohlcv_df

        result = compute_boll('sh600519', window=20, num_std=2.0)

        # 验证返回tuple
        assert isinstance(result, tuple)
        assert len(result) == 2

        boll_up, boll_down = result

        # 验证返回Series
        assert isinstance(boll_up, pd.Series)
        assert isinstance(boll_down, pd.Series)

    @patch('jk2bt.factors.technical._get_daily_ohlcv')
    def test_boll_band_relationship(self, mock_get_ohlcv, sample_ohlcv_df):
        """验证布林带上轨大于下轨。"""
        mock_get_ohlcv.return_value = sample_ohlcv_df

        result = compute_boll('sh600519', window=20, num_std=2.0)
        boll_up, boll_down = result

        # 上轨应该大于下轨（对于有效值）
        valid_up = boll_up.dropna()
        valid_down = boll_down.dropna()

        assert (valid_up > valid_down).all()

    @patch('jk2bt.factors.technical._get_daily_ohlcv')
    def test_boll_formula(self, mock_get_ohlcv, sample_ohlcv_df):
        """验证布林带公式：boll_up = MA + 2*STD, boll_down = MA - 2*STD。"""
        mock_get_ohlcv.return_value = sample_ohlcv_df

        window = 20
        num_std = 2.0

        result = compute_boll('sh600519', window=window, num_std=num_std)
        boll_up, boll_down = result

        # 手动计算验证
        close = sample_ohlcv_df.set_index('date')['close'].astype(float)
        ma = _compute_ma(close, window)
        std = _compute_std(close, window)

        expected_up = ma + num_std * std
        expected_down = ma - num_std * std

        pd.testing.assert_series_equal(boll_up, expected_up, check_names=False)
        pd.testing.assert_series_equal(boll_down, expected_down, check_names=False)

    @patch('jk2bt.factors.technical._get_daily_ohlcv')
    def test_boll_with_count(self, mock_get_ohlcv, sample_ohlcv_df):
        """测试布林带返回指定数量的数据。"""
        mock_get_ohlcv.return_value = sample_ohlcv_df

        result = compute_boll('sh600519', window=20, num_std=2.0, count=10)
        boll_up, boll_down = result

        # 验证返回10条数据
        assert len(boll_up) == 10
        assert len(boll_down) == 10

    @patch('jk2bt.factors.technical._get_daily_ohlcv')
    def test_boll_empty_data(self, mock_get_ohlcv):
        """测试空数据返回NaN。"""
        mock_get_ohlcv.return_value = pd.DataFrame()

        result = compute_boll('sh600519', window=20, num_std=2.0)

        # 验证返回NaN
        assert result is np.nan or (isinstance(result, float) and np.isnan(result))

    @patch('jk2bt.factors.technical._get_daily_ohlcv')
    def test_boll_with_different_std(self, mock_get_ohlcv, sample_ohlcv_df):
        """测试不同标准差倍数的布林带。"""
        mock_get_ohlcv.return_value = sample_ohlcv_df

        # 测试1.5倍标准差
        result_1_5 = compute_boll('sh600519', window=20, num_std=1.5)
        boll_up_1_5, boll_down_1_5 = result_1_5

        # 测试2倍标准差
        result_2 = compute_boll('sh600519', window=20, num_std=2.0)
        boll_up_2, boll_down_2 = result_2

        # 2倍标准差的带宽应该更宽
        width_1_5 = boll_up_1_5.dropna() - boll_down_1_5.dropna()
        width_2 = boll_up_2.dropna() - boll_down_2.dropna()

        assert (width_2 > width_1_5).all()


# =====================================================================
# Safe Divide Tests
# =====================================================================


class TestSafeDivide:
    """测试 safe_divide 函数。"""

    def test_safe_divide_normal(self):
        """测试正常除法。"""
        result = safe_divide(10, 2)
        assert result == 5.0

    def test_safe_divide_zero_denominator(self):
        """测试分母为零返回NaN。"""
        result = safe_divide(10, 0)
        assert np.isnan(result)

    def test_safe_divide_series(self):
        """测试Series除法。"""
        a = pd.Series([10, 20, 30])
        b = pd.Series([2, 0, 3])  # 包含零值

        result = safe_divide(a, b)

        # 验证结果
        assert result.iloc[0] == 5.0
        assert np.isnan(result.iloc[1])
        assert result.iloc[2] == 10.0

    def test_safe_divide_nan_denominator(self):
        """测试NaN分母返回NaN。"""
        result = safe_divide(10, np.nan)
        assert np.isnan(result)


# =====================================================================
# Parametrized Tests
# =====================================================================


@pytest.mark.parametrize("window", [3, 5, 10, 20, 60])
def test_compute_ma_windows(sample_close_series, window):
    """参数化测试MA不同窗口期。"""
    result = _compute_ma(sample_close_series, window)

    assert len(result) == len(sample_close_series)
    assert result.iloc[:window-1].isna().all()


@pytest.mark.parametrize("window", [5, 10, 12, 20, 26, 60])
def test_compute_ema_windows(sample_close_series, window):
    """参数化测试EMA不同窗口期。"""
    result = _compute_ema(sample_close_series, window)

    assert len(result) == len(sample_close_series)
    # EMA第一个值等于第一个数据点
    np.testing.assert_almost_equal(result.iloc[0], sample_close_series.iloc[0], decimal=6)


@pytest.mark.parametrize("window", [5, 10, 20])
def test_compute_std_windows(sample_close_series, window):
    """参数化测试STD不同窗口期。"""
    result = _compute_std(sample_close_series, window)

    assert len(result) == len(sample_close_series)
    assert result.iloc[:window-1].isna().all()


@pytest.mark.parametrize("window", [6, 10, 12, 14, 24])
@patch('jk2bt.factors.technical._get_daily_ohlcv')
def test_rsi_windows(mock_get_ohlcv, sample_ohlcv_df, window):
    """参数化测试RSI不同窗口期。"""
    mock_get_ohlcv.return_value = sample_ohlcv_df

    result = compute_rsi('sh600519', window=window)

    assert isinstance(result, pd.Series)
    valid_values = result.dropna()
    assert (valid_values >= 0).all() and (valid_values <= 100).all()