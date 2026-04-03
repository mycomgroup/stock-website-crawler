"""Compatibility alias for src.factors.qlib_alpha."""

from importlib import import_module
import sys

sys.modules[__name__] = import_module("jk2bt.factors.qlib_alpha")
