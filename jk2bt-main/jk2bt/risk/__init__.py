"""
risk 模块
风控模块 - 风险度量，仓位控制用。

模块结构：
- __init__.py       : 统一接口
- volatility.py     : 波动率风控
- drawdown.py       : 回撤风控
- position_sizing.py: 仓位计算

主要功能：
- 波动率计算与仓位调整
- 回撤监控与预警
- 凯利公式、风险平价等仓位计算方法
"""

from .volatility import (
    compute_volatility,
    compute_volatility_adjusted_position,
    compute_atr_based_stop_loss,
    detect_volatility_regime_change,
)

from .drawdown import (
    compute_max_drawdown,
    compute_drawdown,
    check_drawdown_alert,
    monitor_stock_drawdown,
    compute_recovery_time,
    compute_drawdown_statistics,
)

from .position_sizing import (
    kelly_criterion,
    risk_parity_position,
    equal_risk_contribution,
    volatility_target_position,
    atr_based_position_size,
    optimize_portfolio_positions,
)


__all__ = [
    # 波动率
    "compute_volatility",
    "compute_volatility_adjusted_position",
    "compute_atr_based_stop_loss",
    "detect_volatility_regime_change",
    # 回撤
    "compute_max_drawdown",
    "compute_drawdown",
    "check_drawdown_alert",
    "monitor_stock_drawdown",
    "compute_recovery_time",
    "compute_drawdown_statistics",
    # 仓位管理
    "kelly_criterion",
    "risk_parity_position",
    "equal_risk_contribution",
    "volatility_target_position",
    "atr_based_position_size",
    "optimize_portfolio_positions",
]