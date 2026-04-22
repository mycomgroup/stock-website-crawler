"""
Signals 模块 - 信号检测

信号是择时用的离散值，如金叉、死叉、突破、背离等。
"""

from .base import SignalBase, SignalDetector
from .cross import MACrossSignal, MACDSignal, RSISignal
from .breakthrough import BreakoutSignal, BollingerBreakoutSignal
from .divergence import RSIDivergenceSignal, MACDDivergenceSignal
from .extreme import KDJSignal, WRSignal, CCISignal
from .rsrs import RSSRSSignal, RSSRSIndexSignal

__all__ = [
    "SignalBase",
    "SignalDetector",
    "MACrossSignal",
    "MACDSignal",
    "RSISignal",
    "BreakoutSignal",
    "BollingerBreakoutSignal",
    "RSIDivergenceSignal",
    "MACDDivergenceSignal",
    "KDJSignal",
    "WRSignal",
    "CCISignal",
    "RSSRSSignal",
    "RSSRSIndexSignal",
]