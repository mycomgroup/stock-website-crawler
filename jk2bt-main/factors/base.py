"""Compatibility alias for factors.base."""

from importlib import import_module
import sys

sys.modules[__name__] = import_module("jk2bt.factors.base")
