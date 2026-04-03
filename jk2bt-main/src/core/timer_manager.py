"""Compatibility alias for src.core.timer_manager."""

from importlib import import_module
import sys

sys.modules[__name__] = import_module("jk2bt.core.timer_manager")
