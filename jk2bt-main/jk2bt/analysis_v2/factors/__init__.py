"""
Factors 模块 - 因子计算

因子是选股用的连续值指标，如 PE、PB、动量、波动率等。
"""

from .base import FactorBase, FactorRegistry, compute_factor, compute_factors
from .technical import (
    MA5Factor, MA10Factor, MA20Factor,
    EMA12Factor, EMA26Factor,
    MACDFactor, RSI6Factor, RSI14Factor,
    KDJFactor, BollFactor, ATR14Factor,
    BIAS6Factor, BIAS12Factor, BIAS24Factor,
    ROC12Factor, Momentum10Factor, OBVFactor,
    Volatility20Factor, ADX14Factor, MFI14Factor,
)

__all__ = [
    "FactorBase",
    "FactorRegistry",
    "compute_factor",
    "compute_factors",
    "MA5Factor",
    "MA10Factor",
    "MA20Factor",
    "EMA12Factor",
    "EMA26Factor",
    "MACDFactor",
    "RSI6Factor",
    "RSI14Factor",
    "KDJFactor",
    "BollFactor",
    "ATR14Factor",
    "BIAS6Factor",
    "BIAS12Factor",
    "BIAS24Factor",
    "ROC12Factor",
    "Momentum10Factor",
    "OBVFactor",
    "Volatility20Factor",
    "ADX14Factor",
    "MFI14Factor",
]