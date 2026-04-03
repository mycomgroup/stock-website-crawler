"""Compatibility alias for src.risk.volatility."""

from importlib import import_module
import sys

sys.modules[__name__] = import_module("jk2bt.risk.volatility")
