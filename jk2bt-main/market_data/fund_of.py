"""Compatibility alias for market_data.fund_of."""

from importlib import import_module
import sys

sys.modules[__name__] = import_module("jk2bt.market_data.fund_of")
