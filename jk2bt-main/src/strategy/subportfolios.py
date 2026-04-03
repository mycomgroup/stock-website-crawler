"""Compatibility alias for src.strategy.subportfolios."""

from importlib import import_module
import sys

sys.modules[__name__] = import_module("jk2bt.strategy.subportfolios")
