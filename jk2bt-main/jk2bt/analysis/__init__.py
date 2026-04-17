"""
analysis - 策略分析层

包含因子计算、信号生成、风险管理
"""

# Factors
from jk2bt.analysis.factors import get_factor_values_jq, finance

# Signals
from jk2bt.analysis.signals import (
    compute_rsrs,
    compute_rsrs_signal,
    get_rsrs_for_index,
    get_current_rsrs_signal,
    compute_crowding_ratio,
    compute_gisi,
    compute_fed_model,
    compute_graham_index,
)

# Risk
from jk2bt.analysis.risk import (
    compute_volatility,
    compute_volatility_adjusted_position,
    compute_atr_based_stop_loss,
    compute_max_drawdown,
    check_drawdown_alert,
    kelly_criterion,
    risk_parity_position,
)

__all__ = [
    # Factors
    "get_factor_values_jq",
    "finance",
    # Signals
    "compute_rsrs",
    "compute_rsrs_signal",
    "get_rsrs_for_index",
    "get_current_rsrs_signal",
    "compute_crowding_ratio",
    "compute_gisi",
    "compute_fed_model",
    "compute_graham_index",
    # Risk
    "compute_volatility",
    "compute_volatility_adjusted_position",
    "compute_atr_based_stop_loss",
    "compute_max_drawdown",
    "check_drawdown_alert",
    "kelly_criterion",
    "risk_parity_position",
]
