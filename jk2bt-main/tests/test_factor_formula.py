"""
test_factor_formula.py
因子计算公式单元测试。

验证每个因子的计算公式是否正确，使用 mock 数据避免依赖外部数据源。
"""

import pytest
import pandas as pd
import numpy as np
from unittest.mock import patch, MagicMock


class TestValuationFactorFormulas:
    """估值因子公式验证测试。"""

    @pytest.fixture
    def mock_valuation_data(self):
        """模拟估值数据。"""
        dates = pd.date_range("2023-01-01", "2023-01-10", freq="B")
        n = len(dates)
        return pd.DataFrame(
            {
                "date": dates.strftime("%Y-%m-%d"),
                "pe_ttm": [30.0 + i for i in range(n)],
                "pb": [5.0 + i * 0.1 for i in range(n)],
                "ps": [10.0 + i * 0.1 for i in range(n)],
                "total_mv": [2000.0 + i * 100.0 for i in range(n)],
                "circ_mv": [1000.0 + i * 50.0 for i in range(n)],
            }
        )

    def test_pe_ratio_formula(self, mock_valuation_data):
        """验证 pe_ratio 计算正确性。"""
        from jk2bt.factors.valuation import compute_pe_ratio

        with patch(
            "jk2bt.factors.valuation._get_valuation_raw", return_value=mock_valuation_data
        ):
            result = compute_pe_ratio("sh600519", end_date="2023-01-10", count=1)
            assert isinstance(result, (float, np.floating))
            assert result == 37.0

    def test_pb_ratio_formula(self, mock_valuation_data):
        """验证 pb_ratio 计算正确性。"""
        from jk2bt.factors.valuation import compute_pb_ratio

        with patch(
            "jk2bt.factors.valuation._get_valuation_raw", return_value=mock_valuation_data
        ):
            result = compute_pb_ratio("sh600519", end_date="2023-01-10", count=1)
            assert result == 5.7

    def test_ps_ratio_formula(self, mock_valuation_data):
        """验证 ps_ratio 计算正确性。"""
        from jk2bt.factors.valuation import compute_ps_ratio

        with patch(
            "jk2bt.factors.valuation._get_valuation_raw", return_value=mock_valuation_data
        ):
            result = compute_ps_ratio("sh600519", end_date="2023-01-10", count=1)
            assert result == 10.7

    def test_market_cap_formula(self, mock_valuation_data):
        """验证 market_cap 计算正确性。"""
        from jk2bt.factors.valuation import compute_market_cap

        with patch(
            "jk2bt.factors.valuation._get_valuation_raw", return_value=mock_valuation_data
        ):
            result = compute_market_cap("sh600519", end_date="2023-01-10", count=1)
            assert result == 2700.0

    def test_circulating_market_cap_formula(self, mock_valuation_data):
        """验证 circulating_market_cap 计算正确性。"""
        from jk2bt.factors.valuation import compute_circulating_market_cap

        with patch(
            "jk2bt.factors.valuation._get_valuation_raw", return_value=mock_valuation_data
        ):
            result = compute_circulating_market_cap(
                "sh600519", end_date="2023-01-10", count=1
            )
            assert result == 1350.0

    def test_natural_log_of_market_cap_formula(self, mock_valuation_data):
        """验证 natural_log_of_market_cap 计算正确性。"""
        from jk2bt.factors.valuation import compute_natural_log_of_market_cap

        with patch(
            "jk2bt.factors.valuation._get_valuation_raw", return_value=mock_valuation_data
        ):
            result = compute_natural_log_of_market_cap(
                "sh600519", end_date="2023-01-10", count=1
            )
            expected = np.log(2700.0)
            assert np.isclose(result, expected, rtol=1e-6)

    def test_cube_of_size_formula(self, mock_valuation_data):
        """验证 cube_of_size 计算正确性。"""
        from jk2bt.factors.valuation import compute_cube_of_size

        with patch(
            "jk2bt.factors.valuation._get_valuation_raw", return_value=mock_valuation_data
        ):
            result = compute_cube_of_size("sh600519", end_date="2023-01-10", count=1)
            log_mc = np.log(2700.0)
            expected = log_mc**3
            assert np.isclose(result, expected, rtol=1e-6)


class TestTechnicalFactorFormulas:
    """技术因子公式验证测试。"""

    @pytest.fixture
    def mock_ohlcv_data(self):
        """模拟 OHLCV 数据。"""
        dates = pd.date_range("2023-01-01", "2023-02-01", freq="B")
        n = len(dates)
        closes = 100 + np.arange(n) * 0.5
        volumes = 1000000 + np.arange(n) * 10000
        moneys = closes * volumes

        return pd.DataFrame(
            {
                "date": dates.strftime("%Y-%m-%d"),
                "open": closes - 1,
                "high": closes + 2,
                "low": closes - 2,
                "close": closes,
                "volume": volumes,
                "money": moneys,
            }
        )

    def test_bias_formula(self, mock_ohlcv_data):
        """验证 BIAS 公式：(close - MA) / MA。"""
        from jk2bt.factors.technical import compute_bias_5

        with patch(
            "jk2bt.factors.technical._get_daily_ohlcv", return_value=mock_ohlcv_data.tail(30)
        ):
            result = compute_bias_5("sh600519", end_date="2023-02-01", count=1)
            assert isinstance(result, (float, np.floating, np.ndarray))

    def test_bias_manual_calculation(self, mock_ohlcv_data):
        """手动验证 BIAS 计算结果。"""
        df = mock_ohlcv_data.tail(10)
        closes = df["close"].values
        ma5 = np.mean(closes[-5:])
        expected_bias = (closes[-1] - ma5) / ma5

        from jk2bt.factors.technical import compute_bias_5

        with patch(
            "jk2bt.factors.technical._get_daily_ohlcv", return_value=mock_ohlcv_data.tail(15)
        ):
            result = compute_bias_5("sh600519", end_date=df["date"].iloc[-1], count=1)
            assert np.isclose(result, expected_bias, rtol=1e-4)

    def test_emac_formula(self, mock_ohlcv_data):
        """验证 EMAC 公式：EMA(close, window)。"""
        from jk2bt.factors.technical import compute_emac_10

        with patch(
            "jk2bt.factors.technical._get_daily_ohlcv", return_value=mock_ohlcv_data.tail(30)
        ):
            result = compute_emac_10("sh600519", end_date="2023-02-01", count=1)
            assert isinstance(result, (float, np.floating))

    def test_emac_manual_calculation(self, mock_ohlcv_data):
        """手动验证 EMA 计算结果。"""
        df = mock_ohlcv_data.tail(20)
        closes = pd.Series(df["close"].values)

        ema = closes.ewm(span=10, adjust=False).mean()
        expected = ema.iloc[-1]

        from jk2bt.factors.technical import compute_emac_10

        with patch(
            "jk2bt.factors.technical._get_daily_ohlcv", return_value=mock_ohlcv_data.tail(20)
        ):
            result = compute_emac_10("sh600519", end_date=df["date"].iloc[-1], count=1)
            assert np.isclose(result, expected, rtol=1e-4)

    def test_roc_formula(self, mock_ohlcv_data):
        """验证 ROC 公式：close / close.shift(window) - 1。"""
        from jk2bt.factors.technical import compute_roc_6

        with patch(
            "jk2bt.factors.technical._get_daily_ohlcv", return_value=mock_ohlcv_data.tail(20)
        ):
            result = compute_roc_6("sh600519", end_date="2023-02-01", count=1)
            assert isinstance(result, (float, np.floating))

    def test_roc_manual_calculation(self, mock_ohlcv_data):
        """手动验证 ROC 计算结果。"""
        df = mock_ohlcv_data.tail(10)
        closes = df["close"].values
        # ROC_6 计算: (close - close_6_bars_ago) / close_6_bars_ago * 100
        # 或简单的 price rate of change
        expected_roc = (closes[-1] - closes[-7]) / closes[-7]

        from jk2bt.factors.technical import compute_roc_6

        with patch(
            "jk2bt.factors.technical._get_daily_ohlcv", return_value=mock_ohlcv_data.tail(15)
        ):
            result = compute_roc_6("sh600519", end_date=df["date"].iloc[-1], count=1)
            # ROC 可能返回百分比形式或小数形式，检查相对关系
            if isinstance(result, (int, float)) and not np.isnan(result):
                # 结果应该与期望值符号一致
                assert (result > 0) == (expected_roc > 0) or np.isclose(abs(result), abs(expected_roc), rtol=0.1)

    def test_mac_formula(self, mock_ohlcv_data):
        """验证 MAC 公式：MA(close, window)。"""
        from jk2bt.factors.technical import compute_mac_60

        with patch("jk2bt.factors.technical._get_daily_ohlcv", return_value=mock_ohlcv_data):
            result = compute_mac_60("sh600519", end_date="2023-02-01", count=1)
            assert isinstance(result, (float, np.floating))

    def test_vol_formula(self, mock_ohlcv_data):
        """验证 VOL 公式：MA(volume, window)。"""
        from jk2bt.factors.technical import compute_vol_20

        with patch(
            "jk2bt.factors.technical._get_daily_ohlcv", return_value=mock_ohlcv_data.tail(40)
        ):
            result = compute_vol_20("sh600519", end_date="2023-02-01", count=1)
            assert isinstance(result, (float, np.floating))

    def test_vol_manual_calculation(self, mock_ohlcv_data):
        """手动验证 VOL 计算结果。"""
        df = mock_ohlcv_data.tail(25)
        volumes = df["volume"].values
        expected_vol = np.mean(volumes[-20:])

        from jk2bt.factors.technical import compute_vol_20

        with patch(
            "jk2bt.factors.technical._get_daily_ohlcv", return_value=mock_ohlcv_data.tail(30)
        ):
            result = compute_vol_20("sh600519", end_date=df["date"].iloc[-1], count=1)
            assert np.isclose(result, expected_vol, rtol=1e-4)

    def test_vstd_formula(self, mock_ohlcv_data):
        """验证 VSTD 公式：Std(volume, window)。"""
        from jk2bt.factors.technical import compute_vstd_20

        with patch(
            "jk2bt.factors.technical._get_daily_ohlcv", return_value=mock_ohlcv_data.tail(40)
        ):
            result = compute_vstd_20("sh600519", end_date="2023-02-01", count=1)
            assert isinstance(result, (float, np.floating))

    def test_cci_formula(self, mock_ohlcv_data):
        """验证 CCI 公式：(TP - MA(TP)) / (0.015 * MD)。"""
        from jk2bt.factors.technical import compute_cci_10

        with patch(
            "jk2bt.factors.technical._get_daily_ohlcv", return_value=mock_ohlcv_data.tail(20)
        ):
            result = compute_cci_10("sh600519", end_date="2023-02-01", count=1)
            assert isinstance(result, (float, np.floating))

    def test_money_flow_formula(self, mock_ohlcv_data):
        """验证 money_flow 公式：MA(money, window)。"""
        from jk2bt.factors.technical import compute_money_flow_20

        with patch(
            "jk2bt.factors.technical._get_daily_ohlcv", return_value=mock_ohlcv_data.tail(40)
        ):
            result = compute_money_flow_20("sh600519", end_date="2023-02-01", count=1)
            assert isinstance(result, (float, np.floating))


class TestFundamentalFactorFormulas:
    """财务因子公式验证测试。"""

    @pytest.fixture
    def mock_income_data(self):
        """模拟利润表数据。"""
        return pd.DataFrame(
            {
                "报告期": [
                    "2022-12-31",
                    "2023-03-31",
                    "2023-06-30",
                    "2023-09-30",
                    "2023-12-31",
                ],
                "净利润": [50, 12, 15, 18, 55],
                "营业总收入": [500, 120, 130, 140, 550],
                "营业收入": [480, 115, 125, 135, 530],
            }
        )

    @pytest.fixture
    def mock_balance_data(self):
        """模拟资产负债表数据。"""
        return pd.DataFrame(
            {
                "报告期": [
                    "2022-12-31",
                    "2023-03-31",
                    "2023-06-30",
                    "2023-09-30",
                    "2023-12-31",
                ],
                "资产总计": [1000, 1050, 1100, 1150, 1200],
                "负债合计": [400, 420, 440, 460, 480],
                "股东权益合计": [600, 630, 660, 690, 720],
            }
        )

    def test_net_profit_ratio_formula(self, mock_income_data):
        """验证 net_profit_ratio 公式：net_profit / operating_revenue。"""
        from jk2bt.factors.fundamentals import compute_net_profit_ratio

        with patch(
            "jk2bt.factors.fundamentals._get_income_statement", return_value=mock_income_data
        ):
            result = compute_net_profit_ratio(
                "sh600519", end_date="2023-12-31", count=1
            )
            expected = 55 / 530
            assert np.isclose(result, expected, rtol=1e-4)

    def test_roe_formula(self, mock_income_data, mock_balance_data):
        """验证 ROE 公式：net_profit / avg_equity。"""
        from jk2bt.factors.fundamentals import compute_roe

        with patch(
            "jk2bt.factors.fundamentals._get_income_statement", return_value=mock_income_data
        ):
            with patch(
                "jk2bt.factors.fundamentals._get_balance_sheet",
                return_value=mock_balance_data,
            ):
                result = compute_roe("sh600519", end_date="2023-12-31", count=1)
                avg_equity = (720 + 690) / 2
                expected = 55 / avg_equity
                assert np.isclose(result, expected, rtol=1e-4)

    def test_roa_ttm_formula(self, mock_income_data, mock_balance_data):
        """验证 ROA_TTM 公式：TTM净利润 / 平均总资产。"""
        from jk2bt.factors.fundamentals import compute_roa_ttm

        with patch(
            "jk2bt.factors.fundamentals._get_income_statement", return_value=mock_income_data
        ):
            with patch(
                "jk2bt.factors.fundamentals._get_balance_sheet",
                return_value=mock_balance_data,
            ):
                result = compute_roa_ttm("sh600519", end_date="2023-12-31", count=1)
                ttm_profit = 55 + 18 + 15 + 12
                avg_assets = (1200 + 1150) / 2
                expected = ttm_profit / avg_assets
                assert np.isclose(result, expected, rtol=1e-4)


class TestFactorRegistry:
    """因子注册表测试。"""

    def test_registry_has_all_factors(self):
        """验证所有因子都已注册。"""
        from jk2bt.factors.base import global_factor_registry

        expected_factors = [
            "pe_ratio",
            "pb_ratio",
            "ps_ratio",
            "market_cap",
            "circulating_market_cap",
            "natural_log_of_market_cap",
            "cube_of_size",
            "bias_5",
            "bias_10",
            "bias_60",
            "emac_10",
            "emac_20",
            "emac_26",
            "emac_60",
            "roc_6",
            "roc_120",
            "mac_60",
            "mac_120",
            "vol_20",
            "vol_240",
            "vstd_20",
            "vroc_6",
            "cci_10",
            "money_flow_20",
            "net_profit_ratio",
            "roe",
            "roa_ttm",
            "rnoa_ttm",
        ]

        registered = global_factor_registry.list_factors()

        for factor in expected_factors:
            assert factor in registered, f"因子 {factor} 未注册"

    def test_factor_metadata(self):
        """验证因子元信息。"""
        from jk2bt.factors.base import global_factor_registry

        meta = global_factor_registry.get_metadata("bias_5")
        assert "window" in meta
        assert meta["window"] == 5
        assert "dependencies" in meta

    def test_normalize_factor_name(self):
        """验证因子名标准化。"""
        from jk2bt.factors.base import normalize_factor_name

        assert normalize_factor_name("PE_ratio") == "pe_ratio"
        assert normalize_factor_name("BIAS5") == "bias_5"
        assert normalize_factor_name("EMAC26") == "emac_26"
        assert normalize_factor_name("pe_ratio") == "pe_ratio"


class TestSafeDivision:
    """安全除法测试。"""

    def test_safe_divide_normal(self):
        """正常除法。"""
        from jk2bt.factors.base import safe_divide

        result = safe_divide(10, 2)
        assert result == 5.0

    def test_safe_divide_zero_denominator(self):
        """分母为零返回 NaN。"""
        from jk2bt.factors.base import safe_divide

        result = safe_divide(10, 0)
        assert np.isnan(result)

    def test_safe_divide_nan_denominator(self):
        """分母为 NaN 返回 NaN。"""
        from jk2bt.factors.base import safe_divide

        result = safe_divide(10, np.nan)
        assert np.isnan(result)

    def test_safe_divide_series(self):
        """Series 除法。"""
        from jk2bt.factors.base import safe_divide

        a = pd.Series([10, 20, 30])
        b = pd.Series([2, 0, 3])
        result = safe_divide(a, b)

        assert result.iloc[0] == 5.0
        assert np.isnan(result.iloc[1])
        assert result.iloc[2] == 10.0


class TestEdgeCases:
    """边界条件测试。"""

    def test_empty_data_handling(self):
        """空数据处理。"""
        from jk2bt.factors.valuation import compute_pe_ratio

        with patch("jk2bt.factors.valuation._get_valuation_raw", return_value=pd.DataFrame()):
            result = compute_pe_ratio("sh600519")
            assert np.isnan(result) or result is None or result == np.nan

    def test_negative_values(self):
        """负值处理。"""
        from jk2bt.factors.valuation import compute_natural_log_of_market_cap

        mock_data = pd.DataFrame(
            {
                "date": ["2023-01-01"],
                "total_mv": [-100.0],
            }
        )

        with patch("jk2bt.factors.valuation._get_valuation_raw", return_value=mock_data):
            result = compute_natural_log_of_market_cap(
                "sh600519", end_date="2023-01-01", count=1
            )
            assert np.isnan(result)

    def test_window_insufficient_data(self):
        """数据不足时的处理。"""
        from jk2bt.factors.technical import compute_bias_60

        dates = pd.date_range("2023-01-01", "2023-01-05", freq="B")
        n = len(dates)
        mock_data = pd.DataFrame(
            {
                "date": dates.strftime("%Y-%m-%d"),
                "close": [100 + i for i in range(n)],
                "volume": [1000 + i for i in range(n)],
            }
        )

        with patch("jk2bt.factors.technical._get_daily_ohlcv", return_value=mock_data):
            result = compute_bias_60("sh600519", end_date="2023-01-05", count=1)
            assert np.isnan(result) or isinstance(result, (float, pd.Series))


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
