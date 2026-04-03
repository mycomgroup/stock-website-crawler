"""Compatibility alias for finance_data.shareholder."""

from importlib import import_module
import sys

sys.modules[__name__] = import_module("jk2bt.finance_data.shareholder")
