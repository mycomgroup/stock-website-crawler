"""Compatibility alias for finance_data.share_change."""

from importlib import import_module
import sys

sys.modules[__name__] = import_module("jk2bt.finance_data.share_change")
