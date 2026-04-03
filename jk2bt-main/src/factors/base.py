"""Compatibility alias for src.factors.base."""

from importlib import import_module
import sys

sys.modules[__name__] = import_module("jk2bt.factors.base")
