"""Compatibility alias for src.risk.drawdown."""

from importlib import import_module
import sys

sys.modules[__name__] = import_module("jk2bt.risk.drawdown")
