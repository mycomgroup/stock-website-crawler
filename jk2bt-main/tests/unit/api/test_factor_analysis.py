"""
tests/unit/api/test_factor_analysis.py
因子分析 API 单元测试

测试覆盖:
1. FactorAnalyzer - 因子分析器
2. analyze_factor - 单因子分析快捷函数
3. AttributionAnalysis - 归因分析
"""

import pytest
import pandas as pd
import numpy as np


def create_mock_factor_data(dates=None, stocks=None):
    if dates is None:
        dates = pd.date_range("2024-01-01", periods=10)
    if stocks is None:
        stocks = ["600519.XSHG", "000001.XSHE", "000002.XSHE"]

    data = {}
    for stock in stocks:
        data[stock] = np.random.randn(len(dates))

    return pd.DataFrame(data, index=dates)


def create_mock_price_data(dates=None, stocks=None):
    if dates is None:
        dates = pd.date_range("2024-01-01", periods=10)
    if stocks is None:
        stocks = ["600519.XSHG", "000001.XSHE", "000002.XSHE"]

    data = {}
    for stock in stocks:
        data[stock] = 100 + np.cumsum(np.random.randn(len(dates)) * 2)

    return pd.DataFrame(data, index=dates)


class TestFactorAnalyzer:
    """测试 FactorAnalyzer 类"""

    def test_init(self):
        from jk2bt.api.factor_analysis import FactorAnalyzer

        factor_data = create_mock_factor_data()
        price_data = create_mock_price_data()

        analyzer = FactorAnalyzer(factor_data, price_data)

        assert analyzer.factor_data is not None
        assert analyzer.price_data is not None
        assert analyzer.quantiles == 5
        assert 1 in analyzer.periods

    def test_ic_spearman(self):
        from jk2bt.api.factor_analysis import FactorAnalyzer

        factor_data = create_mock_factor_data()
        price_data = create_mock_price_data()

        analyzer = FactorAnalyzer(factor_data, price_data)

        ic = analyzer.ic(method="spearman")
        assert isinstance(ic, pd.Series)

    def test_ic_pearson(self):
        from jk2bt.api.factor_analysis import FactorAnalyzer

        factor_data = create_mock_factor_data()
        price_data = create_mock_price_data()

        analyzer = FactorAnalyzer(factor_data, price_data)

        ic = analyzer.ic(method="pearson")
        assert isinstance(ic, pd.Series)

    def test_mean_return_by_quantile(self):
        from jk2bt.api.factor_analysis import FactorAnalyzer

        factor_data = create_mock_factor_data()
        price_data = create_mock_price_data()

        analyzer = FactorAnalyzer(factor_data, price_data)

        returns = analyzer.mean_return_by_quantile()
        assert isinstance(returns, pd.Series)
        assert len(returns) <= 5

    def test_quantile_turnover(self):
        from jk2bt.api.factor_analysis import FactorAnalyzer

        factor_data = create_mock_factor_data()
        price_data = create_mock_price_data()

        analyzer = FactorAnalyzer(factor_data, price_data)

        turnover = analyzer.quantile_turnover(period=1)
        assert isinstance(turnover, pd.DataFrame)

    def test_cumulative_returns(self):
        from jk2bt.api.factor_analysis import FactorAnalyzer

        factor_data = create_mock_factor_data()
        price_data = create_mock_price_data()

        analyzer = FactorAnalyzer(factor_data, price_data)

        cum_ret = analyzer.cumulative_returns()
        assert isinstance(cum_ret, pd.DataFrame)

    def test_calc_autocorrelation(self):
        from jk2bt.api.factor_analysis import FactorAnalyzer

        factor_data = create_mock_factor_data()
        price_data = create_mock_price_data()

        analyzer = FactorAnalyzer(factor_data, price_data)

        autocorr = analyzer.calc_autocorrelation(lag=1)
        assert isinstance(autocorr, float)

    def test_summary(self):
        from jk2bt.api.factor_analysis import FactorAnalyzer

        factor_data = create_mock_factor_data()
        price_data = create_mock_price_data()

        analyzer = FactorAnalyzer(factor_data, price_data)

        summary = analyzer.summary()
        assert isinstance(summary, pd.DataFrame)


class TestAnalyzeFactor:
    """测试 analyze_factor 快捷函数"""

    def test_analyze_factor(self):
        from jk2bt.api.factor_analysis import analyze_factor

        factor_data = create_mock_factor_data()
        price_data = create_mock_price_data()

        result = analyze_factor(factor_data, price_data)

        assert isinstance(result, dict)
        assert "ic" in result
        assert "ic_mean" in result
        assert "returns" in result
        assert "turnover" in result
        assert "summary" in result

    def test_analyze_factor_with_quantiles(self):
        from jk2bt.api.factor_analysis import analyze_factor

        factor_data = create_mock_factor_data()
        price_data = create_mock_price_data()

        result = analyze_factor(factor_data, price_data, quantiles=3)

        assert isinstance(result, dict)
        assert len(result["returns"]) <= 3


class TestAttributionAnalysis:
    """测试 AttributionAnalysis 类"""

    def test_init(self):
        from jk2bt.api.factor_analysis import AttributionAnalysis

        portfolio_returns = pd.Series(
            [0.01, 0.02, -0.01, 0.03], index=pd.date_range("2024-01-01", periods=4)
        )
        factor_returns = pd.DataFrame(
            {
                "factor1": [0.01, 0.015, -0.005, 0.02],
                "factor2": [0.005, 0.01, 0.002, 0.015],
            },
            index=pd.date_range("2024-01-01", periods=4),
        )

        analyzer = AttributionAnalysis(portfolio_returns, factor_returns)

        assert analyzer.portfolio_returns is not None
        assert analyzer.factor_returns is not None

    def test_factor_exposure(self):
        from jk2bt.api.factor_analysis import AttributionAnalysis

        portfolio_returns = pd.Series(
            [0.01, 0.02, -0.01, 0.03], index=pd.date_range("2024-01-01", periods=4)
        )
        factor_returns = pd.DataFrame(
            {
                "factor1": [0.01, 0.015, -0.005, 0.02],
                "factor2": [0.005, 0.01, 0.002, 0.015],
            },
            index=pd.date_range("2024-01-01", periods=4),
        )

        analyzer = AttributionAnalysis(portfolio_returns, factor_returns)
        exposure = analyzer.factor_exposure()

        assert isinstance(exposure, pd.Series)

    def test_attribution(self):
        from jk2bt.api.factor_analysis import AttributionAnalysis

        portfolio_returns = pd.Series(
            [0.01, 0.02, -0.01, 0.03], index=pd.date_range("2024-01-01", periods=4)
        )
        factor_returns = pd.DataFrame(
            {
                "factor1": [0.01, 0.015, -0.005, 0.02],
                "factor2": [0.005, 0.01, 0.002, 0.015],
            },
            index=pd.date_range("2024-01-01", periods=4),
        )

        analyzer = AttributionAnalysis(portfolio_returns, factor_returns)
        attr = analyzer.attribution()

        assert isinstance(attr, pd.DataFrame)

    def test_summary(self):
        from jk2bt.api.factor_analysis import AttributionAnalysis

        portfolio_returns = pd.Series(
            [0.01, 0.02, -0.01, 0.03], index=pd.date_range("2024-01-01", periods=4)
        )
        factor_returns = pd.DataFrame(
            {
                "factor1": [0.01, 0.015, -0.005, 0.02],
                "factor2": [0.005, 0.01, 0.002, 0.015],
            },
            index=pd.date_range("2024-01-01", periods=4),
        )

        analyzer = AttributionAnalysis(portfolio_returns, factor_returns)
        summary = analyzer.summary()

        assert isinstance(summary, dict)
        assert "total_return" in summary
        assert "factor_contribution" in summary


class TestFactorAnalysisModuleExports:
    """测试模块导出"""

    def test_all_exports_exist(self):
        from jk2bt.api.factor_analysis import __all__

        expected = [
            "FactorAnalyzer",
            "analyze_factor",
            "AttributionAnalysis",
        ]

        for name in expected:
            assert name in __all__, f"{name} not in __all__"
