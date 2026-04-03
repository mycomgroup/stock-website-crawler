"""Compatibility alias for src.api.factor_analysis."""

from importlib import import_module
import sys

sys.modules[__name__] = import_module("jk2bt.api.factor_analysis")
