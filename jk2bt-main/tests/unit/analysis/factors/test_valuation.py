"""
test_valuation.py
估值因子模块单元测试。

测试范围：
- _normalize_symbol: 股票代码标准化
- _validate_valuation_data: 估值数据质量验证
- _clean_valuation_data: 异常值清理
- compute_market_cap: 总市值计算
- compute_circulating_market_cap: 流通市值计算
- compute_pe_ratio: 市盈率计算
- compute_pb_ratio: 市净率计算
- compute_ps_ratio: 市销率计算
- compute_pcf_ratio: 市现率计算
- compute_turnover_ratio: 换手率计算
- compute_capitalization: 总股本计算
- compute_circulating_cap: 流通股本计算
- compute_natural_log_of_market_cap: 市值对数计算
- compute_cube_of_size: 规模立方计算

测试策略：
- Mock 数据获取函数，避免网络请求
- 测试边界条件（负值、零值、缺失值）
- 验证计算结果正确性
"""

import warnings
from unittest.mock import patch, MagicMock

import pytest
import pandas as pd
import numpy as np

from jk2bt.analysis.factors.valuation import (
    _validate_valuation_data,
    _clean_valuation_data,
    _normalize_valuation_df,
    _estimate_circulating_market_cap_from_daily,
    compute_market_cap,
    compute_circulating_market_cap,
    compute_pe_ratio,
    compute_pb_ratio,
    compute_ps_ratio,
    compute_pcf_ratio,
    compute_turnover_ratio,
    compute_capitalization,
    compute_circulating_cap,
    compute_natural_log_of_market_cap,
    compute_cube_of_size,
)
from jk2bt.analysis.factors.base import global_factor_registry, safe_divide
from jk2bt.utils.symbol import normalize_symbol as _normalize_symbol

warnings.filterwarnings("ignore")


@pytest.fixture
def sample_valuation_data():
    """创建模拟估值数据 DataFrame。"""
    dates = pd.date_range("2024-01-01", periods=10, freq="D").strftime("%Y-%m-%d")
    return pd.DataFrame(
        {
            "date": dates,
            "market_cap": [
                2000.0,
                2100.0,
                2200.0,
                2300.0,
                2400.0,
                2500.0,
                2600.0,
                2700.0,
                2800.0,
                2900.0,
            ],
            "circulating_market_cap": [
                1500.0,
                1550.0,
                1600.0,
                1650.0,
                1700.0,
                1750.0,
                1800.0,
                1850.0,
                1900.0,
                1950.0,
            ],
            "pe_ratio": [25.0, 26.0, 27.0, 28.0, 29.0, 30.0, 31.0, 32.0, 33.0, 34.0],
            "pb_ratio": [3.0, 3.1, 3.2, 3.3, 3.4, 3.5, 3.6, 3.7, 3.8, 3.9],
            "ps_ratio": [5.0, 5.1, 5.2, 5.3, 5.4, 5.5, 5.6, 5.7, 5.8, 5.9],
            "pcf_ratio": [10.0, 10.5, 11.0, 11.5, 12.0, 12.5, 13.0, 13.5, 14.0, 14.5],
        }
    )


@pytest.fixture
def sample_daily_data():
    """创建模拟日线数据 DataFrame。"""
    dates = pd.date_range("2024-01-01", periods=10, freq="D").strftime("%Y-%m-%d")
    return pd.DataFrame(
        {
            "date": dates,
            "open": [100.0] * 10,
            "high": [105.0] * 10,
            "low": [95.0] * 10,
            "close": [
                102.0,
                103.0,
                104.0,
                105.0,
                106.0,
                107.0,
                108.0,
                109.0,
                110.0,
                111.0,
            ],
            "volume": [1000.0] * 10,
            "turnover_rate": [0.5, 0.6, 0.7, 0.8, 0.9, 1.0, 1.1, 1.2, 1.3, 1.4],
        }
    )


@pytest.fixture
def valuation_data_with_issues():
    """创建包含异常值的估值数据。"""
    dates = pd.date_range("2024-01-01", periods=10, freq="D").strftime("%Y-%m-%d")
    return pd.DataFrame(
        {
            "date": dates,
            "market_cap": [
                2000.0,
                0.0,
                -100.0,
                np.nan,
                2400.0,
                2500.0,
                2600.0,
                2700.0,
                2800.0,
                2900.0,
            ],
            "pe_ratio": [
                25.0,
                -150.0,
                800.0,
                np.nan,
                29.0,
                30.0,
                31.0,
                32.0,
                33.0,
                34.0,
            ],
            "pb_ratio": [3.0, -15.0, 150.0, np.nan, 3.4, 3.5, 3.6, 3.7, 3.8, 3.9],
            "circulating_market_cap": [
                1500.0,
                0.0,
                -50.0,
                np.nan,
                1700.0,
                1750.0,
                1800.0,
                1850.0,
                1900.0,
                1950.0,
            ],
        }
    )


@pytest.fixture
def empty_dataframe():
    """创建空 DataFrame。"""
    return pd.DataFrame()


@pytest.fixture
def missing_column_df():
    """创建缺失关键列的 DataFrame。"""
    return pd.DataFrame(
        {
            "date": ["2024-01-01", "2024-01-02"],
            "other_col": [1.0, 2.0],
        }
    )


class TestNormalizeSymbol:
    """测试股票代码标准化函数。"""

    def test_normalize_sh_prefix(self):
        result = _normalize_symbol("sh600519")
        assert result == "600519"

    def test_normalize_sz_prefix(self):
        result = _normalize_symbol("sz000001")
        assert result == "000001"

    def test_normalize_xshg_suffix(self):
        result = _normalize_symbol("600519.XSHG")
        assert result == "600519"

    def test_normalize_xshe_suffix(self):
        result = _normalize_symbol("000001.XSHE")
        assert result == "000001"

    def test_normalize_short_code(self):
        result = _normalize_symbol("1")
        assert result == "000001"

    def test_normalize_already_standard(self):
        result = _normalize_symbol("600519")
        assert result == "600519"

    def test_normalize_combined_prefix_suffix(self):
        result = _normalize_symbol("sh600519.XSHG")
        assert result == "sh6005"

    def test_normalize_standard_combined(self):
        result = _normalize_symbol("600519.XSHG")
        assert result == "600519"


class TestValidateValuationData:
    """测试估值数据质量验证函数。"""

    def test_validate_valid_data(self, sample_valuation_data):
        result = _validate_valuation_data(sample_valuation_data, "sh600519")

        assert result["is_valid"] is True
        assert result["data_count"] == 10
        assert len(result["issues"]) == 0

    def test_validate_empty_data(self, empty_dataframe):
        result = _validate_valuation_data(empty_dataframe, "sh600519")

        assert result["is_valid"] is False
        assert "empty_data" in result["issues"]
        assert result["data_count"] == 0

    def test_validate_none_data(self):
        result = _validate_valuation_data(None, "sh600519")

        assert result["is_valid"] is False
        assert "empty_data" in result["issues"]

    def test_validate_high_missing_rate(self):
        dates = pd.date_range("2024-01-01", periods=10, freq="D").strftime("%Y-%m-%d")
        df = pd.DataFrame(
            {
                "date": dates,
                "pe_ratio": [np.nan] * 8 + [25.0, 26.0],
                "pb_ratio": [3.0] * 10,
                "market_cap": [2000.0] * 10,
            }
        )

        result = _validate_valuation_data(df, "sh600519")

        assert result["is_valid"] is False
        assert "high_missing_pe_ratio" in result["issues"]

    def test_validate_negative_pe_ratio(self):
        dates = pd.date_range("2024-01-01", periods=10, freq="D").strftime("%Y-%m-%d")
        df = pd.DataFrame(
            {
                "date": dates,
                "pe_ratio": [
                    -10.0,
                    -20.0,
                    -30.0,
                    -40.0,
                    25.0,
                    26.0,
                    27.0,
                    28.0,
                    29.0,
                    30.0,
                ],
                "pb_ratio": [3.0] * 10,
                "market_cap": [2000.0] * 10,
            }
        )

        result = _validate_valuation_data(df, "sh600519")

        assert "excessive_negative_pe" in result["issues"]

    def test_validate_extreme_pe_ratio(self):
        dates = pd.date_range("2024-01-01", periods=10, freq="D").strftime("%Y-%m-%d")
        df = pd.DataFrame(
            {
                "date": dates,
                "pe_ratio": [
                    600.0,
                    700.0,
                    25.0,
                    26.0,
                    27.0,
                    28.0,
                    29.0,
                    30.0,
                    31.0,
                    32.0,
                ],
                "pb_ratio": [3.0] * 10,
                "market_cap": [2000.0] * 10,
            }
        )

        result = _validate_valuation_data(df, "sh600519")

        assert "excessive_extreme_pe" in result["issues"]

    def test_validate_invalid_pb_range(self):
        dates = pd.date_range("2024-01-01", periods=10, freq="D").strftime("%Y-%m-%d")
        df = pd.DataFrame(
            {
                "date": dates,
                "pe_ratio": [25.0] * 10,
                "pb_ratio": [
                    -10.0,
                    60.0,
                    3.0,
                    3.1,
                    3.2,
                    3.3,
                    3.4,
                    3.5,
                    3.6,
                    3.7,
                ],
                "market_cap": [2000.0] * 10,
            }
        )

        result = _validate_valuation_data(df, "sh600519")

        assert "invalid_pb_range" in result["issues"]

    def test_validate_zero_market_cap(self):
        dates = pd.date_range("2024-01-01", periods=10, freq="D").strftime("%Y-%m-%d")
        df = pd.DataFrame(
            {
                "date": dates,
                "pe_ratio": [25.0] * 10,
                "pb_ratio": [3.0] * 10,
                "market_cap": [
                    0.0,
                    2000.0,
                    2100.0,
                    2200.0,
                    2300.0,
                    2400.0,
                    2500.0,
                    2600.0,
                    2700.0,
                    2800.0,
                ],
            }
        )

        result = _validate_valuation_data(df, "sh600519")

        assert "zero_market_cap" in result["issues"]

    def test_validate_missing_column(self, missing_column_df):
        result = _validate_valuation_data(missing_column_df, "sh600519")

        assert "missing_col_pe_ratio" in result["issues"]
        assert "missing_col_pb_ratio" in result["issues"]
        assert "missing_col_market_cap" in result["issues"]


class TestCleanValuationData:
    """测试异常值清理函数。"""

    def test_clean_extreme_pe_ratio(self, valuation_data_with_issues):
        result = _clean_valuation_data(valuation_data_with_issues)

        assert np.isnan(result.loc[1, "pe_ratio"])
        assert result.loc[2, "pe_ratio"] == 800.0
        assert result.loc[0, "pe_ratio"] == 25.0

    def test_clean_extreme_pb_ratio(self, valuation_data_with_issues):
        result = _clean_valuation_data(valuation_data_with_issues)

        assert np.isnan(result.loc[1, "pb_ratio"])
        assert np.isnan(result.loc[2, "pb_ratio"])
        assert result.loc[0, "pb_ratio"] == 3.0

    def test_clean_zero_or_negative_market_cap(self, valuation_data_with_issues):
        result = _clean_valuation_data(valuation_data_with_issues)

        assert np.isnan(result.loc[1, "market_cap"])
        assert np.isnan(result.loc[2, "market_cap"])

    def test_clean_zero_circulating_market_cap(self, valuation_data_with_issues):
        result = _clean_valuation_data(valuation_data_with_issues)

        assert np.isnan(result.loc[1, "circulating_market_cap"])
        assert np.isnan(result.loc[2, "circulating_market_cap"])

    def test_clean_empty_data(self, empty_dataframe):
        result = _clean_valuation_data(empty_dataframe)

        assert result.empty

    def test_clean_none_data(self):
        result = _clean_valuation_data(None)

        assert result is None

    def test_clean_preserves_valid_data(self, sample_valuation_data):
        result = _clean_valuation_data(sample_valuation_data)

        assert result["market_cap"].equals(sample_valuation_data["market_cap"])
        assert result["pe_ratio"].equals(sample_valuation_data["pe_ratio"])
        assert result["pb_ratio"].equals(sample_valuation_data["pb_ratio"])


class TestComputeMarketCap:
    """测试总市值计算函数。"""

    @patch("jk2bt.analysis.factors.valuation._get_valuation_raw")
    def test_compute_market_cap_single_value(self, mock_get_raw, sample_valuation_data):
        mock_get_raw.return_value = sample_valuation_data

        result = compute_market_cap("sh600519", end_date="2024-01-01", count=1)

        assert isinstance(result, float)
        assert result == 2000.0

    @patch("jk2bt.analysis.factors.valuation._get_valuation_raw")
    def test_compute_market_cap_series(self, mock_get_raw, sample_valuation_data):
        mock_get_raw.return_value = sample_valuation_data

        result = compute_market_cap("sh600519", count=5)

        assert isinstance(result, pd.Series)
        assert len(result) == 5

    @patch("jk2bt.analysis.factors.valuation._get_valuation_raw")
    def test_compute_market_cap_empty_data(self, mock_get_raw, empty_dataframe):
        mock_get_raw.return_value = empty_dataframe

        result = compute_market_cap("sh600519")

        assert np.isnan(result)

    @patch("jk2bt.analysis.factors.valuation._get_valuation_raw")
    def test_compute_market_cap_missing_column(self, mock_get_raw, missing_column_df):
        mock_get_raw.return_value = missing_column_df

        result = compute_market_cap("sh600519")

        assert np.isnan(result)

    @patch("jk2bt.analysis.factors.valuation._get_valuation_raw")
    def test_compute_market_cap_with_end_date(
        self, mock_get_raw, sample_valuation_data
    ):
        mock_get_raw.return_value = sample_valuation_data

        result = compute_market_cap("sh600519", end_date="2024-01-05")

        assert isinstance(result, pd.Series)
        assert len(result) <= 5


class TestComputeCirculatingMarketCap:
    """测试流通市值计算函数。"""

    @patch("jk2bt.analysis.factors.valuation._get_valuation_raw")
    def test_compute_circulating_market_cap_single_value(
        self, mock_get_raw, sample_valuation_data
    ):
        mock_get_raw.return_value = sample_valuation_data

        result = compute_circulating_market_cap(
            "sh600519", end_date="2024-01-01", count=1
        )

        assert isinstance(result, float)
        assert result == 1500.0

    @patch("jk2bt.analysis.factors.valuation._get_valuation_raw")
    def test_compute_circulating_market_cap_series(
        self, mock_get_raw, sample_valuation_data
    ):
        mock_get_raw.return_value = sample_valuation_data

        result = compute_circulating_market_cap("sh600519", count=5)

        assert isinstance(result, pd.Series)
        assert len(result) == 5

    @patch("jk2bt.analysis.factors.valuation._get_valuation_raw")
    def test_compute_circulating_market_cap_missing_column(
        self, mock_get_raw, sample_valuation_data
    ):
        df_no_circ = sample_valuation_data.drop(columns=["circulating_market_cap"])
        mock_get_raw.return_value = df_no_circ

        result = compute_circulating_market_cap("sh600519")

        assert np.isnan(result)


class TestComputePeRatio:
    """测试市盈率计算函数。"""

    @patch("jk2bt.analysis.factors.valuation._get_valuation_raw")
    def test_compute_pe_ratio_single_value(self, mock_get_raw, sample_valuation_data):
        mock_get_raw.return_value = sample_valuation_data

        result = compute_pe_ratio("sh600519", end_date="2024-01-01", count=1)

        assert isinstance(result, float)
        assert result == 25.0

    @patch("jk2bt.analysis.factors.valuation._get_valuation_raw")
    def test_compute_pe_ratio_series(self, mock_get_raw, sample_valuation_data):
        mock_get_raw.return_value = sample_valuation_data

        result = compute_pe_ratio("sh600519", count=5)

        assert isinstance(result, pd.Series)
        assert len(result) == 5

    @patch("jk2bt.analysis.factors.valuation._get_valuation_raw")
    def test_compute_pe_ratio_missing_column(self, mock_get_raw, missing_column_df):
        mock_get_raw.return_value = missing_column_df

        result = compute_pe_ratio("sh600519")

        assert np.isnan(result)


class TestComputePbRatio:
    """测试市净率计算函数。"""

    @patch("jk2bt.analysis.factors.valuation._get_valuation_raw")
    def test_compute_pb_ratio_single_value(self, mock_get_raw, sample_valuation_data):
        mock_get_raw.return_value = sample_valuation_data

        result = compute_pb_ratio("sh600519", end_date="2024-01-01", count=1)

        assert isinstance(result, float)
        assert result == 3.0

    @patch("jk2bt.analysis.factors.valuation._get_valuation_raw")
    def test_compute_pb_ratio_series(self, mock_get_raw, sample_valuation_data):
        mock_get_raw.return_value = sample_valuation_data

        result = compute_pb_ratio("sh600519", count=5)

        assert isinstance(result, pd.Series)
        assert len(result) == 5


class TestComputePsRatio:
    """测试市销率计算函数。"""

    @patch("jk2bt.analysis.factors.valuation._get_valuation_raw")
    def test_compute_ps_ratio_single_value(self, mock_get_raw, sample_valuation_data):
        mock_get_raw.return_value = sample_valuation_data

        result = compute_ps_ratio("sh600519", end_date="2024-01-01", count=1)

        assert isinstance(result, float)
        assert result == 5.0

    @patch("jk2bt.analysis.factors.valuation._get_valuation_raw")
    def test_compute_ps_ratio_missing_column(self, mock_get_raw, sample_valuation_data):
        df_no_ps = sample_valuation_data.drop(columns=["ps_ratio"])
        mock_get_raw.return_value = df_no_ps

        result = compute_ps_ratio("sh600519")

        assert np.isnan(result)


class TestComputePcfRatio:
    """测试市现率计算函数。"""

    @patch("jk2bt.analysis.factors.valuation._normalize_symbol")
    @patch("os.path.exists")
    @patch("pandas.read_pickle")
    @patch("os.makedirs")
    def test_compute_pcf_ratio_from_cache(
        self, mock_makedirs, mock_read_pickle, mock_exists, mock_normalize
    ):
        mock_normalize.return_value = "600519"
        mock_exists.return_value = True
        mock_read_pickle.return_value = pd.DataFrame(
            {
                "date": ["2024-01-01", "2024-01-02"],
                "pcf_ratio": [10.0, 11.0],
            }
        )

        result = compute_pcf_ratio("sh600519", end_date="2024-01-01", count=1)

        assert isinstance(result, float)
        assert result == 10.0


class TestComputeTurnoverRatio:
    """测试换手率计算函数。"""

    @patch("jk2bt.analysis.factors.technical._get_daily_ohlcv")
    def test_compute_turnover_ratio_basic(self, mock_get_ohlcv):
        dates = pd.date_range("2024-01-01", periods=5, freq="D").strftime("%Y-%m-%d")
        mock_daily_df = pd.DataFrame(
            {
                "date": dates,
                "close": [100.0] * 5,
                "turnover_rate": [0.5, 0.6, 0.7, 0.8, 0.9],
            }
        )
        mock_get_ohlcv.return_value = mock_daily_df

        result = compute_turnover_ratio("sh600519", count=1)

        mock_get_ohlcv.assert_called_once()


class TestComputeCapitalization:
    """测试总股本计算函数。"""

    @patch("jk2bt.analysis.factors.valuation.compute_market_cap")
    @patch("jk2bt.analysis.factors.technical._get_daily_ohlcv")
    def test_compute_capitalization_nan_market_cap(
        self, mock_get_ohlcv, mock_market_cap
    ):
        mock_market_cap.return_value = np.nan
        mock_get_ohlcv.return_value = pd.DataFrame(
            {
                "date": ["2024-01-01"],
                "close": [100.0],
            }
        )

        result = compute_capitalization("sh600519")

        assert np.isnan(result)


class TestComputeCirculatingCap:
    """测试流通股本计算函数。"""

    @patch("jk2bt.analysis.factors.valuation.compute_circulating_market_cap")
    @patch("jk2bt.analysis.factors.technical._get_daily_ohlcv")
    def test_compute_circulating_cap_nan_value(self, mock_get_ohlcv, mock_circ_cap):
        mock_circ_cap.return_value = np.nan
        mock_get_ohlcv.return_value = pd.DataFrame(
            {
                "date": ["2024-01-01"],
                "close": [100.0],
            }
        )

        result = compute_circulating_cap("sh600519")

        assert np.isnan(result)


class TestComputeNaturalLogOfMarketCap:
    """测试市值对数计算函数。"""

    @patch("jk2bt.analysis.factors.valuation.compute_market_cap")
    def test_compute_log_market_cap_single_value(self, mock_market_cap):
        mock_market_cap.return_value = 2000.0

        result = compute_natural_log_of_market_cap("sh600519")

        assert isinstance(result, float)
        assert np.isclose(result, np.log(2000.0))

    @patch("jk2bt.analysis.factors.valuation.compute_market_cap")
    def test_compute_log_market_cap_series(self, mock_market_cap):
        dates = ["2024-01-01", "2024-01-02", "2024-01-03"]
        mock_market_cap.return_value = pd.Series([2000.0, 2100.0, 2200.0], index=dates)

        result = compute_natural_log_of_market_cap("sh600519")

        assert isinstance(result, pd.Series)
        assert len(result) == 3
        assert np.isclose(result.iloc[0], np.log(2000.0))

    @patch("jk2bt.analysis.factors.valuation.compute_market_cap")
    def test_compute_log_market_cap_zero_value(self, mock_market_cap):
        mock_market_cap.return_value = 0.0

        result = compute_natural_log_of_market_cap("sh600519")

        assert np.isnan(result)

    @patch("jk2bt.analysis.factors.valuation.compute_market_cap")
    def test_compute_log_market_cap_negative_value(self, mock_market_cap):
        mock_market_cap.return_value = -100.0

        result = compute_natural_log_of_market_cap("sh600519")

        assert np.isnan(result)

    @patch("jk2bt.analysis.factors.valuation.compute_market_cap")
    def test_compute_log_market_cap_series_with_zeros(self, mock_market_cap):
        dates = ["2024-01-01", "2024-01-02", "2024-01-03"]
        mock_market_cap.return_value = pd.Series([2000.0, 0.0, -100.0], index=dates)

        result = compute_natural_log_of_market_cap("sh600519")

        assert isinstance(result, pd.Series)
        assert np.isclose(result.iloc[0], np.log(2000.0))
        assert np.isnan(result.iloc[1])
        assert np.isnan(result.iloc[2])


class TestComputeCubeOfSize:
    """测试规模立方计算函数。"""

    @patch("jk2bt.analysis.factors.valuation.compute_natural_log_of_market_cap")
    def test_compute_cube_of_size_single_value(self, mock_log_cap):
        log_value = np.log(2000.0)
        mock_log_cap.return_value = log_value

        result = compute_cube_of_size("sh600519")

        assert isinstance(result, float)
        assert np.isclose(result, log_value**3)

    @patch("jk2bt.analysis.factors.valuation.compute_natural_log_of_market_cap")
    def test_compute_cube_of_size_series(self, mock_log_cap):
        dates = ["2024-01-01", "2024-01-02", "2024-01-03"]
        log_values = pd.Series(
            [np.log(2000.0), np.log(2100.0), np.log(2200.0)], index=dates
        )
        mock_log_cap.return_value = log_values

        result = compute_cube_of_size("sh600519")

        assert isinstance(result, pd.Series)
        assert len(result) == 3
        assert np.isclose(result.iloc[0], np.log(2000.0) ** 3)

    @patch("jk2bt.analysis.factors.valuation.compute_natural_log_of_market_cap")
    def test_compute_cube_of_size_nan_value(self, mock_log_cap):
        mock_log_cap.return_value = np.nan

        result = compute_cube_of_size("sh600519")

        assert np.isnan(result)


class TestNormalizeValuationDf:
    """测试估值数据标准化函数。"""

    def test_normalize_with_valid_data(self, sample_valuation_data):
        result = _normalize_valuation_df(sample_valuation_data)

        assert "date" in result.columns
        assert "market_cap" in result.columns
        assert "pb_ratio" in result.columns

    def test_normalize_empty_data(self, empty_dataframe):
        result = _normalize_valuation_df(empty_dataframe)

        assert result.empty

    def test_normalize_none_data(self):
        result = _normalize_valuation_df(None)

        assert result.empty

    def test_normalize_missing_date_column(self):
        df = pd.DataFrame(
            {
                "market_cap": [2000.0, 2100.0],
                "pb_ratio": [3.0, 3.1],
            }
        )

        result = _normalize_valuation_df(df)

        assert "date" in result.columns
        assert pd.isna(result["date"].iloc[0])
        assert "market_cap" in result.columns

    def test_normalize_column_mapping(self):
        df = pd.DataFrame(
            {
                "date": ["2024-01-01", "2024-01-02"],
                "pb": [3.0, 3.1],
            }
        )

        result = _normalize_valuation_df(df)

        assert "pb_ratio" in result.columns
        assert "pb" not in result.columns


class TestEstimateCirculatingMarketCap:
    """测试从日线数据推算流通市值函数。"""

    def test_estimate_circulating_cap_success(self):
        mock_ak = MagicMock()
        mock_ak.stock_zh_a_hist.return_value = pd.DataFrame(
            {
                "日期": ["2024-01-01", "2024-01-02"],
                "收盘": [100.0, 101.0],
                "成交量": [1000.0, 1100.0],
                "换手率": [0.5, 0.6],
            }
        )

        result = _estimate_circulating_market_cap_from_daily(mock_ak, "600519")

        assert "date" in result.columns
        assert "circulating_market_cap" in result.columns
        assert len(result) == 2

    def test_estimate_circulating_cap_empty_response(self):
        mock_ak = MagicMock()
        mock_ak.stock_zh_a_hist.return_value = pd.DataFrame()

        result = _estimate_circulating_market_cap_from_daily(mock_ak, "600519")

        assert result.empty


class TestFactorRegistration:
    """测试因子注册功能。"""

    def test_factors_registered_in_registry(self):
        expected_factors = [
            "market_cap",
            "circulating_market_cap",
            "pe_ratio",
            "pb_ratio",
            "ps_ratio",
            "pcf_ratio",
            "turnover_ratio",
            "capitalization",
            "circulating_cap",
            "natural_log_of_market_cap",
            "cube_of_size",
        ]

        for factor_name in expected_factors:
            assert global_factor_registry.is_registered(factor_name), (
                f"{factor_name} 未注册"
            )

    def test_factor_metadata(self):
        metadata = global_factor_registry.get_metadata("market_cap")
        assert metadata["window"] == 1
        assert "valuation" in metadata["dependencies"]

        metadata = global_factor_registry.get_metadata("natural_log_of_market_cap")
        assert "market_cap" in metadata["dependencies"]

    def test_get_factor_function(self):
        func = global_factor_registry.get("market_cap")
        assert func is not None
        assert callable(func)


class TestSafeDivide:
    """测试安全除法函数。"""

    def test_safe_divide_normal(self):
        result = safe_divide(10.0, 2.0)
        assert result == 5.0

    def test_safe_divide_zero_denominator(self):
        result = safe_divide(10.0, 0.0)
        assert np.isnan(result)

    def test_safe_divide_nan_denominator(self):
        result = safe_divide(10.0, np.nan)
        assert np.isnan(result)

    def test_safe_divide_series(self):
        a = pd.Series([10.0, 20.0, 30.0])
        b = pd.Series([2.0, 0.0, 3.0])

        result = safe_divide(a, b)

        assert result.iloc[0] == 5.0
        assert np.isnan(result.iloc[1])
        assert result.iloc[2] == 10.0

    def test_safe_divide_array(self):
        a = np.array([10.0, 20.0, 30.0])
        b = np.array([2.0, 0.0, 3.0])

        result = safe_divide(a, b)

        assert result[0] == 5.0
        assert np.isnan(result[1])
        assert result[2] == 10.0


class TestEdgeCases:
    """测试各种边界条件。"""

    @patch("jk2bt.analysis.factors.valuation._get_valuation_raw")
    def test_all_nan_data(self, mock_get_raw):
        df = pd.DataFrame(
            {
                "date": ["2024-01-01", "2024-01-02"],
                "market_cap": [np.nan, np.nan],
            }
        )
        mock_get_raw.return_value = df

        result = compute_market_cap("sh600519", end_date="2024-01-01", count=1)

        assert np.isnan(result)

    @patch("jk2bt.analysis.factors.valuation._get_valuation_raw")
    def test_single_row_data(self, mock_get_raw):
        df = pd.DataFrame(
            {
                "date": ["2024-01-01"],
                "market_cap": [2000.0],
            }
        )
        mock_get_raw.return_value = df

        result = compute_market_cap("sh600519", count=1)

        assert isinstance(result, float)
        assert result == 2000.0

    def test_empty_symbol(self):
        result = _normalize_symbol("")
        assert result == "000000"

    def test_very_large_market_cap(self):
        df = pd.DataFrame(
            {
                "date": ["2024-01-01"],
                "market_cap": [1e10],
                "pe_ratio": [25.0],
                "pb_ratio": [3.0],
            }
        )

        result = _validate_valuation_data(df, "sh600519")

        assert result["is_valid"] is True


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
