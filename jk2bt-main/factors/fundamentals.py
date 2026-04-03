"""Compatibility alias for factors.fundamentals."""

from importlib import import_module
import sys

sys.modules[__name__] = import_module("jk2bt.factors.fundamentals")
