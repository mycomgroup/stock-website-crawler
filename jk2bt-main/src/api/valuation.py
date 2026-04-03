"""Compatibility alias for src.api.valuation."""

from importlib import import_module
import sys

sys.modules[__name__] = import_module("jk2bt.api.valuation")
