"""Compatibility alias for src.signals.market_sentiment."""

from importlib import import_module
import sys

sys.modules[__name__] = import_module("jk2bt.signals.market_sentiment")
