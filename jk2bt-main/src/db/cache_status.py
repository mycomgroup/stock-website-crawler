"""Compatibility alias for src.db.cache_status."""

from importlib import import_module
import sys

sys.modules[__name__] = import_module("jk2bt.db.cache_status")
