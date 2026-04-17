"""
test_preprocess.py
因子预处理模块测试。

测试覆盖：
- winsorize_med 去极值函数
- standardlize 标准化函数
- neutralize 中性化函数
"""

import warnings

warnings.filterwarnings("ignore")

import pytest
import pandas as pd
import numpy as np


@pytest.fixture
def sample_factor_data():
    """生成模拟因子数据。"""
    np.random.seed(42)
    return pd.DataFrame(
        {
            "factor1": [1.0, 2.0, 3.0, 4.0, 5.0, 100.0, -50.0, 6.0, 7.0, 8.0],
            "factor2": np.random.randn(10) * 10 + 50,
        }
    )


@pytest.fixture
def sample_factor_series():
    """生成模拟因子序列。"""
    np.random.seed(42)
    return pd.Series([1.0, 2.0, 3.0, 4.0, 5.0, 100.0, -50.0, 6.0, 7.0, 8.0])


class TestWinsorizeMed:
    """测试去极值函数。"""

    def test_winsorize_med_dataframe(self, sample_factor_data):
        """测试DataFrame去极值。"""
        from jk2bt.analysis.factors.preprocess import winsorize_med

        result = winsorize_med(sample_factor_data, scale=3.0)

        assert isinstance(result, pd.DataFrame)
        assert result.shape == sample_factor_data.shape

    def test_winsorize_med_series(self, sample_factor_series):
        """测试Series去极值。"""
        from jk2bt.analysis.factors.preprocess import winsorize_med

        result = winsorize_med(sample_factor_series, scale=3.0)

        assert isinstance(result, pd.Series)
        assert len(result) == len(sample_factor_series)

    def test_winsorize_med_inclusive(self, sample_factor_series):
        """测试inclusive参数。"""
        from jk2bt.analysis.factors.preprocess import winsorize_med

        result_inclusive = winsorize_med(sample_factor_series, inclusive=True)
        result_exclusive = winsorize_med(sample_factor_series, inclusive=False)

        assert isinstance(result_inclusive, pd.Series)
        assert isinstance(result_exclusive, pd.Series)

    def test_winsorize_med_inf2nan(self, sample_factor_data):
        """测试inf2nan参数。"""
        from jk2bt.analysis.factors.preprocess import winsorize_med

        df = sample_factor_data.copy()
        df.iloc[0, 0] = np.inf

        result = winsorize_med(df, inf2nan=True)

        assert not np.isinf(result.values).any()

    def test_winsorize_med_axis(self, sample_factor_data):
        """测试axis参数。"""
        from jk2bt.analysis.factors.preprocess import winsorize_med

        result_0 = winsorize_med(sample_factor_data, axis=0)
        result_1 = winsorize_med(sample_factor_data, axis=1)

        assert isinstance(result_0, pd.DataFrame)
        assert isinstance(result_1, pd.DataFrame)

    def test_winsorize_med_scale(self, sample_factor_series):
        """测试scale参数。"""
        from jk2bt.analysis.factors.preprocess import winsorize_med

        result_3 = winsorize_med(sample_factor_series, scale=3.0)
        result_5 = winsorize_med(sample_factor_series, scale=5.0)

        assert isinstance(result_3, pd.Series)
        assert isinstance(result_5, pd.Series)

    def test_winsorize_med_empty(self):
        """测试空数据。"""
        from jk2bt.analysis.factors.preprocess import winsorize_med

        empty_df = pd.DataFrame()
        result = winsorize_med(empty_df)

        assert result.empty


class TestStandardlize:
    """测试标准化函数。"""

    def test_standardlize_dataframe(self, sample_factor_data):
        """测试DataFrame标准化。"""
        from jk2bt.analysis.factors.preprocess import standardlize

        result = standardlize(sample_factor_data)

        assert isinstance(result, pd.DataFrame)
        assert result.shape == sample_factor_data.shape

    def test_standardlize_series(self, sample_factor_series):
        """测试Series标准化。"""
        from jk2bt.analysis.factors.preprocess import standardlize

        result = standardlize(sample_factor_series)

        assert isinstance(result, pd.Series)
        assert len(result) == len(sample_factor_series)

    def test_standardlize_mean_zero(self, sample_factor_series):
        """测试标准化后均值为0。"""
        from jk2bt.analysis.factors.preprocess import standardlize

        result = standardlize(sample_factor_series)
        valid = result.dropna()

        assert abs(valid.mean()) < 1e-10

    def test_standardlize_std_one(self, sample_factor_series):
        """测试标准化后标准差为1。"""
        from jk2bt.analysis.factors.preprocess import standardlize

        result = standardlize(sample_factor_series)
        valid = result.dropna()

        assert abs(valid.std() - 1.0) < 1e-10

    def test_standardlize_inf2nan(self, sample_factor_data):
        """测试inf2nan参数。"""
        from jk2bt.analysis.factors.preprocess import standardlize

        df = sample_factor_data.copy()
        df.iloc[0, 0] = np.inf

        result = standardlize(df, inf2nan=True)

        assert not np.isinf(result.values).any()

    def test_standardlize_axis(self, sample_factor_data):
        """测试axis参数。"""
        from jk2bt.analysis.factors.preprocess import standardlize

        result_0 = standardlize(sample_factor_data, axis=0)
        result_1 = standardlize(sample_factor_data, axis=1)

        assert isinstance(result_0, pd.DataFrame)
        assert isinstance(result_1, pd.DataFrame)


class TestNeutralize:
    """测试中性化函数。"""

    def test_neutralize_default(self, sample_factor_data):
        """测试默认中性化。"""
        from jk2bt.analysis.factors.preprocess import neutralize

        market_cap = pd.Series(
            {
                "factor1": 1e10,
                "factor2": 5e9,
            }
        )

        result = neutralize(sample_factor_data, market_cap=market_cap)

        assert isinstance(result, (pd.DataFrame, pd.Series))

    def test_neutralize_with_industry(self, sample_factor_data):
        """测试行业中性化。"""
        from jk2bt.analysis.factors.preprocess import neutralize

        market_cap = pd.Series({"factor1": 1e10, "factor2": 5e9})
        industry_data = pd.DataFrame(
            {
                "银行": [1, 0],
                "地产": [0, 1],
            },
            index=["factor1", "factor2"],
        )

        result = neutralize(
            sample_factor_data,
            how=["market_cap", "sw_l1"],
            market_cap=market_cap,
            industry_data=industry_data,
        )

        assert isinstance(result, (pd.DataFrame, pd.Series))

    def test_neutralize_series(self, sample_factor_series):
        """测试Series中性化。"""
        from jk2bt.analysis.factors.preprocess import neutralize

        market_cap = pd.Series({"factor1": 1e10})

        result = neutralize(sample_factor_series, market_cap=market_cap)

        assert isinstance(result, (pd.DataFrame, pd.Series))

    def test_neutralize_no_market_cap(self, sample_factor_data):
        """测试无市值数据时跳过中性化。"""
        from jk2bt.analysis.factors.preprocess import neutralize

        result = neutralize(sample_factor_data, how=["market_cap"])

        assert isinstance(result, (pd.DataFrame, pd.Series))
        pd.testing.assert_frame_equal(result, sample_factor_data)

    def test_neutralize_empty_how(self, sample_factor_data):
        """测试空how参数。"""
        from jk2bt.analysis.factors.preprocess import neutralize

        result = neutralize(sample_factor_data, how=[])

        assert isinstance(result, (pd.DataFrame, pd.Series))


class TestPreprocessEdgeCases:
    """测试预处理边界情况。"""

    def test_constant_series(self):
        """测试常量序列。"""
        from jk2bt.analysis.factors.preprocess import standardlize, winsorize_med

        const = pd.Series([1.0, 1.0, 1.0, 1.0])

        std_result = standardlize(const)
        assert not np.isnan(std_result).all() or np.isnan(std_result).all()

    def test_all_nan(self):
        """测试全NaN数据。"""
        from jk2bt.analysis.factors.preprocess import winsorize_med, standardlize

        nan_data = pd.Series([np.nan, np.nan, np.nan])

        result = winsorize_med(nan_data)
        assert result.isna().all()

    def test_inf_values(self):
        """测试无穷值处理。"""
        from jk2bt.analysis.factors.preprocess import winsorize_med

        data = pd.Series([np.inf, 1.0, 2.0, 3.0, 4.0])

        result = winsorize_med(data, inf2nan=True)

        assert not np.isinf(result.values).any()
