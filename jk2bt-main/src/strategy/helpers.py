"""Compatibility alias for src.strategy.helpers."""

from importlib import import_module
import sys

sys.modules[__name__] = import_module("jk2bt.strategy.helpers")
