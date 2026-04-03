"""Compatibility alias for src.api.stats."""

from importlib import import_module
import sys

sys.modules[__name__] = import_module("jk2bt.api.stats")
