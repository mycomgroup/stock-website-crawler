"""Compatibility alias for src.core.strategy_wrapper."""

from importlib import import_module
import sys

sys.modules[__name__] = import_module("jk2bt.core.strategy_wrapper")
