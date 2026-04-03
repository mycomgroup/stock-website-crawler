"""Compatibility alias for src.market_data.conversion_bond."""

from importlib import import_module
import sys

sys.modules[__name__] = import_module("jk2bt.market_data.conversion_bond")
