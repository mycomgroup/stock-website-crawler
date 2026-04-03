"""Compatibility alias for src.strategy.timer_rules."""

from importlib import import_module
import sys

sys.modules[__name__] = import_module("jk2bt.strategy.timer_rules")
