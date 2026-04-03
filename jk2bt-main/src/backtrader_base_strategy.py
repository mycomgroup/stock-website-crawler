"""Compatibility alias for src.backtrader_base_strategy."""

from importlib import import_module
import sys

sys.modules[__name__] = import_module("jk2bt.core.strategy_base")
