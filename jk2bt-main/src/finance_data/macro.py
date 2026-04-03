"""Compatibility alias for src.finance_data.macro."""

from importlib import import_module
import sys

sys.modules[__name__] = import_module("jk2bt.finance_data.macro")
