"""Compatibility alias for src.api.financial_indicator."""

from importlib import import_module
import sys

sys.modules[__name__] = import_module("jk2bt.api.financial_indicator")
