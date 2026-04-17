"""
test_helpers.py
helpers.py 单元测试

测试场景覆盖:
1. calculate_ma 移动平均线
2. calculate_ema 指数移动平均线
3. calculate_std 标准差
4. calculate_boll 布林线
5. calculate_rsi RSI指标
6. calculate_macd MACD指标
7. calculate_kdj KDJ指标
8. calculate_atr ATR指标
9. normalize_data 数据标准化
10. winsorize 数据去极值
11. calculate_sharpe 夏普比率
12. calculate_max_drawdown 最大回撤
13. calculate_drawdown_duration 回撤持续时间
14. calculate_volatility 波动率
15. calculate_return_series 收益率序列
16. calculate_cumulative_return 累计收益率
17. calculate_annualized_return 年化收益率
18. calculate_position_concentration 持仓集中度
19. calculate_diversification_index 分散度指数
20. calculate_portfolio_beta 组合Beta
21. calculate_tracking_error 跟踪误差
"""

import pytest
import pandas as pd
import numpy as np
from jk2bt.engine.helpers import (
    calculate_ma,
    calculate_ema,
    calculate_std,
    calculate_boll,
    calculate_rsi,
    calculate_macd,
    calculate_kdj,
    calculate_atr,
    normalize_data,
    winsorize,
    calculate_sharpe,
    calculate_max_drawdown,
    calculate_drawdown_duration,
    calculate_volatility,
    calculate_return_series,
    calculate_cumulative_return,
    calculate_annualized_return,
    calculate_position_concentration,
    calculate_diversification_index,
    calculate_portfolio_beta,
    calculate_tracking_error,
)


class TestCalculateMA:
    """测试 calculate_ma 移动平均线"""

    def test_ma_basic(self):
        """测试基本计算"""
        prices = [10, 20, 30, 40, 50]
        result = calculate_ma(prices, window=3)
        assert len(result) == 5
        assert pd.isna(result.iloc[0])
        assert pd.isna(result.iloc[1])
        assert result.iloc[2] == 20.0

    def test_ma_with_series(self):
        """测试Series输入"""
        prices = pd.Series([10, 20, 30, 40, 50])
        result = calculate_ma(prices, window=3)
        assert isinstance(result, pd.Series)

    def test_ma_window_larger_than_data(self):
        """测试窗口大于数据长度"""
        prices = [1, 2]
        result = calculate_ma(prices, window=5)
        assert all(pd.isna(result))


class TestCalculateEMA:
    """测试 calculate_ema 指数移动平均线"""

    def test_ema_basic(self):
        """测试基本计算"""
        prices = [10, 20, 30, 40, 50]
        result = calculate_ema(prices, span=3)
        assert len(result) == 5
        assert not pd.isna(result.iloc[-1])

    def test_ema_with_series(self):
        """测试Series输入"""
        prices = pd.Series([10.0, 20.0, 30.0])
        result = calculate_ema(prices, span=2)
        assert isinstance(result, pd.Series)


class TestCalculateStd:
    """测试 calculate_std 标准差"""

    def test_std_basic(self):
        """测试基本计算"""
        prices = [1, 2, 3, 4, 5]
        result = calculate_std(prices, window=3)
        assert len(result) == 5


class TestCalculateBoll:
    """测试 calculate_boll 布林线"""

    def test_boll_returns_dict(self):
        """测试返回字典"""
        prices = [10, 20, 30, 40, 50, 60, 70]
        result = calculate_boll(prices)
        assert isinstance(result, dict)
        assert "upper" in result
        assert "middle" in result
        assert "lower" in result

    def test_boll_upper_greater_than_lower(self):
        """测试上轨大于下轨"""
        prices = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
        result = calculate_boll(prices, window=5)
        assert result["upper"].iloc[-1] > result["lower"].iloc[-1]

    def test_boll_custom_parameters(self):
        """测试自定义参数"""
        prices = [10, 20, 30, 40, 50]
        result = calculate_boll(prices, window=3, num_std=3)
        assert isinstance(result, dict)


class TestCalculateRSI:
    """测试 calculate_rsi RSI指标"""

    def test_rsi_basic(self):
        """测试基本计算"""
        prices = [10, 15, 12, 18, 20, 17, 22, 25, 23, 28]
        result = calculate_rsi(prices)
        assert len(result) == len(prices)

    def test_rsi_range(self):
        """测试RSI范围"""
        prices = list(range(1, 50))
        result = calculate_rsi(prices)
        valid_values = result.dropna()
        assert all((valid_values >= 0) & (valid_values <= 100))


class TestCalculateMACD:
    """测试 calculate_macd MACD指标"""

    def test_macd_returns_dict(self):
        """测试返回字典"""
        prices = [10, 15, 12, 18, 20, 17, 22, 25, 23, 28]
        result = calculate_macd(prices)
        assert isinstance(result, dict)
        assert "macd" in result
        assert "signal" in result
        assert "hist" in result

    def test_macd_histogram_calculation(self):
        """测试柱状图计算"""
        prices = list(range(1, 50))
        result = calculate_macd(prices)
        result["hist"] = result["macd"] - result["signal"]


class TestCalculateKDJ:
    """测试 calculate_kdj KDJ指标"""

    def test_kdj_returns_dict(self):
        """测试返回字典"""
        highs = [10, 15, 12, 18, 20]
        lows = [8, 12, 10, 14, 16]
        closes = [9, 14, 11, 16, 18]
        result = calculate_kdj(highs, lows, closes)
        assert isinstance(result, dict)
        assert "k" in result
        assert "d" in result
        assert "j" in result

    def test_kdj_custom_parameters(self):
        """测试自定义参数"""
        highs = [10, 15, 12, 18, 20, 22, 25]
        lows = [8, 12, 10, 14, 16, 18, 20]
        closes = [9, 14, 11, 16, 18, 20, 23]
        result = calculate_kdj(highs, lows, closes, n=3, m=2)
        assert isinstance(result, dict)


class TestCalculateATR:
    """测试 calculate_atr ATR指标"""

    def test_atr_basic(self):
        """测试基本计算"""
        highs = [10, 12, 11, 13, 15]
        lows = [8, 10, 9, 11, 13]
        closes = [9, 11, 10, 12, 14]
        result = calculate_atr(highs, lows, closes)
        assert len(result) == len(closes)

    def test_atr_positive(self):
        """测试ATR为正"""
        highs = [10, 12, 11, 13, 15, 14, 16]
        lows = [8, 10, 9, 11, 13, 12, 14]
        closes = [9, 11, 10, 12, 14, 13, 15]
        result = calculate_atr(highs, lows, closes)
        valid_values = result.dropna()
        assert all(valid_values > 0)


class TestNormalizeData:
    """测试 normalize_data 数据标准化"""

    def test_zscore_normalization(self):
        """测试zscore标准化"""
        data = [1, 2, 3, 4, 5]
        result = normalize_data(data, method="zscore")
        assert len(result) == len(data)

    def test_minmax_normalization(self):
        """测试minmax标准化"""
        data = [1, 2, 3, 4, 5]
        result = normalize_data(data, method="minmax")
        assert result.min() == 0.0
        assert result.max() == 1.0

    def test_rank_normalization(self):
        """测试rank标准化"""
        data = [3, 1, 2, 5, 4]
        result = normalize_data(data, method="rank")
        assert len(result) == len(data)

    def test_unknown_method_returns_original(self):
        """测试未知方法返回原数据"""
        data = [1, 2, 3]
        result = normalize_data(data, method="unknown")
        assert len(result) == len(data)


class TestWinsorize:
    """测试 winsorize 数据去极值"""

    def test_winsorize_basic(self):
        """测试基本功能"""
        data = list(range(1, 101))
        result = winsorize(data)
        assert len(result) == len(data)

    def test_winsorize_reduces_extremes(self):
        """测试去极值效果"""
        data = [1, 2, 3, 4, 5, 100]
        result = winsorize(data, lower=0.05, upper=0.95)
        assert result.iloc[-1] < 100


class TestCalculateSharpe:
    """测试 calculate_sharpe 夏普比率"""

    def test_sharpe_basic(self):
        """测试基本计算"""
        returns = [0.01, 0.02, -0.01, 0.03, 0.02]
        result = calculate_sharpe(returns)
        assert isinstance(result, (int, float))

    def test_sharpe_zero_std(self):
        """测试标准差为零时返回0"""
        returns = [0, 0, 0, 0]
        result = calculate_sharpe(returns)
        assert result == 0

    def test_sharpe_with_risk_free(self):
        """测试带无风险利率"""
        returns = [0.01, 0.02, 0.01]
        result = calculate_sharpe(returns, risk_free_rate=0.01)
        assert isinstance(result, (int, float))


class TestCalculateMaxDrawdown:
    """测试 calculate_max_drawdown 最大回撤"""

    def test_max_drawdown_basic(self):
        """测试基本计算"""
        values = [100, 110, 105, 95, 90, 100, 105]
        result = calculate_max_drawdown(values)
        assert isinstance(result, (int, float))
        assert result < 0

    def test_max_drawdown_increasing(self):
        """测试持续上涨无回撤"""
        values = [100, 105, 110, 115, 120]
        result = calculate_max_drawdown(values)
        assert result == 0


class TestCalculateDrawdownDuration:
    """测试 calculate_drawdown_duration 回撤持续时间"""

    def test_duration_basic(self):
        """测试基本计算"""
        values = [100, 110, 105, 95, 90, 100, 105]
        result = calculate_drawdown_duration(values)
        assert isinstance(result, int)
        assert result >= 0

    def test_duration_no_drawdown(self):
        """测试无回撤时返回0"""
        values = [100, 105, 110, 115]
        result = calculate_drawdown_duration(values)
        assert result == 0


class TestCalculateVolatility:
    """测试 calculate_volatility 波动率"""

    def test_volatility_basic(self):
        """测试基本计算"""
        returns = [0.01, -0.02, 0.01, 0.03, -0.01]
        result = calculate_volatility(returns)
        assert len(result) == len(returns)

    def test_volatility_positive(self):
        """测试波动率为正"""
        returns = [0.01, 0.02, 0.01, 0.02, 0.01]
        result = calculate_volatility(returns)
        valid_values = result.dropna()
        assert all(valid_values > 0)


class TestCalculateReturnSeries:
    """测试 calculate_return_series 收益率序列"""

    def test_return_series_basic(self):
        """测试基本计算"""
        values = [100, 110, 105, 115, 120]
        result = calculate_return_series(values)
        assert len(result) == len(values)
        assert result.iloc[0] == 0

    def test_return_series_calculation(self):
        """测试收益率计算"""
        values = [100, 110, 121]
        result = calculate_return_series(values)
        assert result.iloc[1] == pytest.approx(0.10, rel=1e-3)


class TestCalculateCumulativeReturn:
    """测试 calculate_cumulative_return 累计收益率"""

    def test_cumulative_return_basic(self):
        """测试基本计算"""
        values = [100, 110, 121]
        result = calculate_cumulative_return(values)
        assert result == pytest.approx(0.21, rel=1e-3)

    def test_cumulative_return_single_value(self):
        """测试单值返回0"""
        values = [100]
        result = calculate_cumulative_return(values)
        assert result == 0


class TestCalculateAnnualizedReturn:
    """测试 calculate_annualized_return 年化收益率"""

    def test_annualized_basic(self):
        """测试基本计算"""
        values = [100, 110]
        result = calculate_annualized_return(values)
        assert isinstance(result, (int, float))

    def test_annualized_single_value(self):
        """测试单值返回0"""
        values = [100]
        result = calculate_annualized_return(values)
        assert result == 0


class TestCalculatePositionConcentration:
    """测试 calculate_position_concentration 持仓集中度"""

    def test_concentration_basic(self):
        """测试基本计算"""
        weights = {"600519": 0.3, "000858": 0.7}
        result = calculate_position_concentration(weights)
        assert result == 0.7

    def test_concentration_empty(self):
        """测试空持仓返回0"""
        result = calculate_position_concentration({})
        assert result == 0

    def test_concentration_single_stock(self):
        """测试单只股票"""
        weights = {"600519": 1.0}
        result = calculate_position_concentration(weights)
        assert result == 1.0


class TestCalculateDiversificationIndex:
    """测试 calculate_diversification_index 分散度指数"""

    def test_diversification_basic(self):
        """测试基本计算"""
        weights = {"600519": 0.5, "000858": 0.5}
        result = calculate_diversification_index(weights)
        assert result == 2.0

    def test_diversification_empty(self):
        """测试空持仓返回0"""
        result = calculate_diversification_index({})
        assert result == 0

    def test_diversification_single(self):
        """测试单只股票"""
        weights = {"600519": 1.0}
        result = calculate_diversification_index(weights)
        assert result == 1.0


class TestCalculatePortfolioBeta:
    """测试 calculate_portfolio_beta 组合Beta"""

    def test_beta_basic(self):
        """测试基本计算"""
        portfolio_returns = [0.01, 0.02, 0.015, 0.025]
        benchmark_returns = [0.008, 0.012, 0.01, 0.015]
        result = calculate_portfolio_beta(portfolio_returns, benchmark_returns)
        assert isinstance(result, (int, float))

    def test_beta_zero_variance(self):
        """测试基准方差为零时返回0"""
        portfolio_returns = [0.01, 0.02, 0.015]
        benchmark_returns = [0.01, 0.01, 0.01]
        result = calculate_portfolio_beta(portfolio_returns, benchmark_returns)
        assert result == 0


class TestCalculateTrackingError:
    """测试 calculate_tracking_error 跟踪误差"""

    def test_tracking_error_basic(self):
        """测试基本计算"""
        portfolio_returns = [0.01, 0.02, 0.015, 0.025]
        benchmark_returns = [0.008, 0.012, 0.01, 0.015]
        result = calculate_tracking_error(portfolio_returns, benchmark_returns)
        assert isinstance(result, (int, float))
        assert result >= 0

    def test_tracking_error_zero(self):
        """测试完全跟踪时返回0"""
        returns = [0.01, 0.02, 0.015]
        result = calculate_tracking_error(returns, returns)
        assert result == 0
