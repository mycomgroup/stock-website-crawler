"""
test_risk.py
风险因子模块测试。

测试覆盖：
- get_factor_cov 计算因子协方差矩阵
- get_factor_variance 计算因子方差
- get_factor_correlation 计算因子相关性
- factor_risk_analysis 因子风险分析
- portfolio_factor_risk 组合因子风险
- rolling_factor_cov 滚动协方差
- eigenvalue_decomposition 特征值分解
"""

import warnings

warnings.filterwarnings("ignore")

import pytest
import pandas as pd
import numpy as np


@pytest.fixture
def sample_factor_returns():
    """生成模拟因子收益数据。"""
    np.random.seed(42)
    dates = pd.date_range("2023-01-01", periods=252, freq="B")

    return pd.DataFrame(
        {
            "factor1": np.random.randn(252) * 0.02,
            "factor2": np.random.randn(252) * 0.015,
            "factor3": np.random.randn(252) * 0.018,
        },
        index=dates,
    )


@pytest.fixture
def sample_cov_matrix():
    """生成模拟协方差矩阵。"""
    np.random.seed(42)
    return pd.DataFrame(
        np.array(
            [
                [0.0004, 0.0002, 0.0001],
                [0.0002, 0.000225, 0.00015],
                [0.0001, 0.00015, 0.000324],
            ]
        ),
        index=["factor1", "factor2", "factor3"],
        columns=["factor1", "factor2", "factor3"],
    )


class TestGetFactorCov:
    """测试因子协方差矩阵计算。"""

    def test_sample_cov(self, sample_factor_returns):
        """测试样本协方差。"""
        from jk2bt.analysis.factors.risk import get_factor_cov

        result = get_factor_cov(sample_factor_returns, method="sample")

        assert isinstance(result, pd.DataFrame)
        assert result.shape[0] == result.shape[1]
        assert result.shape[0] == sample_factor_returns.shape[1]

    def test_shrinkage_cov(self, sample_factor_returns):
        """测试压缩协方差。"""
        from jk2bt.analysis.factors.risk import get_factor_cov

        result = get_factor_cov(sample_factor_returns, method="shrinkage")

        assert isinstance(result, pd.DataFrame)
        assert result.shape[0] == result.shape[1]

    def test_ewma_cov(self, sample_factor_returns):
        """测试EWMA协方差。"""
        from jk2bt.analysis.factors.risk import get_factor_cov

        result = get_factor_cov(sample_factor_returns, method="ewma", halflife=20)

        assert isinstance(result, pd.DataFrame)
        assert result.shape[0] == result.shape[1]

    def test_cov_with_insufficient_data(self):
        """测试数据不足的情况。"""
        from jk2bt.analysis.factors.risk import get_factor_cov

        small_data = pd.DataFrame({"f1": [0.01], "f2": [0.02]})

        result = get_factor_cov(small_data)

        assert isinstance(result, pd.DataFrame)

    def test_cov_empty_data(self):
        """测试空数据。"""
        from jk2bt.analysis.factors.risk import get_factor_cov

        empty_data = pd.DataFrame()

        result = get_factor_cov(empty_data)

        assert result.empty


class TestGetFactorVariance:
    """测试因子方差计算。"""

    def test_variance_no_annualize(self, sample_factor_returns):
        """测试不年化的方差。"""
        from jk2bt.analysis.factors.risk import get_factor_variance

        result = get_factor_variance(sample_factor_returns, annualize=False)

        assert isinstance(result, pd.Series)
        assert len(result) == sample_factor_returns.shape[1]

    def test_variance_annualize(self, sample_factor_returns):
        """测试年化的方差。"""
        from jk2bt.analysis.factors.risk import get_factor_variance

        result = get_factor_variance(sample_factor_returns, annualize=True)

        assert isinstance(result, pd.Series)
        assert (result > 0).all()

    def test_variance_custom_periods(self, sample_factor_returns):
        """测试自定义周期数。"""
        from jk2bt.analysis.factors.risk import get_factor_variance

        result = get_factor_variance(
            sample_factor_returns, annualize=True, periods_per_year=52
        )

        assert isinstance(result, pd.Series)


class TestGetFactorCorrelation:
    """测试因子相关性计算。"""

    def test_pearson_correlation(self, sample_factor_returns):
        """测试Pearson相关性。"""
        from jk2bt.analysis.factors.risk import get_factor_correlation

        result = get_factor_correlation(sample_factor_returns, method="pearson")

        assert isinstance(result, pd.DataFrame)
        assert result.shape[0] == result.shape[1]

    def test_spearman_correlation(self, sample_factor_returns):
        """测试Spearman相关性。"""
        from jk2bt.analysis.factors.risk import get_factor_correlation

        result = get_factor_correlation(sample_factor_returns, method="spearman")

        assert isinstance(result, pd.DataFrame)
        assert result.shape[0] == result.shape[1]

    def test_correlation_diagonal(self, sample_factor_returns):
        """测试对角线为1。"""
        from jk2bt.analysis.factors.risk import get_factor_correlation

        result = get_factor_correlation(sample_factor_returns)

        assert (result.values.diagonal() == 1).all()


class TestFactorRiskAnalysis:
    """测试因子风险分析。"""

    def test_risk_analysis_no_weights(self, sample_factor_returns):
        """测试无组合权重的风险分析。"""
        from jk2bt.analysis.factors.risk import factor_risk_analysis

        result = factor_risk_analysis(sample_factor_returns)

        assert isinstance(result, pd.DataFrame)
        assert "variance" in result.columns
        assert "std" in result.columns

    def test_risk_analysis_with_weights(self, sample_factor_returns):
        """测试带组合权重的风险分析。"""
        from jk2bt.analysis.factors.risk import factor_risk_analysis

        weights = np.array([0.4, 0.3, 0.3])

        result = factor_risk_analysis(sample_factor_returns, portfolio_weights=weights)

        assert isinstance(result, pd.DataFrame)
        assert "variance" in result.columns
        assert "marginal_contribution" in result.columns
        assert "risk_contribution_pct" in result.columns


class TestPortfolioFactorRisk:
    """测试组合因子风险计算。"""

    def test_portfolio_risk_no_idiosyncratic(self, sample_cov_matrix):
        """测试无特质风险。"""
        from jk2bt.analysis.factors.risk import portfolio_factor_risk

        exposure = np.array([0.4, 0.3, 0.3])

        result = portfolio_factor_risk(exposure, sample_cov_matrix)

        assert isinstance(result, dict)
        assert "total_risk" in result
        assert "factor_risk" in result

    def test_portfolio_risk_with_idiosyncratic(self, sample_cov_matrix):
        """测试带特质风险。"""
        from jk2bt.analysis.factors.risk import portfolio_factor_risk

        exposure = np.array([0.4, 0.3, 0.3])

        result = portfolio_factor_risk(
            exposure, sample_cov_matrix, idiosyncratic_var=0.0001
        )

        assert isinstance(result, dict)
        assert "total_risk" in result
        assert "factor_risk" in result
        assert "idiosyncratic_risk" in result

    def test_portfolio_risk_percentage(self, sample_cov_matrix):
        """测试风险百分比。"""
        from jk2bt.analysis.factors.risk import portfolio_factor_risk

        exposure = np.array([0.4, 0.3, 0.3])

        result = portfolio_factor_risk(exposure, sample_cov_matrix)

        assert "factor_risk_pct" in result


class TestRollingFactorCov:
    """测试滚动协方差。"""

    def test_rolling_cov(self, sample_factor_returns):
        """测试滚动协方差。"""
        from jk2bt.analysis.factors.risk import rolling_factor_cov

        result = rolling_factor_cov(sample_factor_returns, window=60)

        assert isinstance(result, pd.DataFrame)

    def test_rolling_cov_insufficient_data(self):
        """测试数据少于窗口。"""
        from jk2bt.analysis.factors.risk import rolling_factor_cov

        small_data = pd.DataFrame(
            {
                "f1": np.random.randn(10) * 0.01,
                "f2": np.random.randn(10) * 0.01,
            }
        )

        result = rolling_factor_cov(small_data, window=60)

        assert isinstance(result, pd.DataFrame)


class TestEigenvalueDecomposition:
    """测试特征值分解。"""

    def test_eigenvalue_decomposition(self, sample_cov_matrix):
        """测试特征值分解。"""
        from jk2bt.analysis.factors.risk import eigenvalue_decomposition

        result = eigenvalue_decomposition(sample_cov_matrix)

        assert isinstance(result, dict)
        assert "eigenvalues" in result
        assert "eigenvectors" in result
        assert "explained_variance_ratio" in result

    def test_eigenvalue_decomposition_top_n(self, sample_cov_matrix):
        """测试截断特征值分解。"""
        from jk2bt.analysis.factors.risk import eigenvalue_decomposition

        result = eigenvalue_decomposition(sample_cov_matrix, top_n=2)

        assert isinstance(result, dict)
        assert len(result["eigenvalues"]) == 2

    def test_eigenvectors_dataframe(self, sample_cov_matrix):
        """测试特征向量是DataFrame。"""
        from jk2bt.analysis.factors.risk import eigenvalue_decomposition

        result = eigenvalue_decomposition(sample_cov_matrix)

        assert isinstance(result["eigenvectors"], pd.DataFrame)

    def test_explained_variance_ratio_sum(self, sample_cov_matrix):
        """测试解释方差比例和为1。"""
        from jk2bt.analysis.factors.risk import eigenvalue_decomposition

        result = eigenvalue_decomposition(sample_cov_matrix)

        assert abs(result["explained_variance_ratio"].sum() - 1.0) < 1e-10


class TestRiskModuleExport:
    """测试模块导出。"""

    def test_all_exports(self):
        """测试所有导出。"""
        from jk2bt.analysis.factors.risk import (
            get_factor_cov,
            get_factor_variance,
            get_factor_correlation,
            factor_risk_analysis,
            portfolio_factor_risk,
            rolling_factor_cov,
            eigenvalue_decomposition,
        )

        funcs = [
            get_factor_cov,
            get_factor_variance,
            get_factor_correlation,
            factor_risk_analysis,
            portfolio_factor_risk,
            rolling_factor_cov,
            eigenvalue_decomposition,
        ]

        for func in funcs:
            assert callable(func)
