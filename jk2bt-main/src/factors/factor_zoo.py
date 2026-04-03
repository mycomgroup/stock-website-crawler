"""Compatibility alias for src.factors.factor_zoo."""

from importlib import import_module
import sys

sys.modules[__name__] = import_module("jk2bt.factors.factor_zoo")
