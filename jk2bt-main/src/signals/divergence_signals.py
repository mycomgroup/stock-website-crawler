"""Compatibility alias for src.signals.divergence_signals."""

from importlib import import_module
import sys

sys.modules[__name__] = import_module("jk2bt.signals.divergence_signals")
