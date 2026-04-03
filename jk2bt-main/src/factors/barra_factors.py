"""Compatibility alias for src.factors.barra_factors."""

from importlib import import_module
import sys

sys.modules[__name__] = import_module("jk2bt.factors.barra_factors")
