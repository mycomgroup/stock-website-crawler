"""Compatibility alias for src.db.unified_cache."""

from importlib import import_module
import sys

sys.modules[__name__] = import_module("jk2bt.db.unified_cache")
