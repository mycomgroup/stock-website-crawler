"""Compatibility alias for finance_data.index_fundamentals_robust."""

from importlib import import_module
import sys

sys.modules[__name__] = import_module("jk2bt.finance_data.index_fundamentals_robust")
