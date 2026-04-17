"""
Tests for jk2bt/analysis/risk/position_sizing.py
"""

import numpy as np
import pytest
from unittest.mock import patch, MagicMock

from jk2bt.analysis.risk.position import (
    kelly_criterion,
    risk_parity_position,
    equal_risk_contribution,
    volatility_target_position,
    atr_based_position_size,
    optimize_portfolio_positions,
)


class TestKellyCriterion:
    """Tests for kelly_criterion function."""

    def test_positive_expectation(self):
        """win_rate=0.5, win_loss_ratio=2.0 should give positive kelly."""
        result = kelly_criterion(0.5, 2.0)
        assert result == pytest.approx(0.25)

    def test_negative_expectation(self):
        """win_rate=0.3, win_loss_ratio=1.0 should give negative (clamped to 0)."""
        result = kelly_criterion(0.3, 1.0)
        assert result == 0.0

    def test_win_rate_zero(self):
        """win_rate=0 should return 0."""
        assert kelly_criterion(0.0, 2.0) == 0.0

    def test_win_rate_one(self):
        """win_rate=1 should return 0 (boundary condition)."""
        assert kelly_criterion(1.0, 2.0) == 0.0

    def test_win_loss_ratio_zero(self):
        """win_loss_ratio=0 should return 0."""
        assert kelly_criterion(0.6, 0.0) == 0.0

    def test_win_loss_ratio_negative(self):
        """Negative win_loss_ratio should return 0."""
        assert kelly_criterion(0.6, -1.0) == 0.0

    def test_half_kelly(self):
        """fraction=0.5 should halve the kelly value."""
        full = kelly_criterion(0.6, 2.0)
        half = kelly_criterion(0.6, 2.0, fraction=0.5)
        assert half == pytest.approx(full * 0.5)

    def test_quarter_kelly(self):
        """fraction=0.25 should quarter the kelly value."""
        full = kelly_criterion(0.55, 1.5)
        quarter = kelly_criterion(0.55, 1.5, fraction=0.25)
        assert quarter == pytest.approx(full * 0.25)

    def test_high_win_rate_high_ratio(self):
        """High win rate and high ratio should give high kelly."""
        result = kelly_criterion(0.7, 3.0)
        expected = 0.7 - 0.3 / 3.0
        assert result == pytest.approx(expected)

    def test_clamped_to_one(self):
        """Kelly formula with fraction > 1 can exceed 1 and gets clamped."""
        result = kelly_criterion(0.8, 2.0, fraction=2.0)
        assert result == 1.0

    def test_edge_case_just_above_zero(self):
        """win_rate slightly above 0."""
        result = kelly_criterion(0.01, 100.0)
        assert result >= 0.0
        assert result <= 1.0

    def test_edge_case_just_below_one(self):
        """win_rate slightly below 1."""
        result = kelly_criterion(0.99, 100.0)
        assert result >= 0.0
        assert result <= 1.0

    def test_break_even_expectation(self):
        """win_rate=0.5, win_loss_ratio=1.0 should give 0."""
        result = kelly_criterion(0.5, 1.0)
        assert result == 0.0


class TestRiskParityPosition:
    """Tests for risk_parity_position function."""

    def test_empty_volatilities(self):
        """Empty dict should return empty dict."""
        assert risk_parity_position({}) == {}

    def test_equal_volatilities(self):
        """Equal volatilities should give equal positions."""
        vols = {"A": 0.2, "B": 0.2, "C": 0.2}
        result = risk_parity_position(vols)
        assert result["A"] == pytest.approx(1 / 3)
        assert result["B"] == pytest.approx(1 / 3)
        assert result["C"] == pytest.approx(1 / 3)

    def test_high_low_volatility_mix(self):
        """Low vol asset should get higher position."""
        vols = {"low_vol": 0.1, "high_vol": 0.3}
        result = risk_parity_position(vols)
        assert result["low_vol"] > result["high_vol"]

    def test_inverse_volatility_weighting(self):
        """Positions should be proportional to inverse volatility."""
        vols = {"A": 0.1, "B": 0.2}
        result = risk_parity_position(vols)
        inv_a = 1 / 0.1
        inv_b = 1 / 0.2
        total = inv_a + inv_b
        assert result["A"] == pytest.approx(inv_a / total)
        assert result["B"] == pytest.approx(inv_b / total)

    def test_zero_volatility(self):
        """Zero volatility should get 0 position."""
        vols = {"A": 0.0, "B": 0.2}
        result = risk_parity_position(vols)
        assert result["A"] == 0.0
        assert result["B"] == 1.0

    def test_all_zero_volatilities(self):
        """All zero volatilities should give equal positions."""
        vols = {"A": 0.0, "B": 0.0, "C": 0.0}
        result = risk_parity_position(vols)
        assert result["A"] == pytest.approx(1 / 3)
        assert result["B"] == pytest.approx(1 / 3)
        assert result["C"] == pytest.approx(1 / 3)

    def test_max_position_constraint(self):
        """Position should be capped at max_position."""
        vols = {"A": 0.05, "B": 0.5}
        result = risk_parity_position(vols, max_position=0.8)
        assert result["A"] <= 0.8
        assert result["B"] <= 0.8

    def test_single_asset(self):
        """Single asset should get full position."""
        vols = {"A": 0.2}
        result = risk_parity_position(vols)
        assert result["A"] == 1.0

    def test_negative_volatility(self):
        """Negative volatility treated as zero (1/vol would be negative)."""
        vols = {"A": -0.1, "B": 0.2}
        result = risk_parity_position(vols)
        assert result["A"] == 0.0
        assert result["B"] == 1.0


class TestEqualRiskContribution:
    """Tests for equal_risk_contribution function."""

    @patch("jk2bt.risk.position_sizing.compute_volatility")
    def test_normal_case(self, mock_compute_vol):
        """Normal case with valid volatilities."""
        mock_compute_vol.side_effect = (
            lambda symbol, **kwargs: 0.2 if symbol == "A" else 0.3
        )
        result = equal_risk_contribution(["A", "B"])
        assert "A" in result
        assert "B" in result
        assert result["A"] > result["B"]

    @patch("jk2bt.risk.position_sizing.compute_volatility")
    def test_empty_symbols(self, mock_compute_vol):
        """Empty symbols list should return empty dict."""
        result = equal_risk_contribution([])
        assert result == {}
        mock_compute_vol.assert_not_called()

    @patch("jk2bt.risk.position_sizing.compute_volatility")
    def test_all_volatility_failures(self, mock_compute_vol):
        """All volatility calculations fail should return equal weights."""
        mock_compute_vol.side_effect = Exception("API error")
        result = equal_risk_contribution(["A", "B", "C"])
        assert result["A"] == pytest.approx(1 / 3)
        assert result["B"] == pytest.approx(1 / 3)
        assert result["C"] == pytest.approx(1 / 3)

    @patch("jk2bt.risk.position_sizing.compute_volatility")
    def test_nan_volatility(self, mock_compute_vol):
        """NaN volatility should be treated as failure."""

        def mock_vol(symbol, **kwargs):
            return np.nan if symbol == "A" else 0.2

        mock_compute_vol.side_effect = mock_vol
        result = equal_risk_contribution(["A", "B"])
        assert "A" not in result
        assert "B" in result

    @patch("jk2bt.risk.position_sizing.compute_volatility")
    def test_passes_correct_parameters(self, mock_compute_vol):
        """Should pass correct parameters to compute_volatility."""
        mock_compute_vol.return_value = 0.2
        equal_risk_contribution(["A"], end_date="2024-01-01", force_update=True)
        mock_compute_vol.assert_called_once_with(
            "A",
            window=20,
            annualized=True,
            end_date="2024-01-01",
            force_update=True,
        )

    @patch("jk2bt.risk.position_sizing.compute_volatility")
    def test_partial_failures(self, mock_compute_vol):
        """Some symbols fail, others succeed."""

        def mock_vol(symbol, **kwargs):
            if symbol == "A":
                raise ValueError("Network error")
            return 0.25

        mock_compute_vol.side_effect = mock_vol
        result = equal_risk_contribution(["A", "B"])
        assert "A" not in result
        assert "B" in result
        assert result["B"] == 1.0


class TestVolatilityTargetPosition:
    """Tests for volatility_target_position function."""

    @patch("jk2bt.risk.volatility.compute_volatility_adjusted_position")
    def test_normal_case(self, mock_compute):
        """Normal case should return result from compute_volatility_adjusted_position."""
        mock_compute.return_value = {
            "adjusted_position": 0.8,
            "current_vol": 0.2,
            "target_vol": 0.15,
            "vol_ratio": 0.75,
        }
        result = volatility_target_position("A", target_vol=0.15, base_position=1.0)
        assert result["adjusted_position"] == 0.8
        assert result["current_vol"] == 0.2

    @patch("jk2bt.risk.volatility.compute_volatility_adjusted_position")
    def test_passes_correct_parameters(self, mock_compute):
        """Should pass correct parameters."""
        mock_compute.return_value = {
            "adjusted_position": 1.0,
            "current_vol": 0.2,
            "target_vol": 0.15,
            "vol_ratio": 0.75,
        }
        volatility_target_position(
            "000001.XSHE",
            target_vol=0.10,
            base_position=0.5,
            window=30,
            end_date="2024-06-01",
            force_update=True,
        )
        mock_compute.assert_called_once_with(
            "000001.XSHE",
            base_position=0.5,
            target_vol=0.10,
            window=30,
            end_date="2024-06-01",
            force_update=True,
        )

    @patch("jk2bt.risk.volatility.compute_volatility_adjusted_position")
    def test_default_parameters(self, mock_compute):
        """Should use default parameters."""
        mock_compute.return_value = {
            "adjusted_position": 1.0,
            "current_vol": 0.2,
            "target_vol": 0.15,
            "vol_ratio": 0.75,
        }
        volatility_target_position("A")
        mock_compute.assert_called_once_with(
            "A",
            base_position=1.0,
            target_vol=0.15,
            window=20,
            end_date=None,
            force_update=False,
        )
        mock_compute.assert_called_once_with(
            "000001.XSHE",
            base_position=0.5,
            target_vol=0.10,
            window=30,
            end_date="2024-06-01",
            force_update=True,
        )

    @patch("jk2bt.risk.volatility.compute_volatility_adjusted_position")
    def test_default_parameters(self, mock_compute):
        """Should use default parameters."""
        mock_compute.return_value = {
            "adjusted_position": 1.0,
            "current_vol": 0.2,
            "target_vol": 0.15,
            "vol_ratio": 0.75,
        }
        volatility_target_position("A")
        mock_compute.assert_called_once_with(
            "A",
            base_position=1.0,
            target_vol=0.15,
            window=20,
            end_date=None,
            force_update=False,
        )


class TestAtrBasedPositionSize:
    """Tests for atr_based_position_size function."""

    @patch("jk2bt.risk.volatility.compute_atr_based_stop_loss")
    def test_normal_case(self, mock_stop_loss):
        """Normal case with valid stop loss info."""
        mock_stop_loss.return_value = {
            "stop_loss_price": 9.0,
            "atr_value": 0.5,
            "risk_per_share": 1.0,
            "current_price": 10.0,
        }
        result = atr_based_position_size("A", total_capital=100000, risk_per_trade=0.02)
        assert result["symbol"] == "A"
        assert result["risk_amount"] == 2000.0
        assert result["shares"] == 2000
        assert result["position_value"] == 20000.0
        assert result["current_price"] == 10.0
        assert result["stop_loss_price"] == 9.0
        assert result["atr_value"] == 0.5

    @patch("jk2bt.risk.volatility.compute_atr_based_stop_loss")
    def test_nan_risk_per_share(self, mock_stop_loss):
        """NaN risk_per_share should return zero position."""
        mock_stop_loss.return_value = {
            "stop_loss_price": np.nan,
            "atr_value": np.nan,
            "risk_per_share": np.nan,
            "current_price": np.nan,
        }
        result = atr_based_position_size("A", total_capital=100000)
        assert result["shares"] == 0
        assert result["position_value"] == 0
        assert result["risk_amount"] == 0

    @patch("jk2bt.risk.volatility.compute_atr_based_stop_loss")
    def test_zero_risk_per_share(self, mock_stop_loss):
        """Zero risk_per_share should return zero position."""
        mock_stop_loss.return_value = {
            "stop_loss_price": 10.0,
            "atr_value": 0.0,
            "risk_per_share": 0.0,
            "current_price": 10.0,
        }
        result = atr_based_position_size("A", total_capital=100000)
        assert result["shares"] == 0
        assert result["position_value"] == 0
        assert result["risk_amount"] == 0

    @patch("jk2bt.risk.volatility.compute_atr_based_stop_loss")
    def test_negative_risk_per_share(self, mock_stop_loss):
        """Negative risk_per_share should return zero position."""
        mock_stop_loss.return_value = {
            "stop_loss_price": 11.0,
            "atr_value": 0.5,
            "risk_per_share": -1.0,
            "current_price": 10.0,
        }
        result = atr_based_position_size("A", total_capital=100000)
        assert result["shares"] == 0
        assert result["position_value"] == 0

    @patch("jk2bt.risk.volatility.compute_atr_based_stop_loss")
    def test_custom_atr_parameters(self, mock_stop_loss):
        """Should pass custom ATR parameters."""
        mock_stop_loss.return_value = {
            "stop_loss_price": 9.0,
            "atr_value": 0.5,
            "risk_per_share": 1.0,
            "current_price": 10.0,
        }
        atr_based_position_size(
            "A",
            total_capital=50000,
            risk_per_trade=0.01,
            atr_window=20,
            atr_multiplier=3.0,
            end_date="2024-03-01",
            force_update=True,
        )
        mock_stop_loss.assert_called_once_with(
            "A",
            atr_window=20,
            atr_multiplier=3.0,
            end_date="2024-03-01",
            force_update=True,
        )

    @patch("jk2bt.risk.volatility.compute_atr_based_stop_loss")
    def test_shares_is_integer(self, mock_stop_loss):
        """Shares should be integer (int() truncation)."""
        mock_stop_loss.return_value = {
            "stop_loss_price": 9.5,
            "atr_value": 0.25,
            "risk_per_share": 0.5,
            "current_price": 10.0,
        }
        result = atr_based_position_size("A", total_capital=100000, risk_per_trade=0.02)
        assert isinstance(result["shares"], int)
        assert result["shares"] == 4000


class TestOptimizePortfolioPositions:
    """Tests for optimize_portfolio_positions function."""

    @patch("jk2bt.risk.position_sizing.equal_risk_contribution")
    def test_equal_weight_method(self, mock_erc):
        """Equal weight method should give equal positions."""
        result = optimize_portfolio_positions(
            ["A", "B", "C"], total_capital=300000, method="equal_weight"
        )
        assert result["positions"]["A"] == pytest.approx(1 / 3)
        assert result["positions"]["B"] == pytest.approx(1 / 3)
        assert result["positions"]["C"] == pytest.approx(1 / 3)
        assert result["total_capital"] == 300000
        assert result["method"] == "equal_weight"
        mock_erc.assert_not_called()

    @patch("jk2bt.risk.position_sizing.equal_risk_contribution")
    def test_risk_parity_method(self, mock_erc):
        """Risk parity method should call equal_risk_contribution."""
        mock_erc.return_value = {"A": 0.6, "B": 0.4}
        result = optimize_portfolio_positions(
            ["A", "B"], total_capital=100000, method="risk_parity"
        )
        assert result["positions"] == {"A": 0.6, "B": 0.4}
        assert result["allocation"]["A"]["capital"] == 60000.0
        assert result["allocation"]["B"]["capital"] == 40000.0
        assert result["method"] == "risk_parity"
        mock_erc.assert_called_once_with(["A", "B"], end_date=None, force_update=False)

    @patch("jk2bt.risk.position_sizing.equal_risk_contribution")
    def test_unknown_method_defaults_to_equal_weight(self, mock_erc):
        """Unknown method should default to equal weight."""
        result = optimize_portfolio_positions(
            ["A", "B"], total_capital=100000, method="unknown"
        )
        assert result["positions"]["A"] == pytest.approx(0.5)
        assert result["positions"]["B"] == pytest.approx(0.5)
        mock_erc.assert_not_called()

    def test_empty_symbols(self):
        """Empty symbols should return empty positions."""
        result = optimize_portfolio_positions([], total_capital=100000)
        assert result["positions"] == {}
        assert result["total_capital"] == 100000

    @patch("jk2bt.risk.position_sizing.equal_risk_contribution")
    def test_allocation_structure(self, mock_erc):
        """Allocation should contain weight and capital for each symbol."""
        mock_erc.return_value = {"A": 0.3, "B": 0.7}
        result = optimize_portfolio_positions(
            ["A", "B"], total_capital=500000, method="risk_parity"
        )
        assert "allocation" in result
        assert result["allocation"]["A"]["weight"] == 0.3
        assert result["allocation"]["A"]["capital"] == 150000.0
        assert result["allocation"]["B"]["weight"] == 0.7
        assert result["allocation"]["B"]["capital"] == 350000.0

    @patch("jk2bt.risk.position_sizing.equal_risk_contribution")
    def test_passes_end_date_and_force_update(self, mock_erc):
        """Should pass end_date and force_update to equal_risk_contribution."""
        mock_erc.return_value = {"A": 1.0}
        optimize_portfolio_positions(
            ["A"],
            total_capital=100000,
            method="risk_parity",
            end_date="2024-12-31",
            force_update=True,
        )
        mock_erc.assert_called_once_with(
            ["A"],
            end_date="2024-12-31",
            force_update=True,
        )

    def test_single_asset_equal_weight(self):
        """Single asset should get full weight."""
        result = optimize_portfolio_positions(
            ["A"], total_capital=100000, method="equal_weight"
        )
        assert result["positions"]["A"] == 1.0
        assert result["allocation"]["A"]["capital"] == 100000.0
