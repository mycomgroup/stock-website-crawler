"""
tests/unit/api/test_order_api.py
订单 API 单元测试

测试覆盖:
1. order_shares - 按股数下单
2. order_target_percent - 按目标仓位百分比下单
3. LimitOrderStyle / MarketOrderStyle - 订单样式类
4. calculate_position_value - 计算持仓市值
5. get_position_ratio - 获取持仓比例
6. will_sell_on_limit_up / will_buy_on_limit_down - 涨跌停判断
7. rebalance_portfolio - 组合再平衡
8. get_portfolio_weights - 获取组合权重
"""

import pytest
import pandas as pd
import numpy as np
from unittest.mock import patch, MagicMock
import warnings

from jk2bt.api.order import (
    order_shares,
    order_target_percent,
    LimitOrderStyle,
    MarketOrderStyle,
    calculate_position_value,
    get_position_ratio,
    will_sell_on_limit_up,
    will_buy_on_limit_down,
    rebalance_portfolio,
    get_portfolio_weights,
)


class TestOrderStyles:
    """订单样式类测试"""

    def test_limit_order_style_init(self):
        style = LimitOrderStyle(limit_price=100.0)
        assert style.limit_price == 100.0

    def test_market_order_style_init(self):
        style = MarketOrderStyle()
        assert style is not None


class TestOrderFunctionsWithoutStrategy:
    """测试订单函数在无策略时的行为"""

    def test_order_shares_without_strategy(self):
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            result = order_shares("600519.XSHG", 100)
            assert result is None
            assert len(w) == 1
            assert "策略运行时" in str(w[0].message)

    def test_order_target_percent_without_strategy(self):
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            result = order_target_percent("600519.XSHG", 0.1)
            assert result is None
            assert len(w) == 1
            assert "策略运行时" in str(w[0].message)


class TestCalculatePositionValue:
    """测试计算持仓市值"""

    def test_calculate_position_value_without_strategy(self):
        result = calculate_position_value("600519.XSHG")
        assert result == 0

    @patch("jk2bt.api.order._current_strategy")
    @patch("jk2bt.api.order._get_cd")
    def test_calculate_position_value_with_strategy(self, mock_get_cd, mock_strategy):
        mock_position = MagicMock()
        mock_position.size = 100
        mock_strategy.getposition.return_value = mock_position

        mock_entry = MagicMock()
        mock_entry.last_price = 50.0
        mock_get_cd.return_value = {"600519.XSHG": mock_entry}

        result = calculate_position_value("600519.XSHG")
        assert result == 5000.0


class TestGetPositionRatio:
    """测试获取持仓比例"""

    def test_get_position_ratio_without_strategy(self):
        result = get_position_ratio("600519.XSHG")
        assert result == 0

    @patch("jk2bt.api.order._current_strategy")
    @patch("jk2bt.api.order.calculate_position_value")
    def test_get_position_ratio_with_strategy(self, mock_calc, mock_strategy):
        mock_broker = MagicMock()
        mock_broker.getvalue.return_value = 1000000.0
        mock_strategy.broker = mock_broker
        mock_strategy.context = MagicMock()
        mock_strategy.context.portfolio = MagicMock()
        mock_strategy.context.portfolio.positions = {"600519.XSHG": MagicMock()}

        mock_calc.return_value = 100000.0

        result = get_position_ratio("600519.XSHG")
        assert result == 0.1


class TestLimitUpDown:
    """测试涨跌停判断"""

    def test_will_sell_on_limit_up_without_strategy(self):
        result = will_sell_on_limit_up("600519.XSHG")
        assert result is False

    def test_will_buy_on_limit_down_without_strategy(self):
        result = will_buy_on_limit_down("600519.XSHG")
        assert result is False

    @patch("jk2bt.api.order._current_strategy")
    @patch("jk2bt.api.order._get_cd")
    def test_will_sell_on_limit_up_true(self, mock_get_cd, mock_strategy):
        mock_entry = MagicMock()
        mock_entry.last_price = 1150.0
        mock_entry.high_limit = 1150.0
        mock_get_cd.return_value = {"600519.XSHG": mock_entry}

        result = will_sell_on_limit_up("600519.XSHG")
        assert result is True

    @patch("jk2bt.api.order._current_strategy")
    @patch("jk2bt.api.order._get_cd")
    def test_will_sell_on_limit_up_false(self, mock_get_cd, mock_strategy):
        mock_entry = MagicMock()
        mock_entry.last_price = 1000.0
        mock_entry.high_limit = 1150.0
        mock_get_cd.return_value = {"600519.XSHG": mock_entry}

        result = will_sell_on_limit_up("600519.XSHG")
        assert result is False

    @patch("jk2bt.api.order._current_strategy")
    @patch("jk2bt.api.order._get_cd")
    def test_will_buy_on_limit_down_true(self, mock_get_cd, mock_strategy):
        mock_entry = MagicMock()
        mock_entry.last_price = 850.0
        mock_entry.low_limit = 850.0
        mock_get_cd.return_value = {"600519.XSHG": mock_entry}

        result = will_buy_on_limit_down("600519.XSHG")
        assert result is True

    @patch("jk2bt.api.order._current_strategy")
    @patch("jk2bt.api.order._get_cd")
    def test_will_buy_on_limit_down_false(self, mock_get_cd, mock_strategy):
        mock_entry = MagicMock()
        mock_entry.last_price = 1000.0
        mock_entry.low_limit = 850.0
        mock_get_cd.return_value = {"600519.XSHG": mock_entry}

        result = will_buy_on_limit_down("600519.XSHG")
        assert result is False


class TestRebalancePortfolio:
    """测试组合再平衡"""

    def test_rebalance_portfolio_without_strategy(self):
        target_weights = {"600519.XSHG": 0.1, "000001.XSHE": 0.2}
        rebalance_portfolio(target_weights)

    @patch("jk2bt.api.order._current_strategy")
    @patch("jk2bt.api.order.order_target_percent")
    def test_rebalance_portfolio_with_strategy(self, mock_order, mock_strategy):
        target_weights = {"600519.XSHG": 0.1, "000001.XSHE": 0.2}
        mock_strategy.context = MagicMock()
        mock_strategy.context.portfolio.positions = {}

        rebalance_portfolio(target_weights)

        assert mock_order.call_count == 2


class TestGetPortfolioWeights:
    """测试获取组合权重"""

    def test_get_portfolio_weights_without_strategy(self):
        result = get_portfolio_weights()
        assert result == {}

    @patch("jk2bt.api.order._current_strategy")
    def test_get_portfolio_weights_with_strategy(self, mock_strategy):
        mock_position = MagicMock()
        mock_position.size = 100
        mock_position.price = 50.0

        mock_broker = MagicMock()
        mock_broker.getvalue.return_value = 100000.0

        mock_strategy.broker = mock_broker
        mock_strategy.context = MagicMock()
        mock_strategy.context.portfolio.positions = {"600519.XSHG": mock_position}

        result = get_portfolio_weights()
        assert "600519.XSHG" in result
        assert result["600519.XSHG"] == pytest.approx(0.05)


class TestOrderModuleExports:
    """测试模块导出"""

    def test_all_exports_exist(self):
        from jk2bt.api.order import __all__

        expected = [
            "order_shares",
            "order_target_percent",
            "LimitOrderStyle",
            "MarketOrderStyle",
            "rebalance_portfolio",
            "get_portfolio_weights",
            "calculate_position_value",
            "get_position_ratio",
            "will_sell_on_limit_up",
            "will_buy_on_limit_down",
        ]

        for name in expected:
            assert name in __all__, f"{name} not in __all__"
