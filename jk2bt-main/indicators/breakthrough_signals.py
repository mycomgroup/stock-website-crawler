"""Compatibility alias for indicators.breakthrough_signals."""

from importlib import import_module
import sys

sys.modules[__name__] = import_module("jk2bt.signals.breakthrough_signals")
