"""Compatibility alias for src.signals.fields."""

from importlib import import_module
import sys

sys.modules[__name__] = import_module("jk2bt.signals.fields")
