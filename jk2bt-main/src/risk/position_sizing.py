"""Compatibility alias for src.risk.position_sizing."""

from importlib import import_module
import sys

sys.modules[__name__] = import_module("jk2bt.risk.position_sizing")
